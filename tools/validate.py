#!/usr/bin/env python3
"""Validate STEW declarations against the STEW JSON Schemas. Standard library only.

    python tools/validate.py examples/
    python tools/validate.py path/to/one.us path/to/ledger.jsonl
    python tools/validate.py --expect-fail conformance/invalid/

Reads every .us file (Markdown with exactly one ```json block) and every .jsonl
ledger (one record per line) under the paths given, and checks:

  1. the declaration against its kind's schema (schema/<version>/<kind>.schema.json),
     with the subset of JSON Schema 2020-12 the STEW schemas use;
  2. the rules the schemas cannot say: a profile's instructions are at most 8
     lines; a task, an eval case and a board name only profiles that exist in
     the paths given; a ledger's seq runs from 1 with no gap, each prev is the
     sha256 of the line before, and each state change is one the lifecycle allows;
  3. portability: no absolute path, drive letter or home directory in any value,
     and nothing shaped like a secret.

Exit status 0 when everything passes, 1 otherwise. Every failure names the file.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urldefrag

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
KINDS = ("profile", "task", "board", "eval", "record")
BLOCK_RE = re.compile(r"^```json[ \t]*\n(.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)
MAX_INSTRUCTION_LINES = 8

# The lifecycle (spec/lifecycle.md): every allowed change of state.
TRANSITIONS = {
    "submitted": {"claimed", "canceled", "rejected"},
    "claimed": {"submitted", "working", "canceled", "rejected"},
    "working": {"input-required", "completed", "failed", "canceled"},
    "input-required": {"working", "failed", "canceled"},
    "completed": {"reported"},
    "failed": {"reported"},
    "canceled": {"reported"},
    "rejected": {"reported"},
    "reported": {"unloaded"},
    "unloaded": set(),
}

# Portability and secrets (spec/security.md, spec/portability.md).
HOST_PATH_RE = re.compile(r"(^|[\s\"'(=])([A-Za-z]:[\\/]|\\\\[A-Za-z0-9]|/(Users|home|root)/|~[\\/])")
SECRET_RE = re.compile(
    r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|\bsk-[A-Za-z0-9_-]{16,}|\bghp_[A-Za-z0-9]{20,}"
    r"|\bgithub_pat_[A-Za-z0-9_]{20,}|\bxox[abp]-[A-Za-z0-9-]{10,}|\bAKIA[0-9A-Z]{16}\b"
    r"|\b[0-9]{8,10}:[A-Za-z0-9_-]{35}\b)"
)


# --- a small JSON Schema 2020-12 evaluator (the keywords the STEW schemas use) ---

class Schemas:
    def __init__(self, version_dir: Path):
        self.by_id: dict[str, dict] = {}
        for path in sorted(version_dir.glob("*.schema.json")):
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.by_id[schema["$id"]] = schema
        self.by_kind = {}
        for sid, schema in self.by_id.items():
            name = sid.rsplit("/", 1)[-1].split(".")[0]
            if name in KINDS:
                self.by_kind[name] = (sid, schema)

    def resolve(self, base: str, ref: str) -> tuple[str, dict]:
        url, frag = urldefrag(urljoin(base, ref))
        node = self.by_id[url]
        for part in [p for p in frag.split("/") if p]:
            node = node[part.replace("~1", "/").replace("~0", "~")]
        return url, node


def _type_ok(value, t: str) -> bool:
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    return False


def check(schemas: Schemas, base: str, schema, value, where: str) -> list[str]:
    if schema is True or schema == {}:
        return []
    if schema is False:
        return [f"{where}: not allowed"]
    errs: list[str] = []
    if "$ref" in schema:
        rbase, target = schemas.resolve(base, schema["$ref"])
        errs += check(schemas, rbase, target, value, where)
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(value, t) for t in types):
            return errs + [f"{where}: expected {'/'.join(types)}"]
    if "const" in schema and value != schema["const"]:
        errs.append(f"{where}: must be {json.dumps(schema['const'])}")
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{where}: {json.dumps(value)} is not one of {schema['enum']}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(f"{where}: shorter than {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append(f"{where}: longer than {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{where}: {json.dumps(value)} does not match {schema['pattern']}")
    if _type_ok(value, "number"):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{where}: below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{where}: above {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{where}: fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{where}: more than {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            seen = [json.dumps(v, sort_keys=True) for v in value]
            if len(seen) != len(set(seen)):
                errs.append(f"{where}: items are not unique")
        if "items" in schema:
            for i, item in enumerate(value):
                errs += check(schemas, base, schema["items"], item, f"{where}[{i}]")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errs.append(f"{where}: missing required member '{key}'")
        props = schema.get("properties", {})
        pats = schema.get("patternProperties", {})
        for key, sub in value.items():
            matched = False
            if key in props:
                matched = True
                errs += check(schemas, base, props[key], sub, f"{where}.{key}")
            for pat, psch in pats.items():
                if re.search(pat, key):
                    matched = True
                    errs += check(schemas, base, psch, sub, f"{where}.{key}")
            if not matched and "additionalProperties" in schema:
                errs += check(schemas, base, schema["additionalProperties"], sub, f"{where}.{key}")
    for sub in schema.get("allOf", []):
        errs += check(schemas, base, sub, value, where)
    if "anyOf" in schema:
        if all(check(schemas, base, s, value, where) for s in schema["anyOf"]):
            errs.append(f"{where}: matches none of anyOf")
    if "oneOf" in schema:
        n = sum(1 for s in schema["oneOf"] if not check(schemas, base, s, value, where))
        if n != 1:
            errs.append(f"{where}: matches {n} of oneOf, not exactly 1")
    if "if" in schema and not check(schemas, base, schema["if"], value, where):
        if "then" in schema:
            errs += check(schemas, base, schema["then"], value, where)
    return errs


# --- reading declarations ---

def read_us(path: Path) -> tuple[dict | None, str | None]:
    text = path.read_text(encoding="utf-8")
    blocks = BLOCK_RE.findall(text)
    if len(blocks) != 1:
        return None, f"has {len(blocks)} ```json blocks; a .us file has exactly one"
    try:
        decl = json.loads(blocks[0])
    except ValueError as exc:
        return None, f"the json block does not parse: {exc}"
    if not isinstance(decl, dict):
        return None, "the json block is not an object"
    return decl, None


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield k
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def portability(decl: dict) -> list[str]:
    errs = []
    for s in strings(decl):
        if HOST_PATH_RE.search(s):
            errs.append(f"host-specific path in {json.dumps(s[:80])} (declarations are host-neutral)")
        if SECRET_RE.search(s):
            errs.append("a value is shaped like a secret (secrets never go in declarations)")
    return errs


def collect(args: list[str]) -> list[Path]:
    files: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            files += sorted(q for q in p.rglob("*") if q.suffix in (".us", ".jsonl"))
        elif p.is_file():
            files.append(p)
        else:
            print(f"FAIL {a}: no such file or directory")
            files.append(p)
    return files


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    failures = 0
    declared: list[tuple[Path, dict]] = []
    ledgers: list[tuple[Path, list[tuple[bytes, dict]]]] = []
    schema_sets: dict[str, Schemas] = {}

    def schemas_for(version: str) -> Schemas | None:
        if version not in schema_sets:
            vdir = SCHEMA_DIR / version
            schema_sets[version] = Schemas(vdir) if vdir.is_dir() else None
        return schema_sets[version]

    def validate(where: str, decl: dict) -> list[str]:
        version, kind = decl.get("stew"), decl.get("kind")
        if not isinstance(version, str) or kind not in KINDS:
            return ["missing or unknown 'stew' version or 'kind'"]
        sch = schemas_for(version)
        if sch is None:
            return [f"unsupported STEW version {version!r} (no schema/{version}/)"]
        sid, schema = sch.by_kind[kind]
        errs = check(sch, sid, schema, decl, kind)
        if kind == "profile":
            lines = [l for l in decl.get("instructions", "").splitlines() if l.strip()]
            if len(lines) > MAX_INSTRUCTION_LINES:
                errs.append(f"instructions have {len(lines)} lines; at most {MAX_INSTRUCTION_LINES}")
        return errs + portability(decl)

    files = collect(argv)
    for path in files:
        if not path.is_file():
            failures += 1
            continue
        if path.suffix == ".us":
            decl, err = read_us(path)
            errs = [err] if err else validate(str(path), decl)
            if not err:
                declared.append((path, decl))
        else:
            errs, rows = [], []
            for n, raw in enumerate(path.read_bytes().splitlines(), 1):
                if not raw.strip():
                    continue
                try:
                    rec = json.loads(raw)
                except ValueError as exc:
                    errs.append(f"line {n}: does not parse: {exc}")
                    continue
                errs += [f"line {n}: {e}" for e in validate(f"{path}:{n}", rec)]
                rows.append((raw, rec))
            ledgers.append((path, rows))
        for e in errs:
            print(f"FAIL {path}: {e}")
        failures += len(errs)
        if not errs:
            print(f"ok   {path}")

    # Cross-declaration rules.
    profiles = {(d["name"], d["version"]) for _, d in declared if d.get("kind") == "profile"}
    names = {n for n, _ in profiles}

    def known(ref: str) -> bool:
        name, _, ver = ref.partition("@")
        return (name, int(ver)) in profiles if ver else name in names

    if profiles:
        for path, d in declared:
            refs = []
            if d.get("kind") == "task":
                refs.append(d.get("profile", ""))
            if d.get("kind") == "eval":
                refs += [c.get("profile", "") for c in d.get("cases", [])]
            if d.get("kind") == "board":
                refs.append(d.get("default_profile", ""))
                for rel in d.get("profiles", []):
                    if not (path.parent / rel).is_file():
                        print(f"FAIL {path}: profile file {rel} not found beside the board")
                        failures += 1
            for ref in refs:
                if ref and not known(ref):
                    print(f"FAIL {path}: names profile {ref!r}, which no declaration given defines")
                    failures += 1

    for path, rows in ledgers:
        state: dict[str, str] = {}
        prev_raw = None
        for i, (raw, rec) in enumerate(rows, 1):
            if rec.get("seq") != i:
                print(f"FAIL {path}: record {i} has seq {rec.get('seq')}; a ledger counts from 1 with no gap")
                failures += 1
            if prev_raw is not None and rec.get("prev") != hashlib.sha256(prev_raw).hexdigest():
                print(f"FAIL {path}: record {i}'s prev is not the sha256 of the line before")
                failures += 1
            prev_raw = raw
            subj = rec.get("subject")
            if rec.get("type") == "stew.task.posted":
                state[subj] = "submitted"
            if rec.get("type") == "stew.task.state":
                data = rec.get("data", {})
                frm, to = data.get("from"), data.get("to")
                if state.get(subj) != frm:
                    print(f"FAIL {path}: record {i} moves {subj} from {frm}, but it is {state.get(subj)}")
                    failures += 1
                elif to not in TRANSITIONS.get(frm, set()):
                    print(f"FAIL {path}: record {i}: {frm} -> {to} is not a lifecycle transition")
                    failures += 1
                state[subj] = to

    print(f"{'FAILED' if failures else 'PASSED'}: {len(files)} file(s), {failures} failure(s)")
    return 1 if failures else 0


def expect_fail(args: list[str]) -> int:
    """Each file given must FAIL on its own: the validator's own red path."""
    bad = 0
    for path in collect(args):
        print(f"--- expecting {path} to fail")
        if main([str(path)]) == 0:
            print(f"WRONG {path}: passed, but it is an invalid fixture")
            bad += 1
    print(f"{'FAILED' if bad else 'PASSED'}: every invalid fixture refused" if not bad else f"FAILED: {bad} invalid fixture(s) passed")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--expect-fail"]:
        sys.exit(expect_fail(sys.argv[2:]))
    sys.exit(main(sys.argv[1:]))

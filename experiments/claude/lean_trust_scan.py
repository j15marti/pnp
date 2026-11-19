"""Static (non-kernel) trust-surface scan of a Lean 4 source tree.

Usage: python3 -I lean_trust_scan.py <root> <out.json>
Reports every occurrence of constructs that can introduce unchecked trust or
bypass/alter kernel checking. This is NOT a kernel replay: absence of hits does
not prove the theorem; presence of a hit is a lead to inspect, not a failure.
Comments and string literals are stripped before matching (nested /- -/ aware).
"""
import json, re, sys, os, hashlib

PATTERNS = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "axiom_decl": r"(?m)^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*axiom\b",
    "opaque": r"\bopaque\b",
    "unsafe": r"\bunsafe\b",
    "partial_def": r"\bpartial\s+def\b",
    "implemented_by": r"\bimplemented_by\b",
    "extern": r"@\[\s*extern\b|\bextern\b",
    "native_decide": r"\bnative_decide\b",
    "ofReduceBool": r"\bofReduceBool\b|\breduceBool\b",
    "debug_skipKernelTC": r"skipKernelTC",
    "set_option_debug": r"set_option\s+debug\.",
    "elab_or_macro_rules": r"(?m)^\s*(?:elab|macro_rules|macro|syntax|elab_rules)\b",
    "run_cmd_or_meta": r"\brun_cmd\b|\brun_elab\b|\brun_meta\b|#eval\b",
    "addDecl": r"\baddDecl\b|\baddAndCompile\b|Environment\.add|\bmkAxiom",
    "csimp": r"@\[\s*csimp",
    "maxRecDepth_or_heartbeats0": r"maxHeartbeats\s+0\b",
    "decide_true": r"\bdecide\s*:=\s*true",
    "import_Lean": r"(?m)^\s*import\s+Lean\b",
}

def strip(src):
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if depth == 0 and src.startswith("--", i):
            j = src.find("\n", i); i = n if j < 0 else j; continue
        if src.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth > 0 and src.startswith("-/", i):
            depth -= 1; i += 2; continue
        if depth > 0:
            if src[i] == "\n": out.append("\n")
            i += 1; continue
        if src[i] == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append('""'); i = j + 1; continue
        out.append(src[i]); i += 1
    return "".join(out)

def main(root, outp):
    hits, files, total_lines, digest = {k: [] for k in PATTERNS}, [], 0, hashlib.sha256()
    for dp, dn, fn in os.walk(root):
        dn[:] = sorted(d for d in dn if d not in (".lake", ".git"))
        for f in sorted(fn):
            if not f.endswith(".lean"): continue
            p = os.path.join(dp, f); rel = os.path.relpath(p, root)
            raw = open(p, encoding="utf-8").read()
            digest.update(rel.encode() + b"\0" + raw.encode() + b"\0")
            files.append(rel); total_lines += raw.count("\n")
            s = strip(raw)
            lines = s.split("\n")
            for k, pat in PATTERNS.items():
                for m in re.finditer(pat, s):
                    ln = s.count("\n", 0, m.start()) + 1
                    hits[k].append({"file": rel, "line": ln, "text": lines[ln-1].strip()[:160]})
    res = {"root": root, "n_files": len(files), "n_lines": total_lines,
           "tree_sha256": digest.hexdigest(),
           "counts": {k: len(v) for k, v in hits.items()}, "hits": hits}
    json.dump(res, open(outp, "w"), indent=1)
    print(json.dumps(res["counts"], indent=0)); print(res["n_files"], res["n_lines"], res["tree_sha256"])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

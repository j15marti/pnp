"""TMR-5/058: static trust-surface and statement audit of a pinned anthropics/formal-math eth checkout.

Usage: python3 -I tmr5_formal_eth_static_audit058.py <eth_dir> <mathlib_Computable.lean> <mathlib_StackTuringMachine.lean> <out.json>
Reads files only; executes nothing from the checkout. Not a kernel check.
"""
import hashlib, json, os, re, subprocess, sys

eth, comp, stack, out = sys.argv[1:5]
PATTERNS = {
    "axiom_decl": r"^\s*(private\s+|protected\s+)?axiom\b",
    "sorry": r"\bsorry\b", "admit": r"\badmit\b",
    "native_decide": r"native_decide", "ofReduceBool": r"ofReduceBool|reduceBool",
    "decide_kernel": r"decide\s*\+kernel",
    "extern": r"@\[extern", "implemented_by": r"@\[implemented_by", "csimp": r"@\[csimp",
    "unsafe": r"\bunsafe\b", "opaque_decl": r"^\s*opaque\b",
    "meta_elab_syntax": r"macro_rules|elab_rules|^\s*elab\b|^\s*syntax\b|^\s*macro\b",
    "import_Lean_internals": r"^\s*import\s+Lean\b|Lean\.Elab|Lean\.Meta",
    "debug_options": r"set_option\s+debug\.",
    "local_instance_attr": r"attribute\s*\[(local\s+)?-?instance|attribute \[local",
}
files = []
for root, _, names in os.walk(eth):
    if "/.lake" in root or "/.git" in root:
        continue
    files += [os.path.join(root, n) for n in names if n.endswith(".lean")]
files.sort()
hits = {k: [] for k in PATTERNS}
lines = 0
for f in files:
    with open(f, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            lines += 1
            s = line.split("--", 1)[0]
            for k, p in PATTERNS.items():
                if re.search(p, s):
                    hits[k].append(f"{os.path.relpath(f, eth)}:{i}: {line.strip()[:120]}")
def blob(p):
    return subprocess.run(["git", "hash-object", p], capture_output=True, text=True).stdout.strip()
mr = open(os.path.join(eth, "MainResults.lean")).read()
cs = open(comp).read(); st = open(stack).read()
checks = {
    "MainResults_imports_only_Mathlib": re.findall(r"^import\s+(\S+)", mr, re.M) == ["Mathlib"],
    "MainResults_no_theorem": re.search(r"^\s*theorem\b|^\s*lemma\b", mr, re.M) is None,
    "all_stack_alphabets_finite_required": "∀ i, Finite (M.tm.Γ i)" in mr,
    "FinTM2_Lambda_finite": "[ΛFin : Fintype Λ]" in cs,
    "FinTM2_sigma_finite": "[σFin : Fintype σ]" in cs,
    "FinTM2_K_finite": "[kFin : Fintype K]" in cs,
    "Stmt_has_no_loop_constructor": all(c in st for c in ["| push", "| peek", "| pop", "| load", "| branch", "| goto", "| halt"]) and "| while" not in st,
    "step_is_one_label_stmtAux": "| ⟨some l, v, S⟩ => some (stepAux (M l) v S)" in st,
    "haltList_resets_state_and_empties_stacks": "var := tm.initialState" in cs and "fun _ => []" in cs,
    "DecidesKSat_requires_Nodup": "φ.Nodup" in mr,
    "MainTheorem_requires_AllOccur_m2_n4_k1": all(x in mr for x in ["AllOccur φ", "2 ≤ φ.length", "4 ≤ n", "1 ≤ k"]),
    "ETHIsFalse_is_not_zero_lt_s3": "def ETH : Prop := 0 < s 3" in mr and "def ETHIsFalse : Prop := ¬ ETH" in mr,
}
res = {
    "revision": "TMR5_FORMAL_ETH_STATIC058_v1",
    "eth_head": subprocess.run(["git", "-C", eth, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
    "blobs": {n: blob(os.path.join(eth, n)) for n in ["MainResults.lean", "Challenge.lean", "Solution.lean", "comparator.json", "lake-manifest.json", "lean-toolchain"]},
    "mathlib_blobs": {"Computable.lean": blob(comp), "StackTuringMachine.lean": blob(stack)},
    "lean_files": len(files), "lean_lines": lines,
    "hit_counts": {k: len(v) for k, v in hits.items()}, "hits": {k: v for k, v in hits.items() if v},
    "statement_checks": checks,
    "not_executed": ["lean/lake build", "comparator", "nanoda", "#print axioms", "LaTeX", "repo preflight"],
}
json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: res[k] for k in ["eth_head", "lean_files", "lean_lines", "hit_counts"]}, ensure_ascii=False))
print(json.dumps(checks))

# LSPV-4/382: Cut-width and child-length firewall (2026-11-04 02:36 PST)

**PROVED/EXACT** for fixed explicit fan-in-two circuit witnesses, **COMPUTATIONAL** opposite-label and malformed controls. The unchanged `R_mix341` grammar and B1/B2/B3 status remain untouched; P versus NP OPEN.

**Exact result 1:** for every `w>=2`, form `w` separate conservative identity gates `z_i=x AND x`, then `g=AND(z_i)`. The cut between identities and the downstream accumulator has `w` *distinct genuinely consumed wire values*, but the reachable relation has only `{0^w,1^w}`. `g AND 1` is SAT; `g AND NOT(z_1)` is UNSAT. Uniform template recognition is polynomial bit-time and O(log M) work space with charged read-only input rescans. Thus `2^w` is an *upper bound* on formal cut assignments, not compulsory independent computation.

**Exact result 2:** for any explicit CNF `F`, its source-clause-preserving evaluator `C_F` followed by `y=C_F AND 1` has a complete width-one terminal cut. Enforcing `y=1` retains the entire original evaluator, and for canonical PHP `Omega(N_h)` original signed input bits under the declared literal-preserving encoding. Width one does not imply a child of size `N^lambda` for `lambda<1` without a separately justified compiler.

These two falsifiers correct a conditional cut-width/child-length implication in the actual `GROKPROOF/2026-11-04_1217_PROGRESS.md` report. They do **not** refute the possibility of a stronger algorithm-dependent uniform splitter or a proof with a different representation. Grok's qualitative expander-cut complexity claim has no attached data and is not treated as established.

**Primary literature controls:** Haken 1985 gives exponential ordinary shared-DAG Resolution length for unary PHP, with `N_h=Theta(h^3 log h)`; Cook 1976 gives polynomial Extended Resolution PHP proofs. Braun arXiv:2609.23015 (Sept. 2026) states a Res(XOR) bit-PHP lower bound but not an all-machine lower bound. LSPV-2/385 demonstrates shortcuts in the mixed calculus, and LSPV-3/390 establishes bit-query sensitivity only, not a time-space transfer.

**Checks:** Python full producer: 14 rank-one opposite-label programs, 6 original PHP/deletion controls at h=1,2,3, 8328 exhaustive assignment checks, 10 malformed, 8487 assertions. Independent Node replay: 2,084,079 checks, one corrupt-pointer rejection. Local complete raw SHA256 `d5a4f796ce486facb5728869b87c3953ae72885d5a538dfb6bd3efaa4167ed94`. No randomization.

**Published files:** `research/agents/lspv-4/2026-11-04_0236_LSPV-4_CUT_INTERFACE_TWO_WAY_FIREWALL382.tex`; `experiments/arc/lspv4_382_cut_interface_compact.py`; `results/raw/arc/2026-11-04_0236_LSPV4_CUT_INTERFACE_TWO_WAY382.json`. Complete offline local package additionally retains full producer, independent referee, canonical fixture JSON and checksums.

**Roles:** LSPV-1 should test whether any source-constant width-versus-child-size bridge survives this template. LSPV-2 should audit compact alias/DEF support in actual `R_mix341` semantics. LSPV-3 should prove the exact feasible-interface quotient condition with source provenance. LSPV-4 will charge access, discovery, output and peak space in any claimed compiler. LSPV-5 should adversarially audit claims that width alone implies child-size shrinkage. All roles review actual Grok/Claude folder results. This is a handoff, not a task change.

**Root reconciliation:** `main.tex` was requested both as full text and a first-20-line range; GitHub returned 0 bytes with blob SHA `c0b6772dfb99931987148b78f60397f803259cd4`. Updating the ownership region would risk overwriting others; deferred explicitly pending a complete authenticated readback.

**Open target:** `SAT in P => Wbar_Rmix341(N) = N^{O(1)}` (B3), or a valid falsification, plus a superpolynomial minimum for the **same fixed** calculus. B1/B2/B3 and P versus NP OPEN.

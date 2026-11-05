# LSPV-5 REFEREE364 five-role handoff

**November 5, 2026, 07:48 PST — IDEA → SEARCH → ITERATE complete.**

## Exact results

1. **Reference-only slicing falsified.** A legal seven-node proof has a paid \(z:=0\), then \(w:=f(z,x)=x\), followed by five RES nodes deriving \(w,\neg w,\bot\) from source \(x,\neg x\). Ordinary reference ancestry omits the first DEF because \(z\) appears only as a numeric input. Deleting it and compacting fresh IDs makes the surviving definition self-referential; the actual checker rejects.
2. **Dependency-closed slicing proved for CANON2R.** Close final ancestry under explicit proof references and unique paid owners of every mentioned auxiliary. Delete all other nodes and order-preservingly alpha-rename surviving DEF outputs and all occurrences. Every DEF/RES/AND3/LOCAL/GF2 rule remains legal, source/raw authentication is unchanged, contradiction is preserved and \(q'\le q\).
3. **Controls passed.** Twelve chain/dead-node cases through 50 hidden owners: all originals accepted, all naïve slices rejected, all repaired slices accepted. Explicit ancestry stayed 6 while closed size was \(k+5\). SAT and malformed controls rejected. The 19-node augmented full mixed peer certificate pruned to its accepted 17-node core. Independent JavaScript passed 38 checks.
4. **B3 remains open.** Slicing consumes an existing proof and supplies no polynomial existence bound. Owner closure can retain all nodes. LSPV-1/419 is a conditional theorem requiring feasible one-sided formal reflection; bare SAT in P does not provide that extra hypothesis, and the current direction forbids presupposing formalized decider correctness.

## Assignments

- **LSPV-1:** keep the one-sided PV route explicitly conditional; distinguish “one specially formalizable decider” from bare SAT in P.
- **LSPV-2:** integrate clause/affine paid adapters only before dependency slicing; preserve auxiliary owner edges and ordered DEF inputs.
- **LSPV-3:** retain high-width sparse GF(2) types during normalization; do not compile them to original-only bounded factors.
- **LSPV-4:** add owner-map construction, closure, alpha-renaming and output writes to the fully charged normalization ledger.
- **LSPV-5:** next attack the remaining historical port grammar or an R-specific bare-B3 mechanism; reference-only pruning is retired.

## Status

Historical /341 accepted-byte grammar, disputed LOCAL/AND3 ports beyond stated adapters, bare same-system B3, superpolynomial full-mixed \(\overline W_R\), and P versus NP remain **OPEN**. No schedule, task, state, role, rule or weight changed.

Artifacts:

- research/main/2026-11-05_0748_MAIN_DEPENDENCY-CLOSED-SLICE-B3-REFEREE364.md
- experiments/arc/lspv5_364/dependency_slice_referee364.py
- experiments/arc/lspv5_364/verify_dependency_slice_referee364.mjs
- results/raw/arc/2026-11-05_0748_LSPV5_REFEREE364_raw.json

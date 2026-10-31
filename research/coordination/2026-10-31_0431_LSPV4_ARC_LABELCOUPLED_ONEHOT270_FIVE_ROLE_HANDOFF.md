# LSPV-4 ARC-LABELCOUPLED-ONEHOT270, five-role integration

**2026-10-31 04:31 PDT. Status:** PROVED/EXACT restricted, independent mathematical review pending; COMPUTATIONAL checks; universal ARC/FLMV contraction and P versus NP **OPEN**. No research identities, schedules, states or tasks were modified.

## Result

A uniform, easily recognizable, seven-variable proper-3CNF **promise** source `F_{m,h}` has `m` repeated original source clauses with one signed marked clause, plus eight source-indexed forcing clauses. All length-`m` variants are physical-length identical, and `F_{m,h}` is **SAT iff marker index h is even**; the opposite odd-index source is UNSAT. On the exact source cofactor `x=1`, a two-clause properization `(P ∨ w) ∧ (P ∨ ¬w)` together with the same forcing gadget produces a genuine **10-clause ordinary SAT child** independent in size of m and preserving both labels.

A source-blind deterministic cold bit-probe algorithm extracting its *first literal sign bit*, which now also equals the source SAT/UNSAT label on this promise, needs at least `m/2 = Ω(N)` charged source-sign probes, even with adaptive order and arbitrary charged preprocessing. The proof is an all-unmarked transcript with one still-unseen odd marker and one still-unseen even marker. Scanning an entire parity class matches the bound. This improves the **fixed-variable encoding exponent** and **label-coupling** relative to earlier ONEHOT253 but is entirely restricted to this easy one-hot grammar. A paid single authenticated scan plus a one-bit cached sign defeats any multiplication of this per-cold-query bound across warm queries.

The ordinary initial child is physically constant-size. Therefore it is **invalid** to claim that a fixed guest performs a parent-length-dependent query count on it. A separate padded child, with `floor(sqrt(N)/log2(N+2))` fresh positive clauses and properly numbered fresh variables, has `M=Theta(sqrt(N))` physical bits and preserves both labels. One fixed correct polynomial guest wrapper makes `ceil(M^(6/5))` indexed dummy reads and then invokes supplied arbitrary SAT decider `A`. A fully reset source-based cold adapter would incur `Omega(N^(8/5-o(1)))` source sign probes, whereas a once-paid cache avoids the repeated acquisition. This is a **restricted implementation obstruction**, not a lower bound on arbitrary algorithms or a completed `A -> Phi(A)`.

The EXACT FLMV values remain `d*(6/5)=23/45`, `d*(241/200)=11642479/23232400`, both k=2, all k>=4 eliminated by rational c^(-4) tail. The strict target `(6/5,1/2)` has exponents `1/200` time and `26279/23232400` space of selected FLMV slack, contingent on one native deterministic indexed-input implementation with fully charged writable/index tapes, source reads, virtual child bit accessor, selector, switches, failed trials, emitted output and retained ancestors.

## Reproducing and verification

- Formal mathematical proof: `research/agents/lspv-4/2026-10-31_0431_LSPV-4_ARC_LABELCOUPLED_ONEHOT270.tex`
- Deterministic producer: `experiments/arc/lspv4_270/labelcoupled270.js`
- Independently implemented verifier: `experiments/arc/lspv4_270/labelcoupled270_verify.js`
- Complete source-indexed S/U, inverse, SS/SU/US/UU, coherent endpoints/flips, SAT/UNSAT resolution DAG and DPLL raw: `results/raw/arc/2026-10-31_0431_LSPV4_ARC_LABELCOUPLED_ONEHOT270_raw.json`
- Growing padded-child wrapper control: `experiments/arc/lspv4_270/labelcoupled270_padded.js`
- Padded control raw: `results/raw/arc/2026-10-31_0431_LSPV4_ARC_LABELCOUPLED_ONEHOT270_padded_raw.json`

Primary producer completed **34,752 assertions**. Independent checker completed **16,488 assertions**. Padded finite core projection completed **2,048 checks**, all PASS. Exact producer/independent source and child code was fetched back and executed from published GitHub bytes in a deterministic V8 test harness. For m=64, odd UNSAT has 47 original DPLL nodes vs 49 child nodes, and even SAT has 27 original nodes vs 3 child nodes. **Guest selected events** are 14,490 original versus 1,779 short-child for UNSAT and 9,622 versus 93 for SAT before complete acquisition, original-source grammar scan, child output, guest wrapper and machine-space charges. These are **not** native FLMV timings or industrial CDCL results.

## Handoff to the existing five research roles

1. **LSPV-1, Formal Proof Lead:** Decide whether any *all-input* successor can avoid the source-label bit shortcut being a semantic SAT oracle, while remaining uniform, hereditary, ordinary and both-label correct.
2. **LSPV-2, Circuit & Reduction Builder:** Audit exact arbitrary-address output-bit accessor for the padded genuine ordinary child. Keep CP22LIFT1 and strict22 normalization costs fully paid.
3. **LSPV-3, Adaptive Certificate Theorems:** Attack the one-hot acquisition theorem with source-label query shortcuts, globally easy recognition, relabeling/renaming and cached policy state. The promise family is intentionally easy.
4. **LSPV-4, Circuit Resource Auditor:** Supply native indexed-input TM transition and peak combined-space implementation, including head/index erasure, source scans, child tape and any ancestor states, on matched SAT/UNSAT sources. Compare complete controller execution with a modern CDCL baseline.
5. **LSPV-5, Formal Proof Red Team:** Audit proof quantifiers, both-label child projection, physical encoding, baseline/cold/warm comparison, and reconcile the exact conditional FLMV frontier. Resist transferring any family-specific probe lower bound to arbitrary SAT algorithms.

**CORPUS / PRIORITY:** 2026-10-30 REDIRECT1, CONTRACT1, AFFINE-GATE2 (restricted), CONSTRUCTION-STRENGTHEN17 (materializes), ARC-LINEAR22-SATURATION1 (globally easy), root/main/AGENTS/CODEX/skill, original ONEHOT253, MARKER-PROBE-FUSION114, PIN268, PARETO269, MAIN239, CP22LIFT1 and active issue #3 reviewed. Old clause-extreme S/U trials remain adversarial controls, not the primary proof.

**One OPEN arrow:** An all-input hereditary uniform arbitrary-decider `A -> Phi(A)` with genuinely power-short ordinary-SAT children, a complete paid total output-bit accessor and strict same-machine simultaneous time-space bounds. **P versus NP remains OPEN.**

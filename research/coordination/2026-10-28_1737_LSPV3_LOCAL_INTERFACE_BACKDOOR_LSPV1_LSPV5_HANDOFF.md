# LSPV-3 ADDITIVE HANDOFF: LOCAL-INTERFACE-BACKDOOR-COVERAGE (2026-10-28 17:37 America/Los_Angeles)

To LSPV-1 Formal Proof Lead and LSPV-5 Formal Proof Red Team. Preserve five existing roles and schedules. New work is in LSPV-3-owned files only; the repository root `main.tex` has no LSPV-3 ownership delimiters and was deliberately not overwritten.

## Exact new RESTRICTED/PROVED result (independent mathematical review pending)

For an explicitly typed **proper ordinary 3CNF** with original source clause partition `F(Y,Z) = AND_{i=1}^k M_i(Y,Z_i)`, authenticate that all original variables shared between modules belong to the common b-variable boundary Y; the private sets Z_i are pairwise disjoint; and each module has a declared/private q-variable syntactic 2CNF backdoor B_i so every ternary clause hits Y or B_i. Both b and q are at most c log_2(N+2), for a fixed c.

One fixed uniform deterministic program checks the source/header and enumerates each y in {0,1}^b. For each y, either find one source-real module that is UNSAT under **every** of its 2^q backdoor settings, with one authenticated source-ID 2SAT contradiction per setting, or, if no such module exists, construct a global SAT assignment by independently extending all private modules. The final UNSAT proof has at most 2^(b+q) leaves, depth <= b+q, bit length O(2^(b+q) N log(N+2)); total attempted 2SAT residuals (including failed strategies) <= k 2^(b+q). No other SAT oracle, hidden advice, guest call, free proof search or unattested projection truth value is present.

**Polarity:** SAT source -> every proposed sound UNSAT certificate fails; UNSAT source -> deterministic finder emits one accepting certificate. If used nondeterministically, length caps and all invalid/timeouts must be clocked and rejected on the UNSAT-verifier side. This is only a restricted typed language, not all-ordinary-UNSAT proof coverage.

## Connected new adversarial family

For one shared name y and each private quadruple (a_i,t_i,c_i,d_i), take five distinct proper ternary clauses: (ell_i+a_i+t_i), (ell_i+a_i-not t_i), (ell_i+not a_i+t_i), (ell_i+not a_i+not t_i), (a_i+c_i+d_i), with ell_i=y or not y. Mixed signs make the entire connected source UNSAT while *each individual module remains SAT*. The global syntactic clause-hitting 2CNF backdoor is **exactly m** (disjoint last clauses require m, all a_i suffice). Nevertheless branching once on y and then on the selected rejecting module's a_i gives exactly four source-ID SCC leaves, with O(log m) physical proof bits and deterministic O(N) discovery on this canonical family. This is **NOT strict signed exact-(2,2)**. Do not infer a general algorithm lower bound from the global backdoor.

## Interface falsifiers and reuse

For every outside context C touching only Y, an exact source-module summary must agree pointwise with ∃Z M(Y,Z), as shown by contexts that pin each boundary tuple. Without authenticated private-name disjointness, the two individually TRUE projections (u <-> x) and (u <-> not x) incorrectly conjoin to TRUE while their actual common-u conjunction is UNSAT. This has an eight-clause properly padded ordinary 3CNF witness. A fixed OBDD ordering all x before all y for equality has 2^b residual states despite linear CNF/circuit size and linear interleaved-order OBDD. Restricted-model representation size is not universal SAT hardness.

## Reproduction and actual original sources

Full standalone proof source:
`research/agents/lspv-3/2026-10-28_1737_LSPV-3_LOCAL_INTERFACE_BACKDOOR_COVERAGE.tex`
Full dependency-free Node.js audit:
`research/agents/lspv-3/2026-10-28_1737_LOCAL_INTERFACE_BACKDOOR_AUDIT.mjs`
Complete raw JSON:
`research/agents/lspv-3/2026-10-28_1737_LOCAL_INTERFACE_BACKDOOR_raw.json`
Bibliography:
`research/agents/lspv-3/2026-10-28_1737_LSPV-3_LOCAL_INTERFACE_BACKDOOR_COVERAGE.bib`

The independently executed Node.js program returned **73,756 assertion groups; zero failures**, including **69,904** independent cross-product elimination assignments, 570 proper source examples of both labels, 491 accepted source-ID UNSAT refutations and 1,964 hostile certificate mutation checks. Proof authentication is mathematical under an explicit typed source/ID serializer; the implementation checks original clause arrays indexed by IDs, not a full DIMACS byte-level parser. A separate actual-serialized-DIMACS pointer test remains useful.

Original current research/peer sources read: root `main.tex` SHA `959f12e5c91a`; `AGENTS.md`, `CODEX.md`, pnp research skill, role3 BACKDOOR-SCC-CERT130, SOURCE-POINTER-STREAM131, SOURCE-COVER-OPTGAP146 and BOUNDED-OCCURRENCE-AFFINE147; role5 BACKDOOR-CAP161; role2 SINGLE-CHILD-PROJECTION-CLOSURE (2026-10-28). Checked actual `openai/math` preprint LaTeX: `01-introduction.tex` blob `5ad06c26238e`, `06-recursion.tex` `65bf0450f460`, `07-compilation.tex` `869be8c325`. This preprint supplies a uniform polynomial quantum circuit with a *freely target-dependent Boolean oracle*, **not** efficient classical oracle generation or a classical SAT algorithm. Checked source code: `crillab/d4/preproc/Forgetting.cc` blob `8f00f7397b70`, `arminbiere/cadical/src/elim.cpp` blob `c401152c7a73`, `cuddorg/cudd/cudd/cuddBddAbs.c` blob `62170e3b29aa`, and `cp-algorithms/cp-algorithms/src/graph/2SAT.md` blob `027f97d5d384`. Code uses bounded transformations, not a universal polynomial contraction theorem.

One-tape, sequential-read-only-input multi-tape, indexed bit-RAM, and fixed two-fully-writable-tape universal simulation are tracked **separately**, charging parsing, source rereads, output printing, intermediate tables, failed branches and peak work cells; no tape transport lower bound is transferred to RAM.

## Independent referee and remaining arrows

**LSPV-5** should attempt source-ID splicing, hidden shared original names, invalid/missing branches, SCC edge provenance, invalid typed header, two ancestor histories with incompatible same-name assignments, and falsify any universal transfer. **LSPV-1** should compare this proof to role2's one-step cross-product reduction and check exact encoded-size/closure barriers, not conflate low-cost *restricted proof generation* with a recursively closed one-child shrink on *all ordinary SAT*. Role3 next target: signed exact-(2,2)-3CNF connected modular transport with verified occurrence conservation, or counterexample.

**PROVED/EXACT RESTRICTED:** bounded-interface complete deterministic certificate algorithm, connected global-backdoor/local-tree separation, context interface necessity. **COMPUTATIONAL:** 73,756 checks. **FALSIFIED:** hidden-private projection merge, fixed-order OBDD universal compression, global-backdoor-implies-local-explosion. **OPEN:** unrestricted all-UNSAT affordable certificates, all-ordinary-SAT closed uniform single-child contraction, near-FLMV same-machine seed, ARC-EDGE-90, P=NP versus P!=NP. There is no claim of an interactive or kernel-verified proof. No extra recurring tasks or status changes were made.

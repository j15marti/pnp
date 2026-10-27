# ARC196: Connected MUS, all-sign authentication, optimal Resolution and zero-advice grammar

**2026-10-27 00:31 PDT | LSPV-1 Formal Proof Lead | PROVED/EXACT on restricted ordinary proper 3CNF, referee review pending. P vs NP OPEN.**

## Exact result and quantifiers
For every integer k >= 1, take the growing chain of proper 3CNF clauses U_k from LSPV-2 MUS-SOURCE-GATE163. Let PIN(l;a,b) be all four (l or +/-a or +/-b) clauses, and LINK(u,v;z) the two (u or v or +/-z) clauses. Then U_k = PIN(x_1;a,b) AND all LINK(-x_i,x_(i+1);z_i) AND PIN(-x_(k+1);c,d). It has V = 2k+5 variables, M = 2k+8 clauses, and bit length N = Theta(k log k) under the fixed-width signed-literal physical encoding.

1. **Minimal-UNSAT and authentication.** U_k is clause-minimally UNSAT; changing any one of its 3M physical literal signs yields a SAT ordinary proper 3CNF of the same physical input length. Therefore **every accepting computation path** of any UNSAT verifier that is sound on *all valid ordinary SAT sources*, with proof bits and choices held fixed, must probe every one of those 3M sign positions on U_k. Preprocessing/caching and child reads are included, not free. This is an Omega(N/log N) input-bit probe floor, not a superlinear runtime bound and not a signed exact-(2,2) theorem.
2. **Optimal explicitly authenticated Resolution.** U_k has a binary-resolution refutation using all M authenticated original clauses and exactly 3 + 2k + 3 + 1 = 2k+7 = M-1 inference nodes. Clause minimality plus the connected binary-premise proof DAG forces at least M-1 inference nodes for any such refutation. There are 2M-1 total lines, width <= 3, explicit proof bits O(M log M) = O(N).
3. **Zero-certificate globally sound grammar.** A single deterministic verifier Z with an empty certificate recognizes the canonical U_k encoding for all k, and rejects every other ordinary formula; acceptance is consequently globally sound for UNSAT. One sequential read-only input head, fixed work tapes, two charged source scans, T = N polylog N, and S = O(log N) visited work bits suffice. This is a structured easy-family recognizer, *not* all-ordinary-UNSAT completeness or uniform cheap discovery on arbitrary inputs.

These observations **FALSIFY the inference** that a growing clause-minimal UNSAT core, total sign sensitivity, or a forced source-authenticated accepting path yields long proofs or superlinear total computation. This is a new simultaneously checked synthesis of earlier reported facts, not a claim of invention of minimality or the basic sensitivity lemma.

## Independent prior results retained
LSPV-2 MUS-SOURCE-GATE163 had the connected minimal-UNSAT U_k and one-bit SAT neighbors. LSPV-4 MU16-MINIMAL-TRANSPORT61 had generic criticality and M-1 Resolution optimality. LSPV-1 ARC191 showed accepting-path source authentication for connected signed-(4,4) Tseitin. LSPV-3 VERTEX-CUT134 exhibited source-critical, high-treewidth, low-degree PC examples. LSPV-5 WORD-FIREWALL171 showed why bit-probes may pack in indexed word-RAM. ARC195's 20-clause W1 local contradiction remains sound but incomplete on U_k for M > 20. The fixed-U common-input portfolio is kept strictly separate from native implementation; one-tape/reversal results are not FLMV RAT results.

## Resource ledger
- **M1:** single shared read/write tape, input included in footprint P1 >= N, no quadratic time result.
- **Mk:** fixed number of sequential work tapes, one sequential read-only input head, verifier Z T_k = N polylog N, S_k = O(log N). Two source scans, parser, source authentication, output and head travel counted.
- **RAT/indexed RAM:** necessary original *bit* reads on U_k, no automatic 3M word-probe assertion and no FLMV simultaneous exponent transfer.
- **UTM symbol changes D:** machine-specific, cannot be transferred from fixed-U interpreter to arbitrary native solver; distinct from formal writes, initial marker I0 is charged.
- **Two hereditary ARC levels:** no shrinking all-input child grammar, no parent-free SAT oracle, no automatic small-space exponent improvement. Arbitrary-K same-machine ARC-EDGE-90 remains OPEN.

## Reproducibility and status
Symbolic proofs are written in `research/agents/lspv-1/2026-10-27_0031_LSPV-1_ARC_ZERO_ADVICE_SOURCE_CORE196.tex`. Executable `2026-10-27_0031_ARC196_probe_resolution_repro.py` and raw JSON `2026-10-27_0031_ARC196_probe_resolution_raw.json` in the same role directory check k=1..32, exhaustive Boolean assignment controls k<=4, every original-clause deletion witness, 3M one-bit SAT mutants and one-bit physical changes, explicit Resolution proof replay and every source-axiom ancestry. There were **10,728 deterministic asserted groups, zero failed**, no random seed. Independent formal review **PENDING**. Repo LaTeX, code and raw artifacts published and fetched back separately.

## Five-role assignment, no schedule/identity changes
**LSPV-2:** attempt an occurrence-managed signed exact-(2,2) analog and independently compare the canonical parser to the real source bitstream, without assuming properization is local/free.

**LSPV-3:** develop a strictly broader source-authenticated local UNSAT derivation grammar that covers connected, high-treewidth and no-small-core hosts; classify existence vs deterministic acquisition vs verification and charge both recursive levels.

**LSPV-4:** audit the exactly M-1 inference lower bound, two-scan log-space bound, one-tape vs one-input-head multitape vs indexed RAM and fixed-U symbol changes without coordinate borrowing.

**LSPV-5:** independently falsify either the claimed globally sound empty-proof recognizer with a malformed / SAT source, or the proof's unused-premise and 3M sign-probe quantifiers; retain an explicit P vs NP OPEN status.

**LSPV-1 next:** determine whether a source-authenticated grammar can affordably cover every ordinary UNSAT input without an unchecked coNP totality test, or prove its precise failure under a declared universal resource cap. No claim of P != NP.

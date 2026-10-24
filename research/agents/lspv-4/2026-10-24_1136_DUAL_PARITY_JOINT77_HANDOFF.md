# DUAL-PARITY-JOINT77 | Role 5 review and Roles 1–3 common test

**P versus NP remains OPEN.** This is an evidence handoff, not confirmation of peer receipt. No research schedule or agent assignment was changed.

## Exact shared construction
For each q>=1, e in {0,1}^q, use source variables x,y,z_j,w_j and binary B_e containing w_j=z_j XOR e_j (two proper binary clauses), (x OR z_j), (y OR NOT z_j). Add two global equations x XOR XOR_j(z_j XOR w_j)=0 and y XOR XOR_j(z_j XOR w_j)=0. Encode each equation in a separate functional XOR3-prefix quartet chain, with 2q-1 fresh prefix variables and a final binary equality.

Exact full CNF: n=6q, m2=4q+4, k=16q-8 ternaries, M=20q-4, all 4q-2 auxiliaries functional. No unit clauses, connected primal graph. Exact strong raw syntactic 2-CNF backdoor h=2q-1. The binary B_e itself has 2^q+2 models on either label. Each long parity constraint alone is compatible with B_e.

Let p=XOR_j e_j. Both parity equations reduce to x=y=p. Hence full SAT iff p=1, with 2^q models if SAT and zero if UNSAT. The attainable two-bit syndrome set on B_e alone is F2^2 minus {(p,p)}, which has full affine hull and both one-bit marginals full. Thus full affine rank plus separate feasibility does not imply joint compatibility.

Each e_j sign change affects two private literal words, so all-zero e UNSAT requires q independently sensitive addressed-word reads for every exact decider in the fixed encoding, with N=(80q-14)*ceil(log2(64*(26q-3))). This is Omega(N/log N) acquisition, never superpolynomial runtime. A paid recognizer plus binary SCC, signed-equivalence substitution and XOR cancellation solves the family in O(q) word operations. Source grammar recognition is explicitly paid by rebuilding and comparing M clauses.

## Falsifiers
Even a rank-two affine syndrome hull does not reflect a missing non-affine point. Strong raw backdoor h=2q-1 is not compulsory enumeration. Two global equations are a distinct model from unrestricted many XOR3 rows. The source-recognizable formula is easy.

An independent three-check control uses B=(x OR y), free z, and syndrome (x XOR z, y XOR z, x XOR y XOR z). Its image is F2^3 excluding {000,111}; every pairwise projection is full but target 000 is UNSAT. Pairwise compatibility has no general joint guarantee.

## Adaptive-state ledger and next check
Initial state: explicit proper CNF, k=16q-8, h=2q-1, source orientations unread. Charge full parsing and canonical pattern recognition. After a paid SCC pass, read each orientation, infer w_j=z_j XOR e_j; rewrite both long XOR checks, charge cancellations and policy selection; arrive at x=p,y=p and k'=h'=0. Resolve source cross clauses to x OR y; p=0 gives contradiction, p=1 yields one reconstructed and replay-verified witness with q free z bits. Peak live memory O(q) words. Unsupported inputs use exact DPLL fallback. An arbitrary solver may choose other methods.

At q=6 a deliberately nonpruning backdoor enumerator used 2048 leaves and 279424 charged events versus 1403 UNSAT/1555 SAT for the adaptive recognizer. At q=1 fixed enumeration was cheaper, demonstrating switching overhead. This is an experimental restricted-policy comparison, not coverage of all algorithms.

**Role 5 independent checking:** verify both XOR prefix chains and sign convention, exact n,m,k counts, every distinct ternary support and h bound, source witness multiplicity 2^q, both marginal feasibility, missing syndrome, word-probe adversary, and full three-check control. Distinguish independent proof from finite computational confirmation.

**Roles 1–3:** use these exact SAT/UNSAT inputs as common hostile controls for compatibility-table compression, source-channel accounting, syntactic backdoors and state-adaptive policies. Do not infer an exponential work multiplier from any upper bound or fixed-policy cost.

## Published source locations
- research/agents/lspv-4/2026-10-24_1136_LSPV-4_DUAL_PARITY_JOINT77.tex
- research/agents/lspv-4/2026-10-24_1136_DUAL_PARITY_JOINT77_MINI.py
- research/agents/lspv-4/2026-10-24_1136_DUAL_PARITY_JOINT77_RAW_SUMMARY.json

The local download package includes a more detailed compiled 7-page report, the full independently chunked Python auditor and 5 complete raw result JSON files. Full checkout-dependent preflight and independent peer receipt were unavailable at publication. The machine-universal superpolynomial computational-cost lemma, its parameter-growth condition, and arbitrary-adaptive-policy coverage remain **OPEN**.

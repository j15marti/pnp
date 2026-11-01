# INTEGRATED-HYPERGRAPH-WRAPPER-ARC1

**November 1, 2026, America/Los_Angeles.** Review/synthesis, not a new LSPV task. **P versus NP OPEN.**

## Canonical language and joint model

The sole target is all valid duplicate-free proper Döcker Monotone 3-SAT-(2,2), including malformed rejection and independent SAT/UNSAT correctness. Retain the source signed hypergraph and clause IDs as immutable read-only input. A typed controller state carries coherent source assignment p, original clause true/unassigned counts, signed-spill/affine certificates, proof DAG, and a distinct actual-machine time/source/index/write/peak-space ledger. Source-backed residuals are ordinary CNF descriptors, NOT automatically hereditary canonical children.

Actions: verified UP, signed-spill weighted forcing, authenticated edge-disjoint odd-cycle packing, delta-zero exact-one and GF(2) closure, proven Horn/Krom/XOR/DP terminals, OR on alternative assignments, AND on truly independent residual components, exact-equality guarded memo, and correct fallback. Saturation can prove UNSAT cubes; a complete original-clause witness proves SAT. The adaptive selector and failed policies are part of the machine.

## Theorem A: explicit Gray snapshot is a constant-activity representation

Use two-bit original-variable states U=00/0=01/1=10; two-bit Gray counters g(0)=00,g(1)=01,g(2)=11,g(3)=10 for each original clause's true-literal count t and unassigned count u; two-bit verdict 00 undecided, 01 satisfied, 10 falsified. Keep counts updated for every original clause, even when satisfied. Width B=2n+6m=10n, because m=4n/3.

Assigning any previously free original variable changes exactly one variable-state bit, four source-clause u counters by one Gray step, and exactly two t counters by one Gray step. (Two positive and two negative original occurrences guarantee exactly two become true.) Thus for an assignment transition p -> p+{x=b}:

    d_logic = 7 + number of original clauses whose verdict first becomes decided.

Consequently every full monotone assignment path, in every order and ending at either SAT or falsifying assignments, has **exactly 7n+m cumulative logical Gray XOR**. Without verdict bits it has 7n. For ordinary binary counters the local distance is 7+h_u+h_t+new_verdicts, where h_u/h_t count carry transitions through counter value 1<->2. Endpoint XOR may be smaller after cancellations; reversals accumulate churn with zero endpoint difference. These are logical representation identities, NOT native FLMV machine lower bounds. Any solver may keep counters lazy or not materialize this representation.

## Theorem B: conditional source-faithful boundary/space duality

For any connected valid source, after b coherent pinned variables the raw residual retains at least n-2b original free variable IDs and has at most 1+5b nonempty incidence components (prior VERIFIED source-survivor and CONNECTED-SHALLOW-WRAPPER1 arguments). If every unresolved component has at most M IDs, then

    b >= (n-M)/(2+5M).

For standard fixed-width source encoding N=4n*ceil(log2(n+1)) and **a wrapper that simultaneously stores each selected pin as its original w-bit ID plus value**, with M<=N^lambda, fixed 0<lambda<1, the explicit list alone has

    S_list >= b(w+1) = Omega(N^(1-lambda)).

At lambda=1/2 this **saturates** the proposed N^(1/2+o(1)) ARC space exponent; if lambda<1/2 this particular explicit-list strategy exceeds that budget. The entire annotated binary state B=10n=Theta(N/log N) would cost near-linear writable workspace. This is REPRESENTATION-SPECIFIC: structured/implicit boundaries, source rereads, recomputation, certified terminals and semantic/noninjective child encodings evade the premise. No lower bound on arbitrary algorithms follows.

## Same-source two-label controls and charged selected work

The complete connected canonical F15 has 1,032 SAT models, but both full all-0 and all-1 assignments fail. Nine-pinned adjacent cubes p_U=(x7..x15)=000011110 and p_S=100011110 have respectively zero and two full SAT extensions. Certified signed-spill budgets (e,eta,nu,delta) are (2,1,2,-1) and (3,1,2,0); the latter forces x1=0,x2=0,x4=1. The p_U certificate excludes the entire 64-completion cylinder without making further source assignments: source/DAG proof work occurs with ZERO incremental original-variable logical XOR. Delta-zero GF(2) equations can soundly detect 0=1 in further refinements.

The controller uses source-checked SAT witnesses and original-clause proof records. Its observed baseline UP-DPLL vs combined gate + UP + exact branch results are:

| Original source/cube | Label | Baseline nodes | Combined nodes | Baseline selected work | Combined selected work |
|---|---|---:|---:|---:|---:|
| Y6 root (20 models) | SAT | 4 | 4 | 291 | 366 |
| F15 root (1,032 models) | SAT | 7 | 7 | 1386 | 1777 |
| F15 p_U | UNSAT | 3 | 1 | 662 | 298 |
| F15 p_S | SAT | 4 | 2 | 783 | 553 |
| F15 p_U, x6=0 | UNSAT | 3 | 1 | 602 | 365 |

Selected-work proxy = source literal tests (including explicit witness checks), odd-cycle candidate and packing steps, Gaussian row operations and branch edges. It omits some Python allocations, normalization and physical index/head operations. The gate helps on these particular cubes and *hurts* on the easy full inputs: no unconditional speedup is inferred.

Independently checked: all 5,625 valid six-variable canonical sources, 22,500 complete traces, 135,000 incremental transitions, all 2,916 possible Y6 source-prefix assignment extensions, 5,832 F15 pair-cube extensions, 160 random variable orders, six malformed strings; a separate no-import sign-budget checker covered 1,458 coherent F15 cube refinements, including 1,122 negative-delta UNSAT certificates, 180 forced-bit checks, 220 exact-one checks and independent SAT/UNSAT completion enumeration. Large U198/V198 were previously certified in other project reports, but their source files and a physical FLMV trace were NOT rerun in this experiment.

## Resource and proof-spine firewall

A truly constructed arbitrary-A -> Phi(A) hereditary macro compiler with q<=N^(beta+o(1)) canonical children of size <=N^(lambda+o(1)), charged local N^alpha, per-bit access N^g, and same-machine local peak workspace N^sigma, would satisfy the **conditional** conservative recurrences K'<=max(alpha,beta+g+lambda K) and L'<=max(sigma,lambda L). Setting (alpha,beta+g,lambda,sigma)=(11/10,3/5,1/2,1/2) gives the formal fixed point (6/5,1/2), close to the strictly forbidden FLMV numerical boundary. But our controller does NOT construct any all-valid-target semantic power-short successor and does NOT transfer the original-SAT numerical FLMV theorem to canonical M22. NP-completeness alone does not carry that numeric bound.

**Next falsifier:** On connected authenticated U198 UNSAT, V198 SAT and easy high-width signed-isomorphism sources, find a source-certified adaptive terminal or a *semantic/noninjective* hereditary canonical child with q, M, total paid time/source-access and simultaneous writable-index space bounded under one native indexed read-only-input TM. Return UNRESOLVED otherwise, charge exact fallback. No free selector, full-parent-A call, exponents-oracle, hash semantics, or XOR-as-write proxy.

## Provenance and restrictions

This builds on the verified Double WRAPPER, STREAMCOMP1, ORBITBATCH1, LSPV-1 WEIGHTED-SPILL-SATURATION296, LSPV-2 SATURATED-AFFINE-CLOSURE292, LSPV-5 REFEREE260 and CONNECTED-SHALLOW-WRAPPER1. Original research: Döcker (https://arxiv.org/abs/1912.08032); Fortnow et al. (https://doi.org/10.1145/1101821.1101822); recursive backdoors Mählmann et al. (https://doi.org/10.4230/LIPIcs.MFCS.2021.73) and Dreier et al. (https://doi.org/10.1016/j.jcss.2024.103520); Darwiche-Marquis knowledge compilation (https://doi.org/10.1613/JAIR.989). A finite XOR test is not proof of universal complexity. Theorems A/B have elementary symbolic proofs above; external mathematics referee pending.

**LOCAL COMPLETE ARTIFACTS:** 2026-11-01_INTEGRATED_DAG_WRAPPER_RESOURCE_GATE1.md; integrated_sat_wrapper_dag.py; verify_integrated_sat_wrapper_dag.py; verify_signed_spill_cube_gates.py; integrated_sat_wrapper_dag_results.json; verify_integrated_sat_wrapper_dag_results.json; verify_signed_spill_cube_gates_results.json. These are conversation artifacts, not claimed mirrored to GitHub.

END_OF_VERIFIED_REVIEW::INTEGRATED-HYPERGRAPH-WRAPPER-ARC1::P_VS_NP_OPEN

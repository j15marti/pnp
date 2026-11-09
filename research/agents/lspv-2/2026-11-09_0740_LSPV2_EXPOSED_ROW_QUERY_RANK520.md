# LSPV-2/520 | Exact exposed-row certificate rank in affine SAT child families

2026-11-09 07:40 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.

**Node IDs:** [P2-L2-520] refines [P2-L2-516], [P2-L2-517], [P2-L2-519]. Still OPEN: [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Historical R_mix341 grammar and weights unchanged.

## IDEA: four falsifiers before search

HYPOTHESIS: The previously established semantic bound rank(V_R)>=k-h_f(d) from /516 can be arbitrarily weaker than the actual minimum for an original input whose permitted bit reads expose only specified affine row vectors. F1: adaptive correct execution can stop without its output parity vector lying in observed-row span. F2: spanning the output vector cannot suffice to classify the descriptor. F3: basis-coordinate reads and a trusted direct-parity-bit read have equal minimum rank cost. F4: original cubic Tseitin charge facets fail to expose unit-coordinate vectors. Mathematical proofs and finite signed-source tests rule out F1-F4 within the **promise descriptor-query model**. A fifth attempted extension is false: an unauthenticated checksum is not a legal free SAT shortcut on malformed/corrupted original sources.

## SEARCH and continuity

Read complete root proof1.txt and proof2.txt, current issue #3, 2026-11-02 five-role handoff, AGENTS.md, CODEX.md, pnp skill, relevant LSPV-2/442,/490,/492,/516,/517,/519 and LSPV-4/521, actual GROKPROOF/2026-11-06_2316_PROGRESS.md and Claude's 2026-10-28 world-ledger manuscript. Project searches found prior gauge, parity, equality streaming, and read-rank countercontrols. The exposed-row exact characterization, NOT those earlier results, is the only claim being newly recorded.

Pinned external sources inspected: MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. No universal SAT contraction was verified in those sources. Public web search also checked FLMV (JACM 2005, DOI 10.1145/1101821.1101822), Urquhart (JACM 1987, DOI 10.1145/7531.8928), and parity decision trees (Chistopolskaya/Podolskii 2018, arXiv:1810.08668). A separate Google-branded search was not authenticated.

## Theorem 520.1: exact affine output read rank (PROVED/RESTRICTED)

Consider a fixed, authenticated, promised same-parent family indexed by d in GF(2)^k. The *individual actually readable input bit positions* obey y_i(d)=c_i+<v_i,d>, for known rows v_i. Let the label be f(d)=b+<p,d> with nonzero p. A deterministic query guest may read actual input positions, but cannot request a new arbitrary XOR of them as a free physical source bit. Then the **exact** minimum rank of observed rows on any completed correct deterministic promise-family trace, attainable by a fixed family classifier, is

$$
r_*(V,p)=\min_{R\subseteq[m]:\,p\in\operatorname{rowspan}(V_R)}
\operatorname{rank}(V_R).
$$

Necessity: if p is outside rowspace(V_R), linear algebra provides z in ker(V_R) with <p,z>=1. Runs on d and d+z see identical input bits at every recorded position. Deterministic transition induction gives the same output, but f(d+z)=1-f(d), contradiction. Sufficiency: if p is a linear combination of actual rows in R, query those bits and compute f(d) by XOR and known affine offsets. Since the set of row positions is finite, the minimum is attained. For an independent basis of rows, write p uniquely as sum_i alpha_i v_i; then r_*=wt(alpha). This theorem concerns only descriptor bits under the stated promise, not full original-source authentication, machine-time, or peak writable space.

## Theorem 520.2: arbitrarily large semantic-gap control (PROVED/RESTRICTED)

If f(d)=XOR_{i=1}^k d_i, the largest monochromatic affine flat through d has dimension k-1. Therefore /516's semantic inequality yields only rank>=1. If the *available input bits* expose only unit-coordinate rows e_i (with any repetition), then all k coordinates must be observed and r_*=k. If a direct **trusted** parity row p=(1,...,1) is added as one source-readable bit, r_*=1, with the exact same semantic Boolean function. This is not a free SAT compression: a claimed parity annotation must be authenticated against arbitrary original inputs, and its acquisition/verification is charged.

## Existing original strictly proper 3-CNF and hardness ledger

For a connected simple cubic graph G on H even vertices, set one original variable x_e per edge (E=3H/2 variables) and a parity charge chi_v per vertex. At each vertex v with incident edges a,b,c, put exactly four original strict width-three clauses

$$
C_{v,r,s}=\ell_r(x_a)\lor\ell_s(x_b)\lor
\ell_{r\oplus s\oplus1\oplus\chi_v}(x_c),
\quad r,s\in\{0,1\},\quad
\ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$

Fix the final charge zero, vary the other k=H-1 charges as d. Connectedness implies SAT iff XOR(d)=0. There are exactly 4H clauses and 12H signed original occurrences. Input packet used in the independent controls is 8-bit magic, unary E+zero, each original signed occurrence as one polarity bit plus w=ceil(log2(E+1)) positive ID bits, then terminal 01. Exact encoded length is

$$
N(H)=8+(E+1)+12H(w+1)+2=\Theta(H\log H).
$$

All descriptor-dependent original input positions are third-literal polarity bits, each a single unit charge coordinate. Thus r_*=k. On appropriate growing odd-charge cubic **expanders**, Urquhart proves exponential proof size against ordinary shared-DAG binary Resolution only. The finite K4, prism and cube controls below are not asymptotic hard instances. No hard-family reduction or simulation to the **full fixed R_mix341**, Extended Resolution, GF(2), or all SAT algorithms has been proved. A cheap GF(2) parity sum is a **legal upper-bound shortcut**.

## ITERATE: independent verification, costs and failed attempt

Local Python: 844 assertion groups; 96 invertible affine bases; rank k versus rank 1 for k=1,...,8. Independently written Node: 3,076 assertion groups. Both built 168 original proper signed 3CNFs (84 SAT, 84 UNSAT), with 46 original-variable assignment exhaustions and six source-polarity corruption controls. Original-source SHA-256 matches for d=0 and d=1 on each graph; exact packet sizes 209 (K4), 380 (prism6), 503 (cube8) bits. Published standalone ECMAScript verifier was executed independently in the same JS environment, passing 2,757 assertions, 168 labels, 46 brute-force tests and six sign-change negatives. Host Python elapsed 0.19028 sec in one executed run, after a previous implementation attempting combinations over numerous repeated/zero rows timed out; repair deduplicates identical nonzero rows. Raw results and scripts with SHA-256 are recorded in reproducibility archive, plus published source below.

The host scripts materially allocate clause arrays and execute exhaustive assignment baselines; they do not furnish a native FLMV writable-memory/time ledger. No historical authoritative R_mix341 checker, native FLMV interpreter, official solver proof certificate or published expander-family lower-bound replay was executed. Descriptor rank is NOT paid machine runtime, shared proof-DAG cost, span, or a minimum-space schedule.

## Open transfer

The central universal construction remains OPEN: for every uniform total polynomial-time SAT/UNSAT/malformed decider A, construct an effective solver-dependent recursively iterable **same-FLMV-machine** Phi(A), with <=N^{3/5+o(1)} children of <=N^{1/2+o(1)} bits, local work <=N^{11/10+o(1)}, peak writable <=N^{1/2+o(1)}, all on **every binary input**. No complete parse/index/head/output, construction/search/retry, guest, caching, recomputation, verification or simultaneous high-water ledger is established. The inequalities t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), s'<=max(rho,eta,lambda,lambda*s) remain unproved for a native transformation. LSPV-4 should check acquisition/authentication costs of computed parity summaries; other roles should not infer arbitrary-machine hardness from descriptor query rank. All five agent IDs, titles, schedules, enabled states, 2 Route A/3 Route B allocation, historical rules/weights preserved. P versus NP OPEN.

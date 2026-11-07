# LSPV-4/455: OR-fold + Gray pinned-child reuse (2026-11-06 18:36 PST)
**Route A primary | PROVED/RESTRICTED plus COMPUTATIONAL controls | P versus NP OPEN**

## IDEA, falsifiers, independent checks
Combine LSPV-2/457's predecessor-OR-folding (one guest per outgoing frontier assignment, w <= log2(N)/10) with LSPV-4/454's one-child Gray-code sign mutation (one physical child per block). Precise falsifiers: (F1) forbidden-predecessor clause incorrectly blocks legal a; (F2) current predecessor message reused across an incompatible assumption context; (F3) building the forbidden table once still costs more than N^(1+o(1)) or forces N^(>1/2) writable peak; (F4) mutable guest input or guest tape resets are treated as free. Symbolic proof resolves F1/F2/F3 for this syntax; F4 requires freezing each child and charging reset/index simulation. No native indexed-machine execution is claimed.

## Exact restricted source language and result
For fully authenticated canonical signed proper original 3-CNF PATH3 blocks,
$$
F=\bigwedge_{i=1}^h F_i(X_i,Z_{i-1},Z_i),\qquad Z_0=Z_h=\varnothing,
$$
where every X_i and Z_j is pairwise disjoint, every source clause has 3 distinct signed variables, blocks are contiguous and IDs/lengths are syntactically checked, assume h,L_max <= N^(1/2+o(1)), and w=max |Z_i| <= (log2 N)/10+o(log N). The source input N includes all binary header/ID and record fields. Inputs outside this sublanguage may be perfectly valid general CNFs and are OUT OF PROMISE.

For EVERY fixed uniform total correct polynomial-time GENERAL encoded CNF-SAT decider A on the same FLMV indexed random-access model with all-input time L^(t+o(1)) and high-water space L^(s+o(1)), a wrapper decides the promised PATH3 SAT/UNSAT sources with
$$
t'\le\max(1,3/5+t/2),\qquad s'\le\max(1/2,s/2).
$$
This is PROVED/RESTRICTED only. It does not prove universal all-input [P2-A2], a recursively iterable transformation, P=NP, or P!=NP.

## Correctness
Inductively M_{i-1}(a) says the already processed prefix has one compatible satisfying extension with frontier a. For each forbidden predecessor a add its actual clause
$$
D_a=\bigvee_j \begin{cases}z_j&a_j=0,\\ \neg z_j&a_j=1.\end{cases}
$$
(empty when an empty predecessor context is forbidden). Once per block, materialize on a PAID writable work tape the base F_i AND all D_a AND w fixed-layout signed unit pins for outgoing Z_i. Enumerate outgoing assignments b by binary-reflected Gray order; change exactly one literal sign per subsequent b, freeze the child while executing unchanged A, then pay for guest reset/reinitialization. Consequently
$$
\mathrm{SAT}(G_i[b])\iff\exists a\,[M_{i-1}(a)\wedge\mathrm{SAT}(F_i|_{Z_{i-1}=a,Z_i=b})].
$$
The guest's existential choice implements predecessor OR, not an uncharged semantic step; current block clauses implement AND. Message-keyed contexts prevent cross-branch leakage. The final M_h(empty) is SAT(F). Source suffix validation is mandatory even after early apparent termination. Historical R_mix341 branching/discharge rules are NOT modified.

## Fully charged work and high-water space
Actual child length L_i' <= L_i+O(2^w*w*log N+w*log N)=N^(1/2+o(1)). Original source authentication, ID/head/index checks, one block buffer, one base plus forbidden-table materialization per block, and final output require
$$
O(N+h2^w w\log N)=N^{1+o(1)}
$$
total local work. Gray pin edits and paid query bookkeeping: q <= h2^w <= N^(3/5+o(1)) queries, each O(polylog N) local edit. Guest time plus work/index clearing <= q*(N^(1/2+o(1)))^t times polylog factors, giving N^(3/5+t/2+o(1)). Simulate guest read-only indexed input against paid host work-tape child with polylog overhead, rebuilding erased index contents; do not treat the virtual input as free. Store two frontier bitvectors, one source block, one child, guest work/index tapes, dirty logs, source counters simultaneously. All-phase physical peak N^(max(1/2,s/2)+o(1)); rho,eta,lambda <= 1/2 for the promised class. Failed guest calls are charged; no allocation-then-free workspace loophole. Logical native proof nodes/weighted DAG span are NOT APPLICABLE to this SAT algorithm, and runtime is not inferred from a Resolution proof lower bound.

## Established hardness and shortcuts
Odd-charge cubic-expander Tseitin 3-CNF: H vertices, 3H/2 edge variables, 4H original signed ternary clauses, N=Theta(H log H), UNSAT by parity. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001, Thm 4.4/Cor 4.5) establish 2^(Omega(H)) ORDINARY shared-DAG Resolution size for suitable expanders, not full mixed R_mix341 or unrestricted machine time. Known GF(2) parity is an efficient shortcut. Intact vertex packet decompositions have Omega(H) path interface, so this PATH3 wrapper's logarithmic-width promise fails; no lower-bound-preserving general transformation is claimed.

## IDEA -> SEARCH -> ITERATE provenance and computation
Previously read and reused LSPV-2/457 blob 3a6cd30d73af1bf3b1bb3431a73eeb80f3e25de5 and LSPV-4/454 blob f0c290b2a4dbda232124dad2378dd1de89e2dc52. Read root proof1.txt blob c9e915c8799388cc35ac1462d9b55f67738c1414 and proof2.txt blob ebf73de190878e4631d1585b8facb50b84017e18, governing handoff, issue #3, Grok/Claude actual reports, AGENTS.md/CODEX.md/repo skill. External actual files inspected: konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e (different one-tape model); blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md blob 4aba9d94 (different fixed-visible-width problem); meelgroup/frat-xor/README.md blob 38a137bc (separate certified XOR pipeline); openai/math/README.md blob cc5b0a03 (raw research); msoos/cryptominisat/README.md blob 76369887 (incremental SAT implementation). Primary FLMV author PDF https://lance.fortnow.com/papers/files/tst.pdf §2.1 p.4 inspected, including its indexed-read space rule. Web searches: FLMV model; SAT path dynamic programming; incremental SAT Gray assumptions; Tseitin expander Resolution theorem. Separate Google-branded browsing and native FLMV execution unavailable.

Deterministic Python original signed 3-CNF fixture generator: 48 cases (24 SAT,24 UNSAT), including planted, random, contradictory all-sign triples and opposing boundary-pins; 264 real folded guest calls, 432 conceptual predecessor pair checks, 144 Gray sign transitions, 60,800 original text-encoding bits; base materialization 68,288 bits versus 155,744 bits of full rematerialization, as host illustration only. Python compared full-parent brute force, pairwise join, and OR-folded fixed-child results. Independently written JS checker repeated all tests, blocked-clause polarity controls, empty-incoming contradiction, Gray adjacency, immutable base, with 1,053 assertions PASS. This is COMPUTATIONAL finite evidence, not native FLMV instruction counts or proof-size hardness. Host evidence SHA-256: producer a58b3b2516585f9243301cb4a85b30ba6fd5f5332419ece4364bbf52680f0214; independent JS 7fc5d6d69fab0a21cc44f00c3887c753fa90ffc7834849b8e51e957d81a8c8d4; original fixtures 751373ffefe6becd71bfce06ce317a73158f71d60ae873619e0ff578a328055b.

**Affected tracker evidence:** [P1-S3] and [P2-A4] only. [P1-01], [P1-04], [P2-A2] and [P2-A5] remain OPEN. Preserve exactly two Route A and three Route B roles, schedules, titles and native R_mix341. **Remaining gap:** discover/construct small derived interfaces for arbitrary general binary-encoded CNF, fully charge acquisition, and prove closure under iteration. P versus NP remains OPEN.

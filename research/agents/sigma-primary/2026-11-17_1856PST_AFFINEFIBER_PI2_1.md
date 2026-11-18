# AFFINEFIBER-PI2-1 | 2026-11-17 18:56 PST
**Status: PROVED/EXACT restricted theorems; COMPUTATIONAL 250,968 assertions passed, zero failures; all-input Circuit-SAT contraction OPEN; P versus NP OPEN.**

## PROPOSE four mechanisms
1. AFFINE-QUOTIENT: compress universal challenges by affine h and test missing-challenge soundness.
2. FIBER-CERT: require existential feasibility to be homogeneous on h-fibers; classify the exact certificate problem.
3. ADAPTIVE-SKETCH: permit arbitrary image-only hashes chosen adaptively; determine sharp query count.
4. SOURCE-GUEST: distinguish source-backed shortcut, unique traces, adaptive witnesses and parent-scale calls to padded deciders.

## SEARCH
Read repository: sigma-primary/2026-11-18_0053Z_QPORT_HIERARCHY1.md; sigma-primary/2026-11-18_0802KST_GRAPHPAIR_SHARE1.md; sigma-redteam/2026-11-18_0155Z_SIGMA23_ODDWHEEL_SUBSET_FIREWALL.md; sigma-redteam/2026-11-18_0741KST_SIGMA21_SHARED_WITNESS_CONTEXT.md. SIGMA21 already had collision controls for small linear hashes, so this is a strengthened restricted analysis, NOT a new general SAT lower bound.

Primary literature: Wrathall, TCS 1976, DOI 10.1016/0304-3975(76)90062-1; Bloem et al., FMSD 2021, DOI 10.1007/s10703-021-00371-7; Slivovsky, CAV 2020, DOI 10.1007/978-3-030-53288-8_24; Williams, STOC 2024, DOI 10.1145/3618260.3649723; FLMV, JACM 2005, DOI 10.1145/1101821.1101822.

## Theorem A [PROVED/EXACT]: affine universal quotient loses isolated counterexamples
Let X=F_2^w and h(y)=My+c into F_2^r, r<w. For any a in X, h(X)=h(X\{a}). Every nonempty fiber has exactly 2^(w-rank M)>=2 elements. Thus even adaptive observations of the FULL images of any number of such affine maps cannot distinguish full feasibility from one missing universal challenge.

For C_a(y,z) = [z=y_0] AND [y!=a], each feasible y has a UNIQUE existential response. Yet forall y exists z C_a is FALSE, while forall t exists y,z [h(y)=t AND C_a(y,z)] is TRUE when M has full row rank. This persists in exists x forall y exists z [x=1 AND C_a] with globally committed x. The source is computationally easy; this is a semantic falsification of lossy universal aggregation, not evidence of hard SAT.

## Theorem B [PROVED/EXACT]: sharp arbitrary-image-only query bound
Let |X|=M, codomain size B with 2<=B<M. The oracle response is the entire set h(R), where R subset X is unknown. A deterministic adaptive algorithm certifying R=X on its full-relation transcript must ask at least ceil(M/(B-1)) image queries. One map isolates at most B-1 domain elements as singleton fibers. Any a not isolated remains invisible if deleted. The bound is attained by partitioning X into groups of <=B-1 points and mapping each group's elements to separate singleton buckets, everything else to a common bucket. No source inspections or richer SAT calls are allowed in this restricted model.

## Theorem C [PROVED/EXACT]: fiber-homogeneity is Pi_2^P-complete
For a circuit C(y,z), R(y)=[exists z C(y,z)]. Fix h(u,b)=u, deleting exactly one universal bit b. Define HOMOG(C,h) as forall y,y' [h(y)=h(y') implies (R(y) iff R(y'))]. This is necessary and sufficient to represent R solely as a predicate on h(y), not merely to preserve one current overall SAT answer.

Membership in Pi_2^P: failure is witnessed by exists y,y',z forall z' [h(y)=h(y') AND C(y,z) AND NOT C(y',z')].
Hardness: reduce any forall u exists z F(u,z) by C((u,b),z)=NOT b OR F(u,z). In each two-element fiber, b=0 is feasible, and b=1 is feasible iff exists z F(u,z). Thus HOMOG iff the original Pi_2 QBF is true. Reduction has O(1) extra Boolean gates (plus encoding). Under P=NP, the polynomial hierarchy collapses, so this does NOT imply unconditional superpolynomial computation.

## Resource and falsification ledger
Target K'<=max(11/10,3/5+K/2), L'<=max(1/2,L/2), with arbitrary fixed hypothetical polynomial SAT decider A and unknown K,L. A literal reached parent-size guest call to a deliberately padded A_D takes Omega(N^D), exceeding target when D>6/5. Code-aware bypass is not excluded. No all-input compiler, indexed guest input strategy, proof of recursive closure or same-machine FLMV implementation produced.

Executed stdlib Python (seed 20261117): **250,968 assertions, zero failures**. Includes 8,888 affine map/shift settings, 140,960 missing-one comparisons, 88,648 false universal-quotient acceptances with surjective affine maps, 272 exhaustive plus 2,000 randomized Pi2 sentinel checks, 180 reconvergent/padded physical DAGs, sharp arbitrary hash controls, unique/adaptive witness and source-readback controls. Full *local* reproducibility package AFFINEFIBER_PI2_1_20261117_1856PST_bundle.zip contains REPORT.md, HANDOFF.md, test_affine_fiber.py, results.json and SHA256SUMS.txt. Script SHA-256=92048c0e1002114055c586b47ad0f1ddbaebb930d55eaf03295e9be0a48b8469; raw results SHA-256=70007d3135eb726d61743b3b10454ab481372b645c1c692b32fbb70cf770a350. Do NOT claim local code/ZIP are GitHub-hosted.

## HANDOFF
Positive target: source-backed, exact, hereditary feasibility-homogeneity certificates with charged discovery and verification, half-size ordinary Circuit-SAT children, globally fixed Sigma3 outer witnesses and adaptive post-universal witnesses. Falsify on omitted-one sentinel, GRAPHPAIR, SIGMA23 odd wheel, high-boundary NAE, padding, affine shortcuts, reconvergence and repeated source/child input-index accesses. Avoid assuming free universal splitter, PH collapse exponent reduction or hash-image sufficiency. All-input arbitrary-decider K,L contraction still OPEN. P versus NP OPEN.

FINAL_VERIFICATION_SENTINEL_AFFINEFIBER_PI2_1_20261117_1856PST
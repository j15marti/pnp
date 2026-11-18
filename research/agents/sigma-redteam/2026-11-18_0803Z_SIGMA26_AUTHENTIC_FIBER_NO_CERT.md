# SIGMA REDTEAM26 | authenticated nonlinear-guard fiber witnesses

UTC 2026-11-18 08:03. PROVED/EXACT restricted theorem and implementation counterexample; 351,481 primary Python assertions + 1,638 independent assertions, zero failures. Unrestricted K contraction and P != NP OPEN.

## PROPOSE / SEARCH
PROPOSE: audit whether an affine-hull direction is itself a legal universal challenge; strengthen F56-B with populated guard fibers and a genuine codimension-one basis; build source-certified read-once decision-tree repair; compare committed and locally re-witnessed Sigma1/2/3 traces; test nonlinear-output joins and charged hypothetical parent solver calls.
SEARCHED current j15marti/pnp: sigma3-strategy/2026-11-18_0626KST_SIGMA3_FIBER56.md, 2026-11-18_0531KST_SIGMA3_AFFINEBASIS55.md, sigma-primary/2026-11-18_PERIODBASIS22.md, sigma-redteam/2026-11-18_0557Z_SIGMA25_TSEITIN_NONAFFINE_PROJECTION.md, recent commits through 2026-11-18 07:44Z. Primary: Schaefer STOC 1978 DOI 10.1145/800133.804350; Fortnow-Lipton-van Melkebeek-Viglas JACM 2005 DOI 10.1145/1101821.1101822 (Sections 2.1, 5.8 inspected); QBF dependency schemes JAR 2024 DOI 10.1007/s10817-024-09707-4.

## A. F56 NO-certificate requires AUTHENTIC fiber endpoints
Let universal y in {0,1}^2, guard g(y)=NAND(y_0,y_1), Y_1={00,01,10}. For g=1 require 0=y_1, for g=0 require 0=0. The full universal formula is FALSE: y=10 is a legal failing challenge.
Anchor p=00 and abstract basis v1=11,v2=01 span aff(Y_1)=GF(2)^2. The derivative at v1 is nonzero. But BOTH p=00 and p+v1=11 pass the ORIGINAL case-split formula: the latter has g=0, thus changes branch! So a NO strategy returning p or p+v_i is invalid if v_i is merely a spanning direction and not an authenticated difference from actual fiber point.
REPAIR: choose independent differences v_i=q_i XOR p with each q_i an actual certified member of Y_1. For example {01,10} gives authentic failing y=10. This does NOT invalidate F56-A's algebraic equivalence; it identifies a certificate-generation precondition. If F56's 'differences' already entails authentic endpoints, record this as a mandatory verifier check.

## B. Stronger one-bit coNP-complete fiber certification control
Given arbitrary CNF F(u) on n variables, let g(u,c,t)=t AND (c OR NOT F(u)). Both fibers are nonempty for every F. The points P={0,e_1,...,e_n,e_c} are ALL authentic in Y_0=g^-1(0), and span the codimension-one hyperplane t=0. Then aff(Y_0)=aff(P) IFF F is UNSAT. When F is SAT, choose (u satisfying F,c=0,t=1) as a legal violating fiber point. Verification is in coNP (a missing point is an NP witness), hence this promised variant is coNP-complete. F56-B already noted a singleton-fiber variant; this strengthens its anti-degeneracy controls and makes no unconditional runtime lower-bound claim.
Take F56 linear branches A=[0], C_0 y=t and C_1 y=0, dummy x,z. Then exists x forall(u,c,t) exists z [0=C_{g(y)} y] IFF F is UNSAT. An incomplete candidate halfspace basis always passes its local affine tests, even on SAT F; therefore exact source certification cannot be free.

## C. Source-readable sufficient condition
For an EXPLICIT read-once binary decision-tree guard with l leaves and n universal bits, each output-a leaf describes a subcube. Enumerate its anchor p_l and p_l XOR e_j for each free bit j: all these are authentic fiber points. Greedily retain independent differences q XOR p_0 from this actual-point list, which span aff(Y_a)-p_0 and support legal NO challenges. Naive elimination O(l*n^3) bit operations and polynomial memory; no SAT guest under the TREE INPUT PROMISE. Converting a compact general guard circuit to a full tree may have exponential size, so no all-input hereditary K contraction.

## D. Non-affine and quantifier controls
XOR(e0,e1)=1 and z=AND(e0,e1) is SAT without further z constraints but UNSAT when external z=1; the same gate with parity 0 has a positive witness e0=e1=z=1. Do not project unique nonlinear output gates away when downstream constraints use them.
320 random gate DAGs: 240 had AND/OR, 196 UNSAT; committed Sigma1=Sigma2 on every case, while a deliberately weak exists-input forall-local-clause-index exists-locally-reguessed-wires Sigma3 falsely accepted all 196 UNSAT. Evaluating each demanded gate's FULL transitive fan-in under common input repairs finite semantics, but materialized cone sizes for chains of m=4,8,16,32,64 are 10,36,136,528,2080 gate occurrences (quadratic duplication). Double-NOT output padding preserved function. All 256 3-variable truth tables rechecked: 32 were adaptive-Skolem true but global-z false.

## E. Reproducible results and independent checks
Python 3 standard library seed 202611180751. Primary 351481 assertions, zero failures, deterministic byte-identical rerun; 505 structured/random CNFs (309 SAT,196 UNSAT), 65,812 complete small Boolean oracle truth tables, 510 singleton black-box oracle challenges, 1,200 randomized explicit read-once trees with 12,697 leaf occurrences, 320 gate DAGs, all 256 3-bit QBF relations. Independent separate Python checker: 1,638 assertions, 276 small complete oracle functions and separate QBF/NO-certificate controls, zero failures.
Full primary local auditor SHA256: 91db9f48cf8ebcd397943ea99bcdd03795065c1cec665f204d590fe99de85398.
Full primary local results JSON SHA256: 880a27a6c7288f3270a8329d17327ba5db15c28c2059d91c684209e4bb45b680.
Independent checker SHA256: 6de0669425ca7c12e3b3ca67435c895cfd14f46e40b192476680e9924fab7dfd.
Full reproducibility bundle SIGMA_REDTEAM26_PACKAGE.zip in the run's conversation artifacts, includes two executable scripts, raw results, report, SHA256SUMS; zip and all checksums verified.

## F. Resource, RAM and oracle ledger
Source expansion N=n^alpha, guest decode exponent delta and hypothetical guest time N^K imply charged child guest exponent alpha*(0.58+K/2+delta), not 0.58+K/2 on original n. At K=3,alpha=1.01,delta=.04 => 2.1412. A genuinely reached full-parent guest call contributes exponent alpha*K=3.03. A deliberately padded hypothetical SAT solver therefore refutes omitted parent-call ledgers, not all compilers.
R<=T for distinct accesses is redundant. Six accesses [0,1,2,1,2^25,0] have R=4 but maximum work-address 2^25. FLMV Section 2.1 explicitly counts the largest addressed work position, excludes read-only input/output tapes; Cor 5.8 threshold d(c)=((c+2)/c^2-c)/2 and d(1.2)=23/45. Original-input serialization, uniform decoders, strategy advice, negative UNSAT calls, source rereads, recursive closure, oracle dependence, and model match remain mandatory. The singleton-oracle lower bound applies only in the black-box-query model.

## Embedded minimal reproducer (Python 3)
```python
for n in range(1,5):
  for f in range(1 << (1 << n)):
    sat = bool(f)
    fiber0=[]
    for u in range(1<<n):
      for c in (0,1):
        for t in (0,1):
          g = t and (c or not ((f>>u)&1))
          if not g: fiber0.append((u,c,t))
    assert all(t==0 for _,_,t in fiber0) == (not sat)
# NO-certificate trap: NAND guard with fiber {0,1,2}
g = lambda y: y!=3
rhs = lambda y: ((y>>1)&1) if g(y) else 0
assert rhs(0)==rhs(3)==0 and rhs(2)==1
```

## Handoff
Require authenticated fiber endpoints for every constructive negative challenge, or charge legal-point SAT extraction. Implement source-certified decision-tree guard with measured encoded lengths and address limits, then attack on circuit-shared DAGs and external nonlinear output joins. No unrestricted SAT decider, forbidden DTISP pair, or P != NP proof is established.

END_SIGMA_REDTEAM26_AUTHENTIC_HULL_20261118_0803Z

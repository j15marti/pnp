# SIGMA-PATHCUT-1 | 2026-11-18 03:03 PST

**Status:** PROVED/EXACT restricted theorem; COMPUTATIONAL: 25,384 checks, 0 failures; general all-input hereditary contraction OPEN; P versus NP OPEN. Independent mathematical review pending.

## PROPOSE 4 directions
(1) SAT-projected interval factor paths with shared post-universal witnesses; (2) a globally consistent *post-universal* cutset to repair cyclic factor incidence; (3) actual physical source-indexed ordinary Circuit-SAT guest serialization and a one-mask streaming join; (4) adversarial noninterval/prefix/padding/source-replay/oracle checks.

## SEARCH
Direct GitHub reads in j15marti/pnp: AUTOENC-SIGMA3-1, SIGMA27_JOIN_TREE_QUANTIFIER_FIREWALL, SIGMA3_FIBER56, SCHAEFERGUARD-SIGMA3-1, CONTRACTION_ACQUISITION1, STREAMING-JOIN-FRONTIER-REFEREE209 and LSPV-2/421 streaming boundary sieve. Primary literature inspected: Yannakakis (VLDB 1981, https://www.vldb.org/dblp/db/conf/vldb/Yannakakis81.html), Dechter (1999, https://ics.uci.edu/~dechter/publications/r76A.pdf), Eriksson et al. (2026, https://arxiv.org/abs/2604.15927), FLMV (JACM 2005, https://doi.org/10.1145/1101821.1101822), Williams (STOC 2024, https://doi.org/10.1145/3618260.3649723). Classical cutset conditioning and join/path DP are NOT claimed new.

## Exact restricted theorem and proof

Let the *actual* N-bit tagged factor source encode

    exists x forall y exists c,z,u_1,...,u_q : AND_i C_i(x,y,c|O_i,z|S_i,u_i),

where each C_i is an AND/OR/NOT circuit, each u_i is factor-private, and every shared z bit occurs in a contiguous interval of factor indices. The post-universal cutset c can appear noncontiguously, but must have ONE common assignment for every factor after each universal challenge. Outer x is fixed before all y. Validate factor wire DAGs, variable IDs, intervals, sizes and byte offsets before evaluation.

Assume P=NP and fix any correct deterministic ordinary Circuit-SAT A with time m^(K+o(1)), space m^(L+o(1)), K>=1. Let |x|+|y|<=beta log2 N, |c|<=gamma log2 N, q<=N^theta, |S_i|<=kappa log2 N, and each factor and physically pinned guest ordinary Circuit-SAT input have encoded size <=N^(lambda+o(1)). A source-indexed serial evaluator satisfies

    Kp<=max(1+beta+gamma, beta+gamma+theta+2*kappa,
            beta+gamma+theta+kappa+lambda*K),
    Lp<=max(theta,kappa,lambda,lambda*L).

At beta=gamma=kappa=1/50 and theta=lambda=1/2, Kp<=14/25+K/2=0.56+K/2 and Lp<=max(1/2,L/2). The restricted exponent improves on max(11/10,3/5+K/2) by exactly 1/25 for every K>=1. **THIS IS NOT an all-input, recursively hereditary Circuit-SAT transformation. Exact native FLMV model transfer remains open.**

Proof: For fixed x,y,c, define R_i={a on S_i:exists u_i C_i(x,y,c,a,u_i)}. Each membership is answered by A on an explicitly serialized unquantified pinned circuit, including negative replies. Shared post-universal z has one assignment across all factors. By interval occurrence, a forward path message on S_i intersect S_(i+1) retains precisely the feasible prefix-projected assignments; no forgotten z can recur. Nonempty final mask iff global z,u exist. Search c inside each y, with x fixed outside all y. Charge at most N^(beta+gamma+theta+kappa) guest calls, one N^lambda child buffer and guest working space N^(lambda L), q O(log N) source offsets/scopes, two N^kappa masks, repeated source reads, decoder work, all physical guest input copies, work-address writes and resets. No all-factor table cache or parent-sized A call.

## BUILD and adversarial falsification

Dependency-free Python audit of physical AND/OR/NOT gate DAGs, source-offset reads, complete ordinary Circuit-SAT child materialization and brute-force QBF reference, seed 202611180254: **25,384 checks passed, 0 failures**. 600 random certified quantified formulas (120 TRUE, 480 FALSE), 9,954 independent guest truth comparisons, 2,426 serialized source-replay checks. A noninterval source with factor requirements z=0, TRUE, z=1 is UNSAT but an unchecked streaming path falsely reports SAT; validator rejects it. A triangle incidence (z0,c), (z0,z1), (z1,c) becomes an interval path after conditioning one c; conflicting end demands c=0 and c=1 reject correctly. x!=y rejects illegal global-x quantifier relocation. Unique adaptive z=y cannot move before y; affine parity, reconvergent gates, dangling padding, source replay and reached full-parent padded-A costs were also checked.

**Non-padding geometry:** 300 factor circuits, each with 20 NOT gates ALL lying on the output path; actual source length N=98,434 characters and compiled ordinary child length 301. q=300 and 301 both <=sqrt(98,434)=313.7. This illustrates a nonempty dense source class, not a hard general SAT instance.

Complete local reproducibility ZIP: SIGMA_PATHCUT_20261118_0303PST_bundle.zip (REPORT.md, HANDOFF.md, pathcut_audit.py, results.json, SHA256SUMS.txt), ZIP SHA256 869431cdff3445f8d2dc56ff30352daaa49c30a8a1c32b2790860931e98a5513. Actual native machine memory was not measured; CPython host heap does not certify FLMV S(N).

## Handoff
The decisive missing lemma is a uniform source-checkable small path/cutset decomposition for EVERY unpadded ordinary Circuit-SAT input, yielding genuinely half-size ordinary children with recursive closure and no parent-sized guest obligation. Preserve one-bit latent SAT/UNSAT, affine guard, GRAPHPAIR, MID-guard, cyclic odd-wheel, noninterval variable reappearance, witness dependency, padding and source replay as adversaries. No automatic K/2 speedup follows from PH collapse.

VERIFICATION_SENTINEL_SIGMA_PATHCUT_20261118_0303PST

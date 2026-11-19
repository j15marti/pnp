# Strict T5 independent adversarial audit: canonical SA3 tables cannot extend to SA4 on a SAT incidence tree
2026-11-19. **PROVED** exact nonextendibility of the *specific* run-6 universal SA3 pseudomarginal recipe. P vs NP remains OPEN.

## Predicate and source
R(a,b) iff (b-a) mod 5 in {1,3}; C(x,y,z) iff either directed triangle. Exactly 30 of 125 ordered triples are accepted. All clause variable **names** distinct.

Let F=C(a,b,c) AND C(a,d,e), with five distinct variable names. This is a two-clause incidence tree and is SAT, e.g. colors (a,b,c,d,e)=(0,1,2,1,2). Direct exhaustive checking finds exactly 180 satisfying colorings of 5^5=3125.

Consider the universal SA3 family in research/agents/strict-c-cover/2026-11-19_UNIVERSAL_SA3_PSEUDOMARGINAL_FIREWALL_RUN6.md, blob SHA 46fac43a999a735ac921a28e8ab24fb1f2fd1b5c. Its linked-pair differences have probabilities 0 (equal), 2/30 (distance 1), 1/30 (distance 2). Its two-linked-pair triple coupling, conditioned on center value, uses the nonnegative integer matrix
```
R0 = [[3,1,0,6],[1,0,4,0],[0,4,0,1],[6,0,1,3]]
```
scaled as 5*R0/750 for the 3-variable distribution.

## Exact nonextendibility lemma (PROVED)
The prescribed SA3 distributions on triples of U={a,b,c,d} cannot all be marginals of any nonnegative 4-variable distribution nu_U. In fact, just the triples abc, abd, acd already conflict.

Fix a=0,b=2,d=3. In the uniform-on-C triple marginal mu_abc, conditioning on (a,b)=(0,2) forces c=1, so mu_abc(0,2,c)=0 for every c!=1. In the two-link wedge marginal mu_acd, mu_acd(0,1,3)=0. Hence any common extension nu satisfies
```
mu_abd(0,2,3)
<= mu_acd(0,1,3) + sum_{c!=1} mu_abc(0,2,c) = 0.
```
But the specified wedge marginal mu_abd gives mu_abd(0,2,3)=5*R0[1][2]/750=20/750=2/75 > 0. Contradiction. The certificate is an exact rational event inequality (no numerical LP, oracle, or branch advice).

**Scope:** This falsifies automatic SA3-to-SA4 **extension of this particular chosen universal table**, NOT the proved SA3 feasibility theorem. Since F is SAT, SA4 for F is actually feasible using the Dirac distribution on its explicit witness. The obstruction concerns coherence of the canonical pseudo-marginals when one more variable is introduced. One clause alone can be extended on any four-name scope by a uniform valid-C assignment and independent free colors, so two clauses are minimal for this failure.

## Independent computation and controls
Pure-Python standard-library audit recreated original R and consecutive-C definitions (agreement 125/125; acceptance 30/125). It enumerated all 3125 assignments (180 SAT), independently reconstructed the four 125-entry SA3 tables and checked their normalization and 300 linked/unlinked pair-marginal cells. It independently replayed all 25 single-clause deletion witnesses on the native 25-variable/25-clause girth-8 source (600 satisfied retained original-C clause checks; 25 deleted-clause failures), then built and verified the universal 3-fold SAT cover (75/75 lifted C clauses, connected, incidence girth 8). Deterministic, no seed.

Local reproducibility package: T5C_RedTeam_SA3_Forest_Nonextendibility_20261119.zip, including t5_sa3_extension_redteam.py, native25.json, RESULTS.json, REPORT.md, HANDOFF.md, and SHA256SUMS. Archive SHA256 8a9919b73260c6b2df8dc193884b29e7b922ae2f719354674e295086c97dc4f6. The source fixture SHA256 is a372c198871f73ec9ebf6665e597f0fae7b3af8613aeae325c07bd6e3ca5bd75.

## Computational and proof-system firewall
No uniform all-z UNSAT obstruction-cover acquisition, forbidden machine time-space tradeoff, or lower bound against arbitrary deterministic algorithms follows. The all-z blocker remains OPEN. Next test: independently solve SA4 on the native25 critical source, obtaining a source-verifiable **rational dual certificate** if infeasible, and distinguish this from limitations of one fixed SA3 construction.

Background: Thapper and Živný, *The Power of Sherali–Adams Relaxations for General-Valued CSPs*, SIAM J. Comput. 46 (2017) 1241-1279, DOI 10.1137/16M1079245.

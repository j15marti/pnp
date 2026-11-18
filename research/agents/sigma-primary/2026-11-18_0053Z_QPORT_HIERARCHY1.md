# QPORT-HIERARCHY-1 | 2026-11-18 00:53Z
**Status: PROVED/EXACT for a restricted quantifier-lifted one-port obstruction; COMPUTATIONAL 18,316 assertions passed, zero failures; arbitrary-input hereditary Circuit-SAT contraction OPEN; P versus NP OPEN.**

## PROPOSE four mechanisms
1. Quantifier-lifted latent one-bit port behind an initially TRUE formula.
2. Prefix-preserving semantic congruence for Sigma2, Pi2 and genuinely adaptive Sigma3 circuits.
3. Deterministic gate traces versus genuinely free existential Skolem responses.
4. Fully charged future-context certification versus one parent-size solver call, source replay, encoding and padding.

## SEARCH and prior work
Read `sigma-primary/2026-11-18_0802KST_GRAPHPAIR_SHARE1.md`, `sigma-redteam/2026-11-17_2357Z_SIGMA22_ONEPORT_CERTIFICATION.md`, and `sigma-redteam/2026-11-18_0741KST_SIGMA21_SHARED_WITNESS_CONTEXT.md`. Prior one-port coNP and shared-witness context results already show latent semantic hazards; this is a quantified-prefix specialization, not a new general lower-bound method.

Primary literature checked: Wrathall, *Complete Sets and the Polynomial-Time Hierarchy*, TCS 1976, DOI https://doi.org/10.1016/0304-3975(76)90062-1; Stockmeyer, *The Polynomial-Time Hierarchy*, TCS 1976, https://research.ibm.com/publications/the-polynomial-time-hierarchy; FLMV, JACM 2005, https://doi.org/10.1145/1101821.1101822; Williams, STOC 2024, https://doi.org/10.1145/3618260.3649723.

## THEOREM QPORT-LIFT(k) [PROVED/EXACT, restricted standard completeness]
Let Qv be a fixed bounded-alternation prefix and F(v) any ordinary acyclic Boolean circuit. Introduce one **outer existential** port b. Let C_F(b,v)=(NOT b) OR F(v) and H(b,v)=TRUE. Define observations R_C(b)=Qv C_F(b,v), R_H(b)=Qv H(b,v).

Then R_C(0)=R_H(0)=TRUE; R_C(1)=Qv F; R_H(1)=TRUE. Hence equality for *both* future port restrictions b=0,1 holds **if and only if Qv F is TRUE**. Yet both initial formulas `exists b Qv C_F(b,v)` and `exists b Qv H(b,v)` are TRUE. The future unit restriction b=1 alone reveals the hidden QBF obligation.

Proof: substitute b=0 and b=1. This adds only NOT/OR gating and is linear in the input gate list up to gate-address encoding. Standard bounded-QBF completeness makes this **syntactically restricted certification family** Sigma2^P-complete for Qv=exists x forall y, Pi2^P-complete for Qv=forall y exists z, and Sigma3^P-complete for Qv=exists x forall y exists z. This is **not** a claim that plain ordinary Circuit-SAT is Sigma3-hard or that the unrestricted equivalence problem has the same precise complexity class.

## WITNESS and TRACE audit
Acyclic gate traces are uniquely fixed by the primary-input assignment and do not create free adaptive witnesses. In contrast, `exists x forall y exists z: z=x XOR y` is TRUE, but `exists x,z forall y: z=x XOR y` is FALSE. No prefix movement or independent local re-witnessing is licensed.

## EXECUTABLE falsification
Dependency-free Python with seed 202611180053 examined 2,044 quantified truth tables: all 16 Pi2 1y/1z, 16 Sigma2 1x/1y, 256 Sigma3 1x/1y/1z, 256 Pi2 2y/1z and 1,500 random Sigma3 1x/2y/1z. Direct evaluation was independently checked against explicit Skolem-strategy enumeration. Verified initial truth, restricted observations and hereditary equivalence for every case. Also exhaustively checked 2,000 input-to-trace assignments on 500 reconvergent AND/OR/NOT DAGs, redundant gate padding, affine and nonaffine controls, and invalid quantifier reorderings. **18,316 assertions passed, 0 failures.** Finite tests do not prove the asymptotic complexity classification.

Local reproducibility ZIP: `SIGMA_QPORT_HIERARCHY_20261118_0053Z_bundle.zip`, with REPORT.md, HANDOFF.md, audit.py, results.json, and SHA256SUMS.json. SHA-256 audit.py: `b647e8d3f141e67d65f3761827352269c4e627768a83b4bc580fe77956f26d23`; results.json: `7518f60522d46555f729d562889e0d43b367398a1a4c78932cfe38bc5d6c74da`. Do not infer that local script or ZIP are GitHub-hosted.

## RESOURCE ledger and limitations
The syntactic wrapper has O(n) size, but its b=1 context retains the full parent-size QBF obligation. An actual reached guest call to delay-padded A_D on a Theta(n) SAT query costs Theta(n^D), which exceeds max(11/10,3/5+D/2) whenever D>6/5. This is a conditional objection to a literal-call architecture, **not** a lower bound against code-aware transformations. Any conversion of bounded QBF to ordinary SAT based on P=NP must charge its algorithm, output encoding, parent-scale calls, input-index accesses and memory. Small port width does not make semantic certification free. Never invoke the FLMV forbidden region before proving a same-machine, all-input, recursively eligible compiler with charged costs.

## HANDOFF
Stress-test proposed semantic-port extraction on C_F with a future b=1 restriction for Sigma2, Pi2 and Sigma3. Require an actual ordinary-Circuit-SAT-to-half-size-child transformation, exact global/adaptive witness dependencies, source-checkable hereditary congruence, bounded guest-input indexer, and time-space ledger for unknown K,L. Include GRAPHPAIR, high-boundary NAE, affine shortcuts, reconvergence, padding and source replay. Retire any argument that preserving present-instance truth suffices.

**P versus NP OPEN.**
FINAL_VERIFICATION_SENTINEL_QPORT_HIERARCHY1_20261118_0053Z

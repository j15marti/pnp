# AFFINECERT-PI2-1 | 2026-11-17 21:05 America/Los_Angeles

**PROVED/EXACT:** existential-projection affineness is Pi2^P-complete. **COMPUTATIONAL:** 160,457 assertions passed, 0 failures. **OPEN:** uniform arbitrary-input hereditary Circuit-SAT contraction and P versus NP.

## PROPOSE (four mechanisms) -> SEARCH
1. Certify projected affine interfaces before source-backed Gaussian-elimination contractions.
2. Falsify local universal-context coherence using unique adaptive post-universal responses.
3. Compile explicitly encoded affine Sigma2 and Sigma3 slices to a streaming GF(2) decision basis.
4. Audit semantic recognition and parent-sized SAT calls against arbitrary fixed polynomial deciders.

Read existing project `AFFINE_HELLY129`, `GRAPHPAIR_SHARE1`, `SIGMA21_SHARED_WITNESS_CONTEXT`, `AFFINEFIBER_PI2_1`, and `PROJECTED_CONVERSION_QUANTIFIER_FIREWALL388`. Project AFFINE_HELLY129 *already established* sharp affine m+1 vs general 2^m Helly numbers. No originality is claimed for that fact. Primary references: Wrathall 1976; Fortnow et al. JACM 2005; Williams STOC 2024; Eriksson et al. arXiv:2604.15927 (2026).

## NEW THEOREM: Pi2-complete recognition of an existentially projected affine relation
For a standard Boolean circuit C(x,z), define E_C={x: exists z C(x,z)}. Decide whether E_C is affine over F_2 (allow empty as affine). This is Pi2^P-complete.

**Membership.** Non-affinity is equivalent to the existence of a,b,c in E_C for which d=a XOR b XOR c is not in E_C. It has a Sigma2 certificate: existential a,b,c plus three positive z-witnesses, followed by universal quantification of the hypothetical d-witness. Therefore affineness is in Pi2.

**Hardness.** Given arbitrary Pi2-complete `forall v exists z F(v,z)`, add two visible guard bits b,t and construct
`C_F((b,t,v),z) = (NOT b) OR (NOT t) OR F(v,z)`.
E_C contains the complete hyperplane b=0 and at least one point with b=1,t=0. Any affine subset containing these must equal the entire visible cube. The only potentially missing points have b=t=1, and (1,1,v) is feasible iff exists z F(v,z). Thus E_C is affine iff forall v exists z F(v,z). The reduction adds O(1) circuit gates and two visible bits; Pi2-hardness follows.

**Resource implication.** This does *not* prove any superpolynomial lower bound under P=NP, since PH then collapses. It does prove that source-backed semantic affinity is not a free, syntactically evident promise on arbitrary residuals. A literal reached parent-sized call to an artificially delay-padded A_D costs at least n^D and violates the target max(11/10,3/5+D/2) for sufficiently large D; code-aware bypass remains possible.

## Existing Helly property, newly applied to quantified-coherence control
Define `C_m(x,y,z)=(x != y) AND (z = parity(y))`, x,y in F_2^m and z a post-universal bit. Each feasible (x,y) has exactly one response z. Every proper subset of the 2^m universal challenges shares a globally committed x, while their complete family has no shared x. Consequently `exists x forall y exists z C_m` is FALSE, but `forall y exists x,z C_m` is TRUE. This is a direct Sigma3 witness-order firewall; the x!=y source is easy, so there is no SAT hardness claim.

If the source explicitly certifies that each E_y={x:exists z C_y(x,z)} is affine, the existing AFFINE_HELLY129 argument provides an inconsistent subfamily of at most m+1 contexts, sharp for the m equations x_i=0 plus XOR_i x_i=1. For an explicit list of affine systems, eliminate each private post-y variable block and merge x-equations into one streaming GF(2) basis. Under polylog-sized explicitly encoded rows and logarithmic interface, full source scanning and elimination use N polylog^O(1) bit work and polylog^O(1) writable bits in an appropriate conventional model. An arbitrary circuit is *not* known to admit this syntactic form cheaply.

## EXECUTE / AUDIT
Dependency-free deterministic Python, seed 202611172104, completed **160,457 assertions, zero failures**:
- 1,800 Pi2-hardness guard/truth-table reductions (1,300 true, 500 false).
- 1,600 independent CNF->coNP-affinity sentinel reductions.
- 1,400 explicit random affine Sigma3 context families (1,186 false), full existential-projection enumeration and <=m+1 context cores.
- 65,812 all-subset co-singleton checks through m=4, plus 65,808 global-x controls.
- Sharp affine m+1 controls through m=12, source-equation padding and illegal quantifier reorderings.

The full proof, executable `audit.py`, raw `results.json`, SHA256 manifest and ZIP-integrity validation are available in the local run bundle `AFFINECERT_PI2_1_20261117_bundle.zip`. No native FLMV machine trace was executed.

## HANDOFF / EXACT STATUS
Assume P=NP; A is any fixed correct polynomial-time Circuit-SAT decider with unknown K,L. Goal remains `K' <= max(11/10, 3/5+K/2)` and `L' <= max(1/2,L/2)` for ordinary arbitrary sources, with hereditary closure, near-linear source conversion, half-size accessible ordinary SAT guests, charged strategy construction, materialization, guest source-bit access, memory transfers, source replay, recursion and same-machine SAT lower-bound matching.

New acceptance test: apply any proposed semantic-affinity recognizer to `C_F=((not b) or (not t) or F(v,z))`. It must decide arbitrary Pi2 QBF correctly and fully charge its implementation. Retain fast syntactic affine terminals, but never infer affine semantic projections for free. Re-test the co-singleton Sigma3 outer-witness trap, existing GRAPHPAIR, odd Tseitin and padded deciders. All-input Phi(A) **OPEN**. P versus NP **OPEN**.

## Primary citations
[1] Wrathall, *Complete Sets and the Polynomial-Time Hierarchy*, 1976, https://doi.org/10.1016/0304-3975(76)90062-1 .
[2] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, 2005, https://doi.org/10.1145/1101821.1101822 .
[3] Williams, *Self-Improvement for Circuit-Analysis Problems*, 2024, https://doi.org/10.1145/3618260.3649723 .
[4] Eriksson, Lagerkvist, Ordyniak et al., *Backdoors for Quantified Boolean Formulas*, 2026, https://arxiv.org/abs/2604.15927 .

FINAL_VERIFICATION_SENTINEL_AFFINECERT_PI2_1_20261117
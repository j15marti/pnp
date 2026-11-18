# POINTWISE-GUEST-CEILING1 | 2026-11-18 12:55 PST / 20:55 UTC

**STATUS:** Restricted, nonconstructive pointwise-circuit-size obstruction proved using standard Shannon counting. Exact indexed-QBF identity. 223,551 standard-library Python assertions passed with zero discrepancies in the local bundle. No all-input hereditary SAT contraction. P versus NP OPEN.

## PROPOSE (before search)
1. Attack the common-generator indexed dual by forcing pointwise preservation of an arbitrary original SAT predicate and apply a *function-circuit-size* counting bound.
2. Try one shared generator with compressed index decoder instead of q literal source copies; charge where the original predicate information lives.
3. Try compact post-universal Skolem selector circuits instead of an explicit 2^|c| selector table; do not assume free semantic certification.
4. Test source duplication, all invalid selector codes, original-input exponent inflation and padded guest-decider calls.

## SEARCH
Reviewed project's INDEXEDGUEST-SIGMA3-1 (2026-11-18 10:53 PST), ISLANDDUAL-SIGMA3-1 (09:03 PST), SIGMA30 selector-density firewall, SIGMA32 semantic-polarity firewall and project issue #3. The present theorem refines the known padding and input-expansion problem for the specific **pointwise** indexed guest; it is not a novel unconditional Circuit-SAT decision lower bound.

Primary references: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, https://doi.org/10.1145/1101821.1101822 ; R. Ryan Williams, *Self-Improvement for Circuit-Analysis Problems*, STOC 2024, https://doi.org/10.1145/3618260.3649723 ; Fichte, Hecher and Pfandler, *Lower Bounds for QBFs of Bounded Treewidth*, LICS 2020, https://doi.org/10.1145/3373718.3394756 .

## Theorem: pointwise indexed-guest ceiling

For every integer k>=8, let b=2^k. There exists a Boolean function F_k:{0,1}^k -> {0,1} requiring more than floor(b/(16k)) gates in any fan-in-at-most-two Boolean circuit (even allowing all 16 binary operations), yet representable by an explicit full Shannon-ROM circuit with O(b) AND/OR/NOT gates and a normal gate-list encoding of n_k=Theta(k*b) bits.

For arbitrary q>=1, t>=0 and s>=0, consider the correctly scoped quantified parent (outer x is empty):

    P_F := FORALL y EXISTS c,u_0,...,u_(q-1):
           AND_(i<q) G(i,y,c,u_i),
    G(i,y,c,u) := NOT F_k(y).

The global shared c and private u_i are after y but happen to be unused by G. Thus P_F is TRUE iff F_k is UNSAT.

The exact INDEXEDGUEST counterchallenge is

    D_F(y, j_d for all d in {0,1}^t)
      := AND_d [ (j_d<q) AND AND_(a in {0,1}^s)
                 NOT G(j_d,y,d,a) ]
       = F_k(y) AND AND_d(j_d<q).

Set every selector j_d=0. This is valid for any q>=1, and yields D_F(y,0,...,0)=F_k(y) **for every universal assignment y**. Therefore **any** bounded-fan-in circuit representing D_F pointwise, including one with arbitrary local Boolean optimization and common-subexpression sharing, needs at least floor(b/(16k)) gates: fix the selector input pins to zero and obtain an equally small circuit for F_k.

If such a compiler promises a physically serialized ordinary SAT guest with m<=N^(1/2) bits, N being the physical tagged parent source length, then

    m >= floor(2^k/(16k))
    N >= m^2 = Omega(2^(2k)/k^2)
               = Omega(n_k^2/k^4)
               = n_k^(2-o(1)).

Thus the supposed half-size guest RELATIVE TO N forces nearly quadratic growth from the original n_k-bit Circuit-SAT input in this subfamily. For q physically copied factors and q polynomial in n_k, N=Theta(q*n_k) implies q>=n_k^(1-o(1)). The lower bound on *guest complexity* does not rely on a literal copy of F surviving syntactic simplification; it follows from restriction of the guest's Boolean function.

### Standard counting proof
There are 2^(2^k) Boolean functions on k inputs. A size-g Boolean circuit with gates chosen from all 16 binary truth-table operations has at most

    (k+g) * (16*(k+g)^2)^g

possible gate lists and output wire choices, an overcount. Circuits with fewer gates pad deterministically to exactly g gates. For g=floor(2^k/(16k)), the count is strictly less than 2^(2^k) for k>=8, so some F_k has >g gate complexity even over this richer basis. Every truth table has a Shannon-ROM circuit of O(2^k) AND/OR/NOT gates; with O(k)-bit wire identifiers, its fixed unoptimized encoding length is Theta(k*2^k). QED.

### Sharp limitation
This is **not** a lower bound for satisfiability-only (equisatisfiable) compilation: an algorithm allowed to solve F may emit a constant SAT/UNSAT circuit. Under hypothetical P=NP such a compiler exists qualitatively, although not with the required resource exponents. The truth-table ROM family is itself SAT-easy by simply scanning its leaves. Counting hard Boolean *functions* does NOT yield a worst-case SAT decision-time lower bound. No unconditional P!=NP, PH separation, FLMV contradiction, or impossibility for arbitrary A->Phi(A) follows.

## Unknown-K reached-call test
If a specific architecture actually invokes a correct but deliberately padded solver A_D on a guest of m>=n_k^(1-o(1)) bits, and A_D unconditionally takes Omega(m^D) time for every input length, then the *reached* call alone costs Omega(n_k^(D-o(1))). For D>6/5 this exceeds the proposed n_k^(max(11/10,3/5+D/2)+o(1)) budget. This applies only to architectures making the call; shortcutting the easy ROM family or providing a fundamentally different satisfiability-only guest may bypass it.

## BUILD, exact finite checks
A dependency-free Python AND/OR/NOT gate-DAG auditor physically serialized ordinary indexed guests and source copies. Exhaustive finite checks on all 16 two-input and 256 three-input Boolean truth tables exercised q=1,2,3,5, post-y cutset sizes t=0,1 and private witness s=0,1. Invalid non-power-of-two selector codes were rejected. Random ROM tree evaluations, quantified-witness hoisting controls, split-shared-witness contradiction, source replay/mutation rejection and D>6/5 exponent arithmetic were checked. The circuit enumeration upper bound was numerically verified for k=8,10,12,16,24,32,48,64. **223,551 assertions, zero failures.**

Bit-normalized physical example (structurally easy, not a hard-F witness): original n=3,456 bits; q=8,192 copied factors; source N=29,613,616 bits; guest m=4,384 bits; sqrt(N)=5,441.84 bits. Thus m<sqrt(N) although m>n and N/n=8,568.755. At q=2,048 the physical half-size comparison still fails.

The local reproducibility ZIP contains the full standard-library audit.py, results.json, REPORT.md, HANDOFF.md and validated SHA256SUMS.txt. Finite audits are not native random-access Turing machine measurements.

## HANDOFF
Future work should leave the pointwise preservation contract and seek a **satisfiability-only**, source-checkable, fully charged near-linear conversion N=n^(1+o(1)) producing actual ordinary SAT guests m<=n^(1/2+o(1)) with recursive hereditary eligibility. The compiler must avoid running A_D on full-size or near-full-size guests, and explicitly pay for strategy certification, representation, all SAT answers, input/head addressing, memory transfers and source replay. Compact selector/Skolem circuits may help restricted QBFs but neither semantic validity nor the desired unknown-K exponent comes for free.

**FINAL:** Restricted pointwise representation ceiling PROVED; arbitrary-decider hereditary time-space contraction OPEN; P versus NP OPEN.

VERIFICATION_SENTINEL_POINTWISE_GUEST_CEILING1_20261118_1255PST
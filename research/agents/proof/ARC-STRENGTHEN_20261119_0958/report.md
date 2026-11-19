# ARC-RECURSION3: charged hereditary compiler theorem and endpoint falsifier
19 November 2026. ARC Strengthening. P versus NP OPEN. External independent mathematical review pending.

## Candidate and scope
Named dependency: ARC-T5-CRITICAL-PROMISE-REENTRY1, continued after ENCODED-SIZE2. Candidate: a fixed uniform hereditary compiler maps every promised critical T5 deletion of encoded length N into polynomially many promised children of length at most N^theta, then constructs and verifies an original witness from their witnesses. Falsifiers: off-promise children; uncharged child construction or retained answers; an endpoint logarithm lost by exponent iteration; a recurrence upper bound treated as an impossibility theorem.

The present result proves the conditional recurrence theorem and falsifies an exact endpoint O(N^p) inference in a model recurrence. It does not construct the missing T5 compiler. Path/finite-language structural lemmas were audited in preceding runs and are not rerun here.

## Conditional hereditary theorem
Fix constants B>1, 0<theta<1, a>=0, r>=0, C>=1 and D>0, all independent of inputs and recursion depth. Let P be a promise set of explicitly encoded designated critical T5 deletions. Suppose one fixed deterministic compiler, on EVERY input x in P with length N>B:

1. Makes at most C N^a child calls, each to an explicitly encoded member of P of length at most N^theta. Child selection may depend on earlier valid child witnesses.
2. Given any valid witnesses returned by those calls, produces a valid full witness for x.
3. Spends at most D N^r local machine steps, including all parsing, child acquisition/encoding, source reads, failed local work, query and answer handling, decoding, and original-source verification/output. The bound is uniform over valid child answers.
4. Has a sequential depth-first implementation retaining at most D N^sigma bits per active frame, for fixed sigma>0. This includes source copies, live generated children, previously retained witnesses, accumulators, addresses and reconstruction data. Buffers cannot be omitted by calling them advice or read-only external storage.
5. Handles instances of length at most B by direct exhaustive coloring, with constant costs depending only on B. No polynomial witness-finder assumption is needed at the leaves.

Then the recursively implemented promise witness finder is correct and polynomial-time. With p=a/(1-theta), one safe explicit bound is

T(N) = O(N^max(r,p) (log N)^log_{1/theta}(C) (1+log log N)),

and the SAME sequential execution has peak space S(N)=O(N^sigma). Constants and finite small inputs are absorbed into O. These are sufficient upper bounds, not optimality claims.

Correctness proof: induction on input length. Each recursive input is strictly smaller above B and remains in P; the finite base solves it. The local decoder's universal correctness over valid child answers then proves correctness at the parent. This argument is unaffected by adaptive child selection. A supplied SAT-only guarantee cannot be used on off-promise inputs.

Time proof: depth h is O(log log N). At depth i, any path has sizes at most N^(theta^j), j=0..i, so the number of nodes is at most

C^i N^[a(1+theta+...+theta^(i-1))]
= C^i N^[p(1-theta^i)].

Total local work at that depth is bounded by
D C^i N^[p+(r-p)theta^i] <= D C^i N^max(p,r).
Summing through h, including constant-cost leaves, gives the displayed conservative bound: C^h=O((log N)^log_{1/theta} C). Nonuniform early leaves only reduce this bound. Integer child lengths cause no difficulty because the hypothesis uses an exact upper bound, not an unspecified proportionality constant.

Space proof: only one recursion path is active. Above B, successive sizes have ratio at most B^(theta-1)<1. Therefore their sigma-powers form a geometrically bounded sequence. Sum of frame space is O(N^sigma), plus constant base workspace. This conclusion requires the stated per-frame bound: accumulating all child answers may force a larger sigma, and parallel siblings require aggregate space instead. Positive sigma also absorbs O(log N) control information after increasing a constant; sigma=0 requires a separate analysis and is not asserted.

Input acquisition is part of the local step bound. If emitting all maximal-size child strings already exceeds N^r, the assumptions fail. An implicitly represented child requires a separately charged access provider; it is not automatically an N^theta-bit ordinary input.

## Consequence for contradiction-first work
If this compiler exists, it already yields a polynomial witness algorithm for P through constant-size exhaustive leaves. A hypothetical polynomial T5 finder could replace the leaves, but is unnecessary for existence of this recursive algorithm. Thus "assuming a polynomial finder" does not supply the compiler premises.

For one nonrecursive layer with an O(N^k) finder, the familiar upper exponent max(r,a+theta k) is valid under all the charged interface hypotheses. Iterating this exponent map does not automatically produce an algorithm with exact endpoint exponent max(r,p); runtime constants, repeated level work and answer retention need the explicit recursion proof. A fixed-point exponent is not a lower bound on any finder, and the conditional polynomial algorithm contradicts no known unrestricted theorem here.

## Exact boundary counterexample
Set N_h=2^(2^h), T(2)=4, and
T(N_h)=C N_h T(N_(h-1))+N_h^2.
These are ordinary positive integer work budgets, not T5 hardness instances. Put U_h=T(N_h)/N_h^2. Since N_h=N_(h-1)^2, U_h=C U_(h-1)+1, U_0=1.

For C=1, U_h=h+1, so T(N_h)=N_h^2(1+log_2 log_2 N_h). The exponent fixed point is p=2, yet T is not O(N^2) on this sequence.
For C>1, U_h=(C^(h+1)-1)/(C-1), giving Theta(N_h^2 (log_2 N_h)^log_2 C).

This PROVED recurrence identity shows that even a fixed multiplicative call constant can survive as a logarithmic factor at the endpoint. The implication "fixed-point exponent 2 therefore an exact O(N^2) bound for this recurrence" is FALSIFIED. No lower bound on an unrestricted T5 algorithm follows.

## Executed audit
arc_recurrence3.py uses exact Python integers and Fraction, with C in {1,2,3} and h=0..8. All 27 cases match the closed forms. A separate exact sum of retained frame sizes satisfies sum_{j=0}^h 2^(2^j)<=2N_h for sigma=1. No timing or peak-byte claim is inferred from arithmetic assertion counts. Complete parseable raw JSON accompanies the code.

## Project and literature recovery
Read ENCODED-SIZE2 report, blob 38ba3c85e8260aba938732ae87a0c640e91f1eef:
research/agents/proof/ARC-STRENGTHEN_20261119_0904/report.md.
It proves that the explicit full H-thread core has K=Theta(N), so it cannot instantiate theta<1. Its unchanged-designation edge-deletion counterexample also blocks a naive hereditary call. More aggressive elimination, succinct representations, GF(5), flow, treewidth and other compilers remain legal; none is ruled out by that result.

Repository search for recurrence/loglog/fixed-point contraction recovered historical paid-directory and representation controls, but no matching closed T5 hereditary compiler. This is a bounded search, not a proof of absence.

Primary literature search located Akra and Bazzi, On the Solution of Linear Recurrence Equations, Computational Optimization and Applications 10 (1998), 195–210:
https://raw.githubusercontent.com/emintham/Papers/master/Akra%2CBazzi-%20On%20the%20Solution%20of%20Linear%20Recurrence%20Equations.pdf
Its displayed recurrence has fixed coefficients and n/b_i child arguments. We do not apply that theorem directly to N-dependent branching and N^theta child size. The proof above is elementary unrolling. An attempted Leighton notes fetch returned 403; it is not claimed read. Kun's fixed-girth reduction, indexed in earlier recovery reports, still supplies neither this critical promise compiler nor a uniform growing-girth polynomial blowup.

## Status, gates, and next blocker
PROVED/EXACT: conditional compiler-to-recursive-witness theorem; explicit time and same-run space bounds; boundary recurrence identity.
COMPUTATIONAL: 27 exact recurrence and frame-sum checks.
FALSIFIED: dropping all endpoint factors from the exponent fixed point.
CONDITIONAL: application to T5 requires EVERY compiler premise.
OPEN: actual power-shrinking critical-promise compiler, unrestricted witness lower bounds, intrinsic-critical promise NP-hardness, P versus NP.

DISJ gate PASS scoped: no static statistic-to-execution transfer. Relativization/algebrization/Natural Proofs: no separation claimed, unrestricted bridge OPEN. DTISP: same sequential execution conditional upper bounds only, no forbidden-region application. Configuration counting: not used as a lower bound.

Next blocker: exhibit one complete source-encoded compiler with all children still promised, true power shrink, polynomial local work and paid live reconstruction storage. Proving only a size identity or an exponent fixed point does not discharge this dependency.

Additive ARC publication only; ownership and automation states preserved. No local repository checkout/preflight or proof-kernel build was performed. Existing governance was recovered earlier in this conversation. External peer audit remains pending.

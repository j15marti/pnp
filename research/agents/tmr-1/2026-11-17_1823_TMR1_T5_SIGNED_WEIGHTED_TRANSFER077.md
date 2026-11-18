# TMR-1/077 | 2026-11-17 18:23 PST | Exact weighted Boolean transfer for arbitrary signed-3SAT T5 images and a dense mixed YES/NO control

**Owner:** TMR-1 / PNP Machine Model Lead. **Named dependency:** C1-T5-MIXED-HARDCORE-SOURCE-AUDIT. **Status:** PROVED/EXACT restricted symbolic transfer conditional on the already stated precise TMR-5/074 labelled source compiler; mathematical peer review OPEN. Executed bounded evidence COMPUTATIONAL. **P versus NP OPEN.** This report advances the exact algorithm/source-control side of the dependency but DOES NOT produce a necessary-work lower bound.

## Candidate and falsifiers fixed before source/peer audit

For every well-formed unary-header signed width-three source F, with m>=1 clauses, apply the TMR-5/074 ordered-clause deduplication and active-variable compaction. Let k denote retained variables and m' the distinct ordered clauses. Let D(F) denote the actual labelled 3SAT -> NAE/3COLOR -> anchored-C5 -> four-arc T5 image, not a schematic CSP. Claim: the exact number of original five-state target solutions is one explicit positive weighted Boolean partition sum with only k binary free variables, despite D(F) having 57+36k+168m' vertices. Its factors are fixed, finite, exact integer tables.

Four falsifiers: (F1) a splitter/NAE triangle has additional internal completions missed by the local factor; (F2) repeated original variables, signed literals, shared variables, clause sorting or the anchor 10-fold symmetry breaks factorization; (F3) a supposedly polynomial dense-family dynamic program hides exponential state or ignores exact big-integer/output costs; (F4) positive and negative source families lose large genuine post-triad treewidth, or a mixed-answer construction is confused with an all-algorithm necessity theorem.

The exact binary source is 1^n 0 1^m 0 followed by three signed low-first width-w(n) variable addresses per clause; w(n)=max(1,ceil(log2(max(2,n)))). Parse complete headers/records and reject malformed words, bad addresses, truncated and trailing data. Duplicate ordered clauses and unused variables are normalized exactly as in TMR-5/074. Empty-clause sources map to the empty T5 graph, with count 1, and are a SEPARATE case.

## Theorem 1: universal exact original-target partition identity

For each anchored 3COLOR palette (T,F,B) a permutation of (0,2,3), define:
- p(0)=2, p(2)=p(3)=1;
- q(a,b)=0 if a=b, q(2,3)=q(3,2)=3, q=1 on the other unequal pairs;
- P=p(T)p(F)p(B)q(T,F)q(T,B)q(F,B)=6;
- alpha=p(T)p(F)q(T,F)q(T,B)q(F,B);
- W(a,b,c)=sum over permutations (u,v,w) of (0,2,3) of p(u)p(v)p(w)q(u,v)q(u,w)q(v,w)q(u,a)q(v,b)q(w,c);
- L(a,b,c)=alpha * sum over s in {T,F} of W(a,b,s) W(opposite(s),c,F).

For a Boolean assignment z in {0,1}^k, evaluate each signed original clause's ordered literals as colors a_j(z),b_j(z),c_j(z) in {F,T}. Then the COMPLETE original five-symbol solution count of the actual nonempty canonical graph D(F) obeys

    Z_T5(D(F)) = 10 * sum_{all 6 palette permutations} P alpha^k *
                      sum_{z in {0,1}^k} product_{j=1}^{m'} L(a_j(z),b_j(z),c_j(z)).

All factors are nonnegative INTEGERS, and for every palette the local factor is zero precisely on the Boolean triple (F,F,F), positive on all other seven triples. Thus, without requiring a parsimonious SAT-to-T5 map,

    Z_T5(D(F))>0 if and only if Norm(F) is satisfiable.

No uniform proportionality to the ORIGINAL #SAT is claimed. The sole exact parsimonious step in this composition is the middle C5-to-T5 four-arc edge translation.

**Proof.** An authentic C5 anchor has exactly ten automorphisms. Its private two-edge and three-edge paths induce, for each fixed anchor automorphism, p as the vertex weight and q as the proper 3COLOR edge weight; the T5 four-arc gadgets then extend uniquely. The 3COLOR palette is a triangle of three distinct colors and contributes P. Every original variable has one positive/negative literal pair, adjacent to each other and to B; conditional on its Boolean value, this contributes alpha independent of truth orientation. Every clause introduces exactly one independent splitter literal pair (alpha) and exactly two fresh NAE triangle gadgets, each contributing the actual finite completion sum W. Summing the two splitter Boolean possibilities gives L. All other private vertices are disjoint once the original variable bits and palette are fixed. Multiplying all factors, summing z and palettes, and restoring the ten anchor automorphisms gives the displayed EXACT identity for every normalized signed formula, including shared/repeated variables and unsatisfiable formulas. The 3COLOR NAE triangle extension exists exactly when its three terminal colors are not all equal. The fixed splitter existential identity expresses OR(a,b,c) as NAE(a,b,s) AND NAE(not s,c,F); consequently L(F,F,F)=0 and the other factors are strictly positive. This last assertion also follows from the exact eight-entry table below. QED.

The six palette assignments pair under swapping 2 and 3. Their three representative local tables, indexed by ordered truth bits 000,001,010,011,100,101,110,111, are EXACT:

| (T,F,B) | alpha | L_000 | L_001 | L_010 | L_011 | L_100 | L_101 | L_110 | L_111 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| (0,2,3) | 6 | 0 | 7776 | 7776 | 5184 | 7776 | 5184 | 2592 | 864 |
| (2,0,3) | 6 | 0 | 864 | 864 | 5184 | 864 | 5184 | 2592 | 7776 |
| (2,3,0) | 3 | 0 | 34992 | 34992 | 69984 | 34992 | 69984 | 34992 | 34992 |

The full formula is equivalently 120 times the sum of P-free alpha^k weighted assignment sums over those three rows, because P=6, anchor=10 and each row has two palette orientations.

## Theorem 2: high treewidth, mixed YES/NO images, but inexpensive exact counts

For every n>=2, define the genuine signed three-slot formula

    F_n^+ = AND_{0<=i<j<n} (x_i OR x_j OR x_j).

There are k=n active variables, m=binom(n,2) distinct ordered clauses and exactly n+1 Boolean satisfying assignments: at most one variable may be false. Its authentic connected T5 image has

    N_D = 57+36n+168m,    A_D = 80+52n+244m,
    rho_raw = 24+16n+76m, rho_after_triad = 4+3n+15m.

The undirected 3COLOR graph used in the compiler has a **subdivision of K_n** with positive-literal vertices as branch vertices. Indeed, clause (x_i OR x_j OR x_j) contains a private first NAE triangle with a two-internal-vertex path joining the positive literal nodes x_i and x_j. Distinct pairs have disjoint private internal vertices. Every successive anchored C5 edge-path replacement and T5 four-arc replacement preserves that K_n minor. After exact forced-triad contraction the intermediate H still contains the minor. Consequently

    tw(underlying D(F_n^+)) >= n-1,
    tw(H(F_n^+)) >= n-1.

Suppressing degree-two private paths does not eliminate this branch-vertex clique minor, although the residual graph is now weighted. In particular, post-triad feedback rank and genuine treewidth are superlogarithmic in the full encoded source length L_D=Theta(n^2 log n).

Nevertheless define the 2x2 constant table M_{ab}=L(a,b,b), a,b in {0,1}, for any of the three palettes. Let DP_j(t) be the exact weighted partition sum over the first j Boolean variables with t TRUE values, including all pair clauses among those j. Initialize DP_0(0)=1. On appending bit b at position j:

    DP_(j+1)(t+b) += DP_j(t) * M_(0,b)^(j-t) * M_(1,b)^t.

Then

    Z_T5(D(F_n^+))
       = 120 * SUM_{three rows} alpha^n * SUM_{t=0}^n DP_n(t).

This is O(n^2) DP state transitions and O(n) stored BigInts per row, with each integer O(n^2) bits. Parsing, detecting the exact canonical signed source family, constructing/inverting the full image when supplied, all powers, unsuccessful checks, arbitrary precision arithmetic and the final O(n^2)-bit output admit one conventional sequential bit-machine realization with conservative matched T=O((L+1)^12) and S_peak=O((L+1)^4), for either authentic signed source or a strict labelled T5 image recognized and inverted via TMR-5/076. This is a positive polynomial exact-count theorem for a high-treewidth family, not proof that *every* high-treewidth source is easy.

For n>=6 set

    F_n^- = F_n^+ AND (not x_0 OR not x_1 OR not x_2)
                     AND (not x_3 OR not x_4 OR not x_5).

These are two additional signed triples on disjoint sets. F_n^+ allows at most one false variable, whereas the two added clauses demand false variables from disjoint sets. Hence F_n^- is UNSAT. Its positive-pair K_n minor survives in the authentic T5 image and in the forced-triad quotient, but its T5 count is zero. Both source families are polynomial-time *recognizable*, with exact positive count or zero after paid recognition. They form a restricted high-treewidth mixed YES/NO countercontrol, not a mixed hard-core lower bound. Their parameter sizes differ by two clauses; no promise of source-indistinguishability is made.

## Exact algorithmic ledger and NP consequences

The explicit formula evaluates any normalized k-variable signed source in 6*2^k * poly(L) bit time with polynomial peak writable space, *not* universal polynomial time. The published Node test program intentionally caps generic enumeration at k<=26; that is a prototype safeguard, not an UNSAT answer or an asymptotic theorem. For the dense family, independent source recognition and the O(n^2)-state BigInt DP give a polynomial upper on ONE standard sequential machine. It charges every input field, sorting/deduplication, active-variable remapping, all finite table computations, adaptive path selection/failure, exact exponentiation, factor multiplication, intermediate and output bit lengths, caches, physical tape heads and final verification. Shared tables are stored once. The strict labelled raw-image inverse has paid polynomial time O(L_D^5) and writable O(L_D^2) per the independently scoped TMR-5/076 report; generic graph-isomorphism recognition is NOT assumed. Outside that image promise, an arbitrary valid T5 graph may use the exact exponential fallback.

The NP-completeness of T5 remains KNOWN THEOREM by Bang-Jensen, Hell and MacGillivray 1988. A uniform polynomial algorithm for ALL valid T5 inputs would imply P=NP. This dense-family exact algorithm does not solve general SAT, rule out alternative compact algorithms, or establish a superpolynomial time/space bound.

## Independent validation, limitations and scientific gates

ACTUALLY EXECUTED on local Node v22.16.0: deterministic revision tmr1-t5-weighted-sat077-v1, **162 assertions, zero failures**, 25 original 4-arc endpoint enumerations, all 27 triangle terminal triples in an independent counting loop, 3x8 exact palette table cells, canonical low-first source round trips, malformed rejection checks, duplicate-clause/unused-variable normalization, full 2^n truth-assignment comparison against the dense O(n^2) DP for n=2..9, exact source #SAT=n+1, F_n^- Boolean UNSAT and n=6..8 exact weighted count zero, and an earlier independent one-clause target-count check (2,588,008,320). One initial malformed-test *fixture*, which did not actually introduce a nonbinary character when the last bit was 1, failed before the corrected final test run; it was replaced by a genuine trailing '2' mutation. No scientific formula was changed. Source SHA256 7d055b4c29d88573c9d76d5d19de1d20acc0330b35ad202e4cf529fd9f01bd09. Raw JSON SHA256 91557806d5a28aca808eeabbeff1d7ce6de5e9aede2e4efda3cf9e62d7888ad5. The full executed JS and raw JSON are in the current run's separate local artifacts, NOT claimed GitHub-published until fetched and checked. Finite evidence is COMPUTATIONAL; the two identities above have separate symbolic proofs. No native TM microstep trace, full LaTeX compile, repository preflight (no local checkout), independent Lean/nanoda rebuild or external mathematical peer review was executed.

**Four gates:** DISJ sanity PASS restricted positive control; rank/treewidth->mandatory-work inference FAIL. Relativization PASS for this constructive source-algorithm statement; unrestricted nonrelativizing NP separation OPEN (BGS, algebrization and Natural Proofs safeguards remain). Simultaneous DTISP PASS for the single matched upper T/S bound; a forbidden-pair lower-bound premise is NOT APPLICABLE WITH REASON. Deterministic configuration counting PASS only as an upper-bound consistency check, never a lower bound or randomized/quantum extrapolation. Horn/2-SAT/Gaussian-affine, local-basis/field choices, degree-two elimination, polymorphisms, treewidth, twins, equality, autarkies, products, selectors, padding, exact auxiliaries, caching, alternative dynamic algorithms remain legal cheap paths. /341 FAIL as general UNSAT authority; /386 RESTRICTED.

**Named dependency advanced but not closed as necessary work:** C1-T5-MIXED-HARDCORE-SOURCE-AUDIT now contains a fully source-authenticated high-treewidth mixed family with a *cheap exact counting* YES path and a cheap NO path. **ONE next lemma: C1-T5-MIXED-NONEXCHANGEABLE-CORE**, a source-authenticated mixed YES/NO family whose reduced signed weighted factor graph is not efficiently handled by this complete-graph exchangeability DP, twin/triad/degree-two quotient, bounded-width decomposition or affine shortcuts; any arbitrary-machine necessary-work implication remains OPEN.

Sources and corpus: TMR-5/074 and /076, draft PR #209 (not main merged); TMR-1/072,/073,/075,/076 on draft PR #197; TMR-2/072 and TMR-4/075 controls; Bang-Jensen, Hell and MacGillivray (1988), SIAM J. Discrete Math. 1:281-298, DOI 10.1137/0401029; Garey, Johnson and Stockmeyer (1976), TCS 1:237-267, DOI 10.1016/0304-3975(76)90059-1.
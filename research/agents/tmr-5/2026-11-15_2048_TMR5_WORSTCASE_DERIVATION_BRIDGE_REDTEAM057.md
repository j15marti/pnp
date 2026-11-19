# TMR-5/057 | 2026-11-15 20:48 PST | Red team of the worst-case derivation-cost bridge

Role: TMR-5 / PNP Machine Bottleneck Redteam, acting as the "Independent Proof Red Team" of the user's
2026-11-15 scheduled directive (worst-case minimum derivation cost). P versus NP remains **OPEN**.
Retired trackers, historical root main files and peer manuscripts untouched. No schedule/identity changes.

## 1. Target under audit (exact)

For a fixed Cook--Reckhow refutation system R for CNF (sound, complete, proofs checkable in time
polynomial in |F|+|pi|) and cost = proof length in bits (line count is polynomially related for the
systems below), the user's shared object is

    W_R(N) = max_{F in UNSAT, |<F>| <= N}  min_{pi : F |-_R bottom} cost_R(pi).

The proposed "weakest sufficient bridge" is

    B(R):   SAT in P  ==>  W_R(N) <= poly(N).

Together with an unconditional superpolynomial lower bound L(R): W_R(N) >= N^{omega(1)}, B(R) gives
P != NP by contraposition. The "multisign DAG hypergraph" reduction picture and its "minimal reduced
state" are instances of R-derivations; for every UNSAT F the minimal reduced state is bottom, so all
information is in the cost, i.e. in W_R. Granting free knowledge of the optimal derivation is correct
and harmless *for lower bounds on executions that are themselves R-derivations*.

Dependency named and advanced: **BRIDGE-B(R)**, the load-bearing arrow SAT in P => W_R poly.

Falsifiers stated before the literature check:
1. A system R with known L(R) for which B(R) is provable by an argument not already proving P != NP.
2. A correct polynomial-time SAT algorithm A, and an R at least as strong as EF, for which R is
   polynomially bounded but the soundness tautologies of A lack short R-proofs (would break the
   equivalence of Sec. 3).
3. A finite Tseitin control for which the minimum resolution width does not exceed the initial width
   (would weaken the cited control).
4. A fixed R whose minimum derivation cost lower-bounds the running time of *every* algorithm
   pointwise (would make the bridge automatic).

## 2. Theorem A (bridge collapse for systems with known lower bounds) — PROVED/EXACT, elementary

If L(R) holds unconditionally, then B(R) is logically equivalent to P != NP.

Proof. B(R) is (SAT not in P) or (W_R polynomially bounded). The second disjunct is false by L(R).
So B(R) <=> SAT not in P. QED.

KNOWN THEOREMS giving L(R): resolution and tree-like resolution (Haken 1985, PHP; Urquhart 1987,
Tseitin on expanders; Ben-Sasson--Wigderson 2001 width-size), polynomial calculus (Razborov 1998;
Impagliazzo--Pudlak--Sgall 1999; Tseitin hard over characteristic != 2), cutting planes (Pudlak 1997),
bounded-depth Frege (Ajtai 1988; Krajicek--Pudlak--Woods 1995; Pitassi--Beame--Impagliazzo 1993),
Res(k) for small k. For every such R the "weakest bridge" is **not weaker** than the target: it is the
target. Consequence for the five-agent plan: constructing harder UNSAT families for resolution,
polynomial calculus or cutting planes cannot advance B(R) at all; it only re-proves L(R).

Falsifier 1: cannot occur (logical identity). Falsifier 4: refuted by the control in Sec. 5:
Tseitin on expanders has resolution size 2^{Omega(n)} while GF(2) Gaussian elimination decides it in
O(n^3) bit operations; PHP has exponential resolution size while counting pigeons vs holes is linear.
So min_pi cost_Res(pi) is a lower bound only for **resolution-shaped executions** (DPLL ~ tree-like,
CDCL ~ general resolution), never for arbitrary algorithms. The free-optimal-sequence concession does
not touch this gap: the gap is whether a fast algorithm's run *is or yields* an R-derivation.

## 3. Theorem B (exact form of the bridge for strong systems) — KNOWN / PROVED, restricted

Let A be a polynomial-time algorithm, and Sound_{A,n} the standard polynomial-size propositional
formula (with extension variables encoding A's computation) stating: for every F of length n and every
assignment a, if A(F)=UNSAT then a does not satisfy F. Let R p-simulate extended Frege (EF) and be
closed under the polynomial operations used below (substitution of the fixed input F, evaluation of a
circuit on a fixed input, modus ponens) — EF itself qualifies.

Then B(R) <=> [ SAT in P ==> there is a correct poly-time A such that Sound_{A,n} has poly(n)-size
R-proofs ].

Proof. (<=) Given F unsat of length n: an R-proof of Sound_{A,n}, substitute F, add the poly-size
evaluation of A's circuit on F (output UNSAT), and modus ponens yields a refutation of F of size
poly(n). (=>) If R is polynomially bounded and A is correct, every Sound_{A,n} is a tautology of size
poly(n) and so has a poly-size R-proof. QED. This is the propositional form of Cook (1975, PV <-> EF)
and the Krajicek--Pudlak (1989) reflection/simulation correspondence; it is not claimed as new.

Falsifier 2 therefore cannot occur. What B(EF) actually demands is: **if SAT is in P, the correctness
of some SAT algorithm is feasibly (EF-, equivalently PV-for-Pi^b_1) provable.** Nothing known gives
this. The present project has no argument for it, and SAT in P alone does not supply it: an algorithm
can be correct with only a non-feasible (e.g. ZFC) correctness proof. Note further L(EF), and even
superpolynomial Frege lower bounds, are long-standing open problems (Cook's program).

Corollary B' (optimal systems). If R is optimal (simulates every proof system with polynomial
blow-up), B(R) is a KNOWN THEOREM: SAT in P gives the p-bounded system "pi empty, accept iff A(F)=UNSAT",
which R simulates. But then B(R)+L(R) proves NP != coNP, strictly stronger than P != NP as currently
known. Existence of optimal systems is OPEN; Krajicek--Pudlak (1989): NE=coNE implies optimal, E=NE
implies p-optimal systems exist (hypotheses later weakened to doubly exponential classes by
Kobler--Messner--Toran 2003). No explicit fixed system (Frege, EF, ZFC-system) is known optimal.

## 4. Ranking of fixed R for the shared objective

| R | L(R) status | B(R) status | Verdict |
|---|---|---|---|
| Resolution / tree-like / Res(k) | KNOWN superpoly | equivalent to P != NP (Thm A) | bridge is the whole problem; FAIL as "weak" bridge |
| Polynomial calculus, Nullstellensatz, Cutting planes | KNOWN superpoly | equivalent to P != NP | same |
| Bounded-depth Frege | KNOWN superpoly | equivalent to P != NP | same |
| AC0[p]-Frege, Frege | OPEN | OPEN | both arrows open |
| Extended Frege | OPEN | <=> feasible provability of some SAT algorithm (Thm B) | most principled target; both arrows open |
| optimal system (if any) | OPEN; implies NP != coNP | KNOWN (Cor B') | lower bound strictly harder than target |

## 5. Executed finite control (COMPUTATIONAL; illustrates the known theorems, proves nothing asymptotic)

`experiments/tmr/tmr5_derivation_bridge057.py`, revision `tmr5-derivation-bridge057.v1`, git blob
`787ef912db0062af081fde42ee2b022b335d70d9`, sha256
`52b3d74497118a07c412650bd576ffb4da24a6dcb9b6bde177412f486771bb36`; deterministic (no seed);
CPython 3.11.18 locally, about 6 s. Raw: `results/raw/tmr/2026-11-15_2048_TMR5_DERIVATION_BRIDGE057_PY_RAW.json`
(blob `e5c805d41313663abca4c78317c66a77278dba75`; per-stage `seconds` fields vary between runs).
19 assertions, zero failures. Methods: exact minimum resolution width by width-bounded saturation
(complete: a width-w refutation's clauses all lie in the width-w closure); exact minimum tree-like
size by the falsified-clause decision-tree DP; fixed-order DPLL tree; GF(2) elimination with exact row
XOR count; brute-force UNSAT labels.

| instance | vars | clauses | init width | min Res width | min tree-like size | fixed DPLL nodes | GF(2) row XORs |
|---|---|---|---|---|---|---|---|
| Tseitin K4 (odd) | 6 | 16 | 3 | 4 | 55 | 55 | 5 |
| Tseitin K3,3 | 9 | 24 | 3 | 5 | 151 | 167 | 11 |
| Tseitin prism | 9 | 24 | 3 | 4 | 95 | 351 | 9 |
| Tseitin cube Q3 | 12 | 32 | 3 | 5 | 255 | 343 | 20 |
| PHP 3->2 | 6 | 9 | 2 | 2 | 21 | 29 | n/a (counting: 5) |
| PHP 4->3 | 12 | 22 | 3 | 3 | 85 | 197 | n/a (counting: 7) |

SAT control (Tseitin K4 even charge): not refuted at any width <= 6 (raw field `lower_bound_width`=7 means
"no refutation of width <= 6 found"; none exists since the formula is satisfiable), GF(2) consistent.
Every fixed DPLL tree is >= the tree-like minimum, as required (the legitimate half of the user's
"min over derivations" argument). Width already exceeds initial width on these tiny graphs (falsifier 3
not triggered); the asymptotic exponential gap is the cited theorem, not this table.

Alternative-reasoning survival test (user item 4): Tseitin **fails** survival against algebraic
reasoning over GF(2) (Gaussian elimination; PC over F_2 low degree; Res(lin)), and cutting planes has
quasipolynomial Tseitin refutations (Dadush--Tiwari 2020, to be re-verified at primary source). PHP fails survival
against counting (cutting planes has poly PHP proofs). Any family proposed as "hard for all methods"
must be tested against EF-strength reasoning, which is exactly where no lower bounds are known.

## 6. Four gates

DISJ sanity: PASS — no static rank/size invariant used as an algorithm lower bound; DISJ-style easy
families remain cheap. Relativization: the bridge B(R) and L(R) are absolute (oracle-free) statements;
Theorem A shows any proof of B(Res) is a proof of P != NP and therefore must evade relativization,
algebrization and Natural Proofs — NOT APPLICABLE as a pass; barrier burden fully inherited (OPEN).
Simultaneous DTISP: NOT APPLICABLE (no machine simulation claimed; experiment's time/space are
finite measurements only). Deterministic configuration counting: PASS only as upper-bound guard.
/341 FAIL as full UNSAT authority; /386 RESTRICTED.

## 7. Status summary and the one next lemma

Theorem A: PROVED/EXACT (elementary), independent review OPEN. Theorem B: KNOWN THEOREM form
(Cook 1975; Krajicek--Pudlak 1989), proof sketch reproduced here, review OPEN. Corollary B': KNOWN.
Section 5: COMPUTATIONAL. Overall: the bridge B(R) is **not** a weaker sufficient step for any R with
a known lower bound; for R = EF it is equivalent to an open feasible-provability statement.

ONE NEXT LOAD-BEARING LEMMA (for the General SAT Lower-Bound Lead / TMR-1): either (i) prove, for
EF or a named Frege-type R, that SAT in P implies an algorithm with poly-size R-proofs of Sound_{A,n}
(no such argument is known), or (ii) replace the target by a model-restricted statement, e.g. a
proved simulation "every algorithm in class K yields R-derivations of polynomially related cost"
(as known for DPLL/CDCL vs resolution), and state honestly that the resulting lower bound is for K only.

## References (primary)

S. Cook, R. Reckhow, The relative efficiency of propositional proof systems, JSL 44 (1979).
S. Cook, Feasibly constructive proofs and the propositional calculus, STOC 1975.
J. Krajicek, P. Pudlak, Propositional proof systems, the consistency of first order theories and the
complexity of computations, JSL 54 (1989). J. Kobler, J. Messner, J. Toran, Optimal proof systems imply
complete sets for promise classes, Inf. Comput. 184 (2003). A. Haken, The intractability of resolution,
TCS 39 (1985). A. Urquhart, Hard examples for resolution, JACM 34 (1987). E. Ben-Sasson, A. Wigderson,
Short proofs are narrow, JACM 48 (2001). A. Razborov, Lower bounds for the polynomial calculus,
Comput. Complexity 7 (1998). P. Pudlak, Lower bounds for resolution and cutting plane proofs and
monotone computations, JSL 62 (1997). J. Krajicek, Proof Complexity, CUP (2019). Literature check this
run: web search confirming Krajicek--Pudlak NE=coNE / E=NE statements and Cook 1975 PV->EF translation
(arXiv 2304.14702, arXiv 2408.07408, Cook--Reckhow survey arXiv 1909.03691).

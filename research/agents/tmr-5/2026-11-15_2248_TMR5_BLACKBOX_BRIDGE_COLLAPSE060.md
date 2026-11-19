# TMR-5/060 | 2026-11-15 22:48 PST | Relativized (black-box) collapse of the derivation-cost bridge

Role: TMR-5 / PNP Machine Bottleneck Redteam, acting as "Independent Proof Red Team" of the scheduled
worst-case derivation-cost directive. P versus NP remains **OPEN**. Retired trackers, historical root
main files and peer manuscripts untouched. No schedule or identity change.

## 0. Repository state and reconciliation

Base: origin/main `818319a1f`. Two unmerged TMR-5 drafts were merged into this branch before editing:
`origin/tmr5-20261115-2125-pinned-kernel-retry058` (/058 kernel retry, /059 raw-probe affine span;
draft PR #199) and `origin/ccr-1695bd63-dh8nvl` (/057 bridge red team, commit `29a69db39`, never
merged, no PR). Both conflicting handoffs are archived byte-exact:
`archive/handoff_pre_2026-11-15_2248_branch059.md` (blob `df6e484f534095b4fd95da50345fc3133b269862`)
and `archive/handoff_pre_2026-11-15_2248_branch057bridge.md` (blob
`dcbaa9a41f54cb6b0ce333471f704570d2e0ed39`); both blobs equal the branch originals. main5 keeps
both the /057-OR, /059 and bridge sections; nothing was deleted.

Duplicate check: /057-bridge already proved Theorem A (B(R) is equivalent to SAT not in P whenever
L(R) is known) and reproduced Theorem B (for R >= EF, B(R) is equivalent to feasible provability of a
SAT algorithm's soundness). This run does **not** repeat them. It closes the item that /057 left as
"relativization: barrier inherited, OPEN" by proving an exact relativized statement.

## 1. Named dependency and candidate

Dependency: **BRIDGE-B(R), relativization gate.** B(R): SAT in P => W_R(N) <= poly(N), where
W_R(N) = max over UNSAT F with |<F>| <= N of min over R-refutations pi of cost_R(pi) (bit length).

Candidate (stated before literature check): any argument for B(R) that treats the SAT algorithm only
through its input/output behaviour and polynomial running time, so that it remains valid for oracle
algorithms, proves W_R(N) <= poly(N) outright. Hence such an argument cannot exist for any R with a
known lower bound, and for every other R it would already give NP = coNP, refuting the pipeline's
intended conclusion.

Falsifiers stated in advance:
1. An oracle O with SAT not in P^O for every PSPACE-complete O (impossible if SAT <= O).
2. A natural relativization of R in which the proof relation changes with O so that the reduction to
   the oracle-free W_R fails (this is a scope limit, examined in Section 3).
3. An existing bridge-style argument (Theorem B, DPLL/CDCL simulations) that is black-box; if one
   existed the theorem below would contradict Haken.
4. An algebrizing oracle extension under which SAT leaves P^{tilde O}.

## 2. Theorem C (PROVED/EXACT, elementary; independent review OPEN)

Fix a Cook--Reckhow refutation system R whose proof relation "pi refutes F" does not depend on any
oracle (resolution, PC, CP, Frege, EF and every fixed syntactic system qualify). For an oracle O let

    B^O(R):  SAT in P^O  ==>  W_R(N) <= poly(N).

Call an argument for B(R) **black-box (relativizing)** if it establishes B^O(R) for every oracle O.

(i) If B^O(R) holds for some O with NP subseteq P^O, then W_R(N) <= poly(N) unconditionally, and
therefore NP = coNP.

(ii) Consequently a black-box argument for B(R) proves W_R(N) <= poly(N) and NP = coNP.

(iii) For every R with an unconditional superpolynomial lower bound L(R) (resolution, tree-like
resolution, Res(k), polynomial calculus, Nullstellensatz, cutting planes, bounded-depth Frege), the
relativized bridge B^TQBF(R) is **false**; no black-box argument for B(R) exists.

(iv) For every R whatsoever, a pipeline "black-box proof of B(R)" + "proof of L(R)" is inconsistent.
Every successful pipeline must use the white-box fact that the SAT algorithm is an oracle-free machine
whose computation can be represented inside R.

(v) The same holds for algebrizing arguments in the Aaronson--Wigderson sense: for O = TQBF and any
low-degree extension tilde O agreeing with O on Boolean inputs, SAT in P^{tilde O}.

Proof. (i) SAT in P^O holds because SAT in NP subseteq P^O. B^O(R) then gives W_R <= poly. The
statement W_R <= poly mentions no oracle, so it holds in the real world. A polynomially bounded
Cook--Reckhow refutation system puts UNSAT in NP (guess pi, run the polynomial verifier), so
coNP = NP (Cook--Reckhow 1979). (ii) Instantiate O = TQBF; NP subseteq PSPACE = P^TQBF. (iii) L(R)
contradicts W_R <= poly, so B^TQBF(R) is false. (iv) From (ii) we obtain W_R <= poly, contradicting
L(R). (v) tilde O answers every Boolean TQBF query, so P^TQBF subseteq P^{tilde O}; apply (i). QED.

Scope of falsifier 2. If R itself is relativized to R^O whose verifier may query O, then for O = TQBF
the system "accept the empty proof iff the oracle says F is unsatisfiable" is polynomially bounded and
no contradiction arises. Theorem C therefore concerns **fixed** proof systems, which is what the shared
objective W_R(N) fixes. This is a real scope boundary, not a repair.

Falsifier 3 check. Theorem B's direction (<=) substitutes F into an R-proof of Sound_{A,n} and
evaluates A as a polynomial-size circuit inside R. An oracle machine has no such circuit, so the
argument is white-box and does not relativize. The DPLL-to-tree-like and CDCL-to-resolution
simulations (Pipatsrisawat--Darwiche 2011; Atserias--Fichte--Thurley 2011) inspect the solver's
branching and learning trace, also white-box. No known bridge contradicts Theorem C. Falsifiers 1 and 4
cannot occur.

## 3. Consequence for the five-agent plan (ranked)

1. The "weakest sufficient bridge" is not weak. For known-lower-bound systems it is P != NP (Thm A) and
   has no relativizing or algebrizing proof (Thm C). For EF it is the open feasible-provability
   statement (Thm B), and any proof must open up the algorithm.
2. The "free optimal derivation" concession remains sound and irrelevant to the gap. The gap is whether
   the algorithm's run yields an R-derivation, and Theorem C shows that this cannot be shown from
   correctness plus running time alone.
3. The only non-circular route visible is the restricted route of /057: name a class K of algorithms
   whose traces provably convert into R-derivations of polynomially related cost. Then claim a lower
   bound for K only. Proving B(R) for all of P requires a structural theorem about every polynomial-time
   SAT algorithm. Theorem B shows this is equivalent, for EF, to bounded-arithmetic provability of
   correctness.

## 4. Four gates

DISJ sanity: PASS (no static invariant used as a work bound). Relativization: **FAIL for every
black-box/relativizing proof of B(R), PROVED here**; white-box nonrelativizing arguments remain OPEN.
Algebrization: FAIL likewise for algebrizing proofs (Thm C(v)). Natural Proofs: not engaged by the
bridge itself; any L(EF) proof inherits the proof-complexity-generator/natural-proof concerns (OPEN).
Simultaneous DTISP: NOT APPLICABLE (no simulation). Deterministic configuration counting: PASS only as
an upper-bound guard. /341 FAIL as full UNSAT authority; /386 RESTRICTED.

## 5. Validation actually run

No new code. This is a pen-and-paper proof checked by hand. Git blob checks of the archived handoffs
were executed (`git hash-object` equal to branch originals). No preflight script, LaTeX build, Lean or
nanoda was executed in this run. The /057 Python control was not rerun.

## 6. Literature check this run (clues)

Web search, 2026-11-16. Cook (1975) PV-to-EF translation confirmed via the Cook--Reckhow survey
(arXiv 1909.03691) and "Consistency of circuit lower bounds with bounded theories" (arXiv 1905.12935).
Both note the literature mostly runs from EF lower bounds to unprovability of P = NP in PV, which is
the converse of what B(EF) needs. This is a clue that B(EF) is hard. Relativized optimal-proof-system
results: Egidy (arXiv 2602.02294; ICALP 2026 LIPIcs vol. 374 paper 88) and Egidy--Glasser (arXiv
2408.07408) show, relative to oracles, no relativizable proof gives optimal proof systems for sets
outside NP. Dose (arXiv 1904.06175) separates p-optimality conjectures by oracle. These match
Theorem C's message: statements tying algorithms to fixed proof systems are oracle-sensitive. The
arXiv abstracts were read; the full papers were not. ECCC 2025/187 and 2026/109 appeared in results
and are unread.

## 7. One next lemma

For TMR-1 / General SAT Lower-Bound Lead: fix K = algorithms whose computation is a
polynomial-size uniform circuit family together with a PV-proof of correctness. Prove the white-box
transfer "A in K => EF refutes every UNSAT F in poly(|F|) size" with explicit polynomial (Cook 1975
translation, charged). Then state that any lower bound obtained from EF applies only to K. No lower
bound for EF is known.

## References

Baker, Gill, Solovay, SIAM J. Comput. 4 (1975). Aaronson, Wigderson, Algebrization, ACM TOCT 1 (2009).
Cook, Reckhow, JSL 44 (1979). Cook, STOC 1975. Krajicek, Pudlak, JSL 54 (1989). Haken, TCS 39 (1985).
Pipatsrisawat, Darwiche, AIJ 175 (2011). Atserias, Fichte, Thurley, JAIR 40 (2011). Krajicek, Proof
Complexity, CUP 2019. Egidy, arXiv 2602.02294. Egidy, Glasser, arXiv 2408.07408. Dose, arXiv 1904.06175.

# Independent strict-C red-team: optimal 3-sheet SAT-cover threshold (2026-11-19)

**PROVED:** The smallest sheet degree d such that every finite strict-C source admits *some* SAT incidence-graph d-fold cover is d=3. This is an existential covering property, not a SAT decision algorithm or a P versus NP proof.

Canonical: Z5; R(a,b) iff (b-a) mod 5 in {1,3}; C is either orientation of a directed triangle, **30/125** ordered assignments. Every clause has 3 distinct variable **names**, not globally unique values.

## New exact obstruction: 2-cover K6 always UNSAT

Let F6 contain all 20 original physical C clauses on the three-element subsets of six distinct names 0,...,5. Suppose a twofold incidence cover had a satisfying assignment. Each original variable has two copied values. Each source clause has two lifted clauses; each copied variable is incident once above each original incidence. Because every satisfying C triple uses three *different* values, for any original triple of names and any one of the five colors, that color can occur among their six sheet values at most twice.

If any color occurred three times among all 12 copied variables, those occurrences would be contained in at most three original variable names (one variable contributes at most two copies); add other names if necessary to reach exactly three. Their source triple clause would then have a color repeated at least three times over its two lifted clause copies, contradiction. Thus every one of five colors occurs globally at most twice. This would imply 12<=5*2=10. **Impossible**, for *every* two-sheet incidence cover, regardless of edge permutations or connectedness. The proof extends to any ternary all-different relation on q colors using the complete three-uniform source on q+1 names.

## Sharpness: every <=5-name strict-C source has a satisfiable twofold cover

The complete K5 triple source (10 physical clauses) has a **connected** SAT twofold cover. Sheet copy colors for variables 0..4 are:
`(0,1), (0,4), (1,2), (2,3), (3,4)`.
For source clauses `012 013 014 023 024 034 123 124 134 234`, first lifted sheet selector bits are
`010 011 010 000 001 011 000 001 011 000`.
Second lift bits are their complements, independently per source clause. All **20 lifted C clauses** satisfy the exact original predicate and every original incidence has a sheet permutation. Restrict this cover to arbitrary subsets/duplicate occurrences of these triples and isolate extra unused names to cover *every* <=5-name strict-C source. Both complete original K5 and original K6 are UNSAT by exhaustive 5^n original-color search.

The prior separately established universal 3fold construction `C((x0,t),(x1,t+1),(x2,t+2))` for t=0,1,2, coloring `(v,s)` by `s`, satisfies every original strict-C input. Together these results prove the exact universal existential cover degree **3**. Do not claim that every 3fold cover is SAT.

## Deletion-minimal **twofold-cover** obstruction on 6 original names

A deterministic greedy scan of F6 yields 11 original clauses:
`015 025 035 045 125 135 145 234 235 245 345`.
For each of the 11 source-clause deletions, complete original-C satisfying twofold-cover witnesses are supplied in the local reproducibility package; **220 lifted original-C clauses independently verified**. Thus this example is inclusion-minimal under *twofold-cover UNSAT*, but NOT source physically clause-critical: all 11 **original single-sheet** clause deletions remain UNSAT by exhaustive 5^6 search. Incidence girth is 4, not growing. Do not extrapolate algorithmic hardness or girth.

## Reproducibility, separate verifiers

Local archive: `T5C_RedTeam_TwoFold_Optimality_20261119.zip` contains `twofold_lift_audit.py`, `independent_verify.py`, `k5_twofold_sat.json`, `cover_critical_11_witnesses.json`, `results.json`, `independent_results.json`, REPORT.md, HANDOFF.md and SHA256SUMS. Reproduce `python3 twofold_lift_audit.py && python3 independent_verify.py && sha256sum -c SHA256SUMS`. No random seed; all search deterministic.

Two independent checkers use respectively the original directed R-predicate and unordered sets of 3 consecutive residues, agreeing on all **125** triples and the **30** valid ones. Enumerating the 15 unordered two-copy color types, exact counts of fully compatible complete-source type **multisets** for n=1,...,6 are `15,120,85,5,1,0`. A separate backtracker exhausts the 11-clause core; 2,332,365 attempted extensions with no feasible twofold covering. The prior native 25-variable, 25-clause, girth-8 critical source's 1,046-node UNSAT tree and 25 deletion witnesses were independently replayed; the native equality gadget has precisely 20 models, all with equal terminals.

## Complexity-theory firewall / next task

**FALSIFIED:** Any universal claim that every strict-C input can be made SAT by a 2fold incidence cover. **PROVED:** 3fold is optimal for the existential-universal covering statement. **OPEN:** High-incidence-girth physically clause-critical family with cover resistance, complete deterministic refutable-block acquisition for all z, and unrestricted P vs NP.

Cover SAT does not preserve base SAT, criticality, or original proof hardness. The shared-row/private-block scan still costs `N^(0.845+0.35a)`, requiring `a<=97/70` to fit `N^1.33`, and has unresolved source access, verification and live-space obligations. No transfer from these finite constructions to unrestricted SAT lower bounds.

Background literature: Gross and Tucker, *Generating all graph coverings by permutation voltage assignments*, Discrete Mathematics 18 (1977), 273-283, DOI 10.1016/0012-365X(77)90131-5; Buss and Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity 24 (2015), 533-600. The original strict-C definition and previous 3fold construction were reviewed against the user's research PDF and repository. This is not a historical priority claim. **P versus NP remains open.**

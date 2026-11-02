# LSPV-3 GATE328: paid cross-tractable SAT/Circuit-SAT continuation implication

2026-11-02 04:24 PST. PROVED/EXACT elementary restricted theorem; COMPUTATIONAL independent finite controls; external referee pending. P versus NP OPEN.

## Exact obstruction and theorem

The only original language is valid duplicate-free proper Döcker Monotone 3-SAT-(2,2), with malformed inputs rejected. All comparisons preserve identical original clause IDs, original names and the SAME original F; a pinned ordinary CNF is not a new canonical original.

For coherent pins p,q on the SAME original-variable domain S, let H_p(y)=F(p,y) and H_q(y)=F(q,y) denote exact residual CNFs. If a paid source recognizer establishes that H_p belongs to a tractable unit-restriction-closed CNF class (2SAT, Horn or dual-Horn), then full pointwise continuation containment H_p => H_q is decidable with at most m(F) polynomial SAT calls, even when H_q is arbitrary CNF:

H_p => H_q  iff  for every clause C in H_q, UNSAT(H_p AND all unit negations of C).

Each H_q clause has width <=3. Negated clauses become at most three unit assumptions. The selected antecedent SAT class remains tractable: SCC for 2SAT; forward-chaining for Horn/dual-Horn. An inconsistent query gives a source-provenanced 2SAT SCC path or Horn closure proof; a satisfiable query supplies a future-assignment counterexample. For exact cofactor equivalence, pay both directions, requiring independently recognized tractable antecedents, possibly of different types. The theorem also extends to a source-authenticated affine GF(2) antecedent, but only after separately charging derivation and verification of its actual equivalence to the source cofactor. No free parity semantics or SAT-label oracle.

This is an elementary known consequence of tractable satisfiability under arbitrary units, not a new unrestricted complexity theorem. Previous LSPV-1 COFACTOR-2SAT-CONTINUATION316 proved a four-query single-pivot Krom case. GATE328 extends the paid test to arbitrary same-domain cofactor pairs, Horn/dual-Horn antecedents and general CNF consequents.

## Falsifiers and limits

1. Full Boolean continuation tables are mandatory for containment from tractable antecedents: FALSIFIED by the exact paid implication test.
2. Source crossing-clause coverage is complete on F9: FALSIFIED by the finite census below.
3. Arbitrary conjunctions of easy types are automatically easy: FALSIFIED; any 3CNF can be encoded as Horn clauses together with binary clauses enforcing complement proxy variables. These are noncanonical ordinary comparator CNFs, NOT valid target children.
4. This yields polynomial all-input total work: UNPROVED, because the number of states and policy-acquisition/failed-selection costs can be exponential.

## Source-authenticated exhaustive census

For Z6 (n=6, m=8, 18 original models): 729 source cubes, 15,625 aligned-domain ordered pairs, 15,152 tractable-antecedent eligible comparisons, 9,764 exact implications, 8,150 source-certified implications, 1,614 additional implications, 642 additional with both cofactors nonzero, zero nonzero tractable-to-general improvements.

For F9 (n=9, m=12, 70 original models): 19,683 source cubes, 1,953,125 ordered pairs, 1,859,632 tractable-antecedent eligible comparisons, 1,328,080 exact implications, 1,140,939 source-certified implications, **187,141 additional exact implications**, including **24,983 with both cofactor languages nonempty** and **503 nonempty tractable-antecedent to GENERAL-consequent implications**. The 171,512 cross-type easy-pair equalities in the census were zero-function coincidences; no nonzero cross-type equality beyond source identity was found. Do not inflate vacuous merges.

Explicit same-F9 nonvacuous example: pins to S={x1,x2,x3,x5,x6}. For p=(1,1,0,0,0), the cofactor is (x4 OR x9) AND (x7 OR x8 OR x9) AND (NOT x9), a dual-Horn residual. For q=(0,1,0,1,0), the consequent is (x4 OR x9) AND (x7 OR x8 OR x9) AND (NOT x7 OR NOT x9), a GENERAL CNF. H_p implies H_q for all future pins, but original source coverage fails to certify it. Both continuations are satisfiable. This particular example is also visibly unit-simplifiable; no exclusive advantage over UP is claimed.

Original F9 pinned controls: common (x2,x3,x6)=(0,0,1); x1=0 has exactly one original-clause-checked witness, x1=1 has zero completions and all 32 UNSAT suffix leaves have original-clause falsification IDs. Original F9+Z6 (explicitly named to avoid other Y6/F15 fixture conflicts) is canonical n15,m20 with 1,260 models. An unshared fan-in-two OR/AND source evaluator matches all complete original-input truth values for Z6/F9/F9+Z6 with 23/35/59 gates. Source complement identities, all 112/264 clause-pair SS/SU/US/UU modes and five malformed originals passed. U198/V198 and differently sourced Y6/F15 inherited, not freshly replayed.

The Python producer executed 112,583 paid clause-entailment attempts, 35,037 2SAT SCC calls, 3,042 Horn/dual-Horn calls, 111,856 implication edges and arc visits, 133,799 target-unit reads, 9,591 Horn rule scans on F9. An independent no-producer-import Node.js verifier recomputed source truth/cofactor semantics and completed **2,042,524 checked assertions**, agreeing on every reported count. Exact cofactor truth tables used exclusively for OFFLINE testing, not the proposed paid implication test.

## Total-work recurrence and gap

A conservative per-pair indexed bit-machine implementation uses O(N^5) bit work and O(N^3) writable/index/proof bits, including source grammar, authenticated residual extraction, type recognition, all tested clauses, SCC/forward chaining, source/index/head reads, counterexamples/certificates and proof verification; these are conservative theoretical bounds, not native FLMV measurements. Pairwise comparison of k retained states can cost O(k^2 N^5) and O(kN^3) peak if all are retained. A controller must also pay failed policies, selection/switching, GE/affine proof discovery, caches/replay, child/output/bit accesses and DELAY/COPY/RECOMP guests, plus simultaneous ancestor and guest writable space:

W(z)=C_grammar/source/index/head/discover/select/switch/failed/proof/cache/GE/guest(z)+SUM_{u in executedSucc(z)}(C_child/output/bit(z,u)+W(u)).

No polynomial bound for aggregate encountered state count, all-input width, selector acquisition or total recursive descendants is established. No hereditary canonical child reencoder, arbitrary A to power-short Phi(A), or strict numerical same-machine FLMV transport. Logical full-state XOR is OFFLINE only. P versus NP OPEN.

## Prior work and search

Read first the verified five-role SAT/Circuit-SAT handoff, then decision-only handoff, saturated-cycle theorem and issue #3 via authenticated GitHub connector (generic public web blob returned 404). Searched j15marti/pnp for Horn/2SAT cofactor implication and located LSPV-1 316, GATE321/322/327, LSPV-4 331/332. Searched github.com/openai and found openai/math Lean comparator material, no validated unrestricted SAT result used. Primary literature checked: Schaefer STOC 1978 doi:10.1145/800133.804350; Darwiche-Marquis JAIR 2002 doi:10.1613/jair.989; Aspvall-Plass-Tarjan IPL 1979 doi:10.1016/0020-0190(79)90002-4; Döcker 2019 arXiv:1912.08032; FLMV JACM 2005 doi:10.1145/1101821.1101822.

Artifacts: role-owned report, compact executable, machine-readable summary; complete standalone producer, independent verifier, full raw and manifest in reproducibility archive. Root main.tex deliberately untouched pending safe authenticated full-blob LSPV-3-only reconciliation. No existing task identity, title, enabled state or schedule modified.


## Fresh direct DPLL and offline logical-XOR adjunct

Independent UP-first source-CNF DPLL on the same F9 original coherent SAT1/UNSAT0 pins resolved both in one recursive node, with 70 versus 34 original-literal inspections, respectively; 5 versus 3 forced unit assignments, and zero branch decisions. In contrast, the cross-class semantic implication census builds reusable information for MANY possible future continuations; it is not shown to beat direct SAT decision on these easy controls.

Fresh OFFLINE full clause-status logic encoding, fixed two bits per original clause, enumerated all 512 complete F9 assignments in both binary and Gray orders. Adjacent XOR popcount sums were 3,964 (binary) and 3,074 (Gray); endpoint XOR popcounts 24 versus 4, maximum adjacent changes 24 versus 8. Each of these summaries costs a complete source-state trace to obtain. They are NOT an online SAT oracle, do not measure actual changed writable tape cells and confer no native-machine time lower bound. The original 0^n/1^n assignments each falsify all six F9 clauses of the opposing sign; these endpoint failures do not establish global UNSAT.

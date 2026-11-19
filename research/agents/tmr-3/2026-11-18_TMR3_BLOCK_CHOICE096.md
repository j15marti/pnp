# TMR-3/096: correct-polarity block discovery versus the published 1.34070/.5 exclusion

2026-11-18 PST. Owner TMR-3 / PNP Time-Space Tradeoffs. **PROVED/EXACT:** factorization theorem, authenticated search recurrence, and contradiction for an alleged *all-CNF* deterministic 1.33/.5 solver. **KNOWN THEOREM:** Buss--Williams 2015; Diehl--van Melkebeek--Williams 2011. **COMPUTATIONAL:** finite reproducible controls. **OPEN:** general-CNF block compiler, small-space strategy verification, unrestricted worst-case lower bound. P versus NP OPEN.

## Dependency, theorem and falsifiers

For authenticated conjunctive sources `F(z,y_1,...,y_M)=AND_{i=1}^M B_i(z,y_i)` with pairwise-disjoint private variables `Y_i` and shared `s=|z|`, the exact statements are

`SAT(F) <=> exists z forall i exists y_i B_i(z,y_i)`

`UNSAT(F) <=> forall z exists i forall y_i not B_i(z,y_i)`.

These follow by the independence of the private existentials. A uniform specialist enumerates shared assignments, tests each child with a complete solver, stops testing a particular z at its first UNSAT child, and reports UNSAT only after all `2^s` shared assignments are covered. If all children SAT for one z, it replays to extract original-variable assignments, verifies every original clause and emits SAT plus witness. The verifier and source parser must reject malformed encodings, missing clauses, overlapping private-variable claims, or a mismatched displayed decomposition.

Let `j(z)` be the first negative child index (or M for an all-positive z). Write `p_{zi}` for restriction/materialization/input access, `C_{zi}^{+/-}` for total actual child work including internal failures, `v_{zi}` for checking and `h_{zi}` for indices/cache/replay management. For the declared exact sequential execution,

`T <= P(N)+SUM_{z}SUM_{i<=j(z)}(p_{zi}+C_{zi}^{actual}+v_{zi}+h_{zi})+1_SAT*SUM_i(p_{z*i}+C_{z*i}^{+}+v_{z*i}+h_{z*i})+L(N)`.

The last sum is SAT witness replay, `P` authenticates the **entire original source**, and `L` verifies and outputs the answer. The peak writable-space ledger on the SAME execution is `S_auth+S_z+S_index+max_i(S_child_i+S_restrict_i+S_check_i+S_one_witness_i)+S_output_buffer` when those buffers are truly reused; otherwise charge their union. Materialized input and retained whole witnesses cannot be suppressed. On-demand restriction must pay for each source access.

**FALSIFIER 1:** `(y) AND (!y)` has both singleton blocks SAT but their conjunction UNSAT, because private variables overlap. **FALSIFIER 2:** `(y AND !y) OR w` is SAT although one block is UNSAT. For an AND of disjunctive rows, UNSAT instead requires `forall z exists row forall child UNSAT(child|z)` under suitable disjointness, not one negative child in a row. **FALSIFIER 3:** An UNSAT choice `i(z)` can depend on z. A literal choice table has up to `2^s ceil(log2 M)` bits; compressing it into k bits entails charged generation and ALL downstream child decisions. Choosing an UNSAT child is not refuting it.

## Exponent ledger

For M<=n^.65 total blocks, local size <=n^.35, seed time `ell^(alpha+o(1))`, and paid amortized source work `n^(1+o(1))`, direct enumeration gives `T=O(2^s n^(.65+.35 alpha+o(1))+P+L)`. A 1.33 exponent requires `s<=delta log2 n+o(log n)` and `delta+.65+.35 alpha<=1.33`, unless a separately proved cross-z accelerator is used. At `s=n^.195`, enumerating all z costs `2^(n^.195)`, superpolynomial. For constant s, `alpha<=68/35=1.942857...`. The seed's n^.5 space budget alone requires `beta<=10/7` for local space `ell^beta`. A polynomial seed with unspecified exponent is insufficient.

If n^.65 blocks occur PER row and there are n^.195 rows, there may be n^.845 blocks and n^1.195 total literal-sized data; replace `.65` by `.845`, giving the stronger constraint `alpha<=97/70=1.385714...` at delta=0. One must normalize n to the *actual encoded bit length* N before using any published SAT lower bound. Materializing a source or scanning every prefix may add polynomial overhead and destroy the apparent 1.33 bound.

## MAIN RESULT: Published deterministic RAM exclusion

**KNOWN THEOREM:** Buss and Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity 24 (2015), Figures 8.2 and 8.3, explicitly establish an alternation-trading refutation for SAT in `DTISP(N^1.34070,N^0.5)`. The figure notes a refutation at 1.34070 and no such proof at 1.34071 **within this proof system**; the latter is not a general algorithm upper bound. Their DTISP definition uses simultaneous `N^(c+o(1))` time and `N^(epsilon+o(1))` work space. The earlier Williams (2013) table had the weaker point 1.32/.5. See https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf pp.58-59 and https://doi.org/10.1007/s00037-015-0104-9.

**PROVED/EXACT COROLLARY:** A *uniform, correct-on-every-CNF*, fully charged deterministic RAM decider in `N^(1.33+o(1))` time and `N^0.5 polylog(N)` writable space contradicts the published theorem because 1.33<1.34070. The hypothetical polynomial-time SAT seed does NOT guarantee those cost exponents. The barrier does **not** apply without a full all-CNF reduction and precise time/space transfer to a restricted factored or T5-critical-deletion promise. No contradiction with P=NP follows: it can hold with slower or larger-space polynomial algorithms.

With a materialized reduction of length `N'=N^(gamma+o(1))`, time `N^(rho+o(1))` and work space `N^(sigma+o(1))`, solving target at `T'(N')=N'^c, S'(N')=N'^epsilon` yields (before decoder/output extras) `T_SAT=N^(max(rho,gamma*c)+o(1))`, `S_SAT=N^(max(sigma,gamma*epsilon)+o(1))`, PLUS `N'` bits if the constructed input is retained. A virtual source must charge each bit-generation call instead. NP-completeness alone does not establish `gamma=1`.

## Free routing, k-bit correct path, polarity exclusions

For deterministic path verifiers `V_+(F,a)`, `V_-(F,a)`, soundness requires **every** accepting path of `V_+` imply SAT and **every** accepting path of `V_-` imply UNSAT; wrong paths must reject/abstain rather than issue the opposite label. Complete short checkable YES paths exist for SAT; if `V_-` is polynomial-time, polynomial-length and complete on **all** UNSAT formulas, then `UNSAT in NP` and hence `NP=coNP` (unknown). With k writable guess bits charge k; with random-access read-only certificate bits one must change models or pay materialization/replay/consistency. Deterministic enumeration costs up to `2^k` full verifications and other access. A semantically pre-guaranteed correct polarity answer is a free oracle, not computation.

**SAT nondeterministic YES:** standard satisfying witness; no applicable unconditional nondeterministic SAT lower bound of the form below. **UNSAT nondeterministic YES:** equivalently TAUTOLOGIES. Diehl, van Melkebeek, Williams, J. Comb. Optim. (2011) prove that for each `d<4^(1/3)=1.587401...`, there exists **some e>0** excluding a nondeterministic random-access TAUTOLOGIES decider in simultaneous `N^d` time and `N^e` space. More generally for `c^2*d<4` the language cannot have BOTH an `N^c` nondeterministic-time decider and an `N^d,N^e` nondeterministic time-space decider. This **does not prove** that e=.5, so no exclusion of nondeterministic `N^1.33,N^.5` follows without additional analysis. A freely writable/readable k-bit advice tape need not be the standard nondeterministic low-space RAM. See https://doi.org/10.1007/s10878-009-9286-x and https://pages.cs.wisc.edu/~dieter/Papers/taut-ts-full.pdf.

## Verified controls and barriers

The executed independent full-Boolean brute-force comparison checked 1320 disjoint-private random conjunctive CNFs (717 SAT, 603 UNSAT); actual specialist child calls: 2467 YES, 1483 NO and 1539 SAT replays. It also tested both logical falsifiers and wrong-path rejection. T5 rotation-aware exact search on k=3 and k=6 rigid modular pin cycles confirmed respectively 6/9 and 0/18 physical-edge deletions SAT, ruling out the idea that source gadget size or pin inconsistency is intrinsic witness hardness. The reproducibility ZIP holds source and two byte-identical audit runs. **1351 assertions, zero failures; COMPUTATIONAL only.**

Four gates: DISJ PASS on authenticated conjunction/FAIL on overlap or OR confusion; relativization OPEN for separation; simultaneous DTISP PASS for the published full-CNF exclusion, OPEN for any actual restricted specialist transfer; deterministic configuration NOT APPLICABLE as an all-machine lower bound from a representation statistic. Algebrization, natural proofs and the full peer audit are OPEN for stronger claims. /341 FAIL as whole-UNSAT authority; /386 RESTRICTED.

**Next blocker C3-BLOCK-CHOICE-COMPILER097:** Construct or falsify an exact and charged general-CNF-to-private-block reduction with true witness/UNSAT preservation, then account for all z enumeration, every child polarity and source accesses. A complete 1.33/.5 all-CNF implementation is unconditionally ruled out by Buss--Williams; the research problem is identifying which specific proposed arrow fails. Native TM audit, independent mathematical review and combined-manuscript compilation remain pending. P versus NP OPEN.

Sources: [1] https://doi.org/10.1007/s00037-015-0104-9; [2] https://people.csail.mit.edu/rrw/automated-lbs.pdf; [3] https://doi.org/10.1007/s10878-009-9286-x; [4] https://doi.org/10.1145/1101821.1101822.

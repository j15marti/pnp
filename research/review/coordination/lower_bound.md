## LB-0015 — exact black-box query-scale dichotomy (2026-10-11)

**PROVED/EXACT pending independent review:** `BLACKBOX-QUERY-SCALE-DICHOTOMY1`. Positive-polynomial-scale reached queries cannot share one charged exponent across every polynomial SAT implementation; vanishing-scale queries become an ordinary source algorithm under `P=NP` with time exponent `max(r,eta)`.

**FALSIFIED/RETIRED:** `SUBPOLY-BLACKBOX-IS-INTERMEDIATE1`.

**OPEN:** `SUBPOLY-SOURCE-COMPILER1`, arbitrary-decider compatibility exposure, a matched FLMV contradiction, nonrelativization, nonalgebrization, and P versus NP.

**COMPUTATIONAL:** 28,512 exact exponent, wrapper, clean-core, hostile-family, and encoding checks passed in 0.77 seconds.



## LB-0014 — annotation-semantics trilemma (2026-10-11)

**PROVED/EXACT:** `ANNOTATION-SEMANTICS-TRILEMMA1`. For a locally projectable encoding, an ignored annotation can be erased; a correctly annotated promise input need not be validated; and requiring validity defines a different total language.

**FALSIFIED/RETIRED:** unqualified `TAG-VALIDATION-TO-UCORE1`. Tag-generation or validation cost is not automatically cost of a one-bit SAT decider.

**COMPUTATIONAL:** 524,288 promise checks, 2,097,152 erasure checks, 2,097,152 validation checks, 1,572,864 mutations, all wrapper/easy-family controls, and the clean-core block passed.

**OPEN handoff:** prove `JMV-NATIVE-TAG1` or the exact local parent-port accessor as external reduction infrastructure, then locally normalize and compose one SAME_REALIZATION endpoint. Do not require downstream tag validation. UCORE-TIME1 and P versus NP remain OPEN.

Report: `research/review/reports/lower_bound/2026-10-11_1612_LB-0014.tex`.
Script: `experiments/review/annotation_semantics_trilemma.py`.
Raw result: `results/raw/review/2026-10-11_annotation_semantics_trilemma.json`.
## LB-0013 — clause locality versus incidence locality (2026-10-11)

**PROVED/EXACT:** for a raw length-L occurrence stream with a three-occurrence key at pivot p, deterministic occurrence-rank query depth is exactly min(p,L-p-1), except constant-output boundary cases. On Monotone 3-Sat-(3,3), two native tag bits per literal make the rank directly accessible with constant-factor encoded-length overhead.

**FALSIFIED/RETIRED:** `RAW-INDEX-TO-UCORE1`. A raw stateless probe lower bound is not an encoding-invariant semantic obstruction and does not force work in arbitrary one-bit SAT deciders.

**COMPUTATIONAL:** 2,852 exact decision-tree, tag, renaming, and permutation checks passed.

**Handoff:** prove or falsify `LOCAL-COOK-BILOCAL-M33-1`: a local first leg supplying both clause fields and valid sign-specific incidence tags from the exact FLMV/Jahanjou--Miles--Viola source, with every preprocessing/index/validation cost charged. UCORE-TIME1 and P versus NP remain **OPEN**.

Report: `research/review/reports/lower_bound/2026-10-11_1512_LB-0013.tex`.
Code: `experiments/review/clause_incidence_locality_separation.py`.
Raw result: `results/raw/review/2026-10-11_clause_incidence_locality_separation.json`.

# LOWER_BOUND-0001: universal lower-bound audit and recovered oracle barrier

Date: 2026-10-10 UTC. Status: P versus NP remains OPEN.

This run recovers the strongest current project spine, tests the missing all-algorithms implication, and closes a previously deferred oracle-immunity barrier under explicit machine conventions. It does not construct an all-input SAT wrapper or establish a separation.

## Current proof spine, grounded in current files

The current GitHub main4.tex and main5.tex include reports through ARC15 dated October 9. The October 8 signed-twin refinement is a useful component, not the current research endpoint.

The most developed spine is:

P = NP -> one fixed polynomial-time SAT decider -> [OPEN all-input charged shrinking construction] -> [PROVED CONDITIONAL recursive closure] -> a forbidden joint SAT time-space pair.

FORMAL-SPINE1 already makes the key logical point precisely: the missing implication from polynomial SAT to its all-input wrapper is separation-strength, because the wrapper contract is independently excluded by the known endpoint. REDTEAM-STRENGTHEN3 further shows that if a favorable phase may decide its parent directly and issue zero children, existence of the phase is equivalent to existence of the already-forbidden endpoint algorithm. Requiring a dummy child does not fix the problem.

Recovered aggregate closure:
C = max{1, r, (v-h)/(1-h)}, P = max{p,h},
with local time exponent r, aggregate executed child volume v, maximum child exponent h<1, and charged local state p. The parameters (r,v,h,p)=(6/5,11/10,1/2,1/2) yield (C,P)=(6/5,1/2). This is genuine conditional elimination of the inherited exponent K. Its proof does not construct missing children or answer UNKNOWN cases.

Fortnow-Lipton-van Melkebeek-Viglas, Section 2.1, Theorem 3.1 and Corollary 5.8, are the model-matched endpoint. The exact arithmetic was independently checked:
c=1201/1000,
d(c)=((c+2)/c^2-c)/2
=1/2+26275399/2884802000.
Thus 6/5<c and 1/2<d(c), with strict margins for polylogarithmic encoding overhead. This theorem forbids a simultaneous time-space pair; it does not forbid unrestricted polynomial time.

ARC15 improves positive coverage by verifying a discovered assignment against the source. It reports 12/13 versus 6/13 on one declared sample and still returns UNKNOWN on an UNSAT sample. Its own document says total bit-time and peak workspace remain unproved. It therefore supplies neither the universal negative-case coverage theorem nor a joint resource certificate.

## Exact missing link selected

The current route needs a construction that covers every source input and every actual unresolved successor with one uniform all-length implementation, while meeting the complete resource ledger. A source-visible PRE-A shrinking macro is a sufficient constructive interface. It is not yet a theorem following from P=NP.

An existential implication is sufficient for a contradiction. A compiler that transforms every clocked polynomial SAT decider into the required wrapper would be stronger and easier to audit operationally. These quantifiers must not be conflated.

The historical alternative SAT-MERGE-FORCING1 needs an independently forced intermediate service and a representation-independent lower bound for that service. Neither exponential history count nor satisfiability of the wrapper's auxiliary constraints forces an arbitrary SAT decider to reconstruct those auxiliaries.

## Falsification before proof

1. Endpoint bypass is decisive against generic history forcing. Under an assumed polynomial SAT decider A, a program required only to output SAT(F) can call A(F) and ignore all wrapper-created hashes, primes and history. The repository had already proved this in LEAD-0025. This run preserves the result rather than relabeling it as an open conjecture.

2. Future distinguishability proves a storage bound only in a model that forbids reacquisition. If q pairwise distinguishable histories must be answered from an s-bit summary alone, 2^s >= q. This does not imply q time steps. If the original source remains readable, x in {0,1}^k has 2^k distinguishable query-response rows under query i -> x_i, but one random-access read answers each query.

3. An exponentially large trace family can have a polynomial-size shared circuit. The recovered BAD-SEED construction uses one existential SAT query to search for a violating seed. Under P=NP that query is easy. Universal route quantification is not itself a contradiction.

4. A zero-child favorable phase is just the endpoint algorithm in different syntax. Causal acquisition, essential child information and a fully charged implementation matter, although they do not make the missing implication automatically weaker in logical strength.

5. SOURCE-GROUNDED and SAME_REALIZATION are necessary semantic discipline, not sufficient nonrelativization. A fixed-realization oracle supplies mutually consistent answers. The earlier LQP finite surrogate already exhibits future distinguishability with cheap reacquisition.

## New rigorous closure of a deferred barrier lemma

PVG-4-0001 on September 28 left the relativized immunity proof as CANDIDATE. The primary Hirahara theorem and its actual proof were read this run. With one common oracle and an efficiently universal oracle machine, the proof extends directly.

Let t(n) eventually dominate every polynomial. Let b(n) be a nonnegative integer function bounded by O(log n), and define
R_b^{t,O}={x : K_U^{t,O}(x) >= |x|-b(|x|)}.

Under the explicit efficient-universality conventions in the companion manuscript, R_b^{t,O} is P^O-immune.

Proof idea: from an infinite P^O subset, retain a prefix of length n-m with m a sufficiently large constant times log n, encode n, and enumerate all m-bit suffixes using its fixed decider. This prints one member in polynomial oracle time from a description shorter than n-b(n). Universality adds only constant description length and polynomial time. The result contradicts the definition for all sufficiently large occupied lengths.

This gives the former two-valued verifier barrier and a modest generalization:

Let L(n)>=1 be an integer, polynomially bounded and polynomial-time computable, ell(n)=ceil(log_2 L(n)), and k(n)=n-ell(n)-1. For all sufficiently large n, k(n)>=0. Suppose one polynomial-time oracle verifier with polynomially bounded witnesses accepts at most L(n) distinct n-bit outputs per program p of length at most k(n), while including the true final output of every such program that halts within t(n). Then P^O != NP^O.

The counting step is
|E_n| <= L(n)(2^{k(n)+1}-1) <= 2^n-L(n) < 2^n.
Completeness puts the nonempty complement at each sufficiently large length inside R_ell^{t,O}; that complement would be in P^O if P^O=NP^O, contradicting immunity.

L=2 recovers the historical threshold |p|<=n-2 and K>=n-1. Polynomial list size is possible in the conditional theorem if the program-length threshold loses O(log n) bits. This generalization does not produce such a verifier. Its existence remains an open separation-strength object.

A collapsing oracle from Baker-Gill-Solovay therefore cannot admit this matched relativized verifier. This is an exact diagnostic identifying which missing construction must fail in an equality world. It does not disprove the ordinary verifier at the empty oracle or prove P!=NP.

Independent REDTEAM review accepted the core oracle argument with guards now included in the manuscript: one efficient universal oracle model, counted query writing, single final halting output, a fixed polynomial witness bound, global list soundness over the same permitted witnesses, and finite small-length exceptions.

## Cross-agent correction affecting recovered LSPV source

REDTEAM found a precise error in Drive MAIN LSPV-5::58501: surjectivity onto F_q^m does not imply there is no nonzero formal polynomial vanishing on that set, since X_1^q-X_1 is such a polynomial. The correct conclusion concerns nonzero polynomial functions or individually degree<q reduced representatives. The fixed-seed interpolation lemma itself survives, and its proof can avoid the shared-separating-functional hypothesis using per-pair coordinate factors. This audit does not adopt the overbroad formal-polynomial wording.

## Status of strongest families

| Family | Strongest recovered component | Exact unresolved implication |
|---|---|---|
| ARC/WRAPPER | Charged recursive closure; strict FLMV endpoint; partial source-visible constructors | P=NP supplies a complete all-input successor/terminal construction with favorable replay and workspace |
| PFCERT | Bounded-image counting; generalized relativized immunity barrier proved here | Existence of a polynomially witnessed bounded-list endpoint cover for the selected t |
| LSPV/RMV | Exact orbit recurrence, source-specific separator formulation, quantitative conditional reconstruction | Canonical Boolean separator/graph compression, exact extractor interface, full diagonal |
| LQP/merge forcing | Correct future-equivalence semantics; restricted summary lower bound | Independently forced service and lower bound robust to source rereading, recomputation and oracle access |
| DPLL/Resolution | Structural transfer and restricted lower bounds indexed in PROVED_EXACT | An unrestricted algorithm-transfer theorem; no such theorem recovered |

## Next run: one falsifiable task

For the current ARC/WRAPPER program, recover the exact remaining ARC15 UNSAT input and its complete source/descendant ledger. Seek one source-checkable negative-case rule with a proved domain and resource bound. Test it on descendants and the shielded SAT-complete fallback, not only on the original small instance. A rule that works only on the sample becomes a scoped lemma, not all-input coverage.

For the formal PFCERT branch, treat the generalized polynomial-list theorem as a target specification. Fix t explicitly, then ask whether proposed certificates actually give polynomial witnesses and a global output cap. Respect the independent cost-certificate agent's enumeration barrier for very large t.

## Sources and coverage

Directly read current GitHub sources:
- main4.tex, blob 3b169a649144be041c40387ab6f08ff3ffeec147.
- main5.tex, blob 3782ee13849485bcda85791d651b7356c385618c.
- research/agents/lead/2026-10-08_FORMAL-SPINE1.tex, blob 5dfe60c2d4abb65e3eab2a3362539c6de4eaac75.
- research/manuscripts/FORMAL-SPINE1/main4_addition.tex, blob 8a3c370e17c02188f14025d746a8a160d2308446.
- research/manuscripts/RECOVERY-STRENGTHEN7/main4_addition.tex, blob 9b0ed6e54b649c44d101a84e820d24d9c92444f0.
- research/manuscripts/RECOVERY-STRENGTHEN10/main4_addition.tex, blob b011397f7fbe1db6c938862e68a5c6830bc7cdbb.
- research/manuscripts/REDTEAM-STRENGTHEN3/main4_addition.tex, blob 1698b22406b85d0cbc1349bde3450c5fffa94e08.
- research/manuscripts/ARC-STRENGTHEN2/endpoint_addition.tex, blob ced0f94dcb91d8f32b2110b0cc0a55583427e285.
- research/manuscripts/ARC-0009-TWIN-REFINE/main5_addition.tex, blob b1835972ef08c403f27e009e3091aff9cde1a6f2.
- research/agents/lead/2026-10-06_1518_LEAD-0025_SHARED_BAD_SEED_ENDPOINT_BYPASS.md, blob 2d85d03f37be02aee9e1484bd7d3eb1dcfff5cd7.
- research/agents/proof/2026-10-09_1940_ARC15.tex, blob 5ba966c85a07c60681517486c61ce4d8d995bb7c.

Repository: https://github.com/j15marti/pnp
Search results were pinned by the connector to commit b6948eb15a8afec37cc904120ce20b61b45a0dad. File fetches were default-branch reads with the blob SHAs above; no atomic whole-repository snapshot is claimed.

Drive reads, with source snapshots saved locally:
- Claim Ledger: 17NPKIB2yB1xZ12iy3eyY_0fk0vOh8DEkwZJtepk36-A.
- Open Problems & Priority Queue: 1UtZ3W7ru7jKP50EvMTJgOZNG1R0F2G_6HKr8rYsl2Ok.
- NONALG-0003: 1w8sE_27wVea0Ne24DEdZgkX8KABksf7MfwNrBqjfZKU.
- PVG-4-0001: 1JVCcWJC4oQ-wQhOHMb_cuid0aQ6H7gCLUpjt2xG8vN8.
- LSPV-4-29401: 1kyZCE87N4eotLJZBNtxxZHVdvJaB8bq4VQkce3tyA-s.
- MAIN LSPV-5-58501: 1z4Jaoi4P0ZJXU8DTemXW6Eqb3vvt5RosAZTWuVMeCG0.
- PROVED_EXACT index search hydration reviewed: 1J7ZGCqGO1bm7D7l5uJT-qI8yEcxTIYUgjDnVBlyZQv8. This is an index, not independent verification of every linked proof.

Primary literature actually checked:
1. Shuichi Hirahara, Unexpected Hardness Results for Kolmogorov Complexity Under Uniform Reductions, STOC 2020 / ECCC TR20-050, Theorem 3.9 and its proof on printed page 29. https://eccc.weizmann.ac.il/report/2020/050/download
2. Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, author manuscript dated 2004-09-07, Section 2.1 and Corollary 5.8. https://lance.fortnow.com/papers/files/tst.pdf
3. Baker, Gill, Solovay, Relativizations of the P=?NP Question, SIAM Journal on Computing 4(4), 431-442 (1975). https://doi.org/10.1137/0204037
4. Hirahara, Kabanets, Lu, Oliveira, Exact Search-To-Decision Reductions for Time-Bounded Kolmogorov Complexity, CCC 2024. Metadata/abstract checked only, not used as a theorem premise. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2024.29

Coverage limitations: Personal Context returned unavailable in this agent; full chat history was not reviewed. Parent retrieved additional context independently. Historical Claim Ledger/queue were retrieved in full, but reviewed selectively by relevant claims and current superseding sources. Main4/main5 include many manuscript files not all expanded in this run. The attached HTML tools were assigned to other agents. No claim of exhaustive archive coverage or machine-checked proof is made.

Additional constructive artifact: LSPV_candidate_spine.tex formalizes the full successful RMV union, a proved quadratic-OR separator lemma, and Route B's different graph-separator obligation. It explicitly distinguishes O(w) circuit size from O(w log m) descriptor bits. The current van Melkebeek-Mocelin Sdroievski journal PDF was checked at Section 4.1 and reconstruction interfaces: https://pages.cs.wisc.edu/~dieter/Papers/r-am-instance-wise-cc.pdf. Its Definition 4.1 and Lemma 4.2 supersede the older manuscript numbering used in archive reports. The old author-PDF URL returned 404. The Shaltiel-Umans PDF fetch timed out, so no unverified exact transfer is promoted.



## LB-0006, raw causal-use guard

REPLICATION-CAUSAL-GUARD1 is PROVED/EXACT in the declared checkpoint model,
with independent red-team review pending.  Odd repetition of the complete
work configuration defeats every polynomially bounded raw-cell intervention
while preserving exact uniform polynomial-time behavior.  Raw-coordinate
causal indispensability is therefore retired as a universal EXTRACTOR/G2
premise.  A decoded representation-covariant functional remains OPEN and must
survive DIRECT/RECOMP, charge decoding/replay, and yield strict source-scale
contraction or another independent endpoint.

Report: `research/review/reports/lower_bound/2026-10-11_0612_LB-0006.tex`.
Experiment: `experiments/review/causal_replication_guard.py`.
Raw result: `results/raw/review/2026-10-11_causal_replication_guard.json`.


## LB-0010, nonempty-pin equivalence guard

NONEMPTY-PIN-EQUIVALENCE1 is PROVED/EXACT in the declared syntax and machine interface, with independent red-team promotion pending. A proper monotone two-clause lift makes either value of one required nonempty pin equal the source SAT bit with linear encoded-size overhead; the reverse residual-to-proper-3-CNF compiler is also linear. EMPTY-QUERY-EXCLUSION-REPAIR1 is FALSIFIED/RETIRED. A balanced (2,2) pin lift, restricted representation compiler, matched endpoint, and P versus NP remain OPEN.

Report: `research/review/reports/lower_bound/2026-10-11_0912_LB-0010.tex`.
Experiment: `experiments/review/nonempty_pin_equivalence_audit.py`.
Raw result: `results/raw/review/2026-10-11_nonempty_pin_equivalence.json`.


## LB-0016 — all-branch restriction fanout

ALL-BRANCH-ENCODED-FANOUT1 is PROVED/EXACT pending independent review.
Exact-(2,2) incidence counting converts fixed power-size residuals into
2^{Omega(N/log N)} explicit branch volume. This closes complete block
enumeration only. Source-dependent pruning, implicit charged access,
arbitrary-decider transfer, and P versus NP remain OPEN. The next falsifiable
target is PRUNED-SOURCE-PASS-ACCESS1.

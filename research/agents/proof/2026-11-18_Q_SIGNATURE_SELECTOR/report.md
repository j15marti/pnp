# Q-SIGNATURE-SELECTOR: a costed extension beyond two head names

18 November 2026, America/Los_Angeles. Positive restricted-selector assignment. **PROVED/EXACT restricted lemmas; COMPUTATIONAL checks passed; arbitrary-CNF transfer OPEN. Independent peer review PENDING. P versus NP OPEN.**

## Result and recovered scope

The load-bearing dependency advanced here is an implementable, sound, two-label child solver inside the shared-row/disjoint-private-block wrapper. After fixing head colors, each follower has at most five Boolean comparison coordinates, regardless of the number of head names. Its full-alphabet signature relation is bijunctive **if and only if the incident heads use at most two distinct colors**. This gives a linear-size 2-SAT terminal and a source-discoverable strong backdoor: branch on all unpinned heads and on unpinned nonheads occurring below at least three distinct head names. If their number is k, solve either polarity in O(5^k L) indexed word operations and O(L) words, including witness reconstruction. Deterministic label acquisition is charged.

The prior two-head theorem is credited, not rediscovered: LSPV-1/628, `research/agents/lspv-1/2026-11-18_LSPV1_T5_TWO_HEAD_PARITY_PINNED_2SAT628.md`, retrieved blob `7420f80a0dbb0d65e3f23bf42a7b5a78045de8ac`. It proves parity sufficiency for at most two head **names**, and pinned 2-SAT solvability in at most 25 routes. The present extension is arbitrary head names with fixed-head signature recognition and an explicit exceptional-follower parameter, integrated below with support reuse. No claim of literature-wide novelty is made for backdoors or bijunctive CSPs.

Other recovered project results used as dependency boundaries: POSITIVE_SELECTOR_HORN2's support-reuse wrapper; LOCAL4's independent-row certificate enumeration; QBOUNDARY2's failure of unconstrained binary projection; QRECOVERY1's private-head coloring/critical-deletion transfer. These do not provide an arbitrary-CNF layout compiler. Existing fixed-girth critical controls are not asymptotic time lower bounds. The current issue #3 and 628 original report were read; targeted repository searches found no matching signature-majority report. Draft-branch discovery failed argument validation, so unmerged duplicate work has NOT been ruled out.

Falsifiers fixed for this run: a majority-closed terminal with a spurious or missing original Q model; a three-distinct-head-color full-alphabet relation that is bijunctive; an incorrectly accepted wrong route; or an omitted source/replay/coverage cost in the wrapper.

## Definitions and exact terminal

Use A=0,...,E=4 and exactly A:BD, B:CE, C:AD, D:BE, E:AC. Define R(a,a)=0 and Q(h,u,v)=R(h,u) XOR R(h,v). A clause's three variable indices are distinct; colors may tie. NOT R includes ties. P uses AND and is a different relation. Exhaustive value checking gives Q=60, P=20, intersection=0 out of 125.

An input is an explicit variable table, clause list and absolute color pins. L counts variables plus occurrences, including declared isolated variables whose colors must be output. IDs are O(log L)-bit integers; no binary declaration of exponentially many output variables is hidden in L. Indexed arrays give O(L) word-space; arbitrary textual identifiers can be deterministically sorted/renumbered with polylogarithmic time/bit overhead. The source is read-only, output is write-only; all derived structures, assignments, SCC data and counters are workspace. Python timings are not word-RAM theorems.

Fix a color for every head variable. For variable v, let C_v be the set of distinct colors of heads having v as a tail. Coordinates sharing a head color are merged. For allowed color list D_v (full alphabet when free, a singleton when pinned), define

S_v = { (R(c,a))_(c in C_v) : a in D_v }.

Introduce one Boolean b_(v,c) per coordinate. Each Q(h,u,v) becomes b_(u,color(h)) XOR b_(v,color(h))=1, expressed as two 2-CNF clauses. Add an exact representation of S_v. A head that is also a tail is already pinned; its signature is a singleton. No assumption of separate head and tail roles is made.

**Lemma 1 (PROVED/EXACT).** If every S_v is closed under coordinatewise ternary majority, the fixed-head instance reduces exactly to 2-SAT in O(L) time/space and a 2-SAT model lifts to a complete original five-letter model in O(L).

Proof. A Boolean relation is bijunctive iff majority closed [1]. Its forbidden unary and binary projections yield an exact defining 2-CNF: equivalently, take all its entailed clauses of width at most two. This follows by taking any defining 2-CNF; every clause in that definition is among these entailed clauses. Each signature has at most five coordinates and at most five tuples, so testing all at most 125 ordered tuple triples and all unary/binary patterns is constant work per variable. Empty domains reject directly; nonempty zero-coordinate relations are vacuous. Solve the resulting implication graph by SCC. For each variable independently, try its at most five allowed colors and choose one with the required signature. Every original Q clause then holds; conversely every original model induces these Boolean values. Check all original clauses and pins before returning a witness. Total sizes and scans are linear. QED.

The implementation supports full domains and singleton absolute pins; the same proof allows general explicit color lists. List-domain closure/projection equivalence is tested separately, but a public list-domain solver API is not claimed implemented.

**Lemma 2 (PROVED/EXACT: exact boundary of this local compilation).** With D_v the full alphabet, S_v is bijunctive iff |C_v|<=2.

For zero, one or two coordinates every Boolean relation is majority closed: on two coordinates the majority of three tuples is one of those tuples. For three distinct colors, rotations and coordinate permutations reduce all ten color subsets to the following two representatives:

| Head colors | Complete signature set | Three tuples whose majority is absent |
|---|---|---|
| 0,1,2 | 001,010,100,101 | 001,010,100 -> 000 |
| 0,1,3 | 000,010,011,100,101 | 000,011,101 -> 001 |

Rotating the first subset gives 012,123,234,034,014; rotating the second gives 013,124,023,134,024. Thus all three-color cases fail. A relation on more distinct colors projects onto one of these failures; projections preserve majority closure, so it also fails. Repeating coordinates does not change the conclusion. QED.

This excludes an exact existential-auxiliary 2-CNF definition of that *local signature relation* too: conjunction and existential projection preserve majority. It does **not** exclude another global solver or a simplification using interactions among clauses. Failure of this compiler is not NP-hardness or a time lower bound.

Concrete pinned boundary: Q(h0,x,a),Q(h1,x,b),Q(h2,x,c), with colors h0=0,h1=1,h2=2,a=1,b=2,c=0. These force x's three comparison bits to 000. Each pair of requirements is realizable but their conjunction is not. All per-head follower graphs have one edge. The terminal reports UNKNOWN on the nonbijunctive signature; the complete backdoor solver proves UNSAT. This is a pinned boundary control, not a claim of a new smallest unpinned critical obstruction.

## Source-discovered backdoor and fully charged selector

Let H be the set of head names. Let D be the nonhead variables that occur as followers below at least three distinct head names. Let K=(H union D) minus already pinned variables and k=|K|. Both H and D are obtained by scanning source occurrences, without satisfiability advice.

**Lemma 3 (PROVED/EXACT).** Enumerating all 5^k assignments to K and running Lemma 1 on each residual decides both polarities, constructs a full SAT witness, and uses O(5^k L) word time and O(L) live words. With a threshold b, returning UNKNOWN when k>b is a sound bounded specialist on every well-formed input and complete on k<=b.

Proof. Every head has a color after a route is fixed. Every unpinned nonhead has at most two incident head names, hence at most two colors; every other variable has a singleton signature. Lemma 1 applies on every route. A successful route yields an original witness. Only exhaustion of **all** routes licenses UNSAT. A failed route alone does not. Arrays and SCC graphs are released between routes. Preprocessing, enumeration counters, repeated source scans, construction, all failed and successful SCC calls, color acquisition, original-clause checking and the full output are included. There is no free SAT/UNSAT child label. QED.

Without absolute pins and with nonempty K, simultaneous fivefold rotation permits fixing one member of K to 0, reducing routes to 5^(k-1). The current implementation deliberately enumerates all 5^k routes, so evidence includes the factor five. Absolute pins invalidate that normalization in general. Exact solution counting is not preserved by selecting one realizing color per signature; this is a witness/decision algorithm.

**Lemma 4 (PROVED restricted composition; CONDITIONAL applicability).** Assume an authenticated explicit Boolean shared-row source F(z,y)=AND_i F_i(z,y_i), disjoint private y_i, all 2^s shared rows represented, and source-faithful residuals expressible as pinned Q instances with k_i(z)<=b. Assume block-contiguous, block-qualified variable IDs so private disjointness and local access can be authenticated without storing a global N-sized dictionary. The row scan with this child solver is a uniform sound two-label algorithm. An UNSAT answer provides one verified rejecting block index per row. A SAT answer is a full original witness, obtained by replaying all successful children on one good row. This assumes a witness-preserving residual representation; no arbitrary-CNF-to-Q compiler is supplied.

For B blocks of maximum encoded size L, R rows, total source length N, the direct bound is

T = O~(N + R N + R B L 5^b + N 5^b),
S = O~(L + R + log N).

The final N5^b term covers witness replay and checking; the R-sized selector may be stored to output one bad block for every row. All child outcomes and positive children preceding a rejecting child are charged. A streaming SAT output need not coexist with all private witnesses because block-qualified output names and private disjointness allow local verification then emission; shared colors are retained. Converting to a different required output order must be charged separately.

Support reuse gives a stronger source-sensitive statement. If block i depends on r_i shared bits, enumerate each of its 2^r_i restrictions once and solve it. Whenever a restriction is UNSAT, mark all consistent global rows with block i. Enumerating these extensions over all restrictions of a given block touches each row at most once. With explicit supports and deterministic indexing,

T = O~(N + sum_i 2^r_i L_i 5^b + B R + N5^b),
S = O~(max_i L_i + R + log N).

After all blocks, all marked rows certify NO; any unmarked row has every child SAT and can be replayed to produce a full witness. No table of all child witnesses is retained. The NO output is a row-to-block index map, not an uncharged proof object: an external verifier reruns the selected complete child solves, within the same displayed asymptotic bound. Explicit SCC contradiction paths could instead be emitted with their generation, size and verification charged. This support-reuse variant is proved here as a composition, not claimed executed by the small wrapper test, which uses direct row scans. If some children exceed the threshold, they are UNKNOWN: all-row verified rejection still proves NO; a fully verified good row proves SAT; every other outcome stays UNKNOWN. A missed promise never becomes an UNSAT certificate.

Under R<=N^.195, B<=N^.65, L<=N^.35, 5^b<=N^.135, the worst-case bound is N^(1.33+o(1)) time and N^(.35+o(1)) writable bits, within square-root polylog space. Here b<=.135 log_5 N (about .05814 log_2 N). This is a recognized restricted-source result. If the only available seed costs L^(c+o(1)) time and L^(s+o(1)) space, the direct scan instead needs time exponent max(1.195,.845+.35c) and space at least max(.35,.35s) before extra compiler costs. The target requires c<=97/70 and s<=10/7. An unspecified polynomial SAT seed supplies neither those exponents nor hereditary source structure.

## Correct paths, wrong-path soundness, and polarity

| Resource grant | SAT output and validation | UNSAT output and validation | Deterministic accounting |
|---|---|---|---|
| Free true polarity label | Label already reveals decision; still construct/verify full witness | Label already reveals decision; still construct checked refutations | Answer advice is not a uniform algorithm |
| Uniform deterministic specialist | Witness or UNKNOWN; never a false witness | Checked NO or UNKNOWN; never NO on a SAT input | Charge all trials and source access, not merely successful work |
| Verifiable k-bit supplied path | Must encode or produce a consistent full witness; wrong paths reject | Must justify all universal rows and a genuinely UNSAT child per row; wrong or incomplete paths reject | Generic enumeration O(2^k(V+k)), space O(S+k+log V), given a total bounded verifier |
| Alternating/adaptive strategy | Choices may depend on preceding universal history | One selected root-to-leaf history does not cover all universal cases | Bound the complete strategy and universal exploration or retain alternation explicitly |

A supplied path is instance-specific and existentially verified, unlike conventional length-only advice. A two-way read-only certificate of k bits can have V-time/S-workspace verification, but ordinary space-bounded nondeterminism does not get reread access to forgotten guesses. Store the k bits, or account for a valid alternative. The generic enumeration bound is an upper bound, not an acquisition lower bound. Preprocessing independent of the certificate may be reused once if retained; its memory is charged. Input-dependent compact strategies must be validated on every relevant universal history; a k-bit description is not automatically a k-bit accepting transcript.

If row certificates are logically independent, one may enumerate each separately: O(sum_z 2^(k_z)(V_z+k_z)), not automatically 2^(sum_z k_z). Shared adaptive consistency constraints invalidate that factorization unless proved. Selector indices alone cost R ceil(log2 B) bits in a straightforward full-row table; a shorter source-derived selector is legal, but it does not certify the selected blocks' polarity.

For this new solver, free correct head/backdoor colors remove 5^k trial acquisition on a SAT input and leave a linear terminal plus witness output. On UNSAT, one failed head-color route proves only nonextendibility of that route; all 5^k routes remain an obligation for this particular branching proof. Other algorithms may bypass them. Free correct bad-block indices remove block discovery, but not the selected children's NO verification or the universal row coverage. No trial-count lower bound survives these observations.

A deterministic specialist sound on every input, complete on one polarity with a known time and workspace cap, yields a total decider by simulating under those caps and returning the other label on timeout/cap exhaustion. This applies to a SAT-complete or UNSAT-complete specialist alike. It does not apply outside a promise class, to an unknown clock, or to an unsound path. Proof-system-specific refutation length bounds remain restricted to their proof system.

## Simultaneous random-access exclusions: what actually transfers

Input length is encoded formula length. All resource pairs below refer to the **same execution**, with read-only input and write-only output excluded from work space, and indices/stored guesses included. Arbitrary precision/unit-cost RAMs or an extra rereadable guessed tape are not silently substituted. Standard log-word indexed implementations incur at most the charged polylog overhead when translated to the cited random-access models.

| Polarity/model | Sourced exclusion and exact scope |
|---|---|
| Deterministic SAT decision, or deterministic UNSAT decision by complementation | Buss–Williams [2], Theorem 2: SAT not in DTISP(N^1.34070,N^.5), with DTISP using c+o(1), epsilon+o(1) exponents. Thus the stricter all-CNF N^1.33+o(1), N^.5+o(1) target is excluded. At subpolynomial space use c<2cos(pi/7)=1.801937..., keeping strict slack. |
| Uniform clocked, sound, complete deterministic specialist on either polarity | Same exclusion after the capped conversion above, **only if completeness covers all formulas**. It does not contradict the promised Q/block solver. |
| Nondeterministic UNSAT / co-nondeterministic SAT | FLMV [3], Corollary 6.5: NTIME[N] is not contained in coNTISP(N^c,o(N^((1+c)/c^2-c))) for c>1. At c=1.10 the space exponent is .635537..., giving an UNSAT exclusion at time N^1.10+o(1), space N^.5+o(1) using slack and the quasilinear/logspace completeness transfer. At c=1.33 that displayed exponent is negative; this corollary supplies no square-root-space exclusion there. |
| Nondeterministic UNSAT, stronger small-space statement | Diehl–van Melkebeek–Williams [4], Theorem 2: for c^2 d<4 there exists e>0 excluding the coexistence of nondeterministic tautology algorithms of time N^c and simultaneous time N^d/space N^e. Taking c=d gives d<4^(1/3)=1.587401... for sufficiently small e. The theorem does not identify e as .5. Negation connects tautology to formula-UNSAT; transfers to CNF-UNSAT require the usual size/space-accounted encoding. |
| Nondeterministic SAT | The preceding co-nondeterministic/NO statements do not apply. Stored assignments give the usual polynomial-time NP verifier; supplied rereadable assignments admit small-workspace verification in a different certificate-access model. No N^1.33/sqrt-space nondeterministic SAT exclusion is asserted here. |
| Particular resolution, circuit, or oracle proof model | No unrestricted RAM transfer without an additional simulation/coverage theorem. |

The cited bounds do not establish P!=NP and do not automatically apply to Q critical deletions or high-girth promises. A generic NP-completeness reduction can have unacceptable fine-grained blowup or fail to preserve a promise.

## Executed evidence, costs, and limits

The exact-title imported archive was recovered from the available local evidence at `/workspace/scratch/a3c04269c151/evidence/T5_Exact_One_Experiments_2026-11-18.zip`. This run independently rechecked its SHA-256 `d811f0ea0b00fc88ebecf2349585386a2f0079508139aa638a8635e765e8a30a` and all 23 file-manifest entries (zero mismatches), and read the original structural script. It did not rerun the 2,320 paired grid, 600 exploratory appendix, full 4,096-system classification, or all 236 large-fixture deletion witnesses. The appendix's one capped UNKNOWN remains UNKNOWN. The 283/236 fixture's girth remains fixed, not increasing.

New producer `q_restricted_selector.py`, seed 202611180629, completed its main tests in about 1.90 seconds on this host (excluding JSON serialization and the separate heap-measurement pass):

- All 32 head-color subsets, including empty: exact signature lists and explicit majority obstructions for sizes >=3.
- 891 majority-closed signature/list-domain cases: exhaustive equality with unary/binary projection reconstruction.
- 256 two-variable 2-CNF clause subsets: SCC answers checked against exhaustive Boolean assignments.
- 80 new bounded pinned tests: 36 SAT, 44 UNSAT, zero discrepancies against full original Q enumeration; matching P scopes and pins counted separately.
- Eight exact controls: Q/P relation table; odd follower triangle; the five-clause UNSAT core and all five deletions (10,40,10,30,25); the pinned three-signature obstruction. Full SAT witnesses verified on original triples.
- 60 variables, 40 clauses, 20 pinned head names, zero unpinned backdoor variables: SAT, full witness verified.
- Six shared-row/block instances: one UNSAT, five SAT; 20 scan calls and 10 full-witness replay calls, including their individual route/SCC counters. Global formulas separately enumerated.
- Private-head K6: the bounded k<=7 solver reports UNKNOWN, not UNSAT. K6's graph-coloring certificate is a separate valid source-aware solver, not implemented here. No private-head large fixture is claimed covered by this parameter bound.

The five-clause core solve enumerated 625 routes, called SCC 625 times, constructed 17,250 2-CNF clauses/34,500 implication edges, traversed 69,000 directed edges across the two SCC passes, and scanned 3,125 source clauses inside terminals, in addition to its initial five-clause scan. A separate traced execution peaked at 16,288 Python-managed bytes. This is the measured solver call including preprocessing, all routes and counters; its literal input and interpreter/import state preexist tracing. It is not an OS-RSS measurement or asymptotic bit-space proof. Named counters measure specified kernels, not every machine instruction; complete asymptotic charges are in the lemmas.

An initial broader driver under whole-process tracemalloc was interrupted before producing output; it supplied no completed results. The final bounded driver and separate measured solve are the published experiment. No cutoff result was relabeled UNSAT.

`audit_q_restricted_selector.py` uses a separate explicit win matrix, imports neither the solver nor SCC, and directly checked all 88 paired instances, six wrappers and their child labels, full witnesses and signature certificates: **925,082 relation checks; PASS**. This is an independent implementation by the same author, not independent peer review. Raw SHA-256 is `f9f2848eeef629b5c104650dce4261d5af18b1907b3f6ed27deb50c17d6b8630`; the auditor records its own code hash. The producer hash is embedded in raw evidence. Full exact scopes, pins, outputs, counts and all wrapper calls are preserved.

## Ledger and next blocker

| Status | Claim |
|---|---|
| PROVED/EXACT | Fixed-head majority-closed signatures have a linear 2-SAT terminal; full-alphabet boundary is exactly two distinct incident head colors. |
| PROVED/EXACT | Source-discovered heads-plus-exceptional-followers backdoor gives O(5^k L) two-label search, with sound UNKNOWN beyond budget. |
| CONDITIONAL applicability / PROVED composition | Authenticated disjoint-private residuals satisfying the bound yield the stated row/support-reuse selector and SAT replay costs. |
| FALSIFIED | Per-head parity or merely all pairwise signature supports suffices for arbitrary Q. A failed coloring route is a global UNSAT refutation. |
| OPEN | A useful uniform source-preserving compiler from arbitrary CNFs; small backdoors on the required critical/high-girth families; independent peer audit. |

DISJ sanity: PASS for the restricted construction; no information/query lower bound is transferred. Relativization: no separation claimed and no hierarchy consequence asserted. Simultaneous DTISP: PASS for the restricted upper bound; unrestricted promotion blocked by the missing compiler and cited exclusion. Deterministic configuration counting: only an upper-bound consistency observation, never a work lower bound. Algebrization/Natural Proofs/circuit lower bounds: not used. Fivefold rotation, source encodings, equality/ties, Horn/2-SAT/XOR shortcuts and compact source-aware algorithms are permitted.

The next useful dependency is a **source-recognizable way to reduce the number of head colors or exceptional followers before branching**, preserving the full original witness and its acquisition costs. The known equality-partition/tournament characterization and parity component substitutions are possible inputs to that work; they are not free advice. This run makes no minimum-obstruction or growing-girth hardness claim.

Publication is additive under the positive-proof report area, preserving existing titles, identities, ownership and schedules. No matching root-manuscript ownership was assigned in this turn, so no peer manuscript was overwritten and manuscript reconciliation is NOT claimed. Repository preflight was not run: no local repository checkout was available. Draft-branch inspection was unsuccessful; peer review remains pending.

## Primary references

[1] Gopalan, Kolaitis, Maneva and Papadimitriou, *The Connectivity of Boolean Satisfiability: Computational and Structural Dichotomies*, ICALP 2006, Definition 1 and majority characterization: https://users.soe.ucsc.edu/~kolaitis/bio11/papers11/icalp06.pdf . Known Boolean CSP characterization; no new general 2-SAT theorem claimed.

[2] Buss and Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, conference manuscript, Theorem 2/table and DTISP definition: https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf . Consulted source version is explicitly the conference manuscript.

[3] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, September 2004 manuscript, sections 2.1 and 3, Corollary 6.5: https://lance.fortnow.com/papers/files/tst.pdf . Random-access tape/index model; input/output excluded, workspace and indices counted.

[4] Diehl, van Melkebeek and Williams, *A New Time-Space Lower Bound for Nondeterministic Algorithms Solving Tautologies*, Wisconsin TR1601, October 2007, Theorems 1–2 and section 2.1: https://research.cs.wisc.edu/techreports/2007/TR1601.pdf . Explicit warning that forgotten nondeterministic guesses are not rereadable.

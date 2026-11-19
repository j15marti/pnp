# QRECOVERY1: exact-one provenance, private-head wrappers, and ternary decoding

19 November 2026, Asia/Seoul. Role: Prior-Work Recovery. **P versus NP OPEN.** Independent mathematical peer review of this run is pending. This is an additive report; manuscript ownership, titles, schedules and enabled/paused states are unchanged.

## Outcome and scope

The exact-title archive was retrieved by library ID `libfile_00b4599c2cfc8191a859b757dad101a0`. Its SHA256 is `d811f0ea0b00fc88ebecf2349585386a2f0079508139aa638a8635e765e8a30a`. All 23 manifest entries match. The completed random grids and four-variable classification were recovered, not repeated.

The recovered projection already proves that private-head Q is graph coloring. This run makes its wrapper implications explicit: local refutation after assigning all tails is trivial, but the complete row set is exponential. It also records the exact critical-deletion transfer, independently checks the supplied witnesses, and specializes the prior binary sparse-lift decoder to ternary Q. These are upper bounds and correctness statements, not unrestricted lower bounds.

## Relation identity and prior-work ledger

Use the supplied table, with A,B,C,D,E identified with 0,1,2,3,4:

    A: B,D    B: C,E    C: A,D    D: B,E    E: A,C.

Q(x,y,z)=R(x,y) XOR R(x,z); P(x,y,z)=R(x,y) AND R(x,z). There are 60 and 20 accepted ordered triples, respectively, with empty intersection. Distinct names need not have distinct values. In particular Q(x,x,y)=R(x,y), while Q(x,y,y) is false. Negated R includes equality and cannot be replaced by reverse R without a disequality proof.

| Recovered source | Established contribution | Relation/scope firewall |
|---|---|---|
| Exact-one package: `structure/structure_notes.md` | Tournament-independent private-head disequality projection; T3/3-coloring and T5/5-coloring; one-head bipartiteness and counts | Already completed. General Q is not Boolean XOR-SAT and is not a relaxation of P. |
| Package: `redteam/redteam_notes.md`, fixture JSON | Five-clause critical core; full four-variable classification; three Mycielski lifts of C5, 236 deletion witnesses | Q clause criticality; fixed incidence girth 8; easy recognizable certificate. |
| `research/coordination/2026-11-11_AFFINE_TABLE_COMPOSITION2_HANDOFF.md`, blob `ef425dafc15fa7dc3205c1b5c4cdcd548002fbd3` | 33-variable Mycielski 3-color CNF survives 66 singleton probes; exact closure method refutes it. Connected easy bounded-treewidth family has exponential flat expansion. | Earlier compatibility counterexample, not this Q relation. Counts recovered from report, not rerun. Factored/separator methods can avoid flat expansion. |
| `research/agents/cross-track/2026-11-17_1303_T5_LOCALGLOBAL44_STATUS.md`, blob `06cddebfed95f74946eff651fb7222fcc2e99e31` | Same 47-vertex/236-edge source graph already used to separate local from global satisfiability | Earlier instances were oriented binary R; their criticality does not transfer automatically to Q. |
| `research/agents/recovery/2026-11-19_T5_DECODE1.md` | Paid modal-fiber decoder for Kun's binary twisted product, epsilon<1/25 | Recovered from local report and repository search; new Q specialization below uses arity three. |
| `research/agents/recovery/2026-11-19_LOCAL4/report.md`, blob `88695b6575e63e3af9311ba6533768279fba2dd3` | Independent row-certificate enumeration costs a sum, not a Cartesian product; known-clock specialist implies decision | Does not remove the number of universal rows. Maintains correction of erroneous nondeterministic-SAT attribution. |
| `research/agents/proof/2026-11-19_POSITIVE_SELECTOR_HORN2/report.md`, blob `0a2af364629c84b6ca0972d6dad39a964b186f25` | Support-based residual reuse plus discoverable Horn backdoors; target time on a restricted refuting-cover promise | No arbitrary-CNF compiler. Unknown terminals do not certify SAT. |
| `research/agents/redteam/2026-11-19_1312_SELECTOR_ADVERSARY2/report.md`, blob `21dbeeddcea57b6c00e45f21f6e38dde5f46ab2b` | Connected large-backdoor cores with constant refutations; full-range rapidly changing selectors computed cheaply from source | Rules out parameter-only hardness arguments, not the positive selector theorem. |

LOCAL4 also indexes LEAD-0023 (wrappers compile paid actual YES/NO computations), ORBITBATCH1 (address reuse still pays retention/output), WRAPPER_INDEX_REPLAY1 (source replay), and PATH3 (clock, certificate and cache accounting). Their full bodies were recovered in that preceding run; this run re-fetches LOCAL4 rather than claiming a new audit of every original.

The archive preserves 2,320 definitive main runs and 600 exploratory runs with one UNKNOWN: Q, n=40,m=60, seed 202611580003, 10,000-node cap. UNKNOWN remains unresolved. Random, planted, certified-critical, and deletion-witness families are distinct evidence categories; this run adds no new random or planted measurements. Existing paired P/Q scopes and seeds remain authoritative, without inferring a general hardness ordering.

## Exact private-head theorem and critical-deletion transfer

Let T be any loopless tournament of q colors and G=(V,E) a finite simple graph. Introduce a distinct private head h_e for every edge e={u,v}, and set F_G=AND_e Q(h_e,u,v). Heads never occur as tails.

**PROVED/EXACT.** For every tail assignment c:V->[q], its number of extensions is

    product_{uv in E} w(c(u),c(v)),
    w(a,b)=|{h: R(h,a) XOR R(h,b)}|.

Here w(a,a)=0 and w(a,b)>0 for a!=b: choose the head equal in value to the winning endpoint. Thus a tail assignment extends iff it is a proper q-coloring. The total Q count is the sum of those products over proper colorings. For the specified T5, w is the following matrix:

| | A | B | C | D | E |
|---|---:|---:|---:|---:|---:|
| A | 0 | 4 | 2 | 2 | 4 |
| B | 4 | 0 | 4 | 2 | 2 |
| C | 2 | 4 | 0 | 4 | 2 |
| D | 2 | 2 | 4 | 0 | 4 |
| E | 4 | 2 | 2 | 4 | 0 |

Consequently F_G is clause-minimal UNSAT iff G is edge-minimal non-q-colorable, ignoring irrelevant isolated vertices. Deleting Q_e is exactly deleting graph edge e, with h_e now unconstrained. Every coloring of G-e in this situation has c(u)=c(v); otherwise it would color G. Therefore every possible value of the omitted head fails Q_e, while the remaining heads can be constructed independently. The unused head contributes an extra factor q to deletion counts if all original variables remain declared.

Proof of criticality is the decision equivalence applied to G and every G-e. This is an exact reduction between the graph-critical and Q-critical promises, with witness extraction by restriction and lifting by the winner rule. It does not reduce arbitrary SAT to either promise or give a cheap way to find the tail coloring.

Every cycle in the incidence graph alternates original graph vertices and edge clauses; private heads are leaves. Hence incidence girth is twice graph girth, with infinity for forests. Clause-critical Q can therefore have degree-one variables. **The binary R obstruction's no-long-degree-two-thread and 2-connectivity theorems cannot be applied to the Q incidence graph.** The relations and graph models have changed.

Using standard existence of high-girth, high-chromatic graphs, take an edge-minimal non-5-colorable subgraph: removing edges cannot decrease girth; after removing isolated vertices it is connected and has minimum degree at least five. This gives existential growing-girth critical Q families via the transfer. Efficient criticalization with source-witness preservation is a separate, unproved reduction obligation.

## Wrapper/selector consequence: cheap row versus global coverage

For F_G, choose all v graph vertices as shared variables z and each head as one private block. For a fixed z, block e is refutable exactly when z(u)=z(v). The deterministic selector scans for the first monochromatic edge, or returns NONE if the tail coloring is proper. It is universally sound and costs at most m equality tests per row. No polarity advice or local UNSAT solver is needed.

There are 5^v complete rows. One global rotation can normalize one vertex to A, leaving 5^(v-1) rows; this is a valid enumerator, not a lower bound. Tail color permutations also permit graph-coloring symmetry reductions, up to the constant factor 5!, with heads reconstructed afterward. Those permutations need not preserve the original Q extension counts.

For the supplied fixture, v=47 and m=236, even rotation normalization leaves

    5^46 = 142108547152020037174224853515625 rows.

This numerical comparison is descriptive; asymptotically the natural decomposition has exponentially many rows in v, not the promised R<=N^.195. Each block depends on only two shared colors, so it has at most 25 local support assignments. Tabulating its behavior in constant work does not decide whether the union of its bad-row sets covers the full space. That coverage problem is exactly graph non-5-colorability.

A source-aware scanning implementation with indexed edge input uses Otilde(N+5^v(v+m)) time and O(v+log N) writable bits, with colors stored in constant bits each. Input authentication/reformatting costs must be added for other encodings. Streaming a full row-indexed refutation table costs at least its actual output length. A short program "return the first monochromatic edge" is not itself a verified UNSAT certificate: proving that it never returns NONE is the original global problem.

This **falsifies the inference** "constant local residual language plus easy row selection gives a polynomial global specialist." It does not falsify a particular fully costed algorithm or prove that every algorithm enumerates all rows. Mycielski recognition, graph-coloring algorithms, elimination orderings, small-treewidth dynamic programming and other source-aware methods may avoid this enumeration. A supplied width-w decomposition gives the usual finite-domain bag-table approach; decomposition acquisition, 5^(w+1) tables, joins, witness traceback and peak retained tables must still be paid.

For the user's authenticated Boolean layout, LOCAL4 remains applicable:

    T <= P + sum_z 2^{k_z}(V_z+k_z+1) + output,
    S <= W_layout + O(max_z(S_z+k_z)+log N+log T).

Each local verifier must be sound, complete for the required row predicate, independent of choices at other rows, and clocked. For polynomially many rows this can be far cheaper than enumerating whole selector tables. It does not change 5^v into a polynomial row count in the Q decomposition.

With a local exact seed of time ell^c and space ell^s, full-support scanning in the supplied N^.195/N^.65/N^.35 layout has exponents max(1.195,.845+.35c) and max(.35,.35s), before any omitted costs. Target 1.33 and .5 require c<=97/70 and s<=10/7. An unspecified polynomial seed provides neither inequality. Iterating the formal exponent map requires a uniform hereditary compiler applicable to every child; a fixed point is not an impossibility proof.

## Recovered high-girth decoder, now for ternary Q

**PROVED, source specialization of Kun Lemma 13 [K].** Let A have a nonempty ternary epsilon-expander relation, let C be its twisted product with a Q source B, and retain the projection and tuple bijections. If epsilon<1/125, every Q-coloring of C decodes by choosing any most frequent color in each source fiber.

Indeed each chosen class has at least |A|/5 points. Pull the three classes back through the tuple bijections. Expansion gives at least |R(A)|(1/125-epsilon)>0 lifted tuples with those three colors, forcing their Q relation. This holds for every source clause and all modal ties.

Given indexed fibers, decoding plus source verification costs O(M+v+m) word operations and O(v log M) counter bits; lifted-witness storage/access, verification of all lifted clauses, construction, and acquisition are additional paid work. The old binary 1/25 argument must use arity three here. This sufficient threshold is not claimed necessary. Kun fixes the girth parameter; this theorem alone gives neither a growing-parameter complexity bound nor criticality.

## Correct paths, advice and the two polarities

All costs below include original-source reads, preprocessing, failed routes, materialized residuals, every child of either polarity, final verification, output and replay. Peak space counts simultaneously live work; depth-first children can reuse buffers, while retained parent state still counts.

| Interface | SAT successful output | UNSAT successful output | Wrong-path requirement |
|---|---|---|---|
| Uniform deterministic specialist | Full satisfying assignment, otherwise UNKNOWN | Sound refutation/validated full refuting cover, otherwise UNKNOWN | No false claimed label on any input; timeout is not a refutation unless the completeness/clock theorem justifies a total decision conversion |
| Free correct polarity | Correct branch is supplied, but witness acquisition remains | Correct branch is supplied, but evidence acquisition remains | The label is answer advice for decision and is not a uniform algorithm |
| Supplied k-bit existential path | Verifier checks all original constraints | Verifier checks all refutation obligations | Every accepting path must be sound; failure rejects that path only |
| Alternating/adaptive strategy | Choices may depend on preceding universal history | Same | One root-to-leaf trace cannot replace a winning strategy; bound its full description or charge all universal histories |

For the private-head family, a proper tail coloring supplies a successful SAT path of at most 3v bits in a simple encoding. Verify every edge, then choose and emit every head. Retaining the tail uses O(v) bits. With a separately supplied indexed read-only tail certificate, the verifier can instead use logarithmic writable workspace and repeated paid accesses; this stronger certificate interface does not make old nondeterministic guesses freely rereadable. To avoid emitting an invalid deterministic witness before final verification, verify first and replay for output. Nonaccepting nondeterministic outputs do not count as witnesses.

For UNSAT, a guessed monochromatic edge checks one specified row only. Even k=ceil(log_2 m) correct bits per row do not certify all rows. For critical-deletion SAT inputs, the endpoint equality theorem verifies the missing constraint's failure, but acquiring the tail coloring remains essential. The imported Mycielski recursive constructor is an easy special source, not an arbitrary critical-instance solver.

A sound complete k-bit clocked verifier of one polarity can be deterministically enumerated in O(2^k(V+k+1)) time and O(S+k+log V) workspace. Completeness on **all inputs of that polarity** makes failed enumeration decide the opposite polarity. A uniform deterministic one-sided specialist with a known completeness clock similarly yields total decision by timeout. Neither conversion applies unchanged to a promise-only specialist. Independent row witnesses permit the additive LOCAL4 bound; shared-certificate constraints do not. Read-only certificate production and length are separate charges, not silently absorbed into writable S.

## Sourced simultaneous time-space exclusions

Model: uniform indexed/random-access machines with read-only input, write-only output, and charged work and address storage. Bounded-word RAMs are covered through the appropriate polylog-overhead simulation; unbounded unit-cost integers and free rereadable guessed tapes are not. N is actual encoded source length. These are simultaneous resource restrictions, not unrestricted time lower bounds.

| Polarity/model | Exact sourced scope | Consequence |
|---|---|---|
| Deterministic SAT or UNSAT | Buss--Williams [BW], Theorem 2/table, gives the published point (c,epsilon)=(1.34070,.5); DTISP uses +o(1) exponents. Subpolynomial-space benchmark c<2cos(pi/7). | All-CNF deterministic (1.33,.5) is excluded. Complementation preserves deterministic resources. |
| Nondeterministic UNSAT / conondeterministic SAT | FLMV [F], Corollary 6.5: NTIME[n] is not contained in coNTISP[n^c,o(n^d)], d=(1+c)/c^2-c. At c=1.10, d=.635537...; near-linear SAT reductions allow slack for the (.1 above linear,.5 space) calibration. | This yields a NO-side (1.10,.5) exclusion, not (1.33,.5); at 1.33 this displayed d is negative. |
| Nondeterministic tautology/UNSAT | Diehl--van Melkebeek--Williams [D], Theorem 2: c^2 d<4 implies some e>0 forbids both NTIME(N^c) and NTISP(N^d,N^e) tautology algorithms. With c=d, d<cuberoot(4)=1.587401... . | e is not identified with .5. Negation transports tautology to UNSAT with the encoding/reduction overhead paid. |
| Nondeterministic SAT | No matching (1.33,.5) exclusion established from the reviewed sources | Retaining a guessed assignment and checking it is not the same machine as using a free indexed certificate. Do not invert the NO-side theorem. |
| Specified proof system | Lower bounds restrict its allowed certificates | Resolution, monotone-circuit, local-summary or oracle-query bounds do not transfer to unrestricted algorithms without proof. |

The previous erroneous attribution of Fortnow's nondeterministic NO-side result to SAT remains withdrawn, as LOCAL4 records. These statements do not forbid the easy Q controls or the supplied-layout promise. A quantitative reduction is required before transferring an all-CNF exclusion. For an all-CNF one-polarity sound/complete verifier with V=N^(1.33+o(1)), S=N^(.5+o(1)) and k<=alpha log_2 N, enumeration would conflict with [BW] for alpha<.01070. This is a conditional consequence, not an exclusion of arbitrarily long free correct choices.

## High-girth literature reconciliation

[E] is stronger than a fixed-girth statement: its publisher abstract reports that, unless NP=RP, polynomial-time k-colorability is impossible on graphs with girth at least log|G|/(13 log k) and maximum degree at most 6k^13. This run retrieved the primary abstract, not its full proof. By the explicit private-head reduction, its decision consequence transfers to the corresponding Q images, whose incidence girth doubles. This is an inference from [E] and the proved transfer. It still gives no critical-deletion witness reduction. Existence of a minimal noncolorable subgraph neither computes it cheaply nor preserves a source witness decoder.

Thus the ledger must distinguish fixed-girth deterministic CSP reductions [K], the reported growing-girth conditional graph decision result [E], and the still-open intrinsic-critical search transfer. No numerical RAM exponent is transported through unspecified reduction blowup.

## Executed targeted audit

`q_recovery_audit.py` uses only the standard library and deterministic exhaustive scopes, with no random seed. It checks the archive hashes before reading evidence; it does not overwrite imported files.

| Check | Raw outcome |
|---|---|
| Manifest integrity | 23/23 hashes match |
| Q/P counts and disjointness | 60/20, no overlap |
| Five-clause core and deletions | 0; then 10,40,10,30,25 |
| All 64 simple graphs on four vertices, T3 private heads | 331,776 explicit assignment attempts, 570,915 Q evaluations; weighted counts and decision projection agree |
| All eight simple graphs on three vertices, T5 private heads | 27,000 assignment attempts, 42,475 Q evaluations; counts/projection agree |
| Rebuilt Mycielski source and imported deletion witnesses | Exact source match; 236 omitted-edge endpoint equalities; 278,480 rotated clause checks; 55,696 fresh lifted clause checks |
| K6 row selector | All 3,125 rotation-normalized rows covered; 14,157 edge comparisons; all 15 deletion witnesses valid |
| Ternary complete two-point fibers | 15,625 assignments, 780 valid lifts, 2,620 successful modal checks |

Projection without expansion is insufficient: two diagonal lifted triples with fiber values head=(0,0), left=(0,1), right=(1,0) both satisfy Q, but the allowed modal choice (0,0,0) fails. The complete-fiber test is a decoder control, not a high-girth construction.

Raw JSON preserves the graph-mask scopes, edge ordering, per-graph counts, K6 selector histogram, imported archive hash, counters and counterexample. The audit's Python allocations are not measured RAM complexity: the imported JSON is resident. Algorithmic peak-space formulas above are analytical bounds with explicit input/certificate conventions. The experiment counters are logical predicate evaluations, not full instruction counts or timings. No rerun of the 2,920 random runs or 4,096-system classification was performed.

Reproduce after extracting the supplied archive:

    python q_recovery_audit.py PATH/TO/t5_exact_one > q_recovery_results.json

The archive must be in the parent directory of the extraction directory, matching the delivered `q_evidence/unpacked/t5_exact_one` layout, for the archive checksum field.

## Status, gates and next blocker

**PROVED/EXACT:** private-head fiber formula and critical/deletion/girth transfer; row-selector semantics and complete-row cost; ternary modal decoder under its expansion hypothesis; conditional clock/certificate conversions.

**COMPUTATIONAL:** targeted checks above. Imported grids remain imported evidence; their included independent review is not a new peer review of this report.

**FALSIFIED INFERENCE:** local-support tables or free correct per-row choices alone establish polynomial global coverage; a projection alone guarantees modal decoding; binary critical-incidence structure transfers unchanged to Q.

**CONDITIONAL:** arbitrary-source preprocessing bounds, RAM simulations/reduction slack, source-to-promise transfers, and the growing-girth decision exclusion under NP!=RP.

**OPEN:** a uniformly discoverable global five-letter compatibility controller after parity/small-core handling; a paid arbitrary-CNF hereditary compiler meeting (1.33,.5); intrinsic-critical growing-girth witness hardness; independent mathematical audit; P versus NP.

DISJ gate: PASS, no information/rank-to-execution inference. Relativization: no separation asserted. Simultaneous DTISP: explicit same-execution accounting, arbitrary-CNF bridge OPEN. Configuration counting: used for no lower bound. Natural Proofs/algebrization: no unrestricted circuit separation claimed.

Next blocker: characterize a global compatibility class whose row coverage can be checked without enumerating all tail colorings, with a source-recognizable condition and complete SAT lifting/UNSAT verification. Test against the recovered singleton-resistant Mycielski selector and Q critical deletions. A local-message fixed point or a cheap per-row rule alone is insufficient.

No local repository checkout exists; project preflight and manuscript compilation were not run. Repository review is targeted. Publication belongs under the recovery role, with a separate additive handoff; no root manuscript reconciliation is attempted.

## Primary literature

[K] G. Kun, *Constraints, MMSNP and expander relational structures*, arXiv:0706.1701v2, Theorem 1 and Lemma 13. https://arxiv.org/pdf/0706.1701

[E] T. Emden-Weinert, S. Hougardy, B. Kreuter, *Uniquely Colourable Graphs and the Hardness of Colouring Graphs of Large Girth*, CPC 7 (1998), 375–386. Primary publisher abstract: https://doi.org/10.1017/S0963548398003678

[BW] S. Buss, R. Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, CCC 2012, definition and Theorem 2/table. https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf

[F] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), machine model and Corollary 6.5. https://lance.fortnow.com/papers/files/tst.pdf

[D] S. Diehl, D. van Melkebeek, R. Williams, *A New Time-Space Lower Bound for Nondeterministic Algorithms Solving Tautologies*, TR1601 (2007), Theorems 1–2 and Section 2.1. https://research.cs.wisc.edu/techreports/2007/TR1601.pdf

[GJS] M. Garey, D. Johnson, L. Stockmeyer, *Some simplified NP-complete graph problems*, TCS 1 (1976), graph 3-colorability background. Five-colorability follows by adjoining two adjacent universal vertices; this elementary step does not preserve high girth. https://www.acs.uwinnipeg.ca/ychen2/journalpapers/Garey-Johnson-2maxsat.pdf

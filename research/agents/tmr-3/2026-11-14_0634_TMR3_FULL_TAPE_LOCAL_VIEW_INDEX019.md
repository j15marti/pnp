# TMR-3/019: full-tape local-view INDEX lower bound without any retained-space restriction

**Date:** 2026-11-14 06:34 PST (America/Los_Angeles). **Role:** TMR-3 Time-Space Tradeoffs, j15marti/pnp main.
**Claim:** TMR3-FLV19, **CANDIDATE/RESTRICTED** pending independent TMR-1/TMR-5 review. **Finite execution:** COMPUTATIONAL. **Unrestricted 3-SAT lower bound:** OPEN.

## 1. Exact scope and substantive improvement

The preceding TMR-3/018, TMR-5/017, and TMR-1/020 delayed-INDEX arguments used a post-preprocessing writable-space cap s=o(L). Their natural full-input-cache hostile control defeated that premise. This run removes the writable-space cap completely by accounting for **which previously written tape cells can be physically reached during a short query**. Even when the preprocessor writes all L input bits, or an exponentially long string, its fixed number of ordinary local work heads cannot read more than O(t) nearby cells in t transitions.

Fix one finite deterministic **total, uniform** machine A, unchanged across all input lengths. It has q finite states, r>=1 independently moving nonsensing read-only source heads on identical immutable L-bit binary source tapes, and w>=0 independently moving standard writable work-tape heads. Each head moves at most one physical cell per transition. Each writable tape uses a fixed finite alphabet Gamma, |Gamma|<=g, including blank. The source alphabet has at most a=5 symbols (0,1,left marker,right marker,outside blank). Work tapes may be two-way infinite or have a fixed distinguished boundary, with any out-of-range position represented below by an extra sentinel. There are no numerical head-coordinate sensors, free cross-head collision tests, external clocks, shared uncharged output stores, unbounded-word operations, or random access.

A preprocesses the source x in a first phase without seeing the later query index. Preprocessing may be arbitrarily long and may visit **any finite number** of writable cells. Its results include all writable tape contents, head positions and finite control. Then the external interface delivers p in {1,...,L} on a paid, read-only query tape whose initial physical configuration is determined only by p (not by x); phase 2 must halt within t=t_A(L) transitions for **every** pair (x,p) and return the exact bit x_p. Query phase may reread source, rewrite any amount of work, share, cache, and recompute. The output is an ordinary finite decision symbol. No query is sent during preprocessing. All phase-1 operations would also count in a full cost ledger.

The new result addresses this INDEX service, not the 3-SAT decision interface.

## 2. New unconditional-in-that-restricted-model local-view lemma

For the machine just specified, for every L>=1 and any uniform all-(x,p) query-time bound t,

$$
\boxed{2^L \le q\,a^{r(2t+1)}(g+1)^{w(2t+1)}.}
\tag{FLV19-a}
$$

A sharpened bound, retaining the binary information density of the immutable input and allowing source heads parked arbitrarily far beyond the endmarkers, is

$$
\boxed{2^L \le q\,(L+2t+4)^r
       2^{r(2t+1)}(g+1)^{w(2t+1)}.}
\tag{FLV19-b}
$$

Put D=r+w log_2(g+1). For fixed A, if t<L then FLV19-b yields the explicit bound

$$
t \ge \frac{L-\log_2q-r\log_2(3L+4)-D}{2D}.
$$

If t>=L, the resulting asymptotic statement is immediate. Thus for **arbitrarily large** retained writable space, including s(L)>=L or larger,

$$
\boxed{t_A(L)\ge \bigl(1/(2D)-o_A(1)\bigr)L.}
\tag{FLV19-c}
$$

This excludes all same-machine pairs (arbitrary preprocessing time, arbitrary retained S, sublinear post-query t) in this locally moving, fixed-number-of-heads INDEX model. It is stronger in workspace scope than IC18/UW17/UM20, though UM20 may provide a larger leading constant when s=o(L). It is not a lower bound against all uniform polynomial-time 3-SAT deciders.

## 3. Full proof, including all transitions of the query

At the query boundary, construct the **t-local fingerprint** of x's actual retained configuration: (i) the q-valued finite control; (ii) for each of the r source heads, the exact string of 2t+1 source symbols at relative offsets -t,...,+t around its parked physical position; and (iii) for each of the w work heads, the exact 2t+1 work symbols at relative offsets -t,...,+t, with a distinguished sentinel for coordinates outside a one-sided tape. All tape writes performed in preprocessing are already reflected in these actual local strings. Head coordinates themselves are **not** included because standard fixed-transition local heads have no direct absolute-coordinate sensor. The source heads can be parked at arbitrarily large positive or negative integer positions. Repeated source windows, shared writable cells, arbitrary encodings and completely different preprocessing traces are allowed.

There are at most q*a^[r(2t+1)]*(g+1)^[w(2t+1)] such fingerprints. Suppose x != y shared a fingerprint. Supply the SAME later index p to the two executions. At query step zero their scanned source and writable symbols, control and query tape are identical. By induction, after j<=t transitions, each head has the same displacement relative to its own initial parked position in both runs, the same control, the same writes to corresponding relative writable offsets, and the same scanned symbols: every position reached is within the original radius-t local window, whose initial symbols match, and all intervening writes have matched. Fixed tape boundaries and markers are explicitly in the local windows; a boundary reaction therefore matches. Every individual real query transition, including rereads, writes, recomputation, and halt/output, is coupled. Both executions necessarily give the same answer to **every** p. Choose p where x_p != y_p. Both-label correctness is contradicted. Thus the fingerprint map x -> fingerprint(x) is injective on all 2^L strings, giving FLV19-a.

For FLV19-b, refine the source fingerprint. Each parked source-head coordinate has one of at most L+2t+4 physically observable positional types: exact positions -t,...,L+1+t or FAR-LEFT/FAR-RIGHT. Within each type at most 2t+1 true source bits may vary; markers and blanks are determined by its type. With r independently moving nonsensing source heads, the number of source parts is at most (L+2t+4)^r 2^[r(2t+1)]. Retain the exact arbitrary work-tape local neighborhoods. The identical all-step coupling still holds, establishing FLV19-b. This positional typing is independently consistent with TMR-1/020's far-head reasoning but is combined here with local views of **every writable tape** instead of bounding total stored configurations by g^s.

Take logarithms of FLV19-b. With D=r+w log_2(g+1)>0 and t<L, log_2(L+2t+4)<=log_2(3L+4), giving the displayed explicit bound. For fixed finite q,r,w,g, the logarithmic correction is o(L). If t>=L the same asymptotic inequality is trivial. No time is borrowed from a different program or a different source; t is the worst-case phase-2 budget of this ONE A. The injection lower bound produces some same-machine x,p realizing the required cost. Its actual full cost also includes whatever preprocessing A performed on that x.

**Critical assumption:** Query arrival and its initial tape configuration carry no source-dependent information beyond the post-preprocessing physical tape state. An external advice store, unit-cost random-access table, numeric head-coordinate oracle, arbitrary number of heads, or output encoded as a free absolute tape coordinate changes the theorem. There is no assumption that a SAT decider participates in this interface.

## 4. Controls, counterexamples and exact unrestricted gap

**Full-source cache:** A legitimate preprocessor can copy all L source bits into L visited writable cells. This defeats the prior s=o(L) premise but does **not** defeat FLV19: after query p arrives, a locally moving work head still needs physical movement to inspect a far-away copied bit. A fixed finite-head implementation can retrieve a bit in O(L polylog(L+2)) physically charged query time using binary address counters and a source/work scan. Thus FLV19's order-of-growth linear lower bound is consistent with a polynomial upper bound. A complete cache is not freely random-access memory.

**Far-distance encoding:** A preprocessor may park a head at an x-dependent coordinate whose numerical value encodes arbitrarily many input bits. Without a coordinate sensor, two such positions with identical t-neighborhoods yield identical t-step observations. The local fingerprint intentionally quotients these positions. It does not claim that their global configurations are literally equal.

**Compact representations:** Horn, 2-SAT, Gaussian-elimination XOR/Tseitin, bounded-treewidth DP, disjoint products, common-subexpression sharing, reordering, padding, auxiliary variables, renaming, and cache/recompute all remain legal in the preprocessor. They cannot make physical short-query locality disappear on the INDEX service; but an ordinary SAT decider need not answer an externally delayed arbitrary source-bit index. These are symbolic algorithm-compatibility checks, not executed SAT benchmarks.

**Actual 3-SAT target:** The separation contract is for every fixed correct A and every k,C,L0, some valid F with |F|>=L0 must have T_A(F)>C(|F|+1)^k. FLV19 only shows T_query=Omega(L) for a DIFFERENT two-phase all-indices function, even with unlimited S. An all-input polynomial-time SAT solver, if one exists, could simply decide the one-bit label without servicing later INDEX requests. No reduction from SAT semantic processing to this service has been proved. The all-exponent unrestricted arrow remains OPEN. Do not infer P != NP or a superlinear processing cost.

## 5. Exact executed finite checks

The separately published standalone Node/CommonJS source was **actually executed under native Node.js v22.16.0** (not a hosted wrapper) in one short run, with exact raw JSON saved. The script constructs synthetic post-preprocessing states, including a full L-cell work-tape copy, reversed copies, cumulative XOR encodings, x-dependent far-off parked heads, source-head midpoint/edge placement, and a parity finite-control bit. It builds radius-t physical current-cell fingerprints and searches actual collisions. For each collision it chooses a source bit where the pair differs and runs an independently programmed, adaptive local-head probe on BOTH physical tape states. Source/work symbols are read at the current tracked head cell, tape writes and relative moves are simulated, and all scanned-symbol/action transcripts agree through t steps. This tests the query-coupling lemma's mechanism rather than claiming a generic TM compiler or charging host-JavaScript preprocessing.

**Measured results:** L=6..13, r=1,2, w=1,2, t=0..3; 512 parameter cases, 451 fingerprint-collision witnesses, 451 identical paired adaptive physical-current-cell traces, 128 far-position collision cases, 8,190 exhaustive full-copy exactness checks; zero failed assertions. Some finite parameter cases have no collision, as allowed. Every work-tape storage fixture uses Theta(L) copied symbols, so these are explicit hostile cases to the old sublinear-retained-storage assumption. The finite results are **COMPUTATIONAL**; the all-length conclusion rests on the symbolic proof above.

Source path: experiments/tmr/tmr3_local_fingerprint019.cjs (executed Git blob c8eea121a8979ae6aaf08a876f5a5bba61191460).
Raw path: results/raw/tmr/2026-11-14_0634_TMR3_LOCAL_FINGERPRINT019_RAW.json (Git blob c64b750db441ff0c48fd466c94179fbcac5d5934).
Reproduction: node experiments/tmr/tmr3_local_fingerprint019.cjs.

## 6. Primary sources and recovered project context

1. Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, Journal of the ACM 52(6), 835-865 (2005), https://doi.org/10.1145/1101821.1101822 . Its deterministic random-access SAT result excludes simultaneous time n^c and sufficiently small space n^d for c<the golden ratio, not all polynomial workspaces. FLV19 is a separate restricted INDEX fact, not an invocation of that SAT bound.
2. Miltersen, Nisan, Safra and Wigderson, *On Data Structures and Asymmetric Communication Complexity*, JCSS 57(1), 37-49 (1998), https://doi.org/10.1006/jcss.1998.1577 . The primary models are asymmetric communication and cell-probe data structures. Their results do not automatically imply local physical-tape INDEX bounds, and certainly not unrestricted SAT.
3. Borodin and Cook, *A Time-Space Tradeoff for Sorting on a General Sequential Model of Computation*, SIAM J. Comput. 11(2), 287-297 (1982), https://doi.org/10.1137/0211022 . Sorting model and scope, not SAT.

Authoritative 2026-11-13 12:49 PST replacement directive first read and rechecked unchanged blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Complete proof1.txt read (28,714 chars, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343); complete proof2.txt recovered via authentic Git blob (1,051,196 chars, blob 930c5eeddafce656717f28055a7a9a755f44737c), notwithstanding blank file-content endpoint. Complete canonical main.tex recovered via Git blob (2,536,131 chars, blob f0054c990e11602b4b60ead3bccffa73f11d0d7b); canonical file endpoint's empty content was not treated as an empty manuscript. AGENTS.md, CODEX.md, the project pnp-research skill, current issue #3 and latest five TMR handoffs were read; original TMR-1/020 and TMR-5/017 proofs/source/raw, TMR-3/018 and TMR-3/017, and historical TMR-3/002 were inspected. Historical FLMV and prescribed-DAG/ARC findings retain their restricted status. No accepted historical counterexample was suppressed. Full local checkout/preflight script and LaTeX build were **not executed** because source checkout via network was unavailable; this does not alter the independent proof's stated scope.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof trackers left intact. Root main.tex not modified, reserved for TMR-5 synthesis. No tasks or schedules modified.

**Next single target:** TMR-5 independently prove or falsify all-tape local fingerprint injectivity, especially mutable work-tape replay and far-head physical equivalence; TMR-2 must find a genuine semantic SAT bridge that does not impose delayed arbitrary queries. A linear delayed-INDEX lower bound, however workspace-independent, excludes no polynomial-time general 3-SAT solver.

END_OF_REPORT::TMR-3::019::2026-11-14_0634_PST

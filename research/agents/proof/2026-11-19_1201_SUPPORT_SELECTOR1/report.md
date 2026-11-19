# SUPPORT-SELECTOR1: streamed coverage by local restrictions

19 November 2026, Asia/Seoul. Assignment: positive restricted selector lemmas. P versus NP OPEN. External independent mathematical review pending.

## Result and claim card

PROVED/EXACT: a block-major algorithm constructs one genuinely UNSAT block index per shared assignment without answer advice, provided each block's residuals can be decided exactly. Its child-call count is sum_i 2^r_i, where r_i counts shared variables occurring in block i, instead of the general RB bound. It stores only the selector for R rows and one active block, not the entire collection of local truth tables.

UNCONDITIONAL RESTRICTED COROLLARY: if every clause has at most two private literals, fixing the shared variables leaves 2-CNF. Implication-graph SCC algorithms give both local decisions and witnesses. The complete construction meets the requested time/space targets on the supplied layout, with a stronger bound stated below. This closes a restricted selector dependency; no arbitrary-CNF decomposition is obtained.

Pipeline: explicit authenticated layout -> discover each block's shared support -> enumerate its local restrictions -> solve/check each residual -> mark covered rows -> output UNSAT selector or construct and verify SAT witness. Falsifiers: omitted shared dependency; overlapping private variables; unsound NO marking; accidental retention of all block tables or full output; wrong-path advice replacing verified residual computation.

## Model and structural assumptions

Let F=AND_{i=1}^B F_i(z,y_i). All private variable sets y_i are pairwise disjoint. Every shared assignment is included: R=2^h for h shared bits. Each block has encoded length <=ell, and S_i is its syntactic shared support, r_i=|S_i|. The input has n bits, including layout metadata and all literals. Use O(log n)-bit word operations with polylogarithmic bit-model overhead, read-only indexed input and write-only output. No unbounded integer operation is unit cost.

Authentication costs P(n) time and W(n) writable space are explicit. A sufficient encoding is canonical block-delimited records with private IDs carrying their unique owner block and local index, shared IDs in a separate namespace, and bounded/count-checked records. That format can be checked in streaming near-linear time with one block in memory. Arbitrary renaming, conversion, sorting or layout discovery must be added to P,W; no claimed exponent survives an unaudited conversion automatically. Isolated variables can be emitted as zero.

Assume a uniform total exact residual decider has time t(ell) and space s(ell), on both SAT and UNSAT residuals. Any proof output and its verification belong in these costs if certificates rather than semantic decisions are required. Residual construction, empty clauses and all failed SAT probes are charged. Let D=sum_i 2^r_i.

## Streamed-support selector theorem

Initialize an R-entry array A to 'uncovered'. For each block i, discover S_i while reading the block. For every assignment a to S_i, construct F_i[a] and solve it. If it is UNSAT, enumerate all full shared assignments extending a; for every still-uncovered row z, set A[z]=i. Discard the residual and continue. Different a for one block have disjoint extension sets, so at most R row visits occur per block. There is no stored table of all D answers.

After all blocks, if every row is covered, output A. Otherwise choose an uncovered row z*.

Proof: a row is marked only when a block with the same relevant shared bits has been proved UNSAT. Thus a fully covered array certifies forall z exists i: F_i[z] is UNSAT. Conversely, an uncovered row has no UNSAT block, since its unique restriction for each block was tested. Every F_i[z*] is SAT. Private disjointness allows their witnesses to be combined. Hence the algorithm never produces a false UNSAT selector and is complete on UNSAT layouts. It also correctly identifies a SAT row. The selector need not use one globally fixed block.

With polylogarithmic address/enumeration factors suppressed, the simultaneous bounds are

    T = Otilde(P + D*(ell+t(ell)) + BR + R),
    S = Otilde(W + R + ell + s(ell)).

The selector entries require O(R log(B+1)) bits, included in Otilde(R). A source block and a residual coexist, still O(ell). Parent indices, local support, extension counters and addresses are included. All child invocations are sequential. A version that stores every local answer would consume D bits and does not establish this space bound.

For h<=.195 log2 n, B<=n^.65, ell<=n^.35, max r_i<=rho log2 n, with t(ell)=ell^(t+o(1)), s(ell)=ell^(s+o(1)), P=n^(1+o(1)) and W<=n^(.35+o(1)), this becomes

    time exponent <= max(1, .65+rho+.35*max(1,t), .845),
    space exponent <= max(.195,.35,.35*s).

At rho=.05, t=1.8 and s<=10/7, the decision/UNSAT-selector upper bound is (1.33,.5), up to subpolynomial factors. At rho=.195 it recovers the older .845+.35t call term. An arbitrary polynomial seed n^K is not enough to meet this numerical bound. Small support is an additional promise, not a consequence of private disjointness.

## Positive complete specialist and matched SAT witness

Suppose every source clause contains at most two private literals. After any shared restriction, each surviving clause has length at most two. SCC detection decides such a residual and extracts a satisfying assignment in Otilde(ell) time/space. On UNSAT it can produce a contradiction certificate consisting of implication paths x -> not x and not x -> x (or an empty clause). These paths can be constructed and verified in Otilde(ell) per residual, with original-clause references.

Therefore the theorem is unconditional on this syntactically recognized class, with

    T = Otilde(n + D*ell + BR), S = Otilde(R+ell).

Even rho=.195 gives time n^(1.195+o(1)) and space n^(.35+o(1)). A sound one-sided UNSAT specialist runs this construction and emits A only on complete coverage; outside the recognized class it abstains. It never silently invokes SCC on a wider clause.

On SAT, replay the source block by block at z*, run the SCC witness extractor, verify that block against z* and its private witness, emit the private assignment, and discard it. This adds Otilde(n) time and Otilde(ell) workspace. No full n-bit witness must be retained, because the authenticated layout guarantees no private cross-block occurrence. Emit shared values once. Every source clause is verified before its block witness is discarded. This removes the earlier n^1.35 repeated-pinning overhead for this restricted terminal class.

If the backend is merely a decision seed, this witness extraction does not follow at the same cost: ordinary bit-pinning may add B*ell seed calls. The unconditional corollary uses the actual witness-producing SCC algorithm. The finite implementation keeps the encoded input as a host object; its measured Python allocation is not claimed to be the formal read-only-input RAM bound.

An emitted A alone is not an independently trusted refutation. A verifier recomputes its selected residual checks, paying up to R*(ell+t(ell)) plus source-access costs, or receives source-referenced SCC paths. If all paths are requested, output length and replay are charged; processing them one at a time avoids retaining their sum. Canonical block lookup without a stored index can use a full source scan per row, adding Otilde(R*n), still n^1.195 in the unconditional corollary.

## Correct paths, advice and alternation

Free polarity routing supplies the decision answer; the remaining tasks are witness/selector construction and verification. Free choice of an UNSAT block does not establish its UNSAT status. For SAT, one supplied z and a satisfying private assignment for every block can be checked. For UNSAT, coverage of every z is necessary. One chosen root-to-leaf path cannot substitute for a whole strategy.

For either polarity p, let a deterministic verifier V_p(F,w) be sound for every w and complete on polarity p for some |w|<=k. If one replay including all children costs v time and s workspace, enumerating all padded certificates gives deterministic decision in O(2^k(v+k+1)) time and O(s+k+log(n+v+k)) space. Thus k=alpha log2 n adds alpha to the time exponent; log-squared k gives a quasipolynomial generic enumeration bound, and k=n^a gives an exponential-in-n^a upper bound. These are simulations, not enumeration lower bounds.

Wrong paths must reject/abstain, never falsely certify the other polarity. Adaptive binary choices are covered only when their whole transcript fits k and all semantic claims are verified. If existential choices depend on universal history, bound a whole strategy or charge all universal branches during verification. A selector table has R ceil(log2 B) bits before local proof data; a smaller program for it still needs evaluation and global coverage verification.

A supplied random-access read-only certificate is not writable memory, but every access is timed. Ordinary nondeterministic machines do not get free two-way access to earlier guesses; store k bits or provide a paid consistent replay method. Re-guessing independent bits on each read is unsound. A uniformly sound deterministic one-sided specialist with known time/space caps and success on every intended input can be clocked into a total decider, as proved in PATH3. A restricted-class specialist does not have that all-CNF completeness premise.

## Applicable simultaneous lower bounds

The following use original encoded formula length and uniform random-access machines, read-only input, charged indices/bit operations, and writable work space. Transfers to word RAM require compatible bounded-word simulation and exponent slack. They do not cover free per-input answer advice or automatically apply to the restricted layouts above.

| Task/model | Verified exclusion |
|---|---|
| Deterministic SAT or UNSAT decision | c<2cos(pi/7)=1.801937... with n^o(1) space. Buss–Williams Figures 8.2–8.3 also certify (1.34070,.5), excluding (1.33+o(1),.5+o(1)) in their convention. |
| Nondeterministic UNSAT / conondeterministic SAT | Diehl–van Melkebeek–Williams: every c<cuberoot(4)=1.587401... has some e>0 excluding simultaneous n^c time and n^e space. This excludes subpolynomial space but does not set e=.5. |
| NO side, explicit positive-space example | FLMV Corollary 6.5 gives d(c)=(1+c)/c^2-c, with reduction slack. At c=1.10, d=.635537..., excluding time n^(1.10+o(1)), space n^(.5+o(1)). The reviewed statements do not supply a NO-side (1.33,.5) exclusion. |
| Nondeterministic SAT | No opposite-polarity bound above applies. Guess and retain an assignment, then verify in near-linear time with linear space. A supplied read-only assignment permits logarithmic auxiliary verification space but changes the access model. No (1.33,.5) exclusion is asserted here. |
| Specific refutation system | Resolution or other proof lower bounds apply to their verifier/representation only. General machine consequences require a costed simulation, including proof rereads and generation. |

Sources: [Buss–Williams](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf); [Diehl–van Melkebeek–Williams](https://www.ias.edu/sites/default/files/math/csdm/08-09/sdiehl_an_improved_time_space_lower_bound_for_tautologies.pdf), Theorem 1 and Section 2.1; [FLMV](https://lance.fortnow.com/papers/files/tst.pdf), random-access model Section 2.1 and Corollary 6.5. The terminal method is classical [Aspvall–Plass–Tarjan](https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/2SAT.pdf), 1979; no novelty claim for SCC or conditioning.

What survives free correct choices: local residual/proof checking, source access, full output, and coverage of universal rows. Deterministic lower bounds require removal of the advice; the enumeration theorem states its cost. Our unconditional easy subclass is consistent with all cited exclusions.

## Evidence and project integration

support_selector.py, fixed seed 202611191201: 240 randomly generated canonical three-block layouts with three shared bits and two private bits per block, 1,588 local solves, 4,162 row marks. All decisions were compared with exhaustive global assignment search: 13 SAT, 227 UNSAT. Every emitted selector entry was independently checked by exhaustive private assignment search. SCC-generated private witnesses were checked against residual clauses. The control F_0=z, F_1=not z produced the necessary varying selector [0,1].

All 30 oriented T5 path words of lengths 1..4 were checked by exhaustive original-arc evaluation against the endpoint-support formula. T5 thread tables are a local support analogue, but branch-color compatibility remains a global problem; the Boolean 2-CNF corollary is not transferred to arbitrary T5 cores or intrinsic-critical deletions.

Prior work read: PATH3 recovery report excerpt, the supplied ROW_BLOCK_SPECIALIST72 and ORBITBATCH results in the conversation, and complete SELECTOR_LOCALITY59 (Git blob c2b3c0cb9be0604731c7d9962966ebe582ebee41). The latter gives bounded-width selector elimination and SCC controls; it does not supply this arbitrary-CNF compiler. Targeted project search was performed; no priority claim is made for local-support caching. Current role has no designated TMR-owned root manuscript. Additive report/code/raw publication only; no local Git checkout or preflight/LaTeX build. Previously read project research instructions govern proof status and cost accounting.

PROVED/EXACT: streamed local-support coverage and matched SCC witness reconstruction. COMPUTATIONAL: bounded audit above. CONDITIONAL: seed-exponent improvement for small support. FALSIFIED INFERENCE: retaining every local answer is necessary; repeated decision bit-pinning is necessary for the restricted SCC terminals. OPEN: small-support/private-disjoint decomposition of arbitrary CNFs with charged discovery and hereditary closure, external peer audit, P versus NP.

Gates: DISJ PASS (easy inputs remain easy); simultaneous DTISP PASS only under explicit P,W and input model; deterministic configurations used only for consistency, no lower inference; relativization/algebrization supply no separation hinge; Natural Proofs not invoked. No titles, ownership, schedule or enabled states changed.

Next blocker: extend the terminal class while retaining an actual witness/refutation producer and prove a paid bound on D=sum 2^r_i. Small local support alone leaves arbitrary private CNFs, so it cannot replace the child solver.

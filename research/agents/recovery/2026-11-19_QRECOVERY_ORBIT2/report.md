# QRECOVERY-ORBIT2: boundary reuse needs a witness transporter

19 November 2026, America/Los_Angeles. Role: prior-work recovery. **PROVED restricted transport; COMPUTATIONAL targeted audit; all-CNF transfer OPEN; independent peer review PENDING. P versus NP OPEN.**

## Recovery ledger and non-duplication

This run advances one dependency: reusable row/block results must transport original witnesses, not merely labels. The color symmetry itself was already recorded in QRECOVERY1; no novelty is claimed for graph-coloring symmetry. We make its boundary cache, reconstruction costs and failure cases executable.

| Recovered original | Retrieved blob | Reusable result and restriction |
|---|---|---|
| research/agents/recovery/2026-11-19_QRECOVERY1/report.md | 112ee7c7b7f5d9197930ff04c80ea2209a112242 | Private-head Q equals graph 5-colorability for decision; weighted extension counts differ. Critical-deletion transfer is exact, growing-girth critical search reduction remains open. |
| research/agents/recovery/2026-11-19_LOCAL4/report.md | 88695b6575e63e3af9311ba6533768279fba2dd3 | Independent row-certificate enumeration adds costs; it need not enumerate the Cartesian product of all row certificates. Shared consistency obligations can invalidate the factorization. |
| research/agents/proof/2026-11-19_POSITIVE_SELECTOR_HORN2/report.md | 0a2af364629c84b6ca0972d6dad39a964b186f25 | Source-support reuse, UNKNOWN-safe refuting coverage, tractable terminal/backdoor search; source compiler remains conditional. |
| research/agents/proof/2026-11-18_Q_SIGNATURE_SELECTOR/report.md | 216b4b8a683447d7c269174a11830c6a10f45410 | Fixed-head signatures and an O(5^k L) source-discovered backdoor solver; equality-pattern caching below is a different, private-head projection. |

LOCAL4 recovers LEAD-0023, ORBITBATCH1, WRAPPER_INDEX_REPLAY1 and PATH3. Their claims are indexed here through LOCAL4, not represented as fresh audits of all historical originals. Repository searches were targeted; comprehensive unmerged-branch discovery was not performed. Published predecessors sometimes carry different timezone labels; their paths are provenance identifiers, not this run's date.

The supplied archive was resolved by its exact Library ID/title and recovered from the existing local copy. SHA-256 d811f0ea0b00fc88ebecf2349585386a2f0079508139aa638a8635e765e8a30a and all 23 manifest entries were checked again. The completed 2320 paired runs, 600-run appendix and 4096 four-variable systems were not repeated. The capped n40,m60,seed202611580003 result remains UNKNOWN. The 283-variable/236-clause fixture retains fixed incidence girth 8; no new review of its 236 witnesses is claimed this run.

## Exact transport theorem

Use exactly A:BD, B:CE, C:AD, D:BE, E:AC, and R(a,a)=false. Q(h,u,v) is XOR, P is AND. Names in a clause are distinct; letters may coincide. Direct enumeration confirms Q accepts 60 and P 20 ordered triples. The sets are disjoint because XOR and AND cannot both hold.

Let F_G consist of Q(h_e,u,v) for each edge uv of a simple graph G. Every h_e is a distinct private variable occurring only in that clause, never as a tail. All pins under consideration are on a designated tail boundary X of size r; there are no other absolute pins or constraints. Source recognition must check these occurrence and pin conditions before applying the theorem.

**PROVED/EXACT.** Two boundary assignments with the same equality partition have the same extension decision. Given a tail coloring extending one assignment, a full Q witness extending the other can be constructed and verified in O(|V|+|E|+r) indexed operations and O(|V|+|E|) words, with streamed head output allowing less retained head storage.

Proof: each Q clause has some private-head extension iff its two tails differ. If a beats b, set the head to a: Q(a,a,b) is true, since the tie is a non-win. Thus tails must and need only form a proper graph coloring. Equal boundary partitions induce a bijection between their used colors; extend it to a permutation of all five colors. Permute the entire tail coloring. Disequalities are preserved. For each edge, independently test the five possible head colors and choose a successful one; then verify each original Q clause. Restriction of any proposed counterexample and application of the inverse permutation prove NO-label preservation too. QED.

This also works for T3 and any fixed tournament, with the alphabet size charged if it varies. It is not specific evidence of T5 hardness. It depends on independent private heads; shared heads or extra pins require a new proof or a smaller valid symmetry group.

**FALSIFIED transfer:** applying that permutation to all colors of an existing Q witness need not work. Q(A,A,B) is true. Swapping B and C and leaving A fixed produces Q(A,A,C), which is false. This uses distinct variable names assigned the letters shown, so it respects the grammar. Even a single pinned-head clause can therefore invalidate the graph-projection cache.

**FALSIFIED counting transfer:** one private head above tail letters (A,B) has four extensions, while (A,C) has two. Both boundary assignments have the same equality partition. Decision and one-witness transport are valid; unweighted exact-count reuse is not. Original P, binary R and tie-forbidden win/loss variants cannot inherit the cache without a separate reduction. The archive's Q semantics, including ties, are used throughout.

## Uniform cache and cost ledger

Canonicalize a boundary row by numbering its colors in order of first appearance, e.g. (D,D,A) becomes (0,0,1). For fixed alphabet five this takes O(r). The number of possible keys is

A_r = sum_{j=0}^5 S(r,j),

with S(0,0)=1. For r=0..8 it is 1,1,2,5,15,52,202,855,3845. Each orbit has at most 5!=120 members, so 5^r/120 <= A_r <= 5^r. For r>=1 rotation alone has 5^(r-1) representatives. This quotient gives a bounded-factor saving for fixed T5, not an asymptotic exponent improvement. It does not make exponentially many global rows polynomial.

For an authenticated block of size L, R boundary queries, and A encountered keys, let C(L),S(L) be a *total exact* representative solver's worst-case time/space, including every failed attempt and both polarities. A cache retaining one witness per SAT key costs

T = O~(L + A C(L) + R(r+L)),
S = O~(L + S(L) + A L).

The R L term allows reconstructing, checking and emitting a complete witness for every SAT query. It is not needed if only labels are requested. Parsing, detection of true private heads, support extraction, canonical keys, permutation construction and source access must be paid. A falsely reported private head cannot be used to justify a merge. No SAT/UNSAT label is advice.

For the global selector, retain labels and selected block indices rather than all witnesses. Stream one block at a time; build that block's key-to-label table, visit all R shared rows, and mark only rows certified UNSAT by that block. At end, all rows marked means NO. Otherwise, if all needed children were decided, replay all children at an uncovered row to emit its original SAT witness. With explicit block-qualified private IDs, costs are

T = O~(N + sum_i A_i C(L_i) + R sum_i(r_i+1) + sum_i C(L_i) + output),
S = O~(Lmax + max_i S(L_i) + max_i(A_i r_i) + R log B).

A_i counts keys actually encountered; for a full five-valued boundary space it is A_(r_i). Authentication of the canonical layout and witness-preserving residual compiler is a premise. The small functional experiment uses a witness cache, so it does NOT claim to measure this lower-memory label-only wrapper. It additionally retains raw evidence and direct comparison runs.

UNKNOWN labels cannot mark a row. If all rows nevertheless have another checked rejecting block, NO remains sound. SAT requires all children on one row to produce checked witnesses. Unknown keys elsewhere may remain unresolved. Caching UNKNOWN preserves uncertainty, not a final label.

For the user's Boolean shared-row layout, support reuse has at most 2^r_i restrictions; equality-partition merging is valid only if the residual is exactly this private-head family and the compiler respects the color permutations. It is not an arbitrary Boolean-complement symmetry. The old generic scan remains time exponent max(1.195,.845+.35c) and space exponent at least max(.35,.35s) for a child seed L^c/L^s, before additional costs. Achieving 1.33 and .5 requires c<=97/70 and s<=10/7. A polynomial seed with unspecified exponents does not meet these requirements automatically. Our bounded-factor cache supplies no missing exponent contraction or hereditary compiler.

## Correct-path and polarity ledger

A free correct polarity label answers the decision question by advice; it does not acquire a witness or refutation. A uniform specialist instead returns a verified witness, a sound NO, or UNKNOWN. A known time-and-space completeness cap on *all* inputs of one polarity permits a total decider by capped simulation, with the other label on cap exhaustion. A promise-only cap does not.

A supplied k-bit SAT path must produce a consistent full assignment, checked on all original clauses; every incorrect accepting claim is forbidden. Here a supplied tail coloring can be checked and lifted cheaply. It is not the deterministic cost of finding that coloring. A NO path selecting a monochromatic edge checks one specified row only; every universal row still needs coverage. A rejected route is not a whole-input refutation.

For a sound, complete, bounded verifier of cost V and workspace S, deterministic enumeration has upper bounds O(2^k(V+k+1)) and O(S+k+log V), plus source/layout and output costs. For independent per-row verifiers, LOCAL4 gives a sum over rows of those terms, not necessarily 2^(sum k_z). Adaptive cross-row consistency must be proved absent. A k-bit program describing an adaptive strategy is not a k-bit transcript: account for its validation on all universal histories or retain alternation explicitly.

Read-only indexed certificate access differs from ordinary nondeterministic guesses. Forgotten guesses are not rereadable unless stored or consistently reacquired. All replay, cache retention, verification and complete outputs are charged. Our cache is ordinary writable state; a stored witness contributes its full length to peak space. Free correct choices can eliminate search for a SAT representative or bad block, but do not automatically eliminate original-source verification, head reconstruction or universal NO coverage. None of these algorithm-specific obligations is an unrestricted runtime lower bound.

## Sourced simultaneous RAM exclusions

Models: uniform random-access machines, read-only input, write-only output, charged work and address storage; log-word simulations pay polylog factors. No free two-way guessed tape or unbounded unit-cost arithmetic. Formula length is the encoded source length, not an uncharged padded representation.

| Model/polarity | Reviewed theorem and limitation |
|---|---|
| Deterministic SAT and, by complement, UNSAT | Buss–Williams Theorem 2 gives SAT outside DTISP(N^1.34070,N^.5), with +o(1) exponents in its definition; therefore the all-CNF (1.33,.5) target is excluded. Subpolynomial-space benchmark uses c<2cos(pi/7). |
| Uniform sound deterministic specialist, complete with known cap on one full polarity | Same exclusion after capped conversion. Promised private-head blocks are not all CNFs. |
| Nondeterministic UNSAT / co-nondeterministic SAT | FLMV Corollary 6.5: NTIME[N] not contained in coNTISP(N^c,o(N^((1+c)/c^2-c))). At c=1.10, the space exponent is .635537..., allowing a (.1 above linear,.5) exclusion with reduction slack. At 1.33 this displayed exponent is negative. |
| Nondeterministic tautology/UNSAT | Diehl–van Melkebeek–Williams: c^2 d<4 gives some e>0 excluding simultaneous availability of time N^c and time N^d/space N^e algorithms. With c=d, d<cube_root(4)=1.587401...; e is not established as .5. Formula negation and CNF encoding require charged reductions. |
| Nondeterministic SAT | No corresponding (1.33,.5) exclusion follows from those NO-side sources. A supplied rereadable satisfying assignment is a different resource model. |
| Proof-specific refutations | No transfer from resolution, monotone circuits, oracle queries or restricted interfaces to unrestricted execution without proof. |

Sources rechecked this run:
- https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf — Theorem 2/table, exact consulted conference version.
- https://lance.fortnow.com/papers/files/tst.pdf — sections 2.1/3 and Corollary 6.5.
- https://research.cs.wisc.edu/techreports/2007/TR1601.pdf — Theorem 2 and explicit two-way-guess limitation.
- Mendez-Diaz and Zabala, graph-color symmetry context, primary publisher abstract https://doi.org/10.1016/j.dam.2005.05.022 . Full publisher text was inaccessible; no theorem above relies on an unread proof from it.

## Executed evidence and remaining gap

`orbit_recovery.py`, seed 20261119001, tests 16 generated five-tail graphs with three boundary tails, K6, and all 15 K6 edge deletions with two boundary tails. These are 32 source graphs and 2400 boundary rows. All answers matched direct original-tail enumeration: 1770 SAT, 630 UNSAT; 112 cached representative solves. Every lifted witness was checked on original Q, with 10,720 successful clause checks. K6's 15 deletion families all include SAT witnesses, while the full K6 has none. These are small fixed critical controls, not growing-girth results.

A second inline checker used an explicit win matrix rather than the producer's Q predicate; it checked all published SAT witnesses and exhaustively rejected every NO row by tail-color enumeration. This is separate implementation checking by the same author, not independent peer review. The raw file contains all exact graphs, rows, keys, witnesses and counters. The counters deliberately include direct-oracle comparison work and are not presented as cache-only operation counts. Preprocessing/model costs are accounted symbolically above; counters are selected kernels, not every machine instruction.

The run took about 0.63 seconds including audit work before serialization. A separate traced C5 case peaked at 49,960 Python bytes, including witness cache, all row records and direct comparison enumeration, excluding earlier cases and JSON serialization. This is not OS RSS or an asymptotic RAM bit-space measurement. Source SHA is embedded in raw output; published compact-JSON SHA-256 is 7b52ebb80e4c0d2b503901183336220fd6563ba56e65f81d9adcdd128d5057ac (the original pretty-printed run had SHA-256 5a761c957e008b3a63feed30511f9385b287980fc6b961946414eaa01d46bf73). The post-run statistics query initially used a missing zero-valued counter key for the all-UNSAT case; the solver/evidence had already completed successfully. The corrected independent checker established the totals above.

**PROVED:** boundary-partition decision reuse and reconstructed original witnesses on authenticated private-head Q. **FALSIFIED:** whole-Q witness permutation and unweighted count reuse. **CONDITIONAL:** integration into an authenticated arbitrary-source row/block layout. **OPEN:** obtaining that layout uniformly, avoiding global coverage cost by a proved source algorithm, and intrinsic critical/high-girth search reductions. This run adds an executable transport audit to an already recovered symmetry, rather than claiming a new generic coloring algorithm.

DISJ: no information lower bound claimed. Relativization: no separation claim. Simultaneous DTISP: resources of the same cache execution charged; unrestricted transfer blocked. Configuration counts: upper-bound consistency only. Natural Proofs/algebrization/circuit claims are not used. No manuscript ownership, title or schedule changed. No mapped root-manuscript ownership or local checkout was available, so root reconciliation and repository preflight are not claimed. Additive report/code/raw/handoff publication preserves prior evidence. Independent peer audit remains pending.

Next blocker: a source-checkable family of substantially fewer continuation classes, together with a paid witness transporter and global cover algorithm. The present constant-factor symmetry alone cannot supply it. P versus NP remains OPEN.

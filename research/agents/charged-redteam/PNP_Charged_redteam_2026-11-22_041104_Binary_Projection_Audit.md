# Independent audit of the mixed-to-binary decision branch

22 November 2026, 04:11:04 PST. PNP Independent Counterexamples.
**DYNAMIC-BINARY-ADMISSION-ORDER1**, under DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT** restricted semantic audit and order-dependence counterexample. **COMPUTATIONAL** exhaustive finite audit. The proposed extension that admission is invariant under arbitrary parity-row permutations is **FALSIFIED** on general mixed sources. Discovery asserted this coverage for its synchronized cycles, which survives the audit. Its soundness claim survives the independent reconstruction below. This review is internal, with full machine implementation and external review pending. P versus NP is **OPEN**.

## Target and scope

Fix Discovery's reduce_source function at c97d245967c8ed3c3c2abae6f1b42978b0ca65ec before choosing the input. Its source file SHA-256 is 08288167c78590a88462b063e20c4df9588dfec12de81484ef14c85c822261bb. It expects already authenticated disjoint exact-one triples and even-parity triples of distinct variable names. It returns SAT, UNSAT or UNKNOWN. In the complete proposed SAT machine, UNKNOWN triggers exact fallback on the retained original input.

The audited statement is that every decisive return agrees with the original mixed formula. The extra admission-order hypothesis says that merely permuting parity rows preserves whether the function returns UNKNOWN. The latter is a natural strengthening to test, and is not claimed by the peer for arbitrary mixed inputs. [Pinned report](https://github.com/j15marti/pnp/blob/c97d245967c8ed3c3c2abae6f1b42978b0ca65ec/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_034845_Mixed_To_Binary.md) · [Pinned implementation](https://github.com/j15marti/pnp/blob/c97d245967c8ed3c3c2abae6f1b42978b0ca65ec/experiments/dynamic_discovery_mixed_to_binary_20261122.py)

I reconstructed the source semantics independently, using explicit assignments rather than the peer's cycle transfer oracle. The prior cycle test and seven-row-pool experiment were read for provenance. The new experiment covers every multiset of at most three ternary parity rows over eight names, including repeated rows, all cross-factor patterns and helper-sharing patterns possible in this universe.

## Independent soundness reconstruction

Let F be any admitted mixed source. On a pair of checks x XOR h XOR q=0 and y XOR h XOR q=0, where h,q occur nowhere else and in no factor, elimination gives exactly x=y. Necessity follows by adding equations over GF(2). Every equal boundary assignment extends with h=0,q=x. Since both helpers have exactly these two occurrences, no other chosen pair or remaining constraint depends on the eliminated values. The code checks original occurrence counts and consumes each row once. Keeping the equality as two binary clauses preserves the coupling between original factors.

For a surviving even-parity row sharing two ports u,v with exact-one(u,v,w), exact-one implies u XOR v=1-w. Therefore the row u XOR v XOR x=0 is equivalent to w≠x while the factor is retained. If the row equals the entire factor scope, it is immediately inconsistent. Factor disjointness ensures a three-name row cannot share two names with two different factors. This avoids an ambiguous rewrite choice.

After all parity rewrites, forgetting a factor port p absent from every external binary clause is exact. On the other two ports a,z, its projection is ¬a∨¬z. A satisfying pair extends uniquely with p=1-a-z. The forgotten ports are distinct because factor scopes are disjoint. Helpers eliminated earlier are restored only after restoring factor ports, so the extension order is well-defined. Unconstrained original names may be assigned arbitrarily. All extensions agree on retained names. This proves that each successful reduction preserves both labels on every authenticated source, independent of the finite tests.

The peer's implication closure then applies the existential 2-CNF criterion. Each clause supplies the two implications. A contradictory strongly connected component implies UNSAT, and the standard reverse component order constructs a satisfying assignment when no component contains a complementary pair. This is the exact hypothesis of Aspvall, Plass and Tarjan's Theorem 1. The linear random-access tariff in that paper is not the single-tape tariff used here.

Four falsifiers are deleting a helper with an additional occurrence, forgetting a port used in a retained equality, dropping the exact-one factor before its parity replacements, and treating UNKNOWN as UNSAT. The source code guards the first two, orders the third correctly, and exposes UNKNOWN separately. A completed decider must preserve the last distinction through its fallback.

## Small order counterexample and paid repair

Use exact-one factors (0,1,2) and (3,4,5). Supply even-parity checks in this order

(0,3,6), (3,4,5).

There is no pair of checks sharing two private helpers. The first surviving row intersects each factor in one variable, so the code immediately returns UNKNOWN. Reversing the two rows makes it first inspect (3,4,5), which contradicts exact-one(3,4,5), and it returns UNSAT. The formula is UNSAT in both orders. Thus syntactic row order can control admission to the fast branch despite identical logical content.

A preliminary scan for any parity scope equal to a factor scope is a sound repair for this particular early-exit loss. Such a pair certifies UNSAT regardless of other clauses. Run it after source authentication and before the first potentially declining phase. It uses O(c² log(c+2)) logical bit work by direct comparisons of at most O(c) triples. The audit executable includes this pre-scan as a separately checked wrapper around the pinned reducer. Peer-owned files were preserved. This repair improves the sufficient recognition rule. General polynomial coverage remains unproved.

## Reproducible results

Run `python3 experiments/dynamic_redteam_binary_projection_20261122.py` in a checkout containing the pinned Discovery module and its Construction import. The oracle enumerates all 256 Boolean assignments to the eight-name ambient universe, builds a model bitset for each primitive constraint, and intersects these independently of the reducer. The test enumerates all multisets of 0,1,2 or 3 rows from the 56 possible triples, giving 32,509 cases. It checks the original and reversed row sequence in each case.

| Original result / oracle | Cases |
|---|---:|
| SAT / SAT | 4,387 |
| UNSAT / UNSAT | 2,637 |
| UNKNOWN / SAT | 24,081 |
| UNKNOWN / UNSAT | 1,404 |

There were zero incorrect decisions in either order. Reversal changed the returned status in 2,055 cases. The preliminary contradiction scan raised decisive UNSAT returns in the canonical enumeration to 3,591, leaving 450 UNKNOWN/UNSAT cases. SAT and UNKNOWN/SAT totals stayed 4,387 and 24,081. No reversal differences remained in this finite universe. That last observation is COMPUTATIONAL and supplies no theorem of order-invariant admission for arbitrarily many constraints.

A SAT decline is already witnessed by the single check (0,3,6) with the two factors above. For example ports 1 and 4 true and every other variable zero satisfy it. The formula with the same check plus (3,4,5) witnesses an UNSAT decline in its original order. These examples expose the coverage gap directly, while the exact fallback maintains global correctness.

[Executable audit](../../../experiments/dynamic_redteam_binary_projection_20261122.py) · [Raw evidence](../../../results/raw/dynamic_redteam_binary_projection_20261122.json)

## Complete decision execution and resource audit

Fix a globally correct deterministic one-head, finite-alphabet writable-tape machine A. It first authenticates the canonical compiled input by exact regeneration and field comparison, retaining the original for fallback. It then performs the checked contradiction scan and mixed-to-binary procedure, followed by exact implication closure. On a decisive result it stores the answer at origin and emits a terminated Boolean answer. On valid nonmatches or UNKNOWN it enumerates assignments to the original formula. All scope and row comparisons, failed candidates, address construction, copies, matrix initialization, reuse and output are charged. Malformed encodings follow the declared parser convention.

For a source of d occurring names and c proper clauses, use the peer's authenticated dense-range check d≤3c. Its compiler sets g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2, m0=(20c+4)g, n=n0+m0+3, m=2m0+4 and w=ceil(log2(n+1)). The full length is N=3n+2+2 floor(log2(m+1))+3m(w+1)+w. Source literal fields, two n-bit local assignments, unary declaration, gamma clause count and release ID are included. For synchronized cycles d=8t,c=26t,N=Θ(t² log t). The audit gives no claim that source geometry survives compilation.

The inherited authentication budget is O(N³) time and O(N) span. Pair discovery plus full occurrence checks, factor matching, flags, emitted clauses and dense closure fit O((c+1)^4) logical bit operations with all loop and identifier bits charged. The new pre-scan fits this allowance. O(c²) Boolean matrix bits and O(c log(c+2)) source/index records fit O(N), since the canonical wrapper has N=Ω(c² log(c+2)) for growing c. A conservative O(N²) tape-shuttle allowance per logical bit operation gives T=O(N³+(c+1)^4 N²)=O(N⁴), S=O(N) on successful fast-path inputs. It includes cleanup and relocation if the solver normalizes the cached result.

On this same execution, physical CM≤O(TN)=O(N⁵). Separately, input and transition index describe each complete deterministic configuration in O(N+log(T+2)) bits, giving minimum-description CM=O(N⁵). On valid general inputs the bound is O(N⁴+2^n N³) with O(N) span. The Python test is a semantic oracle comparison. It does not execute the compiler-image parser, the full single-tape machine, or an integrated fallback. Those physical implementation claims retain their symbolic status.

The first unresolved premise for promotion to a general polynomial algorithm is coverage with polynomial total cost on every permitted input. The witnessed UNKNOWN cases show that the current branch alone lacks that coverage. A lower-bound argument also still needs an earlier compulsory observation surviving this allowed preprocessing. Decline by this specific reducer implies no hardness lower bound.

## Actual event ledger and scope controls

On the synchronized family take the uniform distribution on the same odd-length opposite-label pair used by Construction, both words all C or both changed to A at one common position. Let U be the final decision, B the public generator, t, pair, prior and fixed solver, excluding the sampled source and cache bit. Let E contain only the real origin-cache read at READY and Π be the bit read. The decoder returns that bit, the records are fixed length, b=1,h=0,ρ=1 and H(U|B)=1. Therefore the shared entropy inequality yields E[T]≥1. Authentication and all previous transitions remain charged. Repeating this obligation raises reuse. Additional residual questions require a separate actual decoder. Bounds' new selector debit also applies if event locations are input-dependent and otherwise unavailable.

Against T≤K N^a, a≥1, the same-execution ceilings are S=O(N^a), physical CM=O(N^(2a)), description CM=O(N^(a+1)), and count-map circuit size O(N^a log N). This audit excludes no fixed exponent. The static transport result keeps its internally reviewed one-tape quadratic/cubic calibration and ceiling. DISJ/equality and simultaneous DTISP checks pass at the stated scope. Deterministic configuration counting is used only for an upper description bound. Relativization, algebrization and Natural Proofs yield no unrestricted promotion. Affine/Tseitin, complement, private-leaf, forced-domain, relocation, shared computation and cheap decision witnesses remain permitted. Counting and strict T5 consequences are outside this decision audit.

## Searches, provenance and handoff

Fresh literature query “Aspvall Plass Tarjan 1979 2SAT strongly connected components theorem pdf” was followed by reading Theorem 1 and its constructive proof in the March 1979 paper. It applies to existential CNF with at most two literals per clause. It supports the final binary decision after the proved rewrites. It gives neither all-input coverage of these rewrites nor compulsory SAT work. [Primary source](https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/2SAT.pdf)

Fresh official GitHub searches used `"variable elimination" "satisfiability"` separately in anthropics, openai, xai-org, google, google-research and google-deepmind. OpenAI's initial HTTP429 was retried successfully with no hits. Four other organizations also returned no hits. Google returned an OR-Tools parameter comment concerning bounded variable elimination occurrence counts, at 4782dbd0aa85621c8115cf33de1574a2e6757004 in ortools/sat/sat_parameters.proto. This excerpt motivates checking discovery costs but supplies no theorem for this reducer. No external code was imported. Ownership was checked from official organization profiles and corporate links. [Google excerpt source](https://github.com/google/or-tools/blob/4782dbd0aa85621c8115cf33de1574a2e6757004/ortools/sat/sat_parameters.proto) · [Anthropic](https://github.com/anthropics) · [OpenAI](https://github.com/openai) · [xAI](https://x.ai/news/grok-os) · [Google](https://opensource.google/documentation/reference/github/where) · [Google Research](https://research.google/resources/) · [DeepMind](https://github.com/google-deepmind)

Mandatory model/governance/coordination/T5 files, all current role handoffs, latest Redteam report, the target proof/code/raw, its Construction dependency and recent issue324 entries were recovered at 77b51cd8f49ed5077f66e4978cb55e09d71016ec. Full-checkout preflight, LaTeX compilation, kernel verification and machine-level execution were unavailable in the selected-file environment. This is a fresh internal adversarial audit, with prior peer context visible. It is not blinded external review.

**One next dependency for Discovery and Synthesis.** Integrate the safe contradiction pre-scan and state coverage in terms of the actual recognizer, preserving UNKNOWN fallback. Seek a proved polynomial extension for still-declined sources rather than inferring complexity from the decline. Accounting receives the unchanged conservative fast-path exponent and the explicit extra scan charge. Bounds receives the surviving one-bit final event and the still-open earlier-observation premise.

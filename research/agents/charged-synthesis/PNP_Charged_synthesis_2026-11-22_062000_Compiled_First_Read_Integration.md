# Compiled first-read obligations and their preprocessing ceiling

22 November 2026, 06:20:00 PST. PNP Charged Proof Synthesis.
**DYNAMIC-COMPILED-FIRST-READ1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT, restricted symbolic result:** the canonical adjacent-witness compiler preserves disjoint decision-sensitive supports for Bounds' parity-chain family. Its first-read theorem therefore holds directly on the complete N-bit image. **COMPUTATIONAL:** full small-image differences and sparse large-image offsets agree with the formula below. The new composition awaits independent adversarial review. It is a reconstruction with peer context visible, not external review or kernel verification. P versus NP remains **OPEN**.

## Source revisions and five-peer integration

All following bodies were recovered at main snapshot `21979fa2c54f0fb44f7e85710408d88045114d5f`. Links pin that snapshot rather than a moving branch. This note continues the compiler audit already undertaken in this conversation; it does not claim a second independent researcher or repeat its completed experiment.

| Peer and exact report | Established statement incorporated | Limitation retained |
|---|---|---|
| [Construction, 05:30:32](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_053032_Monotone_Tail.md) | A closing AA tail with equal endpoints is constant. The explicit both-label family is decided by two candidates despite large AA count and syndrome rank. | Restricted polynomial branch, with correct exponential fallback. Large sufficient search scores are not necessary costs. |
| [Discovery, 05:51:11](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_055111_Switch_Position_Completeness.md), blob `0f2daff4145d6ea3b5bc9112556339edee47275f` | Positive one-in-three SAT reduces to synchronized cycles with AA blocks of lengths two and three. The separator pins each block 1 to 0. | Completeness is a decision equivalence, not compulsory evaluation of a switch DAG. |
| [Accounting, 05:41:00](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_054100_Copy_Event_Ledger.md) | q actual copied-bit reads have reuse one even when all payloads are equal; q aliases of one actual cache read have reuse q. | Neither copied reads nor their physical storage are compulsory for other solvers. Correlation is not event overlap. |
| [Bounds, 06:05:16](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_060516_First_Read_Debit.md) | Every correct fixed solver reads q sensitive regions of the packed parity family; at an observable checkpoint its remaining certificate is q minus regions acquired. | Its report explicitly left transfer from packed length L to compiled length N open. This note closes that layout implication only. |
| [Redteam, 05:15:42](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-22_051542_Forced_Alternation.md), blob `05fd606b8f2dea440da6207fd21a6eac3e636dd4` | No-AA cycles have at most two possible local paths, regardless of full parity-code trellis rank. | The full code and the actually feasible paths are different objects. |

Original evidence inspected includes Discovery's switch generator/raw (blobs `ccc6d04af3ddea47d4891403a10ef1481cf28cd8`, `c865a8a1289cd12bb2c6657765f2bab7dec36f35`), Bounds' generator/raw (`ebd6798218ca868b611a02f5cf0b74bcb38919b5`, `33c3ba531b001197edfe6c08ef986da33b636ca9`), Accounting's suffix checker/raw (`0698ed6cb051e9abcf845346edf8b0baee341c0f`, `2326e532e462d4e95e5fa9a761958547e9cd619b`), and the recovered Construction/Redteam source controls. Their finite counts remain peer evidence, not newly executed tests. The [prior synthesis](PNP_Charged_synthesis_2026-11-22_042119_Binary_Backdoor_Portfolio.md) remains a sound restricted portfolio with no universal polynomial coverage bound.

The strongest general decision candidate is Discovery's short-block cycle template: it captures an NP-complete problem without an exponential truth table. The strongest currently proved compulsory-execution claim within it is Bounds' parity subfamily. We work on its first unresolved implication, physical compiler support, instead of treating completeness as a hardness proof.

## Model, quantifiers and four falsifiers

Fix a deterministic uniform globally correct decision solver A first. A has one finite-alphabet writable tape, one head, unit moves, read-before-write transitions, input-independent initial control, and terminated Boolean output at the fixed origin. Input, copies, addresses, caches and all work occupy this tape. No free source oracle or advice is supplied. Span contains the origin, head and nonblank support. Preprocessing, relocation, algebra and shared computation are permitted and charged.

For every q≥1 and every choice vector b in {0,1}^q, construct the canonical image I_q(b) below. For every stopping checkpoint tau determined by actual observations, let R_tau count supports read by then. The composed restricted theorem is

    T_A(I_q(b)) - tau >= q - R_tau(b).

This universal solver claim concerns this input family and declared machine model, not every SAT input or unrestricted computational model. Four concrete falsifiers are: a coordinate flip preserves the decision; the compiler leaks that coordinate into shared metadata or overlapping supports; the first-read decoder receives an uncharged selector; or previously read coordinates are charged anew. The construction, layout proof, paired simulation and explicit subtraction respectively address them.

## Source semantics and complete length ledger

Let E(a,b,c) mean exactly one true occurrence, with repetitions counted. Use z=0, o=1, x_i=2+i for 0≤i≤q, and w_j=q+2+j for 1≤j≤q as source name IDs. Begin with E(z,z,o), E(x_0,x_0,o), E(x_q,x_q,o). For each j append

    E(x_(j-1),w_j,z),
    E(x_j,w_j,z) if b_j=0; E(x_j,x_(j-1),z) if b_j=1.

The first three clauses force z=0,o=1,x_0=x_q=0. The remaining clauses give w_j=1-x_(j-1) and x_j=x_(j-1) XOR b_j. Thus SAT holds exactly when XOR b=0, and flipping any one b_j reverses the label. Both labels occur.

Discovery's map uses a two-edge AA variable block and a three-edge AA clause block, each followed by CC,AC,CC. The separator forces the preceding endpoint to 0 and the next start to 1, including the cyclic seam. A variable block has vertices 1,X,0. A clause block has 1,B,C,0, with edge differences (1 XOR B,B XOR C,C) equal to exactly one of 100,010,001. Three parity equations equate these differences to the three referenced variable interiors. Repeated names reuse the same variable interior, while all three physical endpoints within each parity equation remain distinct. These facts give both decision directions.

Here v=m=2q+3, cycle columns t=22q+33, and appended parity rows r=6q+9. The proper source CNF has d=8t=176q+264 and c=26t+4r=596q+894. Its canonical order emits the five forbidden exact-one tuples for every factor, then four forbidden odd tuples for every parity equation. No clause sorting, deduplication or input-dependent renaming is performed. Every source name remains present in the unchanged factors or rung clauses.

The compiler is [the original dihedral implementation](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/experiments/dynamic_construction_dihedral_choice_20261121.py), blob `2594827de4212907b08418336b47f15e85f44b92`, using the [adjacent-witness wrapper](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/experiments/charged_unsat_transport_20261121/charged_unsat_transport_audit.py) and [serializer/parser](https://github.com/j15marti/pnp/blob/21979fa2c54f0fb44f7e85710408d88045114d5f/experiments/dynamic_synthesis_reachable_splice_20261121.py), blob `74fec50de87788c6597f108ceb8b7b8368fb0b46`.

    g=max(3,2 floor((c+1)/2)+1)
    n0=d+(10c+1)g+2; m0=(20c+4)g
    n=n0+m0+3; M=2m0+4; W=ceil(log2(n+1))
    H=n+2+2 floor(log2(M+1))
    N=H+3M(W+1)+2n+W=Theta(q² log(q+1)).

H is unary-n plus delimiter plus gamma(M+1); each literal uses a sign and W address bits. The final fields are two n-bit local witnesses and the W-bit release ID. N, not the packed L=Theta(q log(q+1)), is used below. The compiler's Boolean equivalence and adjacent local witness property are inherited, with their existing internal-review status. Briefly, each ternary instruction word translates the dihedral state by 4 exactly on a violated clause and otherwise acts identically. Since g is odd and exceeds c, endpoint zero means zero violated clauses. The wrapper existentially enforces every intermediate clause. This is a decision construction, not a count-preserving assertion.

## Exact compiled support theorem

All indices in this paragraph are zero-based. Flipping b_j changes the first address of appended parity row 6j+7, from column 5(q+2+j)+1 to column 5(j+1)+1. Top z at column k has positive proper-CNF ID 3k+3. Write

    a_j = 3(5(q+2+j)+1)+3,
    a'_j = 3(5(j+1)+1)+3,
    k_j = 26t+4(6j+7).

Exactly the first literal IDs of proper-CNF clauses k_j,...,k_j+3 change from a_j to a'_j; their signs do not change. The four forbidden odd tuples are enumerated in the same order.

In a ten-instruction dihedral word the first literal occurs at positions u=0,2,6,8. Changing its ID with its sign fixed preserves its action and every conditional destination. It changes only the selector guard ID in each of the 2g transition clauses for that instruction. Hence each b_j changes 4·4·2g=32g guard-address fields and no state ID or sign.

For source clause k, instruction position u, vertex v in {0,...,g-1} and branch bit e in {0,1}, set

    ell=10k+u,
    s=4g+2g*ell+2v+e,
    p=H+3(5+2s)(W+1)+(W+1)+1.

s is the intermediate clause index; target clause 5+2s is the second wrapper clause, whose second literal is the unchanged-position selector guard. Thus p is the first bit of its ID field. Let J_j be the positions where the W-bit expansions of a_j and a'_j differ. Define

    D'_j = {p+i : k_j<=k<=k_j+3, u in {0,2,6,8},
                    0<=v<g, e in {0,1}, i in J_j}.

This is precisely the full-image difference support between I_q(b) and I_q(b XOR e_j), independent of the other coordinates. It is nonempty and has size 32g popcount(a_j XOR a'_j). Distinct j have distinct original clauses, hence distinct instruction layers, intermediate clauses and target fields. Their D'_j are disjoint.

All remaining fields are invariant: d,c,g,n0,m0,n,M,W are fixed; every pin and auxiliary allocation is fixed; the two witness strings mark only fixed wrapper variables; the release variable and framing are fixed. The edit has no downstream change to permutation destinations because destination calculation uses the literal's sign and action, not its numeric selector ID. This completes the symbolic proof of the support transfer, including metadata. It does not assume physical adjacency of original columns after compilation.

## Actual decoder and event accounting

If A never reads D'_j, its executions on the two opposite-label images are identical throughout. A write cannot secretly erase a difference because it first reads that cell. Correctness therefore forces a first read of every D'_j, even if that read occurs during copying or relocation.

For uniform b and fixed q, let H_tau contain the actual observed positions, symbols, writes and control transitions through an observation-defined stopping rule. It excludes unread initial cells and the complete tape configuration. This is analytical side information, not a transcript A must store. Set U_j=b_j and B_j=(q,A,encoding,stopping rule,b_-j,H_tau). If D'_j has been read, B_j determines b_j; otherwise paired histories are identical and the conditional bit is fair. Consequently H(U_j|B_j)=Pr[D'_j unread at tau].

For an already read support take E_j empty and Pi_j empty. Otherwise E_j is the singleton actual first-read transition of D'_j after tau, and Pi_j is its initial binary symbol. Given B_j, simulate the two candidate inputs until this first differing read: all preceding observations coincide, so the address is determined without b_j or a supplied timestamp. Pi_j distinguishes the two candidates. This proves the decoder, including event selection. Decoder runtime is irrelevant to the information inequality and is not supplied free to A.

For each fixed B_j the codebook is either {empty} or {0,1}, so it is conditionally prefix-free. Per-event capacity is b_cap=1, framing h_j=0, and maximum reuse rho=1 because one transition scans one cell and supports are disjoint. Summing actual event membership yields

    E[T_suffix] >= (sum_j H(U_j|B_j)-sum_j E[h_j])/(b_cap*rho)
                = q-E[R_tau].

Pointwise T_suffix≥q-R_tau follows from the same event sets. This is now a theorem about the N-bit images themselves, not an inequality obtained by subtracting a reduction runtime from an L-bit lower bound.

The 32g copies do not multiply the proved demand: one of their differing symbols already identifies b_j. We have proved one compulsory event per coordinate, not one per replicated address field. This does not contradict Accounting: distinct actual repeated reads can legitimately have reuse one. The missing statement is that such additional events must occur for every solver.

## Paid bypass, resource ledger and cap comparison

A fixed all-input-correct solver can authenticate the whole canonical image, recover the parity-chain source, evaluate XOR once, cache its label, clear its work and output. All failed guards lead to exact exhaustive fallback on the retained formula. Authentication is exact regeneration/comparison, including witnesses and framing, not hash equality. With the inherited explicit one-tape tariffs:

| Same execution component/resource | Admitted parity-chain image |
|---|---|
| Parsing, bounded fields, source recovery and authentication | Included in O(N⁴) transitions, O(N) span |
| Discovery, failed candidates, conversions, address operations and source access | Included in that same bound; no favorable decomposition is supplied |
| Copies, relocation, initialization, shared XOR accumulator, cache and clearing | O(N) span throughout; all accesses and sweeps paid |
| Return to origin and terminated output | Included in O(N⁴) |
| End-to-end T and peak physical S | O(N⁴), O(N) |
| Physical CM | O(N⁵), by summing actual span on this execution |
| Minimum-description CM | Separately O(N⁵), by original input plus step-index replay |
| General valid-input fallback | O(N⁴+2^n N³) time, O(N) span |

The first-read bound and this upper bound coexist. After the paid full-image scan, R_tau=q, so the first-read certificate is zero. After computing and framing the cached decision the remaining work can be constant. No universal positive fresh-q suffix lower bound survives that checkpoint. This is a legal bypass of a proposed replenishment claim, not a counterexample to Bounds' correctly debited theorem.

Since q=Theta(sqrt(N/log N)), the acquired-information demand excludes no cap K N^a with fixed a≥1. Generic cap ceilings remain S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)); count-map circuit size O(N^a log N) remains a separate counting assertion. No cumulative lower bound is obtained by multiplying unrelated maxima. The internally reviewed permutation theorem retains its single-tape quadratic-time/cubic-CM calibration and static ceilings. This note does not promote it to an unrestricted separation.

## Both research directions and the next dependency

For a general positive one-in-three instance with v occurring variables and m triples, Discovery's cycle has t=5v+6m, r=3m, d=8t and c=26t+12m. Hence N=Theta((v+m)² log(v+m+1)). On total source length L, its conservative reduction cost O(L⁵+N³) is polynomial. A single uniform polynomial-time decider on all such generated images, with constants independent of the input, would therefore prove P=NP. Conversely these explicit instances have polynomially verifiable assignments. The inverse and an O(2^v) exact enumeration give correctness but no general polynomial bound. The parity-chain shortcut only covers a special affine subfamily and does not resolve this general question.

The lower-bound chain is now: explicit both-label family → exact compiled disjoint supports → actual first-read decoder → bounded event reuse → q minus acquired supports. Its next arrow, repeated fresh obligations after paid acquisition, remains OPEN. The new local-view continuation requires actual reachable opposite-answer checkpoints of the same fixed machine and disjoint first-clearing phases. The prepayment continuation forbids resetting exhausted static potential by renaming residuals. Neither premise is supplied by NP-completeness, copy counts, large trellis width, source clauses, or a required witness representation.

**ONE next mathematical dependency: DYNAMIC-POST-ACQUISITION-OPPONENT1, owner Bounds.** For a fixed arbitrary correct solver on the NP-complete short-block template, identify an actual reachable checkpoint after the initial sensitive regions have been acquired and prove a nonzero suffix observation obligation using reachable opposite-answer checkpoints, charged selectors and bounded reuse. Specify the condition selecting that checkpoint; it cannot be an arbitrary checkpoint after the answer is cached. Either exhibit such a model-derived obligation with explicit quantifiers, or return the smallest legal bypass. One such phase alone still does not defeat every fixed polynomial exponent; any eventual separation needs a same-run recurrence and cap comparison for every fixed K,a.

| Receiving role | Concrete handoff |
|---|---|
| Bounds | Use D'_j and the exact debit as the initial phase; own the post-acquisition opponent dependency. |
| Accounting | Audit rho=1 and h=0 for paired first reads, then distinguish real replicated events from aliases before summing phases. |
| Redteam | Independently attack the full offset formula, dense-name invariance and checkpoint decoder. A review is requested before broader promotion. Test any recurrence against the paid cache. |
| Construction | Preserve the exact source and compiler order; provide an opponent-family candidate on the general short-block template, or a further authenticated shortcut. |
| Discovery | Preserve the constructive alternative: seek an acquired exact contraction/key with a polynomial all-input bound. Report UNKNOWN and exponential residuals explicitly; no forced switch-DAG enumeration. |
| Synthesis | Compose only reviewed same-model arrows; retain constructive completeness and the unresolved universal recurrence as separate implications. |

No additional agents were activated. Review requests are carried by this file and issue324.

## Reproducible evidence and review gates

[Standalone checker](../../../experiments/dynamic_synthesis_compiler_support_20261122.py) and [raw evidence](../../../results/raw/dynamic_synthesis_compiler_support_20261122.json) preserve the completed audit byte-for-byte. Code SHA256 is `ecb64f68bdebdb92ceeda5702d34b2382f7060ebdcf7512349a0a30d78702a65`. Four full small compiled strings, each 20,801 bits, cover two independent first-ID edits; exact observed differences equal the predicted sets, 80 bits per coordinate, across all settings. For q=1,...,8, all 36 sparse cycle supports have the exact predicted cardinality, nonemptiness and disjointness. Their ordered-offset digests and endpoints are retained. For q=1 the complete image length is 7,398,884,972 bits; that image was not allocated. Larger controls likewise calculate sparse offsets, not full target formulas. No random seed.

This new evidence tests identifier edits through every compiler field, unlike the earlier sign-edit star control. It does not rerun the 830 projected reductions or 3,069 decoder fibers. No full cycle-image solver run, native tape benchmark, kernel proof or LaTeX build is claimed. Full-checkout preflight was unavailable in this selected-file environment; governance and original sources were recovered through connected reads. No historical TMR manuscript ownership was acquired.

DISJ/equality sanity: PASS as preserved polynomial controls. Simultaneous DTISP: PASS for the stated symbolic same-execution bounds. Deterministic configuration counting: PASS only as a description upper bound. Relativization: no unrestricted separation or nonrelativizing step claimed. Algebrization and Natural Proofs supply no promotion. Affine/Tseitin, complement, forced-domain, private-leaf, relocation, shared computation and cached-decision controls remain legal. Strict T5 counting, symmetric C and ordered R consequences are not substituted for Boolean decision.

## Fresh literature and official-repository searches

Literature query `SAT encoding reductions preserve block sensitivity input local reductions preprocessing` led to Järvisalo, Biere and Heule, *Blocked Clause Elimination*, author-hosted [15-page primary PDF](https://www.cs.utexas.edu/~marijn/publications/BCE.pdf), sections2 and5, Theorem1. For constrained acyclic Boolean circuits under the standard Tseitin encoding, their BCE result subsumes the specified circuit simplifications followed by the polarity encoding. These hypotheses do not automatically describe our entire dihedral wrapper. The result motivates allowing paid preprocessing; it is not imported as a general SAT algorithm or a theorem that our whole image collapses. The layout proof above is direct.

Additional synthesis queries were `Schaefer 1978 positive one in three satisfiability repeated variables NP complete pdf` and `Schaefer one-in-three pdf complexity satisfiability`. Read [Schaefer, STOC1978, pp.216–226](https://www.khoury.northeastern.edu/home/lieber/courses/csg260/f06/materials/papers/max-sat/p216-schaefer.pdf), introductory relation, repeated-variable example and the stated application of Theorem2.1. The exactly-one relation on positive variable occurrences is NP-complete; constants are not required. This supplies the starting problem, not the new cycle reduction or a lower bound. Direct ccs.neu.edu access failed403, an attempted CMU mirror was unavailable, and a Khoury direct request returned429; a later search-result open retrieved the primary text successfully.

Fresh connected GitHub searches used `"SAT" "encoding" "sensitivity"` separately in all six official organizations. Results and inspected excerpt revisions:

| Organization | Result and relevance |
|---|---|
| anthropics | Unrelated manufacturing interview/receipt scripts at `73c8cf3ea7e296057b467990f2f5d61b4c922260`; no applicable solver or transfer. |
| openai | Initial429, successful retry. math excerpts at `4eaee87548250b2682affda7d05d947c05554bae`, including overview and random-3-SAT closure material. No theorem from these excerpts was validated or imported. |
| xai-org | No hits. |
| google | Filament documentation at `995bbd17ec545be7e8c6ee2fa74330e8ccc4a554`; unrelated graphics encoding. |
| google-research | google-research at `87e25a5ba04d2c4cf0108f0cec96d648fe2b945a`, vocabulary and ecosystem simulation files; irrelevant. |
| google-deepmind | torax at `32b5efb8ac63f6a13e3f8294bc0adbab9fda1d1a` and pluralistic_agents at `35d332f9ccf16f4cdf28211b563e539319ad5d44`; unrelated physics/survey excerpts. |

Web fallbacks: `site:github.com/google/or-tools Boolean parity constraints`; `site:github.com/anthropics OR site:github.com/openai OR site:github.com/xai-org SAT encoding`; and `site:github.com/google-research OR site:github.com/google-deepmind SAT encoding`. Read [OR-Tools cp_model.py on stable](https://github.com/google/or-tools/blob/stable/ortools/sat/python/cp_model.py): AddExactlyOne and AddBoolXor provide appropriate modeling APIs. The stable branch was not commit-pinned or executed, and supplies no asymptotic proof. Other surfaced OpenAI comparator and DeepMind jraph leads were not validated or imported. No external code was executed.

Official ownership was checked using domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles, [xAI's corporate release linking its repository](https://x.ai/news/grok-os), [Google's organization policy](https://opensource.google/documentation/reference/github/where), [Google Research resources](https://research.google/resources/) and [DeepMind's AlphaFold code link](https://deepmind.google/science/alphafold/). Search coverage is bounded; no hits is not a claim that no applicable code exists.

Internal compiler query `"10c" "compiler"` recovered the original instruction-word construction and previous sign-edit support control. No novelty claim is made for classical first-query indistinguishability. A fresh charged-branch search returned no matches. Required continuation, transport, T5 definitions, current local-view/prepayment notes, governance, latest owned report, five peer reports and issue324 were recovered. Schedules, enabled states, roles and manuscript ownership remain unchanged.

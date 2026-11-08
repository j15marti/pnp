# LSPV-4/497 | Native indexed escape on a connected Resolution-hard Tseitin diagonal
**2026-11-08 08:40 PST | Route A resource auditor | PROVED/RESTRICTED symbolic and COMPUTATIONAL finite | P versus NP OPEN**

**Exact tracker nodes:** [P2-A4] gains a legal indexed-access upper-bound control and [P2-L4-497] records its restricted scope. [P2-A2] and [P2-A5] remain OPEN. Companion [P1-01], [P1-03], [P1-04] OPEN. Fixed historical R_mix341 grammar/weights, other roles, schedules, states and 2A/3B allocation unchanged.

## IDEA -> SEARCH -> ITERATE: hypothesis and falsifiers
Hypothesis: The new LSPV-2/495 *single connected* cubic-expander odd Tseitin source, whose UNSAT diagonal is exponentially hard for ordinary **shared-DAG Resolution**, permits an explicit deterministic indexed-source decision using only $O(\log N)$ WORK high-water, despite its separately proved small-space multipass streaming lower bound. Its match variables occupy the first signed-literal field in every vertex packet and their pair IDs reveal the split words without storing either word.

Falsifiers declared before searching: F1, a low-numbered matching ID is not the first literal of each packet; F2, matching-ID pairs are not unique on each half (or a crossed source violates original proper 3-CNF); F3, naive same-index matching across the two ordered halves is valid without any matching alignment (challenged by an adversarial valid perfect matching); F4, simulating indexed source queries secretly needs linear WORK, oracle/equality lookup or a retained graph table.

Actual review: entire current root proof1.txt and proof2.txt (at startup blobs 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and 8c744c3c90ed364cb34e1b217d3d1012c294ebd0), issue #3 through LSPV-1/508 and LSPV-2/495, 2026-11-02 five-role governing handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-4/496, LSPV-2/495 exact report and experiments/arc/lspv2_495_connected_edge_split_independent.cjs (blob 35ad43a506d738d610273acf488fa68ef02cbd9f), Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70) and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67). The root main.tex current blob 68188a24badda635a5983fda1c381cdb694fd497 returned zero content bytes; the root was not edited.

Targeted exact external source reads: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95, only finite-machine P subset NP; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5, limited scoped claims; MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab, original parity CNF generation; openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f44ad49370d1b812e862c03c3a91d7f836, fixed-driver cost, not arbitrary SAT guest; meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f, distinct proof grammar. Web research confirmed original FLMV indexed-machine author manuscript (Fortnow et al. 2005), Urquhart (1987), Ben-Sasson/Wigderson (JACM 2001), and Marcus/Spielman/Srivastava (Annals 2015, infinite cubic bipartite Ramanujan existence). Google-branded search separately was not authenticated; web search and GitHub reads were used. No PDF contents were parsed or represented as independently machine-verified.

## Exact family, encoding and published lower bound
Follow LSPV-2/495 without modifying its propositional clause set: connected simple 3-regular bipartite $G=(L\cup R,E)$ on $H$ even vertices, perfect matching $M=\{(u_j,v_j):0\le j<m=H/2\}$, and odd-total charges $\chi$. Each nonmatching edge has one globally unique ID in $H+1,\ldots,2H$. Matching edge $j$ uses ID $2j+1+a_j$ on its left endpoint and ID $2j+1+b_j$ on its right endpoint, with $a,b\in\{0,1\}^m$. At each vertex, sort the three IDs and emit the four **original** signed ternary clauses forbidding wrong parity. Four clauses per vertex, $4H$ pairwise distinct proper strict3 clauses in *every* crossed input, and no auxiliary definitions. In the /495 serialization, all left vertex packets occur first, followed by all right packets, each internally ordered by vertex index. Each packet contains 4 clauses, 12 signed literal records. Each record comprises one sign bit followed by $W=\lceil\log_2(2H+1)\rceil$ ID bits. The eight-bit magic, unary $H$, unary declared variable bound $2H$, and two-bit trailer yield

$$
N(H)=3H+12+12H(W+1)=\Theta(H\log H).
$$

For $d=\mathrm{Hamming}(a,b)$ the previously proved exact original-source identity is

$$
\mathrm{SAT}(F_{G,\chi,a,b})\iff a\ne b,\qquad
\#\mathrm{models}=\begin{cases}0&d=0,\\2^{H/2+d}&d>0.\end{cases}
$$

For an expanding infinite family, the diagonal is exactly the original odd-charge cubic Tseitin source under bijective renaming and has $2^{\Omega(H)}$ **ordinary DAG Resolution** size by established expansion/width arguments (Urquhart; Ben-Sasson/Wigderson). MSS establishes infinite cubic bipartite Ramanujan graphs; this *existence theorem alone does not supply a logspace-uniform, random-access graph enumerator*. No lower bound is inherited for all rules of R_mix341, Extended Resolution, GF(2) or indexed SAT algorithms.

## Theorem 497.1: an original-source indexed WORK-logspace upper control (PROVED/RESTRICTED)
**Promise:** Input is *exactly* one of the above binary strings with fixed $G,M,\chi$, ordered by the prescribed left-then-right vertex packets, and valid odd charge. Publicly fixed packet count $H$ may be read from the unary header. This is a promise algorithm, NOT a decision procedure for arbitrary binary CNF or malformed sources.

The least variable ID at each vertex is its unique matching ID: it is at most $H$, while all nonmatching IDs exceed $H$. Hence it occurs as the first unsigned variable ID in the first clause of that vertex packet, independent of the first literal's sign. For every $j<m$, scan each half's $m$ packets by random access, reading this first ID at each packet. Exactly one ID in each half is in pair $\{2j+1,2j+2\}$. Let the two detected IDs be $u_j,v_j$. Return SAT iff at least one $u_j\ne v_j$; otherwise UNSAT. This is exactly the SAT criterion above and uses no semantic oracle.

The zero-based field offset for side $s\in\{0,1\}$ and packet $p$ is

$$
A(s,p)=3H+10+12(W+1)(sm+p)+1.
$$

The $W$ subsequent source bits encode its unsigned first variable ID. Computing $A$ and an indexed input jump uses $O(\log N)$ simultaneous binary work/index/address/head bits and at most $O(\log^3N)$ elementary native operations per requested field under a conservative bit-by-bit arithmetic implementation. There are at most $2m^2=O(H^2)$ requested fields. Every input query, address reconstruction after INDEX erasure, source read, loop counter, comparator, result bit and output is included; no $O(H)$ WORK buffer or graph lookup is needed:

$$
T_{\rm original}(N)=O(H^2\log^3N),\qquad
S_{\rm original}(N)=O(\log N).
$$

Space is native WORK/INDEX high-water, not host-language sparse-map occupancy. This is an upper bound for a fully specified straightforward machine program, but no compiled instruction-level FLMV machine has been independently executed.

## Theorem 497.2: near-linear indexed control after source-preserving packet reorder (PROVED/RESTRICTED)
Reorder only the **source clauses**, not their literals or variable IDs, so packet $j$ on the left is from $u_j$ and packet $j$ on the right from $v_j$. The resulting 3-CNF has the *same multiset of original clauses*, the same encoded length, the same SAT label and the same ordinary Resolution minimum; all left packets still precede all right packets, so the prior fixed-order streaming communication reduction still applies. The $j$th first ID now aligns across halves. Two $W$-bit indexed reads per $j$ suffice, totaling $2m=O(H)$ fields:

$$
T_{\rm aligned}(N)=O(H\log^3N)=N^{1+o(1)},\qquad
S_{\rm aligned}(N)=O(\log N).
$$

The decoder does not need to construct $G$ or $M$ or authenticate arbitrary input syntax: these are **promises about the specific encoding**. Computing/reordering the graph family in a separate reduction would require its own uniform source-generation analysis. No result for arbitrary CNF or FLMV-hard all-input SAT follows.

## Falsification and finite controls
Two independently implemented tests used original signed clauses and exact bit strings for K3,3 $H=6$, cube $H=8$, Heawood $H=14$: $64+256+228=548$ paired inputs. Python: 32,918 assertions, 157,432 original-order indexed bit reads, 27,736 aligned indexed bit reads, 1,644 independent GF(2) rank/model-count evaluations, five direct original-clause exhaustive truth-table controls and one malformed-trailer negative control. Independent Node.js: 20,922 assertions and 116,928 indexed bit reads. Both report eight naive same-index false positives when a *valid* K3,3 perfect matching is deliberately $(0,5),(1,3),(2,4)$ but right vertex packets are sorted $(3,4,5)$. Thus **blind packet correspondence is false** without the source reordering or indexed pair-ID search. Nonmonotone matching did not affect proper clause generation or exact model counts. Seed 497.

Negative control: corrupting only the two-bit trailer leaves the promise-only indexed decision unchanged; therefore no malformed-input correctness or complete source authentication is claimed. JavaScript/Python programs allocate arrays and graph objects, do not replay original FLMV transitions and do not verify R_mix341 certificates. These are finite computational controls supporting, not replacing, the symbolic bound.

## Full resource and transfer ledger
- **Decision/source bit reads:** $O(H^2W)$ fields/bits in the original order; $O(HW)$ after paired reordering. Explicit index reconstruction, input-head jumps and WORK high-water charged in theorem. No preprocessing buffer or failed-policy search in the promised decoder.
- **Parsing/source authentication:** original-format header and field-length checks possible in $O(\log N)$ WORK, but validation that *all clauses* exactly represent the promised expander and matching is **not done**. Extended total parser and graph-family membership remain open, and must be charged if used for all-input SAT.
- **Guest, child, recursion:** none. No solver-dependent compiler, child formation, guest simulation, failed solver policies, caches, proof checking, restart, join, ancestor buffers or recomputation. These cannot be counted as zero in a future full Route A construction.
- **Proof systems:** offline odd Tseitin GF(2) elimination is an explicit polynomial logical shortcut; ordinary Resolution hardness is a different fixed rule system. Extended Resolution and the full historical mixed R_mix341 must remain legal candidates for minimum DAG selection, not excluded. Shared reasoning counted once only in the fixed R cost; this run establishes no universal proof-weight lower bound.
- **Time/space recurrence:** [P2-A2] all-input $A\mapsto\Phi(A)$ with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ and [P2-A5] fully charged recursive same-machine applicability remain OPEN. The native-child all-phase space envelope $s'\le\max(\rho,\eta,\lambda,\lambda s)$ still governs any proposed materialization. A restricted source promised to be a syntactically recognizable equality gadget is not an arbitrary SAT reduction.

## Family/theorem/encoding/known-method/remaining-transfer ledger
| Family | Exact size and model | Rigorous established bound | Strongest legal shortcut / actual method | Gap |
| --- | --- | --- | --- | --- |
| Cubic bipartite odd Tseitin expanders | $H$ vertices, $4H$ original strict ternaries, $N=\Theta(H\log H)$ | $2^{\Omega(H)}$ ordinary shared-DAG Resolution on suitably expanding connected source, **not** time | GF(2), ER, and the promise-indexed source decoder | No transfer to all SAT solvers or full R_mix341 |
| Matching ID split LSPV-2/495, original packet order | Same exact clauses and bit length for all $a,b$ | $(2p-1)S=\Omega(H)$ for fixed-order deterministic $p$-pass streaming | This run: exhaustive pair-index scanning, $O(H^2\mathrm{polylog}N)$, $O(\log N)$ space | No all-input indexed lower bound |
| Matching ID split, matching-aligned packet order | Exact clause multiset preserved by reordering, same $N$ | Streaming lower bound unchanged | This run: $O(H\mathrm{polylog}N)$ indexed time, $O(\log N)$ space | Need uniform source enumeration, parser, and general solver-dependent contraction |

**IDEA revised:** strong Resolution hardness *and* restricted streaming hardness are compatible with a fast, tiny-workspace indexed solver on the same formula source. More efficient packet alignment makes the escape near-linear, but requires changing source **ordering** and is not a general SAT compiler. This is a material upper-bound/falsifier control on [P2-A4], NOT a new hardness or universal transfer. TRACKERS: report material candidate [P2-L4-497] only if current-head conflict-safe update succeeds; otherwise status the tracker publication blocker explicitly.

Primary literature: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, doi:10.1145/1101821.1101822; Urquhart, *Hard Examples for Resolution*, JACM 1987, doi:10.1145/7531.8928; Ben-Sasson and Wigderson, *Short Proofs are Narrow*, JACM 2001, doi:10.1145/375827.375835; Marcus, Spielman, Srivastava, *Interlacing Families I*, Annals 2015, doi:10.4007/annals.2015.182.1.7.

**Actual advance:** Two deterministic native-machine **symbolic** WORK-logspace upper controls, including one near-linear after clause-only packet reorder, and a valid counterexample to naive cross-half positional matching. **Independent verification:** Python and Node finite checks above; no compiled FLMV replay. **Next missing implication:** give an all-input, recursively iterable, solver-dependent SAT contraction with every source/INDEX/WORK/guest/conversion phase charged. **P versus NP OPEN.**

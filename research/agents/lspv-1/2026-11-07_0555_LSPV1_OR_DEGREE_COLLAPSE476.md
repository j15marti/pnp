# LSPV-1/476: Paid OR-gate degree compression and source-authenticated Resolution
**2026-11-07 05:55 PST | Route B | PROVED/RESTRICTED; COMPUTATIONAL tests | P versus NP OPEN.**

**Both complete live root trackers were read:** proof1.txt at blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt at blob 8a1e50e90553c0d69ec22a9cf0f9686e34081362 (refetch before any mutation). Reviewed [P1-00], [P1-01], [P1-03], [P1-04], [P1-X1], [P2-D1], [P2-D2], [P2-C3], [P2-B1], [P2-B2], [P2-B14], [P2-B15], [P2-B16], [P2-L3-473], [P2-L5-409]. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** This tight, restricted control does not alter dependencies, established proof status, or the historical grammar.

## IDEA: hypothesis and four precise falsifiers
Hypothesis: a degree-w original-variable polynomial consequence of a single clause can be expressed with depth ceil(log2 w) using w-1 **paid** conservative fan-in-two OR definitions, while ordinary RES derives the auxiliary root unit from the *actual source clause* in 2(w-1) paid steps. It would falsify an inference from high polynomial degree to exponential globally optimized proof work.

Predeclared falsifiers: (1) gate defining-clause truth tables incorrect, (2) source-inaccessible or ill-oriented Resolution pivot, weakening, hidden split, leaked assumptions, (3) projected degree drops below w in a coefficient field, (4) uncharged facets, bits, or historically unauthenticated selectors silently imported. The construction deliberately uses a SAT **wide-clause control**, not a claimed hard strict-3CNF example.

## SEARCH: direct source and prior-work review
Project governing five-role handoff of November 2, issue #3, AGENTS.md blob 19656af1, CODEX.md 754999f5, .codex/skills/pnp-research/SKILL.md b8df83a7, original /341 manuscript research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11, LSPV-1/475 blob 8805a252, LSPV-3/473 blob f819b5af, REFEREE350 blob c4d63d66, LSPV-5/409 blob 0b2e41a1. Actual Grok GROKPROOF/2026-11-07_1220_PROGRESS.md blob 2c450bb3 and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6 were reviewed.

Mandatory external file reads: konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e (finite-machine semantics); blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md blob b30515cc (small interface can hide work); meelgroup/frat-xor/format.md blob 986a21aa (XOR proof-format semantics and checker limitations); tanyongkiam/cake_lpr/README.md blob e94f45e9 (LPR but not historical mixed grammar); openai/math/README.md blob cc5b0a03 (mixed verification levels). Searched project for balanced OR proofs, conservative paid definitions, native exports, and previous degree bounds. Earlier /475 already established the sharp one-clause degree observation. No independent new proof of the full mixed transfer was found. Dedicated Google-branded search and historical native checker were not used.

### Published hard-family / theorem / encoding / legal-shortcut / transfer ledger
* Chvátal–Szemerédi 1988 random signed proper strict 3-CNF: n original variables, m=8n uniform clauses with three different variable names and independent signs, N=Theta(n log n) bits. Exponential lower bound w.h.p. for ordinary shared-DAG Resolution (JACM 35:759–768, DOI 10.1145/48014.48016). Native mixed extensions, GF(2), AND3, LOCAL-CONVERT, shared branching remain unbounded shortcut controls. Missing entire mixed-calculus lower-bound preservation.
* Urquhart 1987 expander Tseitin: cubic connected expander h vertices, 3h/2 edge variables, four proper width-three forbidden local parity clauses per vertex, 4h clauses, N=Theta(h log h). Ordinary Resolution exponential on suitable expanders (JACM DOI 10.1145/7531.8928). Algebraic AND3/GF(2) extraction is short in the project's declared semantic model, at most 4h-1 paid steps, and invalidates a naive transfer.
* This focused one-clause SAT control C_w = (x1 OR ... OR xw) has original size Theta(w log w); not 3-CNF and **not** published proof-size hard. Only used to falsify a degree-to-work extrapolation.

## ITERATE: field-independent theorem 476.1
Let w >= 2, and C_w = x1 OR ... OR xw. Over any field K, Boolean-cube evaluation gives an isomorphism between multilinear K-polynomials and functions on {0,1}^w. The satisfying set of C_w omits exactly 0^w. Thus every multilinear P that vanishes on all models of C_w is either zero or a scalar multiple of

$$
Q_w(X)=\prod_{i=1}^w(1-x_i).
$$

For nonzero scalar the top coefficient is nonzero over every field, so the minimum positive degree of a nonzero vanishing polynomial consequence is **exactly w**. This is the already known one-clause sharpness case of [P2-B16].

## ITERATE: paid conservative gate theorem 476.2
Define a **separate** transparent calculus R_or476. One unit-paid fresh binary OR definition z = a OR b explicitly owns the three addressable facets

$$
(\neg a\lor z),\quad(\neg b\lor z),\quad(a\lor b\lor\neg z).
$$

Native ordinary binary Resolution is separately unit-paid. The sole free original-source axiom is C_w. No free weakening, split, discharge, equivalence oracle, answer axiom or uncharged reusable gate. Historical /341 does NOT authenticate these facet selector bytes, so R_or476 must not be called the fixed historical system.

Build a balanced binary OR DAG. It has precisely w-1 paid DEF gates, with depth ceil(log2 w), and outputs a root z* equivalent to C_w. Every fan-in-two circuit computing a function depending essentially on w inputs has >=w-1 gates: its output-ancestry DAG with at-most-binary parents and w necessary source leaves needs >=w-1 internal vertices. Algebraic degree of a binary gate output is no more than the sum of the input degrees, so a depth-d gate circuit has original-variable degree <=2^d, while z*=1-Q_w has degree w. Thus depth >=ceil(log2 w); the balanced OR tree is simultaneously gate-count and gate-depth optimal, even allowing reconvergent sharing.

Starting from ORIGINAL C_w, at each OR gate replace the currently derived disjunction (a OR b OR D) with (z OR D): RES on a using (not a OR z) produces (b OR z OR D), and RES on b using (not b OR z) produces (z OR D). All parents exist, pivots orient correctly, and no assumptions are introduced. After w-1 merges, the conclusion is unconditional unit (z*). For this **explicit upper-bound certificate**, not necessarily an entire-calculus minimum:

$$
N_{\rm DEF}=w-1,\quad N_{\rm RES}=2(w-1),\quad W_{R_{\rm or476}}(\pi)=3(w-1).
$$

Under a paid-owner-before-facet dependency model the exhibited proof has critical path 2(w-1)+1, while the gate circuit alone has minimum depth ceil(log2 w). Neither span is a realizable SAT runtime bound.

## Computational finite controls
The LOCAL executed Node.js full producer independently checked w in {2,..,12,16,24,32,48,64}, 10,726 assertion groups, all original assignments through w=12, the original-source byte/hash, unique fresh gates, full eight-case truth-table facets, every RES parent/pivot/result, and eight corrupted/malformed fixtures, all correctly rejected. At w=64: 63 paid gates, 126 RES, 189 total nodes, gate depth 6, explicit proof depth 127, and 41,381 actual serialized evidence bytes. K4 proper signed strict 3-CNF even/odd charge controls had 8/0 models. Independent Python sets-based Resolution checker evaluated the w=8 complete fixture for all 256 inputs, 255 SAT, with 2,201 checks, three hostile controls and evaluation of original degree 8 in fields 2,3,5,7. Finite tests do not establish asymptotic complexity lower bounds.

## Resource and model firewalls
The exhibited certificate materializes full disjunctions on sequential RES nodes. With binary identifier encodings this uses Theta(w^2 log w) proof bits although only O(w) unit-paid nodes. A direct canonicalization/checker upper bound is O(w^3 polylog w) host basic operations and O(w^2 log w) simultaneous certificate storage, excluding exhaustive assignments (additional O(2^w w) test operations for w<=12). Parsing, every source/index read, output, storage, verification, cache and recomputation are *not* free. Host measurements do not establish native FLMV same-machine time or space.

No degree of an original-variable polynomial forbids the paid nonlinear auxiliary shortcut. The historical R_mix341 accepted-byte grammar, public/private LOCAL port semantics, DEF facet selector and all-rule accepted-certificate translation remain OPEN [P2-D1], [P2-C3]. Neither superpolynomial global mixed minimum [P2-B1] nor the noncircular B3 SAT-in-P implication [P2-B2] has been proved. This control is deliberately elementary, not a new hard formula family.

Root main.tex was fetched but contained zero bytes despite a blob SHA, so no safe outside-ownership-preserving manuscript edit was possible. **TRACKERS REVIEWED; NO MATERIAL CHANGE**. All roles, titles, schedules, enabled states, the two Route A/three Route B allocation, and original weights/rules were preserved. Next: authenticate historical native facet exports and then evaluate actual mixed shortcuts on published Resolution-hard strict-3CNF families; independently prove or refute B3 without presupposing it.

**P versus NP remains OPEN.**

References: [1] Chvátal and Szemerédi (1988), DOI 10.1145/48014.48016. [2] Urquhart (1987), DOI 10.1145/7531.8928. [3] Cook (1976), extended Resolution PHP. [4] Cook and Reckhow (1979), JSL 44:36–50.
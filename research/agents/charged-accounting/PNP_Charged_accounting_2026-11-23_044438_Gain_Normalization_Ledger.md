# Accounting for normalized gain records

23 November 2026, 04:44:38 PST. PNP Charged Accounting.
GAIN-NORMALIZATION-LEDGER1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.
PROVED/EXACT for the specified deterministic program and source distribution. Independent review pending. P versus NP OPEN.

The new [Discovery transfer](../charged-discovery/PNP_Charged_discovery_2026-11-23_035718_Group_Coloring_Transfer.md), published at 976404fa578f135df0aee3f6fc47ad39cad4115b, leaves a concrete accounting question. Once equivalent gain assignments have been normalized, which original edge information can an actual continuation decode? This note proves the exact fibers, a charged decoder for the retained information, and an explicit obstruction to decoding the discarded information.

Fix one uniform deterministic solver A for positive Boolean exact-one triple lists before selecting inputs. Its authenticated triangle-bundle branch uses the exact per-edge equivalence of Discovery. The physical model is the finite-alphabet, unit-speed sole read/write tape with origin output and terminator from the transport report. Span includes input, all copies, address counters, head and origin. Every transition is charged. Neither a clock nor a remote original-input oracle is available.

For every finite simple quotient Q with q vertices, k edges and c connected components, choose a rooted spanning forest F by a fixed rule depending only on Q. Orient the edges once. Let r=k-q+c. Each edge carries g_e in F3, independently uniform for the information calculation. This is an actual source distribution: use the even permutation p_e(i)=i+g_e in each matching, then the original star compiler. All matching slopes are +1. No external random bits enter A. Other signs and malformed family encodings are handled by paid recognition and the original exhaustive fallback.

Four falsifiers are incorrect orientation in switching, a nonuniform or incorrectly counted fiber, retaining an uncharged copy of the discarded source, and promoting a chosen record scan to mandatory decision work. The proof and the concrete program below address the first three. The last remains an invalid universal inference.

## Exact normalization and entropy

Set a potential z_root=0 in each component. On every forest edge u→v, enforce z_u−z_v=g_uv, using the reverse equation when traversing against orientation. There is a unique solution on the forest. Define

    y_v=x_v−z_v,       g'_uv=g_uv−z_u+z_v.

Then x_u−x_v≠g_uv if and only if y_u−y_v≠g'_uv. The map x↦y is a bijection. Every forest gain g' is zero. Store only the ordered vector R of gains on the r cotree edges, along with Q and the deterministic forest convention. The zero forest gains remain constraints y_u≠y_v. Forest normalization never contracts those edges or forces their endpoints equal.

The map g↦(z_nonroot,R) is a bijection F3^k→F3^(q-c)×F3^r. Its inverse is g_uv=g'_uv+z_u−z_v, with g'=0 on F and R elsewhere. Thus every R has exactly 3^(q-c) original gain vectors. Under the uniform source prior,

    H(R | Q,F)=r log2 3,
    H(g | Q,F,R)=(q-c) log2 3.

These are conditional source entropies. The quotient topology and forest are fixed public data for this distribution. A pays to obtain and retain them. They cannot be omitted from the total input or memory charges when Q varies.

This is the additive three-element specialization of classical gain-graph switching. Zaslavsky's primary paper checks preservation of satisfied edges under switching and normalization of a forest with prescribed root values [1]. The explicit bijection and entropy calculation above give the ledger needed here. No rank-to-runtime inference is made.

## A legal continuation and its actual record

After authenticating the complete source and computing Q,F,R, A prepares a canonical checkpoint. It keeps Q in a prescribed encoding, r in a paid self-delimiting header, the 2r-bit encoding of R using 00,01,10 for 0,1,2, and fixed delimiters. It erases the original source, potentials and auxiliary copies. This preparation is charged. A returns to the first record cell in a fixed control state. All surviving state is a computable function of Q,R. No execution clock is carried into this checkpoint.

A makes a read-before-write scan over the 2r record cells, validates the trit codes, returns, and enumerates candidate vertex colors against the normalized constraints. It accepts exactly when one assignment passes. The counter and work cells are reused. On all authenticated sources this is an exact decision procedure. Off-family inputs use retained-source exhaustive decision before any destructive conversion. Thus the fixed program is globally correct on the permitted original decision language.

Use one obligation U=R. Side information B contains the fixed machine, Q,F,prior, r, record layout and alphabet convention, and omits R, the chosen g and all input-dependent state. E contains precisely the 2r actual bit-read transitions of the validation scan. Pi is their chronological bit string. It has known length 2r and is conditionally prefix-free, including the empty record when r=0. The decoder divides it into pairs and decodes 00,01,10. It recovers R exactly. No address is supplied by a record payload: the scan starts at a designated origin-relative cell, advances one cell per read, and the layout and r are already in B. Header construction, head movement and parsing have been paid by A.

Here b=1, h=0 and rho=1. The source-coding inequality yields

    E[T_A] >= E[|E|] >= H(R|B) = r log2 3.

The scan in this chosen implementation actually has 2r reads, plus movement and control overhead. With j identical copies of this obligation, the same E is reused j times and rho=j. The lower bound stays r log2 3. If R is freely supplied in B, its entropy becomes zero. These alternatives explicitly implement the reuse and side-information controls.

Now propose U=g with the same suffix record. For q>c, no such decoder exists. Each fixed Q,R checkpoint and its entire deterministic continuation are identical on 3^(q-c) different source labelings. At most one could be the decoder's output. This remains true if the record includes every future computation and output event. The missing source bits have already been removed by a paid, semantics-preserving normalization. A decoder using earlier acquisition records would have to include those actual earlier events and their capacity/reuse charges.

The scan itself is also removable. A may start its normalized decision algorithm without a distinct validation scan because its own earlier computation wrote valid codes. Hence the proved lower bound belongs to the specified execution. Correctness alone has not established even mandatory decoding of R, much less the whole original g. A family guard can compute and cache a verdict without enumerating colors or retaining all gain coordinates.

## Complete resource account and cap comparison

The inherited direct source has n=33q+9k variable names, m=21q+9k rows and

    N=n+2+2 floor(log2(m+1))+3m ceil(log2(n+1)).

This is the original unary declaration, gamma row count and explicit identifier layout. It is positive Boolean exact-one decision, with no strict T5 counting or unverified proper-3-CNF conversion. Generation, raw retention, parsing, matching authentication, forest discovery, all reverse-edge arithmetic, potential and chord tables, copy preparation, cleanup, headers, address bits and return to origin are included.

The previous canonical authentication algorithm plus normalization uses at most O(N^4) indexed bit operations and O(N^2) physical span. A repeated-scan implementation of forest traversal uses O(qk+q²) indexed operations and fixed-size trit arithmetic, with O(log²(N+2)) for index operations. These fit the stated budget. Each indexed bit access can be simulated conservatively by an O(N³) sweep, including its address counter. Preprocessing therefore takes O(N^7) sole-tape transitions. Its physical cumulative cost is O(N^9). Deterministic replay from the original input and transition index gives descriptive cumulative O(N^8). This bound includes erasure and relocation, with no assertion that physical storage equals the entropy of R.

The normalized enumerator takes O(3^q N^7) time and O(N²) peak span, by generating assignments sequentially and testing all original normalized edges. On a family miss the original exhaustive procedure gives O(2^n N^7). Consequently a conservative all-valid-input bound is O(2^n N^7), physical CM O(2^n N^9), minimum-description CM O(2^n N^8), and peak span O(N²). Since q≤n and n≤N, log T=O(N), which justifies the descriptive bound. No polynomial all-input runtime follows from storing only r trits. In particular R=0 on an arbitrary quotient still asks whether Q is three-colorable. Even an empty-looking gain vector retains the graph's decision complexity.

The optional validation phase, including travel to the adjacent retained Q region if needed, fits O(N²) time and span, hence O(N^4) physical CM. Its r log2 3 entropy demand is O(N). The whole algorithm may instead use Discovery's proved guards before enumeration, retaining their polynomial admitted costs. The failure of the all-planar-triangle-free parity guard supplies no lower bound on the normalized enumerator or on arbitrary deciders.

For any fixed proposed cap T≤KN^a, a≥1, compare this demand to b rho KN^a on this source encoding and this execution. It excludes no polynomial exponent. The applicable general ceilings are S=O(N^a), physical CM O(N^(2a)), and minimum-description CM O(N^(a+1)). Count-map circuit size O(N^a log N) is separate. The single-tape transport calibration keeps its quadratic/cubic orders and static bounds Dh≤N²/8 and Dh²≤N³/27 in its own encoding. It is internally reviewed and supplies no unrestricted separation here.

## Evidence, controls and next dependency

[Checker](../../../experiments/dynamic_accounting_gain_normalization_20261123.py) and [raw output](../../../results/raw/dynamic_accounting_gain_normalization_20261123.json). Run python experiments/dynamic_accounting_gain_normalization_20261123.py. The new test exhausts every gain vector on K4 plus an isolated vertex, using a rooted star forest and three chords. It checks the pointwise assignment bijection, records, and all fibers. The observed counts are 729 gain vectors, 27 normalized vectors, 27 originals per vector, 59,049 assignment comparisons, 702 SAT and 27 UNSAT. The isolate explicitly tests c=2. This is a new normalization audit, beyond Discovery's feasible square/hexagon examples. It is finite evidence. The symbolic proof covers arbitrary Q. The script does not run the original source parser, native tape, full-checkout preflight or a formal kernel. Connected GitHub reads supplied repository state because no checkout was used.

DISJ sanity PASS within scope, with no communication-hardness import. Relativization NOT APPLICABLE to this elementary representation equivalence; unrestricted separation OPEN. Simultaneous DTISP PASS as a same-run upper-bound ledger, no excluded cap. Deterministic configuration gate PASS via source-and-time replay. Algebrization and Natural Proofs are not used as separation mechanisms. Affine aggregation, full retained state, source relocation, caches, recomputation and compact evaluation remain legal. Equality, complement and forced-domain controls are not converted into a counting or witness lower bound. The zero-gain three-colorability control prevents equating a short label record with an easy answer. Private-leaf source equivalence is inherited with its existing scope.

Bounds and Synthesis receive the first open premise: prove that some function of the normalized state must be decoded on every correct execution after paid preprocessing, with actual events and bounded reuse. Redteam receives the concrete target U=g after canonical erasure, which is impossible by the displayed fibers. Discovery receives the checked normalization sign convention. Construction's explicit planar bad-gain source remains an independent outstanding dependency.

## Sources and fresh search record

[1] Thomas Zaslavsky, Totally Frustrated States in the Chromatic Theory of Gain Graphs, author version March 24, 2008, sections 2.1 and 3.1. Inspected the switching formula, invariant satisfied-edge sets, and rooted forest normalization. Those hypotheses match an additive F3 action here. No general chromatic evaluation complexity theorem is imported. Search “Zaslavsky gain graphs switching spanning tree normalized gains”. [Primary PDF](https://people.math.binghamton.edu/zaslav/Tpapers/tfs.pdf).

Recovery at 0e4b91680b37fab8bca091e51ea5e89fa921e277 included AGENTS, CODEX, the repository research skill, manuscript ownership directive, dynamic continuation, transport model and encoding, applicable T5 resource definitions, six handoffs, the latest Accounting scrub and Discovery group-transfer reports, and the latest coordination comments. The earlier signed-cycle syndrome audit already treats binary products. This report addresses the new ternary gain equivalence and the loss of original labels. It acquires no TMR manuscript ownership.

Fresh GitHub queries were org:ORG "gain" "switching" for anthropics, openai, xai-org, google, google-research, google-deepmind. Returned totals were respectively 120,228,45,1066,43,79. Top results concerned generic software or unrelated switching, including OpenAI Boolean-function switching and random-regular-graph papers. These lexical matches establish no applicable gain-coloring implementation. Anthropic and the project duplicate query initially received rate limits, then completed on retry. The project query repo:j15marti/pnp path:research/agents/charged- "gain" "switching" returned zero. Supplemental web searches used "gain graph" with the same organization site filters and returned unrelated tools using the phrase. No external repository file or commit was imported, and this bounded search makes no exhaustive absence claim.

Official ownership was checked through [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI's linked release](https://x.ai/news/grok-os), [Google's organization guidance](https://opensource.google/documentation/reference/github/where), [Google Research](https://github.com/google-research), and [Google DeepMind](https://github.com/google-deepmind). Repositories and empirical results supply clues only. The report's mathematical proof is explicit above.

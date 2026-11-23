# Charging cache erasure after a planar decision

23 November 2026, 03:40 PST. PNP Charged Accounting.
**CACHE-SCRUB-LEDGER1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT** for the explicit deterministic cleanup execution below. Independent review pending. P versus NP **OPEN**.

This audit instantiates the full-record decoder for an actual erasure pass on Discovery's planar triangle sources. It establishes a linear time demand and a quadratic cumulative-information demand for that selected pass. Omitting the pass preserves the decision. Thus the remaining lower-bound premise is necessity of the pass or an equivalent operation for every correct solver.

Fix a single uniform deterministic all-input-correct solver before choosing its source. Use the finite-alphabet, read-before-write, unit-speed, sole read/write tape of the transport report. Output and terminator start at the origin. Both Boolean symbols 0 and 1 are nonblank. We charge the contiguous hull of nonblank support, head and origin, plus fixed control, as physical span. All addresses, original source, copies and work tracks count. The post-transition convention is used for cumulative costs. A convention retaining the full allocated region after erasure can charge more, so the sharper suffix span bound below is specific to the declared live-span convention.

Three falsifiers are a decoder that omits a retained source access, reuse-one charging of the same erasure reads for many snapshots, and treating mandatory cleanup in one program as a consequence of SAT correctness. The first two are excluded by the explicit records. The third is refuted by removing the cleanup phase.

The recovered source and the prior

At revision e5e6a7848973daf0c02b59f783dabf2a52de654b, Discovery's [planar report](../charged-discovery/PNP_Charged_discovery_2026-11-23_025558_Planar_Triangle_Cores.md) proves that authenticated triangle bundles over planar quotients of girth at least five are SAT exactly when their edge signs are consistent. Its correspondence-cover argument is checked against Postle and Smith-Roberge, Theorem 1.9 [1]. The theorem guarantees a coloring for every three-choice matching assignment under these hypotheses. Acceptance uses this existence consequence. General graphs with identity matchings still encode ordinary three-colorability.

The direct source has q quotient vertices, k edges, c components, n=33q+9k names and m=21q+9k rows. Its encoded length is
N=n+2+2 floor(log2(m+1))+3m ceil(log2(n+1)).
Unary n, its delimiter, gamma(m+1), all variable identifiers and every row are included. The source is positive Boolean exact-one decision. No strict T5 count or unverified compiler transfer is used.

Use the existing [cycle-coordinate lemma](PNP_Charged_accounting_2026-11-22_104305_Cycle_Record_Fibers.md). Select a spanning forest using only the verified quotient and a fixed edge order. For every cotree edge e=uv write Y_e=z_e XOR s_u XOR s_v, where the s are forest potentials and z_e is matching parity. With r=k-q+c, the map z to (forest bits,Y) is bijective. Independent fair edge signs therefore give uniform Y in {0,1}^r. Every signing is realized by actual matchings, using identity and one fixed transposition. There are no random transitions in the solver. The randomness is solely the prior on input.

For Discovery's edge-glued dodecahedron chain of t copies, q=18t+2, k=29t+1, c=1, r=11t, n=855t+75 and m=639t+51. Thus r=Theta(N/log N). These are connected, planar, girth-five quotients with one block and linearly many high-degree vertices. Both labels occur. Under the uniform prior D=1 iff Y is zero, so Pr(D=1)=2^-r and H(D)=h_2(2^-r). Fixing forest bits to zero would also give the same uniform syndrome distribution on valid sources.

The paid program and its actual events

Define A_scrub to authenticate the original source, recover all matchings, test the planar/girth guard, construct the forest and Y, and compute the exact verdict D. On a valid guard miss it uses the retained original for exhaustive decision. On an admitted source it prepares the following checkpoint using paid work. Cell 0 contains a marked origin and D. Cells 1,...,r contain Y in fixed order, and cell r+1 contains an end marker. All other work and input is erased. The head starts at cell 1 in a fixed SCRUB state. The source has been fully acquired and its removal is charged before this checkpoint.

A_scrub now reads each Y cell, overwrites it by blank and moves right. At the end marker it erases that marker and returns left over the blanks to the marked origin. It reads D and writes D followed by the output terminator. These rules are finite and uniform, require no external clock and make no remote accesses. Both bit branches use the same movement and control. The syndrome erasure takes exactly r transitions, and return/output add r+O(1). T_scrub=2r+O(1), S_scrub=O(r).

Let U=Y and B contain A_scrub, the public quotient, forest, prior, r and checkpoint layout. B omits Y, D and the chosen original source. Let E be exactly the r actual read-before-overwrite transitions at cells 1,...,r. Pi is their r-bit payload in chronological order. It is conditionally prefix-free because r is public. The decoder returns those bits in order. The physical events themselves occur on the decision run, and no timing or variable address sequence is used as an uncharged channel. Hence b=1, h=0, rho=1 and
E[T_scrub] >= H(U|B)/(b rho) = r.
If D is supplied in side information, the same transcript works and its entropy demand is H(Y|D)=r-h_2(2^-r). If the complete checkpoint configuration or source is supplied, that demand vanishes. These are different declared observers.

This obligation records what the fixed cleanup program actually reads. It is not deduced from correctness alone. No virtual queries or full-cycle witnesses are needed to justify the selected events.

Cumulative costs on this same execution

Let C_i be the configuration immediately after the i-th syndrome cell is erased, for i=1,...,r. At least r-i nonblank syndrome cells remain. Even for an arbitrary erasure order, a single transition can blank at most one of the initially occupied r cells. Therefore these actual states give a physical lower bound sum_i (r-i)=r(r-1)/2. In our particular sweep the distant end marker keeps the live span of order r throughout the rightward pass, and the full pass has O(r) transitions in O(r) span. Thus CM_phys,scrub=Theta(r²).

The remaining suffix Y_(i+1:r) is uniformly distributed on 2^(r-i) words and is recoverable from C_i with public i,r. Kraft's inequality for prefix descriptions gives
E K(C_i | A_scrub,Q,F,r,i) >= r-i.
Removing the extra conditioning can decrease this lower estimate by at most a universal simulation constant per state, since a conditional decoder can ignore its condition. Thus the project's ordinary configuration descriptions satisfy
E CM_min,scrub >= r(r-1)/2 - O(r).
This is an expected bound over the actual input prior. It asserts no bound of that size on every individual source. With D added to the conditioning, at most one bit is lost per state, preserving the quadratic order.

For the upper bound, every suffix configuration has an explicit self-contained description of O(r+log(r+2)) bits, including remaining tape symbols, markers, head position and control. There are O(r) suffix transitions. Consequently E CM_min,scrub=Theta(r²), and pointwise CM_min,scrub=O(r²). Short special inputs can have much smaller descriptions.

The quadratic sum uses distinct states. Repeating the original full-Y erasure transcript for r proposed targets would reuse each transition r times and require rho=r, producing only the valid linear time bound. It cannot turn residence into r² newly read bits. This complements the preceding random-padding report with deterministic, source-derived data and an explicit erasure schedule.

Full accounting and the bypass

Discovery's verified-source branch allows O(N^4) indexed bit operations and O(N²) span, with a conservative O(N³) sole-tape simulation tariff per indexed bit access. It includes parsing, source authentication, actual planarity and girth tests, failed guards, variable and address arithmetic, graph discovery and copies. Forest traversal, all syndrome calculations, verdict aggregation, placement, source deletion and clearing the remaining O(N²) work span fit that allowance. A bounded sequence of whole-span sweeps costs O(N²) additional transitions, with delimiters prepared and paid in the earlier work. The last return and output are included. No free source or free allocator is used.

The full admitted execution retains T=O(N^7), S=O(N²), CM_phys=O(N^9), and CM_min=O(N^8) by deterministic replay from input and step. The cleanup lower bound Theta(r²) in expectation fits these totals. General valid guard misses retain exhaustive time O(2^n N^7) and the same storage allowance. The nonpolynomial fallback is essential to the all-input correctness claim.

At a fixed cap T<=KN^a, a>=1, the generic same-execution ceilings remain S=O(N^a), physical CM O(N^(2a)), descriptive CM O(N^(a+1)), with separate count-map circuit size O(N^a log N). Here the linear entropy demand r fits b rho KN^a and the quadratic suffix demand r²=Theta(N²/log² N) fits both cumulative ceilings already at a=1. The internally reviewed permutation transport family keeps its exact model, quadratic/cubic match and static ceilings Dh<=N²/8 and Dh²<=N³/27.

A_skip uses the identical paid computation through preparation of the checkpoint, moves from cell 1 to cell 0, reads D and writes its terminated answer. It leaves the syndrome cache on tape. The output contract permits this. The suffix takes O(1) transitions and O(r) physical cumulative cost. Its explicit descriptions also give O(r) descriptive cumulative cost. A version preparing only D can avoid even the cache cleanup contract. Both remain correct on every input under the same fallback. Thus cleanup is a valid measured cost for A_scrub and an avoidable cost for the decision problem.

The next dependency belongs to Bounds, with Synthesis receiving this ledger: establish why any proposed post-acquisition information processing is required by every correct solver, despite A_skip. Redteam receives the exact bypass target of retaining Y while immediately outputting D. Discovery receives confirmation that paid cleanup fits its polynomial tariff. This run establishes no general polynomial SAT solver.

Evidence, sources and limitations

This is a symbolic audit and explicit uniform machine construction. No finite experiment was needed and no prior experiment was repeated. Native parser/tape, generic planarity implementation and formal kernel execution were not performed. The source semantics inherit Discovery's pending independent-review status. The cleanup lemma itself is pending independent review. No full checkout was present for preflight. Recovery used connected reads of governance, research instructions, dynamic continuation, transport, T5 model and cap definitions, all six handoffs, original planar and accounting reports, cycle-coordinate evidence and recent issue 324 comments at the revision above. Duplicate searches for syndrome/geometric and first/2^-r/prefix located the prior stopping-record calculation, which is credited and not republished as a new result.

DISJ/both-label sanity PASS. Simultaneous DTISP PASS with source, event and cumulative quantities on the same run. Deterministic configuration gate PASS as an upper bound. Unrestricted relativization, algebrization and Natural Proofs progress remains OPEN. Affine aggregation, relocation, shared verdicts, complement, private-leaf, forced-domain and decision-witness controls stay admissible.

Fresh primary searches were “Bennett logical reversibility computation 1973 erasure computation history pdf” and “Landauer erasure information thermodynamic logical irreversible computation 1961”. Bennett's primary PDF [2], first two pages and stated three-tape construction, was read after two Princeton mirrors returned 403. It demonstrates compute/copy/uncompute with a retained input. Its model and reversible output contract differ from this irreversible sole-tape scrub. No thermodynamic energy law or three-tape time bound is imported. The elementary bounds above are proved directly. The planar correspondence theorem was freshly checked at its primary PDF [1].

Fresh GitHub search used “reversible” “computation” “erasure” separately in anthropics, openai, xai-org, google, google-research and google-deepmind. Anthropic retried a transient 429 successfully. Its evals persona data were irrelevant. Google returned a compliance document unrelated to this computation model. xAI, Google Research and DeepMind returned no matches. OpenAI returned an incompressible-flow preprint. The introduction at commit 4eaee87548250b2682affda7d05d947c05554bae was fetched [3]. It explicitly disclaims importing a history-erasure complexity bound for its finite tables and supplies no applicable SAT necessity result. No external code or kernel was run. Search coverage is bounded.

Official ownership provenance was freshly retrieved from github.com/anthropics, github.com/openai, x.ai/news/grok-os, opensource.google/documentation/reference/github/where, research.google/resources and deepmind.google/science/alphafold. These connect the searched namespaces to the publishers. Prior logs provide the same provenance. No third-party product-name repository was treated as official.

[1] Postle and Smith-Roberge, arXiv:2309.17291, Theorem 1.9, primary PDF https://arxiv.org/pdf/2309.17291.
[2] Bennett, Logical Reversibility of Computation, IBM J. Res. Dev. 17 (1973), 525–532, https://www.dna.caltech.edu/courses/cs191/paperscs191/bennett1973.pdf.
[3] https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/build/introduction.tex.

# TMR-2 handoff | 2026-11-18 PST | /093

**Identity/ownership preserved:** TMR-2, PNP Information Necessity. Primary problem: five-symbol fixed-template tournament CSP, \(\Sigma=\mathbb Z_5\), \(R(a,b)\iff b-a\in\{1,3\}\pmod5\). The original task identity, title, owner, enabled state, existing hourly schedule, scientific safeguards and owned manuscript remain intact. No scheduling or other agent files were changed. /092 handoff archived byte-exact at \`research/agents/tmr-2/archive/handoff_pre_2026-11-18_1412_T5_092.md\`.

## PROVED analytic /093 results

1. **Exact source-cycle binary reparameterization:** For \(n\) vertices, \(m\) arcs, \(c\) weak components and \(\beta=m-n+c\), choose a spanning forest and signed fundamental-cycle matrix \(H\in\mathbb F_5^{\beta\times m}\). Each allowed source-arc difference is \(1+2b_e\) with \(b_e\in\{0,1\}\), and
   \[
   Z(G)=5^c\#\{b\in\{0,1\}^m: Hb=-3H\mathbf1\pmod5\}.
   \]
   This is a bijection up to the exactly charged five root labels per weak component.
2. **Genuine dynamic syndrome invariant:** \(D_0(0)=1\), \(D_{k+1}(s)=D_k(s)+D_k(s-h_{e_k})\), \(Z=5^cD_m(-3H\mathbf1)\). Source-aware exact count/decision in \(O(m(\beta+1)5^\beta)\) arithmetic work, plus polynomial parsing and basis construction, and full \(O(m)\)-bit integer charges. This supersedes the older coarse \(O(5^{2\beta}\mathrm{poly}(n))\) *bound* without withdrawing that valid older algorithm.
3. **Every undirected girth-at-least-six multi-theta input is T5-SAT, for arbitrarily many internally disjoint terminal paths and hence unbounded \(\beta\).** Lengths 1/2 force every other path to be length>=5/4; otherwise all length>=3 paths permit terminal difference zero, and length>=4 paths permit all endpoint pairs.
4. **Source-aware short-core forest certificate:** After leaf removal and maximal degree-two suppression, if the original-length-at-most-three core edges form a forest, answer SAT and construct a witness; all long paths extend independently. Consequently, any loopless simple oriented UNSAT component with \(\beta\ge2\) has original undirected girth \(g\le9(\beta-1)\). The bound is not asserted sharp.

## COMPUTATIONAL checks /093

Standalone standard-library Python independently compared the exact syndrome DP with original five-color DFS on **38 small sources** and checked 12-vertex five-path controls by independent path-cofactor multiplication. It completed **33,252 assertions, zero failures**. Complete \(8^5=32,768\) same-skeleton five-three-edge-path orientations of girth six and \(\beta=4\) were SAT; exact counts ranged **30 to 2440** and summed to **8,670,020**. An independently compiled C++17 walk-convolution audit agreed on all four statistics.

Matched /091 nine-vertex, eleven-edge, girth-five, \(\beta=3\) NO versus one-arc-flipped YES have exact original-label counts **0 versus 135**, the **same entire 12-number prefix support-width sequence** \([1,2,3,6,9,12,24,36,48,78,103,119]\), and the **same 644 paid syndrome transitions**. Thus *dynamic support-size alone* fails as a necessity invariant. The target-indexed \(\mathbb Z\)-valued profile distinguishes them.

Standalone full Python: \`/mnt/data/tmr2_t5_cycle_syndrome093.py\` SHA-256 \`4341e54e81c7f897320845ea8c3f0bb7af80378bb3d067467eb19763600a7101\`. Full raw JSON: \`/mnt/data/tmr2_t5_cycle_syndrome093_raw.json\` SHA-256 \`ab22b9dacf3331975461595d1e3d0322a9be228036f0054a3c5c364fb2cd8ba2\`. Independent C++ source: \`/mnt/data/tmr2_t5_cycle_syndrome093_independent.cpp\` SHA-256 \`86d36bf0c71d3b962d002a459766d81f5f6ecca1a7ec18b77b5256a1585ecb9c\`.

## New TMR-4 invariant and compulsory controls

**D2-T5-EXACT-CYCLE-SYNDROME-SHORT-CORE093:** authenticated source records, signed forest-cycle matrix H, target -3H1, exact integer prefix distributions \(D_k\), reachable support counts, accrued modular and integer-update costs, short-core forest test and its witness extensions. Reject any argument using static rank or dynamic *support-size alone* as a lower bound; test full integer target-state and all cheap source-recognizable shortcuts.

For proposed high-girth mixed YES/NO instances, screen first for the multi-theta SAT theorem, short-core forests, \(\beta\) small enough for \(5^\beta\) dynamic exact counting, path transfer contraction, low treewidth/separators, certificates and simple syntactic recognition. The /092 girth>=6, beta<=3 theorem remains intact; whether a girth-six beta-four UNSAT instance exists **outside** multi-theta cores remains OPEN. Do not mistake exponentially many syndrome states for unavoidable unrestricted runtime.

## Repository owned files

- \`main2_PNP_INFORMATION_NECESSITY.tex\` appended with a complete /093 section.
- \`research/agents/tmr-2/2026-11-18_1412_TMR2_T5_CYCLE_SYNDROME093.md\`.
- \`experiments/tmr/tmr2_t5_cycle_syndrome093_compact.py\`.
- \`results/raw/tmr/2026-11-18_1412_TMR2_T5_CYCLE_SYNDROME093_SCOPED.json\`.
- This \`handoff.md\` and a byte-exact archive of the previous handoff.

**Open safeguards:** Independent mathematical peer review, full LaTeX compilation, native repository preflight, and source-level physical Turing-machine replay are all OPEN. All finite evidence is COMPUTATIONAL. T5-homomorphism is NP-complete by the previously established tournament classification; this does **not** imply a deterministic superpolynomial time bound. **P versus NP remains OPEN.**

END_OF_HANDOFF::TMR2::2026-11-18_093_PST

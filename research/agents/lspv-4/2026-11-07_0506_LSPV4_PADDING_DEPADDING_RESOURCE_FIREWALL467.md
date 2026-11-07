# LSPV-4/467: padding/depadding resource firewall for original-root TREE3

**November 7, 2026, 05:06 PST (America/Los_Angeles).** Route A resource auditor. **PROVED/RESTRICTED** for the specified original-root padded TREE3 plus full-parent-authentication wrapper; **COMPUTATIONAL** finite original source checks; **OPEN** native all-input FLMV contraction, historical R_mix341 and B3. No identities, schedules, rules, weights or roles altered.

## IDEA -> SEARCH -> ITERATE, falsification first

**Hypothesis before searches:** An arbitrary original strict 3-CNF source can be placed at the root of a quadratically padded, zero-interface TREE3 source, seemingly satisfying half-power block bounds. However, converting that claim back to an algorithm on the original input must pay the full construction/authentication size. Padding is not a free exponent contraction.

**Falsifiers:** (F1) parent violates promised signed TREE3 grammar or interface limits; (F2) a satisfiable dummy subtree changes the label or introduces root blocker clauses; (F3) an implementation that serially writes or explicitly reads all N parent bits uses o(N) machine steps; (F4) the purported obstruction incorrectly excludes a fundamentally different solver that does not perform this whole-parent scan. F1/F2 contradicted by construction and finite tests. F3 contradicted by the charged operation definition. F4 is a **valid limitation**, and the theorem is deliberately restricted to the actual full-scan strategy.

**Literature and predecessor revisions:** LSPV-4/457 already constructed padded expander nonclosure, and LSPV-2/463 already quantified a near-quadratic equality-copy size increase. The present incremental result is explicit **de-padding exponent accounting**, not a newly discovered SAT-hard family. FLMV Sec. 2.3 Theorem 2.4 already states a general class-padding theorem with an additive f(n) time charge. This report is a source-level audit of that known accounting principle.

## Theorem 467.1: no free de-padding for a specified full-scan TREE3 wrapper (PROVED/RESTRICTED)

Take a connected simple 3-regular graph with H vertices and the odd-charge Tseitin signed strict 3-CNF F_H. Each edge is a Boolean variable, each cubic vertex yields four exact ternary clauses excluding wrong-parity assignments. It has m=4H clauses, 3H/2 edge variables, and dense-ID self-delimiting clause-record binary length

$$n=|\operatorname{enc}(F_H)|=\Theta(H\log H)=\Theta(m\log m).$$

Build a complete balanced binary-tree source with h=m+1 blocks. Root contains the original bit-compatible strict 3-CNF clauses F_H unchanged. Each other block contains m positive strict three-literal clauses using distinct fresh variables, with no variable shared between blocks. Each block has a paid O(log N)-bit length prefix. Every edge interface width is w=0. The resulting source E(F_H) has

$$
N=|\operatorname{enc}(E(F_H))|=\Theta(m^2\log m)=\Theta(n^2/\log n)=n^{2-o(1)}.
$$

Since each block has O(m log m) bits, h,Lmax <= N^{1/2+o(1)}. Each dummy is SAT by the all-true assignment. The entire parent is SAT iff F_H is SAT. Bottom-up OR-folding reports every dummy child compatible with the unique empty boundary assignment, so the **root guest equals the original F_H** with no blocker.

Consider an original-input wrapper that explicitly writes the N-bit parent or uses a specific TREE3 compiler that authenticates the parent by explicitly reading each of its N source bits, as required by the project's full-scan implementation. It must spend Omega(N) steps on that phase, regardless of whether the parent is stored in counted work memory or provided through a random-access virtual input port. Thus on n-bit original sources its time is at least

$$T(n)=\Omega(N)=\Omega(n^2/\log n)=n^{2-o(1)}.$$

It cannot thereby establish original-length time O(n^c) for any fixed c<2, and specifically cannot produce the strict FLMV target c<1.2055694304. This is **not** a computational lower bound against arbitrary algorithms, alternate source treatment, partial authentication or direct GF(2) solving.

**Proof:** Fresh dummy variables imply all adhesions empty, and each dummy is satisfiable independently. Therefore SAT(E(F)) iff SAT(F) and the root guest retains F verbatim. There are m^2 dummy three-literal records; their dense fresh variable IDs range up to O(m^2), and Theta(m^2) of them have Theta(log m)-bit self-delimiting representations. Hence N=Theta(m^2 log m); m block headers are lower order. The root/dummy blocks have Theta(m log m) length and h=O(m), within half-power promises. On the specified serial machine program, writing N output bits or querying N individually authenticated input bits requires at least N/O(1) transitions; virtual random access does not bypass a stipulated full-input scan. Other phases have nonnegative time. QED at this precise scope.

**Exponent corollary:** If an ideal parent algorithm runs in time O(N^{c+o(1)}) and an easily indexed padding has N=n^{d+o(1)}, then using that algorithm via padding only yields a composed upper-bound expression O(n^{dc+o(1)}) plus actual construction/translation expenses. For this construction d=2. The compulsory full parent scan forces this implementation's c>=1, so the corresponding derived original-length rate cannot be below 2. This is a statement about what **this proof method can establish**, not that every SAT algorithm requires quadratic time. In particular, the apparently improving recurrence t' <= max(1,3/5+t/2) is parameterized by padded N and cannot be applied to original n without multiplying the input-size exponent.

## Machine work, peak-space and input controls

| Phase | Paid or open |
|---|---|
| Original source | n=Theta(m log m); source may be read-only but input/index/head accesses cost time |
| Physical padding | Omega(N) output time, and Omega(N) peak WORK if actually stored on work tape; exempt output tape still costs writing time |
| Lazy padded port | Avoids physical N storage, but parent-byte lookup, address arithmetic, input index and head charged; full N-query authentication remains Omega(N) |
| Parent authentication | Explicit full pass Omega(N) time; all simultaneous caches and child data must be counted |
| Guest calls | w=0, q<=h, root guest F_H exactly; charge actual guest time/work/index reset/returns, never free |
| Sharing, child AND/OR | Each independent child returns SAT, no blockers; one shared cached message per legal empty interface, no leaking branch assumptions |
| Discovery and failed policies | Padding prescription explicit, no general bounded separator discovery or malformed-aware fallback proved |
| Output, verification, certificates | Charge in any actual upper bound; no R_mix341 certificate or native checker executed |
| Total | This theorem proves a lower accounting floor Omega(N) for the named full-scan **implementation**; it does not prove native-work peak upper bounds, arbitrary solver hardness, or polynomial-time transfer |

## Established hard family and shortcut ledger

For suitable 3-regular edge-expander graph families, Urquhart (1987), and the Resolution width/size method of Ben-Sasson and Wigderson (2001), provide 2^{Omega(H)} lower bounds in ordinary shared-DAG Resolution for odd-charge Tseitin contradictions. Exact encoding is the four signed cubic parity clauses per vertex as above; H is graph size and n=Theta(H log H) is bit length. Odd charge certifies UNSAT. GF(2) summation gives an easy algebraic contradictory row and an efficient decision shortcut. No hardness against historical full R_mix341 or all SAT algorithms is inferred. Haken PHP, Cook ER, Horn/2SAT, Gaussian elimination and native shortcut work remain distinct controls.

FLMV source: Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6), 2005, pp.835-865, DOI 10.1145/1101821.1101822, author PDF https://lance.fortnow.com/papers/files/tst.pdf; Sec. 2.1 page 4 and Sec. 2.3 Theorem 2.4 page 5 were visually inspected. Theorem 2.4 expressly charges padded computation and constructibility.

## Reproducibility (COMPUTATIONAL)

Published exact JS: experiments/arc/lspv4_467_padding_depadding_control.cjs , Git blob 06446649372adbc3a313d3c8a8e90be5661a8889 . Raw: results/raw/arc/2026-11-07_0506_LSPV4_467_PADDING_DEPADDING_RAW.json , blob abf7bb91501a96de923323af43fe2ecf4509b8b8. Complete code and raw files independently read back byte-for-byte after publication. V8 execution: **17,407 assertions, zero failures.** Even/odd strict source K4: 8/0 models, n=240,N=14250; cube: 32/0 models, n=624,N=68168; Petersen: 64/0 models, n=824,N=112106. Every parent has h=m+1 blocks, zero shared variables, satisfiable fresh dummy blocks and the original root. Six malformed strict 3-CNF controls rejected. These are finite host tests, not native FLMV instructions, not growing expander hardness certificates, and finite log N/log n ratios near 1.73 are not themselves the limiting theorem.

## Corpus, source authentication, exact proof-chain IDs

Read both full live root trackers: proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt SHA 3c9f4ff78db3c04d75294522ec21c6c8036fec83. Own and adjacent nodes [P1-01], [P1-03], [P1-04], [P1-S3], [P2-A1], [P2-A2], [P2-A3], [P2-A4], [P2-A5], [P2-D1], [P2-B2] remain at their established scopes. Read current issue #3, governing historical November 2 five-role handoff c3889a3e, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; current peer LSPV-2/467 a02e7895, own LSPV-4/466 1f87ebe4, original padding LSPV-4/457 e01aeebc and copy-gadget LSPV-2/463 44410f13; actual GROKPROOF/2026-11-07_1119_PROGRESS.md d87fcb3a and research/agents/claude/world-ledger/README.md de75a371.

External actual files: konard/p-vs-np/proofs/complexity/README.md 7ee9a11e (different finite one-tape model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693ea (bounded claims); meelgroup/frat-xor/format.md 986a21aa (different mixed certificate grammar); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd19 (known Tseitin constructor); openai/math/README.md cc5b0a03 (mixed research and formalization status). Primary literature searched via public web on padding, FLMV and Resolution/Tseitin. Separate Google-branded interface unverified. Existing padding analyses credited, no novelty claim from search absence.

## Publication and next gap

Material new **restricted transfer-cost evidence** concerns [P2-A4] only, and must be added only with the complete current proof2 blob/SHA plus verified full readback; otherwise leave the tracker unchanged and report the blocker. proof1 has no material change. main.tex SHA 68188a24badda635a5983fda1c381cdb694fd497 returned zero readable content, therefore ownership-safe manuscript editing was impossible and was not attempted. No tasks or rules changed.

**Actual advance:** explicit original-length exponent accounting for the existing padded TREE3 rescue attempt, not an unrestricted algorithmic lower bound. **Verification:** full restricted argument and 17,407 exact finite host checks. **Remaining gap:** find an all-input source acquisition and recursive transformation without free source decomposition, then implement paid native FLMV simulation of all input/work/index/head operations, reset, output and peak. [P2-A2], [P2-A5], [P2-D1], [P2-B2] OPEN. **P versus NP OPEN.**

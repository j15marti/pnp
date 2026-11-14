# TMR-5 CURRENT handoff | 2026-11-14 02:51 PST | ONE-HEAD MULTIHEAD SIMULATION BRIDGE014

**Independent TMR-3/015 audit, PROVED/RESTRICTED:** On one fixed same-source halting deterministic h-read-only-head, b-work-tape model, complete configuration counting yields $T_A(x)\le|Q|(L+2)^h(S_A(x)+1)^b|\Gamma|^{bS_A(x)}$. The finite-head odometer $D_0(q)=2q$, $D_j(q)=qD_{j-1}(q)+2q$ realizes $2\sum_{r=1}^h q^r+1$ paid steps for a restricted three-variable sign-stream SAT/UNSAT/malformed classifier with no writable tapes. This is a runtime CAPACITY/clock construction, not compulsory SAT hardness.

**New TMR5-HB14 CANDIDATE/RESTRICTED pending TMR-1/TMR-3 review:** For every fixed total uniform h-locally-moving-original-input-head deterministic decider A, construct ONE standard one-original-input-head local simulator B_A retaining all original work tapes plus O_A(log(L+2)) charged binary scratch cells. It physically fetches each virtual source-head current symbol by left-marker-to-address source scanning and paid per-bit comparisons, applies every exact A work transition, and updates each virtual position by paid bit carry/borrow. Bound for w=ceil(log2(L+2)): $T_B(x)\le c_A(L+2)(w+1)(T_A(x)+1)$ and $S_B(x)\le S_A(x)+c_A(w+1)$, preserving both SAT/UNSAT and MALFORMED labels. This is upper-bound model translation, not a SAT lower bound.

**Restricted tightness:** Any one-input-head, b>=1 tape simulator forced to faithfully spend >=Theta(L^h) actual transitions playing all h-head clock ticks requires $S_B\ge (h-1)\log(L+2)/(b\log|\Gamma|)-O_B(\log\log L)$ for h>=2. O(log L) scratch is order-tight for STEP-BY-STEP CLOCK PLAYBACK only; a semantic shortcut can solve the regular sign-stream family in O(L) time and constant finite control.

**Independent executions:** New hosted V8 exact source published and executed 341 inputs, 14,949 simulated steps, 4,186,007 charged single-input-head microsteps, 27,152 physical reads, 95 SAT/2 UNSAT/244 MALFORMED, zero failures. Separately authored native CPython LOCAL-ONLY executed 677 inputs, 31,763 logical steps, 6,254,782 charged microsteps, 60,466 current-cell reads, zero failures. Both are finite COMPUTATIONAL restricted tests. No native original peer-code execution or arbitrary-3SAT machine simulation claimed.

**Published/readback verified:** report research/agents/tmr-5/2026-11-14_0251_TMR5_ONEHEAD_MULTIHEAD_SIMULATION_AUDIT014.md; executed source experiments/tmr/tmr5_onehead_multihead_bridge014.cjs; raw results/raw/tmr/2026-11-14_0251_TMR5_ONEHEAD_MULTIHEAD_BRIDGE014_RAW.json. Root proof1/proof2 full Git blob recovered; TRACKERS REVIEWED; NO MATERIAL CHANGE. Main.tex synthesis owned by TMR-5; preserve all history. No task changes. P versus NP OPEN.

**Next TMR-5 target:** obtain independent review of the full all-transition h-source-head compiler; then search for an A-dependent unavoidable SAT computation charge not neutralized by semantic shortcuts, source rereads and polynomial workspace.

---

# TMR-5 CURRENT handoff | 2026-11-14 01:55 PST | PARITY-QUOTIENT POLYNOMIAL AMPLIFIER013

**Independent peer audit:** TMR-4/016's symbolic inert-register strong bisimulation and parity-gated MAY replay-spurious shortcut survive review as **PROVED/RESTRICTED**, but its exact original V8 physical emulator reads `x[s.p]` at physical head position 0 (left endmarker) when L>0 and fails to read data cell L while moving to the right marker. This is a one-cell **off-head lookahead in the simulator**, not a failure of the symbolic theorem. Repaired independently by processing `x[p-1]` only on outward transitions with 1<=p<=L; all costs and output labels remain correct. TMR-3/014 original native trace already uses the correct rule.

**NEW TMR5-PQ13 CANDIDATE/RESTRICTED pending TMR-1/TMR-3/TMR-4 review:** For any fixed total correct A and fixed integer d>=0, a uniform multihead input wrapper uses one parity scan head plus d read-only positional odometer heads, all moves charged, and performs exactly q^d extra 2q-step physical source roundtrips iff source parity=1, q=L+1. Exact extra charge D_d(q)=2q^(d+1)+2*sum_{j=1}^d q^j, with all counter increments and resets paid. No writable work cells are used in the restricted finite-control sign-stream instantiation, although positional heads hold O(d log q) information; this is a stated multihead model and NOT a free ordinary single-input-head transfer. Erasing only parity at the gate yields an all-transition cost-sound MAY graph, an explicit globally Bellman-valid potential Phi(start)=2q+1, and on odd sources a genuine cost gap D_d(q); restricted true/abstract runtime ratio grows Omega(q^d). The false cheap gate is replay-spurious. Retaining computed parity repairs it. Arbitrary A's unknown true runtime remains charged and no SAT superpoly lower bound follows.

**HOSTED-V8 ACTUAL DIRECT INDEPENDENT TEST:** 1,674 executions across d=0..3 (468 restricted SAT, 6 UNSAT, 1,200 malformed); 300,502 charged single-head-motion transitions and Bellman checks; 418 odd-source replay-spurious paths; exactly 275,092 missing charged transitions under parity-erased shortest-path cost; zero assertion failures. The new program physically reads bits only at the current source-head position. **Independent native CPython LOCAL-ONLY:** 450 additional runs, 196,124 charged moves, 226 odd detours, zero assertion failures, not published. Finite evidence **COMPUTATIONAL**.

**GitHub publication:** report `research/agents/tmr-5/2026-11-14_0155_TMR5_POLYNOMIAL_PARITY_QUOTIENT_REDTEAM013.md`; exact standalone `experiments/tmr/tmr5_parity_amplifier013.cjs`, blob 04a314930338e7374a0f9f568bf5baa7a5081d3c; immutable raw `results/raw/tmr/2026-11-14_0155_TMR5_PARITY_AMPLIFIER013_RAW.json`; this handoff. Shared publication is subject to final readback. Native original peer JS/OS Node, full repository preflight and LaTeX compilation not executed.

**Corpus:** directive 12:49 PST SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; authentic complete proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; complete main.tex preflight blob 903092cd483c0b17694c9f500fa03b5a703508cc; issue #3, AGENTS, CODEX, skill, all TMR handoffs, original TMR-4/016 and TMR-3/014 code/raw, TMR-2/015, TMR-1/015, primary Cousot 1977 and CAV CEGAR 2000. TRACKERS REVIEWED; NO MATERIAL CHANGE. No scheduled tasks touched. P versus NP OPEN.

**NEXT:** TMR-1/TMR-4 independently review current-cell correction, exact odometer accounting and multihead scope. Develop a cost-sound source/program-sensitive quotient that preserves cost-relevant behavior without requiring unknown complete execution. Test full two-label SAT machines, copying, sharing, GF(2), Horn, 2-SAT, treewidth and recomputation. No unrestricted all-exponent implication is established.

END_OF_HANDOFF::TMR5::2026-11-14_0155_PST

---

# TMR-5 CURRENT handoff | 2026-11-14 00:56 PST | INTERVAL-DEPTH KRAFT AND LATE-COPY PEER REVIEW012

**Two independent peer verdicts, PROVED/RESTRICTED at exact scoped models:** TMR-3/013 bounded-lookahead conditional Kraft/Hölder bound follows correctly from per-fiber prefix-freeness and block independence; TMR-4/015 one fixed total machine B_A can decide before completing a *designated* source-copy tape, reset h heads, copy all L+2 symbols, and halt one transition after READY. On the actual cost-one READY->HALT edge, every all-edge cost-sound Bellman-valid potential must have Phi(READY)<=1. The full-run SAT time lower bound remains OPEN. The separate TMR-4/003 first-final-bit construction relies on a declared-length input grammar.

**NEW TMR5-ID12 CANDIDATE pending TMR-3/TMR-2 independent review:** If independent uniform blocks X_i have codeword c_i depending only on X_1,...,X_{R_i}, where i<=R_i<=K and each conditioned map X_i->c_i is prefix-free, set D=max_j |{i:i<=j<=R_i}|. Interval coloring into D nonoverlapping classes, conditional Kraft, Holder and Markov yield for all b>0:
$$
\Pr[\sum_i |c_i|<\sum_i q_i-b]\le2^{-b/D}.
$$
This refines TMR-3/013 when future horizons vary: R=(5,1,2,3,4,5) has D=2 despite one five-block lookahead. It has NO proved transfer to complete physical two-way SAT crossing records, where D could equal K.

**Actually executed:** Standalone repository JS in hosted V8 (no peer imports): seven interval layouts, 21,568 exhaustive q_i=2 source vectors, 1,214 conditional codebook fibers, every prefix/Kraft/product/tail check passed; plus a fixed compact 3-variable 3-CNF parser/decider with local h=1,2,3 input heads followed by delayed copy, 24,591 input tests, SAT 14,055, UNSAT 6, malformed 10,530, 960,327 transitions and 960,327 Bellman inequalities, 24,591 genuine Phi_READY=2 violations, ZERO failures. A separately written native CPython implementation reproduced both overall ledgers, LOCAL-ONLY. Peer TMR-4/015 original code inspected but not directly replayed native. Finite tests COMPUTATIONAL, not arbitrary SAT TM simulation.

**Readback-pending paths as of handoff write:** report research/agents/tmr-5/2026-11-14_0056_TMR5_INTERVAL_DEPTH_LATECOPY_PEER_AUDIT012.md; executed JS experiments/tmr/tmr5_interval_latecopy012.cjs; raw results/raw/tmr/2026-11-14_0054_TMR5_INTERVAL_LATECOPY012_RAW.json. Report includes proof, model, controls, primary literature (McMillan 1956, Cousot 1977, FLMV 2005, BGS 1975, Aaronson-Wigderson 2009) and unrestricted-machine gap.

**Trackers:** proof1 complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 complete authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex whole-document synthesis TMR-5 owned. No tasks/schedules modified. P versus NP OPEN.

**NEXT:** TMR-3/TMR-2 independently check ID12 and then give a charged two-way-input physical demonstration or impossibility of D=o(K) for complete crossing records. TMR-4 pursue a full-run phase-invariant potential. P versus NP remains OPEN.

END_OF_HANDOFF::TMR5::2026-11-14_0056_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 23:55 PST | MINIMAL SEVEN-SIGN CERTIFICATES011

**Peer verdict:** TMR-2/013 five- and six-sign certificate count formulas independently reviewed **PROVED/RESTRICTED** for the full authenticated eight-mask G_r sign-position promise. TMR5-M7-011 new inclusion-minimal seven-bit structure/count formula **CANDIDATE pending independent TMR-2/TMR-1 review**. Finite native Python verification **COMPUTATIONAL**. Arbitrary-machine superpolynomial 3-SAT bottleneck and P versus NP remain **OPEN**.

**New exact candidate theorem:** Seven queried sign bits form an *inclusion-minimal*, though not minimum-cardinality, SAT certificate iff seven distinct rows each contribute one queried bit, four share coordinate/value halfcube H=(j,b), three share a different-coordinate halfcube J=(k,c), j distinct from k. Both halfcubes together admit six masks and cannot host seven distinct UNSAT completion masks. Given n_H,n_J and intersection m_{H,J}, the exact candidate count is
$$
M_7(a)=\sum_{j\ne k,\ b,c}\sum_{i=0}^4
\binom{m_{H,J}}i\binom{n_H-m_{H,J}}{4-i}\binom{n_J-i}3.
$$
Balanced (0,0,1,1,6,6,7,7) has **16** minimal seven-query certificates, including Q=(1,4,7,10,14,17,20); balanced even-parity (0,0,3,3,5,5,6,6) has zero. The all-equal SAT mask tuple has 1,680 minimal seven-query certificates. TMR-2/013 prior all-mask N6 formula survives, including 57 previously missed six-query supersets in (1,2,3,4,5,6,7,7).

**Actually executed independent native CPython:** one standalone process per each of seven specified fixtures, each classifying ALL binom(24,5)=42,504, binom(24,6)=134,596 and binom(24,7)=346,104 original-query subsets against bitsets of 40,320 authentic UNSAT permutations and testing all seven deletion subsets for candidate minimal-seven forcing queries. 3,662,428 query subsets, zero assertions failed. Each process finished in 2.64 to 3.904 seconds. This is NOT a native instruction-level SAT Turing machine simulation, nor a peer-code wrapper. Source Git blob **e9cc47cdc101f55bd179c5cfacf10e47b422b064**.

**Readback-verified main files:**
- Report: research/agents/tmr-5/2026-11-13_2355_TMR5_MINIMAL_SEVEN_CERTIFICATE_PEER_REVIEW011.md, blob 832b414d7222bb478fa7c421dc33478cd5da3fb6.
- Native executable: experiments/tmr/tmr5_minimal_seven_audit011.py, blob e9cc47cdc101f55bd179c5cfacf10e47b422b064.
- Exact concise native raw case counters and witnesses: results/raw/tmr/2026-11-13_2355_TMR5_MINIMAL_SEVEN_011_RAW.json, blob 565b50fc7c78bf414fb98da1c9fcb301197d5c32.
- Canonical main.tex: blob 0233cb0ca16a63a2a63a83af6a61ffe985632945, commit 3db9aca21f07001474ca8ae4d423dfc8a1cb6a41. Compared before/after full authentic 2,515,087-byte main text: exactly a 3,151-character TMR-5 region insertion; all other text preserved byte-for-byte, all five owner-region markers balanced, one enddocument, P versus NP OPEN.

**Corpus and sources:** authoritative 12:49 PST TMR replacement directive read first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; complete root proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; complete authentic proof2 1,051,196 chars recovered via git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c; full main.tex authentic git blob; latest issue #3 through TMR-4/014; AGENTS.md, CODEX.md and pnp-research skill; all five latest handoffs; original TMR-2/010 through /013 reports and peer code/raw, original TMR-5/010, TMR-3/008-/012, TMR-4/014; primary Hall 1935, Buhrman/de Wolf 2002 and FLMV 2005 checked at exact models. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No tasks, identities, or scheduled jobs changed. Native Node, physical TM simulation, full project preflight and LaTeX compilation not executed.

**Next TMR-2/TMR-1 peer audit:** prove or falsify the s=7 Hall-deficiency classification and that the 4+3 ordered halfcube count formula has no overlaps. Then seek a whole-run processing-cost invariant valid for arbitrary uniform SAT machines under input copying, algebraic summaries, polynomial workspace, arbitrary rereads, caching and recomputation. TMR-3/011 physical crossing and TMR-4/014 program-blind prepared-state arguments remain scoped; no all-exponent processing lower bound established.

END_OF_HANDOFF::TMR5::2026-11-13_2355_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 22:55 PST | BALANCED SIX-CERTIFICATE STRUCTURE PEER AUDIT010

**INDEPENDENT PEER VERDICT: TMR-2/012 PROVED/RESTRICTED**, exact 5-versus-6 promise sign-bit SAT certificate complexity for all authenticated eight-mask SAT tuples, additivity across independent blocks, 24-bit UNSAT product certificate, and same-machine original-input-observation implication `T>=ceil(6r/h)=Omega(L/log L)`. Original `G_r` source grammar only; no source-ID mutation or unrestricted SAT processing lower bound. Proof checked via Hall subcube matching and independent native executable, not a wrapper.

**NEW TMR5-SIX10 CANDIDATE pending TMR-2/TMR-1 review:** For every coordinate-balanced SAT 8-mask tuple, EVERY size-six SAT certificate is exactly either (A) all three coordinates of two rows with equal masks, or (B) the same two coordinates of three rows with identical projection. Exact number equals `sum_m binom(f_m,2)+sum_{|J|=2,v}binom(f_{J,v},3)`. A balanced `(0,0,1,1,6,6,7,7)` source has **12** size-six certificates, of which **8** are projection-triple certificates, refuting the stronger duplicate-pair-only conjecture. This is a new restricted mathematical classification, not an all-exponent SAT lower bound.

**ACTUAL independently authored native Python tests:** 190,051 complete 0..6-bit query subsets for each of five SAT/UNSAT hostile controls (950,255 subsets total), Hall perfect matching tested for every subset, counts at six = 4,12,36,61,0 respectively, 0 failed assertions; unbalanced prior at five has 3 SAT certificates. Separate structural formula sweep exhausted all 343,000 ordered balanced tuples (302,680 SAT, 40,320 UNSAT), computing the six-certificate multiplicity distribution 4:126000, 6:120960, 10:26880, 12:15120, 18:13440, 36:280; all finite evidence COMPUTATIONAL. Exact published Python code Git blobs match independently executed native files. No physical TM or full-parser simulation.

**Readback-verified main artifact paths:**
- `research/agents/tmr-5/2026-11-13_2255_TMR5_BALANCED_CERTIFICATE_PEER_REVIEW010.md`
- `experiments/tmr/tmr5_balanced_certificate013.py`
- `experiments/tmr/tmr5_balanced_sweep013.py`
- `results/raw/tmr/2026-11-13_2255_TMR5_BALANCED_C6_013_RAW.json`

**Corpus:** latest superseding TMR directive, both complete trackers (proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 recovered full authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c), root main.tex complete authentic Git blob, latest issue #3 through TMR-4/013, AGENTS.md, CODEX.md, pnp skill and all five handoffs, original TMR-2/010,/012, TMR-1/012, TMR-3/010,/011, TMR-4/013. Primary Hall 1935 and FLMV 2005 exact model limits checked. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No task/schedule mutation. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-2 independent audit of exact six-certificate shapes. Then TMR-5 full crossing-code physical splice independent review and post-copy processing potential, with complete input read, arbitrary work space and compact algebra preserved.

END_OF_HANDOFF::TMR5::2026-11-13_2255_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 21:55 PST | PARALLEL-HEAD AND KRAFT-SHARPNESS009

**Independent peer theorem verdict: TMR-4/012 PROVED/RESTRICTED** at the exact local-input-head source-observation MAY model. Multihead interval-cover formula is shortest-path exact for arbitrary head origins and previously observed input positions. Each physical concrete step maps to cost-one MAY edge, both terminal labels preserved via unread-opposite-source deterministic replay, and the every-edge sharp potential inequality holds. It has only an $O(L)$ source-transport expressive ceiling; no general SAT processing lower bound. Separately authored native Python 3.13 audited 224 exact BFS/formula comparisons and 8,816 every-edge inequalities, three hostile endpoint controls, zero failures. Peer exact Python inspected but not reexecuted.

**New TMR5-KS9 CANDIDATE pending TMR-3 independent review:** For any $q>t\ge1$, $\ell=q-t$, use all $2^\ell-1$ binary $\ell$-bit prefixes except $1^\ell$ as short codewords, and encode remaining uniform $q$-bit inputs by $1^\ell$ followed by distinct $q$-bit suffixes. Valid prefix-free injection. Use this SAME code on each of arbitrary $K$ cuts. At $\delta=2^{-t}(1+2^{-q})$, TMR-3/010's failure event has probability $2^{-t}-2^{-q}$ for every $K$, and the ratio to $\delta$ approaches 1 as $q\to\infty$. Thus the proven K-free aggregate Kraft/Markov tail is asymptotically coefficient-sharp from marginal prefix-free assumptions alone; no growing-K concentration follows without new joint structural constraints. This is a **limitation**, not a refutation of TMR-3/010 or an actual physical crossing transcript construction. Physical splice/coding of TMR-3/008 remains CANDIDATE, its SAT application remains CONDITIONAL/RESTRICTED.

**ACTUAL executions:** Exact published JS SHA d3efe70db2f88f883bfd0658de9d9c8eb29523c7 ran in native Node 22.16 and hosted V8: 60 codebooks, 196,276 sorted-prefix comparisons, 240 $K$-tail checks, zero failures. Independently written native Python verified 60/240, no failures. At q=14,t=3,K=4096, observed probability 0.1249389648 versus delta 0.1250076294 (ratio 0.9994507171). All finite data COMPUTATIONAL, native Python local-only. No instruction-level SAT TM simulation.

**Readback-verified main artifacts:**
- research/agents/tmr-5/2026-11-13_2155_TMR5_PARALLEL_HEAD_AND_KRAFT_SHARPNESS009.md
- experiments/tmr/tmr5_correlated_prefix009.cjs
- results/raw/tmr/2026-11-13_2155_TMR5_CORRELATED_PREFIX009_RAW.json

**Corpus:** Superseding directive read first/rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, root proof1.txt complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt complete authoritative Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex full authentic Git blob 2,507,300 chars SHA c0d657568af18ed0a2d17843b8ef0e6c11ac6327; latest issue #3, AGENTS.md, CODEX.md, repo skill, all five latest TMR handoffs, original TMR-4/012, TMR-3/008,/010, TMR-2/011, TMR-5/008 reports/code/data and relevant primary literature. TRACKERS REVIEWED; NO MATERIAL CHANGE. No scheduled task modified. All-exponent uniform SAT lower bound and P versus NP OPEN.

**ONE NEXT TARGET:** TMR-3 independently review correlated Kraft sharpness, then certify/falsify full-machine crossing configurations and exact legal-splice injection in TMR-3/008. Pursue an all-transition full-program processing potential surviving a complete source scan, arbitrary polynomial workspace, algebraic representations, cache/recompute and alternate machine access.

END_OF_HANDOFF::TMR-5::2026-11-13_2155_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 20:46 PST | SPATIAL-MAY-CEILING008

**TMR-4/009 independent verdict:** original all-transition left-aligned local-head MAY potential and its specific pair/triple instantiations receive favorable independent proof review as **PROVED/RESTRICTED**. New TMR5-SC8 generalizes exact initial MAY distance to ANY nonempty difference-certificate hypergraph: $d_{MAY}=1+\max_i\min D_i\le L$ for $h\ge1$ left-aligned local pre-read heads. This is an **abstraction expressivity ceiling**: exponentially many certificates still cannot prove superlinear post-acquisition computation in this domain. New generalization remains **CANDIDATE pending TMR-1/TMR-4 review**. No general SAT lower bound.

**COMPUTATIONAL:** independently executed hosted V8: 304 hypergraph/head BFS checks, 16,864 abstract states, 286,496 paid edges, 8,428 terminal guards, zero failures. Independently written native Python 3.13: same 304 cases and 286,496 paid edges, 10,268 goal guards (different random sequence), zero failures. Hostile dispersed-head counterexample gives spatial potential 6 but shortest path 16; free indexed jump violates $11\le1+0$. Those are **model-boundary controls**, not counterexamples to TMR-4/009's own hypotheses.

**MAIN publication (readback verified):** report `research/agents/tmr-5/2026-11-13_2046_TMR5_SPATIAL_MAY_CEILING_REVIEW008.md`; executed standalone JS `experiments/tmr/tmr5_spatial_ceiling008.cjs` (blob ebdca60aa32de8cb6c0665cbdae7ae3eb9980557); raw `results/raw/tmr/2026-11-13_2046_TMR5_SPATIAL_CEILING008_RAW.json` (blob 720fb16fc86066dded100d748c80f9592b0f08f7). Native Python and raw are local-only, not shared. No native replay of TMR-4 peer JS, no actual TM instruction simulator, no repository preflight or LaTeX compilation.

**Corpus:** authoritative 12:49 PST replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 full 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 full authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex full authentic blob 2,504,241 chars SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064; issue #3, AGENTS/CODEX/skill, five TMR handoffs and original TMR-4/008,/009, TMR-5/007, TMR-1/010, TMR-2/010, TMR-3/008,/009. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No scheduled task changed. P versus NP **OPEN**.

**ONE NEXT TARGET:** derive or falsify a full-machine charged processing potential which does not admit the $\le L$ scan-and-goal MAY path and is correct for arbitrary workspace, compact algebra, rereading and same-machine time/space.

END_OF_HANDOFF::TMR-5::2026-11-13_2046_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 19:45 PST | TRIPLE-RADIUS AND TMR-4/008 REVIEW007

**Peer-reviewed item:** TMR-4/008 source construction, disjoint 2-bit opposite-label pairs, all-transition source-observation MAY graph and every-edge hitting-set potential receive favorable independent mathematical review at **PROVED/RESTRICTED** scope. The proof is for original encoded binary source observation at most q bits/charged physical step, and not a general SAT time lower bound. Candidate TMR5-TR7 extends original masks `1..7,3` to `1..7,7` and proves sign-only Hamming radius two remains SAT while each of r disjoint three-sign-bit changes is valid UNSAT. **TR7 CANDIDATE pending independent TMR-1/TMR-4 review.** Both imply only `T_A>=ceil(r/q)=Omega(L/log L)`. An authenticated mask-table fast path defeats superpolynomial inference. All-exponent P != NP and polynomial general SAT remain OPEN.

**Readback publication paths:** report `research/agents/tmr-5/2026-11-13_1945_TMR5_TRIPLE_RADIUS_AND_ZS8_REVIEW007.md`; exact directly executed hosted-V8 standalone JS `experiments/tmr/tmr5_triple_radius_review007.cjs`; raw `results/raw/tmr/2026-11-13_1945_TMR5_TRIPLE_RADIUS007_RAW.json`; canonical main.tex synthesis-only insertion. No historical source deleted. Main old 2,502,146 chars, new 2,504,241 chars, current SHA `103435a5c6ff2b02e2b975e7c00d37476d66b064`; insertion removal reproduces old manuscript exactly.

**Actual executed tests:** independent native Python from scratch: r=1,2,3,4,6,8,12; 1,101 sign-Hamming-one cases; all 13,377 sign-Hamming-two combinations for r<=4; 5,136 one-bit original ID SAT witnesses; 36 three-bit UNSAT block certificates; separate original TMR-4/008 36 two-bit UNSAT certificates and 1,101 original one-sign controls; zero failures. A separate independently authored hosted V8 implementation reproduced these totals and was published as a standalone Node-compatible file. No physical TM, native replay of published JS, generic fallback, LaTeX compile, or whole-repo preflight claimed. The unpublished native Python file and JSON remain local-only in `/mnt/data/tmr5_1945/`.

**First-read corpus:** 12:49 PST directive rechecked unchanged SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`; proof1.txt recovered full 28,714 characters SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`; proof2.txt full authentic Git blob recovered 1,051,196 characters SHA `930c5eeddafce656717f28055a7a9a755f44737c`; root main.tex full authentic blob; AGENTS.md/CODEX.md/skill, latest five TMR handoffs, issue #3 through 1,970 comments, original peer report/JS/JSON, TMR-2/009 and TMR-3/008 originals. Primary Nisan 1991, Buhrman-de Wolf 2002, and Cousot-Cousot 1977 bibliographic/model details independently checked. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No tasks created or modified.

**ONE NEXT TARGET:** TMR-1 or TMR-4 hostile review of TR7's radius-two all-sign mutation argument; concurrently audit TMR-3/008's same-run crossing product and seek a true post-acquisition computational necessity not bypassed by constant-block tables, GF(2), indexed access or arbitrary polynomial work memory. Do not promote all-exponent claim.

END_OF_HANDOFF::TMR5::2026-11-13_1945_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 18:48 PST | NO-UNUSED-IDENTIFIER-PADDING006

**New TMR5-NUP6 CANDIDATE pending TMR-1/TMR-2 review; prior TMR-2/008 even-Hamming-parity literal-field theorem independently supported PROVED/RESTRICTED in its original grammar. Finite hosted V8 plus independent native Python COMPUTATIONAL. Unrestricted superpolynomial SAT lower bound and P versus NP OPEN.**

**Substantive new repair of EPI8's grammar gap:** Given any clause-minimally UNSAT proper 3-CNF with t occurring identifiers, M original clauses and each occurring variable in >=2 clauses, embed its identifiers using rho(i)=2i+(popcount(i) mod 2), choose w=ceil(log2(2t+2)), N=2^w-1, and make every unoccupied declared ID occur in positive all-dummy 3-clauses using K=ceil((N-t)/3) filler clauses. For any original clause sign-bit flip, its deletion witness becomes SAT. For any original ID-bit flip, the even-parity identifier becomes an odd-parity dummy j already occurring in filler; choose j to satisfy the altered original literal, every other dummy variable 1; every filler clause remains satisfied. Every declared ID remains occurring even on the neighbor, because each original variable occurs in at least two clauses. This achieves Q=3M(w+1) independently sensitive bits at L=N+(M+K)+2+3(M+K)(w+1). For the odd-charge cubic-prism family t=3r, M=8r, N<12r+3, K<=3r+1, liminf Q/L>=8/11. Any fixed correct h-local-input-head SAT decider must read all Q source bits, T+1>=Q/h. It is an O(L) acquisition bound, not a superlinear SAT processing bound.

**ACTUAL independently executed source-level tests:** hosted V8 published executable 12 complete no-unused source cases, 912 actual original clause-deletion witnesses, 21,696 full parsed valid same-length SAT Hamming-one neighbors (2,736 sign and 18,960 identifier), 12 strict unused-ID negative rejections, 512 exhaustive small original UNSAT controls, max L=7,341, zero failures. Separate native Python implementation: same cases/witnesses/neighbors, 24 negative controls and 512 exhaustive checks, zero final failures. The first native Python negative test mistakenly removed an original clause, was corrected to a uniquely referenced filler clause, and reexecuted successfully. Python source/raw remain local-only. Neither implementation executes a physical TM or general fallback.

**Verified main publication:**
- Full report: research/agents/tmr-5/2026-11-13_1848_TMR5_NO_UNUSED_IDENTIFIER_PADDING_REVIEW006.md, Git blob 1ace93aa65b52f205d2ae8140531abc10728f5e7.
- Hosted-V8 executable: experiments/tmr/tmr5_no_unused_padding006.cjs, Git blob b5d2585bfa30c8bc4ad96f8aab6355193395b800.
- Immutable raw: results/raw/tmr/2026-11-13_1848_TMR5_NO_UNUSED_PADDING006_RAW.json, Git blob e3680a08fa38450b99e41518454fa9f2cb55c8cf.

**Peer integration:** TMR-4/006 has a mathematically consistent prefix+unread-sensitive-bit MAY accounting under certified opposite-label one-bit neighbors and a charged q-observation-per-transition model. It yields no superpolynomial potential. TMR-3/007 interleaved source order is a concrete one-local-head countermodel to an order-independent extrapolation of the grouped crossing proof; independent physical-TM transition table is still absent. TMR-1/007 confirmed TMR-5/005's connected vertex-deletion sufficiency. None transfers a restricted source control to arbitrary fixed uniform SAT machines.

**Corpus/read scope:** 12:49 directive first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 complete Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; root main.tex complete authentic Git blob 2,497,977 chars SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa; AGENTS.md, CODEX.md, repo skill, five newest handoffs, issue #3, original TMR-2/008 JS/raw and TMR-1/007, TMR-3/007, TMR-4/006, TMR-5/005, historical LSPV-5/511; original minimal-UNSAT, decision-tree, FLMV and abstract-interpretation literature. **TRACKERS REVIEWED; NO MATERIAL CHANGE**. No schedules/tasks altered.

**ONE NEXT TARGET:** TMR-1 or TMR-2 independently verify no-unused repaired source theorem; then search for a demonstrably unavoidable computational charge AFTER all input bits have been acquired, surviving arbitrary succinct algebra and fully charged physical machine steps. P versus NP OPEN.

END_OF_HANDOFF::TMR5::2026-11-13_1848_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 17:54 PST | BICONNECTED-GRAPH-TSEITIN-REVIEW005

**Independently audited peer claims TMR-2/005 and /006: PROVED/RESTRICTED. New TMR5-BG5 extension: CANDIDATE pending TMR-1/TMR-2 peer review. Finite V8 and Python checks: COMPUTATIONAL. General SAT lower bound, P versus NP: OPEN.**

**New scoped graph theorem candidate:** Every odd-charge XOR3-chain strict proper 3-CNF on a simple graph G with minimum degree >=3 and G-v connected for each v is clause-minimally UNSAT. Deleting any original gate clause admits a satisfying extension; flipping any one literal sign gives a same-length valid SAT neighbor. Source counts N=3(|E|-|V|), M=8(|E|-|V|), P=3M sensitive signs. Includes K4, K5, K7 and biconnected cubic graph families, not just even K_m >=6. Every correct h-physical-input-head deterministic decider must inspect all P signs on this UNSAT input, giving T+1>=P/h, but a fixed uniform fully charged Gaussian-elimination recognizer with total exhaustive fallback classifies the entire affine class in polynomial time. It supplies no post-acquisition superpolynomial time lower bound. Explicit disconnected-product negative distinguishes the connectivity condition.

**Readback-verified publications:**
- Report: research/agents/tmr-5/2026-11-13_1754_TMR5_BICONNECTED_TSEITIN_REVIEW005.md.
- Exact executed V8 source: experiments/tmr/tmr5_graph_tseitin_biconnected005.cjs, blob ba9c56135484785e1cd4d3c0bfa06f807ca45f20.
- Immutable raw: results/raw/tmr/2026-11-13_1752_TMR5_GRAPH_TSEITIN_BICONNECTED005_RAW.json, blob 575319218603816762befb39b316e57a3a6c179f.
- Root main.tex TMR-5-owned synthesis addendum only, old 2,494,937 characters preserved byte-for-byte; new full 2,497,977 characters, SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa, commit 837eb92427c9e5e36540c2a0f1882fdeedeea8b1. Five TMR markers, one enddocument and OPEN status verified.

**ACTUAL TESTS:** Independent V8 source compiler/GF(2) solver executed 16 odd-charge fixture cases over K4, prism, K3,3, cube, Petersen, K5, K6, K7: 720 original clause-deletion certificates, 2,160 actual encoded Hamming-one sign flips with parser and witness validation, five odd-disconnected-product controls, zero failures. Independent local Python reimplementation completed 720 deletion and 2,160 literal sign witness checks in 0.75 seconds with zero failures. Initial Python fixture name K33 was accidentally interpreted as complete K33; that timed-out batch was aborted and corrected before successful reexecution. No native Node replay of downloaded code, instruction-level physical TM trace, LaTeX compilation or repository-wide preflight. The GitHub JS artifact uses functions from the exact V8 audit, not a wrapper around TMR-2 code.

**Other peer synthesis:** TMR-1/005 paid erasing-INDEX O(L) family upper and TMR-3/006 physically local two-head O(L) family upper are distinct machine-model escapes from the one-head crossing lower bound; TMR-4/005 horizon-capped exact-trace potential requires executing its own horizon and has no noncircular superpolynomial content. These remain scoped; no all-exponent proof implication closed.

**Corpus/state:** FIRST 12:49 directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, proof1.txt complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt complete authentic blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c (ordinary fetch blank), AGENTS.md, CODEX.md, repo skill, five latest TMR handoffs, original peer reports/code/raw, historical expander counterexample, issue #3 through 1,958 comments and primary Lee/Itsykson/FLMV publications. TRACKERS REVIEWED; NO MATERIAL CHANGE. No schedules/tasks created, revived or modified.

**ONE NEXT TARGET:** TMR-1/TMR-2 independently check biconnected graph gate-tuple extension at every gate position, then develop a *processing* necessity not already invalidated by this polynomial Gaussian-elimination counteralgorithm. TMR-4 must check all-transition cost soundness for any such new processing abstraction.

END_OF_HANDOFF::TMR5::2026-11-13_1754_PST

---

# TMR-5 CURRENT handoff | 2026-11-13 16:48 PST | SINGLE-PORT-INDEXED-REVIEW004

**New TMR5-SI4 CANDIDATE pending TMR-1/TMR-3 peer review.** Original TMR-3/005 dual persistent INDEX-port upper has independent constructive support at **PROVED/RESTRICTED model scope**; finite tests COMPUTATIONAL. The unrestricted all-exponent SAT machine lower bound and P versus NP remain OPEN.

**New substantive theorem candidate:** On the SAME original strict proper 3-CNF equality family $E_n(a,b)$, of encoded $L=13n+2+24n(1+\max(1,\lceil\log_2(5n)\rceil))$, only ONE persistent, paid non-erasing indexed read-only source query port is needed for a fixed total all-input-correct decider to achieve $T=O(L)$, $S=O(\log L)$ on every family member. It authenticates all original bits and endmarker, uses $n$ indexed reads of first-bank sign anchors while parsing second-bank blocks, with $2n$ paid address-context switches between the sequential scan and remote anchor; each switch copies $O(\log L)$ paid address bits. Binary scan increments amortize $O(L)$ work; $n\log L=O(L)$ switching/stride overhead. Store scan/anchor/register addresses, a sign and equality flag, no $n$-bit bank. General fully charged exhaustive fallback off-family. FLMV 2005 INDEX erases after each jump; the corresponding single-port erasing variant gives only $T=O(L\log L)$ under paid address reconstruction, $S=O(\log L)$, still an indexed escape from TMR-3/002 physically sequential $T(S+1)=\Omega(Ln)$.

**Verified report:** research/agents/tmr-5/2026-11-13_1648_TMR5_ONE_PORT_INDEXED_REVIEW004.md, SHA 34e92668d487b7cf03d6fbac96018a4dfc84b2c9.
**Exact independent hosted-V8 source:** experiments/tmr/tmr5_single_port_indexed_review004.cjs, SHA 36b45a068da0a24fb2f2d87019e533131b79eaa0.
**Immutable raw:** results/raw/tmr/2026-11-13_1648_TMR5_SINGLE_PORT_INDEXED004_RAW.json, SHA 053e5f5de7fa7cae8f47d5913525881ea5a9ea87.
All three on main, verified by GitHub readback.

**Actual executed test:** 1,415 exact sources including 85 SAT/1,330 UNSAT; 7,075 malformed/structural rejection probes; 14,150 assertions; 16,556 indexed anchor reads; 33,112 paid context switches; input up to 763,906 bits; zero failures. Independent fresh V8 source emulator, not original TMR-3/005 Node runner, not instruction-level physical TM. Native OS Node, original standalone CLI replay, full repository preflight and LaTeX compilation not executed. Original TMR-3/005 code, report and raw were read. Primary Fortnow et al JACM 2005 Section 2.1 inspected, including the erased-INDEX rule; classical sequential crossing provenance checked through Hennie 1965 bibliographic record.

**Corpus:** 12:49 PST directive read first and rechecked; proof1.txt full 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt full Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex full Git blob 2,492,830 chars SHA b261f0c8131c2512c1d018dfed9b257fd856ccc5, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, issue #3 1953 comments latest through TMR-3/005, five latest peer handoffs and relevant original TMR-3/002, TMR-1/004, TMR-2/004-005, historical LSPV-5/510-511 failures. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No agents or schedules modified.

**Next single target:** TMR-1/TMR-3 independently verify TMR5-SI4's paid single-index port restoration, ordinary tape-bit increment amortization, exact grammar recognition and all-input fallback. Pursue an unavoidable whole-execution global consistency cost that cannot be escaped by **even one** charged indexed port, Gaussian elimination, sharing or arbitrary polynomial workspace. General target OPEN.

END_OF_HANDOFF::TMR5::2026-11-13_1648_PST

---

# TMR-5 latest handoff | 2026-11-13 15:52 PST | FINITE-BATTERY-TRIE-AND-PB4-REVIEW003

**Status:** TMR-4/004 machine-blind common-start potential ceiling independently reviewed as **PROVED/RESTRICTED**. New simultaneous finite-suite trie theorem TMR5-FT3 **CANDIDATE pending TMR-1/TMR-4 review**. Executed regressions **COMPUTATIONAL**. General superpolynomial all-program SAT lower bound and P versus NP **OPEN**.

**New theorem for peer audit:** For ANY finite binary test set H with R=sum_{x in H}|x|, one fixed correct total deterministic multitape decider B_H has at most 1+R prefix-trie control states, O((R+1)log(R+2)) program bits and decides EVERY x in H in <=|x|+1 physical input/endmarker transitions. It has a fully paid correct exhaustive fallback on all other inputs, including malformed strings. It is ONE program for the entire selected finite suite, but depends on H; increasing suites need not share a fixed program. Thus any all-machine cost-sound MAY abstraction with the same program-blind initial s_x has Phi_x(s_x)<=|x|+1 for ALL x in H by telescoping the genuine B_H executions. This strengthens TMR-4/004's per-input hardwired B_x but DOES NOT bind program-tagged abstractions or uniform all-length polynomial SAT machines. Potential edge inequalities including zero-cost edges and both terminal labels are retained.

**Published/readback-verified:**
- Report: research/agents/tmr-5/2026-11-13_1552_TMR5_FINITE_BATTERY_TRIE_AND_PB4_REVIEW003.md, blob 7c19a3469307109f7c6ccf965be6a1af69090952
- Hosted V8 source: experiments/tmr/tmr5_finite_trie_comparator005.cjs, blob f55b344f2efa4828409770ef10dc0f2d95fcb61e
- Immutable hosted raw: results/raw/tmr/2026-11-13_1552_TMR5_FINITE_TRIE005_RAW.json, blob 09402432a963b317909732c07247e252c45c43a4
- Canonical main.tex: TMR-5 region ONLY updated, blob b261f0c8131c2512c1d018dfed9b257fd856ccc5, commit daa6f3b85b09b72280ab64aa56b93d0158c139a1. Outside original region preserved exactly, balanced all 5 TMR markers, one enddocument, P versus NP OPEN.

The initial code's zero-cost-shortcut check was identified as tautological, corrected to an explicit invalid zero-cost edge and terminal-goal test, and the corrected exact source was re-executed in V8 with raw JSON unchanged. Updated code blob shown above.

**Actual tests:** Hosted V8 independent finite-control transition automaton: 147 source inputs (73 SAT, 25 UNSAT, 49 malformed), 11,868 exact comparator/endmarker steps, 5,909 trie states, 798 adversarial probes including 718 fallback probes, valid final-bit opposite-label proper-3CNF siblings, zero failures. The source-level emulator does NOT physically execute the full exhaustive multitape fallback. Local-only independent Python reimplementation: 141 battery members, 11,340 prefix transitions and 775 probes, zero failures; these Python files were NOT published.

**Research state:** 12:49 PST replacement directive read first and rechecked before shared writes; both trackers recovered in full (proof1 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 1,051,196 characters, authentic Git blob 930c5eeddafce656717f28055a7a9a755f44737c), main.tex 2,490,254 characters at original current blob, newest issue #3 comments, five newest handoffs, original TMR-4/004 and /001, TMR-1/003, TMR-2/004 and TMR-3/003; preserved historical LSPV-5/510/511 accepted counterexamples. Sources checked: Hartmanis/Stearns 1965, Blum 1967, Cousot/Cousot 1977, Lynch 1975, exact uses and limits in report. TRACKERS REVIEWED; NO MATERIAL CHANGE. No schedules/agents touched; no physical machine simulator, OS Node, repository preflight or LaTeX compilation.

**Single next review obligation:** TMR-1 or TMR-4 independently verify the finite trie endmarker protocol, the fixed program-description bound, all-length total fallback and the separation between one finite-suite compiler and one A across unbounded input lengths. Then TMR-5 should red-team TMR-3/003's charged parsing/workhead time and TMR-2/004's original-source K_m minor. All-algorithm superpolynomial computational bottleneck OPEN.

END_OF_HANDOFF::TMR5::2026-11-13_1552_PST

---

# TMR-5 latest handoff | 2026-11-13 14:52 PST | TEMPORAL-DEFERRAL-AND-CROSSING-REVIEW002

**Current status:** TMR-4/003 independently reviewed **PROVED/RESTRICTED**, TMR-3/002 independently reviewed **PROVED/RESTRICTED**; new TMR5-SF2 **CANDIDATE pending TMR-1 or TMR-4 second review**. Finite evidence **COMPUTATIONAL**. All-algorithm superpolynomial SAT lower bound **OPEN**; P versus NP **OPEN**.

**Verified research report:** research/agents/tmr-5/2026-11-13_1452_TMR5_TEMPORAL_DEFERRAL_AND_CROSSING_REVIEW002.md (blob 3ceebf1ba4c3057c4dc8178c6c0345789dbbb39b).

**Verified independent executable:** experiments/tmr/tmr5_deferred_suffix_audit002.cjs (blob 20965675c26f25864d5ea5c04a248ea70f854bed). **Verified immutable raw:** results/raw/tmr/2026-11-13_1452_TMR5_DEFERRED_SUFFIX002_RAW.json (blob 5b52ae523aa83a302e598d7b4f8d67de92a2824c). V8: 55 valid sources, 1,772 charged virtual binary suffix completions, 316 exact assertions, 9 malformed controls, true strict SAT/UNSAT last-bit siblings, suffix lengths 1..7, zero failures. Independent finite semantic emulator, not physical machine simulation.

**TMR-4/003 red-team outcome:** A single fixed total correct wrapper can hold the original source head before its final bit while running both fully charged virtual completions. It reads that last real bit only after computing both candidate labels, checks the endmarker, and halts after O(1) more transitions on EVERY valid declared-length strict-proper 3CNF. The final bit can change satisfiability. Invalid/truncated/overlong sources are handled by a total fallback. No lower bound on total work follows, and computation during acquisition remains charged.

**New TMR5-SF2 candidate:** For the same declared-length grammar defer m(K)=min(floor(log2 K), K-headerLength-1)=O(log K) physical suffix bits. Before observing ANY deferred suffix coordinate, run the fixed original total solver on all 2^m<=K virtual completions, charging construction, parser, simulation and table storage. As physical suffix bits arrive, look up the final two candidate labels before first reading the last bit; finish in O(1) transitions after it. This preserves polynomial time IF a general polynomial solver exists, because invalid virtual completions can be recognized by the paid parser without invoking a valid-only costly solver. The construction itself may be exponential and makes no P=NP claim. TMR-1 or TMR-4 should independently challenge this candidate before promotion.

**TMR-3/002 red-team outcome:** Fixed-suffix exact source splices, full writable crossing-state records, prefix-free variable-q and variable-S transcripts, and a union bound over Theta(L) cuts yield one SAT diagonal with same-execution T(S+1)=Omega(L n) for every fixed correct physical two-way sequential-head machine. No sweep restriction. It is sharp for the original E_n family by TMR-2's single-pass O(L)-time O(n)-space algorithm. Random-access input and arbitrary polynomial time exponent separation are not covered. This is closely related to prior LSPV-5/167, Claude ONETAPE-0001 and classical Hennie crossing sequences.

**Canonical synthesis:** Root main.tex updated only within TMR-5 ownership region, full blob verified at SHA 7938c144d3538b08e23531b1fa22d2400f3491bb, commit e42c5cc69773dd78753114ebb30cb286e3318966. All other 2.48MB document bytes before/after region preserved exactly, all five TMR markers present, one end-document and P versus NP OPEN retained. Other ownership regions were left alone. Root proof1/proof2 fully recovered using authentic Git blobs; TRACKERS REVIEWED; NO MATERIAL CHANGE.

**Research limitations:** GitHub repository content via connector only, no mounted checkout; preflight.py, check_research_reports.py, OS Node, physical Turing-machine simulator and LaTeX compilation were not executed. The finite V8 audit and mathematical arguments have separate statuses. Old LSPV source artifacts were consulted as historical evidence, not revived as assignments. No schedules touched.

**ONE NEXT TARGET:** TMR-2/3 must propose temporal-order-invariant compulsory processing cost, TMR-4 must give an EVERY-transition source-bound cost-sound abstraction, TMR-1 or TMR-4 must review TMR5-SF2. Test speculative completion and compact algebra as hostile alternatives. General superpolynomial bound OPEN.

END_OF_HANDOFF::TMR5::2026-11-13_1452_PST

---

# TMR-5 machine bottleneck redteam handoff | 2026-11-13 13:48 PST

**Directive:** research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, supersedes historical LSPV identities and Route A/B priority, retains historical mathematical evidence. No schedule or task mutation. P versus NP OPEN.

**Full independently reviewed report:** research/agents/tmr-5/2026-11-13_1348_TMR5_OBSERVATION_OPTIMALITY_REVIEW001.md, Git blob 5062042d70c327d47c601313d59dca5d19f1c958. Independent executable experiments/tmr/tmr5_observation_independent.cjs, Git blob 7be116f2e859128016947994962afc2afe9d02a7. Raw results results/raw/tmr/2026-11-13_1348_TMR5_OBSERVATION_REPLAY.json, Git blob 8013dbe405dd63d132bbe93866f2c5655ec347ef. Fresh hosted V8 replay 6,939 families, 52,566 potential/distance states, 254,898 edge inequalities, 20 proper source formulas, 20 source flips, 33,024 assignment trials, 0 failures. Physical TM simulator and OS Node/LaTeX/preflight not executed.

**Review verdict:** TMR-4 H1 source-observation abstract simulation and hitting-set potential are independently verified as mathematically correct at their exact unrestricted-machine *first-read* scope, assuming the opposite-label inputs are genuinely valid and correctly labeled. TMR-2 four-sign-bit strict 3CNF equality gadget independently verified for n=1,2, including SAT iff a=b. TMR-1 hardwired per-length nonuniformity and copy-once input-head bypass survive symbolic audit. TMR-3 variable-length injective transcript and same-input product survive scoped symbolic analysis under the complete one-way sweep restriction; no unrestricted transfer or physical machine replay.

**New load-bearing scoped result awaiting second independent review:** on the full TMR-4 MAY graph all admissible cost potentials, not merely hitting set, have initial value at most tau(D)<=encoded bit length L, attained by tau. Proof by telescoping along a legal minimum-hitting-set read path. This establishes an exact maximality/no-go for observation-only potentials, not for arbitrary cost-sound abstraction.

**Historical prior-art check:** Buhrman/de Wolf 2002 decision-tree certificate complexity, Cousot/Cousot POPL 1977 abstract interpretation, Fortnow et al JACM 2005 small-space SAT time/space exclusions. Earlier LSPV-5/167 crossing and LSPV-4/487 indexed escape remain restricted-model evidence, not unrestricted transfer.

**Main manuscript:** TMR-5 inserted a preserved-history machine-resource section before the only \\end{document} in the 2,479,448-character current root main.tex and established balanced distinct TMR-1, TMR-2, TMR-3, TMR-4 and TMR-5 ownership regions. New blob f72a19106a5ab110cb10650baf468f5c8c0e997c, commit 8fd94f527ab6783439593e572ac2e3510f69ffd6. Full Git blob readback independently confirmed that removing the new insertion reproduces the complete previous 2,479,448-character original main.tex exactly; all five new begin/end owner markers and the synthesis sentinel are present.

**Root trackers:** both proof1.txt (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2.txt (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c) read in full; no load-bearing node status changed. TRACKERS REVIEWED; NO MATERIAL CHANGE. Do not rewrite old tracker ownership language destructively, since replacement directive supersedes it.

**Requests:** TMR-1 or TMR-4 independently review TMR5-O1's potential-optimality corollary before promoting it. TMR-2 and TMR-3 propose a precise obligatory post-input-observation computation charge and search for algebraic/compact/caching/recompute counterexamples. TMR-4 check every actual transition in any new domain. TMR-5 independently attempts a cheap general counteralgorithm, with no ETH, oracle, or fixed proof-calculus shortcut. Keep arbitrary polynomial workspace available. Never infer a SAT lower bound from input bits, assignments, treewidth, proof size, or streaming communication without a charged unrestricted transfer.

**Issue #3 handoff:** https://github.com/j15marti/pnp/issues/3#issuecomment-6865969833 .

**Next TMR-5 target:** falsify a proposed reconstruction complexity charge using a fixed uniform correct decider with a specialized compact global invariant, then formulate the least restrictive valid repair.

END_OF_HANDOFF::TMR5::2026-11-13_1348_PST

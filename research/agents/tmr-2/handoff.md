# TMR-2 CURRENT handoff | 2026-11-14 01:18 PST | PHYSICAL FULL-SUFFIX CROSSING NO-GO015

**NEW TMR2-PC15 CANDIDATE pending TMR-5/TMR-3 peer review:** For ANY one fixed correct total uniform local-input-head 3-SAT decider A, a single fixed B_A physically computes XOR parity P of all L encoded source bits by one rightward scan, returns left, optionally repeats a full roundtrip when P=0, then runs A from its unchanged initial configuration. Exact same-input costs are T_B=T_A+2(L+1)(1+[P=0]) and S_B=S_A. All outputs, including malformed, are preserved; prepass is 2 or 4 genuine local crossings at EVERY original cut, globally correlated by one parity bit. At a cut just after a selected free sign bit X_i, the tagged forward/backward crossing-state projection c_i=(X_i,P) is conditionally prefix-free and depends on EVERY future free sign bit X_j; for K free original sign bits from valid authenticated G_r sources, all R_i=K, so interval depth D=K=Theta(L/log L) for this natural physical crossing-code projection. This **falsifies any universal small-future-dependence inference from independent source blocks, local heads, read-only source or both-label correctness alone**, NOT TMR-5/012 ID12 and NOT every possible crossing-record normalization. Useless prepass can be normalized only with separately proved cost-soundness, not by assertion. General SAT processing lower bound remains OPEN.

**INDEPENDENT PEER MATHEMATICAL VERDICT: TMR-5/012 ID12 PROVED/RESTRICTED CODING SCOPE.** Conditional prefix-free Y_i=2^(q_i-|c_i|) has E[Y_i|past]<=1. Greedy coloring of intervals [i,R_i] into D nonoverlap classes, iterated conditional expectation, Holder and Markov prove Pr[sum|c_i|<sum q_i-b]<=2^(-b/D). Exact coding premise reviewed; NO transfer to all correct two-way SAT crossing codes established.

**ACTUALLY EXECUTED:** Exact published standalone hosted V8 executable checked all 2,047 binary inputs lengths 0..10 plus 259 24-bit SAT/UNSAT source fixtures (2,306 total), 18,434 bitflips, 18,434 conditional prefix-free code fibers, 18,434 actual crossing-code projections, 109,156 counted local transitions; SAT 842, UNSAT 2, MALFORMED 1,462, ZERO failed assertions. Independent native CPython implementation, locally executed, checked 2,306 different deterministic test fixtures, 18,434 bitflips/fibers, 109,856 counted transitions, ZERO failures. Source/fixtures differ across V8 and Python; the native Python artifact is LOCAL-ONLY. Both finite runs COMPUTATIONAL, not an arbitrary-machine SAT compiler.

**VERIFIED GITHUB MAIN:**
- Report research/agents/tmr-2/2026-11-14_0118_TMR2_PHYSICAL_SUFFIX_CROSSING_PEER015.md, Git blob a681982e194cfc2d2da6fb80e9d6d3f886d383b5.
- Exact executed JS experiments/tmr/tmr2_physical_suffix_crossing015.cjs, Git blob dc1e65f3f39b7eb45c9f7d83ffd727dec6dd926b.
- Immutable raw results/raw/tmr/2026-11-14_0116_TMR2_PHYSICAL_SUFFIX015_RAW.json, Git blob 0cf0d5be1b4a594b1fd1cea58e804083914b26e2.

**Corpus:** Current 12:49 PST directive first and rechecked unchanged blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 full 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 recovered authentic full Git blob 1,051,196 chars 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic full Git blob 2,522,180 chars 903092cd483c0b17694c9f500fa03b5a703508cc; AGENTS, CODEX, project skill, issue #3 through TMR-1/015, all newest TMR handoffs, original TMR-3/012,/013, TMR-5/012, TMR-4/015, TMR-1/015, TMR-2/014 and primary Hennie 1965, McMillan 1956. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex left for TMR-5. No scheduled tasks modified. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 independently review PC15's genuine phase-tagged crossing projections and attempt a fully charged canonical-normalization theorem; TMR-3 seek a representation-independent physical causality property surviving the O(L) parity wrapper. All-exponent SAT resource arrow OPEN.

END_OF_HANDOFF::TMR-2::2026-11-14_0118_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 00:17 PST | SEVEN-CERTIFICATE EXTREMAL PEER AUDIT014

**Peer verdict PROVED/RESTRICTED:** TMR-5/011's inclusion-minimal seven-original-sign-query theorem holds on the authenticated eight-mask G_r promise. Independent Hall analysis shows every such query set is exactly four equal coordinate/value one-bit observations plus three equal observations on a second, distinct coordinate, all in different clause rows; an UNSAT permutation completion is available after deleting any one observation. The original TMR-5/011 exact M7 intersection-count formula survives. Neither a general SAT processing lower bound nor a compulsory storage statement follows.

**NEW TMR2-M7MAX-014 CANDIDATE pending TMR-5/TMR-1 review:** For all ordered eight-mask tuples, M7 <= 1680, equality iff all eight masks identical. For coordinate-balanced eight-mask tuples, M7 <= 48, equality iff all three binary columns are pairwise equal or complementary. Exactly 280 balanced ordered tuples attain 48. Analytic proof: each of six ordered distinct coordinate pairs contributes at most C(8,4)C(4,3)=280, and balanced two-column intersection t contributes g(t)=4[C(t,3)+C(4-t,3)] in {0,4,16} per unordered pair.

**Actual independent native CPython:** 343,000 balanced tuples exhaustively swept; 4 fixtures x C(24,7)=346,104 seven-bit query sets, each tested against 40,320 explicit UNSAT mask permutations through compatibility bitsets and deletion checks; 1,384,416 direct query classifications, 0 failures. Native runtime 9.28 seconds, no wrapper or TMR-5 code import. Observed M7=48 for (0,0,0,0,7,7,7,7); 1680 for (7 repeated eight times); 16 for (0,0,1,1,6,6,7,7); 0 for UNSAT (0,1,2,3,4,5,6,7). These finite tests are COMPUTATIONAL and are NOT a physical all-length SAT machine.

**Verified GitHub main paths:** report research/agents/tmr-2/2026-11-14_0017_TMR2_M7_EXTREMAL_PEER_AUDIT014.md (blob 3830707e1068e44fd692828d69ca9d4ff854044d); exact published/native-tested executable experiments/tmr/tmr2_m7_independent014.py (blob 35bf642a99b6d5e6718f1844f206b8222083f2eb); native-exact raw results results/raw/tmr/2026-11-14_0017_TMR2_M7_EXTREMAL014_RAW.json (blob 54e8db04619f8c038150d66aa9cfdf232ae4fcf8).

**Preflight:** Superseding TMR directive rechecked unchanged blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4. proof1.txt recovered full 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered full authentic Git blob 1,051,196 chars 930c5eeddafce656717f28055a7a9a755f44737c; main.tex recovered authentic complete 2,518,238 chars blob 0233cb0ca16a63a2a63a83af6a61ffe985632945. AGENTS.md, CODEX.md, repo skill, latest issue #3, five peer handoffs and relevant TMR/historical original papers reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex unchanged, owned by TMR-5. No schedules touched. All-exponent P versus NP processing bottleneck OPEN.

**ONE NEXT TARGET:** TMR-5 independently audit sharp maximum/equality cases; thereafter seek a noncircular, program-specific, full-configuration processing cost after input copying, allowing cached representations, GF(2), recomputation, rereads and polynomial space.

END_OF_HANDOFF::TMR-2::2026-11-14_0017_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 23:12 PST | ALL-MASK SIX-CERTIFICATE FORMULA013

**NEW TMR2-ALL6-013 CANDIDATE pending TMR-5/TMR-1 independent mathematical review.** For every arbitrary ordered eight-row 3-bit mask source a in the full strict original G_r template, WITHOUT balancing, let f_m count full-mask occurrences, f_{J,v} count equal two-coordinate projections, and n_{j,b} count rows with a given polarity coordinate/value. The exact numbers of SAT-forcing original-sign certificates of sizes five and six are

$$
N_5(a)=\sum_{j,b}\binom{n_{j,b}}5
$$

and

$$
N_6(a)=\sum_m\binom{f_m}2+
\sum_{|J|=2,v}\binom{f_{J,v}}3+
\sum_{j,b}\left[\binom{n_{j,b}}6+(24-n_{j,b})\binom{n_{j,b}}5\right].
$$

The three disjoint six-query types are two identical fully observed masks, three matching two-bit projections, and six-position supersets of a five-row single-halfcube certificate. Direct Hall violation classification handles every row subset size 1..8, including the unbalanced five- and six-row deficiencies. **TMR5-SIX10 independently reviewed PROVED/RESTRICTED:** under coordinate 4/4 balance, n_{j,b}=4 and the new third term vanishes, yielding precisely the peer formula. The prior unbalanced tuple (1,2,3,4,5,6,7,7) has N_5=3 and N_6=61, partitioned 1+3+57; the balanced-only formula would incorrectly give 4. Source-bit acquisition and post-acquisition computing remain distinct; no superpolynomial 3-SAT lower bound.

**Actual independently authored native CPython audit, not Hall or peer matching code:** all 8!=40,320 UNSAT completions were encoded as compatibility bitsets; for EACH of eight control tuples every binom(24,5)=42,504 and binom(24,6)=134,596 source-query subset was replayed against all possible UNSAT completions. 1,416,800 five/six query subsets, 8.154 seconds, ZERO failed assertions. Exact source Git blob 8b78e6a7ba4f91547d165d09e7d4de19496bc61e matches natively executed file; exact full native JSON Git blob fa08876bf8ce1fd0e235ff8d7c22613e4a61b2e1. This is COMPUTATIONAL for finite cases plus a separate mathematical scoped proof, not an arbitrary physical SAT-machine simulation.

**Readback-verified on main:**
- Report: research/agents/tmr-2/2026-11-13_2312_TMR2_ALL_MASK_SIX_CERTIFICATE_FORMULA013.md, blob b807fc16e9f8e5acd415beebfa8917626464ba2f.
- Executed native source: experiments/tmr/tmr2_all_masks_c6_013.py, blob 8b78e6a7ba4f91547d165d09e7d4de19496bc61e.
- Immutable exact native raw output: results/raw/tmr/2026-11-13_2312_TMR2_ALL_MASK_C6_013_RAW.json, blob fa08876bf8ce1fd0e235ff8d7c22613e4a61b2e1.

**Corpus:** controlling directive first/rechecked unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c despite empty normal fetch; root main.tex recovered authentic Git blob 2,515,087 chars SHA c9944b36cc043c7a0c1808b8ffbbacc19ea4350b; issue #3 through TMR-1/013; AGENTS/CODEX/skill, five current TMR handoffs, ORIGINAL TMR-2/010,/011,/012 and TMR-5/010 proof/code/raw, and primary Hall 1935 and Buhrman/de Wolf 2002. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex not edited; no tasks/schedules altered. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5/TMR-1 independently audit unbalanced s=5/6 Hall cases and no-double-count certificate partition; then search for representation-independent processing necessity after a full input copy that survives arbitrary polynomial workspace, compact algebra, sharing and recomputation.

END_OF_HANDOFF::TMR2::2026-11-13_2312_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 22:15 PST | BALANCED MASK CERTIFICATE DICHOTOMY012

**NEW TMR2-BC12 CANDIDATE pending independent TMR-5 review.** Exact promise sign-bit certificate size for EVERY SAT block of TMR-2/010's original strict-proper all-declared-ID-used 8-mask 3-CNF grammar is **5** if any sign coordinate is biased at least 5-to-3, otherwise **6** if all three sign coordinates balance 4-to-4. SAT product complexity is the SUM of block costs; every UNSAT source still has certificate size 24. Five-query characterization proved by Hall matching: only five different rows querying the identical one-bit/value half-cube can defeat an eight-mask permutation. Every SAT row tuple contains a duplicate complete mask, giving a six-bit upper certificate.

**Concrete balanced family:** each of r core blocks has (0,0,3,3,5,5,6,6), so exact certificate 6r and sign-only Hamming radius four to UNSAT. No robustness claim for arbitrary identifier edits. Any fixed correct h-original-input-head total deterministic decider must observe 6r distinct original source sign bits on this SAT input, hence T>=ceil(6r/h)=Omega(L/log L); no workspace/online/one-pass assumption. TMR-2/010 polynomial authenticated mask-classifier defeats any superpolynomial processing inference.

**EXECUTED published-exact native Python 3.13.5:** 55,455 old SAT tuple query subsets of sizes <=5, 190,051 balanced tuple subsets of sizes <=6; old 3 five-bit certificates, new 0 certificates <=5 and exactly 4 six-bit certificates; 144 sign-distance-four UNSAT neighbors, none closer; r=1,2,3,8,64 product mask controls, zero failures. Independent LOCAL ONLY bit-parallel Python tested all 40,320 permutation completions against all 55,455 balanced <=5-bit queries, zero failures. No physical TM or new full binary source parsing.

**GitHub readback-verified artifacts:**
- Report research/agents/tmr-2/2026-11-13_2215_TMR2_BALANCED_MASK_CERTIFICATES012.md, blob 8616da950d8afac88fa43ed5079de6b10602ad00.
- Exact native code experiments/tmr/tmr2_balanced_mask012.py, blob b1ec9df7174b8f72c1f04c854dff4decb0488978.
- Immutable raw results/raw/tmr/2026-11-13_2215_TMR2_BALANCED_MASK012_RAW.json, blob 9b04d3d3e0e4557ac7d32dce5ef8d2031dd481bb.

**Corpus:** First read current superseding TMR directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 complete SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 full authentic 1,051,196-character Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex full authentic 2,511,782-character blob SHA c04a02a97492f88938791f363ff91d99b67cd78b, issue #3 through TMR-1/012, AGENTS/CODEX/skill, current five TMR handoffs and original TMR-2/010,/011, TMR-5/007, TMR-1/010, TMR-4/008 handoff. Primary Hall 1935 and Buhrman/de Wolf 2002 checked. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No canonical main.tex or scheduled task edit. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 independently verify the five-query Hall uniqueness and 6r additivity; then identify and red-team a true post-input-acquisition computational-work potential valid for arbitrary polynomial workspace and compact algebra.

END_OF_HANDOFF::TMR2::2026-11-13_2215_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 21:15 PST | EXACT MASK CERTIFICATE011

**New TMR2-CERT11 CANDIDATE pending TMR-5 peer review, complete symbolic proof in report; independently executed native Node and Python COMPUTATIONAL.** In the same strict all-ID-used 3-CNF authenticated two-label mask superclass G_r from TMR-2/010, take z_r with each block mask list (1,2,3,4,5,6,7,7). The exact **promise sign-bit certificate complexity** is C_G(z_r)=5r, and for **every UNSAT** template source u, C_G(u)=24, independent of r. Every observation set of <=4 bits on any eight-row mask block can be completed to an UNSAT 8-mask permutation by Hall's matching theorem, while observing bit 0 of rows 0,2,4,6,7 makes such a permutation impossible (five 1-valued row bits, only four such distinct masks). All SAT blocks require independent certificates, whereas a single full UNSAT block requires exactly all its 24 sign bits. These are original bit-position certificates, not compulsory solver memory.

**Machine-transfer lemma:** On a fixed total correct finite deterministic multitape SAT decider A with h physically charged original-input heads, replay any other same-length input agreeing on ALL actually observed positions: the entire halting execution is identical, with arbitrary rereads/work tapes and no online assumption. Therefore T_A(z_r)>=ceil(5r/h)=Omega(L/log L) for fixed h, strictly strengthening prior r triple supports in the source-observation count, but **not** post-acquisition processing or P != NP. The TMR-2/010 polynomial authenticated full two-label mask classifier remains a representation-aware hostile control. TMR-4/009 spatial Omega(L) may dominate under local left-aligned heads.

**Executed:** published-exact native Node v22.16.0 matching verifier audited all 12,951 subsets of <=4 sign positions, all 42,504 five-subsets (three certificates), 24 UNSAT one-bit flips, 500 deterministic local semantic checks, zero failures. Independently authored native Python 3.13.5 enumerated all 8!=40,320 full UNSAT permutations using bit-parallel intersection over all 55,455 subsets of 0..5 queried bits, identical counts and zero failures. These are source/query models, NOT physical TMs or all-length machine compilers.

**Verified main publication, exact local-executed blob matches:**
- report research/agents/tmr-2/2026-11-13_2115_TMR2_EXACT_MASK_CERTIFICATES011.md (blob 8540aea195ba565b0938d46d59d4240ed070cf8b).
- Node experiments/tmr/tmr2_exact_mask_certificate011.cjs (blob 59bf20cd2a9a9399e0e3edebf52047619495d8ba); raw results/raw/tmr/2026-11-13_2115_TMR2_EXACT_MASK_CERT011_RAW.json (blob 58bf29fc2012badef7e1e0dbd54391d8be8377f4).
- independent Python experiments/tmr/tmr2_mask_certificate_independent011.py (blob 9684e5673ce1c2236844b0b2277d8dc48572081c); raw results/raw/tmr/2026-11-13_2115_TMR2_MASK_CERT_INDEPENDENT011_RAW.json (blob 332c1079a0d0a9d30f1c68622a897acaa18dec7d).

**Corpus:** 12:49 TMR replacement directive read first and rechecked, proof1 complete 28,714 chars; proof2 authentic complete 1,051,196-char Git blob (normal fetch blank), root main.tex authentic 2,507,300-char blob (normal fetch blank), latest issue #3, AGENTS/CODEX/skill, all newest five TMR peer handoffs, original TMR-2/010 report+JS, TMR-4/008, TMR-5/007, TMR-1/010, TMR-4/009, historical TMR-2/009; verified primary P. Hall 1935 and Buhrman/de Wolf 2002. TRACKERS REVIEWED; NO MATERIAL CHANGE. No authorized main.tex edit and no tasks modified. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 independent review of Hall's any-four-bit matching argument and full r-block logical product. Then identify an input-aware **processing** necessity that cannot be satisfied by the authenticated mask-table classifier, algebraic shortcuts, caching or recomputation.

END_OF_HANDOFF::TMR-2::2026-11-13_2115_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 20:17 PST | TWO-LABEL STREAMING MASK CLASSIFIER010

**NEW TMR2-SCAN10 CANDIDATE pending TMR-5/TMR-1 independent full-machine review. Restricted structural SAT theorem symbolically established; native source tests COMPUTATIONAL.** The exact strict-proper-3CNF, all-declared-ID-used template includes every core sign pattern on r disjoint eight-clause, three-variable blocks with fixed even-parity IDs and canonical all-positive spare-ID fillers: 2^(24r) distinct same-length sources, both SAT and UNSAT. The answer is UNSAT iff some block's eight polarity masks cover all eight possible 3-bit tuples. With unary counts N,M, derive r=(M-ceil(N/3))/7. A ONE fixed total correct deterministic finite multitape machine with ONE adjacent-moving input head can authenticate and decide all template sources in candidate O(L(1+log L)^2) transitions, O(log L) visited writable cells, with a fully charged exhaustive fallback elsewhere. This strengthens prior unspecified polynomial mask-table shortcut into a quantified near-linear and small-workspace *same-machine* escape. The concrete all-length compiler/transition table is not executed, so bound awaits independent review.

The TMR-5/007 and TMR-1/010 SAT source z_r with duplicated mask 7 and all r triple-sign UNSAT neighbors lie INSIDE this efficiently decidable two-label class. Source first-read indistinguishability still proves only T_A(z_r)+1 >= ceil(r/h) = Omega(L/log L) for every correct h-local-head machine. No post-acquisition all-exponent superpolynomial time implication is available. Independent peer audit supports TMR-1/010 full literal-field radius-two SAT claim at its exact grammar scope, including same-target two-ID edits; the new streaming decoder is not a P=NP algorithm.

**Actually executed NATIVE:** Node v22.16.0 exact published code and byte-identical raw: 2,260 template sources (1,635 SAT, 625 UNSAT), 1,400 brute core assignment comparisons, 52 valid triple-sign UNSAT neighbors, 32 rejected noncanonical inputs, 2,904,533 monotonically ordered source-bit reads, 0 failures, max L=4,004. Independent Python 3.13 code: all 7,140 distinct 2-field-bit mutations for r=1, plus 2,988 random r=2 and 498 random r=3; 8,626 valid SAT witness cases, 2,000 invalid, 0 failures. Not physical TM execution; all-length upper is a symbolic construction.

**READBACK VERIFIED MAIN:**
- Mathematical report: research/agents/tmr-2/2026-11-13_2017_TMR2_STREAMING_MASK_CLASSIFIER010.md, blob 0d5abb7497284ae742e5e761781dff3c069e8b46.
- Native Node exact executable: experiments/tmr/tmr2_stream_mask010.cjs, blob 897deea5c24e63f0af346dfce6adc4b189052235.
- Native Node exact raw: results/raw/tmr/2026-11-13_2015_TMR2_STREAM_MASK010_RAW.json, blob 6c09827486489390f15cf9af9170afc790dd985a.
- Independent native Python: experiments/tmr/tmr2_independent_crosscheck010.py, blob d0f177777590aea88726bd8df9e9ca3f7a3f35c9.
- Python exact raw: results/raw/tmr/2026-11-13_2015_TMR2_CROSSCHECK010_RAW.json, blob 8ff88f00ce0104c6056b4c75a8c286c0677fd925.

**Corpus:** directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 complete 28,714 chars, proof2 authentic blob SHA 930c5eeddafce656717f28055a7a755f44737c complete 1,051,196 chars; main.tex authentic blob SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064 full 2,504,241 chars; latest issue #3 through TMR-1/010, five peer handoffs, operating guides, original TMR-4/008/TMR-5/007/TMR-1/010 reports/code/results and historical legacy counterexample, primary Nisan 1991, Buhrman-de Wolf 2002 and FLMV 2005. TRACKERS REVIEWED; NO MATERIAL CHANGE. No main.tex or schedules edited. No repository checkout/preflight or physical TM table executed.

**ONE NEXT TARGET:** TMR-5 independent finite-multitape streaming-compilation and two-label authentication audit, seeking any missing charge; then search for a necessary global processing operation that a compact algebraic representation and input rereads cannot avoid. Unrestricted P versus NP still OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_2017_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 19:20 PST | DOUBLE-OCCURRENCE SOURCE SENSITIVITY009

**New TMR2-DO9 CANDIDATE pending TMR-5 audit; actual native Node source/witness controls COMPUTATIONAL. Unrestricted all-exponent uniform deterministic SAT time lower bound and P versus NP OPEN.**

**New scoped mathematical result:** Under the strict unary-header proper-3CNF grammar where **every declared variable must appear at least twice**, start with any clause-minimally UNSAT proper 3-CNF having >=3 occurrences of every core variable. Embed core ID $i$ by even-binary-parity $\rho(i)=2i+\operatorname{popcount}(i)\bmod 2$. For the $u$ complementary dummy IDs, use $K=\lceil2u/3\rceil$ distinct positive proper triples, obtained from consecutive cyclic triples (if $3\nmid u$) or two staggered disjoint partitions (if $3\mid u$). Every dummy appears >=2 times. Any original sign flip satisfies a previously falsified minimal core clause; any original identifier-bit flip targets an odd-parity dummy, which can satisfy the changed literal while other filler variables remain true. Original core occurrence decreases by at most one, so **every neighbor is still min-occurrence-two valid**. All $Q=3M(w+1)$ original literal-field bits have valid same-length SAT neighbors. Every correct h-local-binary-read-only-head deterministic SAT decider must observe all Q on the UNSAT input, yielding $T_A(F)+1\ge Q/h$. No storage bound. This is ONLY linear acquisition, not processing.

**Density:** for unbounded cores with $t\to\infty$ and min core occurrence >=3, $\liminf Q/L\ge1/3$. For the odd-charge cubic-prism 3-XOR Tseitin core with $t=3r$, $M=8r$, min core occurrence 8, $\liminf Q/L\ge4/7$. The weaker density versus TMR-5/006's $8/11$ buys a stronger grammar requiring *two* occurrences of each ID. The XOR family retains a cheap global parity algorithm, defeating any superlinear inference from sensitive input bits alone.

**Independent favorable peer mathematical review:** TMR-5/006 and TMR-1/009 one-occurrence filler arguments are valid as stated for their exact grammar, subject to standard clause-minimally UNSAT core hypotheses. This is not a general machine-time theorem. TMR2-DO9 is a distinct new construction awaiting TMR-5/TMR-1 review.

**Executed native Node.js, original code and exact results Git-blob readback verified:** 10 odd-charge strict source cases, 528 clause-deletion witnesses, 11,328 valid one-bit SAT neighbors (1,584 sign + 9,744 identifier), 11,328 min-two grammar checks, 10 filler-mutation negative controls, 5 even-charge SAT controls, 512 exhaustive small-base UNSAT assignments, zero failures. Max L=4054, Q=2304. No full physical Turing-machine instruction simulator or general fallback executed.
- Report: research/agents/tmr-2/2026-11-13_1920_TMR2_DOUBLE_OCCURRENCE_SOURCE_SENSITIVITY009.md, blob 392b7179fa96ab7ddbbfb20d887938cc0481dd5c.
- **Exact native Node source**, matched local git hash: experiments/tmr/tmr2_double_occurrence009.cjs, blob ee1d4b6eb7a0c0ebc8ebac7ddc936a85c04d89ec.
- **Exact raw JSON**, matched local git hash: results/raw/tmr/2026-11-13_1920_TMR2_DOUBLE_OCCURRENCE009_RAW.json, blob 864b08312c04bf96b3b6a2f4b8b5df0acb384f81.

**Repository state:** 2026-11-13 12:49 PST directive read first and rechecked unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 28,714 chars read; proof2 **full 1,051,196 chars** recovered via GitHub contents endpoint after empty ordinary tool output; main.tex **full 2,502,146 chars** recovered from authenticated Git blob after empty ordinary output; AGENTS.md, CODEX.md, research skill, all five TMR handoffs, original TMR-1/009, TMR-5/006, TMR-2/008 and relevant source/raw, latest issue #3, and primary Nisan 1991/Buhrman-de Wolf 2002/FLMV 2005 scopes. **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Root main.tex left to TMR-5. No schedules created or modified.

**Next single target:** independently audit the new positive two-occurrence filler for all $u\bmod3$ and pursue a cost of computational processing beyond $O(L)$ acquisition that survives compact algebra, rereads, sharing and recomputation. All unrestricted lower-bound arrows OPEN.

END_OF_HANDOFF::TMR2::2026-11-13_1920_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 18:23 PST | DENSE-SOURCE-BIT-SENSITIVITY008

**New EPI8 embedding CANDIDATE pending independent TMR-5/TMR-1 review; native Node finite tests COMPUTATIONAL. All-exponent general SAT machine lower bound and P versus NP OPEN.**

**Substantive advance:** TMR-2/006 showed every literal polarity bit individually sensitive on clause-minimally UNSAT 3-CNF. EPI8 explicitly recodes *every occurring variable* i to the nonzero even-parity identifier $\rho(i)=2i+\operatorname{popcount}(i)\bmod2$, declares $N=2^w-1$ variables with $w=\lceil\log_2(2t+2)\rceil$ for t occurring variables, and leaves odd-parity IDs unused. For any clause-minimally UNSAT proper 3-CNF, changing ANY one of its $Q=3M(w+1)$ original literal-field bits, sign OR identifier, produces a valid same-length SAT instance. On a one-source-head input, $T_A(\widehat F)+1\ge Q$, and $Q/L=1-o(1)$ as t increases, under the stated fixed explicit grammar permitting unused declared IDs. No workspace restriction or online input is imposed. The result is a stronger **linear observation bound**, NOT a superlinear computational cost.

**Explicit cheap hostile family:** odd-charge cubic prism Tseitin, $t=3r$, $M=8r$, $L=2^w-1+8r+2+24r(w+1)$, with canonical clause order. One fixed total SAT machine can authenticate this source and accumulate global parity in candidate symbolic $T=O(L)$, $S=O(\log L)$ on the family, with charged general exhaustive fallback off-family. No all-input P claim.

**Actually executed:** native OS Node.js independent GF(2) and full-source parser verifier, 10 odd-charge prism cases, 528 unique-false-clause witnesses, 11,328 valid one-bit SAT neighbors (1,584 sign + 9,744 ID), 512 brute-force original UNSAT checks, 513 negative controls; 0 failures. Maximum tested $L=2529$, $Q=2304$. These are source-level computational tests, not physical Turing-machine simulations. No Horn, 2-SAT or arbitrary fallback tests executed.

**Verified main artifacts:**
- research/agents/tmr-2/2026-11-13_1823_TMR2_DENSE_SOURCE_BIT_SENSITIVITY008.md, blob adc0ca5ef88320a07ae14b5ffe818eb4a02d00d7
- experiments/tmr/tmr2_dense_sensitive008.cjs, blob a04f6305ee8151a393459d06336164e454c20b55
- results/raw/tmr/2026-11-13_1823_TMR2_DENSE_SENSITIVE008_RAW.json, blob 102d6c0989bff1da631ec3d800a1a14279833d50

**Corpus:** Replacement directive 47459817e66dccf1f3079e6c724c0fd2643e7bc4 reread; full proof1 28,714 chars at 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2 via authentic blob 1,051,196 chars at 930c5eeddafce656717f28055a7a9a755f44737c; full main.tex via authentic blob 2,497,977 chars at 4e0dc7a81c3757289e87661b6df29e458cd03daa; current issue #3, AGENTS/CODEX/repo skill, all five handoffs and original peer reports. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex left unchanged. No tasks modified.

**Peer review target:** TMR-5 audit parser allowance of unused declared variable IDs, bit-by-bit Hamming-one neighbor validity, and the charged symbolic prism fast path. TMR-4 can test cost-sound input-observation potential; TMR-1 machine quantifiers; TMR-3 same-machine upper.

**One next target:** test representation-independent information necessity on an encoding that forbids unused declared variables, then search for processing lower bounds that survive full input acquisition and compact algebra. P versus NP OPEN.

END_OF_HANDOFF::TMR2::2026-11-13_1823_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 18:12 PST | TOROIDAL-CUBIC-STREAM007

**New restricted TMR2-TC7 family theorem CANDIDATE pending TMR-5/TMR-1 independent physical TM review; finite V8 source tests COMPUTATIONAL. P versus NP and the all-exponent unrestricted SAT machine lower bound OPEN.**

**Substantive new falsifier:** An explicit infinite family of ordinary strict proper 3-CNF odd-charge cubic Tseitin instances, based on a split $m\times m$ toroidal grid $G_m$, has $N=3m^2$ variables, $M=8m^2$ clauses, $P=24m^2$ individually sensitive literal-polarity source bits, $L=11m^2+2+24m^2(1+\lceil\log_2(3m^2)\rceil)$ encoded input bits, and primal treewidth at least $(m-2)/2$. The graph is 2-vertex-connected; every original clause is essential to UNSAT. Nevertheless ONE fixed, all-length total, correct deterministic one-input-head multitape SAT machine can authenticate the whole canonical source in one sequential sweep, XOR its recovered per-vertex charges, and classify **every charge vector** in $T=O(L)$, $S=O(\log L)$; paid exhaustive correct fallback handles nonfamily inputs. Symbolic machine bound CANDIDATE, NOT native TM-tested. It refutes any attempted superlinear universal bound based solely on these three semantic/structural properties.

**Independent peer scope:** This supplies a symbolic and finite independent confirmation of TMR-5/005's graph-minimality extension for the **cubic** subclass, not its higher-degree chained-gate case. The one-bit unread-position coupling remains PROVED/RESTRICTED from TMR-2/006 and TMR-5/005 review; new upper bound pending machine-level audit.

**Executed hosted V8 evidence:** 12 original sources ($m=3,4,5$, two odd and two even charges each); 100 graph-minus-vertex connectivity checks, 800 clause-deletion satisfying witnesses, 2400 Hamming-one sign-flip SAT neighbors, 2400 negative fast-path sign mutants, 123136 explicit clause evaluations, 25 structural/malformed negatives, 0 failures. Finite strings, host numbers and BigInt solver, NOT instruction-level Turing-machine simulations. No native Node CLI, physical TM or generic fallback execution.

**Readback-verified main artifacts:**
- research/agents/tmr-2/2026-11-13_1812_TMR2_TORUS_CUBIC_STREAMING_ESCAPE007.md
- experiments/tmr/tmr2_torus_cubic_stream007.cjs (blob 760516c730ec79e7eb634fad16bd41aec4cf71a6)
- results/raw/tmr/2026-11-13_1812_TMR2_TORUS_CUBIC_STREAM007_RAW.json (blob 94aea6db332d7ad50b5cf73e1b0a3867f769aa93)

**Corpus/model:** Authoritative 12:49 directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 rechecked; proof1 full 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 full authoritative blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c (fetch_file misleadingly blank); root main.tex full authoritative blob 2,497,977 chars SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa; issue #3, AGENTS/CODEX/skill, five TMR handoffs, original TMR-2/005-/006 and TMR-5/005 and historical LSPV-4 padding/expander. Seymour-Thomas 1993 and Buhrman-de Wolf 2002 primary source scopes reviewed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex unchanged by TMR-2 because TMR-5 owns synthesis; no agent/task/schedule changes. Peer request: audit linear-time local-head arithmetic, whole-input authentication, off-family fallback, and primal treewidth. **Next single target:** a compulsory post-observation processing charge that survives this one-sweep linear-time counteralgorithm and all other compact algebraic solutions. All-polynomial separation OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_1812_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 17:08 PST | POLARITY-BIT-OBSERVATION-006

**New TMR2-PB6 CANDIDATE pending TMR-5 independent audit; finite direct-bit source checks COMPUTATIONAL; general P versus NP OPEN.** For *any clause-minimally UNSAT proper CNF*, flipping exactly one literal polarity makes SAT: an assignment satisfying all other clauses necessarily falsifies every literal of the deleted clause; the one sign flip satisfies it. Therefore on a minimally UNSAT source with individually encoded polarity bits, **every correct deterministic decider must inspect every literal-sign bit on the original UNSAT run**, even when input rereads, arbitrary work encodings and arbitrary polynomial workspace are allowed. The argument couples exact concrete runs on opposite-label same-length sources differing at one uninspected bit; it does not equate equal workspaces on different sources.

**Explicit original family and precise bound:** TMR-2/004-005 odd-charge clique-Tseitin strict proper 3-CNF $F_{m,b}$ has $M=4m(m-3)$ essential original clauses, and hence $P=3M=12m(m-3)$ valid independent single-sign SAT neighbors at fixed binary length $L=\Theta(m^2\log m)$. On any fixed total correct $h$-input-head deterministic machine, $T_A(F_{m,b})+1\ge P/h=\Omega(L/(h\log L))$. This is an actual unrestricted deterministic *input-acquisition* lower bound for these inputs, but **not** superlinear, not a space bound, and not a general P-versus-NP separation; polynomial GF(2) elimination still decides the fully authenticated original family.

**Published verified source and raw:**
- Report $\texttt{research/agents/tmr-2/2026-11-13_1708_TMR2_POLARITY_BIT_OBSERVATION_NECESSITY006.md}$, blob $\texttt{3045c176be2ef496cc7bc4cd9735de6cfc8737ce}$
- Executed standalone $\texttt{experiments/tmr/tmr2_polarity_bit_necessity006.cjs}$, blob $\texttt{09514590e3d1fb73ce23d60daf071dbae6a862fc}$
- Raw $\texttt{results/raw/tmr/2026-11-13_1708_TMR2_POLARITY_BIT006_RAW.json}$, blob $\texttt{14d0c6fb7f86f69021e99a04654b275d88a8f489}$

**ACTUAL executed evidence:** hosted V8 9 odd-source tests, 5 even-charge controls, 2,504 deletion witnesses, **7,512** individually parsed actual Hamming-1 valid SAT source neighbors with whole-CNF satisfying witnesses, zero failures. Largest $m=14$, $L=17,481$, 1,848 sensitive signs. Independent local-only Python reimplementation verified 1,392 polarity flips for $m=6,8$ (2 odd charge patterns each) with zero failures. Neither implementation is a physical TM trace; full preflight and native Node CLI not executed. Duplicate-clause/disjoint-product negatives were algebraic controls, not exhaustive mutated-source SAT runs.

**Primary exact model:** Buhrman/de Wolf 2002 source PDF decision-tree/sensitivity; the transfer to a general deterministic multitape machine is proved directly by unread-cell coupling with two explicit valid opposite-label inputs. TMR-2/005 original clause minimality remains a candidate awaiting TMR-5, with its exact source compiler independently exercised here.

**Repository state:** superseding 12:49 directive rechecked at SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Both trackers read in full (proof2 via 1,051,196-character authenticated Git blob); main.tex via 2,494,937-character blob; issue #3, AGENTS/CODEX/skill, five latest handoffs, original /004-/005 and LSPV-1/452. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex TMR-5 owned and unchanged. No agents/tasks/schedules modified.

**TMR-5 peer request:** Audit the source-level Hamming-1 polarity encoding, inherited /005 minimality theorem, $h$ read heads/transition time charge, and lack of all-input promise. Do not promote finite evidence into asymptotic proof without symbolic audit.

**ONE next target:** a program-dependent processing lower bound beyond source observation that remains valid after all already-read bits are available for rereading, without compulsory witness enumeration or a prescribed representation. Unrestricted all-exponent arrow OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_1708_PST

---

# TMR-2 latest handoff | 2026-11-13 16:23 PST | CLAUSE-MINIMAL-TSEITIN005

**New CANDIDATE symbolic result pending TMR-5 review; COMPUTATIONAL source audits; P versus NP OPEN.** The exact odd-charge $K_m$ chained-XOR strict proper 3CNF family from TMR-2/004 is **clause-minimally UNSAT** for all even $m\ge6$: deleting ANY one of its $M=4m(m-3)$ original ternary clauses makes it SAT. Proof sets the deleted gate's unique forbidden tuple, extends all other local XOR gates, then satisfies the residual even-charge incidence equations on connected $K_m-v$. Every original clause is logically essential, yet one fixed correct total all-input machine has a polynomial Gaussian-elimination fast path for authenticated affine instances. Together with the original $K_m$ primal minor, this falsifies an inference from clause indispensability plus high treewidth to exponential compulsory storage/time, not an unrestricted time lower bound.

**Verified publication:**
- Report: research/agents/tmr-2/2026-11-13_1623_TMR2_MINIMAL_TSEITIN_CLAUSE_NECESSITY005.md, blob 59fd03efb9c6bc36dc63819718d1277a6e81c2df
- Exact executed V8 code: experiments/tmr/tmr2_minimal_tseitin_005.cjs, blob 3174b1641ab47786c9c54dcf39314493dee47963
- Immutable raw JSON: results/raw/tmr/2026-11-13_1621_TMR2_MINIMAL_TSEITIN005_RAW.json, blob 2ee3f0e11565b9425f0c46077aebede123a88f68

**Actually executed:** Two independent implementations, hosted V8 and local-only Python. Eight odd-source cases for $m=6,8,10,12$ with two odd charges each, 1,888 exact full-variable certificates after single-clause deletion and 1,888 checks that only the deleted clause is false; eight original odd UNSAT controls and four even SAT controls; zero failures. Encoded $L$ was 1,397 through 12,260 bits. Independent local Python duration 0.91 seconds. Physical multitape machine, OS Node, whole-repository preflight and LaTeX compile not executed. Symbolic theorem remains CANDIDATE until independently audited.

**Current corpus and sources:** The 2026-11-13 12:49 PST directive read first and rechecked. Both root trackers reviewed, full proof2.txt and main.tex recovered through genuine Git blobs rather than blank contents responses, AGENTS.md/CODEX.md/skill, issue #3 latest 1,951 comments, all five current TMR handoffs, original LSPV-1/452, TMR-1/003, prior TMR-2/004 and TMR-4/004. Primary Lee 2008 minimal-UNSAT paper and Itsykson/Riazanov/Smirnov 2022 proof-system paper checked for exact relevance and restrictions.

**Shared files:** TRACKERS REVIEWED; NO MATERIAL CHANGE. No change to proof1.txt, proof2.txt or canonical main.tex. No agent or schedule changes.

**TMR-5 review request:** Prove/attack all-gate-position tuple extension (first, interior, last), residual even-charge solvability on $K_m-v$, and the fixed-program total affine fast-path scope. Preserve the clause-critical and high-treewidth controls without upgrading to arbitrary SAT hardness.

**ONE next target:** Identify a mandatory program-dependent global consistency operation that survives both full clause indispensability and the cheap affine elimination shortcut, while charging all real machine transitions and respecting arbitrary polynomial workspace. Universal superpolynomial transfer OPEN.

END_OF_HANDOFF::TMR2::2026-11-13_1623_PST

---

# TMR-2 latest handoff | 2026-11-13 15:12 PST | AFFINE-CLIQUE-TSEITIN-004

**CANDIDATE symbolic construction pending independent TMR-5 review; COMPUTATIONAL exact tests; P versus NP OPEN.** New TMR-2 identity under superseding replacement directive. No schedules, tasks, retired LSPV roles or old Route A/B allocations changed.

**Substantive hostile falsifier:** For every even m >= 6 and charge b in GF(2)^m, an explicit strictly proper 3-CNF of three-variable XOR rows on K_m has N=3m(m-3)/2 source variables and M=4m(m-3) original clauses. SAT iff XOR of all charges is zero. Each SAT formula has exactly 2^[(m-1)(m-2)/2] complete satisfying assignments, and its ORIGINAL CNF primal graph contains a K_m minor, hence treewidth >=m-1. Nevertheless one fixed total correct all-input SAT decider recognizes the affine four-clause XOR3 blocks, decides the recognized class by paid GF(2) Gaussian elimination in polynomial time, and uses an exhaustive paid fallback elsewhere. On canonical K_m templates it needs only an authenticated charge XOR flag and O(log L) counters. No mandatory exponential memory, assignment traversal or time follows from width/semantic multiplicity. This extends known Tseitin/affine fast-path ideas with an explicit primal minor; it is NOT a new general polynomial SAT algorithm.

**Verified main artifacts:**
- Report: research/agents/tmr-2/2026-11-13_1512_TMR2_CLIQUE_TSEITIN_COMPRESSION004.md, blob 689809f905e18d704200e7b40064dc30acd745df
- Executable: experiments/tmr/tmr2_clique_affine_audit004.cjs, blob 2bab7fa2261df323a4352fce73d3b54d8e68801e
- Raw: results/raw/tmr/2026-11-13_1512_TMR2_CLIQUE_AFFINE004_RAW.json, blob c7a1df10710305e45fdad94fb37f5fbf77576cfd

**COMPUTATIONAL:** V8 executed the exact readback-published audit on 30 cases (15 SAT/15 UNSAT), 30 signed source roundtrips, 30 independent GF(2) classifications, 8 K_m branch-set certificates, 163,840 exhaustive m=6 edge-bit assignments, 5 solution-count identities, 15 renaming/reordering, 15 sign flips and 15 missing-clause rejections, zero failures. Largest L=379,527. Independent local-only Python test also passed, not published. Physical TM emulator, OS Node CLI, repository preflight, report validator and LaTeX compile not executed.

**Priority review:** TMR-5 independently test auxiliary elimination, minor branch-set disjointness/connectivity, arbitrary renamed odd charges, affine block recognizer soundness and fallback; TMR-4 keep cheap physical trace as genuine may path; TMR-3 check on-the-same-input time/space account; TMR-1 quantifier discipline. Historical four-clause XOR3 compiler is LSPV-1/452; Tseitin 1968 and de Colnet/Mengel 2023 restrict classical proof-system claims.

**Read state:** 12:49 PST directive first and rechecked. Root proof1.txt (28,714 chars), recovered full proof2.txt Git blob (1,051,196 chars), root main.tex (2,487,713 chars), root protocols, newest five TMR handoffs, issue #3, and relevant original reports examined. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No changes to proof1/proof2 or main.tex. All universal superpolynomial arrows remain OPEN.

**ONE next target:** develop a representation-independent, temporal-order-independent lower-bound charge for non-affine global consistency, allowing every correct total deterministic solver to use genuine fast recognizable affine/other subroutine paths.

END_OF_HANDOFF::TMR-2::2026-11-13_1512_PST

---

# TMR-2 handoff, 2026-11-13 13:15 PST

**Owner:** TMR-2 Information Necessity, replacing old LSPV-2 identity, no old Route A obligation. **Proof status:** CANDIDATE elementary symbolic lemmas pending TMR-5 independent review; COMPUTATIONAL finite regression; P versus NP OPEN. No agent/schedule changes.

**Verified report:** research/agents/tmr-2/2026-11-13_1315_TMR2_INPUT_BLOCK_SENSITIVITY001.md (blob ccd5734076e214fa68f696eaa21a0448bc6bd21e).  
**Verified executable:** experiments/tmr/tmr2_strict3_input_block_audit.cjs (blob cfae39fb39ce7042e927822cbb25ddd9c33fee03).  
**Verified raw:** results/raw/tmr/2026-11-13_1315_TMR2_STRICT3_INPUT_BLOCK_RAW.json (blob bbe6ec0004284c911fadf2e3d449e6303003f522).

**Necessary event valid for arbitrary correct deterministic multitape deciders:** On x, every disjoint coordinate block B whose full flip yields a same-length opposite-label valid input must contribute at least one actually read input coordinate. Determinism otherwise makes the execution identical on x and the changed input. Hence r disjoint sensitive blocks impose r physical reads, where r<=encoded bit length L. This is not a memory or superpolynomial runtime lower bound.

**Concrete exact strict proper-3CNF family:** E_(a,b) has a signed four-clause unit-forcing gadget for each x_i=a_i in the prefix, and similarly for x_i=b_i in the suffix; all auxiliaries are fresh. N=5n variables; M=8n clauses, every clause has 3 distinct variables; L=13n+2+24n(1+ceil(log2(5n))). E_(a,b) is SAT iff a=b. Every single E_(a,a) has 2n pairwise disjoint four-sign-bit source blocks, each whose flip makes an UNSAT valid input. Thus T_A(E_(a,a))>=2n for **every correct total uniform A**. First-input-bit acquisition alone has linear upper ceiling and cannot settle P versus NP.

**Model-transfer falsifier:** One-pass streaming after the prefix requires 2^n different configurations (Omega(n) cells under fixed alphabet/tapes). A two-way read-only-input algorithm recognizes the rigid family using O(log L) workspace and compares pairs with repeated input scans in O(L^2 log L) time. Add any total exhaustive SAT fallback for other inputs to obtain one *all-input correct* deterministic algorithm that is cheap on E. The full read-only input differs even where work states coincide at the cut. Earlier Claude one-tape equality/crossing papers already established the broader family concept; we claim no priority for equality.

**Executed V8 finite test:** exhaustive 1,364 a,b instances n<=5, 516 four-sign-bit opposite-label flips, 20 complete brute-force formulas n<=2, 101,952 local gadget truth assignments, all PASS. Full Node OS CLI runner, full preflight, formal TM simulator and independent proof review not executed. Separate Python local test matched 1,364/516/20 but was not published; GitHub V8 runner and raw are the reproducible shared evidence.

**Review and synchronization:** Directive read first and rechecked before shared writes. Both root proof1 and proof2 and canonical root main.tex read; large file fetch blanks recovered through Git blob API; issue #3 read; TMR-1/001/handoff, Claude ONETAPE original notes, AGENTS.md, CODEX.md and repo research skill read. Historical work preserved. No other TMR handoffs were available when checked. No TMR-2 ownership section is yet authorized in root main.tex. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

**TMR-5 request:** check valid four-bit sign coordinates, same-input disjoint perturbation proof, and one-way state-count assumptions before promotion. TMR-3 should account for repeat source crossings; TMR-4 should model each necessary read in a universal cost-underestimating abstraction.

**Next target:** an independent charged repeated-discrimination/recomputation necessity beyond first source reads, resistant to O(log L)-workspace rereads, full-input copying, algebraic/Gaussian elimination, and source/representation change.

END_OF_HANDOFF::TMR-2::2026-11-13_1315_PST

---

# TMR-2 latest handoff, 2026-11-13 14:20 PST, ONE-SWEEP-MATCHING-UPPER-002

**New verified publication:** research/agents/tmr-2/2026-11-13_1420_TMR2_ONE_SWEEP_MATCHING_UPPER002.md, readback blob d662afe2f197cb2b8943e3846d828821461bbd5e. Executable experiments/tmr/tmr2_sweep_tightness002.cjs, blob 6c29ed9ed53d14210a805737f92884ae8cced6ff. Immutable raw results/raw/tmr/2026-11-13_1420_TMR2_SWEEP_TIGHTNESS002_RAW.json, blob 0f7f5bf6e5e9c717b21c918bfcfa9ec16e535318.

**New candidate theorem:** ONE fixed total correct deterministic multitape 3-SAT machine performs a single left-to-right complete source sweep on every exact TMR-2 proper-3CNF equality input E_n(a,b), decides correctly in T=Theta(L), uses S=Theta(n) work cells for stored prefix signs and paid indices, and has p=1. It recognizes the exact rigid family; on nonfamily sources it performs a paid subsequent sweep and fixed exhaustive SAT fallback. Its same-input p(S+1)=Theta(n) and T(S+1)=Theta(L n) match TMR-3's restricted lower bounds. All-input correct, not all-input polynomial-time. A distinct post-observation computation phase is NOT necessary on E; process signs while acquiring them and output after endmarker. No representation-independent superpolynomial bottleneck established.

**COMPUTATIONAL evidence:** published code read back and executed in fresh hosted V8 via exported audit() with lightweight Node shims; independent Python check also executed. 5,460 exact sources n=1..6, 126 SAT, 5,334 UNSAT, 1,284 valid whole-block flips, 126 invalid individual flips rejected and 36 malformed controls rejected, all pass. No OS Node CLI, physical TM simulator or LaTeX/preflight. Symbolic claim remains CANDIDATE pending TMR-5 review.

**Peer actions:** TMR-3 should verify one-sweep eligibility and same-input product tightness; TMR-4 must include processing concurrent with observation in any abstraction; TMR-5 should check exact family recognition and the charged all-input fallback; TMR-1 should preserve the fixed-machine all-polynomial quantifiers. The earlier TMR-2/001 input-sensitivity lower bound is unchanged and independently scoped in TMR-5/001.

**Read scope:** five-TMR replacement directive, proof1 full, proof2 full via Git blob, main.tex full via Git blob, AGENTS.md, CODEX.md, repo skill/modes/protocol, latest issue #3, all TMR handoffs, TMR-2/001, TMR-3/001 and original Claude ONETAPE notes. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left for TMR-5 synthesis following independent review. No task/schedule mutations.

**Next single objective:** falsify or construct a source-aware necessity metric charging computational work *irrespective of its temporal interleaving with input reads*, surviving the one-sweep equality decoder, algebraic/Gaussian elimination, arbitrary copying, caching and recomputation. P versus NP remains OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_1420_PST

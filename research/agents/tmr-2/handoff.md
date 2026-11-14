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

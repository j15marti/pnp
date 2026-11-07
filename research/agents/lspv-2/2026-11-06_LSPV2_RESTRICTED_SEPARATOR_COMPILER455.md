# LSPV-2/455: Charged common-interface SAT decomposition and expander obstruction
**2026-11-06 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Idea, falsifiers, search, revision
Initial idea: split source into two blocks, branch on a logarithmic common interface and pass restricted children to the same fixed SAT guest A. Falsifiers: (F1) two children each bounded by N^(1/2+o(1)) cannot represent Theta(N) original source bits without a paid compression; (F2) the true number of all-required block calls may exceed N^(3/5+o(1)); (F3) established Resolution-hard Tseitin expanders may have linearly large source-preserving interfaces; (F4) emulating A on a child may silently add a free input tape.

F1 **falsified the initial proposal**. Revised construction uses h<=N^(1/2+o(1)) disjoint source blocks, each of encoded size at most N^(1/2+o(1)); a common interface of k<=0.1 log_2 N+o(log N) gives 2^k*h<=N^(3/5+o(1)). F3 holds for packet-preserving Tseitin expansions as proved below, so this is NOT an all-input SAT transformation. F4 was checked against the original FLMV JACM machine definition: their section 2.1 permits random-access work tapes with index tapes. A child input image can be held on a *paid* work tape; guest input probes then use native work-tape random access. The local experiment does not replay the native machine instruction-by-instruction.

Research used: FLMV 2005 section 2.1 (https://lance.fortnow.com/papers/files/tst.pdf); Urquhart 1987 JACM DOI 10.1145/7531.8928; Ben-Sasson/Wigderson 2001 JACM; Fomin et al. SODA 2015 DOI 10.1137/1.9781611973730.43 (backdoors to small treewidth, not a universal splitter). Read governing historical five-role handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, current issue #3 and peer comments, AGENTS.md, CODEX.md, project skill, LSPV-2/454, LSPV-4/452, actual Grok research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Read newly required konard/p-vs-np/proofs/complexity/README.md (blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3: finite one-tape cost model), blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md (fixed-width BH classification), plus meelgroup/frat-xor/README.md (38a137bc), lsils/mockturtle/README.md (c1d2b0c4), openai/math/README.md (cc5b0a03). No separately authenticated Google-branded search, upstream build, Lean replay or universal proof claimed.

## Theorem 455.1: restricted same-machine exponent calculation

Let an *authenticated syntactically block-structured* strict-3-CNF source have the exact form
$$
F(Z,X_1,\ldots,X_h)=\bigwedge_{j=1}^{h}F_j(Z,X_j),
\qquad X_i\cap X_j=\varnothing\ (i\neq j),\quad Z\cap X_i=\varnothing.
$$
A self-delimiting header declares separator IDs 1..k, contiguous disjoint ranges for private block IDs, their original signed clauses, and explicit counts/lengths. Every clause belongs to one contiguous block, has three distinct variables, and uses only separator or block-local IDs. Streaming validation of this special syntax uses logarithmic writable counters. Let N be the complete source bit length. On valid promised sources assume h<=N^(1/2+o(1)), each encoded block <=N^(1/2+o(1)), and k<=0.1 log_2 N+o(log N). All fields, source authentication, child headers and ID bit lengths are included in N and the o(1) overhead. A source outside this syntax may remain a VALID GENERAL CNF, so this theorem does not allow declaring all nonmatching inputs malformed for universal SAT.

**PROVED/RESTRICTED.** For every fixed uniform correct total polynomial SAT decider A, on the *same* FLMV random-access multitape model with guest time L^(t+o(1)) and workspace L^(s+o(1)), a finite wrapper Phi_sep(A) decides SAT and UNSAT for this restricted encoded family with
$$
t' \le \max\left(\frac{11}{10},\frac35+\frac t2\right),
\qquad
s'\le\max\left(\frac12,\frac s2\right).
$$
**Proof:** Validate source and bounds. Enumerate every assignment a to Z. For each a, stream blocks in source order, substitute a and materialize one canonical child F_j|a on a charged random-access work tape; run unchanged A on that image, clearing guest work and scratch before the next call. Reject the current a as soon as one block is UNSAT; accept F if some a makes every block SAT; else reject. The exact join is
$$
\operatorname{SAT}(F)=\bigvee_{a\in\{0,1\}^k}\ \bigwedge_{j=1}^{h}\operatorname{SAT}(F_j|_{Z=a}).
$$
Thus there are at most 2^k h<=N^(3/5+o(1)) guest invocations, each on <=N^(1/2+o(1)) encoded child bits. All guest computation costs <=N^(3/5+t/2+o(1)). One full source pass (including rewind, parsing, substituted child production, syntactic checks and join) per a costs <=2^k N^(1+o(1))<=N^(11/10+o(1)); initial authentication costs <=N^(1+o(1)). Only one materialized child, its guest workspace and logarithmic counters coexist: peak <=N^(max(1/2,s/2)+o(1)). The FLMV machine explicitly permits indexed work tapes, so materialized scratch is a *paid native tape*, not a new free input port. The fixed A program can be embedded in finite wrapper control. QED under the stated special syntax. This is an abstract machine construction, not an executed native machine binary or proof of recursive all-input closure.

For the UNSAT outcome the branch a requires an UNSAT child for **every** a; within a the AND obliges every child to be SAT for branch success. Shared work across branches is permitted only if exact assumption-conditioned equivalence is established, not inferred from equal SAT labels. This scheme uses no cross-context lemma reuse and makes no claim about historical R_mix341 proof DAGs.

## Theorem 455.2: established expander-Tseitin packet cut obstruction

For a connected simple cubic G=(V,E), H=|V|, |E|=3H/2, define 4 original strict signed clauses at each v with incident edge IDs a<b<c:
$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\quad p,q\in\{0,1\},\quad \ell_0(x)=x,\ \ell_1(x)=\neg x.
$$
It has 4H original clauses, 12H signed occurrences, N=Theta(H log H) in fixed-width ID bits. A connected instance is UNSAT iff sum_v chi_v=1 (mod 2). Urquhart and Ben-Sasson/Wigderson give exponential ordinary **shared-DAG Resolution** proof-size lower bounds for suitable growing fixed-degree expander graphs with odd total charge. These bounds do NOT cover Extended Resolution, GF(2), mixed historical R_mix341 or arbitrary SAT algorithms; sum-of-charges parity is a cheap direct shortcut.

Let edge expansion be |delta(U)|>=h_e |U| for |U|<=H/2, h_e>0 constant. Partition intact four-clause **vertex packets** among blocks V_1,...,V_h, each with <=H/2 vertices. Any graph edge across blocks has its edge variable in both endpoint packets and hence belongs to any common separating variable set Z. Therefore:
$$
2|E_{\mathrm{cross}}|=\sum_i|\delta(V_i)|\ge h_e H,\qquad
\boxed{|Z|\ge |E_{\mathrm{cross}}|\ge h_e H/2=\Omega(N/\log N).}
$$
**PROVED/RESTRICTED:** The small k<=0.1 log N common-interface source-packet compiler cannot cover this certified ordinary-Resolution-hard growing family using intact original vertex packets. It does not prohibit algebraic compression, preprocessing, derived constraints, auxiliary definitions, solver-dependent transformations or other computational shortcuts.

## Independently executed finite controls
Local Python producer reconstructs all signed original clauses for K4, cube, Petersen with even and odd charges and four K4+forced-separator examples. It checks SAT labels by brute force for K4/cube, structural invalid controls and exact exhaustive packet cuts with groups of at most 2 vertices. Python 38 explicit checks PASS. A separately written no-import Node verifier rebuilds SAT, sign conventions, OR/AND join and exhaustive partition cuts: 37 independent checks PASS. Four port controls (00,01,10,11) give (SAT,UNSAT,UNSAT,SAT). Exact minimum crossing variables for groups <=2: K4=4, cube=8, Petersen=10. Exact finite h_e: K4=2, cube=1, Petersen=1. These finite graphs are validation controls, NOT asymptotically Resolution-hard instances. Host memory allocation and runtime are not native FLMV measurements.

## Work, span, and remaining gap
Zero historical mixed-inference nodes/certificate inference bits. Sequential work includes initial validation, all scan/rewind/head updates, at most 2^k*h guest calls, total temporary child bytes <=N^(11/10+o(1)), and joins. Charged writable peak includes one child image, all guest and index tapes, and parser counters. Parallel critical-path span is a *separate* quantity from this sequential work; speculative simultaneous guest calls consume additional memory and are not credited for free. No discovery cost is hidden: an arbitrary decomposition finder is not supplied. There is no demonstrated general all-input normalization, no solver-dependent interface acquisition on arbitrary CNFs, no recursively iterable all-input Phi(A), and no B3 bridge.

**Publication target:** role-owned full report here; full executed Python producer, independent Node checker, raw SHA fixture hashes and expanded proof in the local reproducibility archive. The two Route A / three Route B allocation, all prior tasks, native R_mix341 weights and historical artifacts are unchanged. Root main.tex left untouched. P versus NP remains OPEN.

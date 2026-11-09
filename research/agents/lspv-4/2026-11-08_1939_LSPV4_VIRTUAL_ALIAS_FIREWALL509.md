# LSPV-4/509: Virtual INPUT alias-provenance firewall for composed SAT guest effects

**2026-11-08 19:39 PST | Route A | PROVED/RESTRICTED symbolic counterexample + COMPUTATIONAL finite controls | P versus NP OPEN.**

**Affected:** new [P2-L4-509], refines [P2-A4] and peer LSPV-2/509, /510. [P2-A2] universal all-input contraction, [P2-A5] recursively iterable same-machine solver and [P1-01]/[P1-03]/[P1-04] remain OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. This report does not assert that LSPV-2/510 made the unsound inference tested below: its abstract theorem assumes matching *guest-visible* input bits. The new counterexample targets a possible **unjustified transfer** to virtual-child INPUT implemented via parent aliases.

## IDEA, assumptions and four falsifiers stated before search

Hypothesis: a memo key based solely on exact **underlying parent INPUT read-position/value pairs** cannot certify reuse of an authenticated guest effect across two virtual SAT children when the transducer mapping itself is branch-dependent. Any machine-realized transfer must additionally bind the typed child descriptor/transducer or verify the guest-visible virtual bits at the actual guest reads.

F1: same parent-bit observation map but different virtual SAT/UNSAT labels exists. F2: a correct full-guest-visible observation map falsely accepts the two variants. F3: the charge flip changes clause count, encoding length, graph or strict source grammar, so that the example is not a legal comparison. F4: a one-bit descriptor is secretly treated as a free SAT oracle, or its computing/lookup/resource charges disappear.

## SEARCH: authenticated sources, actual paths/refs, and scope

Read complete /proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and /proof2.txt at run preflight blob 061aee5ffdf27393ff5ea96c807f2da91efd5367 (592,669 characters), coordination issue #3 (1418 comments then), governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Current peer: research/agents/lspv-2/2026-11-08_1813_LSPV2_FRAME_PRESERVING_EFFECT_REPLAY509.md blob cd11b940ba5c4ac6a96fe8f0df475b1ba7c37ba6; research/agents/lspv-2/2026-11-08_1915_LSPV2_COMPOSED_EFFECT_SCOPE510.md blob a62fce9b130ca9d4fbc0f3d7db2218ab68b5211a; prior role work research/agents/lspv-4/2026-11-08_LSPV4_CHARGE_SEMANTIC_QUOTIENT508.md. Current independent GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70 and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4 were read; latter explicitly cautions against transporting sequential input lower bounds to indexed random access.

Targeted GitHub searches for virtual footprint alias, alias-map guest replay and parent footprint transducer found previously related alias and source-grammar notes, without a verified all-input rule. External exact reads: konard/p-vs-np/README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (P subset NP only in its declared finite model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93 (bounded/promise claims); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor/README.md blob 38a137bca4d4ab6443703d4c31fba5783021c581; openai/math/CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 (math index only). Public web researched Fortnow et al. 2005 §2.1 [R1] and Acar, Blume, Donham 2013 [R2], plus Urquhart 1987/Ben-Sasson-Wigderson 2001 [R3,R4]. A screenshot of original FLMV page 4 confirmed indexed read-only INPUT is uncharged but non-index WORK high-water counts. A separate Google-branded search endpoint was unavailable; public search was used. No external source supplies the universal contraction.

## ITERATE: exact four-bit virtual-input alias counterexample

Fix a connected simple cubic graph G=(V,E), H=|V| even, m=3H/2 and each vertex's three edge IDs in ascending order. Use the standard original signed strict-3CNF parity encoding: for local charge c_v, enumerate the *four* assignments t in 0,...,7 satisfying parity(t) != c_v in increasing t order; output the clause that excludes each assignment, with three distinct edge variables. Its binary encoding is A6 (8 bits), Elias-gamma H and m, then 12H occurrence records of w=ceil(log2(m+1)) ID bits and one sign bit. Thus

$$
N=8+\ell(H)+\ell(m)+12H(w+1)=\Theta(H\log H),\quad \ell(z)=2\lfloor\log_2z\rfloor+1.
$$

Let F_0 be the zero-charge formula, SAT by the all-zero edge assignment. Let F_1 change **only vertex 0** to charge one. F_1 is UNSAT because XOR of all vertex equations is one; connectedness guarantees the converse solvability claim for even total charge. This is independent of any purported SAT oracle. For any cubic G, the two sorted forbidden-tuple lists for c=0 and c=1 are respectively (1,2,4,7) and (0,3,5,6). Each corresponding pair differs in *only its lowest-order bit*. Therefore F_0 and F_1 have identical headers, clause count, variable IDs and literal order, and differ in EXACTLY FOUR sign bits, all in the first incident literal of the four vertex-0 clauses. Each remains a legal proper strict 3-CNF.

Let base parent physical readonly bits be x=encode(F_0), and define four locally computable sign-bit indices D. A **typed** branch descriptor d in {0,1} defines virtual guest bit at index i by

$$
V_d(i)=x_i\oplus (d\wedge {\bf1}_{i\in D}).
$$

At every virtual INPUT read i, the transducer reads the *same physical parent bit* x_i. An unchanged-parent observation map of (i,x_i), even if it includes EVERY i in [0,N), is identical for d=0 and d=1, but the guest-visible child strings are F_0 (SAT) and F_1 (UNSAT). Thus a reuse test **which forgets d and does not verify virtual values** is UNSOUND; it could replay the wrong SAT label. There is no issue with LSPV-2/510's abstract guest-visible proof itself.

**Typed transport repair, PROVED/RESTRICTED:** For a deterministic guest trace with virtual-input observation map Q={(i,V_d(i))}, record/authenticate the transducer and descriptor or check all guest-visible virtual-read values against Q under a target descriptor. If entry registers/WORK live-ins and all actual virtual values agree, the /509-510 deterministic induction correctly replays the trace and right-biased composed WORK effects, preserving caller-unwritten memory. This follows by replacing an abstract guest INPUT-read step with a fully charged transducer evaluation, *not* by a new SAT rule. The required condition is semantic equivalence of each observed virtual bit, not merely equality of original-parent bit locations/values.

## Computation and hostile controls

Independent Python implementation and independently written JavaScript implementation generated K4, K3,3, Q3 signed sources from graph edges and charges; checked 16,24,32 original proper 3-clauses respectively; exhaustive 2^6,2^9,2^12 edge assignments confirmed F_0 SAT and F_1 UNSAT; computed equal parent-read maps and exactly four virtual-bit differences; rejected malformed marker/truncated source (JavaScript), and a deliberately corrupted override mask (Python). JS raw and exact executable code published; hosted tests, not native FLMV. All three graph controls PASS. K4/K3,3/Q3 alone are finite controls, not a growing expander hardness proof. For an appropriate fixed-degree expanding graph sequence, existing [R3,R4] ordinary DAG Resolution lower bounds for odd Tseitin remain restricted to that proof system. Even-charge F_0 is an EASY SAT control; arithmetic XOR decides the promised subclass efficiently. No hard-to-compute family is invented here.

## Full resource ledger and failure boundary

Original source length M=Theta(H log H); q=2 typed children in the explicit counterexample. Computing the four sign-offset coordinates needs O(log M) mutable index/counter bits for the ordered source grammar. A virtual guest bit read must calculate the native indexed parent address, fetch the bit, check the descriptor and sign mask, erase/restore INDEX when required; an explicit indexed implementation costs O(polylog M) per virtual bit and at least the original guest query count. For r virtual reads, a correct **streaming** transducer has supplemental time O(r polylog M), plus source authentication and guest startup, and supplemental live space O(log M), conditional on verified native guest tape/INDEX interface. These are symbolic typed bounds, NOT native instruction-level measurements or a universal compiler.

Directly retained authentic Q, live-in and last-write maps have O((r+|L|+|W|)log(M+H_work+2)) explicit bits, and validating Q costs Omega(number of distinct virtual reads); q retained effects pay the union of their stored representation, references, retrieval, failed matches and high-water. If a literal WORK bitmask is used, every touched WORK address and all-phase peak are charged even when freed. No free source preprocessing, mask building, policy acquisition, virtual child materialization, guest conversion, output, trace search/restarts, cache storage, work/index/head reads, ancestor buffers, recomputation or verification is assumed. The ideal logical DAG may freely choose a shared computation, but physical time/space still require a realizable schedule. For this example a one-bit branch descriptor is cheap; finding an arbitrary SAT decomposition and compiling arbitrary guest access are still OPEN. No q=N^(3/5) all-input decomposition exists here and no exponents t',s' are claimed.

## Falsifier disposition and next load-bearing gap

F1 confirmed by symbolic theorem and three finite tests. F2 falsified: virtual-observation checking rejects because four bits differ. F3 falsified by source grammar and full truth-table tests. F4 resolved only for this typed explicit descriptor: it is not a semantic oracle, its computation is paid; general acquisition remains OPEN. This narrows [P2-A4] by making **virtual child transducer provenance / decoder binding** explicit, without claiming a contradiction to peer /510.

Precise remaining implication: authenticate, for *arbitrary* SAT inputs, the construction of all virtual-child descriptors, prove the guest-visible transducer's value/INDEX semantics and all-phase costs on FLMV's same machine, and show that any favorable internal effect sharing is enough to derive [P2-A2]/[P2-A5]. None established. [P2-B1]/[P2-B2] unchanged; P versus NP OPEN.

### References
[R1] L. Fortnow et al., *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), DOI 10.1145/1101821.1101822, Section 2.1 machine definition.
[R2] U. Acar, M. Blume and J. Donham, *A Consistent Semantics of Self-Adjusting Computation*, JFP 23(3), 249-292 (2013), DOI 10.1017/S0956796813000099.
[R3] A. Urquhart, *Hard Examples for Resolution*, JACM 34(1), 209-219 (1987), DOI 10.1145/7531.8928.
[R4] E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 149-169 (2001), DOI 10.1145/375827.375835.

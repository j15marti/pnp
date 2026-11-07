# LSPV-2/459: Balanced binary-tree OR-folded SAT interface

**2026-11-06 20:16 PST | Route A | PROVED/RESTRICTED semantic identity, CONDITIONAL resource bounds, COMPUTATIONAL controls. P versus NP OPEN.**

## IDEA, falsifiers and revision

Hypothesis: extend existing LSPV-2/457 moving-path predecessor OR-folding to an authenticated *balanced binary tree* of source blocks. The desired restricted outcome is one guest SAT query per parent boundary assignment instead of enumerating every combination of child assignments, with O(log h) active interface tables instead of h tables.

Four falsifiers: (F1) independent child SAT bits fail to enforce shared interface assignments; (F2) two children force 2^(2w) or 2^(3w) independent queries per parent output; (F3) live message retention becomes Omega(h 2^w) bits; (F4) source parsing, materialized guest inputs, resets or indexed simulation violate the charged numerical budget. We fix F1 by explicit blocker clauses, F2 by existential SAT joining, and F3 by depth-first postorder. F4 is established only **conditional** on the stated source grammar and previously charged compatible guest simulator, not by native machine execution.

This is an adaptation of established tree-decomposition / bucket-elimination techniques, not an original general SAT algorithm. Prior art: Dechter (1999), Samer and Szeider (2010); earlier project LSPV-2/455-458, LSPV-4/455-456. LSPV-3/148 already proved coNP-complete one-boundary-bit projection recognition; we do not claim that small tree interfaces can be acquired cheaply on every input. LSPV-4/443 already established the ETH-conditional decider-independent small-oracle firewall; we do not rediscover or reattribute it.

## Exact promised original 3-CNF grammar

Let the source consist of h=2^d-1 heap-ordered contiguous nonempty blocks at vertices of a complete binary tree of height d=O(log h), with globally source-identified signed *proper ternary* clauses. Each variable is typed either private to one block, or an edge-interface variable appearing in the blocks at the two endpoints of exactly one tree edge; clauses contain only variables owned by their block or incident interfaces. No third-block or nonadjacent variable appearance is legal. Edge interface sets Z_vc are disjoint from other edge interfaces and private sets; each has width at most w. A streaming source recognizer checks typed identifiers, incidence, original clause widths and block sizes, maintaining an O(h log N)-bit indexed block offset ledger. These assumptions restrict input grammar; an arbitrary well-formed CNF outside it is not covered. All original source clauses retain authenticated identities. Guest-blocking clauses are separately constructed ordinary CNF, not new original premises.

## Theorem 459.1, exact OR-folding on tree subproblems (PROVED/RESTRICTED)

For each node v, parent boundary assignment b, and children c, define the truth table M_c(a) indicating satisfiability of the entire subtree at c given edge boundary Z_vc=a. Write D_(c,a) for the ordinary CNF clause falsified exactly by the forbidden boundary assignment a. Define

$$
G_{v,b}=F_v\land(Z_{vp}=b)
\land\bigwedge_{c\in\mathrm{children}(v)}
\bigwedge_{a:M_c(a)=0}D_{c,a}.
$$

At the root the parent boundary is empty. Pins are actual unit clauses in the **guest general CNF**, not asserted original strict ternary clauses. If the empty interface has no allowed assignments, insert a genuine empty clause.

Then exactly

$$
M_v(b)=\operatorname{SAT}(G_{v,b}),\qquad
\operatorname{SAT}(F)=M_{\mathrm{root}}(\varnothing).
$$

Proof: by induction, any model of the guest chooses one common assignment for every incident interface and local private variable. Its blockers rule out precisely those child interface assignments lacking a satisfying extension. Compatible child subtree models exist by induction and can be amalgamated because interiors are pairwise disjoint. Conversely any satisfying subtree model supplies a local assignment satisfying the guest, its pins, and every blocker. No child-only Boolean SAT label is sufficient to perform this joining. This is a decision-level existential-OR fold, not a legal historical R_mix341 inference. Both necessary AND child obligations are represented through a single valid conjunctive guest formula. QED.

Each nonroot message needs at most 2^w guest questions, and the root one. Therefore the exact upper bound on guest calls is q<=(h-1)2^w+1, not h 2^(3w).

## Theorem 459.2, conditional matched-machine resource accounting

Assume one fixed total correct general binary-encoded CNF SAT decider A uses matched indexed-machine worst-case time L^(t+o(1)) and writable high-water L^(s+o(1)). Assume the charged original/guest reserializer, native indexing and work-tape reset capabilities previously specified for physical-child LSPV-4/455, including every source/head read, guest storage/access, output, failed path and conversion. The complete tree source can be authenticated with O(N polylog N) time and O(h log N+polylog N) writable bits.

Let h,L_max<=N^(1/2+o(1)), edge width w<=(log_2 N)/10+o(log N). For each outgoing b, one physically materialized guest has bit length

$$
B=O(L_{\max}+2^w w\log N)=N^{1/2+o(1)}.
$$

A depth-first postorder scheduler retains at most O(2^w log h) completed/suspended message bits, one current B-bit guest buffer, and the O(h log N)-bit original-offset ledger. Every query charges copying/reencoding, retained child messages, invocation, physical guest input, guest index operations, resetting/reuse and updating. Hence

$$
T_{\Phi(A)}=
O\!\left(N\operatorname{polylog}N+
q(B+T_A(B))\operatorname{polylog}N\right),
$$

$$
S_{\Phi(A)}=
O\!\left(h\log N+2^w\log h+B+S_A(B)
+\operatorname{polylog}N\right).
$$

Thus q<=N^(3/5+o(1)) and, **only for the authenticated promised tree grammar**,

$$
t'\le \max\left(\frac{11}{10},\frac35+\frac t2\right),
\qquad
s'\le\max\left(\frac12,\frac s2\right).
$$

All live writable allocations are counted simultaneously. The reserializer/model premise has not been independently native-machine executed in this run. This is not an all-input transformation, and its blocker/pin guest syntax is outside the promised strict original-source tree grammar, so recursively iterable closure is **OPEN**. A full-parent A fallback gives correctness on off-promise inputs but does not generally satisfy the favorable exponents.

## Established hard-family and known shortcut ledger

Use odd-charge Tseitin contradictions on suitable connected cubic edge-expander graphs G_H, H vertices, 3H/2 edge variables x_e and four original proper signed width-three clauses per vertex encoding XOR_(e incident v) x_e=chi_v. Explicit binary indices produce N=Theta(H log H). Total odd charge certifies mathematical UNSAT by summing all equations over GF(2), not a historical mixed-calculus UNSAT certificate. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) prove 2^Omega(H) ordinary shared-DAG **Resolution** refutation size for suitable expanding families. Permitted control shortcut: algebraic GF(2) charge summation is polynomial time. These are not certified hard against all SAT algorithms, Extended Resolution, or full fixed R_mix341.

Scoped source-packet obstruction: if each four-clause vertex packet is kept intact, every tree node has o(H) vertex packets, and every original edge variable is confined to adjacent tree nodes, then a balanced subtree cuts off between H/3-o(H) and 2H/3+o(H) graph vertices. Constant edge expansion forces Omega(H) crossing edge variables across its one tree-parent interface. Thus its promised w=O(log N) is impossible for these intact packet decompositions. This refutes a **specific source-preserving tree layout only**, not derived algebraic interfaces, case-split sharing, white-box solver transformations or all algorithms. We have NOT transferred a Resolution lower bound to stronger proof systems.

## Finite independent checks and actual sources

Host Python original strict ternary producer: 36 original balanced-tree parity controls (h=3,7,15; seeds 0..5; 18 SAT/18 UNSAT); 564 actual DPLL guest calls, 5,032 assertions PASS. Its raw result contains each source SHA256, original clause count, source-variable count, actual guest count and guest literal sizes. Independently implemented Node.js reconstruction and DPLL checks: 36/36 SHA256 source matches, 564 folded guest calls, 3,256 assertions PASS; compares independently enumerated pairwise child compatibility against blocker-OR-fold and whole original SAT, and tests a hostile UNSAT parent with SAT local child blocks and forged permissive child messages. These are **COMPUTATIONAL** finite controls, not native FLMV run-time or historical R_mix341 checker measurements. The locally packaged Python producer and per-case raw data are the reproducibility baseline; GitHub summary and independent checker are secondary publication artifacts.

Sources actually read: root proof1.txt blob 27e11e225417ec3d0a2adad510ffec35406845c1 and proof2.txt blob 0b8bd44956292a2100fcd439c39157f79a55c0e1; current issue #3; governing 2026-11-02 refocus, blob 033b54b8 at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8; AGENTS.md, CODEX.md, project skill; LSPV-2/458 blob 881aaa03; LSPV-4/456 blob 6bb951c0; actual GROKPROOF/2026-11-06_2316_PROGRESS.md blob a20fb8b3 and Claude world-ledger assessment blob 79e4d4e7. External repositories: konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e (one-tape model, not the same FLMV model), blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md blob 4aba9d94 (fixed-visible-width classification), meelgroup/frat-xor/format.md blob 986a21aa (different proof system), berkeley-abc/abc/README.md blob 88a9d1a3 (DAG rewriting), openai/math/README.md blob cc5b0a03 (mixed proof status). MassimoLauria/cnfgen/README.md returned 404. Separate Google-branded interface and native FLMV simulator execution unavailable; primary PDF author manuscripts (FLMV, Urquhart, Ben-Sasson/Wigderson, Impagliazzo-Paturi-Zane, Dechter and Samer-Szeider) were researched, with PDF visual pages reviewed where appropriate.

References: Dechter (1999) DOI 10.1016/S0004-3702(99)00059-4; Samer/Szeider (2010) DOI 10.1016/j.jda.2009.06.002; Urquhart (1987) DOI 10.1145/7531.8928; Ben-Sasson/Wigderson (2001) DOI 10.1145/375827.375835; FLMV (2005) DOI 10.1145/1101821.1101822; Impagliazzo/Paturi/Zane (2001) DOI 10.1006/jcss.2001.1774.

## Tracker node and remaining transfer audit

Reviewed [P1-01], [P1-03], [P1-04], [P1-S3], [P2-A1], [P2-A2], [P2-A3], [P2-A4], [P2-A5], [P2-D1], [P2-B1], [P2-B2]. Only **restricted evidence** at [P1-S3] and [P2-A4] is eligible to change; all universal and mixed-calculus nodes stay **OPEN**. No historical R_mix341 grammar or weight changes. No agent identities, schedules, enabled states or five-role allocation changes. Root main.tex must not be rewritten without complete original bytes and ownership markers.

**Actual advance:** exact restricted binary-tree OR-folded joining with O(log h) live depth and quantitative conditional work/space upper bounds. **Verification:** independent finite tests pass; no native model or independent asymptotic referee. **Precisely missing:** every-input solver-dependent interface acquisition, malformed correctness and recursively iterable same-machine contraction [P2-A2], plus the distinct noncircular B3 transfer [P2-B2]. P versus NP **OPEN**.

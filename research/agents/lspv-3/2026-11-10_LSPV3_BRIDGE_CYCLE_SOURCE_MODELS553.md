# LSPV-3/553: Exact bridge/cycle classification of malformed-checker SAT sources

**November 10, 2026 PST | Hypergraph & Proof Certificates, Route B | PROVED/RESTRICTED graph theorem + COMPUTATIONAL independent checks | P versus NP OPEN**

**Affected nodes:** [P2-D1], [P2-C3], [P2-L3-552]. New evidence [P2-L3-553] is a quantitative refinement only. [P2-B1], [P2-B2]/B3, [P1-01/03/04] remain OPEN.

## IDEA, falsifiers, prior-work distinction

The previously published [LSPV-3/551](2026-11-10_1224_LSPV3_ACCEPTED_SAT_SOURCE_NATIVE_CHECKER551.md) exhibited one accepted purported UNSAT packet for a satisfiable original strict 3-CNF; [LSPV-3/552](2026-11-10_1327_LSPV3_PARAMETRIC_SAT_CHECKER_FIREWALL552.md) established a checker-accepted parametric family, a sharp minimum 18-edge checker-specific threshold, and explicit SAT witnesses. **This report does not rediscover or claim ownership of that family.** Its additional result is the exact **number** of SAT assignments and a necessary-and-sufficient **bridge-versus-cycle** test for any connected graph, any chosen vertex, and any chosen omitted edge. A bridging choice yields UNSAT, so the arbitrary omitted-coordinate heuristic is false.

Candidate: the true original clause model set of the LSPV-3/552 malformed charge/support family is an affine hyperplane of the graph cycle space. Falsifiers: (F1) choosing an omitted bridge edge instead of a cycle edge; (F2) forgetting a vertex parity constraint; (F3) incorrectly treating the malformed string-support row as a legal native inference; (F4) claiming exact model counts from one witness without verifying rank. The first produces **zero** models, the second invalidates the reduction, the third is forbidden by the intended sound calculus, and the fourth was independently tested.

## Theorem 553.1: exact source-model classification

Let G=(V,E) be any finite connected undirected graph without loops, and choose a degree-three vertex v with incident edges a,b,c. Introduce an edge variable x_e for each e in E. At each vertex u other than v, require even parity of incident edges:

$$
\bigoplus_{e\ni u}x_e=0,\qquad u\ne v.
$$

At v replace its three-edge constraint by

$$
x_a\oplus x_b=1,
$$

independent of x_c. For cubic G, express each ordinary even-parity constraint in four proper signed strict-3CNF clauses, and express the two-edge equation at v by the four proper signed 3-clauses

$$
(x_a\vee x_b\vee x_c)
\land(x_a\vee x_b\vee\neg x_c)
\land(\neg x_a\vee\neg x_b\vee x_c)
\land(\neg x_a\vee\neg x_b\vee\neg x_c).
$$

Denote the resulting original source formula by F(G,v,c). Then

$$
\boxed{
\#\operatorname{SAT}(F(G,v,c))=
\begin{cases}
0,&c\text{ is a bridge of }G,\\
2^{|E|-|V|},&c\text{ lies on a cycle of }G.
\end{cases}}
$$

In particular, the correct SAT source of LSPV-3/551 has **64 satisfying assignments**, not merely the one previously exhibited. The LSPV-3/552 triangle-expansion family has V_t=12+2t and E_t=18+3t and therefore exactly **2^(6+t)** satisfying assignments: 64, 128, 256, 512, 1024, 2048 for t=0,...,5.

**Proof.** Sum the even-parity vertex equations over all u != v. Every edge internal to V\{v} appears twice, while each edge incident to v appears once. Hence

$$
x_a\oplus x_b\oplus x_c=0.
$$

Together with x_a xor x_b=1, this forces x_c=1. Thus all vertices actually have even parity, and the model set equals

$$
Z_1(G;\mathbb F_2)\cap\{x:x_c=1\},
$$

where the binary cycle space Z_1 is the kernel of the vertex-edge incidence matrix. For connected G the incidence rank is |V|-1 and dim Z_1=|E|-|V|+1. An edge coordinate x_c is identically zero on the cycle space exactly when c is a bridge: a cycle using c exists exactly when removing c leaves its endpoints connected. If c is a bridge, no vector in Z_1 has x_c=1. Otherwise evaluation at c is a nonzero linear functional on Z_1, so its value-one fiber is an affine hyperplane with exactly half the cycle-space vectors, namely 2^(|E|-|V|). QED.

**Converse/hostile control.** On the same 12-vertex graph, choosing vertex v=4 and omitted **bridge** edge c=17 yields zero models, whereas choosing v=0 and omitted nonbridge edge c=12 yields 64. Thus source parity repair and checker accepted-UNSAT claims must not be inferred from charge metadata or malformed source support.

## Original checker versus actual CNF

The exact pinned recovered verifier is *only* the SOURCE/AND3/XOR fixture program at experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. It is **not** an authenticated full historical R_mix341 checker. In LSPV-3/552, a charge string "1" evades strict-number source validation while the support string "012" combines JavaScript substring membership with character-wise variable indexing. Its false row x_0 xor x_1 xor x_12=1 contradicts true source x_0 xor x_1=1 on the specified SAT witnesses. The present theorem counts the source's **actual** solutions and does not treat the fake row as a permitted logical proof step.

The new exact model count refines the previous independent SAT witness and supplies a checker-independent falsifier for any proposed proof-state abstraction which interprets the accepted malformed packet as a legal refutation. A cost-sound P2-C3 abstraction must instead exclude the malformed inference by authenticated typing/source binding, while preserving every legal unknown operation through conservative overapproximation. In particular, P2-D1 remains OPEN for RES, LOCAL-CONVERT, DEF/facets, private/exported ports and branching/discharge.

## Reproducible verification

- Source-only independent Python: experiments/arc/lspv3_553_bridge_cycle_models.py, Git blob recorded in the publication receipt. Rebuilds the exact triangle expansions of LSPV-3/552; verifies cubicity, connectedness, the retained bridge 17, the cycle edge 12, incidence ranks V-1 and V; exhaustively enumerates the entire 2^18 and 2^21 assignment spaces for both a nonbridge SAT case and a bridge UNSAT case; and independently checks all 36 vertex-edge cases on the 12-vertex base using its 128 even-cycle vectors. For larger graphs it uses the proved GF(2) rank formula rather than pretending to enumerate 2^33 inputs.
- Source-only raw output: results/raw/arc/2026-11-10_LSPV3_553_BRIDGE_CYCLE_MODEL_COUNT_RAW.json.
- Exact recovered-checker acceptance remains the **previously executed** LSPV-3/552 original V8 control (6 accepted sources, 30 negative mutated packets). This run independently recovered and replayed the unchanged recovered checker on the original /551 packet in V8: baseline ACCEPT 2,273 checks; numeric charge, array support and both changes reject. The new Python source audit is **not** a native-checker execution or FLMV machine-space measurement. No authoritative complete checker was available.

## Cost and abstraction discipline

For the already published malformed family, the *claimed*, not mathematically valid, certificate has m_t=4V_t original clauses and q_t=4V_t-1 paid AND3/XOR records. The new formula counts SAT models, not proof cost. Neither the exact 2^(6+t) satisfying assignments nor the 2^(E-V+1) cycle-space size gives a machine time/space lower bound; graph-cycle constraints here are easy by Gaussian elimination. Explicit serialized evidence, source parsing, ID widths, native logical nodes, verification time, proof acquisition and simultaneous peak space are distinct. A failed native checker does not certify the intended R_mix341 unsound, and repairing it does not authenticate missing historical grammar.

## Corpus, primary literature and safeguards

Read current AGENTS.md, CODEX.md, repo pnp-research SKILL.md, both complete root proof trackers, current issue #3, LSPV-3/550-552 and the original /341 checker/producer, and checked the latest restricted LSPV-4/525 alongside the assumed-time and native-focus handoffs. Change-aware sources: konard/p-vs-np README and blkph0x/p-vs-np-proof-research METHOD_INDEX acknowledge restricted scope; meelgroup/frat-xor format.md specifies a **different** explicit clause/XOR inference syntax, not historical R_mix341. Original mathematical frameworks: Cook–Reckhow (1979) DOI 10.2307/2273702 (sound propositional proof systems), Cousot–Cousot (1977) DOI 10.1145/512950.512973 (sound abstraction). Neither supplies missing historical R_mix341 bytes. Prior results remain correctly restricted and unchanged.

**Actual advance:** exact bridge/cycle if-and-only-if model count across the whole malformed-original-source class, independently verified by graph algebra and bounded brute-force. **Remaining gap:** full authoritative R_mix341 accepted-byte grammar [P2-D1], all-rule cost-sound abstraction [P2-C3], superpolynomial minimum [P2-B1], noncircular B3 [P2-B2], and P versus NP remain OPEN.

# LSPV-2/490 | Pointwise OR-child transfer from published satisfiable-Tseitin 1-NBP lower bounds

**2026-11-08 03:26 PST | Route A | KNOWN THEOREM + PROVED/RESTRICTED conditional-model transfer + COMPUTATIONAL | P versus NP OPEN.**

**Proof-chain nodes:** [P2-A2], [P2-A4], [P2-A5] remain OPEN; companion [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] all remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Complete tracker readback at preflight: proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters), proof2 blob cfe16253a3ce5af2d7b716ff4f8e29c68ef685cf. Historical R_mix341 untouched.

## IDEA -> SEARCH -> ITERATE: predeclared falsifiers

Hypothesis: published lower bounds for **satisfiable Tseitin Boolean-function evaluation** exclude any pointwise OR decomposition into polynomially many *polynomial-size syntactic read-once* guest branching programs, even with private existential witnesses and sharing. This is a sharply restricted Route A architecture, not SAT decision hardness.

F1: the strongest known 2017 expander theorem might fail to apply to **cubic** strict-3CNF sources. **TRUE**: Glinskih–Itsykson 2017 requires absolute second eigenvalue <d/3. For d=3 this threshold is 1, whereas Alon–Boppana forces the asymptotic second eigenvalue to at least 2 sqrt(2)-o(1). Repair: their 2019/2021 Theorem 4.1 covers **all graphs** via treewidth, at a weaker exponent. F2: existentially projected private child wires might escape read-once simulation. **FALSE within model**, by published Lemma 4.2. F3: combining alternatives might silently drop required AND obligations or incompatible assumptions. **FALSE for the declared OR identity**; each accepting child alone witnesses truth, and local assumptions are part of its predicate. F4: read-2 computation might bypass the purported all-computation lower bound. **TRUE**; an explicit read-twice program is linear-size.

## Source-authenticated established-family ledger

For a connected simple cubic graph G=(V,E), H=|V|, M=3H/2, introduce one variable x_e per original edge and charges b_v. At each vertex v with ordered edges a<b<c add exactly four strict proper signed clauses

$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus b_v}(x_c),\quad(p,q)\in\{0,1\}^2,
$$

where \ell_0(x)=x and \ell_1(x)=\neg x. This is the original charge-parity encoding, not a mere equisatisfiable gadget. Clauses=4H, variables=3H/2, canonical dense-DIMACS N=Theta(H log(H+2)) bits. For connected G, SAT iff XOR_v b_v=0. Even-charge sources are SAT and odd-charge sources are UNSAT. For a growing constant-edge-expansion cubic family, tw(G)=Omega(H) by balanced separator/degree counting.

**Established lower bounds:** Glinskih–Itsykson, *On Tseitin Formulas, Read-Once Branching Programs and Treewidth*, ECCC TR19-020 revision 1 (March 25, 2019) Theorem 4.1, published Theory of Computing Systems 65 (2021) 613-633, DOI 10.1007/s00224-020-10007-8, proves size(1-NBP for SAT even-charge Tseitin function) >=2^{Omega(tw(G)^delta)} for every fixed 0<delta<1/36. Thus on cubic expanders this is >=2^{Omega(H^delta)}. This is the *syntactic nondeterministic read-once branching-program* Boolean function model, not arbitrary SAT decision. The stronger Glinskih–Itsykson MFCS 2017 2^{Omega(H)} theorem requires high-degree spectral expansion and cannot be transferred to cubic without a proved preservation theorem. For odd charge, Urquhart 1987 and Ben-Sasson–Wigderson 2001 give exponential **ordinary shared-DAG Resolution** hardness on suitable expanders, not mixed R_mix341 or all-machine hardness. GF(2) summation, Cook ER, shared proof DAGs and read-2 programs are explicit mandatory shortcuts.

## Theorem 490.1, derived restricted OR-child transfer

Suppose for each H there are q_H typed child predicates G_i(x,y_i) with private auxiliaries y_i and **pointwise**, not merely SAT-label, equivalence

$$
\forall x\quad F_{G,0}(x)=\bigvee_{i=1}^{q_H}\exists y_i\ G_i(x,y_i).
$$

Suppose each G_i admits a syntactic 1-NBP with at most u_H nodes over its displayed variables and any branch-specific assumptions are incorporated in G_i. Then for any fixed delta<1/36,

$$
\boxed{q_H(u_H+O(1))\ge 2^{\Omega(H^\delta)}.}
$$

**Proof.** In each child 1-NBP replace auxiliary y_i tests by nondeterministic guess nodes. No path queried a y_i twice, so this computes existential projection with no increase in node count (Glinskih–Itsykson 2019 Lemma 4.2). Add a binary tree of nondeterministic choices selecting one child; merge compatible sinks, and count the union of inference/computation nodes once. This is a syntactic 1-NBP for the displayed pointwise OR with at most sum_i |D_i|+O(q_H) nodes. The published treewidth lower bound gives the inequality. QED.

Thus q_H<=N^{3/5+o(1)} together with per-child 1-NBP size N^{O(1)} is impossible for the authenticated even-charge cubic expander family. **Child CNF bitlength <=N^{1/2} alone DOES NOT imply polynomial child 1-NBP size.** A same-machine SAT solver may reread variables, use XOR or arbitrary computation, and needs preserve only SAT/UNSAT labels; these are legal escapes, not ruled out by this theorem. Shared input-dependent preprocessing must be counted and may itself break the read-once simulation.

## Theorem 490.2: explicit read-2 upper control

A deterministic read-twice branching program evaluates all H parity triples sequentially, with five query nodes per vertex (one first-bit, two second-bit, two third-bit parity states) and two terminal nodes: size <=5H+2. Each original edge appears at exactly two vertices, so no accepting path reads it more than twice. It computes the original **pointwise** F, hence demonstrates that the read-once restriction is essential. Every satisfying edge assignment has only UNSAT Hamming-distance-one neighbors, and every accepting 1-NBP path must query all original edges, already established as Glinskih–Itsykson MFCS 2017 Proposition 4, not novel.

## Finite original-source verification and full resource boundary

Independent Python and Node.js generated the four exact signed vertex clauses for K4, triangular prism, cube and Petersen graphs, both even and odd charges. Each implementation exhaustively matched source-CNF evaluation to GF(2) equations and a separate read-twice evaluator over all original edge assignments, verified every one-edge flip of each satisfying assignment, checked SAT counts 2^{M-H+1} on even charge and zero on odd charge, rejected 5 malformed controls per graph-charge case, and on K4/prism exhaustively checked OR of read-once minterm paths. Python: **152,496** checks. Independent JavaScript: **152,876** checks. Graphs are small validation controls, not certified asymptotic expanders. Neither native FLMV nor historical R_mix341 checker was run, and the 2021 theorem was sourced, not machine-reproved.

**Resource ledger:** Read-2 constructive BP nodes <=5H+2, encoded bit cost O(H log H), not zero; a materialized finite source and incidence arrays occupy Theta(N) host working memory, so no N^{1/2} space claim. The source N=Theta(H log H); OR transfer counts distinct unioned read-once BP nodes with O(q) selection/reference nodes, not physical runtime. Python/Node brute-force input enumeration, parsing, source/index reads, generator search, cache allocation and verification were paid by actual host processes but not translated to FLMV. No SAT guest, native machine transformation, compressed child construction or charged source-port optimizer was implemented. Target all-phase s'<=max(rho,eta,lambda,lambda*s) and t'<=max(11/10,3/5+t/2) remain unproved.

## SEARCH provenance and root safety

Read both root trackers, issue #3 through latest LSPV-1/501, Nov 2 governing handoff, AGENTS.md, CODEX.md and research skill, actual LSPV-2/487, /489; LSPV-4/491, /444; LSPV-2/446; Claude TPORT, Grok REWIRE. Prior LSPV-3/450 and the 2017 paper already cover per-variable support; novelty is not claimed. Verified repository files at current returned blobs: konard/p-vs-np scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2, blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93, MassimoLauria/cnfgen cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab, meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1, openai/math README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae. No external project supplies a universal compiler. A separate Google-branded client was unavailable; public scholarly web search was used. Root main.tex partial fetch returned no readable bytes: do not edit it or another role's region.

**References:** 
1. Glinskih and Itsykson, MFCS 2017, DOI 10.4230/LIPIcs.MFCS.2017.26, esp. Proposition 4.
2. Glinskih and Itsykson, ECCC TR19-020 (2019) Theorem 4.1 and Lemma 4.2, Theory of Computing Systems 2021, DOI 10.1007/s00224-020-10007-8. https://eccc.weizmann.ac.il/report/2019/020/
3. Urquhart, JACM 1987 DOI 10.1145/7531.8928.
4. Ben-Sasson and Wigderson, JACM 2001 DOI 10.1145/375827.375835.
5. Fortnow, Lipton, van Melkebeek and Viglas, JACM 2005 DOI 10.1145/1101821.1101822.
6. Alon-Boppana as summarized by Mohar, arXiv:1002.1084.

**Actual advance:** an exact model-licensed transfer with the crucial 2017-to-2021 cubic-family source repair and independently reproduced read-2 escape. **Open gap:** [P2-A2], [P2-A4], [P2-A5], all-input solver-dependent exponent-oblivious recursively iterable same-FLMV-machine contraction. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] also OPEN. **P versus NP OPEN.**

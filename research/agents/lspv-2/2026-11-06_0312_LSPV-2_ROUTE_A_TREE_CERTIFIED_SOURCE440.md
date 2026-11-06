# LSPV-2/440 | Tree-certified, self-describing Tseitin source authentication
**2026-11-06 03:12 PST | Route A primary | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

## IDEA, falsifiers and project continuity
Hypothesis: replace the predeclared-public-graph premise in LSPV-2/438 by a separately supplied **read-only** full graph adjacency and rooted-spanning-tree annotation. Verify that annotation and *every original signed strict 3-CNF literal* in near-linear time, logarithmic writable space, without a graph-sized index. The hypothesis is conditional on annotation already being supplied, not a new general SAT child generator. Falsifiers: (1) forged disconnected graph/tree accepted; (2) asymmetric/duplicate edge or ID collision; (3) mutated literal accepted as original; (4) the verification or certificate acquisition silently using linear writable space.

Existing project work reviewed: LSPV-3/255 already recognized cubic Tseitin with an O(N)-space host implementation; LSPV-2/438 obtained O(log N) writable-space membership verification *if the public graph is already indexable*; LSPV-2/423 and LSPV-4/419 ruled out direct unrestricted cofactor fanout with a mandatory XOR shortcut. Thus the only positive addition here is the **checked supplied-annotation interface**; acquisition on raw CNF remains open. The governing Nov. 2 five-role handoff, issue #3, AGENTS.md, CODEX.md and pnp-research skill were read.

## Exact original 3-CNF family and model
For a simple connected cubic graph G with H even vertices and 3H/2 edges, put one variable x_e on each edge. At vertex v impose the charge equation x_a ⊕ x_b ⊕ x_c = χ_v. Its exact original strict 3-CNF includes the **four distinct signed width-3 clauses** falsified by the wrong-parity triples. There are 4H clauses and 3H/2 used variables. Choose sorted neighbor slots and name an edge with endpoints u<v by

$$
\operatorname{id}(\{u,v\})=3u+\operatorname{slot}_u(v)+1.
$$

IDs are injective in [1,3H], with unused slots. This is an injective variable renaming from the usual dense-edge convention. In ordinary **no-weakening shared-DAG Resolution**, unused original variable IDs cannot enter a legal derived clause, so changing IDs does not change minimum Resolution size. No corresponding fixed-mixed-calculus transfer is assumed.

The fixed-field binary original source carries 8-bit magic, unary H, unary 3H, 12H signed literals (one sign bit and a w'=floor(log2(3H))+1 bit ID), and two trailer bits. Its exact length is

$$
S_H=8+(H+1)+(3H+1)+12H(w'+1)+2.
$$

The separate annotation stores an 8-bit magic, unary H, then each vertex's three ascending w-bit neighbors, one charge bit, one w-bit parent and one w-bit depth, and a two-bit trailer, where w=floor(log2 H)+1:

$$
P_H=8+(H+1)+H(5w+1)+2.
$$

Both are Θ(H log H). This *augmented-input* contract counts all annotation bits as read-only input, not as free information or part of a general raw-CNF input.

**Known certified hard anchor:** Suitable growing cubic expander odd-charge Tseitin strict 3-CNFs have size 2^{Ω(H)} **in ordinary shared-DAG Resolution** through Urquhart (1987) and Ben-Sasson and Wigderson (2001) expansion/width techniques. K4, cube, Petersen, Heawood and bridged K4 are finite semantic tests, NOT themselves a certified asymptotically hard sequence. Cook Extended Resolution and XOR/GF(2) are essential shortcut controls. Do not infer arbitrary-machine, full historical R_mix341 or B3 lower bounds.

## Theorem 440.1: checkable graph and source (PROVED/RESTRICTED)
A deterministic indexed read-only-input TM verifies the original packet and annotation in O(N polylog N) time and O(log N) **physical writable space**, N=S_H+P_H, by checking all three sorted, distinct, in-range, nonself neighbor IDs per vertex and every reciprocal adjacency. Check parent(0)=0, depth(0)=0, and for each v>0 that parent(v) is an adjacent vertex, depth(v)>=1, and depth(parent(v))=depth(v)-1. Strict depth decrease forces every parent chain to terminate at the **unique** zero-depth vertex 0, hence a spanning tree and graph connectivity. From a neighbor record and a reciprocal record compute every edge ID by the displayed formula. Compare every original source clause and literal at its exact original position, using the four parity-forbidden triples.

There are O(H) local checks, each with O(polylog N) indexed read-only-input operations and O(log N)-bit counters/indices. The FLMV index-tape write, jump, erase and head positioning are all included; no writable H-cell lookup table, copying or precomputed graph index is used. This is a precise machine-design argument, **not an actual native FLMV transition trace**. Generating the annotation from arbitrary unannotated CNF is a separate and fully chargeable computation, not covered by the theorem.

## Theorem 440.2: exact promise labels and bypass (KNOWN linear algebra)
Connectedness implies binary vertex-edge incidence rank H-1. Its only nonzero row dependence is the all-ones vector, so

$$
\operatorname{SAT}(F_{G,\chi})\iff\bigoplus_v\chi_v=0.
$$

Even charge has 2^{H/2+1} assignments to the 3H/2 USED edge variables. Because the encoded header declares 3H possible IDs, its other 3H/2 unused variables are unconstrained, yielding 2^{2H+1} models over ALL declared variables. Odd charge gives the certified global XOR contradiction. A one-bit parity accumulator decides the authenticated family. This legal shortcut defeats any attempted transfer of ordinary Resolution hardness to unrestricted SAT time. Exact acceptance distinguishes bad annotation, malformed original-source framing, **valid but outside-family** signed source, and authenticated SAT or UNSAT. Treating an outside-family source as malformed or using an uncharged original-length fallback guest would be incorrect.

## Independent computational controls
The complete local producer and separately authored JS checker were run successfully: **138 producer assertion groups**, **4,461 independent JS assertions**, ten original odd/even packets across K4, cube, Petersen, Heawood and bridged two-K4 graph, and **70 corrupted or malformed controls**. The independent verifier checks original signed support, each four-clause quartet, reciprocal graph edges, tree, SHA256, and exhaustive model counts for <=15 edges. Source/annotation lengths were K4 268/79, cube 620/187, Petersen 772/231, Heawood 1244/319, bridged K4 772/231 bits. Published compact replay separately executed with 74 checks. Host-language fixtures materialize full sources for testing and do NOT measure native FLMV physical space.

## IDEA -> SEARCH -> ITERATE provenance and strongest objections
Actual GitHub files reviewed: j15marti/pnp GROKPROOF/2026-11-06_0920_PROGRESS.md (blob 6b32bc30...), research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727...), research/agents/lspv-3/2026-10-30_1129_LSPV-3_TSEITIN_SELECTOR_GATE255.tex (f5a19381...), research/agents/lspv-4/2026-11-05_1136_LSPV-4_PERFECT_MATCHING_BRANCH_PORT419.md (98dfb3f4...). Required external repositories: konard/p-vs-np/proofs/complexity/README.md (7ee9a11e..., distinct one-tape formal model); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea...) and CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md (b37da20a..., incomplete proof-carrying quotient). Relevant code: MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd1...), meelgroup/frat-xor/format.md (986a21a...), lsils/mockturtle/README.md (c1d2b0c...), openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f...). These are distinct interfaces/models, not universal SAT transfer proofs. Literature: FLMV JACM 2005 DOI 10.1145/1101821.1101822; BSW JACM 2001 DOI 10.1145/375827.375835; Urquhart JACM 1987 DOI 10.1145/7531.8928; Reingold JACM 2008 DOI 10.1145/1391289.1391291. Indexed web search, not Google-branded search, was executed.

## Complete scope and resource ledger
Certified annotation length P_H and original evidence S_H are both O(N) **read-only** input. Actual host acquisition of graph adjacency and a BFS tree takes linear auxiliary host space, not admitted as an FLMV compilation step. The **verifier alone** uses O(log N) writable peak and O(N polylog N) charged time including headers, index-tape erase, source-bit positions, all source reads and outputs its one-bit decision. No child is materialized, no guest A is invoked for recognized sources, no expensive cache or reference is retained. Search, verification, failed policies, guest fallback, proof production and recursive child generation for arbitrary inputs remain entirely unproved, and must be charged separately. Mixed logical work, critical path, certificate bits and machine-space schedule are distinct.

The required **all-input, same-machine, recursively iterable** transform for every correct uniform polytime SAT decider A,

$$
t'\le\max\{11/10,3/5+t/2\},\qquad s'\le\max\{1/2,s/2\},
$$

remains OPEN. The auxiliary inequality s'<=max(rho,eta,lambda,lambda*s) does not allow treating certificate acquisition as free. Root main.tex had nonempty blob SHA 96851219... but returned zero readable bytes, so was not touched. The historical native R_mix341 grammar, weights, original-coordinate locality, five roles and existing schedules remain unchanged. **P versus NP remains OPEN.**

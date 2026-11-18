# LSPV-3 / T5-WTHREAD-1: weighted forbidden-color core of edge-critical high-girth obstructions

**Date:** 2026-11-18 15:37 PST. **Role:** Hypergraph & Proof Certificates (existing/paused identity unchanged). **Status:** PROVED/RESTRICTED structural theorem; COMPUTATIONAL independent finite replay. **P versus NP OPEN.**

## Candidate and falsifiers (fixed before experiments)
Candidate: after suppressing degree-two threads of a fixed-T5 source, each length-ℓ thread consumes at most q(ℓ)=max(0,4-ℓ) forbidden colors of either branch endpoint. Weighted-4-degenerate cores therefore admit a constructive SAT witness; every edge-minimal UNSAT threaded core has minimum weighted degree at least 5.

Falsifiers: (F1) a short path whose endpoint support is smaller than min(5,ℓ+1); (F2) a globally edge-critical H with weighted-degree <=4 at a branching vertex; (F3) a weighted-4-degenerate oriented threaded source with no T5 witness; (F4) a high-girth critical certificate invalid on any edge deletion. None occurred in the tested sources. A general polynomial-time witness algorithm for all critical deletions is NOT inferred.

## Exact theorem: weighted thread degeneracy and critical minimum

Fix the template T5 on Z/5 with R(a,b) iff (b-a) mod 5 in {1,3}. A *threaded source* consists of distinct branch vertices B and internally vertex-disjoint simple paths P between branch vertices, with arbitrary edge orientations and possibly multiple paths per branch pair. Pendant trees can be appended freely. For each thread P of length ℓ>=1 define its forbidden-color weight

```
q(P) = 5 - min(5,ℓ+1) = max(0,4-ℓ).
```

Let K be the branch multigraph with edge weight q(P), and let d_q(v)=sum of incident thread weights (count multiplicity). Define *weighted-4-degenerate* to mean that every nonempty induced branch subgraph has some vertex with incident internal weight at most 4.

**Theorem WTHREAD-1A (constructive SAT).** Every threaded source whose branch multigraph K is weighted-4-degenerate has a T5 homomorphism. A complete witness can be constructed using a weighted-degree peeling order, reverse five-color greedy reconstruction, and independent linear-time path filling. For fixed five-color arithmetic, this is O(|V|+|E|) primitive word operations after a standard source parse, with full source access and output included; bit-model bounds account for vertex indices.

**Proof.** Along an oriented path of ℓ arcs, the attainable endpoint differences form a translate of {0,2,...,2ℓ} mod 5. Hence for a fixed color at one endpoint, precisely min(5,ℓ+1) colors are permitted at the other, regardless of orientation. A thread therefore forbids at most q(P) colors of a branch vertex whose opposite endpoint has been colored. Repeatedly remove a branch vertex of current weighted degree <=4. Color in reverse order. At each insertion, previously colored neighbors collectively forbid at most four of the five colors, even counting parallel threads, so a legal color remains. Once both endpoints of every path are colored, independently backfill its interior via five-state backward reachability. Pendant trees extend greedily. The construction never assumes search or an oracle. QED.

**Theorem WTHREAD-1B (edge-critical structural necessity).** Let H be an edge-minimal T5-UNSAT simple oriented graph of undirected girth at least 7. Suppress its degree-two threads to the branching core K as in the independently established four-edge unrestricted-path lemma. Then every branching vertex v satisfies

```
3 d_1(v) + 2 d_2(v) + d_3(v) >= 5,
```

where d_ℓ(v) is the number of incident length-ℓ threads. In particular, if deg_K(v)=3, then 2d_1(v)+d_2(v)>=2; if deg_K(v)=4, then 2d_1(v)+d_2(v)>=1.

**Proof.** For each branch vertex v, deleting one incident source edge makes H satisfiable by edge-minimality; therefore deleting v and its incident threads leaves a satisfiable assignment on the other branch vertices. Every nonincident thread retains a valid extension. If d_q(v)<=4, the union bound over forbidden colors from the incident threads leaves a legal fifth color for v, after which all incident interiors extend independently. This would color all of H, a contradiction. Girth >=7 excludes self-return short threads and parallel structural anomalies; all nontrivial threads have lengths 1,2,3. QED.

Summing the degree inequality gives a supplemental whole-core necessary condition. Writing b=|B|, e=e_1+e_2+e_3, beta=e-b+1, n=b+e_2+2e_3, we have

```
2(3e_1+2e_2+e_3)>=5b,
3e_1+2e_2+e_3 = 3e-(n-b) = 4b+3beta-3-n,
n <= (3/2)b + 3beta - 3.
```

This is a source-size/structure inequality, NOT a decision- or witness-time lower bound. If b=2, the prior nine-relation intersection bound supplies at most four essential parallel threads; the weighted degree >=5 excludes four length-3 threads, forcing n<=9. The known (2,3,3,3) obstruction attains equality, giving an independent short proof of the sharp two-branch bound.

## Strong hostile control: high girth and many cycles can be easy

Take any connected 4-regular simple graph B with large girth and replace each edge by a path of exactly three arcs, oriented arbitrarily. Every branch-thread weight is 1 and every branch has weighted degree 4. WTHREAD-1A gives a witness in linear work **for every orientation**. If |B|=b, then the subdivided source has n=5b, m=6b, beta=b+1, and girth three times that of B. Families of 4-regular graphs of arbitrarily large girth are known. Thus high girth, unbounded core size and linear-growing cycle rank by themselves cannot support witness hardness. This construction is SAT, not an intrinsic critical-deletion family, and does NOT refute a hardness claim confined to H-e with H edge-critical.

## Independent finite replay and exact statuses

The attached reproducibility code uses only Python's standard library, computes all nine distinct length<=3 path support relations, all 2^9 subfamilies, and all 4096 orientations of four length-3 parallel paths. It also independently reconstructs AC-plus-branch search from the original graph, verifies UNSAT, and finds a complete original-label witness for **every** individual edge deletion. Rotation fixes vertex 0 to 0 only after source/component checks.

* **Nine-vertex critical theta H9**, four paths of lengths (2,3,3,3): 9 vertices, 11 arcs, beta=3, undirected girth 5; no T5 assignment, 11/11 edge deletions SAT, weighted branch degrees (5,5), all deletion witnesses found using <=6 DFS nodes. The standalone weighted greedy reconstruction also succeeds on all 11 deletions. This establishes sharpness of weight five (at girth five).
* **Published H33**, authenticated original ASCII source SHA256 `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`: 33 vertices, 44 original arcs, 19 branching vertices, beta=12, girth 8; threads length1:20, length2:6, length3:4. Its weighted-degree multiset is {5:1,6:3,7:2,8:5,9:6,10:1,11:1}. Independent five-state AC/DFS found UNSAT in 73 recursive nodes and witness colorings for 44/44 edge deletions, each violating precisely its omitted original arc; at most 123 nodes per deletion.
* **Finite-language census:** exactly nine distinct short-thread supports; maximum irredundant family size four among all 512 subfamilies; all 4096 four-long-thread orientations SAT.
* **Important negative control:** after removing each damaged thread from the H33 core, weighted-4 peeling still leaves 17 branch vertices for two deletions, 18 for eighteen deletions, and all 19 for twenty-four deletions. Nonetheless every H33-e is SAT and has a short finite search witness. Therefore *persistence of a weighted five-core* is not itself a proven lower bound on witness acquisition.

The supplied /mnt/data/T5_Critical_BranchCore_20261118.zip was absent from this runtime. Rather than assume the earlier package's assertions, the above relations, source SHA, criticality checks, and core statistics were independently regenerated. This does NOT constitute an external peer proof audit or a proof of any growing-girth critical family complexity.

## Necessary next gate

The branch weighted-five-core obstruction is an exact **necessity for UNSAT**, not a witness-cost barrier. Seek a *nontrivial* relation invariant that persists after full weighted-core peeling, GF(5) cycle equations with binary edge domains, Gaussian/flow elimination, separator DP, arbitrary variable orders, symmetry, and compact circuits. Specifically compare source-recognized polynomial witness construction on H-e for growing-girth genuinely edge-critical H against the weighted core persistence, rather than counting core vertices or assignments. Verify whether any purported high-girth *critical* promise reduction is source-preserving and polynomial for growing girth; fixed-girth NP-hardness does not prove it.

No scheduled task, tracker, main.tex, title, identity or paused state was changed. HISTORICAL TRACKERS UNCHANGED; NO MATERIAL PROOF-STATUS CHANGE. The repository's 2026-11-15 end-to-end governance retires root trackers and assigns current manuscripts to the TMR owners. This paused LSPV-3 role modified no tracker or TMR-owned manuscript; the proof2.txt connector read was empty despite a nonempty blob SHA and was not interpreted as an empty source. **P versus NP OPEN.**

## Original references

1. Bang-Jensen, Hell & MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 281-298 (1988), https://doi.org/10.1137/0401029. This supplies general fixed-T5 NP-completeness, not critical-promise/growing-girth NP-hardness.
2. Kayll & Morris, *On Colouring Oriented Graphs of Large Girth*, Contributions to Discrete Mathematics 18(2) (2023), https://doi.org/10.55016/ojs.cdm.v18i2.73457. Large-girth homomorphic constructions are not by themselves critical-source reductions.
3. Sachs, *Regular Graphs with Given Girth and Restricted Circuits*, J. London Math. Soc. s1-38 (1963), 423-429, https://doi.org/10.1112/jlms/s1-38.1.423.
4. Existing canonical H33 source: research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5 (SHA above).
5. TMR-2/091, `research/agents/tmr-2/2026-11-18_1212_TMR2_T5_BICYCLIC_TRANSFER091.md`, for the 9-vertex sharp obstruction.

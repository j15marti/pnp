# LSPV-2 T5 intrinsic-critical witness circuits, 2026-11-18 15:16 PST

**Status:** PROVED exact nonuniform finite-deletion circuit theorem; PROVED restricted m-1 source-bit-probe lower bound; COMPUTATIONAL source-bound gate replay on two independently authenticated critical T5 sources; OPEN uniform witness lower bound, intrinsically critical growing-girth NP-hardness, P versus NP.

## Candidate and falsifiers

Fix T5 on Z5 with R(a,b) iff b-a mod 5 is 1 or 3. For *every fixed* connected edge-minimal UNSAT H=(V,E), n vertices, m arcs, construct a source-aware combinational circuit C_H on all n(n-1) ordered-pair adjacency bits that recognizes *exactly* the m masks H-e and emits a verified five-symbol witness on each. Reject input mutations outside the deletion promise, charge witness discovery, and compare with a uniform branch-core algorithm.

Falsifiers: (F1) H is SAT or a deletion remains UNSAT; (F2) a foreign arc, no deletion or double deletion is accepted; (F3) a witness has a bad surviving edge or illegal three-bit symbol; (F4) hidden witness-table advice or a treewidth/GF(5) shortcut makes an unrestricted complexity inference invalid. F1-F3 passed two independent local checks and two hostile mutations; F4 blocks the uniform conclusion.

## Exact theorem A: finite-deletion source-mask circuit

For each e in E let w_e be any independently certified coloring of H-e. Set
S_e = (NOT x_e) AND (AND_{f in E minus e} x_f).
Set B = AND_{a not in E}(NOT x_a).
The valid flag is B AND OR_e S_e. Each output color bit (v,j) is B AND OR_{e:bit_j(w_e(v))=1} S_e. A distinct verifier checks legal 0..4 codes and each surviving original arc, with certified=valid AND checks.

A balanced all-except-one AND tree with shared subexpressions yields O(m) selectors of depth O(log m). The complete source guard, all 3n color bits and verifier have O(n^2+mn)=O(n^3) fan-in-two AND/OR/NOT gates and O(log(n+m)) combinational depth. The circuit distinguishes real adjacency masks, not a free deletion-index oracle. Invalid masks yield valid=certified=0, **not** an UNSAT classification.

**Quantifiers:** FOR ALL critical H EXISTS C_H, not EXISTS one uniform polynomial-time compiler working for all H. Brute acquisition and certification of w_e may cost O(m5^n poly(n+m)) bit operations. Thus the result **falsifies proposed superpolynomial nonuniform circuit-size lower bounds for one fixed H_n's finite deletion family**, but it is not a uniform FP algorithm, P=NP algorithm, or unrestricted time lower bound.

## Exact theorem B: restricted sequential-query lower bound

Given the promise that exactly one of the m expected H edges is deleted, any deterministic sequential edge-presence bit-probe witness algorithm has worst-case at least m-1 probes, even with H known. If two unqueried edges e,f remain and every queried edge is present, either source is possible. Any shared output satisfying both H-e and H-f would satisfy H, contradiction. Query m-1 bits to attain the bound. Foreign adjacency bits provide no information on the promise. **This is a tight linear lower bound for that restricted model only.**

## Exact theorem C: uniform no-advice branch-core upper bound

Given H and the designated deleted edge e, suppress degree-two threads in connected, 2-vertex-connected edge-minimal T5-UNSAT H. Full threads have length L<=3; the broken thread contributes two independently extendable dangling arms. The surviving branching core stays connected. Fix one branch color 0 by Z5 rotation. Pick a spanning tree T of intact threads; enumerate at most prod_{t in T}(L_t+1) branch assignments, checking every other core relation and reconstructing all original path colors. This is a uniform correct witness algorithm with poly(n+m) times that product, at most 4^(b-1) poly(n+m), and polynomial depth-first memory. A min-product tree is found by a minimum spanning tree on weights log(L+1). **Not a polynomial bound when b grows.** For the tested 33-vertex H, the minimum candidate-leaf products after deletion are 262144 through 524288, compared with 4^18=68719476736.

## Original source and completed tests

Source: j15marti/pnp/research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5, SHA-256 **0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac**. Independent source suppression: n33,m44,girth8,b19,beta12, 30 threads (20 length1, 6 length2, 4 length3), maximum parallel multiplicity1. Exact enumeration independently verifies 9 distinct short-path endpoint relations and all 512 subsets: maximum irredundant intersection size4; 4-edge paths are universal.

| Critical source | Gates for witness A/N/O | Depth | Gates including certified verifier A/N/O | Depth | Independently replayed masks |
|---|---|---:|---|---:|---:|
| 33 vertices, 44 arcs, girth 8 | 263/45/1491 = **1799** | 20 | 1031/137/2035 = **3203** | 36 | 2003 |
| 9 vertices, 11 arcs, four paths, girth 5 | 59/12/104 = **175** | 12 | 206/32/208 = **446** | 26 | 2176 |

The baseline 33-source circuit used 2318 gates at depth47; balanced selector tree and shared OR factoring reduced it to 1799 gates at depth20. All 44 and all 11 genuine edge deletions yielded independently verified distinct SAT witnesses. For both test sources each deletion admits both reverse endpoint differences 2 and 4; this is finite, not a universal assertion. The 9-source audit includes all 2048 expected-edge masks. The 33-source audit tested 44 valid masks, unchanged source, 946 two-edge deletions and all 1012 possible single foreign-arc injections. Independent DAG interpreter detected forged certification and output mutations. Two complete serialized netlists were generated; original 33-source netlist SHA-256 **75484368cb216c9566c7e4813c4825a7f973cc40139b960a428d5efb12975112**.

AC+DFS compiler executed 1521 total search nodes for 33-vertex H and both pinned endpoint options for every deleted edge, including a 73-node original UNSAT audit; exact CPU/TM costs are not inferred from this node count. Source parsing, serialization, verification, compiler time, table acquisition and output bits remain separately charged. Reproducibility package in the corresponding 2026-11-18 LSPV-2 ChatGPT run contains complete executable compiler (SHA e1c766367e8321215fc1c711160a1d65f7d5c591d751aeeff52a65d3b8da4f68), independently implemented DAG evaluator (SHA 7456d6b3e45f859982f8aa500caa4fa5352411cdfc860636a637bdde6ac8d960), both source graphs, 2 netlists, 2 full JSON outputs, a distinct branch-core audit, and a SHA manifest. Exact package SHA-256: **2d1213ed852ecc4a102450014d555e30d38d79ac6c8c729d1f6d62a0ba9e7dfc**. The full reproducibility archive is delivered in the associated chat; these large raw netlists and executables were not uploaded to this repository.

## Literature and essential caveats

Bang-Jensen, Hell, MacGillivray (1988), DOI https://doi.org/10.1137/0401029 establishes general fixed-T5 CSP NP-completeness. Kun (2013), DOI https://doi.org/10.1007/s00493-013-2405-4 gives general fixed-large-girth CSP complexity, not a growing-girth intrinsically critical promise result. Kayll/Morris (2023), DOI https://doi.org/10.55016/ojs/cdm.v18i2.73457 gives large-girth oriented graph homomorphism lifts, not uniform critical witness hardness. Project TMR-2/093 gives a valid exact GF(5) syndrome DP and cheap multi-theta controls; project TMR-2/081 reports width-four weighted elimination on this 33-source. They remain admissible alternative algorithms. No static-rank/monotone/bit-probe/proof-system lower bound is promoted to arbitrary deterministic time.

**Ownership:** dated LSPV-2 report only; no root tracker, main.tex, peer-owned main manuscripts, automations or schedules changed. Independent external mathematics peer audit is OPEN. P versus NP is OPEN.

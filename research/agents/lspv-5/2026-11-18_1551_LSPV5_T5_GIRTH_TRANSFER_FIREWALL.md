% LSPV-5 REPORT::LSPV5-T5-GIRTH-XFER-001::2026-11-18T15:51:00-08:00
# LSPV-5 independent proof red team: T5 girth-transfer firewall

**Run:** `LSPV5-T5-GIRTH-XFER-001`  
**Date:** 2026-11-18 15:51 PST  
**Role:** LSPV-5 INDEPENDENT PROOF RED TEAM; historical title, ownership, schedule, Route B label, and paused/disabled state preserved. No agent or automation was activated, created, renamed, or rescheduled.  
**Strongest verdict:** **PASS** for the local branch-core theorem and for fixed-threshold high-undirected-girth T5-CSP hardness; **FAIL** for the cited Kayll--Morris undirected-girth transfer; **OPEN** for growing-girth intrinsic-critical designated-deletion SAT-only witness hardness and every unrestricted witness-time lower bound. **P versus NP remains OPEN.**

## One target claim and exact falsifiers

**Target `T5-CRIT-GIRTH-WITNESS-HARD`:** known fixed-template/high-girth results establish a uniform hard family of inputs `(H,e)` where `H` is connected edge-minimal T5-UNSAT, undirected girth grows with input size, and the algorithm must output a full T5 coloring of the promised SAT deletion `H-e`.

Quantifier form required for the target is a single uniform, polynomially computable, source-authenticated reduction or generator over unbounded input lengths, together with promise closure and a witness decoder. It is not enough to have `for every fixed g, there exists H_g`.

Falsifiers fixed before the literature search and experiment were:

1. the invoked “girth” theorem measures directed cycles rather than the underlying undirected graph;
2. the construction is polynomial only after fixing the girth threshold, not uniformly for a threshold growing with the encoded input;
3. extracting an edge-minimal UNSAT subsource requires SAT/UNSAT decisions and loses the reduction's witness decoder;
4. exact path contraction, treewidth/DP, GF(5) cycle syndromes, or compact circuits remain legal source-aware witness algorithms, so core size/girth alone cannot transfer to arbitrary execution time.

Falsifiers 1--4 all apply. The target remains **OPEN**; the Kayll--Morris route is **FALSIFIED/RETIRED for undirected girth**.

## Primary-source literature verification

### A. General fixed-T5 CSP

Bang-Jensen, Hell, and MacGillivray (1988), DOI [10.1137/0401029](https://doi.org/10.1137/0401029), prove that coloring by a fixed semicomplete digraph is NP-complete when the target has more than one directed cycle. This covers the present cyclic tournament T5. It is a decision theorem for unrestricted sources; it does not mention criticality, designated deletions, witness-only promises, or growing girth.

### B. Kayll--Morris does not prove the needed undirected girth

Kayll and Morris, *On Colouring Oriented Graphs of Large Girth* (2023), DOI [10.55016/ojs/cdm.v18i2.73457](https://doi.org/10.55016/ojs/cdm.v18i2.73457), explicitly define in Section 2: cycles of oriented graphs are **directed cycles**, and girth is the length of the shortest directed cycle. Their Theorem 1.1 therefore cannot be substituted for a theorem about the ordinary undirected girth of the source skeleton.

An explicit model-matched counterexample is the transitive orientation of `K4`: it has no directed cycle, hence infinite directed girth under their convention, while its underlying undirected girth is three. The finite reproducer checks this source directly. Therefore Section 4 of `research/agents/shield1/2026-11-18_1455PST_SHIELD1_INTRINSIC_CRITICAL_PROMISE.md` has the right cautionary conclusion but cites the wrong theorem for its asserted undirected-girth existence statement.

**Status:** `T5-KM-UNDIRECTED-XFER` = **FALSIFIED/RETIRED**. This is a theorem-hypothesis mismatch, not evidence against structural existence by another route.

### C. Kun repairs fixed-threshold structural existence, not the critical witness bridge

Kun, *Constraints, MMSNP and expander relational structures* (Combinatorica; arXiv [0706.1701](https://arxiv.org/abs/0706.1701)), Theorem 2, states: for fixed positive integers `t,k` and fixed finite relational type, every source structure `S` has a polynomial-time constructible `S'` of relational girth greater than `k`, preserving homomorphism to every target of size less than `t`. In a loopless simple oriented binary source, relational girth equals ordinary underlying undirected girth. Guzmán-Pro and Martin (ICALP 2025), DOI [10.4230/LIPIcs.ICALP.2025.158](https://doi.org/10.4230/LIPIcs.ICALP.2025.158), restate this exact incidence-girth convention for digraphs.

Taking the target size bound above five and target T5 gives a deterministic polynomial reduction from general fixed-T5 CSP to T5 CSP restricted to any **fixed** undirected-girth threshold. Thus:

- for every fixed `g`, T5 CSP on sources of undirected girth greater than `g` is NP-complete (**KNOWN THEOREM consequence**);
- for every fixed `g`, applying the construction to any T5-UNSAT source and then choosing an inclusion-minimal UNSAT edge subset proves existence of a connected edge-minimal T5-UNSAT source of undirected girth greater than `g` (**PROVED/EXACT consequence**, nonuniform choice allowed).

The second bullet is pointwise existence. Minimalization is not supplied by Kun's reduction and may require deciding up to all edge deletions. More importantly, neither theorem gives a witness-preserving map into the promise `(H,e) -> H-e`, and the fixed `k` quantifier does not establish one polynomial reduction with girth increasing as a function of encoded input length.

**Status:** fixed-threshold high-girth T5 CSP = **PASS/KNOWN THEOREM**; arbitrarily high-girth critical obstructions = **PASS/PROVED consequence**; growing-girth critical deletion witness hardness = **OPEN**.

## Independent branch-core and hostile-control replay

The user-provided `/mnt/data/T5_Critical_BranchCore_20261118.zip` and `/mnt/data/t5_critical_structure/THEOREM.md` were not mounted in this execution. I did not treat their absence as evidence. I independently reconstructed the exact finite language and checked the accessible GitHub reports.

The new standalone Python audit establishes the following finite facts by exhaustive exact arithmetic:

- each F/B orientation word of length `L` has endpoint differences equal to a translate of `{0,2,...,2L}` modulo five;
- there are exactly nine distinct nonuniversal supports for lengths one through three;
- every length-four support is all of `Z5`;
- among all `2^9=512` support subfamilies, exactly 63 are irredundant and the maximum irredundant size is four (15 of the irredundant families have empty intersection);
- the four-vertex five-arc source `(0,2),(0,3),(1,2),(3,1),(3,2)` is T5-UNSAT, every edge deletion is SAT with model counts `10,10,10,10,5`, and the last deletion has missing-edge difference support exactly `{2}`;
- transitive `K4` has directed girth infinity and underlying undirected girth three.

This independently supports the path/thread portion of the handoff and the endpoint-support counterexample already reported by SHIELD1. It supplies no asymptotic hardness. The stronger high-girth core inequalities in LSPV-1 are consistent: when undirected girth is at least seven, parallel suppressed threads would lift to a cycle of length at most six, so the core is simple and `n <= b^2`, stronger than the earlier general `n <= 4b^2-3b`.

**Artifacts:**

- `experiments/review/lspv5_t5_girth_transfer_audit_20261118.py`, SHA-256 `bc22df6e4bbab92807fa14b5a89e7e679828790db00d8387f6b1a251106725f7`;
- `results/raw/review/2026-11-18_LSPV5_T5_GIRTH_TRANSFER_RAW.json`, SHA-256 `5f003398ae748b0f152efb9f8dea99a5c6bf06bbe33f7ddfbb95559c7f3f7775`;
- internal canonical payload SHA-256 `82cba12197f5d5267103e827a549ad7626a0e928b841f8efbf831f8019d3c033`.

The experiment finishes in under one second; no chunking or timeout increase was needed. Finite results are **COMPUTATIONAL** unless separately proved above.

## Why the hardness transfer remains open

The chain still lacks all of the following:

1. **Uniform growing girth.** Kun's theorem fixes the girth threshold before the input. Its statement does not supply the required encoded growing parameter with a proved polynomial bound.
2. **Uniform criticalization.** Choosing a minimal UNSAT edge subset is an existence step. A charged construction can use a SAT decision oracle or, conditionally, a total all-SAT witness finder with timeouts and verification; that is not the desired unconditional reduction.
3. **Promise closure.** A deletion-witness algorithm is promised input `(H,e)` with H already critical. Calls on arbitrary intermediate graphs are off-promise unless separately justified.
4. **Witness decoding.** Homomorphism-existence preservation does not force every coloring of `H-e` to encode a witness of an arbitrary original SAT instance. A total compiler outputting a promised deletion on every input and requiring every deletion coloring to decode a satisfying assignment would put UNSAT in NP, hence imply NP=coNP; this is a barrier hypothesis, not a construction.
5. **All-algorithm transfer.** Exact thread contraction, the TMR-2/093 GF(5) syndrome DP, bounded-treewidth/elimination, algebraic/flow methods, alternate variable orderings, source recognition, and compact circuits remain admissible. No theorem makes branch count, girth, beta, DP table width, proof size, or oracle-query count compulsory for unrestricted deterministic execution.

The exact TMR-2/093 identity

`Z(G)=5^c |{b in {0,1}^m : H b = -3 H 1 (mod 5)}|`

is an upper-algorithm control and exact semantic reformulation. Dropping the Boolean restriction would make Gaussian elimination only a relaxation. Neither the number of syndrome states nor a branch-core Moore bound is a time lower bound.

## Corpus reconciliation

**CORPUS REVIEWED.** Local `proof1.txt`, `proof2.txt`, root `main.tex`, `AGENTS.md`, `CODEX.md`, the PNP research protocol, repository tree, issue #3 body, current T5 GitHub reports LSPV-1 critical-thread, LSPV-2 witness-circuit, SHIELD1 intrinsic-critical, TMR-2/079, /091, /093, the current proof/ARC-strengthen report and their coordination handoffs; primary papers above.

**DUPLICATION / CONTRADICTION AUDIT.** The short-path theorem, four-vertex endpoint-support counterexample, and warning that fixed-girth hardness does not imply the target were already in the current corpus and are independently reproduced, not claimed novel. The material contradiction is SHIELD1 Section 4's use of Kayll--Morris for undirected girth; the same structural conclusion is repairable only by replacing that citation/dependency with Kun's relational sparse-incomparability theorem and retaining fixed-threshold quantifiers.

**WHAT CHANGED RELATIVE TO ROOT MAIN.** No root theorem is strengthened. A compact result was inserted only inside the balanced LSPV-5 ownership region: it adds the literature firewall, records the independent replay, and downgrades only the invalid Kayll--Morris transfer. All other ownership regions and executive text are byte-preserved.

**ADOPTED.** Exact T5 relation, path/thread normal form, high-girth simple-core consequence, GF(5) syndrome identity, and nonuniform circuit hostile control.  
**REJECTED/RETIRED.** Kayll--Morris as a source of high **undirected** girth; any inference from fixed threshold to growing girth; any free criticalization/minimality step; any transfer from structural size to unrestricted time.  
**STALE OR OVERSTATED CLAIM FOUND.** SHIELD1 Section 4's cited proof of arbitrary undirected-girth critical obstructions is unsupported by its cited theorem. The conclusion is retained only under the corrected Kun dependency.

## Final status and handoff

| Claim | Verdict |
|---|---|
| Nine short endpoint relations; length four universal; irredundance <=4 | **PROVED/EXACT + COMPUTATIONAL replay** |
| Kayll--Morris implies large underlying undirected girth | **FALSIFIED/RETIRED** |
| Fixed-threshold high-undirected-girth T5 CSP remains NP-complete | **KNOWN THEOREM consequence** |
| Arbitrarily high-undirected-girth intrinsic critical T5 obstructions exist | **PROVED/EXACT consequence**, nonuniform minimalization |
| Growing-girth intrinsic-critical designated-deletion witness problem is NP-hard | **OPEN** |
| Branch-core/girth growth implies superpolynomial witness time | **FALSIFIED as an inference / OPEN as any new all-machine theorem** |
| P versus NP | **OPEN** |

**Next blocker:** give one explicit polynomial-time, source-authenticated reduction whose outputs satisfy the intrinsic critical deletion promise at the necessary quantifiers and whose witness decoder is proved for all relevant colorings, while charging criticalization, girth construction, source access, candidate acquisition, verification, memory, and output. Alternatively, prove a complete polynomial witness algorithm for the promise by combining thread contraction with treewidth and GF(5) syndrome methods.

TRACKERS REVIEWED; NO MATERIAL NODE CHANGE. The authorized LSPV-5 root-main region was reconciled with this firewall; no automation, role state, schedule, route label, or proof tracker was modified.

% END_OF_VERIFIED_REPORT::LSPV-5::LSPV5-T5-GIRTH-XFER-001

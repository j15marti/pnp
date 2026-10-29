# LSPV-4 handoff: RANK-INTERFACE-GRID229
29 October 2026, 14:36 America/Los_Angeles. Formal status PROVED/EXACT for specified clause-atomic grammar, COMPUTATIONAL independent controls, OPEN general P-vs-NP. No schedule or team change.

## New strictly scoped rank-interface tradeoff
Reuse LSPV-4 GRID209's connected strict signed exact-(2+,2-)-3CNF family F_q: n=3q^2, m=4q^2, with a q-by-q subdivided primal grid and the explicit SAT witness A=1,B=C=0. Encode each original ternary clause with its independent 3-selector parity=1 plus exactly-one binary clauses plus selector-implies-literal binaries. Assume every whole selector gadget is assigned once to one module of a running-intersection tree. If module t owns p_t gadgets, its original affine coefficient rank is e_t=p_t. Let b_t count the FULL shared interface over original-variable names, across all other bags, rather than only the parent separator. The primal grid bramble gives some module bag |X_t|>=q. Every name in X_t not among the at most 3p_t owned clause names must be shared, yielding

    THERE EXISTS t:  b_t + 3 e_t >= q.

Therefore, under this *atomic* grammar, bounded original local rank e_t=O(1) forces some complete interface b_t=Omega(q)=Omega(sqrt(N/log N)). Conversely logarithmic b_t forces e_t=Omega(q). The sufficient conditions of TREE-AFFINE227 cannot cover this family via this specific atomic encoding. When the atomic full-interface algorithm literally constructs every row, any fixed e_t<=E has at least 2^(q-3E) row examinations and explicit row-output bits. The lower bound concerns this implementation, not SAT decision: every F_q is trivially SAT and can be contracted to a constant YES formula when only the decision must be preserved.

The theorem does NOT rule out other encoding grammars, splitting selector gadgets, rich semantic preprocessing, 2CNF-good child absorption in HYBRID228, alternative polynomial local solvers for high e, or source-present contextual query replay. Do not transfer it to general SAT runtime or RAM/TM forbidden regions.

## Independently checked evidence
Read actual GitHub AGENTS.md, CODEX.md, repository pnp-research skill, GRID209 source (blob d5a4736d), HYBRID228 source (74823ca4), ARC227 source (fc4a02dc), AFFINE-LIFT-BVE229 (23ebfe32), and MIXED-PORT-CYCLE230 handoff (2b0558ec). Inspected NetworkX's heuristic treewidth source (ef1b2f7351bd), which supplies upper approximations, not lower bounds. Read Arvind/Guruswami IPEC2021 Theorem17 (fixed e gives XP N^{O(e)}) and Theorem19 (W[1]-hardness), including primary PDF page image.

Ran new standard-library `repro_grid_rank.py` in 5.79 seconds: q=2,3,4,5,6,8,12,16,24,32, ten proper balanced connected sources, ten disjoint internal grid-path audits, ten explicit models, renamed/signed controls, and 60 certified running-intersection path module trees with grouping sizes 1,2,4,8,16,4q. All checked inequalities pass. For q=32: n=3072, m=4096, ASCII DIMACS 71,364 bytes, and one-gadget path maximum full interface b=68. Symbolic table-row count was computed but tables were NOT enumerated. Raw SHA256 6c282a63452f25099a278b483f41b24aec5c36fdcaf02da170caa52027e3bc33.

Materialized all three user-provided Library ZIPs. Independently reran coverage (9.64 seconds) with byte-identical JSON, and restart extension (4.96 seconds) with identical logical decisions/counters but variable timing/tracemalloc fields. Inspected portfolio archive and compared its extracted JSON byte-identically, but did not rerun its full 312-case audit this time. No universal algorithm coverage follows from these archives.

Root `main.tex` fetched on this run at blob dd3e5f4d34b316101ef88884674631ba28f18772 had 180 lines, an explicit truncation remark and NO role ownership markers. No root mutation was attempted. LSPV-5 owns recovery. A root snapshot previously reported by LSPV4 HYBRID228 as substantive with markers may differ; do not silently replace the current root with inferred missing text.

## Specific requests
LSPV-1: Referee the exact quantifier and bag-size inequality and explore whether a non-atomic semantic summary can bypass the tradeoff with charged discovery, fixed local codimension, and small exceptional unions. The q-grid is easy SAT and must be used as a hostile control against claims that width alone implies runtime hardness.

LSPV-5: Keep this as a restricted refinement of GRID209, not a new grid-width theorem. Verify that main.tex is recovered from authentic Git history before any integration. Continue tracking one-program SAT/UNSAT work and all acquisition costs.

**Next lemma:** On the GRID209 source, produce or falsify a uniformly polynomially discovered **non-atomic** exact summary grammar with O(1) local affine codimension and O(log N) exceptional-message unions; any negative claim must state the precise grammar.

# TMR-1 compact handoff | 2026-11-18 03:04 PST | sharp three-subdivision saturation /087

**Authority:** TMR-1 / PNP Machine Model Lead. Existing title, identity, enabled state, hourly schedule, ownership, living manuscript and issue #3 stay unchanged. Draft PR #197 remains unmerged. No agents created, duplicated, disabled, rescheduled or immediately rerun. P versus NP OPEN.

**NEW EXACT THEOREM C1-T5-THREE-SUBDIVISION-SATURATION087:** Replace each edge of an arbitrary undirected multigraph H by an internally vertex-disjoint path of length at least three, with arbitrary orientations on the new path arcs. Every result is T5-colorable for the fixed tournament relation R(u,v) iff v-u mod 5 in {1,3}. For path length 3, equal endpoint colors have precisely 3 internal extensions with coherent orientations, 1 with mixed orientations. For path length >=4 all endpoint label pairs are extendible. In particular, the all-three subdivision has at least 5^c * 3^a global solutions, where c is skeleton connected components (isolates included), a is coherently oriented paths. This is a LOWER bound only, not the full exact count.

**PROOF SPINE:** Along path signs sigma_i=+1/-1 and increments sigma_i(1+2b_i), total differences are p-q+2t mod5 with t running every integer from -q to p. For length >=4 this interval contains all five residues. For length 3, zero always lies in the four-residue support, and the exact binomial count is 3,1,1,3 for p=0,1,2,3. Constant source colors per component and disjoint path interiors give a global witness and polynomial DP.

**SHARP NO INSTANCE:** Replace each K6 edge {u,v} (u<v) by u->w_uv->v. The two-step endpoint relation forbids equality because 1+1,1+3,3+3 give 2,4,1 mod5; six branch vertices would require six distinct colors. This is an UNSAT bipartite, girth-six DAG with 21 vertices, 30 arcs and 353 canonical source bits. In contrast, its arbitrary-orientation three-step subdivision with 36 vertices, 45 arcs and 623 canonical source bits is SAT. No hardness-preserving reduction may simply subdivide every edge into >=3 unconstrained directed steps.

**SOURCE/MACHINE:** Original canonical T5 source: unary n, 0, unary m, 0 and sorted unique ordered arcs using w(n)=max(1,ceil(log2(max(2,n)))) bits/endpoint, length L=n+m+2+2mw(n); 3n-bit witness. Triple-subdivision gives n'=n+2m, m'=3m, L'=n+5m+2+6mw(n+2m). Validate input and explicit path decomposition before constructive five-state DP. Conservative simultaneous sequential bit upper bound O((L+1)^4) time, O((L+1)^2) space when decomposition size is polynomial in L. The unannotated degree-two-chain sufficient-class recognizer is sound, not complete for SAT.

**FINITE COMPUTATIONAL EVIDENCE:** Executed local full source /mnt/data/tmr087/tmr1_t5_subdivision087_certificate.js, raw /mnt/data/tmr087/tmr1_t5_subdivision087_raw.json. 126 direction words for path lengths 1..6; 203 skeletons; 2,612 actual path extensions; 7,836 constructed arcs; all 15,625 K6 branch colorings. 14,606 assertions, zero failures. Raw SHA256 fc0cdfba9c87c9cb975847079770c61a7ef0360a22d85ea34f64486c486055e8. Separately executed published compact JS: 6,564 assertions, zero failures; local file SHA256 8b56b31c6c5ad383f1bbed18b63f99561c1f7c65d08e623f9545087a6b53e40d. Finite tests do not replace the symbolic proof.

**OWNED PUBLICATION:**
- research/agents/tmr-1/2026-11-18_0304_TMR1_T5_SUBDIVISION_SATURATION087.md
- experiments/tmr/tmr1_t5_subdivision087_certificate.js
- results/raw/tmr/2026-11-18_TMR1_T5_SUBDIVISION087_RAW.json
- main1_PNP_MACHINE_MODEL_LEAD.tex (additive /087 section, prior material retained)
- research/agents/tmr-1/archive/handoff_pre_2026-11-18_T5_087.md (byte-preserved /086)
- research/agents/tmr-1/handoff.md (this file)

**GATES/NEXT:** DISJ no universal lower bound; relativization OPEN; SAME_REALIZATION parse, verify, DP, arithmetic, output and writable peak space charged together; configuration-counting arguments do not prove mandatory time. Keep all cheap polymorphism, Fourier/flow, Gaussian for proved subclasses, local propagation, separators, compact-representation algorithms and graph-homomorphism shortcuts. Unrestricted T5-CSP NP-complete by Bang-Jensen, Hell, MacGillivray 1988 DOI https://doi.org/10.1137/0401029 and independent /080 reduction. This subdivision theorem is compatible with NP-hard bipartite DAG gadgets having shortcut constraints; do not infer arbitrary high-girth hardness/easiness. Independent peer review, complete LaTeX compilation and Lean/nanoda replay OPEN. P versus NP OPEN.

**NEXT C1-T5-NONSUBDIVISION-RESIDUAL:** Audit hard-source YES/NO images surviving residue all-pairs closure and /086 binary-cycle constraints, then look for exact algorithms or a rigorously representation-independent resource necessity theorem. Never count forced long paths as a hardness mechanism.

END_OF_HANDOFF::TMR1::2026-11-18_0304_PST

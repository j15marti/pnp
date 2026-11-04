# LSPV-2/400 five-role handoff: adaptive charged-gate collapse (2026-11-04 14:24 PST)

**PROVED/EXACT** only for the strict Resolution plus charged conservative AND2 fragment. Independent specialist review pending. **P versus NP OPEN**. No change to R_mix341, active task IDs, schedules, roles or enabled states.

**IDEA:** Replace LSPV-2/398's static original-input backdoor of size b by an adaptive binary decision tree whose L leaves each make every auxiliary gate output a constant or signed residual original literal. The falsifiable prediction was a same-source strict Resolution translation W_Res(F) <= L(r+1)-1 from an r-Resolution-inference proof over F plus a paid acyclic AND2 bank. **SEARCH:** Haken 1985, Cook 1976, SAT backdoors (Nishimura--Ragde--Szeider 2004; Gaspers--Szeider 2012), project LSPV-1/355 adaptive Horn/2SAT tree and LSPV-2/381,/397,/398,/399, GitHub openai/math Lean ExecCNFWidthSearch/Correctness, current Grok and Claude reports. Direct Google-branded search unavailable; general web search used. **ITERATE:** At each branch substitute gate outputs, discard now-tautological defining facets, lift a strict Resolution proof to a blocker subclause, and combine branches with L-1 strict joins. The theorem is proved for this fragment, not GF(2), AND3 or LOCAL-CONVERT.

Exact family: F_n = AND_i(x_i) AND (OR_i NOT x_i), with y_2=x_1 AND x_2, y_j=y_(j-1) AND x_j. Minimal static input collapse backdoor b=n-1. Minimal complete adaptive collapse tree L=n (stop at first zero). An actual gate-using certificate has r=3n-1 strict RES inferences plus n-1 paid gate declarations. Old translation upper bound: 2^(n-1)*3n-1. New upper bound: 3n^2-1. The **true original-source minimum** W_Res(F_n)=n, independently from both upper bounds. For n=8, compare 3071 versus 191 versus actual 8.

**Established-hard-family transport, restricted:** Haken's explicit unary PHP_h for h+1 pigeons and h holes, with m_h=h+1+h*binom(h+1,2) clauses, h(h+1) variables and N_h=Theta(h^3 log(h+2)) bits has every ordinary shared-DAG Resolution proof >=2^(ch) total lines for all sufficiently large h. Every strict AND2+RES proof with a collapsing adaptive tree satisfies L(r+1)>=2^(ch)-m_h+1. Polynomial r requires exponential L. This is NOT a full mixed-calculus lower bound and says nothing about arbitrary uniform SAT computation. Cook's polynomial ER proofs need not have short adaptive collapse trees; Tseitin has a GF(2) escape.

**Verification:** Local Python producer 9,918 assertions n=2..8, independent local no-import Node verifier 2,096 assertions n=2..9. Both check exact source/gate resolution, all smaller static backdoors, adaptive leaves, SAT/UNSAT controls and malformed/corrupted rejection. A separate GitHub-stored independent JS checker was re-executed from complete authenticated readback, 1,060 checks n=2..9, same numeric rows. Physical parser/source/index/head, tree discovery, conversions, checking, serialization, live DAG space, and outputs are not the logical node measure. No high-level machine runtime inference.

**Published artifacts:**
- Report: research/agents/lspv-2/2026-11-04_1424_LSPV-2_ADAPTIVE_GATE_COLLAPSE_TREE400.tex
- Standalone independent checker: experiments/arc/lspv2_400_adaptive_tree_independent.js
- Raw: results/raw/arc/2026-11-04_1424_LSPV2_ADAPTIVE_GATE_COLLAPSE_TREE400_raw.json

**Specialist handoff:** LSPV-1 verify quantifiers and machine/proof distinction; LSPV-2 explore actual typed LOCAL-CONVERT, AND3 and GF(2) cofactor behavior; LSPV-3 audit DAG and conservative-auxiliary semantics; LSPV-4 build fully charged bit-time/peak-space erasure scheduler and lazy-circuit adversaries; LSPV-5 challenge branch substitution, PHP model scope and novelty relative to /355 and /398. Neither Grok GROKPROOF/2026-11-04_2215_PROGRESS.md nor Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex supplies B3.

**OPEN:** B1, B2, B3 and superpolynomial worst-case Wbar_R_mix341; P versus NP OPEN.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-2::ADAPTIVE_GATE_COLLAPSE_TREE400 -->

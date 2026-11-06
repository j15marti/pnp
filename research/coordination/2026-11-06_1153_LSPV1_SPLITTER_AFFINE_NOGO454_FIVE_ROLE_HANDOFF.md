# LSPV-1/454 Five-role handoff | November 6, 2026, 11:53 PST

**Unchanged:** Exactly five agents. Route A LSPV-2 and LSPV-4 (FLMV all-input same-machine); Route B LSPV-1, LSPV-3, LSPV-5 (fixed R_mix341 shared-DAG Wbar and noncircular B3). No task, schedule, enabled state, rule, weight or main.tex edits.

**PROVED/RESTRICTED:** In standard proper 3-CNF chain splitting of any distinct-literal width-k clause, k >= 4, the first private splitter cannot be an affine function of the original literal values admitting an extension for every satisfying original assignment. Six satisfying assignments force affine f(0)=1 and f(0)=0. A valid nonlinear signed-AND section uses k-3 gates, with the first splitter of minimum algebraic degree two. This rules out only an affine-only **local Skolem elimination** for Braun bit-PHP LSPV-1/453 strict-3CNF splitters, not all polynomial proof backtranslations.

**COMPUTATIONAL:** Python k=4..8, affine candidates 32/64/128/256/512, valid zero. Independent Node 1,554 checks plus four rejected hostile controls. Additional standalone Node 1,715 checks and three hostile rejections. Six-row certificate checked k=4..20. Original clause existential projection checked. Local ZIP SHA-256 caf0260bcfd4666ec50c984fa9d7fb813536919558c45f5c4c1c2a7096a3cc6e.

**Established family/theorem/encoding:** Braun, arXiv:2609.23015v2, Nov 3 2026: bit PHP with n=2^ell holes, n+1 pigeons. Unrestricted-DAG Res(XOR) refutations of the original formula require >exp(n/(32768 ell^2)) nodes for ell>=32. Strict3 expansion of LSPV-1/453 has A=n*binom(n+1,2) forbidden-address wide clauses, S=A*(2ell-2) proper 3-clauses, V=(n+1)*ell + A*(2ell-3) original variables. This **does not** preserve the lower bound into historical R_mix341 by equisatisfiability. Cook ER PHP, LSPV-1/453 ER-FACET and expander-Tseitin mixed GF(2) remain mandatory upper controls.

**LSPV-3:** Authenticate actual historical /341 gate/facet/private/exported-wire ports. A selected nonlinear Skolem section is not freely an entailment of the original existential y-wire. Any translation must charge definitions and prove rule legality.

**LSPV-5:** Red-team the six forced rows, scope of extra original variables, and attempted whole-proof promotions. A proof-level simulation using nonlinear definitions would be consistent with this local theorem and must not be excluded.

**LSPV-2/LSPV-4:** Use published hard family as tests while retaining every decider, all inputs, SAT/UNSAT/malformed handling, recursive applicability and actual same-machine fully charged time/space.

**OPEN:** historical grammar and all-rule source-authenticated simulation, superpolynomial full-mixed Wbar, B1/B2/B3, Route A all-input contraction and P versus NP.

Report: research/agents/lspv-1/2026-11-06_1153_LSPV1_BITPHP_SPLITTER_AFFINE_SKOLEM_FIREWALL454.md.
Code: experiments/arc/lspv1_454_affine_skolem_standalone.cjs.
Raw: results/raw/arc/2026-11-06_1153_LSPV1_SPLITTER_AFFINE_NOGO454_summary.json.
Root main.tex was untouched because current blob SHA has zero readable content.

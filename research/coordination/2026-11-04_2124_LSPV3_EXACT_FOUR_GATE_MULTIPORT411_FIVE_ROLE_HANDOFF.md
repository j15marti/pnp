# LSPV-3/411 five-role handoff | November 4, 2026, 21:24 PST

**IDEA -> SEARCH -> ITERATE completed.** Status: **KNOWN THEOREM** (Seidler's sharp four-gate maximum on three-variable Boolean functions), **PROVED/EXACT** conservative standalone fixed-native paid-DEF multiport corollary, **COMPUTATIONAL** independent exhaustive checks; **OPEN** native LOCAL-CONVERT / individual DEF facet / GF(2) export grammar, full proof translation, B1/B2/B3, mixed superpolynomial minimum and P versus NP. No calculus, schedule, title, enabled state or role mutations.

## New restricted result

LSPV-3/410's five-DEF-per-public-output upper bound is reduced to **four**. For every acyclic paid arbitrary two-input DEF network over exactly three original source variables, and b distinct original named public output gates, there is a new fresh conservative DEF network of **at most 4b paid gates** that has the identical public-output vector for every original valuation. This is independent of original private DAG sharing, complexity and reconvergence. If output is an original variable, use a single paid identity gate to preserve a fresh public name. The bound is *sharp as a universal constant for b=1* (majority needs four). It does **not** state 4b is optimal for multiple outputs, which may share subcomputations.

The known four-gate classification is Seidler, *Minimal Circuits for Boolean Functions of Few Variables* (2022), Table 4. Our independent gate-enumeration under actual **paid** arbitrary two-input gates, without free NOT, gives exact 0..4 histogram **(3,35,114,80,24)**. The 3-gate reachable count is 232/256 and 24 remaining outputs received explicit four-gate circuits. Independent code re-enumerated 35, 1,490, 77,406 possible nonredundant circuit states at depths 1,2,3 and checked all 256 published witnesses, 8 rows each, with **6,840** truth/gate checks, plus malformed opcode and SAT/UNSAT controls. This is finite exact synthesis, not unconditional SAT computation hardness.

**Source-authentication boundary:** The reconstructed network is globally fresh and conservative, so public valuations and source model counts are preserved. Private old gate records, old DEF CNF facets, Resolution pivots, GF(2) row exports and LOCAL private circuit consumers are **not** reauthenticated by public output equality. Native /341 rule text lacks the necessary byte selectors. This is not a legal all-rule counterexample and not a full compiler.

**Evidence:** [Report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-11-04_2124_LSPV-3_EXACT_FOUR_GATE_PUBLIC_PORT411.tex); [generator](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_411_exact_three_input_paid_defs.js); [independent verifier](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_411_independent_four_gate_verify.js); [all 256 witness circuits](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-04_2124_LSPV3_EXACT_FOUR_GATE_MULTIPORT411_raw.json). Every artifact was fetched after write and compared byte-for-byte. Root main.tex reconciled **only inside LSPV-3 OWNED**, read back full new blob 56e1548a58ec458ce01f2fe20b67e067374b5bae; all outside-region bytes remained identical.

## Required literature, primary code and critiques reviewed

Governing 1204 handoff; authoritative /341 blob c87acd11; original LOCAL addendum bbcdad9a; active issue #3 through LSPV-1/409, LSPV-2/407, LSPV-4/402 and REFEREE353; AGENTS.md/CODEX.md/pnp-research skill; own /409-/410; actual Grok GROKPROOF/2026-11-05_0315_PROGRESS.md and Claude TPORT-0002. General web queries: three-input arbitrary binary gates minimal four, exact synthesis 256, Cook Reckhow 1979, Haken 1985, Raz Tzameret Res(lin). Seidler 2022 original PDF Table 4 read with a page screenshot. Authenticated github.com/openai queries: ExecCNFNodeSearchCosts, LRAT, resolution proof checker; full openai/math Lean ExecCNFNodeSearchCosts.lean (blob 1ced21f4) read. No native Rmix compiler or B3 result. Direct Google-branded search was unavailable; general web was used, not misreported as direct Google.

Haken PHP ordinary shared-DAG Resolution lower bound is system-specific with explicit N_h = Theta(h^3 log h) bit input. Cook Extended Resolution and GF(2) odd-Tseitin shortcuts are countercontrols. New 4b is an upper bound on restricted **logical** nodes; old M-bit payload parsing, physical gate evaluation, output serialization and all-phase storage are separately charged. No FLMV lower bound or B3 consequence.

## Five-role next-step handoff

LSPV-1: require noncircular, same-preselected-R B3, without presupposing short proof bits or decider-correctness reflection.

LSPV-2: derive authoritative original DEF clause/row facet selector, GF(2) output export and LOCAL private/public serialized wire contract, preferably one actual distinguishing fully typed proof record.

LSPV-3: next consumer-aware source-retracting compiler, with literal old private-facet references and AND3 original support preserved, or an explicit *legal* counterexample.

LSPV-4: account for old M-bit payload and normalized gate name lengths L(P), plus construction, access, checking, output and all-phase peak space. No conversion of logical paid q to unrestricted runtime.

LSPV-5: adversarially verify that public semantic equality does not authenticate private wire/facet uses and that 4b does not imply full native normalization.

Full native normalization, B1/B2/B3, mixed superpolynomial worst-case minimum and P versus NP remain **OPEN**.

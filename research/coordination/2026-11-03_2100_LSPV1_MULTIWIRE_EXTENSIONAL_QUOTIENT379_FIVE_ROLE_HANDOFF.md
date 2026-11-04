# LSPV-1/379 multiwire extensional quotient: five-role handoff
November 3, 2026, 21:00 PST (America/Los_Angeles). **Restricted theorem, independent specialist review pending.** No task identities, schedules, enabled states, rule grammar, weights or root synthesis ownership changed. P versus NP OPEN.

**PROVED/EXACT in the stated typed interface model:** For every circuit C with b syntactically fixed common external inputs, arbitrary acyclic internal gates/sharing, and r publicly observed wires, the entire simultaneous r-wire function is implementable by a canonical shared bank with at most

$$
\min\{r,2^{2^b}\}(b+b2^b-1)
$$

gates plus r aliases. For b=3 this is <=6656 gates plus r aliases, **independent of the original circuit gate count**. Every continuation that consults these wires only by their values, with sound local inference checks and consistent alpha-renaming, sees the same complete joint truth values. Root-only normalization from LSPV-1/376 and Red Team/328 therefore extends to multiple visible wires **under these stricter, explicit common-support and extensionality hypotheses**. This does not certify that such substitutions are legal in the still unresolved published Rmix341 LOCAL-CONVERT grammar. It does not prove any minimum lower bound or unrestricted computation transfer.

**Exact countercontrols:** Two circuits can share root x yet expose different internal wire values u=y and u=NOT y, so *root-only* quotient is unsound when named internal wires are observable. If b grows, parity has a compact O(b)-gate XOR chain but an exponential 2^b truth table. Semantic support recognition is coNP-complete per LSPV-3/382; the fixed-b assumption must be syntactic or independently certified. Converting an actual g-gate circuit by exhaustive b-input evaluation costs O(2^b(g+r)) and must read its explicit payload; an ideal short bank does not remove this physical work. Source-local parent requirements remain mandatory, no arbitrary global F=>false gate.

**Computational:** Deterministic producer 31,357 checks; independent recursive/memoized checker 47,963 checks; fixture circuits 20/130/1030 gates with 5/17/73 exposed wires and 5/11/18 distinct semantic functions. Every observed wire was checked for all eight valuations, 2048 three-bit DNF mask identities checked by each implementation, 512 sampled producer suffix contexts for each circuit, independent pairwise XOR suffix contexts, odd/even K4 models 0/8, malformed/alias-corruption controls. No claim of machine-resource hardness. Sources and raw readback separately required.

**LSPV-1:** Audit direct application to legal Rmix341 record semantics; keep B3 primary and B1/B2 distinct. **LSPV-2:** Resolve public gate alias naming and compact bank construction versus paid DEF nodes, and whether syntax has a global common-3-input invariant. **LSPV-3:** Check source ancestry and equivalence of whole interface vectors, not just root Boolean value; require authentic source-local proof DAG parents. **LSPV-4:** Charge normalization gate reads, index movement, proof verification, aliases, emitted bank, simultaneous memory, and all conversion phases; use strict rho envelope. **LSPV-5:** Attack the typed interface hypotheses with observable hidden state, semantic support oracle, names-as-data, or uncharged source-conditioned conversions; independently examine whether even the restricted claimed logical q equivalence follows from the actual rule grammar.

**Primary anchor:** Haken (1985) exponential **ordinary shared-DAG Resolution** lower bound for explicit signed unary PHP(h+1,h) of Theta(h^3 log h) encoded bits. Cook 1976 polynomial Extended Resolution PHP and odd expander Tseitin's GF2 shortcuts block transfer of that theorem to Rmix341 or all uniform SAT machines. B1/B2/B3 remain OPEN.

**Grok/Claude actual reads:** GROKPROOF/2026-11-04_0116_PROGRESS.md blob ca5a835356eb918b8cb4ab94d14de6174edeab03; research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4. No general B3 evidence in these restricted reports.

**Research artifacts**:
- research/agents/lspv-1/2026-11-03_2100_LSPV-1_MULTIWIRE_EXTENSIONAL_QUOTIENT379.tex
- experiments/arc/lspv1_379_multiwire_interface_quotient.js
- experiments/arc/lspv1_379_multiwire_independent_verify.js
- results/raw/arc/2026-11-03_2100_LSPV1_MULTIWIRE_INTERFACE_QUOTIENT379.json
- results/raw/arc/2026-11-03_2100_LSPV1_MULTIWIRE_INTERFACE_QUOTIENT379_independent.json

**Next missing arrow:** prove the actual LOCAL-CONVERT syntax supports a sound, completely charged extensional public-wire replacement while every original source/local premise remains authenticated. No unrestricted SAT lower bound follows merely from source incidence, DNF banks, GF2, or shortest proof DAGs. P versus NP OPEN.

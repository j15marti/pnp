# LSPV-3/418 five-role handoff: source-fixed paid-DEF polarity gauge

**November 5, 2026, 01:57 PST.** Fixed native $R_{\mathrm{mix341}}$, original sources, charged weights, agent identities, schedules and enabled states unchanged. P versus NP OPEN.

## IDEA → SEARCH → ITERATE

Hypothesis: unlike merely renaming an auxiliary wire, complementing its **value** is a legal source-preserving transformation of every globally fresh paid native two-input DEF gate, provided all later gate tables and typed consumers are simultaneously conjugated. Falsifiers: (1) lost conservativity/freshness; (2) repeated/reconvergent inputs; (3) wrong unchanged GF(2) RHS; (4) silently assuming unratified native DEF facets or LOCAL port selectors. (1) and (2) pass proof and tests; (3) fails the negative control; (4) remains an unmet grammar obligation.

For every native legal acyclic paid-DEF prefix $D: z_i=f_i(u_i,v_i)$ with $a$ gates, original CNF $F$ and output flip vector $\delta\in\{0,1\}^a$, define

$$
f_i^\delta(s,t)=f_i\bigl(s\oplus\delta(u_i),t\oplus\delta(v_i)\bigr)\oplus\delta(z_i),\qquad \delta(x)=0\ (x\text{ original}).
$$

The map fixing every original value and sending $z_i$ to $z_i\oplus\delta(z_i)$ is a bijection of satisfying assignments to $F\land D$ and $F\land D^\delta$. The same $a$ paid native DEF nodes, original source bytes, input names, and unique extensions remain. The $2^a$ fully labeled value gauges are equivalent presentations and cannot be counted as independent lower-bound work. **PROVED/EXACT for native paid-DEF prefix semantics**, external specialist review pending.

For a properly authorized typed GF(2) row, the required correction is

$$
\bigoplus_{v\in S}v'=b\oplus\bigoplus_{v\in S}\delta(v).
$$

Every signed clause literal involving a flipped paid wire must also have its sign inverted. The affine, clause and Resolution semantic identities are proved, but full native downstream proof replay is **CONDITIONAL** because original /341 does not settle individual DEF-facet selectors, private LOCAL exported wires or GF(2) row selectors. No new rule is invented and no unratified row is claimed native.

## Verification

Python: 80 six-gate seeded networks (seed 418), all 64 output flips, 16 assignments, 1,832,971 assertions. Independent JS: 70 differently generated six-gate networks, all 64 flips, 16 assignments, 1,433,607 assertions. SAT source $F^+=(x_0\lor x_1)\land(\neg x_0\lor x_2)$ has 8 models. Adding contradictory $(x_0),(\neg x_0)$ yields zero models. Four Python malformed gate records, three JS malformed records and wrong uncorrected GF(2) RHS rejected. The first Python attempt mistakenly claimed 10 SAT models, corrected to exact 8 after enumeration. These are computational checks, not shortest-proof certificates.

## SEARCH and exact corpus

Read verified November 2 refocus, issue #3, AGENTS.md, CODEX.md, repo skill; original /341 blob c87acd11; grammar addendum /384; relevant LSPV-1/412, LSPV-2/412, LSPV-3/414--417, LSPV-4/402 and /408, REFEREE358. Reviewed actual GROKPROOF/2026-11-05_1218_PROGRESS.md (blob d3183283), Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). None supplies B3.

General web queries: Cook-Reckhow proof systems, Haken ordinary Resolution PHP, Pich-Santhanam Extended Frege, AIG complemented edges, Gocht-Nordström parity proofs. Primary publisher records read. **Direct Google-branded search unavailable**; general indexed-web used, not claimed Google. Authenticated github.com/openai searches: ExecCNFNodeSearchCosts, CookLevin, LRAT proof checker; read full openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4. It is not a same-R compiler.

LSPV-1/348 previously established signed ORIGINAL-input orbit cost invariance; LSPV-4/402 already established auxiliary NAME alpha-renaming. Here the native operation is OUTPUT-VALUE complementation, not either of those. Standard logic-synthesis complemented edges are related; no academic novelty claimed. Haken PHP is ordinary shared-DAG Resolution $2^{\Omega(h)}$ lines on unary PHP with $\Theta(h^3\log h)$ source bits. Cook ER PHP and native short odd-Tseitin GF(2) remain countercontrols. REFEREE358 already blocks polynomial GF(2)-erasing source-only Resolution retraction.

## Cost, two obligations, and roles

Paid node count stays $q_{\rm DEF}=a$. Input $E$-bit prefix must all be read; validation, construction, serialization and all-phase peak charged polynomial in $N+E+a$. Flat native DEF-only alpha-compacted outputs use $O(N+a(N+\log(a+2)))$ bits, preserving large original variable names. Full arbitrary LOCAL payloads are NOT covered.

Outstanding: (1) settle exact native DEF facets, LOCAL private/exported wire and GF(2) selector bytes and prove full mixed consumer-preserving polynomial normalization, or a LEGAL counterexample; (2) prove/refute noncircular same-calculus B3, $\mathrm{SAT}\in P\Rightarrow \overline W_{R_{\mathrm{mix341}}}$ polynomial. Both OPEN.

LSPV-1: B3 quantifiers/reflection. LSPV-2: fixed byte grammar/selectors. LSPV-3: authenticated hypergraph ports and gauges. LSPV-4: full bit work and all-phase peak. LSPV-5: independent adversarial rule/retraction audit. Existing roles/schedules/states untouched.

Artifacts: research/agents/lspv-3/2026-11-05_0157_LSPV-3_NATIVE_DEF_POLARITY_GAUGE418.tex; experiments/arc/lspv3_418_gauge_producer.py; experiments/arc/lspv3_418_gauge_independent.js; results/raw/arc/2026-11-05_0157_LSPV3_NATIVE_DEF_GAUGE418_raw.json; research/coordination/2026-11-05_0157_LSPV3_NATIVE_DEF_POLARITY_GAUGE418_FIVE_ROLE_HANDOFF.md.

Root main.tex fetch returned current SHA but zero content even for first 35 lines, so it was NOT overwritten. Request LSPV-5 later ownership-safe reconciliation. Full normalization, B1, B2, B3 and P versus NP remain OPEN.

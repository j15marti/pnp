# LSPV-2 SOURCE-EXACT-MIXED-ESCAPE368, five-role research handoff

November 3, 2026, 11:12 PST. Source-first established lower bound, exact transfer direction and its explicit failure for the full preselected mixed calculus. This note does not alter any existing task identity, ownership, enabled state, title, offset or schedule.

## Prior claim and controlled increment

LSPV-1 `research/agents/lspv-1/2026-11-03_0956_LSPV-1_RESTRICTION_STABLE_REFLECTION367.tex` (blob 64f4e87aa7c6050d088bb599ec4919aa119ba10e) already proved that a witness-transparent clocked selector source inherits strict Resolution lower bounds by source-exact partial restriction. LSPV-5 `research/main/2026-11-03_1048_MAIN_REFLECTION-FAMILY-EQUIVALENCE-REFEREE318.md` (d5164f4e977aac7c2b420c0989f26b972ba6d902) independently reviewed and localized B3 under hypothetical mixed restriction stability. **Neither theorem is claimed new here.**

New incremental construction: a pinned equality-recognizer selector source `U(F_h)` made from a known odd cubic expander Tseitin 3-CNF. Its authentic source clauses are one-hot selectors, proper width-three guarded witness clauses, an ordinary binary AND equality chain and a positive unit output. There are no new calculus rules or free machine-correctness axioms. Fix all selectors and gate values, and the source clause multiset reduces to **exactly** `F_h`, with no auxiliary contradiction.

Known Urquhart (1987) / Ben-Sasson–Wigderson (2001) give a cubic expander odd-Tseitin unrestricted shared-DAG Resolution lower bound `W_Res(F_h) >= 2^(c h)-4h` for some c>0. Resolution restriction closure gives `W_Res(U(F_h)) >= W_Res(F_h)`.

**Same-source mixed escape:** In unchanged Rmix341, derive all 3m selected units backwards from the equality chain using 2(3m-1) genuine RES inferences; derive the m original signed clauses using 3m RES steps against guarded sources; extract h local parity rows with 3h paid AND3 nodes; XOR h rows in h-1 paid nodes. With m=4h the exact displayed upper certificate cost is **40h-3**. Thus a source-exact reflecting formula is exponentially Resolution-hard yet admits a linear-in-h mixed refutation, without assuming the full mixed calculus is restriction stable. This is a **FAMILY FAILURE** of a proposed unrestricted hardness transport, not a disproof of worst-case mixed hardness elsewhere.

Encoded source dimensions: `V(U)=n+6mn+(3m-1)`; `C(U)=3m(1+binom(2n,2))+8mn(n-1)(n-2)+3(3m-1)+1`. For cubic odd Tseitin, `N_U=Theta(h^4 log(h+2))` ASCII bits, distinct from original `Theta(h log h)` bits. No rescaling is free.

## Independent finite evidence

Python producer and separately written no-import JavaScript verifier passed **170,283 assertions**, including every authentic source-line check, separate SHA-256 reconstitution, genuine RES pivots, local AND3 truth tables, row aliases, GF(2) sums, exact source restriction, 8+16 single-clause-deletion SAT witnesses, eight malformed-DIMACS rejections and nine corrupted-certificate rejections. Opposite three-variable parity pair: 8 source clauses, U has 170 variables/838 clauses, mixed proof 77 nodes, original UNSAT. Odd K4: 16 original sources, U has 629 variables/18,718 clauses and 409,694 actual ASCII DIMACS bytes, mixed proof 157 nodes, original UNSAT. Even K4 counterpart: 8 original satisfying assignments, selector source SAT, no UNSAT proof. The finite checks are **COMPUTATIONAL upper certificates**, not a global optimum or an asymptotic computational lower bound.

Full raw dataset: `results.json` SHA-256 `a6419561d86172e4c97b883988141a2445810393b587dba3d6e90e88a394f1d7`; full producer `af17d6a63f05e8d451196d27768c71edab287d48bc66b16dff7e52765c8ce162`; separate checker `63715cc77ff768b99836ae3603ded06bbcee6129c9d508d8fb3ebdc887c85d12`. Full files are in the user reproducibility archive. The GitHub public checker is explicitly compact and does **not** purport to replay the complete paid-node DAG; the GitHub public JSON is a ledger.

## Independent other-agent assessments, exact scope

Actual directories were located in the GitHub tree. Read `GROKPROOF/2026-11-03_1518_PROGRESS.md` (blob 234fc189b01fa163eb10e128556e9d22e085b755): universal charged ARC contraction remains unproved; its restricted low-space barrier does not justify the present reflection step or B3. Read `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67): portfolio bound is restricted to its alternation-trading rules, not all SAT algorithms. Prior Grok 12:17 UTC upper-as-lower query-cost issue is credited to earlier audits rather than presented as a discovery. Searches of github.com/openai returned unrelated uses of mathematical resolution.

Read governance: November 2 12:04 latest refocus (current cumulative file), active issue #3, AGENTS.md, CODEX.md, pnp-research skill; original LSPV-2 341/365/366/INLINE-CONE367; LSPV-1 367; LSPV-4 366 and LSPV-5 318. Primary literature verified Urquhart, Ben-Sasson–Wigderson, and contemporary Pich–Santhanam / Krajicek on feasibility reflection and circuit rewriting. No novelty claimed for restriction arguments.

## Outbox and publication safeguard

- `research/agents/lspv-2/2026-11-03_1112_LSPV-2_SOURCE_EXACT_MIXED_ESCAPE368.tex`
- `experiments/arc/lspv2_368_source_exact_public.js` (compact public regeneration)
- `results/raw/arc/2026-11-03_1112_LSPV2_SOURCE_EXACT_MIXED_ESCAPE368_public.json`
- `research/coordination/2026-11-03_1112_LSPV2_SOURCE_EXACT_MIXED_ESCAPE368_FIVE_ROLE_HANDOFF.md`

The full local archive contains the complete separately implemented checker, producer, full actual source DIMACS and proof dataset, full LaTeX and BibTeX, validated PDF and SHA-256 manifest. Root main.tex was deliberately **not** overwritten: its authenticated fetch returned zero content with blob SHA d07161c26020ac3d985b278211f101ba8b976ef8. The full repository could not be checked out in the isolated host, hence no repository-wide preflight. No task-state changes.

## Exact next implication

Focus on the **full mixed** correctness/reflection bridge. The new proof shows source-exact Resolution restriction inheritance is compatible with very cheap mixed derivations. A transfer must separately handle all permitted GF(2), AND3, paid extensions and named LOCAL-CONVERT interfaces. B1/B2/B3 and the superpolynomial worst-case Wbar_R remain OPEN. P versus NP remains OPEN.

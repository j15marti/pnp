# LSPV-4 TREE-OVERLAP-SAT241, October 29, 2026, 23:06 PDT

**To LSPV-1 (formal lead), LSPV-2 (circuit/reduction builder), LSPV-3 (adaptive certificate), LSPV-5 (red team and root synthesis).** Active user directive: [coordination issue #3](https://github.com/j15marti/pnp/issues/3); issue #2 equity work remains paused. The five existing task identities, enabled states and hourly schedules are unchanged.

## PROVED/EXACT, restricted, independent referee pending

For each ORIGINAL source clause `C_j`, each signed occurrence `x_{i,j}`, local S_j (all literals TRUE), U_j (all FALSE), and inversions, preserve one globally coherent source-variable assignment. The known SS/SU/US/UU feasibility matrix was independently rechecked; incompatibility between local extremes does NOT imply clause-level UNSAT. Full 3-bit truth vectors and 0^n/1^n/intermediate flips are recorded in the downloadable full raw experiment.

Let `p_j(alpha)` be the exact uniform-completion probability source clause j is ALL FALSE, and `p_jk(alpha)` its simultaneous false probability with clause k. For any fixed source-clause spanning tree T, Hunter's known union bound gives:

`B_T(alpha)=1-sum_j p_j(alpha)+sum_{(j,k) in T} p_jk(alpha) <= Pr(F SAT | alpha)`.

**A positive bound guarantees a full SAT witness.** Holding the tree fixed, conditional averages mean one of each pair of variable branches maintains positivity, giving a charged polynomial-time deterministic witness constructor on this restricted positive-bound class.

**Sharp root-only obstruction:** for duplicate-free proper width-k CNF with m original clauses, `B_T(empty)<=1-(m+1)/2^(k+1)`. At width three, m>=15 rules out a positive unconditioned tree certificate, and the trivially SAT star `AND_j(x OR y OR z_j)` attains equality. Conditional bounds after partial assignments are *not* ruled out.

**Small strict22 implication:** for m=2^k proper kCNF, UNSAT iff all false-clause cubes pairwise disjoint (Kullmann hitting clauses); in strict signed (2,2) proper 3CNF with n=6,m=8, only 24 signed-opposition occurrence-pair witnesses exist for 28 clause pairs, hence every such source is SAT.

## FALSIFIED/RETIRED

Adding **ALL** pairwise overlaps as if they were independent creates a false SAT certificate: UNSAT 8-sign-pattern CNF on x1..x3 augmented by 14 star clauses has naive expression 91/16=5.6875>0, but actual model count 0 and valid tree bound -13/16.

## COMPUTATIONAL charged and hostile controls

19 named source fixtures; 5,604 exact SS/SU/US/UU checks; 66,552 full source-complement checks; all 46,656 balanced 6-variable signings for a fixed incidence skeleton SAT, with 8..22 models. Horn, 2SAT, XOR, K4 odd-charge Tseitin, random, polarity rename, and source-parent resolution adversaries included.

**Identical-source baseline saturated-UP DPLL vs tree-prefilter+DPLL fallback**, reported selected operations include failed prepass and all original-source reads:

| Source | Root bound | DPLL nodes base/tree | Selected work base/tree |
|:--|--:|--:|--:|
| strict22 SAT cyclic, n=9,m=12 | 1/64 | 6 / 0 | 449 / 2393 |
| strict22 UNSAT W1, n=15,m=20 | -1 | 151 / 151 | 11218 / 16271 |
| strict22 SAT S, n=15,m=20 | -55/64 | 9 / 9 | 975 / 6030 |
| SAT star14 | 1/16 | 3 / 0 | 425 / 3145 |
| SAT star15 | 0 | 3 / 3 | 455 / 2790 |
| UNSAT hitting8 | 0 | 7 / 7 | 222 / 631 |

On W1 same-run Python traced peak 3456 B baseline vs 14160 B controller; not native machine space. Controller materializes O(m^2) pair weights and retains exponential worst-case DPLL fallback. It reduces SAT search nodes on select fixtures but **increases total selected work** in all displayed comparisons.

## Provenance and publication

Readback-verified GitHub concise formal report: [TREE-OVERLAP-SAT241.tex](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-29_2306_LSPV-4_TREE_OVERLAP_SAT241.tex), blob `950ee40c1605aad13ce1f053e5316211b4f74dd0`; independent [JavaScript checker](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_TREE_OVERLAP_SAT241_compact_check.js), blob `b66767ede209efaa4107b620ff6cc180989eee81`; [selected raw summary](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/LSPV4_TREE_OVERLAP_SAT241_public_results.json), blob `c02295b630936c214bc794c54de86b647ec17710`.

Full local source (19,473 B) SHA256 `03cf03eefdf28293b212e6b15c193f20333b8efad1b4bedd7901f22823a404b0`; complete 820,480-B raw JSON SHA256 `d415f27bfb5348bd54175e2e52b65bd4d8f451920eaa07866f475a85050a4685`. The full four-page PDF and local raw/code form a downloadable bundle. GitHub LaTeX is shorter and not byte-identical to expanded local PDF source. Library upload **PENDING/BLOCKED**: each container_path upload returned `container_session_unavailable`; folder `/PNP/LSPV-4/2026-10-29_TREE_OVERLAP_SAT241` was created, but files were not uploaded.

**Root main.tex integrity alert for LSPV-5:** fresh source readback had blob `eff8cd89cc3c4e83f6dc8ab03dff4bbce046f90a`, only 5,344 characters, missing both `% BEGIN LSPV-4 OWNED` and `% END LSPV-4 OWNED`. LSPV-4 did **not** modify root, per AGENTS.md ownership protocol. Recover from authenticated history before attempting synthesis; do not invent old manuscript regions.

## Next OPEN lemma

Construct or falsify a charged, polynomially discoverable **conditional higher-order overlap certificate** whose bound is positive for all members of an unbounded, nontrivial strict22 SAT family with matched UNSAT controls; compare failed strategies, source access, exact proof acquisition and same-run peak space. P versus NP remains OPEN.

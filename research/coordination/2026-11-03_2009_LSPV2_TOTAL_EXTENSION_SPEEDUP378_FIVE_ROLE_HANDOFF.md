# LSPV-2/378: conservative total-extension / source-essentiality transfer no-go

**November 3, 2026, 20:09 PST.** **PROVED/EXACT** theorem by explicit witness constructions and Haken/Cook published results; finite tests **COMPUTATIONAL**. **OPEN:** full Rmix341 minimum-hardness, B1/B2/B3, unrestricted machine lower bounds, P versus NP. Existing five task identities, schedules, enabled states and Rmix341 grammar/weights unchanged.

## Decisive new result
For canonical unary PHP \(P_h\), Haken proved every unrestricted shared-DAG **ordinary Resolution** proof requires \(2^{\Omega(h)}\) lines; Cook proved polynomial Extended Resolution proofs. Move Cook's \(O(h^3)\) acyclic extension gate definitions (four 3-CNF clauses per gate) into the initial source to form \(G_h=P_h\wedge D_h\). Then:

$$
W_{\rm Res}(P_h)=2^{\Omega(h)},\qquad W_{\rm Res}(G_h)=h^{O(1)}.
$$

But **all original signed PHP clauses remain literally present, each remains clause-deletion essential, and for every original assignment there is exactly one auxiliary extension satisfying \(D_h\)**. The two explicit source sizes are both \(\Theta(h^3\log h)\) bits. Each deleted-occupancy witness is an injection of the other \(h\) pigeons; each deleted-collision witness places exactly one designated pair into the same designated hole. The witnesses extend uniquely through the Cook gates. The only published asymptotic lower bound involved is Haken's **restricted-proof-system** bound; no unrestricted SAT lower bound follows.

This sharply limits a proposed invariant based solely on *authenticated original signed hypergraph, original-source preservation, clause deletion witnesses, conservative totality or original source-size*. A polynomial conservative augmentation can erase the exponential ordinary-Resolution obstruction while preserving all those. The earlier LSPV-1/378 linear source-arity floor survives and does not conflict.

This is a theorem for *ordinary Resolution after adding definitional premises*. It is **not** a freely justified ordinary-Resolution inference from \(P_h\) and it is **not** a new independent full-Rmix341 proof certificate. A paid signed-AND2 + local-resolution compiler should be checked rule-by-rule against actual LOCAL-CONVERT/DEF grammar before asserting a specific full-R bound.

## Independent controls
Python producer **22,596** assertions, independently authored Node verifier **132,587**, and GitHub-readback public JS code independently executed in V8 **123,413** assertions. Six \(h=1..6\) sources, every original-clause-deletion SAT witness, exhaustive original assignments through \(h=3\), six malformed encodings, odd/even K4 parity (0/8 models), corrupted auxiliary-wire output rejection. Neither proof-complexity theorem was regenerated or re-proved by these finite tests.

## Handoff by role
- **LSPV-1:** Do not interpret deletion-fibre survival as stronger-than-linear hardness. Continue B3, with the exact fixed-calculus rule semantics and correct \(\forall A\exists p_A\forall N\) quantifiers.
- **LSPV-2:** Next compile Cook's actual local steps into source-authenticated paid Rmix341 DEF/RES/LOCAL-CONVERT nodes, with a proof stream and independent checker; count bit length, retrieval and shared DAG cost.
- **LSPV-3:** Test whether any invariant using original-source hypergraph and every surviving deletion witness survives these total functional extensions. Source provenance alone cannot transfer Haken's exponential Resolution bound.
- **LSPV-4:** Charge parsing, constructor, all pointer/gate reads, definition checking, proof output, peak space and nonmaterialized/lazy variants. \(\Theta(h^3\log h)\) bit writes for explicit extension, not free; no FLMV transfer.
- **LSPV-5:** Attack whether Cook's recursive gate list alone suffices for the stated polynomial ordinary Resolution proof, and whether any opaque Rmix rule violates source-ancestry typing. Verify no B1/B2/B3 inference slipped in.

## Actual Grok and Claude assessment files reviewed
Grok: \`GROKPROOF/2026-11-04_0116_PROGRESS.md\` sha \`ca5a835356eb918b8cb4ab94d14de6174edeab03\`; \`GROKPROOF/2026-11-03_1912PST_PROGRESS.md\` sha \`66576e888e5c147c64264d4856089b6d3e7903e3\`. Both retain the unproved universal fully charged ARC/FLMV contraction.

Claude: \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\` sha \`1f9fc727d3e2b009cba7afec2a93beb62959dd67\`; \`research/agents/claude/2026-09-30_CLAUDE-0266_review.tex\` sha \`694c1c8169d9a193397b94e6ee572c476e639a94\`. The former proves results in its restricted alternation-trading portfolio rules, not B3; the latter documents failed representation-insensitive influence/Fourier candidates. Neither upgrades proof complexity to all-algorithm hardness.

## Exact artifacts and governance
- **Report:** \`research/agents/lspv-2/2026-11-03_2009_LSPV-2_TOTAL_EXTENSION_SPEEDUP378.md\`.
- **Public standalone code:** \`experiments/arc/lspv2_378_conservative_extension_public.js\`, blob \`b7b1780645299f9a5abe5f959ddb13903e30564f\`.
- **Machine-readable ledger:** \`results/raw/arc/2026-11-03_2009_LSPV2_TOTAL_EXTENSION_SPEEDUP378_public.json\`.
- Prior art: \`research/coordination/2026-11-03_1955_LSPV1_CLAUSE_DELETION_FIBRE378_FIVE_ROLE_HANDOFF.md\`, \`research/coordination/2026-11-03_1948_LSPV5_TO_FIVE_ROLE_UNIFORM-GENERATOR-COLLAPSE-REFEREE327.md\`, LSPV-2/377.
- Primary papers: Haken 1985 TCS 39:297–308; Cook 1976 SIGACT News 8(4):28–32; Grosof et al. arXiv:2207.11284.
- Read \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, coordination 2026-11-02_1204, issue #3. The public GitHub web returned 404 for private repository URLs, but authenticated connector reads and writes succeeded.
- **Next gap:** full Rmix341 gate/LOCAL-CONVERT semantics, independently verifiable Cook-size proof and genuine worst-case B3. **P versus NP OPEN.**

# LSPV-1/546: Certified affine-coset conditioning reduces a scoped mixed-to-Res(XOR) proof compiler

**2026-11-09 15:16 PST | Route B lead | PROVED/RESTRICTED (given an authenticated prior compiler) + COMPUTATIONAL. P versus NP OPEN.**

**New material evidence:** [P2-L1-546], dependent on [P2-L2-369] and related [P2-L3-456]. This is NOT a native-full-calculus claim. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain **OPEN**. No historical rule, unit weight, agent identity, route allocation or scheduled task was modified.

## IDEA and four falsifiers, fixed before SEARCH

**Candidate.** The prior source-authenticated locally opaque mixed-to-Res(XOR) compiler branches over every assignment to the $b$ original variables directly exposed to paid DEF gates, at cost $2^b$. If an independently **source-certified and paid** affine system of rank $r$ restricts these variables, then replace this by exactly $2^{b-r}$ guarded branches. This is a proof-to-proof normalization with a separate cost ledger for learning those affine equations, not free semantic SAT pruning.

- **F1:** The affine relations might be valid semantically but have no short original-source Res(XOR) certificates. **TRUE potential obstruction:** their full size $P_H$ is retained; on UNSAT F semantic entailment alone gives no discount.
- **F2:** Assigning the $b-r$ free coordinates might fail to uniquely fix all original DEF inputs. **Rejected** under an authenticated consistent rank-$r$ affine system, by explicit GF(2) row reduction.
- **F3:** The restricted source clause or signed literal might lack a derivation from the actual source using legal externally typed RES, guard prefixing and semantic weakening. **Rejected** for the declared Res(XOR) rules by the construction below; it is still **OPEN** for the historical mixed byte grammar.
- **F4:** The reduction could omit some legal shared-DAG inference, reuse a paid owner twice, introduce free native branching, or count a rank equation as an oracle. **Avoided** in the theorem by given-proof simulation, full external source proof cost and charging the blocker join. Full historical coverage remains OPEN.

## SEARCH and continuity

Read both complete root trackers: proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and proof2.txt initial blob `f00fbdc995b88a1b7f5676675855e2d59d1a8bb7`; current issue #3 (1,521 comments at read), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md and required abstract-interpretation handoff `research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md` (blob `8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b`). Actual peers reviewed: LSPV-3/542 (DEF facet completeness), LSPV-5/469 (paid-history/legality correlation), LSPV-1/545 (nonadditive cover potential). Reused LSPV-2/369 source-authenticated compiler at `research/agents/lspv-2/2026-11-03_1212_LSPV-2_BRAUN_GF2_NATIVE_BACKTRANSFER369.tex` (blob `927ba2172c920a29e1094867038ace7bf2faa465`). Read original semantic /341 declaration (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`), actual Grok `GROKPROOF/2026-11-09_2015_PROGRESS.md`, and Claude `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`. Neither authenticates the missing native bytes.

Prior duplication control: LSPV-2/514 uses affine coset caching for deterministic guest **input-read traces**, not the present source-certified **refutation backtranslation**. LSPV-3/456 combines /369 with Pang's PC-degree theorem but uses the unconditioned $2^b$ bound. Linear algebra and guarded reasoning are standard; no academic novelty claim is made.

Required change-aware GitHub source reads: `konard/p-vs-np/README.md` (`0e0ec77f...`), `konard/p-vs-np/scripts/proof_status.json` (`93b77ed3...`), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (`18d693ea...`), `meelgroup/frat-xor/format.md` (`986a21aa...`), `tanyongkiam/cake_lpr/README.md` (`e94f45e9...`), `peitl/short-proof/README.md`, `MassimoLauria/cnfgen/cnfgen/families/tseitin.py`, `openai/math/README.md` and `anthropics/formal-math/README.md`. None supplies the historical R_mix341 DEF/LOCAL-CV accepted-byte parser. Public indexed literature queries covered Braun 2026 bit-PHP Res(XOR), Pang 2026 fixed-degree Res(PC), source-certified extension shortcuts and Cook's PHP extended resolution. No separate Google-branded search, official CakeML proof checker or native historical R_mix341 execution was claimed.

## Theorem 546.1: paid affine conditioning of a locally opaque mixed proof

Fix a binary-encoded UNSAT CNF F, with m original indexed source clauses. Let pi be ANY legal acyclic, source-authenticated proof in the **locally opaque, wire-defined subgrammar explicitly fixed in LSPV-2/369**, with q distinct unit-paid derived nodes. Let B be the set of b distinct original variables directly entering its paid DEF owners. The given-proof /369 normalization permits arbitrary shared RES, GF(2) XOR rows, local three-original-variable factors and definitions whose outputs are determined by an assignment to B.

Let H be a **consistent** system of r independent affine equations over GF(2) on precisely variables B, each proved as an unconditional original-source consequence of F by an explicit semantic Res(XOR) DAG. Let P_H count every non-source proof node needed to derive these equations, including any subsequent XOR row reductions. Neither H's semantic truth nor Gaussian elimination is assumed free.

Then there is an original-source Res(XOR) refutation of F with node count

$$
\boxed{
S_{\oplus}(F)\le P_H+C\,2^{b-r}(b+1)(m+q+1)
}
$$

for an absolute constant C determined by the existing /369 local-node translator and the external semantic Res(XOR) grammar. This counts source records in the second term and all shared paid copies once. It is an existence/simulation bound on explicit proof nodes, NOT a runtime bound. No such theorem is claimed for the unauthenticated full historical grammar.

**Proof.** Row-reduce H, using certified affine unit steps (at most polynomial in r) with the actual elimination charged inside P_H. Choose b-r free original variables Y. For each beta in {0,1}^Y, the affine equations uniquely extend beta to an assignment alpha(beta) of ALL B. Let

$$
D_{\beta}=\bigvee_{y\in Y}(y\ne\beta_y).
$$

From each certified normalized unit equation expressing a dependent original bit x as an affine function of Y, one valid semantic weakening derives the guarded literal $D_{\beta}\vee(x=\alpha_x(\beta))$: if the guard is false, the normalized equation forces that value. For each free bit, its corresponding guarded-value statement is tautological and need not be a paid premise.

Evaluate the paid acyclic DEF network under alpha(beta), then run the already-established /369 local translation of the restricted mixed proof. To lift a restricted ORIGINAL clause C, start with its exact signed, indexed source clause in F. Each dependent B-literal falsified under alpha(beta) is removed by correctly oriented RES against its derived guarded-value literal; each falsified free B-literal is already contained in D_beta. A satisfied restricted clause is omitted. This yields a legitimate $D_{\beta}$-guarded version of every required original-source premise at O(b+1) extra node overhead per clause. Add the **same guard** to the /369 translated local-factor and XOR deductions. Semantic weakening and complementary affine RES preserve this common disjunct, including wide GF(2) rows and shared proof nodes. The restricted terminal contradiction gives D_beta, at cost O((b+1)(m+q+1)) per beta. All these are external Res(XOR) inferences; no split/discharge rule is inserted into R_mix341.

Resolve the $2^{b-r}$ resulting blockers in a binary tree over the free variables Y, paying $2^{b-r}-1$ RES nodes, yielding false. H's source-certified proof is shared once across branches. Summing yields the displayed bound. Every branch is authenticated from original F; cost of constructing H is fully included. QED, conditional on the cited /369 given-proof compiler and external rules.

**Noncircular qualification.** An UNSAT source semantically entails every affine equation, so treating H as free would be a hidden UNSAT oracle. Here an equation only qualifies when an actual source-indexed certificate with cost P_H is supplied. A certifier may fail to find any useful H. No new unrestricted proof-system lower bound follows.

## Corollary 546.2: quantitative hard-source firewall

Braun 2026 proves $S_\oplus(F_n)>\exp(n/(32768\ell^2))$ for bit-PHP with n=2^ell holes, ell>=32, in unrestricted shared-DAG Res(XOR). Applying the theorem only when H has the required external certificates gives the precise restricted tradeoff

$$
P_H+C 2^{b-r}(b+1)(m+q+1)
> \exp\left(\frac{n}{32768\ell^2}\right).
$$

It does **not** forbid a short mixed proof when b-r is large or P_H itself is enormous. Pang 2026 gives an analogous $\exp(\Omega(n))$ lower bound for a published random proper signed 3-CNF family in a distinct bounded-degree Res(PC1/F2) calculus. Using it here additionally requires the /456 semantic-to-syntactic simulation and all its line-bit charges; no numeric constant is copied across that conversion. These are *restricted model comparisons*, not [P2-B1] or B3.

## Established-family ledger and hostile shortcuts

- Braun bit-PHP: n=2^ell holes, n+1 pigeons, (n+1)ell Boolean input variables, m=n*binom(n+1,2) width-2ell collision clauses; binary encoded length Theta(n^3 ell^2) under standard signed DIMACS. Every DAG Res(XOR) proof has >exp(n/(32768 ell^2)) lines for ell>=32 (Braun 2026, preprint with Lean claims). **Shortcut:** Cook's polynomial ER PHP proof can escape a restricted parity-only lower bound; charged DEF and full grammar remain uncontrolled. Lower-bound transfer into strict 3-CNF requires a separate simulation theorem.
- Pang proper strict 3-CNF: n variables, 8n independently sampled proper signed width-three clauses with replacement, length O(n log n); exponential DAG Res(PC1/F2) lower bounds with high probability conditional on the cited PC degree theorem. **Shortcut:** paid definitions and full LOCAL wire export are not covered by /369. The present affine-conditioning theorem does not magically restore all-native coverage.
- Odd cubic Tseitin: h vertices, 3h/2 original edge bits, 4h strict ternary source clauses; Urquhart's expander subfamily is exponential in ordinary Resolution only. An explicit AND3/GF(2) refutation of declared /341 cost 4h-1 is a compulsory upper control, not an abstract path to exclude.

## ITERATE: independently checked ORIGINAL K4 finite certificate

For the six-edge K4 odd-charge original strict signed 3-CNF, all 16 exact source clauses are indispensable. Independent enumeration finds 0 satisfying assignments; even-charge control finds 8. Three selected vertex parity rows have rank r=3 on b=6 original edge variables. Each row has a **source-indexed EXTERNAL semantic Res(XOR) derivation** with eight E-or-forbidden-assignment weakenings and seven oriented binary cuts: 24 weakening nodes and 21 cut nodes total. RREF requires four additional XOR row operations in the particular elimination trace. Exactly eight assignments to the remaining three free edge variables extend to these rows, versus 64 assignments to all six original variables. Every completion falsifies a clause of the fourth vertex, and every guard-literal implication from a single normalized parity row or a free-bit tautology was checked over all 64 assignments. This tests the semantic guard-lift lemma, not a run of the full /369 compiler or native R_mix checker.

Two implementations: independent Python 1,837 grouped checks and independent Node.js 1,778 checks, both PASS. The exact published standalone JavaScript was refetched from GitHub and independently replayed in V8 with 1,778 PASS checks. Source deletion, odd/even parity, row-provenance, complementary pivot and inconsistent-row controls are included. The small K4 graph is **NOT** asserted to be a published expander-hard instance.

Published evidence: `experiments/arc/lspv1_546_coset_guard_independent.cjs` (full original-source independent verifier); `results/raw/arc/2026-11-09_1516_LSPV1_546_AFFINE_COSET_BACKTRANSFER_RAW.json` (machine-readable counts). Independent Python complete source and witness JSON are retained in the current conversation's reproducibility ZIP. No official Res(XOR) checker or historical mixed checker was run.

## Resource ledger and precise remaining gap

Logical node upper-bound improvement replaces 2^b by 2^(b-r) only after paying P_H; branch depth, complete certificate bits, evidence generation, source/index lookups, Gaussian row elimination, guard literals, repeated conditioned copies, serialization, verifier execution and peak simultaneous memory are separate. The reconstructed proof uses at most the displayed number of logical nodes; its explicit bit encoding may be larger by a polynomial factor in n+m+q+b plus original identifier bit lengths. On K4 this witness is finite only. No guest runtime, general SAT machine bound, peak-space guarantee from time alone, or Route A FLMV contraction is asserted.

**Three ledgers:** (i) chosen solver classes: no all-input algorithm or machine lower bound; (ii) whole fixed historical R_mix341: still OPEN due to DEF facet/export bytes, LOCAL-CONVERT and branch context, so no global Wbar_R lower bound; (iii) unrestricted deterministic SAT machines: no B1/B2/B3 bridge and no P != NP proof. LSPV-3 should test whether source-certified affine row imports, each native selector and guard RES have actual byte-level accepted traces. LSPV-5 should attack the legality/paid-history correlation, zero-cost closures and whether H certification smuggles in the target contradiction. Known cheap shortcuts are permitted.

**Publication:** report/code/raw/handoff and tracker reconciliation receipts are maintained separately. No root main.tex edits unless complete safe original is readable. Independent full repository report preflight was unavailable in this scratch workspace. All original inference weights, five roles, schedules, enabled states and 2 Route A / 3 Route B allocation unchanged.

**P versus NP remains OPEN.**

### References
[1] K. Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2 (2026-11-03), https://arxiv.org/abs/2609.23015.
[2] S. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), https://arxiv.org/abs/2610.00837.
[3] D. Itsykson and D. Sokolov, *Resolution over Linear Equations Modulo Two*, Annals of Pure and Applied Logic 171(1), 2020.
[4] S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976.

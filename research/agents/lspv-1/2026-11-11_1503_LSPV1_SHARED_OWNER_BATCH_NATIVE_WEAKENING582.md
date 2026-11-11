# LSPV-1/582: one globally paid signed AND2 owner weakens a batch of original clauses at amortized native cost

**2026-11-11 15:03 PST | General SAT Lower-Bound Lead | historical Route B retained | PROVED/RESTRICTED syntactic theorem + COMPUTATIONAL independent checked certificate. P versus NP remains OPEN.**

## IDEA: one candidate theorem and four falsifiers fixed before research

**Candidate 582.1.** In the original archived /386 SOURCE/paid conservative signed-AND2/zero-extra-charge-DEF-facet/strict oriented Resolution sibling calculus, one fresh paid owner can be shared across *m* distinct earlier signed clauses containing the same literal \(\ell\). Each clause can be compatibly weakened by the same new literal \(t\) with exactly two additional paid RES inferences. Total incremental logical work is \(1+2m\), not \(3m\) from paying a separate conservative owner for each clause. This is a constructive **upper bound on the macro's incremental work**, not a minimality claim and not a full historical \(R_{\mathrm{mix341}}\) theorem.

Four falsifiers fixed for this test: **F1:** shared positive/negative DEF clauses are not genuine non-tautological facets of the exact checker-accepted signed owner; **F2:** one of the \(2m\) inferences violates strict signed pivot orientation, chronology or exact resolvent; **F3:** source authenticity, fresh owner identity, count-once payment or completeness changes; **F4:** the candidate packet fails independent exact checker-rule replay or a hostile undercharge/forgery is accepted. F1–F4 did not occur in the 12-case independent audit. **Original /386 OS-CLI replay remains unperformed** and is an additional open acceptance falsifier.

## SEARCH and authority

Before constructing the example I read both current complete root trackers (preflight Git blobs \`proof1.txt\` \`f46f6aae25571340a5fd17a5181d51c271509947\`; \`proof2.txt\` \`42943fe447c6061fb8009a526f46ac8a6684765c\`), issue #3 and most recent peer evidence, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, the five current role-owned handoffs and reports LSPV-1/581, LSPV-2/565, LSPV-3/578, LSPV-4/551, LSPV-5/496, and materially relevant older LSPV-1/539–549, /566, /569–570, /579–581; LSPV-2/341, /352, /386, /539–549, /560; LSPV-3/539–549, /577; LSPV-4/539–551; and LSPV-5/491–496. The new construction is an **amortized batch version** of the LSPV-1/580 single-clause weakening and /581 two-fresh-owner certificate, not an invented new inference rule. Relevant prior cost-sound stepwise /386 abstraction is LSPV-2/565. LSPV-5/496 independently requires one immutable common source and rejects joining the /341 and /386 sibling acceptance languages.

Historical sibling authority: \`experiments/arc/lspv2_386_independent_verify.js\`, **unchanged exact Git blob** \`338305c0ce101704205e57543756b8127074a986\`. It checks full signed cubic-Tseitin SOURCE sets, ordered paid gate declarations, truthful DEF facets and exact oriented binary RES. Its CLI additionally runs 11 destructive negative controls. Source seed: \`results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json\`, blob \`807aaf7b7cf5e4a4feb29c2599f9e582ea140e30\`, previously verified against original OS CLI. The new certificate preserves that exact in-band source and its 41 SOURCE records, but no *separately supplied, immutable external* source-binder replay is claimed here.

Primary literature inspected: S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44 (1979), 36–50, https://doi.org/10.2307/2273702 (proof-system and relative-simulation boundaries); P. Cousot and R. Cousot, *Abstract Interpretation*, POPL 1977, 238–252, https://doi.org/10.1145/512950.512973 (sound may transitions); and E. Clarke, O. Grumberg, S. Jha, Y. Lu and H. Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, 154–169, https://doi.org/10.1007/10722167_15 (legal cheap native paths cannot be deleted merely because they defeat a proposed bound). None authenticates the missing mixed checker.

## Theorem 582.1: shared-owner batch signed weakening

Fix a completed or extensible legal /386 proof prefix containing \(m\ge1\) distinct earlier canonical non-tautological signed clauses \(C_1,\ldots,C_m\). Suppose every \(C_i\) contains the **same** signed literal \(\ell\), none contains \(t\) or \(\neg t\), \(|t|\ne|\ell|\), and the accepted native signed-gate policy allows a new globally fresh auxiliary wire \(z\) with inputs \(\ell,\neg t\), neither referring to the prohibited source guard. Let one fresh paid owner declare

\[
 z\leftrightarrow(\ell\land\neg t).
\]

Its genuine non-tautological checker-generated facets are

\[
 D_+=(z\vee\neg\ell\vee t),
 \qquad D_-=(\neg z\vee\ell).
\]

The third facet, \( \neg z\vee\neg t\), need not be emitted. For each \(i\), orient two strict RES steps as

\[
 (C_i,D_+)\overset{\ell}{\longrightarrow}
 A_i=(C_i\setminus\{\ell\})\vee z\vee t,
\]

\[
 (A_i,D_-)\overset{z}{\longrightarrow}
 B_i=C_i\vee t.
\]

All \(A_i\) and \(B_i\) are canonical non-tautological signed clauses: the freshness of \(z\), \(t\notin C_i\cup\neg C_i\), and \(C_i\)'s cleanliness exclude complementary literals. The first pivot occurs with \(+\ell\) in \(C_i\) and \(-\ell\) in \(D_+\), interpreted as the *same signed literal* \(\ell\) regardless of its numerical sign. The second pivot is \(+z\) in \(A_i\) and \(-z\) in \(D_-\). Both parent records precede the child. Reusing \(D_+\) and \(D_-\) adds **zero** new owner charges. Only one globally distinct owner and \(2m\) distinct RES occurrences are newly charged.

Therefore

\[
 \boxed{\Delta W_{\mathrm{batch}}=1+2m}
\]

for this exhibited legal extension, compared with the exhibited *separate fresh-owner* implementation cost \(3m\), saving \(m-1\) charged nodes when \(m\ge2\). The result does not say \(1+2m\) is the least possible cost among **all** native derivations. A previously declared suitable paid owner could reduce the marginal charge to \(2m\), and other whole-proof shortcuts remain unrestricted.

**Shared-DAG obligation:** All \(m\) new derivations share the same two DEF records and paid owner identity. The correct work is counted by distinct charged node occurrences and owner declarations, **not** by summing the marginal price of four separately isolated proof trees. The theorem adds no branch, uncharged oracle, semantic weakening primitive or proof-system change. The source remains fixed.

## Exact 4-clause original-source witness

Start with the pinned accepted /579 source, which has 10 vertices, 15 original edge variables, source guard 16, 41 mandatory SOURCE records, 60 paid RES, one paid owner, \(W=61\) and 101 records. Select four unmodified, distinctly indexed original SOURCE clauses:

| SOURCE record | Original signed clause |
|---:|---|
| 0 | \([1,2,15,-16]\) |
| 3 | \([1,-2,-15,-16]\) |
| 13 | \([1,-4,6,-16]\) |
| 14 | \([1,4,-6,-16]\) |

Take \(\ell=+1\), \(t=-3\), and a fresh paid owner tuple \`[1,18,1,3]\`, meaning \(z_{18}=x_1\wedge x_3\). The exact original /386 facets reused by every derived pair are record 100, \`[-1,-3,18]\), and record 101, \`[1,-18]\). The newly paid RES records are 102–109; records 103,105,107,109 respectively yield:

\[
\begin{aligned}
B_0&=[1,2,-3,15,-16],\\
B_3&=[1,-2,-3,-15,-16],\\
B_{13}&=[1,-3,-4,6,-16],\\
B_{14}&=[1,-3,4,-6,-16].
\end{aligned}
\]

The final original empty-clause RES record is preserved with the **same parent identities**, shifted from original last array index 100 to new index 110. All source clauses and their original 0–40 indices are byte-identical to the seed.

| Ledger | Pinned /579 | New /582 | Delta |
|---|---:|---:|---:|
| SOURCE records | 41 | 41 | 0 |
| Free authentic DEF facet records | 0 | 2 | +2 |
| Paid strict RES records | 60 | 68 | +8 |
| Globally paid distinct AND2 owners | 1 | 2 | +1 |
| **Logical work W** | **61** | **70** | **+9** |
| Total certificate records | 101 | 111 | +10 |
| New certificate UTF-8 bytes | 6,523 | **7,160** | +637 |

The four independent-owner version of *this same batch macro* would add four paid owners and eight RES for **+12**, versus this shared-owner **+9**. This is 25% cheaper *for the added macro only*, **not** a 25% saving in an optimal refutation.

All ten newly inserted records are **outside the final contradiction's terminal-ancestor cone**. Consequently the prior \(W=61\) original-checker-accepted refutation remains the best published upper bound for this fixed source. This example authenticates local availability/sharing and a potential falsifier of an overly additive abstraction, **not** a shorter terminal proof or a bound on minimal full mixed-calculus work.

## Computational verification and exact limitations

Published exact new packet \`results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_PACKET.json\` (Git blob \`d3afbee95a49e528134dc036da482a6399297d6d\`, exactly 7,160 bytes). A **separately written mathematical-rule replayer**, not the original verifier, checked the full source-generated signed set, every original and new RES record and chronological parent, the two paid owner definitions, two exact free facets, freshness, summary, terminal empty clause and full 15-variable original source semantics. It also exhaustively tested all \(2^{15}=32,768\) original-edge assignments and found **zero** satisfying the odd-charge source.

The independent differential completed **12 of 12** predicted outcomes with **8,274 replayer assertions**: two accepted packets (\(W=61\) and \(W=70\)), and ten appropriately rejected hostiles (undercharge, wrong facet, pivot polarity, paid-wire collision, changed resolvent, future parent, forged SOURCE, wrong facet owner, removed facet and corrupted guard). A separate direct four-pair signed-resolution check was executed in an OS Python process. These are **independent reproductions of the archived mathematical rule specification**, not observed original-checker acceptances.

A complete published Node.js original-checker OS subprocess reproducer pins the three exact Git blobs and independently reruns seed, witness, ten hostiles and SOURCE satisfiability:
\`experiments/arc/lspv1_582_shared_batch_weakening.cjs\`, blob \`d6ada4aa454aa26965f6fc255ea4b4ff6dc280cc\`.

**Verification blocker:** The standalone Node runner was created and Git-readback verified but **not executed** as an operating-system subprocess in this run. The 11 built-in original /386 CLI negative controls were therefore **not observed** for the new exact packet here. Original-checker acceptance should be classified **PENDING NATIVE REPLAY**, rather than claiming verified ACCEPT. LSPV-5 should execute this exact script against the pinned original checker and independently attack sharing, payment and parent orientation. Its answer must be reported without treating the replayer as the original authority.

Independent raw test ledger: \`results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_INDEPENDENT_RAW.json\`, blob \`a575fafc988364de3db7dea6fdb3e6161c2b7791\`. All three new files passed exact Git readback. Other physical metrics (discovery cost, actual execution time, verifier span, peak working bits, reference indexing and reserialization) are **not** identified with the logical charge \(W=70\).

## Implications for required proof chain

**P2-D1 OPEN.** This certificate stays in the authentic sibling /386 calculus. It does not authenticate a single native full \(R_{\mathrm{mix341}}\) grammar with SOURCE, Resolution, AND3, GF(2), LOCAL-CONVERT, owners/facets, freshness, private/exported wires, weakening, branches, contexts, discharge, join, deletion and all other truly accepted operations. Unknown historical behavior must be conservatively overapproximated rather than prohibited. The distinct /341 checker is not composed into /386.

**P2-C3 OPEN.** A cost-sound *full-rule* abstraction still requires a concrete configuration carrying the immutable original source, whole shared DAG, paid owner identity, active/discharged contexts, complete definitions, provenance and exact weights. Every legal native step must be included and have abstract cost no more than concrete cost; accepted goals must be preserved. The current /582 witness requires one owner payment shared by multiple legal RES conclusions; a lower-bound heuristic that charges each clause's weakening owner separately can incorrectly rule out this real cheap path. CEGAR may only prune a cheaper counterexample after an original-checker replay proves it spurious. Do not use a free abstract OR inference or drop paid owner distinctions.

**P2-B1 OPEN.** The optimum must minimize over **all** source-bound fully legal shared proof DAGs, including alternative proofs, GF(2), extensions, compact circuits, learned derivations, branch reconvergence and legally shared local owners. Neither the signed macro nor the independent replay establishes any superpolynomial all-rule minimum or SAT machine lower bound. The original hard ordinary-Resolution odd-Tseitin sources have known efficient GF(2) and paid-ER shortcuts, including LSPV-2/386.

**P2-B2/B3 OPEN separately.** The existence of an accepting checker, a short sibling proof, correct abstraction or a polynomial SAT algorithm in a hypothetical universe does not provide a polynomial bound for \(\overline W_{R_{\mathrm{mix341}}}\) absent an explicit uniform same-fixed-calculus transfer theorem.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither complete root proof chain's load-bearing theorem status, quantifier or strongest fixed-source upper bound changes; no root tracker write is justified. Root \`main.tex\` ownership was respected and left unchanged. No automations, titles, identities, schedules, roles, historical weights or the original TWO Route A / THREE Route B distribution were altered. All unavailable sources and replay gaps are disclosed. **P versus NP remains OPEN.**

## Reproducibility and five-role handoff

- Exact packet: \`results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_PACKET.json\`.
- Reproducer: \`experiments/arc/lspv1_582_shared_batch_weakening.cjs\`.
- Independent raw matrix: \`results/raw/arc/2026-11-11_1503_LSPV1_582_SHARED_OWNER_BATCH_WEAKENING_INDEPENDENT_RAW.json\`.
- Shared handoff: \`research/coordination/2026-11-11_1503_LSPV1_SHARED_OWNER_WEAKENING582_FIVE_ROLE_HANDOFF.md\`.
- Actual next gate: independently execute the original Node CLI on the exact packet and attempt a genuinely mixed-rule single-checker source-bound transition for P2-D1; if either fails, preserve the counterexample and qualify the theorem.

### Primary references

1. Cook, S. A., and Reckhow, R. A. (1979). The relative efficiency of propositional proof systems. *Journal of Symbolic Logic* 44:36–50. https://doi.org/10.2307/2273702.
2. Cousot, P., and Cousot, R. (1977). Abstract interpretation: a unified lattice model for the static analysis of programs. *POPL*, 238–252. https://doi.org/10.1145/512950.512973.
3. Clarke, E., Grumberg, O., Jha, S., Lu, Y., and Veith, H. (2000). Counterexample-Guided Abstraction Refinement. *CAV*, 154–169. https://doi.org/10.1007/10722167_15.

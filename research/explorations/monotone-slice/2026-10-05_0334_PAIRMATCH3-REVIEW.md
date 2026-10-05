# 2026-10-04 20:34 PT PAIRMATCH3 review

External review of PAIRMATCH3, read against the concurrent ORDER3EXACT1 exact census. Full note: `research/explorations/monotone-slice/2026-10-05_0334_PAIRMATCH3-REVIEW.tex`.

**Status unchanged: OPEN.** Not a monotone-circuit lower bound. Not P!=NP.

The pair-matched null is accepted as computational: after matching, pair balanced accuracy sits near chance, and neither the sampled triple-orbit scan nor the exact q=20 census (held-out BA 0.45 on 10 evaluation pairs, 81 orbits, all binom(70,3) triples) replicates. The caliper q=28 value 0.70 on 29 positives is noise-compatible. Deletion minima (m_min=26 at q=20) are not MUS certificates.

Literature alignment: alpha=3.5 is inside the Scott-Sorkin open interval between the pure-literal threshold (about 1.636) and satisfiability. Below pure literal, rare UNSAT is a unique minimum-excess MUF; above satisfiability, Chvatal-Szemeredi says the obstruction is linear. A bulk order-three orbit census is the wrong aggregator for a sparse core. Xu-Hoos-Leyton-Brown (about 70%) and Cameron-Chen-Hartford-Leyton-Brown (about 79-84%) separate SAT from UNSAT at the phase transition, and the two-feature tree is LPSLACK variation plus polarity, not a triple orbit. Zhou long-range frustration onsets near alpha_R(3) about 4.19. Bresler-Huang multi-OGP is a large-k search barrier. Robust sunflowers attack large uniform set systems, the opposite of a minimum-excess core.

## Revised queue

1. **MATCHED-MUF2 first.** Exact or branch-and-bound MUS on the pairs already in hand, at q=16,18,20. Record excess e=2m-n_core, uniqueness, and whether the core is absent from the matched SAT twin.
2. **Free-resource check.** On the same matched pairs, LPSLACK coefficient of variation and the GE/XOR defect. If slack separates, the residual is inside resources already granted.
3. **ORDER3EXACT2 only inside the core or failed-literal closure**, plus one confirmatory bulk pass at q=20. Do not lead with q=32 bulk enumeration.
4. **PAIR-MATCH2** only after that, and only to kill or confirm the q=28 caliper spike. On the order of a hundred caliper-retained positives.
5. **Hold SAT-SUNFLOWER2** until the core-order distribution is in hand.

The resource that still has to scale, once exact 2-SAT, exact GE, and depth-1 triple attention are free, is either search for a small excess core or a delocalized incompatibility on the matched pair. The present tables do not separate those two.

TASK-008 was not rewritten in place. Paste this section there if the task log should carry the queue change.

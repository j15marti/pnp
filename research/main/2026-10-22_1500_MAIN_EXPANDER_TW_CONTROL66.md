# EXPANDER-TW-CONTROL66

Timestamp: 2026-10-22 15:00 KST (hourly check run)

**Global status: P versus NP OPEN.** No load-bearing arrow closed.

## Baseline reviewed
HEAD bfc8d9f6; EQUALITY-LOCALIZATION-MINOR-BARRIER65 (Lemmas 65A/65B, Cor. 65C), its handoff next-test ":48 — require wall/expander controls for every separator compiler", Grok 4.7 review 14:11, root `main.tex`.

## Experiment (COMPUTATIONAL)
Script `research/code/2026-10-22_1500_expander_tw_control66.py` (runtime ~4 s, single stage), result `research/code/2026-10-22_1500_expander_tw_control66.json`.
Random 3-CNF at clause ratio 4.26, incidence graph, networkx min-fill-in treewidth UPPER bound, one seed per n:

| n | incidence edges N | tw upper bound | tw_ub / n | 2c·log2 N (c=0.1) |
|---|---|---|---|---|
| 20 | 255 | 14 | 0.700 | 1.6 |
| 40 | 510 | 27 | 0.675 | 1.8 |
| 80 | 1020 | 55 | 0.688 | 2.0 |
| 160 | 2043 | 109 | 0.681 | 2.2 |
| 320 | 4089 | 215 | 0.672 | 2.4 |

Reading: the heuristic bound is an *upper* bound, so by itself it certifies nothing about the true treewidth. It is consistent with the known linear treewidth of random-CNF incidence graphs (expansion arguments, e.g. Alekhnovich–Razborov-style; KNOWN THEOREM, not re-verified here), which with Lemma 65A/65B means: any exact occurrence-localized encoding of such formulas has treewidth Omega(n) >> 2c·log N, so they also lie outside the SMALL-INTERFACE64 recursive class. This gives a second control family besides walls (random/expander rather than planar-like grids). Classification: EXACT OBJECT TRANSFER of the 65C argument; no new theorem.

## Limits
Single seed; heuristic upper bound only; the constants c=0.1 and the class definition are taken from SMALL-INTERFACE64 without re-audit. Nothing here touches the OPEN item (nonlocal semantic compiler under P=NP that does not preserve the incidence minor).

## Suggested next step
Test whether a *semantic* (solver-assisted) child construction could reduce incidence treewidth of random 3-CNF without being a minor-preserving rewrite; the only obstruction known so far is that exact reductions must still preserve satisfiability and any such compiler would itself decide SAT on those inputs, i.e. this is circular unless a uniform resource bound is shown (OPEN).

% END_OF_VERIFIED_REPORT::EXPANDER-TW-CONTROL66

# LSPV-4/561 | Fixed native-/386 proof DAG: recomputation does not lower four-register minimum

**2026-11-12 05:36 PST | PNP Time-Space Resource Auditor | historical Route A retained | PROVED/EXACT finite state graph; independent computational replication | P versus NP OPEN**

## New result

Revisit the accepted **W38 original signed odd-K4** proof from LSPV-4/560, with 17 SOURCE, six free DEF facets, three distinct globally paid gate owners and 35 paid RES. Preserve all parent edges, record identities, original SOURCE and terminal contradiction. Treat each paid output as one abstract clause-array register; original SOURCE/DEF are read-only. Unlike /560, allow **arbitrarily many paid RES recomputations**, any free deletion/reconfiguration and even arbitrary-size in-place overwrite of a resident paid parent. Enumerate *every* possible resident-output subset under capacity three.

**Exact four-register pebbling minimum survives unrestricted recomputation in this fixed graph:**

| Model | Slots | Reachable states | Legal transitions | Terminal empty output |
|---|---:|---:|---:|---|
| Arbitrary expansion, recomputation | 2 | 473 | 10,778 | NO |
| Nonexpanding, recomputation | 3 | 5,355 | 284,491 | NO |
| Arbitrary expansion, recomputation | 3 | 5,912 | 320,309 | NO |
| Nonexpanding, recomputation | 4 | 46,414 | 5,290,378 | YES, exactly 35 RES executions |

Two independent algorithms, a hosted V8 BFS and a separately written actual Python OS BFS, returned identical state counts. For the positive 4-register witness, all 35 existing signed RES records are executed once, so the declared archival logical charge remains **W=35+3=38**. No claim about physical RAM: the old Node checker stores the full 3,639-byte JSON source and parsed records separately from the hypothetical output registers.

## Falsification / CEGAR

Deliberately erase one required dependency of paid node 33, which has paid parents 31 and 32. Erasing 33<-31 creates a fictitious 3-register, 21-RES trace; erasing 33<-32 creates a fictitious 3-register, 17-RES trace. Neither is a legal proof under the authenticated strict RES rule. Therefore any cost abstraction that drops parent availability may propose spurious cheap paths, but only \emph{proved-spurious} paths should be refined; all legitimate mixed-rule shortcuts remain available.

The result is \emph{stronger than /558-/560 within the same fixed graph} because their exact register calculations excluded recomputation. It is **not** an all-proof, all-algorithm, or mixed R_mix341 lower bound. The source itself has a previously demonstrated legal W29 alternative, and the full historical checker/parser remains missing.

## Published and readback verified

- [LSPV-4/561 mathematical report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-11-12_0536_LSPV4_NATIVE386_RECOMPUTE_PEBBLING561.tex), Git blob **e4321a3109a56dd0c871ab5c949041c32d4d77c2**
- [Reproducible independently written Python BFS](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_561_recompute_pebble.py), Git blob **566df1a81a83df4fc900a4325bfa96dc106ba7f1**
- [Raw exhaustive counts and traces](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0536_LSPV4_561_RECOMPUTE_PEBBLING_RAW.json), Git blob **d4e4a46296ea3af541e8e6dd1f638153015ac245**
- [Original unchanged /560 accepted W38 certificate](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json), Git blob **6b72c961c2db19be87a0936361c467ef3445f4e2**

**Checker boundary:** Reused the *unchanged* previously checker-body-accepted original packet; no new operating-system native-checker claim. The Python tool may be run with the original packet path to validate every hard-coded paid parent and canonical clause-byte length before the state search. The independent Python OS execution for this run used its pinned in-code fixture and completed all six exhaustions. The hosted V8 independent search had previously recomputed the arrays directly from the original GitHub packet.

## Publication/governance and role handoff

Root **proof1.txt** and **proof2.txt** reviewed: **TRACKERS REVIEWED; NO MATERIAL CHANGE** because [P2-D1], [P2-C3], [P2-B1], separate [P2-B2/B3], and [P1-01/03/04] stay OPEN. The root **main.tex** fetch interface yielded empty content despite a nonempty blob and its raw route rejected the large file; it was deliberately not overwritten without a complete, conflict-safe ownership-region merge. This is the publication blocker for main.tex; full root-main reconciliation awaits a viable full-content fetch.

**LSPV-1 (historical Route B):** Keep the distinction between this fixed-DAG register lower bound and all-proof minimum \(W_R\); check the W29 bypass and the checker-core versus wrapper distinction (/590).

**LSPV-2 (historical Route A):** Probe an actually original-checker-accepted alternative recomputation or source equivalence shortcut, retaining mandatory original signed SOURCE and paid global ownership.

**LSPV-3 (historical Route B):** Prioritize authentication of the complete native R_mix341 byte grammar and actual fixed weights, especially mixed RES/AND3/GF(2), DEF and context joins. No /386-only theorem transfers automatically.

**LSPV-4 (historical Route A):** Audit actual sequential verification, retrieval/recomputation and peak writable-bit space for a native source-sound mixed-rule proof with genuinely necessary shared paid lemmas.

**LSPV-5 (historical Route B):** Independently challenge the exhaustive state-model coverage and the two spurious edge-forgetting traces; check that no counted shared owner is duplicated across branches.

The **five original enabled hourly Pacific automations were inspected** and left unchanged: :00, :12, :24, :36, :48; historic TWO Route A / THREE Route B labels retained, no task created, renamed, disabled or rescheduled.

**P versus NP remains OPEN.**

# LSPV-4/472: FLMV INDEX-space source audit and two-model resource bifurcation

**2026-11-07 08:36 PST | LSPV-4 Route A | PROVED/RESTRICTED model disjunction; COMPUTATIONAL checks | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** Recent LSPV-2/471 and LSPV-4/470-471 proofs assume every sequential guest INDEX bit is uncharged by original FLMV space, because the original machine-model paragraph specifically says non-index WORK tapes contribute their largest visited address. Test this inference against the *entire* original paragraph, especially the configuration-size statement. Exact affected node: [P2-A4]. Related OPEN dependencies: [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04].

**Falsifiers stated before search:** (F1) FLMV expressly exempts INDEX alongside INPUT/OUTPUT; (F2) the paper excludes INDEX contents and heads from configurations; (F3) arbitrary n-bit input cannot be copied to an INDEX tape without visiting non-index WORK above address zero; (F4) a prior report supplies a fully charged model-preserving conversion of the completely free-INDEX variant to the exact FLMV model. The reading did not support F1, F2 or F4. An explicit program and finite check refuted F3.

## Source and peer review

Primary: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, author PDF https://lance.fortnow.com/papers/files/tst.pdf, §2.1 printed p.4, read as text and PDF screenshot. **INPUT and OUTPUT** are expressly excluded from space. Non-index tapes contribute their largest accessed location. A configuration is explicitly defined to include INDEX tape contents and INDEX head locations. The next statement says each configuration of a computation using space s has size O(s). There is **no explicit sentence that all INDEX tapes are uncharged**. Exact per-INDEX contribution is not completely specified in that paragraph, so this report does not assert a definitive interpretation without additional original-source authority.

Corroborating author survey: D. van Melkebeek, *A Survey of Lower Bounds for Satisfiability and Related Problems*, Foundations and Trends in TCS 2(3), 2007, https://pages.cs.wisc.edu/~dieter/Papers/sat-lb-survey-fttcs.pdf, §2.1 printed pp.214-215, text and screenshot reviewed. It calls INDEX a sequential-access tape and repeats the configuration inclusion and O(s) sentence. The repetition is not proof of a specific missing convention.

Read BOTH complete root trackers, issue #3, governing five-role Nov. 2 handoff, AGENTS.md, CODEX.md, pnp research skill, role reports LSPV-2/471 (research/agents/lspv-2/2026-11-07_0819_LSPV2_DENSE_INDEX_SPACE_TRANSFER_FIREWALL471.md, SHA acde2a98), LSPV-4/471 (research/agents/lspv-4/2026-11-07_0811_LSPV4_QUANTIFIED_INDEX_PAYLOAD_BARRIER471.md, SHA 7da90975), LSPV-4/469. Project Grok actual GROKPROOF/2026-11-07_1220_PROGRESS.md (SHA 2c450bb3), Claude actual research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (SHA 9a5b05d6). The historical governing handoff SHA is c3889a3e. Neither peer critique resolves INDEX accounting.

External repository review, exact refs: konard/p-vs-np/README.md blob 0e0ec77f and proofs/complexity/README.md blob 7ee9a11e, a finite one-tape model; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea and INDEPENDENT_AUDIT.md blob b30515cc, restricted interface/acquisition caveats; meelgroup/frat-xor/format.md blob 986a21aa, external certificate grammar; MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd19, signed parity source; openai/math/README.md blob cc5b0a03, mixed proof formalization statuses. Used public web search and connected GitHub; a separately identifiable Google-branded engine and official native FLMV checker were not available.

## Theorem 472.1 (PROVED/RESTRICTED): two distinct INDEX accounting models

Let W be largest non-index non-input WORK address visited, H largest sequential INDEX tape position visited, and consider *distinct conventions*:

$$
S_{\mathrm{work}}=\max(1,W),\qquad S_{\mathrm{full}}=\max(1,W,H).
$$

A single fixed deterministic machine M copies the n bits of its input x sequentially onto the associated INDEX tape and halts without accessing any non-index WORK position above zero. Thus T_M(x)=O(n), S_work(M,x)=O(1) and H(M,x)>=n. Its terminal INDEX word equals x. Across the 2^n possible inputs, the terminal INDEX contents are pairwise distinct. Therefore a source-independent *explicit injective* description of every such configuration needs at least n bits for some word, by counting.

Under the model that declares INDEX completely FREE, the blanket assertion that every explicit configuration has size O(s) is **false when s is S_work alone**. A representation that rereads original x lazily or reconstructs INDEX state at further cost is a separate simulation with its own resource ledger, not an immediate O(s) literal configuration.

Under the distinct model charging sequential INDEX high-water, S_full>=H; the configuration-size claim is consistent, but a wrapper that writes B^k guest INDEX cells is not a guest-space-O(B^s) wrapper for k>s, because S_full>=B^k. Therefore one must EITHER authenticate the exact INDEX contribution and recompute the guest-space exponents, OR prove a separately charged transfer from a genuinely FREE-INDEX model into the theorem's machine. The original paragraph cannot simultaneously serve as an unqualified source for arbitrary free INDEX payloads and O(s) explicit configurations. This is an **interpretation/transfer firewall**, NOT a refutation of FLMV's published theorem.

## Revision of prior project claims

LSPV-2/471 Fenwick direct-WORK INDEX port and LSPV-4/470-471 counted-WORK canonical-radix ports have genuine restricted space blowups under the stipulated FREE-INDEX guest model. The claim that such a guest *necessarily has low space in the exact original FLMV model* was not authenticated by the supplied wording and needs a formal INDEX convention. If INDEX high-water counts, the quoted low-space prologues no longer meet their assumed guest exponent. LSPV-2/469 native INDEX-to-INDEX alternative and arbitrary source-aware SAT transformations are not excluded. Historical evidence is preserved and not silently retired.

## Full resource accounting for this finite countercontrol

| Resource | INDEX-copy witness | INDEX-padding variant |
| --- | --- | --- |
| Indexed source reads | n input bits, one per step | source-independent prologue |
| Guest time | Theta(n) | Theta(B^k) index writes |
| Non-index WORK high-water | O(1) | O(log B) counter |
| INDEX payload and head | Omega(n) | Omega(B^k) |
| Lossless explicit configuration width | >=n for some n-bit input | literal INDEX length B^k |
| Actual input/output restoration | witness halts; wrapper must pay | index erasure and head restore must be charged |
| Construction, failed policies, cache, verification, guest simulation, child buffers | none in witness | still open for universal Route A |
| Charged INDEX interpretation | S_full>=n | S_full>=B^k |
| Free INDEX interpretation | S_work=O(1), but config is large | S_work may be small, native FLMV transfer unresolved |

**Established hard family control:** on suitable cubic expanders of h vertices, odd-charge signed Tseitin strict proper 3-CNF has 4h clauses, 3h/2 edge variables and length Theta(h log h); ordinary shared DAG Resolution has published exponential lower bounds (Urquhart 1987; Ben-Sasson/Wigderson 2001), while GF(2) parity summation provides a short algebraic shortcut. This does not certify full R_mix341 hardness, all-algorithm hardness or B3. Finite signed K4 even/odd controls have 8/0 satisfying assignments; no asymptotic hardness is claimed.

## Independent executed checks

Published code at experiments/arc/lspv4_472_index_model_independent.cjs. Independently executed Python reference source in the reproducibility archive. For n=1 through 8 all 510 binary inputs were copied to INDEX; 18 n^k padding configurations for n=2,3,4,5,8,12 and k=1,2,3; signed K4 parity controls and malformed literal regression. Python: 4,671 assertions. Independent Node: 4,671 assertions. Aggregated records matched. Raw: results/raw/arc/2026-11-07_0836_LSPV4_472_INDEX_MODEL_RAW.json. These are finite host-language semantic controls, not native indexed-TM instruction measurements.

## Status and next precise gap

**Actual advance:** a source-authenticated correction to the assumption that FLMV §2.1 expressly declares INDEX storage free, plus a proved two-model configuration-size disjunction. **Remaining gap:** identify the exact original machine space metric, including INDEX tape contents/head high-water, then redo LSPV-2/469-471 and LSPV-4/470-471 on that single metric and charge all phases. Universal all-input, malformed-aware, recursively iterable same-machine contraction [P2-A2]/[P2-A5] and P1-01/P1-03/P1-04 OPEN. Route B [P2-D1], [P2-B1], [P2-B2] also OPEN. The conditional target t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) and gap 1/90 at (6/5,1/2) remain conditional. No change to historical R_mix341 grammar/weights or any of the five agents' identities, roles, schedules or enabled states. **P versus NP OPEN.**

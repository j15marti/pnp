# Five-role handoff: co-nondeterministic FLMV boundary, strict-3CNF witness access

**November 9, 2026, 19:00 PST | LSPV-1 result 551 | P versus NP OPEN**

**Scientific result:** FLMV 2005 Theorem 6.4 applies to coNTISP, not ordinary existential NP recognition. For the separate co-nondeterministic recurrence $g_0=1$, $g_{k+1}=c^2 g_k/(1+c g_k)$, the space-exponent bound $d_k^{co}(c)=\min\{(1/g_k-c)/k,c^{-2k}\}$ is positive for some integer $k$ exactly when $1<c<\sqrt2$, and its optimized positive endpoint obeys

$$
d_*^{co}(c)\sim 4\log2\,\frac{\sqrt2-c}{\log(1/(\sqrt2-c))}.
$$

A signed proper 3-CNF family encoding equality between two blocks of witness variables has read-only random-access assignment verification using $O(\log N)$ writable work bits, yet requires $\Omega(N/\log N)$ bits in the explicitly restricted deterministic one-pass ordered-witness model. This isolates a representation/access-model distinction, not an unrestricted machine-space lower bound. Exact-rational and finite truth-table controls passed. The full report includes proofs, source URLs and limits.

**LSPV-1 (Route B):** Maintain separate proof-chain ledgers for the hypothetical *deterministic*, total, all-input $A_P$ and the *existential nondeterministic* SAT recognizer $A_{NP}$. CoNTISP recognition requires independent semantics and cannot be created by flipping branches. Do not confuse a separately supplied assignment with the internal machine work tape. Quantify strict slack when polylog factors occur; B3 remains separate OPEN.

**LSPV-2 (Route A):** Try to defeat the strict-3CNF streaming separation by identifying a genuinely legal one-pass, no-rewind deterministic strategy using fewer than $h-O(1)$ bits. Any use of random-access, certificate rereads, machine-model changes, source reshaping, or offloaded witness state must be explicit and charged. Retain the Section 2.1 sparse-normalization guard.

**LSPV-3 (Route B):** Independently authenticate Theorems 1.2, 6.2 and 6.4 of the actual FLMV PDF: coNTISP versus NTISP versus DTISP; formalize the extra read-only assignment tape, witness length and source grammar as a typed transition interface. Verify that the four source clauses for each variable pair are all required and that a missing facet is a hostile control. Preserve historical R_mix341 grammar ownership and do not treat the example as a native rule.

**LSPV-4 (Route A):** Preserve existing disabled automation state; no rescheduling. When reviewed, compare native ever-indexed work-tape high-water, input/certificate exclusions, $N$ binary length, and time/space exponent regions for deterministic and co-nondeterministic machines. Thresholds $N^d$ are exponent-only scales, not actual memory.

**LSPV-5 (Route B):** Red-team the recurrence closed form, threshold $c<\sqrt2$, globally optimized $k$, and the asymptotic coefficient $4\log2$. Attempt falsification under alternative witness-access policies; independently challenge the use of a streaming lower bound for full SAT or the use of existential $A_{NP}$ as coNTISP.

**Repository evidence:** report research/agents/lspv-1/2026-11-09_1900_LSPV1_CONONDET_FLMV_WITNESS_FIREWALL551.md; code experiments/arc/lspv1_551_conondet_exact.py; raw results/raw/arc/2026-11-09_1900_LSPV1_551_CONONDET_WITNESS_RAW.json. Tracker node [P2-L1-551] added to root proof2.txt; proof1.txt unchanged. All [P1-01],[P1-03],[P1-04],[P2-A1],[P2-A2],[P2-A3],[P2-D1],[P2-C3],[P2-B1],[P2-B2] remain OPEN; original two Route A/three Route B allocation, five task identities/titles/schedules/enabled states and historical $R_{\mathrm{mix341}}$ inference costs are unchanged. Root main.tex was not overwritten because safe retrieval returned zero content.

Primary sources: https://lance.fortnow.com/papers/files/tst.pdf , https://doi.org/10.1145/1101821.1101822 , https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html and https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/ .

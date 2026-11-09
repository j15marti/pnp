# LSPV-4/510R | Corrigendum: malformed-safe unary header repairs the all-phase WORK bound

**2026-11-08 PST | Route A, resource auditor | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Corrects the scope of [P2-L4-510] and its preceding report.** The initial gamma-header version did not establish $O(\log L)$ WORK space for malformed inputs of length $L$: an $L$-bit malformed source can gamma-encode a putative $H$ exponentially larger than $L$, making an unchecked binary header counter require $\Theta(L)$ WORK bits, notwithstanding the immediate later trailer rejection. This is a substantive all-phase resource gap, not an acceptable hidden promise. The first gamma-based finite examples and accepted-source theorem remain valid **in their stated accepted-source scope only**.

## IDEA -> SEARCH -> ITERATE; four falsifiers

**Repair hypothesis:** Replace the potentially enormous gamma-coded graph size with a unary prefix, retain the explicit terminal marker, and derive other parameters from the counted $H$. Falsifiers: F1 malformed no-terminator header or enormous declared size forces more than logarithmic WORK; F2 a truncation or suffix extension passes despite the footer check; F3 a tail-sign flip changes a guest-visible read or classification; F4 the completed guest trace is retained or semantic SAT answer assumed without payment.

**Exact new binary grammar, distinct from any historical R_mix341 parser:** 8-bit magic `10100101`, then `1^H 0` for even $H\ge4$; then $4H+k$ ordered original strict-three-clause records containing three $w$-bit IDs and three sign bits each, with

$$
m=3H/2,\qquad
k=\max\left(2,\left\lceil \frac25\left\lceil \log_2 H\right\rceil\right\rceil\right),\qquad
w=\left\lceil\log_2(m+3k+1)\right\rceil.
$$

Finish the packet with two bits `01` and require the immediately following INPUT cell blank. The $4H$ prefix clauses are exactly the one-odd-charge cubic-Tseitin parity encoding, with each edge-ID appearing in two distinct vertices. The last $k$ clauses have pairwise-disjoint fresh triples of IDs. Every tail sign pattern is syntactically valid, even when individual literals change polarity. The source length is

$$
M=8+(H+1)+3(4H+k)(w+1)+2=\Theta(H\log H).
$$

This grammar remains unbounded. The standard Ben-Sasson/Wigderson Corollary 4.5 ordinary **shared-DAG Resolution** exponential lower bound holds for the underlying expanding cubic-graph sequence. Padding by independently satisfiable, fresh-variable clauses preserves that ordinary-Resolution minimum **exactly** under a fresh-variable satisfying restriction, not merely equisatisfiability. Neither fact transfers to arbitrary algorithms or historical mixed R_mix341.

## Fully charged malformed-aware guard lemma (PROVED/RESTRICTED)

**Claim.** There is a uniform indexed random-access-Turing-machine source guard recognizing this special binary family with correctness on *every binary input*, including malformed or truncated encodings, which (a) never reads any of the $u=3k$ tail-sign coordinates on accepted inputs, (b) uses $O(\log(L+2))$ supplemental non-input WORK and INDEX high-water for **all** inputs of length $L$, and (c) takes $O(L^2\operatorname{polylog}(L+2))$ time for **all** inputs. A tighter $O(M^2)$ time bound holds on valid sources of length $M$ under standard arithmetic-tape operations.

**Proof and explicit physical costs.** Read magic; count unary 1s into a binary counter, one bit at a time. On any finite $L$-bit input the counter never exceeds $L$, even if the final 0 is missing: reading the next blank terminates and rejects. Hence all retained parameters $H,m,k,w$ and the expected final byte position have $O(\log(L+2))$-bit representations. Compute the marker offset, write its index on the INDEX tape, read the two literal `01` marker cells and the following blank, paying INDEX erasure every indexed jump. If any check fails, reject. Only after this bound is authenticated, perform repeated *recomputed* scans: each of the $4H$ original clauses matches one of four allowed local parity patterns, every original edge ID appears at two different vertex blocks, and each tail ID is a predetermined fresh variable. To verify incidence, for every edge ID rescan every vertex's first clause instead of storing an $H$-entry graph; keep only $O(1)$ clauses, counters and current indexed bit-address. Since all counters and INDEX data fit $O(\log L)$ bits and input tape cells are not charged as WORK high-water by the 2005 FLMV Section 2.1 machine semantics, peak supplemental WORK is logarithmic. On accepted inputs $H=O(L)$; the nested rescans and $O(\log L)$ charged index generation per bit access take $O(L^2\operatorname{polylog} L)$ time. No length oracle, full-source buffer, bitmap, or retaining an entire $O(L^2)$ dynamic trace is invoked.

For any fixed total correct general SAT/UNSAT/malformed decider $B$, the program $G_B$ that returns UNSAT after guard acceptance and otherwise clears temporary registers and calls $B$ correctly handles **all** binary inputs. Its full worst-case time includes the guard and $T_B(L)$ and its all-phase peak space includes $S_B(L)$; no claimed speedup of B. A fallback B running in polynomial time is a *conditional* premise of the Route A contradiction, not supplied here. We have proved a small-space specialized guard, **not** the requested arbitrary-solver contraction.

Every accepted source has exactly one odd-charge vertex, so the original XOR constraints force $0=1$. The k padded clauses cannot affect UNSAT. All $q=2^{3k}=\Theta(H^{6/5})$ same-parent virtual tail-sign variants share **one actual deterministic completed guest trace** and its UNSAT output; variation is confined to genuinely unread sign positions. Runtime can cache the verified accepted-family flag and apply a **source-authenticated structural invariance proof**, rather than keeping an uncharged copy of the entire anchor trace. For formal $N=M^2$ (no actual all-input parent reduction), one checked source plus streamed $q$ descriptors uses $N^{1+o(1)}$ time and logarithmic WORK, whereas explicitly serializing every $M$-bit child costs $qM=N^{11/10-o(1)}$ bit writes. This is a restricted upper-bound control, not a general 3-SAT decomposition.

**All-phase charges:** unary parsing at most $L+1$ INPUT bits, $O(\log L)$-bit counter; expected-end computation, position arithmetic, INDEX writing/erasure and bound checks all paid; repeated source reads $O(L^2)$ and per-read index complexity polylog; guest B on every rejected source with its full time/workspace; output of all child labels $q$ steps, or all child bit encodings $qM$ steps; streamed descriptor iterator $O(qk\log M)$ time and $O(\log M)$ WORK; no simultaneous q-child buffers; no retained full anchor trace; invalid descriptors and cache misses must be paid outside the accepted special family. No original-source-authenticated native R_mix341 proof was produced.

## Reproduction and limitations

Two independently authored **finite hosted-language** scripts, Python and Node, generate identical packet SHA-256 values on K4, K3,3, Q3 and Heawood. For each graph, $k=2$, 6 unread sign bits and 64 distinct children. **256** accepted virtual children per implementation, all with identical actual read-position sets/observations, plus seven negative controls per source for malformed header, wrong/truncated/extended trailer, core mutation, wrong tail ID and an even-charge SAT control. Source sizes are **285, 407, 631, 1069** bits; distinct read positions including one EOF blank probe are **280, 402, 626, 1064**; modeled read operations are **569, 1051, 2067, 5475**. Python also exhaustively checked SAT/UNSAT for original K4 and K3,3 sources. Heawood is a finite control, not an infinite certified expander family. Node uses finite Number values, so only the mathematical counter proof, not the hosted test, establishes the unbounded all-input bound. No native FLMV transition-by-transition replay, historical R_mix341 checker, actual recursive SAT transformation or full source-to-computation transfer was executed.

Published corrected verifier: `experiments/arc/lspv4_510_unary_safe_node.mjs`. Corrected raw: `results/raw/arc/2026-11-08_2036_LSPV4_510_UNARY_SAFE_RAW.json`. The original gamma packet code/results remain untouched as explicitly limited historical controls. Independently written Python reproducer is available in the attached archive.

**Reconciliation:** This corrects [P2-L4-510] source grammar/resource-scope text and narrows a *malformed input* barrier for [P2-A4]. [P2-A2], the rest of [P2-A4], [P2-A5], [P2-D1], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04] remain OPEN. No schedule, identity, allocation, title, enabled state, historical R_mix341 grammar/weight or other role manuscript edit. P versus NP remains OPEN.

## Primary sources and actual corpus

Fortnow, Lipton, van Melkebeek, Viglas (JACM 2005), *Time-Space Lower Bounds for Satisfiability*, Section 2.1, https://lance.fortnow.com/papers/files/tst.pdf. Ben-Sasson and Wigderson (JACM 2001), *Short Proofs Are Narrow*, Theorem 4.4 and Corollary 4.5, https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf. Exact project, Grok, Claude, konard, blkph0x, cnfgen, FRAT-XOR, ABC, openai/math paths and SHAs are recorded in the original LSPV-4/510 report. Both root proof chains and issue #3 were read this run; this correction uses the same corpus and independent tests, not a new external survey.

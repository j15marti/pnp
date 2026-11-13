# LSPV-4/582: Exact expectation, variance, and lower-envelope abstraction for accepted /341 literal-order aliases

**13 November 2026, 02:41 PST | PNP Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED symbolic theorem + COMPUTATIONAL pinned-corpus moments. P versus NP remains OPEN.**

## Candidate and four falsifiers fixed before this audit

**Candidate.** The canonical 7Ve short-circuit witness-probe total from LSPV-4/581A is not an invariant of every byte string accepted by the recovered /341 checker, as LSPV-5/523 independently falsified. Nevertheless, for **independent uniform permutations of each ternary SOURCE clause's three distinct signed literals**, the exact **expected** witness-probe count is 7Ve for every possible set of complete assignments. Within this fixed finite alias class, a per-clause minimum-cost quotient is cost-sound and its minimum is concretely realizable without changing the original proof DAG, logical charge, or JSON evidence length.

F1: One of the four forbidden parity patterns is missing, duplicated or of incompatible signs, invalidating the four-clause parity premise. F2: Permutations change source truth values, signed incidence, source-table aliases, deletion witnesses, accepted checker goals, or packet byte length. F3: An abstract 7Ve tariff incorrectly overcharges an accepted low-cost alias, as in the LSPV-5/523 accepted 29,238-probe packet. F4: Treating each witness's literal order as a fresh random draw understates the variance because the same SOURCE clause order persists across all 324 witnesses. Additional implementation falsifier: V8 sort comparator invocation counts need not be stable between execution engines.

## Authority, corpus, and novelty boundary

Authoritative source for the **restricted recovered /341 sibling only**: experiments/arc/lspv2_341_independent_verify.js, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**. Original seven-fixture packet: results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json, Git blob **fe27fe1011d0021e721ccaeb747ed58da65d7464**, 197,514 bytes. The checker recognizes SOURCE, AND3 and XOR; it does not authenticate the full historical Resolution/AND3/GF(2)/LOCAL-CONVERT/DEF/branch/discharge/join calculus or its original mixed-rule weights.

Compared both root proof trackers, issue #3 and latest comments, AGENTS.md, CODEX.md, project research SKILL.md, current LSPV-5/523 handoff and original checker, current LSPV-4/581A report, sampled relevant LSPV-4/539, /544 and /549 source records, and current LSPV-1/614 and LSPV-2/595 context. Root main.tex and proof2.txt were retrieved in full through immutable Git blob reads because contents text extraction returned empty on these very large files. No whole-repository Python preflight was executable without a local checkout. No autonomous redefinition of missing historical rules.

**Adopted:** /581A's exact canonical packet count and its common-order combinatorial theorem; /523's authentic OS-accepted order alias and witness-cost extrema. **Rejected:** promotion of the canonical 7Ve equality to an all-accepted-byte deterministic tariff. **New contribution:** a symbolic order-randomization identity, a fully correlated exact variance and cost-sound realizable quotient for the entire independent token-permutation subclass. Neither the six choices per clause nor the original accepted minima is claimed as newly discovered; those are /523 predecessors.

## Theorem 582.1: exact expected seven probes with no common-order requirement

For a ternary signed parity block with three distinct Boolean variables and four SOURCE clauses forbidden by one fixed charge, choose one of six token orders independently and uniformly for each of the four clauses. The OR short-circuit verifier inspects literals sequentially until the first true literal, or until all three have been examined. Conditional on a clause having t true literals on a complete assignment, the expected probe count is:

| t true literals | Expected probes over six orders |
|---:|---:|
| 0 | 3 |
| 1 | 2 |
| 2 | 4/3 |
| 3 | 1 |

For an assignment of the forbidden parity class, the four clauses have true-literal counts (0,2,2,2), giving expected total 3+3(4/3)=7. For the opposite parity class, the counts are (1,1,1,3), giving 3(2)+1=7. Therefore **for every complete assignment**, without distributional assumptions on witnesses, the four-clause block has expected cost exactly 7.

For any V such blocks and any fixed family of e complete deletion-witness assignments, retaining each chosen clause order across all witnesses,

$$
\boxed{\mathbb E_{\pi}[Q_{\rm witness}]=7Ve.}
$$

The expectation needs only uniform marginal literal order for each clause; independence is not required for this equality. Independence **is** used below for the exact variance and simultaneous extremal realizability. No assertion is made that every accepted alias has this cost. This is a theorem about the actual short-circuit loop for parity SOURCE blocks, not the optimal verification algorithm or SAT solving.

For a corpus of separate fixture formulas indexed by f, replace Ve by the sum of V_f e_f. Here it equals 5,896, yielding an exact expected **41,272 witness literal probes**.

## Theorem 582.2: exact variance and realizable cost-sound projection

For each of the 328 signed SOURCE clause occurrences c, let the *single fixed* token permutation \(\pi_c\) be uniform over six possible orders, independently across clauses, and let

$$
q_c(\pi_c)=\sum_{a\in\mathcal D_f}\operatorname{probes}(c,\pi_c,a)
$$

for that fixture's **actual** nonnull deletion-witness multiset \(\mathcal D_f\). The same \(\pi_c\) is used every time c is read, so repeated uses are *not* independent draws. Set \(S_c=\sum_{\pi}q_c(\pi)\) and \(T_c=\sum_{\pi}q_c(\pi)^2\). Then

$$
Q=\sum_c q_c(\pi_c),\qquad
\operatorname{Var}(Q)=\sum_c\frac{6T_c-S_c^2}{36}.
$$

This follows by linearity of expectation and independence between SOURCE occurrence choices, not between the repeated evaluations of one clause. The finite per-clause enumeration gives the exact rational value

$$
\boxed{\operatorname{Var}(Q)=\frac{17\,409\,088}{36}
       =483\,585.777\ldots,\quad \sigma=695.4033\ldots.}
$$

Define a partial cost abstraction over the chronological source-token choices, forgetting their exact order only after a clause's six alternatives have been evaluated. At SOURCE clause c, the abstract edge has weight \(m_c=\min_{\pi}q_c(\pi)\), while the source/proof identity and operational-goal bits are retained. Each concrete choice has \(m_c\le q_c(\pi)\); hence total abstract cost never exceeds the corresponding concrete witness-scan cost. Conversely, a concrete witness packet attaining all minima exists because each clause's permutation can be selected independently and the unchanged checker accepts any literal reorder that preserves clause polarity and incidence. The minimum is therefore *realizable*, not a spurious low-cost abstract path. This argument uses the exact original fixed 7-fixture corpus and does not establish all-rule C3 closure.

The lower envelope over this subclass is **29,238 probes**, not 41,272; the maximum is **53,310**. Any abstract cost that maps every accepted permutation to one class and assigns the canonical 41,272 as a supposed lower bound is *not cost-sound*: the accepted minimum packet is a constructive counterexample, overcharged by **12,034 probes**. All these packets preserve each signed SOURCE clause's semantics and the original AND3/XOR DAG, fixed logical work (321 paid deductions across seven separate proofs), 642 parent applications and the same pretty-printed 197,514-byte packet length. The source-table phase itself remains exactly 4,592 literal probes (14 per three-literal clause over its eight local assignments).

## Original-source seven-fixture evidence

| Fixture | e witnesses | Exact mean | Exact min | Exact max | Variance |
|---|---:|---:|---:|---:|---:|
| K4 | 16 | 448 | 396 | 500 | 128 |
| K33 | 24 | 1,008 | 816 | 1,200 | 1,024 |
| Cube | 32 | 1,792 | 1,408 | 2,176 | 3,413 1/3 |
| Petersen | 40 | 2,800 | 2,124 | 3,476 | 8,234 2/3 |
| Prism6 | 48 | 4,032 | 3,008 | 5,056 | 15,274 2/3 |
| Prism16 | 128 | 28,672 | 19,648 | 37,696 | 447,488 |
| Bridged K4x2 | 36 | 2,520 | 1,838 | 3,206 | 8,023 1/9 |
| **Seven independent packets** | **324** | **41,272** | **29,238** | **53,310** | **483,585 7/9** |

The original source contains 328 independent ordered triples and therefore \(6^{328}\) byte-distinct permutation aliases in this syntactic subclass. The mathematical invariance of incidence, each clause's OR truth values, and every downstream checker operand proves every such alias is accepted, conditional on the original baseline being accepted. This is not a brute-force enumeration of \(6^{328}\) strings. LSPV-5/523 already executed the unchanged OS checker on the minimum and maximum witness-cost packets, both accepted with 30,714 assertion groups. The original checker was **not newly executed in an OS subprocess in the present run**. The self-contained published script supplies an optional --native mode for that replay.

An independent Python proof-control enumerated both possible parity charges, eight complete local assignments each, all six token orders per clause, and obtained exact mean seven in 16/16 cases. A separate original packet JavaScript enumeration evaluated 328 occurrences times six permutations times each fixture's nonnull witnesses, with no sampling.

## Additional same-realization verifier-cost firewall

The original checker also sorts each source clause's three edge IDs before comparing signed incidence, and uses three literal searches via Array.find per clause. The latter requires exactly 1+2+3=6 matches/scans for each source triple, or 1,968 scans across all 328 originals, independent of order. By contrast, **sort comparator invocation counts depend on the JavaScript engine implementation** and should not be written into the fixed logical R_mix341 tariff. This was explicitly falsified during this run: the isolated V8 execution and local Node v22.16.0 V8 12.4.254.21-node.26 report different comparator counts for permutations of three integers. The raw audit preserves both engine-specific ledgers with that warning. In local Node v22.16.0, the six rank orders 012/021/102/120/201/210 use 2/4/3/4/4/2 comparator calls. In that *declared Node model only*, the jointly minimized witness-plus-source-sort-comparator total is 30,133, the maximum 54,281, and the canonical total 41,928. These are not physical CPU-time or bit-operation measurements.

A sound final same-realization ledger must separately charge parsed evidence, source-byte access, paid deduction W, reference applications, actual verification instruction/model costs, cache retention/retrieval, recomputation, scratch and peak writable space. This restricted experiment settles none of the last four coordinates.

## Status and handoff

**F1 not observed** on the authenticated 328 source clauses; all signed parity blocks retain the correct four patterns. **F2 refuted by source semantics and independent predecessor OS min/max acceptance**; order aliases do not change proof or pretty byte length. **F3 confirmed**: 41,272 overcharges the true accepted minimum 29,238. **F4 avoided** by selecting one permutation per clause and taking exact variance across all reuses. Implementation comparator instability was observed and kept separate.

Scientific barriers: the source checker accepts previously identified semantically invalid String-support deductions on satisfiable sources; checker acceptance cannot be conflated with sound UNSAT. Neither the distinct recovered /386 checker nor this experiment supplies the historical full R_mix341 byte grammar or fixed mixed-rule weights. A full shared-DAG cost-sound proof abstraction admitting all legal Resolution, XOR, LOCAL-CONVERT, paid DEF, learning, branches, context joins, weakening, deletions, recomputation and compact representations is still missing. We do not combine bounds from distinct representations or different executions.

Primary methodological sources: Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., CAV 2000, DOI 10.1007/10722167_15; Cook and Reckhow, JSL 44 (1979), DOI 10.2307/2273702. These justify abstract soundness and proof-verifier separation, but supply no historical R_mix341 specification or SAT lower-bound transfer. No relativization/algebrization/Natural Proofs claim is implicated by this restricted finite verifier-cost theorem.

**TRACKERS REVIEWED; NO MATERIAL LOAD-BEARING NODE CHANGE.** This gives a restricted quantitative repair to P2-D1/P2-C3 evidence under prior P2-L5-523, not closure. P2-D1 → P2-C3 → P2-B1 remain OPEN, with P2-B2/B3 separately OPEN. P versus NP remains OPEN. The exact five existing roles and historical two Route A/three Route B labels, identities, titles, schedules, fixed weights and ownership remain unchanged. Next target: apply the same lower-envelope technique to an authenticated **actual mixed-rule** operation with the original historical checker, not a proposed completion.

Publication: executable experiments/arc/lspv4_582_order_expectation_firewall.cjs; raw results/raw/arc/2026-11-13_0241_LSPV4_582_LITERAL_ORDER_MOMENTS_RAW.json; coordination handoff research/coordination/2026-11-13_0241_LSPV4_ORDER_EXPECTATION_FIVE_ROLE_HANDOFF582.md.

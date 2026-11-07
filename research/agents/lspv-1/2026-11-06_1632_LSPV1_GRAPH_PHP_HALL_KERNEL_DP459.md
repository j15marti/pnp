# LSPV-1/459: a certified small-Hall-kernel pure Resolution shortcut

**November 6, 2026, 16:32 PST. Route B lead.** **PROVED/RESTRICTED** upper-bound lemma; **COMPUTATIONAL** independent source-authenticated replay. Historical R_mix341 grammar, B1/B2/B3, full mixed hardness and P versus NP **OPEN**. No tasks, schedules, identities, grammar, weights, peer manuscripts or root `main.tex` were changed.

## Idea, falsifiers and iteration

**Hypothesis:** a small Hall-deficient neighborhood in degree-three graph-PHP gives a **legal RES-only** polynomial-work shortcut even without the four-on-three duplicate-neighborhood obstruction in LSPV-1/458. Four precise falsifiers: (1) selecting $h+1$ pigeons fails to retain a Hall contradiction; (2) binary collision clauses are uncharged instead of derived from the original signed 3-CNF; (3) the proof secretly uses new SPLIT, DISCHARGE, weakening, LOCAL-CONVERT or unproved DEF facets; (4) signed pivots, source indices or assumption scope fail independent replay. The theorem and finite controls exclude these within ordinary RES, not in the unsettled full historical certificate serialization.

**Corpus:** governing Nov. 2 five-role handoff, current issue #3 (including LSPV-1/458), AGENTS.md, CODEX.md, pnp-research skill, original LSPV-2/341 grammar, LSPV-1/457-458, peer LSPV-3/412 and LSPV-5/REFEREE396. Actual Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` were read; neither supplies B3. External checks: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea`; `meelgroup/frat-xor/format.md`; GitHub code searches `openai/math` for CookLevin and Resolution, with no native R_mix341 proof compiler. Sources were inspected as research hypotheses, not authority. General web search was used; a separately branded Google search was unavailable.

## Source definition and published hardness qualification

Take bipartite graph $G=(P,H,E)$, $m$ pigeons, $n$ holes, each pigeon having exactly three **distinct** neighbors. Each edge $(i,j)$ gives one Boolean variable $x_{ij}$ and each pigeon gives an original signed width-three clause $A_i=\bigvee_{j\in N(i)}x_{ij}$. For each pair $i<k$ sharing hole $j$, use two *original* proper three-literal clauses with fresh private padding $z_{ikj}$:

$$
(\neg x_{ij}\vee\neg x_{kj}\vee z_{ikj}),\qquad
(\neg x_{ij}\vee\neg x_{kj}\vee\neg z_{ikj}).
$$

**One paid, oriented RES inference** recovers the corresponding binary collision clause. If $B=\sum_{j\in H}\binom{\deg(j)}2$, the original indexed 3-CNF has exactly $m+2B$ clauses and $3m+B$ variables. UNSAT for $m>n$ follows by pigeonhole; it is not itself a proof-size hardness certificate. De Rezende, Nordström, Risse and Sokolov, *Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs*, TheoretiCS 4 (2025) art. 9, DOI 10.46298/theoretics.25.9, prove exponential **ordinary shared-DAG Resolution** hardness for selected sparse-expander graphs, **not arbitrary graph PHP**. This run constructs deliberately easy negative controls, not a certified-hard expander from their theorem.

## Theorem 459.1 (PROVED/RESTRICTED)

Suppose $S\subseteq P$ has $h=|N(S)|<|S|$. Choose any $S'\subseteq S$ with $|S'|=h+1$. For the exact source above, a source-authenticated, acyclic, shared **strict RES-only** refutation exists with

$$
\boxed{W_{\mathrm{RES}}(F)\le B_{S'}+3^{3(h+1)}
\le 3\binom{h+1}{2}+3^{3(h+1)}.}
$$

**Proof.** $h+1$ pigeons mapped into at most $h$ holes are contradictory, because the pigeon rows force each pigeon to choose a hole and collision clauses forbid sharing. Derive each relevant binary collision from **both original padding clauses**, one paid RES node each. There are at most $3\binom{h+1}{2}$ collisions since each pigeon has three neighbors. The remaining clauses use at most $v=3(h+1)$ original edge variables. Apply the standard *Davis–Putnam variable-elimination* procedure: for each variable, resolve every positive/negative pair with a correctly oriented RES node, discard tautological resolvents, deduplicate and remove pivot-bearing clauses from the **working set**. Each elimination preserves SAT iff SAT, as witnessed by selecting a pivot truth value that satisfies its positive/negative premises when their resolvents hold. Hence after all variables the working set contains the empty clause. Across $v$ variables there are only $3^v$ possible distinct non-tautological signed clauses, so deduplication bounds the paid new nodes by $3^v$. Prune unused proof ancestors to leave an acyclic, source-authenticated refutation DAG. Every retained node is original RES, and shared nodes are counted once. QED.

**Corollary (PROVED/RESTRICTED):** If $h\le c\log_2(N+2)$ for a fixed constant $c$ and source bit length $N$, the ideal **full-mixed** minimum is bounded above by

$$
W_{R_{\mathrm{mix341}}}(F)\le3\binom{h+1}{2}+27(N+2)^{3c\log_2 3}=N^{O(c)}.
$$

This upper bound holds because native RES is a subsystem, regardless of other legal GF(2), AND3, DEF, LOCAL or branching shortcuts that could produce still cheaper proofs. Under standard identifiers, explicit certificate evidence needs $O((N+W)(h+1)\log(N+W))$ bits. If a Hall witness is supplied, certificate construction and checking are polynomial for fixed $c$; **witness discovery** is separately charged. The theorem is neither an all-input SAT algorithm nor a superpolynomial lower bound. On published hard expanders with large Hall neighborhoods it leaves exponential cost possible.

## Independent finite controls

Isolated five-pigeon/four-hole graph: neighbor triples `012,013,023,123,012`. **No four pigeons share one triple**, so LSPV-1/458's constant-size duplicate-neighborhood test does not apply. Complete authentic original strict-3 source: **47 clauses, 36 variables, 575 DIMACS bytes**. A larger seven-pigeon/six-hole graph with neighbor triples `012,013,023,123,012,345,245` has **67 clauses, 51 variables, 832 DIMACS bytes**, while the same 5/4 Hall kernel remains available.

A deterministic Python producer generated **325 candidate** inference nodes then pruned to **92 actual proof-DAG inference nodes**: **21 paid pad eliminations, 71 paid Davis–Putnam resolvents**, 47 original source leaves, ideal unit-weight span **12** and observed intermediate active clause count up to **113**. A separately written JavaScript checker rebuilt every signed original clause and verified every oriented pivot, DAG edge and the root empty clause; **10 corrupted source/proof controls rejected**. The isolated original 47-clause source is **minimally UNSAT**, with **47 independently replayed complete single-source-deletion satisfying assignments**. Thus, under the unchanged unit-paid at-most-binary-conclusion conservative semantics, the restricted exact-minimum interval is $46\le W_R(F_{5/4})\le92$, **not an exact optimum**. The full 7/6 source only has the proved upper bound $W_R\le92$, because another contradiction could be cheaper. Both SAT four-pigeon controls have a matching `0,1,2,3`.

Host measurements in one replay: Python producer/internal validation 0.88 seconds / 96,788 KiB peak RSS, independent Node checker 0.05 seconds / 34,800 KiB peak RSS. Full-source reads, parsing, 325 candidates, failed/unused nodes, clause caching, reference traversal, validation and output are **actual acquisition costs**, not included in the free ideal 92-node choice. Neither host measurement is an FLMV same-machine exponent.

**Duplicate/novelty firewall:** Davis–Putnam resolution elimination is classical (Davis and Putnam, JACM 7(3):201–215, 1960, DOI 10.1145/321033.321034); Hall injection is standard; LSPV-1/458 already addressed a special duplicate-neighborhood kernel. The present small-Hall-kernel bound and authenticated control are a scoped synthesis, **not** claimed new to the literature. Haken Resolution PHP, Cook ER PHP and odd Tseitin GF(2) remain mandatory shortcut/model comparisons.

**Verification/publication firewall:** The complete original signed CNFs, 92-node certificates, 47 deletion models, Python producer, independent JavaScript checker, adversarial tests, raw summary and SHA-256 manifest are in the reproducibility archive delivered to the user. A small public standalone `experiments/arc/lspv1_459_compact_hall_check.cjs` regenerates and verifies the 47-clause/92-node proof. This is a semantic RES proof, **not accepted-byte replay by the unavailable historical R_mix341 checker**. Root `main.tex` was not changed because safe complete readback and preservation were not available.

**Handoff:** LSPV-3 to replay native typed proof; LSPV-5 to attack source ancestry, corrupted pads and possible stronger shortcuts; Route A LSPV-2/4 to retain charged two-label controls without treating this as an all-input splitter. LSPV-1 returns to all-mixed-rule **lower** bounds and genuinely noncircular same-R B3.

**OPEN:** historical native full grammar and compiler, B1, B2, B3, superpolynomial mixed $\overline W_R$, and **P versus NP**.

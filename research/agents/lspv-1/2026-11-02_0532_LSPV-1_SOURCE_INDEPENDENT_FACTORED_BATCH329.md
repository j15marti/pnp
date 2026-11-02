# LSPV-1 SOURCE-INDEPENDENT FACTORED BATCH329

**November 2, 2026, 05:32 PST | Formal Proof Lead | PROVED/EXACT elementary scoped source construction, COMPUTATIONAL finite independent checks; external mathematical review pending. P versus NP OPEN.**

## Exact obstruction and four falsifiers

The only target is ALL valid, proper, duplicate-free Döcker Monotone 3-SAT-(2,2) ORIGINALS with exactly two positive and two negative appearances per original variable. The original-variable forward circuit computes F(x) efficiently for a supplied x; existential Circuit-SAT decision has separately charged work. A raw resolution-CNF representation can expand while a different acyclic circuit representing its *exact existential projection* shrinks.

F1. Does projecting s original variables require enumerating all 2^s Shannon branches before obtaining an exact circuit? **FALSIFIED** for polynomially acquired primal-independent source batches.

F2. Does raw four-resolvent CNF expansion necessarily imply that any forward circuit of the projected Boolean function expands? **FALSIFIED** under two explicitly declared source-private gate architectures.

F3. Does polynomially acquired batch projection solve SAT in polynomial total work on all originals? **NO**: the new circuit is a noncanonical child and its existential satisfiability remains to be determined.

F4. Does the gate difference establish representation-independent lower bounds against all SAT deciders? **INVALID**: these are counts in stated source-private circuit templates, not unrestricted circuit minima or necessary decision-work.

## Theorem 329A: exact simultaneously factored original-source projection

For every valid canonical F on n original variables and m=4n/3 original clauses, construct the source-primal graph, of maximum degree at most 8, and choose its ascending-name greedy maximal independent set I. It is polynomially acquired and has s=|I| >= ceil(n/9). Since no two pivots in I occur in any common original clause, each pivot has four disjoint incident source clauses. Write their two-literal remainders after removing x or NOT x as P_x1,P_x2,N_x1,N_x2, with immutable original source-clause IDs; let H_I be the conjunction of all nonincident original clauses. For every full surviving-variable assignment z,

$$
Q_I(F)(z)=\bigvee_{b\in\{0,1\}^I}F(z,b)
=H_I(z)\wedge\bigwedge_{x\in I}
\big[(P_{x1}\wedge P_{x2})\vee(N_{x1}\wedge N_{x2})\big].
$$

**Proof.** For a given z, x=0 makes both negative source clauses true and requires the two positive remainders; x=1 makes both positive source clauses true and requires the negative remainders. For different selected x, the four incident original clauses are disjoint in source clause identity. Hence existential quantification over the independent pivot inputs distributes among these local factors, while H_I is invariant. This is pointwise equality on all future surviving assignments, not a mere equality of current SAT labels. No source-variable assignment needs to be reconstructed. QED.

This is a simultaneous extension of the already published **LSPV-5 REFEREE281 one-pivot formula** and the **LSPV-1 BATCH321 source-primal n/9 guarantee**. The underlying Davis-Putnam existential elimination principle is classical.

## Theorem 329B: exact restricted gate ledger and adversarial comparator

Fix a fan-in-two AND/OR gate basis with original literal inputs and free unary NOT. In the declared unsimplified source-private factored architecture, there are m-4s unaffected three-literal clauses, each represented by two OR gates; s pivot modules, each requiring four remainder ORs, two ANDs and a final OR; and m-3s factors joined by m-3s-1 binary ANDs. Thus the gate count **exact within this declared syntax** is

$$
g_{\rm factored}=2(m-4s)+7s+(m-3s-1)=3m-4s-1.
$$

The original source-private clause evaluator costs g_forward=3m-1 binary gates. The raw UNNORMALIZED resolution CNF removes four three-literal parents per pivot and inserts four four-literal resolvent records. Its m clause records contain exactly 3m+4s *signed literal occurrences*. A separately declared raw, unshared clause-private AND/OR evaluator costs

$$
g_{\rm raw}=3m+4s-1,\qquad
g_{\rm raw}-g_{\rm factored}=8s.
$$

Each template computes the same exact existential Boolean function Q_I. Tautological resolvents, duplicate outputs, repeated subexpressions and optimal global factoring may lower other circuits' costs. This is **NOT** an unrestricted minimum-gate theorem. In particular, the 8s gap cannot be interpreted as decision-work hardness.

The source-primal maximum degree 8 gives s>=ceil(n/9), and the AG(2,3) B9 valid canonical fixture has primal K9. Disjoint B9 copies have maximum primal independent set exactly n/9; this is sharp for the source-clause-disjoint selection architecture. These copies are efficiently recognizable satisfiable controls and are not decision-hardness witnesses.

## Producer and independently verified same-source controls

The complete reproducibility archive contains a gate-level producer, separate no-producer-import verifier, raw JSON and SHA-256 manifest. Public compact code is at [compact329_public.py](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_329/compact329_public.py). The published [raw summary](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_0532_LSPV1_SOURCE_INDEPENDENT_FACTORED_BATCH329_summary.json) is explicitly finite COMPUTATIONAL evidence.

| Valid canonical original | n,m | Source #SAT | Greedy I | Projected #SAT | Original / factored / raw gates |
|:--|:--|--:|:--|--:|:--|
| F9 | 9,12 | 70 | {1,4} | 48 | 35 / 27 / 43 |
| Z6 (18-model source) | 6,8 | 18 | {1,6} | 12 | 23 / 15 / 31 |
| B9 affine-plane | 9,12 | 18 | {1} | 17 | 35 / 31 / 39 |
| H15 = F9 disjoint union Z6 | 15,20 | 1260 | {1,4,10,15} | 576 | 59 / 43 / 75 |

The independent verifier passed **42,737 counted source, projected-cofactor, complement, S/U compatibility and malformed checks**. On the same original valid F9, common original-variable pins (x3,x5,x6,x7,x8)=(0,1,0,0,0) give two satisfying completions when x1=0 and zero when x1=1; the latter has eight complete independently reconstructed original-clause-falsification leaves. All 264 F9 clause-pair S/U modes were checked, with 37/49/49/37 feasible SS/SU/US/UU cases. Producer malformed source/declared JSON grammar rejection: 17; separate no-import malformed source rejection: nine. The experimental JSON grammar is *not* a native FLMV binary machine specification. U198/V198 are inherited, not freshly rerun.

## Full charges, computation and universal quantifier audit

The *one-round compiler* scans and validates the source and signed quotas, constructs primal adjacency and four-clause incidence indices, pays for every rejected greedy candidate, source/index/head movement, four literal-removal tests per pivot, all gate writes, pointer addresses, output/provenance records and optional raw-resolution comparison. With O(m) gate records of O(log(n+m)) address bits, one explicit materialized implementation has polynomial total bit work and O(N polylog N) peak writable bits, including intermediate source/index/gate/proof sidecars. Finite exhaustive test work is **OFFLINE** and not given free to the SAT machine. Logical XOR is also OFFLINE unless charged.

For an actual adaptive controller D, **all** executed work is charged:

$$
W_D(z)=C_{\rm grammar/source/index/head}
+C_{\rm acquire/gate/proof/GE}
+C_{\rm failed/select/switch}
+C_{\rm cache/replay/child/output/access/guest}
+\sum_{y\in {\rm ExecutedChildren}(z)}W_D(y).
$$

Peak space is the maximum simultaneous live source/index/head, ancestor, cache/proof, output and guest DELAY/COPY/RECOMP work-tape configuration. This finite circuit reduction does not bound the aggregate successor sum, choose free exact semantic classes, yield hereditary canonical children, or give a strict same-machine FLMV numerical transfer.

The P=NP constructive target needs a *single* total exact uniform D and constants c,C such that **for every binary input** u, W_D(u)<=C(|u|+1)^c. A P!=NP necessary-work route needs a lower bound against **every** correct decider and every fixed polynomial degree on arbitrarily large target inputs. The alternative arbitrary-A ARC transformation must work for unknown K,L, be uniformly power-short and fully charged, and separately satisfy strict numerical native FLMV transfer. **None is established. P versus NP OPEN.**

The exhaustive fallback after this batch takes polynomial times 2^(n-s), still exponentially bounded and slower than the reviewed **Peng–Xiao IJCAI 2023** unchanged-source four-occurrence SAT algorithm O*(1.2628^n) with polynomial space. The **October 25, 2026 OpenAI ETH preprint**, if its claimed k-CNF exact counter is validated, would provide another direct subexponential polynomial-space route; that result remains **CONDITIONAL pending independent examination**, not a settled theorem in this report.

## Prior work, references and next falsification

Preflight: read the verified 2026-11-01 19:50 five-role SAT/Circuit-SAT handoff first, then the decision-only handoff, AGENTS/CODEX/pnp-research skill, issue #3, LSPV-1 BATCH321/ITERATED327/SOURCE-ALGORITHM328, LSPV-5 REFEREE281, and current cofactor resource reports. Project GitHub query "independent set circuit existential projection" identified REFEREE281. GitHub openai search "quantifier elimination circuit" returned no code matches; this is not evidence of novelty. Literature searches examined original SAT variable elimination and current bounded-occurrence and ETH claims.

Primary sources: Davis and Putnam (JACM 1960, DOI 10.1145/321033.321034); Dechter (Artificial Intelligence 1999, DOI 10.1016/S0004-3702(99)00059-4); Eén and Biere (SAT 2005, DOI 10.1007/11499107_5); Peng and Xiao (IJCAI 2023, DOI 10.24963/ijcai.2023/223); OpenAI *The Exponential Time Hypothesis is False*, preprint dated October 25, 2026, [source repository](https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026).

**Next precise gate:** test whether source-factored batches can be repeatedly eliminated with polynomial **total** DAG size and paid semantic sharing on overlapping source variables. Use adversarial separators, affine/Horn/2-SAT controls, and known faster direct decision algorithms as falsifiers. No tasks, schedules or identities were changed. **P versus NP OPEN.**

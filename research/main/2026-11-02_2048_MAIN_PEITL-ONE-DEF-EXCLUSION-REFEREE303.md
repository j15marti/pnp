# PEITL-ONE-DEF-EXCLUSION-REFEREE303

**PNP Independent Proof Red Team — November 2, 2026, 20:48 PST**

**Status.** **PROVED/EXACT** for the topology reduction in the unchanged source-independent-VARDEF $R_{\mathrm{mix341}}$; **COMPUTATIONAL/EXHAUSTIVE FINITE** for two independently implemented relaxed tree enumerations; **PROVED** that the one-DEF cost-eight class is impossible for the authentic Peitl--Szeider source; **OPEN** for the remaining bicyclic cost-eight class, a superpolynomial worst-case mixed minimum, B1, B2, B3, and P versus NP.

## Exact obstruction and claim card

- **Claim ID:** PEITL-ONE-DEF-EXCLUSION-REFEREE303.
- **Input:** authentic `rsmu_5_7_1.cnf`, SHA-256 `6ca65edf800525363d4153b266cd4f4d207bd3a8977064c74996bc363ee8f6d6`, 74 encoded bytes, five variables and seven clauses.
- **Fixed calculus:** the preselected $R_{\mathrm{mix341}}$: authenticated original clauses cost zero; binary RES, exact AND3, binary affine GF(2) XOR, exact unary CONVERT and source-independent conservative VARDEF are paid unit nodes. A VARDEF introduces a fresh variable for a local two-input Boolean gate and exposes its authenticated defining CNF slots. Every used slot cites that paid zero-premise DEF node.
- **Cost:** distinct paid nodes in a shared contradiction DAG. The best derivation is selected freely; optimizer discovery is not charged to $W_R$.
- **Predecessor interval:** REFEREE302 proved

$$
8\leq W_{R_{\mathrm{mix341}}}(F)\leq 9.
$$

- **Exact obstruction attacked here:** can the lower endpoint be attained by one paid zero-premise DEF plus seven binary inference nodes?

The remaining cost-eight split follows from the already proved source-excess identity. For a clause-minimally UNSAT source with $\mu=7$, let $q$ be paid nodes, $\beta$ the undirected cyclomatic excess of the contradiction ancestry, $u$ the number of paid unary nodes and $d_0$ the number of paid zero-premise nodes. Then

$$
q-(\mu-1)=\beta+u+2d_0.
$$

At $q=8$, the excess is two. REFEREE302's stronger free-alias tree/unicycle search already excludes the cases containing one or two unary conversions: contracting those conversions produces a previously exhausted tree or unicycle with the same freely available exact representation alias. Thus the only unresolved classes entering this run were

$$
(\beta,u,d_0)=(2,0,0)\quad\text{or}\quad(0,0,1).
$$

This report excludes the second class.

## Why one DEF reduces to one arbitrary local slot

Assume $(\beta,u,d_0)=(0,0,1)$. The seven non-DEF derived nodes all have two named proof premises, so the ancestry has fourteen premise edges on fifteen vertices: seven original sources plus eight paid nodes. Connectedness and $eta=0$ force the underlying graph to be a tree. The DEF node is one of the eight indegree-zero vertices. It cannot feed two different consumers: two directed paths from the same DEF to the unique contradiction root would reconverge and create an undirected cycle. Therefore exactly one authenticated DEF slot occurs as one leaf of a source-once binary inference tree.

Every total local two-input gate relation $y\leftrightarrow g(a,b)$ admits only defining clauses involving the fresh output $y$ and at most the two input variables. An input-only non-tautological clause would forbid an input assignment and would not be a conservative definition of a total gate. To avoid depending on the finite gate basis or on a preferred prime CNF, the enumeration grants the DEF leaf **every** non-tautological clause that contains fresh variable $y=x_6$ and zero, one or two of the five original variables, in all polarities. The number is

$$
2\left(1+\binom51 2+\binom52 2^2\right)=102.
$$

This is a strict rule relaxation: it includes every AND, OR, XOR and other local binary-gate defining slot, including unary/constant degeneracies, whether or not the fixed basis actually contains that gate.

For each of the 102 possible extra leaves, the program exhausts every source-once binary tree over the seven labelled original clauses and that leaf. At every internal node it grants a further lower-bound relaxation:

1. every exactly equivalent clause representation is available for free;
2. every exactly equivalent affine GF(2) representation is available for free;
3. AND3 is allowed whenever the **output** truth function has essential support at most three, even when the two inputs jointly mention more variables.

RES, XOR and AND3 outputs are memoized only by their exact 64-bit truth tables. Absence of the false truth table after these relaxations excludes the actual fixed-calculus tree.

## Exhaustive result

The producer enumerated all 102 relaxed DEF slots and found no contradictory terminal. Aggregate counts were:

| quantity | count |
|---|---:|
| relaxed DEF slots | 102 |
| operand-pair tests | 557,276 |
| generated rule outputs before deduplication | 192,480 |
| stored subset states across all cases | 99,286 |
| distinct cached operand pairs | 52,815 |
| terminal-function range by slot | 0 to 107 |
| contradictory terminals | 0 |

A separate no-import verifier reimplemented parsing, truth tables, clause/affine aliases, the rule combiner, subset partition order and all 102 slots. It agreed case by case and reproduced all aggregate counts. The producer raw SHA-256 checked by the verifier is `705d79148b0baa61867614583f1efca1e5d3ce85d318c43a4c7417e09b12479e`.

**Theorem (finite exact branch exclusion).** The authentic `rsmu_5_7_1.cnf` has no cost-eight $R_{\mathrm{mix341}}$ refutation with one paid source-independent local VARDEF. Consequently, if its mixed minimum is eight, every cost-eight refutation has bicyclic binary ancestry. The certified state is

$$
8\leq W_{R_{\mathrm{mix341}}}(F)\leq9,
$$

with the lower endpoint now confined to $(\beta,u,d_0)=(2,0,0)$.

This does **not** prove $W=9$: a complete bicyclic enumeration or an eight-node witness remains necessary.

## Both-label, malformed and provenance controls

The authentic source is UNSAT by complete enumeration. Deleting its seven clauses gives SAT model counts

$$
(4,4,4,4,4,1,1),
$$

so all seven sources are indispensable. All 20 individual signed-occurrence flips are SAT, with model counts ten copies of 4 followed by ten copies of 1. The prior nine-node Resolution certificate was replayed unchanged as the upper witness.

The independent run rejected all eight malformed DIMACS fixtures: missing header, wrong problem keyword, declared-count mismatch, out-of-range variable, missing zero terminator, duplicate literal, tautological clause and negative dimensions. Odd-charge $K_4$ Tseitin has zero models; the matched even-charge control has eight. These controls prevent an all-UNSAT promise, parser acceptance or parity-only shortcut from entering the branch exclusion.

## Four falsifiers and dispositions

1. **One clever XOR/AND/OR extension gate supplies a cost-eight proof. — FALSIFIED for this source.** Every one of its local defining clauses is among the 102 relaxed leaves, and none reaches false in any mixed source-once tree.
2. **The finite gate basis was underspecified, so the negative search omitted a legal slot. — REPAIRED and FALSIFIED at the slot level.** The search covers every conservative total two-input gate clause over the fresh output and its at most two original inputs, not merely the AND replay used in REFEREE299.
3. **A one-DEF proof can use two different authenticated slots without paying another node. — FALSIFIED by topology at cost eight.** Multiple uses of the zero-premise DEF create reconvergence and positive cyclomatic excess, contradicting $(\beta,u,d_0)=(0,0,1)$.
4. **Eliminating the one-DEF branch proves the exact minimum nine or a worst-case lower bound. — FALSIFIED.** Bicyclic binary ancestry remains open; this is one 74-byte finite source and gives no asymptotic lower bound.

## B1, B2 and B3 referee classification

This run proves none of the transfer obligations.

- **B1 remains OPEN.** No arbitrary correct decider trace was translated to an $R_{\mathrm{mix341}}$ proof.
- **B2 remains OPEN.** One finite instance and one topology branch do not bound $\overline W_R(N)$ from worst-case runtime.
- **B3 remains OPEN.** SAT in P is not shown to imply polynomial worst-case proofs in this same fixed calculus.

The distinction is material. Atserias--Müller show hardness of approximately automating Resolution, which concerns discovering short proofs, whereas $W_R$ grants the best proof for free. Conversely, a fast SAT decider does not automatically emit a sound proof or a proof of its own correctness. Neither fact settles B3.

## Logical cost versus implemented work and space

The branch being excluded has logical cost eight. The exhaustive certificate search is external work, not part of that minimum. The producer charged source parsing, 64-bit truth-table construction, alias generation, all 102 sequential subset banks, failed candidates, cache accesses, complete SAT/deletion/sign controls, malformed controls, parity controls, upper-proof replay and JSON materialization. It took 1.684 seconds and 17,924 KiB peak host RSS. The separate verifier took 1.864 seconds and 28,640 KiB peak host RSS. These are implementation upper measurements, not matched-machine lower bounds.

The logical DAG count also does not by itself give a storage schedule. Encoded certificate bits, random dependency validation, cache retention, recomputation and input rereads remain separate. Any recursive machine-space use must retain

$$
s'\leq\max\{\rho,\eta,\lambda,\lambda s\},
$$

where $\rho$ covers every local phase, including parsing, slot generation and allocate-then-free preprocessing.

## Literature, project and GitHub audit

Search queries recorded for this run included: `Extended Resolution proof system lower bounds open problem primary paper`; `Extended Resolution defining clauses binary gate proof checker TACAS 2021 BDD`; `Peitl Szeider Finding the Hardest Formulas for Resolution JAIR 2021`; `Atserias Muller Automating Resolution is NP-hard primary paper`; project searches for `VARDEF source-independent REFEREE299`, the 20:00/20:12/20:24 peer reports and the cost-eight Peitl interval; and OpenAI GitHub searches `extended resolution SAT proof checker`, `resolution proof DRAT auxiliary variable`, and `Peitl Szeider resolution`.

Relevant findings:

- R. Bryant and M. Heule, *Generating Extended Resolution Proofs with a BDD-Based SAT Solver*, TACAS 2021, <https://doi.org/10.1007/978-3-030-72016-2_5>, explicitly counts defining clauses for extension variables and independently checkable derived clauses. It supports treating definition slots as syntax that must be authenticated, not as a free semantic oracle.
- A. Atserias and M. Müller, *Automating Resolution is NP-Hard*, JACM 67(5), 2020, <https://www.cs.upc.edu/~atserias/papers/automating-resolution-np-hard/automating-resolution-np-hard.pdf>, separates proof search/automatization from shortest proof size. It does not prove a lower bound for this mixed system.
- T. Peitl and S. Szeider, *Finding the Hardest Formulas for Resolution*, JAIR 72 (2021), 69--97, and extended abstract <https://doi.org/10.24963/ijcai.2021/657>, concern exact Resolution hardness. The present source is authentic, but their optimum does not transfer automatically to $R_{\mathrm{mix341}}$.
- REFEREE299 and LSPV-2 DEF-SUPPORT-COVERAGE346 fix the operative source-independent local VARDEF reading and explicitly distinguish it from an unformalized source-factor macro. The 20:00 LSPV-1 corridor and 20:24 LSPV-3 iterated-guard theorem remain consistent: neither supplies mixed hardness or B3.
- The searched `github.com/openai` results were unrelated notebook prose or mathematical uses of the word “resolution”; no relevant classical ER/Rmix checker was identified. No novelty is inferred from that negative search.

No task, title, enabled state, schedule or ownership was created or changed. Historical paused descriptions were treated only as history. P versus NP remains OPEN.

## Exact next gap

Enumerate or structurally exclude every eight-node all-binary contradiction DAG with seven indispensable sources and cyclomatic excess two, under the same free clause/affine alias and output-support AND3 relaxations; alternatively exhibit and independently replay an eight-node legal mixed proof. This is the only remaining finite route to decide whether the authentic source has mixed minimum eight or nine. Separately, seek a growing nonaffine family hard for **every** fixed rule and prove B3 for this same calculus.

## Artifacts

- `experiments/arc/lspv5_303/peitl_one_def_exclusion_referee303.py`
- `experiments/arc/lspv5_303/verify_peitl_one_def_exclusion_referee303.py`
- `results/raw/arc/2026-11-02_2048_LSPV5_PEITL_ONE_DEF_EXCLUSION_REFEREE303_raw.json`
- `results/raw/arc/2026-11-02_2048_LSPV5_PEITL_ONE_DEF_EXCLUSION_REFEREE303_verify.json`


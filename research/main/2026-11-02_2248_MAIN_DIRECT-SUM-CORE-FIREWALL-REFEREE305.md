# DIRECT-SUM-CORE-FIREWALL-REFEREE305

**PNP Independent Proof Red Team — November 2, 2026, 22:48 PST.**  
**Status:** **PROVED** universal axiom-monotonicity firewall for the unchanged fixed calculus; **FALSIFIED** direct-sum/additive amplification; **COMPUTATIONAL/EXACT** finite controls; B1, B2, B3, superpolynomial worst-case hardness, and **P versus NP remain OPEN**.

## Result

Fix the already selected sound, complete, effective $R_{\mathrm{mix341}}$: authenticated CNF sources have weight zero; every legal RES, AND3, affine XOR, CONVERT, and source-independent conservative VARDEF inference has unit weight; shared DAG nodes count once. The calculus and weights are fixed independently of every input below.

The proposed amplification lemma was:

> If an UNSAT core $F$ has minimum cost $h$, then the conjunction of $k$ variable-disjoint renamed copies has minimum cost at least $kh$.

This lemma is false, not merely unproved.

### Axiom-monotonicity theorem

Let $R$ be any source-monotone refutation calculus: a derivation citing source axioms from $F$ remains valid after additional source axioms are supplied. This includes the fixed $R_{\mathrm{mix341}}$. If $F\subseteq G$ are CNFs and $F$ is UNSAT, then

$$
W_R(G)\le W_R(F).
$$

**Proof.** Choose a minimum $R$-refutation DAG $\pi$ of $F$. Every source leaf cited by $\pi$ is still an authenticated source of $G$. Every rule justification, dependency edge, auxiliary freshness condition and inference weight is unchanged. Hence the identical DAG $\pi$ refutes $G$ at the same cost. Minimizing over all refutations of $G$ proves the inequality. $\square$

For pairwise variable-disjoint renamed copies $F^{(1)},\ldots,F^{(k)}$,

$$
W_R\!\left(\bigcup_{i=1}^{k}F^{(i)}\right)
\le \min_i W_R(F^{(i)}).
$$

Thus unguarded direct sums, arbitrary extra clauses, disconnected UNSAT replication and syntactic padding cannot amplify a fixed hard core. The proof is independent of optimizer discovery because the best core refutation is selected freely in $W_R$.

## Falsifiers

1. **Additive direct sum:** $W_R(F^{\dot\cup k})\ge kW_R(F)$. **FALSIFIED:** the first-copy proof gives $W_R(F^{\dot\cup k})\le W_R(F)$.
2. **Encoded-length padding forces logical growth.** **FALSIFIED:** the tested family grows from 74 to 12,894 encoded bytes while retaining a nine-node upper proof.
3. **Minimality/sign sensitivity survives local replication.** **FALSIFIED:** for $k\ge2$, deleting one clause or flipping one occurrence in one block leaves another untouched UNSAT block; the full conjunction remains UNSAT.
4. **A small contradictory core cannot destroy a large-family lower bound.** **FALSIFIED:** adjoining $(z)$ and $(\neg z)$ gives an exact one-node Resolution refutation irrespective of all other clauses.

These are **FAMILY FAILURES**. They do not refute any transfer bridge.

## Authentic Peitl calibration

Use the authentic seven-clause, five-variable Peitl--Szeider source from REFEREE304, whose fixed-calculus minimum is already certified as

$$
W_{R_{\mathrm{mix341}}}(F)=9.
$$

For $k\in\{1,2,4,8,16,32,64,128\}$, rename variables independently in each copy and concatenate all clauses. The nine-node Resolution certificate from the first copy is lifted only by shifting references to derived lines past the newly inserted unused source clauses. Every pivot, resolvent and final empty clause replays exactly.

| copies $k$ | variables | clauses | encoded bytes | false additive target $9k$ | certified upper |
|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 7 | 74 | 9 | 9 |
| 2 | 10 | 14 | 144 | 18 | 9 |
| 4 | 20 | 28 | 312 | 36 | 9 |
| 8 | 40 | 56 | 648 | 72 | 9 |
| 16 | 80 | 112 | 1,321 | 144 | 9 |
| 32 | 160 | 224 | 2,910 | 288 | 9 |
| 64 | 320 | 448 | 6,238 | 576 | 9 |
| 128 | 640 | 896 | 12,894 | 1,152 | 9 |

No exact value is claimed for $k\ge2$; cross-component mixed rules might shorten the proof further. The constant upper bound alone disproves additive amplification.

## Both-label and hostile controls

The base source is UNSAT. Removing its first clause gives four models; flipping its first occurrence also gives four models. Applying the same deletion or sign flip in **every** disjoint block yields SAT, and the verifier joins one local witness per variable-disjoint block. Applying the change in only one block yields SAT only for $k=1$ and remains UNSAT for $k\ge2$, because another authentic block is untouched.

The largest tested union plus fresh units $(z),(\neg z)$ has 641 variables, 898 clauses and 12,907 encoded bytes, yet

$$
W_{R_{\mathrm{mix341}}}=1.
$$

The lower bound is one because there is no empty source clause and inference nodes have unit weight; resolving the two units attains it. Odd/even $K_4$ parity controls have respectively 0 and 8 models. Eight malformed DIMACS fixtures are rejected. The no-import verifier independently reconstructs all copy sizes, encoded lengths, lifted proof indices, local model counts and status classifications: **75 checks PASS**.

## Why this does not address the maximum incorrectly

The worst-case function is a maximum:

$$
\overline W_R(N)=max_{F\text{ valid UNSAT},\ |F|\le N}W_R(F).
$$

Producing large easy formulas does not upper-bound this maximum and does not rule out other hard formulas at the same length. The theorem only retires an attempted construction of a hard family from a fixed core. A genuine amplification transformation must prevent a proof from ignoring all but one embedded contradiction and must be proved sound for every rule in the **same** fixed mixed calculus. Published proof-complexity hardness amplification and hardness condensation use nontrivial gadgets/lifting, not mere disjoint replication; their restricted-system conclusions do not automatically transfer to extension-enabled $R_{\mathrm{mix341}}$.

## Transfer classification

| Obligation | Status | Exact reason |
|---|---|---|
| B1 pointwise | **NOT REFUTED / OPEN** | The replicated family has a constant-cost $R$ proof, so it cannot witness a fast-decider/large-proof separation. |
| B2 worst-case | **NOT REFUTED / OPEN** | No total decider or $T_A^{\mathrm{wc}}(N)$ comparison is used. |
| B3 weakest bridge | **OPEN** | Retiring one family construction neither proves nor falsifies conditional p-boundedness of the same $R$. |
| Superpolynomial $\overline W_R$ | **OPEN** | The maximum may be attained by unrelated interacting formulas. |

No accepting/rejecting trace is treated as a correctness proof. No SAT oracle, nonuniform advice, instance-tailored axiom, semantic jump, or hidden uncharged computation is introduced.

## Literature and project search record

Searches included `proof complexity disjoint union direct sum resolution refutation size`, `resolution hardness amplification disjoint union CNF`, `proof complexity hardness condensation direct product CNF`, `site:github.com/openai resolution proof checker SAT direct sum`, and project searches for `DIRECT-SUM`, `disjoint union`, `COMPONENT-AMORTIZATION-FIREWALL`, `GUARD-EXCESS-CAP350`, `HETEROGENEOUS-SPLIT-EXCESS353`, and the 22:01 selector-shape audit.

- Beame, Huynh and Pitassi, *Hardness Amplification in Proof Complexity* (2010), give a genuine transformation from tree-Resolution hardness to rank hardness in stronger bounded-degree systems; this supports the distinction between nontrivial lifting and naive union: [ECCC TR09-072](https://eccc.weizmann.ac.il/report/2009/072/), [arXiv](https://arxiv.org/abs/0912.0568).
- Berkholz and Nordström's hardness-condensation work combines nontrivial condensation with proof-space lower bounds rather than padding a fixed contradiction: [ECCC TR16-203](https://eccc.weizmann.ac.il/report/2016/203/), [ICALP version](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2016.57).
- Peitl--Szeider's work computes finite shortest Resolution proofs, including the authentic source used here; it does not assert direct-sum amplification: [IJCAI 2021](https://www.ijcai.org/proceedings/2021/657).
- Project REFEREE259 handled certified peeling of **satisfiable** disconnected components for a historical canonical re-entry construction. It did not state the present UNSAT-subcore minimum-cost monotonicity theorem. Current peer guard/split and selector-shape results independently show that several more sophisticated padding constructions also fail to amplify excess.
- GitHub/OpenAI searches returned no relevant implementation of this exact mixed-calculus direct-sum claim. No novelty inference is drawn from a failed search.

## Resource ledger

The final producer run completed parsing, replication through 128 copies, canonical DIMACS sizing, certificate lifting/replay, SAT witness construction, parity and malformed controls, and JSON output in about 0.006 seconds with 11,136 KiB peak RSS. The independent verifier completed in about 0.003 seconds with 10,112 KiB peak RSS. These host measurements are certification work, not $W_R$. The logical upper proof has nine paid nodes regardless of $k$; reading or materializing the padded input is separate scheduled machine work. No FLMV space claim is made.

## Classification and next gap

- **PROVED:** source-axiom monotonicity and constant-cost disjoint-replication upper bound.
- **FALSIFIED:** additive direct-sum amplification, length-only padding growth, inherited local minimality, and immunity to tiny contradictory cores.
- **COMPUTATIONAL/EXACT:** eight replication sizes, proof replays, both-label controls, tiny-core proof, malformed and parity controls.
- **RESTRICTED:** the concrete constant nine uses the authentic Peitl core and fixed $R_{\mathrm{mix341}}$; the monotonicity theorem is broader.
- **OPEN:** a genuinely interacting growing family, a mixed-rule/VARDEF-stable lower invariant, B1, B2, B3, and P versus NP.

The next candidate must be globally contradiction-minimal or otherwise prevent every small UNSAT sub-CNF, while also surviving affine, circuit, Horn, Resolution and auxiliary-definition shortcuts in the same preselected calculus.

## Artifacts

- `experiments/arc/lspv5_305/direct_sum_core_firewall_referee305.py`
- `experiments/arc/lspv5_305/verify_direct_sum_core_firewall_referee305.py`
- `results/raw/arc/2026-11-02_2248_LSPV5_DIRECT_SUM_CORE_FIREWALL_REFEREE305_raw.json`
- `results/raw/arc/2026-11-02_2248_LSPV5_DIRECT_SUM_CORE_FIREWALL_REFEREE305_verify.json`

**END::LSPV5::DIRECT-SUM-CORE-FIREWALL-REFEREE305::B1-B2-B3-OPEN::P-VS-NP-OPEN**

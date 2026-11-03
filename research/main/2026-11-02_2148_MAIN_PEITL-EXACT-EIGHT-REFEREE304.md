# PEITL-EXACT-EIGHT-REFEREE304

**PNP Independent Proof Red Team — November 2, 2026, 21:48 PST.**  
**Status:** **PROVED/EXACT finite in the fixed project calculus, conditional only on ordinary finite SAT-solver correctness; independently reproduced by two SAT engines and a no-import artifact auditor.** A superpolynomial worst-case minimum, B1, B2, B3, and **P versus NP remain OPEN**.

## Executive result

Fix the already selected source-independent calculus $R_{\mathrm{mix341}}$: authenticated source clauses have weight zero; every binary Resolution, exact support-at-most-three conjunction (AND3), affine GF(2) row addition (XOR), exact unary conversion, and conservative local VARDEF inference has unit node weight. Shared DAG nodes count once. The calculus, rule syntax, and weights were fixed before this instance.

For the authentic seven-clause, five-variable Peitl--Szeider instance `rsmu_5_7_1.cnf`, this run closes the last eight-versus-nine gap:

$$
W_{R_{\mathrm{mix341}}}(F)=9.
$$

REFEREE302 had excluded every relaxed derivation with at most seven paid nodes. REFEREE303 excluded the only cost-eight topology containing a paid source-independent VARDEF and reduced every remaining cost-eight candidate to an all-binary bicyclic ancestry. This run gives an exact propositional encoding of that remaining class. Glucose4 and MapleChrono independently report all 105 exhaustive topology-degree cases UNSAT. A nine-node mixed proof is admitted by the same encoder and replays directly; the existing nine-node Resolution certificate also replays to the empty clause.

This is a finite calibration, not an asymptotic result. It proves only

$$
\overline W_{R_{\mathrm{mix341}}}(N_F)\ge 9
$$

at the source's encoded-length threshold $N_F$. It supplies neither superpolynomial growth nor any transfer bridge.

## Exact obstruction and falsifiers

The obstruction was: **can two shared binary reconvergences compress the authentic seven-source contradiction from nine paid nodes to eight by mixing Resolution, affine cancellation, and compact AND3 states?** Four falsifiers were tested.

1. **Bicyclic mixed shortcut.** Search every eight-node binary DAG, permitting RES, XOR, and AND3 at every node, free exact clause/affine aliases, temporary nonclausal states, adaptive rule choice, and shared subproofs. **FALSIFIED:** all encoded cases are UNSAT.
2. **Hidden one-DEF shortcut.** Allow one paid local source-independent conservative definition and every legal defining slot. **FALSIFIED previously by REFEREE303:** all 102 relaxed defining-slot searches exclude false at cost eight.
3. **Encoding accidentally rejects legal short proofs.** Run the identical encoder at nine nodes and require contradiction. **FALSIFIED:** SAT in 5.37 seconds; all nine nodes replay under the declared mixed semantics and the final truth table is false.
4. **Finite optimum silently establishes a bridge.** Check B1, B2, and B3 separately. **FALSIFIED as an inference:** the result contains no arbitrary-decider simulation, worst-case domination theorem, or conditional fixed-system p-boundedness theorem.

## Why 105 cases are exhaustive

There are seven indispensable source lines and eight paid binary inference lines. REFEREE302's $W\ge8$ result means an eight-node counterproof cannot contain padding: every source and every nonfinal inference must occur in the final contradiction's ancestry. The eight binary nodes select exactly sixteen premise edges. There are fourteen nonroot lines, each with outdegree at least one, so

$$
\sum_{v\ne r}(\operatorname{outdeg}(v)-1)=16-14=2.
$$

Consequently exactly one of two degree patterns occurs:

- one of fourteen lines has outdegree three and every other nonroot line has outdegree one; or
- two of fourteen lines have outdegree two and every other nonroot line has outdegree one.

Thus the exhaustive split has

$$
14+\binom{14}{2}=105
$$

cases. Acyclic line order plus the requirement that every nonfinal line is used later makes every line a root ancestor. Canonical left-parent $<$ right-parent is without loss because AND3 and XOR are commutative and the RES encoding contains both pivot orientations. Same-parent nodes are redundant in a minimum proof: AND3 repeats its premise, XOR of an affine row with itself gives the true row, and a non-tautological clause cannot resolve with itself.

## Propositional encoding

Each of eight derived nodes contains a 32-bit truth table over the five original variables. It selects two earlier lines and exactly one rule.

- **RES:** each selected premise and output is tied exactly to a non-tautological clause representation; one signed pivot orientation is selected; the output is precisely the non-tautological resolvent.
- **XOR:** each premise and output selects one of the 64 affine equations over five variables, and the output mask/right-hand side is the GF(2) sum.
- **AND3:** the output is the pointwise conjunction, and one pair of variables is certified inessential, which is equivalent here to essential support at most three.

The final 32 output bits are false. Exact parent selection, topological order, full ancestry, canonical operand order, and one of the 105 degree cases are imposed propositionally. The generated DIMACS has **26,787 variables**, **168,121 clauses**, and SHA-256 `c6febf1d1bcbd0718a4f9e8ec65104d024c44896cba15371258965771fa4c74f`.

The encoder is a lower-bound relaxation of the fixed calculus on the remaining branch: exact clause and affine conversions are free, and AND3 is admitted solely from its output support. Therefore UNSAT excludes the actual all-binary cost-eight branch.

## Results and controls

| Check | Result |
|---|---:|
| Glucose4 degree cases | 105/105 UNSAT |
| Glucose4 time / conflicts / peak process RSS | 281.70 s / 2,581,170 / 116.9 MiB |
| MapleChrono degree cases | 105/105 UNSAT |
| MapleChrono time / conflicts / peak process RSS | 185.97 s / 1,271,676 / 95.1 MiB |
| Nine-node positive encoding | SAT; replay valid |
| No-import auditor | 14/14 checks PASS |
| Authentic source models | 0 |
| Every one-clause deletion | SAT |
| Every occurrence-sign flip | SAT |
| Odd/even K4 parity controls | 0 / 8 models |
| Malformed controls | all rejected |
| Nine-node Resolution upper | direct replay to empty clause |

The no-import auditor independently reparses the source and generated DIMACS, recomputes labels, deletion and sign-flip neighbors, checks all 105 pattern identities and results, verifies the DIMACS hash/header/body counts, and replays the Resolution upper certificate. It does not pretend that reading a solver's `UNSAT` bit is a formal proof trace; the second CDCL engine is an independent computational reproduction over the same generated encoding. A future strengthening should emit and independently check DRAT/LRAT certificates for every assumption case.

## Transfer referee

| Obligation | Status | Reason |
|---|---|---|
| Pointwise B1 | **OPEN** | No translation from every total correct SAT decider into $R_{\mathrm{mix341}}$ derivations was constructed. |
| Worst-case B2 | **OPEN** | One finite hard instance and two finite optimizer runs say nothing about $T_A^{\mathrm{wc}}(N)$ for arbitrary $A$. |
| Weak conditional B3 | **OPEN** | No proof that `SAT in P` makes this same fixed calculus polynomially bounded was supplied. |
| Superpolynomial $\overline W_R$ | **OPEN** | Exact value nine is finite and constant; the peer split/guard results show naive padding need not amplify excess. |

An accepting/rejecting machine trace was never treated as a proof of machine correctness. No SAT oracle, instance-tailored axiom, correctness axiom, after-answer constant circuit, or free semantic jump was added. Optimizer discovery cost is intentionally excluded from $W_R$ but recorded separately below.

## Literature and project search log

Queries included `Peitl Szeider shortest resolution proof SAT encoding`, `bicyclic proof DAG shortest resolution`, `extended resolution lower bounds auxiliary definitions`, `DRAT LRAT independently checked UNSAT proof`, project searches for `REFEREE302`, `REFEREE303`, `GUARD-EXCESS-CAP350`, `HETEROGENEOUS-SPLIT-EXCESS353`, `G342_MIXED_SPLIT_FLOOR350`, and GitHub searches in `openai/*` for shortest-proof and proof-checker implementations.

- Peitl and Szeider's shortest-proof work explicitly uses SAT encodings to compute shortest Resolution proofs and publishes the `short-proof` implementation: [IJCAI extended abstract](https://www.ijcai.org/proceedings/2021/657), [implementation](https://github.com/peitl/short-proof). This run adapts the methodology to the declared mixed truth-table calculus; it does not claim novelty for SAT-based proof minimization.
- PySAT is the implementation substrate (Ignatiev, Morgado, Marques-Silva, SAT 2018), already cited by Peitl--Szeider.
- The proof-complexity literature stresses that auxiliary definitions can dramatically shorten Resolution proofs and that strong general lower bounds are unavailable; this is why VARDEF was handled as a separate fixed-calculus branch rather than ignored.
- Project peers at 21:12, 21:24, and 21:36 PST independently showed that guard/split padding does not manufacture growing excess and closed nearby exact split minima. Those results are consistent with this finite optimum and sharpen the next-family requirement.
- The OpenAI GitHub search returned no relevant shortest propositional-proof encoder or independent DRAT/LRAT checker; no novelty inference is drawn from that negative search.

## Work/space ledger

Logical cost is nine distinct paid inference nodes. The best derivation is freely selected in $W_R$; neither SAT encoding nor solver search is charged to that minimum. Actual certification work was separate: source parsing, truth-table construction, 26,787-variable CNF materialization, 105 incremental assumption solves per engine, both-label/malformed controls, direct replay, JSON output, and readback auditing. Peak host RSS was 119,692 KiB for the Glucose run and 97,396 KiB for MapleChrono. The explicit 1.7 MB DIMACS and solver databases are not a sublinear-space algorithm, do not satisfy an FLMV hypothesis, and imply no arbitrary-machine work lower bound.

## Classification and next gap

- **PROVED:** topology identity and the composition of prior branch reductions with the current exhaustive encoding.
- **COMPUTATIONAL/EXHAUSTIVE FINITE:** all 105 UNSAT cases, reproduced by Glucose4 and MapleChrono; positive nine-node replay and 14-check independent audit.
- **RESTRICTED:** exact minimum nine only for this authentic formula in the fixed $R_{\mathrm{mix341}}$ grammar and weights.
- **CONDITIONAL:** solver answers rely on ordinary SAT-engine correctness; a proof-logged LRAT upgrade would reduce this trust base.
- **OPEN:** a growing family with superpolynomial $\overline W_R$, a mixed-rule invariant surviving auxiliary definitions, B1, B2, B3, and P versus NP.

The next scientific target is not another finite instance or syntactic padding. It is a growing, genuinely interacting nonaffine family whose excess survives every permitted mixed rule and conservative definition, together with a separately proved B3 bridge for the same preselected calculus.

## Artifacts

- `experiments/arc/lspv5_304/peitl_exact_eight_referee304.py`
- `experiments/arc/lspv5_304/independent_maple_solver_referee304.py`
- `experiments/arc/lspv5_304/positive_control_peitl_nine_referee304.py`
- `experiments/arc/lspv5_304/verify_peitl_exact_eight_referee304.py`
- `results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_raw.json`
- `results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_maple.json`
- `results/raw/arc/2026-11-02_2148_LSPV5_PEITL_NINE_NODE_POSITIVE_REFEREE304.json`
- `results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_verify.json`
- generated DIMACS `results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EIGHT_NODE_ENCODING_REFEREE304.cnf` (hash above; reproducible from the producer)

**END::LSPV5::PEITL-EXACT-EIGHT-REFEREE304::B1-B2-B3-OPEN::P-VS-NP-OPEN**

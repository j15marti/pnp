# REFEREE310: Local truth-table compiler coefficient audit

**PNP Independent Proof Red Team — November 3, 2026, 02:48 PST**

## Classification

- **PROVED/RESTRICTED:** the LSPV-1 LOCAL-TRUTHTABLE-ER2-COMPILER359 factor coefficient improves from 440 to 48 in the same unchanged calculus.
- **PROVED/RESTRICTED:** every implied clause over at most three named variables either has a paid derivation of cost at most 32, or the authenticated input CNF already has a Resolution refutation of cost at most 26 and the global proof can terminate.
- **COMPUTATIONAL/EXHAUSTIVE:** all 256 three-variable Boolean relations and all 1,889 entailed non-tautological clause cases were independently enumerated; canonical complete-blocker CNFs required at most seven ordinary Resolution nodes.
- **OPEN:** global XOR and unrestricted circuit-valued `LOCAL-CONVERT`, the full mixed-system simulation, B1, B2, B3, superpolynomial worst-case minimum derivation cost, and P versus NP.

No task identity, state, schedule, ownership, rule, or weight was changed.

## Fixed calculus and exact obstruction

Keep the preselected source-independent unit-cost `Rmix341`. Let $E$ be its strict binary Resolution plus charged conservative signed two-input `VARDEF` fragment. One fresh gate $q\leftrightarrow(a\wedge b)$ costs one node and exposes the three authenticated slots

$$
(\neg q\vee a),\qquad(\neg q\vee b),\qquad(q\vee\neg a\vee\neg b).
$$

Let $L_3$ be LSPV-1's restricted subsystem adding only explicit Boolean factors and local conversions on a common support of at most three named variables. Names may be original or auxiliary. Global GF(2) rows and unrestricted circuit-valued conversions remain outside this audit.

The concrete question was whether one output factor really needs eight applications of the general 55-node local-implicate compiler, producing the reported coefficient $8\cdot55=440$.

## Falsifiers

1. **F1: every complete output blocker may cost 55.** Falsified. A complete blocker has one falsifying assignment and costs at most six.
2. **F2: 440 is the best coefficient supplied by the reported construction.** Falsified. The same paid weakening construction gives 48.
3. **F3: canonical complete-blocker inputs still need paid weakening.** Falsified. Every required blocker is already an input clause; cube elimination needs at most seven strict Resolution nodes for an arbitrary entailed clause.
4. **F4: the improved constant supplies a full mixed compiler or B3.** Rejected. The global XOR/large-conversion seam is untouched.

These are construction and scope corrections. They are not proof-search lower bounds and do not charge optimizer discovery to $W_R$.

## Six-node complete-blocker lemma

Let $U$ contain $s\le3$ named variables. Let $S$ be an authenticated CNF on $U$, and let $Q$ be an exact output factor logically implied by $S$. For every assignment $\alpha$ that falsifies $Q$, define its complete blocking clause

$$
B_\alpha=\bigvee_{x\in U}
\begin{cases}
\neg x,&\alpha(x)=1,\\
x,&\alpha(x)=0.
\end{cases}
$$

Because $S\models Q$, assignment $\alpha$ cannot satisfy $S$. Hence some authenticated clause $D_\alpha\in S$ is false under $\alpha$. Every literal of $D_\alpha$ is therefore one of the literals of $B_\alpha$, so

$$
D_\alpha\subseteq B_\alpha.
$$

If $D_\alpha$ is empty, the refutation is already complete. Otherwise put $k=|D_\alpha|$ and $r=s-k$. The already legal paid-clause-weakening construction costs

$$
3k+2r-2=k+2s-2.
$$

When $r>0$, $k\le s-1$, and therefore

$$
k+2s-2\le3s-3\le6.
$$

When $r=0$, $D_\alpha=B_\alpha$ is reused at zero additional cost. Thus every complete output blocker costs at most six paid $E$ nodes. An $s$-variable factor has at most $2^s\le8$ false rows, giving

$$
W_E(\text{one local factor translation})\le8\cdot6=48.
$$

Reproducing ordinary `RES` and `VARDEF` nodes one-for-one and replacing each local Boolean-factor node by this construction yields the corrected restricted simulation

$$
W_{L_3}(F)\le W_E(F)\le48W_{L_3}(F)+O(1).
$$

The prior 440 inequality remains true, but it is strictly dominated by this bound. This does not silently add weakening: each widening is an explicit signed-gate and strict-pivot certificate.

## Thirty-two-node general local compiler

There are exactly $3^s\le27$ non-tautological clauses, including the empty clause, on a fixed support of $s\le3$ variables. By the Resolution subsumption theorem, if a satisfiable local CNF $S$ implies a non-tautological clause $C$, ordinary Resolution derives some $D\subseteq C$. Saturating only previously unseen clauses adds at most 26 Resolution nodes. If $D=C$, stop. Otherwise $D$ is nonempty and the same paid weakening construction costs at most six. Hence

$$
S\models C\quad\Longrightarrow\quad
\operatorname{cost}_E(S\vdash C)\le26+6=32
$$

for satisfiable $S$. If $S$ is UNSAT, saturation derives the empty clause within the same 26-node cap and the global refutation terminates; no unsound ex-falso clause insertion is needed.

This strengthens the earlier 55-node bound while preserving its source authentication and auxiliary-name typing firewall.

## Exhaustive finite audit

The standard-library Python producer and a separately authored no-import Node verifier checked:

- all 27 non-tautological clause patterns on three variables, including the empty clause;
- all 56 pairs $(D,\alpha)$ where nonempty clause $D$ is false under assignment $\alpha$;
- a complete signed `VARDEF` and Resolution replay for every one of those 56 paid weakenings;
- all 256 Boolean relations and all 1,889 entailed target-clause cases;
- 255 SAT relations and the unique empty UNSAT relation;
- both parity labels, each with four models;
- 11 malformed encodings and five corrupted proof certificates.

The complete-blocker cost histogram was:

| Paid nodes | Cases |
|---:|---:|
| 0 | 8 |
| 5 | 24 |
| 6 | 24 |

For canonical complete-blocker source CNFs, every required full blocker is already present. Resolving the blocker cube on variables absent from the target gives cost at most

$$
2^{3-|C|}-1\le7.
$$

Both implementations obtained maximum seven across all 1,889 canonical cases. The Node verifier passed 4,114 assertions. Raw SHA-256:

`7ec254731b204e7bbaba33fe4726911588e7db2197f0b2c86d2da16bf10f331e`

Producer wall time was 0.097 seconds with peak host RSS 10,752 KiB. These are implementation measurements, not native FLMV time or writable space. Parsing, source/index access, policy discovery, failed trials, serialization, checking, and all simultaneous allocations remain separate from the ideal inference-node minimum.

## Literature and repository review

Searches performed before the proof audit:

- `resolution implicational completeness derives subclause of entailed clause primary paper theorem`
- `Cook Reckhow propositional proof systems resolution extended resolution 1979 PDF`
- `extended resolution weakening clause proof conservative extension resolution`
- project GitHub: `PAID-CLAUSE-WEAKENING352`, `local truth table compiler weakening resolution subsumption`
- `github.com/openai`: `resolution proof checker clause`

The key classical input is Lee's Resolution subsumption theorem, reviewed through Fermüller's *Implicational Completeness of Signed Resolution* and Nienhuys-Cheng and de Wolf's *The Subsumption Theorem for Several Forms of Resolution*. Cook and Reckhow supply the proof-system and conservative-extension background. The OpenAI GitHub search found only general explanatory material, not a compatible signed proof checker.

- [Fermüller, Implicational Completeness of Signed Resolution](https://www.logic.at/ftp98/papers/fermueller.pdf)
- [Nienhuys-Cheng and de Wolf, The Subsumption Theorem for Several Forms of Resolution](https://repub.eur.nl/pub/514/)
- [Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf)
- [LSPV-1 compiler359](../agents/lspv-1/2026-11-03_0200_LSPV-1_LOCAL_TRUTHTABLE_ER2_COMPILER359.tex)
- [LSPV-2 paid weakening352](../agents/lspv-2/2026-11-02_2312_LSPV-2_PAID_CLAUSE_WEAKENING352.tex)

No novelty is claimed for implicational completeness or conservative extension. The new project contribution is the corrected constant and its independent source-indexed replay in the already fixed calculus.

## Transfer classification and next gap

- **B1:** OPEN. No arbitrary decider-to-proof translation was constructed.
- **B2:** OPEN. No worst-case running-time domination was established.
- **B3:** OPEN. Only the bounded local Boolean fragment was simulated; the same fixed full calculus still contains global XOR and unrestricted conversion rules.
- **Worst-case lower bound:** OPEN. A smaller upper-simulation constant supplies no superpolynomial lower bound.

The next exact obstruction is a paid all-DAG compiler—or a checked counterexample—for global GF(2) rows and circuit-valued `LOCAL-CONVERT`. An accepting/rejecting machine trace still does not authenticate its own correctness. Nonuniform instance-specific axioms, free equivalence tests, and semantic one-step contradictions remain forbidden.

P versus NP remains **OPEN**.

## Reproducibility

- Producer: `experiments/arc/lspv5_310/local_compiler_coefficient_referee310.py`
- Independent verifier: `experiments/arc/lspv5_310/verify_local_compiler_coefficient_referee310.js`
- Raw results: `results/raw/arc/lspv5_310/local_compiler_coefficient_referee310.json`


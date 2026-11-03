# PNP Independent Proof Red Team — PHP32-EXACT-MIXED-REFEREE307

**November 2, 2026, 23:48 PST, America/Los_Angeles.**  
**Task:** `6ad42a2a9a088191ab9042245f3b4393`, PNP Independent Proof Red Team.  
**Status:** **PROVED/EXACT** finite minimum under the already published source-independent zero-premise VARDEF convention of `Rmix341`; **COMPUTATIONAL/EXHAUSTIVE** stronger-relaxation searches, independently reimplemented; **OPEN:** a growing superpolynomial worst-case minimum, B1, B2, B3, and P versus NP.

No task, title, enabled state, schedule, ownership, calculus, or weight was created or changed.

## Exact obstruction and four falsifiers

The exact obstruction is the two-valued gap left by LSPV-4 SOURCE-CYCLE-SLACK353 for canonical pigeonhole `PHP(3,2)`: can a cost-eight source tree, a cost-nine unary tree, or a cost-nine one-cycle binary DAG beat its exhibited ten-node Resolution proof in the same mixed calculus?

1. **F1 — FALSIFIED:** a cost-eight source-read-once mixed tree refutes `PHP(3,2)`.
2. **F2 — FALSIFIED:** one paid LOCAL-CONVERT inside such a tree yields a cost-nine proof. The search grants every implied Boolean relation on any at-most-three-variable subset, including outside-variable weakenings, not merely exact aliases.
3. **F3 — FALSIFIED:** one shared subderivation, hence one undirected proof cycle, yields a cost-nine all-binary proof.
4. **F4 — MODEL-LOCK FINDING:** treating VARDEF as a two-proof-premise inference instead of the previously operative source-independent zero-premise definition is a different calculus. The exact result does not transfer to that unformalized alternative.

## Fixed calculus and source

Use the preselected input-independent unit-weight `Rmix341`: free authentic source clauses; paid binary Resolution; exact `AND3`; binary GF(2) XOR; paid unary LOCAL-CONVERT; and paid conservative source-independent two-input gate VARDEF. In the operative convention explicitly fixed by REFEREE303, a VARDEF is a charged zero-proof-premise definition node whose later authenticated defining slots cite that node. Every distinct paid node costs one and sharing counts once. There is no SAT oracle, formula-tailored axiom, free defining slot, correctness axiom, or semantic jump.

The 76-byte canonical DIMACS source has six variables and nine clauses:

```text
(1 2) (3 4) (5 6)
(-1 -3) (-1 -5) (-3 -5)
(-2 -4) (-2 -6) (-4 -6)
```

It is UNSAT and clause-minimal. Deleting the nine clauses gives model counts

$$
(2,2,2,1,1,1,1,1,1),
$$

and all eighteen single-occurrence sign flips are SAT, with counts six copies of two followed by twelve copies of one.

## Exact topology reduction

For a contradiction ancestry using all `m` indispensable sources, let `q` be paid nodes, `beta` its undirected cycle rank, `u` the number of unary paid nodes, and `d0` the number of zero-proof-premise paid nodes. With all remaining nodes binary, elementary edge accounting gives

$$
q-(m-1)=\beta+u+2d_0.
$$

Here `m=9`. The source-capacity bound first gives `q>=8`. At `q=8`, the only class is a full binary source-read-once tree. At `q=9`, `d0=0` and exactly one of two classes remains:

$$
(\beta,u,d_0)=(0,1,0)\quad\text{or}\quad(1,0,0).
$$

Thus no VARDEF occurs below cost ten in the fixed zero-premise convention. A connected unicyclic acyclic proof has the standard diamond normal form: a source tree for the shared subproof, two source-disjoint exclusive branch trees, one reconvergence, and a source-disjoint tail tree. Empty exclusive branches and parallel reuse of the same shared node are included.

## Stronger-relaxation exhaustive exclusion

Every state is its exact 64-bit truth table. The combiner grants more than the legal calculus:

- every exactly equivalent clause and affine representation is free;
- every legal clause resolvent is available;
- affine rows may be XORed;
- exact conjunction is allowed whenever the **output** has at most three essential variables, even if the inputs jointly mention more;
- in the one-unary class, the single LOCAL-CONVERT may be placed at any source or derived state and may output **every** logically implied Boolean relation over **any** subset of at most three of the six variables, including weakenings that introduce an outside variable.

The last item includes arbitrary bounded-circuit or clause implications and is stronger than an exact representation conversion. Absence of contradiction in this relaxation excludes the actual rule class.

| Exhausted class | operand-pair tests | generated outputs | contradictory terminal |
|---|---:|---:|---:|
| cost-8 binary tree | 8,392 | 1,974 | no |
| cost-9 one-unary tree | 631,592 | 158,170 | no |
| cost-9 binary unicycle | 58,193 reconvergence tests | 15,749 | no |

The unicycle normal-form search made 20,147 memoized branch-extension calls. The combined rule cache had 162,866 misses and 1,892,410 hits. The one-unary terminal bank contained 798 truth functions, none false. Two independent implementations reproduce every count.

## Matching ten-node upper proof

A separately replayed ordinary Resolution DAG derives:

```text
(-1,4), (-1,6), (-1,-6), (-1),
(-2,3), (-2,5), (-2,-5), (-2),
(2), ()
```

with fully indexed parents and pivots in the raw certificate. Hence the exhaustive lower exclusion and explicit upper witness give

$$
\boxed{W_{R_{\mathrm{mix341}}}(\mathrm{PHP}(3,2))=10}
$$

under the fixed source-independent zero-premise VARDEF convention. This is a finite global free-choice minimum, not a claim about the cost of discovering the proof.

## Independent controls and resources

A no-import Node.js verifier independently reconstructs all truth tables, clause/affine aliases, tree and unicycle enumeration, strong unary implications, source labels, deletion and sign-flip models, and the ten-step proof. It passed 31 grouped assertions and exactly matched all enumeration counts.

- both-label parity control: odd-charge `K4` Tseitin has 0 models; even charge has 8;
- nine malformed DIMACS strings were rejected;
- three corrupted proof certificates (pivot, predecessor index, claimed resolvent) were rejected;
- producer raw payload hash: `09c4ec1df6c78cfcc99ed6adbd25fca594846e01279d6d3ac286f458f3970e26`;
- producer: 3.92 seconds, 39,496 KiB peak host RSS;
- independent verifier: 2.93 seconds observed command wall time; `/usr/bin/time` was unavailable, so no verifier RSS is fabricated;
- file sizes: producer 17,024 bytes, verifier 9,759, raw result 3,865, independent result 1,309.

These are host implementation measurements. Parsing, alias generation, failed states, policy selection, caches, JSON materialization, proof replay and independent checking are external scheduled work. None is charged to the ideal ten-node `W_R`. Conversely, the ten-node logical minimum is not a native-machine time or space lower bound. Any recursive space claim still must charge every local phase in

$$
s'\leq\max\{\rho,\eta,\lambda,\lambda s\}.
$$

## Literature and repository audit

The finite result is consistent with, but not supplied by, existing work:

- Kleine Büning, Wojciechowski and Subramani, [On the computational complexity of read once resolution decidability in 2CNF formulas](https://arxiv.org/abs/1610.04523), show that read-once refutability questions remain nontrivial even for 2-CNF and that copy complexity two suffices in that setting.
- Peitl and Szeider, [Finding the Hardest Formulas for Resolution](https://doi.org/10.1613/JAIR.1.12589), study exact shortest Resolution proofs. Their pure-Resolution measurements do not automatically cover the mixed calculus.
- Haken, [The Intractability of Resolution](https://doi.org/10.1016/0304-3975(85)90144-6), proves asymptotic pigeonhole lower bounds for Resolution and notes polynomial Extended Resolution proofs; it gives no lower bound for this mixed system.
- Bryant and Heule, [Generating Extended Resolution Proofs with a BDD-Based SAT Solver](https://doi.org/10.1007/978-3-030-72016-2_5), emphasize explicit checkable defining clauses. It supports authenticating extension syntax rather than treating a definition as a semantic oracle.
- Atserias and Müller, [Automating Resolution is NP-Hard](https://doi.org/10.1145/3409472), concern discovery of near-shortest proofs; optimizer discovery is intentionally excluded from `W_R`.
- Cook and Reckhow, [The Relative Efficiency of Propositional Proof Systems](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf), do not identify this preselected `Rmix341` as polynomially bounded under `SAT in P`.

Logged web queries covered read-once 2-CNF, exact Resolution, PHP lower bounds, Extended Resolution definitions, and automatization. GitHub searches found 48 generic `read-once resolution` hits, 160 generic `PHP(3,2)` hits, and 77 project `VARDEF` hits; the relevant project result was REFEREE303's explicit zero-premise convention. An OpenAI repository search for `resolution` returned 28 unrelated software/image-resolution matches and no reusable proof checker. Negative searches are not novelty evidence.

Corpus reviewed first: the verified 12:04 five-role refocus, current issue #3 and peer updates, original `MIXED-TSEITIN-MIN-DAG341`, LSPV-4 SOURCE-CYCLE-SLACK353, and REFEREE303/306. This run closes the peer's finite `8..10` interval only under the already operative DEF convention; it does not silently redefine the calculus.

## B1/B2/B3 classification

- **B1: OPEN.** No computation-to-proof translation for every total correct SAT decider is given. A single easy 2-SAT instance cannot refute or prove the quantified statement.
- **B2: OPEN.** No comparison is made with any decider's worst-case time over every string of length at most `N`.
- **B3: OPEN.** Nothing here proves `SAT in P => Wbar_Rmix341 polynomial` for the same fixed calculus.
- **Worst-case lower bound: OPEN.** One 608-bit finite instance with excess two does not yield a growing lower bound, much less a superpolynomial one.

The result is a precise finite model audit and candidate-family warning. The next target is a growing nonaffine construction forcing unbounded cycle/slack excess against Resolution, XOR, AND3, LOCAL-CONVERT and authenticated source-independent definitions simultaneously, followed independently by B3. P versus NP remains OPEN.


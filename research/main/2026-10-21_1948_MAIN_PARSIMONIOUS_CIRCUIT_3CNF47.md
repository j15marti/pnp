# PARSIMONIOUS-CIRCUIT-3CNF47

**Timestamp:** 2026-10-21 19:48 Asia/Seoul  
**Scope:** Circuit-SAT comparison inside the existing MKTP and RP work; not a third P-vs-NP route or a sixth role.  
**Global status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Repairs proposed before source review

1. Replace multiplicity-producing 2-clause padding by a **canonical local-relation gadget** whose satisfying rows are exactly the legal gate rows and whose fresh variables are uniquely fixed.
2. In randomized arguments, sample only the original circuit inputs and deterministically construct the gate trace. Never confuse projected accepting-input density with the density of satisfying assignments among all formula variables.
3. Preserve a **source ledger**: circuit source, canonical gadget grouping, variable renaming/permutation metadata, generated formula bytes, gate trace, and auxiliary bits are separate channels. A digest-only lower bound applies only when every other channel is forbidden or charged.

The run then checked the immediately preceding `CIRCUIT-TSEITIN-TRACE-AUDIT46` and `UNIQUE-WITNESS-EXPLICITNESS-FORK45`. No newer complete role report appeared after the 18:48 synthesis; later repository commits were root-review annotations rather than a new role result. The shared Drive fallback remained unchanged at its prior ARC handoff.

## 2. Canonical proper-3-CNF relation gadget

Let $R\subseteq\{0,1\}^q$, where $1\le q\le3$. Add $3-q$ fresh variables and define the uniquely padded relation

\[
E_R=\{(a,0^{3-q}):a\in R\}\subseteq\{0,1\}^3.
\]

For every triple $u\notin E_R$, let $D_u$ be the proper width-three clause that is false exactly on $u$: its $i$-th literal is $v_i$ when $u_i=0$, and $\neg v_i$ when $u_i=1$. Set

\[
\Phi_R=\bigwedge_{u\notin E_R}D_u.
\]

**Lemma 47A (ESTABLISHED).** Every clause of $\Phi_R$ contains three distinct variables, and

\[
\Phi_R(a,b)=1 \quad\Longleftrightarrow\quad a\in R\text{ and }b=0^{3-q}.
\]

Hence each legal interface row has exactly one auxiliary extension and every illegal row has none.

**Proof.** A three-literal clause $D_u$ excludes exactly the row $u$. Conjoining the clauses for all rows outside $E_R$ leaves exactly $E_R$. The padding coordinates in every member of $E_R$ are zero. ∎

Useful exact sizes are:

- AND or OR relation on two distinct inputs and one output: four legal rows, four clauses, no auxiliary;
- NOT or equality relation on one input and one output: two legal rows, six clauses, one uniquely-zero auxiliary;
- output condition $o=1$: one legal row, seven clauses, two uniquely-zero auxiliaries.

Repeated-input gates such as $z=a\land a$ are normalized to equality $z=a$; this avoids repeated variables inside a purported proper clause.

## 3. Circuit composition theorem

Let $C$ have $n$ input variables and $g$ acyclic AND/OR/NOT gates. Give every gate one output variable. Apply Lemma 47A to its local functional relation and finally apply the $o=1$ gadget to the circuit output.

**Theorem 47B (ESTABLISHED; parsimonious projection).** The resulting formula $F_C$ is proper 3-CNF with at most $6g+7$ clauses and at most $n+2g+2$ variables. For every input $x$,

\[
\#\{w:F_C(x,w)=1\}=C(x).
\]

Consequently,

\[
\#SAT(F_C)=|\{x:C(x)=1\}|.
\]

**Proof.** Topologically, each gate output is uniquely fixed by prior wires. Lemma 47A gives exactly one local auxiliary extension for a legal gate row and none for an illegal row. The final gadget admits that unique global trace exactly when the output is one. The size bounds follow from at most six clauses and one auxiliary per gate, plus seven clauses and two auxiliaries for output forcing. ∎

This answers the preceding run's constructive question: **proper 3-CNF can preserve unique gate traces.** The $4^g$ multiplicity in naive 2-to-3-clause padding is an encoding artifact, not an unavoidable feature of proper 3-CNF.

## 4. Why the repair does not prove hardness

### Gate sharing

For

\[
S_0=x,\qquad S_i=(S_{i-1}\land y_i)\lor(S_{i-1}\land\neg y_i),
\]

the circuit has $4d$ gates and the unrolled tree has $2^d$ base occurrences, but $S_d=x$. The new formula preserves one variable for each shared gate and has linear size. It has exactly $2^d$ satisfying assignments—one for each accepting original input—not a hard-to-interpret auxiliary explosion. Forward circuit evaluation still takes $O(d)$.

### Unique witnesses and source access

For the point circuit $P_a$, Theorem 47B creates a proper 3-CNF with exactly one satisfying assignment. But the circuit's literal polarities reveal $a$ directly, and a canonical grouped emission exposes the gate relations. Thus the unique assignment does not imply language hardness. If clauses and variables are scrambled, the permutation and grouping may become a separate information channel; hiding it is a restricted representation assumption and recovering it must be charged.

### RP density

Sampling all variables of $F_C$ uniformly is the wrong simulation: its probability includes guesses for every forced gate and auxiliary bit. The faithful randomized simulation samples $x$, computes the unique trace, and accepts with probability

\[
|\{x:C(x)=1\}|/2^n.
\]

A unique satisfying input therefore still has density $2^{-n}$, not the inverse-polynomial density required for RP. Parsimony supplies no automatic RP membership, derandomization, or separation.

### MKTP and ARC

The conversion is a linear-size, uniformly computable representation map. It supplies no both-label ordinary-KT gap, and a canonical easy circuit family remains source-inspectable after conversion. It is also not an ARC contraction: $O(g)$ clauses replace $g$ gates, with no $n^{1/2}$-scale hereditary successor or simultaneous time-space improvement.

## 5. Computational consistency check

`experiments/review/2026-10-21_parsimonious_circuit_3cnf47_audit.py` exhaustively checked:

- canonical AND, OR, NOT, equality, and output-one gadgets;
- proper width three and three distinct variables in every clause;
- exactly one auxiliary extension for every legal local row;
- shared-DAG identity circuits through depth two;
- repeated-wire AND/OR gates;
- every point circuit through three inputs and all its formula extensions.

Result: **163 assertions over 50,160 assignments, zero failures.** These are finite controls; Lemma 47A and Theorem 47B are the general proofs.

## 6. Proof-status ledger and next discriminating tests

| Role | Status | Model / quantifier / resource boundary | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** **ESTABLISHED:** proper-3-CNF conversion can be parsimonious and linear. | Need a deterministic total both-label KT gap for every source, with target indexing, source reads, generation, output and runtime on one machine. Parsimony alone is satisfiability preservation, not a KT gap. | For one proposed target, identify the first output bit not computable by the canonical circuit/formula evaluator below the actual $p_k$ threshold; test both the point-circuit family and a minimally UNSAT family. |
| :12 P≠RP | **OPEN.** **RETIRED:** unique proper-3-CNF assignment as a language lower bound. | Must exhibit a uniform language in RP outside every deterministic polynomial-time machine. Gate inspection and canonical gadget recognition remain deterministic bypasses for the audited families. | For each Circuit-SAT candidate, compute projected accepting-input density and run the canonical-gadget/source-inspection bypass before considering any verifier obstruction. |
| :24 ARC/FLMV | **OPEN.** | Linear equisatisfiable conversion is all-input but not a hereditary contraction. Shared gate variables create boundary-consistency obligations under any attempted partition. | Partition one parsimonious formula across a high-fanout shared gate; exhibit the exact boundary state needed to glue children, then charge its serialization and peak workspace. |
| :36 P=RP | **OPEN.** **RETIRED:** low clause width or unique trace implies low acceptance-polynomial degree. | A uniform deterministic simulation of every RP machine is required. The known $R_n$ family retains degree $n+1$ despite local width-three constraints and unique traces. | Convert $R_n$ with Theorem 47B and symbolically eliminate gate variables; verify that the projected acceptance function and its high ANF degree are unchanged. |
| :48 synthesis | **ESTABLISHED:** Lemmas 47A and 47B. **OPEN:** both class questions. | Mixed-width Tseitin, naive padded 3-CNF, and parsimonious proper 3-CNF are three different witness maps. Source/grouping access and random sampling domain must be explicit. | Randomly permute clauses and variable names in the canonical image and measure which reconstruction claims require hidden grouping metadata; do not promote finite reconstruction cost to a lower bound. |

## 7. Source and publication audit

- Immediate predecessor: [`CIRCUIT-TSEITIN-TRACE-AUDIT46`](https://github.com/j15marti/pnp/blob/26d53b8930c1ac6ffb1c34257865c990ab2c9a3a/research/main/2026-10-21_1848_CIRCUIT_TSEITIN_TRACE_AUDIT46.md).
- Unique-witness firewall: [`UNIQUE-WITNESS-EXPLICITNESS-FORK45`](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-21_1748_MAIN_UNIQUE_WITNESS_EXPLICITNESS_FORK45.md).
- Shared Drive fallback was readable and unchanged; its last substantive entry remained the earlier scoped ARC handoff.

No circuit, 3-CNF gadget, unique witness, digest bound, randomized verifier, selected solver, finite computation, or conditional recurrence is claimed to separate complexity classes. Root manuscripts and role assignments were untouched.

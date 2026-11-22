# T5. Three fresh unknowns: shortest source obstructions and evidence cost

Date: 2026-11-22.

## 1. Results and status

For the strict symmetric five-value relation defined below, the maximum size of a minimum source obstruction with three unknown values is exactly

\[
H_3=5.
\]

The universal upper bound of five is a **complete finite, computer-assisted classification**. Two separately written programs enumerate all minimal obstructions of the exact 46-atom residual language. The Python program additionally checks every reported obstruction and every single-row deletion directly on all 125 assignments. The classification contains 5,635 minimal obstructions, of which 285 have size five. No claim is made that a short symbolic proof of the universal upper bound has been found.

The lower bound of five has a short symbolic proof. An explicit globally UNSAT source with eight variables and ten constraints also has the independent erasure profile

\[
(\mu_0,\mu_1,\mu_2,\mu_3)=(1,2,4,5).
\]

The four entries concern four fresh inputs. They do not describe a solver retaining work while values are removed.

The exact conjunction closure of the three-unknown residual language has 3,403 supports. It therefore requires and admits 12 fixed bits under the specific contract of an exact, source-free summary that must answer every later compatible context. This is a contextual information statement, not a lower bound on the time needed to answer the single decision question.

## 2. Relation, source convention, and quantity measured

Let \(D=\{0,1,2,3,4\}\). Define \(C(u,v,w)\) to hold exactly when the unordered set of its three values is one of

\[
\{0,1,2\},\quad\{1,2,3\},\quad\{2,3,4\},\quad
\{3,4,0\},\quad\{4,0,1\}.
\]

All permutations of these triples are accepted. Repeated values are rejected. Source constraints use three distinct variable names. This is the project's strict symmetric relation, not an ordered tournament relation.

A fresh input supplies a source conjunction \(F\) and a partial assignment \(\alpha\), leaving exactly \(r\) variable values unspecified. The source rows and the supplied values jointly determine residual relations \(R_i\subseteq D^r\). For an UNSAT residual input define

\[
\mu(F,\alpha)=
\min\left\{|J|:\bigcap_{i\in J}R_i=\varnothing\right\}.
\]

Thus the supplied values are background information, and \(\mu\) counts source constraints. It does not count bytes, source positions, deductions, CPU instructions, or proof-verification steps. A minimum core has smallest cardinality. A minimal core is UNSAT but loses UNSAT when any row is deleted. These are distinct notions, as in the standard definitions of Lynce and Marques-Silva [1].

Let \(H_r\) be the maximum possible \(\mu\) for this residual language. To establish \(H_r\), it suffices to enumerate all inclusion-minimal cores. Every UNSAT source contains such a core, and a minimal core itself has no smaller UNSAT subset. Repeated residual rows can be discarded. A true constant row can be discarded. A false constant row already gives \(\mu=1\).

## 3. Exact three-unknown residual language

Let the unknown slots be \(x,y,z\). After the supplied values are substituted, every nonconstant source row has one of three forms.

| Number of unknown slots in the row | Form | Distinct nonempty residual atoms |
|---|---|---:|
| One | \(C(x_i,a,b)\) | Ten unary supports per slot, 30 total |
| Two | \(C(x_i,x_j,a)\) | Five relations per unordered slot pair, 15 total |
| Three | \(C(x,y,z)\) | One relation |
| Total | | **46** |

The ten unary supports are the five singletons and the five doubletons

\[
\{0,2\},\quad\{0,3\},\quad\{1,3\},\quad\{1,4\},\quad\{2,4\}.
\]

They are derived by trying the ten unordered pairs of distinct supplied values. If the two supplied values agree, the residual is empty and has already been handled as a singleton obstruction. The tuple universe is exactly \(D^3\), containing 125 tuples. There are no hidden auxiliary unknowns in this classification.

Every listed atom is realizable by an ordinary source row with distinct variable names. For example, use five supplied anchor names with respective values 0 through 4. This also makes all conjunctions in the finite language realizable by literal source conjunctions.

## 4. Why the enumeration is complete

For a selected set \(J\) of residual rows, maintain its common support

\[
S(J)=\bigcap_{i\in J}R_i
\]

and each row's private witness set

\[
P_i(J)=
\left(\bigcap_{j\in J\setminus\{i\}}R_j\right)\setminus R_i.
\]

The condition \(P_i(J)\ne\varnothing\) says that row \(i\) excludes at least one tuple that all the other selected rows permit. On adjoining a new row \(R\), the updates are exactly

\[
S(J\cup\{R\})=S(J)\cap R,
\]

\[
P_R(J\cup\{R\})=S(J)\setminus R,
\]

\[
P_i(J\cup\{R\})=P_i(J)\cap R\quad(i\in J).
\]

These formulas justify the pruning rule. If any private set is empty, its row is redundant. Adding more conjuncts can only shrink the private set, so the row can never become essential again. No extension containing that row can be a minimal UNSAT core.

Conversely, every prefix of a minimal UNSAT core has nonempty private sets: a full-core deletion witness for a row remains a witness when other rows are removed. Consequently, depth-first search over increasing atom indices, rejecting exactly the extensions with an empty private set, reaches every minimal UNSAT core once. When the common support first becomes empty and all private sets remain nonempty, the selected set is exactly a minimal UNSAT core. Once UNSAT is reached, no strict superset can be minimal.

No maximum core size is assumed by the search. All 46 possible first-row roots were completed. The code searches irredundant prefixes, rather than trying all \(2^{46}\) subsets.

The C++ implementation uses 125 bits inside an unsigned 128-bit integer. Its relation predicate constructs the five allowed cyclic triple masks. The independent Python implementation uses arbitrary-precision integer masks and a separately constructed set of sorted allowed triples. After enumeration, Python rechecks every core and every deletion using direct tuple membership, without using the private-set invariant for those checks.

## 5. Complete finite classification

| Core cardinality | Number of minimal cores | Number containing the ternary atom |
|---:|---:|---:|
| 2 | 135 | 0 |
| 3 | 950 | 75 |
| 4 | 4,265 | 875 |
| 5 | 285 | 165 |
| Total | **5,635** | **1,115** |

There are no larger minimal cores. The satisfiable irredundant-prefix counts, including the empty prefix, are

| Prefix size | Count |
|---:|---:|
| 0 | 1 |
| 1 | 46 |
| 2 | 870 |
| 3 | 7,240 |
| 4 | 9,750 |
| 5 | 3,810 |
| 6 | 635 |

No satisfiable irredundant prefix of size seven exists. Prefixes are counted as sets of residual atoms, with a unique increasing-index traversal.

The 285 size-five minimal cores break down as follows.

| Unary rows | Binary rows | Ternary rows | Number |
|---:|---:|---:|---:|
| 2 | 3 | 0 | 120 |
| 2 | 2 | 1 | 30 |
| 3 | 1 | 1 | 120 |
| 4 | 0 | 1 | 15 |

In particular, the increase from four to five does not require a row containing all three unknowns. The explicit witness below uses only unary and binary residual rows.

## 6. A symbolic sharp witness

With supplied values 0 through 4 available as anchors, consider these five source residuals:

\[
\begin{aligned}
A&: C(x,1,4),\\
B&: C(y,3,4),\\
D&: C(x,y,1),\\
E&: C(y,z,1),\\
F&: C(y,z,3).
\end{aligned}
\]

They are UNSAT for the following reason. Row \(A\) forces \(x=0\). Row \(D\) then forces \(y\in\{2,4\}\), while \(B\) forces \(y\in\{0,2\}\). Together these force \(y=2\). However, the simultaneous allowed pairs of \(E\) and \(F\) are precisely

\[
(y,z)\in\{(0,4),(4,0)\},
\]

which excludes \(y=2\).

Each row is essential. The following complete assignments satisfy all four other rows.

| Deleted row | \(x\) | \(y\) | \(z\) |
|---|---:|---:|---:|
| \(A\) | 2 | 0 | 4 |
| \(B\) | 0 | 4 | 0 |
| \(D\) | 0 | 0 | 4 |
| \(E\) | 0 | 2 | 1 |
| \(F\) | 0 | 2 | 0 |

Every proper subset omits at least one row, and that row's deletion witness also satisfies the subset. Therefore all five rows are needed, establishing the symbolic lower bound \(H_3\ge5\). The complete finite classification supplies \(H_3\le5\).

This argument combines evidence through shared restrictions. It does not count the 125 tuples. It exhibits one short sound derivation, without asserting that these displayed deductions are mandatory steps for every solver.

## 7. Globally UNSAT source and independent erasure profile

Introduce distinct variables \(a_0,\ldots,a_4,x,y,z\). First impose the five anchor rows

\[
C(a_i,a_{i+1},a_{i+2})\qquad(i\in\mathbb Z/5\mathbb Z).
\]

Every pair of anchor names occurs together in at least one of these rows. Thus all five anchors have distinct values and form a permutation of \(D\). That permutation preserves the five allowed triples. Their complements are exactly the edges of the five-cycle, so the permutation is a dihedral symmetry of the five-cycle. These are the ten possible anchor frames.

Add the five rows

\[
\begin{aligned}
A&: C(x,a_1,a_4),\\
B&: C(y,a_3,a_4),\\
D&: C(x,y,a_1),\\
E&: C(y,z,a_1),\\
F&: C(y,z,a_3).
\end{aligned}
\]

Applying the inverse anchor symmetry converts any possible satisfying assignment to the identity frame. In that frame, the five-row contradiction of the previous section applies. Hence the original source, before any values are supplied, is globally UNSAT.

Use the reference assignment

\[
(a_0,a_1,a_2,a_3,a_4,x,y,z)=(0,1,2,3,4,0,2,0).
\]

Exactly row \(F\) is false at this reference. For each level below, create a fresh input from the source and the indicated supplied values.

| Fresh level | Unspecified values | Minimum core | Exact size |
|---:|---|---|---:|
| 0 | None | \(F\) | 1 |
| 1 | \(z\) | \(E,F\) | 2 |
| 2 | \(y,z\) | \(B,D,E,F\) | 4 |
| 3 | \(x,y,z\) | \(A,B,D,E,F\) | 5 |

At level one, row \(E\) permits \(z\in\{0,3\}\), whereas \(F\) permits \(z\in\{1,4\}\). Each row alone is satisfiable, and their intersection is empty.

At level two, \(x=0\) remains supplied. The four rows \(B,D,E,F\) are UNSAT by the previous derivation. Their deletion witnesses for \((y,z)\), respectively, are \((4,0),(0,4),(2,1),(2,0)\). All remaining source rows are true constants under the supplied values. Thus no source subset of size three is already UNSAT.

At level three, the five deletion witnesses in the preceding table apply. Again, all anchor rows are true constants under the supplied values.

The Python audit also checks all \(5^8=390{,}625\) complete assignments to this source and finds zero models. It checks the unique failed reference row and directly enumerates source subsets to confirm all four minimum-core sizes. The symbolic arguments establish the profile independently of that brute-force verification.

### Exact combination across a removed value

There is a useful general identity that keeps shared evidence visible. Let \(\mathcal M\) be the family of inclusion-minimal source cores at a parent level, and let \(\mathcal M_v\) be that family in the slice where one of its unknowns is supplied with value \(v\in D\). All families use the same source-row identifiers. For an UNSAT parent,

\[
\mathcal M=
\operatorname{Min}_{\subseteq}
\left\{\bigcup_{v\in D} K_v:
K_v\in\mathcal M_v\text{ for every }v\right\}.
\]

Here \(\operatorname{Min}_{\subseteq}\) retains the inclusion-minimal members. A union on the right is UNSAT because its rows refute every slice. Conversely, if \(K\) is a minimal parent core, each slice has a minimal core \(K_v\subseteq K\). Their union is a parent core contained in \(K\), so parent minimality forces equality. This proves both inclusions, after removing any nonminimal unions. In particular,

\[
\mu_{\mathrm{parent}}=
\min_{K_v\in\mathcal M_v\;(v\in D)}
\left|\bigcup_{v\in D}K_v\right|.
\]

The minimizing choice may use a slice core larger than that slice's minimum-cardinality core if it overlaps better with the other choices. Retaining only each slice's minimum size therefore loses information needed for the exact parent recurrence.

For this source, split the three-unknown level according to \(x\). In the \(x=0\) slice, the minimal core is \(\{B,D,E,F\}\). In each of the four other slices, \(\{A\}\) is a singleton core. Their shared union is precisely \(\{A,B,D,E,F\}\), of size five. Summing the five individual minimum sizes instead would give eight. The union identity is semantic and does not prescribe a branch-by-branch algorithm or require its costs to be added.

### Literal encoding length

Under the project's canonical source convention

\[
1^n0\;\gamma(m+1)\;\text{the }m\text{ triples},
\qquad w=\lceil\log_2(n+1)\rceil,
\]

the source has \(n=8\), \(m=10\), and \(w=4\). Its length is

\[
(8+1)+|\gamma(11)|+3\cdot10\cdot4
=9+7+120=136\text{ bits}.
\]

A canonical three-bit value-or-unknown entry for each of the eight variables contributes another 24 bits. With codes 0 through 4 for values, code 5 for unknown, and codes 6 and 7 invalid, each of the four fresh inputs has exactly **160 bits** under this convention. This uses an ordinary literal source encoding, with no compact program hidden in an auxiliary representation.

## 8. Exact source-free contextual information

Starting from \(D^3\), repeatedly intersecting with each of the 46 atomic relations produces the entire realizable support family \(\mathcal S_3\). The completed closure has

\[
|\mathcal S_3|=3403.
\]

Its support-cardinality histogram is

| Support cardinality | Number of supports |
|---:|---:|
| 0 | 1 |
| 1 | 125 |
| 2 | 645 |
| 3 | 330 |
| 4 | 810 |
| 5 | 285 |
| 6 | 345 |
| 7 | 30 |
| 8 | 350 |
| 10 | 210 |
| 12 | 90 |
| 15 | 30 |
| 20 | 105 |
| 25 | 15 |
| 30 | 16 |
| 50 | 15 |
| 125 | 1 |

To interpret this count as distinguishable information, specify the contract. A summary is constructed from an arbitrary source over these three known slots; after construction, the original source is unavailable. Given the summary and any additional permitted conjunctive context on these slots, a decoder must decide satisfiability exactly. Slot identities, value labels, the fixed template, and the decoder are shared background.

Two distinct supports \(S,T\) differ on some tuple \(t\). A permitted context can pin each slot to its coordinate in \(t\). For value \(c\), the source row

\[
C(x_i,a_{c-1},a_{c+1})
\]

with the anchor values supplied and subscripts modulo five permits exactly \(x_i=c\). The conjunction of these three rows has support \(\{t\}\). Hence

\[
S\cap\{t\}\ne\varnothing
\quad\Longleftrightarrow\quad t\in S,
\]

and similarly for \(T\). The same context therefore gives different answers for \(S\) and \(T\). They cannot share a summary state under the stated contract. Conversely, knowing the support suffices to answer every such context by intersection. The 3,403 supports are thus exactly 3,403 contextual equivalence classes.

The exact fixed-bit requirement is consequently

\[
\lceil\log_2 3403\rceil=12.
\]

An enumeration index proves 12-bit sufficiency; the distinguishing contexts prove necessity. Previous fresh-level classifications gave 12 supports at one unknown and 157 at two unknowns, yielding 4 and 8 fixed bits under the same contract. The observed sequence \(4,8,12\) does not establish a general \(4r\) theorem.

This contextual result does not require a decision algorithm to preserve all support information when it only needs to answer the current SAT/UNSAT question. That output is one bit. It also excludes retaining and rereading the original source, so it is not an unconditional machine-space bound. The support count does not charge the construction or decoding time of the summary.

## 9. What this contributes to a fully charged cost analysis

There are two measurements to retain simultaneously.

First, \(\mu(F,\alpha)\) gives the smallest number of source rows whose conjunction with the supplied values is already incompatible. The classification proves that this measure grows from four to five between two and three unknown values in this template, and the explicit source realizes that growth along the requested fresh erasure levels.

Second, the cost of recognizing an obstruction depends on how its evidence is acquired, represented, combined, and checked. A minimum-cardinality core need not be the cheapest core to discover or establish. A larger core may have an easier recognition pattern, better source locations, or a much shorter derivation under the charged model. Any optimum-cost definition must therefore range over all sound evidence combinations, including larger cores and shared deductions, rather than first requiring the solver to find a minimum core.

For the five-row witness, the displayed argument gives an available path: derive \(x=0\), combine two restrictions to derive \(y=2\), combine \(E\) and \(F\) to derive \(y\in\{0,4\}\), and recognize incompatibility. A table-driven implementation could combine these same facts in another order, or process them through a precomputed exact state transition. The mathematics does not force these particular local steps.

Under an ordinary query contract where unobserved source records can still be replaced independently by satisfiable alternatives, the deletion witnesses explain why all five critical records must have been accounted for in a correct certificate for this target. This claim requires the both-label input contract and the stated access model. It does not imply five further steps after preprocessing has already accounted for those records. If a charged representation already stores a sound UNSAT flag, outputting that flag can be the whole remaining task.

For a fixed number of three unknowns, the semantic state space is finite. A fixed lookup table can recognize the incompatibility of the residual relation types once the relevant types have been acquired. The finite classification therefore supplies no intrinsic superpolynomial inference cost at this level. Any further lower bound must identify cost that remains unavoidable for every allowed representation and inference method as the number of unknowns grows, counting preprocessing and shared work exactly once.

## 10. Reproducibility and recorded executions

All files for this note are in the same directory.

| File | Role |
|---|---|
| `c5_r3_core_enumeration.cpp` | C++17 exhaustive minimal-core enumerator |
| `c5_r3_core_results.json` | Completed C++ run, roots 0 through 45 |
| `c5_r3_audit.py` | Standalone independent Python audit, standard library only |
| `c5_r3_template_audit.json` | Completed Python enumeration, direct core/deletion checks, and support closure |
| `c5_r3_source_audit.json` | Completed exhaustive global-source and fresh-level audit |

Recorded C++ enumeration time: 0.00359138 seconds. Recorded Python template time: 0.8533935460000066 seconds. Recorded Python source-audit time: 0.44344172299861384 seconds. These are execution observations, not algorithmic lower bounds. Both Python stages completed under their 30-second process limits. The C++ run reports `complete: true`, `first_root: 0`, `last_root_exclusive: 46`, and `completed_through_root: 45`.

The canonical sorted list of minimal cores, encoded as comma-separated atom indices with newline-separated cores, has SHA-256

```text
fe83300615cde7bc6745ec1057088c0e056132dd895b35ebdc75a81323572ae4
```

The following commands reproduce the principal audits from this directory.

```bash
g++ -std=c++17 -O3 c5_r3_core_enumeration.cpp -o c5_r3_core_enumeration
./c5_r3_core_enumeration > c5_r3_core_results.json
timeout 30s python c5_r3_audit.py --stage template > c5_r3_template_audit.json
timeout 30s python c5_r3_audit.py --stage source > c5_r3_source_audit.json
```

The exhaustive finite upper bound is supported by the proved search-coverage invariant, two implementations, and the complete recorded executions. It has not been translated into a formally verified proof-assistant artifact.

## Reference

[1] Inês Lynce and João Marques-Silva. *On Computing Minimum Unsatisfiable Cores*. SAT 2004. Definitions 2 and 3 distinguish minimum cardinality from inclusion minimality. Primary author paper: <https://www.satisfiability.org/SAT04/programme/110.pdf>. Accessed 2026-11-22. This reference supplies terminology only; the C5 results above are the new finite analysis recorded in the accompanying files.

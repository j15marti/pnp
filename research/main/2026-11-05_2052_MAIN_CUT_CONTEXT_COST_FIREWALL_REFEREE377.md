# REFEREE377: exact parity-context cover and the native-wide-row cost firewall

**November 5, 2026, 20:52 PST. LSPV-5 Independent Proof Red Team, Route B.**

**Status.** **PROVED/EXACT, RESTRICTED:** if a proposed split-to-localize protocol must cover all assignments to a $k$-wire parity boundary by subcube contexts leaving at most three wires free, its exact minimum number of leaf contexts is $2^{k-3}$. **PROVED/EXACT cost firewall:** that leaf count is not a lower bound on historical $R_{\mathrm{mix341}}$ work. The native XOR rule combines two already-derived opposite $k$-wide rows into $0=1$ in one paid node, using no branch contexts; on the source-authenticated odd $K_4$ control the complete established mixed proof still costs exactly 15 nodes. **COMPUTATIONAL:** 33,811 producer checks, 8,303 independent checks, and exact replay of LSPV-3/438's published compact 1,356-check program. Historical accepted-byte syntax, full-rule normalization, superpolynomial mixed $\overline W_R$, B3, and P versus NP remain **OPEN**.

## IDEA -> SEARCH -> ITERATE

### Initial idea and falsifiers

The first hypothesis was that a polynomial rejecting computation trace cannot by itself be compiled into a sound $R_{\mathrm{mix341}}$ proof. Four falsifiers were stated before search: (1) a native trace/reflection rule already exists; (2) source authentication excludes the adversarial even-charge source; (3) LSPV-1/3 supply a noncircular soundness proof; or (4) the objection attacks only an artificial trace-blind compiler. Project search then found that this was already the substance of REFEREE363. It was abandoned as a duplicate.

The revised hypothesis targets LSPV-3/438: the $2^{k-3}$ context bound is exact in the separately proposed split-to-localize model, but any unqualified promotion to full mixed-calculus work is false because the historical GF(2) rule can retain and combine wide rows without branching. Precise falsifiers were:

1. the original strict-3 source does not project exactly to opposite parity rows on the same cut;
2. fewer than $2^{k-3}$ valid local contexts cover all $2^k$ boundary assignments;
3. the historical XOR rule forbids wide rows or requires a branch context;
4. the claimed native shortcut omits the work needed to derive its two antecedent rows.

Falsifiers 1--3 were rejected. Falsifier 4 is real and determines the scope: the final XOR costs one, but the full odd-$K_4$ native proof costs 15, not one.

### Continuity and source review

Read the governing five-role refocus at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3 through LSPV-4/429, LSPV-1/433, LSPV-3/438 report/code/raw/handoff, historical `/341` native-rule theorem, actual `GROKPROOF/2026-11-06_0415_PROGRESS.md`, and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`. LSPV-1/433's legal Horn Resolution shortcut and LSPV-4/429's authenticated autarky port reinforce the same red-team rule: a restricted optimizer or branch count cannot be imported after ignoring a native shortcut.

Primary sources actually inspected:

- Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), pp. 209--219: an infinite linear-size Tseitin graph family needs exponentially many steps in unrestricted Resolution; the paper also states a width-three variant. This is a Resolution theorem, not full mixed-calculus or machine hardness.
- Ben-Sasson--Wigderson, *Short Proofs Are Narrow--Resolution Made Simple*, JACM 48 (2001), pp. 149--169: width-to-size relations for general and tree-like Resolution and expansion-based applications.
- Kothari--Racicot-Desloges--Santha, *Separating Decision Tree Complexity from Subcube Partition Complexity*, RANDOM 2015: subcube partitions are a distinct computation model, so decision-tree or partition cost must not be silently identified with native proof work.
- Glinskih--Itsykson, *On Tseitin Formulas, Read-Once Branching Programs and Treewidth*, Theory of Computing Systems 65 (2021): lower bounds are for nondeterministic read-once branching programs and OBDD-derived systems under stated graph parameters, not arbitrary branching/shared $R_{\mathrm{mix341}}$ proofs.

Indexed queries included `primary paper parity function certificate complexity decision tree subcube cover lower bound`, `Tseitin formulas branching programs resolution parity cuts proof complexity`, and `Ben-Sasson Wigderson Tseitin parity width resolution PDF 2001`. A direct Google-branded interface was unavailable; indexed web search was used and no direct Google access is claimed.

Change-aware GitHub review found unchanged heads for `konard/p-vs-np` (`ecedd2b45f1c524d85c00b2da27a9c140025550c`), `blkph0x/p-vs-np-proof-research` (`7dedc73f758dfbdc072e7aa29dfc08505761ebd5`), `meelgroup/frat-xor` (`18cd6bc17af10a9891c10a846ce966166f9fe0dc`), and `openai/math` (`4eaee87548250b2682affda7d05d947c05554bae`). Actual files inspected were `proofs/complexity/README.md`, `RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md`, `format.md`, and `lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`. They supply explicit machine-cost, residual-equivalence, proof-format, and same-execution accounting precedents. None contains a same-historical-$R_{\mathrm{mix341}}$ branch-context transfer or B3 theorem.

## Established family and exact encoding

Let $G=(V,E)$ be a connected simple cubic graph and let $\chi\in\{0,1\}^V$ have odd total parity. Put one Boolean variable $x_e$ on every edge. At vertex $v$ with incident edges $e_1,e_2,e_3$, impose

$$
x_{e_1}\oplus x_{e_2}\oplus x_{e_3}=\chi_v
$$

by the four proper width-three clauses that forbid exactly the four assignments of parity $1\oplus\chi_v$. For $h=|V|$, the source has $3h/2$ variables and $4h$ strict width-three clauses. Under ordinary binary DIMACS with numerical identifiers its byte length is $\Theta(h\log(h+2))$.

For suitable cubic expanders, Urquhart's theorem gives $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution length. This is the established hard-family starting point. Historical `/341`, however, permits three source-authenticated AND3 nodes per vertex to recover its local row and $h-1$ XOR nodes to sum all rows. It proves the exact global mixed optimum

$$
W_{R_{\mathrm{mix341}}}(F_{G,\chi})=4h-1.
$$

Thus this family is a mandatory transfer falsifier: established Resolution hardness coexists with a linear full-mixed proof.

### The finite $K_4$ source-bound cut

Use edge order $(01,02,03,12,13,23)$, charge vertex 0 by one, and all others by zero. The exact DIMACS source has six variables, sixteen proper strict-3 clauses, and 163 bytes. Its SHA-256 is `ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096`. Exhaustive replay finds no model. The even-charge counterpart has SHA-256 `d2947ac9567bd6ed42c5557f2abaccfc69b745b1cdfe29ee7ad761761ea73273` and exactly eight models.

Take $S=\{0,1\}$ and $\bar S=\{2,3\}$. Both sides are connected and their common cut is

$$
\delta(S)=\{02,03,12,13\},\qquad k=4.
$$

Existentially eliminating the internal edge $01$ from the eight source clauses on $S$ gives exactly the odd parity row on these four cut wires. Eliminating internal edge $23$ from the complement gives exactly the even row. The producer exhaustively checked all 16 boundary assignments and both internal completions on each side. These are semantic source-bound checks, not execution of the authoritative historical byte parser.

## Exact restricted context theorem

### Theorem 377.1 (parity subcube cover)

Fix $k\ge3$. Suppose every leaf context is a subcube that fixes at least $k-3$ of the $k$ boundary coordinates, so that at most three coordinates remain free, and the AND obligation requires the union of leaf contexts to cover all $2^k$ complete boundary assignments. Then the exact minimum number of distinct leaf contexts is

$$
L_k=2^{k-3}.
$$

**Proof.** Each allowed context covers at most $2^3=8$ complete assignments. Covering $2^k$ assignments therefore requires at least $2^k/8=2^{k-3}$ contexts, even if overlaps are allowed. Equality is attained by fixing any predetermined $k-3$ coordinates in all possible ways and leaving the other three free. These $2^{k-3}$ subcubes are disjoint and partition the full cube. QED.

For a parity row, before $k-3$ pins every projection onto at most three unpinned coordinates is the full Boolean cube: choose another unpinned coordinate to repair total parity. At exactly $k-3$ pins, the remaining three-wire parity is nontrivial. This proves the locality threshold used by LSPV-3/438.

The theorem is about a **proposed split-to-localize calculus**. It is not yet a theorem about historical proof bytes, and it is not a $W_R$ lower bound unless the calculus explicitly assigns positive cost to the distinct contexts and/or leaf closures.

### Theorem 377.2 (native-wide-row cost firewall)

In historical `/341`, XOR takes any two GF(2) equations and infers their XOR sum, including $0=1$. Hence, once the two source-authenticated cut rows

$$
\bigoplus_{e\in\delta(S)}x_e=0,
\qquad
\bigoplus_{e\in\delta(S)}x_e=1
$$

have been derived, one paid XOR node gives $0=1$. It uses zero split contexts. Therefore no positive $2^{k-3}$ branch-context count can be promoted, without an additional simulation theorem, to a lower bound on unrestricted historical $R_{\mathrm{mix341}}$ work.

This theorem does **not** make the complete proof cost one. For odd $K_4$, `/341` derives all four vertex rows with 12 AND3 nodes and combines them with three XOR nodes, so the established optimum remains 15. The one-node statement refers only to the final combination of two already-derived opposite cut rows.

The $k=4$ instance is the smallest clean countercontrol in this run:

| Quantity | Split-to-localize model | Historical mixed proof |
| --- | ---: | ---: |
| Boundary width | 4 | 4 |
| Required branch contexts | exactly 2 | 0 |
| Final contradiction from two opposite rows | not a native premise of the model | 1 XOR node |
| Complete source-bound proof | rule/weights not historically declared | exactly 15 nodes |

## AND/OR sharing, work, span, and realizable space

The lower-bound relaxation chooses the optimal legal DAG after the fact. OR means choose one complete legal derivation; it does not charge unsuccessful alternatives. A split is an AND obligation: both child contexts must close unless another proof avoids the split. A lemma labelled $\Gamma\vdash C$ can be reused only where $\Gamma$ is justified; conclusions depending on $x$ cannot leak into a $\neg x$ branch. Shared unconditional nodes are counted once.

For the canonical restricted cover with $L=2^{k-3}$ leaves:

- **context count:** exactly $L$;
- **proposed tree work if every split/context node has unit weight:** $L-1$ internal split nodes and $L$ leaves, hence $2L-1$ nodes before any leaf-closure work; this is not a historical weight assignment;
- **parallel span:** $k-3$ split decisions plus the span of one leaf closure, so exponential leaf work can coexist with $O(k)$ span;
- **materialized context storage:** $L(k-3)$ fixed-bit records for all leaves, up to representation constants;
- **depth-first live context:** $O(k)$ fixed bits plus the live leaf proof, at the cost of sequential work and any required recomputation;
- **historical native control:** wide-row derivations can reconverge without branch contexts. Their antecedent work remains charged once under the existing DAG weights.

If contexts, assumption labels, or leaf closures are free, context cardinality alone implies no positive $W_R$ bound. Conversely, actual algorithmic upper bounds must charge parsing, source lookup, branch construction, failed searches, references, retention/retrieval, recomputation, output, and peak simultaneous storage. Logical node work, critical path, and a realizable time/space schedule are distinct quantities.

## Family/theorem/encoding/shortcut/transfer ledger

| Family | Exact 3-CNF and size parameter | Established theorem/model | Known method or shortcut | Remaining transfer |
| --- | --- | --- | --- | --- |
| Cubic-expander odd Tseitin | Edge variables; four signed proper width-three blockers per vertex; $3h/2$ variables, $4h$ clauses, $N=\Theta(h\log h)$ bits. | Urquhart 1987: $2^{\Omega(h)}$ length in unrestricted ordinary Resolution on an expander sequence; Ben-Sasson--Wigderson supplies width/size machinery. | Historical AND3/GF(2) proof is exactly $4h-1$ nodes; balanced row summation and sharing are legal upper controls. | Need an invariant surviving **all** RES/AND3/XOR/LOCAL/DEF proofs. Current family fails as a mixed lower-bound witness. |
| Odd $K_4$ Tseitin | Six edge variables, sixteen strict-3 clauses, 163 authenticated bytes. | Finite UNSAT and exact historical mixed optimum 15; no asymptotic hardness claim. | Two connected sides export opposite four-wide rows; final native XOR closes in one node after antecedent derivation. | Authoritative accepted-byte replay and exact exporter grammar remain unavailable. |
| Haken PHP | Standard PHP CNF is not proper strict 3-CNF. | Exponential ordinary Resolution lower bound. | Cook Extended Resolution is the mandatory strong shortcut control. | No lower-bound-preserving strict-3 transformation into full mixed calculus has been proved; equisatisfiability is insufficient. |
| Tseitin read-once/OBDD systems | Tseitin sources under graph/treewidth conditions in Glinskih--Itsykson. | Exponential lower bounds in nondeterministic read-once branching programs and OBDD-derived systems. | General DAG, algebraic, extension-variable, and reconvergent proofs are outside those restrictions. | No simulation from full historical mixed proofs to those restricted models. |

Certified UNSAT, established proof-size hardness in a named system, and empirical solver difficulty are not interchangeable. This run uses no empirical runtime as a proof lower bound.

## Reproducibility, malformed/corrupt controls, and ledgers

The independent producer regenerated exact odd/even $K_4$ sources, exhaustively evaluated all 64 assignments, verified both four-wire cut projections, proved the $k=3,\ldots,12$ canonical covers, checked the general volume bound, and tested opposite/same GF(2) rows. It rejected a bad header and an out-of-range literal.

- Producer: 33,811 assertions; 22.58 host seconds; Python `tracemalloc` peak 3,065,904 bytes.
- Independent Node verifier: 8,303 assertions; exact source/raw hashes, model counts, cover disjointness, work/span/storage formulas, and corruptions.
- LSPV-3/438 compact program: exact authenticated GitHub bytes replayed independently; 1,356 checks over 11 K4/cube/Petersen/prism cases.

Artifact SHA-256 values:

- producer `d016917f291e814bf3d1a8b26718fd702763c0a92a3bc382773f11a35f6e50a4`;
- independent verifier `7e35219109fc83458e1afb2bc89e62a914494e31d6b7ea9bf05b76d65d19db29`;
- raw results `bdcfac8d3add2e46217acd3414333116ac5404094a9888606a679c875d329879`.

The finite programs do not execute an authoritative $R_{\mathrm{mix341}}$ parser, certify accepted trace bytes, or prove an asymptotic mixed lower bound. The active workspace did not contain the project preflight scripts; the preserved instruction snapshot at `/workspace/scratch/3244a8e12dc8` passed its own preflight, which is not represented as validation of the new active-workspace artifacts.

## Final status and next precise gap

- **PROVED/EXACT RESTRICTED:** $2^{k-3}$ is the exact context-cover minimum when every leaf must leave at most three parity wires free and all boundary assignments must be covered.
- **PROVED/EXACT:** the context count is not a historical mixed-work lower bound. Native wide GF(2) rows give a zero-context route; the full odd-$K_4$ proof still costs 15.
- **COMPUTATIONAL:** 33,811 producer checks, 8,303 independent checks, and replayed 1,356 checks from LSPV-3/438; both labels, malformed source, corrupt literal, and same-row noncontradiction controls.
- **NOT CLAIMED:** a new hard family, a lower bound for full $R_{\mathrm{mix341}}$, an authoritative accepted-byte certificate, or any SAT-machine lower bound.
- **OPEN:** prove a rule-by-rule normalization that maps every legal full-mixed branching/shared proof to a restricted model while preserving work polynomially, or find a published family with a lower-bound invariant surviving every native rule and legal shortcut. Separately, the weakest noncircular same-calculus B3 bridge remains open. P versus NP remains OPEN.

The immediate red-team demand on future branch lower bounds is a declared **context-cost simulation theorem**: specify the native derivation of split and discharge, prove that every full mixed proof can be converted without exponential blow-up, and show why unconditional wide GF(2), RES, DEF sharing, and reconvergence cannot bypass the counted contexts. Without that theorem, the context result is useful restricted structure, not $\overline W_{R_{\mathrm{mix341}}}$.

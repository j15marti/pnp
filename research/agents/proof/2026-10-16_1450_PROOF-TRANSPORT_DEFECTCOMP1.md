# PROOF-TRANSPORT DEFECTCOMP1: Posterior Components, Randomized Search, and Same-Realization Exact-(2,2) Lift

**Timestamp:** 2026-10-16 14:50 Asia/Seoul  
**Status:** Two proved conditional-model theorems, finite exhaustive audits, unrestricted decider bridge OPEN.  
**Sentinel:** DEFECTCOMP1::P_VS_NP_OPEN

## 0. Proposals recorded before research

This run began with the following four candidates, in the required order.

1. **DEFECT-POST1:** Under the correlated unique-defect distribution for odd-charge Tseitin formulas, a partial transcript of edge-bit queries leaves the defective vertex exactly uniform over one connected component of the graph of *unqueried* edges.
2. **EXPAND-QUERY1:** Edge expansion should turn this posterior fact into a linear randomized decision-tree lower bound for locating a falsified parity clause. It must work against adaptive queries and 1/3 error.
3. **COMPILED-CRITICAL1:** A canonical source-to-target assignment extension through the original exact-(2,2) Tseitin compiler should preserve the one-defect distribution, source-clause labels, and per-query cost on the *same compiled realization*.
4. **DECIDER-FIREWALL1:** Show explicitly why even a successful restricted query or communication lower bound cannot be charged automatically against an arbitrary polynomial-time SAT decider.

The first three receive proofs or exact reconstructed model tests below. The fourth remains a precise limitation rather than a new arbitrary-machine bridge.

## 1. Sources searched after the proposals

**Current project records:** The immediately preceding PROOF-TRANSPORT turns, especially DISTFIREWALL2, RAND-SEEDFIREWALL1, SPLITRECT-INDEXFRONT1, ORDEPTH-ORACLE1, and OR3-SYNCP1. The current branch of the GitHub repository \`j15marti/pnp\` and recent commits were searched; the key reports were fetched.

**Primary project material:** \`research/main/2026-10-13_0408_MAIN_ROUNDINGSQUEEZE5.tex\`, \`research/main/2026-10-13_0948_MAIN_BLACKBOXQ1.tex\`, \`research/agents/lspv-4/2026-10-13_0035_LSPV-4_PC22_ALLFIELD1.tex\`, and the executable \`experiments/review/universal22.py\` were read. The source compiler's actual Q-gadget, clone pairing and constant-valued projection were reconstructed, not merely inferred from compiler counts.

**Google Drive:** The documents *SIL-PR-20260917-PROOF-001: Proof-Resource Transfer Certificates*, *21 P C: Punctured Tseitin Continuation Collapse*, and *21 P C A: Arbitrary-Target Restriction Factorization* were searched/read. These explicitly distinguish proof-resource transport from arbitrary-machine extraction and establish the constant-port clone/Q semantics.

**Literature:** Ben-Sasson and Wigderson, *Short Proofs Are Narrow* (JACM 2001); Göös, Pitassi and Watson, *Query-to-Communication Lifting for BPP* (FOCS 2017, SICOMP 2020); Chattopadhyay et al., *Query-to-Communication Lifting Using Low-Discrepancy Gadgets* (2019); and de Rezende et al., *Lifting with Simple Gadgets* (2020). Existing randomized lifting results motivate a future communication transfer, but no off-the-shelf relation/distribution theorem was assumed in this run.

## 2. Setup: an explicit correlated distribution

Let \(G=(V,E)\) be a connected loopless graph, \(n=|V|\), \(m=|E|\), and \(B\) its vertex-edge incidence matrix over \(\mathbb F_2\). Let \(b\in\mathbb F_2^V\) be an odd-charge vector, so \(\sum_v b_v=1\).

For an edge assignment \(x\in\{0,1\}^{E}\), define the defect syndrome

\[
d(x)=Bx+b.
\]

Define the single-defect distribution \(\mu\) by choosing \(v\in V\) uniformly and then choosing \(x\) uniformly from

\[
\mathcal X_v=\{x:Bx=b+\mathbf e_v\}.
\]

Since \(G\) is connected, \(\operatorname{rank}(B)=n-1\). Thus every \(\mathcal X_v\) is nonempty and has exactly

\[
|\mathcal X_v|=2^{m-n+1}
\]

assignments. Equivalently, \(\mu\) is uniform over assignments with exactly one parity-defect vertex.

For a cubic graph, the standard Tseitin 3-CNF \(F_{G,b}\) has four parity-forbidding clauses per vertex, exactly one falsified clause for each defective vertex. Thus every \(x\) in the support of \(\mu\) falsifies exactly one source clause.

Define the edge-expansion constant

\[
h(G)=\min_{\varnothing\ne U\subsetneq V}
\frac{|\partial_G U|}{\min\{|U|,n-|U|\}}.
\]

For a constant-degree expander family, \(h(G)\ge h_0>0\).

## 3. Theorem DEFECT-POST1: exact posterior component

### Theorem

Let \(S\subseteq E\) be any set of queried edges with observed bits \(x_S=a\), including an adaptively generated transcript. Put \(H=(V,E\setminus S)\), with components \(C_1,\ldots,C_k\). If the transcript has positive probability under \(\mu\), then there is **exactly one** component \(C_*\) such that

\[
\Pr_\mu[v=u\mid x_S=a]
=
\begin{cases}
1/|C_*|,&u\in C_*,\\
0,&u\notin C_*.
\end{cases}
\]

For every \(u\in C_*\), the number of completions is the same:

\[
\#\{x_{E\setminus S}:Bx=b+\mathbf e_u,\ x_S=a\}
=
2^{m-|S|-n+k}.
\]

### Proof

Write \(r=b+B_Sa\). For a prospective defect \(u\), the unqueried bits \(y=x_{E\setminus S}\) must solve

\[
B_Hy=r+\mathbf e_u.
\]

Over \(\mathbb F_2\), the image of the incidence matrix of a graph with \(k\) connected components is precisely the set of vectors whose coordinate sum is even on every component. Consequently a completion exists exactly when

\[
\sum_{w\in C_j}r_w=\mathbf 1[u\in C_j]
\qquad(1\le j\le k).
\]

Since \(\sum_w r_w=1\), exactly one component has odd residual parity; call it \(C_*\). Every vertex in \(C_*\), and no vertex outside it, is a possible unique defect.

The incidence matrix \(B_H\) has rank \(n-k\). Every solvable system therefore has \(2^{(m-|S|)-(n-k)}\) completions, independently of \(u\). Equal priors \(\Pr[v=u]=1/n\) imply the stated uniform posterior.

In an adaptive deterministic decision tree, the sequence of queried indices is a deterministic function of the observed bits. Conditional on the final observed pairs \((S,a)\), there is no extra constraint beyond those pairs. For randomized trees, fix the coins first. The same conclusion follows. \(\square\)

**Interpretation:** An algorithm can gain information about the defect vertex only when the queried edges disconnect the current possible-vertex component. Non-bridge queries may reveal random edge values, but do not change the posterior on \(v\).

## 4. Theorem EXPAND-QUERY1: explicit randomized query lower bound

### Theorem

Let \(G\) and \(\mu\) be as above, and let an adaptive, possibly randomized edge-query algorithm ask at most \(t\) edge bits in every execution before outputting a vertex. If

\[
t<\frac{h(G)n}{2},
\]

then its success probability under \(\mu\) is at most

\[
\boxed{
\Pr[\widehat v=v]
\le
\frac{t/h(G)+1}{\,n-t/h(G)\,}.
}
\tag{A}
\]

In particular, success at least \(2/3\) requires

\[
\boxed{
t\ge\frac{h(G)(2n-3)}5.
}
\tag{B}
\]

On any bounded-degree expander family with \(h(G)=\Omega(1)\), the randomized query complexity of finding a falsified Tseitin clause is \(\Omega(n)\).

### Proof

Fix the algorithm's randomness. Repeated edge queries cannot improve the information obtained, so count at most \(t\) distinct queried edges.

**Unique giant component.** For any deleted-edge set \(S\) with \(|S|<hn/2\), \(G-S\) has a unique component \(C_{\max}\) containing more than \(n/2\) vertices. Otherwise every component \(C_j\) has \(|C_j|\le n/2\) and

\[
hn\le\sum_j|\partial_G C_j|\le 2|S|<hn,
\]

a contradiction. The complement \(R=V\setminus C_{\max}\) satisfies \(|R|<n/2\), and all edges in \(\partial_G R\) were queried. Expansion yields

\[
h|R|\le|\partial_G R|\le |S|\le t,
\]

so at every stage

\[
|C_{\max}|\ge n-t/h.
\tag{C}
\]

**Exit process.** Call a query transcript *alive* when its posterior-active component \(C_*\) from Theorem DEFECT-POST1 is the giant component of \(G-S\). Initially all transcripts are alive.

At a query performed while alive, the giant either remains connected or splits into a new giant \(C'_{\max}\) and a discarded component of \(s_i\) vertices. Theorem DEFECT-POST1 says the conditional probability that the hidden defect falls in that discarded component is precisely

\[
p_i=\frac{s_i}{|C_{\max}|}.
\]

If no giant split occurs, set \(s_i=0\). In all cases, \(p_i\le s_i/(n-t/h)\).

Along any sequence up to and including its first exit, the successive giant components are nested. The discarded sizes telescope:

\[
\sum_{\text{queries before and including first exit}}s_i
\le n-|C_{\max,\mathrm{final}}|
\le t/h.
\tag{D}
\]

Taking conditional expectations of the exit hazard and using (C),(D) gives

\[
\Pr[\mathrm{Exit}]
\le \frac{t/h}{n-t/h}.
\tag{E}
\]

On transcripts that have not exited, the posterior is uniform over a component with at least \(n-t/h\) vertices. No proposed vertex can then be correct with conditional probability greater than \(1/(n-t/h)\). Bounding success on exited transcripts by one and combining with (E),

\[
\Pr[\widehat v=v]
\le\frac{t/h}{n-t/h}+\frac1{n-t/h},
\]

which is (A).

If \(t\ge hn/2\), inequality (B) already holds for \(n\ge2\). Otherwise (A) and success \(\ge2/3\) give

\[
\frac23\le\frac{t/h+1}{n-t/h}
\quad\Longrightarrow\quad 5t/h\ge 2n-3,
\]

proving (B). The bound holds for randomized algorithms by averaging the fixed-coin analysis. Finally, a correctly identified falsified clause reveals the defective vertex, so the same query lower bound holds for clause search. \(\square\)

**Scope:** This is an ordinary black-box *edge-assignment decision-tree* lower bound, not a SAT decision-time bound, and its \(\Omega(n)\) order is compatible with trivial linear-time full-input scanning.

## 5. Theorem COMPILED-CRITICAL1: exact-(2,2) same-realization transport

Let \(G\) be a connected simple cubic graph with \(n\) vertices and \(m=3n/2\) edges. The Tseitin 3-CNF \(F_{G,b}\) has \(m\) variables, \(4n\) clauses, and every variable occurs exactly four times positively and four times negatively.

Use the **original occurrence-halving compiler** \(C\) from LBO3SAT-0031 / PROOF-0034, instantiated as in the checked source \`experiments/review/universal22.py\` with the balancing-gadget count \(g=0\). Every source edge variable is replaced by four clones linked by directed implication cycles; implication clauses are padded with forced-false ports from independent copies of the 15-variable, 19-clause gadget \(Q\). The source clauses have one-to-one transformed copies.

The compiled formula \(H=C(F_{G,b})\) has exactly

\[
\boxed{
N_H=24m=36n \text{ variables},\qquad
M_H=32m=48n \text{ clauses}.
}
\]

Its standard binary-index encoding has length \(\Theta(n\log n)\). The formula is proper, signed, distinct-clause, exact-(2,2); it is **not asserted to be clause-monotone**.

### Canonical critical-assignment map

Define \(\Phi:\{0,1\}^m\to\{0,1\}^{N_H}\) as follows: set every clone of source edge \(e\) to \(x_e\), and set every variable inside every \(Q\) copy to zero.

All \(Q\) clauses are satisfied by zero, the padded implications are satisfied because clones agree, and each transformed source clause has the truth value of its source clause. Therefore

\[
\boxed{
\operatorname{FalseClauses}(H,\Phi(x))
=
\operatorname{Transformed}(\operatorname{FalseClauses}(F_{G,b},x)).
}
\tag{F}
\]

On \(\mu\), the left side is exactly one transformed clause. Every target variable queried on input \(\Phi(x)\) is computable using either zero source queries (constant Q variable) or one source edge-bit query (clone).

### Corollary

Any randomized algorithm that finds a falsified clause of the *fixed compiled realization* \(H\) with probability \(\ge2/3\) using at most \(t\) target-variable queries on every input must satisfy

\[
\boxed{t\ge h(G)(2n-3)/5.}
\]

Proof: run the target search algorithm on virtual input \(\Phi(x)\), answering each query with at most one edge query, and map its output clause back to its source vertex. Equation (F) establishes correctness on the pushforward of \(\mu\). Theorem EXPAND-QUERY1 applies. \(\square\)

For a cubic expander family, this gives an \(\Omega(N_H)\) randomized variable-query lower bound for falsified-clause search on exact-(2,2) instances, with an explicit hard input distribution. It is a *restricted query-model theorem* and not a superpolynomial runtime lower bound.

## 6. Independent adversarial and computational audit

Two complete local scripts were run independently:

- \`proof_transport_defect_component_audit.py\`: enumerates every critical edge assignment, verifies every reachable transcript of up to three or four queried edges, checks the completion count and uniform-component posterior, computes exact edge expansion, and uses an exact adaptive minimax dynamic program to determine the optimal success probability for every query budget.
- \`proof_transport_defect_lift_audit.py\`: independently reconstructs the actual 15-variable/19-clause \(Q\) gadget, four-clone equality cycles, target projection and transformed source clauses from \`experiments/review/universal22.py\`; checks target properness, distinctness and exact (2,2) occurrence counts; tests all critical source assignments and every auxiliary clause.

| Graph | \(n\) | \(m\) | \(h(G)\) | Reachable posterior transcripts checked | Exact optimal success at \(t=3\) |
|---|---:|---:|---:|---:|---:|
| \(K_4\) | 4 | 6 | 2 | 473 | \(1/2\) |
| \(K_{3,3}\) | 6 | 9 | \(5/3\) | 2851 | \(1/3\) |
| \(C_6\) | 6 | 6 | \(2/3\) | 313 | \(2/3\) |
| \(P_8\) | 8 | 7 | \(1/4\) | 393 | \(1\) |
| Cube \(Q_3\) | 8 | 12 | 1 | 2049 | \(1/4\) |

All posterior assertions and all applicable success bounds passed. The adaptive DP explored 344, 4876, 679, 2368, and 62,559 cached states, respectively.

**Hostile control:** A false extrapolation from nonadaptive queries would assert success \(\le(t+1)/n\) for *adaptive* algorithms on every connected graph. \(P_8\) refutes it: with three edge queries an adaptive binary-search tree identifies the unique defect with probability 1, whereas the best nonadaptive three-query success is only \(1/2\). Expansion is essential, and the theorem above does not make that invalid extrapolation.

**Exact compiler replay:**

| Source graph | Compiled vars | Compiled clauses | Critical assignments checked | Auxiliary clauses evaluated and satisfied |
|---|---:|---:|---:|---:|
| \(K_4\) | 144 | 192 | 32 | 5,632 |
| \(K_{3,3}\) | 216 | 288 | 96 | 25,344 |
| Cube \(Q_3\) | 288 | 384 | 256 | 90,112 |

Every tested critical source assignment falsified **exactly one** source clause and **exactly the corresponding one** target clause, with all structural clauses satisfied. Each compiled target had exactly two positive and two negative occurrences per variable. No mismatch was found.

These finite checks do not replace the mathematical proofs or establish novelty.

## 7. Compiler and proof-system reconciliation

**Original balanced Tseitin compiler:** Source variables \(m=|E|\) occur (4,4). The occurrence-halving compiler yields \(24m\) variables and \(32m\) clauses; source-to-target assignment map and Resolution restriction/projection are valid for the stated source. This is the compiler used in the new exact-(2,2) query lower bound.

**Clause-selector compiler:** The separate selector/duplication compiler audited in CP22LIFT1 has \(72q\) variables and \(96q\) clauses for its prescribed source with \(q\) proper 3-clauses. It must not be identified with the \(24m/32m\) occurrence-halving instance.

**Universal proper-source balanced compiler:** PC22_ALLFIELD1's broader regularizer gives \(9(q+7g)\) target variables and \(12(q+7g)\) clauses, where \(g=\sum_x(2r_x-p_x-q_x)\), \(r_x=\max(p_x,q_x,2)\), with \(g\le9q\). Its input-dependent sizes differ from the specific selector and original balanced cases. For the Tseitin source, \(g=0\), and these formulas agree with \(24m/32m\).

**Compiled OR shield:** With \(q=m_A+m_B\) source clauses, the already audited OR-shield followed by its selector compiler has \(144q\) variables and \(192q\) clauses. These numbers apply to that distinct realization, not to the same Tseitin source compiled above.

**Cutting Planes:** OR3-SYNCP1 and ORDEPTH-ORACLE1 concern syntactic integer CP and correctly charge guarded rounding/division. Their quoted two-way depth bounds \(D_{\rm OR}\le2\max(D_A,D_B)+4\) and projected depth \(\le D+4\) do not imply a result for every semantic CP representation or an arbitrary SAT decider.

**PC/PCR and SoS:** Ring substitutions and real SoS substitutions are proof-system-specific. In particular, the original compiled odd-charge Tseitin family is not a hard instance for PC over \(\mathbb F_2\); the project's all-field PC/PCR hardness branch uses *different* graph-colouring sources. Do not transfer a characteristic-\(0\) or SoS bound across fields without its theorem.

**Resolution:** The source Tseitin expander lower bounds and the original exact-(2,2) literal/zero Resolution projection concern actual refutations of the named formula. The new query distribution is on assignments to the **same named target**, with no oracle hash, simulation-time shortcut or change of realizations.

**Spread-budget triangle lifting:** ROUNDINGSQUEEZE5 gives strict Resolution width \(W\le w\), depth \(D\le wd\) and size \(S\le s M_w2^w\) from a globally correct triangle DAG of size \(s\le\tfrac12b^{(1-\delta)w}\) under its explicit spread conditions. A deterministic public-output \(c\)-bit protocol yields a same-realization triangle DAG with \(s\le2^{c+1}-1\), \(d\le c\). Our present randomized edge-query theorem is **not** itself such a protocol and does not by itself create a globally correct triangle DAG. A valid relation-specific randomized lifting theorem and parameter accounting would be needed. The earlier uniform-distribution counterexample forbids a naive 2/3-error version of the RS5 theorem.

## 8. The arbitrary-decider obstruction is unchanged

Theorem COMPILED-CRITICAL1 concerns the separate input \(\Phi(x)\), an **assignment** to one fixed unsatisfiable compiled formula \(H\). Its lower bound says a search procedure must inspect linearly many assignment bits to identify an actual falsified clause. It does **not** say solving the SAT *decision* problem for \(H\) takes that many operations. For this fixed \(H\), the decision answer is simply UNSAT.

An arbitrary polynomial-time SAT decider is not required to emit any falsified-clause search protocol, Resolution proof, CP proof, PC/PCR derivation, SoS derivation, or triangle DAG. Full-input scanning is polynomial and compatible with the new \(\Omega(n)\) query bound.

The TQBF-oracle countermodel from ORDEPTH-ORACLE1 remains decisive against any purely relativizing decider-to-fixed-proof translation. Under a PSPACE-complete oracle \(O\), \(P^O=NP^O\), while ordinary Resolution lower bounds for explicit formulas remain. Thus, a blanket transformation from any fast oracle decider to short ordinary Resolution cannot be relativizing.

There is also a simple positive observation illustrating the gap: if a polynomial-time SAT decider \(D\) existed, then the machine-dependent proof verifier

\[
V_D(F,\pi)=
[\,\pi=F\ \wedge\ D(F)=\mathrm{UNSAT}\,]
\]

would give linear-size certificates for UNSAT *in that specially defined Cook-Reckhow-style proof system*. This does not produce short proofs in Resolution or another fixed restricted system. A lower bound against all possible polynomially verifiable proof systems would be a much stronger proposition.

## 9. Outcome and next strictly weaker bridge

**Closed this run:**

1. A precise posterior-component theorem for the proposed single-defect distribution.
2. An adaptive randomized linear edge-query lower bound, complete with explicit finite-\(n\) inequality.
3. A same-realization lift of that query bound to the original exact-(2,2) compiled Tseitin family, reconstructed and exhaustively checked for three finite graphs.
4. An explicit adaptive-path counterexample to a tempting stronger but false nonadaptive formula.

**Still open:** an actual theorem connecting an *arbitrary polynomial-time SAT decider* to a representation covered by a superpolynomial unconditional lower bound. The new linear query lower bound cannot serve as that missing bridge.

**Next target, in order:** (i) verify the precise applicability of a randomized **search-relation** query-to-communication lifting theorem to \(\operatorname{Search}(F_{G,b})\circ\operatorname{IND}_b^m\); (ii) specify and analyze the induced correlated gadget distribution rather than assuming a product-uniform distribution; (iii) if a valid communication lower bound follows, assess whether its error and parameters can coexist with the deterministic same-row/same-realization RS5 requirements; (iv) independently attempt a nonrelativizing arbitrary-decider extraction theorem, rejecting any argument that silently grants a solver a proof-system interface.

## References

- E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 2001. DOI: https://doi.org/10.1145/375827.375835
- M. Göös, T. Pitassi, T. Watson, *Query-to-Communication Lifting for BPP*, FOCS 2017 / SIAM J. Comput. 2020. https://arxiv.org/abs/1703.07666
- A. Chattopadhyay, Y. Filmus, S. Koroth, O. Meir, T. Pitassi, *Query-to-Communication Lifting Using Low-Discrepancy Gadgets*. https://arxiv.org/abs/1904.13056
- S. F. de Rezende, O. Meir, J. Nordström, T. Pitassi, R. Robere, M. Vinyals, *Lifting with Simple Gadgets and Applications to Circuit and Proof Complexity*. https://arxiv.org/abs/2001.02144
- Project: \`research/agents/proof/2026-10-16_1339_PROOF-TRANSPORT_DISTFIREWALL2.md\`.
- Project: \`research/main/2026-10-13_0408_MAIN_ROUNDINGSQUEEZE5.tex\`.
- Project: \`experiments/review/universal22.py\`, original Q/clone/constant projection.
- Google Drive: \`21 P C\` and \`21 P C A\` source projection records.

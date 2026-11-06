# LSPV-1/457: bidirectional Extended Resolution transport across published bit-PHP strict-3 splitting

**2026-11-06 15:00 PST | Route B | PROVED/RESTRICTED in a separately declared ER gate/facet calculus; COMPUTATIONAL independent replay; specialist review pending.** Historical native \(R_{\mathrm{mix341}}\), B1/B2/B3, and P versus NP remain **OPEN**. No agent, rule, weight, or schedule was changed.

## Initial idea, falsifiers and prior work

Instead of substituting potentially high-degree Boolean polynomials for private 3-CNF splitter variables (LSPV-1/454-455), translate *entire ER proof DAGs* using conservative signed AND2 definitions and actual Resolution pivots. Falsifiers: (1) a defining facet has the wrong sign, (2) a split clause cannot be derived by the proposed number of legal steps, (3) a private variable is not globally fresh, (4) an implicit new native R_mix341 rule, weakening, or assumption leakage is being used. We excluded (1)-(3) for the explicitly declared ER calculus and *do not claim* (4) resolved for historical R_mix341. This is standard Extended Resolution proof transport, not a novelty claim or a contradiction of restricted-system hardness.

Read governing Nov 2 five-role handoff (blob c3889a3), current issue #3, LSPV-1/453-456, LSPV-3/455 independent checker, LSPV-5/315 LOCAL-CONVERT payload referee, Grok's actual 2026-11-06_0515_PROGRESS.md and Claude's actual TPORT-0002.tex. The Claude report concerns a separate restricted time-space portfolio model. Sources inspected: Braun arXiv:2609.23015v2, Pang arXiv:2610.00837v2, Cook ER PHP work, konard/p-vs-np README and scripts/proof_status.json, blkph0x/p-vs-np-proof-research/METHOD_INDEX.md, and meelgroup/frat-xor/format.md. No external file establishes native R_mix341 FACET/LOCAL-CONVERT accepted-byte compatibility.

## Certified-hard family and scope

Braun's bit pigeonhole principle has \(n=2^\ell\) holes, \(m=n+1\) pigeons, \(m\ell\) Boolean bits and \(A=n\binom m2\) wide clauses. Each pair \(i<j\) and hole label \(z\) yields

$$
C_{i,j,z}=\bigvee_{t=1}^\ell(b_{it}\ne z_t)
\ \vee\ \bigvee_{t=1}^\ell(b_{jt}\ne z_t).
$$

These clauses have width \(k=2\ell\); the formula is UNSAT by pigeonhole. Braun's preprint (Theorem 1.1) gives more than \(\exp(n/(32768\ell^2))\) proof lines for \(\ell\ge32\) in unrestricted shared-DAG **Resolution over parities**, with complementary-parity Resolution and semantic weakening but **without** freely definable extension predicates. It does not cover ER, split-3CNF, or R_mix341. The paper counts source lines; the project's W_R charges paid inference nodes. Haken ordinary Resolution PHP and Cook polynomial ER PHP, plus expander-Tseitin's existing GF(2) shortcut, remain mandatory stronger-rule controls.

## Exact theorem: two-way ER certificate transport

Let \(C=a_1\vee\cdots\vee a_k\) be a non-tautological clause with \(k\ge4\) distinct underlying variables, and \(t=k-3\). Introduce globally fresh \(y_1,\ldots,y_t\), forming the standard proper 3-CNF chain

$$
T(C)=(a_1\vee a_2\vee y_1)\wedge
\bigwedge_{j=2}^{t}(\neg y_{j-1}\vee a_{j+1}\vee y_j)
\wedge(\neg y_t\vee a_{k-1}\vee a_k).
$$

It has \(k-2\) clauses and \(t\) private variables. In a **separate, declared ER-AND2 calculus**, the conservative definition \(z\leftrightarrow(u\wedge v)\) yields the three explicit facets \((\neg z\vee u),(\neg z\vee v),(z\vee\neg u\vee\neg v)\). The calculus pays for gate definitions and all Resolution inferences, and records the facets (and their bits) explicitly; no free semantic implication or SPLIT/DISCHARGE is available.

**Direction A, split to wide:** Resolve the first split clause successively with the following split clauses on \(y_1,\ldots,y_t\). Exactly \(t=k-3\) correctly oriented Resolution nodes derive \(C\). For any original ER proof of the wide formula \(F\), derive each authenticated wide source from its split sources, then replay its ER proof DAG with hygienically renamed identifiers. The extra Resolution-node count is \(\sum_C(|C|-3)_+\).

**Direction B, wide to split:** Introduce the signed conservative gate definitions

$$
y_1\leftrightarrow(\neg a_1\wedge\neg a_2),\qquad
y_j\leftrightarrow(y_{j-1}\wedge\neg a_{j+1})\ (2\le j\le t).
$$

The first and intermediate clauses of \(T(C)\) are literally third facets of the corresponding gates. Starting from the original authenticated \(C\), resolve with \((\neg y_1\vee\neg a_1)\) and \((\neg y_1\vee\neg a_2)\), obtaining \(\neg y_1\vee a_3\vee\cdots\vee a_k\). For \(j=2,\ldots,t\), resolve successively with \((\neg y_j\vee y_{j-1})\) and \((\neg y_j\vee\neg a_{j+1})\). The final result is exactly \((\neg y_t\vee a_{k-1}\vee a_k)\). Total: **\(t\) conservative gate definitions, \(3t\) explicit gate facets and \(2t\) Resolution nodes per wide clause**. Now replay all nodes, shared lemmas and legal extensions of any ER proof from the strict-3 source. Cross-branch assumptions cannot leak because no new branch rules are invoked and all new local premises are source/global conservative definitions.

For every indexed wide CNF \(F\) with distinct literal variables per clause, the resulting \(T(F)\) has ER refutation size polynomially equivalent to that of \(F\), with additive \(O(\sum_{C\in F}|C|)\) gates and Resolution nodes and polynomial **explicit evidence-bit** overhead. Here proof-size accounting includes the original source size. The written proof is exact for this *ER calculus*, but specialist independent review is pending.

**Crucial simulation direction:** An ER upper bound transfers across the split. A published lower bound for weaker Res(XOR) does **not** transfer into ER or R_mix341 because that would require a polynomial back-simulation from *every permitted stronger refutation* into the published restricted calculus. Equisatisfiability and the two ER directions do not supply such a simulation. The earlier all-splitter ANF degree bound does not forbid a compact AND2 gate circuit.

For Braun's family, strict-3 has \(A(2\ell-2)\) original clauses and \((n+1)\ell+A(2\ell-3)\) total variables. From the wide source the added rules are \(A(2\ell-3)\) gate definitions, \(3A(2\ell-3)\) facets and \(2A(2\ell-3)\) oriented resolutions; in reverse there are \(A(2\ell-3)\) resolutions. No claim about the historical grammar or its fixed weights follows.

## Finite independent replay

Python producer and separately implemented Node verifier reconstructed original signed bit-PHP clauses and strict-3 clauses, every signed gate truth table, both directional Resolution sequences, all original source indices and full first-clause certificates. Node verification passed **417,574 assertions** with 14 corruption/malformed controls rejected. For \(\ell=2\), exhaustive original-bit enumeration found **0 models** for 5 pigeons/4 holes and **24 models** for 4 pigeons/4 holes. For \(\ell=3\), 9/8 UNSAT is established combinatorially, not by full Boolean enumeration.

| Case | Wide clauses | 3-CNF clauses | Gate defs | 3CNF-to-wide RES | Wide-to-3CNF RES |
|---|---:|---:|---:|---:|---:|
| 5 pigeons, 4 holes | 40 | 80 | 40 | 40 | 80 |
| 4 pigeons, 4 holes | 24 | 48 | 24 | 24 | 48 |
| 9 pigeons, 8 holes | 288 | 1152 | 864 | 864 | 1728 |

Full local reproducibility archive includes complete Python generator, independent Node verifier, original wide+strict CNFs, signed certificates, logs and SHA-256 manifest. One measured host replay: Python 0.17 s / 40,640 KiB RSS; Node 2.12 s / 96,904 KiB RSS. These are construction/checking resources, **not** minimum mixed proof work or FLMV same-machine time/space. Actual implementations pay parsing, source authentication, proof references, gate/facet serialization, output, validation and simultaneous memory. The free ideal proof choice excludes discovery cost intentionally; minimum work and ideal span differ from realized time and peak space.

## Exact remaining transfers

B1: for every uniform total correct SAT decider \(A\), a fixed polynomial \(p_A\) bounds \(W_R(F)\) by \(p_A(|F|+T_A(F))\) for all UNSAT \(F\).
B2: the corresponding \(W_R\) worst-case bound uses \(T_A^{wc}(N)\).
B3: \(\mathrm{SAT}\in P\Rightarrow \overline W_{R_{\mathrm{mix341}}}(N)=(N+1)^{O(1)}\) for the same **fixed** historical calculus. None is proved. A polynomial accepting/rejecting machine trace is not automatically a legal historical R refutation without an appropriate correctness/reflection and rule-simulation argument.

Next: authenticate historical paid-DEF/FACET/LOCAL-CONVERT accepted-byte interfaces, then test the *native* simulation against all legal shared mixed rules, and seek a superpolynomial all-rule invariant plus noncircular B3. Neither is delivered by this restricted ER result. **P versus NP OPEN**.

Primary sources: Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2 (2026); Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026); Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution* (1976); Haken, *The intractability of resolution* (1985).

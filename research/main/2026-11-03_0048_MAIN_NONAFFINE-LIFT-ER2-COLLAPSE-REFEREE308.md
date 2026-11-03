# NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308

**PNP Independent Proof Red Team — November 3, 2026, 00:48 PST**

**Status.** **PROVED/RESTRICTED** polynomial upper bound for the LSPV-3 lifted-Tseitin family in the unchanged fixed calculus; **PROVED/EXACT** fixed finite ER2 rewrite certificates; **COMPUTATIONAL** both-label, malformed, and independent replay controls; **OPEN** superpolynomial worst-case minimum cost, B1, B2, B3, and P versus NP.

No task identity, title, enabled state, schedule, ownership, safeguard, rule, or weight changed.

## Exact obstruction and claim card

The obstruction was the fresh-output support check in `AND3`: LSPV-3 recovered the four parity clauses on three fresh gate outputs, but its displayed global proof used a strengthened rule permitting `AND3` on those outputs. The proposed falsifier was that this grammar gap might preserve the nonaffine lift as a hard family for the unchanged calculus.

The fixed calculus remains `Rmix341`. This run uses only its source-independent two-input `AND`/`XOR` `VARDEF` gates and strict binary `RES`, already identified as the embedded `ER2` fragment in REFEREE299. Every gate instruction and every Resolution node has weight one; authenticated original CNF clauses cost zero; shared DAG nodes are counted once. No semantic XOR jump, SAT oracle, tailored axiom, or proof-search charge is hidden in the logical minimum.

## New theorem: the fresh-AND3 barrier is avoidable

Let \(G\) be a connected simple cubic graph with \(h\) vertices and odd Tseitin charge. Replace each edge variable by a disjoint \(k\)-bit input to a surjective Boolean gadget \(g\), and use the canonical local CNF of LSPV-3. Suppose \(g\) has a source-independent fan-in-two circuit of \(c(k)\) gates. Let \(M_v\) be the number of local input, gate, and output variables at vertex \(v\), as in the proved LSPV-3 local-projection theorem.

**Theorem.** The same unchanged `Rmix341` has a refutation of the lifted formula of cost at most

$$
|E|c(k)+\sum_{v\in V}3^{M_v}+69(3h)^3+9.
$$

Consequently, if \(c(k)=O(k)\) and \(k=O(\log h)\), this family has polynomial minimum cost. For the explicit \(g=\mathrm{AND}_2\) family in LSPV-3,

$$
W_{Rmix341}(F_h)
\le 1863h^3+\frac{163}{2}h+17.
$$

Since its encoded length is \(N=\Theta(h\log h)\), this is polynomial in \(N\). The earlier source-indispensability lower bound \(W_R(F_h)\ge 28h+7\) remains true; it is linear and compatible with this upper bound.

### Proof

1. Apply the proved local compiler at every vertex. Paid gadget definitions plus ordinary Davis–Putnam Resolution derive the four exact parity clauses on the three fresh edge-output variables. This costs at most

$$
|E|c(k)+\sum_v3^{M_v}.
$$

2. For each vertex, introduce two fresh binary XOR gates computing the XOR of its three incident edge outputs. The four parity clauses and the two gate definitions derive the charged vertex-output unit by an ordinary Resolution template. XOR the \(h\) vertex outputs. Unit propagation through binary XOR definitions derives unit value one because the total charge is odd.

3. Reassociate this circuit into a left-associated XOR of all \(L=3h\) edge occurrences in vertex order. Permute the occurrences into edge-paired order using adjacent swaps. Each local associativity or commutativity identity is certified by a fixed ordinary-Resolution DAG over its binary XOR definitions. An equality is propagated through the remaining suffix by a fixed XOR-congruence Resolution DAG.

4. The two appearances of each edge output have the same variable name, while the fixed gate grammar forbids identical absolute input IDs. Build the already verified nine-node true rail once. For one appearance of every edge output \(z_e\), introduce a fresh copy

$$
c_e\leftrightarrow (T\wedge z_e).
$$

The true-rail unit and the `AND` slots derive \(c_e\leftrightarrow z_e\). Congruence replaces the selected occurrence. Now the legal distinct-input gate \(p_e\leftrightarrow(z_e\oplus c_e)\) yields the unit \(\neg p_e\) by a fixed Resolution certificate.

5. Reassociate the paired expression into the XOR of the \(p_e\). Unit propagation derives final value zero. The equality chain identifies this output with the value-one output from step 2; one final Resolution step derives the empty clause.

For an explicit conservative count, the finite certificates below show that every rewrite application needs at most four paid gate nodes and 30 Resolution nodes, hence at most 34 charge. A left-chain adjacent swap uses at most three core rewrites and at most \(L\) congruence propagations. There are fewer than \(L^2/2\) adjacent swaps. Copy replacement, reassociation, cancellation, and unit propagation contribute only \(O(L^2)\) further applications. For every simple cubic instance \(h\ge4\), fewer than \(2L^3\) template applications suffice. The initial circuit and rail fit inside the slack of

$$
69L^3+9.
$$

Substituting \(L=3h\) proves the general displayed bound. For `AND2`, LSPV-3 exhibited \(80h+8\) local Resolution nodes and \(3h/2\) paid output definitions, giving the second displayed bound. Every dependency is acyclic and every assumed equality or unit in a template is a previously derived DAG node, not a free axiom. QED.

## Exact finite certificates

The Python producer saturated ordinary binary Resolution and retained only target ancestry for eleven fixed templates:

- XOR commutativity;
- XOR associativity;
- XOR congruence under an already proved input equality;
- true-rail `AND` copy equivalence;
- XOR of a value and its authenticated copy equals zero;
- all four Boolean unit-input XOR cases;
- both three-bit parity labels compiled to the corresponding XOR-output unit.

The retained certificates contain 155 lines, of which 81 are genuine Resolution nodes. The largest template is associativity, with 30 Resolution nodes. A separately implemented Node.js verifier reconstructs every permitted source slot, checks every pivot and exact resolvent, and accepts all eleven targets. Raw SHA-256:

`b85f616ce678b1bf7653e7bb4bafbf843ba971c9cdb42f7528a24cc8a7453ac9`.

This is a finite verification of the constant templates, not a finite extrapolation to the global theorem: the polynomial global composition is the explicit rewrite construction above.

## Four falsifiers and dispositions

1. **Fresh-output `AND3` is essential to finish the lifted proof. — FALSIFIED.** The legal `ER2` fragment finishes it using only paid two-input definitions and strict Resolution.
2. **A regular or bounded-depth `Res(⊕)` lower bound for a lifted Tseitin formula transfers to `Rmix341`. — FALSIFIED as an inference.** The fixed calculus admits extension variables, unrestricted DAG reuse, and the polynomial construction above.
3. **The local projection already proves the full global upper bound. — RESTRICTED/REPAIRED.** Projection alone stops at four clauses per vertex. The rewrite/cancellation layer is separately necessary and now supplied.
4. **A polynomial upper bound for this family proves B3. — FALSIFIED.** It only retires one candidate hard family. It supplies no polynomial upper bound on worst-case minima over all UNSAT CNFs.

## Both-label, malformed, and shortcut controls

- Odd-charge \(K_4\) Tseitin: independently enumerated 0 models.
- Even-charge neighboring \(K_4\): independently enumerated 8 models.
- Valid SAT and valid UNSAT DIMACS controls parse.
- Bad header, wrong clause count, out-of-range variable, missing terminator, and nonnumeric literal are rejected.
- A source empty clause or instance-specific correctness/advice axiom is rejected because it is neither an authenticated original clause nor a slot of a fixed source-independent gate.
- A semantic “XOR values cancel” jump is rejected; the cancellation, equality, and rewrite steps must name the retained Resolution certificates.

## B1/B2/B3 referee classification

This result proves none of B1, B2, or B3.

- **B1 remains OPEN.** No arbitrary SAT-decider trace is compiled into a proof.
- **B2 remains OPEN.** A short proof on this one family gives no upper relation between worst-case runtime and worst-case minimum proof cost.
- **B3 remains OPEN.** Even assuming SAT in P, no polynomial bound is proved for the same fixed calculus on every UNSAT input.

The exact implication chain B1 \(\Rightarrow\) B2 \(\Rightarrow\) B3 is unchanged. A solver fast on this family and this family's short derivations do not settle any bridge. P versus NP remains OPEN.

## Work, certificate length, and all-phase space

Logical cost counts only the exhibited proof DAG. Best-sequence discovery is free in \(W_R\), as required. Materializing the global certificate has polynomial output work and encoded length; checking requires parsing sources, validating gate freshness/slots, references, pivots, and final ancestry. A schedule that stores all clauses uses polynomial space, while a streaming/recomputation schedule may use less; no machine-space lower bound is claimed.

The finite producer charged closure discovery, exhaustive label enumeration, malformed parsing, certificate extraction, JSON serialization, and host overhead: 4.375 seconds wall time and 10,112 KiB peak RSS. The independent verifier was a separate process. These measurements are experimental upper costs, not logical weights or a Turing/RAM transfer. Any recursive use retains

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
$$

with \(\rho\) covering every local phase, including parsing, conversion, certificate construction, and checking.

## Literature and project audit

Searches recorded before proof work included: `extended resolution Tseitin formulas polynomial proof parity`, `extended Frege polynomial proof Tseitin tautologies parity`, `GitHub extended resolution proof checker XOR Tseitin`, and separate GitHub searches in `j15marti/pnp` and `github.com/openai`.

- Alekseev and Itsykson, *Lifting to Bounded-Depth and Regular Resolutions over Parities via Games*, ECCC TR24-128 rev. 2 (2025), proves restrictions on regular/top-regular and bounded-depth `Res(⊕)`, not extension-enabled `Rmix341`: <https://eccc.weizmann.ac.il/report/2024/128/>.
- Bhattacharya and Chattopadhyay, *Exponential Lower Bounds on the Size of ResLin Proofs of Nearly Quadratic Depth*, ECCC TR25-106 rev. 2 (2025), is likewise depth restricted: <https://eccc.weizmann.ac.il/report/2025/106/>.
- Bryant and Heule, *Generating Extended Resolution Proofs with a BDD-Based SAT Solver*, TACAS 2021, gives checkable ER proof generation and reinforces the need to distinguish solver computation from certificates: <https://doi.org/10.1007/978-3-030-72016-2_5>.
- Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), is the classical proof-system reference: <https://doi.org/10.2307/2273702>.
- The `meelgroup/frat-xor` repository exposes an XOR-aware proof format and verified `cake_xlrup` checker, but it is not silently treated as this fixed calculus: <https://github.com/meelgroup/frat-xor>.

Project reads included the verified 12:04 five-role handoff, issue #3, REFEREE299, LSPV-2 TWO-RAIL-GATE-SLOT-RT354, LSPV-3 NONAFFINE-GADGET-LOCAL-PROJECTION356, and LSPV-1 GODEL-REFLECTION-B3-FIREWALL357. The `github.com/openai` search found general math repositories but no relevant fixed-calculus implementation. A public fetch of one external formal-resolution repository returned an access/tool error; no conclusion relies on it. No novelty is claimed for classical ER reasoning; the new project-level result is the exact legal composition in the already fixed `Rmix341` grammar.

## Exact next gap

Remove this family from the mixed-hard atlas. The next lower-bound candidate must survive the full source-independent `ER2` fragment, not only Resolution, regular `Res(⊕)`, bounded depth, or the original-variable `AND3` support test. Independently, B3 still requires a same-calculus theorem of the form

$$
\mathrm{SAT}\in P\Longrightarrow \overline W_{Rmix341}(N)\le\mathrm{poly}(N).
$$

No such theorem is supplied here. **P versus NP remains OPEN.**

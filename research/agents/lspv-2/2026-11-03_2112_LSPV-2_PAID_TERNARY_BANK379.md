# LSPV-2/379: Paid three-wire Boolean-function bank and representation cut

**2026-11-03 21:12 PST, America/Los_Angeles.** Specialist: PNP SAT-Circuit Reduction Builder. Fixed inherited calculus: **R_mix341**. Status: **PROVED for an explicitly typed conservative signed-AND2 subcircuit**, with separate independently checked finite certificates; **NOT** proved for arbitrary R_mix341 LOCAL-CONVERT or unrestricted SAT algorithms. Independent specialist referee review pending. P versus NP remains **OPEN**.

## 1. Established hard-family anchor (model and quantifiers)

The starting point, not a regenerated lower bound, is Haken's 1985 theorem for the ordinary unary pigeonhole CNF PHP(h+1,h). Variables p(i,j) state pigeon i occupies hole j; occupancy clauses are positive h-literal disjunctions and collision clauses are negative binary disjunctions for pairs of pigeons in each hole. Explicit signed DIMACS encoding uses v=h(h+1) variables and m=(h+1)+h*binom(h+1,2) clauses, for N=Theta(h^3 log(h+2)) encoded **bits**. There exist c>0 and h0 such that for all h>=h0 and **every ordinary, unrestricted shared-DAG Resolution refutation** of PHP(h+1,h), at least 2^(c h) proof lines are necessary. This theorem is NOT a lower bound for Extended Resolution, Resolution over GF(2), R_mix341, arbitrary Turing machines, or arbitrary uniform SAT algorithms.

Cook 1976 supplies polynomial-length Extended Resolution proofs of the same PHP family, with acyclic conservative definitions. This is a mandatory shortcut. Previous LSPV-2/378 used these results to refute simple source-clause-retention-based hardness transports. The current result studies a narrower problem: whether a large **already paid, conservative** circuit component can be replaced by a small joint Boolean interface without semantic-support oracles.

## 2. Exact subgrammar and proved theorem

Fix a type **CUT3-DEF**, NOT asserted to be the complete LOCAL-CONVERT grammar of R_mix341. The three boundary wires u0,u1,u2 are earlier authenticated values: they can be original inputs or arbitrary previously charged, acyclic Boolean functions of any number n of original variables. In the enclosed component, every new internal wire is introduced by one paid R_mix341 signed two-input AND definition, w=(literal a) AND (literal b). Signed complement views of available wires are allowed; every new definition has a fresh name and a unit logical node cost. No additional source clauses or source-condition-dependent deductions are introduced by these definitions. Every exposed output is a signed wire reference, with no observation of internal wire identities, gate indices, side effects, or source metadata downstream. All incoming dependencies to exported outputs factor *syntactically* through the same three boundary wires. This cut condition is an explicit graph/typing promise, not a semantic-support promise.

**Theorem (paid three-wire bank).** For **every** finite acyclic CUT3-DEF circuit C and **every** finite collection of r exposed output values, there exists a single acyclic bank B of at most **783 paid signed-AND2 definitions** and r signed output references which simultaneously realizes all exposed outputs for **every valuation of all n original variables**. The bank is universal: the same 783-gate bank serves every C, and only the output-reference map changes. If a particular public-interface encoding charges an extra inference for reassigning each output name, add at most r paid nodes, and do NOT silently treat those output-name operations as free in R_mix341.

This is a statement about conservative circuit subcomponents with a trusted explicit cut and extensional output uses. It does NOT replace a source-authenticated inference, allow a false root, create a short refutation of general CNF, or establish a global W_R optimum. The theorem leaves the R_mix341 legal exported-wire interface and LOCAL-CONVERT rule completion open.

**Analytic synthesis bound.** For any two-variable Boolean function, synthesize its smaller ON or OFF set of at most 2 minterms. Each 2-literal minterm requires one signed AND, and two minterms combine with one signed AND implementing OR through complemented inputs and output. Constant zero requires one signed AND x AND NOT x; constants and complements need no special semantic rule. Thus at most 3 gates per two-variable function. For an arbitrary three-variable f, use exact Shannon decomposition:

$$
f(u_0,u_1,u_2) = (\neg u_2 \wedge f_0(u_0,u_1)) \vee (u_2\wedge f_1(u_0,u_1)).
$$

The two cofactors require at most 3+3 paid ANDs, with at most 3 additional ANDs for the selector and OR. Thus **at most 9 paid gates per three-input Boolean function**. Complemented output views are syntactically signed references. There are 256 truth functions on three bits but only 128 classes modulo global complement; three of these classes are bare input wires, and the constant class costs one gate. Independent construction gives the elementary global upper bound 1+124*9=**1117** paid gates for all functions. The submitted fixed deterministic synthesis improves this upper bound constructively to **783** gates, without claiming 783 is minimal. Each class is synthesized independently so there is no uncharged subcircuit sharing; the complete bank is a valid acyclic graph with fresh names.

**Independence of the original support size.** The theorem allows u_i(x) to have arbitrary and overlapping original-variable support, because the circuit identity is checked for **all eight formal valuations of the three named wires**, before substitution. For every original x, those wires take some such valuation, so the entire vector of exposed outputs is preserved. No essential-original-support test, which LSPV-3/382 proved coNP-complete for unrestricted succinct circuits, is required. The graph cut can be checked syntactically by tracing dependencies. This explicitly distinguishes "three trusted interface wires" from "at most three essential original input variables."

## 3. Independently verified finite construction

The exact public dataset contains 783 ordered paid signed-AND definitions, 256 signed output ports, a count for each of the 128 complement representatives, and all source-independent truth semantics. The per-class gate-count histogram is:

| paid gates | number of complement classes |
|---:|---:|
| 0 | 3 |
| 1 | 5 |
| 3 | 1 |
| 5 | 44 |
| 7 | 60 |
| 9 | 15 |

All 128 complement classes sum to **783** gates. The separately written checker re-evaluated every gate for all 8 boundary valuations, verified every one of 256 output functions on every valuation (2,048 output checks), enforced strict acyclicity, fresh names, legal signs and per-class gate bounds, and rejected **nine** deliberately corrupted records. It passed **52,191 assertions**. The public generator, checker and certificate were fetched from GitHub and replayed together, confirming exact JSON equality and the same 52,191 checks.

The second independent correlated-cut tester uses five original variables and nontrivial boundary values

$$
u_0=x_0x_1,\quad u_1=x_0\oplus x_1,\quad u_2=x_2\oplus x_3\oplus x_4.
$$

It checked all 32 original assignments and all 256 bank ports (8,192 port comparisons), **33,250 assertions**; the boundary realizes only six of the eight possible cut vectors, but the bank is separately valid on all eight. For example, the parity output u0 XOR u1 XOR u2 has **five essential original variables**, disproving the inference that constant interface arity forces constant original support. A hostile bypass output x4 cannot be expressed from this cut: original assignments 4 and 16 have identical boundary vector 001 but opposite x4 values. This explicit same-cut/different-output witness proves that silently dropping a bypass input is unsound. Separate odd/even K4 Tseitin controls give 0/8 satisfying assignments.

These are exact certificate checks for a **constructive upper bound**, not exhaustive searches ruling out cheaper banks and not a global R_mix341 minimum.

## 4. Falsifiers and actual resource costs

**F1 (large original support defeats the three-wire quotient): FALSIFIED.** If all exposed dependencies factor syntactically through three existing values, their original support can be arbitrarily large and correlated. The exhaustive five-input test above verifies the substitution mechanism.

**F2 (root-only or incomplete-cut quotient preserves exposed internal values): FALSIFIED.** Two circuits with identical root x0 but exposed u=x1 versus u=NOT x1 have different public interfaces. A bypassed x4 output has the explicit same-cut witness above. The replacement must preserve the full joint output vector, and all public dependencies must pass through the declared cut.

**F3 (any source-conditioned semantic LOCAL-CONVERT is subsumed): NOT PROVED; countercontrol.** Conservative DEF only defines new values. It does not assert that a source CNF entails a Boolean statement. An unrestricted semantic conversion F=>false, or a global antecedent with unbounded hidden original dependencies, is not licensed by this subgrammar. LSPV-5/328 demonstrates why antecedent locality is essential.

**F4 (logical gate count is physical time/space): FALSE INFERENCE.** Original g-gate syntax must be parsed and its graph/support authenticated; evaluating its Boolean values on eight abstract assignments takes O(8g) gate operations and source/index accesses. Reading an explicit representation takes Omega(encoded input bits) work. A straightforward bit-machine implementation costs O((g+r+783) polylog(g+r+783)) time and O((g+r+783) polylog(g+r+783)) **peak live bits** for a materialized representation, including source, wiring, truth masks, output aliasing and checking; an efficient streaming implementation may reduce peak memory but does not remove mandatory reads. The bank's 783 charged nodes do not include conversion discovery, parsing, output, or checking. If the source circuit is exponentially large, its actual materialization is charged; a compact generator must pay for generating or accessing needed gate semantics. No time-space lower bound for arbitrary algorithms is inferred.

## 5. Transfers and quantifier firewall

The current fixed project definition is W_R(F)=minimum sum of distinct paid derivation-DAG nodes over all valid R_mix341 refutations, with Wbar_R(N)=maximum over valid UNSAT sources of encoded bit length at most N, empty maximum zero. The bank theorem is a local **upper construction** and does not establish Wbar_R hardness.

For any fixed uniform total correct all-binary SAT decider A (SAT, UNSAT and malformed), the still **OPEN** obligations are:

$$
\begin{aligned}
\mathrm{B1}:&\quad \forall A\ \exists p_A\ \forall F\in\mathrm{UNSAT}:\quad W_R(F)\le p_A(|F|+T_A(F)),\\
\mathrm{B2}:&\quad \forall A\ \exists p_A\ \forall N:\quad \overline W_R(N)\le p_A(N+T_A^{wc}(N)),\\
\mathrm{B3}:&\quad \mathrm{SAT}\in P\ \Longrightarrow\ \overline W_{R_{\rm mix341}}(N)=N^{O(1)} .
\end{aligned}
$$

The source-to-proof implication B3 is the weakest sufficient bridge, but remains unproved. Do not transfer Haken's Resolution hardness into signed-AND/ER/GF2/mixed hardness, and do not reverse any simulation inequality. The 783-bank result neither proves nor refutes B3.

## 6. Repository history, independent assessments and literature

The repository paths were discovered by authenticated contents listings, not guessed. Reviewed as actual files:

- \`GROKPROOF/2026-11-04_0513_PROGRESS.md\`, blob \`085e27e9984a46697556125c37beb18d4eea7113\`: explicitly records universal fully charged FLMV all-input contraction **OPEN**.
- \`research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex\`, blob \`1f9fc727d3e2b009cba7afec2a93beb62959dd67\`: bounds concern a specific alternation-trading portfolio calculus, not arbitrary SAT decisions.
- \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\`, blob \`9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a\`: one-tape restrictions, not unrestricted machine lower bounds.
- \`research/coordination/2026-11-03_2100_LSPV1_MULTIWIRE_EXTENSIONAL_QUOTIENT379_FIVE_ROLE_HANDOFF.md\`, blob \`6c52aaf76954079b1b8a8106ce9dc0fdc3ca2cef\`: previously proved an upper bank bound of 6656 for common **three original inputs**. This result adds a charged **783-gate explicit bank** and the broader common **three authenticated wires** formulation, with strict scope.
- \`research/coordination/2026-11-03_2024_LSPV3_SEMANTIC_SUPPORT_LOCALITY382_FIVE_ROLE_HANDOFF.md\`, blob \`5e5aeca8d0374dfbbd107be755d63a3d8d2ce419\`: essential support coNP barrier avoided by syntactic cut, not disproved.
- \`research/coordination/2026-11-03_2048_LSPV5_TO_FIVE_ROLE_ANTECEDENT-LOCALITY-ROOT-QUOTIENT-REFEREE328.md\`, blob \`a12f8a53abc0f3f31f2e0e32a9e543200b7d92bb\`: mandatory source/antecedent guard; our result does not weaken it.

Primary research checked: Haken (1985) *The Intractability of Resolution*, Theoretical Computer Science 39:297-308, DOI 10.1016/0304-3975(85)90144-6; Cook (1976) *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4):28-32, DOI 10.1145/1008335.1008338; Grosof, Zhang, Heule (2022) *Towards the Shortest DRAT Proof of the Pigeonhole Principle*, arXiv:2207.11284; Shannon's cofactors (classical Boolean expansion). Project searches included prior LSPV-1/379, LSPV-3/382, LSPV-5/328, LSPV-2/378 and GitHub OpenAI math/SATVariance; the latter is random k-SAT formalization, not a proof compiler. No original lower bound was regenerated.

Reviewed governance \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, the 2026-11-02 12:04 five-role directive and current issue #3. All previous research artifacts, schedules, agent identities and R_mix341 rules are unchanged. Standard container-backed preflight and PDF/TeX compilation **could not be run** because the container/Python backend returned a Redis ResponseError. Instead both executables and full certificate were GitHub-readback-replayed inside a fresh V8 isolate. Do not treat this as running the requested external preflight scripts. Root \`main.tex\` was left untouched rather than risking an incomplete large-file overwrite.

## 7. Next precise missing arrow

Determine the *authoritative* full legal syntax of R_mix341 \`LOCAL-CONVERT\` and public DEF references, and whether source-authenticated, circuit-valued proof nodes can be given a syntactically certified common cut with every conversion, alias, source and verification cost paid. Without that grammar and a correct source-rooted proof translation, the three-wire bank cannot be promoted from a conservative subcircuit theorem to a full derivation equivalence, a lower-bound transfer, or B3.

**P versus NP remains OPEN.**

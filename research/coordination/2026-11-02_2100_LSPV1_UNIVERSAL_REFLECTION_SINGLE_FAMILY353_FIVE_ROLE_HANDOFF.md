# LSPV-1 UNIVERSAL-REFLECTION-SINGLE-FAMILY353 | November 2, 2026, 21:00 PST

**PROVED/EXACT**: one uniform polynomial-size signed-CNF soundness-counterexample family for every fixed correct P-time general CNF decider, and a *conditional* proof-transport inequality; a 5-node exact mixed-system global optimum for a three-variable six-clause signed micro-instance. **COMPUTATIONAL**: separate Python producer and no-import JavaScript checker, 112 local independent assertions, six essential source deletions, twelve single-literal SAT neighbors, four both-label cases, six malformed source rejects and five corrupted-proof rejections. **OPEN**: full Rmix341 proof specialization and source compilation, polynomial proofs of universal soundness, B1/B2/B3, superpolynomial mixed Wbar and P versus NP.

## One-family reflection target

Fix **one** total correct uniform polynomial-time SAT decider A, if such an A exists. Define the polynomial-size CNF $H_{A,\ell}$ by a complete paid Tseitin representation of

$$
\operatorname{ValidCNF}(s)\land[A(s)=\operatorname{UNSAT}]\land[y\models F_s].
$$

Correctness of A makes every such formula UNSAT, but does not provide short proofs in the fixed Rmix341.

Precisely separate **RT**, legal paid restriction/retyping of every Rmix341 proof node after fixing exact source bits, from **SC**, legal paid compilation of each specialized soundness-CNF source from authenticated original clauses and checked gate calculations. Both remain **OPEN for the full mixed calculus**. If both hold with polynomial overhead, then with $Q_A(\ell)=W_R(H_{A,\ell})$ there is a polynomial $P_A$ such that

$$
\overline W_R(N)\le\max_{1\le\ell\le N}P_A(\ell+Q_A(\ell)+1).
$$

Polynomial $Q_A$ would then imply weakest B3 for the same R; conversely B3 under SAT in P already implies polynomial $Q_A$ by the explicit polynomial length rescaling. These are *conditional* statements and are not a proof of SAT in P or of B3. This is a narrower and more concrete reflection target than requiring R size-optimal for every proof system.

## Exact signed control and falsifiers

The micro-instance $H_{\rm toy}$ has variables $a,b,x$, six original binary clauses, and three exact parity relations: $a\oplus b=1$, $x\oplus a=1$, $x\oplus b=1$. All six sources are indispensable. Global minimum mixed cost **exactly 5**: three paid AND3 conjunctions plus two paid XOR additions match the source-fanin floor $6-1$. A wrong reject-all decider makes the purported universal soundness CNF satisfiable, so computation traces cannot be imported as an UNSAT axiom.

Four falsifiers: (1) unsound rejects make the reflection formula SAT, (2) ordinary RES restriction does not establish full VARDEF/CONVERT/XOR retyping, (3) smallest logical DAG is not general machine time/space, and (4) decider $A$ cannot change with input length.

## Role handoff

**LSPV-1:** hold exact B3 and quantifiers, review whether any historical finite reflection or wrapper supplies RT or SC without an implicit soundness oracle. **LSPV-2:** specify a restriction-checker transition and source-authenticated, fully charged Tseitin-to-CNF compiler in unchanged Rmix341. **LSPV-3:** test guard/affine/DEF counterexamples to RT, and look for a growing nonaffine high-deficiency/high-width mixed-hard MUS. **LSPV-4:** audit polynomial input-length rescaling, proof-bit length and verifier/producer actual charged work and all-phase peak space. **LSPV-5:** falsify universal-reflection correctness and check any claimed legal specialization against malformed, opposite-label, corrupted gate/alias and hidden-axiom controls.

**Duplication:** LSPV-1 CLOCKED336 already gives conditional size-optimality-to-B1; FINITE-REFLECTION337 supplies a bounded arithmetic theory finite-proof route. This run instead localizes to one Boolean CNF family per input length with explicitly separate RT and SC obligations; standard Cook--Levin and bounded-reflection math is not claimed novel. Ordinary guarded Resolution transport in peer LSPV-2 349 is insufficient for mixed RT. Peitl and Szeider 2021 supplies finite hard controls, not an unconditional bridge.

## Verified public artifacts

- [Formal LaTeX report](../agents/lspv-1/2026-11-02_2100_LSPV-1_UNIVERSAL_REFLECTION_SINGLE_FAMILY353.tex)
- [Standalone signed Python producer](../../experiments/arc/lspv1_353_universal_reflection_producer.py)
- [No-import independent Node referee](../../experiments/arc/lspv1_353_universal_reflection_independent_verify.js)
- [Raw exact source, five-node DAG, deletion and sign-flip witnesses](../../results/raw/arc/2026-11-02_2100_LSPV1_UNIVERSAL_REFLECTION_SINGLE_FAMILY353.json)

Fixed Rmix341 unchanged. Original priorities, task IDs, titles, actual enabled states, schedule and role ownership unchanged. P versus NP OPEN.

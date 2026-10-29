# LSPV-3 CONTEXTUAL-PORT-LEAK163, LSPV-1/LSPV-5 handoff

29 October 2026, Los Angeles. The complete local LaTeX proof, Python reproducer, JSON and PDF have been tested in this run. A standalone condensed theorem, independent JavaScript source audit and raw provenance summary are published under research/agents/lspv-3/. Full local source code and PDF are downloadable from the conversation. File Service returned "No active container session" for direct Library upload; do not describe those uploads as successful.

**PROPOSE/BUILD:** Two 15-variable strict signed exact-(2,2) source modules can have the identical exposed triple relation R(t)=(t!=3) yet differ in hidden port p=x4. Define t=x1+2*x2+4*x13. Mode f in {0,1} flips all signs of hidden x4, leaving R invariant. Complete finite enumeration establishes Q_f(t,p)=(t!=3) AND ((t!=1) OR (p==f)). Simultaneously removing both negative hidden-port clauses forces their two feet to be 00 whenever physical p=0, including when the two clauses are used for distinct neighboring splices.

One negative literal-occurrence exchange between two modules forces physical hidden-port equality. Consequently, with exposed (t0,t1)=(1,1), modes 00 give SAT, modes 01 give UNSAT, even though the modules share the same exposed three-port truth table. This *falsifies* the belief that such a table is sufficient for contextual replacement before a future splice of an already forgotten hidden variable. It does NOT refute ordinary compositional existential quantification when all shared ports are retained.

**PROVED/RESTRICTED given audited finite lemma:** For every k>=2 and mode string f, the prescribed negative-swap connected chain is proper strict signed exact-(2,2), with 15k variables and 20k clauses, and exact 3k-port relation
```
AND_i(t_i != 3) AND NOT(
  OR_{i:f_i=0}(t_i==1) AND OR_{j:f_j=1}(t_j==1)
)
```
A one-bit retained physical port p makes the entire network exactly composable. A uniform recognizer and table compiler constructs both SAT witnesses and authenticated relational UNSAT certificates with polynomial time including source parsing, discovery, validation, reconstruction, failed attempts and output. These are **not** standard LRUP/2CNF-SCC certificates.

**COMPUTATIONAL:** Full enumeration of the 2^15 source; double-puncture tables for both modes; 455 independent full original-CNF SciPy HiGHS MILP cofactors (304 SAT, 151 UNSAT), including all 256 two-module mode/cofactor pairs; structural and semantic certificate controls at k=5,12,30; three forged-certificate rejections; two byte-identical Python runs, SHA256 0ea172a205f5ce012d7ea1653a66001efaf3acac11afbfdf5d995dee15f0e129. The user's Connected_Interface_Audit.zip was independently rerun byte-identically, SHA256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca.

**SEARCH:** Inspected lammich/lrat_isa/thys/LRAT_Checker_Impl.thy (Isabelle-verified LRUP checker); cuddorg/cudd/cudd/cuddBddAbs.c (symbolic abstraction, node limit); arminbiere/cadical/src/elimfast.cpp (bounded resolution), and openai/math/.../build/sections/06-recursion.tex (uniform one-child quantum skeleton but oracle table acquisition not implied). GitHub searches for the exact hidden-port noncongruence claim returned no exact match, not novelty evidence.

**IMPORTANT PRIOR RESULT:** LSPV-2 TWO-SWAP-EXACT-PORT-TRANSPORT223 already proves a distinct two-polarity pointwise equality transport for arbitrary strict exact-(2,2) sources. Do not reinterpret the present **one-negative-swap** contextual counterexample as falsifying LSPV-2's stronger regulator. That regulator still expands encoded length and does not imply universal SAT shrinkage.

**Next role targets:** LSPV-1 should require quantified compositional semantics under all future uses of discarded ports and compare the new one-bit state with the ARC resource ledger. LSPV-5 should independently falsify or certify the *simultaneous* two-slot puncture lemma in mode one and test alternative signed swaps. LSPV-3 should test whether these relational UNSAT traces admit a uniform polynomial source-authenticated original-clause LRUP/2CNF-SCC translation and whether two consecutive ordinary SAT descendants maintain the same boundary semantics. All universal SAT, contraction, proof-system and P-versus-NP claims remain OPEN. No scheduled agents were created or modified.

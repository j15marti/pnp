# LSPV-1/455 | Five-role handoff | November 6, 2026, 13:05 PST

**Route B lead only, unchanged five task identities and 2A/3B allocation. P vs NP OPEN.**

**PROVED/RESTRICTED, pending specialist review.** The standard $k$-literal disjunction -> $k-2$ proper 3-CNF clauses with $k-3$ private splitters has an exact Skolem coordinate minimum. At splitter $j$, $p=j+1$, $s=k-p$:

$$
\deg_{\mathrm{ANF}}f_j\ge\min(p,s),\qquad
\mathrm{ANFterms}(f_j)\ge\min(2^p,2^s-1).
$$

A **single valid full section** simultaneously attains both for all $j$: prefix-zero indicator for $p<s$, suffix-OR for $p\ge s$. The maximum degree is $\lfloor k/2\rfloor$. Braun's published Res($\oplus$)-hard bit-PHP wide clause has $k=2\ell$, so its middle local splitter requires degree $\ell$ and at least $2^\ell-1$ expanded ANF monomials for *clause-local* Skolem substitution. This strengthens LSPV-1/454's first-splitter affine-only obstruction; novelty unclaimed.

**Mandatory upper controls:** Signed AND/OR gate circuits realize the entire section with $O(k)$ gates; arbitrary paid Boolean definitions, reconvergence and shared branching remain candidate proofs. Do **not** assert preservation of Braun's bound for 3-CNF or full mixed R_mix341. Unlike a native mixed certificate, the local existential splitter section is not a public definition axiom.

**COMPUTATIONAL:** Python 66 coordinate rank cases, 293 degree-threshold tests, 32,741 satisfying original assignments; independent Node 55 coordinate cases and 35,346 assertions. Odd/even K4 Tseitin and malformed/corrupt controls passed. Short standalone verifier is under `experiments/arc/lspv1_455_compact_selfcheck.cjs`; the full report and raw summary are role-owned. Production historical Rmix341 checker was **not** run.

**Cross-role:** LSPV-3 should test whether a source-authenticated polynomial proof-level translation can legally consume private splitters without smuggling in free definitions. LSPV-5 should adversarially check the simultaneous section and exact model scope. LSPV-2/4 keep Route A primary and use these established formulas only for all-input algorithm/space controls. Keep free ideal choice of the full AND/OR shared proof DAG and separate logical work, span, proof encoding, solver search and machine peak space.

**OPEN:** native historical LOCAL-CONVERT/paid facet grammar; a superpolynomial $\overline W_{R_{\mathrm{mix341}}}$ invariant over all legal rules; noncircular B3 ($\mathrm{SAT}\in P\Rightarrow\overline W_R\in N^{O(1)}$); and Route A's all-input same-machine contraction. No schedules/roles/rules/weights altered. Root main.tex remained unreadable in partial fetch and is untouched.

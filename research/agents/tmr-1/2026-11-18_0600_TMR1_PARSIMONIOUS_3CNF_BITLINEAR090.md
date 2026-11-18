# TMR-1/090: Parsimonious 3-CNF compiler with isolate-normalized constant-factor bit growth

**Owner:** TMR-1 / PNP Machine Model Lead. **Date:** 2026-11-18 06:00 America/Los_Angeles. **Status:** symbolic mathematical proof plus finite COMPUTATIONAL verifier. Independent mathematical review, full LaTeX compile, and Lean/nanoda replay OPEN. **P versus NP OPEN.**

## Template and primary classifications

The fixed loopless regular tournament is \(T_5=(\mathbb Z_5,R)\) with \(R(a,b)\iff b-a\bmod5\in\{1,3\}\). The source is a directed constraint graph \(G=(V,E)\), \(n=|V|, m=|E|\). No SAT classification is inferred from superficial syntax. NP-completeness is independently established by Bang-Jensen, Hell and MacGillivray (1988), *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1:281--298, DOI [10.1137/0401029](https://doi.org/10.1137/0401029); the theorem classifies templates containing more than one directed cycle as NP-complete. The project also has explicit \(C_5\)-coloring to \(T_5\) reductions; the earlier /080 five-arc gadget is parsimonious.

Dyer and Greenhill (2000), *The Complexity of Counting Graph Homomorphisms*, Random Structures & Algorithms 17:260--289, DOI [10.1002/1098-2418(200010/12)17:3/4<260::AID-RSA5>3.0.CO;2-W](https://doi.org/10.1002/1098-2418(200010/12)17:3/4%3C260::AID-RSA5%3E3.0.CO;2-W), establish \(\#\mathrm{Hom}(-,C_5)\) as \(\#P\)-complete (under the counting-reduction notion in that theorem). Combined with the **parsimonious** /080 gadget this proves \(\#\mathrm{Hom}(-,T_5)\) is \(\#P\)-complete under at least the corresponding polynomial-time counting/Turing reductions. Do **not** infer parsimonious \(\#3SAT\) hardness solely from this citation.

## Theorem C1-T5-3CNF-PARSIMONIOUS-ISOLATE-OPT090

For every finite directed \(G\) including loops and opposed arcs, construct an explicit width-at-most-three Boolean CNF \(F(G)\) with exactly
\[
\boxed{B=7n \text{ variables},\quad K=17n+5m \text{ clauses},\quad
K_2=14n,\quad K_3=3n+5m.}
\]
There are exactly \(37n+15m\) literal occurrences. Every satisfying \(T_5\)-assignment extends to **exactly one** satisfying Boolean assignment, and every Boolean satisfying assignment decodes to precisely one \(T_5\)-assignment. Consequently
\[
\boxed{\#\mathrm{SAT}(F(G))=\#\operatorname{Hom}(G,T_5).}
\]

**Explicit compiler.** For every vertex \(v\), use five primary bits \(y_{v,0},\ldots,y_{v,4}\) (one-hot colors) and two auxiliary bits \(p_v,q_v\). For each \(0\le a<b\le4\), add \((\neg y_{v,a}\lor\neg y_{v,b})\): ten binary clauses. Introduce definitional gates \(p_v\leftrightarrow(y_{v,0}\lor y_{v,1})\) and \(q_v\leftrightarrow(y_{v,2}\lor y_{v,3})\), each using exactly the following three clauses:
\[
(\neg p_v\lor y_{v,0}\lor y_{v,1}),\quad
(p_v\lor\neg y_{v,0}),\quad(p_v\lor\neg y_{v,1}),
\]
and similarly with \(q_v, y_{v,2}, y_{v,3}\). Add the ternary clause \((p_v\lor q_v\lor y_{v,4})\). This uses 14 binary and 3 ternary clauses per vertex, forces exactly one primary color, and **uniquely** determines both auxiliary bits.

For each directed source arc \(u\to v\), add exactly five ternary clauses, one for each \(a\in\mathbb Z_5\):
\[
\boxed{(\neg y_{u,a}\lor y_{v,a+1}\lor y_{v,a+3})}
\qquad\text{(subscripts modulo five).}
\]
Under one-hotness, precisely the clause with \(a=x_u\) can restrict \(v\); it forces \(x_v-x_u\in\{1,3\}\). All other arc clauses are vacuous. This works for self-loops: every possible color then contradicts its own arc clause, and both sides are UNSAT. It also works for antiparallel arcs and disconnected input. No additional arc-variable and no nonfunctional Tseitin witness is introduced. Summing clause widths gives all stated counts.

**Canonical source bit format.** A valid source encodes \(n,m\) by the headers \(1^n0\,1^m0\), followed by lexicographically sorted, unique ordered pairs \((u,v)\in[0,n)^2\), each endpoint in exactly \(w(n)=\max(1,\lceil\log_2\max(2,n)\rceil)\) bits, low bit first. Directed loops and opposed pairs are permitted, duplicate arcs forbidden. A canonical source has exactly
\[
L_G=n+m+2+2m\,w(n)
\]
bits. Invalid source strings are rejected before compilation; in a total **decision** reduction they map to the fixed contradiction \(z\wedge\neg z\), not to an assumed promise.

**Canonical target bit format.** Number target variables \(0,\ldots,B-1\) in vertex order, five colors then \(p,q\). Use \(1^B0\,1^K0\), then for every clause a 2-bit clause-length field followed by the specified 2 or 3 signed literals, each encoded by one sign bit and \(w(B)\) index bits. A canonical order is ten pairwise-exclusion clauses, the six definitional clauses, and the final at-least-one clause for each vertex, followed by five clauses per lexicographically ordered arc. With \(B=7n\), this output has **exact** bit length
\[
\boxed{L_F=58n+15m+2+(37n+15m)(w(7n)+1).}
\]
For \(n=0\), use an empty CNF with zero variables and zero clauses; define \(w(0)=1\). Clause-length field uses 2-bit labels for lengths 1,2,3; the presented compiler uses only 2,3.

**Isolate-normalized constant-factor bit theorem.** The fully parsimonious \(F(G)\) may cost \(\Theta(n\log n)\) bits when the source has \(n\) isolated vertices, so **do not** claim universal constant-factor encoded growth for that exact full compiler. Instead, identify and drop the \(i\) isolated vertices, relabel the remaining \(n'=n-i\) vertices in sorted order, and compile \(G'\) with the same \(m\) arcs. Then
\[
\#\mathrm{Hom}(G,T_5)=5^i\,\#\mathrm{SAT}(F(G')).
\]
Decision and witness recovery remain equivalent, but the isolate-normalized map is **not parsimonious** when \(i>0\). Each deleted isolate receives arbitrary color 0 during witness reconstruction.

If \(m\ge1\), then \(n'\le2m\), \(w(7n')\le w(n)+3\), and
\[
\begin{split}
L_{F(G')}&=58n'+15m+2+(37n'+15m)(w(7n')+1)\\
&\le 487m+89m w(n)+2\\
&\le 489m+89m w(n)
<200(m+2m w(n))\le 200 L_G.
\end{split}
\]
For \(m=0\), output the canonical empty satisfied CNF of **two bits**, and return all isolated source vertices color 0. Therefore the isolate-normalized many-one decision map has \(L_{F(G')}\le200L_G\) for all valid input strings. The factor 200 is deliberately conservative, not optimal. For malformed inputs the fixed contradiction has constant bit length; a trivial fixed-size exception for the shortest malformed streams yields the same \(O(L_G+1)\) size accounting.

A deterministic sequential binary bit machine can validate and sort the input, identify isolates, relabel vertices, emit clauses, verify a Boolean witness and reconstruct a \(T_5\) witness with conservative simultaneous bounds \(O((L_G+1)^4)\) time and \(O((L_G+1)^2)\) peak writable space, including all parsing/serialization. The resulting deterministic reduction composition is \(O((L+1)^4)+T_{\rm 3SAT}(200L+O(1))\); this is an **upper bound**, not a claimed lower bound. Its precise \(T,S\) guarantees must use the same underlying machine realization on both sides.

## Counting and complexity consequences; strict limits

The full compiler is parsimonious for \(\#T_5\) to \(\#3SAT\), in the **width-at-most-3** convention allowing binary clauses. If exactly-three-literal clauses are required, a separate padding gadget must be accounted for; do not casually equate the two conventions for parsimonious counting. The normalized decision compiler is constant-factor encoded but loses precisely the \(5^i\) witness-count factor; no counting claim without that correction.

Prior /080 gives a parsimonious \(C_5\to T_5\) reduction with \(N=n+3m\), \(M=5m\); the above gives the reverse \(T_5\to3CNF\) map. If a deterministic polynomial-time general \(T_5\) decision algorithm existed, \(C_5\)-coloring and hence SAT would be polynomial-time, yielding \(P=NP\). A polynomial-time algorithm restricted to cactus, Eulerian, bounded-treewidth, long-subdivision or modular-consistent subclasses does **not** imply such a collapse. Neither a \(\#P\) classification nor finite tests prove a superpolynomial time lower bound.

## Finite computational audit

The local Node.js verifier \`/mnt/data/tmr090/tmr1_t5_cnf090_certificate.js\` ran 741 digraphs (all 512 loop-permitted digraphs on three vertices, plus exhaustive smaller sizes and 210 seeded controls on 4--6 vertices), checked 2,573,078 enumerated five-symbol assignments and its canonical unique Boolean extension, verified all 25 arc endpoint pairs, checked isolate-count factors, parsed clause counts/literal totals and tested the exact bit-size inequality. It completed **2,579,782 assertions, zero failures**. These are COMPUTATIONAL checks; the general equalities and bit-bound have the separate symbolic arguments above. The smaller published verifier and raw record preserve an independently executable check.

## Handoff

Retain existing ownership, enabled state, agent title, hourly schedule, draft PR #197 and issue #3. Maintain the living manuscript. Do not create, duplicate, disable, reschedule, merge or immediately rerun any agent. Next highest-value audit: construct a standard exactly-3-literal parsimonious translator if needed and test any claims of lower bounds against polynomial-time CNF, symmetry, Fourier/flow, DP, modular, local-consistency and alternative-encoding algorithms. **P versus NP OPEN.**

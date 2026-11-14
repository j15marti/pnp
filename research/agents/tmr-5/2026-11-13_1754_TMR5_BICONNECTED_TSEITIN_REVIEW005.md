# TMR-5/005: independent TMR-2 minimality review and biconnected graph-Tseitin extension

Date: 2026-11-13 17:54 PST (America/Los_Angeles). Repository: j15marti/pnp, main. Role: TMR-5 Machine Bottleneck Redteam and synthesis under the 12:49 PST five-new-TMR replacement directive.

**Independent peer verdict: TMR-2/005 and its elementary TMR-2/006 one-bit sensitivity transfer are PROVED/RESTRICTED at their explicitly encoded, correct-machine scopes, conditional only on the standard fixed explicit source model.** New TMR5-BG5 extension to arbitrary biconnected graphs below is **CANDIDATE pending independent TMR-1 or TMR-2 review**. Finite source tests are **COMPUTATIONAL**. All-exponent deterministic SAT lower bound and P versus NP remain **OPEN**.

## Specific audited claims

**Peer review, TMR2-MU5 and PB6.** The original TMR-2/005 construction takes the complete graph $K_m$, with a private XOR3 chain per vertex, odd vertex charge, and exactly four strict-proper 3-clauses per gate. Removing any one original clause permits a full satisfying assignment; the selected deleted clause alone is false. TMR-2/006 then flips any one of the selected clause's three original sign bits and uses the same assignment to obtain a *valid same-length opposite-label* input. Unread-source-bit coupling forces any fixed correct deterministic decider to physically inspect all those sign coordinates on the UNSAT run. This is an input-access bound, not compulsory exponential computation or memory. The independent graph/matrix argument below verifies both claims and removes an unnecessary restriction on the clique size.

**New extension TMR5-BG5 (CANDIDATE).** Let $G=(V,E)$ be a finite simple undirected graph with minimum degree at least three and $G-v$ connected for every $v\in V$. Choose $b\in\{0,1\}^V$ with $\bigoplus_v b_v=1$. Introduce one Boolean edge variable per $e\in E$. At a degree-$d$ vertex write its edge-incidence parity equation as a chain of $d-2$ XOR3 gates using $d-3$ private auxiliary variables, with the last gate carrying charge $b_v$. Encode each gate exactly by the four proper ternary clauses forbidding parity-incorrect triples. Denote the resulting ordinary 3-CNF by $F(G,b)$.

Then, subject to independent peer review,

$$
F(G,b)\in\mathrm{UNSAT},\qquad
\forall C\in F(G,b):F(G,b)\setminus\{C\}\in\mathrm{SAT}.
$$

Moreover, for every original literal occurrence $\ell$ in $C$, flipping only its original polarity bit produces a *strict-proper, same-encoded-length* SAT formula. The source counts, without padding, are

$$
N=3(|E|-|V|),\quad
M=8(|E|-|V|),\quad
P=3M=24(|E|-|V|),
$$

$$
w=\max\{1,\lceil\log_2N\rceil\},\qquad
L=N+M+2+3M(1+w).
$$

For a cubic graph, $|E|=3|V|/2$, so $N=3|V|/2$, $M=4|V|$ and $P=12|V|$. For a clique $K_m$ the earlier formula becomes $M=4m(m-3)$; the proof works already for **every integer $m\ge4$**, including odd $m$, not just even $m\ge6$.

For one fixed correct deterministic total multitape SAT decider with $h$ physically local source heads observing at most $h$ source bits per transition, the genuine *same-run* observation bound is

$$
T_A(F(G,b))+1\ge P/h.
$$

No workspace, online-input, solver-template, proof-system, or mandatory-enumeration premise is needed; the machine may reread source bits and use arbitrary temporary encodings. With a family of cubic graphs of unbounded size, this gives only $\Omega(L/(h\log L))$, not superlinear time. The number of input heads $h$ is a machine constant.

## Independent symbolic proof

1. **Odd parity obstruction.** XOR all $d-2$ gates at vertex $v$. Its private auxiliary variables cancel in pairs, leaving $\bigoplus_{e\ni v}x_e=b_v$. XOR across all vertices: every edge occurs exactly twice and cancels, whereas $\bigoplus_v b_v=1$. Consequently the original CNF is UNSAT.

2. **Forbid exactly one gate tuple.** Fix any original clause $C$, in a gate $q$ at vertex $v$. Its three signed literals are false on one unique Boolean tuple $\tau$. Exactly that gate equation is violated by $\tau$, and the *other three clauses in the same four-clause block* are true. The gate must remain false, not be silently repaired.

3. **Extend inside vertex $v$.** If $d=3$, the selected gate is the whole vertex parity constraint and all three edge bits are fixed. If $d\ge4$, the XOR chain is a path: removing the selected gate splits it into a possible left segment and a possible right segment. A first-gate selection leaves at least two free final incident edges to satisfy the prescribed terminal charge. A last-gate selection leaves two free first incident edges to attain its prescribed input auxiliary. An interior-gate selection leaves free incident edges on *both sides*, allowing its two frozen auxiliary boundary bits to be attained independently. All other local gates can therefore be satisfied with the three bits of $\tau$ fixed. Summing the now-single-violated chain gives incident edge parity $b_v\oplus1$.

4. **Solve the rest of the graph.** Freeze the edge bits incident to $v$. At every other vertex $u$, the residual parity requirement is $c_u=b_u\oplus x_{uv}$, with $x_{uv}=0$ when there is no edge. Its total parity is
$$
\bigoplus_{u\ne v}c_u
=(\bigoplus_u b_u)\oplus b_v\oplus
(\bigoplus_{u\ne v}x_{uv})
=1\oplus b_v\oplus(b_v\oplus1)=0.
$$
Since $G-v$ is connected, the residual vertex-edge incidence system is solvable over GF(2): assign non-tree edge bits arbitrarily and satisfy the remaining charges by leaf elimination on a spanning tree. At each $u\ne v$, fill its private auxiliary gate chain consistently. Thus precisely the selected gate has its parity violated on tuple $\tau$. Its four forbidden-tuple clauses exclude distinct assignments, so **exactly $C$ is false**.

5. **Literal flip and access transfer.** Under this assignment, each of $C$'s three literals is false. Flipping any one of their signs makes that literal true without changing identifiers or any other clause. Every such source is a valid Hamming-one SAT neighbor of the original UNSAT source. If a deterministic correct program does not read the changed bit on the original run, the two complete concrete executions remain identical, including all work tapes and source-head movements, contradicting the opposite outputs. Hence each of the $P$ positions must be observed. At most $h$ new positions can be observed per step.

**Concrete smallest tested witness.** The odd-charge $K_4$ source has six edge variables, 16 original clauses, 216 encoded bits and 48 individually sensitive sign bits. Let $b_0=1$, all other charges zero. The three edge bits at vertex zero are $x_{01},x_{02},x_{03}$. Removing its parity-forbidden all-zero clause $(x_{01}\lor x_{02}\lor x_{03})$ makes the all-zero assignment satisfy every remaining clause. Flipping one sign of this clause also makes the all-zero assignment satisfy all clauses. The clique proof does not require even $m$.

**Why the new condition matters.** $G-v$ connectivity is an explicit sufficient condition, not a theorem about all connected graphs. A disjoint union of two odd-charge $K_4$ components is UNSAT even after removing a clause from one component, since the other remains UNSAT. An independent executed negative control confirms this. We do not claim biconnectivity is necessary.

## Hostile algorithm and barrier audit

One fixed correct total deterministic SAT decider, independent of the graph and source length, can parse arbitrary strict proper 3-CNF sources; if its clauses partition into groups of exactly four clauses on the same triple of distinct variable IDs, with each group exactly a parity-XOR3 truth table, it recovers a GF(2) linear system and runs fully charged bitwise Gaussian elimination. If the pattern does not match, it invokes a fully charged total exhaustive solver. This fast path recognizes the entire encoded affine class including $F(G,b)$, with a polynomial bound on its recognized inputs; malformed input is rejected. No free oracle, length-dependent advice, unbounded-word arithmetic or special proof calculus is supplied. Thus even clause-minimal global inconsistency, Hamming-one sensitivity of every sign bit, and arbitrarily structured primal graphs do not imply expensive *post-acquisition* SAT processing.

Horn, 2-SAT, bounded-treewidth dynamic programming, products, renamings, padding, auxiliary variables, alternate encodings, sharing and recomputation are permitted by the fallback and cannot be excluded by this source-specific lemma. The GF(2) fast path is the decisive counteralgorithm to a proposed universal independent-per-clause cost. Pure semantic multiplicity, graph treewidth and proof-system refutation size are not transferred to arbitrary TM time. A relativizing/black-box read-only distinguishability argument does not establish any nonrelativizing general SAT separation. No Natural Proofs or algebrization theorem is invoked to claim impossibility.

## Actual executed checks and provenance

**Independent hosted V8 implementation** was executed before publication. Its own separately constructed graph-gate compiler and BigInt GF(2) solver checked eight graph fixtures (K4, prism, K3,3, cube, Petersen, K5, K6, K7), with two different odd-charge patterns each: **16 cases, 720 distinct clause-deletion certificates, 2,160 actual encoded one-bit-flip sources parsed and validated, 5 disconnected-product negative checks, zero failures**. Each deletion certificate was evaluated against every original source clause to check that only the selected clause was false. The script constructs full signed CNF and source encodings. The published code is an independent implementation, **not** a wrapper invoking TMR-2/005 or /006. Finite tests are COMPUTATIONAL; its JS big integers and runtime are not a charged physical TM simulation.

**Separate local Python reimplementation**, standard library and an independently written GF(2) solver, ran eight graph fixtures and both odd-charge patterns in a single 0.75-second completed chunk, also checking **720 clause deletions and 2,160 polarity neighbors, zero failures**. Local Python source and output were created in the container but are **not** claimed to be published in the repository; the corresponding published JS is fully self-contained. The Python script initially misparsed the fixture name K33 as the 33-vertex complete graph; the mistaken 25-second batch was stopped, the fixture dispatch was corrected, and the final completed Python run passed. This was a test-harness bug, not a source contradiction. No OS Node replay of the published JS, physical TM instruction trace, full repository preflight, check_research_reports.py or LaTeX compilation was performed.

GitHub readback-verified artifacts:
- Code: experiments/tmr/tmr5_graph_tseitin_biconnected005.cjs, blob ba9c56135484785e1cd4d3c0bfa06f807ca45f20.
- Raw: results/raw/tmr/2026-11-13_1752_TMR5_GRAPH_TSEITIN_BICONNECTED005_RAW.json, blob 575319218603816762befb39b316e57a3a6c179f.

**Corpus read:** FIRST authoritative 12:49 directive (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4); root proof1.txt complete 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; root proof2.txt recovered from authentic Git blob, 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c (ordinary contents returned blank, not treated as empty); canonical main.tex complete 2,494,937 characters SHA 873daeec6e11d4a7448f3b0547c9ed1ccfebd805; AGENTS.md; CODEX.md; .codex/skills/pnp-research/SKILL.md; all five newest TMR handoffs; issue #3 through 1,958 comments; original TMR-2/005 and /006 reports, executable sources/raw, TMR-1/005, TMR-3/002 and /006, TMR-4/005, TMR-5/004, and historical LSPV-4/459 expander/adhesion report. No old role or legacy-checker allocation was revived. Independent literature checks were conducted on the actual models and scopes.

## Primary sources and scope

[1] C. Lee, *On the Size of Minimal Unsatisfiable Formulas* (2008), https://arxiv.org/abs/0811.0427. Establishes the clause-minimality definition and separate constructions, not this project-specific graph-gate theorem.

[2] D. Itsykson, A. Riazanov, P. Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, https://doi.org/10.4230/LIPIcs.SAT.2022.6. Restricted **regular resolution and OBDD** refutation size in terms of treewidth; no arbitrary deterministic SAT TM runtime implication.

[3] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), https://doi.org/10.1145/1101821.1101822. Section 2.1 explicitly uses erased index tapes; its sub-golden-ratio simultaneous time/small-space exclusions do not rule out all polynomial SAT machines. Original author PDF physical page 4 inspected separately.

[4] TMR-2/005 and /006 original reports and exact code/raw under research/agents/tmr-2/, experiments/tmr/, results/raw/tmr/; TMR-3/006 two-physical-head model counterexample; LSPV-4/459 original-structure adhesion counterexample. These are project sources, not peer-reviewed external complexity results.

**Epistemic result:** The independent review supports the original clique minimality and source-polarity transfer as PROVED/RESTRICTED, with explicit computer-checked cases. The generalized graph theorem TMR5-BG5 is a new CANDIDATE until another agent's independent mathematical review. No resource lower bound beyond compulsory source observations has been proved. The complete all-exponent deterministic 3-SAT lower-bound implication remains OPEN, as does P versus NP.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt or proof2.txt. Canonical root main.tex will receive at most a qualified TMR-5 synthesis note, preserving all other text and statuses. No tasks or schedules created, revived or modified.

**Single next target:** TMR-2 independently prove the BICONNECTED-GRAPH extension with arbitrary gate positions and arbitrary odd charge, and TMR-3 attempt an all-step processing invariant that survives its fully charged Gaussian-elimination fast path. TMR-4 must check every-transition soundness for any candidate stronger cost abstraction.

END_OF_REPORT::TMR5::BG5::2026-11-13_1754_PST

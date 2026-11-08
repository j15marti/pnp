# LSPV-2/479 | No effective extraction of unknown polynomial SAT-decider exponents

**2026-11-07 16:18 PST | Route A | PROVED/RESTRICTED application of standard recursion theory and COMPUTATIONAL controls | P versus NP OPEN**

Proof-chain nodes: [P2-A2] (material restricted strategy firewall), [P2-A4] (unknown-exponent resource accounting OPEN), [P2-A5] (same-machine recursion OPEN), [P1-01], [P1-03], [P1-04] OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged. Historical R_mix341 grammar and weights unchanged.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** A code-aware compiler might automatically extract guaranteed polynomial-time exponents from the source code of every hypothetical correct polynomial-time SAT decider, then choose a contraction strategy using those values.

**Falsifiers declared in advance:** (F1) a self-referential padded decider can outrun its returned bound; (F2) such a counterexample fails if the extractor is partial, promised to halt only on correct polynomial deciders; (F3) the diagonal machine is not itself polynomial-time; (F4) a genuinely exponent-oblivious compiler does not require an extractor. The bounded-simulation repair defeats F2; F3 is false by the case analysis below; F4 remains an explicit limitation.

**SEARCH:** Reviewed both complete living trackers, current issue #3 comments, governing refocus/AGENTS.md/CODEX.md/pnp-research skill, latest LSPV-2/478 report and five-role handoff, LSPV-4/480 issue-#3 summary, actual GROKPROOF/2026-11-06_2316_PROGRESS.md, and research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. External files inspected include konard/p-vs-np README.md plus proofs/complexity/README.md (P subset NP only in its finite-machine model), blkph0x/p-vs-np-proof-research README.md plus affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md (restricted classification), openai/math README.md (varying verification status), and berkeley-abc/abc README.md (DAG-aware circuit rewriting, not universal SAT reduction). Primary literature check: MIT OCW Theory of Computation, Lecture 11, recursion theorem and self-reference; FLMV, JACM 2005, time-space lower bounds; Ben-Sasson and Wigderson, JACM 2001, ordinary Resolution width-size bound. Web queries covered computability of program runtime exponents and recursion theorem fixed points. Google-branded search unavailable; standard web search used. The attempted exact LSPV-4/480 report path yielded 404, but issue #3 contains its technical findings.

**ITERATE:** A naïve contradiction assumed an exponent extractor total on all program codes. Replace it by a self-referential machine that runs the extractor for *only n steps*. It remains polynomial whether or not the extractor halts. Hence the impossibility covers promise-partial extractors, a stronger and relevant quantifier.

## Theorem 479.1 (restricted exponent-extraction firewall)

Fix any language L having a uniform total correct deterministic polynomial-time decider A0, and any acceptable effective enumeration of deterministic programs with an actual transition-count time measure. No **partial computable** extractor E has the following promise property:

For every code d of a total correct polynomial-time L-decider D, E(d) halts with an integer k>=0 such that

$$
T_D^{wc}(n)=O((n+1)^k).
$$

**Proof.** Construct, by the *intensional* self-reference/quining implementation underlying Kleene's recursion theorem, an actual program with code d that on a binary input x of length n (i) simulates E(d) for at most n simulated steps, (ii) if a valid integer k is returned in that window, executes **at least (n+1)^{k+2} actual dummy transitions**, then (iii) executes A0(x) and returns its exact answer. This is an actual bounded interpreter and padding loop, not merely an extensionally equivalent fixed-point function that might omit the padding.

All inputs receive A0(x)'s correct output. If E(d) diverges, only n simulated E-steps plus A0 execute. Simulation overhead is polynomial in n for this fixed code. If E(d) halts, its step count h and returned k are constants independent of n. For n>=h the machine executes n^{k+2}-scale padding with polynomial-time counters; for n<h it executes at most n interpreted E-steps. Thus **in either case** this machine is a total correct polynomial-time L-decider. By E's promised domain property, E(d) must halt with some k. For all n>=h,

$$
T_D^{wc}(n)\ge(n+1)^{k+2},
$$

which contradicts T_D^{wc}(n)=O((n+1)^k). QED.

The theorem applies unconditionally to the trivial all-zero language. For **CNF-SAT**, it applies only under the **hypothetical SAT in P** premise, using A0 that correctly reports SAT, UNSAT and malformed encodings. It therefore does not establish SAT hardness. Even a promised partial subroutine guaranteed to learn a correct program's worst-case polynomial degree is impossible. An exponent-oblivious A -> Phi(A), with symbolic unknown t and s, is not excluded; neither are particular syntactic program classes carrying explicit degree certificates.

## Established hard-family control

For a connected cubic graph with H vertices, encode each charge equation XOR of three incident edge variables = b_v by four proper signed width-three clauses excluding the four wrong-parity edge assignments. This yields 4H clauses, 3H/2 variables and N=Theta(H log H) bits under conventional binary variable IDs. XOR of charges =1 certifies UNSAT. On cubic expander graphs, published width-size reasoning establishes exp(Omega(H)) **ordinary Resolution** proof-size hardness, not all-algorithm SAT hardness and not automatically full R_mix341 hardness. GF(2) charge elimination is a mandatory polynomial-time shortcut.

The executable **K4 finite control** has H=4, six original edge variables and sixteen strict 3-clauses. All 16 charge choices were classified against all 64 edge assignments: eight SAT and eight UNSAT. K4 itself is not asymptotic hardness certification. This is a regression family, not an assumption in Theorem 479.1.

## Independent finite controls and resources

The separate JavaScript implementation passed **884 assertions**, including 16 complete signed K4 controls, 84 padding/original-string cases with 28 malformed toy-string checks, and 256 bounded-extractor timeout-versus-halting cases. Independently written Python passed **542 checks**, including 16 original K4 charge classifications and 510 bounded-delay/padding arithmetic controls. These checks do NOT execute a Kleene fixed point, establish unbounded resource bounds computationally, or run a native FLMV machine.

For the theoretical padded D: A0's input parsing, index/source reads, SAT labels, malformed behavior, and output costs remain charged. The n-step E interpreter has polynomial actual time and space on the fixed native machine, including its scratch and head positions; if the extractor halts with fixed k, padding is at least (n+1)^{k+2} actual transitions and can be implemented with O(k log(n+2)) extra counter bits and polynomial time of degree depending on k. No guest oracle, children, source-only splitting, certificates or free shared subcomputations appear. The extractor and quine code are finite constants, not advice dependent on n. A full multi-child FLMV ledger is neither inferred nor claimed.

## Gap, status and handoff

**PROVED/RESTRICTED:** Using the known constructive recursion theorem, a promise-partial routine cannot return valid polynomial runtime exponents for all correct polynomial deciders of any fixed language in P. For SAT the implication is conditional on SAT in P. This is a narrow *exponent-learning prerequisite* no-go, not a universal solver-intensional contraction no-go.

**OPEN:** [P2-A2] solver-intensional, unknown-exponent-oblivious, all-input A -> Phi(A); [P2-A4] fully charged same-FLMV-machine ledger including s'<=max(rho,eta,lambda,lambda*s); [P2-A5] recursive closure and FLMV forbidden-region applicability. P1 and Route B load-bearing nodes unchanged. No P=NP/P!=NP resolution.

Sources: M. Sipser, MIT OCW *Lecture 11: The Recursion Theorem and Logic* (2020), https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/resources/mit18_404f20_lec11-1/ ; Fortnow et al., *Time-Space Lower Bounds for Satisfiability*, JACM 52:835-865 (2005), DOI:10.1145/1101821.1101822; Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48:149-169 (2001). External repositories are research clues only. P versus NP remains OPEN.

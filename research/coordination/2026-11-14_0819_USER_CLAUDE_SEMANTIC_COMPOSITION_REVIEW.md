# User-directed review: TMR-5/019, Claude, and the semantic-composition gate

Date: November 14, 2026, America/Los_Angeles (PST).
Scope: supervisory research review requested by the user after TMR-5/019. This is not an additional scheduled agent. Preserve the five TMR identities, schedules, historical evidence, and canonical manuscript ownership.

**Status:** corrected TMR-5/019 receives favorable scoped mathematical review. The elementary audit lemmas below have complete proofs, with independent project review pending. Finite results are COMPUTATIONAL. The proposed research direction is CANDIDATE. No unrestricted SAT lower-bound obligation is closed.

## 1. Assessment and provenance

The useful content of the latest result is an explicit easy-family falsifier, not a growing general lower bound. For the fixed-three-variable sign-stream family U_r, the corrected block sensitivity is 24, the distance to SAT is r, and the nearest-SAT count is 8*3^r. A fixed finite-control signature mask still decides the entire family in linear source length. Increasing duplication, certificate counts, or local mutation radius does not supply the missing all-machine processing theorem.

The latest explicitly Claude-authored reports located in the named repository directory, file search, and commit search are dated October 28, 2026. No newer Claude-authored document was located in those searches. This is a retrieval limitation, not a claim that newer work cannot exist elsewhere. The reviewed sources are ONETAPE-0001, DIRECTPRODUCT-0001, TPORT-0001 (model and rules portion), and TPORT-0002. Later agents' references to Claude were not misattributed as new Claude results.

Claude's relevant conclusions are:

* ONETAPE-0001: the equality/crossing argument also applies to nondeterministic machines in its stated tape model. Its near-quadratic bound principally measures transport. The supplied nondeterministic upper bound and the cut-counting ceiling explain why improving constants in this argument does not separate deterministic from nondeterministic polynomial time.
* DIRECTPRODUCT-0001: the proposed unconditional hitting-set proof has an unsupported derandomization step. A polynomial-size verifiable-search portfolio can be simulated by one fixed program with the portfolio factor charged. An assumed hardness premise for every polynomial budget already contains a separation-strength assertion.
* TPORT-0001/0002: the stated alternation-trading calculus has a portfolio barrier at c+d >= 2, c >= 1. The limitation concerns that calculus and its small-space model, not all possible proofs. This review did not independently rerun its rational LP certificates or certify every supporting hierarchy sketch.

The project should retain these as falsification requirements. Repeatedly returning to source-only sensitivity, delayed external queries, or optional parity delays without a new transfer should cease to be the main separation effort.

## 2. Independent review of the new robustness result

Let C_sigma be the three-variable clause falsified only by assignment sigma. Let

$$
U_r=\bigwedge_{\sigma\in\{0,1\}^3}\bigwedge_{j=1}^{r}C_\sigma.
$$

The restricted sign-stream length is 24r. Ordinary encodings must additionally charge headers and identifiers.

To become SAT, at least one signature must disappear. Its r original occurrences must each change, requiring at least r sign flips. At radius r, exactly one bit changes in every occurrence of one chosen signature, and no changes occur elsewhere. This yields exactly 8*3^r distinct nearest SAT strings.

For every signature and each of its three literal positions, changing that position in all r occurrences gives one sensitive block. All 24 such blocks are disjoint. Each sensitive block has size at least r, and only 24r positions exist, proving the upper bound 24 as well. Thus bs(U_r)=24. The superseded value 8 is false.

The minimum sign-query certificate size for UNSAT at U_r is exactly 24, not just at most 24. Observing one full occurrence of each signature suffices. Conversely, if some signature has no fully observed occurrence, each partially observed occurrence can independently be completed to a different signature. The resulting formula omits the chosen signature and is SAT. Therefore every UNSAT-forcing partial observation must fully determine all eight signatures, using at least 24 sign coordinates. This statement is within the fixed-variable, fixed-clause-count sign language; it is not a certificate for arbitrary unauthenticated variable identifiers.

Our independently authored native Python test examined 63,468 nonzero-radius mutations across U_1,U_2,U_3, matching the exact nearest counts 24,72,216, and tested 384 disjoint sensitive blocks for r=1,...,16. The older report's 63,471 count includes three radius-zero sources; that is not a discrepancy in the formulas.

## 3. A concrete semantic-composition falsifier

The next experiment uses the same new family to test an actual algebraic substitution, rather than another sensitivity parameter.

For a CNF F on n Boolean variables, write f_F(a)=1 if assignment a satisfies F and 0 otherwise. Over the rational numbers its unique multilinear extension is

$$
\widetilde f_F(z)=\sum_{a\in\{0,1\}^n} f_F(a)
\prod_{i=1}^{n}\bigl(a_i z_i+(1-a_i)(1-z_i)\bigr).
$$

**Exact identity:**

$$
\widetilde f_F(1/2,\ldots,1/2)=\#\mathrm{SAT}(F)/2^n.
$$

Proof: each Boolean assignment contributes its label times 2^{-n}. Thus a generic polynomial-time exact rational evaluator for this extension would compute exact model counts. Merely assuming a SAT decision procedure does not provide that evaluator or its time-space budget. This observation is not an unconditional lower bound on extension evaluation.

Compare the cheap gate-by-gate arithmetic expression

$$
P_F(z)=\prod_{C\in F}\left(1-\prod_{\ell\in C}(1-\ell(z))\right),
$$

where a positive literal is z_i and a negative literal is 1-z_i. It agrees with F at every Boolean point, but repeated/shared variables usually make it nonmultilinear. For every proper three-literal clause its midpoint value is 7/8. Hence, for every r,

$$
P_{U_r}(1/2,1/2,1/2)=(7/8)^{8r}>0,
\qquad \widetilde f_{U_r}(1/2,1/2,1/2)=0.
$$

A nearest SAT neighbor has exactly one model, so its canonical midpoint is 1/8. The formula containing 8r copies of just one signature has seven models, so its canonical midpoint is 7/8. All three formulas have the same naive arithmetic midpoint (7/8)^{8r}.

This falsifies replacing a required multilinear extension by an arbitrary easy Boolean-equivalent arithmetic circuit. It does NOT rule out useful nonmultilinear extensions when an algorithm's interpolation proof permits them. Williams explicitly leaves such alternatives relevant. Nor is the rational midpoint an assertion about his characteristic-two implementation: 1/2 does not exist in characteristic two. The algebraic domain, interpolation set, degree, field size, output encoding and arithmetic bit cost must be stated separately.

Our test builds the canonical multilinear polynomial by multiplying modulo x_i^2=x_i, and independently evaluates the original CNF truth table. Across 195 formulas and 5,178 assignments both representations agree on all Boolean points. All 195 exact midpoint/count identities passed. The naive and canonical midpoint values differ in 175 fixtures. Controls include Horn, 2-SAT, proper-3-CNF lifting, affine parity, duplicates, disjoint products, shared variables and renaming. Sparse polynomial expansion is only a finite audit implementation, not a representation forced on arbitrary algorithms.

## 4. A size constraint on explicit abstract graphs

**Elementary ceiling lemma.** Let a finite abstract graph have at most M reachable states, a reachable decision terminal, and nonnegative edge weights at most W. Every potential satisfying Phi(u) <= c(u,v)+Phi(v) on every edge and Phi(goal) <= 0 obeys

$$
\Phi(start)\le d(start,goal)\le(M-1)W.
$$

Proof: telescope along any terminal path. Delete cycles, whose costs are nonnegative, to obtain a simple path with at most M-1 edges. Its cost is at most (M-1)W.

Therefore a polynomial number of explicitly represented states with polynomially bounded weights cannot yield a superpolynomial lower-bound potential. An abstraction may instead have a polynomial-size succinct description of exponentially many states, or genuinely justified large macro-costs. A constant-size finite controller with unbounded tapes does NOT have a constant number of configurations.

The audit tested 180 finite weighted graphs, including zero-cost cycles, with 4,039 potential-edge inequalities and 180 terminal checks. Binary countdown controls of widths 1 through 12 demonstrate the essential succinct-state distinction: a short description can represent exponentially many states and a correspondingly large potential. These countdowns are optional delay computations, not SAT lower bounds.

## 5. Recommended main target: charged composition of actual machine computations

My judgment is to shift the center of effort from input-shape invariants to **the cost of composing succinct machine computations while retaining shared dependencies**. This is a research prioritization, not a claim that its missing theorem is easier than P versus NP.

A concrete primary source is Ryan Williams, Simulating Time With Square-Root Space, STOC 2025. It gives an arbitrary-multitape-machine simulation through implicit Tree Evaluation instances and a square-root-scale space bound. Its discussion identifies an expensive low-degree-extension subroutine and explains why applying the space simulation recursively is not immediate. This is a legitimate all-machine setting, unlike requiring a SAT solver to answer an external delayed INDEX query. It does not by itself yield simultaneous polynomial time and small space, or a P-versus-NP separation.

The new October 7, 2026 Li-Tell preprint studies much stronger simulation phenomena under low-space Range Avoidance hardness assumptions, with average-case guarantees. Treat it as conditional technique evidence, not an unconditional premise or an all-input SAT algorithm. No such assumption is adopted here.

### First concrete deliverable

Specify and audit ONE actual block-evaluation/interpolation service from the Williams/Cook-Mertz simulation. It must expose:

1. The finite machine A, encoded input length L, time budget T, block size b, valid and invalid boundary encodings, and original SAT/UNSAT output binding.
2. Exactly which Boolean or field-valued function is queried. Distinguish ordinary evaluation, arbitrary extension evaluation, canonical multilinear evaluation and counting.
3. Bit costs of constructing or accessing the computation graph, discovering tape-access dependencies, generating extensions, arithmetic, caching, recomputation and combining shared values.
4. The same simulation's time and peak writable space. Never borrow the time of one implementation and the space of another.
5. A concrete attempt to replace its expensive operation, with a correctness proof or a smallest counterexample. U_r is a required positive/negative algebraic test, not a hardness premise.

The closest credible constructive question is whether some noncanonical, low-degree extension or different compositional summary supports the actual interpolation identity with lower charged acquisition/evaluation cost. The first test is algorithmic validity and joint resource accounting. No premise that every SAT machine must compute a canonical extension is allowed.

### Exact proof obligations

G0: one fixed correct total general SAT machine and ordinary explicit encoding. Established as the problem model, not existence of a fast machine.

G1: an applicable arbitrary-machine normalization with proved overhead and genuine original-source binding. Published simulations supply some versions; import only the exact verified version.

G2: a compositional simulation or abstract resource measure that covers all eligible A and every real operation, including algebraic shortcuts. OPEN for a new useful improvement.

G3: either a lower bound beyond every fixed polynomial for the same A-dependent abstract computation, or a genuine all-input, recursively closed joint-resource transformation that would turn a hypothetical polynomial SAT decider into a contradiction with a verified lower-bound theorem. OPEN. Merely writing a favorable exponent recurrence does not establish a compiler.

G4: correct all-exponent quantifiers and model transfer. A conditional final implication is straightforward only after G2/G3 are proved. Restricted proof-system size, source reading, space upper bounds and average-case conditional simulations do not close it.

Under the lower-bound formulation, one needs an independently defined measure D_A(F), a proved transfer D_A(F) <= poly(L,T_A(F)), and superpolynomial D_A on hard instances for EVERY fixed correct A. Defining D_A as the unknown runtime is only a restatement. Under the resource-transformation formulation, all access/construction/recursion costs must survive iteration and the final forbidden-region theorem must match the model and both resources. These are alternative proof routes, not interchangeable bounds.

## 6. Concrete next assignments, preserving TMR roles

These are the scientific next-step priorities for the existing team in response to the user's request. No schedule, task identity, or enabled state is changed.

| Role | Primary next deliverable | Excluded shortcut |
|---|---|---|
| TMR-1 | Source-verify the all-machine normalization and exact block interface; make L, T, b and all quantifiers explicit | No solver portfolio or per-length algorithm minimum |
| TMR-2 | Audit semantic extension/composition services and identify any hidden counting or reachability oracle; independently check the U_r midpoint counterexample | No assumption that generic SAT decision supplies exact model counting |
| TMR-3 | Derive the actual simultaneous time-space ledger for that one service and any proposed replacement; test recursive closure | No uncharged extension construction, random access or favorable recurrence without a machine |
| TMR-4 | Build a source/program-specific symbolic abstraction of the same interface, retaining shared dependencies; use the finite-graph ceiling to reject inadequate explicit-state models | No potential defined by unknown runtime; no compulsory temporal post-copy phase |
| TMR-5 | Independently replay the producer; test nondeterministic portability, algebraic controls, graph-generation costs and every purported bridge | No promotion of a small-model or code-count theorem to unrestricted SAT hardness |

Keep sensitivity variants, further fixed-variable certificate counts, late-copy wrappers and optional delay-amplifier examples as regression controls. Prioritize another such variant only when it changes a named main proof obligation or falsifies a live candidate. Do not delete their historical evidence.

A successful next run should publish a specific compiler component, counterexample, or quantitative cost bound for the common service. It should not merely repeat that a processing invariant is needed. The independent proof of the new elementary audit observations remains requested from TMR-2/TMR-4/TMR-5.

## 7. Evidence, limitations and preservation

Executed locally: one standalone native CPython audit, 0.514276 seconds, no failed assertions. It uses integer/rational arithmetic, truth tables and independent graph shortest paths. No physical generic SAT Turing-machine compiler was executed. No peer JavaScript was rerun; the robustness test was independently authored. The finite polynomial construction is deliberately small and exponential in variable count.

Repository review: authoritative TMR directive in full; corrected TMR-5/019 in full; the named Claude reports and specified TPORT-0001 portion; CODEX and repository research skill; AGENTS excerpts; root tree/commit and Claude-directory searches; current issue and a recent comment page; root proof1 opening and root proof2 beginning via fallback contents fetch; Nov13 full-chain review opening. The ordinary file endpoint returned a SHA but no main.tex or proof2 body. Alternative proof2 retrieval yielded authentic beginning text, but this session did not inspect the complete million-character tracker or the complete canonical manuscript. No claim of full-corpus byte review is made. No unreadable file is overwritten. The repository-wide preflight and LaTeX build were not executed.

Root proof1.txt, proof2.txt, and main.tex remain unchanged. Their reviewed status is OPEN. This additive supervisory report must not be represented as closure of a root obligation. Publication and independent review are separate from mathematical proof.

## References and source anchors

[1] TMR-5/019, corrected report: research/agents/tmr-5/2026-11-14_0754_TMR5_SIGN_ROBUSTNESS_REDTHEOREM019.md; inspected blob 4eeb75ffb6655e55dc06b9c43637b30b739c0d98.

[2] CLAUDE ONETAPE-0001: research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a.

[3] CLAUDE DIRECTPRODUCT-0001: research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; blob 95c2649b29ae7efac79e9400effffd2c3bdeb2fc.

[4] CLAUDE TPORT-0001 and TPORT-0002: research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex. These are project-authored claims, not independently validated journal publications.

[5] Ryan Williams. Simulating Time With Square-Root Space. STOC 2025; author manuscript dated February 25, 2025, Theorem 1.1, Section 5 and Appendix A. https://people.csail.mit.edu/rrw/time-vs-space.pdf . Read original text and rendered PDF pages. The rational midpoint audit is not the paper's characteristic-two construction.

[6] Zeyong Li and Roei Tell. Trading Time, Space, and Alternations: General Plasticity for Algorithms from Hardness of Range Avoidance. ECCC TR26-233, October 7, 2026. https://eccc.weizmann.ac.il/report/2026/233/ . Abstract inspected; conditional average-case scope only, no detailed theorem import.

[7] Samuel Buss and Ryan Williams. Limits on Alternation-Trading Proofs for Time-Space Lower Bounds. ECCC TR11-031; Computational Complexity 24(3), 2015. https://eccc.weizmann.ac.il/report/2011/031/ . Restricted proof-method barrier, not an impossibility theorem for P versus NP.

END_OF_REVIEW::USER_CLAUDE_SEMANTIC_COMPOSITION::2026-11-14

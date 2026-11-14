# TMR-4/016: cost-exact parity erasure versus a replay-spurious cheap path

**Pacific timestamp:** 2026-11-14 01:44 PST (America/Los_Angeles). **Role:** NEW TMR-4 Cost-Sound Abstraction. **Repository:** j15marti/pnp, main. **New theorem status:** CANDIDATE/RESTRICTED pending independent TMR-5 or TMR-1 review. **Executed tests:** COMPUTATIONAL. **Full-uniform 3-SAT lower bound and P versus NP:** OPEN.

## 1. Exact claim and its relevance

The recent TMR-3/014 proof constructs an all-length fixed-program parity-prepass wrapper whose genuine prepass crossing records contain global future-source parity after only two crossings per cut. This report independently checks its one-head composition at the symbolic level and distinguishes two notions that must not be conflated:

1. **Semantically inert parity:** If the control register is never subsequently inspected, erasing it and the unused last-read bit gives a **strong, cost-exact bisimulation** of all physical steps, for every fixed source and every fixed underlying decider A. The suffix dependence intentionally injected into those crossing tags is removable. The remaining A computation is preserved exactly, not assumed easy.
2. **Cost-relevant parity:** If that same register decides whether to perform one further charged full input roundtrip, the analogous MAY quotient remains forward cost-sound but introduces a **replay-spurious cheap path** on odd-parity sources. Its Bellman potential underestimates the actual prepass by exactly 2(L+1). Retaining the physically computed parity through the gate repairs the particular abstraction. The genuine detour must not be deleted.

The distinction is a nontrivial example of what a cost-sound, program-sensitive *crossing-record normalization* can and cannot automatically discard. It is **not** a proof that any universal SAT crossing normalization exists, that decision-relevant future information can be discarded, or that the remaining processing cost is superpolynomial.

## 2. Fixed total physical machine family

Fix any one finite, total, correct, uniform deterministic multitape SAT decider A with at least one locally moving read-only original-input head starting at physical cell 0, other heads and work tapes initially in their usual states, fixed finite control and alphabet. Input x has L encoded bits at cells 1 through L and endmarkers at 0 and L+1. Only one original head is used in the prepass. All input movements, writable-cell visits and A steps are charged. A may process valid SAT, valid UNSAT and malformed strings by arbitrary algorithms and arbitrary writable space.

Define one fixed uniform wrapper W_A^0: sweep the input head right from 0 to L+1, physically updating in finite control parity P(x) and most recently scanned bit; sweep it back left to 0; discard both registers and run A from its exact original initial configuration. The wrapper costs, on the **same x**,

$$
T_{W_A^0}(x)=T_A(x)+2(L+1),\qquad S_{W_A^0}(x)=S_A(x).
$$

Define another fixed uniform wrapper W_A^1 with the **same first two sweeps**, but at the end of the return it performs **one additional fully charged right-and-left roundtrip if and only if P(x)=1**, then runs A identically:

$$
T_{W_A^1}(x)=T_A(x)+2(L+1)(1+P(x)),\qquad
S_{W_A^1}(x)=S_A(x).
$$

No information from A is obtained in the prepass, and the original source is never replaced. The parity register is one finite-control bit. Each optional extra traversal is 2(L+1) actual physical input-head transitions. Output labels, totality and all-length uniformity follow from unchanged A; no free oracle, answer table, advice, unbounded word operation or solver template is used. In the finite-control restricted implementation below a final terminal transition contributes one more step.

## 3. Exact simulation and source binding

Fix the **actual full source x** as a read-only component of each concrete configuration; retain the fixed program identity, phase, current input-head position, every A control/work/head component, all interim clause masks and parsing fields where present, and output labels. Initially the source and blank work tapes are identical in concrete/abstract initial states. At SAT/UNSAT/malformed terminals the same label is preserved.

For W_A^0, let q erase only the finite-control fields (parity, last-read-bit) that are dead after being updated. Before A begins, phase/head motion depends on the endmarkers and head position but not those fields. A's entry discards them. For every pair of well-formed concrete configurations c,d with q(c)=q(d), **every legal step** satisfies q(next(c))=q(next(d)). A's subsequent concrete transition table is copied without abstraction. Each corresponding edge has cost exactly one. Conversely, the unique abstract successor is the projection of each concrete successor in the related fiber. Induction gives exact complete paths of identical transition count, and in particular

$$
d_{\mathrm{abs}}(q(c_0),G_{\mathrm{true\ label}})
  =T_{W_A^0}(x)
$$

for the fixed source and deterministic terminating actual machine. This is a **cost-exact scoped quotient**, not a new computable formula for the unknown T_A(x).

For W_A^1, the same q, if applied as an existential MAY quotient of **all well-formed configurations** (including unreachable choices of the erased parity at the return gate), includes BOTH cost-one gate edges: return-to-A and return-to-extra-roundtrip. Every concrete transition is still represented at exactly its actual increment, so the required forward simulation and terminal preservation hold. But the two abstract edges are not both replayable from a given fixed source's *reachable* gate state.

For odd P(x)=1, after the first two sweeps the real source-bound gate must take the extra roundtrip. The cheap abstract choice corresponds to an artificial P=0 concrete register inconsistent with the actual scan history. Replaying it from the fixed initial state fails at the precise final return transition, not at a SAT label. Thus the cheap path is **spurious in this declared MAY graph**, and the source-bound concrete trace must remain intact. Retaining the already physically computed parity in the abstract state through that gate removes this particular spurious branch. Equivalently a proved reachable-state invariant connecting the return parity to the source removes it. This is refinement of replay-proved spurious behavior, not deletion of a genuine program execution.

Note the qualification: a different source-conditioned quotient containing **only actually reachable states** could infer the real parity from x and remain exact. That source-specific reachability characterization is extra proof information, and cannot be silently supplied as an operationally free SAT classifier. It does not alter the actual paid execution.

## 4. Bellman potential and precise false-shortcut gap

In the finite restricted model, every step costs 1. Let p be the current physical input-head position and let phases F, R, DO, DB, O, H denote first outward scan, first return, optional detour outward, detour return, output step, and halt. The parity-erased MAY graph admits the explicit nonnegative potential

$$
\Phi(F,p)=2(L+1)-p+1,\quad
\Phi(R,p)=p+1,\quad
\Phi(DO,p)=2(L+1)-p+1,
$$

$$
\Phi(DB,p)=p+1,\qquad
\Phi(O)=1,\quad \Phi(H)=0.
$$

Direct substitution proves **every abstract edge**, including BOTH gate choices and all ordinary input-head movements, obeys

$$
\Phi(a)\le 1+\Phi(b),\qquad \Phi(H)=0.
$$

The shortest abstract path to the true terminal has exactly

$$
\Phi(q(c_0))=2(L+1)+1
$$

steps, because the MAY gate can always choose to skip the optional detour. For odd parity the concrete cost is 4(L+1)+1, so the abstract minimum is low by **exactly 2(L+1)**. This violates no lower-bound inequality: a valid MAY abstraction is permitted to be overly optimistic. What fails is any assertion that the erased quotient's minimum *equals* actual time, or that all its cheap paths are genuine. At the real odd-parity return gate, keeping the finite-control parity restores a cost of 2(L+1)+2 from that pre-gate state, instead of the erased bound 2.

The inequalities above are arithmetic facts in the restricted graph. They are not a construction of a superpolynomial initial potential. Even the exact quotient still contains the unknown full computation of A and proves no unrestricted SAT processing bound.

## 5. Native/hosted execution and test integrity

Published standalone JavaScript was **actually executed in hosted V8** by invoking its exact source. It models one locally moving read-only source head and a constant-width finite-state classifier for the unbounded sign-stream language of clauses over exactly three variables. Each three-bit clause forbids one assignment; mask 255 means UNSAT, another mask means SAT, and nonmultiples of 3 are MALFORMED. The eight-bit mask and parity are finite control, not unbounded words. An independently written three-variable truth-table evaluator authenticates terminal outcomes.

Fixtures: every binary string of genuine lengths 0 through 11 (4,095 strings), 256 deterministic seeded 24-bit strings and three additional 24-bit adversarial controls, including an eight-mask UNSAT permutation. Both inert and gated machines were checked on each source. At each executed transition, the full concrete successor, parity-erased alternative successor, label, paid transition count, and Bellman inequality were tested.

| Executed metric | Count |
|---|---:|
| Distinct test executions per wrapper | 4,354 |
| Even / odd parity sources | 2,191 / 2,163 |
| SAT / UNSAT / MALFORMED outcomes | 843 / 1 / 3,510 |
| Concrete charged edges and Bellman checks | 265,692 |
| Inert strong-bisimulation edge checks | 107,418 |
| Gated ordinary same-quotient edge checks | 153,920 |
| Parity-gate divergence controls | 4,354 |
| Odd-source replay-spurious paths detected | 2,163 |
| Parity-refined true residual-cost checks | 2,163 |
| Failed assertions in corrected full rerun | 0 |

An initial development test erroneously omitted the final halt step from an odd-parity detour suffix; the formula was corrected to 2+2(L+1) and the full run repeated. A subsequent audit corrected the L=0 fixture from string "0" to the real empty input, updated the exact published executable and immutable raw ledger, and reran all checks. These failures were test-harness errors, not omitted physical computations. OS-native Node, independent Python reimplementation, general SAT machine compilation and repository-wide LaTeX/preflight were **not** executed. The finite checks are COMPUTATIONAL, not an asymptotic proof.

**Exact published source:** experiments/tmr/tmr4_parity_quotient016.cjs, Git blob 6a4300b02c7c0598bd04bd42d8374c7002975673.

**Raw evidence:** results/raw/tmr/2026-11-14_0142_TMR4_PARITY_QUOTIENT016_RAW.json, Git blob 562db7fc6ddfc44485caf14a0a2c431009165c44.

## 6. Sources, original historical counterexamples, and falsifiers

Primary literature:
- P. Cousot and R. Cousot (1977), *Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints*, POPL, pp. 238-252, DOI https://doi.org/10.1145/512950.512973. This motivates sound overapproximation; the paper does not supply a SAT superpolynomial cost potential.
- E. Clarke, O. Grumberg, S. Jha, Y. Lu and H. Veith (2000), *Counterexample-Guided Abstraction Refinement*, CAV, pp. 154-169, DOI https://doi.org/10.1007/10722167_15. Spurious paths require actual feasibility/replay analysis.
- L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas (2005), *Time-space lower bounds for satisfiability*, JACM 52(6), pp. 835-865, DOI https://doi.org/10.1145/1101821.1101822. Its paired time/low-space exclusions are not an arbitrary-polynomial-space separation.

Original peer records read: TMR-3/014 two-crossing report and its original model, TMR-2/015 parity-gated crossing report, TMR-4/015 actual late-copy potential counterexample, TMR-1/015 indexed original-input model-transfer report. Original historical LSPV-5/511 authentic string-valued-support accepted-by-checker counterexample was also read and **preserved**: the concrete accepted packet is not erased by adopting a tidier intended grammar.

Hostile controls: the arbitrary-A wrapper proof is agnostic to Horn, 2-SAT, GF(2)/Gaussian elimination, bounded-treewidth DP, disjoint products, sharing, auxiliary variables, renaming, padding, caching and recomputation. The finite simulator itself tests **only the fixed-three-variable sign-stream subclass** and malformed encodings, not those separate polynomial-time algorithms. No assignment-enumeration or boundary-state counting is charged as unavoidable computation.

The unrestrained arbitrary-machine bridge remains OPEN: no resource-lower-bound potential has been shown to grow faster than every polynomial on at least one valid input for every fixed all-length correct decider. In particular, inert-parity erasure does not prove that every future-dependent machine state is inert, and the parity gate shows why that generalization fails.

## 7. Governance, dependencies and next target

The overriding five-TMR replacement directive was read first and rechecked unchanged (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4). Root proof1.txt was recovered completely via contents (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343). Root proof2.txt returned a blank content body with a valid SHA, so the **authentic full 1,051,196-character Git blob** 930c5eeddafce656717f28055a7a9a755f44737c was separately recovered. Root main.tex similarly required its full Git blob (2,522,180 characters at read, SHA 903092cd483c0b17694c9f500fa03b5a703508cc). AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the latest issue #3 comments and all five current handoffs were read. TMR-5 remains canonical main.tex synthesis owner.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Nodes P1-01/P1-03/P1-04 and P2 all-exponent unrestricted machine transfer remain OPEN. Canonical main.tex unchanged. Scheduled tasks unchanged.

**One next target:** TMR-5 independently review the cost-exact inert quotient, the parity-gate replay-spurious branch and whether a proposed full-trace SAT abstraction can identify semantically inert versus cost-relevant state *without requiring a solver-completeness oracle*. Request the same-source all-edge simulation and both-label preservation in each candidate. Do not assume bounded future-interval depth from these restricted normalizations.

END_OF_REPORT::TMR-4::016::2026-11-14_0144_PST

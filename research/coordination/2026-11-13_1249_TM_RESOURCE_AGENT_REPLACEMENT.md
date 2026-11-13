# TMR: five NEW Turing-machine resource agents

Directive: user request of 2026-11-13 12:49 PST (America/Los_Angeles). Repository: j15marti/pnp, main.

## Authority and transition

The user explicitly requested halting the current five agents and producing five NEW agents pursuing the computational bottleneck of a Turing machine deciding 3-SAT. This is a replacement, not a rename or another additive topic. It supersedes conflicting older instructions to preserve LSPV identities, historical Route A/Route B allocation, or mandatory investigation of one legacy checker. Preserve all verified mathematics, counterexamples, source provenance, reproducibility, and publication safeguards. Do not revive retired tasks or delete historical artifacts.

The five old schedules were successfully disabled on 2026-11-13 at 12:50 PST:
- LSPV-1: 6ad6f02da1bc8191bfd844daded8e1ec
- LSPV-2: 6ad6f04620a881918aecb8078ce2f2d1
- LSPV-3: 6ad6f05603248191abb281a5b43b3fc2
- LSPV-4: 6ad42a1f03448191b8ded0c1f2dfa791
- LSPV-5: 6ad42a2a9a088191ab9042245f3b4393

Disabling a schedule is not proof that an already-started execution was interrupted. Any legacy execution that sees this directive should stop its superseded assignment, preserve already-produced evidence, and avoid changing current ownership or allocation. New agents must recheck the latest directive before shared writes. The new task-ID registry will be posted to issue #3 after creation. Other projects are untouched.

## Shared research goal

Identify and prove, or decisively falsify, an unavoidable computational resource bottleneck for arbitrary correct uniform deterministic 3-SAT deciders. Prioritize the cost of establishing globally decisive SAT/UNSAT distinctions, the tradeoff between retained information and recomputation, and cost-sound abstract interpretation of actual machine computations. Do not assume that every solver enumerates assignments, constructs a proof in a particular calculus, or materializes all boundary states.

A successful endpoint could be a representation-independent superpolynomial lower bound, or a fully proved general polynomial-time algorithm that refutes a proposed bottleneck. Neither conclusion is presumed. The replacement itself establishes no new mathematical theorem. All new load-bearing claims start CANDIDATE/OPEN.

## Machine and quantifier contract

Let L be the bit length of a fixed explicit 3-CNF encoding. Distinguish L from the numbers of variables and clauses. Use one fixed finite uniform deterministic machine A across all lengths, with a fixed finite alphabet and a fixed finite number of work tapes. Declare the read-only input interface, head positions, endmarkers, malformed-input behavior, and all writable storage. Count actual transitions as time and all visited writable work cells as space. Include input rereads, indices, stacks, temporary representations, lookup construction, conversions, and recomputation. Random-access or word-RAM claims require a separately proved, quantitatively charged model translation.

The intended separation target is: for every correct total deterministic 3-SAT decider A, every integer k >= 1, every constant C > 0, and every L0, there exists a valid formula F with |F| >= L0 and T_A(F) > C(|F|+1)^k. The hard formula may depend on A, k, C, and L0. Do not invert these quantifiers or unnecessarily require a single recognizable all-UNSAT family hard for every solver.

Do NOT define the central uniform lower-bound objective by minimizing independently over all algorithms at each input length. A different enormous finite lookup program can be chosen for each length, so that pointwise minimum does not express the fixed-machine P versus NP question. An algorithm-dependent bound with the correct quantifiers is acceptable.

A small-space lower bound does not rule out all polynomial-time machines. Cover arbitrary polynomial workspace when needed, or explicitly exploit the same-machine fact that writable cells visited are bounded by transition count up to model constants. Time and space must be charged to the same machine and realization. Configuration counting gives capacity and halting upper-bound information, not by itself a lower bound on required time.

## Five roles and first deliverables

| Identity | Task title | Hourly minute, Pacific | Responsibility |
|---|---|---|---|
| TMR-1 | PNP Machine Model Lead | :00 | Exact machine model, quantifiers, bottleneck theorem, and dependency chain |
| TMR-2 | PNP Information Necessity | :12 | Information distinctions, input-aware indistinguishability, and valid communication transfers |
| TMR-3 | PNP Time-Space Tradeoffs | :24 | Retention, retrieval, recomputation, access costs, and joint resource inequalities |
| TMR-4 | PNP Cost-Sound Abstraction | :36 | Direct abstraction of full machine configurations and all-transition cost simulation |
| TMR-5 | PNP Machine Bottleneck Redteam | :48 | Independent falsification, model-transfer audit, and integrated proof synthesis |

The stagger is a scheduling convenience, not a barrier or guarantee that predecessor executions have finished. Each role works from the latest verified artifacts available.

### TMR-1: Machine Model Lead

Specify the fixed-machine resource model, both-label correctness, target quantifiers, encoding parameters, and exact dependency DAG. Formulate the weakest sufficient bottleneck lemma rather than declaring an equivalent form of P != NP to be progress. Maintain an explicit unrestricted-machine transfer obligation for every restricted result. First deliverable: a precise target and baseline model audit, including the per-length-minimization counterexample and a map of which proposed inequalities would exclude every polynomial exponent. Subsequently prove, construct, or falsify one concrete implication each run. Coordinate with TMR-5 rather than merely producing status reports.

### TMR-2: Information Necessity

Develop a notion of distinctions that a correct computation must acquire or recover, allowing arbitrary encodings, compact algebraic summaries, and adaptive input rereads. Investigate adversary, indistinguishability, communication, and crossing-sequence methods with their exact access restrictions. First deliverable: one explicitly scoped necessity lemma or minimal counterexample to a proposed one, plus the missing transfer to unrestricted multitape computation. A streaming state lower bound is not automatically a lower bound when the full input remains readable. The input itself has only L bits and the decision output has one bit: exponential semantic possibilities are not exponentially many independent input bits. Explain the actual computational obstacle, not only Shannon entropy or witness count.

### TMR-3: Time-Space Tradeoffs

Seek a quantitative same-machine tradeoff relating retained state, rereads, recomputation, and total transitions. Charge sharing, caching, adaptive layouts, repeated queries, address bits, all simultaneously live memory, preprocessing, and final output. Investigate relevant primary SAT time-space literature and pebbling/communication methods, keeping their hypotheses and limitations explicit. First deliverable: one proved restricted tradeoff or concrete failure of a candidate, and an exact account of the gap to arbitrary polynomial workspace. Do not repeatedly optimize an already-small-space exponent without a justified path to the all-polynomial target. A pebbling bound for one prescribed DAG does not bind an algorithm that computes a different representation.

### TMR-4: Cost-Sound Abstraction

Build abstractions of actual Turing-machine configurations and computations, not merely a selected legacy proof calculus. For each concrete initial state, provide a related abstract initial state. Every concrete legal step must map to an abstract path reaching a related successor at no greater cost, with correct SAT and UNSAT terminal labels preserved. All real executions must be represented. Derive abstract minimum decision-path cost <= concrete execution time. Prove a lower-bound potential with Phi(a) <= cost(a,b) + Phi(b) on every abstract edge and Phi(goal) <= 0, or give an explicit counterexample. Repeated states, zero-cost edges, input rereads, arbitrary tape encodings and program-dependent behavior must be covered. First deliverable: the exact simulation theorem and a nontrivial scoped instantiation or hostile failure, with the universal-machine coverage gap exposed. Do not define the unknown potential to be the desired runtime and treat that as a completed lower-bound proof. Refine only replay-proved spurious abstract paths; retain genuine cheap computations.

### TMR-5: Machine Bottleneck Redteam

Independently test the most consequential claim from TMR-1 through TMR-4. Seek a compact global invariant, alternate algorithm, reencoding, algebraic shortcut, reread/recompute strategy, or counterexample bypassing the claimed bottleneck. Audit uniformity, quantifiers, SAT/UNSAT correctness, all-transition inclusion, space scope, abstraction direction, and machine-model translation. First deliverable: a smallest reproducible falsifier or independent verification of a concrete new-team claim, followed by an integrated dependency update. Produce a rigorous repair where available, not only generic objections. Audit constructive polynomial-algorithm candidates as seriously as lower bounds. TMR-5 owns whole-document synthesis of root main.tex; its own substantive claims need another role's independent review before promotion.

## Shared falsification requirements

Mandatory relevant controls: 2-SAT, Horn, affine/XOR and Tseitin with Gaussian elimination, bounded-treewidth dynamic programming, disjoint products, shared subcomputations, padding, renaming, auxiliary variables, compact circuit/algebraic representations, and recomputation instead of storage. A difficult-looking family that has a cheap global invariant falsifies the proposed invariant if it predicts large time there.

No unrestricted conclusion from assignment count, configuration capacity, proof width/length, treewidth, prescribed-DAG pebbling, communication cost, or restricted circuit size without the precise model-preserving implication. No free oracle, uncharged truth table, length-dependent advice, unbounded-word unit-cost arithmetic, or assumed proof-system completeness/optimality. Treat ETH/SETH and cryptographic assumptions as conditional, never as unconditional premises.

A strict quasipolynomial runtime can be superpolynomial. A quasipolynomial upper bound alone or a fixed superlinear lower bound does not resolve the target. Report exact growth and quantifiers rather than labeling quasipolynomial and superpolynomial mutually exclusive. Do not assume the conclusion from the outset.

## Reading, evidence, and shared writes

Every run first reads this directive, BOTH root proof1.txt and proof2.txt, current issue #3 updates, root main.tex, AGENTS.md, CODEX.md, the repository pnp-research skill, and newest TMR handoffs. Survey the repository and read materially relevant original historical results and counterexamples, including legacy LSPV/Grok/Claude artifacts where relevant. Older scientific results remain evidence; older conflicting assignments do not regain authority. Primary-literature claims require fresh source verification and exact model/hypothesis citations. Do not inherit unsupported citations from chat.

The connector returned a SHA but a blank proof2.txt body during this transition. That does not establish that the stored file is empty. Recover readable authoritative contents before editing it. Never replace an unreadable tracker with a reconstructed summary.

Use role-owned reports research/agents/tmr-1/ through research/agents/tmr-5/, named with Pacific timestamps. Keep reusable code, experiments and immutable raw data separate. Maintain a compact latest handoff in each role directory. Reports must record the exact claim, dependencies, model, proof or counterexample, checked controls, sources, actual executed tests, status, publication status, and one next target. Use the existing strict scientific statuses. Finite evidence remains COMPUTATIONAL; no separation claim with an OPEN load-bearing arrow.

Each run should advance one substantive lemma, construction, counterexample, independent verification, or rigorous obstruction. Do not substitute a plan, another resummary of all history, or a restatement of P != NP. Keep Python invocations within 25 seconds when practical and at most the project 30-second chunking convention; checkpoint larger experiments and disclose unavailable execution.

Preserve proof1.txt for P=NP and proof2.txt for P!=NP. Update only material claims with full current contents and current SHA, conflict-safe merging, and full readback; otherwise report TRACKERS REVIEWED; NO MATERIAL CHANGE or the exact read blocker. Do not promote mathematical status solely because the team was replaced.

TMR-5 is the new synthesis owner of the one canonical root main.tex, preserving historical contributions and qualified statuses. TMR-1 through TMR-4 may edit only newly authorized TMR-owned regions after TMR-5 creates them; until then publish role reports and handoffs rather than editing old LSPV-owned regions. Do not create another main.tex. Preserve the historical source files and checker counterexamples without silently fixing or relabeling them.

Before publication save exact local outbox content where possible, refetch current state, merge concurrent changes, verify each published file by readback, and post a concise evidence/path handoff to issue #3. Never report a local-only artifact as shared. Missing or blocked reads/writes must be explicit and must not trigger destructive reconstruction. Never modify schedules or create more agents from a research run without a new user request.

Use GitHub-compatible $...$ and $$...$$ math in Markdown and simple standard LaTeX in chat. Use America/Los_Angeles timestamps with the correct daylight/standard designation. No em dashes or emojis in user-facing writing.

END_OF_DIRECTIVE::TMR_FIVE_NEW_AGENTS::2026-11-13_1249_PST

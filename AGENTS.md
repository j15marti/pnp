# AGENTS.md | Current P versus NP research strategy
**Effective November 27, 2026 (America/Los_Angeles). P versus NP remains OPEN.**

This section is the operative repository-wide guidance. It consolidates the latest user-authorized strategy; it does not establish a mathematical result or change any agent's schedule, identity, enabled state, environment, or manuscript ownership. The historical instructions reproduced below are subordinate to this section. In particular, their older source priorities, active-cohort counts, startup order, scheduling authorizations, issue numbers, and obsolete manuscript routing must not override the current directives.

## 1. Governing directives and order of work

Read these pinned documents at startup, with the newest common signed E/B source taking precedence over conflicting input priorities:

1. [Common signed E/B network feasibility and aggregate contraction](https://github.com/j15marti/pnp/blob/869007811cfe4a6b703e7f111111b820f3afcb03/research/coordination/shared-eb-2026-11-27/DIRECTIVE.md) — common native decision language, exact shared inputs, universal progress obligation, cost model.
2. [Shared UNSAT parallel-track directive](https://github.com/j15marti/pnp/blob/b1e93ffb3f7698009554e3a6fe19c20e0d06067a/research/coordination/shared-unsat-2026-11-27/DIRECTIVE.md) — original CNF corpus, empty guards, benchmark queue, paid reference verification.
3. [Communicating proof tracks and current roster](research/coordination/2026-11-27_COMMUNICATING_PROOF_TRACKS.md) — four distinct workstreams and certificate exchange.
4. [Public proof release gate, standing user instruction](https://github.com/j15marti/pnp/blob/fc87c43ad1a247e4133b931911f7cfa4afeb17c0/research/coordination/2026-11-27_PUBLIC_PROOF_RELEASE_GATE.md) — mandatory eligibility, review and public-release process.
5. Compatible scientific rules from the [both-directions directive](https://github.com/j15marti/pnp/blob/ef05e45509b1f8cfc53a1e13a40cdf56a29cec93/research/coordination/2026-11-26_MULTI_TRACK_PNP_BOTH_DIRECTIONS.md), [independent replica directive](https://github.com/j15marti/pnp/blob/4f0b145ab21ae1640a776a596f143c1de4a4865d/research/coordination/2026-11-26_1311_REPLICA_COOPERATIVE_PROOF_TRACKS.md), and [hybrid proof-gap directive](https://github.com/j15marti/pnp/blob/62f3c43eb7f15d7ef0813e3a8ea8bc7a95b4ca90/research/coordination/2026-11-26_1813_HYBRID_PROOF_GAP_DIRECTIVE.md).

Also read CODEX.md, .codex/skills/pnp-research/SKILL.md, current role-owned reports, relevant peer evidence, and the newest comments on [issue #328](https://github.com/j15marti/pnp/issues/328). Apply older operational guides only where compatible. Issue #328 is the active shared certificate exchange; #327 and #3 are historical coordination references, not substitutes for it.

## 2. One common NP-complete source and identical primary inputs

Use STRICT-EB4-v1, the native strict signed E4/B4 feasibility language authenticated by [RT01](https://github.com/j15marti/pnp/blob/e71b388635cd817b4fd3f641a3ab938ccdca906c/research/hcl201/red-team/2026-11-24_0140_RT01.md). Independently review the reduction before relying on its scope. A valid native instance is a finite simple undirected four-regular graph, with four distinct incident ports per vertex and vertex type E or B. Every port has a Boolean bit; an edge with sign s requires x_p XOR x_q = s. E requires all four local bits equal; B requires their **integer** sum to equal two. Do not replace B by XOR alone, or silently assume planarity, a supplied inverse compiler, free unary pins, dangling ports, degree-two nodes or parallel edges. Certified guarded residuals may differ from the original promise. Every transformation must preserve the appropriate decision/witness semantics or be a sound, explicitly directed negative certificate.

Every active agent begins each research run with both common native instances, in this order, same original bytes and IDs, guard EMPTY and residual ROOT. Use the pinned compiler, not an alternate encoding.

| Primary instance | Original native N (bits) | Vertices | B vertices | Authoritative native SHA-256 |
|---|---:|---:|---:|---|
| EB-JOINT-24 | 5363624 | 18931 | 788 | e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209 |
| EB-RANDOM-3CNF-40 | 5027816 | 17765 | 736 | 8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb |

Source pins:
- [Canonical instance registry, full SHA-256 identities and native/source-map/CNF lengths](https://github.com/j15marti/pnp/blob/0c14cdc57925788cf7a451dcd5aa171dce860f2c/research/coordination/shared-eb-2026-11-27/instance-registry-v1.json)
- [Original ordered CNF corpus](https://github.com/j15marti/pnp/blob/e315349cd6c1fe3fa696504859f28312f6aab69a/research/coordination/shared-unsat-2026-11-27/benchmarks.json)
- [Deterministic native compiler](https://github.com/j15marti/pnp/blob/21b9d53fb8166c819b24e708656c742cd3c24f10/research/coordination/shared-eb-2026-11-27/compile.js)
- [Reference CNF replay checker](https://github.com/j15marti/pnp/blob/1c4f25dabf9b6e2c715f9f2eaf71ebab397f5717/research/coordination/shared-unsat-2026-11-27/verify.js)

Use exact ASCII JSON.stringify({format,types,edges}) plus LF for native bytes, with N = 8 times byte length; vertex IDs and edge IDs are zero-based indices, port ID = 4v+j. Original ordered DIMACS bytes, variable IDs and one-based clause IDs remain unchanged for CNF comparisons. Verify full SHA-256, not merely a short alias or diagnostic FNV checksum. First perform native source-only discovery; separately attempt the corresponding pinned JOINT-24 and RANDOM-3CNF-40 CNFs and compare provenance-assisted and cooperative methods. Any compiler map, reference proof, imported result or encoding conversion must be identified, independently checked and charged; reference UNSAT labels are audit-only, never free solver advice. Gauge pins are allowed only with a proved symmetry or explicit guard. If generation, access or a run exceeds cap, preserve identity and report UNKNOWN. No substitution for either common input.

After both primary cases, use the shared queue (EQUALITY-CHAIN-8, PHP-4, TSEITIN-TORUS-3, ODD-WHEEL-5, CYCLIC-3DM-4, RANDOM-3CNF-24, then larger pinned instances, native compiled versions first when available). MFC-13 five-plane systems, reciprocal-fiber embeddings, November 26 replay, CHARGED-UNSAT-TRANSPORT1, cubic flow/coloring, strict T5 and older source families remain methods or secondary research only, with explicit faithful costed adapters to the common target when claimed.

## 3. Research objective and the exact OPEN universal theorem

Follow evidence toward either P=NP or P!=NP. The current research focus is UNSAT/NO instances and inconsistent guarded residuals. Prefer difficult post-closure NO instances with paid exact authentication; retain only minimal YES controls necessary to falsify unsound refutations. A candidate with a satisfying witness must be removed from the NO set. Stagnation, timeout, finite tests, and a label do not establish UNSAT.

The shared constructive obligation is to establish ONE uniform deterministic algorithm A on every valid native encoded input, with fixed polynomials p,q,r. Initialize a checkable nonnegative integer potential Phi on the **entire live residual, branch and shared-proof state**, with Phi(S0) <= p(N) in numeric value, not merely bit length. On every reachable unresolved state, obtain a correct terminal decision or a certified decision-preserving residual replacement/exhaustive guarded decomposition giving a strict global potential decrease of at least one, within q(N) aggregate bit work. Alternatively establish an explicit well-founded amortized recurrence with fixed polynomial total cost and fully charged neutral steps, credits, expenditures and replenishment. Keep all live obligations, not just a successful child or favorable replica. Prove polynomial intermediate representation, reverse witness maps, output and peak storage <= r(N), and charge cumulative memory on the same execution. Universal progress/coverage and the aggregate cost theorem are separate obligations. Neither is established by successful benchmarks.

For an UNSAT-only endpoint, a sound refutation algorithm with a proved uniform fixed polynomial time bound on **every NO input** suffices: only then can its timeout safely imply YES. Do not claim P=NP from a promise-only procedure or an arbitrary experimental clock. For P!=NP, exclude every fixed polynomial-time deterministic decider in the unrestricted standard model or prove an independently audited equivalent implication. Restricted proof-system, circuit, arithmetic, rank, matching/energy, representation or solver-portfolio obstructions do not imply unrestricted hardness. Keep decision, witness extraction and counting distinct. Report the first OPEN arrow explicitly.

## 4. Communicating tracks, independent replicas and genuine hybrids

Preserve existing workstream, title, identity, enabled state, schedule, environment and ownership. The November 27 communicating roster records 20 active agents in four workstreams and five paused reserves; treat that as a dated roster, not permission to change settings. Current saved task states control. Ordinary research runs must not create, reactivate, disable, reschedule or immediately rerun any agent.

- **T1:** local exact terminals — signed equality and balance occupancy, energy/plateau and flow, matching/Hall, wheel gluing, planar and cardinality terminals.
- **T2:** global representations — affine/bijunctive and bit projections, parity, syzygies/orientation, orbit quotients, separator interfaces and response bases.
- **T3:** deterministic replay, source-authenticated lifts, all-decider/resource transfer, precision and adversarial alternate representations.
- **T4:** global potential and branch credits, certificate DAG accounting, solver synthesis, independent audit and universal coverage.

Apply each specialty on identical native inputs. Run at least three independent copies before exchanging deductions: (A) local constructive/algorithmic; (B) complementary global algebraic/geometric/matching or contradiction/resource; (C) adversarial reconstruction and falsification. Use actual parallel execution only if available; otherwise disclose interleaving. Apply certified unconditional forced-information closure initially, after each verified import/deduction, and at stagnation. Preserve exact guards, original IDs, joint support and reconstruction. Do not merge independent marginal witnesses or confuse affine hulls with exact relations. At the first stalled dependency, try a genuine hybrid that changes another method's representation, invariant, admissible domain or acquisition cost. Compare standalone, imported and combined progress on the same declared caps; record failed approaches too. All lanes may use exact Gaussian elimination, exact 2-SAT, charged random access, and polynomial-dimensional/depth finite-precision attention; define uniform computation and arithmetic costs, not an oracle. No free semantic equivalence, SAT, counting or chart enumeration.

## 5. Shared certificate bus and exact exchange

Read [issue #328](https://github.com/j15marti/pnp/issues/328) and newest messages at startup, before consuming dependencies, and again before publication. Independently replay a peer's pinned proof/checker before using it. Reject mismatched guards and unverifiable claims; publish a concrete verified falsifier when appropriate. Reclose after importing. Broadcast newly verified, nonduplicate results promptly, with instance_id (full registry hash), original N, source/compiler/map pins as applicable, original IDs, exact guard and residual ID/version, claim and quantifiers, method/model/precision, parent certificate and message links, deterministic checker, certificate length/hash, scope, discovery versus verification costs, and potential change charging all children. Allowed evidence: verified witnesses, contradictions, safe contractions, forced bits, exact guarded incompatibilities, resource-bounded survival or refusal proofs, and credit-decrease proofs. Reference proofs are not new discoveries. Keep inconclusive work in timestamped role notes. Deduplicate by instance, guard, claim, model and parents; logical DAG sharing never makes separate physical replay free. Synthesis lanes maintain the checked dependency DAG and aggregate ledger. Coordinate through #328; do not overwrite peer work.

## 6. Accounting, literature, red-team and evidence

Apply CONTEXTUAL-ATTAINED-TARIFF: count actual attained candidates only via a paid extension oracle/verified terminal; otherwise charge exact joins or bounded branching. Fixed polynomial bounds must be in the original encoded bit length N on the same execution. Include parsing, authentication, preprocessing, all discovery, failed probes, every replica and logical branch, switching, arithmetic bit lengths, queries/accesses, maps, verification, communication, caching/recomputation, witness lifts, representation/output size, peak live space and cumulative memory. Parallel span is not total work. The optional 10^7 instrumented primitive events per case per run is a finite experimental cap, not a comparable bit-time metric or a proof of asymptotic termination. State unmetered work separately. Use a fixed polynomial aggregate budget for limited exponential kernels, not per-residual resets.

EVERY research run conduct bounded fresh task-specific searches of original literature (support and counterexamples/barriers), relevant j15marti/pnp reports/branches/issues, substantive public GitHub P vs NP attempts, specialist solvers/checkers, official Anthropic (including anthropics/formal-math), OpenAI (including openai/math), xAI, Google Research and Google DeepMind repositories. Read relevant original statements/proofs, exact hypotheses and inspectable arguments, not snippets alone. Record query, URL, version or actual commit/blob, applicability, scope, corrections, failure/no-result and review status. Distinguish an external claim, theorem statement, proof term, CI report, independently executed build, and faithful target formalization. Arithmetic complexity claims are not Boolean P vs NP dependencies absent a proved bridge. Never claim a build or review that did not occur.

Use 2-4 explicit falsifiers for each named obligation. Include applicable equality/affine, matching, cardinality, bounded-width joins, compact circuit, repeated-clause/padding, gauge/relabeling, joint guarded incompatibility, and growing post-closure NO controls. Retain DISJ, relativization, algebrization, Natural Proofs, simultaneous DTISP and deterministic-configuration checks with explicit applicability/status; never infer arbitrary machine lower bounds from restricted models. Label KNOWN THEOREM, PROVED WITH SCOPE (state independent-review status), COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, or FALSIFIED. Every report includes source/quantifiers, pinned dependencies, derivation or falsifier, actual tests and cost ledger, review status, safe peer handoff, first unresolved implication and one next lemma. Publish new timestamped owned reports with separate reproducible code/raw results where applicable. Recover full current file contents and SHA before existing-file edits; use conflict-safe writes, preserve peer and historical material, verify exact readback. If publication fails, preserve pending evidence and disclose failure. Keep current role-owned manuscripts; never infer new ownership from topic similarity. Retired proof.txt, proof1.txt, proof2.txt and legacy tracker/root write gates remain retired.

## 7. Public release gate

P versus NP is OPEN. Scoped lemmas, benchmark refutations, conditional frameworks and arithmetic-complexity claims are not completed Boolean proofs. Immediately bring a candidate full proof to issue #328 with pinned complete manuscript, precise theorem, dependency DAG, source/checker pins, open-gate audit and falsifiers; request actual independent reconstruction and adversarial review. Do not claim resolution until all load-bearing steps are established, substantive objections resolved, and independent mathematical review has actually occurred.

**Only after the standing release eligibility gate is met**, coordinate a single release owner and publish a new timestamped versioned release to [j15marti/pvsnp](https://github.com/j15marti/pvsnp): production-ready standalone LaTeX, bibliography and figures/build instructions; matching compiled and inspected PDF; supporting reproducibility code, checkers, input encodings, pins, seeds, data, checksums and limitations; independent audit and resource ledger. Fetch full public README.md and SHA, preserve history, add dated theorem/scope/status and proof/PDF/data links and build instructions, and verify complete commit and artifact readbacks. Disclose any failed review/build/upload or missing artifact. No public resolution claim or README announcement before gate and successful verification. The current E/B specification is a research framework, not a completed proof.

---

# Historical governance (preserved verbatim)

The following is the previous AGENTS.md body (blob 7476b8abf1df8a4e00d4eda0e4497bc083547773). It is retained for history and compatible safeguards only. Any older instructions about which directive to read first, primary sources, roster counts, scheduling/activation, issue routing, manuscript/tracker routing or proof status are superseded by the operative guidance above. Do not execute a historical scheduling authorization or reactivate reserves. 

# Current research redirection, November 27, 2026

Read [the communicating proof tracks directive](research/coordination/2026-11-27_COMMUNICATING_PROOF_TRACKS.md) first. It supersedes earlier track priorities, active counts and schedules, and preserves compatible ownership and scientific safeguards. All tracks consume and broadcast verified certificates through [issue 328](https://github.com/j15marti/pnp/issues/328). The earlier directives below are historical wherever they conflict.

# Current research redirection: 2026-11-26

The user's latest request assigns every P versus NP research agent a distinct obligation toward P=NP or P!=NP and requires literature, Anthropic, OpenAI and other substantive GitHub searches on every run, cooperative multiple-method work at obstructions, and constructive or contradiction proofs for individual lemmas.

Read FIRST [the multi-track both-directions directive](research/coordination/2026-11-26_MULTI_TRACK_PNP_BOTH_DIRECTIONS.md) ([initial verified revision](https://github.com/j15marti/pnp/blob/ef05e45509b1f8cfc53a1e13a40cdf56a29cec93/research/coordination/2026-11-26_MULTI_TRACK_PNP_BOTH_DIRECTIONS.md)). It supersedes conflicting older topic/source assignments and active-cohort counts while preserving compatible scientific safeguards, task identities, current schedules/enabled states, historical files and manuscript ownership. The current roster has 14 enabled agents and 11 paused reserves; paused reserves are not restarted by this redirection. All prior chat claims, including the proposed grid/overlap lemmas, retain candidate status until independently audited in a precise model.

Use the role-specific namespaces and handoffs in the new directive. Neither P=NP nor P!=NP is established by this assignment change. Ordinary research runs do not change task settings. The older governance below remains intact and applies where compatible.

---

# Research objective: follow the evidence toward P=NP or P!=NP

User clarification: 2026-11-21, America/Los_Angeles.

The objective is to resolve P versus NP in whichever direction the mathematical evidence supports. Either P=NP or P!=NP is an acceptable final outcome. Do not presuppose a separation or treat a valid polynomial-time algorithm as an outcome to avoid. Pursue the strongest rigorously supported route, including constructive algorithms, upper bounds, lower bounds, and counterexamples.

Treat current compulsory-work and lower-bound proposals as hypotheses to test. If preprocessing, compatibility aggregation, algebra, or a shared representation suggests a general polynomial-time solver, investigate that possibility and audit its full costs. Productive existing work can continue; this clarification neither requires equal time for both outcomes nor requires restarting investigations.

Apply the same proof standards in both directions. An algorithmic P=NP claim must establish uniform correctness on every permitted input of an NP-complete decision problem and a polynomial worst-case bound in the total encoded input length, including preprocessing, discovery, access, conversion, sharing, recomputation and output. A P!=NP lower-bound claim must exclude every fixed polynomial-time cap in the relevant unrestricted decision model. Any alternative route must establish the corresponding full implication.

Failure of a proposed lower bound does not prove P=NP. Failure of a candidate algorithm does not prove P!=NP. Keep counting and decision consequences distinct, and label restricted, conditional and open claims accurately. Report evidence supporting or challenging either outcome. The project remains unresolved until a complete argument is established.

This clarification takes precedence over any older wording that requires the final conclusion to be P!=NP. Preserve current roles, identities, schedules, enabled states, manuscript ownership, publication practices, mandatory literature and official-repository searches, and compatible scientific safeguards.

---

# Current charged UNSAT continuation: 2026-11-21

Read FIRST [the dynamic compulsory-work continuation](research/coordination/2026-11-21_CHARGED_UNSAT_DYNAMIC_CONTINUATION.md) and its linked charged UNSAT transport report. The user's latest request, "Direct and activate agents to continue this work," authorizes the coordinator to resume the six existing charged-research agents and request an immediate run while preserving their existing schedules and identities. This directive supersedes conflicting topic priorities and paused-state preservation instructions below; compatible scientific safeguards and ownership remain in force. Ordinary research runs preserve the resulting agent settings and do not alter the scheduler. The original protocol below is retained in full as compatible background.

---

# PNP agent protocol: end-to-end models and owned manuscripts

## Current research assignment: 2026-11-21

Read FIRST [the T5 resource-lower-bound assignment directive](research/coordination/2026-11-21_T5_RESOURCE_LOWER_BOUNDS_AGENT_ASSIGNMENTS.md) and its linked exhaustive handoff. The user's 2026-11-21 request assigns the six active PNP charged-research agents to this program. That directive supersedes older topic priorities and active-cohort counts where they conflict. It preserves the manuscript ownership table below and compatible scientific safeguards. The six charged roles use their own report namespaces and do not inherit a TMR manuscript by topic similarity. Preserve existing schedules and enabled states.

The older end-to-end directive below continues to govern compatible manuscript and publication practices. This update changes research assignments, not mathematical proof status.

Effective user authorization: 2026-11-15 15:10 PST, America/Los_Angeles.

Read FIRST [the end-to-end and agent-manuscript directive](research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md). It is the active coordination authority. Read the [SAT-compression scientific directive](research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md) for compatible A/B/C scope and scientific guards, but its earlier tracker/main reading and writing requirements are superseded.

## Living files and ownership

| Owner | Root living LaTeX manuscript |
|---|---|
| TMR-1 / PNP Machine Model Lead | main1_PNP_MACHINE_MODEL_LEAD.tex |
| TMR-2 / PNP Information Necessity | main2_PNP_INFORMATION_NECESSITY.tex |
| TMR-3 / PNP Time-Space Tradeoffs | main3_PNP_TIME_SPACE_TRADEOFFS.tex |
| TMR-4 / PNP Cost-Sound Abstraction | main4_PNP_COST_SOUND_ABSTRACTION.tex |
| TMR-5 / PNP Machine Bottleneck Redteam | main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex |

Edit your assigned file in place, creating it only if absent. The role number is stable, not a run counter. Do not overwrite a peer manuscript. TMR-5 maintains cross-track synthesis in main5 and sends peer corrections through handoffs/issue #3.

STOP normal-run reads, edits and reconciliation of proof.txt, proof1.txt and proof2.txt. Preserve them untouched. Root main.tex and older main-number files remain historical references, not required active trackers or write gates. Do not delete, rename or overwrite historical files. No old preflight, task or handoff may restore those retired requirements.

## Work selection

Favor a complete encoded-input-to-output construction or correctly scoped model transfer. Each run must advance or falsify a named dependency in one selected end-to-end pipeline. Isolated toy variants, assertion counts, repeated easy counterexamples and coefficient retuning are not sufficient progress. Partial results are welcome when their integration point and unresolved premises are explicit.

TMR-1: source/formalization verification and complete compiler/solver/hierarchy transfer. TMR-2: actual-source transformations and execution-sensitive invariants. TMR-3: virtual checkpoint/graph access plus improved evaluator with complete resource costs. TMR-4: faithful costed compiler/model transfer preserving sharing and adaptive behavior. TMR-5: independent reproduction of full chains and ranked synthesis.

## Research and publication

Use CODEX.md and .codex/skills/pnp-research/SKILL.md. Read your manuscript completely, relevant peer manuscript sections, current handoffs, issue #3 and original evidence. Survey the repository for duplicates, contradictions and pending draft branches. State exact quantifiers/model and 2-4 falsifiers; consult primary sources. Preserve source authentication, both-label/counting semantics, uniformity, all legal compact shortcuts and SAME_REALIZATION time/space. Charge discovery, all accesses and queries, conversion, switching, failed work, caches, sharing, retention, recomputation and output. Networks use total work and aggregate space.

Every candidate has DISJ, relativization, simultaneous DTISP and deterministic-configuration gates with explicit status. Retain algebrization/Natural Proofs and all applicable easy-family/wrapper controls. No unrestricted runtime claim from rank, multiplicity, encoding size, prescribed DAG or restricted proof/circuit complexity. /341 FAIL as full UNSAT authority; /386 RESTRICTED. P versus NP remains OPEN.

Use KNOWN THEOREM, PROVED/EXACT, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED with scope and independent-review status. Finite tests are not asymptotic proofs. Preserve source versions, code revisions, seeds, exact raw data and unexecuted-check disclosures. Individual Python stages should finish in about 30 seconds.

Maintain a coherent manuscript with current target, model, dependency chain, proofs, full resource ledger, gates, controls, references, evidence and one next lemma. Detailed timestamped reports remain under research/agents/tmr-i/; code and raw results stay separate. Use prose or item[] for LaTeX lists. Update compact handoff.md and issue #3 after verified publication. If no material manuscript change, say MANUSCRIPT REVIEWED; NO MATERIAL CHANGE, not TRACKERS REVIEWED.

Before an existing-file write, recover the entire current body plus SHA. Merge conflicts without destroying others' work, use branch/current-head leases, verify complete readback and report draft/merge status accurately. Missing content blocks only that overwrite, not research. Preserve an exact pending report and handoff instead. Retry transient failures once after checking current state; never invent unavailable scientific content or executed tests. Diagnose predecessor publication failures without blocking your own run or changing schedules.

The five active TMR identities/titles/enabled states and hourly Pacific offsets are unchanged. Do not create, revive, disable, duplicate, reschedule or immediately rerun agents as part of ordinary research.

The previous AGENTS.md is preserved byte-for-byte at research/governance/archive/2026-11-15_PRE_END_TO_END_AGENTS.md (original blob 8f477279a014b4e2fd61544fe9e53f9a6d25d70f). It is historical; conflicting priorities and mandatory reads/writes there do not apply. This file changes governance, not mathematical proof status.

## Mandatory literature and official-repository searches on every run

User directive: 2026-11-21, America/Los_Angeles.

Every research agent must perform a fresh, task-specific literature search on every run, aimed at its current target lemma, obstruction, algorithm, or model-transfer gap. Search for supporting results and counterexamples or barriers. Read promising primary papers and check their exact hypotheses before importing a theorem.

Every run must also search relevant public GitHub repositories from Anthropic, OpenAI, xAI (Grok), and Google, including Google Research and Google DeepMind where relevant. Verify official ownership rather than assuming a repository using a product name is official. Search for applicable algorithms, SAT/CSP and counting methods, theorem proving, formal verification, circuit complexity, information-transfer techniques, and reproducible research code as appropriate to the assigned task. Use web search as a fallback when connected GitHub search lacks access or coverage.

Record queries, sources and links, paper versions or repository commit IDs when inspected, relevance to the named dependency, exact scope, and the resulting proof attempt, test, counterexample, or reason for rejection. Report no relevant results and access failures honestly; never invent findings. Use prior search logs to avoid redundant deep reviews while still performing fresh searches. Repository code and empirical results are clues, not proofs of unrestricted asymptotic lower bounds. Keep searches bounded enough to advance or falsify the assigned lemma during the same run.

Preserve current roles, schedules, enabled states, manuscript ownership, and scientific safeguards.

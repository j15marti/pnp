# Two proof spines: persistent research instructions

Authorized by the user on 2026-10-07. Repository: j15marti/pnp.
Root main4.tex is the achievable-region (ARC) manuscript. Root main5.tex is the concrete recursive WRAPPER manuscript. These are detailed route manuscripts; main.tex remains the existing overall dashboard. This explicit user request authorizes maintaining main4/main5 in place. Do not overwrite unrelated main.tex ownership regions or reactivate unrelated teams.

## Scientific memory

P versus NP remains OPEN. Assume P=NP only inside the contradiction argument. A finite achievable SAT pair exists, but no SAT-specific contraction has been established.
ARC route: R consists of joint time/space exponent pairs witnessed by one uniform exact algorithm each. The forbidden region is t+s<2 cos(pi/7), subject to exact Williams model/encoding matching. Candidate closure V(y)<=lambda V(x)+c, fixed lambda<1, c/(1-lambda)<gamma, would imply finite crossing. Different algorithms can witness successive pairs. Universal source-code compilation is NOT necessary. Matrix variants require nonnegative maps, a downward-closed forbidden region, and controlled slack. The SAT-specific closure is OPEN.
WRAPPER route: a uniform exact inner procedure emits at most M^(a+o(1)) children of encoded size M^(b+o(1)), b<1, with all local work M^(c+o(1)). Regeneration, representation access, combination, workspace, and effective error bounds must be charged. PRF3-0018 conditionally yields C=max(c,a/(1-b)) and subpolynomial space under its full hypotheses. Explicit-child implementations may instead use sigma=max(s,b), provided their actual access and storage model justifies this. Endpoint C+sigma<gamma. Inner general-SAT construction is OPEN. Double wrappers, parallel portfolios, disjunctive covers, backdoors, and macro-merges are candidates, not established universal shrinkers.
Aggregate compression: D_r=2^k/product G_i=2^(k-x), x=sum log2 G_i. Polynomial residual count requires x>=k-d log2 N. Raw assignment counts are not machine lower bounds. Current-scale calls to a hypothetical N^K SAT solver retain K unless a separately proved improvement changes that cost.

## Team

LEAD: ARC and main4.tex owner; existence-level quantifiers and potential/closure mechanisms.
PROOF: WRAPPER and main5.tex owner; explicit reducers, double wrappers, parallel/disjunctive mechanisms, charged access and recursion.
RESEARCH: primary literature and historical repository results; exact theorem transfers and duplication search.
RED: independent falsification, smallest counterexamples, time-space/model/quantifier/relativization/algebrization audit.
WRITE: synchronization, manuscript reconciliation, reproducibility, repair and independent verification.
All five must do literature review, GitHub review, build/formalize at least one model, and run a bounded test every run. A model can be a precise mathematical countermodel; if code cannot run, record that as an execution blocker, not a completed test.

## Every-run procedure

Read this protocol, main4.tex, main5.tex, AGENTS.md, CODEX.md and the repository pnp-research skill. Follow its relevant preflight and research workflow. Survey repository paths/history and read materially relevant old and new sources, main.tex, main2/main3 if relevant, tasks, peer reports, governance, and cited raw experiments. Do not rely solely on old summaries. Record what was actually accessible.
Identify one highest-value open arrow, exact quantifiers, model, same-realization object, and weakest useful theorem. Search current primary literature before substantive work. Record source URLs, theorem numbers, hypotheses, and limitations. Check one appropriate cross-domain transfer where relevant; distinguish theorem transfer from analogy.
Build or revise a concrete candidate/model, attempt to falsify it, and execute at least one reproducible relevant test. Use exact arithmetic where practical and seed random tests. Test easy SAT families, source-carry/current-scale-call escapes, padding, independent products, and oracle/algebraic replacement as relevant. Do not infer asymptotics from finite tests.
Every Python invocation must be designed for <=30 seconds. Use a 25-second cooperative budget and roughly 30-second hard subprocess timeout. Split larger work by seeds, sizes, parameter ranges, or checkpointed stages; persist partial output and resume. Never increase timeout to avoid splitting.
Write code, raw outputs and interpretation separately. Each new run gets an immutable report research/agents/<role>/YYYY-MM-DD_HHMMSS_<ROLE>_<runid>.tex, with start and end markers, reviewed sources, proof attempt, status, tests, failed controls, open arrows, and one peer handoff. LaTeX uses prose or item[] entries rather than bullet glyphs. Cite spines.bib or add verified BibTeX entries.
Reconcile BOTH main4.tex and main5.tex every run against the new evidence. Update the relevant argument/proof/ledger, and add a concise dated review entry to the other manuscript if unchanged, stating no mathematical status change. Do not pad the mathematical exposition with repetitive log text; detailed history belongs in reports. Preserve all unrelated content and labels. No OPEN arrow may silently become PROVED. Refetch current blob SHA immediately before each write; merge concurrent edits instead of overwriting. Compile when available; record compilation blockers. Verify every upload by reading it back.

## Local records and GitHub failure recovery

Before network writes, create local research/local_logs/<role>/<timestamp>_<runid>.json and an exact-body outbox research/outbox/<runid>/. Record target path, base blob SHA, body hash, status, test command/results, and write error. Start with state=RUNNING and finish with VERIFIED or PENDING_SYNC. Check prior local logs if the environment shares them; never assume another scheduled runtime shares this disk.
On transient failure preserve identical bodies, wait about 30 seconds if supported, refetch target, and retry once. A stale SHA requires a fresh read and a content merge. Do not bypass permissions/authentication/safety denials or change publication targets to evade them. A blocked write remains blocked and must be reported accurately.
If GitHub remains unavailable, preserve the exact outbox in persistent storage when available and authorized by the user's artifact request. Record its resolvable location and digest. Local scratch alone is NOT guaranteed cross-run storage. To communicate across isolated runs, append a bounded SHARED_FALLBACK_LOG entry (run ID, blocker, status, preserved artifact location, next action) to this five-agent team's automation prompts using automations.peek/update. Refetch each prompt first, preserve all other instructions and schedules, deduplicate by run ID, and never claim a body was recovered from a summary.
At startup inspect predecessor/peer reports and pending fallback entries. Repair a peer's stalled write or narrow technical/procedure bug when evidence supports it; preserve scientific scope and attribution. After two missed verified cycles, diagnose exact tool error/path/SHA/prompt conflict. Small technical prompt repairs are authorized; do not change schedules or scientific objectives without a separate user instruction. Never invent missing research. Successful synchronization closes the fallback entry with verified path and commit/blob SHA.

## Status and reporting

Allowed scientific labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED. One load-bearing OPEN arrow means no separation proof. Every run ends with concise result, manuscript changes, test results, write verification or explicit failure, and next target. Negative results and rigorous corrections count as progress.

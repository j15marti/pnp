# LSPV-2/375: Uniform source-prefix compiler, five-role handoff

**November 3, 2026, 17:12 PST.** PROVED/EXACT elementary theorem, including inherited exact LSPV-2/341 minima; COMPUTATIONAL independently checked finite controls; external review pending. P versus NP OPEN. Rmix341 rules/weights, agent task ID 6ad6f04620a881918aecb8078ce2f2d1, enabled state and schedules unchanged.

## Concrete scoped result

Start with Urquhart (JACM 1987) and Ben-Sasson--Wigderson (JACM 2001) exponential **ordinary DAG Resolution** lower bounds on appropriate odd expander Tseitin CNFs, NOT unrestricted SAT computational hardness. The unchanged mixed calculus has a previously proved exact minimum of 4h-1 paid nodes for connected bridgeless cubic odd-charge sources.

A single, all-general-valid-CNF, uniform polynomial-time source-preserving compiler E authenticates the complete odd bridgeless cubic parity-quartet grammar. If accepted, append new fresh opposite source units (z) and (not z); if not, append only (z). All old clauses and occurrences remain as original prefix. Recognition is sound; E preserves SAT and UNSAT labels, gives unique satisfying extension in the benign branch, and is clause-prefix reversible on canonical DIMACS. Malformed sources are rejected. Outputs cost O(N) bits and require full charged parsing/verification/writing. This compiler is NOT an Rmix341 derivation step.

For every member of the earlier exact family:

$$
W_{R_{\mathrm{mix341}}}(F_h)=4h-1,\qquad
W_{R_{\mathrm{mix341}}}(E(F_h))=1.
$$

The output has the two authenticated opposite units and a one-RES-step empty clause. No zero-node contradiction exists. Thus **source-clause preservation + polynomial-time uniform reversible label-preserving compilation does not preserve minimum paid logical DAG cost**. This is a restricted falsifier of an overly extensional/source-prefix representation-invariant minimum-node lower bound, NOT a superpolynomial all-algorithm lower bound.

The previously established LSPV-3/377 12h opposite-label source-sign neighbors imply a deterministic label-preserving compiler operating on its fixed-width sign grammar must read every such sign on the odd input. Even an output proof of one node does not render those bit operations, source authentication, or output writes free.

## Computational controls

Python producer: **861 checks**. Separate independent JS checker: **1,103 checks**, six corrupted fixtures rejected. Four standard graphs: K4, K3,3, cube, Petersen with h=4/6/8/10, source clauses m=16/24/32/40, prior exact native paid cost 15/23/31/39, output exact paid cost 1 each. **336** one-sign-change benign-branch controls, even-charge SAT controls, general-CNF SAT/UNSAT/tautology/empty/duplicate controls, nine malformed strings rejected. Python host 1.51 s / 96,908 KiB RSS; JS 0.12 s / 30,708 KiB RSS. No native TM/FLMV bound and no new globally shortest proof search.

## Corpus and Grok/Claude

Read verified November 2 12:04 directive at blob 033b54b87b7cbe94912af5cf67daa52859143a07, issue #3, AGENTS.md, CODEX.md, repo skill, LSPV-2/341/372/373/374, LSPV-3/377/378, LSPV-4/347/371, and LSPV-5/289/324. **Duplicate firewall:** LSPV-5/289 already has recognizable both-label input islands; LSPV-5/324 already has uniform source-prefix encoders E_k exposing absence of a common polynomial; LSPV-2/372 rules out semantic-only proof-cost invariants. The increment is one uniform all-general-CNF compiler and same fixed Rmix341 exact native-cost drop with physical accounting.

Actual repository folders were listed: `GROKPROOF/` and `research/agents/claude/`. Read Grok `GROKPROOF/2026-11-03_2214_PROGRESS.md`, SHA `59fe73c20473bd6bc20500cf58d75e42519aee88`, and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, SHA `1f9fc727d3e2b009cba7afec2a93beb62959dd67`. Grok universal all-input charged contraction is OPEN; Claude's barrier is in a restricted alternation-trading rule grammar, not B3. Claude 0266's separate critical review was checked. No result is imported as an unrestricted SAT lower bound.

## Exact publication outbox

- `research/agents/lspv-2/2026-11-03_1712_LSPV-2_UNIFORM_SOURCE_PREFIX_COMPILER375.md`
- `experiments/arc/lspv2_375_source_prefix_public.js`
- `results/raw/arc/2026-11-03_1712_LSPV2_UNIFORM_SOURCE_PREFIX_COMPILER375_public.json`
- `research/coordination/2026-11-03_1712_LSPV2_UNIFORM_SOURCE_PREFIX_COMPILER375_FIVE_ROLE_HANDOFF.md`

Full Python producer, separately written JavaScript verifier and complete fixture JSON are in the conversation's reproducibility archive. The repository JSON is a public ledger, not the full fixture. The public compact JS was **retrieved from GitHub and executed**, passing K4/K33/cube and four malformed controls.

Local full checkout unavailable, so repository preflight.py and reports checker were not run. No task or schedule mutation. Root main.tex reconciliation should use the full recovered Git blob and current SHA with ownership-only edits, or document a failure and preserve original.

## Next shared gap

Do **not** promote a representation-invariant low node count into SAT runtime hardness. Seek a *single common polynomial* lower-bound cost-reflection envelope across source-authenticated paid circuit/GF(2)/extension transformations while retaining full encoded evidence, construction, checking, source bit access and peak live space. Separately prove B3:

$$
\mathrm{SAT}\in P\;\Longrightarrow\; \overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$

B1, B2, B3, superpolynomial Wbar_Rmix341, and P versus NP are all OPEN.

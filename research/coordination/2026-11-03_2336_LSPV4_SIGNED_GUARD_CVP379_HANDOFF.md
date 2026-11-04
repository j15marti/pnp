# LSPV-4/379 to five PNP research roles

November 3, 2026, 23:36 PST. **PROVED/EXACT within an explicitly specified subproblem; B1/B2/B3 and P versus NP OPEN.**

## Result

Guard-dependent signed conservative AND2 definitions in the fixed R_mix341 fragment form a P-complete constant-restriction acquisition problem even when the only public input is guard t. Given a topologically ordered DAG of paid gates z_i=(signed earlier input) AND (signed earlier input), the output bit after t=1 is P-complete by a uniform logspace reduction of Circuit Value: assigned input constants -> t/not t; AND -> signed AND2; OR -> complemented signed-AND2 output; NOT -> sign toggle. Evaluating the DAG is polynomial, not superpolynomial. This strengthens the resource audit of LSPV-2/381, but neither invalidates its polynomial-time proof transport nor supplies SAT hardness.

Complete read-only annotations for each gate enable O(log M) writable-space, O(M^3) time checking by rescans; producing the correct annotations from unannotated evidence is P-complete. Eager cache O(M) space / O(M^3) time; uncached depth-d recursion O(d log M) scratch / O(2^d M^3) time. Neither schedule is automatically an FLMV contraction. If an unannotated uniform logspace generator returned all correct gate constants, then L=P, which is OPEN. No unconditional logspace lower bound is asserted.

## Verified controls

Deterministic code experiments/arc/lspv4_379_signed_guard_cvp.js, raw results/raw/arc/2026-11-03_2336_LSPV4_SIGNED_GUARD_CVP379.json. 166 circuits x 8 assignments = 1,328 source cases; 2,656 output-forcing CNFs, 1,328 SAT / 1,328 UNSAT; 4,384 gate records; 9 malformed rejects; 5,322 assertions; K4 even/odd charge 8/0 models. Code uses no external packages. Report research/agents/lspv-4/2026-11-03_2336_LSPV-4_SIGNED_GUARD_CVP379.md.

## Direct next actions

LSPV-1: retain B1/B2/B3 quantifiers and avoid claiming a generic normalization lower bound. LSPV-2: audit whether signed-AND2 restriction uses eager gate values or alternate logspace rewrites; do not presume all gate annotations free. LSPV-3: extend the guarded typed compiler proof to GF(2), AND3 and named-wire LOCAL-CONVERT only if each semantic equivalence/implicate is independently and efficiently witnessed. LSPV-4: evaluate chosen normalization schedules in the indexed FLMV machine including preprocessing rho, source query heads, actual gate memory and proof-output access. LSPV-5: try to find a legal R_mix341 operation that bypasses the assumed normalizer, and independently verify the exact signed-AND2 CVP reduction.

## Current external assessment paths actually inspected

Grok: GROKPROOF/2026-11-04_0720_PROGRESS.md blob 06304e87e03b707fd7930f3b2c5a43d0c9c0cf9b, all-input fully charged contraction OPEN.

Claude: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a; restricted sequential/portfolio results, no B3.

Peer: research/agents/lspv-2/2026-11-03_2312_LSPV-2_GUARD_DEPENDENT_AND2_RESTRICTION381.tex blob 671d56bfb6448ee6867b053169967e4e2bdb01b6, proof is polynomial-work and linear-space as stated; our result does not dispute that.

Main.tex safety: an authenticated bounded fetch reported blob 491477d17dfb5fef794bb2963a8c55118fd5f10a with empty textual body; no root manuscript modification attempted. No tasks, titles, enabled states, schedules, inference grammar or weights changed. B1/B2/B3, superpolynomial worst-case mixed derivation cost and P versus NP remain OPEN.

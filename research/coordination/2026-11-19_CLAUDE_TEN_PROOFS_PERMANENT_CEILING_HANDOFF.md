# Claude routine handoff: ten-proofs permanent formula bound, source audit and method ceiling
2026-11-19. P vs NP OPEN. No TMR manuscript, task or schedule modified.

KNOWN THEOREM (upstream Lean, sorry_count 0, axioms propext/Classical.choice/Quot.sound; our kernel/Comparator check
UNEXECUTED): openai/ten-proofs@94bc0feb Permanent.lean: any division-free C-formula for per_n has >= n^4/(128 log2 n)
variable leaves (192 with division), n >= 32; i.e. N^2/(64 log2 N), N = n^2. Kalorkoti-style blocks of 2 clog2 n matching entries.

COMPUTATIONAL: independent Jacobian-rank-mod-p check of the block coefficient TD lemma, n = 7,8,13,14, two seeds:
certified TD = 2^(2 ell), i.e. saturates its ceiling (>= claimed m^2). experiments/claude/perm_block_td_20261119.py,
results/raw/claude/2026-11-19_perm_block_td.json.

PROVED (mine, unreviewed): for ANY multilinear N-variate target, the block-TD method yields at most N^2/(4 floor(log2 N)).
So it is within ~16x of its ceiling and cannot pass N^2; no Boolean SAT/#SAT transfer exists in the needed direction.
Use as a hostile ceiling control for any block rank/transcendence invariant (TMR-2/TMR-4) and as a pinned
source-ledger entry (TMR-1). Not load-bearing for the strict-C or DTISP chains.

Next lemma: characteristic-free (GF(2)/GF(p)) version of the block TD lemma, or a proof it fails.
Report: research/agents/claude/2026-11-19_TEN_PROOFS_PERMANENT_FORMULA_SOURCE_AUDIT.md

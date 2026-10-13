# COMPLETIONCUT1 verified handoff

Status: CANDIDATE with complete elementary proofs; independent review pending. P versus NP remains OPEN.

Report: `research/agents/lspv-4/2026-10-14_0717_LSPV-4_COMPLETIONCUT1.tex`
Commit: `c32e8c6686d8e63ca7fbcf9a78c7877d5fcda6f1`
Blob: `b660e75c459f1ccd3cdcda7d1000da6d44cade07`
Required header and final sentinel read back. Full local bytes match the Git blob.

Code: `experiments/review/completion_cut_audit.py`
Commit: `add22beec4031fab6dd9d676ff2f61b10778c3ed`
Read-back blob: `239dc90e90cc78a9b77c1264fd79a59dc0390326`, matching full local bytes.

Summary: `results/raw/review/2026-10-14_0717_completioncut1_summary.json`
Commit: `98ec412ee6cb8dba82cd2bb9d0ae94deb29f11d5`
Read-back blob: `caad8bed97026a15d1f229686a4257b41ebde4d7`

Root update commit: `548ba44b73cb4d445c989866051e7c60a8595f49`
Before blob: `0fa921347e299dea1c7dff375de924ca5c1c05cd`
After/read-back blob: `7010b69ba7493418c4e8d437926a9c88ba391414`
The complete current root was staged and hash-verified. Every byte outside the LSPV-4 ownership region was preserved. All ownership markers and OPEN status were checked; the local amended root compiles. No full-checkout preflight or repository-wide CI is claimed: direct git access failed DNS resolution. No schedules or automations changed.

The six-page standalone PDF was rendered and visually inspected. The conversation's exact reproduction ZIP includes the full code, three raw result JSONs, report, SHA-256 manifest, and before/after root snapshots for audit. ZIP size 116008 bytes; SHA-256 `32f37027dd12ba5bc8f9f9c52e8054af91e849895cc1d0eed8c86887f1b78de2`. All 11 manifest entries verified. This note does not claim a new Drive upload.

## Result and boundary

Completion-time freshness contributes actual source acquisition and a bound on precommitted values. For M causal programs with q precommitted guesses of ell fresh bits, union success is at most M*q*2^(-ell), even with different stopping times on a common stream. That is not a bound on compact post-release programs and does not make a common stream one common static SAT input. Exact replay of live randomness requires the sampled blocks, not code/input alone.

Clock-free semantic event laws can be identical even when same-stream paths differ. The test exhausts 4096 twelve-bit streams: fast/slow paths differ on 4032 (63/64), while logical transcript distributions agree. Timestamp-fed hashes are excluded from that law and fail the equality control. Early-compute/wait controls match the entire semantic completion record. The 15820 assertions are COMPUTATIONAL, not a SAT runtime lower bound; logical work/wait counters are stipulated protocol costs, not measured machine instructions.

## One next target

Use the actual two-tree/residual response consumer. Substitute a different correct witness or compact post-challenge evaluator and identify a mandatory semantic failure beyond the metadata hash. That source-matched necessity theorem is not established here. Preserve the older compilers and proof-model scope, and do not promote chronology to nonrelativization.

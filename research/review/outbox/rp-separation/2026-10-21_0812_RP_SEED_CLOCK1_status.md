# RP-SEED-CLOCK1 | 2026-10-21 08:12 KST

P versus RP OPEN. P versus NP OPEN.

A uniformly polynomial-time public seed list H_n of at most n^c n-bit strings cannot hit every RP verifier. The explicit verifier for the easy language of all strings rejects exactly H_n and accepts other tapes, giving success 1-|H_n|/2^n >=1/2 for sufficiently large n. The language remains trivially deterministic.

Every polynomial-time RP verifier reading at most c log n independent fair bits has a deterministic polynomial-time exact simulation by exhaustive tape replay and OR. This includes adaptive completion-time reads when all sampled bits are accounted for.

A single random assignment is not an RP SAT solver on unique-witness formulas: success is 2^-n.

Executable local audit: 64,486 assertions, zero failures. Raw SHA-256: cb7823e3947981c6588e8b585ab514a4027ada820aec450f78b2115aed389fae.

Historical recovery is PARTIAL, not exhaustive. Missing: original prime-lineage scripts and full WRAPPER archive. Next task for :36 and :48 reviewers: check machine-specific seed selection, unrestricted coin budget, and deterministic bypass before accepting any separation claim.

Status: scoped exact lemmas only; no P versus RP resolution.

# LSPV-5/413 handoff — historical /341 checker recovered and scoped

**2026-11-07 09:01 PST | Route B | affected IDs [P2-D1], [P2-L5-412] correction, [P2-L5-413] | P versus NP OPEN**

## Actual advance

Commit archaeology recovered and exactly replayed the historical /341 producer, 197,514-byte proof/source packet, independent verifier and 30,714-check record. The producer output is byte-identical to the committed packet, and the verifier output is identical to the committed record.

The verifier implements exactly two inference tags:

- original clauses are internally coerced to 'factor';
- 'AND3': 'factor × factor -> factor', with an exhaustively checked optional affine alias;
- 'XOR': two row-bearing parents -> 'affine'.

It rejects 'RES', 'LOCAL-CONVERT' and 'DEF' as 'unknown rule'. Thus it authenticates the original source/AND3/XOR certificates but is not the full declared $R_{\mathrm{mix341}}$ parser and cannot decide RES -> AND3.

## Correction

[P2-L5-412]'s sentence “No official historical checker ran” is false. The corrected statement is: the exact historical restricted checker ran, but no authenticated full mixed checker or accepted RES-to-AND3 record was found. The TAGGED/EXTENSIONAL ambiguity survives only for the unimplemented cross-rule composition.

## Exact historical chain

- producer commit 'c3e8eb6a...', blob '4081022e...'
- raw commit 'a0645529...', blob 'fe27fe10...'
- verifier commit '45945352...', blob 'fcb7d4ce...'
- verification record commit '5d80c973...', blob '42ba4cad...'
- report commit '2d1dd3a...', blob 'c87acd35...'

## Artifacts

- 'research/main/2026-11-07_0901_MAIN_HISTORICAL_341_CHECKER_SCOPE_REFEREE413.md'
- 'experiments/review/lspv5_413_historical_341_checker_audit.py'
- 'experiments/review/verify_lspv5_413_historical_341_checker.mjs'
- 'results/raw/review/2026-11-07_0858_LSPV5_HISTORICAL_341_CHECKER_AUDIT413.json'

## Remaining gap

[P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Next target is one historically authorized full mixed parser or one authenticated accepted packet in which a RES-produced clause is consumed by AND3. No restricted proof lower bound is promoted to full mixed hardness or P-versus-NP resolution.

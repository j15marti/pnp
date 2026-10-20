# ARC-BOUNDARY-ONEWAY-GLUE6 independent review (hourly check, 2026-10-20 ~20:00 Asia/Seoul)

Status: P versus NP remains OPEN. Nothing here strengthens any claim.

## Corpus reviewed
Last ~40 commits (all 2026-10-20), root main.tex (192 lines), UNIFORMITY_BRIEF, EXPONENT-EXTRACTOR-FIREWALL21 status, ARC_BOUNDARY_GLUE6 status/script/results.

## Finding 1: the published checker does not test the load-bearing equivalence
`experiments/review/2026-10-20_arc_boundary_glue6_minimal.py` asserts `(a==c)==all(bitwise equal)`, which is a tautology, and `len(set(synopsis))<8` for values in range(4), which is pigeonhole by construction. The SAT-level claim "conj satisfiable iff vectors match" is never solved.

## Finding 2: the claim itself holds (COMPUTATIONAL, restricted)
`experiments/review/2026-10-20_2000_arc_glue6_bruteforce_check.py` solves all 5b variables exhaustively. Result: b=1,2,3 give 4+16+64 = 84 pairs, 0 failures; both blocks individually satisfiable; conjunction satisfiable iff a==c. Runtime ~6 s (chunked by b; b=4 would need 2^20 assignments x 256 pairs, so split it by pair ranges if wanted).

## Classification
The b-bit one-way lower bound is the deterministic one-way communication complexity of EQUALITY (KNOWN THEOREM). The gadget is an exact instance transfer of it to proper 3-CNF, with a CNF split along the shared variables. Per the status file, it does not bind random-access (FLMV) algorithms. It is therefore an interface no-go for irrevocable left-first summaries, not progress toward a lower bound on SAT. The load-bearing ARC compiler arrow stays OPEN.

## Suggested next step for the ARC line
Test the same split against *non-equality* separators: the pin gadget reduces to EQ, which is the hardest case for one-way summaries but the easiest for randomized hashing (O(log b) bits with public coins). State explicitly whether the target model allows randomized or advice-assisted summaries; if it does, this no-go evaporates.

## Housekeeping observation
Root main.tex carries ~hundreds of near-identical "independent Grok review ... confirms" lines in the executive box. These are annotations, not evidence. LSPV-5/MAIN could collapse them into one line with a count and date range. I did not edit main.tex (ownership rule).

% END_OF_VERIFIED_REPORT::ARC-GLUE6-REVIEW::2026-10-20_2000

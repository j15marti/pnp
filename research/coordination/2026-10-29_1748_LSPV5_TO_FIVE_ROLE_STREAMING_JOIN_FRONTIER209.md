# LSPV-5 additive handoff: streaming-join frontier referee 209

Timestamp: 2026-10-29 17:48 America/Los_Angeles  
Role: LSPV-5 independent red team / synthesis  
Status: **P versus NP remains OPEN.**

## Verified artifacts

- Standalone report: `research/main/2026-10-29_1748_MAIN_STREAMING-JOIN-FRONTIER-REFEREE209.tex`, commit `30bda09631a8e1ec876ffda63a1a3e947b1c3068`, readback blob `dbce9946596af3bb9b79a0d372612131c48b63b2`.
- Reproducer: `research/main/2026-10-29_1748_STREAMING_JOIN_FRONTIER_REFEREE209_repro.py`, commit `6078eb7f3422cde61585582d5356b0c632aa3996`.
- Raw results: `research/main/2026-10-29_1748_STREAMING_JOIN_FRONTIER_REFEREE209_raw.json`, commit `4ad0cc74f63d47b82175ea249e12056ad6cdcdaa`.
- Root synthesis: `main.tex`, commit `3daee6cefe8d44e2b9bb9e21fcc6d8f1482cd156`, readback blob `d2d6f26bee127a0e9472cc0a9765aa9154a92ab7`; 170159 characters, one header, one sentinel, one balanced ownership-marker pair for each LSPV-1 through LSPV-5, and explicit OPEN status.
- Recovery record: `research/governance/2026-10-29_1748_REPEATED_ROOT_TRUNCATION_RECOVERY2.tex`, commit `867e4d12f58b81ebfa4dd6c8d158cf69e3994919`.

## PROVED/EXACT scope

For a parent that must retain all completed child summaries, child `i` having stored size `s_i` and computation peak `M_i`, an order `pi` has

`P_live(pi) = max(max_r(sum_{l<r} s_{pi_l} + M_{pi_r}), sum_i s_i + j)`.

Nonincreasing `M_i-s_i` is optimal for arbitrary fanout by adjacent exchange.

For `h` child relations that are all explicit `B`-bit tables on the same interface, with a parent defined by pointwise intersection, one accumulator gives

`P_fold(pi) = max(M_{pi_1}, B + max_{r>=2} M_{pi_r}, B+K)`,

and a maximum-`M_i` child first is optimal.  Time is `Theta(hB)`.  For the exact star control `M_i=s_i=B` and a separate `B`-bit parent output, all-live peak is `(h+1)B`, while folding uses `2B` for `h>=2`.  If `h=N^{mu+o(1)}` and `B=N^{beta+o(1)}`, both have time exponent `mu+beta`, but their space exponents are respectively `mu+beta` and `beta`.

Therefore the all-live weighted schedule is an exact frontier only under its storage contract; it is **FALSIFIED/RETIRED as a representation-independent Pareto frontier**.  This is an upper-bound architecture result, not a SAT lower bound.

The finite checker completed in 1.405 seconds: 840 arbitrary-fanout all-live permutation checks, 840 streaming permutation checks, 45 star coordinates, 36 balanced-tree coordinates, and 144 SAT/UNSAT semantic common-interface cases.

## Dominated-crossing firewall

In LSPV-2's affine-profile family, `B(k)-A(k)=k(2w+10h-1)>0` and `A(k)<D(k)` throughout the declared range.  Hence the numerically correct dense/BDD crossing at `k=3` is absent from the global lower envelope because the affine representation dominates both curves.  Pairwise equality is not by itself a Pareto crossing.

## Peer audit obligations

1. **LSPV-3:** state the storage contract beside every weighted scheduling theorem; add fold/recompute/on-demand alternatives before calling an envelope a frontier.
2. **LSPV-2:** publish `connector231.py` or remove the hidden dependency from the GitHub reproducer; preserve canonical-recognizer versus arbitrary-renaming scope; apply the dominated-crossing firewall.
3. **LSPV-1:** add current required report markers and charge exhaustive pair-separator discovery; do not promote adhesion-two closure to arbitrary adhesion.
4. **LSPV-4:** keep the `q=0,1` points as structural/proxy points unless realizability and a matched algorithmic resource measurement are supplied; its current report correctly keeps the runtime bridge OPEN.
5. **All roles:** a short representation must be paired with a charged discovery/access/replay procedure on the same execution.  Do not combine independent time and space maxima from different runs.

## Root recovery

The pre-run root was a 15446-character truncation with no final sentinel.  Git history identified the last full verified source at commit `f3c898ddf242f2fecf3e208e396f84a55ca7867c`; two later partial replacements were not used as scientific synthesis.  The recovery preserved recorded authorship and OPEN status, then reconciled only verified specialist artifacts and this report.  No missing manuscript prose was invented.

## Next exact lemma

Prove or falsify a mixed-message fold theorem in which child summaries may be bijunctive clauses, affine row spaces, or bounded exceptional tables.  The target must give a polynomial-size canonical combine operation, projected lookup, witness/certificate replay, and a same-run access-aware `(T,S)` bound including representation discovery and failed choices.  A pure common-interface bitwise intersection is not sufficient.


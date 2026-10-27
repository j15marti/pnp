# ARC201 PCP-SEED-UNION-FIREWALL201 | five-role handoff

Date: 2026-10-27 05:00 PDT. Owner: LSPV-1 Formal Proof Lead.
Status: Restricted aggregation theorem PROVED under its explicit uniform indexed verifier premises; independent peer review pending. Universal affordable certificate coverage, arbitrary-K ARC contraction, ARC-EDGE-90 and P vs NP OPEN. No task, role or scheduling changes.

## New exact arrow

A randomized binary-proof verifier with R(N) <= N^(rho+o(1)) seeds, per-seed time N^(v+o(1)) and simultaneous indexed workspace N^(s+o(1)) with a completeness/soundness gap can be made into one globally SAT-sound deterministic proof verifier by testing ALL seeds and thresholding. Its proof-cell observation budget is the union across ALL seeds and both hereditary levels, using exact physical proof-store and bit-address keys.

If every ordinary UNSAT F has one successful proof with this GLOBAL union <= (a+o(1)) log_2 N, ARC200 first-read enumeration constructs one deterministic ordinary-SAT indexed solver with T <= N^(max(1,rho+v+a)+o(1)) and S <= N^(s+o(1)). Williams' verified subpolynomial-space native SAT lower bound forces rho+v+a >= 2cos(pi/7) = 1.8019377358... when s=o(1). This is a necessary condition only. For positive s, use FLMV/Buss-Williams in their precise native strict range, never blindly extend the cosine endpoint.

## Exact falsifiers

A full-source-matched proper signed exact-(2,2) W1 family has 20 clauses, 15 variables, model counts (772,272,272,0). A valid randomized promise checker accepts every SAT W1 mode at one seed despite SAT-side soundness error 1/R; existentially choosing that seed invents an UNSAT certificate. Its UNSAT execution reads only ONE bit per seed, but R distinct physical bits in the complete all-seed transcript. Exhaustive artifact: 6,278 assertion groups, zero failures, R=2..8.

## Files and verification

- Role-owned full LaTeX: research/agents/lspv-1/2026-10-27_0500_LSPV-1_ARC_PCP_SEED_UNION_FIREWALL201.tex
- Executable: research/agents/lspv-1/2026-10-27_0500_ARC201_PCP_SEED_UNION_repro.js
- Raw: research/agents/lspv-1/2026-10-27_0500_ARC201_PCP_SEED_UNION_raw.json
- Root: main.tex, LSPV-1-owned section only after report readback.

## Assignments within the existing five agents

LSPV-2: Build source-to-physical-proof-locator rank/select for multiple seeds and children, charging output and aliases.
LSPV-3: Formally quantify the global union of queried proof cells over all seeds and two hereditary levels, plus SAT/UNSAT semantic soundness and construction.
LSPV-4: Audit fixed-machine seed enumeration, epoch resets, exact Williams/FLMV native model and strict exponent inequalities.
LSPV-5: Independently falsify one-seed existential acceptance, physical alias reuse, premature stopping, and uncharged proof advice.

## Predecessor technical write-readback observation

The latest substantive LSPV-5 PHYSICAL-ALIAS-AGGREGATION179 report at research/agents/lspv-5/2026-10-27_0444_LSPV-5_PHYSICAL_ALIAS_AGGREGATION179.tex is readable and has a substantial proof and raw evidence, but its final marker is END_OF_REPORT::PHYSICAL-ALIAS-AGGREGATION179 rather than the AGENTS.md prescribed END_OF_VERIFIED_REPORT::LSPV-5::<RUN_ID>. Request a role-owned sentinel reconciliation/readback, without reconstructing or overwriting the peer's scientific body. The discrepancy alone does not invalidate its mathematics.

END_HANDOFF::ARC201_PCP_SEED_UNION

# Five-role handoff: LSPV-2/420, nonlinear-gate-parameterized exact semantic support

November 5, 2026, 08:12 PST. All roles, weights, task IDs, enabled states and hourly schedules unchanged. **P versus NP OPEN; B1/B2/B3 OPEN.**

## New restricted result

Given an explicit, conservative paid two-input DEF-DAG with E encoded bits, output cone k nonlinear truth-table gates and a syntactically active original coordinates, the full set of essential source coordinates can be decided in **O(a * 16^k * poly(E+1))** bit operations and polynomial peak space. Proof: for each input coordinate compare C(x) vs C(x xor e_j); guess the 4 input bits of each nonlinear gate across the two executions, then test up to 4k+1 linear GF(2) constraints. Every consistent branch produces a genuine witness, every witness gives a consistent branch. Hence for k=O(log E) even exact **semantic** support recognition is polynomial-time, unlike the unrestricted-k coNP-complete paid DEF-prefix recognition established already by LSPV-2/406, /414, /419 and LSPV-3/382. This is a restricted parameter theorem, not a new full-R rule or B3.

## Falsifiers, evidence, provenance

Paid-cone-only algorithm and independently authored full truth-table evaluator were committed, retrieved via authenticated GitHub and executed in the JavaScript V8 research runtime. Producer 1,287 assertions across 1,282 circuits; separate oracle 2,291 checks; sparse nvars=10^9, XOR cancellation, repeated inputs, dead nonlinear gates, SAT/UNSAT guard, malformed inputs covered. Initial live/dead-gate and independent oracle bugs were caught, fixed and both code paths rerun. Exact source links:

- Report: research/agents/lspv-2/2026-11-05_0812_LSPV-2_FPT_NONLINEAR_SUPPORT_GRAMMAR420.md
- Producer: experiments/arc/lspv2_420_fpt_semantic_support.js (blob 1cd475d4fe4f741f5d05dcf6511b75ac20ea6de9)
- Independent: experiments/arc/lspv2_420_fpt_semantic_support_independent.js (blob 9aa69d8ff1916f827e1214a77b545247d45530e6)
- Raw: results/raw/arc/2026-11-05_0812_LSPV2_FPT_NONLINEAR_SUPPORT420_raw.json

Mandatory IDEA -> SEARCH -> ITERATE: original /341 blob c87acd11, November 2 /1204, issue #3 through REFEREE364, AGENTS/CODEX/skill, own 406/414/419, peers LSPV-1/419, LSPV-3/424, LSPV-4/415, LSPV-5/363+364. Actual GROKPROOF/2026-11-05_1428_PROGRESS.md blob a0e35e77, Claude TPORT-0002 and ONETAPE-0001 inspected. Indexed primary research Haken, Cook ER, Raz-Tzameret, multiplicative complexity/Soeken, Gwynne-Kullmann; OpenAI GitHub Lean ExecCNFNodeSearchCosts blob 1ced21f4 fully read. Direct branded Google unavailable; indexed web used, no false claim of a direct Google session.

## Crucial firewall, assigned next work

**LSPV-1, B3 lead:** This semantic circuit-subroutine does *not* turn a polynomial-time decider reject bit into native R_mix341 evidence. B3 SAT in P => polynomial Wbar same R requires an independent proof, no assumption of polynomial native certificates or formalized decider correctness.

**LSPV-2, builder:** Require exact original /341 LOCAL-CONVERT public vs private wire, DEF facet selection, AND3 support and GF(2) operand typing before promoting any circuit support check to a proof inference. Attempt a nested paid DEF+GF2+AND3+LOCAL *source-authenticated* compiler and test the first unauthorized export. Use the FPT checker to reject false support tags; pay all physical checking.

**LSPV-3, hypergraph/certificates:** Verify that the definition-to-port interface permits the necessary globally unique owners; preserve nonlinear and high-width affine relations, do not erase sparse GF(2) into only <=3 factors. Owner-closed reindexing from REFEREE364 required.

**LSPV-4, resource auditor:** Distinguish t paid DEF nodes vs O(a16^k poly(E)) checking work vs input acquisition and actual materialized peak memory. A huge DIMACS header does not justify huge dense arrays; parser must use arbitrary-precision decimal IDs and active dense indices. Maintain s'<=max{rho,eta,lambda,lambda*s} and rho>=1 for copied full evidence.

**LSPV-5, adversarial reviewer:** Independently attack the two-copy guessed-nonlinear-input linearization, especially reused inputs, dead gates, scalar constants and public-wire support claims. Original grammar remains incomplete; do not promote a conditional syntax as historical native R.

Haken's lower bound applies to standard ordinary shared-DAG Resolution PHP, NOT ER or full mixed R. Cook's ER PHP proofs and Raz-Tzameret's XOR shortcuts are countercontrols. No full-R hardness or P!=NP inference.

## Publishing safeguard

Original root main.tex fetch returned nonempty Git blob 1b8a7d9a1514b06c96501849a7902b7aa3dae2a1 but empty content, even with a line-range request. No partial/unsafe overwrite of main.tex or another specialist region was attempted. This handoff asks LSPV-5 to reconcile from a complete verified blob if available. All existing schedules, roles, weights and artifact history preserved. Next run should use the exact native grammar and work on full source-authenticated proof translation, not repeat generic support hardness.

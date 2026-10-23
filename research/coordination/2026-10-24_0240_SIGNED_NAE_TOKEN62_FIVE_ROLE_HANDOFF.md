# SIGNED-NAE-TOKEN62: five-role coordination, 24 October 2026 KST

Verified standalone report: `research/agents/lspv-2/2026-10-24_0240_LSPV-2_SIGNED_NAE_TOKEN62.tex`.

**PROVED/EXACT restricted:** For unique proper signed exact-(2+,2-) 3-CNF, maximize complementary full-sign clause pairing across all four sign-pattern orbits. The exact declared-calculus defect is t_pm = m - 2 sum_{S, {p,~p}} min(c_{S,p},c_{S,~p}). It is computable and source-checkable in O(m log m), and t_pm <= DUALPAIR61 monotone-only t. Original variables participate in <=2 NAE pairs.

**PROVED/EXACT restricted constructive:** When t_pm=0, signed NAE constraints of source-degree <=2 have an explicit O(m^2+n) token-walk source-witness algorithm. Every step flips a single named original variable and repairs the current BAD triple, and each walk terminates before revisiting an earlier support.

**FALSIFIED/RETIRED:** Global signed-gauge reducibility is not necessary. The mixed-sign frustrated prism C_h x K_2 has n=3h, m=4h, t_mono=4h, t_pm=0, and an inconsistent edge-sign gauge parity around a cycle. Every member is SAT and has a quadratic certified witness.

**Both-label control:** The strict exact-(2,2) 198-variable/264-clause Doeker UNSAT source with Role 4 TWO-SIGN-SWAP64 SAT repair is a genuine fixed-language matched pair. Its earlier source certificate was imported but NOT rerun this run. The separately executed ordinary 8-clause UNSAT cube and 7-clause SAT controls are outside the exact occurrence promise.

**COMPUTATIONAL:** 132 strict SAT prism cases, 7,840 source clause replays, 1,120 trace flips checked, 140 auxiliary general degree-two NAE controls (1,176 flips), 18,432 brute-force assignments. Zero assertion failures. Full stdlib audit SHA256 80c8b42310e456eec1d9ec268c73119c3be273853c8f642cccd8f4ecff23f9a3.

Roles 1 and 3: the old monotone-only defect is not minimal among complementary signed source pairs; use t_pm. Role 4: stress the signed degree-two token proof on frustrating cycles, loops prohibited, named variable-sharing and UNSAT controls. Role 5: integrate the exact restricted result while preserving OPEN all-decider arrow. All: challenge any claimed transfer from optional representation, flip trace, or symbolic nonemptiness service to mandatory time.

**First missing lemma, OPEN:** For one fixed NP-complete signed exact-(2,2) source grammar and *every* uniform deterministic exact decider, prove either a polynomial-time all-input symbolic continuation or superpolynomial unavoidable charged work. The SAT-only root quotient remains two-state, so rich context processing is not mandatory. No change to existing schedules or tasks.

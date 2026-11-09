# LSPV-2/517 five-role handoff | 2026-11-09 03:17 PST

Route A. New restricted proof-chain evidence [P2-L2-517], refining [P2-L2-516] and controlling [P2-L2-515], [P2-L4-515], [P2-L4-516]. [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04] OPEN. No modification to rules, weights, task identities, schedules or 2A/3B role allocation.

**Result:** The signed-Tseitin **original strict proper-3CNF** charge family of any connected cubic G with n even vertices has k=n-1 independently switchable charges and 4n signed ternary clauses. Charge j toggles exactly four first-literal source sign bits, and no other packet bit. Its SAT label equals even total charge. In contrast to LSPV-2/516's unique-UNSAT selector, this parity-of-source-bits family forces ANY deterministic all-input correct SAT decider to READ at least one sign from each of k charge groups on EVERY source; otherwise flipping an unread charge leaves its observed input unchanged but reverses its answer. Therefore rank(V_R)=k and all 2^k complete input-read-value traces are pairwise different, for any such decider. The previously published semantic affine-coset bound k-h_f gives only 1 here because parity's monochromatic affine cosets have dimension k-1. The strengthening arises from the physical INPUT-bit coefficient rows being limited to {0,e_j}.

**Independent implementation:** Python original-packet DPLL: 680 decoded sources, 340 SAT/340 UNSAT, 11,140 assertions; independent JS Gaussian elimination plus 50,944 exhaustive local parity-facet checks: same classifications, 9,793 assertion groups. K4, triangular prism, cube and pentagonal prism were finite controls, NOT asymptotic hard certificates. The general construction includes published odd-charge expander-Tseitin ordinary Resolution-hard instances but grants polynomial GF(2) solution, so there is no general computation lower bound, native R_mix341 transfer or FLMV contradiction.

**Artifact paths:**
- research/agents/lspv-2/2026-11-09_0317_LSPV2_LOCAL_CHARGE_PARITY_READ_FIREWALL517.md
- experiments/arc/lspv2_517_parity_access_independent.js
- results/raw/arc/2026-11-09_0317_LSPV2_517_LOCAL_CHARGE_READ_RAW.json
- this handoff
- separate Python reproducibility archive in the run history.

**Role-specific:** LSPV-2 retain A-dependent all-input construction priority; LSPV-4 audit this access-information floor against native indexed skip and all-phase source/evidence costs; LSPV-1/3/5 may treat this as restricted trace-cache control only, not proof-system hardness. Recent topology link/SAT handoff is candidate only. Next work should seek a compiler beyond complete-trace replay and prove recursive same-FLMV-machine application. Root main.tex full retrieval unavailable, so it was not edited.

**TRACKERS:** P2-L2-517 requires a material proof2.txt addendum after current-head optimistic merge and full readback; proof1.txt unchanged unless separately proven necessary. P versus NP OPEN.

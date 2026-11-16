# TMR-5 current handoff | 2026-11-15 19:48 PST | WR056 BIT-PHP EXTENSION COLLAPSE + merged W̄_R line

**Authority / ownership:** end-to-end directive first; compatible SAT-compression constraints; shared worst-case objective W̄_R(N), Bridge(R): SAT∈P ⇒ W̄_R ≤ poly. Owned root `main5_PNP_MACHINE_BOTTLENECK_REDTEAM.tex` only, reconciled in place. Previous main handoff (/055 nonaffine Williams, blob 0dca4272c2e1f9813d7dc670965b0fc375abd9ed) archived byte-exact at `research/agents/tmr-5/archive/handoff_pre_2026-11-15_1948.md`. Unmerged branch-line handoff /055W (blob cf87de92de2ed60516ba29c462a63b50e5b80243) archived byte-exact at `archive/handoff_055W_unmerged_branch_4oyies.md`. Retired proof trackers, historical root main, peer main1..4 and the five schedules are untouched. **P versus NP OPEN.**

**Merged into this branch:** the previously unmerged W̄_R line, /053 (ysu7ts) and /055W (4oyies).
- Theorem A: Bridge(R) ⇔ P≠NP for every R with a known superpolynomial lower bound.
- Theorem B: the open arrow is T-provable correctness of a poly-time SAT algorithm.
- Theorem C: componentwise hardness is FALSIFIED by the switch composition (F∨z) ∧ (G∨¬z).
- Corollary D: an R_comb with extension is ≥_p EF.

**NEW Theorem E, PROVED/EXACT (KNOWN ingredients: Cook 1976, BKS 2004; independent review OPEN).**
- Claim: BPHP^{n+1}_n (n = 2^k, N = Θ(n³ log n)) has an explicit ER refutation with (3/8)n⁴ + O(n³) RUP lines and n(n+1) + (n+1)n(n−1)/3 conservative extensions. Total size is O(N^{5/3}).
- Contrast: the same family is KNOWN exponential for Res, Res(k), Sherali–Adams and CP (2^{Ω(n^{1/4})}, Beame–Whitmeyer ICALP 2025), and CANDIDATE exponential for DAG Res(⊕) (Braun arXiv:2609.23015, unverified). SoS is KNOWN polynomial.
- Verdict: bit-PHP does NOT survive compression or definitional DAG sharing in R_comb. No family is known to be hard for EF.

**Executed (CPython 3.11.18, deterministic):**
- Code: producer rev `tmr5-bitphp-er-collapse056.v1`, independent checker rev `tmr5-er-rup-checker056.v1`.
- Results: n = 2, 4, 8, 16, 32 all PASS with 0 failures; the largest case has 403,095 RUP lines and 11,968 extensions, checked in 19.8 s.
- Controls: 6/6 corruption controls rejected at n = 2 and at n = 4; generated counts match the closed forms; brute-force UNSAT holds for n = 2 and 4.
- Raw: `results/raw/tmr/2026-11-15_1948_TMR5_BITPHP_ER_COLLAPSE_WR056_PY_RAW.json`.
- Not run: preflight, LaTeX build, DRAT-trim, Lean.

**Gates:** DISJ N/A; relativization N/A (unconditional upper bound, no separation claimed); DTISP N/A to proof size; configuration counting PASS as an upper-bound guard. /341 FAIL, /386 RESTRICTED.

**Machine-model line (unchanged from /055):** C3 nonaffine Williams image is PROVED/EXACT RESTRICTED, with a two-bit forward simulator that falsifies nonaffinity-as-hardness. The Lean MainResults rebuild remains OPEN for independent TMR-5 review. TMR-1/058 reports FinTM2 physical stack transfer as closed in restricted form; TMR-5 has not independently reviewed it.

**Artifacts:**
- main5 (owned);
- `research/agents/tmr-5/2026-11-15_1948_TMR5_BITPHP_EXTENSION_COLLAPSE_WR056.md`;
- `experiments/tmr/tmr5_bitphp_er_collapse056.py`;
- `experiments/tmr/tmr5_er_rup_checker056.py`;
- the raw JSON above;
- the two archives;
- the /053 and /055W files imported from their branches.

**ONE NEXT LEMMA:** in R⁻_comb = DAG Res(⊕) + CP (clause interface, no definitions), decide whether BPHP^{n+1}_n has polynomial refutations. Build Braun's Lean artifact independently before using its bound.

END_OF_HANDOFF::TMR5::2026-11-15_1948_PST

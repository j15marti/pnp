# RESTART-RACE-CUTFLOW110 handoff

**Status:** P versus NP remains **OPEN**.

## New exact adaptive upper simulation

Role 3's simultaneous two-child SAT race can be implemented with serial geometric restarts. At budgets `1,2,4,...`, run each child from its initial configuration, discarding the guest state between runs, and stop only on a computed SAT answer.

If `t` is the faster SAT-child runtime, the charged guest work is `<8t`. Only one guest configuration is live, so peak guest space is the **maximum** truncated child space plus `O(log t)` counter bits—not the sum of both child states. Across self-reduction stages this preserves `O(nM+n T_A^+(M))` SAT witness time while improving the space ledger.

## Conditional transport inequality

Any compatible all-witness-generator lower bound `L_wit(F)` would imply

`T_A^+(M) >= (L_wit(F)-c_A n M)/(c_A(n+1))`.

Only a positive numerator transfers. No unconditional superpolynomial witness-search lower bound is known; proving one would already settle a central FP/FNP consequence.

## Independent peer audits

- **CUTFLOW85:** its crossing-splice proof and `(k-1)(k-2)/(sigma+1)` arithmetic are valid in the declared one-head local-source model. It yields `Omega(k+k^2/(s+1))`, but interleaving or random access gives `O(k)`. This is a layout-sensitive polynomial time-space bound, not an unrestricted SAT theorem.
- **CANCEL-JOIN69:** counts and source quotas replay: `n=6q`, `m=8q`, `2q` complementary pairs, `4q` unmatched ternaries, raw backdoor `h=q`. Paid tautological Davis-Putnam elimination collapses the trajectory to binary 2SAT in polynomial work.
- **SAT-SIDE-RACE77:** label-specific timeout dualization is exact but equivalent to the corresponding P-vs-NP statement, not independent separation evidence.

## Computational audit

- 235,720 assertion-accounted checks, zero failures.
- 87,380 equality cases through `k=8`.
- 49,152 restart-race controls; worst charged/fastest-SAT ratio `6.876923 < 8`.
- SAT FORCE and contradictory UNSAT controls.
- CUTFLOW arithmetic through `k=1024`.
- CANCEL-JOIN structural replay through `q=16`.

## First missing lemma

After complete random-access source acquisition, prove a decision-oriented continuation lower bound for every total uniform adaptive decider, with positive transport remainder. It must not require witness output or a fixed representation and must survive restart racing, SCC/Horn/affine rules, Davis-Putnam cancellation, learning, caching, recomputation, direct decision and label-asymmetric stopping.

## Files

- `research/agents/lspv-5/2026-10-24_0948_LSPV-5_RESTART_RACE_CUTFLOW110.tex`
- `research/agents/lspv-5/2026-10-24_0948_LSPV-5_RESTART_RACE_CUTFLOW110_HANDOFF.md`
- `research/agents/lspv-5/code/restart_race_cutflow110_audit.py`
- `research/agents/lspv-5/results/RESTART_RACE_CUTFLOW110_raw.json`


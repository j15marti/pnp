# LSPV-3 STRICT3-UP-BACKDOOR354 | November 2, 2026, 22:53 PST

**PROVED/EXACT (symbolic, fixed Rmix341); COMPUTATIONAL (two-language controls); B1/B2/B3 and P versus NP OPEN.** Same five task identities, roles, enabled states and hourly offsets unchanged.

## New family exclusion and exact structure

Let F_n be the n-variable implication cycle with two opposite long clauses P=(x_1 OR ... OR x_n) and M=(NOT x_1 OR ... OR NOT x_n), for n>=4. For n=5,6 this matches the authentic Peitl--Szeider sources (up to clause order). The family is already known as an easy-to-refute implication cycle, not a new hard-source discovery.

Lift uniformly to **proper distinct-literal width-exactly-three CNF T_n** by (i) replacing each binary implication E_i with (E_i OR g) AND (E_i OR NOT g) using ONE common global g; and (ii) replacing P and M by ordinary private OR chains. Then

- v=3n-5 variables; m=4n-4 indispensable clauses; 12n-12 individually sensitive signs; explicit N=Theta(n log n) bits.
- **Exact minimum strong UP-backdoor cardinality = 2**: every assignment to {g,x_j} makes UP refute the residual, but any one assigned variable leaves all original width-three clauses at width >=2.
- **4n-5 <= W_Rmix341(T_n) <= 5n-7**. First inequality is source indispensability plus fixed binary-premise ancestry. Upper certificate uses *only ordinary Resolution*: n guarded edge reconstructions, 2(n-3) OR-chain reconstructions, 2(n-1) implication-chain unit derivations, one final contradiction. The global mixed-system optimum is not claimed.

The added project-specific theorem is the minimal/sign-sensitive strict-3CNF conversion with exact constant UP backdoor and completely replayed fixed-system proof upper. Strong backdoors and Peitl fixed-clause extremal sources are established literature. This is a **FAMILY FAILURE**, not a separation or B2/B3 failure.

## Adaptive proof-frontier compiler

For any complete adaptive binary assignment tree whose UNSAT leaves each have a verified **pure Resolution** refutation with q_l nodes, guard-lift source clauses and resolve opposite branch literals. This yields W_Rmix341(F) <= sum_l q_l + (number of branch nodes). The generic resolution simulation is standard. **Mixed GF(2)/AND3/VARDEF guard-lifting is not proved**; do not assume it.

## Independent checks and resource distinctions

Seven sizes n=4,5,6,8,12,20,32. Python full producer, separate no-import Node referee (1188 assertions PASS), and independently replayed compact GitHub code. Source deletion witnesses: 320; sign flips: 960; successful size-two partial UP branches: 348; all 452 size-one UP branches fail to contradict; malformed source fixtures rejected: 28; invalid Resolution certificates rejected: 14. Entire unsatisfiability exhaustively checked n<=6, otherwise syntactically certified. Opposite-label odd/even K4 parity models 0/8. For n=32: source 12072 DIMACS bits, 124 source clauses, exhibited 153 RES nodes; its *minimum* could be smaller.

Source bits, derived logical node count, proof evidence, eager verification reads, hindsight proof-selection cost and host process memory are separate. No native same-machine FLMV inequality is asserted. All-phase rho retains every local phase, including temporary materialization.

## Duplication, literature and exact next gap

Read 12:04 five-role contract, issue #3, AGENTS, CODEX, pnp-research skill, current tree and authentic Peitl DIMACS, LSPV-5 REFEREE304, LSPV-3 prior SPLIT353, LSPV-4 backdoor and selector notes. Primary literature: Peitl--Szeider IJCAI 2021, Williams--Gomes--Selman IJCAI 2003, Dreier--Ordyniak--Szeider JCSS 2024, and Cai--Li arXiv:2610.02047 (October 2026). GitHub/openai searches for SAT/Resolution produced no reusable fixed mixed-system checker.

**Next high-value target:** a genuinely interacting nonaffine family lacking constant/log strong UP or Horn/2SAT backdoors, with mixed-rule/charged-extension-resistant **superpolynomial MINIMUM derivation cost**. Separately establish B3 for the same preselected R, not merely an arbitrary trace simulator. P versus NP OPEN.

## GitHub artifacts, verified source

- [Formal report](../agents/lspv-3/2026-11-02_2253_LSPV-3_STRICT3_UP_BACKDOOR354.tex)
- [Standalone Node producer/replayer](../../experiments/arc/lspv3_354_strict3_up_backdoor_compact.js)
- [Machine-readable raw ledger](../../results/raw/arc/2026-11-02_2253_LSPV3_STRICT3_UP_BACKDOOR354_public.json)
- Local full Python producer, no-import Node independent verifier, actual proof scripts, source-deletion witnesses and all raw results in user-facing archive lspv3_upfrontier354_repro.zip.

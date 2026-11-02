# LSPV-5 to five-role handoff: RANDOMIZED-PIN-QUERY-REFEREE276

**November 1, 2026, 16:48 PST. Status: PROVED/EXACT restricted randomized bit-query theorem; independently COMPUTATIONAL; P versus NP OPEN.**

## Exact result

On the same valid connected canonical \(G_t\) original used by DECISION-WORK-ONLY307, authenticate each block as A or B. One physical x2 pin bit distinguishes A from B, and the pinned original is SAT iff all blocks are A.

For every \(0\le\varepsilon<1/2\), the exact minimum worst-input expected number of discriminating pin-bit queries is

\[
R^{\mathrm{exp}}_\varepsilon=(1-2\varepsilon)t.
\]

The lower bound couples the all-A run with each one-B input: if \(E\) is SAT output on all-A and \(Q\) the queried block set, then \(\Pr(E)\ge1-\varepsilon\) and \(\Pr(E\land i\notin Q)\le\varepsilon\), hence \(\mathbb E|Q|\ge(1-2\varepsilon)t\). Equality is achieved by querying all and deciding with probability \(1-2\varepsilon\), otherwise making a fair zero-query guess. Exact and zero-error cost \(t\); error \(1/3\) costs exactly \(t/3\) in expectation.

This uses no recovered assignment, injective pin key, or stored trajectory. It is linear, not exponential, and only a promised pin-query theorem—not an arbitrary-machine runtime or FLMV bound.

## Controls and charges

- All A/B words through \(t=3\) checked directly on their same connected canonical originals: all-A has one model, all others zero.
- Independent no-import verifier: 115 assertion groups.
- Completed UP-DPLL trees through \(t=4\): one node on both labels; largest all-A/last-B runs 452/404 clause visits and 780/691 literal reads.
- Y6 20, F9 root 70, F9 A/B 1/0, independent F9 S/U 3/0 with complete eight-leaf false-clause cover, F15 2/0, all 264 F9 S/U modes, six malformed rejects.
- U198/V198 inherited and unused in this theorem. XOR is offline. DELAY/COPY/RECOMP and changed-restored controls remain charged.

Full controller work remains grammar + source/index/head + discover + select/switch/failed + deduction/GE/proof + cache/replay + child/output/access + guest, with combined simultaneous peak space. The theorem bounds only one paid summand. No free semantic label or selector is supplied.

## Consequences

- Falsified: bounded-error randomization makes the promised decision \(o(t)\) in expected pin queries.
- Preserved: \(84^t\) or \(2^t\) syntactic/continuation multiplicity does not imply exponential work.
- Open: uniform all-input semantic acquisition, polynomial total work on every valid target original, arbitrary-\(A\) ARC, numerical same-machine FLMV transfer, and P versus NP.

Artifacts: [formal report](../main/2026-11-01_1648_MAIN_RANDOMIZED-PIN-QUERY-REFEREE276.tex), [producer](../../experiments/arc/lspv5_276/randomized_pin_query_referee276.py), [independent verifier](../../experiments/arc/lspv5_276/verify_randomized_pin_query_referee276.py), [raw JSON](../../results/raw/arc/2026-11-01_1648_LSPV5_RANDOMIZED_PIN_QUERY_REFEREE276_raw.json).

No task identity, title, enabled state, schedule, or ownership changed.

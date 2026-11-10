# Five-role handoff: adaptive random-access dependencies and FLMV-compatible theorems

**November 9, 2026 PST | User-requested additional research | No task or schedule changes | P versus NP OPEN**

Interactive LSPV-5 report and independently replayed controls:
\`research/agents/lspv-5/2026-11-09_1914_LSPV5_MANUAL_RANDOM_ACCESS_TIME_SPACE_THEOREM_AUDIT.md\`

## Exact result and scope

- FLMV 2005, Fortnow 2000, Williams 2006/07 and Buss–Williams 2012 apply to **general random-access SAT machine time-space lower bounds** within their exact hypotheses.
- Williams STOC 2025 gives $T$-time to approximately $\sqrt{T}$-space simulation on ordinary multitape machines, and a similarly space-efficient simulation for **input-independent oblivious register schedules** satisfying his Remark 1.6. The arbitrary random-access extension is **explicitly OPEN**; no simultaneous $\tilde O(T)$ runtime is proved for the simulator.
- Separate limited-memory model result: in \`INDEX_M(a,y)=y_a\` with $M=2^d$ independent source bits, an input-independent fixed oblivious schedule reading only table cells needs at least $M$ distinct probes on all inputs; one adaptive probe suffices. This is a source of *linear*, not superpolynomial, worst-case overhead in length $N=M+d$.
- A Cartesian product of independently abstracted write/read address sets invents illegal source-dependent combinations. The relational invariant \`writeAddr=readAddr\` repairs the tiny example with $O(\log M)$ symbolic bits. No symbolic representation-space lower bound is implied.
- Hypothetical same-time square-root-space exponent $s=c/2$ conflicts with the FLMV branch only when $2c^3-c-2<0$ ($c<1.165373043\ldots$) and with the Buss-Williams product bound only when $3c/2<2\cos(\pi/7)$ ($c<1.201291824\ldots$); neither covers all finite $c$.
- Finite validation: Python 703,136, independent JS/V8 1,051,638 checks, zero failures, 1,022 missing-cell adversarial controls and 348,502 spurious marginal pairs.

## Role-specific investigation, preserving 2 Route A / 3 Route B allocation

- **LSPV-1:** Verify mathematical statement/model scope of FLMV, 2000 Fortnow, 2006/07 Williams, Buss-Williams 2012, and Williams 2025; derive conditionals for arbitrary large $c$. No time-space separation claim.
- **LSPV-2:** Build a symbolic last-write dependency DAG for adaptive memory; compare all-possible-address $\Theta(T^2)$ naive edge expansion to compact relational alternatives. Charge actual construction, replay, caching, time and peak space, source access, and both-label correctness.
- **LSPV-3:** Audit typed source, address equality, last-write provenance, history, branches, and AND/OR obligations. Distinguish dependency graph and separately supplied certificates from actual machine memory.
- **LSPV-4:** If scheduled/enabled under its independent configuration, audit the model conversion and all-phase machine resource ledger; do not automatically enable a disabled task.
- **LSPV-5:** Attack every proposed obliviousization using the INDEX_M adversary, nonuniform schedule assumptions, data-dependent reads, partial proof source authentication, polynomial exponent quantifiers, and any claim of $T$-preserving Williams simulation.

Retain original native $R_{\mathrm{mix341}}$ grammar/weights, other proof obligations, schedules, task IDs, titles, time zones and enabled states. Every scheduled agent reads **both** proof1.txt and proof2.txt, existing current handoff, issue #3, peers/Grok/Claude, primary literature and mandatory external repositories. IDEA -> SEARCH -> ITERATE; cite exact tracker IDs and update only material deltas with current complete blob/SHA and full readback. This interactive memo does not claim a material tracker change, nor does it start or alter any scheduled run.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-A5] and B3 remain at their prior statuses. P versus NP remains OPEN.

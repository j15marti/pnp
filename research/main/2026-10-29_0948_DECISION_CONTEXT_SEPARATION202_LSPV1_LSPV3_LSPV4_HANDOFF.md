# LSPV-5 additive handoff: DECISION-CONTEXT-SEPARATION202

Timestamp: 2026-10-29 09:48 America/Los_Angeles  
Status: PROVED/EXACT restricted firewall; unrestricted SAT OPEN; P versus NP OPEN.

## Result to adopt

For the connected proper 3CNF sources

\[
F_{t,s}=\bigwedge_i(z\lor(a_i\oplus s_i)\lor b_i)
\land\bigwedge_i(\neg z\lor c_i\lor d_i),
\]

all unaugmented instances are SAT, so a decision-only summary needs one state.
But the four-pin contexts

\[
Q_i=(\neg a_i)\land(\neg b_i)\land(\neg c_1)\land(\neg d_1)
\]

satisfy `SAT(F_{t,s} ∧ Q_i) = s_i`, so any source-free state supporting an
adversarially selected `Q_i` needs `2^t` values and at least `t` bits on some
source.

This proves an exact separation between decision-only and context-complete
interfaces. It retires any inference from a full-port or future-context floor
to a decision-only contraction lower bound unless a new theorem forces the
successor to support those contexts.

## Constructive restricted control

The canonical class consisting of these sources plus fixed YES/NO bases is
polynomially recognizable and closed under the uniform map sending every
source to the fixed YES base. This is a genuine power-short one-child
successor on that promise class. It does **not** contain arbitrary SAT and does
not imply P=NP.

## Role targets

- **LSPV-1:** For every proposed unrestricted successor, state the minimal
  continuation/query contract that correctness and recursive closure actually
  require. Do not import all-context preservation by default. ARC226's
  successor-existence equivalence remains the logical firewall.
- **LSPV-3:** SOURCE-RUP-CHAIN164 survives mathematical audit for fixed block
  width/path locality. The GitHub TeX blob
  `89d79fdd6e845a3c31bf7de8c67c031435023a58` lacks the mandatory first report
  marker and final sentinel; repair publication without changing the research
  body. Clarify that top-level maximum 3,205 is UNSAT-only, whereas the per-test
  maximum derived count is 3,607 on a SAT elimination run.
- **LSPV-4:** FOUR-PIN226's abstract online-state theorem is adopted. Keep its
  writable-cell corollary conditional on fixed heads, finite alphabet,
  polynomial preprocessing time and source unavailability. The next useful
  audit is whether a real proposed successor needs contexts rich enough to
  embed INDEX.

## Reproducer

`research/main/2026-10-29_0948_DECISION_CONTEXT_SEPARATION202_repro.py`
checks 30 source witnesses, 98 contextual SAT instances, the `2^t` signatures
through `t=4`, and the proper-3CNF pin gadget. Canonical payload SHA-256:
`11c64e0a6d3e4a5e4896150cbdb170ffcc981e67850f7c040f082957e7b4ac37`.

No agent identity, enabled state, schedule, or role ownership is changed.

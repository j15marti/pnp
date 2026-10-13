# LSPV-4 handoff — CERTDPLL-BRIDGE1

Status: **P versus NP remains OPEN**.

- **KNOWN THEOREM:** Berger–Lawrence–Nordvall Forsberg–Seisenberger, Theorem 6, translates an explicit DPLL derivation of size `n` to Resolution size at most `n`.
- **CANDIDATE pending independent research review:** composing that theorem with the clause-to-semantic-CP embedding gives a charged, same-input bridge for explicit certificate-producing DPLL solvers. This does not cover arbitrary one-bit deciders.
- **COMPUTATIONAL:** `dpll_certificate_bridge_audit.py` passed 19,877 assertions on 654 formulas, including Horn, Krom, affine, bounded-treewidth, product, renaming/phase, tautology-padding, and wrapper controls. The semantic fingerprint excludes wall-clock time.
- **FALSIFIED/RETIRED:** a fixed evaluated trace plus opposite output is not an input-clause proof; see `2026-10-13_1402_LSPV-4_TRACEEXT-FIREWALL1.tex`.
- **OPEN load-bearing arrow:** every total uniform one-bit decider of `L22` -> a proof in the lower-bounded semantic-CP/triangle model.

Highest-value next review: independently check the bit-cost and semantic-CP embedding, then extend only to explicitly proof-logging CDCL variants whose primary simulation theorem supplies a polynomial quantitative bound.

Canonical report: `research/agents/lspv-4/2026-10-13_1455_LSPV-4_CERTDPLL-BRIDGE1.tex`.

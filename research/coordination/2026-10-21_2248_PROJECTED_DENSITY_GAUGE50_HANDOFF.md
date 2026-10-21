# PROJECTED-DENSITY-GAUGE50 handoff

Date: 2026-10-21 22:48 Asia/Seoul. Circuit-SAT remains a comparison representation, not a third P-vs-NP route. P versus NP and P versus RP remain OPEN.

## Exact theorem

If \(E_C(r,w)\) is a parsimonious deterministic extension of circuit \(C(r)\) with \(m\) primary variables and \(q\) trace variables, then
\[
\#SAT(E_C)=|\{r:C(r)=1\}|,
\qquad
\Pr_{r,w}[E_C=1]=2^{-q}\Pr_r[C(r)=1].
\]
Sampling only \(r\) and deterministically completing the trace preserves \(\Pr_r[C(r)=1]\).

Adding \(d\) uniquely determined copy/trace variables preserves the language and model count but multiplies full-formula density by \(2^{-d}\). Therefore full Tseitin-assignment density is a representation gauge, not a language invariant or lower bound.

## Cross-track consequences

- “DENSE-BYPASS14” retains a trivial selector seed despite high ANF degree, high gate width, relevance of every random bit and arbitrarily sparse padded Tseitin images.
- Unique trace and unique complete assignment do not imply hardness.
- Gate sharing changes the number of trace variables and full density but not the projected accepting inputs.
- Digest-portfolio bounds apply to primary witness tests; random guessing of deterministic trace bits is an artificial loss.
- Short-seeded scrambling is chargeable; hidden role metadata removes the projection sampler but proves no hardness.

## Next tests

- **:00:** require MKTP label/KT invariance under deterministic copy padding.
- **:12:** quotient trace/padding and test the primary function for selector and direct-decider bypasses.
- **:24:** partition only the residual semantic circuit and charge its true live frontier.
- **:36:** recover the primary randomness projection for arbitrary RP verifiers without semantic dead-variable analysis.
- **:48:** require projected/full density, extension multiplicity, role-map access and trace-completion cost.

Audit: 769,806 assertions, zero failures.

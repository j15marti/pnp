# LSPV-5/REFEREE388 five-role handoff

**Pacific timestamp:** 2026-11-06 07:48 PST  
**Primary route:** B  
**Status:** PROVED-RESTRICTED + COMPUTATIONAL; global mixed minimum and B3 OPEN.

## Result to reuse

For the authenticated bridge-cut control, the two 18-source side formulas semantically force opposite bridge units:

$$L\models x_{15},\qquad R\models\neg x_{15}.$$

Nevertheless, exhaustive exact closure proves that neither unit has a strict non-tautological source-once Resolution tree using all 18 side clauses exactly once. Each side closure tests 1,126,097,195 clause pairs and has 1,888 distinct full-source outcomes; the required unit is absent.

Therefore the canonical 35-node proof consisting of two 17-node pure-Resolution side-unit trees and one root RES node does not exist. This does not exclude an interleaved global 35-node tree or a mixed AND3/XOR/RES tree.

Exact source DIMACS SHA-256: `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`.

## Independent verification

The producer uses positive/negative bitmask clauses. The independent verifier uses base-3 clause encoding and a separately generated 43,046,721-entry resolution table. It reproduces both closures, all pair counts, 1,888 full outcomes, and target absence; four corrupt controls are rejected.

This is an exact finite strict-Resolution computation, not an authoritative historical byte-checker execution and not an optimizer over all mixed rules.

## Role actions

- **LSPV-1:** the 35-node floor survives. Any candidate must interleave sides or mix AND3/XOR/RES; the canonical side-unit Resolution join is closed.
- **LSPV-3:** test whether native pure-Resolution assumption discharge can transform a hypothetical interleaved full tree into side-unit trees without source duplication. Do not assume this commutation.
- **LSPV-5:** attack interleaved trees and the three 36-node excess classes; reject weakening, repeated sources, and context leakage.
- **LSPV-2/4:** this finite closure is only a correctness/resource control and supplies no same-machine FLMV contraction.

## Boundaries

Urquhart Tseitin and Haken PHP remain lower bounds for their stated Resolution systems. GF(2), extension variables, LOCAL, sharing, and other historical mixed shortcuts remain mandatory. No lower-bound-preserving all-rule transfer or noncircular same-system B3 bridge is established.

Full report: `research/main/2026-11-06_0748_MAIN_READONCE_BRIDGE_UNIT_REFEREE388.md`.

P versus NP remains OPEN.

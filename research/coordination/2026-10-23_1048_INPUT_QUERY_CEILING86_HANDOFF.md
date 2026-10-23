# INPUT-QUERY-CEILING86 handoff to Roles 1-4

Timestamp: 2026-10-23 10:48 KST  
Status: P versus NP OPEN.

Verified standalone source:
\`research/main/2026-10-23_1048_MAIN_INPUT_QUERY_CEILING86.tex\`
(blob \`3393c642a0870d4a2925665861c2362539fca8b8\`; exact connector readback).
Root reconciliation commit: \`988ea26b869cca9031a2dac5485cd5db1276bb34\`.

## Exact base rung

For
\[
F_b=(z_0)\wedge(\neg z_q)\wedge\bigwedge_{i=1}^q C_i(b_i),
\]
with \(C_i(1)=(\neg z_{i-1}\vee z_i)\) and
\(C_i(0)=(\neg z_{i-1}\vee\neg z_i)\), \(F_b\) is UNSAT iff
\(b=1^q\). Flipping any one orientation bit gives an equal-length SAT
instance with witness \(z_i=1\) for \(i<j\), \(z_i=0\) for \(i\ge j\).
Thus every deterministic exact decider in the orientation-field query model
reads all \(q\) fields on the all-one input. This is exact and all-algorithm
within that model.

Field/bit/record/word/Turing conversions require a fixed layout. No
layout-free time theorem is claimed.

## Charged transport

Every compatible simulation obeys
\[
L_{\rm old}\le R+H+Q\tau T_{\rm new}^{\le}(g).
\]
Only a positive remainder yields
\[
T_{\rm new}^{\le}(g)\ge (L_{\rm old}-R-H)/(Q\tau).
\]
A linear explicit reduction can consume the entire linear source lower bound.
Direct inclusion preserves the bound but not its order.

## Ceiling and ladder

Any explicit \(m\)-field input has deterministic field-query complexity at
most \(m\), by reading all fields. Pure query/direct-product/padding
amplification to superlinear or superpolynomial order is therefore
**FALSIFIED/RETIRED**.

For 2-CNF plus at most \(k\) ternary clauses, binary branching on a variable
from a ternary clause gives \(O(2^k\operatorname{poly}(N))\) time and
\(O(N+k)\) depth-first space. This is an upper bound, not necessary work.
\(k=O(\log N)\) is polynomial; unrestricted \(k\) contains NP-complete 3-CNF.
No unconditional \(2^{\Omega(k)}\) lower bound is established.

## Role-specific use

- Roles 1-3: do not seek more explicit query gadgets. The first plausible
  amplification obligation is a post-acquisition theorem: after every source
  read is charged, every uniform exact decider must either acquire and validate
  a \(2^{\Omega(k)}\) compatible summary or spend \(2^{\Omega(k)}\)
  continuation steps. It must survive SCC, Gaussian elimination, small
  interfaces, source-aware gate recognition, caching, alternate
  representations, and decide-first normalization.
- Role 2: ORDER-PROJECTION47 remains a fixed-order representation lower bound;
  its source-first linear elimination is a hostile control against arbitrary
  SAT-time promotion.
- Role 4: the user-supplied chain baseline was independently verified. No
  current Role 4 ladder report was visible at the reviewed repository head;
  reconcile any later extension against the positive-remainder inequality and
  query ceiling.

No finite experiment, NP-completeness statement, or restricted proof-system
bound is promoted to P != NP.

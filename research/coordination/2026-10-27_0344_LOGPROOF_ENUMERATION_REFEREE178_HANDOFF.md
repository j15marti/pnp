# LOGPROOF-ENUMERATION-REFEREE178 additive handoff

Timestamp: 2026-10-27 03:44 America/Los_Angeles  
Owner: LSPV-5 independent red team

## Exact result

For one fixed uniform total indexed interpreter `I(F,j,pi)`, suppose:

- at most `N^(b+o(1))` verifier indices `j`;
- proofs of at most `(a+o(1)) log_2 N` bits;
- every verifier is globally sound on every SAT input;
- the portfolio is complete on every ordinary UNSAT input;
- each fresh call costs time `N^(r+o(1))` and space `N^(s+o(1))` on the same native indexed machine.

Then deterministic fresh enumeration decides ordinary SAT in

`T <= N^(max(1,r+a+b)+o(1))`, `S <= N^(max(0,s)+o(1))`.

Using the verified strict FLMV box, `s < 11642479/23232400` forces
`max(1,r+a+b) >= 241/200`. The `b=0` case independently upholds LSPV-1 ARC199.

## Falsifiers

- **FALSIFIED:** candidate enumeration without fresh reset. A two-proof stateful verifier is freshly sound/complete but falsely accepts SAT when dirty state survives.
- **FALSIFIED:** input-selected short verifiers without global SAT soundness. Two local verifiers cover two UNSAT inputs but both accept a SAT input.
- **FALSIFIED/RETIRED:** importing the theorem to sequential tape promises or reversing an upper simulation.

## LSPV-4 coefficient repair

For proof cap `P` and maximum sequential reach `J`, the exact number of visible proof classes is

- `2^(J+2)-1` if `J<P`;
- `2^(P+1)-1` if `J>=P`.

The published `2^(A+1)-1`, `A=min(P+1,J+1)`, is safe but overcounts by about two when the physical cap binds. Existing inequalities and exponent faces remain valid.

## Role-addressed actions

- **LSPV-1:** adopt the referee confirmation and optional portfolio coefficient, but keep one uniform common interpreter, global soundness, total clocks and fresh reset explicit.
- **LSPV-3:** the rank--exception theorem is upheld in its matched-projection scope; projection computation/authentication and the exponential exception term remain outside any claimed all-input proof cap.
- **LSPV-4:** use the exact visible-prefix formula above when claiming exact finite multiplicity. Pointer traffic is a property of the prescribed checker, not every verifier.

## Reproducibility

- 829,745 deterministic assertion groups, zero failures.
- Raw SHA-256: `e8f576bee6674c2851cc8550e60fadfed4817ed472ad506241ecce8c9d79b6c8`.

The existence of a uniformly capped all-ordinary-UNSAT verifier, deterministic acquisition, two hereditary ordinary-SAT levels, ARC-EDGE-90 and P versus NP remain **OPEN**.

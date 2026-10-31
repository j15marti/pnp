# Five-role handoff — TARGET-SCOPE-FLMV-REFEREE247

Timestamp: 2026-10-31 11:48 America/Los_Angeles

All five roles should use the total language of duplicate-free proper Monotone
3-SAT-(2,2) as the canonical target. Malformed strings are NO. The broader proper
strict-2P2N family is only a comparative superset, and the all-positive exact-two
family is not a hardness target.

Verified synthesis:

- A polynomial decider for every string of this one NP-complete total language is
  equivalent to P=NP. A superpolynomial deterministic lower bound for the same
  language implies P!=NP.
- NP-completeness alone does not transport the strict FLMV numerical box.
- Under output length `M=N^(a+o(1))`, setup exponents `(u,v)`, accessor exponents
  `(q,r)`, and target exponents `(K,L)`, the source simulation costs
  `time=N^(max(u,q+aK)+o(1))`, `space=N^(max(v,r,aL)+o(1))`.
- The existing Monotone-3-SAT*-(2,2)-to-target fixed-block leg is adequate and
  locally accessible. The open first leg remains `LOCAL-COOK-MONOTONE22STAR1`.
- Raw restriction is not hereditary: one pin creates binary clauses. Recursive
  children must remain in target or be re-encoded with full cost.
- Independent exact controls certify one valid 198-variable UNSAT target and one
  valid 198-variable SAT target. Both all-zero/all-one endpoints fail on the SAT
  fixture, so endpoint failure is not an UNSAT rule.

Highest-value target: close or falsify `LOCAL-COOK-MONOTONE22STAR1` with exact
same-model length, arbitrary-bit access, time, index-tape and peak-space bounds on
both labels. P versus NP remains OPEN.

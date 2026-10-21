# RP-ORBIT-CERTIFICATION-FIREWALL40 handoff

Timestamp: 2026-10-21 12:48 Asia/Seoul. P versus NP and P versus RP remain
OPEN.

## Exact result

If an RP verifier has a uniformly generated polynomial-size partition of its
random tapes into acceptance-constant orbits, one representative per orbit
gives an exact deterministic polynomial-time simulation.

However, given circuit C(z), the verifier predicate

F_C(q,a,b,z)=q OR (a AND NOT b AND C(z))

recognizes Sigma* with acceptance probability at least 1/2, while invariance
under swapping a,b holds iff C is unsatisfiable. Thus coordinate-swap
symmetry certification is coNP-complete even for verifier circuits whose
language is trivially in P. This independently validates the new :36 stub
while adding the language-invariance firewall.

## Computational audit

65,814 truth tables through four z bits, 8,405,584 tape pairs, 20,000 random
promised orbit partitions, and 10,000,659 assertions passed with zero
failures. Raw SHA-256:
c671544472ab006fb3ff229111909515b7a41e3e8f8d51d930c8433775917f41.

## Assignments

- :00: demand an all-input ordinary-KT gap after full target/source ledger.
- :24: build one high-width semantic successor and charge eager serialization.
- :12: attack language-level separation candidates with the trivial-language
  verifier-geometry embedding.
- :36: supply one nontrivial uniform orbit generator/representative algorithm
  and charge certification and simulation.
- :48: keep PNP and RP DAGs separate; orbit symmetry is restricted evidence.

Artifacts:

- research/main/2026-10-21_1248_MAIN_RP_ORBIT_CERTIFICATION_FIREWALL40.md
- experiments/review/2026-10-21_rp_orbit_certification_firewall40_audit.py
- results/raw/separation/2026-10-21_1248_RP_ORBIT_CERTIFICATION_FIREWALL40_raw.json


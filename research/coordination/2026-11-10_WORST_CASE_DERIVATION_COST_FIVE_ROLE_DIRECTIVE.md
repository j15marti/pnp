# Shared directive: worst-case minimum derivation cost (2026-11-10)
Status: CANDIDATE research direction. P vs NP OPEN. Additive: no change to schedules, roles, or proof-status rules.

Object: W_R(N) = max over UNSAT F, |<F>|<=N, of min over refutations pi in fixed R of cost_R(pi).
Strategy discovery is NOT charged (free optimal sequence). Cost = distinct paid nodes of the multisign shared-DAG hypergraph (R_mix341 model) plus certificate bits.
Target bridge B(R): SAT in P => W_R(N) <= poly(N).
Roles: General Lower-Bound Lead, Reduction Builder, Hypergraph/Certificates, Time-Space Auditor, Red Team.
Living log: research/worst-case/LOG.md (append one entry per run).
Key facts established in the first entry (see LOG.md): bridge circularity for systems with known lower bounds; sufficient conditions for the bridge.

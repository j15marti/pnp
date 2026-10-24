# FIXED-SYNDROME-FIREWALL113 — cross-role handoff

**Global status: P versus NP remains OPEN.** This handoff reports a primary-source upper-theorem transfer and an independently checked hostile family; it is not a deterministic SAT lower bound.

## Exact correction to the ladder

For explicit 2-CNF `B(x)` and affine rows `A x = b` of GF(2)-rank `rho`, define `G=F_2^rho`, `g_j(0)=0`, and `g_j(1)=A[:,j]`. Then

```text
sum_j g_j(x_j) = b  iff  A x = b.
```

Brakensiek–Gopi–Guruswami, SIAM J. Comput. 51 (2022), Definition 2.5 and Proposition 5.2, give `(n+m)^{O(rho)}` exact time for this weighted 2-SAT-MOD instance. Therefore:

- every fixed-rank/fixed-number-of-parity-check rung is polynomial;
- rank `O(log N)` has a quasipolynomial `N^{O(log N)}` upper bound;
- this is XP-style in `rho`, not an FPT claim;
- unrestricted rank contains an NP-complete language via the selector/XOR3 reduction;
- none of these upper results proves an unrestricted lower bound.

Role 4 DUAL-PARITY-JOINT77 left the general two-check complexity unresolved. That sentence is stale: the full two-check language is polynomial by the theorem above. Its exact marginal-syndrome counterexample remains valid—it refutes marginal checking and affine-hull summaries, not the complete group algorithm.

## Independent Role 4 check

For every `q>=1` and orientation `e`, with `p=xor(e)`:

```text
n=6q, m2=4q+4, k=16q-8, M=20q-4, h2=2q-1
SAT iff p=1
#SAT=2^q on SAT, 0 on UNSAT
R_e=F_2^2 \ {(p,p)}
```

Both labels have equal metadata. The all-zero orientation is UNSAT and each one-field flip is SAT, giving `q` exact addressed orientation queries; the canonical parity scan matches this in `O(q)` word work. This is acquisition order only.

The audit performed 646 assertion-accounted checks in 4.657258 seconds with zero failures: every orientation through `q=5`, full compiled-CNF model counts through `q=3`, exact backdoor minima through `q=4`, 98 weighted-group equivalence controls, and symbolic accounting through `q=4096`.

## Adaptive ledger

1. Parse and retain the original source; no label is supplied.
2. `XR1`: extract complete parity blocks with occurrence provenance.
3. `XR2`: row-reduce to independent rank `rho`; charge failed extraction and Gaussian work.
4. If the residual is 2-CNF plus `rho` rows, dispatch to weighted 2-SAT-MOD over `F_2^rho`; a source-specific scan may be selected when recognized.
5. SAT: lift eliminated variables, reconstruct prefixes, and replay one original-source witness.
6. UNSAT: return the exact bit; no designated proof object or enumeration is required.
7. Unsupported inputs retain exact fallback, with switching, cache, source access and peak live space charged.

## Status changes

- **KNOWN THEOREM + PROVED/EXACT model mapping:** `(n+m)^{O(rho)}` fixed-syndrome upper algorithm.
- **PROVED/EXACT:** DUAL-PARITY-JOINT77 counts, labels, syndrome image and `h2=2q-1`.
- **COMPUTATIONAL:** 646 finite audit checks, zero failures.
- **FALSIFIED/RETIRED:** fixed two checks as a hardness boundary; separate marginal feasibility; affine hull; raw backdoor or rank as mandatory all-decider work.
- **OPEN:** an all-decider superpolynomial lower bound on the unrestricted NP-complete endpoint.

## Required peer update

Roles 1–3 should consume this theorem before using check count, affine rank, marginal compatibility or raw parity-prefix backdoor as a lower-bound resource. DUAL-PARITY-JOINT77 is now a mandatory hostile control for candidate acquisition/continuation measures.

The first missing lemma must define a representation-neutral interaction obstruction and prove an acquisition-or-continuation lower bound that survives modular recursion, Gaussian basis changes, SCC/Horn, SIL rewriting, tree joins, learning, proof-core replay, caching, restarts, recomputation and direct decision.

## Artifacts

- `research/agents/lspv-5/2026-10-24_1248_LSPV-5_FIXED_SYNDROME_FIREWALL113.tex`
- `research/agents/lspv-5/2026-10-24_1248_LSPV-5_FIXED_SYNDROME_FIREWALL113_HANDOFF.md`
- `research/agents/lspv-5/2026-10-24_1248_FIXED_SYNDROME_FIREWALL113_audit.py`
- `research/agents/lspv-5/2026-10-24_1248_FIXED_SYNDROME_FIREWALL113_raw.json`

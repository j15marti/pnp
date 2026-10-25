# ARC-HETEROWORD165 | LSPV-1 additive five-role ARC handoff

Date: 2026-10-25 03:32 America/Los_Angeles. **ARC/FLMV only.** Five pre-existing enabled hourly tasks and :00/:12/:24/:36/:48 staggers unchanged. No peer-region or scheduler modifications. **ARC-EDGE-90 and P versus NP remain OPEN.**

## Verified exact contribution
Every *valid machine-producing* fully charged eager/lazy ARC stage with an exponent envelope can be normalized to:
```
t_i <= max(L_i, u_i + lambda_i * t_(i-1))
s_i <= max(V_i, nu_i * s_(i-1))
```
For eager: `u=a`, `L=max(r,a+lambda+g)`, `V=max(lambda,eta,kappa)`.
For fully lazy repeated probes: `u=a+g`, `L=r`, `V=max(eta,kappa)`.
Additional semantic guest work, actual nested generator service and shared source probes must be included; this is NOT a gratis profile.

The finite heterogeneous route-word theorem (report Theorem 1) gives an **exact max over all reset branches**. Algebraic certification requires *every* time branch < `241/200` and *every* space branch < `11642479/23232400`. A stage's profile may differ from other stages, and temporary stage failure to enter the box does not automatically disqualify a later *valid* finite route. Code tests at K=10: 11 eager => 3083/2560; lazy then 10 eager => 4933/4096; 10 eager then lazy => 3211/2560 (fails); six recovery eager => 196747/163840 (enters). At repeated lazy g=1/400, `t_d=c_star+(K-c_star)/2^d > c_star` for all finite d and K>c_star: this particular **upper-envelope certificate** cannot succeed, but does NOT lower-bound actual machine time.

The scalar g thresholds, homogeneous recurrence, and promised scoped join were already in the repository. This run adds a heterogeneous finite-word exact certificate with correct reset floors and explicit finite negative schedules, **not a new machine transformation**.

## Genuine SAT/UNSAT controls
Reproducer builds 16 roots, 8 SAT and 8 UNSAT, as q^2 disjoint 2CNF XOR cycles for q=3,4,5,6. Every root and its two real recursive levels are fully serialized, reparsed ordinary DIMACS CNF. Disjoint AND joins agree with independent deterministic SCC decisions at 72 level-one and 344 level-two actual child calls. A minimal hostile shared-variable pair `(x)` and `(not x)` has two SAT child labels but an UNSAT parent; therefore **scope compatibility is not optional**. One malformed-DIMACS guard rejects invalid variable fields. 6,001 exact rational checks and 124 SAT/UNSAT checks, zero failures. These are *restricted easy 2SAT/affine* sources and Python operation counts are **not FLMV machine measurements**.

## Sole missing ARC arrow, with role-owned tasks
- **Role 1 lead:** keep the proof DAG; demand a real same-machine, all-ordinary-input or fixed-hard-image contractor, then apply the exact finite-word certificate.
- **Role 2 constructor:** supply an A-dependent semantically sufficient lossy source normalizer with fully charged near-linear acquisition and genuinely power-short ordinary descendants, including off-promise fallback.
- **Role 3 semantics:** prove actual descendant type/eligibility and source-variable compatibility across both levels, for both SAT and UNSAT; the hostile shared-unit pair must be rejected.
- **Role 4 bit auditor:** derive real `g`, generator fusion/cache terms, sources, unchanged writes, guest probes, parent calls, and peak simultaneous indexed/writable bits *before* issuing a route profile. Nested `g` composes.
- **Role 5 red team:** independently reject any route that mixes exponents from different machines, silently assumes hard-image low-width scope, or reads upper-envelope failure as SAT lower bound. Reconcile executive synthesis only when proven.

Source and readback verified:
- `research/agents/lspv-1/2026-10-25_0332_LSPV-1_ARC_HETEROWORD165.tex` (commit `b9d548364afac369547b506f9cd88da9a7782d88`)
- `research/agents/lspv-1/2026-10-25_0332_ARC_HETEROWORD165_repro.py` (commit `5e2101268c42281766ad25d93bc2c06d1cb8ec04`)
- `research/agents/lspv-1/2026-10-25_0332_ARC_HETEROWORD165_results.json` (commit `81d3a8553c2043b191b2cec1f7315ee58a400242`)

Prior source anchors: current `main.tex`, `main13.tex`, `CACHE-MISS-FRONTIER18`, `ARC-SCOPE-TOLL160`, `ARC-SCOPED-DEPTH-BUDGET112`, `ARC-NESTED-ACCESS-TAX113`, `ARC-IMAGE-SCOPE-NONINVARIANCE163`, and Fortnow--Lipton--van Melkebeek--Viglas, JACM 2005, doi:10.1145/1101821.1101822.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-1::ARC-HETEROWORD165 -->

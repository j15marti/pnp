# TWO-PROBE-NONLINEAR-FRONTIER237: Additive LSPV-2 handoff

**Date:** 2026-10-29, 19:12 PDT. **Status:** PROVED/EXACT, RESTRICTED, pending independent referee. **Unrestricted P versus NP:** OPEN. No changes to task identity, enabled state, schedule, or other role-owned content.

## Narrow exact theorem

Let a canonical unary source contain `b` unknown sign bits `a`, which are *retained* as indexed, read-only source. Before the later mask `w` is known, an arbitrary deterministic, possibly nonlinear preparer stores an `L`-bit **fixed-length** summary. A deterministic, possibly adaptive query algorithm must answer `w dot a (mod 2)` for every source and every mask after at most `Q` indexed raw source-bit probes. Original source access, summary reads, mask parsing, address calculations, persistent memory and full time are separate resources.

**General nonlinear lower bound** (proved by restricted real-Fourier/decision-tree dimension argument): `2^L * sum_{j=0}^Q binom(b,j) >= 2^b`. Each fixed-summary fiber has at most `sum_{j=0}^Q binom(b,j)` members because every restricted parity character must belong to the span of real monomials of degree <=Q; the characters span every real function on that fiber.

**Tight two-probe family:** for every `m>=1`, `b=2(2^m-1)` has exact optimal `L_2(b)=b-2m` even against arbitrary nonlinear preparation and adaptive decisions. The volume `V(b,2)=2^(2m+1)-3*2^m+2` lies in `[2^(2m),2^(2m+1))`. The matching summary uses two groups with all nonzero `m`-bit labels, storing the nonbasis deviations from its `m` basis bits. A future parity query takes at most one raw source read in each group. Encoder and decoder are uniform and polynomial, and the addresses are determined by the query and summary layout before reads.

The first three exact fixed-length Pareto coordinates are `(Q,L)=(0,b),(1,b-m),(2,b-2m)` at these source lengths. Examples: `b=6 -> L=6,4,2`; `b=14 -> 14,11,8`; `b=30 -> 30,26,22`.

The lower bound **does not** prove an exact value for unrestricted non-prefix variable-length summaries. Direct counting then yields only `(2^(L+1)-1)*V >=2^b`; prefix-free codes satisfy the fixed-length count. This distinction is intentional and independently reviewable.

## Fully charged model, controls, computational record

The native source-probe theorem is for indexed bit-RAM only, with `N=Theta(b log(b+1))` encoded unary CNF source bits. Preparation `P=O(N+b*m)` and per future query `T=O(N+b*m)` include scans, cached summaries, arithmetic and materialized storage. Peak writable memory `L+O(m+logN)` bits is an explicit upper, separate from retained immutable source `N`; total post-preparation original-bit probes are at most `2*M` for `M` queries. A one-batch two-address read is possible with two ports, or two sequential reads with one port. Sequential tape head movement is not a two-bit source probe: those native model bounds are separate and weaker. Exact changed-cell counts and physical UTM simulations remain unmeasured.

The deterministic stdlib reproducer passed 4,112 exhaustive source/mask pairs for `b=2,6`, 70,216 additional pairs (including every mask for four selected `b=14` sources), 2,728 finite independent unary-source-plus-XOR SAT comparisons, and 33 degree/volume identities. Independent 2SAT/XOR/mixed CNF and strict exact-(2+,2-)-3CNF SAT/UNSAT controls were checked; the 15-variable W1 UNSAT source was exhaustively checked on 32,768 assignments. Each paired Python runtime/peak-memory row is from the **same execution** and is not a native model lower bound. Seed 237; no external SAT solver or uncharged source answer bit.

The `(fact)|_v` interpreter records a certificate/provenance/context/score, explicit score-discovery enumeration, acquisition and verification/application costs; two complementary XOR shares jointly have value 1 under the declared projected-support potential while either alone and any duplicate have value 0. A distinct realized Bayesian-entropy value is negative at about -0.5310 bits; it is not a certified SAT progress measure.

## Prior sources and primary literature read

- `j15marti/pnp` `NONLINEAR_ONE_PROBE236.tex` blob `2d3deb8ee9496970dd12139860f88993efef5345`; `CONTEXTUAL_VALUE_HAMMING235.tex` blob `b4a1a846dab97bd02691578d9abe5a081890d8b7`.
- `j15marti/pnp` `ARC227_ONE_PARITY_AFFINE_HULL.tex` blob `fc4a02dc004e363e28dc78ebc3b969e2c27ad1f7`; `DECISION_CONTEXT_SEPARATION202` blob `6c31e5782e054febd190d90828ff5c038624ec07`.
- SageMath `src/sage/coding/hamming_code.py` blob `431e660fae77184147230223f66c76f2d5f04b38` and `src/sage/coding/reed_muller_code.py` blob `f5b9a17a3960a1f95d00ee591a3f6094ddf9fd27` were inspected; not executed as proof oracles.
- Nisan and Szegedy (1994), *Computational Complexity* 4, 301-313, DOI `10.1007/BF01263419`; Darwiche and Marquis (2002), *JAIR* 17, 229-264, DOI `10.1613/jair.989`; Hamming (1950), *BSTJ* 29, 147-160.

## Role-specific next tests

**LSPV-1:** independently referee the exact general `V(b,Q)` fiber-dimension argument and no-P-vs-NP firewall. **LSPV-2:** investigate the exact non-prefix variable-length `Q=2` frontier, especially the smallest feasible `b=6, L<=1` hypothesis; then build a certified, source-faithful SAT-interface transport, charging code construction and expansion. **LSPV-3:** seek connected strict22 contexts capable of querying arbitrary boundary parity, or a minimal counterexample. **LSPV-4:** measure native read-only-input versus one-write-tape physical accesses and memory changes; no bit-RAM transfer by assumption. **LSPV-5:** independently review theorem and reconcile only scientific statements under valid ownership markers.

## Artifacts and status

`research/agents/lspv-2/2026-10-29_1912_LSPV-2_TWO_PROBE_NONLINEAR_FRONTIER237.tex`, `.bib`, `_repro.py`, `_raw.json`; handoff under `research/coordination/`. Standalone mathematical PDF and ZIP are in the run's Library workspace. **Do not infer a SAT runtime lower bound from the bit-probe data-structure theorem.**

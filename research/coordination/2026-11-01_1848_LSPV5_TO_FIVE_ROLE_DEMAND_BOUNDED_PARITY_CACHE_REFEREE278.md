# LSPV-5 to five-role handoff: DEMAND-BOUNDED-PARITY-CACHE-REFEREE278

**November 1, 2026, 18:48 PST. Status: PROVED/EXACT restricted source-layout query theorem; independently COMPUTATIONAL; P versus NP OPEN.**

## Exact result

For LSPV-4 INCIDENCE-RANK-MIGRATION320's authenticated source family, the designated alternative block-boundary address bit is

\[
a_r(z)=\operatorname{bit}_2(1072r+4(r-|z|))=(r\bmod2)\oplus\bigoplus_i z_i.
\]

- Raw deterministic query complexity is exactly \(r\).
- With error \(\varepsilon<1/2\), exact minimum worst-input expected raw queries are \((1-2\varepsilon)r\).
- After one **charged** \(r\)-tag scan, a single retained parity bit answers every repetition of this fixed query with zero further source probes and constant cache/output work.
- Therefore \(q\) repeated identical requests cost \(r+O(q)\), not \(qr\), once the paid cache is allowed.

The raw lower bound is preserved. What is falsified is recharging it independently for every identical request or requiring a lossless source/rank key for one output bit.

## Equivalence boundary

For one fixed pivot, current semantic equivalence has two classes and one bit suffices. For every possible pivot, all prefix parities reconstruct the entire width word by adjacent XOR, so the declared all-pivot continuation table has \(2^r\) possible values and requires \(r\) lossless bits. It is nevertheless built in \(O(r)\) work and queried in constant random-access work. Exponential class count is not exponential computation.

Unknown adaptive pivots still require a paid miss, scan/rebuild, or a declared directory. Addresses, source authentication, head/index movement, cache construction, lookup, failed policies, proof/replay, children, guests, and simultaneous peak space are all charged.

## Independent controls

- Producer: 8,190 authenticated source variants through \(r=12\), 90,114 pivotal flips, and 11,141 selected-demand checks.
- No-import verifier: 21,385 assertion groups, 2,046 variants, 18,434 flips, and 79,600 reconstructed prefix bits.
- Original controls: F9/Y6/F15 roots 70/20/1032; same-original F9 and F15 SAT/UNSAT 3/0 and 2/0; eight-leaf F9 UNSAT cover; 264 S/U modes; six malformed rejects.
- U198/V198 inherited and unused. XOR offline. DELAY/COPY/RECOMP and changed-restored controls charged.

## Scope firewall

This is a source-layout/address query theorem, not SAT-decision complexity. It does not establish an upstream SAT-to-signed compiler, all-input polynomial controller, arbitrary-machine ARC contraction, strict same-machine FLMV transfer, or either resolution of P versus NP.

Artifacts: [formal report](../main/2026-11-01_1848_MAIN_DEMAND-BOUNDED-PARITY-CACHE-REFEREE278.tex), [producer](../../experiments/arc/lspv5_278/demand_bounded_parity_cache_referee278.py), [independent verifier](../../experiments/arc/lspv5_278/verify_demand_bounded_parity_cache_referee278.py), [raw](../../results/raw/arc/2026-11-01_1848_LSPV5_DEMAND_BOUNDED_PARITY_CACHE_REFEREE278_raw.json), [verification](../../results/raw/arc/2026-11-01_1848_LSPV5_DEMAND_BOUNDED_PARITY_CACHE_REFEREE278_verify.json).

No task identity, title, enabled state, schedule, or ownership changed.

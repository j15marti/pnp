# LSPV-5 -> FIVE ROLE: PREFIX-ALIGNED-B2-INVARIANCE-REFEREE339

**November 4, 2026, 07:48 PST · fixed `R_mix341` unchanged**

## Shared proved lemma

For the same authenticated abstract CNF `F` and same fixed logical cost `W_R(F)`, let two canonical P-recognizable encodings have valid-source prefixes

`S_i(N)={F:|e_i(F)|<=N}`.

If polynomially bounded cutoff maps `a,b` give exact bidirectional alignment

`S_1(N)=S_0(a(N))`, `S_0(M)=S_1(b(M))`,

and conversion, validation, output and access translation are uniform polynomial time, then B2 holds under `e_0` iff it holds under `e_1`. Each arbitrary decider is transported to one different fixed wrapper decider; cumulative worst-case time is compared at matched cutoffs. No per-`N` machine or advice occurs.

Exact strictly increasing polynomial length laws are a corollary. For

`E(c)=1^n 0 c 0^(n^2)`, `|E(c)|=(n+1)^2`,

the inverse cutoff is `r(N)=max(0,floor(sqrt N)-1)` and

`Wbar_E(N)=Wbar_0(r(N))` exactly.

## Critical correction to carry forward

LSPV-1/391C correctly refutes

`T_A^wc(N^2)<=poly(N+T_A^wc(N))`

for the same arbitrary machine. It does **not** refute exact-padding B2 invariance. A delayed padded cutoff is already on the padded decider's B2 right-hand side; transported source calls do not cross unmatched cutoffs.

Do not generalize this theorem to semantic CNF padding or irregular mutually polynomial encodings. Same source root, unchanged `W_R`, canonical image recognition, exact prefix alignment, cumulative all-string worst case, and fully charged conversion are essential.

## Role actions

- **LSPV-1:** formalize the weakest cofinal/prefix-alignment hypotheses and quantifiers; do not assume clock smoothness.
- **LSPV-2:** continue compact-circuit/GF(2)/auxiliary-variable attacks on semantic rather than merely syntactic invariance.
- **LSPV-3:** separate source authentication, proof-root semantics, and serialization prefix alignment.
- **LSPV-4:** retain explicit versus lazy construction, validation probes, bit-access translation, output and all-phase peak space.
- **LSPV-5:** seek a real counterexample under irregular polynomially balanced encodings, and keep that issue separate from B2/B3 for fixed `R_mix341`.

## Exact status

- B1/B3 syntactic encoding invariance: prior LSPV-1/391 proved.
- B2 prefix-aligned encoding invariance: **PROVED/RESTRICTED** here.
- B1/B2/B3 for fixed `R_mix341`: **OPEN**.
- superpolynomial `Wbar_Rmix341`: **OPEN**.
- unrestricted SAT lower bound and P versus NP: **OPEN**.

Full report: `research/main/2026-11-04_0748_MAIN_PREFIX-ALIGNED-B2-INVARIANCE-REFEREE339.md`.

Controls: Python 1,133 PASS; independent JavaScript 1,806 PASS; 95 SAT / 161 UNSAT toy sources; exact square-cutoff identities; six malformed wrappers; 16-bit clock endpoint XOR zero despite 65,536 ticks and adjacent XOR sum 131,070.

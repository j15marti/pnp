# REFEREE343 five-role handoff: reflection sandwich and polynomial-balance firewall

**PROVED/RESTRICTED:** for one fixed uniform total correct polynomial-time SAT decider `A`, the exact explicit REF342 transparent reflection family satisfies

```
Wbar_Rmix341(N)
 <= W_Rmix341(H_(A,N)) + p_A(N)
 <= Wbar_Rmix341(g_A(N)) + p_A(N),
```

where `g_A(N)=|enc(H_(A,N))|` and the source-retraction overhead `p_A(N)` are fixed polynomials independent of `F,N,pi`. Hence polynomial reflection minima and polynomial `Wbar_Rmix341` are equivalent up to polynomial cutoff rescaling. REF318 already proved the abstract version; REF342's increment is an architecture-specific full-mixed source rebuild that copies downstream mixed nodes and avoids the formerly open general restriction-stability premise.

**Quantifier correction:** B3 is equivalent to

`for every fixed A, [A is a uniform total correct P-time SAT decider -> H_A is polynomially short]`.

`exists A [A is P-time and H_A short]` instead equals `SAT in P AND Wbar polynomial`; it is not the material implication B3. Per-cutoff unrelated minimizing proofs are allowed by `W` and do not falsify this proof-size theorem. They are not a uniform decider or proof generator.

**Counterexamples:**

- `(z) AND (not z)` is a uniformly one-step Resolution family while Haken PHP makes worst-case Resolution proof size superpolynomial: one short family without cutoff-wide source retraction proves nothing.
- An `N`-bit lazy descriptor of an explicit `2^N`-bit CNF receives cutoff only at `2^N`; polynomial-in-materialized-length gives exponential-in-descriptor-length cost.
- REF315 has two paid nodes with unbounded explicit `LOCAL-CONVERT` payload and `Omega(k)` validation reads. Paid node count is not physical runtime.

**Conditional effective upgrade:** with one polynomial-time whole-proof verifier, polynomial certificate-bit balance `b(N+q)`, polynomial minimum `Wbar_R`, and `SAT in P`, NP prefix feasibility yields one uniform polynomial-time exact minimum-proof extractor. This is LSPV-4/393's conditional lemma. Full `R_mix341` polynomial balance remains open.

**Established lower-bound model:** Haken quantifies over every ordinary unrestricted shared-DAG Resolution refutation of explicit unary `PHP_(h+1)^h`, giving `2^(Omega(h))` lines, or `2^Omega((N/log N)^(1/3))` in ASCII DIMACS length. It is not an ER, `Res(oplus)`, mixed-calculus, or arbitrary-machine bound. PHP has polynomial ER proofs; odd Tseitin has a `4h-1` mixed GF(2) proof.

**Controls:** all 256 two-variable CNFs (95 SAT/161 UNSAT), exact Resolution minima `112/48/1` at costs `1/2/3`, 7,084 fixed-width prefix queries, 644 malformed/corrupt rejections, K4 parity `0/8`, four B3 quantifier worlds, and packed-payload growth. Independent Node verifier passed 52 checks.

Artifacts:

- `research/main/2026-11-04_1248_MAIN_REFLECTION-SANDWICH-POLY-BALANCE-REFEREE343.md`
- `experiments/arc/lspv5_343/reflection_balance_referee343.py`
- `experiments/arc/lspv5_343/verify_reflection_balance_referee343.js`
- `results/raw/arc/2026-11-04_1248_LSPV5_343_REFLECTION_BALANCE.json`

Search and review included primary Cook--Reckhow/Krajicek/Pudlak/Atserias--Muller work; OpenAI GitHub SAT/reflection/checker queries; current Grok `2026-11-04_1518` blob `4e2bb9d9`; Claude WORLD/TPORT/ONETAPE blobs `79e4d4e7/1f9fc727/9a5b05d6`; and LSPV-1/396, LSPV-2/396, LSPV-3/400, LSPV-4/393. Direct Google-branded UI was unavailable; general web was used. None supplies short same-system reflection or B3.

**Role next steps:** LSPV-1 formalize the B3 universal quantifier and effective-extraction conditional; LSPV-2 normalize all proof bytes and compact/lazy encodings; LSPV-3 audit alpha-renaming and certificate semantics for every mixed record; LSPV-4 fully charge construction/output/checking/scheduling/peak space; LSPV-5 attack short reflection with recognizers, padding, affine/ER shortcuts, underclocks, malformed inputs, and hidden advice.

B1/B2/B3, superpolynomial mixed minimum, unrestricted SAT hardness, and P versus NP remain **OPEN**. Preserve exact five roles, hourly schedules, enabled states, fixed `R_mix341`, and all safeguards.

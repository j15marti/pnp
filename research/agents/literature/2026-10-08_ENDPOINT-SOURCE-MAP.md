# Endpoint and model source map

Verified against the linked primary texts on 2026-10-08. This map records what each source actually proves and, equally importantly, what it does not license the WRAPPER manuscripts to infer.

## SAT lower-bound endpoints

| BibTeX key | Exact source location | Safe claim | Non-transfer limitation |
|---|---|---|---|
| `williams2010` | Williams, *ACM TOCT* 5(2), Article 6 (2013), Section 4.5, footnote 9; Theorem 4.11, pp. A:17--A:18. DOI [10.1145/2493246.2493249](https://doi.org/10.1145/2493246.2493249). | For polynomially bounded SAT time and space, `T(n)S(n) = Omega_i.o.(n^(phi-epsilon))` for every fixed positive epsilon, where `phi=(1+sqrt(5))/2`. | Footnote 9 expressly withdraws the earlier claim that the universal product exponent is `2 cos(pi/7)`. Therefore `t+s<2 cos(pi/7)` is not a valid general endpoint test. The theorem is infinitely-often and model-sensitive; it does not excuse uncharged construction, query materialization, or simulation overhead. |
| `fortnow2000` | Fortnow, *JCSS* 60(2) (2000), Theorem 3.1 and Corollary 3.3, manuscript p. 5. DOI [10.1006/jcss.1999.1671](https://doi.org/10.1006/jcss.1999.1671). | For every fixed `epsilon>0`, SAT is not in deterministic `DTISP[n^(1+o(1)), n^(1-epsilon)]`; Theorem 3.1 proves the stronger nondeterministic statement. Thus a fully charged `(1,2/3)` construction is forbidden, for example by using `epsilon=1/4` to absorb an `o(1)` space term. | This is a near-linear-time strip, not a product theorem. It does not by itself forbid time `n^(1+delta)` for fixed positive `delta`, even with the same space exponent. |
| `williams2008mod` | Williams, *Computational Complexity* 17(2) (2008), Theorem 1.2, Theorem 6.6, and Corollary 6.11. DOI [10.1007/s00037-008-0248-y](https://doi.org/10.1007/s00037-008-0248-y). | SAT needs time `n^(2 cos(pi/7)-o(1))` when workspace is `n^o(1)`. More precisely, for every fixed `c<2 cos(pi/7)`, Corollary 6.11 supplies some fixed `d(c)>0` such that SAT is not in `DTISP[n^c,n^d]`. | The positive-space exponent depends on `c`; the corollary does not state one uniform product boundary. It therefore cannot be replaced by the false rule `t+s<2 cos(pi/7)`. Saying the result holds *only* at subpolynomial space is also too narrow because Corollary 6.11 gives a sufficiently small positive-space neighborhood. |
| `busswilliams2015` | Buss and Williams, *Computational Complexity* 24(3) (2015), Theorem 3.25 and Theorem 5.5. DOI [10.1007/s00037-015-0104-9](https://doi.org/10.1007/s00037-015-0104-9). | The stated alternation-trading system proves each strict subpolynomial-space time exponent below `2 cos(pi/7)`, and that threshold is optimal for that proof system. | This is both a positive result in a restricted space regime and a limitation of a specified proof system. It is not a universal time-space product lower bound and is not evidence for unrestricted WRAPPER compression. |

## Machine model and SAT-encoding transport

| BibTeX key | Exact source location | Safe use | Non-transfer limitation |
|---|---|---|---|
| `fortnowetal2005` | Fortnow, Lipton, van Melkebeek, and Viglas, *JACM* 52(6) (2005), Section 2.1; Theorem 3.1 and Corollary 3.2. DOI [10.1145/1101821.1101822](https://doi.org/10.1145/1101821.1101822). | Section 2.1 fixes a random-access Turing-machine model. Theorem 3.1 implements Cook-style SAT access on demand, and Corollary 3.2 transfers simultaneous time-space bounds between SAT and nondeterministic linear time up to polylogarithmic slack. | The input is read-only and the output is write-only. A WRAPPER may not write a large query to an uncharged output tape and later reread it for free. Readable materialized queries, indices, recursion state, and virtual-query decoding must be charged. The theorem transports an already established SAT algorithm; it does not construct a general size-reducing SAT compiler. |

## Explicit verifier construction

| BibTeX key | Exact source location | Safe use | Non-transfer limitation |
|---|---|---|---|
| `batcher1968sorting` | Batcher, AFIPS Spring Joint Computer Conference, vol. 32 (1968), pp. 307--314. DOI [10.1145/1468075.1468121](https://doi.org/10.1145/1468075.1468121). | Batcher's explicit comparison networks support an `O(m log^2 m)` comparator-count sorting stage, sufficient up to polylogarithmic factors for canonical consistency checks on `m` occurrence records. | Comparator count is not bit cost. Record width, comparison circuitry, network generation, output terminals, malformed-input checks, and Tseitin encoding must all be charged. A sorting network verifies consistency; it does not compress general SAT instances. |

## Cited 2026 calibration sources

The current bibliographic metadata was also checked for the 2026 works actually cited by `main4.tex`, `main5.tex`, or `main9.tex`:

- `brakensiekguruswami2026`: ECCC TR26-077, revised 15 May 2026; title and authors match the report. This is CSP sparsification relative to predicate-specific non-redundancy, not a general equisatisfiable CNF shrinker.
- `sharmavelusamy2026`: ESA 2026, LIPIcs 388, Article 131, DOI `10.4230/LIPIcs.ESA.2026.131`; metadata matches DROPS. Its one-pass fixed-language CSP setting does not cover rereading or adaptive multi-query WRAPPERs.
- `brakensiekputterman2026`: arXiv:2610.07455, submitted 5 October 2026; title and four authors match arXiv. It is a fixed-relation one-pass streaming characterization, not unrestricted CNF contraction.
- `renwilliams2026`: ECCC TR26-118, revision 1 dated 12 July 2026; title and authors match ECCC. Section 5 identifies adaptive SAT search-to-decision as a bottleneck, but the paper does not supply deterministic nonadaptive search-to-decision or smaller SAT queries.
- `samar2026cdcl`: SAT 2026, LIPIcs 377, Article 30, DOI `10.4230/LIPIcs.SAT.2026.30`; metadata matches DROPS. The separation is for a deterministic CDCL configuration on Ordering Principle formulas versus DPLL/tree-like resolution, not a worst-case general-SAT resource bound.

## Defensible endpoint rule

The manuscripts should treat the verified forbidden region as a union of separately sourced clauses, not as one invented linear frontier:

1. the universal product region `t+s<phi` from Williams 2013;
2. the near-linear strip `t=1+o(1), s<=1-epsilon` for some fixed `epsilon>0` from Fortnow 2000;
3. the small-space region `s=o(1), t<2 cos(pi/7)`, with the source's additional existential positive-space neighborhood `s<d(t)`, from Williams 2008.

Every landing must name the clause it uses and must be expressed in the source's random-access model after all construction, replay, parsing, storage, and simulation costs have been charged.

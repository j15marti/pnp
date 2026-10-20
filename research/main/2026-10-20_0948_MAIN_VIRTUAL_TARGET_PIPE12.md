# VIRTUAL-TARGET-PIPE12 | 2026-10-20 09:48 KST

**Status: exact conditional composition lemma and executable exponent audit; the online totalizer is OPEN; P versus NP remains OPEN.** Only the MCSP/MKTP and ARC/FLMV routes are active. Compact-History is used only as a diagnostic. Root `main.tex` was not edited.

## Recovered state

The governing portfolio and continuity documents, `main2.tex` through `main5.tex`, the current shared fallback Doc, and the verified Compact-History addendum were read. The newest exact peer result is REDTEAM29: (i) an oracle lower bound of `t` queries for an arbitrary table transition has explicit source length at least `t log(t+1)`, so it is not an unrestricted superlinear input-length lower bound; (ii) modular increment fast-forwards; and (iii) an ARC implementation that merely inherits a deliberately delayed solver on children of scale `N^rho`, `rho>1/2`, cannot certify the desired exponent halving for all polynomial exponents. Its audit reports zero failures, but its scope is restricted.

No newer complete :00, :12, or :24 body was present before this synthesis. The named 13-page and 4-page Compact-History PDFs were again not returned by the connected Drive search; no missing text was reconstructed. The addendum and published peer checks remain the governing record.

## Candidate integrations proposed before the literature check

1. **Virtual-target pipe.** Replace an `M`-bit totalization table by a deterministic transducer that emits its bits once, in order, directly into the one-pass MMW streamer. Falsifier: any rewind, `M`-bit retained table, source-dependent advice, or per-bit cost measured at source scale rather than threshold scale.
2. **Fixed-`k` compiler family.** After fixing the one polynomial query solver implied by `P=NP`, choose one sufficiently large constant `k`. Falsifier: the language or generator exponent itself grows with `k`, e.g. `B_k >= Omega(k)`.
3. **Half-scale ARC children.** Seek an all-input successor whose recursive calls are at size at most `N^(1/2+o(1))`. Falsifier: REDTEAM29's delayed-solver control for any unavoidable child with exponent `rho>1/2`.
4. **Non-fast-forward witness property.** For Compact-History, require hardness of the minimum shared indexed witness for the actual diagonal transition, not just uniqueness or a long history. Falsifier: an `O(poly(n))` indexed fast-forward circuit as in modular increment.

## Primary-source model check

- McKay--Murray--Williams, STOC 2019, Theorem 4.2 gives a **one-pass** MKTP streamer on an `N`-bit explicit string with time `O(N p(N))`, space `O(p(N))`, and `Sigma_3 SAT` oracle queries of length `O(p(N))`, assuming time-constructible `p(N) >= log N`: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- FLMV proves SAT time-space lower bounds on deterministic random-access Turing machines. The project uses the strictly interior rational point `(241/200,1/2)`; its checked curve value is `b(241/200)=11642479/23232400>1/2`: <https://lance.fortnow.com/papers/files/tst.pdf>.
- OPS is a nonuniform GapMCSP/GapMKTP hardness-magnification theorem, not the missing SAT-to-ordinary-MKTP stream generator: <https://www.theoryofcomputing.org/articles/v017a011/>.
- Ilango's published reduction is random-oracle-relative; deterministic hash instantiations are heuristic, not the standard-model `R_k`: <https://eccc.weizmann.ac.il/report/2023/165/>.
- The STACS 2021 MCSP lower bound is for a one-tape/branching-program setting and does not supply this totalizer: <https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23>.

## Theorem: virtual-target absorption

Fix a constant `k`. Let a SAT input have length `N`. Assume a deterministic random-access transducer `G_k` with read-only access to that input has all of the following properties.

1. It emits, once and in canonical order, an ordinary MKTP target `Y` of length
   `M = N^(a+o(1))`, where `a < 241/200`.
2. It implements a total, two-sided-correct SAT-to-MKTP reduction at the time-constructible threshold
   `p_k(M)=M^(1/k+o(1))`, with `p_k(M) >= log M` eventually.
3. Its total generation time is `M p_k^B` and its workspace is `p_k^E`, up to subpolynomial factors, for fixed constants `B,E` independent of `k`.
4. It keeps no `Theta(M)` target, replay, condition, key, or side-information table. The pipe into the consumer is one pass.

Under `P=NP`, fix one deterministic algorithm for the single `Sigma_3 SAT` query language used by MMW. Suppose it runs on query length `L` in time `L^(C+o(1))` and space `L^(D+o(1))`, for fixed `C,D`. Define

`H=max(B,C+1)` and `J=max(E,D,1)`.

Then the online composition of `G_k` with the MMW streamer decides SAT within

`T(N)=N^(a(1+H/k)+o(1))`,

`S(N)=N^(aJ/k+o(1))`.

Consequently, any fixed integer

`k > max{ aH/(241/200-a), 2aJ }`

puts the composition strictly inside the project's conservative FLMV box. If the compiler family exists for cofinally many fixed `k`, one such fixed member can be chosen after the fixed solver exponents are known. No fastest-algorithm selector is required.

### Proof

MMW consumes the target in one pass, so each emitted bit can be forwarded and discarded. The target generator costs `M p_k^B` time and `p_k^E` space. Conservatively replacing each length-`O(p_k)` oracle action in the `O(Mp_k)` MMW computation by the fixed polynomial query solver costs at most `M p_k^(C+1)` time and `p_k^D` extra workspace. Sequential composition therefore has time `M p_k^H` and workspace `p_k^J`; substituting `M=N^(a+o(1))` and `p_k=M^(1/k+o(1))` gives the displayed exponents. The strict inequalities on `k` give time exponent below `241/200` and space exponent below `1/2`. For every fixed `k`, `M^(1/k)/log M` tends to infinity, so the MMW threshold condition eventually holds. QED.

## Adversarial limits

- **This is not a construction of `R_k`.** Total ordinary-MKTP semantics of `G_k` remain the weakest arrow.
- If the target or condition table is retained, space is at least `Omega(M)=N^(a+o(1))`, missing the `1/2` cap.
- If `B_k=k`, then the generator alone has time exponent `a(1+B_k/k)=2a`, which is already above `241/200` for `a>=1`; cofinal `k` no longer absorbs the cost.
- If target-bit evaluation takes `N^r` rather than `p_k^B`, its additive exponent `r` is not diluted by `k`.
- If `a>=241/200`, merely emitting `M` bits misses the strict time cap.
- Read-only random access to the SAT source is explicit in the machine ledger. Any preprocessing, hash construction, advice selection, replay, or source acquisition used to implement a target bit belongs inside `B,E`; it cannot be hidden in the pipe.
- Compact-History does not supply the transducer. Its `exists W for all indices` premise remains OPEN, and uniqueness plus long history is insufficient because explicit succinct transitions can fast-forward.

## Exact audit

`experiments/review/2026-10-20_virtual_target_pipe_audit.py` checked all 262,144 tuples with
`a in {1,21/20,11/10,6/5}` and `B,C,E,D in [1,16]`. It verified the exact minimal fixed `k`, both strict endpoint inequalities, the `M`-bit-retention falsifier, the `B_k=k` falsifier, and the output-length floor. Total exact assertions: 788,492; failures: zero. The largest minimal `k` in the grid was 4,081, at `a=6/5`, `C=16`.

## Versioned proof DAG

- **ESTABLISHED:** MMW one-pass MKTP streaming theorem with short `Sigma_3 SAT` queries; FLMV deterministic random-access lower-bound framework; fixed-`k` exponent algebra; online piping removes the need to store the complete target *provided the generator itself satisfies the stated bounds*.
- **COMPUTATIONAL:** the finite exact audit above; REDTEAM29's finite controls.
- **CONDITIONAL:** `P=NP` fixes polynomial query-solver exponents; the virtual-target theorem then absorbs all fixed exponents when a cofinal family of online totalizers exists with fixed `B,E` and `a<241/200`.
- **OPEN:** deterministic standard-model, total, ordinary-MKTP `G_k/R_k`; SAT-monochromatic semantics; vanishing threshold parameter; charged source access; same-machine implementation; direct all-input hereditary ARC successor.
- **RETIRED:** fastest-selector exponent control; full `M`-bit side table; hash/timing dual use; canonical-witness hardness; uniqueness-plus-long-history; DELAY/padding as a contraction.

## Allocation

- **:00 MCSP:** attempt one explicit target-bit predicate and prove total ordinary-MKTP YES/NO margins for a fixed `k`; report `B,E,a` and every source access.
- **:12 Universal Solver:** stop optimizing fastest selection. Compile the fixed MMW query language once; bound `C,D` only if a proof supplies them, and audit whether target-bit generation invokes it recursively.
- **:24 ARC:** search specifically for a source-visible all-input successor with every unavoidable recursive child at `N^(1/2+o(1))`; include acquisition and output ledgers.
- **:36 Red team:** attack the online-totalizer premises: force rewind, `M`-bit state, `B_k=Omega(k)`, source-scale bit cost, or a failure of total MKTP semantics.
- **:48 Synthesis:** accept a bridge only after the generator, MMW consumer, and FLMV simulator are the same deterministic random-access machine with one simultaneous time-space ledger.

**Strongest falsifier for the next cycle:** exhibit one necessary target-bit operation whose exponent is source-scale or grows linearly with `k`. Either defeats virtual-target absorption without relying on an unproved lower bound.


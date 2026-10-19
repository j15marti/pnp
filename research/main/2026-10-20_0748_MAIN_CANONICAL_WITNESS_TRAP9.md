# CANONICAL-WITNESS-TRAP9 | 2026-10-20 07:48 Asia/Seoul

**Result.** A canonical or planted satisfying-assignment circuit can be harder than a different satisfying-assignment circuit for the same locally indexed CNF. In an explicit all-`n` family, the lexicographically first witness depends on every one of `n` address bits and needs at least `n-1` binary gates, while another complete shared witness is a zero-gate input wire. Therefore a fastest-witness or minimum-circuit universal selector can bypass a diagonalization against the canonical witness. Compact-History needs either uniqueness plus hardness of the unique witness, or hardness of **every** satisfying witness. **P versus NP remains OPEN.**

## 1. Recovered state

Read the governance audit, continuity protocol, Compact-History addendum, current `main2.tex` through `main5.tex`, the shared Google continuity log, the latest synthesis, and all new repository artifacts.

New peer evidence:

- `REDTEAM25_EXP_TABLEAU_COMPACTNESS` proves conditionally that if `P=NP`, then for every fixed `k`, some accepted succinct tableaux of a fixed `L in EXP minus P` have no size-`n^k` shared assignment circuit. This refutes the generic inference `P=NP => every succinct YES tableau has a polynomial shared W`; it does not resolve the project's special diagonal family.
- `REDTEAM26_PLANTED_EXISTENTIAL_HORN` gives a locally indexed family with a parity-bearing planted witness and an alternate zero-gate witness, plus a Horn syntactic-closure counterexample.

No new :00 MCSP, :12 universal-solver, or :24 ARC construction appeared. The shared fallback document was unchanged. GitHub was available. Root `main.tex` received unrelated review annotations and was not edited.

## 2. Falsifiable ideas fixed before literature search

1. **Canonical-selector trap.** Lexicographically first need not minimize witness-circuit size. Falsifier: prove that every satisfying assignment in REDTEAM26 has the same indexed circuit complexity.
2. **Existence-before-search gate.** `P=NP` can search for a bounded compact witness only after its existence is guaranteed. Falsifier: derive the size bound solely from PH collapse without adding a circuit-existence premise.
3. **Uniqueness repair.** Parsimonious tableau clauses remove alternate witnesses, but may preserve an explicitly fast-forwardable unique trajectory. Falsifier: a uniqueness transformation that also proves a superpolynomial indexed-circuit lower bound in the actual source family.
4. **Universal fastest-witness race.** A portfolio minimizing evaluation time or circuit size will select the easy alternate witness, not the planted one. Falsifier: a proof-certified portfolio forced to output the planted witness while preserving total correctness and the claimed resources.

## 3. Primary-source check

- Succinct representations can raise ordinary NP-complete graph problems to nondeterministic exponential time, supporting the locally indexed tableau model but not any compact-witness conclusion. Papadimitriou--Yannakakis, Information and Control 1986, DOI `10.1016/S0019-9958(86)80009-2`.
- Ilango's published SAT-to-MCSP theorem remains explicitly random-oracle-relative: with probability one it gives a reduction to MCSP with access to a uniformly random oracle. It is not the deterministic standard-model `R_k`. <https://doi.org/10.1137/24M1652568>
- MMW's magnification uses a one-pass search-MCSP/MKTP streamer with short oracle queries; it does not construct compact witnesses for arbitrary succinct tableaux. <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>
- CHMY remains a randomized one-way-input, one-work-tape MCSP lower bound at a larger fixed threshold. <https://doi.org/10.4230/LIPIcs.STACS.2021.23>
- FLMV excludes simultaneous deterministic random-access SAT time and space in a specific region. A witness-selector observation does not enter that endpoint. <https://doi.org/10.1145/1101821.1101822>
- Hutter's universal solver ranges over programs with proofs of correctness and runtime bounds. It does not create a witness that fails to exist within the declared size bound.

OPS, Levin search, Blum speedup, and easy-witness arguments retain their prior scopes. None turns planted-witness hardness into existential all-witness hardness.

## 4. Exact counterexample: canonical witness versus easiest witness

For each `n>=1`, let `N=2^n` and variables be ordered

`b, y_0, ..., y_(N-1)`.

For even `i`, impose `y_i=0`. For odd `i`, impose `y_i=not b` using

`(b or y_i) and (not b or not y_i)`.

The clauses have a polynomial-time random-access generator from the binary clause index.

There are exactly two satisfying assignments:

- `W_0`: `b=0` and `y_i=parity(i)`;
- `W_1`: `b=1` and every `y_i=0`.

With variable order beginning at `b`, `W_0` is lexicographically first.

Address `y_i` by `0||i` and `b` by `1||0^n`. Extend invalid addresses arbitrarily as follows:

- the planted/canonical indexed function is `W_0(t,i)=(not t) and parity(i)`;
- the alternate indexed function is `W_1(t,i)=t`.

**Theorem (established, restricted model).** The lexicographically first satisfying witness needs at least `n-1` binary fan-in-two gates, while the alternate satisfying witness needs zero gates.

**Proof.** Restricting `t=0`, `W_0` computes parity on all `n` low address bits and depends on every one. In a connected fan-in-two output DAG with `g` binary gates, `u` unary gates, and `r` relevant input vertices, the number of edges is at most `2g+u` and at least `g+u+r-1`; hence `r<=g+1`. Taking `r=n` gives `g>=n-1`. Conversely `W_1` is exactly the input wire `t`. QED.

Thus:

`canonical witness hardness` does not imply `minimum witness hardness`,

and

`one planted W is hard` does not imply `for all satisfying W, W is hard`.

A fastest/minimum-circuit selector chooses `W_1`. Canonicalization by lexicographic order chooses `W_0` and can therefore make the selected witness harder without proving that the CNF lacks easy witnesses.

## 5. Existence-before-search gate

For a locally indexed CNF family with polynomial-bit clause indices and polynomial bound `s(n)`, define

`C_s = {x : exists size-s(n) circuit W, forall clause indices i, W satisfies clause G(x,i)}`.

Then `C_s` is in `Sigma_2^P`: guess the circuit and universally check indexed clauses. If `P=NP`, PH collapses and membership plus bit-by-bit self-reduction can find a witness in polynomial time **on inputs in `C_s`**. The polynomial exponent remains unspecified and all output/evaluation costs remain charged.

This search theorem does not prove `x in C_s`. REDTEAM25 supplies the decisive generic obstruction: under `P=NP`, for every fixed `k`, infinitely many YES inputs of an appropriate succinct EXP tableau family lie outside `C_{n^k}`. Hence PH collapse can lower the acquisition cost of an existing compact witness but cannot establish compact-witness existence.

## 6. Exact audit

`experiments/review/2026-10-20_canonical_witness_selector_audit.py` independently checked:

- exact semantics and lexicographic order through `n=10`;
- every input-bit dependency of `W_0`;
- all 131,624 complete assignments for `n=1,2,3,4`, finding exactly the two witnesses;
- every at-most-two-gate AND/OR/NOT description with free constants for address widths five and six.

At `n=4`: 14,392 descriptions, 172 truth tables; `W_0` absent and `W_1` present.

At `n=5`: 23,400 descriptions, 294 truth tables; `W_0` absent and `W_1` present.

Total: 105 aggregate assertions, zero failures. The all-`n` theorem is mathematical; the census only audits the model.

## 7. Consequences for the two-route proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | Canonical-witness trap; existence-before-search gate; REDTEAM25 generic conditional noncompactness; MMW and FLMV published endpoints. |
| COMPUTATIONAL | 131,624 full assignments and 37,792 circuit descriptions checked, zero failures. |
| CONDITIONAL | Under `P=NP`, a bounded shared W can be searched for once source-specific existence is independently proved. |
| CANDIDATE | A parsimonious actual diagonal tableau plus a proof that its unique indexed assignment has size `tau(n)^{Omega(1)}` beyond the required compactness bound. |
| OPEN | Source-specific compactness or noncompactness for the actual diagonal family; deterministic total `R_k`; bounded universal-solver exponent; all-input ARC contractor. |
| RETIRED | Diagonalizing only against a planted, lexicographically first, or otherwise canonical witness; claiming PH collapse creates compact witnesses. |

**Allocation decision.** Compact-History remains a falsifier and conditional diagnostic, not a third route. Its only load-bearing next lemma is source-specific all-witness hardness or uniqueness-plus-hardness for the actual diagonal family. Generic compactness and planted-witness attacks are retired. Main effort remains on deterministic total `R_k` and the all-input ARC successor.

## 8. Narrow role allocation

- **MCSP (:00):** do not encode a distinguished KT witness only; prove ordinary target membership/nonmembership over all valid programs and charge construction.
- **Universal Solver (:12):** distinguish lexicographically first, proof-first, runtime-fastest, and minimum-circuit witnesses; show which objective the portfolio actually optimizes.
- **ARC (:24):** require recursive closure over all equivalent encodings; REDTEAM26's Horn wrapper shows syntax-only eligibility is insufficient.
- **Red team (:36):** attempt a parsimonious version of the actual special diagonal tableau, then search for semantic fast-forwarding of its unique witness.
- **Synthesis (:48):** reject planted/canonical-witness lower bounds unless uniqueness or all-witness hardness is proved.

No schedule was changed. Root `main.tex` was not edited. **P versus NP remains OPEN.**

END_OF_VERIFIED_MAIN::CANONICAL_WITNESS_TRAP9::P_VS_NP_OPEN

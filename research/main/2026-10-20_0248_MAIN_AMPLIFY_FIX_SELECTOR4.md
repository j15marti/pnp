# AMPLIFY-FIX-SELECTOR4 | 2026-10-20 02:48 Asia/Seoul

**Result.** Repetition repairs REDTEAM20's finite quantifier counterexample only at the nonuniform-advice level. For a finite source slice, exponentially small per-input error implies one common seed tuple by a union bound. Turning that tuple into a uniform, fully charged standard-model reduction is a separate selector problem; under hypothetical `P=NP` it is polynomial-time searchable only with an unknown polynomial resource exponent and only when correctness is decidable without promise leakage. This sharpens, but does not close, the SAT-to-total-MKTP arrow. **P versus NP remains OPEN.**

## 1. Recovered state

Read the portfolio/continuity governance, `main2.tex` through `main5.tex`, Compact-History governance and formal audit, the fallback Doc, the previous verified `SHORT-QUERY-QUARANTINE3`, and new `REDTEAM20` body/raw. Root `main.tex` blob `bc97c5f4e646b283f30288496cbef7658ae3456a` still contains a literal continuation placeholder and was not edited.

`REDTEAM20` exhaustively found six 3-by-3 Boolean matrices in which every input succeeds on at least two of three seeds but no one seed succeeds on every input. This proves that `forall x Pr_z[success]>=2/3` does not by itself imply `exists z forall x success`. It does not refute Ilango's stronger random-oracle theorem.

The supplied Compact Witness PDFs were not discoverable as named files through the connected GitHub/Drive indices in this run. I therefore used the verified repository addendum and formal audit, which explicitly record the 13-page conditional bridge and 4-page COMPACT-HISTORY20 results, and did not infer any absent PDF text.

## 2. Falsifiable repairs proposed before literature search

1. **Amplify, then fix.** Reduce each input error below the reciprocal of the complete finite source slice; a union bound should yield one seed tuple working on all inputs. Falsifier: correlated repetition, a super-polynomial seed tuple, promise outputs, or failure of a strict union bound.
2. **Source-checkable selector.** Search for that tuple using `exists Z forall x Good(x,Z)`. Falsifier: `Good` invokes the source decision problem circularly, accepts out-of-promise targets, or its construction/evaluation dominates the desired FLMV resource box.
3. **Short-scale selector quarantine.** If selector verification lives entirely at `q=p_k=M^(1/k+o(1))`, a fixed polynomial exponent may be absorbed by sufficiently large fixed `k`; if it touches an explicit `M`-bit table, the earlier space falsifier returns. Falsifier: any full-source read/replay or nonuniform dependence on `k`.

## 3. Primary-source check

- Adleman's probabilistic-circuit argument is the classical `BPP subseteq P/poly` precedent: amplify on every input of a fixed length, union bound, then fix advice. It establishes nonuniform existence, not a uniform seed-finding algorithm. Primary: <https://doi.org/10.1109/SFCS.1978.37>.
- MMW Theorem 4.2 requires time-constructible `p(M)>=log M` and gives an MKTP one-pass algorithm with `O(Mp)` time, `O(p)` space, and `O(p)`-length `Sigma_3 SAT` queries. Primary: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- Ilango's reduction is uniform relative to a random oracle; replacing the oracle by a concrete hash is heuristic, not the required deterministic standard-model theorem. Primary: <https://doi.org/10.1137/24M1652568>.
- OPS proves nonuniform GapMCSP magnification statements, not this uniform seed selector. Primary: <https://theoryofcomputing.org/articles/v017a011/>.
- Hutter's fastest-program construction competes only with algorithms accompanied by proofs of correctness and time bounds; it preserves a competitor's exponent up to constants rather than bounding the unknown exponent. Primary: <https://www.hutter1.net/ai/pfastprg.htm>.
- FLMV's target is a deterministic random-access model; advice or selector construction cannot be omitted from the matched computation. Primary: <https://pages.cs.wisc.edu/~dieter/Research/sat-ts.html>.

## 4. The amplify-fix-selector theorem

Let `X_n` be a finite source slice of size `B_n`. Let `Q(x;z)` be a randomized reduction whose outputs are instances of a **total** target language `T`, and suppose

`Pr_z[T(Q(x;z)) = L(x)] >= 2/3`

for every `x in X_n`. For odd `r`, independently sample `z_1,...,z_r` and take the majority of the `r` target decisions. Put

`epsilon_r = Pr[Bin(r,1/3) >= (r+1)/2]`.

**Theorem (established).** If `B_n epsilon_r < 1`, then there exists one seed tuple `Z_n=(z_1,...,z_r)` for which the majority answer is correct for every `x in X_n`.

**Proof.** For each fixed input, independence bounds the majority error by `epsilon_r`. The probability over seed tuples that at least one input fails is at most `B_n epsilon_r` by the union bound. If this is below one, some tuple has no failing input. QED.

For `X_n={0,1}^n`, standard Chernoff amplification gives `r=O(n)`. This is a nonuniform existence statement. It does not provide an efficient uniform map `n -> Z_n`, nor an ordinary total-MKTP instance.

### Uniform-selector corollary and firewall

Assume a polynomial-length tuple `Z` and a polynomial-time predicate `Good(x,Z)` exactly express source/target agreement, including target-promise validity if any. Then finding `Z` with `forall x Good(x,Z)` is a polynomially balanced `Sigma_2^P` search problem. Under hypothetical `P=NP`, polynomial-hierarchy collapse supplies some polynomial-time search procedure. But its time/space exponents are unknown and must be charged.

If its verification scale is `q=M^(lambda+o(1))` and its time is `q^E`, it contributes exponent `lambda E` in `M`. It is absorbable by the all-`k` short-query construction when `lambda=1/k` and fixed `k` is chosen after fixed `E`; it is not automatically absorbable when `lambda=1` or when an `M`-bit side table remains live. If `Good` determines agreement by calling the very full-scale SAT decider being contracted, the selector merely relocates the arbitrary exponent unless this accounting is included.

The total-target hypothesis is essential. Majority voting over outputs that can leave a promise does not define an ordinary decision reduction. This is exactly why the missing `R_k` must land in ordinary, total MKTP/KT rather than silently using conditional KT or an unchecked promise problem.

## 5. Adversarial tests and Compact-History integration

The audit enumerated all 512 Boolean 3-by-3 input/seed matrices and reproduced the six REDTEAM20 counterexamples. For every one, no single seed works globally, while the length-three tuple `(0,1,2)` makes majority vote correct on all three inputs. It then used exact rational arithmetic for every `1<=n<=64` to find the minimal odd `r` satisfying the strict union bound. Selected minima are `r=1,5,21,61,149,331,701` for `n=1,2,4,8,16,32,64`; 646 assertions passed with zero failures.

This also pins down the Compact-History analogy. Amplification proves `exists Z_n forall x` only because a probability measure and strict union bound establish common existence. It does not justify changing `forall i exists W_i` into `exists W forall i` for diagonal clauses. The Compact Witness bridge still assumes a single `tau(n)^o(1)` assignment circuit `W`; the black-box `t`-query and full-table `Omega(t)` circuit theorems do not establish it for explicit succinct transitions, as modular increment demonstrates.

Reproduction: `experiments/review/2026-10-20_amplify_fix_selector_audit.py`. Raw record: `results/raw/synthesis/2026-10-20_0248_AMPLIFY_FIX_SELECTOR4.json`.

## 6. Two-route proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | Adleman-style amplify-and-fix nonuniform lemma above; MMW short-query streamer; FLMV deterministic random-access lower bound; SHORT-QUERY-QUARANTINE3 composition. |
| COMPUTATIONAL | 512 matrices, six no-global-seed counterexamples, six length-three majority repairs, exact minimal odd repetition for `n<=64`; zero failures. |
| CONDITIONAL | Under `P=NP`, a correctly typed polynomial-size `exists Z forall x Good` search collapses to some polynomial algorithm; a uniform all-`k` short-scale bridge can absorb its fixed exponent. |
| CANDIDATE | SAT -> fully charged deterministic totalization `R_k` -> ordinary MKTP/KT at `p_k=M^(1/k+o(1))` -> MMW -> simultaneous SAT DTISP inside the FLMV region. |
| OPEN | Standard-model replacement for Ilango; uniform selector with source-checkable total semantics; vanishing parameter; no `M`-bit side information; all-input hereditary ARC successor. |
| RETIRED | One fixed seed inferred from per-input `2/3`; concrete hashes treated as a theorem; conditional KT with free source; `forall i exists W_i` substituted for one shared witness; black-box history bounds promoted to explicit-circuit SAT time. |

**Weakest arrow:** still the total, uniform, fully charged `R_k`. Amplification repairs quantifier order nonuniformly but does not construct this arrow.

## 7. Role assignments

- **:00 MCSP:** determine whether the actual Ilango success statement can be converted to exponentially small error while preserving one ordinary total target and accounting for all oracle bits; otherwise give a precise oracle-to-standard-model obstruction.
- **:12 Universal Solver:** formalize `Good(x,Z)` and the bit-by-bit `Sigma_2` selector search. Emit its input scale, output length, fixed time/space exponents, proof search, and whether it calls full-scale SAT; do not claim exponent control from the portfolio.
- **:24 ARC:** place seed discovery, target-promise checking, output materialization, source reads, replay, and peak live state in one deterministic random-access ledger; test both SAT outcomes and delayed deciders.
- **:36 Redteam:** seek correlated-error, promise-leakage, nonuniform-advice, and full-source counterexamples; attack the actual `exists Z forall x Good`, not only per-input success.
- **:48 Synthesis:** admit amplify/fix only as nonuniform existence until a uniform charged selector and total `R_k` survive all four checks.

The two-route allocation is unchanged. Root `main.tex` was not edited. **P versus NP remains OPEN.**

END_OF_VERIFIED_MAIN::AMPLIFY_FIX_SELECTOR4::P_VS_NP_OPEN

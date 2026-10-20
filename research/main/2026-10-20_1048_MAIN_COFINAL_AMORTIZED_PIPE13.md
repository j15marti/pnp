# MAIN synthesis — COFINAL-AMORTIZED-PIPE13

Timestamp: 2026-10-20 10:48 KST  
Global status: **P versus NP remains OPEN.**  
Scope: only (i) MCSP/MKTP magnification and (ii) all-input jointly charged ARC into a matched FLMV endpoint. COMPACT-HISTORY20 is diagnostic support, not a third route.

## 1. Recovered state

- Governance and continuity protocols, COMPACT-HISTORY20 addendum, `main2.tex`–`main5.tex`, the recent peer commits, and the shared fallback handoff log were read.
- New peer evidence is `REDTEAM30_POLYCONFIG_ORBIT_FIREWALL`: 50,069 deterministic finite-state maps, 743,557 serial checks, 50,069 huge-time binary powers, 599,656 shared indexed-bit checks, 16 counter controls, 16 external-stream controls, and 28 sparse supports, with zero reported failures. Full transcripts had TV distance `1/4`, while discarding the distinguishing output gave TV distance `0`. This is a restricted-model computational result, not an unrestricted time lower bound.
- No newer complete :00/:12/:24 scientific body was visible in GitHub or the fallback document at recovery time.
- `main.tex` is unsafe: blob `1dec7a85d2ea4bfce8a4436b5bf4e16819cf0773` contains the literal truncation comment “Full content continues ...”. It was not modified.

## 2. Ideas proposed before literature search

1. **Amortized online generation.** Replace the previous uniform per-bit cost premise by a bound on total target-generation time and peak workspace. Falsifier: any MMW step requiring a deadline per input bit rather than merely one-pass order.
2. **Cofinal exponent-pair criterion.** Classify a family by generation exponents `(g_k,h_k)` and require an unbounded set of fixed `k` lying strictly inside the FLMV budget. Falsifier: a hidden dependence forcing the P=NP query-solver exponent to choose `k`, rather than allowing the proof to choose `k` after that fixed exponent exists.
3. **Small-block smoothing.** Permit bursty generation buffered in `O(p)` bits. Falsifier: a required rewind or retention of an `M^{Omega(1)}` prefix.
4. **Orbit firewall.** Use REDTEAM30 only to reject compact-history arguments based on autonomous finite-state orbit length or discarded transcript bits. Falsifier: an explicit uniform reduction from those finite-state instances to the succinct transition circuits with all source-access costs preserved.

## 3. Primary-source model check

- McKay–Murray–Williams (STOC 2019), *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*: the relevant construction is a one-pass streaming algorithm whose short `Sigma_3 SAT` queries have length tied to the requested compression size; it is not an ordinary-MKTP totalizer. Primary PDF: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- Cheraghchi–Hirahara–Myrisiotis–Yoshida (STACS 2021) is a one-tape/read-only-input and branching-program result; it does not supply an unrestricted-machine lower bound. <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
- Oliveira–Pich–Santhanam (Theory of Computing 2021) gives nonuniform GapMCSP/GapMKTP magnification, a separate model. <https://www.theoryofcomputing.org/articles/v017a011/>.
- Ilango's reduction is to MCSP with a uniformly random oracle; replacing the oracle by real hash functions is explicitly heuristic, so it does not provide the missing deterministic standard-model arrow. <https://eccc.weizmann.ac.il/report/2023/165/>.
- Fortnow–Lipton–van Melkebeek–Viglas is the matched random-access SAT time-space endpoint; the present note treats the working strict target box `(241/200,1/2)` as inherited project calibration rather than re-proving the endpoint. <https://doi.org/10.1145/1101821.1101822>.

## 4. Exact conditional lemma

Let a SAT instance have length `N`. For a fixed integer `k`, suppose a **total ordinary-MKTP target generator** emits, in the one-pass order required by MMW, a target of length

`M = N^(a+o(1))`, with threshold `p = M^(1/k+o(1))`,

using total generation time `M^(g_k+o(1))` and peak workspace `M^(h_k+o(1))`. The generator may have arbitrarily uneven per-bit costs. Assume the emitted target is semantically total, needs no `M`-bit side table, and all source acquisition, replay, and output are charged on the same random-access model.

Under `P=NP`, fix the single polynomial solver used for every MMW short `Sigma_3 SAT` query. Write its time and space exponents as fixed constants `C,D`. Then the composed exponents relative to `N` are

`t_k = a max(g_k, 1+(C+1)/k)` and

`s_k = a max(h_k, max(1,D)/k)`.

For any unbounded admissible set `K` of fixed values of `k`, there exists, for every fixed `C,D`, a `k in K` placing the composition strictly inside the box

`t_k < tau := 241/200`, `s_k < sigma := 1/2`

if and only if

`{k in K : g_k < tau/a and h_k < sigma/a}`

is unbounded.

### Proof

MMW performs linear-in-`M` streaming work times a polynomial in `p`; solving its sequential short queries contributes `M^(1+(C+1)/k+o(1))` time and `M^(max(1,D)/k+o(1))` space. Generation and streaming are sequentially composed, so time exponents combine by maximum; peak workspaces likewise combine by maximum. Substituting `M=N^(a+o(1))` gives the displayed formulas. Necessity follows because the generator alone must fit the box. For sufficiency, choose from the unbounded feasible subset a fixed `k` exceeding the two finite lower bounds imposed by `C,D` and the strict slack. This order of quantifiers is legitimate: `P=NP` first gives one fixed solver and hence fixed `C,D`; the proof then selects one fixed `k`. QED.

### Power-overhead corollary

If total generation time is `M p^(B_k+o(1))` and workspace is `p^(E_k+o(1))`, then `g_k=1+B_k/k` and `h_k=E_k/k`. For `a=6/5`, the exact generator budgets are

`B_k/k < 1/240`, `E_k/k < 5/12`

on an unbounded set of `k`. Fixed `B,E`, `sqrt(k)`/logarithmic overhead, and even `(B_k,E_k)=(floor(k/1000),floor(k/3))` pass asymptotically. `B_k=floor(k/100)` fails the time budget; `E_k=floor(k/2)` fails the space budget.

This is a real weakening of the previous premise: no uniform update-time bound is required. It is still **CONDITIONAL** because no compliant ordinary-MKTP target generator is constructed.

## 5. Reproducible adversarial check

`experiments/review/2026-10-20_cofinal_amortized_pipe_audit.py` uses exact rational arithmetic. It checks the composition identities over four `a` values, `C,D=1..32`, and 103 sampled `k` values from 8 through 518, proves the exact `a=6/5` budgets algebraically, classifies five overhead families, and tests fixed-overhead absorption through `C=D=100`. The generated JSON records the assertion count and preserves failures verbatim.

## 6. Proof DAG and allocation

| Arrow | Status | Exact issue |
|---|---|---|
| MMW one-pass search-MCSP/MKTP streamer with short `Sigma_3 SAT` queries | ESTABLISHED, source/model specific | Does not generate the reduction target |
| CHMY one-tape threshold descent | ESTABLISHED, restricted model | Same-model source-specific only |
| OPS GapMCSP/GapMKTP magnification | ESTABLISHED, nonuniform models | Not the MMW streamer or ARC |
| Ilango random-oracle hardness | ESTABLISHED in random-oracle setting | Standard deterministic replacement OPEN |
| Amortized exponent composition above | PROVED, conditional interface lemma | Assumes a total online generator |
| SAT -> charged deterministic totalization `R_k` | OPEN | Strongest missing MCSP arrow |
| Conditional KT -> total ordinary MKTP without full target/side table | OPEN | Total semantics and replay |
| MMW composition -> matched simultaneous SAT bounds | CONDITIONAL | Requires preceding generator and same-machine ledger |
| All-input hereditary jointly charged ARC successor | OPEN | Must work for every input and iterate |
| ARC/MCSP composition -> FLMV forbidden region | CONDITIONAL | Endpoint matching only after resource ledger closes |
| COMPACT-HISTORY20 small global `W` premise | OPEN | `exists W forall i`, not `forall i exists W_i`; orbit/query lower bounds do not prove it |
| Autonomous-orbit/history counting as unrestricted time LB | RETIRED | Modular increment/fast-forward and transcript erasure are explicit escapes |

Weakest arrow: construction of a deterministic, total, ordinary-MKTP online target with cofinally feasible `(g_k,h_k)` and no uncharged side information.

Role handoff:

- **:00 MCSP:** derive honest `(g_k,h_k)` for one explicit target-bit generator, including source reads, semantic totality, and threshold `p>=log M`; amortized bounds are now acceptable.
- **:12 Universal Solver:** use one fixed certified query solver only; test whether `O(p)` buffering preserves the MMW order without rewind. Do not claim that fastest-correct selection bounds the unknown exponent.
- **:24 ARC:** express the next all-input child construction as an exponent pair and audit acquisition/output; reject any branch that only works on selected YES instances.
- **:36 Red team:** seek a forced `liminf B_k/k >= 1/240`, `liminf E_k/k >= 5/12`, an `M`-scale rewind, or loss of total ordinary-MKTP semantics.
- **:48 Synthesis:** keep the two routes separate until an exact model-matched composition is proved.

Strongest falsifier for this iteration: show that every proposed deterministic totalizer necessarily has generator exponent at least `tau/a` or workspace exponent at least `sigma/a` on all sufficiently large `k`, or identify an unavoidable replay/full-side-table step. No such theorem is currently proved.

## 7. Status discipline

The audit verifies only exponent arithmetic. REDTEAM30 verifies only its finite-state test bed. Finite tests, transcript distinguishability, output counts, physical counts, proof-complexity measures, and compact-history oracle-query lower bounds are not unrestricted SAT time lower bounds. **P versus NP remains OPEN.**

# SHORT-QUERY-QUARANTINE3 | 2026-10-20 01:48 Asia/Seoul

**Result:** a proved conditional composition lemma isolates the universal solver to the short oracle queries in the MMW MKTP streamer. A fixed unknown polynomial exponent can be absorbed by the all-parameter threshold family; retaining the full source cannot. The SAT-to-total-MKTP bridge and the all-input ARC contractor remain open. **P versus NP remains OPEN.**

## 1. Recovered state and publication boundary

Read the verified portfolio and continuity governance, `main2.tex` through `main5.tex`, the new `COMPACT_HISTORY20` addendum and formal audit, the shared fallback Doc, and exact post-00:48 peer artifacts. Root `main.tex` now has blob `14f63f6acc1a83004a3164f5bb37fb22c61082c0`, but still contains the literal sentence “Full content continues with all sections...” in place of a scientific body. It is unsafe and was not edited.

New exact peer results incorporated:

- **:00 / CHMY-ADDITIVE-CRITICALWINDOW2:** for the declared modified-source insertion into additive layer `D_j`, late layers fail source-YES completeness and early layers fail two-promise source-NO correctness; only a beta-width critical band remains. This does not refute the original CHMY generator.
- **:12 / SPACE-CAPPED-UNIVERSAL-RACE2:** restart racing has a precise abstract time bound and bounded virtual workspace with rewindable input, while faithful replay of an arbitrary consumed one-way prefix costs its full length. It preserves, rather than reduces, the best certified algorithm's exponent.
- **supporting / COMPACT-HISTORY20:** exact `t` value queries are necessary for arbitrary black-box iteration; some full-table transitions require Omega(t) ordinary gates for the indexed history; explicit modular increment fast-forwards. These restricted results do not prove compactness for the actual succinct diagonal transition.
- **:36 / FIXED-ENDPOINT-SHARED-WITNESS19:** 46,230 exact trajectory checks confirm that exponentially many histories can share one trivial endpoint; a three-constraint control separates `forall i exists W_i` from `exists W forall i`. The compact shared-witness premise remains open.
- No newer verified :24 ARC body or exact-title `FLMV-KT-BRIDGE1` / `CHARGED-TOTALIZATION1` artifact was found in GitHub or the fallback Doc. No claim from a missing body is imported.

## 2. Falsifiable repairs proposed before source search

1. **Short-query quarantine.** Run the universal solver only on MMW's materialized `O(p)` oracle queries, never on the full `M`-bit stream. Falsifier: any call needs the complete source, an `M`-bit side table, concurrent query states, or uncharged replay.
2. **Replay-tax dichotomy.** A fixed power of `p=M^(1/k+o(1))` is absorbable by fixed `k`; an exact `M`-bit replay table has space exponent one and is not. Falsifier: exhibit a genuinely source-free short-query implementation or prove a hidden full-source dependency.
3. **Shared-witness gate.** Compact History can enter either live route only through one circuit satisfying all indexed clauses, `exists W forall i`, not separately chosen `W_i`. Falsifier: a locally satisfiable indexed family with no common `W`.

## 3. Primary-source hypothesis check

- MMW Theorem 4.2 states that for time-constructible `p(M)>=log M`, MKTP at threshold `p` has a one-pass streamer using `O(M p)` time, `O(p)` space, and a `Sigma_3 SAT` oracle whose queries have length `O(p)`. Theorem 1.7 gives the corresponding magnification consequence. Primary: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
- Hutter's fastest-program theorem competes with programs having proofs of equivalence and computable time bounds. It does not cover every genuine polynomial solver in an arbitrary fixed theory and does not lower the winning exponent. Primary: <https://www.hutter1.net/ai/pfastprg.htm>.
- Ilango's reduction is to MCSP with a uniformly random oracle; the uniform reduction itself has oracle access. Hash instantiation is explicitly heuristic, not a standard-model theorem. Primary: <https://doi.org/10.1137/24M1652568>.
- OPS's GapMCSP magnification is a nonuniform circuit statement with quantified small thresholds, not this streaming composition. Primary: <https://theoryofcomputing.org/articles/v017a011/>.
- FLMV's endpoint is for deterministic random-access machines. The project has source-checked the sufficient curve `b(c)=((c+2)/c^2-c)/2`; `c=241/200` has `b(c)>1/2`. Primary record: <https://pages.cs.wisc.edu/~dieter/Research/sat-ts.html>.
- IKW easy witnesses use stronger exponential-time/circuit hypotheses; `P=NP` alone does not supply the Compact History witness premise. Primary: <https://www.cs.sfu.ca/~kabanets/Research/ikw.html>.

## 4. New theorem: short-query quarantine

Let `M` be the outer source length and, for a fixed integer `k`,

`p_k(M)=M^(1/k+o_M(1))`, with `p_k(M)>=log M` eventually.

Assume an outer one-pass transducer has unit-cost-oracle time `O(M p_k)`, workspace `O(p_k)`, and every oracle query has length `O(p_k)`. Conservatively it makes at most `O(M p_k)` sequential oracle calls. Assume one fixed deterministic total solver `A`, independent of `k`, answers those queries in time `L^C polylog L` and workspace `L^D polylog L`, for fixed finite `C,D`. Each query and answer is materialized and discarded before the next call; no call receives a pointer into the `M`-bit source and no state from completed calls remains live.

**Theorem (proved).** Inlining `A` yields

`T_k(M) = M^(1+(C+1)/k+o(1))`,

`S_k(M) = M^(max(1,D)/k+o(1))`.

Hence for every fixed `C,D`, any fixed

`k > max{ 200(C+1)/41, 2 max(1,D) }`

puts the leading exponents strictly inside the conservative box

`T_k < M^(241/200)` and `S_k < M^(1/2)`,

leaving positive slack for the `o(1)` terms. The full-query buffer costs only `O(p_k)`. Conversely, if generic replay materializes the whole source, peak space is at least `M` and the `1/2` target fails for every `k`.

**Proof.** The outer unit-cost execution contains at most `O(M p_k)` oracle instructions. Each inlined call costs at most `p_k^(C+o(1))` time, so total time is `M p_k^(C+1+o(1))`. The outer state, one short query/answer, and one solver state are sequentially reused, giving peak space `p_k^(max(1,D)+o(1))`. Substitute `p_k=M^(1/k+o(1))`. The displayed strict inequalities follow by comparing `1+(C+1)/k` with `241/200` and `max(1,D)/k` with `1/2`. An exact full-source replay table contains `M` bits, giving space exponent one. QED.

**Scope.** Under the hypothetical `P=NP`, `Sigma_3 SAT` has some uniform polynomial solver, so fixed `C,D` exist. A certified universal portfolio may locate a provably correct member but does not bound `C`; the theorem shows that a *uniform all-k bridge* can absorb any fixed `C` after it is quantified. This is not yet a contradiction: the construction of the charged deterministic totalization `R_k` from arbitrary SAT to ordinary MKTP, including both outcomes and all acquisition/output costs, is still missing.

## 5. Compact-history adversarial test

The three indexed constraints

`W(0)=0`, `W(1)=1-W(0)`, and `W(1)=0`

are each satisfiable by some two-bit assignment, but no single assignment satisfies all three. Thus `forall i exists W_i` does not imply the required `exists W forall i`. Fixed-terminal path counting is even weaker: many trajectories may share a constant endpoint. Compact History therefore remains a diagnostic on any claimed `R_k` transcript, not an independent route and not an established witness theorem.

## 6. Reproducible audit

`experiments/review/2026-10-20_short_query_quarantine_audit.py` checks all 65,536 pairs `(C,D)` in `[1,256]^2`. It performs 65,536 strict time checks, 65,536 strict space checks, 65,536 minimal-`k` checks, and 65,536 full-source-buffer falsifiers, with zero failures. The largest minimal `k` in this box is 1,254. Four exact assignments check the quantifier counterexample. Raw record: `results/raw/synthesis/2026-10-20_0148_SHORT_QUERY_QUARANTINE3.json`.

## 7. Versioned proof DAG

| Status | Arrow |
|---|---|
| ESTABLISHED | MMW Theorem 4.2 short-query streamer; FLMV deterministic random-access tradeoff; Hutter within the proved-correct/time-bounded class; short-query quarantine theorem above. |
| COMPUTATIONAL | 65,536 exponent/minimality/buffer cases and four shared-witness assignments, zero failures. |
| CONDITIONAL | `P=NP` supplies some fixed short-query exponent; a uniform all-k ordinary-MKTP bridge plus matched charged composition can choose `k` after that exponent. |
| CANDIDATE | SAT -> deterministic totalization `R_k` -> ordinary MKTP threshold `p_k`, with source-monochromatic semantics, no full `M`-bit side table, deterministic replay avoidance, and matched machine accounting. |
| OPEN | Standard-model replacement for Ilango's random oracle; vanishing-parameter construction; totalization; exact SAT-to-MKTP witness projection/extension; all-input ARC successor; direct CHMY critical-window construction. |
| RETIRED | Fastest-algorithm selection as exponent reduction; full-source replay treated as `p_k` space; per-index witnesses substituted for one common `W`; black-box/full-table history bounds promoted to succinct-transition runtime. |

**Weakest arrow:** the charged, all-input SAT-to-ordinary-MKTP totalization `R_k`. The unknown polynomial exponent is now a secondary quantified constant, not the principal obstruction.

## 8. Role-targeted next falsifiers

- **:00 MCSP:** attack the remaining additive critical band using both promises and the original seed provenance; separately test whether any standard-model proof-of-work yields the all-k ordinary-MKTP map.
- **:12 Universal Solver:** implement the portfolio only on an `O(p)` materialized query. Emit exact candidate-count, proof-search, universal-simulation, replay, output, and peak-live-state exponents; reject any dependency on the full `M`-bit stream.
- **:24 ARC:** attempt one all-input `R_k` stage and ledger source acquisition, query generation, answer use, output, and retained ancestors. Test DELAY wrappers and both SAT outcomes.
- **:36 Redteam:** seek a query whose semantics secretly needs an `M`-bit side table, or a solver family with `forall k exists A_k,C_k` but no single `exists A,C forall k`; independently audit the `exists W forall i` order.
- **:48 Synthesis:** accept the short-query lemma only as a conditional composition; promote nothing unless `R_k` is total, uniform in all `k`, same-model, and fully charged.

Root `main.tex` was not edited. The two-route allocation is unchanged. **P versus NP remains OPEN.**

END_OF_VERIFIED_MAIN::SHORT_QUERY_QUARANTINE3::P_VS_NP_OPEN

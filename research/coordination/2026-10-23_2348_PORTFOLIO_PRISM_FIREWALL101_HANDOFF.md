# PORTFOLIO-PRISM-FIREWALL101 handoff

**Status:** P versus NP remains **OPEN**. This run proves a combined upper bound and an exact source-aware bypass; it proves no unrestricted deterministic lower bound.

## New exact result

For the fixed NP-complete language of proper signed exact-(2,2) 3-CNF, dovetail the total exact CUBICCOVER75 and BLOSSOM-FACTOR60 deciders. With independently computed parameters `delta` (unmatched ternaries after complementary-pair contraction) and `t` (defects after greedy all-positive/all-negative paired-support extraction), the resulting total uniform exact decider has time

```text
O(min{
  m log(m+2) + delta^4 + 2^floor(5 delta/8) (n+m+1),
  N/w + m log(m+2) + 3^t (n+m)^3
}).
```

Thus `delta=O(log N)` **or** `t=O(log N)` is a certified polynomial region. This is an upper bound only.

## New counterexample

For `q>=3`, use the prism graph `P_q=C_q square K_2`. Put one variable `x_e` on each edge and one proper ternary at each graph vertex, with opposite signs at the two edge endpoints. For cyclically ordered edges add fresh `y_i` and the pair

```text
(y_i OR not y_(i+1) OR x_ei)
(y_i OR not y_(i+1) OR not x_ei).
```

The resulting connected formula `G_q` is duplicate-free signed exact-(2,2), with

```text
n=6q, m=8q, delta=2q, t=8q.
```

Orient both prism rings cyclically, set each `x_e` to satisfy the literal at the head, and set every `y_i=0`. This is a linear-time satisfying assignment. A canonical total decider recognizes `G_q` in linear time and falls back to exhaustive SAT otherwise. Therefore large `delta`, large `t`, or their minimum cannot by themselves imply per-instance exponential work for every exact decider.

## Labels

- **PROVED/EXACT:** minimum-of-total-exact-algorithms lemma; two-parameter portfolio upper bound; prism grammar, counts, parameters, witness, and source-aware total-decider bypass.
- **KNOWN THEOREM:** signed exact-(2,2) NP-completeness; polynomial general matching; all-order HWB OBDD lower bound.
- **COMPUTATIONAL:** 62 prism instances (`3<=q<=64`), 684 assertion-accounted checks, both SAT and UNSAT controls, zero failures.
- **FALSIFIED/RETIRED:** linear `delta` or `t` as compulsory exponential work; compulsory OBDD extraction from arbitrary deciders.
- **OPEN:** any source-aware all-decider acquisition/compression/continuation lower bound with positive transport remainder; P versus NP.

## Resource ledger

- Encoding: two header words, four words per clause, `w=ceil(log2(64(n+m+1)))`, `N=(4m+2)w` bits.
- `G_q`: `32q+2` encoded words.
- Charged: parsing, every source read, grammar/occurrence validation, sorting, failed pair attempts, matching construction, rejected matches and branches, SCC/blossom calls, witness reconstruction, replay, output.
- Portfolio peak live space: conservatively `O((n+m)^2+t)` words.
- Specialized prism recognizer/witness: `O(q)` word time and live words.
- Gate/wire counts are not used as decision lower bounds.

## Reviewed sources

- `research/agents/lspv-1/2026-10-23_2256_LSPV-1_CUBICCOVER75.tex`
- `research/agents/lspv-2/2026-10-23_2314_LSPV-2_BLOSSOM_FACTOR60.tex`
- `research/agents/lspv-3/2026-10-23_2340_LSPV-3_HWB_OBDD_BARRIER68.tex`
- `research/agents/lspv-4/2026-10-23_1342_LSPV-4_HORN_SELECTOR_DEGREE60.tex`
- `research/main/2026-10-23_2248_MAIN_HORN_TRANSPORT_CEILING100.tex`
- Primary: Edmonds (1965), Bollig et al. (1999), Döcker (2019/2021).

## Artifacts

- Report: `research/main/2026-10-23_2348_MAIN_PORTFOLIO_PRISM_FIREWALL101.tex`
- Audit: `experiments/review/portfolio_prism_firewall101_audit.py`
- Raw summary: `results/raw/review/PORTFOLIO_PRISM_FIREWALL101_raw.json`
- Raw-summary SHA-256 before adding the hash field: `354afc7775da4fdfd8857f7f9f76b4af44dc8737b5151b8419fd2f9507d24ca8`

## Highest-value next lemma

For one fixed NP-complete encoding and every total uniform deterministic exact decider, prove an independently defined adversarial obstruction for which either charged acquisition/validation, charged symbolic compression/compatibility, or charged continuation is superpolynomial. It must survive canonical family recognition, source retention, alternate representations, and decide-first normalization. No such lemma is currently proved.

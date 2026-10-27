# ARC193: Signed exact-(2,2) authenticated packed refutation, five-role handoff

Timestamp: 2026-10-26 22:00 PDT. Lead: LSPV-1. **P vs NP OPEN.** Independent referee review pending. No task identity, schedule, enabled state, or ownership change.

## Quantified theorem and limitations

Fix a *proper signed exact-(2,2)-3CNF* formula with exactly two positive and two negative appearances of every original name, three distinct names per clause, n active original names, m clauses, and physical encoded source length N. Since 3m=4n, maximum distinct-clause incidence per name is four. A greedy disjoint-clause packing has h >= ceil(m/10) >= ceil(2n/15). Branch on all three original names of each packed source clause, closing precisely one of eight local assignments by an authenticated original-clause EMPTY offset. Continue seven others, then branch on the remaining n-3h names and close each full falsifying assignment with an original-byte-offset EMPTY leaf.

On every UNSAT instance this produces a syntactically sound complete BRANCH/EMPTY proof with exactly

L = (7^h - 1)/6 + 7^h * 2^(n-3h) <= (7/6)*2^(alpha*n),

alpha = 1 + (2/15)log2(7/8) = 0.9743139896076806.

On SAT inputs a genuine satisfying witness survives, so never certify false UNSAT. This is a restricted **PROVED/EXACT upper construction**, not polynomial certificate coverage, a novel fast SAT algorithm, a resolution lower bound, or a new FLMV/van Melkebeek bridge. It is a modest quantitative strengthening of LSPV-3's pre-existing 2^n exhaustive authenticated proof. LSPV-1 PIN-BUDGET171's bounded-degree full-cube *length obstruction* is older and distinct. The residuals are ordinary CNF and cease to be exact-(2,2). **Source authentication requires physical immutable original byte offsets.**

## Reproduced finite checks

Original W1 UNSAT (15 variables, 20 clauses) and original G SAT (3 variables, four clauses) were run on four sources including products. Complete prefix-tree replay checks all original source-offset EMPTY claims, correct SAT leaves, signed occurrence quotas, source lengths, source reduction after two real packed clauses, leaf counts and explicit output bits. 529,210 assertions, zero failures. Exact W1 tree: 22,009 leaves, 44,017 nodes, 330,130 proof bits. W1 plus G: 154,064 leaves, 308,127 nodes, 2,619,082 proof bits. G/Gx2 produce SAT models, not false refutations. No finite result is an asymptotic proof by itself.

Original author-owned GitHub artifacts:

- research/agents/lspv-1/2026-10-26_2200_LSPV-1_ARC_PACKED_SOURCE_REFUTATION193.tex
- research/agents/lspv-1/2026-10-26_2200_ARC193_packed_clause_refutation_audit.py
- research/agents/lspv-1/2026-10-26_2200_ARC193_packed_clause_refutation_raw.json

## Model-native ledgers

M1 is a single shared read/write tape with N input bits counted in footprint and retained materialized proof output counted. Mk has one sequential read-only input head, fixed number of work tapes, visited work cells, actual head travel/reversals and output writes charged. RAT/FLMV uses indexed read-only input and charged writable/index bits. The naive compiler has polynomial(N)*L time and polynomial(N) peak work in each appropriately implemented model (one-way output excluded from reread storage). Do not transfer M1 or Mk crossing arguments to unrestricted indexed RAM. For conservative *decision-only* simulation the known upper transfer t_single <= t_multi + max(1,s_multi) is not a lower bound, and materialized output needs its separate footprint.

## Role-specific follow-ups

**LSPV-2 (:12):** audit per-record original-byte offset proof serialization, inverse source access, and output gate/wire counts without implicit storage.

**LSPV-3 (:24):** test affine/SCC/PATH terminal contractions against connected and disjoint signed exact-(2,2) hard controls; distinguish affordable witnesses from universally polynomial coverage.

**LSPV-4 (:36):** independent three-model time/space/head-move/output audit across genuine two hereditary levels and the SAT/UNSAT controls.

**LSPV-5 (:48):** formally referee m/(3Delta-2) greedy packing, exact 7^h2^(n-3h) leaves, immutable source-offset replay, and non-duplication claims. Preserve all OPEN arrows.

For LSPV-1 the immediate missing theorem remains all-ordinary-UNSAT affordable authenticated proof coverage or a noncircular arbitrary-K same-machine contraction. An exponent alpha<1 in **n** is still exponentially large in physical N. Short circuit witnesses and near-linear source access do not replace an all-input SAT decision circuit.

All five existing schedules and roles are unchanged. P != NP and ARC-EDGE-90 remain **OPEN**.

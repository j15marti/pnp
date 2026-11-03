# LSPV-2 LOCAL-TREE-TRANSFER368: five-role handoff

**November 3, 2026, 10:59 PST.** PNP SAT-Circuit Reduction Builder/LSPV-2, unchanged task, cadence and actual enabled status; unchanged fixed unit-cost, source-authenticated Rmix341. **PROVED/EXACT within audited paid-wire subgrammar, independent specialist review pending. COMPUTATIONAL finite local verification. P versus NP OPEN.**

## Published theorem and new transfer

Start with Buss and Turán (1988), Theorem 1, standard PHP(p,h) only one occupancy clause per pigeon and one binary collision clause for each pigeon pair per hole. For p>h, **every ordinary DAG Resolution refutation** has >= (1/2)(3/2)^(h²/(50p)) total lines, where source count m=p+h*binom(p,2). In balanced p=h+1, encoded bits N=Theta(h³ log h). This is restricted proof-system hardness, not unrestricted SAT runtime.

Adopt peer LSPV-2 INLINE-CONE-TRANSFER367 (blob ff7fa6df98d45ce62ba2a3f852cdbfcbe8ae59c7), which inlines paid deterministic conservative two-input VARDEF and compiles each remaining sound local inference on original-variable support U_j into canonical blocking-clause Resolution; its bound is W_Res(F)<=sum_j 2^(|U_j|+1). No global 2^b branching factor is needed.

**Refinement.** For each non-DEF inference j and each assignment v falsifying its inlined Boolean conclusion Q_j, let ell(j,v) be the **minimum leaf count** of a variable-query tree on as-yet-unassigned variables in U_j which terminates only when an authenticated canonical premise clause is already falsified. Decision-tree leaves weaken that premise blocker to the path blocker, interior nodes resolve queried variables; weakening erasure yields a strict Resolution proof. This proves, in the same audited paid-wire grammar,

```
W_Res(F) <= D(pi) = SUM_(j nonDEF) SUM_(v: Q_j(v)=0) [2*ell(j,v)-1]
                 <= SUM_(j nonDEF) 2^(|U_j|+1).
D(pi) >= 0.5*(3/2)^(h^2/(50p)) - m  on standard PHP(p,h).
```

Hence when p=h+1 and paid mixed q<=h^a, at least one inference has **exponentially large cumulative minimum local leaf mass** over falsifying output assignments. This is NOT an exponential lower bound on mixed q. A compact global XOR conclusion may have exponentially many canonical blockers yet a small legal paid inference. Never infer B1/B2/B3 or machine time from these trees. Explicit original-variable support and source authenticated formulas are required. If LOCAL-CONVERT permits uncharged named internal wires, the theorem does **not** yet apply.

## Independent producer and checker

Full Python producer and independently authored no-import Python verifier, exact local DP up to six original variables, 9 cases and 10 targets, 8 entailed and 2 false claims with SAT countermodels. Independent verifier 901 assertions, 4 corrupt certificate rejections, 4 malformed literal-list rejections. Full records, scripts and SHA-256 manifest in conversation ZIP. Local tree minima not claimed globally shortest Resolution or full mixed proof minima. Controls: 2SAT unit and binary implications, three-link chain (3 leaves versus 4), two equality/XOR clauses (2 each), parity eight forbidden assignments (8 leaves), redundant six-variable premise with an immediately falsified unit (1 leaf versus 32 exhaustive); both-label and malformed controls. Source-cost, proof bytes, optimizer time and checking/physical all-phase memory remain distinct; producer 1.18s/96,140KiB RSS, verifier 1.51s/96,392KiB RSS, not FLMV.

## Corpus and external assessments

Read 2026-11-02 12:04 master refocus, current issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-2 341/365/366/367, LSPV-1 reflection361, LSPV-3 bounded interface367, LSPV-5 Cook-Reckhow-B3 referee317 and payload firewall315. Existing blocking-clause/decision-tree simulation is prior work; novelty of generic technique NOT claimed. Increment is exact per-inference minimum tree profile replacing worst-case support expansion.

Located and independently assessed real Grok/Claude files: `GROKPROOF/2026-11-03_1518_PROGRESS.md`, blob `234fc189b01fa163eb10e128556e9d22e085b755`, leaves universal ARC charged transformation open; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, studies a restricted alternation-trading portfolio, not B3. Original Buss–Turán PDF (printed page 3) read and visually checked. github.com/openai search gave unrelated cohomological resolutions. No preflight checkout was available.

## Priority next arrows

**LSPV-1:** determine whether local tree mass has any independently justified bearing on one-family universal reflection; do not claim B3. **LSPV-3:** test compact high-support XOR with exponential leaf mass yet short correct evidence. **LSPV-4:** all-phase computation including DP policy search, parsing, source/index/head, checking, caches, live ancestors and output; retain s'<=max(rho,eta,lambda,lambda*s). **LSPV-5:** attempt to falsify semantics of gate inlining, weakened-leaf proof construction and named-internal-wire access. **LSPV-2:** apply tree extraction to actual authenticated mixed proof DAGs, then seek a sound bridge that remains valid under unrestricted rule mixing. Both superpolynomial Wbar_R and same-R B3 remain open.

## Exact new-file outbox

- `research/agents/lspv-2/2026-11-03_1059_LSPV-2_LOCAL_TREE_TRANSFER368.tex`
- `experiments/arc/lspv2_368_local_tree_public.py`
- `results/raw/arc/2026-11-03_1059_LSPV2_LOCAL_TREE_TRANSFER368_public.json`
- `research/coordination/2026-11-03_1059_LSPV2_LOCAL_TREE_TRANSFER368_FIVE_ROLE_HANDOFF.md`

The public dataset is a summary, not the full independently verified certificate dataset. The local ZIP contains all full code/raw. Root main.tex will only be reconciled after complete authenticated blob retrieval, within owned LSPV-2 markers, conflict-safe, preserving every external byte. No task mutations. P versus NP OPEN.

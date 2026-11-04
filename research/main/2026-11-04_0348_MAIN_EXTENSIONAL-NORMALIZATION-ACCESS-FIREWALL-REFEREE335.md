# EXTENSIONAL-NORMALIZATION-ACCESS-FIREWALL-REFEREE335

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 03:48 PST**

**Status:** PROVED/RESTRICTED polynomial node-to-bit normalization for the literal abstract `R_mix341` rules; PROVED/EXACT all-legal `Omega(M)` raw-payload access lower bound for any deterministic faithful extensional local normalizer; COMPUTATIONAL independent finite controls. The concrete machine-readable full-calculus parser remains unspecified. No superpolynomial mixed lower bound, B1/B2/B3 bridge, unrestricted SAT lower bound, or P-versus-NP conclusion is proved. The fixed calculus, five roles, task states and schedules are unchanged.

## Outcome

REFEREE334 left one precise question: does fixed `R_mix341` itself exclude a one-node hidden-payload defect? The literal abstract rule answer is **yes for certificate existence**, but **no for the work needed to compact an arbitrary supplied presentation**.

The authoritative text gives every derived node at most two antecedent-node identifiers, makes `LOCAL-CONVERT` derive one clause or one bounded-support circuit condition, and makes paid `DEF` the only rule that introduces a fresh reusable two-input gate variable. It contains no rule by which a later node cites a private `LOCAL-CONVERT` gate. Therefore internal circuit gates are representation-private under the declared abstract calculus; free public-wire export would be a new rule.

Consequently, every `q`-node abstract proof has a same-node-count polynomial-bit representative. But an explicitly supplied private-root circuit may still be arbitrarily long. The family below makes **every payload legal** and its canonical result two bits, while forcing an exact extensional normalizer to read every payload bit. Thus existential normalization does not itself provide a `poly(N+q)` physical transformer from arbitrary proof records.

## Published lower-bound anchor: exact scope

Let `P_h=PHP(h+1,h)` be the standard unary pigeonhole CNF with `h(h+1)` variables and

`m_h=(h+1)+h*binom(h+1,2)=Theta(h^3)` clauses.

Under an explicit signed binary-index/DIMACS-style encoding, `N_h=Theta(h^3 log(h+2))`. Haken's 1985 theorem has the form

`there exist c>0,h0 such that for every h>=h0 and every ordinary unrestricted shared-DAG Resolution refutation pi of P_h, |pi|>=2^(c h)`.

Source clauses are axioms; derived lines are ordinary resolvents; width, pivots and DAG sharing are unrestricted. This is not a lower bound for Extended Resolution, `Res(XOR)`, `R_mix341`, `LOCAL-CONVERT`, or arbitrary uniform SAT algorithms. Cook's polynomial Extended Resolution pigeonhole proofs are the mandatory compact-representation countercontrol. No published lower bound is regenerated here.

Primary sources: Armin Haken, *The intractability of resolution*, TCS 39 (1985), DOI 10.1016/0304-3975(85)90144-6; Stephen Cook and Robert Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702; Richard Ladner, *The Circuit Value Problem Is Log Space Complete for P*, SIGACT News 7(1) (1975), DOI 10.1145/990518.990519.

## Fixed calculus and literal-reference audit

The authoritative source is

`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

It fixes:

1. free authenticated CNF source clauses;
2. unit-paid, at-most-binary-premise `RES`, `AND3`, binary GF(2) `XOR`, unary `LOCAL-CONVERT`, and conservative two-input `DEF`;
3. a single `LOCAL-CONVERT` conclusion, checked by an explicit constant-support truth table; and
4. one fresh globally reusable variable per paid `DEF`, with later uses citing that charged node.

No rule exports or later addresses internal `LOCAL-CONVERT` gates. Therefore a public/internal-wire bundle is not a legal counterexample to this literal abstract grammar. The project still lacks one authoritative serialized full-system parser, so this conclusion is a mathematical-rule theorem rather than executable end-to-end syntax authentication.

## Theorem 1: polynomial node-to-bit normalization in the literal abstract grammar

For every valid source `F` of `N` encoded bits and every finite `q`-node `R_mix341` derivation under the literal abstract reference semantics, there is an extensionally equivalent derivation with the same source, dependency DAG and no more paid nodes whose complete certificate has `O((N+q+2)^3)` bits.

### Proof

- At most `N` source-variable names can occur in the explicitly written source, and at most `q` globally reusable fresh names exist because each needs a paid `DEF`. Alpha-rename paid fresh variables canonically.
- A clause or reduced affine row over that universe has polynomial length; node and parent identifiers use `O(log(q+2))` bits.
- `AND3` has at most three support names and an eight-bit table. `DEF` has one fixed two-input opcode.
- The explicit constant-support legality check for `LOCAL-CONVERT` means its one observable root denotes a Boolean function on fixed constant support. Replace any private internal circuit by its canonical truth table or a fixed canonical DNF/circuit. Because later rules cite the conclusion node, not private gates, root equivalence preserves every later inference.
- Summing these coarse record bounds over `q` nodes gives the cubic envelope.

This proves certificate **existence**, not a fast optimizer, parser, or compiler. LSPV-1/386 independently proves the stronger `K_a(N+q+2)^3` bound for a typed fragment with bounded public observations; that extra theorem remains conditional for any future public-port completion.

## Theorem 2: all-legal extensional normalization still costs `Omega(M)` reads

Let the already-derived authenticated local condition be `S(x)=x`. For a separately encoded payload `b=(b_1,...,b_k)`, let `t_b=AND_i b_i` and let the private-root circuit conclusion be

`C_b(x)=x OR NOT t_b`.

Every record is legal because `x => C_b(x)` for every `b`:

- if `b=1^k`, then `C_b=x`, with truth table `(0,1)`;
- if any payload bit is zero, then `C_b=1`, with truth table `(1,1)`.

Let `A` be a deterministic local normalizer required to output the exact extensional root condition. Run `A` on `1^k`. If it leaves position `i` unread, change only `b_i` to zero. The two executions are indistinguishable to `A`, but the required outputs differ. Therefore `A` must read all `k` payload bits on `1^k`.

The result is stronger than a legal-versus-illegal verifier test: both neighboring records are valid `LOCAL-CONVERT` consequences. The raw record can have `M=Theta(k)` sensitive bits while its canonical output uses two truth bits and its paid prefix remains two nodes (one local-factor construction and one conversion).

### Exact scope

This is a lower bound for a **faithful extensional local normalizer** or verifier of the supplied record. It is not a lower bound for a source-only proof generator, which may ignore an irrelevant supplied presentation and directly emit a canonical proof. It therefore separates proof existence from transformation work; it does not prove B1, B2, or B3.

## Fully charged ledger

| phase/object | logical-node cost | time/access | output/encoded length | peak writable space |
|---|---:|---:|---:|---:|
| supplied `C_b` record | 1 `LOCAL-CONVERT` node | `Omega(M)` exact extensional inspection on `1^k` | `Theta(M)` | syntax-dependent |
| streaming canonicalizer | unchanged | `Theta(M)` | `O(1)` for this family | `O(log M)` counters plus constant accumulator |
| eager materialization | unchanged | `Theta(M)` | `O(1)` normalized output | `Theta(M)` available upper bound, not a lower bound |
| direct canonical generator | unchanged | source/generator work charged | `O(1)` local record | generator-dependent |
| exponential explicit intermediate | node-model dependent | at least its output/access volume | exponential if materialized | may be streamed/recomputed |
| lazy descriptor | descriptor nodes only | generator construction, every bit query, recomputation and validation charged | compact descriptor | schedule-dependent |

Thus an exponential raw presentation incurs exponential work if actually read or emitted, while a compact equivalent is allowed and must be checked. Streaming prevents an unjustified linear-space conclusion. Full-state XOR remains an offline diagnostic unless its computation is charged.

## Four falsifiers

1. **The literal `R_mix341` grammar permits free public export of every `LOCAL-CONVERT` internal wire. — FALSE as a reading of the declared rules.** Only node conclusions are antecedents; global reusable gates require paid `DEF`.
2. **A polynomial-bit representative makes every supplied proof polynomial-time normalizable in `N+q`. — FALSE.** The all-legal family has fixed `N,q`, arbitrarily large `M`, and exact normalization needs `Omega(M)` reads.
3. **The access lower bound forces `Omega(M)` writable space. — FALSE.** A one-pass normalizer uses logarithmic counters and a constant Boolean accumulator.
4. **Node-to-bit normalization supplies the arbitrary-algorithm bridge. — FALSE AS AN INFERENCE.** It bounds certificate presentation after a proof is known; it gives neither a trace-to-proof compiler nor `q=poly(N)`.

## B1/B2/B3 classification

| obligation | unchanged `R_mix341` status | effect of this run |
|---|---|---|
| B1: every correct decider is pointwise dominated | OPEN | no trace compiler supplied |
| B2: worst-case domination for every correct decider | OPEN | no worst-case compiler supplied |
| B3: `SAT in P` implies polynomial `Wbar` for this fixed R | OPEN | normalization does not bound `q` |

The exact next transfer is still: under hypothetical `SAT in P`, compile the rejecting computation of one fixed polynomial-time correct all-input decider into this same `R_mix341` with polynomial node cost. That is B3, not a consequence of certificate compactness.

## Finite controls

The Python producer exhaustively evaluated all `2^k` payloads for every `1<=k<=12` (8,190 records), checked that every record is legal under `S=x`, checked all 78 single-bit neighbors of the all-ones inputs, and separately checked one SAT source, one UNSAT source and nine malformed-source rejections. It made **16,685 assertions**.

An independently written Node verifier replayed the sensitivity adversary, legality, output quotient, streaming counter bound and bridge classifications with **272 assertions**.

Artifacts:

- `experiments/arc/lspv5_335/all_legal_normalization_access_referee335.py`
- `experiments/arc/lspv5_335/verify_all_legal_normalization_access_referee335.js`
- `results/raw/arc/lspv5_335/all_legal_normalization_access_referee335.json`

Finite controls do not reproduce Haken's asymptotic theorem and do not certify unrestricted `R_mix341` hardness.

## Five-role, project, Grok, Claude and GitHub review

Issue #3 was read through 767 comments before publication. The five role audits agreed on the literal private-root conclusion and independently separated certificate existence from physical normalization work.

Current peers:

- LSPV-1/386: `research/agents/lspv-1/2026-11-04_0256_LSPV-1_BOUNDED_OBSERVATION_BIT_NORMALIZATION386.md`, blob `82f85a2d66841929970b261a360156be0306ac90`. It proves bounded-observation normalization under an explicit typed interface; no B bridge.
- LSPV-2/386: `research/agents/lspv-2/2026-11-04_0312_LSPV-2_UNIFORM_STRICT_AND2_ER386.md`, blob `37dae975a6e9823242c0a1fa130c10faed21921d`. It gives a uniform polynomial paid-AND2/Resolution compiler for guarded cubic odd Tseitin, defeating transfer from ordinary Resolution to full mixed rules.
- LSPV-3/391: `research/agents/lspv-3/2026-11-04_0324_LSPV-3_INTERFACE_QUOTIENT_COST_GAP391.tex`, blob `816c47326a863d5557a6dd912f4bcf5ff5e787e8`. Identical one-bit interface semantics and signed degree data can coexist with exact mixed costs `h+1` and `1`.
- LSPV-4/383: `research/agents/lspv-4/2026-11-04_0340_LSPV-4_EXACT_OR_CUT_ACQUISITION383.tex`, blob `4c2f782b9533dcb98c0f6b100a18ad2da0547c12`. Width-one exact output can still force all explicit source bits read; lazy pointers shift access costs.

Current Grok was located at `GROKPROOF/2026-11-04_0213_PROGRESS.md`, blob `8e7d18760c7371f43ea897a09f61843f89c0f16f`; it explicitly leaves the universal fully charged arbitrary-`A` transformation open. The older `GROKPROOF/2026-11-04_1217_PROGRESS.md`, blob `cae0560d2e4f8c243da802c1d5d48ebf32bedd5c`, is likewise restricted.

Claude has no post-October-28 assessment. The relevant exact reports remain DIRECTPRODUCT `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`; TPORT `...1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`; and ONETAPE `...1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`. They cover restricted portfolios or access models and provide no node normalization plus B3 bridge.

Project GitHub search found LSPV-3/367 and LSPV-1/376 as prior opaque-root and legal/illegal payload controls. The new point is the exact **all-legal** extensional normalization lower bound combined with literal-grammar certificate normalization. Searches in `github.com/openai` and `openai/openai-cookbook` for Cook--Reckhow/proof-normalization implementations returned no applicable result; absence is not novelty evidence.

## Exact next gap

Freeze and implement one authoritative full-system proof parser matching the literal node-reference semantics, then mechanically prove the cubic certificate bound. Scientifically, the load-bearing gap is unchanged: derive B3 by a polynomial node-cost compiler from a hypothetical polynomial-time correct all-input SAT decider into the same fixed system, or find a valid counterexample. P versus NP remains OPEN.

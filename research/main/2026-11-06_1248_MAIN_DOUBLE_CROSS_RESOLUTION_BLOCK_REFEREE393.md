# LSPV-5/REFEREE393: two first cross-cut resolvents cannot legally recontract to AND3 at the 35-node floor

**November 6, 2026, 12:48 PST | Route B independent red team | COMPUTATIONAL exact finite result | P versus NP OPEN.**

This report preserves the historical $R_{\mathrm{mix341}}$ grammar, source authentication, and unit weights. It adds no split, discharge, weakening, clause export, or semantic oracle. The finite advance refines REFEREE392: although pairs of first cross-cut resolvents can semantically resolve to support at most three, every such pair necessarily reuses original sources on both sides of the cut and is therefore illegal in the authenticated 35-node source-once tree.

The global interval remains

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

## 1. Claim card and IDEA -> SEARCH -> ITERATE

**Claim ID:** LSPV-5/REFEREE393 double-first-cross Resolution block.

**Exact quantifiers:** for every two support-four clauses $C_1,C_2$ that are each obtained by one lowest cross-cut strict Resolution between arbitrary source-once side-local clause outcomes, if $\operatorname{Res}(C_1,C_2)$ is strict and has support at most three, then every realization of $C_1,C_2$ reuses at least one left source and at least one right source. Hence $C_1,C_2$ cannot be sibling subtrees in the 35-node source-once proof tree.

**Model:** the authenticated 36-source bridge MUS; 35 paid binary nodes; full binary source-once tree; historical strict Resolution and support-at-most-three AND3. At this floor, clause outputs arise only from Resolution.

**SAME_REALIZATION:** the same original source indices, left/right cut, original-variable coordinates, strict pivots, and child subtrees used in the proposed 35-node derivation.

**Initial falsifiers:**

1. a legal pair producing support at most three;
2. such a pair with disjoint source ancestry on both halves;
3. a peer or accepted historical trace realizing the route;
4. a historical rule contracting the pair without the counted strict Resolution.

Falsifier 1 occurs semantically: 13,120 unordered clause pairs give support at most three. Falsifier 2 does not occur: none is source-disjoint, and all 13,120 pairs overlap separately on both halves. Falsifiers 3 and 4 were not found. The initial semantic-only hypothesis was therefore repaired to the exact source-authenticated theorem below.

## 2. Source, grammar, and prior dependencies

The fixed source is REFEREE386's 15-variable, 40-clause proper strict-3-CNF bridged cubic odd-Tseitin instance, DIMACS SHA-256 `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`. Its unique essential 36-clause MUS is indexed `0..15,17,18,20..36,39`. The two 18-source halves share only $x_{15}$.

The historical grammar source remains `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

Dependencies retained at their verified scope:

- REFEREE386: every 35-node proof is a full binary tree using all 36 sources exactly once.
- REFEREE389: the pure-Resolution 35-node class is impossible.
- REFEREE390: every remaining 35-node proof contains a cross-cut AND3-produced factor/equation.
- REFEREE391: its lowest cross-cut ancestor is strict Resolution and every first cross resolvent has support at least four.
- REFEREE392: one further Resolution with any side-local sibling cannot reach support at most three.

No unary LOCAL, paid DEF, reconvergence, or source duplication fits at the 35-node floor. AND3 and XOR do not produce clauses consumed by strict Resolution. Thus the present clause-interface test is complete for the stated double-first-cross shape, but it is not a global closure of every longer mixed tree.

## 3. Exact finite enumeration

For each side and every nonempty subset of its 18 authentic sources, the producer enumerates every source-once strict-Resolution clause outcome. For each globally keyed clause it retains the inclusion-minimal antichain of source masks. This loses no potential disjoint witness: if two nonminimal realization masks were disjoint, contained minimal masks would also be disjoint.

Both implementations reproduce:

| Quantity | Exact value |
|---|---:|
| Unique side-local clauses | 3,234 per side |
| Subset-clause occurrences | 11,705,410 per side |
| Side strict-Resolution pair tests | 1,126,097,195 per side |
| Legal first cross-cut resolvents | 4,056,196 |
| Support-four first cross resolvents | 6,724 |
| Unordered support-four pair tests | 22,602,726 |
| Strict double-cross Resolution pairs | 8,592,320 |
| Semantic outputs of support at most three | 13,120 pairs; 2,296 distinct clauses |
| Pairs with some left-disjoint realization | 0 |
| Pairs with some right-disjoint realization | 0 |
| Pairs disjoint on both halves | 0 |
| Minimum total reused source count | 3 |

Only support-four first resolvents need testing. For a strict Resolution, every nonpivot literal of either parent survives. If either parent has support greater than four, the output has support at least four. Thus the complete candidate set has

$$
\binom{6724}{2}=22{,}602{,}726
$$

unordered pairs.

The semantic-only check is deliberately not treated as a proof of legality. It finds 13,120 attractive shortcuts, but exact ancestry masks show that every one reuses sources on the left and on the right. The least possible total overlap is three original source clauses.

## 4. Theorem and proof

### Theorem 393.1 (COMPUTATIONAL exact finite theorem)

Let

$$
C_i=\operatorname{Res}(L_i,R_i),\qquad i\in\{1,2\},
$$

where each $L_i$ is any source-once left-local strict-Resolution outcome and each $R_i$ is any source-once right-local strict-Resolution outcome. Suppose $C_1,C_2$ have support four and $E=\operatorname{Res}(C_1,C_2)$ is strict with support at most three. Then the left ancestries of $C_1,C_2$ intersect and the right ancestries intersect. More strongly, across the two halves at least three original source indices are reused.

Therefore $C_1$ and $C_2$ cannot be siblings in a legal 35-node full binary source-once refutation tree.

### Proof

The side dynamic programs close every source subset under strict binary Resolution and retain every resulting clause. For each clause they retain all inclusion-minimal source masks. REFEREE391 proves that every first cross-cut resolvent has support at least four. A strict Resolution with output support at most three can therefore use only two support-four first resolvents.

The primary implementation constructs all 6,724 such resolvents with their exact left and right mask antichains and tests all 22,602,726 unordered pairs. Of 8,592,320 strict pairs, 13,120 yield support at most three. For every one, the minimum left-mask intersection is nonempty and the minimum right-mask intersection is nonempty; the minimum sum of the two intersection sizes is three. Hence no pair has disjoint sibling ancestry.

An independently written implementation reconstructs the 40-clause source from graph incidence, encodes local clauses in base three, constructs a separate 43,046,721-entry Resolution table, recomputes every subset closure and mask antichain, and reproduces every count and the zero. $\square$

### Corollary 393.2 (surviving immediate-sibling shape)

For the next strict Resolution after the lowest cross-cut resolvent in a putative 35-node proof:

1. its sibling cannot be side-local, by REFEREE392; and
2. its sibling cannot itself be a first cross-cut resolvent, by Theorem 393.1.

Thus if that sibling crosses the cut, its root must already contain at least one post-cross strict Resolution. Longer cross-cut sibling subtrees and paths with two or more further Resolution nodes remain open.

## 5. Branching/shared-DAG interpretation

At 35 nodes the paid dependency graph is a full binary tree. Every inference is an AND obligation over both premises, and sibling source ancestries must be disjoint. Alternative pivots, source partitions, and proof shapes are OR alternatives granted free after-the-fact optimization.

The 13,120 semantic shortcuts are a useful adversarial control: accepting any of them while ignoring ancestry would leak a source across incompatible sibling obligations. No distinct inference is double-counted, no branch assumption is introduced, and no discovery cost is charged to the ideal minimum. At 36 nodes reconvergence or a unary node can occur and must be analyzed separately.

## 6. Established-family, theorem, encoding, and shortcut ledger

| Family | Exact encoding and size | Established lower bound/model | Known legal shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Braun bit-PHP | $n=2^\ell$ holes, $n+1$ pigeons; pair lines are disjunctions of bit disequalities | Braun arXiv:2609.23015v2: every unrestricted shared-DAG Res($\oplus$) refutation has more than $\exp(n/(32768\ell^2))$ lines for $\ell\ge32$ | Cook-style paid extension gates; LSPV-1/454 quantifies exponential backtranslation output to the original Res($\oplus$) source | Historical DEF/LOCAL/export typing and a polynomial lower-bound-preserving strict-3 transfer remain OPEN |
| Pang random proper strict 3-CNF | $F\sim\mathcal F(n,3,8n)$ sampled from the $8\binom n3$ proper signed triples | Pang arXiv:2610.00837v2: restricted exponential shared-DAG Res(PC$_r/\mathbb F_p$) bounds under stated PC-degree hypotheses | Full mixed DEF, LOCAL, sharing, learned lemmas, and branching remain legal | LSPV-3/457 proves only $q\ge\mu(F)-1$ and span $\ge\lceil\log_2\mu(F)\rceil$ in its source-explicit binary-premise semantic model; this is linear/logarithmic, not superpolynomial mixed hardness |
| Haken unary PHP | Standard pigeon clauses and collision clauses | Haken 1985: exponential ordinary shared-DAG Resolution | Cook 1976 polynomial Extended Resolution proof | Equisatisfiable strict-3 conversion alone is insufficient |
| Cubic odd Tseitin | Four proper width-three clauses per degree-three parity vertex | Exponential ordinary Resolution on suitable expanders | Historical AND3/XOR proof has $4h-1$ paid nodes | Established family failure for full mixed hardness |
| Authenticated bridge control | 15 variables, 40 strict 3-clauses; unique 36-clause MUS | Certified finite UNSAT and bounded exact proof analysis only | Known 37-node proof: 28 AND3, 6 XOR, 2 LOCAL, 1 RES | Complex cross-cut siblings, longer chains, and all 36-node classes remain OPEN |

Certified UNSAT, certified restricted proof-size hardness, and empirical solver difficulty remain distinct. No listed theorem is described as an arbitrary-algorithm SAT lower bound.

## 7. Search, repository, and peer audit

The governing November 2 handoff, current issue #3 through the REFEREE392 update, root instructions, research protocol, original /341 grammar, REFEREE386--392, LSPV-1/454, current LSPV-3/457, Route-A peers, actual `GROKPROOF/2026-11-06_1617_PROGRESS.md`, and Claude `2026-10-28_1326_CLAUDE_TPORT-0001.tex` were reviewed. LSPV-3/457's source-core theorem is a useful generalized work/span control but does not yield the desired superpolynomial $\overline W_R$.

At search time the project head was `95bc684e1339323aef83744e61d2dd0cbb94ed6c`. Required external heads were unchanged: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, FRAT-XOR `18cd6bc1...`, short-proof `2c524cfc...`, drat-trim `2e3b2dc...`, CNFgen `24e633bd...`, openai/math `4eaee875...`, and anthropics/formal-math `16a5ce41...`. Actual files reread included konard's proof-status manifest and complexity model, blkph0x's method index and external-status audit, FRAT-XOR's format, and short-proof's README. None authenticates the historical /341 byte checker or proves the missing B3 implication.

Primary indexed literature search rechecked Braun arXiv:2609.23015v2, Pang arXiv:2610.00837v2, Haken 1985, Cook 1976, and read-once Resolution recognition. A direct Google-branded interface was unavailable. The local scratch checkout lacks root `main.tex`, AGENTS, CODEX, and the research skill; complete current versions were read through GitHub, and safe root reconciliation is performed only from complete remote bytes. No authoritative historical accepted-byte checker was located or executed.

## 8. Resource and hostile-control ledger

| Phase | Charged result |
|---|---|
| Primary logical work | 2,252,194,390 side pair tests; 4,056,196 cross pairs; 22,602,726 double-cross pair tests |
| Primary final run | 33.712 s internal / 33.80 s shell wall; 789,800 KiB peak RSS |
| Independent final run | 42.842 s internal / 42.85 s shell wall; 491,120 KiB peak RSS |
| Explicit evidence | Two C++ sources, primary and verification JSON, manifest, report, handoff, root fragment, issue outbox |
| Hostile controls | Fifteen independently coded count, support, overlap, and result mutations rejected |
| Failed/preliminary policies | One shell timing command failed before execution because `/usr/bin/time` was absent; preliminary producer/verifier runs of 39.785 s, 43.130 s, and 46.165 s were charged while overlap fields and warning cleanup were added |
| Parsing/search/publication | Current heads, issue, reports, repository files, primary indexed literature, writes, and readback charged as performed; remote service peak memory is not exposed |
| Simultaneous measured peak | 789,800 KiB; caches and remote publication memory unmeasured |

The materialized subset closures and mask antichains are implementation costs, not proof-space lower bounds. The ideal $W_R$ continues to grant free selection of the best legal derivation. No FLMV same-machine time/space consequence follows.

## 9. B3 verdict and remaining gap

This finite obstruction is neither a superpolynomial mixed-family lower bound nor a compiler from an arbitrary polynomial SAT decider into this same calculus. It supplies no arbitrary-decider correctness/reflection theorem. B1, B2, B3, superpolynomial $\overline W_{R_{\mathrm{mix341}}}$, and P versus NP remain **OPEN**.

**Actual advance:** all 13,120 semantic double-first-cross shortcuts are illegal under exact source authentication; every one reuses sources on each half, with at least three reused source indices in total.

**Precise finite gap:** enumerate or structurally exclude a cross-cut sibling whose root already contains a post-cross Resolution, and longer paths containing at least two further strict Resolution nodes before AND3. Then analyze the three 36-node topology classes.

**Precise asymptotic gap:** prove a polynomial lower-bound-preserving original-source transfer from an established hard 3-CNF family through every historical native shortcut, or find a legal counterexample, and separately prove a noncircular same-system B3 implication.

## Artifacts

- `experiments/review/lspv5_393_double_cross_resolution.cpp`
- `experiments/review/lspv5_393_independent_verify.cpp`
- `results/raw/review/2026-11-06_1248_LSPV5_DOUBLE_CROSS393.json`
- `results/raw/review/2026-11-06_1248_LSPV5_DOUBLE_CROSS393_verification.json`
- `results/raw/review/2026-11-06_1248_LSPV5_DOUBLE_CROSS393_manifest.json`
- `research/coordination/2026-11-06_1248_LSPV5_DOUBLE_CROSS393_HANDOFF.md`

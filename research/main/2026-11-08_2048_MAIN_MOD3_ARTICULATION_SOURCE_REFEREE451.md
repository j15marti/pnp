# LSPV-5 independent red-team report 451: mod-3 articulation source essentiality

**Pacific time:** 2026-11-08 20:48 PST  
**Role / route:** LSPV-5 Independent Proof Red Team / Route B  
**Status:** PROVED/RESTRICTED source-semantics theorem plus COMPUTATIONAL exact finite control. Historical `R_mix341` accepted grammar, all-rule superpolynomial minimum, noncircular B3, and P versus NP remain OPEN.

## Result first

The 2-connected hypothesis in `[P2-L1-523]` is quantitatively necessary. For a connected simple cubic graph $G$ and vertex $v$, let $c_v$ be the number of connected components of $G-v$. In the original signed proper strict-3 mod-3 Tseitin source with nonzero total charge, exactly

$$3^{3-c_v}$$

of the 18 forbidden triples at $v$ are individually indispensable. The nine-per-vertex count of `[P2-L1-523]` is the special case $c_v=1$.

On the explicit 16-vertex, 24-edge three-arm cubic control, the distribution of $c_v$ is one vertex with $c_v=3$, three with $c_v=2$, and twelve with $c_v=1$. Hence the exact forbidden-facet count is

$$1+3\cdot3+12\cdot9=118,$$

not $16\cdot9=144$. All 24 edge ALO sources are independently indispensable, so this source has exactly 142 individually indispensable original clauses; mechanically applying the 2-connected formula would overcount by 26. The pair-defect theorem `[P2-L3-521]` survives articulation: all 120 vertex pairs for each nonzero total charge have an explicit flow falsifying exactly one $R_u$ and one $R_v$ source.

This is linear source-ancestry evidence only. It is neither a superpolynomial proof lower bound nor a historical `R_mix341` checker execution.

## IDEA

Initial hypothesis: assuming a uniform polynomial SAT decider, compile its rejecting computation tableau into paid `R_mix341` definitions and Resolution, thereby obtaining B3 for the same fixed calculus.

Falsifiers registered before search:

1. the compiler needs an unproved reflection/correctness axiom for the decider;
2. computation-tableau clauses or facets cannot be authenticated to the original source under the historical grammar;
3. `SAT in P` supplies a polynomially bounded proof system but transfer to this fixed system still requires a p-simulation/optimality theorem;
4. the historical grammar lacks finite native records for a required tableau operation.

## SEARCH

The initial B3 proposal was not advanced. Cook--Reckhow's definition and Proposition 1.6 make the missing direction explicit: a target proof system inherits polynomial boundedness from another only when it p-simulates it. The project already contains stronger adversarial controls: LSPV-5/331 constructs a fixed padded proof-system obstruction, LSPV-1/462 supplies the exact clock/padding control, and LSPV-5/445 records the same p-simulation direction. Falsifiers 1 and 3 therefore fire. No same-`R_mix341` p-simulation or noncircular B3 bridge was found.

Queries/change-aware review included: `Cook Reckhow polynomially bounded proof systems p-simulation Proposition 1.6`, `p-optimal proof systems reflection principles`, `mod 3 Tseitin articulation source essentiality`, and repository searches for `p-optimal`, `reflection`, `3^(3-c)`, `articulation`, and `proof status`.

### Project and peer reads

- `proof1.txt`, complete prepublication blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.
- `proof2.txt`, complete prepublication blob `9b2775decaa27a89bd94345fee0c2816cc99913b`; exact affected IDs are `[P2-L1-523]`, `[P2-L3-521]`, `[P2-L3-510]`, `[P2-F6]`, `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]`.
- Governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current blob `c3889a3...`; required historical commit remains `4e29ed7646f484707767acb6e63ec5f38afd98a8`.
- Issue #3 read through comment `6732429353` (LSPV-3/521).
- LSPV-1/523 report blob `6b59bc1259bab9f6c26cb123290c05e0769f214d`; exact independent JS blob `13de985fbb2e0ad83ea7729089826924e1dc82db` reran successfully: both nonzero K4 charges have 42 essential clauses.
- LSPV-3/521 report blob `05f972d483782aee97eaf48057474f5c8ad93051`; exact compact JS blob `0a59f16e35d97f50a885071e2d55c5ea0461e5cb` reran successfully: 428 pair witnesses.
- Current Grok artifact `GROKPROOF/main.tex`, blob `b5c5a6bd74c8d56f4319a394231938813132be71`, read after directory inventory. An initially guessed timestamped path returned 404 and was not treated as reviewed.
- Current relevant Claude artifact `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4...`; no newer relevant Claude artifact was found in the actual directory listing.
- `AGENTS.md` blob `19656af...`, `CODEX.md` blob `754999...`, `.codex/skills/pnp-research/SKILL.md` blob `b8df83...`, `.codex/skills/pnp-research/modes.md` blob `c211e9...`, and protocol blob `25b38d...` were read.

### Required external corpus pins

| Source | Pin / path reviewed | Result at this scope |
|---|---|---|
| `konard/p-vs-np` | commit `ecedd2b45...`; proof-status blob `93b77...` | unchanged; no fixed-`R_mix341` B3 or articulation theorem |
| `blkph0x/p-vs-np-proof-research` | commit `7dedc73...`; `METHOD_INDEX` blob `18d693...` | unchanged; hypothesis index only, no transfer theorem |
| `meelgroup/frat-xor` | commit `18cd6b...`; format blob `986a21...` | proof-format/checker control, not a lower-bound transfer |
| `peitl/short-proof` | commit `2c524c...`; README blob `93d209...` | minimum-proof tooling control, not same-calculus B3 |
| `tanyongkiam/cake_lpr` | commit `033aad...`; README blob `e94f45...` | verified-checker boundary/control; final-release supersession noted |
| `uds-psl/cook-levin` | commit `e24a92...`; README blob `7edfec...` | reduction/formalization control; no target p-simulation |
| `openai/math` | commit `4eaee...`; README blob `cc5b0...` | formal-math repository checked; no same-calculus bridge used |
| `anthropics/formal-math` | commit `16a5ce...`; `eth/README` blob `0b3dc...` | trust-boundary control; challenge `sorry` statements are not this theorem |
| `cslib-community/complexitylib` | head query returned no commit | access limitation recorded; no claim of review |

Indexed web search was available; no separate Google-branded search interface was available. Absence of a search hit is not evidence of novelty.

Primary sources consulted: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979), especially Definition 1.1 and Propositions 1.4/1.6; Krajicek and Pudlak on optimal proof systems; Pudlak on reflection principles. These sources support the p-simulation/reflection obstruction, not historical B3.

## ITERATE

### Exact source encoding

Fix an orientation of a connected simple cubic graph $G=(V,E)$, charges $b\in\mathbb F_3^V$, and nonzero total charge $\sigma=\sum_v b_v$. For every edge $e$ use original one-hot indicators $x_{e,0},x_{e,1},x_{e,2}$ and the original ALO clause

$$x_{e,0}\vee x_{e,1}\vee x_{e,2}.$$

At vertex $v$ with signed incident edges $(e_i,s_i)$, include for every $(a_1,a_2,a_3)\in\mathbb F_3^3$ whose signed sum differs from $b_v$ the original strict-3 forbidden clause

$$\neg x_{e_1,a_1}\vee\neg x_{e_2,a_2}\vee\neg x_{e_3,a_3}.$$

Thus for $h=|V|$ and $m=3h/2$, there are $3m=9h/2$ indicator variables and $m+18h=39h/2$ original clauses. With binary IDs the encoding length is $N=\Theta(h\log h)$.

### Theorem 451.1: exact articulation correction

**Claim.** For each vertex $v$, exactly $3^{3-c_v}$ forbidden clauses are individually indispensable; their triples have signed sum $b_v-\sigma$. Every other forbidden clause is individually redundant.

**Proof.** Delete one forbidden clause at $v$ and fix its incident triple $t$. All other original clauses force exact one-hot values on every edge and enforce every divergence equation except possibly the one at $v$. For each component $C$ of $G-v$, summing its vertex equations cancels internal edges and gives one nonzero linear constraint on precisely the boundary-edge values from $C$ to $v$. The $c_v$ constraints use disjoint, nonempty subsets of the three incident values, hence have rank $c_v$. Exactly $3^{3-c_v}$ incident triples extend to flows satisfying all equations away from $v$. Summing those equations globally forces their signed sum at $v$ to be $b_v-\sigma$. Conversely every such triple extends, by the standard incidence-image characterization on each connected component. Therefore exactly those clauses have singleton-deletion models. $\square$

The proof does not invoke a checker, discovery cost, or any new inference rule.

### Theorem 451.2: pair defects ignore articulation

For distinct $u,v$, change the desired divergence vector to

$$b+\sigma(e_u+e_v).$$

Its coordinate sum is $\sigma+2\sigma=0$ in $\mathbb F_3$. The image of an oriented incidence matrix of a connected graph is the zero-sum subspace, so a flow exists. Its one-hot assignment falsifies exactly one original wrong-class source in $R_u$ and one in $R_v$. With only one wrong group removed the total divergence remains nonzero, so no such model exists. This proves the pair-group deletion statement for every connected graph, including the articulation control.

### Finite exact audit

The producer built the explicit 16-vertex graph, all 312 original clauses for each $\sigma\in\{1,2\}$, and explicit singleton-deletion and pair-defect witnesses. It performed 163,520 clause checks and emitted 524 logical witnesses in 0.242 s with 11,008 KiB recorded maximum RSS. Results per charge:

- 118 forbidden singleton-deletion witnesses with per-vertex counts $1,3,3,3,9,\ldots,9$ according to $c_v$;
- 24 ALO singleton-deletion witnesses;
- 120 pair-defect witnesses;
- all 16 single wrong-group targets rejected.

An independently written Node verifier reconstructed the graph and all clauses, checked every witness and count in 2,371 assertions, and ran five hostile in-memory mutations: duplicate source ID, corrupt forbidden owner, wrong pair scope, non-ternary/multihot value, and mismatched missing edge. All were rejected. Producer SHA-256 `b5cfd383...`, verifier `d25b7fbc...`, raw `6a5326e0...`.

### Family / theorem / encoding / known-method / remaining-transfer ledger

| Item | Exact statement |
|---|---|
| Family | Original signed proper strict-3 mod-3 Tseitin source above; selected finite articulation control has $h=16,m=24$, 72 indicators, 312 clauses |
| Established restricted theorem | Pang, arXiv:2610.00837v2, Theorem 7.2(b), gives exponential all-shared-DAG lower bounds only in fixed syntactic $\operatorname{Res}(PC_r/\mathbb F_2)$, fixed $r$, for the stated expander strict-3 Tseitin regime; it is not a theorem about this articulation graph or full `R_mix341` |
| This run | Exact original-source singleton-deletion classification and pair-group witnesses; linear ancestry consequences only under separately stated source-authenticated bounded-arity rules |
| Known methods/shortcuts retained | spanning-tree/Gaussian flow construction; Resolution/CDCL branching; shared DAGs; Cook ER/extension variables; algebraic/Tseitin shortcuts; `ER2` and compact affine reasoning remain adverse upper-bound controls |
| Remaining transfer | authenticate historical native bytes and exact facets; prove conservative source ancestry through every legal mixed rule; cover high-arity/compact algebra/extension shortcuts; then prove a superpolynomial invariant and noncircular same-system B3 |

Certified UNSAT, certified proof-size hardness, and empirical difficulty are distinct here: the finite instances are certified UNSAT and have explicit deletion witnesses; no proof-size hardness for the historical mixed calculus is certified, and solver runtime is not used as evidence.

## Branching/shared-DAG accounting

The result is compatible with free after-the-fact minimization over valid proof DAGs. Source leaves are counted once; shared subproofs are not duplicated. Pair-defect witnesses are adversarial source-subset models, not extra case-split rules. No branch-local conclusion is reused outside its assumptions, no AND obligation is omitted, and no case-split/discharge/weakening rule is added to `R_mix341`.

For an at-most-binary, unit-paid, sound source-authenticated DAG, $r$ indispensable leaves in contradiction ancestry imply at least $r-1$ paid internal nodes. This remains a restricted combinatorial corollary, not a statement about unspecified historical high-arity mixed rules. Work, span, and realizable time/space are not conflated.

## Resource and trust ledger

- Logical nodes/witnesses: 524 generated; independent verifier 2,371 assertions.
- Explicit evidence: 276,188-byte JSON before publication; exact assignments retained.
- Construction/search: 0.242 s producer; failed B3 idea and prior-art duplicate controls recorded.
- Peak producer space: 11,008 KiB `ru_maxrss`; parser/source arrays and witness output coexist at peak.
- Parsing/source/index/head reads: complete proof trackers and required governance files read; GitHub blobs pinned above.
- Verification: independent language and implementation; exact peer executables rerun; neither is called an authoritative historical checker.
- Output/cache/retrieval: raw JSON, report, producer, verifier, handoff, delta, fallback, and publication receipt are separately charged artifacts.
- External trust: repository claims, badges, builds, and formalization labels were not promoted beyond inspected theorem scope.

## Tracker and publication disposition

Material change: add `[P2-L5-451]` to `proof2.txt`, refining `[P2-L1-523]`, `[P2-L3-521]`, `[P2-L3-510]`, and `[P2-F6]`. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]` stay OPEN. `proof1.txt` has no material Route-A change.

Root `main.tex` metadata reported blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba`, but the connector returned zero content bytes. Therefore no manuscript edit was attempted; a role-owned insertion fallback is published instead. This is an exact read blocker, not a claimed successful manuscript update.

**Actual advance:** the exact articulation correction $3^{3-c_v}$ falsifies an unsafe nine-per-vertex generalization and shows that pair-defect coverage, unlike individual essentiality, survives articulation.  
**Precise remaining gap:** no authenticated rule-by-rule argument transfers even this strengthened linear source obstruction through all historical `R_mix341` rules, and no noncircular same-calculus B3 bridge is known.  
**P versus NP remains OPEN.**

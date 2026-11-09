# LSPV-5/457 | Pure-affine auxiliary projection barrier and nonlinear shortcut control

**2026-11-09 02:53 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Node accounting:** new evidence `[P2-L5-457]` strictly extends the original-coordinate affine-hull result `[P2-L1-530]` to arbitrary fresh auxiliaries **only when the entire candidate relation remains affine over $\mathbb F_2$**. It refines the missing mixed-transfer gap `[P2-C3]` and grammar qualification `[P2-D1]`; `[P2-B1]` superpolynomial minimum work and `[P2-B2]` noncircular B3 remain **OPEN**. `[P1-01]`, `[P1-03]`, `[P1-04]`, `[P2-A2]`, `[P2-A4]`, and `[P2-A5]` are unchanged.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** For an odd-modulus one-hot boundary fiber $S$ with at least three groups, adding any number of fresh Boolean variables and any shared system of linear GF(2) equations cannot exclude a wrong-charge one-hot boundary tuple if every valid boundary tuple has some auxiliary witness.

**Precise falsifiers fixed before search:** (F1) existential projection of a finite affine GF(2) solution set is non-affine; (F2) the source-authenticated valid tuples in `[P2-L1-530]` do not all have the assumed auxiliary lifts; (F3) there exists an affine extension relation containing a lift of every valid tuple but excluding some wrong-charge one-hot tuple; (F4) `[P2-L1-530]` has different boundary/quantifier hypotheses from those used here.

**Search changed the claim.** F1--F4 did not fire, but the current LSPV-3/530 artifact provides the decisive hostile control: a linear-size **nonlinear Boolean** three-state modular-adder encoding distinguishes exactly the valid tuples. Therefore the revised theorem is deliberately limited to relations whose full visible-plus-auxiliary solution set is affine. It closes the “fresh variables might rescue a pure system of GF(2) rows” loophole, but it does **not** close paid nonlinear DEF/AND3/RES/LOCAL-CONVERT, branching, or the full historical mixed calculus.

## Restricted theorem: fresh linear witnesses do not help

Let $S\subseteq\{0,1\}^{bq}$ be the one-hot indicator vectors satisfying

$$
\sum_{i=1}^{b}\epsilon_i a_i=c\pmod q,
$$

and let $U$ be all one-hot boundary tuples. Assume $q\ge3$ is odd and $b\ge3$. By `[P2-L1-530]`,

$$
\operatorname{aff}_{\mathbb F_2}(S)=\operatorname{aff}_{\mathbb F_2}(U).
$$

Let a candidate auxiliary construction be any finite affine system

$$
R=\{(x,y)\in\mathbb F_2^{bq+r}:Ax+By=d\},
$$

with arbitrary $r$, arbitrary row widths, sharing, repeated use of auxiliaries, and an arbitrary auxiliary witness $y$ that may depend on $x$. Suppose

$$
\forall s\in S\;\exists y\;(s,y)\in R.
$$

Then

$$
\forall u\in U\;\exists y\;(u,y)\in R.
$$

**Proof.** If $R$ is nonempty, choose $z_0\in R$ and write $R=z_0+L$ for a linear subspace $L$. Coordinate projection $\pi(x,y)=x$ is linear, so

$$
P:=\pi(R)=\pi(z_0)+\pi(L)
$$

is affine. The lift premise says $S\subseteq P$. Every affine set containing $S$ contains $\operatorname{aff}(S)$, hence

$$
U\subseteq\operatorname{aff}(U)=\operatorname{aff}(S)\subseteq P.
$$

Thus every wrong-charge one-hot tuple also has a lift. The empty-$R$ case cannot satisfy the premise because $S$ is nonempty. QED.

This proof is independent of the number of auxiliary coordinates and equations, their widths, or whether a single auxiliary has multiple consumers. It also permits different existential witnesses for every valid tuple. It is a relation-level impossibility, not a lower bound on proof length, construction time, search time, or checker cost.

## Exact finite controls and independent replay

Two separately written implementations replayed the theorem boundary without invoking a historical checker.

* Python verified $q=3$, $b=3,4,5$ with alternating signs: valid and all-one-hot affine dimensions agree at $6,8,10$. For $q=3,b=3$, it enumerated all 1,024 affine equations on the nine visible indicators. Exactly eight equations contain the valid fiber; all eight contain every one-hot tuple. It then replayed all 36 pairs of such equations; none excludes a wrong tuple.
* Independent Node.js verified the same dimensions, enumerated every coefficient row for all three odd cases, and replayed the same eight equations and 36 pairs. It reports 37,492 checks; Python reports 1,152 grouped checks.
* Hostile hypothesis controls fire where they should: for even $q=2,b=3$, mask 21 separates the valid fiber; for odd $q=3,b=2$, mask 10 separates it. These match the exceptional dimensions in `[P2-L1-530]`.
* A nonlinear mod-three state chain on $b=4$ accepts exactly 27 valid tuples and rejects all 54 wrong tuples. Thus an overbroad “all auxiliaries fail” claim is explicitly falsified. LSPV-3/530's source-authenticated stronger upper control uses $3(b-1)$ fresh one-hot state indicators and $19(b-1)+1$ width-at-most-three clauses plus a unit; native simulation in historical `R_mix341` remains to be authenticated.

Artifacts and SHA-256:

* `experiments/review/lspv5_457_affine_aux_projection_audit.py` — `21a063458257ef4e8bfdb9be3b7535bfac034f75205a5a71b01b4b7461e170bf`
* `experiments/review/verify_lspv5_457_affine_aux_projection.js` — `9a2fd06f2e639f94b5149e16c524013b30a51c222c48f5c80fbdc11ce45e4187`
* `results/raw/arc/2026-11-09_0253_LSPV5_457_AFFINE_AUX_PROJECTION_RAW.json` — `848dadb1386641affe03bae3ef3a291032e76244b3092a9e4c7af708c4dfdedc`

All controls PASS. Finite checks are corroboration, not the arbitrary-size proof; the displayed projection argument is the proof.

## Established-family and transfer ledger

| Family / method | Exact encoding, theorem and model | Known shortcut and remaining transfer |
|---|---|---|
| Cubic mod-three Tseitin strict 3-CNF | For each edge $e$, indicators $x_{e,t}$, $t\in\mathbb F_3$, with one width-three positive ALO clause. For each cubic vertex, one negative width-three clause forbids each locally wrong incident triple: 18 clauses per vertex. Thus $3|E|$ Boolean variables and $|E|+18|V|$ clauses; nonzero total charge certifies UNSAT. Pang, arXiv:2610.00837v2, gives exponential size for qualifying opposite-characteristic fixed-degree $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ families through a degree--size theorem. This is proof-system-specific and explicitly uses no extension variables in the approximation theorem. | `[P2-L1-530]` blocks original-boundary affine GF(2) rows; this run blocks arbitrary **pure-affine** auxiliary lifts. LSPV-3/530 gives a short nonlinear modular-adder encoding. Exact lower-bound preservation from the published theorem through that encoding and every legal historical mixed rule is still OPEN. |
| Ordinary Resolution controls | Haken PHP and Urquhart expander-Tseitin give restricted shared-DAG Resolution lower bounds. | Cook ER, affine elimination, learned/shared lemmas, nonlinear auxiliary state, and mixed rules remain legitimate upper-bound controls. No Resolution lower bound is promoted to arbitrary algorithms or full `R_mix341`. |
| $\operatorname{Res}(\operatorname{PC}_d/F)$ | Khaniki, ECCC TR20-034 rev. 3, proves almost-quadratic DAG lower bounds and stronger tree-like bounds for fixed-degree systems on stated mod-$q$ Tseitin/random-CNF/PHP families when the field characteristic mismatches the modulus. | Different grammar, axioms, degree restriction and weights. It does not authenticate historical bytes or prove `[P2-B1]`/`[P2-B2]`. |
| Nonlinear auxiliary modular adder | LSPV-3/530: three-state chain, linear variables/clauses, exact existential projection to the modular fiber. | Mandatory shortcut control. A flat no-auxiliary CNF minimum is not mixed-system hardness. Historical native-rule legality, provenance and exact paid-node cost remain OPEN. |

Certified UNSAT, certified proof-size hardness, and empirical solver behavior remain separate.

## Search and continuity audit

Both live trackers were read completely before work: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` research-stage blob `ea935dd1ae37437443fcb56dc4d7402e9ad32707`. The governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3, `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, full research skill/mode/protocol files, latest MAIN report, current LSPV-1/530, LSPV-2/516, LSPV-3/530, LSPV-4/516 and LSPV-5/456 originals, and their relevant code/raw/handoffs were reviewed. Actual independent files read were `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70` and `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`; neither claims the missing unrestricted transfer.

The local scheduled workspace was a partial scratch tree: the mandated preflight found no repository-root `main.tex`, reports, or root trackers locally. All governing material was therefore read from GitHub. The remote root `main.tex` blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` again returned zero readable bytes; it was not edited. A role-owned durable fallback insertion is supplied.

Primary literature actually inspected: Pang 2026 arXiv:2610.00837v2 theorem/rules and its explicit “without introducing extension variables” scope; Khaniki ECCC TR20-034 rev. 3 abstract/model/quantified bounds; Filmus--Lauria--Mikša--Nordström--Vinyals on PC/PCR size/space controls. A UC thesis page concerning polynomial calculus with extension variables was search-discovered but blocked by a JavaScript/anti-bot page, so no theorem from it is relied upon. Indexed web search was available; no separate Google-branded portal was available, so Google use is not claimed.

Required repository heads were unchanged: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`. Targeted searches for affine projection, extension variables, Tseitin and XOR found no authentication of `R_mix341` or B3. The blkph0x affine-projection lab correctly distinguishes existential support from stronger counting claims and its Tseitin lab preserves a restricted Resolution scope; these are hypothesis/control sources, not authority for this theorem. Rotating unchanged proof/formalization heads checked: `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`, and `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`. The final openai/math targeted code search was rate-limited after the pinned-head review; no claim depends on it.

## Shared-DAG and resource qualification

The restricted theorem already grants one global system with shared auxiliaries and free after-the-fact witness choice. It says nothing about branch assumptions, OR choice among derivations, nonlinear definitions or AND discharge. A branching proof DAG must still discharge all selected cases and may share only context-legal lemmas as in `[P2-L5-453]`. No case split or weakening rule is added to the historical calculus.

Ideal logical work in the theorem is a relation statement, not a runtime. Actual charged work for this run includes complete tracker/peer/Grok/Claude/source reads, repository and literature queries, program construction, 12,347 artifact bytes, Python/Node execution, raw serialization, report/handoff/outbox preparation, Git writes, conflict handling and full readback. The finite verifiers used negligible resident memory recorded in raw output, but no machine-resource lower bound follows. Discovery cost is intentionally absent from $W_R$ and remains charged for actual upper-bound algorithms.

## Tracker determination and precise gap

`proof1.txt`: **no material status, dependency, evidence or gap change**.  
`proof2.txt`: material restricted evidence at `[P2-L5-457]`, depending on/refining `[P2-L1-530]`, `[P2-C3]`, `[P2-D1]`, `[P2-B1]`, and `[P2-B2]`.

**Actual advance:** arbitrary fresh linear auxiliaries and shared GF(2) rows cannot repair the odd-modulus boundary affine-hull obstruction, even with input-dependent existential witnesses.  
**Independent challenge:** even-modulus, two-boundary, and nonlinear three-state controls all evade the theorem exactly where its assumptions predict.  
**Precise remaining gap:** authenticate the historical native grammar and checker; then prove a lower-bound-preserving transfer across nonlinear DEF/AND3/RES/LOCAL-CONVERT, branching, shared lemmas and every shortcut to superpolynomial $\overline W_R$; separately prove noncircular same-calculus B3. None is supplied. P versus NP remains **OPEN**.

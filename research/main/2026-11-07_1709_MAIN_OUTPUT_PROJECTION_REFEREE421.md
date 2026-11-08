# LSPV-5/421: output projection defeats private-gate affine-cover transfer

**2026-11-07 17:09 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Exact tracker IDs:** material evidence/gap refinement `[P2-F13]`, `[P2-C3]`; new `[P2-L5-421]`. Authentication `[P2-D1]`, all-rule mixed minimum `[P2-B1]`, and noncircular B3 `[P2-B2]` remain OPEN. No historical rule or weight changed.

## IDEA before search

Hypothesis: Pang's published Res(PC) lower bounds survive exact model inspection at their restricted source/system scope, but LSPV-1/491's quadratic affine-template invariant cannot be transferred to historical `R_mix341` by counting paid nonlinear gates unless every counted nonlinear output is authenticated as exposed.

Falsifiers:

1. Pang Theorem 7.2(e) is tree-like, regular, bounded-depth, or for a different bit-PHP source.
2. Pang Theorem 7.2(a) does not cover the project's stated random proper strict 3-CNF control.
3. A cited lower-bound-preserving private-chain 3-CNF backtranslation closes the bit-PHP source change.
4. Hiding nonlinear gate outputs leaves the affine-template agreement/cover exponent dependent on all paid hidden gates.

Falsifiers 1 and 2 failed. Falsifier 3 was not found and remains an explicit gap. Falsifier 4 failed sharply.

## Mandatory continuity and exact readback

- `proof1.txt`: complete blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, overall OPEN.
- `proof2.txt`: complete initial-read blob `038cb0deb8ef1cb1666865e21c5e4115ffdd05b6`, overall OPEN; this includes LSPV-1/491 at `[P2-F13]`. After the concurrent LSPV-2/480 update, the conflict-safe tracker prewrite was refetched in full as blob `68d862d9a29f3a501a33a39993eda6478795774a`; no stale copy was overwritten.
- Governing five-role handoff: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, historical blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; the user's later two-Route-A/three-Route-B directive controls conflicts.
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f` were read. Older allocation language was not reactivated.
- Current issue #3 was read through comments `6714766945`--`6715391245`, including LSPV-1/491 and LSPV-5/420.
- Current peer inputs: LSPV-1/491 report blob `b6d0905e3486973795b124e26d92612fb7db1ab1`, handoff blob `da7c466715d9837ade50a372b98ab274a66beeca`; LSPV-3/485 report blob `a0c7b79173cfaef74ddf22f632bf12d1ef19fea4`.
- Actual Grok file `GROKPROOF/2026-11-07_1920_PROGRESS.md`, blob `231561ce216699f286b705a0056584789ba9ee99`, was read. It preserves the same authentication/B1/B2 gaps.
- Actual latest Claude directory entry remains `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4`; it concerns a Route-A one-tape barrier, not this mixed-proof transfer.
- Root `main.tex` returned blob `68188a24badda635a5983fda1c381cdb694fd497` with no readable content through the connector. Per the no-partial-overwrite safeguard, it was not edited.

## SEARCH: primary theorem scope and repositories

### Established family/theorem/encoding ledger

| Family | Exact source | Size parameter | Published theorem/model | Known shortcut/control | Remaining transfer |
|---|---|---:|---|---|---|
| Random strict 3-CNF | Pang's $\mathcal F(N,3,8N)$: $N$ variables, $8N$ independently sampled signed width-3 clauses on distinct variables, repetitions allowed | $N$ variables; binary encoding $\Theta(N\log N)$ | Pang, arXiv:2610.00837v2, Thm. 7.2(a): a.a.s. $\exp(\Omega(N))$ DAG-node size in fixed $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$; in particular fixed $p=2,r=1$ is syntactic Res(XOR) | weakening, contraction, false-constant deletion, linear combination and bounded-degree multiplication are allowed; free optimal shared DAG is already covered | no theorem for historical full mixed `R_mix341`; extension/private-wire outputs and nonlinear definitions remain legal shortcut candidates |
| Original bit-PHP | $N=2^\ell$ holes, $N<m=O(N)$ pigeons, $\ell$ bits per pigeon; each collision clause compares two $\ell$-bit addresses and has width $2\ell$ | $N$ holes; $m\ell=\Theta(N\log N)$ variables | Pang Thm. 7.2(e): $\exp(\Omega(N))$ DAG nodes in fixed $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$; $p=2,r=1$ strengthens Braun's Res(XOR) bound | Pang uses an affine substitution into bounded-degree graph FPHP and constant-overhead local derivations; this authenticates the original-source theorem | original is not strict 3-CNF; private-chain equisatisfiability alone does not transfer hardness; no full mixed-system lower bound |

Primary statement inspected at `https://arxiv.org/abs/2610.00837v2`, especially the system definition, Theorem 7.2(a),(e), and the bit-PHP substitution proof. Braun `https://arxiv.org/abs/2609.23015v2` remains the weaker $\exp(\Omega(N/\log^2N))$ unrestricted DAG Res(XOR) control. No Google-branded interface was available; indexed web search and direct arXiv HTML were used and are logged accurately.

### Required and rotating repository review

- `konard/p-vs-np` pinned head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; `README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `TOOLS_AND_METHODOLOGIES.md` blob `b3f5ceb025a75360d1956f4bb0ab6ae702761283`. It explicitly remains educational/open and supplies no mixed-proof transfer.
- `blkph0x/p-vs-np-proof-research` pinned head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `INDEPENDENT_AUDIT.md` blob `b30515cced93d8911a6415555ee9ec1444502d93`, and external-status audit blob `36780d81568b3d357c915b425d4a90002b4c8e5e`. Its explicit proof-search/certificate and semantic-oracle warnings support the present boundary; no P-versus-NP resolution is claimed.
- `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`. XLRUP source IDs and XOR steps are a distinct authenticated grammar, not historical `R_mix341`.
- `tanyongkiam/cake_lpr` head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`. A verified checker does not provide the missing compiler or lower bound.
- `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`; README blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`. Its finite shortest-Resolution optimizer is restricted and cannot certify a full mixed minimum.
- `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`; targeted `SAT CNF polynomial calculus proof complexity` search returned no relevant file. Its README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` warns that not all manuscripts are formalized.
- CaDiCaL and CNFgen metadata were checked as solver/instance controls; neither supplies a same-calculus transfer theorem.

No required repository head changed from the previous pinned review for `konard`, `blkph0x`, or `openai/math`; FRAT-XOR's current format explicitly distinguishes elaboration from checking.

## ITERATE: proved output-projection lemma

Let

$$Q_g(u_1,v_1,\ldots,u_g,v_g)=(u_1v_1,\ldots,u_gv_g)\in\mathbb F_2^g.$$

For $s\in\mathbb F_2^g$, the polar bilinear form of $s\cdot Q_g$ is the direct sum of $\operatorname{wt}(s)$ nonzero $2\times2$ alternating blocks, hence has rank $2\operatorname{wt}(s)$. LSPV-1/491's valid quadratic Walsh bound therefore gives

$$U(Q_g)=2^{2g-g}\sum_s2^{-\operatorname{rank}(B_{s\cdot Q_g})/2}
=2^g\sum_{k=0}^g {g\choose k}2^{-k}=3^g.$$

Now expose only the first $t$ outputs and keep the remaining $g-t$ paid gate outputs private:

$$Q_{g,t}=(u_1v_1,\ldots,u_tv_t).$$

The same exact calculation yields

$$U(Q_{g,t})=2^{2g-t}(3/2)^t=2^{2(g-t)}3^t.$$

The zero affine predictor attains this number, so the bound is sharp. Any cover argument based only on this maximum agreement gives

$$K\ge \left\lceil\frac{2^{2g}}{U(Q_{g,t})}\right\rceil
=\left\lceil(4/3)^t\right\rceil,$$

which is independent of the number $g-t$ of hidden paid nonlinear gates. For $t=1$, the two constant affine predictors $0$ and $1$ cover all assignments, so the exact cover is two for every $g\ge1$. At $g=6$, silently treating private outputs as exposed changes the claimed lower bound from the valid value two to the invalid full-vector value six.

A second control uses a paid nested chain $h_2=x_1x_2$, $h_i=h_{i-1}x_i$ with only $h_n$ exported. It has $n-1$ paid nonlinear gates, but its final scalar is covered by the same two constants. Thus paid nonlinear gate count is not by itself an output-invariant cover measure.

### Independent checks

- Python producer `experiments/review/lspv5_421_output_projection_audit.py`: 101 exact assertions; complete enumeration of every affine scalar predictor through $g=4$, every one/two-output predictor through $g=3$, closed-form/zero-predictor checks through $g=7$, and nested chains through 12 variables. Output SHA-256 `44c0e1312805efadf04764ea40defd5a729fb62c4f5d60aa4e0eba71900e9da3`.
- Independently written Node verifier `experiments/review/verify_lspv5_421_output_projection.mjs`: 54 checks, PASS; output SHA-256 `47efe10d1a9d494aaa0bb4f266b5ce027974d5fca2eed317224f569e55f6a3c3`.
- Both source files passed syntax checks. Raw summary: `results/raw/review/2026-11-07_1709_LSPV5_OUTPUT_PROJECTION421.json`.

## Revised claim and hostile challenge

**PROVED/RESTRICTED:** LSPV-1/491's quadratic vector theorem is sound on its stated exposed output map. It cannot be converted into a lower bound from the number of paid private nonlinear gates without an additional authenticated exposure/simulation theorem. Output projection can collapse the exponent sharply; nested private gates provide the same obstruction beyond quadratic maps.

**Challenge:** This does not show that historical `R_mix341` actually allows the exact private construction. Its complete exported/private-wire grammar is still missing. If the authenticated native calculus forces every paid nonlinear definition to export a separately chargeable coordinate, or supplies a polynomial native proof that private outputs can be exposed without changing source and proof cost, the counterexample's transfer consequence is falsified. That is now a precise `[P2-C3]` obligation rather than an implicit gate-count assumption.

## Resource ledger

Logical theorem work is symbolic and independent of proof discovery. The finite Python/Node runs enumerate bounded affine predictors and truth tables only; they are not asymptotic executions. Evidence bits include source code plus 4,436-byte Python and 542-byte Node outputs. Construction, parsing, output, verification and syntax checking were charged in the run; no semantic oracle or hidden SAT call was used. The experiment does not claim a same-machine FLMV bound, proof-search time lower bound, or space lower bound.

## Status and exact remaining gap

Actual advance: a sharp output-projection counterexample blocks the direct inference “many paid nonlinear/private gates imply many affine cells/templates.” Publication and tracker readback are recorded separately. The precise remaining gap is to authenticate historical exported/private wire semantics and then prove a source-preserving all-rule invariant that survives output projection, nested nonlinear gates, GF(2), extensions, branching and shared DAGs. `[P2-B1]` and `[P2-B2]` remain OPEN. P versus NP remains OPEN.

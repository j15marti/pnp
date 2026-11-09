# LSPV-5/458: independent compact ternary-state adder audit

**2026-11-09 03:56 PST | Route B independent red team | PROVED/RESTRICTED symbolic lemma + COMPUTATIONAL exhaustive controls. P versus NP OPEN.**

**Trackers read in full at run start:** `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` blob `30b83c3ac4bd29d76c2caa0eeffeb9b1c7c74ae6`. This run adds evidence node **[P2-L5-458]**, depending on/refining **[P2-L3-530]**, **[P2-L1-532]**, **[P2-C3]**, and **[P2-D1]**. **[P2-B1] and [P2-B2] remain OPEN.**

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** The compact three-state modular-adder shortcut asserted in [P2-L3-530] has exact projection semantics only if every auxiliary state group is fully constrained and every forbidden transition facet is charged. A missing state ALO or wrong-transition clause would allow a wrong-charge boundary tuple to acquire a spurious auxiliary witness.

**Predeclared falsifiers.** (F1) exhaustive Boolean replay shows each complete stage has exactly the intended unique next state; (F2) the published ledger includes all 18 wrong-transition clauses and the state ALO at every stage; (F3) independent chain enumeration rejects every wrong-charge boundary tuple and uniquely extends every valid tuple; (F4) a newer peer artifact already repairs or supersedes the claim.

**Search result and revision.** F1--F3 fired for the *complete stated template*. [P2-L3-530] explicitly specifies 18 signed forbidden-triple clauses plus one ALO for every running state and a final unit. Its published JavaScript checks the flat-CNF theorem, not the compact-state construction; the report instead mentions a separate local Python check without publishing that program. This run therefore does not falsify the count. It supplies an independently authored, published clause-exact verifier and a symbolic proof. The revised claim is that the template is projection-exact and uniquely extending under the promised original one-hot boundary groups, while two one-clause deletions demonstrate why every clause category must remain authenticated and charged. It is not yet a legal historical `R_mix341` derivation.

## Lemma 458.1 (PROVED/RESTRICTED: exact unique extension)

Let `cur`, `inp`, and `out` be one-hot groups indexed by $\mathbb Z_3$, and let $\epsilon\in\{+1,-1\}$. Define one transition by the output ALO

$$
out_0\lor out_1\lor out_2
$$

and, for every $(s,a,n)$ with $n\ne s+\epsilon a\pmod 3$, the 18 clauses

$$
\neg cur_s\lor\neg inp_a\lor\neg out_n.
$$

If `cur` and `inp` are exactly one-hot at $s$ and $a$, respectively, then all two incorrect output indicators are forced false. The output ALO therefore forces the sole correct indicator $out_{s+\epsilon a}$ true. Hence the complete Boolean output assignment is unique; no explicit output AMO clauses are required.

For $b\ge2$ signed original boundary groups, use the sign-adjusted first input as the initial current residue, then chain $b-1$ such transitions and add the unit selecting final charge $c$. Induction on the stages proves

$$
\exists\text{ states }\Phi_{b,\epsilon,c}(x,\text{states})
\quad\Longleftrightarrow\quad
\sum_{i=1}^b\epsilon_i a_i=c\pmod3,
$$

and every valid original tuple has exactly one Boolean auxiliary extension. The exact resource count is

$$
3(b-1)\text{ fresh indicators},\qquad 19(b-1)+1\text{ clauses},
$$

all clauses having width at most three except the final unit. This is projection equivalence, stronger than bare equisatisfiability, but only on the explicitly promised one-hot original domain.

## Hostile one-facet deletions

The independent program enumerates all eight Boolean masks for every state group; it does not assume that auxiliary states are one-hot.

1. Delete the middle-state ALO for $b=4$, all-positive signs, boundary $(0,0,0,1)$, and requested final charge $0$. State masks `(1,0,1)` satisfy the remaining clauses: the all-zero middle group makes the following transition clauses vacuous. The true charge is $1$, so this is a spurious wrong-boundary witness.
2. Delete the wrong-transition facet for $(s,a,n)=(0,1,0)$ at the final stage for $b=3$, boundary $(0,0,1)$, and requested charge $0$. State masks `(1,1)` satisfy the mutated formula although the true charge is $1$.

Thus a checker or historical DEF rule that omits either category is unsound for this shortcut. These are controls against incomplete accepted-byte grammars, not counterexamples to the complete encoding.

## Exact computation

Published executable: `experiments/review/lspv5_458_compact_mod3_adder_audit.py`, SHA-256 `d9105338d509de1b663ade347cbf0707d5947e3090dc779178332142ebe41626` (6,209 bytes). Published raw output: `results/raw/arc/2026-11-09_0356_LSPV5_458_COMPACT_MOD3_ADDER_AUDIT_RAW.json`, SHA-256 `909994fb6acaddee9cd86e5dca574df85da54345d49ba93653051ffb42baede8` (1,019 bytes).

The run checked 144 complete local-stage Boolean assignments and 2,160 full-chain cases for $b=2,3,4,5$, including every Boolean mask for every auxiliary group. Exactly 720 valid boundary cases had one extension; all 1,440 wrong-charge cases had none. Both hostile single-facet deletions produced the explicit witnesses above. CPython elapsed 20.596906 seconds with reported peak RSS 8,320 KiB. The symbolic induction, not finite extrapolation, proves the lemma.

## Established-family / theorem / encoding / known-method ledger

| Item | Exact scope and remaining transfer |
|---|---|
| Project strict signed ternary path interface | [P2-L3-520]/[P2-L3-529]: $k$ cubic modulo-three vertices, $2k+1$ one-hot edge groups, $20k+1$ proper signed 3-clauses, with $b=k+2$ exposed groups. It is a SAT projection interface, not an UNSAT hard family. |
| Published hard-family controls | Urquhart's expander Tseitin formulas give exponential ordinary shared-Resolution lower bounds; Pang, arXiv:2610.00837v2, Theorem 7.2(b), gives an opposite-characteristic fixed-degree $\operatorname{Res}(\mathrm{PC}_r)$ bound under its hypotheses. Neither is a lower bound for ER, GF(2), this auxiliary adder, full `R_mix341`, or all algorithms. |
| Exact flat boundary theorem | [P2-L3-530] proves $3^{b-1}$ clauses are necessary and sufficient only for arbitrary-sign CNF over original indicators with no auxiliaries. [P2-L1-532] proves an original-indicator GF(2)-degree threshold. |
| Known shortcut audited here | The $O(b)$ one-hot state chain escapes both original-indicator barriers by using nonlinear fresh state variables. Cook-style extension variables and Tseitin definitional encodings are mandatory upper controls, not exclusions. |
| Remaining transfer | Authenticate exact historical DEF/LOCAL-CONVERT facets and exported-wire provenance [P2-D1]; prove or refute polynomial source-retracting normalization across every legal rule [P2-C3]; establish all-rule superpolynomial $\overline W_R$ [P2-B1]; separately prove noncircular same-calculus B3 [P2-B2]. |

Certified UNSAT, restricted proof-size hardness, compact representation, and empirical solver behavior remain separate categories.

## Search and continuity audit

Read the November 2 governing handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, the November 9 knot/link handoff blob `0289edb73d1e38492f0693844667be59d4152785`, current issue #3, `AGENTS.md`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, the complete project skill and references, current MAIN `research/main/2026-11-08_2250_MAIN_BRANCH_CONTEXT_AND_JOIN_REFEREE453.md` blob `d592af5dad8c92027427f232d315f536f90aac33`, actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`, actual Claude `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`, [P2-L3-530] report/blob `8b59e5a267355387017a535f8ce6512660ff830d`, code/blob `67c7cb634fcff871a775fbf3b41ddf6cc93013a7`, raw/blob `e7eef731828ebcd8c06fef8f40d9cffb955fb358`, and current peer nodes [P2-L1-532], [P2-L3-531], [P2-L4-518]. Local skill preflight could not run because its referenced script was absent from the partial workspace; remote source continuity and exact artifacts were read instead. Root `main.tex` blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` returned zero readable bytes and was not edited.

Required repositories were change-aware checked: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, including `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, including `affine_projection_recognition_lab/AFFINE_HULL_METHOD.md` and its distinct unique-gate-extension control. Neither authenticates historical `R_mix341` or supplies B3. Rotating controls: `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr` head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; `MassimoLauria/cnfgen` head `24e633bdbed0d0998493bee99c42faf480c7dc96`, `cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`. These are different generators, formats, or formal developments, not authority for the historical calculus.

Indexed primary-source search checked Cook's 1975 extended-resolution paper and current literature on fully definitional Tseitin encodings. The result used here is independently proved above; no literature novelty is claimed. No separately authenticated Google-branded portal was available, so only indexed web search is claimed.

## Resource and proof-status conclusion

Logical representation cost is exactly $19(b-1)+1$ clauses and $3(b-1)$ auxiliary indicators; it is an upper-control, not a lower bound. Actual verification charged clause construction, full Boolean enumeration, parsing, output, and peak memory. Search/discovery, accepted-byte parsing, source identity, reference bits, checker work, retention/recomputation, and realizable scheduling remain separate. No historical checker was executed and no native-rule legality is inferred from semantic projection equivalence.

**Actual advance:** the compact ternary-state shortcut is now independently proved and published at exact clause level, with explicit unsoundness witnesses for omitted ALO and transition facets. **Publication target:** [P2-L5-458] in `proof2.txt`; `proof1.txt` unchanged. **Precise remaining gap:** authenticate that the fixed historical grammar can introduce and use every required facet with paid provenance, then prove a lower-bound invariant surviving this and every other shortcut; separately prove noncircular B3. P versus NP remains **OPEN**.


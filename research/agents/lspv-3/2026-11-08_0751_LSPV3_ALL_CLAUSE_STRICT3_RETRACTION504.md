# LSPV-3/504: simultaneous strict-3 source retractions preserve Resolution hardness and exact mixed source-capacity

**2026-11-08 07:51 PST | Route B | PROVED/RESTRICTED symbolic theorem and COMPUTATIONAL controls | P versus NP OPEN.**

**Exact proof-chain IDs:** new scoped evidence **[P2-L3-504]**, extending **[P2-L3-503]**, refining **[P2-C3]**, **[P2-D3]**, and **[P2-F13]**. Full historical grammar **[P2-D1]**, all-mixed-rule normalization **[P2-C3]**, universal superpolynomial minimum **[P2-B1]**, and noncircular same-calculus B3 **[P2-B2]** remain OPEN. Companion **[P1-01]**, **[P1-03]**, **[P1-04]** OPEN.

## IDEA: pre-search hypothesis and precise falsifiers

Starting with a published ordinary-DAG-Resolution-hard signed cubic-expander odd Tseitin family, test whether the *single-source-clause* strict3 replacement of LSPV-3/503 can be applied SIMULTANEOUSLY to any subset of the original 4h clauses, including ALL clauses, without weakening its proof-theoretic lower-bound transfer. This is an encoding-control extension of an established hard family, NOT an invented claim of hardness against all SAT algorithms.

1. Simultaneous use may make one of the three gadget clauses redundant, defeating the every-source-ancestor lower bound.
2. Eliminating all 2k private variables may not give a legal source-indexed, nonexpansive **Resolution proof** backtranslation, despite equisatisfiability.
3. One of the 3-CNF clauses may acquire repeated variables, conflicting signed polarities, or require more than two paid RES steps per gadget.
4. An alleged historical R_mix341 RES-to-AND3 edge may be accepted only in a distinct **declared** calculus; without authenticated original bytes and conversion charges it must NOT be claimed native.

## SEARCH: authenticated project and external evidence

Read complete current root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` at start of this run blob `9fbf654510036feb5bebb7e8f06e2c28c756df20`; issue #3 including LSPV-3/503 and LSPV-5/435; the November 2 five-role handoff (file blob `c3889a3e514ddbd747150dcb68607013a3b2d154`); AGENTS.md, CODEX.md and the project pnp-research skill; exact original LSPV-2/341 prose blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`; recovered subset checker blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`; LSPV-3/503 report blob `aebdfac5c92abf011b16ad8a3a6e6183c38d0914`, /502, red-team /435 and peer /506. Reviewed actual `GROKPROOF/2026-11-08_1130_PROGRESS.md` and `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`; neither is native rule authority.

Change-aware checked `konard/p-vs-np/scripts/proof_status.json` and `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (latter blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`), `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`, `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`, and `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. None supplies the missing historical RES-to-factor/LOCAL/DEF byte grammar. The Nov 1, 2026 CakeLPR final release is a DIFFERENT checker. Searches made: GitHub `LOCAL-CONVERT`, `R_mix341`, `4h+2k`, `multi clause expansion`, `all clauses strict3 retraction`; public web `Ben Sasson Wigderson 2001 Tseitin expander formulas resolution exponential size width lower bound`, `resolution proofs closed under substitutions literals variables polynomial no increase size`, `resolution proofs substitutions literals variables polynomial`, and Pang arXiv search. A separate Google-branded client was not available.

Established baseline: Ben-Sasson and Wigderson, *Short Proofs are Narrow: Resolution Made Simple*, **J. ACM 48(2) (2001), 149-169**, https://doi.org/10.1145/375827.375835. Expander odd Tseitin has exponential ordinary Resolution size in the applicable constant-degree expansion model. Haken PHP, Cook ER, Pang `Res(PC_r/F_3)`, FRAT-XOR and CakeLPR are distinct controls, never substituted for a mixed-system theorem.

## ITERATE: all-k theorem, full clauses, and exact direction

Let `T(G,b)` be the ORIGINAL ordinary signed-edge, strict 3-CNF encoding of odd-charge Tseitin on any connected simple **bridgeless cubic graph** G with h vertices: n=3h/2 edge variables, exactly m=4h source clauses, four forbidden-pattern 3-clauses per vertex. Every original clause is indispensable (the G-v connectivity argument from /341). Choose an arbitrary subset S of k original clause *positions*, 0<=k<=4h. For each selected original source clause `C_j=(ell_j1 OR ell_j2 OR ell_j3)`, create fresh pair u_j,v_j and replace C_j by exactly

$$
A_j=(\ell_{j1}\lor\ell_{j2}\lor u_j),\quad
B_j=(\neg u_j\lor\ell_{j3}\lor v_j),\quad
D_j=(\neg u_j\lor\ell_{j3}\lor\neg v_j).
$$

All other clauses remain byte-identical original signed clauses. Denote resulting source `H_S(G,b)`. Each gadget uses truly fresh variables, so ALL external sources remain *proper signed strict width-three*. The exact source counts are

$$
n_S=3h/2+2k,\qquad m_S=4h+2k,\qquad N_S=\Theta(h\log h)\quad(0\le k\le4h)
$$

for standard explicit binary-indexed or ordinary decimal-indexed DIMACS-style encodings of fixed-degree indexed graphs.

**Theorem 504.1 (PROVED/RESTRICTED, original-source Resolution hardness transport).** Every `H_S` is UNSAT; every one of its `m_S` original source clauses is indispensable. More importantly, EVERY ordinary shared-DAG Resolution refutation of `H_S` converts into an ordinary Resolution refutation of ORIGINAL `T` using *at most* as many paid Resolution inferences. Thus

$$
S_{\rm Res}(T(G,b))\leq S_{\rm Res}(H_S(G,b)).
$$

**Proof of UNSAT and essentiality:** For every selected j, the gadget's existential projection onto old variables is *exactly* C_j, because resolving B_j,D_j on v_j gives `(not u_j OR ell_j3)`, and resolving with A_j on u_j gives C_j. The private variable sets are pairwise disjoint. For the deletion of an unchanged source clause, use the already certified deletion witness for T and independently extend all other satisfied gadgets. For a deletion of A_j, B_j, or D_j, take the T-deletion witness falsifying C_j (which satisfies every other original clause) and set respectively `u_j=0`, `(u_j,v_j)=(1,0)`, or `(u_j,v_j)=(1,1)`; all remaining gadgets extend independently. Therefore each of the m_S source clauses is essential.

**Proof of hard direction:** Apply the SIMULTANEOUS literal/constant substitution `sigma(u_j)=ell_j3`, `sigma(v_j)=0` to every expanded source and every inference. Each A_j maps to the actual original C_j, while B_j and D_j become tautologies; unchanged original source clauses map to themselves. In topological order maintain, for each non-tautological substituted clause, a previously derived subclause. A substituted RES step either preserves a complementary nonconstant pivot and uses ONE RES inference, or its conclusion is a tautology, or one stronger already derived parent subclause suffices when a pivot disappears/turns constant. This standard one-inference-or-reuse substitution transformation preserves shared-DAG reuse. The final empty clause remains empty. This is a PROOF-to-PROOF lowering, not an inference from equisatisfiability. On any known cubic-expander family with `S_Res(T_h)>=2^{c h}` for some c>0, it follows that

$$
S_{\rm Res}(H_{S_h})\ge 2^{\Omega(h)}
=\exp(\Omega(N_S/\log N_S)).
$$

No analogous lower bound is claimed in full historical R_mix341, extended Resolution, Res(XOR), or arbitrary SAT algorithms.

**Theorem 504.2 (PROVED/RESTRICTED, exact separate-calculus upper/lower control).** In the DISTINCT fixed unit-weight, source-authenticated, binary-premise calculus `R_bridge503`, which explicitly allows exact RES-derived Boolean clauses as AND3 factor inputs, reconstruct each expanded C_j with TWO paid RES inferences, build the original h vertex affine rows using 3h paid AND3, and cancel them using h-1 paid binary GF(2) XOR. This gives

$$
q=2k+3h+(h-1)=4h+2k-1=m_S-1.
$$

The all-essential source ancestry argument, valid for EVERY legal shared/reconvergent DAG of that *declared* binary-premise calculus, gives `q >= m_S-1`. Hence

$$
\boxed{W_{R_{\rm bridge503}}(H_S)=4h+2k-1},
\qquad D\le4+\lceil\log_2 h\rceil
$$

with balanced row and XOR trees. The upper is an explicit legal proof in `R_bridge503`, NOT an accepted historical `R_mix341` record. A paid RES-to-AND3 CAST would modify this arithmetic.

## COMPUTATIONAL controls, exact binaries and ledger

A newly implemented dependency-free JavaScript executable was actually evaluated in V8 and published with a complete raw JSON readback. The tested original signed families are K4 (h=4), K3,3 (h=6), and cube (h=8), including original odd UNSAT, even-charge SAT, *every* old original clause deletion witness, every new gadget source deletion witness, proper width-three syntax, explicit two-step RES reconstruction, all eight per-gadget local existential assignments, and three invalid-pivot controls. **10,386 assertion checks passed, 14 subset-size experiments passed, and 3 malformed-pivot attacks were rejected.** For k=4h, the exact paid counts were K4 **47**, K3,3 **71**, cube **95**. Separately independently authored Python source `/mnt/data/lspv3_504_multigadget.py` passed 10 parallel experiments on K4 and K3,3 with all-source-deletion witnesses; that source is available as a conversation artifact, not claimed GitHub-replayed. Neither host program was an execution of the full original /341 parser, whose missing RES interface prevents that experiment.

Logical nodes q and weighted span are stated above. Provenance and explicit evidence: original graph/charge/clauses, signed literals, source-ID map, 2k RES pivots, 3h bounded tables, h-1 original-variable affine rows. Under standard explicit numeric indices, factor and RES node records use O((h+k)log(h+k)) bits; dense affine masks and row references can take O(h^2) additional bits, polynomial when k<=4h. A deterministic direct producer and checker are polynomial-time, with construction, local gadget checks, source parsing, output, checking, reserialization and live buffers charged separately from ideal q. The experiment's brute-force original source deletion witnesses cost up to O(h 2^{3h/2}) in this finite control and are NOT part of a purported all-input polynomial decider. No native FLMV instruction or simultaneous peak RSS was measured. No genuine historical private/exported-port or source-sensitive LOCAL-CV annotation was authenticated.

## Publication, role scope, remaining gap

Published code `experiments/arc/lspv3_504_multigadget_retraction.js`, raw `results/raw/arc/2026-11-08_0751_LSPV3_504_MULTIGADGET_RAW.json`, this report and role-owned handoff. Exact readback required; root main.tex untouched; five existing agents, 2A/3B allocation, native rule weights, task identities and schedules preserved.

The actual new result is simultaneous, **ALL k** original-source hardness transfer and matched binary source-capacity optimum in a DIFFERENT declared calculus. Its deliberately adverse conclusion is that even the fully expanded, published Resolution-hard expander family can have a linear explicit mixed refutation when RES clauses legally enter bounded AND3 factors. Historical [P2-D1] accepted-byte grammar and paid cross-type conversions, [P2-C3] all-native-rule normalization, [P2-B1] universal mixed minimum hardness, and [P2-B2] noncircular fixed-system B3 are **OPEN**. **P versus NP remains OPEN.**

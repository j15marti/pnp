# LSPV-1/436: Compact proper-3-CNF guard and a full mixed-rule linear source-work floor

**2026-11-05 22:26 PST | Route B, LSPV-1 lead.** PROVED/RESTRICTED ordinary Resolution projection and sound binary-premise source floor; CONDITIONAL native /341 mixed upper; COMPUTATIONAL finite controls. B1, B2, B3 and P versus NP OPEN. Independent specialist review pending.

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** reuse already-published LSPV-1/435 signed-literal projection on a smaller shared guard construction. Compared with the 3m-clause proper-3-CNF clause-split padding in /435, a shared four-clause negative guard might give 2m+4 proper clauses, preserve established Resolution hardness, and expose an all-mixed linear source floor.

**Four falsifiers:** (F1) Boolean projection or strict width-three syntax fails; (F2) any transformed source is dispensable although the original is clause-minimally UNSAT; (F3) proof projection requires a weakening step, duplicates a shared subproof, or adds depth; (F4) the known GF(2) shortcut cannot be reattached through accepted historical /341 rules. F1–F3 rejected by proof and finite replay; F4 remains conditional on native grammar/parser authentication.

**Prior work:** This is NOT a new signed-literal projection theorem. The full-DAG projection for literal identification is LSPV-1/435 (2026-11-05 22:08 PST; blob ffbb0928). The positive-guard unit isometry is /434. The original cubic Tseitin mixed minimum 4h-1 is LSPV-2/341 (blob c87acd11). This run's increment is the more compact UNSAT strict-3 construction and its all-source minimum-work accounting.

## Exact source and lower-bound-preserving map

For any proper signed 3-CNF $F=\bigwedge_{i=1}^m(a_i\vee b_i\vee c_i)$ over $n$ variables, introduce fresh $g,u,v$ and distinct private $y_i$. Define

$$
K(F)=\bigwedge_{i=1}^{m}
 [(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)]
\wedge\!\!\bigwedge_{\epsilon,\delta\in\{0,1\}}
 (\neg g\vee u^{\epsilon}\vee v^{\delta}),
$$

with $u^0=u,u^1=\neg u$, likewise $v$. Its **$2m+4$ clauses are all proper width three**; it uses $n+m+3$ variables after dense renumbering. The four last clauses force $g=0$, so $\exists g,y,u,v\,K(F)\iff F$ for each original assignment. More decisively the fixed source substitution

$$
\sigma(g)=\sigma(u)=\sigma(v)=0,\qquad
\sigma(y_i)=\neg a_i,\qquad\sigma(x_j)=x_j
$$

maps all first block clauses and all four pad clauses to tautologies, and every second block clause EXACTLY to the original source clause $a_i\vee b_i\vee c_i$. This is a genuine proof-complexity projection, not mere equisatisfiability.

**Theorem 436.1, PROVED/RESTRICTED.** For the globally minimum number of distinct paid ordinary strictly oriented shared-DAG Resolution inferences, with original source leaves free,

$$
\boxed{L_{\rm Res}(F)\le L_{\rm Res}(K(F))\le L_{\rm Res}(F)+2m+3.}
$$

The lower direction uses /435's proved signed-literal substitution/compiler, with Boolean-constant restriction. At each original inference its substituted image is either tautological, carries an already derived stronger parent, or is obtained through one genuine correctly oriented Resolution step. No weakening, uncharged split, ancestry loss or duplicated shared node is required. This works on the **whole arbitrary shared DAG**, not only individual chains. The reverse direction derives $\neg g$ with three RES nodes from the four pad clauses; for each i resolves on $y_i$ and then on g, recovering the original $C_i$ in two further RES nodes. Append any selected shared Resolution refutation of F, costing $2m+3$ additional paid nodes. Ideal parallel proofwise depths satisfy $D_{\rm Res}(F)\le D_{\rm Res}(K(F))\le D_{\rm Res}(F)+3$, with a simultaneous $(q+2m+3,d+3)$ uplift for any original proof of work q and span d. Physical TM work/space is separate.

**Theorem 436.2, PROVED/RESTRICTED source floor.** If F is clause-minimally UNSAT, K(F) is clause-minimally UNSAT. For any deleted block source i, use a model of $F\setminus\{C_i\}$ (which necessarily falsifies $C_i$), take g=0, satisfy other blocks with their private y choices, and set $y_i=0$ when the first clause is deleted or $y_i=1$ when the second is deleted. For deletion of a pad, use g=1 and choose u,v to falsify only the deleted pad, with every private y=0. Thus all $2m+4$ original clauses are **indispensable**. Any sound source-authenticated DAG calculus with zero-cost original leaves, positive paid distinct nodes and at most two antecedents per derived node obeys the standard connected-ancestry bound

$$
\boxed{W_R(K(F))\ge 2m+3.}
$$

This holds with all legal algebra, auxiliary definitions, temporary growth, reconvergence, and freely chosen optimal proof, provided sound source ancestry and binary fan-in remain fixed. It is LINEAR, not superpolynomial. It is not a theorem for a different system adding cost-free multisource or branch-discharge rules.

## Established hardness control and mixed shortcut

Odd-charge degree-three Tseitin contradictions on suitable connected bridgeless cubic expanders $G_h$ have $3h/2$ original edge variables and $4h$ proper signed 3-clauses, four per local XOR row. Source is UNSAT by summing vertex parities. Urquhart 1987 and Ben-Sasson/Wigderson 2001 supply $2^{\Omega(h)}$ ordinary shared-DAG Resolution hardness, for suitably expanding graph sequences only. Explicit indexed size is $\Theta(h\log h)$ bits. The original F_h is clause-minimally UNSAT on bridgeless cubic graphs. Consequently the derived K(F_h) has **$8h+4$ proper three-clauses, $11h/2+3$ variables**, remains $2^{\Omega(h)}$ Resolution-hard with a PROVED lower-bound preservation direction, and improves /435's old 12h-clause strict source.

The known LSPV-2/341 semantic mixed R_mix341 proof for F_h has $4h-1$ paid AND3/GF(2) nodes. Since RES is a declared historical native rule, the 3-node pad derivation and $2m=8h$ RES clause recoveries can precede that proof. Thus, **conditional on authentic native historical acceptance of the /341 local-factor and GF(2) interfaces**,

$$
\boxed{8h+3\le W_{R_{\rm mix341}}(K(F_h))\le 12h+2.}
$$

No shortcut was excluded from the minimum. This is an all-legal-rule LINEAR lower bound plus conditional linear upper, NOT an all-mixed superpolynomial result. Exported/private wires, defining-clause facet permissions, AND3, LOCAL-CONVERT, and historical byte grammar require further authentication.

## Executed finite tests and resource separation

Standard-library Python reused earlier published odd/even cubic-Tseitin **fixture generator**, but independently built K(F), source-bound shared Resolution proof, constant/literal proof projection, and exact satisfying clause-deletion witnesses. An independently written Node verifier replayed both whole proof DAGs with correctly oriented pivots and source identity, every one of K4's 36 deletion witnesses, the exact source substitution, and rejected five corruptions.

| original | F clauses | K clauses | K variables | exhibited K strict-RES nodes | projected F nodes | indispensable K clauses | conditional mixed bounds |
|:--|--:|--:|--:|--:|--:|--:|:--|
| K4 | 16 | 36 | 25 | 51 | 31 | 36 | 35 to 50 |
| K3,3 | 24 | 52 | 36 | 103 | 75 | 52 | 51 to 74 |
| Cube | 32 | 68 | 47 | 219 | 183 | 68 | 67 to 98 |

Python passed 3,728 assertions; independent Node passed 2,551, plus five negative corruptions rejected. The K4 strict-3 source is 384-byte DIMACS SHA256 bc669b8665a3ab0dcb132fbae71fdf5396b9dd3522cb616f0f669f1982ec2755. Source-bound K4 proof+projection JSON SHA256 4a6b92bb5679b016bbcac0d50f931d40a7d90a375b410cce41b7a116743b28a8. The exhibited 51-node strict K proof JSON is 37,896 bits and its 31-node F projection 20,320 bits, using the producer's compact representation. Python measured approximately 0.83s / 97184 KiB peak RSS, independent Node 0.03s / 28276 KiB. These are HOST readings, not same-machine complexity bounds. Executed full code and raw certificates reside in the reproducibility archive saved in the automation workspace; this GitHub report documents their checksums. No authoritative historical mixed checker was run.

## Actual searches and literature / repository scope

Read Nov 2 five-role governance handoff at historical commit 4e29ed76, current issue #3 including prior /435 (do not double-count), AGENTS.md (19656af1), CODEX.md (754999f5), project skill (b8df83a7); LSPV-1/434 and /435, LSPV-2/341, peer LSPV-3/438 and /439, LSPV-5 REFEREE377, actual Grok GROKPROOF/2026-11-06_0515_PROGRESS.md (93f9202d), actual Claude 2026-10-28_1521_ONETAPE-0001.tex (9a5b05d6). Reviewed primary Urquhart 1987, Ben-Sasson/Wigderson 2001 and Pich/Santhanam 2026 self-provability paper summaries, and Braun 2026 arXiv Res(XOR) scope. Targeted actual public repositories: konard/p-vs-np README 0e0ec77f and shared machine README 7ee9a11e; blkph0x/p-vs-np-proof-research METHOD_INDEX 18d693ea and affine theorem 4aba9d94; FRAT-XOR format.md 986a21aa; cake_lpr README e94f45e9; openai/math README cc5b0a03. No formal Lean replay, historical native /341 execution or direct Google-branded search. General web search and authenticated GitHub source reads were used.

Root main.tex returned existing blob 7b5243f9 with ZERO readable bytes, so it was not modified. No agents, schedules, timezones, titles, native weights or allocations changed.

**Remaining OPEN:** authenticate exact historical LOCAL-CONVERT / DEF facet and export interfaces; prove a superpolynomial minimum for every rule of SAME R_mix341; prove the noncircular B3 implication SAT in P => polynomial worst-case Wbar_R in that same R (without assuming proof certificates, arbitrary-decider correctness reflection, or the conclusion). B1=>B2=>B3, all OPEN. P versus NP OPEN.

## References

1. Urquhart, Hard Examples for Resolution, JACM 34 (1987), DOI 10.1145/7531.8928.
2. Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 48 (2001), DOI 10.1145/375827.375835.
3. Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8 (1976).
4. Pich and Santhanam, Towards P != NP from Extended Frege Lower Bounds, JACM 73(2) (2026), DOI 10.1145/3801091.
5. Braun, Bit Pigeonhole in Res(XOR), arXiv:2609.23015 (2026), proof-system-specific, specialist independent review not asserted.

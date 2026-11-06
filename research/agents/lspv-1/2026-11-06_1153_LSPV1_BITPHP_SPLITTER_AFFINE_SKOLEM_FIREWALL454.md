# LSPV-1/454 | Affine Skolem obstruction for strict-3CNF splitter chains

**November 6, 2026, 11:53 PST | Route B lead.** **PROVED/RESTRICTED**, exact six-row impossibility; **COMPUTATIONAL**, exhaustive bounded replay; **OPEN**, native historical R_mix341 hardness/grammar, B1/B2/B3 and P vs NP. Five role allocation (Route A 2/4; Route B 1/3/5), task schedules, rules, weights and ownership unchanged.

## IDEA -> SEARCH -> ITERATE

Hypothesis: a particular *affine-only clause-by-clause Skolem substitution* cannot eliminate the private splitter variables used by the established Braun bit-PHP -> proper-3CNF encoding. Four falsifiers: (F1) some affine section works; (F2) six source forcing patterns are invalid; (F3) no short nonlinear section exists; (F4) the local obstruction is wrongly promoted to arbitrary proof hardness. F1 and F2 fail by a six-row GF(2) contradiction; F3 fails by an explicit signed AND chain; F4 is explicitly outside the theorem.

Read 2026-11-02 governing refocus at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-1/452 and /453 (including actual `experiments/arc/lspv1_453_bitphp_er_compiler.py`), LSPV-3/427 Resolution branch lifting, LSPV-5/373 and /374 proposed CANON2R audits, Grok `GROKPROOF/2026-11-06_0515_PROGRESS.md`, Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`. The native historical /341 accepted-byte grammar remains unauthenticated. No authenticated full mixed proof is asserted.

Primary literature: Braun arXiv:2609.23015v2 (Nov 3, 2026) and Cook 1976 / Buss 1987 PHP shortcuts. Search of project for `affine Skolem splitter` and `nonfunctional splitter` found no exact indexed match (novelty not claimed). Required external review: `konard/p-vs-np/scripts/proof_status.json` SHA `93b77ed3d8fe456f81c690035f45f07910a247f2`, `konard/p-vs-np/proofs/complexity/README.md` SHA `7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md`; `meelgroup/frat-xor/format.md` SHA `986a21aa92b62f844ef1fce852193142c41b2b1f`; `peitl/short-proof/README.md` SHA `93d2090dba9739bc4983c65ea639a24e1f5e0fab`. Indexed web searches were used, not a separate Google-branded search.

## Exact source model

For any $k\ge4$, let $a_1,\dots,a_k$ be independently choosable original **literal-truth coordinates** (signs may be negative). Put $C_k=\bigvee_{i=1}^{k}a_i$. The standard chain of **proper width-three** clauses with private splitters $y_1,\dots,y_{k-3}$ is

$$
T_k=(a_1\lor a_2\lor y_1)\land
\bigwedge_{j=2}^{k-3}(\neg y_{j-1}\lor a_{j+1}\lor y_j)
\land(\neg y_{k-3}\lor a_{k-1}\lor a_k).
$$

For $k=4$ the middle conjunction is empty. Direct existential projection shows $\exists y\,T_k(a,y)\iff C_k(a)$, but many satisfying $a$ admit both $y_1$ values. Equisatisfiability does not supply unique definitions.

## Theorem 454.1 | all-k six-row obstruction

There is **no** affine map $f(a)=b\oplus\bigoplus_i c_i a_i$ over GF(2) for which **every** $a$ satisfying $C_k$ extends to some $T_k$-model with $y_1=f(a)$.

Proof: let $A=a_1\lor a_2$, $B=a_3\lor\cdots\lor a_k$. If $A=0$ and $B=1$, the first clause forces $y_1=1$. If $A=1$ and $B=0$, choosing $y_1=1$ would force all later splitters to 1 and make the final clause false; hence $y_1=0$. Write $e_i$ for the assignment with sole true coordinate $i$. The six **satisfying original assignments**

$$
e_3,\quad e_4,\quad e_3\oplus e_4,\quad
e_1,\quad e_2,\quad e_1\oplus e_2
$$

force output values $1,1,1,0,0,0$. Every affine function satisfies

$$
f(0)=f(e_i)\oplus f(e_j)\oplus f(e_i\oplus e_j).
$$

Thus the first triple forces $f(0)=1$ whereas the second forces $f(0)=0$. This is an exact inconsistency from six valid semantic constraints, **not** a native R_mix341 derivation. The argument remains valid if $f$ also mentions independent original variables outside this clause, by fixing those coordinates. QED.

**Tight nonlinear upper control:** choose

$$
y_1=\neg a_1\land\neg a_2,\qquad
y_j=y_{j-1}\land\neg a_{j+1}\quad(2\le j\le k-3).
$$

All $C_k$-models extend, and $k-3$ signed-AND2 gates suffice. Since $y_1=(1+a_1)(1+a_2)$ has degree 2, and affine (degree <=1) is impossible, the minimum algebraic degree of a polynomial Skolem **section for the first splitter** is exactly two. This compact choice is not a theorem asserting each original y-wire equals its selected function in all models.

## Application to an established hard family, with exact encoding ledger

Braun bit-PHP has $n=2^\ell$ holes, $n+1$ pigeons and $\ell$ binary address bits per pigeon. For every pair of pigeons and hole address, forbidding their shared value yields one $k=2\ell$-literal clause over their distinct address variables. There are $A=n\binom{n+1}{2}$ such wide clauses. LSPV-1/453 translates each into $2\ell-2$ proper 3-clauses with $2\ell-3$ fresh private splitter variables, producing

$$
S=A(2\ell-2),\qquad
V=(n+1)\ell+A(2\ell-3)
$$

and binary source length at most $O(S\log(V+2))$ under compact DIMACS numbering.

Braun v2 proves every unrestricted-DAG Res($\oplus$) refutation of the **original bit-PHP** has more than $\exp(n/(32768\ell^2))$ nodes for $\ell\ge32$. The standard calculus allows reused affine-disjunction clauses but **not arbitrary paid Boolean extension-variable rules**. Theorem 454.1 blocks *one affine local back-substitution tactic* for the 3-CNF splitter encoding; it does **not** prove a full proof-level backtranslation impossible. LSPV-1/453 supplies a polynomial ER-FACET original-3CNF-to-unary-PHP compiler under a **separate** declared calculus; Cook's polynomial ER PHP proof is a mandatory upper-bound control. None authenticates historical R_mix341.

Other hard-family controls: Haken unary PHP has exponential ordinary DAG Resolution lower bounds but polynomial Cook ER proofs, and cubic-expander odd Tseitin proper 3-CNF has exponential ordinary Resolution proofs but the declared mixed AND3/GF(2) shortcut of $4h-1$ nodes. Restricted lower bounds are not all-machine hardness.

## Independent finite checks and resource audit

The local Python producer enumerated all affine $f$ for $k=4,5,6,7,8$: exactly 32/64/128/256/512 candidates, **zero valid**. Independent Node.js checker enumerated all source patterns and private splitter assignments and verified the counts and independent valid failure witnesses: **1,554 assertions passed; four hostile forgery/malformed controls rejected**. The symbolic six-row contradiction was also checked for $k=4,...,20$.

| k | Models of $C_k$ | Candidate affine maps | Valid maps | Forced $y_1=1$ | Forced $y_1=0$ | Free |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 15 | 32 | 0 | 3 | 3 | 9 |
| 5 | 31 | 64 | 0 | 7 | 3 | 21 |
| 6 | 63 | 128 | 0 | 15 | 3 | 45 |
| 7 | 127 | 256 | 0 | 31 | 3 | 93 |
| 8 | 255 | 512 | 0 | 63 | 3 | 189 |

Python bounded computation was ~0.0143 seconds excluding startup/repository/search/publication; raw results are 8,785 bytes, the six-row witness 721 bytes, independent log 931 bytes. Actual machine time includes code parsing, file reads/writes, certificate production/verification, memory, failed requests and publication. This is a semantic lemma, not an R_mix341 proof DAG, so no invented logical node count, FLMV contraction, or all-algorithm lower bound is claimed. For a future translator, record output evidence bits, all-phase peak memory, lookup/recomputation and the exact inference acceptance grammar.

## Precise open arrows

A polynomial-cost, original-source-authenticated, **all-rule historical** R_mix341 normalization/simulation remains OPEN, including LOCAL-CONVERT, DEF facets and exported/private ports. Superpolynomial $\overline W_{R_mix341}$ under every legal shared/branching mixed derivation remains OPEN. B1/B2/B3, notably $\mathrm{SAT}\in P\Rightarrow \overline W_{R_mix341}(N)=N^{O(1)}$, remain OPEN. No new tasks/schedules/weights or main.tex edits: the current root blob has a SHA but returned zero readable text, so safe outside-byte preservation forbids touching it.

**Reference:** Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2 (Nov 3, 2026); Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution* (1976); Buss, *Polynomial Size Proofs of the Propositional Pigeonhole Principle* (1987).

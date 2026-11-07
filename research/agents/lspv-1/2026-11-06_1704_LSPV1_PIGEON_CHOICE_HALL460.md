# LSPV-1/460: All-degree Hall kernel, pigeon-choice Resolution refutation
**2026-11-06 17:04 PST, Route B Lead. PROVED/RESTRICTED; COMPUTATIONAL controls. P versus NP OPEN.**

## Idea, falsifiers, iteration
Hypothesis: a pigeon-first exhaustive choice tree over a Hall-deficient graph-PHP kernel compiles to *strict original-source Resolution*, improving the earlier Davis–Putnam $3^{3p}$ proof-work bound to $d^p$, without adding split/discharge/weakening rules. Falsifiers: omitted choice at an AND-join; free weakening or unauthorized inference; any unauthenticated source or inaccurate pivot; leakage of branch-local assumptions. The new proof avoids conditional assumptions completely: every node is an unconditional source consequence.

Read the exact published graph-PHP clauses in de Rezende, Nordström, Risse, Sokolov (TheoretiCS 2025, equations 1.1a–c, Cor. 4.7) and generalized the initial cubic proposal to left degree $d\ge3$. Their exponential lower bound is **ordinary shared-DAG Resolution** for selected sparse graph families, not for all graph-PHPs or fixed mixed R_mix341. Source definitions come from the journal, not from the finite generated controls.

## Exact strict 3-CNF source
For each pigeon $i$, let its distinct ordered neighbors be $j_1,\ldots,j_{d_i}$, $d_i\ge3$, and use edge variables $x_{ij}$. Its wide pigeon clause is $\bigvee_{j\in N(i)}x_{ij}$. For $d_i>3$ convert this clause using globally fresh private splitters $y_{i,1},\ldots,y_{i,d_i-3}$ into
$$
(x_{i,j_1}\vee x_{i,j_2}\vee y_{i,1}),\quad
(\neg y_{i,t-1}\vee x_{i,j_{t+1}}\vee y_{i,t})\;(2\le t\le d_i-3),\quad
(\neg y_{i,d_i-3}\vee x_{i,j_{d_i-1}}\vee x_{i,j_{d_i}}).
$$
For $d_i=3$, retain the pigeon clause. Each binary hole collision $\neg x_{ij}\vee\neg x_{kj}$ becomes two original strict3 clauses using a private $z_{ikj}$:
$$
(\neg x_{ij}\vee\neg x_{kj}\vee z_{ikj}),\qquad
(\neg x_{ij}\vee\neg x_{kj}\vee\neg z_{ikj}).
$$
For *functional* PHP also add the equally padded per-pigeon negative functionality clauses. The proof below uses only the common pigeon/collision subformula. With $B=\sum_j\binom{\deg(j)}2$, the basic strict3 source has $\sum_i(d_i-2)+2B$ clauses and $|E|+\sum_i(d_i-3)+B$ variables. Equisatisfiability does NOT imply preservation of any published lower bound.

## Theorem 460.1, PROVED/RESTRICTED
For a Hall-deficient subset $S$ with $h=|N(S)|<|S|$, select $p=h+1$ pigeons and $d=\max_{i\in S'}d_i\ge3$. A strict, unconditional, source-authenticated ordinary-Resolution refutation DAG exists with
$$
W_{\rm RES}(F)\le\sum_{i\in S'}(d_i-3)+\sum_j\binom{\deg_{S'}(j)}2+
\frac{d(d^p-1)}{d-1}
\le p(d-3)+d\binom p2+\frac{d(d^p-1)}{d-1}.
$$
Unit critical-path depth is at most $dp+\max(d-3,1)$ in the explicitly ideal unlimited-processor parallel model.

**Proof.** Recover each original pigeon disjunction by $d_i-3$ correctly oriented Resolution steps on its splitters and recover each collision by one Resolution on the two private-pad clauses. Recursively analyze every one of the at most $d$ *choices* for the next pigeon. At each partial tuple $\sigma$ derive an unconditional negative clause $C_\sigma$ contained in the negations of the selected edges. A duplicate-hole choice gives an authenticated collision clause. Otherwise each child returns $C_{\sigma j}\subseteq C_\sigma\cup\{\neg x_{i,j}\}$. Resolve the recovered pigeon disjunction against all the children containing the negative pivot; if a child omits the pivot, return that already stronger clause without weakening. At depth $p$, Hall deficiency guarantees a collision on every choice path. Thus the empty tuple yields the empty clause. There are at most $(d^p-1)/(d-1)$ internal vertices, at most $d$ paid Resolution nodes per vertex, and at most $d\binom p2$ collisions. Sharing can only reduce the paid-node union; no branch-local conclusion is reused as an unconditional lemma. QED.

At $d=3$, the generic bound improves from $3\binom p2+3^{3p}$ (previous LSPV-1/459 DP) to $3\binom p2+\tfrac32(3^p-1)$. If $p\log d=O(\log N)$, the ideal RES minimum has polynomial *upper* bound in original source bits $N$. Detecting/authenticating the Hall witness is separate charged algorithmic work. The bound also constrains the minimum size of Hall kernels in any graph family certified exponentially Resolution-hard, including the 2025 FPHP families. It supplies **no** all-mixed lower bound, SAT time lower bound, or B3 proof.

## Actual source-authenticated finite controls
| source | pigeons/holes; degree | clauses/vars | paid RES: rows + collisions + branch | unit span |
|---|---|---|---|---|
| Hall 012,013,023,123,012 | 5/4; 3 | 47/36 | 105=0+21+84 | 13 |
| duplicate 012 | 4/3; 3 | 40/30 | 66=0+18+48 | 10 |
| six pigeons/five holes | 6/5; 3 | 54/42 | 147=0+24+123 | 15 |
| degree-four six/five | 6/5; 4 | 104/76 | 596=6+46+544 | 19 |

Independent JavaScript source regeneration, SHA verification, exact pivot/result verification, acyclicity and root-ancestor checks: **75,414 assertions PASS**, 52 hostile controls rejected. Additional seeded stress: 60 Hall cases, 7,122 checked paid nodes. Four/4 SAT control: nine injective choices. Host metrics: Python four-fixture producer 0.73s and 97,548 KiB peak RSS; independent Node verifier 0.05s and 34,268 KiB; stress 0.77s and 97,432 KiB. These are implementation measurements, not FLMV bounds. No root source or branch assumption is freely inferred.

## Evidence and limitations
Reviewed the five-role Nov. 2 handoff, current issue #3, AGENTS/CODEX/repository skill, LSPV-1/459, LSPV-3/461, LSPV-5/REFEREE396, real GROKPROOF and Claude files. Required external repository reads: konard/p-vs-np proof_status.json SHA 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693ea; meelgroup/frat-xor format.md SHA 986a21aa; openai/math directory. The latter provide no B3 transfer. The primary paper was inspected, including its PDF rendered page. No distinct Google service. Exact historic R_mix341 accepted-byte RES/DEF/LOCAL grammar and full source-to-mixed production checker remain unverified. Root main.tex fetched blob SHA d48dd0fb but content was empty; it was **not** edited. Full Python producer, independent Node verifier, original CNFs, JSON proof DAGs, raw stress controls and checksum manifest are in the separately generated reproducibility archive.

**OPEN:** Superpolynomial $\overline W_{R_{\mathrm{mix341}}}$ over every native mixed rule; noncircular same-calculus B3 ($\mathrm{SAT}\in P\Rightarrow\overline W_R=N^{O(1)}$); B1/B2; P versus NP.

[1] de Rezende et al., *Exponential Resolution Lower Bounds for Weak Pigeonhole Principle and Perfect Matching Formulas over Sparse Graphs*, TheoretiCS 4 (2025), art.9, DOI 10.46298/theoretics.25.9: https://theoretics.episciences.org/15419/pdf
[2] Davis–Putnam, JACM 7 (1960), 201–215 (prior DP bound).
[3] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8 (1976), 28–32 (shortcut control).
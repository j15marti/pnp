# LSPV-5/423 independent referee: duplicate-free Pang transfer and exact formal-encoding overhead

**Pacific timestamp:** 2026-11-07 18:43  
**Role:** LSPV-5 independent red team, Route B primary  
**Tracker nodes:** `[P2-B3]`, new evidence node `[P2-L5-423]`  
**Status:** **PROVED/EXACT** elementary representation lemmas; **PROVED-RESTRICTED / CONDITIONAL** B1 consequence for a distinct fixed proof calculus; historical $R_{\mathrm{mix341}}$, B2, B3 and P versus NP remain **OPEN**.

## IDEA: falsifiable target before search

Initial hypothesis: the newest LSPV-3 private-wire theorem might still permit two copied private wires to alias one public output, invalidating source retraction.

Precise falsifiers stated before search:

1. the declared grammar requires each copied output ID to be globally fresh and pairwise distinct;
2. the latest peer theorem proves injective source-to-public output correspondence, not merely fresh syntax;
3. exhaustive accepted-byte witnesses reject every attempted alias; or
4. the issue is irrelevant to all current tracker dependencies.

Search falsifier 1 occurred: `[P2-L3-487]` explicitly works in a declared distinct-output `DEF_AND+RES` grammar. The initial idea therefore did not attack that restricted theorem. I revised the target to LSPV-1/492's new conditional B1 evidence, asking whether Pang's with-replacement random formulas are represented faithfully by the formalized `Finset` CNF encoding and whether unary literal codes hide superpolynomial input length.

## SEARCH: actual sources, versions and scope

The governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, current issue #3, `AGENTS.md` (`19656af1`), `CODEX.md` (`754999f5`), the project skill (`b8df83a7`), both current trackers `proof1.txt` (`96aefb3d`) and `proof2.txt` (`9a3566f6` at the final prewrite fetch), LSPV-1/492 (`73018cc7`), LSPV-3/487, and the actual peer program `experiments/arc/lspv1_492_subexp_b1_firewall.js` (`4b671264`) were read. Exact node IDs were taken from the trackers, not reconstructed from chat.

Primary/repository evidence actually inspected:

- Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837, especially the definition of $F(n,w,\Delta n)$ and Theorem 7.2(a). This is a recent preprint, not treated as an all-algorithm theorem.
- `openai/math` at `4eaee87548250b2682affda7d05d947c05554bae`: `lean/ComparatorChallenges/SubexponentialSAT.lean` (`a8d5ff3a...`), `lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean`, and `lean/docs/378.md` (`223bbe...`). The challenge file ends in `sorry` by design; the proof theorem is in `Final.lean`.
- `unaltuzun/exponential-time-hypothesis-verify` at `a775e22...`: `VERIFICATION.md` and `docs/REPORT.md`. It reports a kernel build at OpenAI commit `7ef5c0...`, standard axioms only, and Comparator acceptance. The statement/proof/doc blobs relevant here are unchanged at the current OpenAI head. This is third-party evidence, not my local execution.
- `anthropics/formal-math` at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`: `eth/MainResults.lean` and `eth/Solution.lean`; inspected as a cross-check, not as a substitute for the OpenAI theorem used below.
- Required repository deltas: `konard/p-vs-np` remains at `ecedd2b45...`; its issue-568 material still labels residual sharing conjectural. `blkph0x/p-vs-np-proof-research` remains at `7dedc73f...`; `INDEPENDENT_AUDIT.md` and `PUBLIC_METHOD_REVIEW.md` retain explicit counterexample/claim boundaries. Neither supplies this transfer or historical-$R_{\mathrm{mix341}}$ B3.
- Rotating proof-checker corpus: `meelgroup/frat-xor` at `18cd6bc1...` and `tanyongkiam/cake_lpr` at `033aad53...`. They support authenticated checking, not proof discovery or this asymptotic bridge.
- Current project critiques: `GROKPROOF/2026-11-08_0118_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`). Both keep unrestricted transfers open.

Actual indexed queries included Pang `F(n,w,Delta n)` / Theorem 7.2, the OpenAI exact-count theorem, and independent kernel replay. A separate Google-branded interface was unavailable; I used the available indexed research search and direct GitHub files. I did not execute Lean, Comparator, Pang's proof, or the authoritative historical $R_{\mathrm{mix341}}$ checker.

## Established-family ledger

| Field | Exact record |
|---|---|
| Family | $F(n,3,8n)$: $m=8n$ clauses sampled independently and uniformly with replacement from the $M=2^3\binom n3=8\binom n3$ proper width-3 clauses on $n$ variables. |
| 3-CNF encoding | Each clause has three distinct variables and one sign per variable. For the duplicate-free subfamily below, sorting into OpenAI's `Finset (Finset Literal)` loses no clause occurrence. |
| Size parameter | $n$ variables, $m=8n$ clauses; Pang proof size counts nodes in a syntactic proof DAG. OpenAI encoded length satisfies $L\le192n^2+129n+2$. |
| Published theorem | Pang Theorem 7.2(a): for fixed prime $p$, fixed $r\ge1$, fixed $w\ge3$ and $\Delta\ge2^w$, $F(n,w,\Delta n)$ a.a.s. needs $\exp(\Omega_{p,r}(n))$ size in $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$. |
| Model/rules | Restricted `Res(PC_r/F_p)` proof DAG, not arbitrary algorithms and not historical $R_{\mathrm{mix341}}$. |
| Known shortcut/control | The formalized fixed-$k$ exact counter is a legal algorithmic upper-bound control with time $(L+1)^{O_k(1)}2^{O_k(n(\log\log n)^2/\sqrt{\log n})}$ and polynomial visited tape space. Algebraic/extension shortcuts remain allowed in the respective calculus. |
| Remaining transfer | No lower bound across every native rule of historical $R_{\mathrm{mix341}}$; no noncircular B3 for that same fixed calculus. |

Certified UNSAT/proof-size hardness/solver behavior are distinct here: Pang supplies a probabilistic restricted proof-size lower bound for UNSAT formulas. This run did not generate a DRAT/FRAT certificate or benchmark empirical SAT-solver difficulty.

## ITERATE: exact repair

### Lemma 423.1 (duplicate-free hard subsequence)

Let $D_n$ be the event that at least two of the $m=8n$ independently sampled clauses coincide. A union bound gives

$$
\Pr[D_n]\le \frac{\binom{8n}{2}}{8\binom n3}
=\frac{3(8n-1)}{(n-1)(n-2)}
\le \frac{48}{n}\qquad(n\ge6).
$$

The last inequality is equivalent to $24n^2-141n+96\ge0$, which is strict for $n\ge6$. If $H_n$ is Pang's hard event, $\Pr[H_n]=1-o(1)$, then

$$
\Pr[H_n\cap\neg D_n]\ge1-o(1)-O(1/n)=1-o(1).
$$

Therefore infinitely many Pang-hard instances contain no duplicate clause. They embed exactly into the formalized `Finset` CNF. No unsupported claim that arbitrary deduplication preserves proof hardness is needed.

### Lemma 423.2 (exact unary/framing overhead)

In the inspected OpenAI encoder, `encodeNat q` has length $q+1$; a literal code is at most $2n-1$, so each encoded literal has length at most $2n$. `frame` maps $r$ bits to $2r+1$ bits and each list element adds one tag bit. Thus a three-literal clause consumes at most

$$1+3(2(2n)+2)=12n+7$$

bits as an inner list, and each outer clause consumes at most $2(12n+7)+2=24n+16$ bits. Including the final list terminator and the $n+1$-bit variable-count prefix,

$$
L\le n+2+m(24n+16).
$$

At $m=8n$, $L\le192n^2+129n+2$. Hence the theorem's polynomial factor $(L+1)^d$ is $2^{O(\log n)}$, and the formalized time bound remains $2^{o(n)}$ on this family.

### Restricted conditional B1 consequence

Assume the inspected formal theorem and Pang's cited theorem at their stated scopes, and fix the distinct source-authenticated calculus whose paid cost is polynomially related to Pang's DAG node count. On the duplicate-free hard subsequence, the decider time is $2^{o(n)}$ while proof cost is $2^{\Omega(n)}$. Any B1 polynomial $p_A$ would imply

$$W_R(F_n)\le p_A(|F_n|+T_A(F_n))=2^{o(n)},$$

contradicting $W_R(F_n)=2^{\Omega(n)}$. This is a conditional B1 failure for that **distinct restricted calculus**. It is neither a B2/B3 result nor a lower bound against the decider. It does not transfer the lower bound to historical $R_{\mathrm{mix341}}$.

Independent challenge: the repair would fail if the hard event were only supported on formulas with many repeated clauses, if the formal encoding grew exponentially, or if the proof-cost metric were not polynomially related to Pang's DAG size. Lemmas 423.1--423.2 remove the first two possibilities; the precise calculus/weight identification remains an explicit premise.

## Executed verification and resource ledger

- Peer replay: 297 checks passed from `lspv1_492_subexp_b1_firewall.js` (140 strict-3-CNF samples, SAT/UNSAT controls, six malformed rejections). Its own label correctly says no Lean replay.
- Python producer: 40,030 checks passed, including exact rational bounds for $3\le n\le10{,}000$, direct clause-universe enumeration for $3\le n\le9$, exact encoder reconstruction, duplicate canonicalization, SAT/UNSAT and malformed controls.
- Independent Node/BigInt verifier: 30,021 checks passed with independently implemented fractions and encoder.
- Logical nodes: no $R_{\mathrm{mix341}}$ node, rule or weight changed. Evidence bits are the two compact programs and raw JSON. Construction/search time, parser time, repository reads, output and verification are ordinary host costs; no proof-search cost was hidden inside $W_R$.
- Space/span: scripts used ordinary host memory; no FLMV-machine or parallel-span claim. No large certificate was retained, no shared proof was double-counted, and no branch-local lemma was reused across assumptions.

## Tracker decision, actual advance and remaining gap

Material evidence changed for `[P2-B3]`: the representation and bit-length objections to LSPV-1/492's restricted conditional B1 argument are discharged by Lemmas 423.1--423.2. Add `[P2-L5-423]` as a dependency/evidence note. `[P2-B1]`, `[P2-B2]`, `[P2-D1]`, `[P2-C3]` and historical-$R_{\mathrm{mix341}}$ B3 remain **OPEN**. `proof1.txt` has no material change.

**Actual advance:** a duplicate-free hard subsequence and exact $O(n^2)$ formal encoding are proved.  
**Verification:** 70,051 new independent checks plus 297 peer checks; no Lean/Pang replay.  
**Precise remaining gap:** a full all-native-rule lower bound and a noncircular same-calculus B3 bridge for the fixed historical $R_{\mathrm{mix341}}$.  
**P versus NP remains OPEN.**

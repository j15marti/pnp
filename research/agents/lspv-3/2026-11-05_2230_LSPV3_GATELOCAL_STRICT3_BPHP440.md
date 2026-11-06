# LSPV-3/440: Gate-owner LOCAL translation on strict 3-CNF bit-PHP

**November 5, 2026, 22:30 PST | Route B primary. PROVED/EXACT in an explicitly declared GATE-LOCAL grammar, COMPUTATIONAL independent finite replay, historical R_mix341 acceptance OPEN. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** If the paid conservative DEF relation is eligible as a *single local-factor antecedent* for paid LOCAL-CONVERT, all three standard Boolean defining-clause facets can be recreated without owner-qualified direct facet selectors. Four falsifiers: (1) any one of eight local assignments violates the facet implication, (2) nested gates or shared RES dependencies fail reconstruction, (3) strict-3 source bytes, DEF freshness, or source ancestry are wrong, (4) the historical /341 grammar does not allow DEF-owner-to-LOCAL inputs. The first three were rejected by proof and independent finite verification. **Falsifier 4 is unresolved:** it is a typed-interface question, not a question that a truth table can decide.

**Corpus/duplication audit:** Read original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11`, LSPV-3/412, /435, /436 and /439, LSPV-5/REFEREE378 blob `2223e878`, governing five-role handoff, current issue #3, AGENTS.md, CODEX.md, project skill, actual Grok REWIRE and Claude ONETAPE files. Prior /435 already establishes paid bounded-local conversions; /436 distinguishes direct facet grammar acceptance; /439 derives unary premises from bit-PHP using FACET-A; REFEREE378 independently reconstructs proper strict-3 sources. Those are **not** new claims here. New work is the *proofwise* alternative interface with exact paid overhead and independently replayed strict-source certificate family, plus the all-size strict-source essentiality proof below.

Targeted external files: Braun [1], `konard/p-vs-np/proofs/experiments/np_subset_p_proof_attempt.md` blob `f07e4821` (SAT-polynomial-machine obligation OPEN); `blkph0x/p-vs-np-proof-research/PROOF_PORTFOLIO_BRIDGE_REPORT.md` blob `22215cec` (bounded extraction only); `meelgroup/frat-xor/format.md` blob `986a21aa` (XLRUP, not historical /341); `tanyongkiam/cake_lpr/README.md` blob `e94f45e9`; and `peitl/short-proof/README.md` blob `93d2090d`. Authenticated github.com/openai search found `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`, not a proof-grammar compiler. ABC/mockturtle code searches concern circuit rewriting, not /341. General web was used; direct Google-branded search was unavailable. Local `git ls-remote` failed DNS. All failures are recorded.

## Established hard family, exact 3-CNF, source theorem

For `ell >= 2`, put `n = 2^ell`, `m=n+1` and Boolean address bits `b_(i,t)`. The bit-PHP clause for pair `i<j` and address `a` is

$$
C_{ij,a}=\bigvee_{t=1}^{\ell}[b_{it}\ne a_t]\ \vee\ \bigvee_{t=1}^{\ell}[b_{jt}\ne a_t].
$$

There are `M=n*binom(m,2)` width-`2ell` clauses and `m ell` source variables; the formula is UNSAT by pigeonhole counting. Braun [1], revised October 22, 2026, reports a Lean-linked lower bound `> exp(n/(32768 ell^2))` for `ell>=32` against unrestricted *shared-DAG Res(XOR)* with semantic weakening but **no extension axioms**. Independent peer review is not assumed. The result does **not** apply automatically to strict-3 conversion or the full mixed calculus.

Use the standard private signed chain to split each width-`k=2ell` clause `(l1 ... lk)` into `k-2` proper 3-clauses:

$$
(l_1\vee l_2\vee w_1),\qquad
(\neg w_t\vee l_{t+2}\vee w_{t+1})\ (1\le t<k-3),\qquad
(\neg w_{k-3}\vee l_{k-1}\vee l_k).
$$

Each old wide clause is reconstructed by exactly `k-3` paid oriented RES steps. Strict 3-CNF sources have **`S=M(2ell-2)` clauses** and **`V=m ell + M(2ell-3)` source variables**. Definition outputs are allocated strictly above `V`. This is an **upper-bound lifting** direction, not a Res(XOR) lower-bound-preserving theorem.

## Exact conditional gate-owner-to-LOCAL lemma

Define a distinct *GATE-LOCAL* grammar: a charged, globally fresh conservative two-input AND-DEF node carries the exact three-variable factor `z <=> (A & B)`; one paid LOCAL-CONVERT may take **that DEF owner factor** as its unary antecedent if a complete three-variable truth table establishes the conclusion. Direct RES references to a DEF facet are forbidden. In this declared grammar the three clauses

$$
(\neg z\vee A),\quad(\neg z\vee B),\quad(z\vee\neg A\vee\neg B)
$$

are each derived by **one paid LOCAL** from the same owner, since the exact gate factor implies each on all eight Boolean valuations. For any source-authenticated FACET-A proof DAG with `D` paid AND definitions, `R` paid RES nodes, and only these three defining facets, replace each facet use with one such paid LOCAL and replay every downstream RES node unchanged. Result: **at most `D+3D+R` paid nodes**, preserving distinct-node sharing, acyclicity, names, source hashes, and assumption scopes. The owner may itself depend on other globally fresh earlier gates. This statement is conditional on the explicit parent typing. If historical LOCAL cannot read DEF relations, the conversion is **not** native.

Combining the prior /439 decoder and REFEREE378 strict3 source reconstruction gives exact *exhibited work deriving all unary PHP premises*:

$$
\boxed{W_{pre,GL}=M(4\ell-3)+m(2n\ell+6n-21).}
$$

Here `D=m(2n-4)`, RES includes the strict-source chains, and the extra `3D` LOCAL nodes are paid. Relative to the `S` source clauses,

$$
W_{pre,GL}/S=2+\frac{1}{2\ell-2}+O(2^{-\ell}).
$$

This is **not a complete empty-clause certificate or a global minimum**. Cook/Buss ER/Frege PHP shortcuts remain upper-bound controls; no polynomial *historical* /341 refutation is asserted.

**Nondegenerate-gate qualification:** The compiler theorem and its three-facet accounting as verified here require each AND gate's two signed inputs to name **distinct underlying variables** and its output to be globally fresh, as in every bit-PHP prefix gate. For repeated or complementary occurrences of the same variable, individual facets can become duplicates or tautologies; the historical acceptance and any canonicalization cost are not established by this run.

## New all-size indispensable-source lemma (independent of gate grammar)

**PROVED/EXACT:** Every one of the `S` private-chain strict-3 source clauses is individually indispensable. Remove the chain clause `t` belonging to old `C_(i,j,a)`. Assign pigeons `i,j` the same hole `a`, inject all other `n-1` pigeons into the other `n-1` holes. Exactly `C_(i,j,a)` is falsified among the wide sources. For every true old clause set its private `w_r=1` exactly when its first `r+2` literals are all false. For the one false old clause choose `w_r=1` exactly when `r<t`. Every strict source clause except the removed one is now satisfied. Thus every source is essential. Any sound, conservative, unit-cost **at-most-binary-premise** refutation DAG must depend on all `S` sources, so the standard connected fan-in argument yields

$$
\boxed{W_R(\mathrm{Chain}_3(\mathrm{BPHP}))\ge S-1.}
$$

This only gives a **linear** generalized proof-work lower bound and does not transfer Braun's restricted proof hardness or imply machine time.

## Verification and resources

The archive contains a complete Python proofwise translator, independent Node checker, original /439 inputs, both strict-3 typed topological proof DAGs, exact source hashes and SHA manifest. The Node checker reconstructs the source without importing the producer, checks every DEF/LOCAL/RES rule, all output unary clauses, every source ancestor, **every one-clause-deletion SAT witness**, and hostile mutations. It does **not** execute an authoritative historical checker.

| ell | clauses S | vars V | DEF | LOCAL | RES | paid pre-work | ideal span | source bytes | typed trace bytes | Node assertions |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 80 | 50 | 20 | 60 | 215 | **295** | 6 | 868 | 36,026 | 7,114 |
| 3 | 1,152 | 891 | 108 | 324 | 2,835 | **3,267** | 10 | 15,423 | 453,073 | 375,386 |

Hostile controls **13/13 rejected**. Source deletion SAT controls **80/80, 1,152/1,152**. Every 375 / 4,419 serialized proof node is in the union of unary-premise dependency subgraphs. Original strict source SHA256: ell2 `13361aa6164d76373ac8d4b4b6935f05257bb99266441f3405cfeecb653da6a6`, ell3 `27f97b3a3c906b2858769ad9e9d691dfd95002852c5f99febf01e21f11c3bd9d`.

Observed Linux-host translator: 0.87 seconds wall, 100,616 KiB maximum RSS; independent Node replay: 0.26 seconds wall, 56,448 KiB maximum RSS. Not FLMV model bounds. Implemented algorithms pay acquisition, all parsing/hash/checking, output, full reference bits, cache, storage, recomputation and simultaneous peak `O(E_old+E_new+N)` for a materialized translation; the offline proof minimum excludes derivation discovery by design. Logical work is not physical time, and critical-path depth assumes unlimited parallel resources.

**OPEN:** authentic native DEF-owner-to-LOCAL type, direct facet selectors, private/exported wires, high-width GF(2)/AND3 mixed-DAG normalization, noncircular same-calculus B3, superpolynomial full mixed `Wbar_R`, and P versus NP. Root `main.tex` fetch returned SHA `7b5243f9` but zero readable bytes; deliberately not overwritten. Exactly five agent roles, 2A/3B allocation, schedules, weights and ownership unchanged.

## References

[1] K. Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015 (revised October 22, 2026), https://arxiv.org/abs/2609.23015 .

[2] S. Buss, *Polynomial size proofs of the propositional pigeonhole principle*, JSL 52 (1987), 916-927.

[3] S. Cook, *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8 (1976); S. Cook and R. Reckhow, *The relative efficiency of propositional proof systems*, JSL 44 (1979).
# LSPV-2/472 | Exact source-blind INDEX snapshot threshold and FLMV model qualification

**2026-11-07 09:17 PST | LSPV-2 Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Initial idea.** Could replacing the LSPV-2/468 dense and LSPV-4/469 canonical WORK-backed guest INDEX representations with an optimal lossless code restore a universal low-WORK guest interpreter? Hypothesis: source-independent faithful encoding of every $k$-one INDEX state of span $H$ might use $o(k\log(H/k))$ WORK bits. This is one representation strategy, **not** the universal solver-dependent $A\mapsto\Phi(A)$.

**Falsifiers stated before search:** (F1) the original FLMV text expressly exempts INDEX payload from all space charges; (F2) an injective fixed-width representation of $\binom Hk$ distinguishable states uses fewer than $\lceil\log_2\binom Hk\rceil$ bits; (F3) combinadic ranking fails to give a bijection; (F4) a source-aware/code-aware compiler can regenerate or avoid the state and thereby escape the source-independent hypothesis. F2/F3 are false by proof and exhaustive test; F4 is a **valid exception**, so the theorem must NOT be generalized to all SAT deciders. F1 is not authenticated by FLMV section 2.1.

**Current project review:** Read both complete proof trackers (initial blobs proof1 `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 `e8767e8771afba510f8984569197aea12dbed022`), issue #3, November 2 five-role handoff (`c3889a3e`), AGENTS.md (`19656af1`), CODEX.md (`754999f5`), .codex skill (`b8df83a7`), LSPV-2/471 (`acde2a98`), peer LSPV-4/472 (`977c9f1a`), actual Grok `GROKPROOF/2026-11-07_1220_PROGRESS.md` (`2c450bb3`) and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6`). This is an exact continuation of peer LSPV-4/472's dense-state information control, not an independently new general bound.

**Literature and GitHub inspected:** FLMV, *Time-Space Lower Bounds for Satisfiability* (JACM 52, 2005), section 2.1, printed p.4, source https://lance.fortnow.com/papers/files/tst.pdf (read text and PDF image). It says INDEX contents/head positions occur in configurations and each configuration has size $O(s)$, but does not specify an unambiguous standalone INDEX charge. LSPV-2/471's claim that this paragraph *expressly declares* INDEX free must therefore be retired as an unconditional FLMV interpretation. Classical combinatorial number-system ranking and counting are prior art (Lehmer/Knuth; https://arxiv.org/abs/1601.05794). Searched both required external repositories and inspected `konard/p-vs-np/README.md` (blob `0e0ec77f`), `proofs/complexity/README.md` (`7ee9a11e`), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (`18d693ea`), `affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md` (`4aba9d94`), `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` (`4bb5fd19`), `meelgroup/frat-xor/format.md` (`986a21aa`), `openai/math/README.md` (`cc5b0a03`). These are restricted methods or differently specified models; none proves the FLMV contractor. Public research search used; separately branded Google and a native FLMV executable were unavailable.

## Theorem 472.1 (PROVED/RESTRICTED): exact source-independent fixed-width snapshot cost

Fix $H\ge1$, $0\le k\le H$, an INDEX head location, and public integers $H,k$. There are exactly $\binom Hk$ binary INDEX tape patterns of length $H$ with $k$ one-cells. Suppose a source-independent **fixed-width** snapshot in charged WORK bits must preserve all these patterns and permit every later INDEX-bit observation, with no retained native INDEX copy, source rereads or uncharged regeneration. It must be injective; hence

$$
m\ge\left\lceil\log_2\binom Hk\right\rceil.
$$

This *information-bit* lower bound is sharp. Given occupied coordinates $0\le p_1<\cdots<p_k<H$, the classical colex combinatorial-number-system rank

$$
r(p_1,\ldots,p_k)=\sum_{j=1}^k\binom{p_j}{j}
$$

bijects the patterns with the integers $0,\ldots,\binom Hk-1$. Binary rank storage uses precisely $m=\lceil\log_2\binom Hk\rceil$ fixed bits. This does **not** prove cheap dynamic ranking, source access, random-bit retrieval, or native work/index time.

For $1\le k\le H/2$:

$$
m\ge k\log_2(H/k),
$$

since $\binom Hk\ge(H/k)^k$. For $k=\lfloor H/2\rfloor$,

$$
m\ge H-\log_2(H+1)
$$

because $\binom H{\lfloor H/2\rfloor}\ge2^H/(H+1)$.

**Scope:** Fixed-width and source-independent are essential. Variable-length descriptions have a different additive bit convention; uncharged retained native INDEX, reconstructibility from the source, a code-aware shortcut, and charged recomputation bypass this exact snapshot premise. The theorem is independent of the still-ambiguous exact original FLMV INDEX-space metric. It is a quantitative representation-cost control, **not** a machine-independent SAT lower bound or a no-go for $A\mapsto\Phi(A)$.

## Established hard-family / encoding / shortcut ledger

On a connected simple cubic expander with $H$ vertices and odd charge, the directly encoded strict-proper signed 3-CNF Tseitin formula has $3H/2$ edge variables, four local forbidden-parity clauses per vertex ($4H$ total), and $N=\Theta(H\log H)$ encoded bits. Odd charge certifies UNSAT. Urquhart 1987 and Ben-Sasson/Wigderson 2001 (Theorem 4.4/Corollary 4.5, https://doi.org/10.1145/375827.375835) prove exponential **ordinary shared-DAG Resolution** lower bounds for suitable expander sequences. GF(2) elimination gives a polynomial shortcut and the project reports $4H-1$ declared-semantic AND3/GF2 nodes, subject to the native accepted-grammar distinction. The K4 parity tests are finite label controls, not asymptotic hardness certificates. No reduction from outside 3-CNF or illicit split/discharge rule is used.

## Verification and all-phase costs

Independent Python producer (host language): all $2^H$ states, every $1\le H\le14$; **32,766 subsets and 131,420 assertion groups**, direct combinadic rank, greedy unrank, exact $m$, plus large-$H$ exact binomial illustrations and 16 signed K4 3-CNFs (eight SAT/eight UNSAT), five malformed controls. Independently written JavaScript verifier: **16,382 subsets, 17,526 assertions**, independent increasing-mask ordinal enumeration, 16 K4 parity checks. Both passed. Host-language enumeration is not native FLMV execution.

Explicit evidence-bit floor: $m$ above. An upper code exists with that many bits, but computing/maintaining it, source/index/head reads, construction, failed strategies, cache, recomputation, verification, and any full simulator time or simultaneous WORK/INDEX peak remain **OPEN**. The proof has no charged $R_{\rm mix341}$ inference nodes: Route B's shared AND/OR proof-DAG calculus and original weights were not modified.

## ITERATE and remaining proof obligations

Optimal source-independent compression fails to rescue dense INDEX states: $m=H-O(\log H)$. For sparse states it is *offline* information-optimal, but dynamic access is not yet paid. The next genuine alternatives are a source-aware regenerating transducer, a direct native INDEX-to-INDEX implementation under the **authenticated** metric, or safe guest-code-aware simplification. Those strategies remain legal and unexcluded.

**Node IDs:** [P2-A4] INDEX/WORK transfer OPEN and conditional model; [P2-A2] solver-dependent all-input adaptive acquisition OPEN; [P2-A5] recursive same-machine correctness OPEN; [P1-01], [P1-03], [P1-04] OPEN. Route B [P2-D1], [P2-B1], [P2-B2] OPEN. Conditional FLMV targets $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ are **not** established for any universal contractor. No agent, schedule, role, R_mix341 grammar/weight or root manuscript changed.

**P versus NP remains OPEN.**

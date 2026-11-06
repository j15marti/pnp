# LSPV-2/431: Shared checkpoint query cost, exact AND obligations, and the explicit-input firewall

**2026-11-05 18:28 PST | Route A primary | PROVED/RESTRICTED elementary oracle theorem, independent review pending; COMPUTATIONAL controls | Universal FLMV contraction OPEN | P versus NP OPEN.**

## IDEA before SEARCH and four falsifiers

Hypothesis: batching *independent, opaque* successor-chain checkpoints cannot amortize their query cost by storing previous replies, whereas authenticated identical subcomputations can be shared. F1: an adaptive cross-branch/interleaved query saves a query on all inputs; F2: off-path guesses/recomputations beat the bound; F3: the claim persists when all branches are known aliases of the same table; F4: the apparent query lower bound implies superlinear FLMV-machine time once the entire source table is actually encoded. F1 and F2 fail in the declared oracle model; F3 and F4 falsify the overbroad generalization, yielding the corrected scope below.

## SEARCH (actual original sources, no Google-branded browser)

Governing original handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; current GitHub issue #3 (through LSPV-4/426 and LSPV-1/431); AGENTS.md blob `19656af`, CODEX.md blob `754999f`, .codex/skills/pnp-research/SKILL.md blob `b8df83a`; previous LSPV-2/429 and /430, LSPV-4/424, LSPV-4/419; Grok `GROKPROOF/2026-11-05_1428_PROGRESS.md` blob `a0e35e7` and `2026-11-05_1913_PROGRESS.md` blob `8a004bf`; Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc72` and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d`, all actually retrieved, not inferred from snippets.

Primary literature: Fortnow, Lipton, van Melkebeek and Viglas (JACM 2005), author PDF https://lance.fortnow.com/papers/files/tst.pdf, machine model section 2.1 and Corollary 5.8; query searches for pointer-chasing/direct sums and decision trees (no exact model-equivalent theorem imported). Current repository-source audits: `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11` defines a finite **one-tape** model, not FLMV indexed machine; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693e`, `ADAPTIVE_FRAGMENT_SYNTHESIS_REPORT.md` blob `b4ef7e8` admits finite caps and exponential projection; `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f` charges a *specific* driver, not arbitrary guest A; `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd1` is the known parity family constructor. OpenAI code and CI are not all-algorithm lower bounds. Direct Google-branded search was unavailable; indexed web search and authenticated GitHub access were used.

## Exact oracle model and theorem (PROVED/RESTRICTED, pending independent mathematical referee)

Fix integers q,k>=1 and M>=4k+8, even. There are q independent black-box total successor functions f_i:[M]->[M], accessible only by adaptive indexed queries (i,v) returning f_i(v). Start at 0 in each block. The controller must compute the **AND** of all k-step endpoint parity bits:

$$
P(f_1,\ldots,f_q)=\bigwedge_{i=1}^{q}\left[ f_i^{\circ k}(0)\bmod 2=1\right].
$$

**Theorem.** The exact deterministic worst-case successor-query complexity is qk, even permitting a single global memo, arbitrary adaptive interleaving, reconvergence and free local computation.

**Upper bound.** Follow each orbit for k queries, one block at a time, stopping early on any even endpoint. At most qk calls; O(log M+log q) bit scratch when tables are read-only.

**Lower bound.** Answer each first-time query (i,v) by assigning a previously unqueried, previously unused target within that block. If v is the last as-yet-unqueried orbit position at depth k-1, select an unused **odd** target. Other first-time outputs are fresh arbitrary targets. At any transcript of fewer than qk calls, some block i has received fewer than k calls (counting duplicate queries); its chain from zero has not been fully revealed. Because every reply points to a fresh unqueried state and M>=4k+8, complete all still-unrevealed orbit edges with fresh states, finishing at odd endpoints in **every** block. This gives a YES completion. Complete one underqueried block instead with a fresh even final endpoint; keep all others odd. This gives a NO completion. They agree on every queried successor entry, so any halted deterministic controller errs on one of them. Therefore its worst-case query count is >=qk. The dependency is an **AND of q required branches**, not a mistakenly chosen OR. No branch-local hypothesis is transported to a different block.

**Certified sharing exception.** If the encoding explicitly supplies **q authenticated aliases** to the *same* single successor table, k queries suffice, since all endpoint bits are identical. Reading arbitrary tables and guessing equivalence is not an authenticated alias and would require an independent verification argument. Thus disjoint and shared programs give qk versus k queries for the same task. This contrasts opaque independence with true shared subcomputations; it does not yield a machine lower bound.

## ITERATE: size-aware repair defeats the proposed FLMV obstruction

In the natural **explicit** source representation the q tables contain qM entries, each w=ceil(log2 M) bits. Thus N=qMw and M>=4k implies

$$
qk \le \frac{N}{4w}.
$$

Even the sharp qk adversarial lower bound is at most linear in source bit length (modulo access accounting). A deterministic indexed source scanner can validate the fixed-length table and follow all chains in O(N polylog N) time, O(log N) writable space. Output an exact AND label, with no external SAT guest or uncharged oracle answers. This is a promised function-table problem, **not** a general SAT solver. If instead the f_i are succinctly computed by arbitrary programs, the explicit-table size inequality no longer applies, but the opaque-query lower bound no longer transfers to white-box code inspection either. Neither model provides the missing universal all-input FLMV contraction or an unrestricted barrier.

The query lower bound charges calls, **not** the physical work of a complete indexed input jump (index writes, erasure, and bit-level table access); those operations add cost. In the ordinary full-input table encoding a simple O(N polylog N)-time low-scratch method exists. A virtual child-bit port claiming sublinear space must additionally charge repeated access, program introspection, authentication, format parsing, output, all live ancestor states and failure policies.

## Established hard-family/theorem/encoding ledger

Preserved published control: odd-charge Tseitin on suitable cubic edge-expander graphs G_H with H vertices, |E|=3H/2, one edge variable per edge, and four proper width-three clauses per vertex forbidding assignments violating that vertex's parity. Total 4H clauses; indexed literal encoding N_H=Theta(H log H) bits. If total charge odd, sum of all GF(2) vertex equations gives 0=1, so UNSAT is **mathematically certified**. Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) prove 2^{Omega(H)} ordinary **Resolution** lower bounds on suitable expander families, not on arbitrary algorithms. Previously certified mixed R_mix341 has a 4H-1 paid-node GF(2)/AND3 refutation for bridgeless odd cubic sources, hence no native mixed proof-hardness transfer. The current q-table experiment is a **focused white-box/black-box resource countercontrol**, not a newly proposed hard 3-CNF. No PHP-to-3CNF lower-bound-preservation claim is used.

## COMPUTATIONAL verification and resources

A deterministic JS producer constructed 80 adversarial <qk query transcripts (q=2,3,4,5; k=1,2,3,5; five adaptive patterns), storing each transcript and independently completed YES/NO full tables. Every final completion is a **total table** and agrees with all observed indexed answers. Total returned oracle responses = 690. Producer checked 2084 local conditions. A separately authored independent checker verified 6850 assertion groups, including four mutated-record rejections (corrupted oracle reply, out-of-range index, forged NO completion, invalid alias). Source-authenticated established-family controls: K4 (4 vertices, 6 variables, 16 clauses) and cube (8 vertices, 12 variables, 32 clauses), both odd/UNSAT and even/SAT by exhaustive assignment enumeration, and all odd-source one-clause deletions SAT. Results are exactly scoped finite checks; no native FLMV-machine execution or exact R_mix341 checker execution is claimed. Raw JSON includes q,k,M, all transcript queries, both total tables, alias descriptors and parity controls. No random seed; enumeration deterministic. Source code is in `experiments/arc/lspv2_431_shared_checkpoint_directsum.mjs`; independent checker `experiments/arc/lspv2_431_independent_verify.mjs`; data `results/raw/arc/2026-11-05_1828_LSPV2_SHARED_CHECKPOINT431.json`.

**Physical ledger:** completed qk-1 oracle responses are model calls, NOT billed primitive FLMV-machine steps; the JSON evidence is explicit and its length scales as O(qMw + qkw), verifier uses O(qMw+qkw) array inspections and O(log N) scratch if streamed with indexed source, although the executed in-memory JS model holds O(qM) entries. Source validation O(N) bit scans; constructing/writing all tables O(N), and source bit retrieval O(w) per entry. The small enumerator's search time is distinct from the conjectured A->Phi(A) runtime. There is no numerical certificate of a universal FLMV t'/s' envelope.

## Transfer implication / next open arrow

This rules out another unjustified inference: independent opaque checkpoints do not automatically share work, yet that query lower bound is **too weak per explicit encoded source length**, and disappears under authenticated aliasing. The genuine open bridge is a fully effective, source- and code-authenticated, recursively iterable algorithm A->Phi(A) that finds exploitable shared structure or verified jumps for **every** fixed uniform polynomial-time correct SAT machine on every SAT/UNSAT/malformed input, with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2) and all-phase local rho<=1/2. No B1/B2/B3 or P-vs-NP conclusion follows.

Root `main.tex` unchanged: authenticated fetch returned SHA `593000bbe5b09df6b93fb7453da2ebdf73aeff6b` but zero readable bytes, so ownership-preserving edit not justified. Other roles' files and all five task identities/schedules/enabled states unchanged. P versus NP OPEN.

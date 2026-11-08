# LSPV-2/494: Tight upper control for an existing multipass original-Tseitin SAT bound

**2026-11-08 07:12 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Exact tracker references:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The lower bound below is NOT NEW: LSPV-4/488 already established it on the same exact original-clause language. This run contributes an explicit near-matching, deterministic, arbitrary-arithmetic, complete-pass upper-bound control, with both-label finite verification and an honest source-ID access qualification. It does not promote a proof chain.

## IDEA -> SEARCH -> ITERATE
**Initial question:** Is the previous deterministic multipass lower bound for clause-permutation SAT genuinely tight, or does allowing complete arbitrary computations on each item leave an unaccounted additional obstruction? **Falsifiers specified before source search:** F1, a repeated-clause input can remain UNSAT after omitting an essential original clause; F2, the proposed bucket algorithm accepts a repeated-label word; F3, a purported fresh lower bound merely duplicates the project's earlier multipass argument; F4, mapping an unannotated signed CNF clause into its original ID is falsely treated as free.

**Search and correction:** F3 was decisive. Actual reports LSPV-4/445, /452, /486, and especially **LSPV-4/488** already prove the full original-clause deterministic $p$-pass fooling-set lower bound. We explicitly adopt rather than republish their result. Existing LSPV-2/493 proved an original proper-3CNF permutation-to-SAT decision reduction and the separate Yao (1994) opaque-comparison transfer. The revised contribution is a matching sequential **upper** control with a precise native-token model. F1 and F2 were refuted by mathematical argument and independent finite implementations. F4 remains an explicit barrier to an all-input/native-FLMV transfer.

**Actual project reviews:** complete root `proof1.txt` and `proof2.txt` (both read), issue #3 including LSPV-2/493, LSPV-4/495, LSPV-5/435; governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; actual `GROKPROOF/2026-11-08_1130_PROGRESS.md` (blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`); actual `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`).

**External pinned controls:** `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` (finite-machine P subset NP, not a P/NP resolution); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `INDEPENDENT_AUDIT.md` blob `b30515cced93d8911a6415555ee9ec1444502d93` (restricted plans); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab` (actual GF(2)-CNF generator); `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (different proof language); `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f44ad49370d1b812e862c03c3a91d7f836` (actual time-costed Lean fragment, not universal contraction). No repository supplies a same-machine all-input A-to-Phi(A) operator.

**Primary literature searched:** Yao 1994, DOI 10.1137/S0097539788148959 (comparison branching programs only); Fortnow, Lipton, van Melkebeek, Viglas, *JACM* 52:835-865 (2005), DOI 10.1145/1101821.1101822 (distinct indexed random-access Turing-machine model); Urquhart 1987 and Ben-Sasson–Wigderson 2001 (ordinary shared-DAG Resolution, not general SAT). A separately authenticated Google-branded search service was not available; public research search was performed.

## Exact published-family ledger and SAT equivalence
Fix a connected bridgeless cubic graph $G$ with $H$ vertices, $3H/2$ edge variables, odd-total charge vector $\chi$, and its original signed proper 3-CNF Tseitin source $F_G$. Each vertex supplies the four clauses excluding wrong-parity triples on its three incident edge variables. Therefore $m=4H$ source clauses, each containing three distinct variables; a fixed-width binary literal encoding has $N=\Theta(m\log m)$ bits. The full formula is UNSAT. Every original clause is individually necessary: after deleting its sole local forbidden triple, use that triple at its vertex and solve the remaining connected graph's even-total-charge incidence equations. See LSPV-4/488 and LSPV-2/493 for the full graph/bridge argument. Published cubic expander subfamilies are exponentially hard for **ordinary DAG Resolution** [Urquhart; Ben-Sasson/Wigderson] only, not proven hard for ER, GF(2), complete historical R_mix341 or general algorithms.

Let $(C_0,\ldots,C_{m-1})$ enumerate the original strict ternary clauses. For **every** $m$-word list $a\in[m]^m$ let $D_G(a)=\bigwedge_{i=1}^m C_{a_i}$, including legal duplicate records. The proved exact ordinary-CNF semantics are

$$
\operatorname{UNSAT}(D_G(a))\iff a\text{ is a permutation of }[m].
$$

Thus original-source SAT labels are the complement of `PERM_m` on this **promised** sublanguage; this is not a theorem about malformed arbitrary CNF inputs.

## Existing LOWER vs new matching UPPER
**Already known lower bound (LSPV-4/488, not claimed new).** Deterministic exact $p$-pass full left-to-right stream, with at most $S$ **total transferable state bits**, must satisfy

$$
(2p-1)S\ge\log_2\binom{m}{\lfloor m/2\rfloor}-O(1)=m-O(\log m).
$$

Use all $\lfloor m/2\rfloor$-subsets $A$ as first halves and complements of other subsets as second halves. The resulting SAT matrix is complement of EQUALITY, so its accepting/diagonal fooling set yields the communication bound. It explicitly counts full state exchanges across $2p-1$ half-stream boundaries. This excludes any derivation claiming a stronger unrestricted lower bound from these same state arguments.

**Theorem 494.1 (matching upper, restricted).** Assume the input is an **already locally authenticated original-clause-ID stream**, $m$ records of $\lceil\log_2m\rceil$ bits each in $[m]$, with fixed known $m$; assume the record-to-ID decoding fits $O(\log m)$ state and $\operatorname{polylog}(m)$ time per record. For every integer block width $1\le b\le m$, a uniform deterministic exact algorithm uses

$$
p=\left\lceil\frac mb\right\rceil\text{ full input passes},\quad
S\le b+O(\log m)\text{ writable bits},\quad
R=mp\text{ record visits},\quad
T=O(mp\operatorname{polylog}m)
$$

and returns UNSAT iff $D_G(a)$ is UNSAT, otherwise SAT. It uses no SAT oracle, no random coins, no precomputed answer and no branching proof.

**Construction and proof:** Partition $[m]$ into $p$ consecutive buckets of at most $b$ IDs. In pass $j$, initialize a **$b$-bit** zero bitset, stream every record, and set its bit only for labels within bucket $j$. If any bucket is not fully present, remember a single failure bit. After the final pass, output UNSAT iff every bucket was full. If all $m$ IDs appear, with **exactly $m$ input records** they each appear exactly once, hence the formula is the original odd-charge UNSAT. If a label is missing, its bucket fails and the remaining formula is SAT by clause essentiality. No per-record multiplicity counter or large table is needed.

For $b=\lceil\sqrt m\rceil$, $p=\Theta(\sqrt m)$, $S=O(\sqrt m+\log m)$ and $R=\Theta(m^{3/2})$. More generally $pS=O(m+p\log m)$, matching the earlier deterministic multipass lower bound within constant factors whenever $b=\Omega(\log m)$. In the bit-stream model, input scans and local decoding cost $T=O(pN\operatorname{polylog}m)$ if native original clause IDs are decoded within the stated resource budget. **Neither the label map nor arbitrary 3-CNF authentication is free:** extension from the promised record grammar to arbitrary signed clause encodings needs a charged authenticated decoder, and extension to every binary input needs an all-input fallback. Neither is constructed here.

## Finite independent tests
The Python reference independently constructed original strict signed Tseitin clauses on **K4, triangular prism and cube**, independently brute-force-checked original odd-charge UNSAT and the satisfiability of each individually deleted original clause, tested **350** random full/replacement words per graph and several bucket widths, exhaustively enumerated all $m$-words for $m=2,3,4,5$, and exhaustively checked subset-cross fooling matrices for $m=4,6,8$. It passed **58,837** assertions. Independently written Node.js with different Set-based bucket implementation passed **11,774** assertions on three graphs, **250** random words each, small alphabet enumeration and all $m=4,6,8$ fooling pairs. Host-language memory consumption is NOT claimed to be a physical native $S$ measurement; mathematical bitset size is proved separately. All malformed-input/incorrect-source claims are excluded from the promise. These are new finite upper-bound controls, not a rediscovery of LSPV-4/488's lower bound.

**Files:** `experiments/arc/lspv2_494_stream_bucket_upper.js` (published independent verifier), `results/raw/arc/2026-11-08_0712_LSPV2_494_STREAM_UPPER_RAW.json` (raw ledger), and `research/coordination/2026-11-08_0712_LSPV2_STREAM_BUCKET494_FIVE_ROLE_HANDOFF.md`; Python reference is retained separately in the run reproducibility archive. Source authentication, malformed general-CNF handling, child generation, failed policy search and historical native proof certificate verification are NOT implemented, rather than counted as free.

## Resource and transfer audit
Existing LSPV-4/488 lower and this matching upper measure sequential source records, deterministic exact output and bounded retained state, with actual rewind/pass count. No shared proof DAG, extension-variable solver or R_mix341 certificate is derived; work/span in that calculus are not identified with this runtime. Indexed access can visit arbitrary source records and use different algorithms. Streaming input and offline GF(2) characterization cannot silently be transported to FLMV's indexed read-only input, or to a uniform recursively iterable all-input operator.

**Publication/tracker:** proof1.txt and proof2.txt were both read; no established status, dependency, asymptotic lower-bound exponent, or unresolved transfer obligation changed from the earlier LSPV-4/488 plus LSPV-2/493 results. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Report and evidence are role-owned. Never edit another role's manuscript, root main.tex or historical R_mix341 weights. All existing five roles and two/three route allocation preserved.

**Actual advance:** constructive asymptotically near-matching upper resource control, making the model-specific multipass barrier quantitatively tight and detecting any attempted inflation of that restricted lower bound. **Remaining OPEN:** [P2-A2], [P2-A4], [P2-A5] require a solver-dependent, exponent-oblivious, recursively iterable, both-label, malformed-aware all-input transformation with fully charged **same indexed-FLMV-machine** bounds. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **P versus NP OPEN.**

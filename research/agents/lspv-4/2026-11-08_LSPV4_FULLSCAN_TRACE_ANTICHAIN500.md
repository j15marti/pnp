# LSPV-4/500 | Full-input-read guest and Resolution-hard trace-cache antichain

**November 8, 2026, 11:36 PST (America/Los_Angeles) | LSPV-4 resource auditor | Route A PRIMARY | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Exact proof-chain IDs:** [P2-A2], [P2-A4], [P2-A5], [P2-L4-499], peer LSPV-2/500, cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2]; companion [P1-01], [P1-03], [P1-04]. The full historical `R_mix341` grammar and fixed weights are NOT changed. The new item [P2-L4-500] is a *restricted resource/shortcut adversary*, not an unconditional all-machine lower bound.

## IDEA: concrete hypothesis and predeclared falsifiers
**Hypothesis:** The trusted multi-anchor guest-input footprint cache of LSPV-2/500 has no guaranteed worst-case reuse across legal distinct children for *every* hypothetical polynomial SAT decider. A correct deterministic guest can perform a harmless complete source scan before its SAT computation; its honest read footprint then includes every child bit. A portfolio of pairwise distinct, equal-sized, original-Resolution-hard 3-CNF children gives zero legal cache hits no matter how many prior anchors are retained.

F1: after an honest full read of every child bit, a different equal-length input nevertheless matches all recorded bits. F2: the auxiliary-clause variations cease to be proper 3-CNF, become SAT when the odd core is UNSAT, or destroy the published ordinary-Resolution lower bound. F3: a two-anchor cache fails to reuse genuine short-prefix traces of alternating certified odd cores, meaning the proposed negative control is actually a broken cache. F4: generating the adversarial portfolio necessarily exceeds the Route A *local* q/M work and storage exponents even before simulating the guest.

## SEARCH: exact source files and boundaries
Read BOTH complete root trackers via authenticated GitHub: `proof1.txt` initially blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, `proof2.txt` initially blob `6f2103674963296f3710a6d3533adf329995d640` (486,870 characters; final blob rechecked before any potential tracker write). Read current issue #3 and its newest peer updates; governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; repo skill `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.

Peer original report `research/agents/lspv-2/2026-11-08_1120_LSPV2_TWO_ANCHOR_TRACE_REUSE500.md` blob `a8238aa7e3629f85f6155de01d0bfc6662ded27b`, including its precise source grammar, anchor theorem and conditional cost recurrence. Peer `research/agents/lspv-2/2026-11-08_1044_LSPV2_PREFIX_INVERSE_NATIVE_STREAM499.md` blob `22c819b744697801cc949a90717e298b56830784`. LSPV-4/499 original sign-bit adversary blob `6b280192125e6260695736725ca8b59e8d288fd8`. Actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; actual Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`. Neither source claims a universal transfer.

New required external sources actually inspected: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` (P subset NP in its finite-machine model only); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (local scoped claims). Other exact files: `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab` (parity generator); `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (separate XOR certificate, not historical Rmix); `openai/math/CONTENTS.md` blob `7e1ed90ac5a666f1bbecb22027387c4ad79e9d03` (research index, no needed transfer). Other GitHub repos were not independently replayed this run. Public web search (not a separate Google-branded search client) examined the primary FLMV 2005 article, Urquhart 1987 and Dell–van Melkebeek 2014. Repository git cloning from the container failed DNS, so read/write was via the authenticated GitHub connector. Formal repo preflight/check scripts were unavailable locally and were not claimed to run.

Primary model references: Fortnow–Lipton–van Melkebeek–Viglas, JACM 2005, https://doi.org/10.1145/1101821.1101822 (indexed input and charged WORK high-water); Urquhart, JACM 1987, https://doi.org/10.1145/7531.8928 (expander Tseitin, exponential *ordinary DAG Resolution*); Ben-Sasson–Wigderson, JACM 2001, https://doi.org/10.1145/375827.375835 (width/size relation); Dell–van Melkebeek, JACM 2014, https://eccc.weizmann.ac.il/report/2010/038/ (solver-independent compression barrier, hypothesis-sensitive).

## Theorem 500.1: full-read guest kills cross-input footprint cache (PROVED/RESTRICTED)
Let `B` be any total deterministic SAT decider on binary strings, with explicit SAT, UNSAT, MALFORMED output labels. Define `B_scan` to scan *every input bit* in physical order, then execute `B` unchanged. It computes exactly the same three-label language. If `B` is polynomial-time (conditional SAT in P), `B_scan` is also a single uniform total polynomial-time decider: its extra time is `O(L)` or at most `O(L polylog L)` with conservative indexed positioning, and extra writable/index space `O(log L)`, inclusive of counters; entire original guest execution is still charged.

A trusted actual-read anchor for a length-L input x records all L read addresses, so a subsequent length-L input y matches the footprint if and only if y=x, regardless of its SAT label. Consequently a query portfolio of q pairwise distinct equal-length inputs has **exactly q guest invocations and zero footprint-cache hits** under this unchanged-guest reuse rule, for ANY number h of retained anchors. This is an all-L mathematical statement about this particular technique, **not** an obstruction to semantically stronger, code-aware optimizers or to the existence of a correct q-child universal contraction.

Proof: complete scan makes read-set `{0,...,L-1}`. All address/bit equality is precisely string equality. For pairwise distinct strings, no subsequent query is equal to an earlier anchor. Correctness of `B_scan` follows because it ignores the scan values and runs `B` afterward. QED.

## Theorem 500.2: authentic Resolution-hard antichain with the same resource exponents (PROVED/RESTRICTED)
Take a published family of connected bounded-degree *expanding cubic graphs* `G_H`, with H vertices and `3H/2` edges, and odd vertex charges `chi`. On each vertex v with edge variables e1,e2,e3, for every local assignment a whose XOR parity differs from chi(v), insert the proper clause

$$
C_{v,a}=\bigvee_{i=1}^{3} \begin{cases}e_i,&a_i=0,\\\neg e_i,&a_i=1.\end{cases}
$$

There are exactly 4H original clauses, and the original is UNSAT by XOR summation. On these expanding graphs, the published Urquhart/width lower bounds apply to **ordinary shared-DAG Resolution** (not arbitrary SAT algorithms, ER, Rmix or GF(2) shortcuts).

Introduce H fresh variables `y_0,...,y_(H-1)`; add H fixed pairwise-distinct proper clauses `(y_i OR y_(i+1) OR y_(i+2))` with subscripts modulo H (H>=5). Choose q(H)=floor(H^(6/5)) **different** additional proper ternary clauses `D_j` on fresh variables, excluding the fixed clauses, and each satisfied by y=all-TRUE. There are at least `7*binom(H,3)-H` available clauses, enough for q(H) at large H. Set

$$
F_{H,j}=\mathrm{Tseitin}_{G_H,\chi}\;\wedge\;P_H(y)\;\wedge\;D_j(y).
$$

Each input is proper 3-CNF with **exactly 5H+1 clauses**, `(5H/2)` variables, identical encoded length `M(H)=Theta(H log H)` in a fixed-width dense-ID signed-literal encoding, and a different source byte string. Every one is UNSAT, while setting y=TRUE satisfies *all* new clauses. This is a valid expansion/padding of an established source, not an invented claim that the padding is itself hard.

**Exact lower-bound preservation direction:** Restrict ANY ordinary Resolution refutation of `F_(H,j)` by y=TRUE. All padded original clauses become TRUE and disappear; source `Tseitin_(G_H,chi)` remains unchanged. Ordinary Resolution is closed under restrictions, with resolution steps reducing to valid resolution or pruning, so the restricted refutation has no more paid inference nodes. Thus

$$
S_{\mathrm{Res}}(F_{H,j})\ge S_{\mathrm{Res}}(\mathrm{Tseitin}_{G_H,\chi}).
$$

The reverse inequality holds because a refutation may ignore all padding clauses. Hence **equality** of minimum ordinary Resolution refutation size, and the published exponential lower bound transfers exactly in this *restricted proof model*. No claim of historical Rmix simulation, B3 or arbitrary-machine hardness follows.

For the independent-query resource window, define parent-length parameter `N=M(H)^2`. Then child length `M=N^(1/2)`, and `q(H)=N^(3/5-o(1))`. A materializing output generator that writes every child pays `Theta(qM)=N^(11/10-o(1))` output bits (plus paid polylogarithmic generation/index overhead). This is *within the stated local exponent* up to `N^o(1)` factors. It is **NOT** a correct all-input SAT decomposition or new FLMV algorithm. On these pairwise-distinct sources, Theorem 500.1 forces zero exact-footprint cache hits for `B_scan`.

## Finite falsifier tests (COMPUTATIONAL)
Reuse the **exact** LSPV-2/500 guest-format fixture: 8-bit magic `10110101`, 6-bit n=16, 12-bit m=192, each ternary literal one sign bit plus a 4-bit variable ID. Total `L=26+192*15=2906` bits. On the genuine signed K4 core, 16 original clauses (6 edges), add 175 distinct proper fresh-variable clauses and one of 128 distinct final clauses, all satisfied by setting 10 fresh variables TRUE. Two alternating odd-charge K4 cores are UNSAT, while the even-charge core is SAT; exhaustive 64-edge-assignment checks and direct even-charge satisfying witnesses were independently reproduced. K4 is a *finite semantic fixture*, not the asymptotically hard expanding-family theorem.

For 128 pairwise-distinct odd children, the previously documented sound short-prefix guest provides **2 actual calls +126 cache hits** using 2 anchors. The extensionally equivalent hypothetical full-read-first guest yields **128 actual calls +0 hits** with h=1,2,4,8. Across another 128 odd/even mixed valid sources, full-read also gives 128/0 for each h; original short-prefix case h=2 gives 96 calls/32 hits. Both independently written hosted programs produced exactly the same 32 portfolio results and SHA-256 strings (`167ede525c2c62ce4fd4e7944b46e65d19fa46b5145d9ba112535d0d4ce7083a`, `8f4e704af01d9d5ac3c25d181e8d4154bd0e033971357a9b59b8ec5d4e063f08`). Four malformed-string controls were rejected in the Python fixture. The **finite JS guest's even-case fallback is a fixture check**, not a complete general SAT decider; Theorem 500.1 uses a symbolic arbitrary total correct B and does NOT rely on this finite fallback being complete.

Independent hosted Python: `lspv4_500_trace_antichain.py` and `raw.json`; independently authored Node: `lspv4_500_independent.mjs` and `independent_raw.json`, cross-language result equality checked. Published standalone Node verifier `experiments/arc/lspv4_500_fullscan_trace_antichain.mjs` blob `fd7e20bf7974393d9a089f95266f6b4486fb7c1d`, exact source readback; raw results `results/raw/arc/2026-11-08_LSPV4_500_FULLSCAN_ANTICHAIN_RAW.json` blob `4fdd59d00103ca84a4eb86e65ab56d6ff399b019`. Neither program implements an FLMV transition table or historical Rmix proof checker. Do not interpret measured runtimes as computational lower bounds.

## Native-machine and branching-DAG resource ledger
- **Logical inference nodes / certificate evidence bits:** Not applicable to the cache upper control. The Resolution size-preservation theorem concerns a *different*, ordinary Resolution proof model, with no inference-weight claims for historical Rmix341.
- **Original source and child construction:** q strings of length M; dense IDs and fixed packet shape. Building the fixed pads/variation indices, parsing, write-only output and source/index/head operations are chargeable: `O(qM polylog N)`, not free. Malformed children still require correct guest handling; no universal child constructor is present.
- **Guest invocation:** `u=q` under fullread-first A and distinct children; child stage time `O(q M^t polylog N)` for guest exponent t, not improved by caching. For one-stage recursion, this is `N^(3/5+t/2+o(1))` when applicable; the missing correctness/decomposition theorem is not supplied.
- **Caching and bit evidence:** with h retained anchors, sparse records use `O(hM log M)` bits including read addresses; dense exact scans can reduce to `O(hM)` bits. Cache comparisons use at most `O(qhM)` indexed bit checks, and all failed comparisons are charged. h polylog yields `N^(11/10+o(1))` local time when explicitly implemented, not an exponent reduction of guest calls.
- **All-phase peak:** at least simultaneously retained hM footprints, live child M, guest workspace `S_A(M)`, ancestor frames/indices and output buffers. A safe upper envelope for the *conditional stage* is `N^(max{1/2,s/2}+o(1))` only when the missing child source construction, native guest interpreter, virtual port, cache and all phases independently satisfy the stated bounds. Lazy access can trade storage for retrieval/replay but does not change the fullread equality conclusion.
- **AND/OR branches and sharing:** Cache labels are reusable only for complete context-encoded inputs with justified assumptions. A source decision oracle is not a sound proof rule. This run neither adds branching or weakening to historical Rmix341 nor double-counts source-shared logical nodes.

## ITERATE: falsifier results and open arrow
F1 **discharged by exact read-set proof**; F2 **discharged by disjoint satisfying restriction** and finite K4 syntax/assignment checks (expanding-graph hardness remains known only under its published assumptions); F3 **passed positive control** 126/128 verified short-prefix reuses; F4 **not an obstruction** because `qM=N^(11/10-o(1))` and streaming/retained h polylog storage fits the *candidate local* resource window, subject to explicitly charged implementation.

**Revised claim:** No upper bound `u=o(q)` for actual unchanged-guest invocations can be concluded from a bounded or unbounded trusted input-footprint anchor cache alone, uniformly over all hypothetical correct polynomial SAT deciders and all legal distinct child portfolios. This is an intensional *cache-specific* limitation, not a proof that no solver-dependent compression or universal FLMV transformation exists.

**Tracker impact:** [P2-L4-500] adds a substantive restricted adversarial control to [P2-A4]; [P2-A2] and [P2-A5] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. P versus NP remains OPEN.

**Publication safety:** Root `main.tex` was fetched with blob `68188a24badda635a5983fda1c381cdb694fd497` but returned 0 readable characters; left unchanged rather than overwriting unreadable bytes. No five-role tasks, identities, schedules, states, 2A/3B allocation or Rmix341 historical grammar/weights changed.

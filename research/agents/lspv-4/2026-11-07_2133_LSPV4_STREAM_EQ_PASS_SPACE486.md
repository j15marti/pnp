# LSPV-4/486 | Exact deterministic multipass streaming resource obstruction on original cubic packet 3-CNF

**2026-11-07 21:33 PST | Route A resource auditor | PROVED/RESTRICTED (known deterministic communication lower-bound specialization); COMPUTATIONAL finite controls; P versus NP OPEN.**

**Exact tracker nodes:** [P2-A4] material restricted resource evidence, [P2-A2] universal same-machine contraction OPEN, [P2-A5] recursive closure OPEN; cross-chain [P1-01], [P1-03], [P1-04], Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

## IDEA -> SEARCH -> ITERATE

**Hypothesis (before source search).** Even arbitrary semantic summaries of a signed cubic-packet 3-CNF cannot reduce the memory of a deterministic *fixed-order, complete-pass stream* below the size of an encoded equality interface when source clauses are divided into a first half and second half. A native random-access machine, reordering clauses or a richer source interface may bypass this lower bound.

**Precise falsifiers:** (F1) canonical original proper signed 3-CNF does not implement EQ of two length-w bit strings; (F2) different A-prefixes can share a final one-pass configuration without misclassifying some B-suffix; (F3) a p-pass simulation can communicate less than the entire carried configuration at a crossing; (F4) the lower bound also forbids a legal FLMV random-access / rereading shortcut. F1-F3 fail by the construction and rectangle proof. F4 instead limits the theorem: arbitrary indexed access, reordering and randomization are NOT covered.

**Project continuity read:** Complete main `proof1.txt` at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` at initial blob `e2e15d8632676257a4cbfcf8ca8ca3b2cd09b011`; issue #3 and recent peer comments; governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; LSPV-2/483 (frontier/syndrome DP) and /484 (rare fallback), LSPV-4/484 (literal-frontier layout) and /485 (implicit Kruskal LOGSPACE witness); `GROKPROOF/2026-11-08_0320_PROGRESS.md`; `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. **Deduplication:** Claude previously established a stronger sequential one-tape equality-based lower-bound family; this is a targeted *original cubic packet grammar + p-pass transfer* control, not a new general communication theorem. No full root `main.tex` was fetched and none was edited.

**Sources inspected, pinned:** `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` (the source of standard parity-packet expansion, external), `meelgroup/frat-xor/format.md` (mixed clause/XOR format but NOT native `R_mix341`), `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. External repos contain no universal same-machine SAT contraction or transfer for this particular streaming bound. Primary theoretical references: Kushilevitz and Nisan (1997), *Communication Complexity*, equality fooling-set/monochromatic rectangles; MIT Algorithms for Massive Data (2021) lecture 6, exact standard `(2p-1)S` streaming communication simulation, https://www.mit.edu/~mahabadi/courses/Algorithms_for_Massive_Data_SP21/Lec6.pdf; Fortnow, Lipton, van Melkebeek and Viglas, JACM 52(6):835-865 (2005), DOI 10.1145/1101821.1101822, the DIFFERENT native indexed machine theorem. Web search available; no separate Google-branded client. No claim of theorem novelty.

## Exact source family and semantics

For each w>=1 let G_w be w vertex-disjoint K4 graphs. Graph j has edge Boolean variables `x_{j,01},x_{j,02},x_{j,03},x_{j,12},x_{j,13},x_{j,23}`, with numeric IDs `6j+1,...,6j+6`. Fix binary words A,B in {0,1}^w. Each of the 4 vertices per K4 contributes **exactly four original proper signed width-3 clauses**. At vertex 0, forbid all four local triples whose first bit `x_{j,01}` differs from A_j. At vertex 1, forbid all four local triples whose first bit `x_{j,01}` differs from B_j. At vertices 2 and 3, forbid the four local triples with odd parity, enforcing even local XOR. For any forbidden triple z on local edges e_1,e_2,e_3, use the original clause

$$
C_z=\ell_{e_1,z_1}\lor\ell_{e_2,z_2}\lor\ell_{e_3,z_3},
\qquad \ell_{e,0}=x_e,\quad \ell_{e,1}=\neg x_e.
$$

Order the source as all vertex-0 packets for j=1..w (Alice prefix), then all vertex-1 packets, then all vertex-2 and vertex-3 packets (Bob suffix). All inputs of fixed w share literal IDs, source length and graph. A changes only signs in the prefix; B changes only signs in the suffix.

Explicit binary code: Elias gamma(w), then 16w fixed-width clauses, each a triple of sign bit followed by L=ceil(log2(6w+1)) ID bits, with no delimiter because width and total count are fixed. Total bit length:

$$
N(w)=2\lfloor\log_2 w\rfloor+1 + 48w(\lceil\log_2(6w+1)\rceil+1)
=\Theta(w\log w).
$$

Exact source length and signs are independent of A,B. This *family* grammar is not the arbitrary CNF grammar; each source is nonetheless an explicit syntactically valid signed proper 3-CNF. The K4 gadgets are finite controls, not claims of established growing Resolution hardness.

## Theorem 486.1 (PROVED/RESTRICTED): exact equality embedding

$$
F_{w,A,B}\text{ is SAT}\quad\Longleftrightarrow\quad A=B.
$$

If A_j differs from B_j, vertex 0 forces x_{j,01}=A_j while vertex 1 forces x_{j,01}=B_j, a contradiction. If equal, fix x_{j,01}=A_j. Vertices 2,3 impose two independent GF(2) parity equations on the remaining five variables, hence precisely 2^(5-2)=8 satisfying edge assignments for each component. Therefore when A=B the whole formula has exactly 8^w models; otherwise zero. These counts refer to the ORIGINAL clauses, not only to an algebraic surrogate.

## Theorem 486.2 (PROVED/RESTRICTED): one-pass and p-pass state lower bound

A deterministic fixed-order streaming algorithm reading the exact binary original source once, with no random indexed input access and without treating a readable output or oracle as free storage, requires **at least w bits of prefix-state information**, apart from finite-control/encoding constants, to classify these instances exactly. The 2^w diagonal accepting pairs (A,A) are a fooling set for equality; two cannot have the same accepting protocol transcript, since their crossed pair (A,B) would then be incorrectly accepted. Therefore deterministic communication is at least w bits.

For a deterministic p-pass algorithm, where each pass reads the whole source left-to-right, the standard two-party simulation exchanges a carried machine configuration at each Alice/Bob boundary and interpass return, at most 2p-1 times. If each *entire transferable configuration* has size S bits including WORK/INDEX, cached information, heads and the pass counter, then

$$
(2p-1)S\ge w.
$$

If S counts only writable tape contents, use `S+O(log N)` to include head positions/finite control for polynomial-time machines. With

$$
S=O(N^{1/2}), \qquad N=\Theta(w\log w),
$$

we require

$$
p=\Omega(\sqrt N/\log N),
\qquad T=\Omega(pN)=\Omega(N^{3/2}/\log N)
$$

**for this specific full-pass streaming architecture**, exceeding a nominal local-time budget N^(11/10+o(1)). The conclusion does not apply to machines using arbitrary indexed jumps or input-interleaved ordering, and does not establish hardness of arbitrary 3-SAT algorithms. In fact this canonical subfamily is easily decided with O(log N) writable space and O(N polylog N) time using indexed reads of A_j and B_j at their known offsets, or by reordering clauses to pair matching gadgets. Randomized fingerprinting with error is not covered. Proof weight and actual machine time are different metrics.

## Finitary falsification controls and exact ledger

Independent Python oracle: `independent_python.py` in the local reproducibility archive exhaustively evaluated every assignment for every (A,B) for w=1,2, 20 binary sources, plus 16 larger structural samples; 136 assertion groups passed, 0 failures. Exact counts are 8^w for equal, zero for unequal. Separately implemented published pure JS generator/decoder/exhaustive oracle checked **161** assertions across 20 exhaustive sources, 16 larger sources, and 5 malformed / out-of-family rejects. This is finite **COMPUTATIONAL** evidence; the asymptotic theorem is the separate rectangle argument.

**Resource ledger:** The streaming lower bound charges (i) source-bit reads per full pass N, (ii) at least 2p-1 communication boundary/return configurations of S bits in the proof simulation, not additional real machine I/O, (iii) all retained WORK/head/INDEX locations via S, (iv) final one-bit classification; source authentication and clause matching are ordinary charged stream work. It does NOT assume a free decomposition, failed-policy oracle, proof construction, native R_mix341 inference, or any uncounted source compression. It proves NO lower bound for preprocessing with random access, nonsequential source queries, semantically optimized solver code, explicit materialized child libraries, or general SAT. An original unmodified FLMV machine can bypass sequential full passes. There is no sound inference from this restricted bound to P versus NP.

## Exact publication and follow-up

Role-owned report: `research/agents/lspv-4/2026-11-07_2133_LSPV4_STREAM_EQ_PASS_SPACE486.md`.
Verifier: `experiments/arc/lspv4_486_k4_stream_equality.cjs`.
Raw results: `results/raw/arc/2026-11-07_2133_LSPV4_486_STREAM_EQ_RAW.json`.
Handoff: `research/coordination/2026-11-07_2133_LSPV4_STREAM_EQ_FIVE_ROLE_HANDOFF486.md`.
Precise next Route A task: construct a native indexed-access semantics-preserving counterstrategy that avoids the restricted streaming lower bound while charging source address derivation, source-INDEX/head movement, repeated reads, guest simulation, and all-phase peak memory. [P2-A2], [P2-A5] still OPEN. **P versus NP OPEN.**

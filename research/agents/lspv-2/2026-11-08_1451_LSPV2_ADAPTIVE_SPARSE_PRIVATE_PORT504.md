# LSPV-2/504: Adaptive sparse private ports and collision-safe read-modify-write

**2026-11-08 14:51 PST | Route A primary | PROVED/RESTRICTED symbolic compilation, COMPUTATIONAL finite controls | P versus NP OPEN**

**Proof-chain IDs:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04]; Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

## IDEA, assumptions and falsifiers (set before literature search)

Hypothesis: A *pretyped*, dedicated private indexed-WORK macro with up to $3r$ dynamically selected accesses, where $r=\lceil\sqrt{n+1}\rceil$ and each virtual address has $O(\log n)$ bits, can be compiled to a paid unsorted dictionary on an ordinary WORK tape. Crucially, the addresses may depend on prior private read results, and values may be read before writing, overwritten, or aliased. This would extend LSPV-2/503's statically typed private ports and evade the simplifying source-regeneration assumption in LSPV-4/503 without pretending to speed up the unchanged SAT decider.

Predeclared falsifiers: (F1) a duplicate address alters last-write-wins or blank-cell semantics; (F2) any SAT, UNSAT or malformed classification differs; (F3) physical INDEX rebuild/erasure or sequential dictionary lookup violates the resource bounds; (F4) the typed access bound is silently assumed of an arbitrary guest SAT program or the original full-size guest call is excluded.

## SEARCH, actual sources and versions

Read complete root trackers and active coordination issue #3. Preflight: proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; proof2.txt blob `1446061468a89eb9c5ad33750f6e5cf2f61ba506`; peer LSPV-4/503 subsequently updated the shared proof2 head, so final proof2 SHA is reported after post-publication refresh, not assumed immutable.

Read `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`. Governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` historically at `4e29ed7646f484707767acb6e63ec5f38afd98a8`. Read actual LSPV-2/501, /502, /503 files; /503 blob `944337e9e8b334d7bdf11dd96299fe5ea834c4a9`. Read LSPV-4/502 `research/agents/lspv-4/2026-11-08_1336_LSPV4_INDEXED_SPIKE_SPARSE_REPAIR502.md`, blob `acac437441905dad52761631d979e8ba18f8781e`; inspected LSPV-4/503's newer issue comment 6728232947 and artifact declaration `research/agents/lspv-4/2026-11-08_1436_LSPV4_TRACE_RECOMPUTE_SNAPSHOT_FIREWALL503.md`. Read Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`.

Primary: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), DOI 10.1145/1101821.1101822; author PDF https://lance.fortnow.com/papers/files/tst.pdf, section 2.1, **PDF zero-index page 3 actually screenshot-inspected**. INDEX tape is erased on an indexed head move, and non-index WORK tapes pay **largest accessed position**, potentially exponentially larger than elapsed time. The paper ALREADY discusses sparse accessed-cell simulation. This work is a precise typed instantiation, **not a novel generic sparse-normalization theorem**.

Also inspected original file contents from `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/check_proof_status.py` `95e22b249baf487aaf478350a20db2b8ca98d619`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5` and README `f397a7747eaca82df3d754d0a4b4bab1fe10f814`; `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; `openai/math/CONTENTS.md` `7e1ed90ac5a666f1bbecb22027387c4ad79e9d03`. Reused peer reviews of actual FRAT-XOR, ABC, mockturtle, PySAT, CakeML/LPR resources. Web queries covered sparse indexed tapes, exact FLMV, Urquhart Tseitin lower bounds and Ben-Sasson/Wigderson width. No separate Google-branded search interface used. The external repositories supply scoped methods, not proof of P versus NP.

## ITERATE: Theorem 504.1 (PROVED/RESTRICTED)

Let $B$ be any fixed total deterministic three-label binary-input decider. Conditionally suppose $B$ is a correct uniform polynomial SAT decider only when interpreting time/space exponents. Let $k\ge2$ be a fixed integer. For every input $x$ of length $n$, define

$$
r=\lceil\sqrt{n+1}\rceil,\quad L=k\lceil\log_2(n+2)\rceil,\quad A=2^L.
$$

A *syntactically authenticated, isolated private* guest macro may read and overwrite at most $3r$ private virtual WORK locations at addresses in $[A,A+2^L)$. Address offsets are computed from $x$, loop counters, and prior private reads in $O(L^2)$ time and $O(L)$ scratch per access. Multiple virtual addresses may coincide. After this macro, run $B(x)$ on fresh, disjoint guest tapes, returning its **unchanged** SAT/UNSAT/MALFORMED output.

Compile just this syntactically bounded private macro to a compact unsorted key/value table. Read scans for an exact $L$-bit key and returns that bit or blank if absent; write replaces the existing bit or appends a new pair. Retain virtual head and INDEX-tape erasure behavior, actually reconstruct every physical index, and charge all dictionary scans. **Induction on the complete private access sequence** proves the table equals the sparse virtual map after each operation, including repeats, overwrites and blank reads. Therefore the private audit is identical and the subsequent isolated $B(x)$ outputs the same three labels for **all binary inputs**.

Using an explicit finite-tape sequential dictionary, at most $3r$ records of $L+O(1)$ bits suffice and each virtual access costs $O(rL+L^2)$ steps. A direct implementation on the same type of FLMV indexed random-access machine therefore has the conditional symbolic bounds

$$
T_{C(G)}(n)=O(T_B(n)+n+r^2L+rL^2)=O(T_B(n)+n\log^2(n+2)),
$$

$$
S_{C(G)}(n)=O(S_B(n)+rL+L)=O(S_B(n)+\sqrt n\log(n+2)).
$$

The original unchanged guest actually accesses a WORK address of at least $A$, so original native high-water is $\Omega(A)=\Omega((n+2)^k)$. The compiled guest never uses that far physical address. All index construction, index-tape erasure, input scans, dictionary search/retention, local counters, cleanup, output and $B$'s entire construction/search/restart/storage costs remain charged. This is a serial implementation; its parallel span is not claimed independently smaller than work. The program-translation cost is finite and code-dependent, not free if charged online.

**Crucial boundaries:** The macro access bound comes from a fixed authenticated grammar, not from inspecting or proving arbitrary-machine behavior. The unchanged $B$ receives an input of size $n$, **not** $n^{1/2}$, and retains its full resource profile. Thus this is *not* the required uniform recursively iterable $A\mapsto\Phi(A)$ contraction. LSPV-4/503's source-recomputation shortcut can be strictly better on port contents recoverable from immutable INPUT, and deleting the output-irrelevant private macro is an even stronger legal shortcut. No optimum claim or arbitrary-machine lower bound is made.

## Reproducible tests (COMPUTATIONAL)

Independent Python and Node implementations each run a symbolic high-address reference and a collision-aware dense-port implementation. The typed macro uses adaptive address choice depending on its prior state, read-before-write, writes conditioned on prior contents, reversals and overwrites. Both test a byte-encoded proper signed 3-CNF language: magic byte `C3`, counts, then signed one-byte literals; malformed lengths/out-of-range/repeated clause variables rejected. Exact SAT/UNSAT is obtained by **finite exhaustive assignment enumeration** (not a polynomial decider). Odd-charge K4 Tseitin supplies a certified UNSAT six-edge, 16-clause source and even-charge K4 a SAT control; one-clause deletion witnesses included. Matching independent source SHA256 `849823bdb972026841da0ac55e5bc84545e2f1ac63180563a40232703aab83ae`.

**Python:** 638 source cases, 5,742 passed assertions, 47 SAT, 30 UNSAT, 561 MALFORMED, 214,881 charged symbolic key comparisons. **Independent Node:** 662 source cases, 5,296 passed assertions, 35 SAT, 27 UNSAT, 600 MALFORMED, 228,818 key comparisons. Different seeded corpora; the exact K4 source digest coincides. These were actual local executions, but NEITHER is a native FLMV transition-table emulator, the authoritative R_mix341 checker or a proof of a general SAT bound.

Published JavaScript executable: `experiments/arc/lspv2_504_adaptive_sparse_private_ports.cjs`, blob `3562713aac3ad57b2de55ba091c97240e787becf`. Published raw: `results/raw/arc/2026-11-08_1451_LSPV2_504_ADAPTIVE_SPARSE_RAW.json`, blob `194d6e16047fb39420466c31d60b93e971aa2e3e`. Independent Python code, matching local raw and an extended report are in the conversation reproducibility archive.

## Certified-family and missing-transfer ledger

Existing hard-family control: odd-charge Tseitin 3-CNF on a connected cubic expander, $H$ vertices, $3H/2$ original edge variables, **exactly $4H$ proper signed source clauses** from four forbidden assignments per cubic parity vertex, binary encoded source size $N=\Theta(H\log H)$. Parity sum proves UNSAT. Urquhart, *Hard Examples for Resolution* (JACM 1987, DOI 10.1145/7531.8928), and Ben-Sasson/Wigderson, *Short Proofs Are Narrow* (JACM 2001, DOI 10.1145/375827.375835), establish restricted ordinary Resolution hardness via appropriate expander/width assumptions, **not all-algorithm hardness**. Small K4 in the finite test is a structural control only, not an asymptotic lower-bound instance. GF(2) summation and algebraic shortcuts remain legal upper-bound controls under their specified models; a short GF(2) argument does not by itself authenticate any mixed R_mix341 proof rule.

**Open after this run:** P2-A2 / P2-A5 require a full solver-dependent, exponent-oblivious, recursively iterable all-input SAT decomposition giving $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ in the same fully charged FLMV machine. P2-A4 must account for every intermediate child/source, local operation, writable high-water and copying. Route B's native grammar authentication, unrestricted shared mixed-calculus proof-size bound and noncircular same-$R$ B3 remain OPEN. P versus NP OPEN.

**Tracker decision:** This typed program optimization changes no load-bearing dependency, status or transfer gap. Both full tracker heads are checked again after publication. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No agent, schedule, enabled state, Route A/B assignment, R_mix341 grammar/weights or other role-owned manuscript region was modified.

# LSPV-2/471: Dense INPUT-INDEX representation cannot inherit FLMV WORK-space bounds

**2026-11-07 08:19 PST | Route A | PROVED/RESTRICTED transfer falsifier; COMPUTATIONAL tests; P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** LSPV-2/468's dense Fenwick-backed INPUT-INDEX macros have a legitimate space bound in the *guest INDEX-head high-water* H, but this does **not** imply the space bound needed in the original FLMV machine's charged non-index WORK usage S. The live proof2.txt [P2-A4] sentence treating INPUT-INDEX high-water as counted guest space is false for the original model.

Before sources, four falsifiers: (F1) FLMV §2.1 actually counts INDEX head positions as WORK space; (F2) the /468 direct WORK-indexed flag/Fenwick arena never visits the high guest INDEX position; (F3) an INDEX-only prologue cannot restore INPUT/INDEX before running an arbitrary decider with just logarithmic extra WORK; (F4) our proof incorrectly excludes source-aware simplification or a separate native-INDEX simulator.

**Read/reviewed:** complete proof1.txt initial blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, complete proof2.txt initial blob `390b55471df24fb20c0a49879da1f9ee41717e55`, issue #3, AGENTS.md (`19656af1`), CODEX.md (`754999f5`), repo research skill (`b8df83a7`), Nov. 2 handoff (`c3889a3e`), LSPV-2/468 (`784206b7`), /469 (`32f118a3`), /470 (`b1567c04`), peer LSPV-4/469 (`5a14c68a`), /470 (`12a09e9a`), GROKPROOF/2026-11-07_1220_PROGRESS.md (`2c450bb3`), Claude world-ledger source (`79e4d4e7`). A guessed latest handoff and a guessed generic LSPV-4 report returned 404; actual file directory inventory and direct report reads succeeded. Root main.tex was not edited without an authenticated complete source read.

**Primary sources:** [FLMV, Time-Space Lower Bounds for Satisfiability, JACM 52 (2005), §2.1, printed p.4](https://lance.fortnow.com/papers/files/tst.pdf), read as text and visually as a PDF page; INDEX contents are erased by an indexed move and only non-index tapes (excluding input/output) contribute their maximum accessed position to charged space. Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), provide only **ordinary Resolution** hard-family controls.

Authenticated external files inspected with exact git blobs: `konard/p-vs-np/README.md` `0e0ec77f` and `proofs/complexity/README.md` `7ee9a11e` (finite-machine P subset NP, not the general question); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea` and `INDEPENDENT_AUDIT.md` `b30515cc` (conditional promise methods); `meelgroup/frat-xor/format.md` `986a21aa` (distinct certificate format); `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` `4bb5fd19` (published family generator); `openai/math/README.md` `cc5b0a03` (mixed verification statuses). Public research search performed; no separately authenticated Google-branded search. None proves the universal transfer.

## Theorem 471.1 (PROVED/RESTRICTED): a space-transfer falsifier for the exact /468 dense port

Conditionally assume a fixed deterministic **total correct** CNF-SAT decider A exists, with time `T_A(B)=O(B^{t+o(1)})` and charged WORK high-water `S_A(B)=O(B^{s+o(1)})`. For any fixed integer `k>max(1,s)`, form a fixed uniform decider `D_k`:

1. Compute H=B^k using a clock costing O(log B) extra WORK and polynomial time.
2. On the associated INPUT INDEX tape, walk to position H and write a one. There is no corresponding non-index WORK read or indexed WORK move.
3. Execute one indexed INPUT move, which erases the INDEX contents. Rewind its sequential head to zero if needed. Execute a blank-address indexed INPUT move to restore the read-only INPUT head to zero.
4. Run A in its ordinary initial configuration. Return A's result, including the malformed-input label.

The preparatory steps use O(B^k polylog B) time and O(log B) counted WORK; hence **every binary input** is classified exactly as by A, and

$$
T_{D_k}(B)=O(T_A(B)+B^k\operatorname{polylog}B),
\qquad
S_{D_k}(B)=O(S_A(B)+\log B).
$$

Despite the charged WORK bound, the **guest INPUT-INDEX head high-water** is H=B^k. The specific LSPV-2/468 implementation stores each guest INPUT-INDEX bit at a direct-addressed host *non-index WORK* flag slot with corresponding Fenwick metadata. Its write at guest INDEX coordinate H therefore touches host WORK coordinate at least H. Erasing the guest INDEX afterward cannot undo peak space:

$$
S_{\rm dense\ host}(B)\ge B^k.
$$

Take the target child size B=N^{1/2} on the integer subsequence N=B^2. The Route A target for the original guest space exponent s is N^{max(1/2,s/2)+o(1)}=B^{max(1,s)+o(1)}. Because k>max(1,s), this **particular** dense encoding violates the desired space transfer. Increased guest runtime exponent does not relax the independent space target.

**Scope:** This does **not** refute a general A -> Phi(A), any native INPUT-INDEX implementation, or static code analysis removing the deliberately useless prefix. It does **not** invalidate /468's theorem stated with guest INDEX-high-water H:

$$
S_{\rm port}=O((H+1)\operatorname{polylog}(B+T+2)+\log N).
$$

It **falsifies the additional inference** that H is measured guest WORK space in FLMV §2.1. The distinct LSPV-4/470 canonical-radix *live payload* obstruction reinforces this concern for another representation, but the current theorem directly audits the LSPV-2/468 dense array and resets the guest's INPUT to ensure full behavioral preservation.

## Independent finite controls

Exact published Node program: `experiments/arc/lspv2_471_dense_index_transfer_falsifier.cjs`. **144 assertion groups passed**, 9 B values 4 through 96 for k=2, physical dense flag/Fenwick arrays, modeled INDEX erasure and head restore, 16 strict signed 3-CNF K4 Tseitin charge configurations (8 SAT, 8 UNSAT), 5 malformed encodings rejected. Independent Python: `experiments/arc/lspv2_471_independent.py`, **33 checks**, 10 independent B controls, 7 symbolic exponent controls, all 16 K4 charges verified against full edge assignments. These are host-language semantic checks and do not claim native FLMV simulation or finite asymptotic hardness.

Raw: `results/raw/arc/2026-11-07_0819_LSPV2_471_DENSE_INDEX_RAW.json`, with original-code SHA256 `a2765b4a134e047dc7afa5631f8dbe1830dd814d9eb00fe643756f710f85c355`. Complete Python raw and expanded proofs are in the independent reproducibility archive.

## Hard-family / theorem / known-method / missing-transfer ledger

An odd-charge connected simple cubic expander Tseitin source has H vertices, 3H/2 edge variables and 4H strict proper ternary clauses. At each vertex v, for its three incident edges, include the four clauses falsified by local assignments with parity different from charge b_v; total XOR of charges odd guarantees UNSAT. Binary-encoded size N=Theta(H log H). Known width-expansion arguments imply exponential **ordinary shared-DAG Resolution** refutations for suitable expander graphs, not all-system R_mix341 or arbitrary-machine hardness. GF(2) Gaussian elimination provides a polynomial-time upper-bound shortcut. K4 tests verify labels only, not growing proof hardness. Cook ER and Haken PHP remain mandatory controls.

Logical nodes, proof bits, proof checking: not applicable to this INDEX representation witness. Guest clock, source access, INDEX moves, erasure, rewind and parsing delegated to A are charged in the argument. Dense host flags, Fenwick, resize, address construction and all-stage peak are explicitly **not free**; one high WORK coordinate already proves the lower bound. The valid /468 INDEX-coordinate bound is retained. The erroneous substitution H<=S_guest is FALSIFIED/RETIRED.

**Tracker IDs:** repair [P2-A4]; [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-B2] remain OPEN. Preserve the five existing agents, two Route A / three Route B allocation, schedules and historical R_mix341 grammar/weights. Do not equate a restricted macro obstruction with a universal lower bound.

**Remaining gap:** a fully charged same-machine virtual INPUT implementation respecting uncharged guest INDEX state, then an effective **all-input recursively iterable** solver-dependent contraction for every total correct polynomial SAT decider. Universal Route A and Route B B3 remain OPEN; P versus NP OPEN.

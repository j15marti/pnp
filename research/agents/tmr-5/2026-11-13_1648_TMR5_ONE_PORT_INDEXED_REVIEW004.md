# TMR-5/004: one-port indexed equality shortcut and DI5 independent review

**Date:** November 13, 2026, 16:48 PST (America/Los_Angeles). **Role:** TMR-5, new Machine Bottleneck Redteam and whole-document synthesis. Repository: j15marti/pnp, main.

**Exact status:** New TMR5-SI4 one-port construction **CANDIDATE pending TMR-1/TMR-3/TMR-4 independent proof review**. Independent support for original TMR-3/005 two-port upper **PROVED/RESTRICTED at its expressly persistent-INDEX interface**, with the remaining physical machine implementation caveat below. Finite tests **COMPUTATIONAL**. The unrestricted all-exponent 3-SAT lower bound and P versus NP are **OPEN**.

## Target and independently strengthened lemma

TMR-3/005 claimed a fixed, total, correct 3-SAT machine with TWO charged persistent input-index ports that authenticates the original strict proper 3-CNF equality family $E_n(a,b)$ with $T=O(L)$, $S=O(\log L)$. This review attacks the number of ports: **one persistent indexed input register suffices** when every switch, address rewrite, source read, parser operation and persistent shadow is charged.

Let

$$
w_n=\max(1,\lceil\log_2(5n)\rceil),\quad
g_n=12(1+w_n),\quad h_n=13n+2,\quad
L_n=h_n+2ng_n.
$$

$E_n(a,b)$ has $N=5n$ original variables, $M=8n$ strict proper ternary clauses and is SAT iff $a=b$. This is the SAME binary original-source family, not a chosen alternative encoding.

**TMR5-SI4 candidate theorem.** In the explicitly specified **non-erasing, persistent single-INDEX input interface**, there exists one fixed finite deterministic total machine $B$ handling all binary strings, with correct SAT/UNSAT output for every valid 3-CNF and a defined malformed-input response, such that for every $n\ge1$ and $a,b\in\{0,1\}^n$,

$$
T_B(E_n(a,b))=O(L_n),\qquad S_B(E_n(a,b))=O(\log(L_n+2)).
$$

Only one read-only input query port and one charged persistent binary INDEX tape are allowed. Every bit change, index-tape head movement, work tape, shadow cursor, formula parser, output, and fallback is charged. This is **not** the erasing-INDEX model of Fortnow et al. [1]. It is also **not** a physical sequential input-head model; no claim transfers its upper bound to that model without simulation costs.

### Construction and real-resource charge

The program scans the unary $1^{5n}0\,1^{8n}0$ header and all original literal bits, verifying every expected identifier, sign row, auxiliary ID, clause width, position and endmarker. The main source cursor uses paid binary increments. On second-bank block $i$, before resuming the scan, the program saves its main cursor, changes the ONE INDEX register to $h_n+ig_n$, reads the first-bank sign bit, updates the equality flag, and restores the main cursor. It stores only the current block sign, two shadow addresses, the physical INDEX register, a few counters and flags; it never stores the $n$ first-bank signs. It finishes authentication even after an early mismatch.

There are exactly $L_n+1$ main queries including endmarker, $n$ anchor queries and $2n$ remote/main context switches. Scanning consecutive binary addresses with a moving ordinary tape head has total charged carry-and-return work $O(L_n)$, since

$$
\sum_{t=1}^{L_n}(1+\nu_2(t))=O(L_n).
$$

Each context switch copies at most $O(\log L_n)$ bits between a charged shadow tape and the single INDEX register. The $n$ anchor strides also cost $O(\log L_n)$ apiece, with binary arithmetic charged. Verification of $\Theta(n)$ explicit literals of $\Theta(\log n)$ bits costs $O(n\log n)=O(L_n)$. Therefore

$$
T_B(E_n(a,b))
 =O(L_n+n\log(L_n+2))=O(L_n),\qquad
 S_B(E_n(a,b))=O(\log L_n).
$$

All constants are machine-dependent, not input-dependent. On nonmembers the program restarts a fully paid standard parser and exhaustive deterministic SAT decider; it rejects malformed inputs and correctly classifies every other valid 3-CNF. Off-family running time may be exponential. This is a single fixed all-length program, not length-dependent advice, and neither a polynomial general SAT algorithm nor an oracle.

**Erasing-INDEX variant.** When every indexed source query erases its INDEX tape as in [1], an actual non-erasing register cannot be assumed. Instead reconstruct it from the paid binary shadow in $O(\log L_n)$ work before each of the $O(L_n)$ queries. This yields $T=O(L_n\log L_n)$ and $S=O(\log L_n)$ on the same family, not the one-port persistent $O(L_n)$ bound. Both violate an overhead-free importation of TMR-3/002's physically sequential $T(S+1)=\Omega(L_n n)$ to indexed access for sufficiently large $n$.

### Independent audit of TMR-3/005 and scope

The original report and exact published two-port JavaScript, its immutable raw data, TMR-1/004's indexed-to-sequential paid bridge, TMR-3/002's physical two-way crossing theorem, and TMR-2/001 equality source were inspected. TMR-3/005 correctly distinguishes persistent address tapes from erasing INDEX tapes. The one-port program here provides a stronger independent constructive witness under precisely the same persistent-index conventions, and preserves both labels, all-length total fallback, exact original input length, and same-machine time/space. This **does not** establish an unrestricted random-access or physically sequential SAT time lower bound.

The project corpus also contains TMR-2/005 affine clause-minimal UNSAT controls, TMR-1/003 polynomial fast-path islands, and historical LSPV-5/510-511 genuine accepted-byte checker counterexamples; none may be excluded from unrestricted MAY-machine abstractions merely because they bypass a proposed representation. Full proof1/proof2 and main.tex were recovered through authentic Git blobs; the root operating instructions and five latest handoffs were inspected, as were current issue #3 updates. Superseding TMR directive was checked before writes.

### Controls, provenance and actual execution

A new independent JavaScript emulator was authored from scratch, not a wrapper calling TMR-3/005. Its exact published standalone source was executed directly in hosted V8 this run, with the same bytes subsequently published on main and verified by GitHub readback. It models a SINGLE persistent indexed port with paid context switches, cursor restoration, anchor reads, bit-level carry counts, source authentication and off-family rejection.

- **1,415** valid exact sources, including **85 SAT** and **1,330 UNSAT** cases, with exhaustive ordered $(a,b)$ pairs for $n=1,\ldots,5$ and seeded/large cases to $n=2048$.
- **7,075** malformed or structurally altered source controls rejected, including truncation, extra suffix, unary-header damage and auxiliary sign tampering.
- **14,150** completed assertions; **0** failures.
- **16,556** anchor queries; **33,112** paid remote/main context switches.
- Maximum original input length **763,906** bits. Maximum emulator charged-proxy ratio **17.6815** units per original bit; this is a proxy, **not** an actual multitape transition count.

**Execution limitations:** This was hosted V8 semantic and paid-address emulation. The full exhaustive fallback was established symbolically, not instruction-simulated. OS Node, physical TM execution, full repository preflight, LaTeX compilation and the independently supplied published TMR-3/005 executable were **not** run. The latter was retrieved and inspected; local operating-system Internet access prevented downloading its source for a native replay. The emulator uses finite JavaScript Number arithmetic for tested $n$, while the asymptotic mathematical machine uses unbounded charged binary tape arithmetic. Finite tests alone do not prove any asymptotic bound.

Source: \`experiments/tmr/tmr5_single_port_indexed_review004.cjs\` (exact V8-executed source).
Raw: \`results/raw/tmr/2026-11-13_1648_TMR5_SINGLE_PORT_INDEXED004_RAW.json\`.

### Dependency synthesis and next obligation

**Strongest surviving implication:** Input geometry can force a polynomial time-space product on a physical sequential input-head machine, but one **paid** persistent indexed input port defeats this transport product at small logarithmic space on the exact same easy original-source family. Two indexed ports are not essential to that escape. Original indexed-to-sequential simulation necessarily pays translation overhead; neither family proves hard unrestricted SAT computation.

**OPEN load-bearing arrow:** Establish an unavoidable **whole-execution**, representation-independent, program-dependent resource cost for every fixed correct total 3-SAT machine, at every polynomial exponent, surviving all indexed/reread/recompute methods, compact GF(2), Horn/2-SAT, bounded treewidth, auxiliary reencoding, padding and polynomial fast paths. TMR-4 must prove all-transition cost soundness and edgewise potential lower bounds; nothing here supplies a superpolynomial initial potential. A fully proved general polynomial SAT algorithm would be an equally valid outcome.

**Required peer review:** TMR-1 or TMR-3 must independently verify the one-port switch-and-restore amortization, exact grammar recognition, one-program/all-length fallback, and physical-cost translation. Leave the new theorem CANDIDATE pending that review. Review the erasing-index model separately.

## Primary literature and original sources

[1] Fortnow, L., Lipton, R., van Melkebeek, D., and Viglas, A. *Time-Space Lower Bounds for Satisfiability.* Journal of the ACM 52(6), 835-865 (2005). DOI: https://doi.org/10.1145/1101821.1101822. Section 2.1 in original author PDF https://lance.fortnow.com/papers/files/tst.pdf explicitly **erases** the index tape on each jump. Theorem 1.1 excludes selected $(n^c,n^d)$ bounds with $c<(\sqrt5+1)/2$, not arbitrary polynomial time.
[2] Hennie, F. C. *Crossing Sequences and Off-Line Turing Machine Computations.* 1965. Primary NASA bibliographic record https://ntrs.nasa.gov/citations/19660035639; the classical approach assumes physically local sequential head movement.
[3] Internal original: TMR-3/002 \`research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md\`, TMR-3/005 \`research/agents/tmr-3/2026-11-13_1620_TMR3_DUAL_INDEX_LINEAR_ESCAPE005.md\`, TMR-1/004 \`research/agents/tmr-1/2026-11-13_1558_TMR1_INDEXED_SEQUENTIAL_MODEL_BRIDGE004.md\`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No proof1.txt/proof2.txt or historical source rewritten. No task, title, schedule, or agent changed.

# LSPV-4/487 | Fully charged native indexed-input escape on canonical K4 equality 3-CNF
**November 7 2026 PST | Route A resource audit | PROVED/RESTRICTED + COMPUTATIONAL; P vs NP OPEN.**

**Nodes:** [P2-A2], [P2-A4], [P2-A5] and cross-chain [P1-01], [P1-03], [P1-04] reviewed. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The result quantifies a native indexed-access escape already explicitly anticipated in LSPV-4/486, not a changed global theorem or status.

## IDEA -> SEARCH -> ITERATE
Hypothesis: An authenticated, canonical original signed K4 equality family admits indexed-input SAT/UNSAT decision in $O(N\log^2N)$ time, $O(\log N)$ WORK+INDEX space on the original FLMV model. This falsifies extension of LSPV-4/486's source-streaming time-space obstruction to indexed machines. It does NOT imply a universal SAT solver.

Precommitted falsifiers: (F1) the source clauses fail $F_{A,B}$ SAT iff $A=B$ or have a wrong model count; (F2) authentication needs simultaneous $\Omega(w)$ bits; (F3) regenerating the INPUT INDEX and saving heads incurs hidden polynomial WORK usage or superlinear per-bit overhead; (F4) the sequential-communication lower bound still applies with indexed jumps. The exact local proof and independent finite clause tests exclude F1. Explicit one-packet-anchor verification excludes F2. The source/index/head construction below excludes F3. The disjoint hypotheses of the streaming and indexed models dispose of F4.

Continuity actually read: both complete current root trackers, issue #3 and latest peer comments, historical November 2 five-role handoff, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md, LSPV-4/486 and /485, LSPV-2/480 and /485, GROKPROOF/2026-11-08_0320_PROGRESS.md, and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Claude's older one-tape crossing-sequence theorem precludes novelty claims for sequential equality restrictions.

Primary authority: Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6) (2005), 835-865, Section 2.1 and Corollary 5.8, https://lance.fortnow.com/papers/files/tst.pdf. Its INPUT tape is read-only and excluded from measured space, while INDEX tape and WORK tapes and their head positions are charged. One indexed INPUT jump takes one machine step after the binary address has been written to the associated INDEX tape, which is then erased. Our analysis **pays to regenerate addresses** and does not pretend random access is a cost-free oracle.

Targeted external sources inspected with actual file/commit blobs: konard/p-vs-np README.md 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 (P subseteq NP only in finite model); blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93 (no universal plan acquisition); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (different proof grammar); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean 1ced21f44ad49370d1b812e862c03c3a91d7f836 (charged narrow SAT search, no universal contraction). General web/primary searches completed; no separate Google-branded client. No reliance on claims from research repository titles.

## Original signed source, exact model count
For $w\ge1$, the graph is $w$ disjoint labelled K4 graphs, component $j$ with six original edge variables having IDs $6j+1,\dots,6j+6$: edges 01,02,03,12,13,23. Vertex-ordered edge triples: $V_0=(01,02,03)$, $V_1=(01,12,13)$, $V_2=(02,12,23)$, $V_3=(03,13,23)$. At vertices 0 and 1, the four signed proper width-three source clauses forbid all triples with first-edge bit $1-A_j$ and $1-B_j$, respectively; the other two forbidden bits range in order 00,01,10,11. At vertices 2 and 3, forbid odd-parity triples 001,010,100,111. The original clause for forbidden triple $z$ uses positive literal when $z_h=0$ and negated literal when $z_h=1$. No clauses are inferred or omitted.

The $16w$ clauses are written in four groups $V_0$ through $V_3$, ordered by $j$ and forbidden triple. The binary source consists of Elias gamma($w$), followed by three $(sign,ID)$ fields per clause, sign 1 bit and ID $L=\lceil\log_2(6w+1)\rceil$ bits. Exactly
$$
N=2\lfloor\log_2 w\rfloor+1+48w(L+1)=\Theta(w\log w).
$$
For every $j$, vertices 0/1 both force shared original edge $x_{j,01}$ to their prescribed $A_j$ and $B_j$; inconsistent if unequal. If equal, after fixing this one edge, the two independent parity constraints at vertices 2 and 3 on five remaining edges leave $2^{5-2}=8$ models. Thus **PROVED/RESTRICTED** original signed-3CNF satisfiability iff $A=B$, with exactly $8^w$ models in the SAT case.

## Indexed physical algorithm and all-phase costs
One fixed deterministic program first discovers input length $N$ by scanning INPUT, parses gamma($w$), validates $w\ge1$, computes $L$, verifies exact encoded length. It scans all 48w literal fields, maintaining counters $(v,j,r,h)$, each current packet's one forbidden-first-bit sign, and expected ID $6j+e$. Packet header, every original sign, every literal ID, clause order and count are authenticated with no materialized formula or arrays A/B. Invalid binary/gamma/length yields MALFORMED; a well-formed source with inconsistent packet structure yields OUT_OF_FAMILY; both are distinguished from authentic UNSAT. The latter classification is NOT a solution to arbitrary CNF.

After authentication, compare first-sign bits of vertex-0 and vertex-1 packets at INPUT addresses
$$
a_j=g+12j(L+1),\quad b_j=g+12(w+j)(L+1),
\qquad g=2\lfloor\log_2w\rfloor+1.
$$
Prepare each address in binary on the native INPUT INDEX, jump and read the input bit, then explicitly rewrite an address for the next jump after the index tape is erased. A single disagreement determines UNSAT; otherwise SAT. Index jump and all scratch/head restoration costs are counted.

**Theorem 487.2 (PROVED/RESTRICTED, symbolic native machine construction):**
$$
T(N)=O(N\log^2 N),\qquad S(N)=O(\log N).
$$
Proof: $O(N)$ source bits/fields read; grade-school binary address and expected-ID construction costs at most $O(\log^2N)$ per field, and $2w$ indexed jumps cost at most $O(\log^2N)$ each including address reconstruction. The only simultaneous live WORK and INDEX contents, binary counters, heads and address arithmetic use $O(\log N)$ cells and no WORK position past $O(\log N)$. Read-only INPUT does not count toward native space. No uncharged child, guest, learned lemma, cache or materialized table exists. $N\log^2 N=N^{1+o(1)}$, hence eventually meets the nominal *local* $N^{11/10}$ time envelope. No actual native FLMV instruction-level emulator has been run. This only shows a specific fixed-family native implementation exists mathematically.

## Independent finite execution
Published independent JavaScript experiments/arc/lspv4_487_indexed_equality_audit.cjs blob e6ba182601bc27baa2ee6c4e48337e9ce70b7130: 20 original signed source cases w=1,2 exhaustively evaluated; 89 assertions PASS, 35 malformed/sign/ID negative controls, source/parser original-clause model counts 8 and 64 on equal pairs, zero otherwise. Re-fetched exact published JS and executed unchanged in V8; raw recomputation matched committed results/raw/arc/2026-11-07_2236_LSPV4_487_INDEXED_EQ_RAW.json blob 3392aeef72f75a12276b241e0c004076bdd811ea. An independently authored Python program repeated all original-clause brute-force checks and reported 91 PASS assertions, 36 negative controls, no failures. These finite programs are not executions of an authoritative FLMV machine or native R_mix341 checker.

Resource ledger: Source parsing and authentication $O(N\log^2N)$ time, $O(\log N)$ live; indexed random source reads $O(w\log^2N)$ time, $O(\log N)$ INDEX; no failed policies, precomputed semantic hints, child ports, source conversion, guest A, caches, ancestor buffers, certificate construction or retained outputs; final one classification bit; all-phase peak $O(\log N)$. Proof-bit cost, mixed proof-DAG work/span and branch/scope obligations are N/A: no R_mix341 certificate is claimed. Local logical XOR is not treated as an executable SAT oracle.

Hard-family contrast: connected cubic epsilon-expander odd-charge Tseitin has $4H$ original signed width-three clauses, $3H/2$ edge variables, encoded size $\Theta(H\log H)$, and $2^{\Omega(H)}$ ordinary shared-DAG Resolution lower bound under the established conditions (Urquhart 1987; Ben-Sasson and Wigderson 2001). GF(2) provides a fast semantic shortcut, not a Resolution refutation. The disjoint K4 equality family here is explicitly an **easy targeted falsifier/control**, NOT a new proven hard growing family. No lower bound is transferred to the whole mixed calculus or arbitrary algorithms.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Earlier /486 already recorded the existence of this indexed escape, so no redundant [P2-A4] tracker update. No edits to main.tex, fixed R_mix341 grammar/weights, roles, IDs, five task schedules, enabled states or 2 Route A/3 Route B assignment.

**Actual advance:** Complete native indexed-input source-parsing and head/resource audit for the precise /486 streaming escape, with independent original-source controls. **Verification:** restricted mathematical construction and independent finite code/readback PASS; native machine instruction-level replay unavailable. **Publication:** role-owned report/code/raw/handoff published; issue #3 coordination updated. **Remaining gap:** an ALL-INPUT effective recursively iterable A-to-Phi(A) transformation on the *same* FLMV machine satisfying $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$, including SAT/UNSAT/malformed and all guest/construction costs. [P2-A2], [P2-A5], Route B B3 and mixed-system lower bound OPEN. **P versus NP OPEN.**

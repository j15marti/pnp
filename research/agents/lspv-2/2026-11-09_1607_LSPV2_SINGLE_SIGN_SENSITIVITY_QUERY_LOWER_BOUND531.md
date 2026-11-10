# LSPV-2/531: every literal polarity is label-sensitive in 2-connected cubic Tseitin 3-CNF
**2026-11-09 16:07 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Relevant tracker nodes:** new evidence [P2-L2-531], related [P2-L2-519], [P2-L2-520], [P2-L2-530]. OPEN: [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2], B3.

## IDEA, falsifiers, SEARCH, ITERATE
**Hypothesis:** A signed-source authentication cost remains even when native GF(2) algebra gives a cheap Tseitin contradiction: each source literal polarity may affect SAT/UNSAT.

**Falsifiers specified before testing:** F1, one flipped sign leaves a 2-vertex-connected source UNSAT; F2, a claimed SAT witness violates another original clause; F3, the single sign edit changes proper 3-CNF syntax or encoded length; F4, the claim incorrectly includes graphs with cut vertices. F1-F3 were excluded by proof and independent controls; **F4 is real**: 12 of 120 edits fail to make an adversarial cubic cut-vertex graph SAT.

**Pre-existing result:** Minimal unsatisfiability of odd-charge Tseitin CNF on 2-connected graphs was proved explicitly by Emil Jeřábek in a February 2024 answer, https://cs.stackexchange.com/questions/166831/tseitin-formula-on-2-connected-graph . The theorem below is a fixed-width input-bit *query-complexity corollary* of this known minimality property, **not a novel claim to minimal unsatisfiability**. Ben-Sasson and Wigderson, JACM 48(2) 2001, give exponential **ordinary Resolution** size for suitable expander Tseitin contradictions; no unrestricted computational bound follows. ACDCL (D'Silva, Haller, Kroening, POPL 2013), Abstract Satisfaction (POPL 2014), complete shells (Giacobazzi et al., JACM 2000), CEGAR and cost-sound overapproximation provide methodology, not the missing Route A theorem.

Read complete governing November 9 handoff (blob `8a6fd9f5`), root trackers (`proof1.txt` blob `96aefb3dce07`, startup `proof2.txt` blob `d12292f2c768`), issue #3, AGENTS.md, CODEX.md, project skill, previous LSPV-2/528-530, LSPV-1/547, LSPV-5/470, Grok 2026-11-09_2015_PROGRESS, Claude WORLD-LEDGER-0001, and MODELBRIDGE-0010. Exact change-aware source files: `konard/p-vs-np:scripts/proof_status.json` (`93b77ed3`); `blkph0x/p-vs-np-proof-research:METHOD_INDEX.md` (`18d693ea`); `MassimoLauria/cnfgen:cnfgen/families/tseitin.py` (`4bb5fd19`); `openai/math:README.md` (`cc5b0a03`); `marijnheule/drat-trim:README.md` (`eb6ffcc4`). The CryptoMiniSat README fetch failed with a remote protocol error. Literature search used general web search, not an independently authenticated Google index.

## Family, encoding, and scope
Let $G=(V,E)$ be a simple connected 3-regular graph on $h$ vertices, with $G-v$ connected for **every** $v$. There is one original SAT variable for each edge, $n=3h/2$. Let vertex charges $b_v\in\mathbb F_2$ have odd total XOR. Each vertex parity equation is encoded by the **four proper signed 3-clauses** that forbid its wrong-parity incident assignments. Total clauses $m=4h$ and independent literal-sign slots $Q=12h$.

For the **asymptotic theorem**, each signed literal has one independent sign bit and a variable identifier of width $\lceil\log_2(n+1)\rceil$ bits plus a self-delimiting header: $N=\Theta(h\log(h+2))$. Every sign edit is exactly one bit and leaves the binary input length and strict 3-CNF validity unchanged. The *finite verifier* instead uses fixed 32-bit IDs in `S3C1`, giving $12+60h$ bytes; this bounded-ID container is **not** silently used as an infinite-size encoding.

## Theorem 531.1: single-sign SAT sensitivity (PROVED/RESTRICTED)
For **every** such $(G,b)$, its original Tseitin 3-CNF $F$ is UNSAT, but flipping **any one** of its $12h$ literal-sign bits produces a SAT proper signed 3-CNF $F_{i}$.

**Proof.** Summing all vertex parity equations cancels every edge and contradicts the odd total charge. Fix any source clause $C_{v,a}$, falsified by a three-edge assignment $a$ of parity $1\oplus b_v$. Freeze those three incident edges. Delete $v$; the adjusted charges on the connected graph $G-v$ sum to
$$
\bigoplus_{u\ne v}b_u\ \oplus\ \bigoplus_{e\ni v}a_e
=(1\oplus b_v)\oplus(1\oplus b_v)=0.
$$
The incidence parity system on a connected graph has a solution iff charges sum to zero, e.g. solve on a spanning tree. It yields a full assignment satisfying all source clauses except $C_{v,a}$, whose unique falsified pattern is $a$. Reversing **any single sign** in $C_{v,a}$ changes its unique falsifying pattern to a different three-bit assignment; the constructed assignment now satisfies this clause too. No other clause changes. QED.

## Theorem 531.2: cost-sound read-query lower bounds
On original $F$, any **deterministic** correct all-input SAT algorithm that reads independently encoded sign positions through paid bit queries must query **all** $Q=12h$ positions. An unqueried position could be flipped with no change to any observed bit, forcing the same computation and wrong answer on a SAT $F_i$.

For **randomized** bounded-error ($\le1/3$ on each input), use the distribution placing mass $1/2$ on $F$ and $1/(2Q)$ on each $F_i$. A deterministic tree querying $q$ sign slots on $F$ has average correctness at most $1/2+q/(2Q)$ (at most $1/2$ if it misclassifies $F$ already). Averaging over coins yields
$$
\mathbb E[\text{distinct sign-bit queries on }F]\ge Q/3=4h.
$$
This holds irrespective of downstream Resolution, CDCL, XOR, RAT, auxiliary definitions or shared computation **provided the input interface is this independent-sign-bit query model**. It does not hold when supplied an external authenticated digest, a promise-only input interface, a nonuniform precomputed answer or differently charged source representation.

A sound cost abstraction can use the number of distinct queried polarity bits as a potential $V$. An actual paid single-bit read increases $V$ by at most one; a correct deterministic terminal UNSAT state on $F$ must have $V\ge12h$. The MAY abstraction must include every concrete transition and must charge batch reads by the number of bits read. Thus budget $B<12h$ excludes this **specific** correct source-query execution. It is NOT a lower bound on R_mix341 inference nodes, proof search or general SAT computation beyond the model; a linear scan and GF(2) elimination remain efficient.

## Independent verification and hostile controls
Original signed strict 3-CNF generation and binary-source SHA-256 authentication were implemented independently in Python (GF(2) witness solver) and Node.js (exhaustive assignment enumeration, no Gaussian elimination). The programs match **all five canonical SHA-256 fingerprints**, perform exact one-bit-edit comparisons, reject **six malformed binary sources per graph**, and directly check every SAT witness against the whole modified source. Python additionally exhaustively checked **216 modified formulas** on the three smallest graphs; Node independently enumerated **70,208 complete assignments** across all five graphs.

| Graph | h | Sign bits | SAT after one flip | SHA-256 prefix |
|---|---:|---:|---:|---|
| K4 | 4 | 48 | 48 | `911c4ef063b1` |
| triangular prism | 6 | 72 | 72 | `7b68e4dd33d3` |
| cube | 8 | 96 | 96 | `4df8543b5c22` |
| Petersen | 10 | 120 | 120 | `ecc271654f84` |
| cut-vertex cubic bridge | 10 | 120 | **108** | `41ff89a5472c` |

**Total independently authenticated SAT mutations:** 444. All original odd-charge sources are UNSAT. Even-charge SAT controls are valid. A separately executed compact V8 verifier reproduced 444 cases (without cryptographic hashing). These finite controls do not certify expander hardness or asymptotic SAT difficulty.

**Resource ledger:** $4h$ clauses, $12h$ sign positions, source parse and hashing, six malformed cases per graph per implementation, independent full-scope witness replays, 70,208 enumerated assignments and 216 explicit brute-force formula checks. Python uses bit-vector GF(2) elimination; Node enumeration is exponential by design and serves only as an independent checker. No native FLMV machine measurement, same-machine ancestor-space bound or optimal proof-size claim.

**Established hard-family ledger:** odd-charge cubic expander Tseitin, original encoding above, suitable expansion => exponential ordinary shared-DAG Resolution size under Ben-Sasson-Wigderson (2001); XOR/GF(2) permits polynomial algebraic reasoning. The added vertex-deletion connectivity condition for /531 is not asserted for every expander in the literature. Neither this linear query bound nor restricted Resolution hardness implies general SAT runtime hardness.

## Outstanding transfer
[P2-A2], [P2-A4], [P2-A5] remain **OPEN**: no uniform, recursively iterable, malformed-aware, source-authenticated same-machine transform for **every** fixed polynomial-time SAT decider $A$ was produced with
$$
t'\le\max(11/10,3/5+t/2),\qquad s'\le\max(1/2,s/2).
$$
Historical native R_mix341 and B3 remain OPEN; MODELBRIDGE-0010 prevents treating a static normalizer as this missing arrow. This run does not change roles, schedules, historical weights, titles, or Route A/B allocation. **P versus NP OPEN.**

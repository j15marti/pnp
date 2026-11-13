% LSPV-4 REPORT::574::2026-11-12T18:36:00-08:00
# LSPV-4/574: Packed semantic-value storage changes the exact time-space optimum

**November 12, 2026, 18:36 PST (America/Los_Angeles) | LSPV-4 Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED fixed two-register semantic-value model; COMPUTATIONAL original-source audit | P versus NP OPEN.**

## One candidate theorem and four falsifiers

Candidate: replace the full compact JSON paid-node records retained by LSPV-4/573 with an explicitly invertible packed *semantic value*, without modifying the original archived /341 source, paid inference DAG, rule payments or certificates. Determine the exact optimum retained payload, fresh-output payload peak and slot area for the SAME restricted execution, and prove a uniform closed formula.

F1: LSPV-4/573's JSON-record-area optimum is a representation-independent physical-memory lower bound. **FALSE.** On original Prism16 its record-byte optimum is 23,836 byte-steps; the separate packed-value evaluator uses 1,346 byte-steps. Neither number is actual JavaScript verifier RAM.

F2: the record-byte-optimal /573 execution order also minimizes packed-value retention. **FALSE.** On Prism16 that order costs 1,348 packed byte-steps, while an interleaved trace costs 1,346 and uses 221 rather than 220 retained slot-steps.

F3: replacing a terminal AND3 factor with its compact affine row loses a needed later AND3 view, or the alias is semantically false. **Excluded for the seven original fixed trees.** Every terminal factor has only an XOR consumer. All 246 AND3 deductions, 82 affine aliases, and 75 XOR deductions were independently source-replayed.

F4: two post-step live atomic registers imply at most two value buffers while an inference executes. **FALSE.** Allocate-before-parent-release payload peak is 21 bytes on Prism16; this excludes decoding and actual scratch.

## Exact source and prior art

Read both root proof trackers (proof1 Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2 blob f678f707880da4dfc97dabf778430c6dc816cb1f recovered via Git blob), issue #3 including latest LSPV-2/586 and LSPV-5/514, AGENTS.md, CODEX.md, the research skill, /573 handoff, original archived /341 packet and verifier, and relevant LSPV-4/539, /548, /549, /571, /572, /573 and LSPV-3/416 artifacts.

Original packet: results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json, Git blob fe27fe1011d0021e721ccaeb747ed58da65d7464. Archived checker: experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. It is a partial SOURCE/AND3/XOR checker, **not the authenticated historical unified R_mix341 grammar**. The distinct /386 original checker cannot be silently combined.

Sethi-Ullman register ordering [1], prior LSPV-4/409 sparse-versus-dense evidence differences and LSPV-3/416 large-index issues were already known. The new mathematical result is the exact homogeneous packed-value area/peak theorem, its threshold and the change in the simultaneously optimal slot-area coordinate on the same original source fixtures. Beame and Kornerup [2] distinguish cumulative space from peak space, and Bilardi and De Stefani [3] provide generic DAG pebbling upper bounds in another model.

## SAME_REALIZATION model

For one original cubic graph with V vertices and E=3V/2 edges, the *fixed* paid tree has three local AND3 steps per vertex, then V-1 left-associated XOR steps. There are exactly four signed original SOURCE clauses per vertex; each local three-step AND3 chain combines these four premises. In every fixture the original certificate is read-only and the original SOURCE clauses are read-only. No paid inference may be recomputed. Every produced value is retained until its last application and then deleted. At most two paid values are live after a step. The output may atomically overwrite a dead parent, but the fresh-output peak measure conservatively allocates an output before parent release.

Write b=ceil(log2(E)). The first two local AND3 results are stored as one-bit type, eight-bit table and three ordered b-bit support indices, using F=ceil((9+3b)/8) bytes. A completed local AND3 factor is checked against the original packet and thereafter retained solely as its affine row, containing one-bit type, one RHS bit and E coefficient bits, using R=ceil((E+2)/8) bytes. All XOR results are similarly rows. Both encodings are invertible for the source-authenticated original support and mask ranges. Original proof objects, references, parser state, computation and conversion scratch are not included in this restricted *derived-value* area metric.

The fixed logical tariff is W=4V-1 unit paid inferences, the parent application count is 8V-2 and the dependency span is V+2. These are distinct from original serialized evidence, proof search and sequential verification.

For exact post-step live set L_t and step t's new paid node v_t, define

$$
A_{\mathrm{payload}}=\sum_{t=1}^{4V-1}\sum_{u\in L_t}w(u),\qquad
A_{\mathrm{slot}}=\sum_t|L_t|,\qquad
P_{\mathrm{fresh}}=\max_t\left(\sum_{u\in L_{t-1}}w(u)+w(v_t)\right).
$$

## Theorem 574.1: exact two-register packed-value resource frontier

For any V>=3 of these left-associated original paid-tree templates, with constant positive F for the nonterminal factor values and R for completed affine rows and XOR values, read-only original premises, no recomputation and at most two post-step live paid values:

$$
\boxed{
A_{\mathrm{payload}}^{*}=2FV+(5V-4)R-\max(0,2R-3F).
}
$$

For allocate-output-before-release *value payload only*, the exact minimum peak is

$$
\boxed{P_{\mathrm{fresh}}^{*}=\max(R+2F,F+2R,3R).}
$$

If 2R>3F, an area-optimal schedule has 7V-3 retained slot-steps rather than the slot-minimum 7V-4. When 2R<=3F, a byte-optimal DFS schedule attains the slot minimum.

**Proof.** Before the first XOR, at most two unfinished/completed local vertex chains can coexist, because every such chain needs a live factor/row and no recomputation is permitted. Two finished rows also force the first XOR before another chain can start. Finishing one full chain before the second and then XOR costs exactly 4F+6R post-step byte-steps and 10 slot-steps. Starting and advancing both chains through their first two factor deductions before completing either row and then joining costs 7F+4R and 11 slot-steps. All other legal two-chain interleavings have at least as many simultaneous factor checkpoints, and hence cannot improve on both of these for positive F and R. Therefore first-join area is 4F+6R-max(0,2R-3F).

After the first XOR, the R-weighted accumulator must remain live while each of the remaining V-2 local three-step chains is produced, followed immediately by its XOR join. That sequence's four post-step live byte totals are R+F, R+F, 2R, R, totaling 2F+5R. Adding the first-join minimum proves the area equation, and both alternative schedules attain it. They use respectively 10 and 11 first-join slot-steps, followed by the same fixed continuation, proving the slot-area statement. For V>=3, every allocation-before-release schedule must pass through R+2F (a subsequent intermediate factor), F+2R (a subsequent terminal local row), and 3R (a binary XOR with two rows live); these mandatory peaks are achieved by the exhibited schedules. Hence their maximum is the exact peak optimum. All work is counted once on this same fixed tree. QED.

The exact completed-paid-node-set DP gives a concrete-to-abstract path of *equal* cost for every concrete execution **within this precisely declared packed-value machine**, retaining node identity, representation, goal and paid count. This does NOT establish simulation of all historical mixed native rules or a cost bound on the actual original JavaScript checker.

## Source-backed results

| Original fixed fixture | /573 full JSON record area | Packed value area optimum | Packed area in /573 order | Optimum retained slots | Fresh payload peak |
|---|---:|---:|---:|---:|---:|
| K4 | 2,452 | **40** | 40 | 24 | 7 |
| K3,3 | 3,862 | **88** | 88 | 38 | 8 |
| Cube | 5,272 | **120** | 120 | 52 | 8 |
| Petersen | 6,751 | **198** | 198 | 66 | 9 |
| Prism6 | 8,211 | **240** | 240 | 80 | 9 |
| Prism16 | 23,836 | **1,346** | 1,348 | **221** | **21** |
| Bridged K4x2 | 6,724 | **198** | 198 | 66 | 9 |

The Prism16 packed optimum begins d0,d1,d3,d4,d2,d5,d96,..., retaining two small nonterminal factors before emitting two larger rows. For that fixture 2R=14>3F=12. All other original fixtures have 2R<=3F.

The hosted V8 source audit checked 1,968 source-based AND3 truth-table assignment cases, 656 terminal AND3 affine-alias assignments, 75 GF(2) XOR identities and 321 packed codec round-trips. All passed. A separately executed operating-system Python DP on the original universal tree incidence, implemented independently of the source packet parser, agreed on seven minima and all state/edge counts. A separate 225-case exhaustive (F,R) control grid on the 15-node V=4 tree agreed with the closed form.

The original seven fixture packet remains 77,714 bytes when compactly serialized with one newline and 197,514 bytes in its archived pretty-printed form. It consists of seven **separate** proofs totaling 321 paid occurrences and 642 parent applications; it is not one combined 321-node refutation. No original paid proof records were modified. An operating-system execution of the original /341 checker on a newly reordered packet and repository-wide preflight remain **outstanding**. The new Python executable performs the pinned-source structural and semantic checks when run with the complete repository checkout.

## Evidence and next blockers

Executable: experiments/arc/lspv4_574_native341_packed_semantic_area.py.
Raw complete optimal orders, values, costs and replay checks: results/raw/arc/2026-11-12_1836_LSPV4_574_PACKED_AFFINE_RESOURCE_RAW.json.
Coordination handoff: research/coordination/2026-11-12_1836_LSPV4_PACKED_AFFINE_FIVE_ROLE_HANDOFF574.md.

Exact fixed native weights for the **complete** historical R_mix341 remain unauthenticated. Other unproven charges include original evidence bits and reference decoding, source authentication, sequential verification and output buffers, all-phase memory, recomputation, branch contexts and joins, extensions, direct GF(2), learned shared clauses and private/exported wires. Alternative legal representations and shared-DAG reconvergence remain admissible. This theorem is one fixed-tree semantic storage upper-bound witness, not a physical-memory lower bound or any general SAT computation lower bound. The ideal W_R is not proof discovery cost, certificate verification cost or deterministic decision time.

**P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 separately OPEN; P1-01/P1-03/P1-04 OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE. P versus NP OPEN.**

## Primary literature

[1] Sethi and Ullman (1970), The Generation of Optimal Code for Arithmetic Expressions, J. ACM 17, 715–728. https://doi.org/10.1145/321607.321620.

[2] Beame and Kornerup (2023), Cumulative Memory Lower Bounds for Randomized and Quantum Computation. https://arxiv.org/abs/2301.05680.

[3] Bilardi and De Stefani (2024), A Universal Bound on the Space Complexity of Directed Acyclic Graph Computations. https://arxiv.org/abs/2410.20547.

[4] Ben-Sasson and Nordström (2010), Understanding Space in Proof Complexity. https://eccc.weizmann.ac.il/report/2010/125/.

% END_OF_VERIFIED_REPORT::LSPV-4::574

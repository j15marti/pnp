# LSPV-2/517 | Source-local Tseitin charge bits force full completed-read transcript separation

**2026-11-09 03:17 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof-chain nodes:** New restricted evidence [P2-L2-517] refines [P2-L2-516] and audits [P2-L2-515], [P2-L4-515], [P2-L4-516]. The load-bearing [P2-A2], [P2-A4], [P2-A5] stay OPEN; [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] stay OPEN. No R_mix341 native rule, proof weight, task or allocation was changed.

## IDEA -> SEARCH -> ITERATE

**Hypothesis before search.** In contrast to the one-exception selector family of LSPV-2/516, use an established *original proper 3-CNF* Tseitin charge family whose SAT/UNSAT label is parity of independently signed *source-local* charge bits. Then every correct deterministic all-input SAT decider must read at least one original bit from each charge group on **every** completed execution. Consequently the affine input-read matrix has rank k and all 2^k physical sources have distinct complete read-value transcripts. This is a restricted obstruction to the **exact full-transcript reuse** of /515, not an unconditional computational lower bound.

**Predeclared falsifiers.** (F1) An independently varied charge bit changes IDs, packet length, clause width or source syntax instead of exactly four signed literal positions. (F2) The decoded 3-CNF SAT truth table disagrees with the parity of charges, for even or odd charge assignments. (F3) A deterministic correct decider reads no bit in some locally variable charge block on some source, yet distinguishes that source from the source with that single charge flipped. (F4) A fixed packet contains an additional *global parity input bit* that could legitimately bypass local readings; this would falsify the claimed physical query restriction.

**Actual continuity read.** Complete current main-branch proof1.txt (Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (research-stage blob 9ad6edc54ae84b7c5d35bbdb5f2fb1860493ed07, 694237 characters), current issue #3 with recent role comments, governing 2026-11-02_1204 handoff (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md. Read actual LSPV-2/515 (blob 3c29ef7536316c1aa328f5c3a4e3ee866ca36412), LSPV-2/516 (blob 409f49e5322efa71a178544548e04528938dd16e), LSPV-4/515 (blob 801d1df31daa04b47bc3bfe2b8821dd0e069c137), LSPV-4/516 (blob 046320755c89dd3f863b7434c4be72a4f4bbcdf3), its five-role handoff and the new 2026-11-09 knot/topology five-role candidate handoff (blob 0289edb73d1e38492f0693844667be59d4152785). Independent work: GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70) and research/agents/claude/world-ledger/README.md (blob de75a371ce3143a4495e6892df7fb04794a6b708). The topology idea is recorded but has no proved same-machine transfer relevant to the present Route A test.

**External primary search / repository evidence.** A. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209-219, DOI 10.1145/7531.8928, gives expander-Tseitin exponential ordinary Resolution length lower bounds, **not** general computation hardness. L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), 835-865, DOI 10.1145/1101821.1101822: fixed random-access indexed-tape model and joint time-space barriers, not an automatic implication from a trace argument. Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), ordinary Resolution width/size controls. Standard Boolean deterministic query/certificate complexity and parity decision-tree literature is prior art for needing to inspect all independent source bits. Verified public repositories with actual files and pinned blobs: MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research README.md (f397a7747eaca82df3d754d0a4b4bab1fe10f814) and INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93); meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); berkeley-abc/abc README.md (88a9d1a316dd9751acade746de315fd1e6e6c362); openai/math/CONTENTS.md (7e1ed90ac5a666f1bbecb22027387c4ad79e9d03). Sources establish format, model and scope controls, not an all-input FLMV compiler. Public search was used, but a separately authenticated Google-branded search and native FLMV execution were unavailable.

## Precise original-source family, parameters and known hardness

Fix **any connected, simple cubic graph** G=(V,E) with n even vertices, m=3n/2 edges, ordered local edge triples (e0,e1,e2). This includes any chosen published cubic expander family used for ordinary Resolution-hard odd-charge Tseitin formulas. Set k=n-1 and descriptor d in GF(2)^k. Charges b_v=d_v for v<n-1 and b_(n-1)=0. For every vertex v encode

$$
x_{e_0}\oplus x_{e_1}\oplus x_{e_2}=b_v
$$

as FOUR proper, distinct ternary clauses, one forbidding each local triple of parity different from b_v. In the fixed clause order use the four base forbidden triples 001,010,100,111 for b_v=0; for b_v=1 toggle **only the first edge bit** in each of the four forbidden triples. If a forbidden assignment is a=(a0,a1,a2), its clause is the disjunction of x_e when a_j=0 and NOT x_e when a_j=1. Thus each descriptor coordinate toggles precisely four **first-literal sign bits**, with disjoint positions across vertices. All source clause widths are exactly 3; all three variables in every clause are distinct; no auxiliary variables, template pin, or non-3CNF intermediary is needed.

One exact binary packet for this experiment is 8-bit magic 10110110, unary variable count 1^m0, exactly 4n ordered ternary clauses with unsigned w=ceil(log2(m+1))-bit variable IDs followed by one sign bit per literal, then terminal 01. No global charge, parity or answer field is included. Original-source bit length:

$$
N(n)=8+m+1+12n(w+1)+2=\Theta(n\log n),\qquad w=\lceil\log_2(m+1)\rceil.
$$

All charge descendants for fixed G have exactly this length, and each y_i(d) is affine in d with coefficient row either 0 or a standard basis vector e_j. This is a specified proper-3CNF encoding; any changes to the generic parser/machine representation must be proved and charged before transferring to native FLMV or historical R_mix341.

**Label theorem.** XOR all vertex equations: every edge occurs exactly twice, so their left sides cancel. Therefore a solution requires sum_v b_v=0. Conversely, a connected graph's incidence matrix over GF(2) has rank n-1, so every even-charge vector admits an edge assignment. The four clauses at each vertex are equivalent to its XOR equation by their truth table. Hence

$$
\operatorname{SAT}(F_d)\iff\bigoplus_{j=0}^{k-1}d_j=0.
$$

This is a *polynomial-time algebraic family*, with an independent Gaussian-elimination upper control. For the subset of graph/charge pairs of Urquhart's published expander-Tseitin construction, the published exponential lower bound is for **ordinary DAG Resolution proof length only**. It is not a lower bound for Gaussian elimination, R_mix341, or any deterministic SAT algorithm. Our finite K4/prism instances are NOT certified proof-size-hard instances.

## PROVED/RESTRICTED: query-access strengthening of [P2-L2-516]

Let y(d)=p+Vd be *any* fixed-length affine source family, let f(d) be its correct SAT/UNSAT label, and let A be an arbitrary deterministic **total correct all-input** SAT decider run from the same non-input initial configuration. Let I_d be every actual input bit position read before A halts on y(d), and let S_d be the linear span of V's rows at those positions.

By deterministic transition induction, A has the same complete trace and label on every descriptor in d+S_d^\perp. Therefore the **allowed-query certificate rank**

$$
r_{\mathrm{access}}(d)=\min\{\dim\langle v_i:i\in I\rangle:\ f\hbox{ is constant on }d+\ker(V_I)\}
$$

with minimum over subsets I of *physically present input bit rows* satisfies

$$
\operatorname{rank}(V_{I_d})\ge r_{\mathrm{access}}(d)\ge k-h_f(d),
$$

where h_f(d) is the largest dimension of any f-monochromatic affine subspace through d, as in [P2-L2-516]. This lemma is an access-geometry/certificate-complexity refinement, not a new decision-tree principle. If a self-describing packet contains a global parity bit as an input row, the available-query rank could be only 1. That alternate format is NOT the packet here.

For the explicit charge packet, f(d) is parity on k bits, so **h_f(d)=k-1** for k>=1, making the previous semantic bound only rank>=1. Nevertheless each physical row is 0 or e_j. If a completed trace omitted every sign position in charge group j, flipping descriptor bit j would leave *every observed input value unchanged* while reversing SAT/UNSAT, contradicting total correctness. Therefore **every correct A on every y(d)** must read at least one source bit from each of the k charge groups:

$$
\boxed{\operatorname{rank}(V_{I_d})=k,\qquad |I_d|\ge k\quad(\hbox{all }d).}
$$

For any d != d', choose differing coordinate j. The trace on d includes an input read at a sign position in group j, whose value flips on d'. Hence the complete observed-input-value traces cannot coincide. Thus, for any correct deterministic A,

$$
\boxed{\#\text{complete read-value trace classes on }\{F_d\}=2^k.}
$$

This is a precise **worst-family limitation** on exact completed-trace replay by [P2-L2-515]. On this fully variable-source family, that cache method needs one authenticated *distinct complete trace* for each child if it insists on answering each solely by exact previous-trace reuse. It is **NOT** a proof that every actual SAT algorithm needs 2^k computations: a compiler can apply parity algebraically, aggregate query answers by a different proof, bypass full guest execution, or use a different representation and pay all its costs. The direct lower bound is only Omega(k) source input-bit queries per independent guest execution, with N=Theta(k log k). No R_mix341 bound or FLMV exponent barrier follows.

**Relation to peer controls.** [P2-L4-515] uses satisfiability-INVARIANT signed tags and can skip them, so this theorem does not apply to those tags. [P2-L4-516] established exactly k+1 attainable trace classes for a unique-UNSAT selector family; on its SAT branches, early termination leaves many coordinates unread. Here parity flips the SAT/UNSAT label when **any** coordinate flips at **every** descriptor, so early short-circuit is impossible in the declared physical-read model. These results are compatible.

## COMPUTATIONAL checks and independent methods

Two independent implementations were executed. Python directly parsed each original bit packet, checked all proper-width clauses, and classified each decoded original CNF by complete DPLL. JavaScript independently used GF(2) Gaussian elimination on the original graph incidence equations and exhaustively checked all 8 local truth assignments against each original four-clause group. Neither program uses the other's solver.

- n=4 K4, n=6 triangular prism, n=8 cube, n=10 pentagonal prism: k=3,5,7,9, respectively.
- 680 physical original strict-three sources in total, exactly 340 SAT and 340 UNSAT. Python: 11,140 assertions and 680 decoded original-CNF DPLL calls. JavaScript: 9,793 assertions and 50,944 independent local truth-table checks. Both confirm all 680 source labels.
- At each n, every descriptor toggled exactly its four signed positions per chosen charge, all 2^k one-sign-per-charge read signatures distinct. Packet lengths 209,380,503,626 bits. Python rejected 20 framing corruptions plus 4 invalid literal IDs; JavaScript rejected 16 framing corruptions. The scripts do **not** assert that a frame-only check authenticates an arbitrary source, and no authoritative historical native certificate checker was run.
- Independent zero-descriptor packet SHA-256 checksums (Python): n=4 4b28b3f6a80e1bb339af6a36b0272bd9d74a25895a837f92dd2ace0dc3fb0d6d; n=6 de62f81a5015ce9d06df59654515cce729272da1e2f28f9a6f9cdee7405f2c79; n=8 6158781b9e83ab0e6353fefac20e347a3d3669f08560acd7c3072c4de966d62a; n=10 ac3516b46ca75fc6c7e2d76fc4242e71c80747d95cc942eae3e4986cb3d43e0e. The JS run did not compute cryptographic hashes.

Published JS: experiments/arc/lspv2_517_parity_access_independent.js. Python and raw JSON reproducibility files are separately available in the run archive. Raw summary: results/raw/arc/2026-11-09_0317_LSPV2_517_LOCAL_CHARGE_READ_RAW.json.

## Full resource firewall and remaining transfer

- **Logical work**: the family has 4n source clauses, 12n literal fields, and k=n-1 varying charge coordinates; no proof DAG or R_mix341 inference-node minimum is claimed.
- **Evidence bits**: explicit packet N=Theta(n log n); 4k variable sign positions; per-guest read log may contain up to T addresses each of O(log N) bits and output history; source and authenticated trace acquisition are not free.
- **Upper control**: parity of charge vector from source, or GF(2) elimination of n-by-m incidence matrix, decides every valid family member in polynomial time; generic original-CNF solver/fallback remains necessary for all other well-formed sources.
- **Lookup/reuse**: full-rank trace has no nontrivial affine descriptor kernel; a cache of all exact completed traces may require 2^k entries and Omega(2^k k) observed-sign evidence, while a different algebraic solver stores only O(k) bits.
- **Physical costs**: original source acquisition, all INPUT/INDEX head transitions, writing each observed signature, local extraction, authenticated descriptor recognition, failed fallback, guest interpreter, output, storage/retrieval, memory retention versus recomputation, final result and all-phase peak must be charged under one actual native FLMV realization. No native instructions or same-machine time-space exponents were measured.
- **Scope**: no creation of the user-required <=N^(3/5+o(1)) children of length <=N^(1/2+o(1)); this is an affine *family of entire sources* of equal length. Does not establish [P2-A2], the simultaneously charged bounds [P2-A4], or recursive closure [P2-A5].
- **Barrier check**: no relativization/algebrization/natural-proofs bypass or all-algorithms computational lower bound. It is an information-access query limitation for a fixed packet and cache policy. Ordinary Resolution hardness on expander members is not transported to R_mix341 without a sound legal simulation direction.

**Main document reconciliation blocker:** root main.tex returned an empty content field under authenticated GitHub fetch_file despite a SHA. Outside-byte preservation could not be certified; root main.tex was deliberately left untouched. Native repository preflight/check scripts could not run in the separate local container because its network DNS could not fetch the GitHub repository. The complete independent Python experiment ran locally; the exact published JavaScript function was executed in the connected-code runtime prior to GitHub publication.

**Precise next target:** For Route A, either construct an ALL-INPUT A-dependent adaptive decomposition using information beyond completed input-read traces, with a charged source-to-child/guest-native model and recursive closure, or give a focused no-go for a precisely stated such compiler class. Focus on native FLMV costs and known hard-family shortcuts, not simply enlarging finite trace examples. [P2-A2], [P2-A4], [P2-A5] remain OPEN. P versus NP OPEN.

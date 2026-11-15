# TMR-4/035: Zero-cost SCC quotient and exact-rational tariff LP

**2026-11-14 19:43 PST.** TMR-4, PNP Cost-Sound Abstraction. Claim TARIFF-SCC-LP051. **PROVED/RESTRICTED** finite-system all-step/telescoping lemma, **COMPUTATIONAL** native calibration, independent peer review **OPEN**. P versus NP **OPEN**.

## Candidate, falsifiers, and qualification

**Candidate:** construct an exact zero-cost closure and seven-coordinate rational tariff certificate for a fully specified two-bit source-query protocol. Before the source review, four falsifiers were registered: (1) a legal zero-price step reduces potential; (2) a paid read discharges overlapping components more than its price; (3) a cheap affine/cached/malformed operation finishes with fewer paid reads; (4) a source-aware compact instruction changes the optimal tariff. These explicitly attack, rather than assume, the model's soundness.

Source domain comprises the four authenticated two-bit strings b=00,01,10,11. Concrete state C=(b,m,t,h) consists of exact source, the two-bit observed-source mask, redundant tag t in {0,1}, and terminal flag. Authenticated source b occurs in the mathematical state but is **not freely accessible** to the executing program. The two writable cached values are the corresponding observed source bits. Terminal output is b0 XOR b1 only when both bits have been observed. The exact legal rules on nonhalted states are:

| Rule | Price | Meaning |
|---|---:|---|
| free_tag_swap | 0 | Toggle redundant representation tag, reversible |
| free_affine_xor_finish | 0 | After observing both bits, compute XOR and terminate |
| read_0, read_1 | 1 | Read addressed bit, set mask bit; repeated read still costs 1 |
| bad_index_2 | 1 | Invalid-index no-op; no fact or terminal label |

All adaptive reading and repeated reads are allowed. The qualified protocol has **36 states, 136 edges, 40 zero edges, and 20 zero SCCs, including 16 nontrivial SCCs**. It is not an unrestricted SAT machine, an MCSP oracle, /341, or /386. A general SAT syntax inspection is deliberately *not* an operation of this restrictive protocol, so arbitrary-machine transfer remains OPEN.

## Full zero closure, relation, and all-step lemma

Let Z(C) be the set reachable from C by zero or more authentic zero-cost operations. The implementation uses Tarjan SCCs and then **full directed zero reachability**. Free finalization is a one-way edge between SCCs, not an equivalence. Define the closed vector componentwise by

$$
p_j(cl_0(C))=\min_{D\in Z(C)} f_j(D).
$$

For any zero edge C to C', Z(C') is a subset of Z(C), so the closed component cannot decrease. More generally, an abstract node is the concrete zero-SCC with authenticated source/control information retained; every actual concrete edge is included in the abstract graph at exactly its actual price. An SCC-internal free step may be represented by an empty zero-cost abstract path. For **every** related concrete state and **every** concrete transition the corresponding abstract path costs no more than the concrete increment. Initial states and both correct output labels are preserved. Every concrete execution is covered. This proves a finite-system cost-underestimating simulation, **not** a TM simulation for unlisted operations.

Use seven directive components (CNF, XOR, separator, fusion, Gamma, interface, machine). In this affine laboratory all except Gamma and interface are zero. Let u(C)=2-popcount(m). The reduced-product vector is

$$
\mathbf p(cl_0(C))=(0,0,0,0,u(C),u(C),0).
$$

These are correlated components, since a single source read reduces *both*. The full CSV has one row per distinct rule/delta combination and the exact multiplicity, including all seven columns:

| Rule group | Delta Gamma | Delta interface | Price | Multiplicity |
|---|---:|---:|---:|---:|
| Tag toggles | 0 | 0 | 0 | 32 |
| Affine finishes | 0 | 0 | 0 | 8 |
| Useful first reads | 1 | 1 | 1 | 32 |
| Repeated reads | 0 | 0 | 1 | 32 |
| Malformed requests | 0 | 0 | 1 | 32 |

The rational LP maximizes initial potential subject to every legal edge tariff and four terminal constraints:

$$
\max_{\lambda\ge0}\lambda^\top\mathbf p(C_0),\qquad
\lambda^\top[\mathbf p(cl_0(C))-\mathbf p(cl_0(C'))]\le w(C,C').
$$

The only nontrivial inequality is lambda_Gamma + lambda_interface <= 1. An **exact feasible certificate** is

$$
\boxed{\lambda=(0,0,0,0,1/2,1/2,0),\quad\Phi(C_0)=2,\quad\Phi(goal)=0}.
$$

The full graph yields **140 independently checked edge/terminal inequalities**, all passing. Exact rational simplex obtains optimum **2**, an extreme primal witness (0,0,0,0,1,0,0), and an exact dual multiplier 2 on a useful-read row. Independently, the genuine path read_0, read_1, free_affine_xor_finish has price 2, establishing tightness on all four source strings. The general finite telescoping lemma then gives Phi(initial) <= minimum complete paid execution cost. This is constant work, not asymptotic hardness.

The **naive fusion failure** is explicit: lambda_Gamma=lambda_interface=1 would demand tariff 2 for a single useful read of price 1. This edge is real, so the double counting is rejected rather than removed.

## Hostile controls and CEGAR

In an *expanded* model with a new source-aware compact_parity_hint instruction of price 1, the eight new initial-to-terminal transitions each discharge (2,2) for price 1. The original rational certificate is **falsified** on all eight new rows; exact LP optimum becomes **1**, with valid certificate (0,0,0,0,1/4,1/4,0) and a real one-step terminal path.

In a further *expanded* model admitting free_omniscient_hint of price 0, the initial state's directed zero closure contains an actual terminal. The saturated initial obstruction and LP optimum are both **0**. Using the raw, unclosed vector would cause a legal zero-cost decrease and be unsound. This is an authentic counterexample in the expanded model, not a spurious abstract path.

Additional controls: XOR finish is cost zero once input is read; cached rereads never discharge again; free reversible tag rewrites are preserved; invalid index requests remain paid no-ops. No shortcut is deleted by CEGAR. Refinement is permitted only when independent replay proves an abstract path spurious against the authenticated concrete authority. Prior /341 accepted SAT-source counterexample remains **FAIL** for general logical UNSAT; distinct /386 verifier remains **RESTRICTED**. Neither is repaired or relabeled.

## Provenance, execution, and research limits

Read governing fusion-Lipschitz directive **FIRST** (Git blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6); then TMR replacement, both root trackers, full root main.tex, issue #3, AGENTS.md, CODEX.md, repository research skill, all TMR handoffs, and original Lipschitz, checker, normalizer, multiscale/fusion and MCSP evidence. In particular: research/agents/lead/2026-10-07_0855_LEAD-0029_LIPSCHITZ_SQUEEZE_AUDIT.md; research/agents/lspv-3/2026-11-13_0727_LSPV3_615_HASH_BINDING_SOUNDNESS_COUNTEREXAMPLE.md; research/agents/lspv-1/2026-11-11_0600_LSPV1_386_PARSE_SERIALIZE_QUOTIENT572.md; research/agents/lspv-5/2026-10-25_0648_LSPV-5_ARC_DP_DOMINATES_FUSION167.tex. Previous semantic mass, source entropy, prescribed DAG and cost-free sharing arguments remain retired.

Primary methodology, no unsupported theorem transfer: Cousot and Cousot, POPL 1977 pp.238-252, DOI 10.1145/512950.512973; Clarke, Grumberg, Jha, Lu, Veith, CAV 2000 pp.154-169, DOI 10.1007/10722167_15; Cook and Reckhow, JSL 44 (1979) pp.36-50, DOI 10.2307/2273702.

Native CPython **PASS** on the locally executed prototype: qualified 36 states / 136 edges / 140 inequalities / optimum 2; paid-compact extension 144 edges / eight exact violations / optimum 1; zero-hint extension optimum 0. Source in the repository is a refactored equivalent of the locally executed prototype; source-byte identity is **not** claimed. The complete executable generates reproducible JSON evidence; CSV explicitly records tariffs and multiplicities. All numerical calculations use exact fractions, no floating point. Experiments are finite **COMPUTATIONAL** data. This result has no parameterized initial gap.

Root proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 characters), proof2 full Git blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters), root main.tex full Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 characters) were read/recovered after the Contents API gave blank bodies for large files. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex and all five schedules unchanged.

**OPEN arrows:** qualify the exact source-bound native machine or proof system, represent all actual operations with an all-step simulation, prove fusion-safe growing initial obstruction and a joint rule tariff, then prove the same-system unrestricted SAT bridge. This lab proves none of those. **P versus NP OPEN.**

**Peer request:** TMR-1 qualify the next authority and columns; TMR-2 propose a nontrivial affine-quotiented separator/fusion obstruction; TMR-3 provide full native rule costs and shared-identity accounting; TMR-5 independently rerun the published Python and test the compact/zero shortcuts and dual. Next TMR-4 target: a genuine authenticated transition slice with zero definitions, branching, sharing, and precise resource costs.

END_OF_REPORT::TMR4::035::2026-11-14_1943_PST

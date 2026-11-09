# LSPV-2/507 | Charged input-read trace cylinders and deterministic cache trie

**2026-11-08 17:16 PST | Route A | PROVED/RESTRICTED lemma; COMPUTATIONAL finite controls | P versus NP OPEN**

**Exact nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN; cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No historical R_mix341 grammar/weights were modified.

## IDEA and four falsifiers, stated before search

Hypothesis: for one fixed deterministic guest program, one fixed input length, and identical full initial non-INPUT configurations, a genuine completed in-range INPUT read trace defines a sound answer-reuse cylinder. Distinct such completed traces are either identical or have disjoint cylinders. A single branching decision trie can therefore identify a matching trusted anchor without a linear search over all anchors.

F1: two distinct genuine completed traces match the same input. F2: ignoring out-of-range INPUT-blank reads changes a future transition. F3: a forged external trace or different initial WORK state is incorrectly accepted. F4: a full-scanning guest necessarily experiences a cache speedup or retained state costs are hidden.

## SEARCH, exact inputs and prior art

Read both full live trackers: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters; proof2.txt blob 7b715962da692f3693c7cc074d6c7712bce00657, 557,976 characters. Read issue #3 (1,401 comments at inspection, most recent comment LSPV-3/516). Read governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154, AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef, and .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f. Reviewed LSPV-2/500, /501, /505 blob 4f9d34d3d84362a8909e3efdecdcc5572da2c843, /506 blob bf49022935074512b6641bf7abd40e8ae74c2227; GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70; and research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67. Historical trace-sharing results are preserved, not claimed new.

External actual files checked: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and DETAILED_SOLUTION_PLAN.md blob 19450e384269f1ccf890b924ae0b10ce8da212cd; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and verify_residual_equivalence_barrier.py blob f204ac6009559c07602a43c400a0ee2ad47cb86d; MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor/README.md blob 38a137bca4d4ab6443703d4c31fba5783021c581; openai/math/lean/docs/378.md blob 223bbe187394bffca8a2c7ba1656538bfba26e3b; and anthropics/formal-math/eth/README.md blob 0b3dcf4a858ff802b3275fc5999ffb134c74de60. These do not establish a polynomial-time SAT solver. Public web searched original FLMV, Acar self-adjusting computation, Urquhart resolution hard examples and October 2026 subexponential SAT work; Google-branded search unavailable. Fortnow et al. original PDF section 2.1, PDF zero-index page 3, was inspected with the web screenshot tool. No external Lean replay, no original R_mix341 execution.

## ITERATE: theorem 507.1 (PROVED/RESTRICTED, elementary deterministic semantics)

Fix a total deterministic guest $M$, input length $m$, and identical complete initial non-INPUT configuration $c$, including code, control, WORK/INDEX tape contents and heads. INPUT is read-only; positions outside $[0,m-1]$ have a fixed blank symbol. For an actual *completed* run on source $x$, let

$$
\tau_{M,c}(x)=((p_1,x_{p_1}),\ldots,(p_r,x_{p_r}))
$$

be the ordered sequence of reads only at in-range INPUT positions. Repeated observations are retained. Define

$$
C(\tau)=\{y\in\{0,1\}^m:y_{p_i}=b_i\text{ for all }(p_i,b_i)\in\tau\}.
$$

**Claim 1:** For any $y$ in this cylinder the deterministic execution and final SAT/UNSAT/MALFORMED output equal those of anchor $x$. **Claim 2:** Two genuine completed traces for the same $(M,c,m)$ are identical including output, or their cylinders are disjoint. **Claim 3:** The genuine read sequences have a prefix-compatible binary decision trie, with one next in-range position after a shared observation prefix and no completed trace being a strict prefix of another.

**Proof.** Induct on the machine transitions on anchor $x$ and candidate $y$. Their initial non-INPUT states and input length coincide. All internal and WORK/INDEX operations agree by determinism. An in-range INPUT read returns the same recorded bit on both sources; an out-of-range read returns the same fixed blank. Thus transitions, future addresses, physical accesses and halting classification agree. If distinct completed trace cylinders intersect, the input in the intersection would have to execute both trajectories, contradicting determinism. A shared read-value prefix determines the same next in-range address; a halted trajectory cannot be a strict prefix of a nonhalted trajectory. QED.

For $K$ trusted anchors totaling $R$ in-range read events, a standard explicit binary trie uses at most $K+R$ nodes and $O((K+R)(\log(m+1)+\log(K+R+1)))$ bits for positions, child pointers and labels. A cache hit follows at most its observed trace depth with the additional paid indexed pointer/input accesses; there is no compulsory scan over every anchor. A miss must actually execute the guest, collect its trace and charge all construction/verification. A structurally plausible external trace is NOT authenticated. Extremely high out-of-range INPUT addresses can be omitted from the *input-dependence key* because they return a fixed blank, but construction of their INDEX address and any WORK-tape high-water remain charged under FLMV.

## Established family, exact encoding and known shortcut

Control: original proper signed 3-CNF Tseitin on K4, variables $x_{01},x_{02},x_{03},x_{12},x_{13},x_{23}$. For each vertex of charge $\chi_v$ use exactly four width-three clauses excluding assignments with incident-edge parity different from $\chi_v$: 16 source clauses total, 6 variables. Odd overall charge XOR certifies UNSAT; even charge is SAT. Original clause truth was brute-force checked over all 64 edge assignments for all 16 charge patterns. Urquhart (1987) proves exponential **ordinary DAG Resolution** refutation lower bounds on suitable *growing expander* Tseitin families, not on K4, arbitrary SAT algorithms or mixed R_mix341. GF(2) is a short valid upper-bound control.

The executed guest separately uses a **compact specialized grammar**: fixed four-bit header, four charge bits, and arbitrary ignored padding. MALFORMED means bad header or too short. It is NOT the original strict signed 3-CNF encoding, a general CNF parser, or a lower-bound-preserving compression from arbitrary CNF. A deliberately full-scanning guest supplies the adverse control.

## Finite controls and physical-charge qualifications

Local Python implementation PASSED 4,629 assertion groups (seed 507): 584 initial compact sources (266 SAT, 310 UNSAT, 8 MALFORMED); 256 altered-padding queries; 128 distinct full-scan negative controls; exhaustive original K4 signed CNF parity control for 16 patterns; incompatible next-read, repeated read, out-of-range read and untrusted external trace controls. Main trie: **25 trusted anchors, 69 nodes, 816 hits, 25 misses, 7,463 input-bit comparisons, 163 fresh in-range read events, conservative 1,809 explicit node-field bits**. Full-scan adverse case: 128 distinct anchors, 128 guest executions, zero hits, 1,416 trie nodes. Python original-signed-source SHA-256: d4f4bd88aebddc2c71d548f9fb9b330fd85376e8abfddad68cfd2cf564fbcbb4 (byte identity, not proof of UNSAT). Independently authored Node.js code PASSED 1,182 checks, with 24 trusted anchors, 59 nodes, 1,008 hits and 9,191 source-bit comparisons; its distinct full-scan controls again needed 128 guest executions and obtained zero hits. Independent test datasets need not coincide.

These host tests count abstract comparisons and node-field bits but **do not execute native FLMV instructions** or historical R_mix341. They do not certify construction time, persistent host memory, source/index/head reads, cache eviction, failed policies, physical WORK high-water, input-grammar conversion, parallel scheduling, or guest execution under a single native resource bound. Trusted-anchor construction costs cannot be amortized without a proved schedule and exact input population.

## Conditional cache-only resource estimate and OPEN transfer

If an independently supplied all-input child constructor already provides $q\le N^{3/5+o(1)}$ guest children, encoded lengths $B\le N^{1/2+o(1)}$, and only $K=\mathrm{polylog}(N)$ authenticated anchors, each with $r\le B^{1+o(1)}$ recorded input reads, then a *hypothesized fully charged* native trie backend with polylog overhead would use $qr\operatorname{polylog}N\le N^{11/10+o(1)}$ lookup time and $Kr\operatorname{polylog}N\le N^{1/2+o(1)}$ trace storage. This does NOT bound full program costs: arbitrary guests can have $r=B^t$, distinct read traces, no reusable anchors, and expensive trace acquisition. The missing all-input child constructor and recursively iterable same-machine realization remain OPEN. In particular $s'\le\max(\rho,\eta,\lambda,\lambda s)$ must include every phase and ancestor high-water.

**Actual advance:** exact partition/trie construction and a full-scan negative control refine the acquisition-versus-reuse ledger. The universal nodes [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN; Route B full mixed-calculus lower bound and noncircular B3 remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE. P versus NP OPEN.**

## Literature

1. Fortnow, Lipton, van Melkebeek, Viglas. *Time-Space Lower Bounds for Satisfiability*. JACM 52(6), 835-865 (2005). DOI 10.1145/1101821.1101822. https://lance.fortnow.com/papers/files/tst.pdf .
2. Urquhart. *Hard Examples for Resolution*. JACM 34(1), 209-219 (1987). DOI 10.1145/7531.8928.
3. Acar, Blelloch, Blume, Harper, Tangwongsan. *An Experimental Analysis of Self-Adjusting Computation*. TOPLAS 32(1) (2009), DOI 10.1145/1596527.1596530.
4. Acar, Blume, Donham. *A Consistent Semantics of Self-Adjusting Computation*. JFP (2013), https://arxiv.org/abs/1106.0478.

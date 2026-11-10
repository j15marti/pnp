# LSPV-3/554: No sound single-goal abstraction of recovered /341 acceptance

**November 10, 2026, 14:24 PST | LSPV-3 Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED logical no-go + COMPUTATIONAL pinned checker replay | P versus NP OPEN**

**Affected obligations:** [P2-D1] and [P2-C3] remain OPEN; [P2-B1] and separate [P2-B2]/B3 remain OPEN. New scoped inference [P2-L3-554] is **derived from previously verified [P2-L3-551]**, not a newly found malformed-source exploit. [P1-01], [P1-03], [P1-04] remain OPEN. Exactly five existing roles, schedules, native weights and 2A/3B allocation unchanged.

## IDEA and falsifiers registered before source search

**Candidate:** The accepted terminal of the recovered historical /341 *fixture* checker cannot be used as a sound UNSAT goal for an overapproximating abstract interpretation that preserves all of that checker's raw accepted computations. Prove this as an impossibility result for **every** candidate abstract domain, not merely as a complaint about a particular malformed local inference. Then define the precise two-goal trust separation required for [P2-C3].

Four falsifiers: (F1) the alleged accepted SAT packet is in fact UNSAT; (F2) the immutable verifier rejects that packet; (F3) semantic validity and raw acceptance coincide, so no separate goal is needed; (F4) a cost-sound may abstraction can somehow preserve the erroneous accepted terminal *as a semantically valid refutation* without classifying the satisfiable source as UNSAT. F1–F3 are refuted by independent source evaluation and checker replay; F4 is excluded by the theorem below.

## SEARCH and duplication audit

Read the complete current root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (startup blob 4af38840364e80c49a4d3d87b41d8507b9e0673f); current issue #3 and specialist updates; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; abstract-negative/assumed-time governance; the exact /341 original declaration, producer, checker and packet; LSPV-5/413; LSPV-1/553, /556; LSPV-2/538, /539, /541; LSPV-3/549–553; relevant LSPV-4/525; GROKPROOF/2026-11-10_1435_PROGRESS.md; and Claude's world-ledger README. Retained earlier restricted results and scope.

The exact **pinned historical** artifacts are: declaration at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), original checker experiments/arc/lspv2_341_independent_verify.js (fcb7d4ced8f922de14c0bda16263a8cc7853e8e0), original packet results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json (fe27fe1011d0021e721ccaeb747ed58da65d7464), and previously discovered accepted SAT packet results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json (706947c767361e7c979b8208677eb983d33838f4).

**Important nonduplication:** LSPV-3/551 already discovered the forged SAT packet; /552 parametricized it; /553 counted its models. LSPV-1/553 already exhibited a semantically legal padded proof rejected by the fixture checker, and LSPV-2/539 built a **separate** source-bound typed reference checker with a two-sided differential corpus. This run claims **none of those discoveries as new**. The new theorem is the universal *abstraction-goal impossibility* quantified over **all domains, gamma/alpha choices and resource charges**, together with its explicit two-goal repair obligation for [P2-C3]. It is an immediate but previously unstated **mathematical corollary** of the already published counterexample.

Primary sources rechecked: Cook–Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1):36–50 (1979), DOI 10.2307/2273702; Cousot–Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973; D'Silva–Haller–Kroening, *Abstract Conflict Driven Learning* (POPL 2013) and *Abstract Satisfaction* (POPL 2014). These supply the verification and approximation framework, **not** the project-specific byte counterexample. Change-aware original-repository reads: konard/p-vs-np/scripts/proof_status.json (93b77ed3...), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea...), meelgroup/frat-xor/format.md (986a21aa...), tanyongkiam/cake_lpr/README.md (e94f45e9...). The latter two define **different** authenticated proof languages and do not fill R_mix341's grammar.

## Theorem 554.1: operational acceptance cannot be a semantic UNSAT goal

Let $C_B$ denote the concrete complete byte-level executions of the **recovered** /341 SOURCE/AND3/XOR checker, including raw source/proof bytes, parse types, graph/charge/clauses, all proof records and their order, original/provenance identities, a current state, and terminal verdict. Let $G_B\subseteq C_B$ be **all checker-accepted terminals**, regardless of the underlying formula's satisfiability. Let $G_{\mathrm{UNSAT}}\subseteq C_B$ consist of states whose **actual original signed CNF** is UNSAT.

The pinned checker accepts a terminal $c_*$ for an **actually satisfiable** 18-variable, 48-clause signed proper 3-CNF $F_*$, with explicit witness

$$
w_*=101001000000100000.
$$

Its accepted purported proof has 47 distinct paid records. Consequently,

$$
c_*\in G_B\setminus G_{\mathrm{UNSAT}}.
$$

**No** abstraction $\alpha$ and concretization $\gamma$ into **any** abstract state domain $A$ with abstract goal $G^\#\subseteq A$ can simultaneously satisfy all three conditions:

1. **Extensivity:** $c\in\gamma(\alpha(c))$ for every concrete state $c$.
2. **Preserve every recovered accepted terminal as goal:** $\alpha(G_B)\subseteq G^\#$.
3. **Interpret every abstract goal as semantically sound UNSAT:** $\gamma(G^\#)\subseteq G_{\mathrm{UNSAT}}$.

**Proof.** Apply (2) to $c_*$: $\alpha(c_*)\in G^\#$. By (1), $c_*\in\gamma(\alpha(c_*))$. Hence $c_*\in\gamma(G^\#)$. Condition (3) gives $c_*\in G_{\mathrm{UNSAT}}$, contradicting the explicit satisfying assignment. QED.

This contradiction is independent of abstract precision, widening, CEGAR refinement, cache representation, resource budget, node sharing and cost partitions. Adding a required inequality $\mathrm{cost}^\#\le\mathrm{cost}_{B}$ cannot rescue the three incompatible goal properties. In particular, the no-go is already witnessed within the concrete **47-paid-node** budget and therefore within every larger budget.

**Scope:** It forbids a specific mistaken identification of *recovered checker ACCEPT* with *sound semantic UNSAT*. It does **not** rule out a source-preserving abstraction of the intended correctly typed calculus, a corrected checker, or proof-size lower bounds for a separately authenticated sound rule system. No all-rule R_mix341 parser has been found. An accidentally accepted malformed trace is not thereby a legal inference of the intended mathematics.

## Correct abstract-state polarity and trust boundary

A sound research implementation must maintain **two distinct goals**:

- **Operational goal** $G_B$: the recovered executable returned ACCEPT on the raw source/packet. This can include a SAT source and is not an UNSAT certificate.
- **Certified goal** $G_C$: the source is authenticated against independent input bytes and every typed inference step/assumption discharge has been validated by a **sound** rule checker, producing a refutation. This implies UNSAT by induction, but the fully authenticated R_mix341 checker remains OPEN.

A conservative reduced product may carry a verdict tag $\mathrm{accepted}\in\{0,1,?\}$, a separate provenance/semantic-validity tag $\mathrm{certified}\in\{0,1,?\}$, plus the **complete** shared DAG, source bytes/identities, paid first-use set, contexts, definitions, freshness, interfaces and per-node cost. The best sound collecting transformer is $\mathrm{Post}^\#=\alpha\circ\mathrm{Post}\circ\gamma$. A may state with $(\mathrm{accepted}=1,\mathrm{certified}=? )$ is **not** a certified proof goal, even if a finite search or native checker terminated ACCEPT. The forged packet has $(1,0)$ by explicit SAT countermodel.

For the **separately declared** typed SOURCE/AND3/XOR reference fragment, LSPV-2/539's proof gives soundness of $G_C$ and includes the authentic K4 proof while excluding the forged SAT packet. This does not make the reference checker authoritative for unimplemented RES, LOCAL-CONVERT, DEF, fresh-wire/port, branching or discharge rules. Such unknown rules must remain MAY-permissive in any *whole-historical-language lower-bound relaxation*, with no unsound promotion of its operational terminals into semantic goals. In a sound fixed calculus, true concrete refutations must always map to abstract paths of NO GREATER native paid cost. The ideal minimum counts shared nodes once; byte-validation work and actual peak machine space are separate resources.

## Actual immutable-checker replay and hostile controls

The published standalone script is experiments/arc/lspv3_554_operational_semantic_goal_firewall.cjs. It reads the pinned original checker and two independently published source/packet files in an actual repository checkout. Inside an isolated V8 evaluation, the exact published JavaScript was retrieved from GitHub and executed unchanged **except for the outer readFileSync and console/argv shims**. No reconstructed proof-system checker was substituted.

| Test | Result |
| --- | --- |
| Original historical seven-fixture packet, including odd K4 | ACCEPT, **30,714 assertion groups** |
| Previously published two-fixture packet with SAT forged source | ACCEPT, **2,273 assertion groups** |
| Independent evaluation of the 18-bit SAT witness | **48/48 clauses SAT** |
| Distinct paid nodes in forged accepted packet | **47** |
| Semantically exact fresh 16th paid K4 AND3 inserted into original 15-paid proof | **REJECT**, "proof candidate length" |
| Forged packet with final XOR RHS corrupted | **REJECT**, "bad GF2 elimination" |

The redundant K4 factor is the exact eight-row conjunction of its original source parents; adding its fresh unused identity does not affect the rest of the original proof under the **declared permissive** DAG semantics. The original fixture checker enforces the special $4V-1$ length and thus rejects it, independently corroborating the earlier LSPV-1/553 and LSPV-2/539 two-sided boundary. We retain that finding as a control, not a new result.

Raw exact replay: results/raw/arc/2026-11-10_1424_LSPV3_554_OPERATIONAL_SEMANTIC_GOAL_RAW.json. **No OS Node subprocess ran**; the exact fetched published JavaScript was executed in V8 with filesystem shims, and the standalone Node script is designed for a full local checkout. No historical full-mixed checker, checker certification system or actual machine-space proof executed in this run. A fresh project checkout was unavailable in the container, so the repository-wide preflight and check_research_reports.py commands were not executed.

**Resource ledger:** operational paid work is 15 for K4, 47 for forged source, 16 for the redundant K4 test; the explicit certificate file sizes, all source-read operations, Node parser/VM memory, proof acquisition, full time/space work and span are independent and NOT inferred from these numbers. The theorem is an all-domain logical impossibility, not a time, space or proof-size lower bound.

## Disposition and precise next dependency

**Actual advance:** theorem 554.1 proves no abstraction can simultaneously overapproximate *all recovered checker ACCEPT terminals*, preserve those terminals as proof goals and declare every such goal semantically UNSAT. This is a **P2-C3 trust-boundary no-go**, using an already authenticated accepted SAT packet, and prevents mistaken CEGAR promotion of a genuine checker-accepted invalid trace. It does **not** close P2-D1, P2-C3, P2-B1 or the independent B3 transfer.

**Next highest-value task:** recover one historically authoritative accepted-byte **RES, DEF/facet, LOCAL-CONVERT or branching/discharge** certificate and its checker branch; then type and replay that native transition against independently bound signed source bytes. Do not invent an opcode or replace the historical grammar with CANON1/2/2R. If the authoritative full grammar is unavailable, report it rather than declaring the incomplete fixture checker complete.

**Publication:** role-owned report/code/raw and five-role handoff committed to main with exact source/readback verification; proof trackers and issue #3 reconciled only for material evidence. Preserve every historical rule weight and all five role identities/schedules. P versus NP remains OPEN.

## References

1. Cook, S. A., and Reckhow, R. A. (1979). The Relative Efficiency of Propositional Proof Systems. *Journal of Symbolic Logic*, 44(1), 36–50. https://doi.org/10.2307/2273702
2. Cousot, P., and Cousot, R. (1977). Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints. *POPL*, 238–252. https://doi.org/10.1145/512950.512973
3. D'Silva, V., Haller, L., and Kroening, D. (2013). Abstract Conflict Driven Learning. *POPL*. https://www.kroening.com/papers/popl2013.pdf
4. D'Silva, V., Haller, L., and Kroening, D. (2014). Abstract Satisfaction. *POPL*. https://www.kroening.com/papers/popl2014.pdf

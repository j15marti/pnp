# LSPV-3/587: Functionally identical paid gates expose distinct native free facets

**November 12, 2026, 04:24 PST | LSPV-3 Hypergraph & Proof Certificates | Route B | PROVED/RESTRICTED original-code theorem + COMPUTATIONAL actual unchanged-checker Node OS replay.** P versus NP remains OPEN. P2-D1 -> P2-C3 -> P2-B1 and separate P2-B2/B3 remain OPEN.

## Candidate and four pre-search falsifiers

Candidate: two differently encoded globally paid AND2 definitions of the *same complete Boolean function* can have incompatible authentic zero-cost DEF facet operations in the recovered original /386 checker, so semantic truth functions cannot replace signed defining syntax in a rule-exact abstract state.

F1: complement-input gate owner fails freshness, source, or payment checks. F2: both gates permit the same signed DEF facets or crossed facets pass. F3: semantic consequence [-8] may be emitted directly as a free original DEF record. F4: the consequence cannot be derived from authentic free facets plus exactly one paid RES node, or undercharging succeeds. All falsifiers were contradicted by source-code inspection and the original OS replay.

## Exact checker and external source binding

Original archived restricted checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. Original W29 certificate: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, Git blob 318c52d99977ea4e91bc8554051138a700c1dc94. Independently supplied original signed source: results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf, blob e8bc4300f1f4518cb447edaf3f699bcee4839803, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c. The executable compares all 17 externally supplied original signed clauses, in order, against the unchanged seed SOURCE records before invoking the checker. The historical /386 checker itself does NOT accept a separately supplied original CNF parameter; this additional binding is a property of the experiment, not the checker.

Base proof: 17 signed original SOURCE records, 28 paid oriented RES steps, one separately globally paid AND2 owner, no facets, 45 records total, W=29. Preserve every base SOURCE and signed parent edge. Only change the native gate_defs bank from [[0,8,1,4]] to A=[[0,8,1,-1]] or B=[[0,8,2,-2]]. Both gates are paid once with owner ID 0 and output wire 8, fresh relative to original wires 1..6 and guard 7.

For each complete original assignment, both gates compute z=0:
  
$$z=x_1\land\neg x_1=x_2\land\neg x_2=0.$$

The original program derives eligible DEF clause facets from SIGNED operands via views(z,a,b), not from the extensionally equivalent complete truth function. The authentic zero-paid facet sets are

$$V_A=\{[1,-8],[-1,-8]\},\qquad V_B=\{[2,-8],[-2,-8]\}.$$

An exact native DEF record using [1,-8] is accepted under A and rejected under B; [2,-8] is accepted only under B. The direct free DEF record [-8] is rejected under both, even though z=0 implies it. Two valid free DEF records [1,-8] and [-1,-8] plus one strict RES on pivot 1 yield [-8] at a new cost of exactly one paid step. The analogous derivation uses 2 under B. Both are accepted at W30, and both are rejected when spuriously charged W29.

## Theorem 587.1: semantic-owner quotient is not rule-exact

Let C_A and C_B be the two accepted W29 configurations. Let alpha_0 retain the exact original source, the entire prior signed record/parent DAG, paid owner ID and output, accumulated W, and the complete Boolean function truth table, while forgetting signed defining operands. Then alpha_0(C_A)=alpha_0(C_B), yet an authentic free facet [1,-8] is legal only from C_A. Consequently no rule-exact transition function on alpha_0 states can both accept every legal facet and reject all illegal facets.

This does NOT refute sound MAY abstraction. With gamma_0(s)={C:alpha_0(C)=s}, the existential MAY successor set

$$\widehat T_r(s)=\{\alpha_0(C'):\exists C\in\gamma_0(s),\,C\xrightarrow{r}C'\}$$

must preserve both genuine facets. Replaying the crossed choice in the wrong concrete owner produces a spurious trace, which may be refined without forbidding the authentic choice. The refinement alpha_1=(alpha_0,V_C), where V_C retains signed native defining-facet syntax and paid owner identity, separates the two configurations and is rule-exact for this fixed restricted facet-eligibility test. For the pinned bank/base DAG, the paid work marginal to expose the implied [-8] is one RES node, not zero. The two original genuine facets are free and the owner is charged only once. This is not a minimum theorem ranging over arbitrary alternative proofs, full R_mix341 or unrestricted SAT algorithms.

Proof: x AND NOT x equals zero for every valuation. All projected old records, source, paid owners and truth tables therefore agree. Direct application of the original program's facet enumerator gives the displayed disjoint V_A and V_B and its strict membership tests. Strict RES on pivot 1 or 2 resolves the two authentic clauses to [-8]; the original verifier checks their exact signed parent indices, pivot and conclusion. None of the authentic free facets equals [-8]. All original RES parent indices are correctly rebased when prefix records are inserted, preserving the entire shared proof DAG. The experimental original-OS execution confirms every claimed acceptance/rejection. QED.

## Reproducibility and hostile controls

The unchanged pinned checker executed as a **real Node.js v22.16.0 OS subprocess**, once per exact JSON packet. An independent source-file pin and signed-clause comparison precedes replay. All 64 original-variable truth assignments were checked for the two constant-zero gates. **18 differential cases: 6 ACCEPT and 12 REJECT; 19,764 original-checker assertion groups plus 66 bundled original negative controls across the accepted cases.**

Acceptances: two base W29 proof packets, two owner-matched single free facet W29 packets, and two legitimate two-facet + RES W30 packets. Rejections: two crossed facet packets, two directly inserted free [-8] units, two W29 underpayment attempts for the legitimate unit derivation, and six further corruptions of owner identity, defining literal, payment, parent chronology, SOURCE signed literal and foreign opcode. No independent reimplementation was used to decide checker acceptance.

Reproducer: experiments/arc/lspv3_587_semantic_gate_alias_cegar.cjs, Git blob 6b23029cff5aa147fbff0500c286b19d9411ae55. Raw 18-case original OS results: results/raw/arc/2026-11-12_0424_LSPV3_587_CONSTANT_GATE_FACET_OS_COMPACT.json, blob c2241d65d7ad9765e9b1330e41d2494e368c49b5. Exact checker-accepted facet packet: results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json, blob 4177ec15a0c7253378d5652a6b13b7152601d300. The separate reported physical certificate byte lengths, verifier execution effort, span and memory are not logical paid W.

## Reconciliation, prior work and scientific blockers

Read root proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2.txt blob 6291dd695659574f01ab982c36eaf5d21aeba4ba; issue #3 (including LSPV-2/573); AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; original /341 and /386 checkers; LSPV-3/539, /544, /549, /578, /580, /584, /586; LSPV-2/549 and /573; original mixed declaration, proposed CANON1, Grok 2026-11-12 09:17 UTC and Claude TPORT-0002. No historical complete R_mix341 checker surfaced. LSPV-2/573 had exposed operand-dependent facets for DIFFERENT Boolean functions; this result shows the failure persists for IDENTICAL full truth functions and gives the one-paid-step repair. No previously restricted result is promoted.

Primary literature: Cousot and Cousot, Abstract Interpretation, POPL 1977, https://doi.org/10.1145/512950.512973; Clarke, Grumberg, Jha, Lu and Veith, Counterexample-Guided Abstraction Refinement, CAV 2000, https://doi.org/10.1007/10722167_15; Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 1979, https://doi.org/10.2307/2273702. Compared external FRAT-XOR syntax https://github.com/meelgroup/frat-xor/blob/main/format.md; it is a DIFFERENT proof system and cannot authenticate the historical R_mix341.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1, separately P2-B2/B3, and P versus NP remain OPEN. Current root main.tex blob 8eda549cb687e942c264867ff3ad50ac04341136 could not be read through the repository connector even with requested tiny bounded line ranges, so there was NO safe LSPV-3-owned-region manuscript edit. Publication and readback of separately owned artifacts succeeded; full-repo preflight scripts and LaTeX compilation were not run without a full checkout. Exactly five current agent roles, their historical weights, ownership, America/Los_Angeles schedules and two Route A / three Route B labels remain unchanged; no automations created or modified.

**Next decisive dependency:** recover a single original-source-bound authoritative historical R_mix341 checker and accept/reject a genuine RES->AND3 or DEF-facet->LOCAL-CONVERT mixed edge. Feed this signed-facet counterexample to LSPV-2 (byte parser), LSPV-4 (resource cost), LSPV-1 (quantifiers) and LSPV-5 (adversarial replay).

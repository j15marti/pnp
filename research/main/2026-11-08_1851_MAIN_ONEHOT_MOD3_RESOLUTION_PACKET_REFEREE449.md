# LSPV-5/449: exact one-hot mod-3 ER2 Resolution packet

**2026-11-08 18:51 PST | Route B independent red team | PROVED/RESTRICTED for the separately declared signed-AND-definition plus ordinary-Resolution ER2 fragment; COMPUTATIONAL exhaustive and byte-packet replay; historical R_mix341, generalized mixed lower bound, and B3 remain OPEN.**

**Affected exact IDs:** [P2-L5-449], [P2-L1-520], [P2-L1-519], [P2-L1-518], [P2-L5-448], [P2-D1], [P2-C3], [P2-F6]. Peer [P2-L3-518] was reviewed as a separate source-linear Resolution upper control. Proof1 and Route A nodes are unchanged.

## IDEA: initial hypothesis and falsifiers

Initial hypothesis, stated before search: [P2-L1-520]'s finite-implicate-completeness argument does not by itself produce an exact clause needed by a downstream Resolution macro when weakening is unavailable; a derived proper subclause may omit the intended pivot.

Registered falsifiers were: (1) every relevant target has an exact ordinary-Resolution derivation; (2) frozen R_mix341 has a paid authenticated weakening rule and the construction charges it; (3) a compositional theorem shows that every downstream Resolution consumer accepts stronger subclauses by pivot-or-parent aliasing; (4) the local target is a prime implicate, so no proper subclause follows from the local premises.

Search falsified the broad Resolution-only version through (3): LSPV-1/521 located prior LSPV-1/442 and the standard subsumption theorem. A shared-DAG ordinary-Resolution suffix can be replayed topologically with a stronger same-context clause: resolve if both pivots remain, otherwise alias the parent missing the pivot. No weakening or duplicate shared work is needed. This does not automatically preserve exact typed AND3/GF(2)/LOCAL/DEF consumers, but /520's separately declared ER2 local Boolean macros are intended to expose clauses and then use ordinary Resolution. The revised target was therefore to materialize one requested exact clause packet rather than repeat the already known replay theorem.

## SEARCH: project, primary sources, and current corpus

- Complete live trackers read at start: `proof1.txt` blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** and `proof2.txt` blob **c47e614ee6f4e8ae0905675e1dff7edc48171510**. Current issue #3 was read at 1,413 comments and update time 2026-11-09 02:48:45 UTC. Any tracker publication below uses another complete fresh read and optimistic SHA lease.
- Governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` was checked against historical commit **4e29ed7646f484707767acb6e63ec5f38afd98a8**. `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md` blob **b8df83a7b0b1428f349b0e02ce1387d979e8db7f**, red-team modes **c211e9f545f94b636b119f1e721b475a31e925f9**, and protocol **25b38dc02bc0b0331ed03b0a4c7ff1b1e2a4ed00** were read. Local preflight completed but correctly reported that the scratch directory is not a repository checkout; complete GitHub files/blobs were used instead.
- Root `main.tex` was fully fetched through blob **63b54c9988cc83533472a05c25bda2ab48b5e4ca**, 1,786,990 characters, with one balanced ownership pair for every LSPV-1 through LSPV-5 and 102 OPEN-status sentences.
- Direct peer evidence: LSPV-1/521 report `research/agents/lspv-1/2026-11-08_1800_LSPV1_SUBSUMPTION_DUPLICATE_AUDIT521.md`, blob **3b6687e786dd89487676383c1e4eb6c32c51a4e4**, and its handoff blob **d46294e20d7739c314eeee8af1031a03b13a4f3c**; prior LSPV-1/442 blob **cd99bd6b75b68518a86b6159b756ecdb6e777394**; REFEREE372 blob **56993afbb42373445a5e795d8a115b6111f56ff1** and REFEREE373 blob **143a97a4808a48217c47fd946577ba6b14abe0be**. The last two remain exact-typed-consumer firewalls, not objections to pure Resolution replay.
- The target /520 report was read at blob **915aaa2be30ac06d75c63c2f625d24bd8a57fe09** and the /448 distinct-port repair at **8eb79a64d3c440d51671ae27e02f336760e0f6f5**. Current LSPV-3/518 Shannon Resolution report, blob **3632fbbddfe5ee1a7480fc866aea0be6102de2b4**, and executable blob **5e3ffa153a66b59775ff3d03cf741cf7f2ebdfd8** were read. Its every-matching $O(m)$ ordinary-Resolution upper bound is a legal shortcut control; only $n=4$ is strict 3-CNF.
- Historical declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob **c87acd11d32ccfc3b7acd3667ef11daeb60079cb**, remains the rule prose source. No complete authoritative historical byte checker was found or executed.
- Actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob **6942a99f176e996e9542f0386b7aa7fe2ce89e70**, and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob **79e4d4e7e0e3edff3aba8610852c45534bdde128**, were read. Neither supplies this packet or the missing historical transfer.
- Required change-aware repository review found unchanged heads: `konard/p-vs-np` **ecedd2b45f1c524d85c00b2da27a9c140025550c**, `blkph0x/p-vs-np-proof-research` **7dedc73f758dfbdc072e7aa29dfc08505761ebd5**, `meelgroup/frat-xor` **18cd6bc17af10a9891c10a846ce966166f9fe0dc**, `tanyongkiam/cake_lpr` **033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2**, `peitl/short-proof` **2c524cfceecf68b56f51d23f6b63255b502856d3**, `openai/math` **4eaee87548250b2682affda7d05d947c05554bae**, and `anthropics/formal-math` **16a5ce41304fcdaea4e0be7c132e1c361dc26da5**. None supplies an exact R_mix341 simulation. FRAT-XOR remains an external multi-hint format, and the formal-math ETH claim is not treated as authority for this project.
- Primary sources checked: Nienhuys-Cheng and de Wolf, *The Subsumption Theorem for Several Forms of Resolution* (1996), for unconstrained Resolution's subclause theorem; Shuo Pang, arXiv:2610.00837v2, for the fixed-$r$ opposite-characteristic lower bound; Cook--Reckhow (JSL 1979) for proof-system scope; Urquhart (JACM 1987) for expander-Tseitin ordinary-Resolution hardness. A separate Google-branded portal was unavailable and is not claimed.

## Family, theorem, encoding, shortcut, remaining-transfer ledger

| Family | Exact encoding/size | Established scoped theorem | Legal shortcut control | Remaining transfer |
|---|---|---|---|---|
| Pang opposite-characteristic mod-3 Tseitin [P2-L1-518] | Connected cubic $G$, even $h$; three one-hot variables per edge; canonical base $9h/2$ variables and $24h$ clauses. Pad each of the $9h/2$ binary clauses $B$ to $(B\vee z),(B\vee\neg z)$ using one fresh original $z$: $9h/2+1$ variables, $57h/2$ proper signed strict-three clauses, $N=\Theta(h\log h)$. | Pang Thm. 7.2(b)/Cor. 7.3: $\exp(\Omega_r(h))$ syntactic Res$(PC_r/\mathbb F_2)$ size for fixed $r$ on the stated expander subfamily, subject to preprint assumptions. Not all-algorithm hardness. | /520 balanced signed-ER2 cancellation, /448 distinct-port zero repair, matching-characteristic algebra, and the exact local packet below. | Vertex-source entailment, LCA cancellation/congruence packets, exact historical DEF/RES/LOCAL ports, and all-rule normalization remain OPEN. |
| Odd-charge cubic-expander Tseitin | Four proper signed ternary clauses per vertex, $3h/2$ edge variables, $N=\Theta(h\log h)$. | Exponential ordinary shared-DAG Resolution under expander hypotheses (Urquhart and subsequent width work). | Declared native AND3+GF(2) linear-size refutation, Cook/ER-style extensions. | Cannot transfer restricted Resolution hardness to the full mixed calculus or all algorithms. |
| $Q_n$ matching CNF [P2-L3-518] | $m=2^{n-1}$ original width-$(n-1)$ clauses, each excluding one matched edge; only $n=4$ is strict 3-CNF. | Source indispensability gives $m-1$ binary-node floor. | Uniform ordinary-Resolution upper below $2m$ nodes. | Not an asymptotically hard 3-SAT family and no generic XLRUP/native simulation. |

Certified UNSAT, named-system proof-size hardness, and empirical solver difficulty remain distinct. No empirical difficulty claim is used.

## ITERATE: exact packet construction

### Declared local interface

Let input groups be $P=(p_0,p_1,p_2)$ and $Q=(q_0,q_1,q_2)$, with the exact one-hot CNF for each group: one positive ternary clause and three pairwise negative binary clauses, eight input clauses total. Use fifteen paid, globally fresh, two-distinct-signed-input AND definitions:

1. nine term gates $t_{ij}\leftrightarrow(p_i\wedge q_j)$;
2. for each $k\in\mathbb F_3$, two gates computing the negation-AND implementation of $r_k=\bigvee_{i+j=k}t_{ij}$.

Every definition contributes its exact three standard facets. With deterministic IDs, the signed output literals are $r_0=\neg x_{17}$, $r_1=\neg x_{19}$, $r_2=\neg x_{21}$. The four required output clauses are

$$
(\neg x_{17}\vee\neg x_{19}\vee\neg x_{21}),
\quad(x_{17}\vee x_{19}),
\quad(x_{17}\vee x_{21}),
\quad(x_{19}\vee x_{21}).
$$

### Exact syntactic result

`lspv5_449_onehot_mod3_resolution_packet.py` performed a width-at-most-seven, subsumption-aware ordinary-Resolution closure and then emitted only the ancestry union of the four exact targets. The compact certificate contains:

- all eight input clauses and all 45 definition facets;
- 131 distinct, correctly oriented Resolution nodes;
- 184 total distinct lines and maximum used clause width six;
- unit-Resolution critical-path depth 12 for every target;
- canonical compact JSON size 13,945 bytes and SHA-256 **919b1df5f1a79c205199b4a6fa5b4d65962e88d49f5cd0acf016f9cdf8a45857**.

Under the separately declared ER2 accounting where each of the fifteen definitions and each Resolution inference has unit weight, this local macro has the explicit upper control

$$
W_{\mathrm{ER2,local}}\le 15+131=146.
$$

This is not a claim about unspecified historical weights or byte acceptance. Shared proof nodes used by multiple target clauses are charged once in the 131-node union.

### Independent validation and hostile controls

The generator exhausted all 64 input vectors: exactly nine satisfy both one-hot inputs, and all nine produce the correct one-hot mod-3 sum. Deleting an input positive clause admits a no-output countermodel; deleting an input pairwise-negative clause admits a multiple-output countermodel. Every literal deletion from every one-hot output target has a valid-input falsifying witness (nine witnesses total), proving the four targets are prime implicates of this local relation and triggering initial falsifier (4): no proper target subclause is entailed.

The closure created 5,308 candidate lines after 340,103 attempted resolutions, but only the 184-line ancestry union is emitted. Search/construction is not hidden inside the ideal proof measure. Measured generator execution was 5.4194 seconds with 15,488 KiB `ru_maxrss` in this runtime. Parsing, indexing, clause normalization, candidate generation, rejected attempts, output, and verification remain actual implementation work separate from the 146 logical-node bound.

Independent `verify_lspv5_449_onehot_packet.py` reconstructs the expected eight input clauses, fifteen distinct/fresh gate definitions and 45 facets from scratch, then replays every compact parent/pivot/conclusion. It accepts all 184 lines and rejects three independent corruptions: bad pivot, out-of-range parent, and altered conclusion. This verifier is independent code for the declared packet, not the authoritative historical checker.

## Revised status, barrier audit, and remaining gap

**PROVED/RESTRICTED advance:** one exact source/facet-indexed signed-ER2 one-hot mod-3 adder packet now exists. The broad subclause objection was falsified for ordinary Resolution by /442-/521, while this packet independently avoids it because all four output clauses are exact prime implicates. The result supplies one constant-size macro needed by [P2-L1-520].

It does **not** derive the input one-hot clauses from Pang's strict original vertex/edge sources, materialize the LCA exclusion-context identity, prove ancestor congruence/cancellation, authenticate historical definition-facet selectors, or show that the historical R_mix341 parser accepts these bytes. Exact AND3/GF(2)/LOCAL consumers remain non-monotone controls under REFEREE372/373. Thus [P2-D1], [P2-C3], [P2-B1], and [P2-B2] remain OPEN.

The packet is a context-free acyclic proof DAG. It introduces no branch, case-split, discharge, weakening, or semantic oracle. If later used under a context $\Gamma$, every premise and reused lemma must be lifted under the same legally justified context; this run proves no such historical lift. Relativization/algebrization do not turn this finite syntactic upper packet into an arbitrary-machine lower bound. Cook ER and matching-characteristic algebra remain mandatory stronger-system controls.

**Next decisive target:** materialize the exact source-indexed fixed-support Resolution packet that derives one vertex's mod-3 equation interface from the padded strict original clauses, then compose it with this adder under globally fresh IDs. After that, materialize one complete LCA pair-cancellation/congruence packet and attempt authoritative historical byte replay. Until these exist, /520 remains a declared-ER2 upper schema, not a theorem about exact historical R_mix341.

**P versus NP remains OPEN.**

## Artifacts

- Generator and self-checker: `experiments/arc/lspv5_449_onehot_mod3_resolution_packet.py`.
- Independent verifier: `experiments/arc/verify_lspv5_449_onehot_packet.py`.
- Raw summary plus complete compact certificate: `results/raw/arc/2026-11-08_1849_LSPV5_ONEHOT_MOD3_RESOLUTION_PACKET449_RAW.json`.
- Five-role handoff: `research/coordination/2026-11-08_1851_LSPV5_ONEHOT_MOD3_PACKET449_HANDOFF.md`.

## References

1. S.-H. Nienhuys-Cheng and R. de Wolf, *The Subsumption Theorem for Several Forms of Resolution* (1996), https://repub.eur.nl/pub/514/.
2. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026), https://arxiv.org/abs/2610.00837.
3. S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979).
4. A. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987).

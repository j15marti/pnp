% LSPV-1 REPORT::583::2026-11-11 16:00 PST
# LSPV-1/583: source-view composition requires exact occurrence binding, not equal component sources

**2026-11-11 16:00 PST | General SAT Lower-Bound Lead | Historical Route B | PROVED/RESTRICTED symbolic interface theorem; COMPUTATIONAL exact controls. P versus NP OPEN.**

## IDEA and four predeclared falsifiers

**Candidate D1-583.** For multiple *individually sound* proof components, exact equality of each component's entire source view to the external formula is a convenient sufficient firewall but is **not necessary**. A single immutable external original $F$, an authenticated occurrence-indexed source inclusion map from every local SOURCE premise into $F$, and **independently verified sound typed cross-component transitions** suffice to compose a completed refutation. No source substitution, arbitrary joining, or uncharged use of a secondary checker is permitted.

The claim addresses the potential interpretation of LSPV-5/496's exact-whole-source join $J(E,y)$ as a **necessary** condition. That original (J) theorem remains correct as a sufficient condition. This result does **not** rescue the LSPV-3/578 and LSPV-5/496 dual-checker polyglot: those sibling acceptance checks lack an authenticated shared external source and any native cross-rule transition.

Four falsifiers fixed before construction:

1. **F1 (source forgery).** The composed verifier accepts an altered external formula whose local clause contents are not bound to its occurrence IDs, including a satisfiable external source.
2. **F2 (view spoofing).** A component reads a clause or source identity absent from its declared view, or the view identifies a source occurrence absent from the immutable root.
3. **F3 (unsound join/context).** A reversed Resolution pivot, wrong resolvent, or an undischarged assumption is accepted as a cross-component refutation.
4. **F4 (work/oracle leakage).** A duplicate paid identity, unsupported inference opcode, absent empty goal, or fabricated uncharged join passes verification.

The deterministic implementation rejects all eleven hostile cases covering F1–F4. The symbolic theorem below does not depend on that finite test.

## SEARCH: required corpus and primary literature

Preflight read the complete root (proof1.txt) at Git blob `f46f6aae25571340a5fd17a5181d51c271509947` and (proof2.txt) at blob `42943fe447c6061fb8009a526f46ac8a6684765c` (1,024,949 UTF-8 characters); issue [#3](https://github.com/j15marti/pnp/issues/3) with current peer comments; `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; the 2026-11-09 abstract-interpretation five-role refocus; and the actual relevant LSPV-1/539, /543, /545, /553, /582; LSPV-2/341, /565, /566; LSPV-3/579; LSPV-4/552; and LSPV-5/496 results, as well as repository search of native checker, source grammar, LOCAL-CONVERT, DEF facets, and assumption discharge. Reviewed the pinned recovered /341 checker (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) and the declared five-rule /341 calculus (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`).

The latest LSPV-5/496 [independent audit](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-5/2026-11-11_1448_LSPV5_DUAL_CHECKER_SOURCE_FIREWALL_AUDIT496.tex) demonstrates that two original programs can accept the same JSON bytes while examining **different, incompatible** sources, one SAT and one UNSAT. It introduces the sufficient exact-byte condition (J(E,y)=\bigwedge_i(A_i$y$\wedge S_i$y$=E)). LSPV-2/565 independently authenticates a full signed-source occurrence multiset for the archived /386 sibling. Neither establishes that all components must contain *all* original SOURCE clauses.

Primary disciplines: Cook and Reckhow (1979), [doi:10.2307/2273702](https://doi.org/10.2307/2273702), on the formula-specific proof-verification relation; Cousot and Cousot (1977), [doi:10.1145/512950.512973](https://doi.org/10.1145/512950.512973), on concrete/abstract simulation; Clarke et al. (2000), [doi:10.1007/10722167_15](https://doi.org/10.1007/10722167_15), on counterexample-guided replay; and Baek, Carneiro, and Heule's FRAT (2022), [doi:10.46298/lmcs-18(2:3)2022](https://doi.org/10.46298/lmcs-18(2:3)2022), as a **distinct** formal-proof-interface example. No external proof system is substituted for the historical $R_{\mathrm{mix341}}$.

## THEOREM 583.1: exact-source-view composition, with quantified hypotheses

Fix arbitrary $n,m\ge0$, an **immutable** original source
$$
F=(C_1,\ldots,C_m)
$$
whose separate SOURCE occurrences have unique authenticated identities. Consider any finite number $k\ge1$ of components $P_1,\ldots,P_k$, each having a declared view $V_i\subseteq\{1,\ldots,m\}$, and a finite globally acyclic joint proof DAG $D$. Assume:

1. Every leaf referenced as SOURCE in any component or cross-component inference carries an *exact* clause occurrence ID $j\in V_i$ and the same signed Boolean clause $C_j$, authenticated by the external source, not merely by the packet's self-description.
2. Every paid and free logical rule application, including a cross-component bridge, is checked under **one explicit sound semantics**. Auxiliary definition owners are conservative, globally fresh or explicitly matched, with every defining facet attributed to its owner. Every assumption-context transfer, branch split, AND obligation, discharge and reconvergent join, if present, obeys its sound context rule. Nothing is inferred solely because another checker reports ACCEPT.
3. A single global paid-occurrence ledger gives each charged inference/owner a unique ID. Reusing an earlier verified result makes no new paid occurrence and no implicit new premise. Fixed nonnegative rule weights are charged **once per distinct paid occurrence**.
4. The final result is the empty Boolean clause in an assumption-free, fully discharged context, or an equivalently sound explicit contradiction view in the **same** authenticated calculus.

Then $F$ is UNSAT. **No assumption (V_i=V_j) or $V_i=\{1,\ldots,m\}$ is needed**.

**Proof.** Suppose $a\models F$. Every authenticated SOURCE leaf is one of the true clauses $C_j$ under (a). Extend (a) to every fresh conservative definition in its topological declaration order. Induct over the complete shared-DAG topological order. Sound inference rules preserve all their assertions under every valuation satisfying their premises, with the appropriately recorded contexts. Each sound discharged branch or join preserves the assertion in the resulting outer context; undischargeable contexts cannot supply the terminal goal. All nodes are therefore valid in the interpretation extending (a), including nodes used by several consumers. But the empty clause is false in every interpretation. Contradiction. Global occurrence identities affect cost, not this semantic induction. QED.

**Cost lemma 583.2 (conditional on the fixed rule tariffs).** If $E_{\rm paid}(D)$ is the set of distinct globally charged occurrences, the witnessed logical work is
$$
W(D)=\sum_{e\in E_{\rm paid}(D)}w_R(e).
$$
The paid work is a global union sum, not $\sum_i W(P_i)$; cross-component paid joins are included and shared paid owners counted only once. This proves no lower bound for arbitrary proof selection: $\overline W_R(F)$ minimizes over **every** legal whole DAG, including cheaper alternative refutations. It also charges neither the physical evidence bytes nor search, verifier work, span, actual time, or peak space, which are separate measures.

**Conservative CEGAR interpretation.** An abstraction retaining the root occurrence IDs, local views, exact signed parent ports and explicit verified joins can admit the genuine joint trace. Requiring every view to equal the root would reject this legal trace in the *declared* component calculus and is a **MUST-like underapproximation**, unsuitable as a general MAY coverage argument. It remains permissible as a restricted sufficient validation firewall. A truly native $R_{\mathrm{mix341}}$ abstract transformer still needs authenticated byte grammar and pricing for every historical operation. No cheap path is ruled out by a source-view mismatch alone.

## EXACT 2-VARIABLE COUNTEREXAMPLE TO NECESSITY OF FULL-VIEW EQUALITY

Let
$$
F=(x\vee y)\wedge(\neg y)\wedge(\neg x),
$$
with distinct signed SOURCE occurrences (s_0,s_1,s_2). Component (A) authenticates only $V_A=\{s_0,s_1\}$ and derives by one **paid** oriented Resolution on $y$:
$$
(x\vee y),\ \neg y\ \vdash_{\rm RES}\ x.
$$
Component (B) authenticates only $V_B=\{s_2\}$, the original $\neg x$ clause. A **separately paid, explicitly verified** cross-component Resolution on $x$ derives (□). The entire joint DAG has exactly two paid inference occurrences and three authenticated SOURCE leaves, and is valid as a typed SOURCE/Resolution proof of this root. Both component source views differ from each other and from the full root. There is no unchecked transfer from one accept/reject predicate to another.

The root is UNSAT by direct enumeration of its four assignments. If $s_2$ is **forged** from $\neg x$ to $x$, the altered root has exactly one model, $x=1,y=0$. The source-bound verifier rejects the original component's claimed $\neg x$ leaf before accepting any join.

## Reproducible computational audit

**Exact GitHub-published deterministic program**: [`experiments/arc/lspv1_583_source_view_join.cjs`](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_583_source_view_join.cjs), blob `ecc0157627048fa481123ef1cb4835b9f4b4239e`. **Raw results**: [`results/raw/arc/2026-11-11_1600_LSPV1_583_SOURCE_VIEW_JOIN_RAW.json`](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1600_LSPV1_583_SOURCE_VIEW_JOIN_RAW.json), blob `e686ef44bacb4c8f59e95896b679caeb11de55ab`.

The same self-contained JavaScript function was actually executed in a fresh V8 code runner. It checks the chronological exact signed Resolution rules; root occurrence binding; globally unique node IDs; empty assumption contexts; root model counts; and the terminal empty clause. Against the two-variable universe of eight distinct non-tautological signed clauses, the program exhaustively tested **32** root superformulas that contain the three baseline clauses. Every valid extension preserves this refutation and paid work two. All **eleven** hostile controls were independently rejected: false source, missing source identity, wrong view, wrong pivot, wrong resolvent, duplicate paid ID, undischarged assumption, unsupported unpaid opcode, missing terminal empty clause, unbound source occurrence and noncanonical source clause order. The original root has zero models; the signed forged root has one.

This executable was committed and reread in GitHub and is structured for standalone Node.js execution. **The published file has not independently been run through an operating-system Node subprocess.** V8 checks and a direct elementary proof are all claimed. This is a deliberately defined, sound SOURCE/RES *composition checker*, **NOT** an archived /341 or /386 or complete native mixed checker and **NOT** an all-rule $R_{\mathrm{mix341}}$ certificate.

## Full chain and barrier ledger

| Proof ID | Status after Result 583 | Exact gap |
| --- | --- | --- |
| P2-D1 | **OPEN** | Authenticating complete historical native accepted bytes, source occurrences and all mixed opcodes. Result 583 refines a *general interface necessity claim*, not the checker grammar. |
| P2-C3 | **OPEN** | Cost-sound MAY alpha/gamma and transformers for **every** native legal shared-DAG step, including source-view joins, paid owners, contexts and all unknown rules. |
| P2-B1 | **OPEN** | All-rule superpolynomial minimum whole-DAG lower bound on a known hard 3-SAT family with exact encoding and all GF(2), extension, branching, learning and circuit shortcuts permitted. |
| P2-B2/B3 | **OPEN separately** | Noncircular transfer from a concrete uniform SAT machine to polynomial minimum work for this **same** fixed calculus. |
| P1-01/03/04 | **OPEN** | General SAT decider, correctness and fully charged machine time/space. |

No superpolynomial lower bound follows. P2-C3 needs full native semantics before the theorem can be interpreted as its abstract-step coverage. The ordinary Resolution-hard expander Tseitin literature does not carry over to an unrestricted mixed GF(2) calculus: the declared /341 parity shortcut offers (4h-1) paid nodes on bridgeless cubic sources. The actual native RES/AND3 conversion remains unauthenticated.

**Barrier controls:** relativization/algebrization are inapplicable to this finite soundness-composition lemma as stated; there is no circuit-complexity property for a Natural Proofs argument and no computational time lower bound. The hard question remains uniform full-rule transfer, not a magic increase in the lower bound from joining these components. The CEGAR idea of concrete replay is applicable, but the cited generic CEGAR theorem does not authenticate historical byte syntax.

**Duplication and scope:** The proof is an elementary compositional soundness lemma; no academic novelty asserted. LSPV-5/496's equality-based (J) theorem is *not falsified*. Only an extrapolation from sufficient exact equality to necessary equality is refuted by the explicit source-bound join construction. LSPV-2/565's whole-source external binder is a correct sufficient checker design, not an assertion of necessity. Adopt immutable occurrence binding, explicit checked bridge, count-once owners; reject unchecked acceptance intersections. No previous full-system claim is promoted.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Latest root proof SHA values recorded above, with no change to P2-D1, P2-C3, P2-B1 or P2-B2/B3 node statuses. Historical LSPV-1 Route B, LSPV-2/4 Route A, LSPV-3/5 Route B, all five roles, fixed historical weights, timezones, schedules and ownership retained unchanged. No automation modification.

**Five-role handoff:** LSPV-2 should test external signed source subset-view APIs and native replay; LSPV-3 should seek authenticated cross-rule same-dispatcher joins; LSPV-4 should preserve global paid-node identity and charge evidence bits separately; LSPV-5 should independently falsify the source-view theorem, especially assumption scopes, forged occurrence IDs and nested DEF owners. LSPV-1 retains the quantifier/dependency ledger. **Next load-bearing target remains one authoritative source-bound native RES-to-AND3 or DEF-to-LOCAL-CONVERT accepted-byte certificate**, not an invented replacement grammar.

**P versus NP remains OPEN.**

% END_OF_VERIFIED_REPORT::LSPV-1::583

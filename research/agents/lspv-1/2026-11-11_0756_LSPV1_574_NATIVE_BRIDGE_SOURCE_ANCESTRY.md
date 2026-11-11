# LSPV-1/574: Archived native checker permits four mandatory SOURCE records outside the final proof cone

**2026-11-11 07:56 PST | LSPV-1 General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA and falsifiers

**Theorem 574.1 (P2-D1/P2-C3).** A complete original archived /386 SOURCE/DEF/strict-RES checker accepts a source-bound 143-record refutation with all 41 mandatory original SOURCE records, but only 37 in the final contradiction's ancestry. The four unused original SOURCE records are neither missing nor forged.

F1: the selected 10-vertex graph is not simple cubic with odd total charge. F2: the 36 retained signed clauses are SAT. F3: the unchanged original checker rejects a correct 41-SOURCE/102-RES/one-paid-owner proof for lack of complete terminal source ancestry. F4: hostile modifications of signed sources, RES pivots, parent IDs, cost, gate owners or opcodes still accept. F1-F3 were falsified by direct graph checks, symbolic proof and original-body checker acceptance; six F4 mutations rejected.

## Exact fixed original source

The graph has vertices 0 through 9 and ordered 0-based edges:

\[
(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),
(5,8),(5,9),(6,7),(6,8),(6,9),(7,8),(7,9),(0,5).
\]

Its 15 ordered edge variables are \(x_1,\ldots,x_{15}\); bridge edge \(x_{15}\) connects the two 5-vertex diamond components. Charge vector \(\chi=(1,0,0,0,0,0,0,0,0,0)\) is odd. The checker grounds four signed wrong-parity clauses per vertex and adds negative guard literal \(\neg g\) with \(g=x_{16}\). Source includes the unit \(g\). There are 40 vertex clauses and one guard unit, all 41 present in the certificate.

SOURCE records 0 through 39 are ordered by vertex and the wrong-parity triples in binary order. SOURCE record 40 is the guard unit. The final proof does not depend on original SOURCE indices \(D=\{1,2,21,22\}\), yet those four still occur exactly once as required.

**Symbolic proof of the 36-clause core.** The parity constraints at vertices 1,2,3,4 cancel internal edges and imply \(x_1\oplus x_2=0\). The constraints at vertices 6,7,8,9 imply \(x_8\oplus x_9=0\). The two retained vertex-0 clauses forbid bit patterns (0,0,0) and (1,1,0) on \((x_1,x_2,x_{15})\), so their conjunction with \(x_1=x_2\) and guard true forces \(x_{15}=1\). The two retained vertex-5 clauses forbid (0,0,1) and (1,1,1) on \((x_8,x_9,x_{15})\), forcing \(x_{15}=0\) when \(x_8=x_9\). Contradiction. This parity explanation is external reasoning; the accepted native certificate uses only genuine, paid strict Resolution steps.

A conservative extra paid Boolean definition owner represents \(x_{17}=x_1\land x_2\) and costs one, but has no defining facets in the proof cone. This legitimately activates the original CLI's paid-owner corruption control. Exact certificate accounting:

\[
\boxed{
N_{\mathrm{SOURCE}}=41,\quad
N_{\mathrm{SOURCE}\cap\mathrm{Anc}(\bot)}=37,\quad
N_{\mathrm{RES}}=102,\quad
N_{\mathrm{owners}}=1,\quad W=103.
}
\]

There are 143 proof records, 0 free defining facet records, and one owner declared outside the record array. All original SOURCE records are present, including the four terminal-dead records. This is a sound refutation of an UNSAT formula, not a checker-soundness defect.

## TEST and hostile controls

Original unchanged archived /386 verifier at experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**, was executed as a hosted V8 original function body. Adaptations affect only file/argv input, diagnostic SHA256 display and JSON-safe structuredClone compatibility, not the rule semantics. The positive packet **ACCEPTED** with 11,806 original assertions and all 11 original built-in corruptions rejected. Six independent hostiles also rejected: bad signed source, bad terminal pivot, dangling parent, underpayment, removed owner, invalid AND3 opcode.

An independent implementation rechecked all 102 exact parent-pivot-resolvent triples and exhaustively tested all \(2^{15}=32768\) edge assignments. Both the original 40-clause source and 36-clause reduced source had zero satisfying assignments. For every one of the 36 retained clauses a distinct computed witness satisfied the other 35, verifying that this particular reduced core is inclusion-minimal under single-clause deletion. Neither minimal cardinality among all cores nor optimal proof work was established.

The standalone Node >=18 program is published with an exact pinned checker SHA-1, real operating-system subprocess replay, the six negative controls and optional --write output. Its OS subprocess mode **was not executed during this hosted run** and awaits LSPV-5 independent execution.

**Reproducibility:**
- experiments/arc/lspv1_574_bridge_source_ancestry.cjs, Git blob 2720b0b1d4a71b605dc24d2e0e4d095f669c1a63.
- results/raw/arc/2026-11-11_0756_LSPV1_574_BRIDGE_PACKET.json, Git blob 1efb525f0c84dfffb626c00e592f4952cc796c69.
- results/raw/arc/2026-11-11_0756_LSPV1_574_BRIDGE_HOSTED_V8_RAW.json, Git blob de339776fafc1b617afe1209cdd5c52200159c6b.

## SEARCH: corpus and primary theory

Read root proof1.txt at blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b**, root proof2.txt at blob **7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3**, current issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md and recent five-role handoffs. Relevant actual prior work consulted includes LSPV-2/539 and /549 through /558, LSPV-3/551 and /571, LSPV-4/542-544, LSPV-5/488R1 and /489, and LSPV-1/569-573, with earlier /341 bridge essentiality noted. The observed /386 terminal-cone accepted-byte example is a different original checker and does not claim novelty for the general nonessential-clause phenomenon.

Historical R_mix341 prose remains research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). Distinct /341 verifier blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0 was not substituted. Primary theory checked: Cook/Reckhow, JSL 44 (1979), DOI 10.2307/2273702; Cousot/Cousot, POPL (1977), DOI 10.1145/512950.512973; Clarke et al., CAV (2000), DOI 10.1007/10722167_15; Ben-Sasson/Wigderson, JACM 48 (2001), DOI 10.1145/375827.375835. These results do not define the missing historical mixed-rule transition relation.

## Exact dependencies and role handoff

**P2-D1 OPEN.** Archived /386 requires full SOURCE presence but not source terminal ancestry. The distinct complete historical mixed checker, including SOURCE, RES, AND3, GF(2), LOCAL-CONVERT, paid DEF, facet and wire visibility, branching, weakening, contexts, discharge, joins, deletions and exact historical tariffs, is still unavailable.

**P2-C3 OPEN.** An abstraction forgetting terminal-dead SOURCE records must still preserve mandatory SOURCE completeness, source identities and original accepted byte semantics. It must not use the false premise that source presence implies terminal ancestry when deriving minimum-work lower bounds. All native transitions and cost-sound alpha/gamma remain unauthenticated.

**P2-B1 OPEN.** This bridge example does not refute bridgeless-source-essentiality bounds or establish a superpolynomial all-rule lower bound. GF(2), extensions, learning, sharing, reconvergence and compact shortcuts remain allowed for the historical fixed-calculus objective.

**P2-B2/B3 separate and OPEN.** Neither checker validity nor a finite certificate provides a noncircular same-calculus polynomial Wbar transfer.

LSPV-2 should maintain the source-versus-ancestry distinction while recovering a unified dispatcher. LSPV-3 should independently inspect source provenance and signed pivots. LSPV-4 should distinguish W=103 from evidence bits, checker operations, span and physical time/space. LSPV-5 should run the native OS replay and challenge the 36 deletion witnesses. LSPV-1 retains the exact quantifiers and dependency ledger.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The specific bridge caveat was already known and the load-bearing statuses are unchanged. No research role, title, hourly schedule, historical weight, ownership boundary, or TWO Route A / THREE Route B allocation was modified. P versus NP remains **OPEN**.

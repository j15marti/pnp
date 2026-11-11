# LSPV-2/554: Archived /386 gate-owner dependency-order transport

**2026-11-11 03:16 PST | SAT-Circuit Reduction Builder | Historical Route A | PROVED/RESTRICTED code theorem + COMPUTATIONAL (12 original-CLI hosted-V8 tests). P versus NP OPEN.**

## One construction and four falsifiers

Construct an accepted K4 guarded-source certificate with three paid AND2 gate owners, two independent and one nested. Claim: permuting its gate-owner declarations preserves original-checker acceptance and logical price **exactly** when the new declaration order is topological for the signed input-wire dependency DAG.

Precommitted falsifiers: (F1) legal independent-owner reorder rejected; (F2) dependent owner declared before its producer accepted; (F3) complete original CLI hostile tests fail after a legal reorder; (F4) wrong signed facet, absent gate owner, altered original source, wrong RES parent or underpaid summary accepted. All four are excluded for the tested packet. The general iff is proved directly from the pinned code.

## Source/corpus/research status

Original /386 checker: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Original previously accepted /553 seed: results/raw/arc/2026-11-11_0213_LSPV2_553_ACCEPTED_PREFIX_K1.json, blob **5426883cf45e4fbccc5cc8661e91c08e4e0cb625**.

Reviewed both living proof trackers, issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, actual LSPV-2/539-553 reports and latest five-role handoffs. Prior work: LSPV-1/566 established a **proof-record** topological transport, while LSPV-2/553 established repeated free DEF facets. Here the transport acts on the **separately declared paid owner list**, allowing a different independent quotient of one archived calculus.

Relevant primary external literature: Cook and Reckhow, Relative Efficiency of Propositional Proof Systems (JSL, 1979); Cruz-Filipe et al., Efficient Certified RAT Verification (2017); Clarke et al., Counterexample-Guided Abstraction Refinement (CAV, 2000); DRAT-trim official source repository (marijnheule/drat-trim). None defines this lost R_mix341 mixed-rule byte grammar.

## Theorem 554.1: exact archived /386 gate-owner ordering (PROVED/RESTRICTED)

Fix a packet P accepted by the pinned archived /386 mathematical function checkProof. Gate-owner tuples have distinct owner IDs and distinct fresh outputs, each with two signed inputs that are original variables or outputs of earlier declared gates. Define the gate DAG D with edge j -> i whenever one signed input of gate i has absolute value equal to output z_j of owner j. For a permutation pi of the gate_defs rows, keep everything else exactly the same, including IDs, output wires, records, source, pivots, clauses and summary.

Then, **for this pinned mathematical checker**,

$$
\operatorname{Accept}_{386}(P^\pi)=1
\quad\Longleftrightarrow\quad
\pi\text{ is a topological order of }D.
$$

For every accepted permutation,

$$
W(P^\pi)=N_{\mathrm{RES}}+|V(D)|=W(P).
$$

**Proof:** In every topological order, the exact original code's gate_defs prepass sees each signed derived input only after its unique output has been stored in defs. All stored owner IDs, outputs and signed defining-facet clause sets are unchanged. Subsequently SOURCE checks depend only on fixed original graph/charge/guard, DEF facet checks use the same owner-ID maps, and RES steps use the unchanged chronological parent-index graph, signed pivots and derived clauses. Source completeness, sink emptiness, graph controls and all summary counts agree. Conversely, if a producer comes after its consumer, the consumer input is neither an original edge wire (all gate outputs are greater than the original edge count) nor present in defs at its check, so the original checker throws the forward-declaration error. Count-once work is invariant. QED.

**Scope qualification:** The archived /386 complete CLI also runs eleven synthetic corruptions. For an arbitrary mathematical-checker-accepted packet, those extra testing controls can depend on the first gate owner and need not be invariant. Here all three paid owners have genuine DEF facet records, so deleting the first owner breaks the packet in every accepted permutation. Therefore this specific packet passes the complete original CLI for every legal order. The theorem is not about a unified R_mix341 implementation.

## Exact source-authenticated construction

Use the original odd-charge signed K4 source of sixteen guarded three-clauses plus one guard unit. Retain all seventeen SOURCE records, the original twenty-eight paid RES nodes and their exact shared dependencies. Add two zero-additional-charge DEF records, shifting older RES parent references by the corresponding chronological bijection, and declare the owners as follows:

| ID | output | signed inputs | ancestor owner |
|---|---:|---|---|
| 0 | 8 | (1,4) | none |
| 1 | 9 | (2,5) | none |
| 2 | 10 | (8,3) | 0 |

The three checked, free facets are [1,-8], [2,-9] and [3,-10]. All original SOURCE, charge, branch-free context, fixed weights and paid identity sets remain unchanged.

The published accepted packet has **3,039 UTF-8 bytes with LF**, **48 records** (17 SOURCE, three zero-paid DEF facets, 28 RES), and exact logical price **W=31** (28 distinct RES plus three paid gate owners). This is a finite accepted original-checker witness, not an optimized proof, an invented rule or a complexity bound.

| Owner ordering | Complete original checker | Paid work | Original assertion groups |
|---|---|---:|---:|
| [0,1,2] | ACCEPT | 31 | 3,329 |
| [0,2,1] | ACCEPT | 31 | 3,322 |
| [1,0,2] | ACCEPT | 31 | 3,342 |
| [1,2,0] | REJECT, forward wire | n/a | n/a |
| [2,0,1] | REJECT, forward wire | n/a | n/a |
| [2,1,0] | REJECT, forward wire | n/a | n/a |

Six further hostile packets were rejected by the original code: wrong facet, missing owner, wrong paid charge, future RES parent, corrupted original signed SOURCE, and foreign LOCAL-CONVERT opcode. The last rejection is limited to this *sibling checker*. It cannot exclude LOCAL-CONVERT from the unrecovered full historical calculus.

**12/12 expected outcomes, three accepted and nine rejected.** All three acceptances also passed the eleven original bundled corruption tests: 9,993 original checker assertion groups across the three positives.

Execution used the original mathematical and complete CLI source in hosted V8, adapting only file input, deep-clone availability and output-only hash printing. This is **not a claim of an independently executed OS Node subprocess**. Published executable experiments/arc/lspv2_554_gate_owner_dag_transport.cjs pins the original checker and seed by exact Git blob, writes all 12 byte-exact packets and invokes actual OS Node subprocesses on systems with a checkout. That executable has been committed but was not executed end-to-end in this run. Raw original-body matrix: results/raw/arc/2026-11-11_0316_LSPV2_554_GATE_OWNER_TOPOLOGY_V8_RAW.json; byte-exact positive certificate: results/raw/arc/2026-11-11_0316_LSPV2_554_ACCEPTED_GATE_ORDER_012.json.

## Restricted abstract transformer / CEGAR

For archived /386 only, concrete owner-creation state contains the source identity, owner ID and output-wire maps, signed parent dependencies, a declared-owner down-set, its free facet banks, original clause provenance, all live and shared RES records, and exact count-once paid identities. An alpha projection forgetting only the *particular topological owner-list order*, retaining D and its signed owner/facet semantics, represents all three authenticated paths with unchanged cost and completed refutation. Gamma includes only source-equivalent accepted /386 representatives of that owner-labelled graph; there is no future-wire shortcut.

A coarse order-insensitive MAY abstraction admits the spurious order [2,0,1]; a CEGAR refinement adding the producer-before-consumer condition removes this spurious route without excluding any genuine permutation accepted by the pinned checker. The exact logical cost remains W#=W=31 for this packet. Full P2-C3 still requires all authenticated operations and stepwise alpha/gamma, assumption discharge, shared DAG identities and legal shortcuts. Certificate bit length, ideal span, physical time, construction cost and peak writable space remain separate, unmeasured resources.

## Reconciliation

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root proof chain status warrants promotion. [P2-D1] full historical accepted-byte grammar, [P2-C3] all-rule cost-sound abstraction, [P2-B1] superpolynomial all-rule lower bound, and separate [P2-B2/B3] noncircular transfer remain **OPEN**. P versus NP remains OPEN. No automation was created, renamed, disabled or rescheduled; all five identities, historical tariffs, ownership markers, TWO Route A and THREE Route B labels remain intact.

**Next falsifier:** Independent full OS Node replay, then locate an original *single checker* accepting genuine RES-to-AND3 or DEF-to-LOCAL-CONVERT shared dependency, with positive and corrupt-port controls before upgrading P2-D1.

# LSPV-1/624: unique false base affine row in accepted /341 SAT-source packet

**2026-11-13 America/Los_Angeles (PST) | GENERAL SAT LOWER-BOUND LEAD | historical Route B | PROVED/RESTRICTED plus COMPUTATIONAL. P versus NP remains OPEN.**

**Affected proof IDs:** candidate recovered checker P2-D1 = FAIL as sound proof predicate on its *full operational accepted language*, consistent with LSPV-3/551, /609 and /620. The desired historical unified R_mix341 P2-D1 remains OPEN/NOT QUALIFIED, as do P2-C3 and P2-B1, with P2-B2/B3 separately OPEN. This result is the exact first-fault isolation and model-complete audit of the previously reported SAT-source fixture, not discovery of a new checker or new unsoundness mechanism.

## Predeclared candidate and three falsifiers

Candidate S624: in the pinned /341 two-fixture accepted packet, all 64 genuine models of the second signed SOURCE formula satisfy every one of the eleven correctly typed local AND3 affine rows, while each violates the first row d2. Consequently the final XOR contradiction is a one-defective-premise artifact, not a valid UNSAT derivation.

F1: one of the 64 reported models actually violates a signed source clause, or all 64 cannot be obtained by exhaustive enumeration and GF(2) rank. F2: a local affine row other than d2 fails on some genuine source model, or d2 holds on one source model. F3: the original in-band packet differs from the pinned model, supports, masks or source; the original verifier rejects rather than accepts the packet. F1 and F2 were defeated by independent new symbolic argument, OS Node regenerated-source enumeration and independent connector V8 exact packet analysis. For F3 the pinned JSON Git blob was read and checked field-by-field through GitHub; original archived checker acceptance is reported by LSPV-3/551 and /620, NOT independently OS replayed in this run.

## Pinned original source and checker

- Original two-fixture packet: results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json, Git blob 706947c767361e7c979b8208677eb983d33838f4.
- Original checker: experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.
- Original signed SAT-source CNF: results/raw/arc/2026-11-13_1128_LSPV3_620_ACCEPTED_341_SAT_SOURCE.cnf, Git blob c6f8bbf09baf6547de6fea04ac74dd0ecb32f6bd.
- Source: 12-vertex connected cubic BRIDGE_K4x2 graph, 18 edge variables, 48 signed proper ternary clauses, original f.charges[0] a JavaScript String "1", and eleven remaining numeric-zero charges. Proof has 47 paid AND3/XOR records. The mixed Resolution/DEF/LOCAL-CONVERT/CASE dispatcher was not recovered.

## Theorem 624.1 (exact unique-base-fault normal form)

Let F be the literal 48-clause signed in-band source of the pinned /341 packet. Write x1,...,x18 for its edge variables, and let R_v be the degree-three vertex incidence masks for v=0,...,11, indexed as in the source packet. There are exactly 64 models of F. Every model of F satisfies the eleven affine rows R_v=0 for v=1,...,11 and violates the claimed native row d2: R_0=1. All other eleven native row-producing AND3 aliases are valid on all 64 models. The eleven XOR descendants d36,...,d46, including 0=1, are false on all 64 models because the sole false d2 row is inherited.

**Proof (symbolic, independent of checker verdict).** At exceptional vertex v=0 the four original clauses are

$$
(x_1\vee x_2\vee x_{13})\wedge
(x_1\vee x_2\vee\neg x_{13})\wedge
(\neg x_1\vee\neg x_2\vee x_{13})\wedge
(\neg x_1\vee\neg x_2\vee\neg x_{13}).
$$

Their exact conjunction is

$$
x_1\oplus x_2=1,
$$

which leaves x13 unrestricted *locally*. Each other vertex has the complete, correctly typed even-parity four-clause source, so its incident edge XOR is zero. The graph is connected. Its eleven nonexceptional incidence rows are linearly independent over GF(2), since the full incidence matrix of a connected graph has rank V-1 and deleting any one row leaves an independent set. The exceptional row x1 XOR x2 is independent of those eleven: the sum of eleven nonexceptional rows is x1 XOR x2 XOR x13, and x13 occurs in no nonexceptional-row linear combination yielding x1 XOR x2. The source rank is therefore 12 on 18 variables, giving exactly 2^(18-12)=64 satisfying edge assignments.

XOR-ing the eleven true nonexceptional vertex rows cancels every edge outside vertex 0, giving

$$
x_1\oplus x_2\oplus x_{13}=0.
$$

Combining with x1 XOR x2=1 forces x13=1 on **every** genuine source model. Native d2 instead claims

$$
x_1\oplus x_2\oplus x_{13}=1
$$

with mask 0x1003 and rhs 1. Thus d2 is false on every one of the 64 models. The eleven remaining native local rows have their correct incidence masks and rhs 0 and are all true. XOR descendants of this single incorrect affine row with only true zero-rhs rows retain a false affine equality. This is the unique false *base affine row*, not a proof that every preceding factor representation is correctly typed. QED.

**Exact operational mechanism:** String charge "1" passes the checker’s numeric strict-inequality source-pattern filter even for forbidden patterns of wrong parity, while bitwise XOR coerces "1" numerically. The output d2.support is String "012", not [0,1,12]; JavaScript "012".includes(12) returns true because it sees substring "12", but character-indexed truth-table evaluation uses coordinates 0,1,2, not 0,1,12. Hence a false row alias is certified by the defective checker.

**CEGAR consequence:** If the unchanged /341 checker really accepts the packet, this is an actual checker path, not a spurious abstract shortcut. CEGAR must not erase it while claiming all-transition inclusion. Any sound UNSAT interpretation of that entire accepted language fails. A new repaired/typed checker can be studied separately but cannot be called the original historical authority.

## Evidence and hostile controls

- Independent OS Node.js regenerated the exact graph and all 48 signed clauses, verified rank 12, enumerated all 262144 assignments, found 64 models, and verified d2 is false on all 64 while other eleven rows hold. Its source-only mode was executed; exact original-packet hash/field verification mode and --native OS checker subprocess mode were **not** executed locally because the repository was unavailable in the container.
- A separate connector V8 analysis fetched the unchanged pinned JSON packet at its exact Git blob, directly enumerated the 262144 assignments over its actual 48 clauses, and evaluated the native twelve row masks and eleven XOR descendants. Results: source SAT=64, each of 11 correct base rows false on 0 models, d2 false on 64, and each XOR descendant false on 64.
- Hostile semantic controls from this exact second audit: replacing the exceptional source quartet by the standard odd-parity quartet yields 0 models; replacing it by the standard even-parity quartet yields 128 models; correcting d2 rhs from 1 to 0 makes that row true on all 64 original models. All three controls matched the expected GF(2) rank/parity account.
- Explicit source witness x1..x18: 101001000000100000.
- Code: experiments/arc/lspv1_624_first_bad_alias.cjs, Git blob b8f2c65c137a546089f729fa60b81c08c5267a10.
- Raw: results/raw/arc/2026-11-13_LSPV1_624_FIRST_UNSOUND_ROW_RAW.json, Git blob 4d3f1dc3e9374d72336bf8cad69b1c3033dde370.

**No independent original-checker OS verdict** was produced in this run. Prior original-body hosted V8 acceptance is evidence reported in LSPV-3/620 and earlier work, not a fresh native reproduction by LSPV-1/624. The exact full historical mixed authority is still unidentified. The source result does not constitute a lower bound of any kind.

## Chain and hard-family status

Gate S=P2-D1: recovered /341 is unsound on its whole accepted packet language; recovered /386 enforces its own odd-charge guarded source domain and is not an arbitrary external-source proof system. The actual historical complete R_mix341 accepted-byte grammar/source binding/soundness/coverage is missing. Before any whole-calculus proof potential or Gate T transfer, the genuine authority must be authenticated. Recovered /341 **candidate fails**; full R_mix341 qualification remains OPEN, not automatically failed or repaired.

Gate T=P2-B2/B3: independently require SAT in P implies eventually Wbar_R(F_n)<=C*N_n^d on an explicit family F_n and **the identical** qualified calculus. Arbitrary correct rejecting computations are not native source entailment proofs. A family-only detector with fast per-instance time does not establish a bound in worst-case T_A(N), as emphasized by LSPV-4/591. LSPV-2/604 DPLL-to-RES is a scoped positive compiler, not an arbitrary-decider transfer.

P2-C3: every actual native transition must be abstractly simulated at no higher charged cost, maintaining whole shared paid identity, source provenance, active/discharged contexts, wire freshness, AND obligations and all unknown legal rules as conservative MAY. P2-B1: prove superpolynomial potential on explicit hard 3CNFs of encoded bit lengths N_n, including *every* native shortcut; no such potential exists yet. This run supplies a qualification counterexample, not a new hard-family lower bound.

## Literature, corpus, and role interface

Both root proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and full proof2.txt (blob 930c5eeddafce656717f28055a7a9a755f44737c, 1,051,196 chars, read via GitHub contents fallback), issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, 2026-11-13 two-gate user handoff, LSPV-3/551 and /609 and /620, LSPV-2/547 and /604, LSPV-5/527 and current peer comments, and prior archive pointers including the 539-549 series were consulted. This is not a complete independent audit of every historic peer/Grok/Claude paper or the entire root main.tex. Report 551 already states the exceptional source formula and false row; the **new** scoped increment is the unique-base-row, all-64-model isolation and exact 11-correct/11-descendant-false partition with three negative semantic controls.

Primary method references: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44:36-50, for sound fixed proof-system semantics; Cousot and Cousot (1977), *Abstract Interpretation*, POPL 238-252, for sound concrete/abstract inclusion. Neither authenticates the historical R_mix341 program. CEGAR cannot turn an actual accepted semantic error into a sound proof.

**TRACKERS REVIEWED; NO MATERIAL LOAD-BEARING NODE STATUS CHANGE:** root proof1.txt and proof2.txt unchanged. Statuses remain P2-D1/P2-C3/P2-B1 OPEN, P2-B2/B3 separately OPEN, and P1-01/03/04 OPEN. No automations, role titles, identities, schedules, original rules/tariffs, ownership regions, Pacific timezone or two Route A / three Route B allocation were modified. Root main.tex must be separately reconciled only inside LSPV-1 ownership region with complete-current-file safe SHA, or reported blocked. Full preflight and LaTeX compilation were not run.

**LSPV-5 independently falsify:** execute unmodified checker in an OS Node process against pinned accepted packet, verify source blob and accepted stdout; inspect whether a different genuine historical dispatcher authorizes the full rule set. Obtain a minimal source-bound native RES-to-AND3 or DEF-to-LOCAL-CONVERT certificate. P versus NP remains OPEN.

END_OF_VERIFIED_REPORT::LSPV-1::624

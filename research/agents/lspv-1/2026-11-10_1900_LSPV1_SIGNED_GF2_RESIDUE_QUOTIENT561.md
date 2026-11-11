# LSPV-1/561: Signed GF(2) residue projection on the recovered native fixture checker

**2026-11-10 19:00 PST | PNP General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED symbolic + COMPUTATIONAL original-code replay | P versus NP OPEN**

**Dependencies:** [P2-D1] -> [P2-C3] -> [P2-B1], with [P2-B2]/B3 separate, all OPEN. [P1-01], [P1-03], [P1-04] OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Five roles, titles, schedules, time zones, historical weights, ownership and two Route A/three Route B unchanged.

## IDEA and four falsifiers, registered before SEARCH

**Candidate 561.1.** For EVERY parsed proof packet ACCEPTED by the pinned recovered historical SOURCE/AND3/XOR cubic-Tseitin **fixture** checker, project every paid affine row mask simultaneously onto the E original edge-variable coordinates. This preserves checker acceptance, the entire globally unique paid-node identity set, whole-DAG references, and exact logical work, even when masks are negative signed BigInts or contain arbitrarily high bits. It is a one-way **accepted-packet** representation normalizer, not a general R_mix341 rule, not source-authenticated UNSAT soundness, and not a full-calculus lower bound.

F1: negative BigInt masks or AND3 aliases cause checker acceptance to depend on high sign-extension bits after projection. F2: low-bit projection does not commute with exact parent XOR and changes a valid sink. F3: the verifier inspects discarded mask bits elsewhere in source, charge, witness, paid-node, or summary checks, rejecting a projected previously accepted packet. F4: the operation mistakenly promotes the already accepted satisfiable-source counterfeit to a genuine mathematical UNSAT proof. F1-F3 are excluded by direct inspection and proof of the actual code; F4 is explicitly denied, with an accepted SAT-hostile replay.

## SEARCH: exact original artifacts, previous work, and literature

The historical mathematical declaration is research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (Git blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). Free SOURCE; one unit per **distinct** paid RES, AND3, XOR/GF(2), LOCAL-CONVERT, conservative binary DEF; shared acyclic proof DAG. **No complete accepted-byte grammar** is supplied for all five rules, definition facets, contexts, branching, weakening, discharge or deletion. Original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js (Git blob 4081022e8a3841d79f751a3d3a7a10decbb026da); actual recovered independent checker: experiments/arc/lspv2_341_independent_verify.js (Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0). This executable recognizes only the SOURCE/AND3/XOR fixture fragment, checks exactly 4V-1 paid records and has **no independently supplied DIMACS binding**.

**Predecessor distinction.** LSPV-5/413 recovered original-code scope; LSPV-1/553 exposed incomplete accepted-rule coverage; LSPV-1/556 found paired **positive** ghost-mask variants; LSPV-2/538-545 found ill-typed supports, lexical aliases and invalid UTF-8 raw-byte acceptance. LSPV-3/551-558 exposed accepted SAT counterfeit packets and, in /558, a **whole-packet source-driven regeneration** with external source binding; the present work instead proves a **local step-by-step signed-mask quotient on every accepted packet**, leaving all paid IDs and original fields intact. LSPV-4/528 warned that quotienting **occurrence identities** by semantic row labels can create false cycles. This theorem never merges or renames occurrence IDs. LSPV-4/531 and LSPV-5/467 distinguish actual verifier peak space and whole-DAG count-once accounting.

Reviewed original complete root proof1.txt (Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters) and proof2.txt (Git blob 12745b7b10a0b698d7828979d0b8293eef4a61f9, 963,424 characters); issue #3 and 1,598 comments, AGENTS.md, CODEX.md, repository pnp-research/SKILL.md, the two November 9 governing handoffs, LSPV-1/553/560, LSPV-2/545, LSPV-3/555-558, LSPV-4/523-524/531, LSPV-5/467, and targeted recent 539-549 corpus results. This is a change-aware substantive selection, not a claim to have reread every report in 539-549 individually. Original Grok note GROKPROOF/2026-11-11_0120_PROGRESS.md and original Claude TPORT-0001 were also checked.

Primary literature: [1] Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44, 36-50, DOI 10.2307/2273702, supports exact proof-system and evidence-cost distinctions; [2] Cousot and Cousot (1977), *Abstract Interpretation*, POPL, DOI 10.1145/512950.512973, supports the MAY simulation direction. These sources do **not** authenticate R_mix341 bytes. Original-file external repository review: konard/p-vs-np/scripts/proof_status.json, Git blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md, Git blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md, Git blob 986a21aa92b62f844ef1fce852193142c41b2b1f. The latter is a separate XLRUP/FRAT-XOR externally authenticated **different** proof language, not the missing native byte grammar.

## Exact Theorem 561.1: accepted-packet, cost-equal signed-mask projection

Fix any **parsed packet P accepted by the pinned original recovered checker**, with all of its original source, graph, charges, proof DAG, parent IDs, optional affine masks and witnesses. For each graph fixture with E edge-variable coordinates, and for every existing paid record carrying an affine row mask M interpreted by the original BigInt parser, define

$$
\pi_E(M)=M\mathbin{\&}(2^E-1),
$$

where bitwise AND is JavaScript BigInt two's-complement arithmetic and the result is the canonical nonnegative low-E-bit residue. This operation is meaningful for signed negative integers, positive integers, and accepted BigInt-coercible JSON encodings. Simultaneously replace **every** AND3 optional affine row mask and **every** XOR row mask by the canonical hexadecimal encoding of its projected value. Keep all SOURCE clauses, graph, charge, original IDs, paid IDs, antecedent references, support, factor table, row RHS, kind, ordering, deletion witnesses, even witness and summary unchanged. Call this map Pi.

**PROVED/RESTRICTED:**

$$
\boxed{
\mathrm{Accept}_{341}(P)
\Longrightarrow
\mathrm{Accept}_{341}(\Pi(P)),\qquad
W(\Pi(P))=W(P),\qquad
\Pi^2(P)=\Pi(P).
}
$$

Here W counts **distinct paid inference-node first creations** in this specific fixture language, not evidence bytes, physical CPU work, or a minimized complete-calculus proof length.

**Proof.** The recovered verifier first authenticates graph, internally stored signed source clauses, charges, source identities, deduction length, deletion/even witnesses and metadata. None of those checks accesses high affine-mask coordinates, and none of those fields is altered. For a paid AND3 row alias the verifier checks the parity row's support and exact local Boolean correspondence by iterating only edge coordinates e in 0,...,E-1. Thus Pi leaves every computed table bit, supported literal coordinate and alias check unchanged, including when the original accepted BigInt is signed negative and has sign-extended high ones.

For each XOR instruction the verifier compares the full BigInt output mask with the XOR of its two parent masks and compares the parity RHS. For all integers A,B, including signed ones, low-E residue is a bitwise XOR homomorphism:

$$
\pi_E(A\oplus B)=\pi_E(A)\oplus\pi_E(B).
$$

All the input and output affine rows are projected simultaneously; their exact XOR equalities remain valid. Their RHS values, reference IDs, topological ordering, proof DAG and occurrence identities remain identical. The original checker-accepted sink has exact full BigInt mask zero and RHS one, and Pi leaves it zero/one. Consequently every acceptance test survives. The original checker-enforced paid length is unchanged, every paid identity is still unique and all shared references still refer to the same paid occurrence, so cost equality holds. Finally the residue is already in [0,2^E-1], proving idempotence. QED.

**Critical nonconverse.** A K4 packet with one signed negative high-bit AND3 alias, all subsequent XOR rows correctly recomputed, has terminal mask -64 instead of zero and is REJECTED by the original checker. Its projected packet is ACCEPTED, with exactly the same 15 paid nodes. Therefore the theorem is only ACCEPT implies ACCEPT after projection; an abstract path admitted after projection may be spurious with respect to a particular unprojected packet.

**Critical semantic-soundness counterexample.** An original-checker-accepted 48-clause signed proper 3-CNF packet is actually SAT, witnessed by the explicit 18-bit assignment 101001000000100000. The original checker accepts it with 3,273 assertions and also accepts its projected packet with the same count. Thus the theorem does NOT imply accepted source UNSAT, NOR a goal-preserving abstraction for mathematically valid unsatisfiability without separately sound SOURCE/charge/support/definition checks. LSPV-1/559-560 and LSPV-3/558 supply *separate guarded* retractions. Their guards cannot be silently omitted.

## P2-C3 abstract-state interface and resource account

For the recovered accepted-prefix **fragment only**, concrete state is

$$
C=(F_{\rm packet},G,\chi,D,\mathrm{Paid},\mathrm{Parents},
\mathrm{Types},\mathrm{Supports},\mathrm{Tables},\mathrm{Rows},
\mathrm{SourceIDs},q).
$$

D is the **entire ordered shared occurrence DAG**, Paid records each distinct charged first creation, and q is cumulative logical native-fixture charge. The abstract map alpha applies Pi to every paid affine mask, leaving every other field, especially source IDs, occurrence DAG and paid history, exactly unchanged. Gamma contains all accepted-prefix concrete states whose projected form is the abstract state. For every actual accepted AND3/XOR extension, the theorem constructs an abstract extension of the identical logical charge (one for each fresh paid ID, zero new *inference* units for reuse), preserving the **checker-accepted** terminal. This is a genuine local cost-equal transition simulation on the pinned recovered fragment, but cannot establish a semantic UNSAT goal if the checker itself accepts SAT-source counterfeits.

Contexts, branches, discharge, definition owners, private/exported wires and RES/LOCAL-CONVERT are **not present in this recovered fragment**. Their absence is **NOT** permission to delete them from the full historical calculus: until authoritative original bytes/rules are authenticated, an all-native MAY abstraction must conservatively overapproximate all such potentially legal transitions. Do not infer any full-calculus B1 distance from this projection.

The ideal W is distinct from serialized certificate bits: hexadecimal normalization may enlarge or shorten strings, while negative masks are finite encoded integers despite infinite mathematical sign extension. Node materializes full JSON and byId maps; parser buffers and high-water work space were not measured. Actual BigInt processing, authentication, source access, recomputation, output, span, proof discovery, host CPU time and memory are different resources. No FLMV time-space assumption or B3 same-calculus bridge is discharged.

## ITERATE: unchanged original-code replay

The **pinned original producer and checker mathematical function bodies** were evaluated in V8, replacing only Node file/console input/output adapters. The new standalone Node reproducer was published and JavaScript syntax-checked, **not independently executed as an OS Node subprocess**. Actual raw V8 cases and exact checker counts:

| Test | Original checker | After Pi |
| --- | --- | --- |
| Unmodified original seven-fixture packet | ACCEPT, 30,714 checks | ACCEPT, 30,714 checks |
| All 16 subsets of K4's four vertex AND3 aliases with negative signed high-bit tails | **8 ACCEPT** (even number), **8 REJECT** (odd number) | **16/16 ACCEPT**, 1,401 checks each |
| Other six even-V fixtures, every vertex AND3 alias assigned negative high-bit tail | 6/6 ACCEPT | 6/6 ACCEPT |
| K4 two paired positive ghost bits at position E+256 = 262 | ACCEPT, 1,401 checks | ACCEPT, 1,401 checks |
| K4 one negative alias with recomputed downstream XOR | REJECT: invalid sink -64 | ACCEPT, 1,401 checks, falsifying reverse implication |
| Published accepted SAT counterfeit, 48 original clauses, 47 paid nodes | ACCEPT, 3,273 checks; explicit 18-bit SAT witness verified | ACCEPT, 3,273 checks; **not** semantic soundness |
| Pi applied twice to all seven original fixtures | n/a | Identical to Pi applied once |

The seven original paid counts are 15,23,31,39,47,127,39. The charge/byte distinction holds for every transformed packet. This is not a demonstration of asymptotic SAT hardness or unrestricted proof cost.

**Reproducer:** experiments/arc/lspv1_561_signed_gf2_quotient.cjs, pinned original source blobs verified at execution, prints JSON and accepts an optional fresh replay-output path. **Actual raw evidence:** results/raw/arc/2026-11-10_1900_LSPV1_561_SIGNED_GF2_QUOTIENT_RAW.json. Published code was JavaScript-syntax-checked in the connected V8 host; OS-Node and repository-wide preflight were unavailable.

## Load-bearing node ledger, handoff and constraints

| Node | Status after this result | Required next |
| --- | --- | --- |
| P2-D1 | **OPEN**; verified only additional signed-mask accepted-byte/parsed representation equivalence on SOURCE/AND3/XOR | Recover and authenticate genuine original-source-bound full RES, AND3, GF(2), LOCAL-CONVERT, paid DEF and facets, fresh/private/exported wires, branching, weakening, contexts, discharge, joins and deletion |
| P2-C3 | **OPEN**; partial checked-prefix stepwise alpha/gamma test | Derive concrete/abstract **full native** transitions including entire shared DAG, paid history, provenance, complete assumption discharge, goal preservation and abstract charge <= concrete; replay every cheap CEGAR path in the full checker |
| P2-B1 | **OPEN** | A genuine superpolynomial minimum over every optimal whole shared DAG with every legal algebraic/ER/learning/branching shortcut; standard odd-Tseitin expander Resolution hardness is defeated by linear native GF(2) refutations |
| P2-B2/B3 | **OPEN**, separate | Prove noncircular same-R compact-refutation transfer from arbitrary hypothetical polynomial-time SAT decider; no such theorem here |
| P1-01, P1-03, P1-04 | **OPEN** | Uniform total exact all-input polynomial algorithm and complete machine accounting absent |

**LSPV-2 (Route A):** test Pi against its invalid UTF-8 and duplicate-JSON raw-byte aliases; a parsed quotient need not be a raw-byte equivalence. **LSPV-3 (Route B):** only after actual historical facet/RES syntax is recovered, test extension of Pi to those rules and discharged contexts. **LSPV-4 (Route A):** fully charge BigInt parser/normalizer, source binding, physical RAM and recomputation on a specified native machine. **LSPV-5 (Route B):** independently attack the universal accepted-packet direction with pathological BigInt coercions and SAT counterfeit variants; ensure no occurrence-ID quotient silently enters.

The complete root main.tex blob 45d57198b0d2ea8e0090085cb16e9d581c21e362 (1,927,748 characters) was recoverable via Git Blob but the Contents API returned empty; root main.tex is untouched, with no authorized full-math claim to reconcile. The full current root trackers were reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The repository Python preflight could not run in the connector-only workspace. All historical role identities, weights, five enabled states, schedules, ownership and two Route A/three Route B allocation were left unchanged. **P versus NP remains OPEN.**

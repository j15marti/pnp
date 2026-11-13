# LSPV-3/599: Original /341 deletion-witness object-container acceptance

**November 12, 2026, 16:28 PST | LSPV-3 Hypergraph & Proof Certificates | Historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One candidate and four falsifiers, stated before replay

Candidate [P2-D1-DELETED-CONTAINER]: For any /341 packet accepted by the unchanged archived SOURCE/AND3/XOR checker, replacing every fixture's array-valued **deleted** witness list with an ordinary JSON object having the same numeric length and the same entries at every numeric key preserves acceptance, exact signed sources, witness-to-source binding, paid nodes and proof DAG.

F1: the original checker insists on array identity or iteration for the deleted field. F2: the object changes the checked source or proof semantics. F3: missing index entries, incorrect source IDs or incorrect length remain accepted. F4: acceptance is only a property of a newly written checker. Source inspection and direct unchanged-body V8 replay refute F1/F2, ten negative controls refute F3, and the original mathematical body was not rewritten, answering F4 within the stated execution scope.

## Repository and literature reconciliation

Read root proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2.txt (blob f678f707880da4dfc97dabf778430c6dc816cb1f; read through GitHub fetch_blob after bounded fetch_file returned no text), issue #3 and latest comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, latest LSPV-3/598 handoff, original /341 and /386 checkers, LSPV-2/539 and /549, LSPV-3/549 and /550, LSPV-2/584, LSPV-5/505, GROKPROOF 2026-11-12 progress and Claude world-ledger README.

Source of authority: original /341 checker, experiments/arc/lspv2_341_independent_verify.js, blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**; original seven-fixture packet, results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json, blob **fe27fe1011d0021e721ccaeb747ed58da65d7464**.

This is distinct from LSPV-3/596's top-level summary shape, LSPV-3/550's signed literal coercions, LSPV-3/598's binary-tree rigidity, and LSPV-5/505's /386 CORE-versus-CLI array distinction. No priority or rule grammar from a separate typed reference is promoted to historical status.

Primary sources used as scope controls: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973. FRAT-XOR format (https://github.com/meelgroup/frat-xor/blob/main/format.md) is a distinct external proof grammar, not a reconstruction of R_mix341.

## Theorem 599.1 (native /341 checked-evidence object equivalence)

Let V be the unchanged archived /341 checker on JSON input bytes, and p an accepted parsed packet whose fixture-deletion lists are arrays. For each deleted array D of length m, replace D by an ordinary JSON object with property **length=m** and properties **"0":D[0], ..., "m-1":D[m-1]**. Leave every other field unchanged. Call the resulting serialized packet T(p). Then:

$$
V(p)=\mathrm{ACCEPT}\ \Longrightarrow\ V(T(p))=\mathrm{ACCEPT}.
$$

Furthermore, the returned original-checker assertion counter is identical and every signed SOURCE clause, deletion-witness identity, checked witness assignment, paid proof node, inference parent, truth table, affine row and terminal contradiction is unchanged.

**Proof from the unchanged source:** The only operations on the deleted field are a strict numeric comparison of deleted.length against clauses.length, indexing deleted[i] for i from 0 through length minus one, and accessing each indexed element's sourceId and assignment. It never calls Array.isArray, iterates deleted as an iterable, invokes an array method on deleted, or enumerates its extra properties. The replacement supplies precisely the same values at every read, so every conditional and assertion proceeds identically, including its exact returned check count. The property outside the numeric range may contain arbitrary unused metadata with no impact. QED.

This authenticates a **deletion-essentiality witness container**, not a native inference for deletion of proof nodes. It also does not make source bytes externally bound or restore checker soundness on the already reported accepted SAT-source packets.

## Computational replay and hostile evidence

The archived verifier mathematical body ran unchanged in hosted V8 with input/output adapters, using JSON serialization and reparsing of every tested packet. Original seven-fixture baseline accepted with 30,714 assertion groups. Replacing the deleted arrays in all seven fixtures with indexable objects also accepted with exactly 30,714 assertions. Seven separately re-encoded single-fixture packets all accepted, plus a K4 object with deliberately bogus extra unindexed metadata accepted.

| Original /341 test | Result |
|---|---|
| All seven converted fixtures in one packet | ACCEPT, 30,714 checks |
| Seven separately converted fixture packets | 7/7 ACCEPT |
| K4 with extra unused object property | ACCEPT |
| Missing first or last indexed witness | 2/2 REJECT |
| Incorrect source ID or swapped witness indices | 2/2 REJECT |
| Wrong numeric or string length | 2/2 REJECT |
| Null / absent indexed witness containers | 2/2 REJECT |
| Corrupted assignment length or scalar witness | 2/2 REJECT |

Positive cases: **9 packet executions, 15 distinct fixture executions, 78,118 original-checker assertion groups** excluding baseline. Negative controls: **10/10 rejected**. The original distinct fixtures contain SOURCE clause counts 16, 24, 32, 40, 48, 128 and 40, with corresponding paid-node counts 15, 23, 31, 39, 47, 127 and 39. The 321 paid nodes are distributed across seven separate certificates, not one shared 321-node refutation.

Verified evidence:
- Runnable, pinned archived-checker replayer: experiments/arc/lspv3_599_native341_deletion_object_domain.cjs, blob **119fc298093c1bf56a38964e500f76758f99e454**.
- Exact 16-source, 15-paid-node K4 JSON accepted-byte witness: results/raw/arc/2026-11-12_1628_LSPV3_599_NATIVE341_DELETION_OBJECT_ACCEPTED.json, blob **d34bf6d5450c3d524d2e8b30c3e850ca58a29274**.
- Complete 19-case hosted-V8 ledger: results/raw/arc/2026-11-12_1628_LSPV3_599_NATIVE341_DELETION_OBJECT_HOSTED_RAW.json, corrected blob **4e6202813cdc50452218c1f261d33c847cffab9f**.

The OS Node replayer was syntactically parsed but not executed as a separate OS subprocess in this run; no claim of independent OS replay is made. The hosted original mathematical body is the authority for the finite checks. Full repository preflight and LaTeX compilation were unavailable in this connector-only execution.

## Cost-sound restricted quotient, P2-C3 guard

For this *one identified acceptance fiber only*, define alpha to replace the deleted array or complete index-object with the canonical witness sequence D, retaining original SOURCE bytes/IDs, parent DAG, paid identities, fixed weights, assumptions, contexts and interfaces unchanged. Let gamma contain both encodings with exactly matching checked entries. The witness-checking transition commutes with alpha, its accepted goal is preserved, and logical work is unchanged. Raw evidence length, parsing cost, machine time, span and peak memory are separate quantities and must not be conflated with paid logical work.

An array-only MAY abstraction of all archived /341 accepted packets is false: the newly published K4 object witness is a genuine acceptance-path counterexample and must survive CEGAR. This does not imply that the complete historical R_mix341 accepts the object, and no other unauthenticated rule may be filtered out.

**P2-D1 OPEN**, except for this newly authenticated /341 evidence-field sublanguage. **P2-C3 OPEN** for the complete source-bound shared-DAG transformer. **P2-B1 OPEN** and **P2-B2/B3 separately OPEN**. P1-01/P1-03/P1-04 remain OPEN. **P versus NP remains OPEN**.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** All historical roles, identities, ownership boundaries, five Pacific schedules, two Route A / three Route B labels, fixed rule weights and charge semantics remain unchanged. A full mixed-rule original checker and a genuine source-bound RES-to-AND3 or DEF-facet-to-LOCAL-CONVERT inference remain the decisive next witness.

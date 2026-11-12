# LSPV-2/571: Original-/386 joint Resolution and paid-AND2 port symmetry

**2026-11-12, 02:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate, four falsifiers and precedence

**Candidate:** In the *unchanged archived /386 SOURCE/DEF/RES checker*, freely swap the two ordered input positions of any paid AND2 owner with distinct inputs, and independently swap the two parent positions and negate the pivot at any paid strict-Resolution record. Both operations preserve the complete accepted proof, including original signed source, every DEF facet, paid work and shared DAG. Their independent choices yield a free presentation orbit of size at least \(2^{R+T}\), where \(R\) is the number of RES records and \(T\) counts paid owners with unequal ordered input literals.

F1: changing a paid gate's ordered operands causes a formerly valid defining facet to be rejected. F2: paired RES parent/pivot changes interact with a gate swap and cause rejection. F3: changing one pivot/parent alone or changing an owner operand without swapping both is accepted. F4: two distinct flip masks serialize identically, or a legal flip changes the native logical charge. All are contradicted by original-code analysis and the finite subprocess corpus. Distinguish a general source-code theorem from the finite tests and never extrapolate to the missing mixed calculus.

**Precedence:** LSPV-2/564 and LSPV-3/564 already established the restricted signed-RES orientation involution. LSPV-2/563 constructed the terminal-live nested paid copy DAG. LSPV-2/570 established a limited source-bound CEGAR filter, and LSPV-3/584 established an exact-cost owner-bank fiber. The incremental result here is the *independent second AND2 input-port involution*, its exact product with the preexisting RES involutions, and an executed combined native-OS corpus with every inserted gate facet in the terminal ancestry. This does **not** discover an entirely new form of general proof normalization.

## Theorem 571.1: restricted, original-code exact joint port orbit

Fix one certificate \(P\) accepted by the original complete command-line implementation
\`experiments/arc/lspv2_386_independent_verify.js\` (Git blob
\`338305c0ce101704205e57543756b8127074a986\`).
Let \(R\) be its number of strict RES records and let \(T\) be the number of globally paid \`gate_defs\` declarations \`[id,z,a,b]\` with \(a\ne b\).
Every independent selection of the following actions preserves acceptance and paid logical work:

1. On a chosen RES record with \`parents:[i,j]\` and \`pivot:p\`, replace only those fields by \`parents:[j,i]\` and \`pivot:-p\`.
2. On a chosen nondegenerate AND2 owner \`[id,z,a,b]\`, replace only its two signed inputs by \`[id,z,b,a]\`.

All SOURCE records, derived signed conclusions, DEF facets, owner IDs, proof-node indices, dependency sets, freshness and summary counters are unchanged. Thus the actions commute and induce at least
\[
\boxed{2^{R+T}}
\]
pairwise byte-distinct accepted JSON presentations of the **same** chronological proof, with the same checker-paid \(W\), critical dependency span, and global paid-owner identities. Certificate bit length need not remain the same because printing a negative pivot may use one extra character.

**Proof from the original source.** The checker constructs the AND2 owner facet set from
\[
(-z\lor a),\qquad(-z\lor b),\qquad(z\lor\neg a\lor\neg b).
\]
It canonicalizes each signed clause and stores its defining-facet keys in a set; switching \(a,b\) leaves that set exactly invariant, as well as all gate-freshness tests, dependencies and owner payment. The strict RES rule checks that the first parent contains \(p\), the second contains \(-p\), and that its claimed canonical resolvent is the union after deleting those two pivots. Simultaneously exchanging parents and \(p\mapsto-p\) preserves every check and the exact derived resolvent. Both transformations change only disjoint input fields; therefore they commute. For a RES, the two parent indices are distinct by native acceptance and the oriented pair changes; for a nondegenerate gate \(a\ne b\), its two printed ordered inputs change. Hence distinct action subsets yield distinct serialized JSON documents. The main checker self-tests remain unchanged because the mathematical proof, gate-owner bank cardinality, first/last records and the summary are unchanged. No extra paid identity is created. This proves the stated original-code theorem, not a theorem about an unauthenticated R_mix341 dispatcher. \(\square\)

An input-order normalizer choosing a fixed order for each gate's two signed inputs and a consistent RES signed-port orientation is idempotent and paid-work preserving **within this archived checker**, but not necessarily byte-count preserving and not a complete grammar normalizer.

## Executed original operating-system replayer

The exact newly committed executable \`experiments/arc/lspv2_571_native386_joint_port_orbit.cjs\`, Git blob **\`1d1a1bc5c7534a658f63ad73e1847d077059894a\`**, ran end to end in actual independent Node.js OS subprocesses invoking the **unchanged original checker**. It pins the original W29 seed blob \`318c52d99977ea4e91bc8554051138a700c1dc94\` and constructs terminal-live W31 and W37 copies. The original source and ALL defining facets remain literal-identical under each orbit transformation. Both positive families inherit the same signed 17-clause guarded K4 source.

| Live proof | Paid RES \(R\) | Paid owners | Nondegenerate owners \(T\) | Paid \(W\) | Guaranteed accepted orbit |
|:--|--:|--:|--:|--:|--:|
| k=0, terminal-live gate | 30 | 1 | 1 | 31 | \(2^{31}=2,147,483,648\) |
| k=2, two nested copy gates | 34 | 3 | 1 | 37 | \(2^{35}=34,359,738,368\) |

The 24 selected positives cover for each \(k\): both gate input orders times six orientation masks (none, first, last, all, alternating, every-third). **24/24 original-CLI ACCEPT**; every one passed 11 built-in negative corruption controls; combined assertion groups **87,636** and internal negative tests **264**. Nine hostile packets were rejected: changing rather than swapping one gate input; pivot-only flip; parent-only flip; SOURCE forgery; SOURCE count underreporting; cost underpayment; duplicate paid owner; forward parent; and unsupported LOCAL-CONVERT tag. **33/33 observed native results matched predetermined polarity.**

The k=2, gate-swapped/all-RES-flipped accepted JSON packet is **3,578 UTF-8 bytes**, SHA-256 \`8dca238025ec6a287807e32a3d1896aac2f387e8b87c33a8ed4e85295549447f\`, Git blob \`ae515a483bf7ec5a32232266adb17ef664ba7e9a\`. The same k=2 proof with its natural ports is 3,554 bytes. These byte counts are evidence lengths, **not** logical-work differences. Node subprocess elapsed time and the certificate's physical footprint are measured or represented separately from paid \(W\), construction time, critical span and peak live space. The finite corpus does not test billions of variants; that orbit size follows from the exact independent involution proof.

## Artifacts and source provenance

- Executable exact original-OS replayer: \`experiments/arc/lspv2_571_native386_joint_port_orbit.cjs\` (blob \`1d1a1bc5c7534a658f63ad73e1847d077059894a\`).
- Immutable compact actual OS manifest with all 33 certificate SHA-256s, verdicts, original accepted assertion groups, and rejection messages: \`results/raw/arc/2026-11-12_0212_LSPV2_571_ORIGINAL_OS_JOINT_PORT_COMPACT.json\` (blob \`f1c223a2cd90a557504c93a3682e5bd9b2f4838f\`).
- The exact 3,578-byte accepted witness: \`results/raw/arc/2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json\` (blob \`ae515a483bf7ec5a32232266adb17ef664ba7e9a\`).
- Complete per-case OS timing/error/raw ledger generated by the script: \`results/raw/arc/2026-11-12_0212_LSPV2_571_ORIGINAL_OS_JOINT_PORT_RAW.json\`. It is part of the user-visible supplementary local evidence archive, not committed separately; the compact manifest is the archived immutable GitHub data.
- Current five-role handoff: \`research/coordination/2026-11-12_0212_LSPV2_NATIVE386_JOINT_PORT_FIVE_ROLE_HANDOFF571.md\`.

## Research, limitations, exact affected nodes

Read current \`proof1.txt\` (blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`), \`proof2.txt\` (blob \`1bf4929f872506fcbc357810bd72d016694618b2\`), GitHub issue #3, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, latest LSPV-2/570 and peer /583-/584 handoffs, historical /341 and /386 programs, and prior /539-/549, /563-/570 research artifacts. This exact-scoped port transformation is consistent with source-bound and count-once cost requirements. It retains owner identities, contexts and assumptions (none are active in this subset), and the shared proof DAG.

Primary literature reviewed as methodological context: Cook and Reckhow, *J. Symbolic Logic* **44** (1979), 36–50, DOI [10.2307/2273702](https://doi.org/10.2307/2273702); Cousot and Cousot, *POPL* (1977), 238–252, DOI [10.1145/512950.512973](https://doi.org/10.1145/512950.512973); Clarke et al., *CAV* (2000), 154–169, DOI [10.1007/10722167_15](https://doi.org/10.1007/10722167_15); and the **distinct** [FRAT-XOR external proof format](https://github.com/meelgroup/frat-xor/blob/main/format.md). They do **not** authenticate historical R_mix341 grammar.

**Proof status:** The theorem is **PROVED/RESTRICTED** for the exact /386 code; finite subprocess evidence is **COMPUTATIONAL**, peer review pending. The archived /386 checker is not the original unified R_mix341 checker. No native RES-to-AND3, GF(2), DEF-to-LOCAL-CONVERT, private/exported wires, branching, contexts/discharge, weakening, joins or deletions have been authenticated by this run. All remain **MAY** in a cost-sound full-calculus abstraction; they must never be silently removed. Both live examples are **upper-bound proof witnesses**, not minimum lower bounds; the known W29 genuine alternative remains available by free optimal proof choice. This result neither establishes a cost-sound full-calculus abstraction nor tests B1/B2/B3. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain **OPEN**, as do P1-01/03/04.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No proof-chain node status or historical rule weight changed. Existing five identities, titles, historical Route A/B assignment (TWO A, THREE B), ownership and Pacific schedules are preserved; no automation was created, renamed, rescheduled or disabled. Root \`main.tex\` may be changed only in the marked LSPV-2 section after full-content readback and conflict-safe update.

**Next decisive target:** locate the actual original **single** historical source-authenticated rule dispatcher that accepts a genuine RES-to-AND3 or paid DEF-to-LOCAL-CONVERT premise and execute accepted-byte plus corrupted-port tests. P versus NP remains **OPEN**.

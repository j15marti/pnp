# LSPV-4/540: Native /386 paid-owner incidence defeats record-only shared-cone accounting

**2026-11-11 03:36 PST | PNP Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One candidate theorem and four falsifiers

**Candidate resource theorem.** In the **unchanged original archived /386 SOURCE/paid DEF owner/free DEF facet/strict RES checker**, if \(A,B\) are backward-closed sets of chronological proof records, then the cost of using both sets is obtained by deduplicating **paid Resolution record identities AND globally paid gate-owner identities**, not merely intersecting their record sets. Let \(\mathcal R(C)\) denote RES records in \(C\) and \(\mathcal O(C)\) denote owners of DEF facet records in \(C\), and define the induced cost

$$
W(C)=|\mathcal R(C)|+|\mathcal O(C)|.
$$

Then for all record subsets \(A,B\) (in particular backward-closed cones),

$$
\boxed{W(A\cup B)=W(A)+W(B)-|\mathcal R(A)\cap\mathcal R(B)|-|\mathcal O(A)\cap\mathcal O(B)|.}
$$

In general, **\(\mathcal O(A\cap B)\ne\mathcal O(A)\cap\mathcal O(B)\)**. A different zero-paid defining facet of the *same* globally paid owner may occur in each disjoint record cone. Consequently, using \(W(A\cap B)\) as the subtraction can be **unsound as a cost-sound abstraction**: the inferred abstract work exceeds a realized accepted concrete work.

**Precommitted falsifiers:** (F1) no original-checker-accepted packet has disjoint proof-record cones with the same paid owner; (F2) adding the two real facets and two real Resolution deductions corrupts original signed SOURCE, fixed charges or the unmodified complete original CLI; (F3) paid-RES reconvergence cannot be counted once at the native terminal; (F4) the original checker charges only deductions reachable from the terminal, so unused paid owners or RES records can be silently dropped from a packet's reported cost. The first three are refuted by accepted witnesses; F4 is refuted in the opposite direction by a positive witness with paid but terminal-unreachable records. No universal mixed-calculus lower bound is asserted.

## Recovered authoritative scope and exact fixed charges

Pinned unchanged original checker: [experiments/arc/lspv2_386_independent_verify.js](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv2_386_independent_verify.js), Git blob **338305c0ce101704205e57543756b8127074a986**. Its code explicitly requires 17 original signed guarded SOURCE records for K4, verifies sorted clauses and exact binary Resolution pivots, and charges

$$
W_{\!/\!386}=N_{\mathrm{RES}}+N_{\mathrm{gate\_defs}}.
$$

Native /386 operation ledger, without inventing any missing historical rule:

| Authenticated item | Logical charge in /386 | Physical/verification work not included in \(W\) |
|---|---:|---|
| SOURCE from original signed input | 0 | Serialized clause, source provenance, signed-clause comparison, source ledger, retained references |
| Declared conservative gate DEF owner | 1 once per distinct declaration | Four-number tuple and output/input validation, namespace lookup, gate-order and edge legality |
| A true defining DEF facet of declared owner | 0 additional | Literal-array bytes, canonical comparison, records and subsequent retrieval |
| Strict binary RES deduction | 1 per record | Two indexed parent references, pivot lookup, literal filtering, canonical sorting, application check and storage |
| Full-checker negative controls | not proof work | Eleven hostile replays, which are executable-test overhead and not the historical logical charge |
| AND3, GF(2), LOCAL-CONVERT, branch/split, weakening, discharge, join, deletion, exported/private wires | **not authenticated together in /386** | Their missing byte grammar, physical operations, weights, source/goal interfaces remain OPEN for actual historical \(R_{\mathrm{mix341}}\) |

A globally declared owner may be paid even if no defining facet or RES descendant is in the final contradiction's ancestry. This behavior is distinct from the cost of the **minimum** legal proof for that source.

## New original-checker-accepted disjoint-record/overlapping-owner witness

Start from LSPV-1/568's original signed K4 source-bound packet (Git blob **e3eb2a46857776089ab83f4ad50159ef622d2869**), accepted by the complete original CLI: 17 SOURCE, 28 paid RES, one globally paid but unused gate owner \([0,8,1,4]\), \(W=29\). Keep its original signed source, edges, charge, guard, 28-RES proof and final contradiction unchanged.

Insert before the final contradiction:

1. Record 44: a **real free DEF facet** of owner 0, clause \([1,-8]\).
2. Record 45: a **real paid RES** of record 44 with original signed SOURCE record 1 on pivot \(+1\), yielding \([-2,3,-7,-8]\).
3. Record 46: a second **real free DEF facet** of the *same* owner 0, clause \([4,-8]\).
4. Record 47: a second **real paid RES** of record 46 with original signed SOURCE record 5 on pivot \(+4\), yielding \([1,5,-7,-8]\).
5. Preserve the original final RES as record 48 with unchanged parent references. Update only the actual record-kind counters and total \(W\).

The resulting **49-record, 3,080-byte** ASCII JSON packet, [accepted witness](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json), Git blob **25b5c1f95734f6eae36bdbb4a17c948c00753cff**, has **17 SOURCE, two free facets, 30 paid RES and one paid gate owner, \(W=31\)**. Both original source parity checks remain 0 satisfying assignments for odd K4 and 8 for even control among 64 edge assignments.

Let \(A\) be the entire backward cone ending at RES45 and \(B\) end at RES47. They contain **no common proof record**:

$$
A\cap B=\varnothing,\quad
W(A)=2,\quad W(B)=2,\quad W(A\cap B)=0.
$$

But both contain different facets of globally paid owner 0. Hence

$$
\mathcal O(A)=\mathcal O(B)=\{0\},
\qquad
W(A\cup B)=1+1+1=\boxed{3},
$$

not the **4** produced by record-intersection-only cost addition. This is a concrete accepted, exact **one-unit overcharge** for a plausible abstract resource transformer. It is not a native historical branch/discharge operation: these are two independently reachable proof **record cones**, and the accepted certificate has one final contradiction.

The **unchanged full original /386 CLI body** executed in hosted V8, with only fs/crypto/structuredClone I/O adapters. It accepted the packet, passed all eleven built-in hostile controls, reported **3,750 assertion groups**, and correctly returned \(W=31\). Five further targeted invalid gate/facet/pivot/reference/counter variants were rejected by the original core. The published Node standalone audit was syntax-checked; OS Node end-to-end execution was **not** independently performed in this environment.

## Second independent original-checker control: paid RES sharing across the terminal

The original archived /386 69-record K4 certificate ([pinned exact original](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_0336_LSPV4_540_SHARED_K4_ORIGINAL_COPY.json), original Git blob **d0fa96a155672f8f6a6a3428eacafa15e79b9e88**) has 17 SOURCE, three zero-added-cost DEF facets, 49 paid RES, one globally paid gate owner, **\(W=50\)** and 4,144 bytes.

The terminal RES has record parents 67 and 66. Their full backward cones each contain **29 paid RES plus owner 0**, cost 30 each. Their intersection has **21 common record occurrences, including 10 paid RES**, and the same globally paid owner 0, cost 11. The final RES costs one:

$$
\boxed{W=30+30-11+1=50}.
$$

Naively adding the two individual cone costs and the terminal costs **61**, overcharging by **11**, although all computations are genuinely shared in the accepted certificate. The same original full CLI passed its eleven negative controls, reporting **4,492 assertion groups**.

**Global-vs-sink charge identity.** For any /386 accepted packet \(P\), let \(S\) be the final contradiction's backward record cone and let \(\mathcal G\) be all paid gate owners declared globally. Then

$$
W(P)=W(S)+|\mathcal R(P)\setminus\mathcal R(S)|+|\mathcal G\setminus\mathcal O(S)|.
$$

On the new \(W=31\) witness, the final contradiction's backward cone costs only 28 RES and zero paid gate owners, with **two terminal-unreachable RES and one terminal-unreachable globally paid owner** supplying the remaining three units. A sink-only ledger is therefore not equal to the actual historical packet charge, even though its value may be a valid *lower* abstract cost.

## Exact resource audit and the realizability firewall

| Resource | Owner-overlap witness | Native shared-terminal witness |
|---|---:|---:|
| Serialized packet bytes, including trailing newline if present | 3,080 | 4,144 |
| Total native records | 49 | 69 |
| SOURCE, DEF facet, RES | 17, 2, 30 | 17, 3, 49 |
| Globally paid gate owners | 1 | 1 |
| Distinct paid logical work \(W\) | 31 | 50 |
| Resolution parent references | 60 | 98 |
| Longest terminal unit-RES dependency span | 7 | 9 |
| Total serialized clause-literal occurrences | 190 | 226 |
| Largest concrete clause width | 5 | 4 |
| Constructive chronological/no-recompute fresh-result paid-value peak | 9 slots | 18 slots |
| Actual indexed-machine sequential time, physical RAM peak or bit-space minimum | **not measured** | **not measured** |

The last paid-slot measurement is **only** a particular schedule upper bound in a specified slot abstraction: source clauses and zero-paid facets are externally readable, each RES materializes a fresh result, dead paid results are evicted at last use, and no recomputation is performed. It is **not** a lower bound on minimal actual memory, not a proxy for native JS heap usage, and not a substitute for source/packet reading, identifier length, canonicalization, temporary buffers, retention of contexts, sparse versus dense affine rows, retrieval, or recomputation charges. The full checker has host arrays, hashes, maps and repeated assertions.

Resource firewall for [P2-C3]: an abstract state may freely forget or merge an owner at lower cost only if **every** concrete native transition remains represented and the resulting abstract path charge is **no larger** than the actual concrete charge. A cost partition that taxes distinct DEF facets as distinct paid owners fails this condition. The correction is owner-identity incidence, plus independent RES dedup and a separate physical evidence ledger. Globally paid but terminal-unused owners demonstrate that **counting fewer** paid objects can be cost-sound as a lower abstraction yet not faithfully reflect historical certificate checking. This proof does not imply an all-rule nonreachability invariant.

## Literature and corpus comparison

This is a **specific native-checker witness** for a general DAG-sharing principle, not the first mathematical discovery of sharing nonadditivity. LSPV-1/468 already identified arbitrarily large overestimates in a **different abstract** AND/OR graph; LSPV-4/535–539 proved restricted owner/facet and normalization results in archived /386. New here is the **same-checker accepted certificate in which paid owner identity overlaps while proof-record identities do not**, plus a second independent accepted checker control exhibiting 11 units of terminal paid-cone reconvergence overcharge. It must not be recast as a new historical split, XOR or LOCAL-CONVERT rule.

Cook–Reckhow's proof-system framework [1] requires specifying the verifier and proof representation. Nordström–Håstad [2] and Nordström's pebbling survey [3] distinguish resolution length from proof space and motivate separating DAG work and execution scheduling. These works do **not** establish the new checker-specific numerical fixtures.

[1] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. *J Symb Log.* 1979;44:36–50. DOI 10.2307/2273702. https://doi.org/10.2307/2273702

[2] Nordström J, Håstad J. Towards an Optimal Separation of Space and Length in Resolution. *Theory of Computing*. 2013;9:471–557. https://theoryofcomputing.org/articles/v009a014/

[3] Nordström J. Pebble Games, Proof Complexity, and Time-Space Trade-offs. *Logical Methods in Computer Science*. 2013;9(3). https://lmcs.episciences.org/1111

## Artifacts, preflight and proof-status disposition

Executable: [experiments/arc/lspv4_540_native_paid_owner_cone_audit.cjs](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_540_native_paid_owner_cone_audit.cjs), Git blob **a90ba4feaca99ceade8c2f2886dc4e59884d1e8a**. Both accepted raw packets linked above. Exact numeric ledgers, hostile controls and methodological qualifications: [results/raw/arc/2026-11-11_0336_LSPV4_540_NATIVE_PAID_CONE_RESOURCE_RAW.json](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_0336_LSPV4_540_NATIVE_PAID_CONE_RESOURCE_RAW.json), blob **d450539b0fc59b02010b864cdadd6ab5f6e290b1**. Five-role coordination handoff accompanies this report.

Read **both complete root proof trackers**, issue #3 and its current comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, current /539 handoff, original /386 source, /568 and /539 peer evidence, and materially relevant 539–549 and later work reflected in root tracker/issue. The two root trackers had respective current Git blobs **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** and **e7cb9e738ea31173766c553b2a5541e71df0c503** at preflight. No repo preflight Python subprocess, OS Node end-to-end run or native machine bit-space measurement is claimed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt or proof2.txt. No changes to main.tex, agent identities, schedules, labels, historical rules/weights or ownership regions. An original accepted fragment is not authentication of the unavailable full \(R_{\mathrm{mix341}}\) byte grammar.

**[P2-D1] OPEN.** A single historical checker connecting RES/DEF to AND3, GF(2), LOCAL-CONVERT, branches, discharge and joins remains missing.

**[P2-C3] OPEN.** This is a restricted exact owner-aware cost ledger and an accepted overcharge falsifier, not a universal all-rule abstraction with a general lower bound.

**[P2-B1] OPEN.** No superpolynomial minimum-work lower bound across all legal historical refutations is known. Separate **[P2-B2/B3] OPEN**. **P versus NP remains OPEN.**

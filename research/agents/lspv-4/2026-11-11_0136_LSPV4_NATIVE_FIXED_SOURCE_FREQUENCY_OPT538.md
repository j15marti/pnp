# LSPV-4/538: Frequency-optimal native /386 gate-wire serialization, with a same-source dense-ordinal counterexample

**2026-11-11 01:36 PST | PNP Time-Space Resource Auditor | historical Route A | PROVED/RESTRICTED plus COMPUTATIONAL | P versus NP OPEN**

## Candidate theorem and precommitted falsifiers

**Candidate:** For every accepted parsed certificate in the exact pinned archived /386 SOURCE/paid-DEF-owner/free-facet/strict-Resolution checker, with original SOURCE clauses, original guard, graph and charge FIXED, and with the paid gate definitions and record dependencies FIXED, optimize the JSON decimal byte length of all **gate-output wire magnitudes** by an injective safe-integer relabelling. The exact optimum among these relabellings is determined solely by weighted occurrence frequency and decimal token lengths. Every relabelled proof must remain legal and retain exactly its original distinct paid work. This sharpens LSPV-4/537's dense **maximum-ID** bound, without claiming that /537 was already byte-optimal.

F1: legal source-bound gate wire relabelling changes a SOURCE clause or a paid owner and is rejected. F2: first-fit definition-ordinal dense IDs are universally minimum-byte. F3: zero-additional-paid defining facets must each be charged again or deduplicated before legality is preserved. F4: a collapsed output wire, incorrect owner, forged original SOURCE, underpayment or invalid RES pivot survives original checker replay. Outcome: F1/F3/F4 failed in the tested domain; F2 is **FALSIFIED** by a concrete accepted 115-byte saving on a fixed 55-paid shared proof DAG.

## Exact archived authority and relation to peer corpus

Original archived checker body: \`experiments/arc/lspv2_386_independent_verify.js\`, Git blob \`338305c0ce101704205e57543756b8127074a986\`.
Original signed two-owner guarded K4 packet: \`results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json\`, blob \`08aa169b5db49b2ddd1cb5a9b6890fcc3b790916\`.
The checker explicitly validates a set of globally fresh, positive, safe-integer output wires, each distinct from original edges and the fixed guard, with earlier-defined gate inputs permitted. Its numeric **order** is never a prerequisite for wire legality; the owner ID is a separate, globally unique paid identity. RES parents reference prior *record positions*, not output-wire numbers; true DEF facets are uncharged clause views.

The original /341 checker, by contrast, recognizes SOURCE/AND3/XOR only and is neither a /386 resolver nor the unavailable complete historical R_mix341 dispatcher. LSPV-2/539-549 documented the critical /341 source, JSON duplicate-key, nonfinite-ID, invalid UTF-8, BOM, and polyglot noncomposition hazards. LSPV-2/552 authenticated both archived dispatchers but not a joint rule. LSPV-3/544, /561, /563, /564 and LSPV-4/535-537 supplied owner-aware proof-DAG controls, a signed native packet, orientation symmetry and dense gate-wire relabelling. LSPV-1/544's shared-obligation LP dual is a different bound. LSPV-5/482 supplies prototype-name transport falsifiers in the disjoint /341 checker. This run adds an **exact weighted-byte optimum** and an **accepted fixed-SOURCE counterexample** to interpreting dense numerical order as physical byte optimality.

Read both complete root trackers, issue #3 and recent coordination comments, AGENTS.md, CODEX.md and the pnp-research skill, current /536 handoff, peers /539-549 and later, and the pinned original /386 verification body and real accepted packet. Attempts to read root main.tex via fetch_file yielded an empty content field; direct Git blob fetch recovered the complete current manuscript for inspection. Root tracker statuses remain OPEN.

## 538.1 Fixed-SOURCE optimal wire assignment theorem (PROVED/RESTRICTED)

Fix an accepted **parsed** /386 proof packet P with E original edge-variable indices, guard G, g paid gate definitions in their given chronological declaration order, and distinct output wires z_1,...,z_g. Fix all fields except those recognised as output-wire literals in gate definitions, DEF/RES record clauses and RES pivots. Original SOURCE records, graph, charges, guard, source occurrence identifiers, record ordering, parent indices, owner IDs, summaries and extraneous ignored metadata remain **unchanged**.

Restrict relabellings to injections from the g gate-output wires into the positive safe integers greater than E and different from G, with sign-preserving substitution and original-checker canonical resorting of each affected clause. Suppose at least g eligible labels exist. For each wire z_i let f_i be the number of decimal numeric occurrences of its magnitude over all affected semantically recognised numeric fields, counting each gate definition's output and signed input ports, each record clause and each RES pivot exactly once per occurrence. Let the g shortest eligible decimal token lengths be

$$
\ell_1\le \ell_2\le\cdots\le\ell_g,
$$

and let frequencies be sorted

$$
f_{(1)}\ge f_{(2)}\ge\cdots\ge f_{(g)}.
$$

Then for this **fixed proof and fixed original SOURCE**, the minimum canonical JSON serialization size among those accepted gate-wire relabellings is exactly

$$
\boxed{B_{\mathrm{wire\ optimum}}(P)
  =B(P)-\sum_{i=1}^g f_i\,\operatorname{digits}_{10}(z_i)
       +\sum_{i=1}^g f_{(i)}\ell_i.}
$$

All accepted relabellings in this orbit preserve

$$
\boxed{W=N_{\mathrm{RES}}+g, \qquad
R=2N_{\mathrm{RES}}, \qquad
\text{the entire owner-qualified shared proof DAG}.}
$$

The theorem is about JSON.stringify of parsed packets (ordinary numeric tokens) and does **not** equate different historical raw JSON byte streams or supply an all-rule abstract interpreter.

**Proof, legal renaming.** A mapping injective on positive gate output magnitudes and disjoint from the fixed original edges and guard preserves original-source membership **exactly**, because SOURCE clauses and guard are not modified. It preserves all signed Boolean gate-definition clauses under a sign-equivariant variable permutation, the gate-input dependency order, and distinct paid gate-owner IDs. RES complementary pivot tests and exact resolvents commute with the same permutation, after canonical re-sort by the checker's key comparator. DEF facet clause sets similarly commute. Induction over the chronological record array preserves each accepted record, source provenance, all parents, each derived clause and the final empty clause. The gate_defs array stays in the same order, and every charge and summary count is unchanged. The original archived checker does not compare relative magnitudes of distinct fresh gate wires; its inequalities are against the fixed E and G. Hence the modified packet is accepted by the same checkProof core. QED for legality.

**Proof, exact bytes.** In canonical JSON.stringify integer serialization, each recognised wire occurrence contributes its unsigned decimal digit count plus a sign character precisely when originally negative; signs are preserved. Commas, brackets, field names, unchanged values and punctuation are independent of the relabelling. Reordering literals inside an affected clause does not change their aggregate byte contribution. Therefore the full byte count is constant plus \(\sum_i f_i \operatorname{digits}_{10}(\pi(z_i))\). Among eligible safe integers, a set with a longer-digit selected label but an unused shorter-digit label can be exchanged without increasing bytes. Among selected labels, exchanging frequencies f_i>f_j assigned respective lengths d_i>d_j decreases bytes by \((f_i-f_j)(d_i-d_j)\). Repeated exchanges attain the displayed sorted-frequency/shortest-length minimum. QED.

**Scope firewall.** Source identity is exact only because G and all SOURCE records are held fixed. Earlier /537 also allowed changing the guard while preserving the original *underlying graph/edge variable meaning*, but that changes in-band guarded SOURCE byte strings. The present claim deliberately does NOT identify these two source commitments. Owner-ID renaming, raw duplicate keys, nonfinite numeric JSON, ignored-field renormalization, arbitrary variable elimination, proof-DAG shortening and historical unknown rules are outside this theorem.

## 538.2 Original checker experiment: 24 x 5 accepted same-source packets

Begin with the pinned 74-record original guarded odd-K4 proof containing 17 SOURCE records, six free DEF facets, 51 paid RES and two paid gate owners. Add two **paid but unused** conservative gate definitions [2,10,1,2] and [3,11,1,3] without changing any proof record. For each k in {0,1,16,64,120}, add k redundant true facets for the fourth gate immediately before the final empty RES record, updating only the correctly computed summaries. Each facet has zero **additional** paid charge; the 51 RES steps still have exactly 102 premise references. All variants have four once-paid gate owners and W=55.

For each k, exhaustively try all 4!=24 injective assignments of original gate-wire identities (8,9,10,11) to eligible labels (8,9,10,11), keeping guard 7 and each of the 17 original SOURCE records byte-for-byte intact after JSON.stringify. Execute the **unchanged original /386 checkProof body** in hosted V8 with its full semantic control enabled.

| Extra free facets k | Paid W | Total records | Dense-order bytes | Exact min bytes | Saved |
|---:|---:|---:|---:|---:|---:|
| 0 | 55 | 74 | 4,443 | 4,443 | 0 |
| 1 | 55 | 75 | 4,492 | 4,492 | 0 |
| 16 | 55 | 90 | 5,228 | 5,217 | 11 |
| 64 | 55 | 138 | 7,581 | 7,522 | 59 |
| 120 | 55 | 194 | 10,326 | **10,211** | **115** |

Every one of the **120** distinct transformed packets passed the original native mathematical checker, without any patch to its rule validation. The cumulative run executed 138,828 original checker assertion groups. Five corrupted packet controls were rejected: duplicate output-wire name, wrong gate facet, underpaid owner, altered SOURCE clause and false terminal pivot. The exact minimum agreed with the exchange formula in every k row. This is exhaustive **within a four-wire relabelling orbit**, not an enumeration of all possible proofs.

At k=120 the gate-wire occurrence frequencies are (11,6,1,121). Definition-ordinal labels (8,9,10,11) place 121 occurrences at a two-digit wire. An accepted optimum uses (8,10,11,9): the 121-occurrence wire receives one digit and the once-used wire receives two. The accepted k=120 optimum reduces 10,326 to 10,211 bytes, with W=55, R=102, exactly the same source records, paid owners, and final refutation. Four assignments tie for the optimum because 10 and 11 have equal digit lengths.

**Executable and raw evidence:**
- Source: \`experiments/arc/lspv4_538_native_frequency_wire_audit.cjs\`, which SHA-pins the original checker/seed, independently reconstructs all 120 packets, invokes the complete unchanged original /386 CLI in separate real Node subprocesses, and asserts the original 11 built-in corruption controls on each accepted packet. The script parsed successfully in hosted V8 but its OS-Node path has **not** been executed in this run.
- Observed raw V8 ledger: \`results/raw/arc/2026-11-11_0136_LSPV4_538_NATIVE_WIRE_FREQUENCY_OPT_V8_RAW.json\`. This is original-checkProof mathematical acceptance, NOT a claim of native OS CLI execution. No indexed-machine physical time or peak-RSS measurement was conducted.

## Resource ledger and consequences for P2-C3

| Resource | Exact value or control for this experiment | Interpretation |
|---|---|---|
| Fixed original source | Guarded odd K4, 17 identical SOURCE records in every relabelled packet | No source rewriting or external-source substitution |
| Distinct paid inference nodes | 51 RES + 4 gate owners = 55 | Each owner charged once, including two intentionally dead ones |
| Zero-additional-paid views | 6+k DEF facet records | Original checker checks bytes and clause validity, but no new logical payment |
| Premise/reference applications | 102 RES parent-index references, constant with k | Referring to a paid result does NOT create another paid result |
| Sequential verification | Original checker scans parsed records and checks RES/facet predicates; input reading necessarily depends on serialized size | Actual CPU cycles and full-CLI wall time not measured in V8 |
| Critical dependency span | Inference dependency edges are unchanged under any accepted gate-wire relabelling | Byte shortening does not prove a shorter proof DAG or faster discovery |
| Live retention | The archived implementation constructs its known[] array of record clauses; k redundant views raise implementation storage despite unchanged paid work | This implementation is not an optimal proof-space theorem |
| Retrieval/recomputation | Same parent positions and valid shared uses; no recomputation in the observed verifier | Recompute schedules or in-place streaming are separate realizations |
| Peak writable space | No native machine-space measurement; source/packet buffers, parsed objects, references, arrays and output must all be charged | Cannot identify minimum physical memory from W |
| Certificate bytes | 10,326 -> 10,211 at k=120 | Exact optimum only in fixed-source wire-relabelling orbit |
| Ideal proof minimum | Not measured; the constructed extra gates/facets are deliberately redundant | W=55 is an upper-bound witness, not a lower-bound certification |

A lower-bound-safe abstract interpreter must contain *every* accepted relabelling of a concrete proof and never assign higher **logical** cost. An abstraction that interprets first-fit dense numerical identifiers as the *unique byte-minimal representation* is false, even on an accepted same-source /386 trace. Correct canonical byte minimization is frequency-sensitive. It does not justify treating byte minimization as free online time, nor does it imply an ideal SAT-decider resource bound.

The theorem is a **direct rule-source transfer** for the archived /386 parser only. General abstract interpretation is methodological background (Cousot & Cousot, POPL 1977, DOI 10.1145/512950.512973); Cook & Reckhow (JSL 1979, DOI 10.2307/2273702) distinguish proof systems and proof length; Nordström & Håstad (Theory of Computing 2013, DOI 10.4086/toc.2013.v009a014) study Resolution length/space in a different proof model. None transfers this finite serialization optimum into a historical all-rule lower bound. A knapsack/LP cost-partition dual for shared proof nodes is only an **analogy** here until every native action, zero-cost facet, branch and goal obligation is authenticated. Assuming a paid checker event for every repeated facet would be a **failed transfer**.

## Reconciliation, blockers and next action

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (preflight blob 8927e4ba0c54ba701ceac55e918203fcdf675e1a) were read completely and not amended. This scoped counterexample narrows a representation assumption; it does not close [P2-D1], [P2-C3], [P2-B1], or separate [P2-B2/B3]. P1-01/P1-03/P1-04 remain OPEN.

The only operational acceptance authority for this result is the **archived /386** checker. Its complete CLI has separate known self-test artifacts (LSPV-4/535, LSPV-1/567); the new standalone runner is designed to execute that CLI but did not do so in the present V8 run. The full historical preselected R_mix341 byte language, exact all-rule tariff and RES-to-AND3 or DEF-to-LOCAL-CONVERT mixed-rule interface remain missing. main.tex ownership reconciliation requires a complete current readback and optimistic-SHA safe edit; if unavailable, leave the manuscript untouched rather than risk overwriting the other specialists.

**Next decisive falsifier:** find one authoritative mixed-rule dispatcher with a real accepted RES-to-AND3 or DEF-to-LOCAL-CONVERT edge, then verify whether source-preserving frequency/owner canonicalization is still cost-sound across that actual interface. Independently run the published original-CLI executable in a full Node checkout and measure its physical parsing/output/retrieval costs.

Exactly the existing five role identities, titles, hourly Pacific schedules, historical tariffs, two Route A/three Route B labels and manuscript ownership boundaries are preserved. No automation changed. **P versus NP remains OPEN.**

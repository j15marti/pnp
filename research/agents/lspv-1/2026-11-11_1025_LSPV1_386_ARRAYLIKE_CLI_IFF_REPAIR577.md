# LSPV-1/577: Falsification and repair of the archived /386 raw-byte CLI iff

**2026-11-11 10:25 PST | LSPV-1 General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED source-code counterexample and corrected criterion; COMPUTATIONAL original-body V8 replay | P versus NP OPEN**

## Candidate theorem and four falsifiers, stated before searching

Target: [P2-L1-571] asserted that for EVERY raw byte input to the archived original /386 verifier, full CLI acceptance equals mathematical checkProof acceptance, nonempty gate owners and terminal pivot unequal to 999999. Candidate falsification: the original checkProof loops over numeric keys and the length of the records object without requiring a real Array, whereas the full CLI mutation calls the Array-only method records.at(-1).

Four falsifiers: **F1** an integer-indexed ordinary JSON object containing all original 103 records and length 103 fails the original mathematical checker; **F2** it passes the original full CLI despite lacking the at method; **F3** an ordinary object with string length "103" or fractional length 102.5 cannot pass the core; **F4** a native-accepted Array with nonempty gate owners and nonsentinel terminal pivot still fails a remaining corruption mutation. F1-F3 are refuted by concrete original-body executions. F4 is excluded by the original 571 inspection of all eleven mutations once the missing Array precondition is added.

## Corpus and priority audit

Read both root proof chains, including P2-D1, P2-C3, P2-B1, separate P2-B2/B3, P2-L1-571, P2-L1-575 and P2-L1-576; issue #3 including latest five-role contributions; AGENTS.md, CODEX.md, the pnp-research skill, pinned checker source, the exact signed LSPV-1/575 packet, LSPV-1/571 and /576, current LSPV-2/561, LSPV-3/573, LSPV-4/546 and LSPV-5/491, and materially relevant historical 539–549 reports. Inspected the 575 handoff. Repository search for array-like records, records.at errors, live native byte grammar and historical R_mix341/LOCAL-CONVERT found no prior exact version of this counterexample.

**Duplication control:** An initially considered graph-articulation clause-essentiality generalization had already been proved in LSPV-3/134 and /510; it was discarded rather than published again. Earlier isolated /386 wrapper self-test anomalies are credited to LSPV-1/565–571. This result **corrects**, rather than independently repeats, 571.

Primary literature used for scope and method: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 1979, https://doi.org/10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL 1977, https://doi.org/10.1145/512950.512973; Clarke, Grumberg, Jha, Lu and Veith, *Counterexample-Guided Abstraction Refinement*, CAV 2000, https://doi.org/10.1007/10722167_15; Urquhart, *Hard Examples for Resolution*, JACM 1987, https://doi.org/10.1145/7531.8928. None authenticates missing historical mixed rules.

Exact unchanged original code: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Original signed source packet: results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json, Git blob **d5de0f477cd736ec5fd7b01be18350f9cb594fd2**. The packet's 41 original SOURCE occurrences, 62 paid RES nodes, one distinct paid AND2 owner, W=63, 103 records, terminal empty clause and final pivot 16 are unchanged.

## Theorem 577.1: exact counterexample to unqualified 571.1

Take the accepted original /575 parsed packet P. Replace ONLY its records array by a plain JSON object with numeric string keys "0" through "102" mapping to the same records and a property "length":103. All source identities, proof nodes, chronological parent references, source specification, gate_defs, summary and last pivot are unchanged. Call the resulting raw JSON certificate b.

Then

$$
\operatorname{Core}_{386}(\operatorname{Parse}(b))=\mathrm{ACCEPT},
\quad |\mathrm{gate\_defs}|=1,\quad p_{\mathrm{last}}=16\ne999999,
$$

but

$$
\boxed{\operatorname{CLI}_{386}(b)=\mathrm{REJECT/CRASH}.}
$$

**Proof.** The exact original mathematical checkProof has a for-loop i=0,...,records.length-1 and accesses dat.records[i]. It does not test Array.isArray(dat.records). Numeric object properties supply every previously accepted row. All source, cost, parent, summary and terminal checks therefore return as before, with the same W=63. The full CLI next invokes the first corrupt mutator: it evaluates o.records.at(-1). The structured clone of a plain object remains a plain object and has no callable at method. This throws a TypeError **before** entering the helper's catch-wrapped call to checkProof. The original executable fails rather than accepting b. Consequently the universal iff published in /571 is FALSE as stated. QED.

This is not a new legal short proof or an R_mix341 mixed-rule certificate. It is a concrete accepted-byte grammar discrepancy within a pinned sibling checker.

## Theorem 577.2: corrected original full-CLI criterion

For EVERY one-file byte input b under the unchanged Node runtime, let P be its actual decoded JSON.parse output. Interpret parse errors, mathematical-checker failures, thrown mutations and nonzero wrapper exits as rejection. Then the exact corrected criterion is

$$
\boxed{
\operatorname{CLI}_{386}(b)\ \Longleftrightarrow\
\operatorname{Core}_{386}(P)
\land \operatorname{Array.isArray}(P.\mathrm{records})
\land |P.\mathrm{gate\_defs}|>0
\land P.\mathrm{records}.\mathrm{at}(-1).\mathrm{pivot}\ne999999.
}
$$

**Necessity.** The CLI first executes the core. Its first mutation requires a callable at method on the parsed records; an ordinary JSON object cannot supply such a method. Successful full CLI thus requires an Array. As already established by /571's source-code analysis, an empty gate owner array or terminal pivot equal to 999999 makes one of the eleven negative mutations ineffective and so fails the wrapper.

**Sufficiency.** On a core-accepted Array, the final record exists, is empty and is valid strict RES. Its at(-1) method works. Of the eleven original mutations, nine necessarily destroy a checked invariant for this Array; the other two are effective because the owner list is nonempty and the pivot differs from 999999. Thus every mutated packet fails the core and the original full CLI accepts. QED.

The missing Array condition is an **essential extra hypothesis**, not a silent reinterpretation of the /571 original theorem.

## Differential replay

The original checker function and original CLI loop were executed unchanged in hosted V8, adapting only fs, crypto, process and structuredClone interfaces. Seven differential controls produced:

| Parsed records | Mathematical core | Original full CLI | Explanation |
|---|---|---|---|
| Original Array of 103 records | ACCEPT | ACCEPT | All 11 mutations reject |
| Object, 0..102, length 103 | ACCEPT | FAIL | at is not a function |
| Object, length string "103" | ACCEPT | FAIL | Coercive core loop, then TypeError |
| Object, length numeric 102.5 | ACCEPT | FAIL | Coercive core loop, then TypeError |
| Object, length 102 | REJECT | REJECT | No terminal contradiction visited |
| Object, altered terminal clause | REJECT | REJECT | Incorrect signed resolvent |
| Original Array, unused owner removed | ACCEPT | REJECT | Owner-shift mutation ineffective |

The core genuinely accepts numeric-indexed object records with noninteger or string length properties because it compares i against length coercively; these are not accepted full-CLI certificates. The transcript and exact test predicates are in results/raw/arc/2026-11-11_1025_LSPV1_577_CLI_ARRAYLIKE_HOSTED_V8_RAW.json.

**Reproducible OS replay** is provided by experiments/arc/lspv1_577_386_cli_arraylike_counterexample.cjs. It pins both original Git blobs, invokes the unchanged original Node verifier as subprocess for seven generated byte files, and checks outcomes and the repaired iff. The new standalone script passed syntax compilation; its OS subprocess suite **was not executed during this run**. Independent LSPV-5 OS execution is pending, so computational evidence is qualified as hosted V8, while the source-level conditional is proved for the pinned implementation.

## Abstract interpretation and proof-chain effect

**P2-D1 remains OPEN.** The full R_mix341 grammar is still unauthenticated. The sibling checker does not recognize AND3, GF(2), LOCAL-CONVERT, contexts, branching, weakening, discharge, joins, deleted states, fresh/private/exported wire transports or any cross-rule dispatcher. Do not substitute CANON1/2/2R.

**P2-C3 remains OPEN.** In a concrete configuration intended to preserve **full CLI** completed proofs, include the records-container type (Array versus object) in addition to source provenance, paid identities, assumptions, definitions, freshness and all fixed tariffs. Alpha must not equate these two terminal states if it promises exact full-CLI acceptance preservation. One sound CEGAR refinement is the predicate records_is_array. For a merely MAY cost lower bound, one must distinguish legitimate cheap paths from rejected-wrapper artifacts by original checker replay. No complete mixed-calculus alpha/gamma or all-rule transformers have been proved.

**P2-B1 remains OPEN.** Original /575 W=63 upper bound and /576 core W>=36, full CLI W>=37 lower floors remain source-fixed sibling results. There is no superpolynomial lower bound for the complete mixed calculus. All legal algebraic, extension, branch and learning shortcuts must remain admitted.

**P2-B2/B3 separately OPEN.** A short proof in another system, checker existence, abstract validity or SAT in P does not establish polynomial Wbar in the same historical fixed calculus without an explicit noncircular transfer.

**Resource ledger:** The object-shaped core packet costs exactly W=63, not a cheaper proof. Evidence bytes, actual verifier runtime, discovery, span and peak memory are distinct, and a CLI crash is not a paid inference.

**Required tracker action:** downgrade unqualified [P2-L1-571] to FALSIFIED/RETIRED as written and add [P2-L1-577] corrected PROVED/RESTRICTED. No status promotion for P2-D1/C3/B1/B2/B3. Both root trackers read; proof1.txt has no material change. Attempt main.tex ownership-only reconciliation only with safe complete current content+SHA; otherwise disclose blocker.

**Five-role handoff:** LSPV-2 Route A tests native byte-typing against live checker; LSPV-3 Route B verifies all source/facet/provenance properties under repaired grammar; LSPV-4 Route A distinguishes W and actual verification resources; LSPV-5 Route B independently executes OS replay and tries to falsify repaired iff. LSPV-1 Route B owns exact quantifier/arrow ledger. Five existing titles, identities, schedules, America/Los_Angeles timezone, historical tariff and ownership boundaries and TWO Route A / THREE Route B allocation are preserved. No automations changed.

**P versus NP remains OPEN.**

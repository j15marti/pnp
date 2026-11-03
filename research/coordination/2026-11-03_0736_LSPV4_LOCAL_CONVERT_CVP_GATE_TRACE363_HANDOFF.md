# LSPV-4 to five-role handoff: LOCAL-CONVERT circuit syntax and CVP barrier 363

**November 3, 2026, 07:36 PST.** Task ID \`6ad42a1f03448191b8ded0c1f2dfa791\` and exact title/status/schedule left unchanged. General CNF-SAT; unchanged preselected Rmix341. **P versus NP OPEN.**

## Scoped mathematical result

For the fixed SAT source \`(x) AND (x OR y)\`, a paid AND3 gives exact factor \`S=x\`. The fixed Rmix341 LOCAL-CONVERT wording includes a “bounded-support Boolean circuit condition” with a local implication check. **Conditional on the literal unbounded-gate-output reading U**, input a constant-fed CVP DAG \`G\` as the circuit-valued proposed conclusion \`C_G=x AND output(G)\`. Its original-variable support is at most one even for arbitrarily large \`G\`; \`S => C_G\` iff \`output(G)=1\`. Therefore the **unannotated rule legality test under U is P-complete by Ladner's original CVP theorem**, despite constant original-variable support. It is *not* proved outside logarithmic space because \`L=P\` is unresolved.

The k-bit AND-constant chain gives a separate exact **Omega(k) authenticated input probes** on the all-ones valid proof record (flipping any constant bit invalidates it). This is a source/evidence-access lower bound, not a general SAT time lower bound.

## Supplied gate-by-gate truth tables repair the checking-space bound

Attach an 8-bit truth vector per internal gate. An indexed read-only-source verifier checks syntax, earlier references, all eight parent-to-child operations, input source factor and final implication in **O(log M) writable bits** and **O(M^3) charged steps** for complete augmented evidence length M, using rescans and counters. Annotation size is at most 8g bits for g gates beyond normal framing. Producing these gate values is separately charged; the materializing producer can use Theta(g) memory in an all-phase accounting.

This applies only to supplied, authenticated LOCAL-CONVERT output records. It does not show arbitrary correct SAT deciders produce these proofs or establish full Rmix341 logspace replay.

## Critical ambiguity to settle before proof-system conclusions

Is an arbitrary-length circuit DAG *inside one* LOCAL-CONVERT conclusion legal for **one charged node**, or must every internal gate be materialized as an independently paid DEF node? If the latter, the same reduction no longer shows q=2 with g independent payload gates. If the former, \`q\` alone cannot uniformly bound the raw size/work of every noncanonical proof presentation. A downstream-preserving canonical short form may still exist; the current results do not refute it. Do NOT change Rmix341 tacitly: pin this preselected rule's syntax from its initial definition before tightening the evidence normalizer.

## Independent controls

Python (seed 202611030736) 792 SAT/UNSAT-labelled local conversions, 396 SAT witnesses, 396 exhaustive UNSAT controls, 201 forged-output and 201 forward-reference rejections, 259 independent constant flips for chain widths to 128, ten malformed raw DIMACS and eleven malformed proof records. Independent no-producer-import Node referee passed 5,858 assertions, generating separate circuit instances and checking source labels and gate edges. Python host RSS 96,520 KiB and JS 33,252 KiB, neither a FLMV machine-space figure.

Proof cost \`W_R\` chooses the optimal valid derivation freely. This is a verifier/presentation audit and conditional P-completeness under U, not a minimum-cost lower bound. B1, B2, B3 and superpolynomial \`Wbar_R\` remain OPEN.

## Publication paths

- Formal report: \`research/agents/lspv-4/2026-11-03_0736_LSPV-4_LOCAL_CONVERT_CVP_GATE_TRACE363.md\`.
- Compact published reproducer: \`experiments/arc/lspv4_363_local_convert_compact.js\`.
- Public summary: \`results/raw/arc/2026-11-03_0736_LSPV4_LOCAL_CONVERT_CVP363_summary.json\`.
- User-facing archive: complete Python producer, independent JavaScript verifier, raw fixture JSON, source hashes, and this handoff.

Primary literature: Ladner, *The Circuit Value Problem Is Log Space Complete for P*, SIGACT News 7(1), 1975, DOI 10.1145/990518.990519; Cook/Reckhow, JSL 1979, DOI 10.2307/2273702. Project sources: five-role 12:04 handoff; LSPV-2 MIXED-TSEITIN-MIN-DAG341; LSPV-4 CANONICAL-EVIDENCE354; LSPV-4 AUGMENTED-AFFINE362; LSPV-5 SOURCE-AWARE-EXIT314.

## Next formal question

Freeze the exact allowed LOCAL-CONVERT output size and every DEF gate-slot source-dependency. Prove or falsify a **polynomial bounded-output canonical normal form preserving all later mixed-rule uses**, and only then attempt a complete mixed proof verifier under actual indexed-machine work/peak-space accounting. The critical global B3 implication is untouched.

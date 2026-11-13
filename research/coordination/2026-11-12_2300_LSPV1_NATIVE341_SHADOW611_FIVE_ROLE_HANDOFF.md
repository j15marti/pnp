# Five-role handoff: LSPV-1/611 /341 exact AND3 carrier/coordinate semantics

**November 12, 2026, 23:00 PST | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Result, precisely scoped.** In the unchanged original /341 SOURCE/AND3/XOR fixture checker (blob \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`), any reachable accepted AND3 support after unmodified \`JSON.parse\` with pristine JavaScript intrinsics must be an Array or String. Arrays must be actual permutations of the three numeric parent supports. Strings that pass the gate have length three in UTF-16 code units, three distinct Unicode code points (no surrogate pair), and are evaluated through the precise **ASCII-single-digit shadow map**: only array edge slots 0..9 can be written, regardless of whether \`"10"\` or \`"12"\` occurs as a substring accepted by \`support.includes(e)\`. Row-mask eligibility uses the *substring* test while row parity uses those same shadow bits. This is a complete native *local* transformer for those two JSON types, not a whole mixed proof checker and not an UNSAT-soundness theorem for String carriers.

**Concrete example:** with both parent supports \`[0,1,10]\`, \`support:"10A"\` passes the name gate, permits mask coordinate 10 but never writes actual edge bit 10. Parent truth tables \`0x96\` and \`0xe7\` give local derived table 102; \`"A10"\` yields 60. Unsupported assertion that String support equals an ordered list of numeric edge names is falsified.

**Execution:** Exact committed standalone Node-compatible reproducer loaded by GitHub SHA, executed in hosted V8 with dummy CommonJS bindings: 96,250 carrier/triple candidates, 92 positive String local gates, 65,628 original-versus-shadow table checks (including all 65,536 parent-table pairs on \`"10A"\`), 1,840 affine-row comparisons, 210 Array permutations, seven negative JSON types. All PASS. Independent OS Node execution and an original full-checker replay are not claimed.

**LSPV-1 (Route B):** Keep P2-D1 -> P2-C3 -> P2-B1 quantifiers exact; separate P2-B2/B3. Count each distinct shared paid inference once and never infer SAT/UNSAT from a buggy accepted /341 packet. This is a source-level partial-D1 refinement only.

**LSPV-2 (Route A):** Search the historical one-file dispatcher for authentic externally source-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT. Do not substitute /386 or CANON implementations.

**LSPV-3 (Route B):** Integrate the exact Array/String shadow transition into the native accepted-byte schema, retaining UTF-16 codeunit indexing, Unicode codepoint Set semantics, decimal substring membership, numeric \`BigInt\` masks, row scopes, and exact source IDs. Test non-Array non-String counterexamples and provenance ownership.

**LSPV-4 (Route A):** Audit the full tuple: paid W, parent references, literal evidence bytes, parse and verification time, actual machine steps, span, all-phase peak space. Neither the 65,628 test comparisons nor the 92 local passes are charged native proof nodes.

**LSPV-5 (Route B):** Independently falsify type exhaustiveness and exact shadow/row rules with malformed surrogate pairs, JSON objects with \`length\`, string \`includes\` substring collisions, negative/high mask coordinates and real accepted terminal fixtures. Compare directly against the original unchanged Node checker; do not claim new full historical rules.

**Artifacts:**
- report: \`research/agents/lspv-1/2026-11-12_2300_LSPV1_NATIVE341_ARRAY_STRING_SHADOW611.md\`
- executable: \`experiments/arc/lspv1_611_native341_shadow_transformer.cjs\` (blob \`40e24d0ec7f6a388ccae04a4b05c4079d2590d1a\`)
- raw: \`results/raw/arc/2026-11-12_2300_LSPV1_611_NATIVE341_SHADOW_TRANSFORMER_RAW.json\`
- this handoff.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1 and P2-B2/B3 remain OPEN. P1-01/03/04 remain OPEN. Preserve all five research roles, names, identities, hourly Pacific schedules, existing TWO Route A / THREE Route B, weights and owner boundaries; no automation changed. Next decisive target is still a single authoritative historical full mixed-rule accepted-byte checker with independent SOURCE-binding and a true cross-rule port. **P versus NP remains OPEN.**

# LSPV-1/387 post-publication root main.tex reconciliation

**November 4, 2026, 04:11 PST (America/Los_Angeles).** This is an additive correction to the *publication-status* statements in the 04:00 LSPV-1/387 formal report, five-role handoff, and original issue #3 comment. Their mathematics and statuses remain unchanged. No older research artifact is overwritten.

Initially \`fetch_file\` returned blob SHA \`07f76ecdf0a73c2e8bd8326c56ca274d2cbfba23\` with zero textual lines. Subsequently the GitHub **\`fetch_blob\` action succeeded**, returning the COMPLETE 1,594,815-character root \`main.tex\` from that exact SHA. After checking that the \`% END LSPV-1 OWNED\` marker existed exactly once, the new LSPV-1/387 paragraph was inserted immediately before it, preserving all 1,594,815 old characters in order and without editing any other region.

A GitHub \`update_file\` was sent against the authenticated current-head SHA, and succeeded at commit **\`562f4cfaa548f2f6e168ba1a07f8121257a086c2\`**. The exact new blob SHA is **\`6636883c332e399eec4130434d233cf9f0345d1a\`**, complete content length **1,596,702** characters. Independent full \`fetch_blob\` readback satisfied both:
- \`fetchedNew === constructedNew\` (exact byte-compatible text equality in the GitHub UTF-8 interface).
- \`fetchedNew.replace(insertedLSPV1Block, "") === originalFullBlob\` (all bytes outside the authorized insertion preserved).

The earlier "root reconciliation deferred" statement was **true at the time of the original publication**, but is now superseded by this authenticated completion. All fixed rules/weights, agent identities, enabled states and hourly schedules remain unchanged. The new theorem is a restricted encoding countercontrol; superpolynomial full-mixed cost, B1/B2/B3, and P versus NP remain OPEN. The full repository CI and LaTeX compilation were not executed; do not claim them.

# LSPV-1/562: Exact raw UTF-8 quotient for the recovered /341 checker

**2026-11-10 19:55 PST | General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Dependencies:** [P2-D1], [P2-C3], [P2-B1], [P2-B2]/B3 remain OPEN; [P1-01], [P1-03], [P1-04] remain OPEN. No historical grammar, weight or ownership change.

## IDEA and four pre-search falsifiers

**Candidate 562.1:** Every raw byte packet accepted by the exact recovered original SOURCE/AND3/GF(2) fixture checker has a strictly valid UTF-8 representative with identical decoded JSON, identical checker result, original-source identities, globally distinct paid-node identities, shared-DAG edges and logical paid cost. Representation bytes may expand, but by at most a factor three. This is NOT a native full R_mix341 rule theorem.

F1: Replacement decoding followed by UTF-8 re-encoding changes the JavaScript string. Excluded mathematically and on 4,107 native Node controls.

F2: A leading BOM is silently removed. Excluded: the original Buffer decoder preserves U+FEFF and JSON.parse rejects it. Default TextDecoder would differ.

F3: Live source-ID sharing depends on the invalid raw octets instead of decoded strings. Excluded for the recovered original checker by source inspection and original-code V8 replay.

F4: External raw-byte SHA provenance or missing historical mixed-rule parser invalidates the normalization. NOT excluded; explicitly outside this theorem.

## SEARCH: authoritative original evidence and provenance

Read current root proof1.txt and proof2.txt, issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, latest five-role handoffs and relevant LSPV-1/2/3/4/5 work, including 539-549 and subsequent results. The original mathematical rule declaration is research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). Pinned original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js (blob 4081022e8a3841d79f751a3d3a7a10decbb026da). Pinned independently authored original fixture checker: experiments/arc/lspv2_341_independent_verify.js (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0). This verifier only dispatches AND3 and XOR, hardcodes fixture length, and has no independently supplied external DIMACS binding.

Direct precedence: LSPV-2/543 active-token editor, /545 ill-formed UTF-8 accepted byte packets, /546 BOM parser false-positive; LSPV-3/558 guarded source-driven reconstruction and /559 exhaustive dispatcher audit; LSPV-4/531-532 physical work-space controls; LSPV-1/559-561 typed guards and signed mask quotient. This report resolves the *strictly valid byte representative* existence question left by /545 without claiming new full-rule authentication.

Primary literature: [1] Cook and Reckhow (1979), The Relative Efficiency of Propositional Proof Systems, JSL 44:36-50, DOI 10.2307/2273702; [2] Cousot and Cousot (1977), Abstract Interpretation, POPL, DOI 10.1145/512950.512973; [3] Node.js Buffer UTF-8 decoding documentation (ill-formed bytes produce U+FFFD). Literature provides proof-system/may-abstraction discipline, not authentication of historical native grammar.

External original repository review: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f. None supplies the missing historical R_mix341 full mixed-rule byte grammar; external FRAT-XOR is a different proof calculus.

## Theorem 562.1 (PROVED/RESTRICTED)

Let $D$ be Node Buffer's UTF-8 replacement decoder, preserving a leading U+FEFF code point, and let $E$ canonically encode scalar Unicode text into UTF-8 bytes. For arbitrary finite raw packet bytes $b$, define

$$
\nu(b)=E(D(b)).
$$

Every character in $D(b)$ is a Unicode scalar, including replacement U+FFFD. UTF-8 re-encoding is exact on these scalars. Thus

$$
D(\nu(b))=D(b),\qquad \nu(\nu(b))=\nu(b).
$$

The packet $\nu(b)$ is strictly valid UTF-8. Every valid UTF-8 segment is preserved byte-for-byte; every malformed nonempty subpart is replaced by one or more U+FFFD code points, each of which costs three bytes but consumes at least one original byte. Hence

$$
|\nu(b)|\le 3|b|.
$$

The bound is NOT nonexpansion: byte sequence 22 80 22, accepted as a quoted replacement-character JSON string, becomes 22 EF BF BD 22, increasing three bytes to five.

On the pinned original fixture verifier, raw packet acceptance factors as

$$
C(b)=Q(\operatorname{JSON.parse}(D(b))),
$$

with parse failure defined as REJECT and $Q$ the unchanged complete fixture-checker body. Therefore

$$
\boxed{C(b)=C(\nu(b))\ \text{for EVERY raw packet }b.}
$$

For accepted packets the parsed source labels, source clauses, source-ID aliases, all paid occurrence IDs, parent references, AND3 tables, GF(2) rows, deletion witnesses, and sink are identical. Consequently the first-creation count-once logical paid work satisfies $W(\nu(b))=W(b)$; NO statement about physical processing time or peak memory follows.

**Corollary 562.2 (exact minimum paid cost):** Fix independently authenticated decoded source $F$ and the recovered checker's accepted packets whose decoded source is $F$. Let $\mathcal A_F$ be the raw-byte accepted set, and $\mathcal A_F^\mathrm{strict}$ its strictly valid UTF-8 subset. Then, provided the sets are nonempty,

$$
\inf_{b\in\mathcal A_F}W(b)=
\inf_{b\in\mathcal A_F^\mathrm{strict}}W(b).
$$

Proof: strict packets are a subset, and every raw accepted b maps via $\nu$ into that subset with identical W. For discrete weights and attained minima, replace infimum by minimum. This is NOT source soundness: an already accepted SAT-source counterfeit stays accepted after $\nu$.

**Corollary 562.3 (evidence-size comparison):** For a fixed decoded source and upper bound on logical W, shortest accepted raw proof bytes $B_\mathrm{raw}$ and shortest strictly valid UTF-8 bytes $B_\mathrm{strict}$ satisfy

$$
B_\mathrm{raw}\le B_\mathrm{strict}\le 3B_\mathrm{raw}.
$$

The conclusion fails if the permitted source language uses an independently supplied RAW-BYTE hash or if a different unseen checker treats byte identity as semantic provenance. It does not transfer unchanged to the full historical grammar.

## ITERATE: actual executed tests and falsification controls

**Local OS Node v22.16.0:** executed 4,107 byte strings, covering isolated 0x80/0x81, truncated or overlong sequences, BOM at start/inside JSON, duplicate keys, escaped lone surrogate, and 4,096 SHA-256-derived buffers. All 4,107 passed decoder stability, normalizer idempotence and JSON acceptance equivalence. Canonical packet bytes grew in 3,783 cases, were equal length in 324, and shrank in none. These tests support the decoder implementation; the universal claim has the direct proof above.

**Original source bodies executed unchanged mathematically in connected V8:** seven original fixtures ACCEPT, 30,714 original checker assertion groups; consistent live K4 source ID U+FFFD ACCEPT, 30,714; consistent live source ID U+FEFF ACCEPT, 30,714; missing shared-parent ID REJECT; inserted missing DEF rule REJECT; leading BOM REJECT at JSON.parse. Host fs/process/console were shimmed. K4 has six edge variables, 16 strict source clauses, and 15 paid nodes. The separate LSPV-2/545 experiment previously independently verified the accepted *raw* invalid-UTF8 identities.

**Standalone script publication:** The committed original-checker OS Node harness syntax-checked in V8, but was NOT executed end-to-end in this run because the container lacks a GitHub checkout and cannot resolve GitHub DNS. The decoder-only OS Node test WAS executed. These are distinct validation categories.

Reproducer: experiments/arc/lspv1_562_utf8_quotient_native.cjs. Raw: results/raw/arc/2026-11-10_1955_LSPV1_562_UTF8_QUOTIENT_RAW.json. Shared handoff: research/coordination/2026-11-10_1955_LSPV1_UTF8_QUOTIENT562_FIVE_ROLE_HANDOFF.md.

## Dependency effect and exact remaining blocker

A fatal-UTF8 reference parser directly excludes accepted /545 packets, but a decoder-first, canonical-UTF8 normal form **preserves minimum paid work and decoded-source identity** for the recovered fragment. This is a rigorously cost-equal **representation quotient**, not a step simulation of the full proof calculus.

[P2-D1] remains OPEN until an authoritative original-source-bound accepted certificate exposes actual paid DEF owner, defining facet, Resolution consumer, LOCAL-CONVERT, wiring and branching/assumption-discharge syntax. [P2-C3] needs all-rule cost-sound alpha/gamma and transformers. [P2-B1] needs a superpolynomial lower bound over optimal whole shared DAGs, and separate [P2-B2]/B3 needs an explicit noncircular all-algorithm transfer.

No automation, role, label, rule, weight, schedule, enabled state, main.tex or other role artifact was modified. Two Route A/three Route B retained. **P versus NP remains OPEN.**

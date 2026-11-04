# LSPV-3/394 five-role handoff: lossless semantic recoding does not preserve proof-DAG minimum

**November 4, 2026, 06:24 PST. PROVED/EXACT in specified ordinary Resolution and uniform encoding models, with independently checked finite cases. External mathematical referee pending.** P versus NP OPEN. No rule, weight, task, identity, state or schedule changes.

## Exact statement and established published starting point

Haken (1985) proves for standard unary pigeonhole CNF P_h with h+1 pigeons and h holes that there exist c>0 and h0 such that, for every h>=h0, **every ordinary shared-DAG Resolution refutation** has >=2^(c h) lines. P_h has h(h+1) variables, (h+1)+h*binom(h+1,2) clauses and Theta(h^3 log(h+2)) explicit signed DIMACS bits. After subtracting O(h^3) source lines, the paid-inference bound remains exponential. This is **not** an Extended Resolution, Res(XOR), R_mix341 or arbitrary uniform SAT-algorithm lower bound. Cook 1976 gives polynomial ER PHP proofs.

**New theorem:** One fixed uniform polynomial-bit-time pair E,D acts on every finite raw byte string s with D(E(s))=s and E(s) a valid signed DIMACS CNF of O((|s|+1)log(|s|+2)) encoded bits. For every valid original CNF F, the model projection of E(F) onto even-indexed renamed original variables equals the model set of F. Nevertheless,

$$
W_{\mathrm{Resolution}}(P_h)\ge 2^{c'h},
\qquad
W_{\mathrm{Resolution}}(E(P_h))=0.
$$

Implementation: preserve every original signed source bit twice as the sign of the third literal in genuine tautological odd-ID clauses (z_j OR NOT z_j OR +/-a_j). Rename original variables to even IDs. Recognize canonical PHP syntax in uniform polynomial time; on that guaranteed-UNSAT family, replace active source clauses with one empty clause. Other valid CNFs retain their exact source conjunction on even variables; malformed strings are recovered via tags alone. A decoder reconstructs all bytes from the signed indexed tags. For PHP both old and new source theories have no models; for all others signed model projection is exact. The original source is *reversibly present as syntax*, but not necessarily active derivational premises.

If scalar I is invariant under E and upper-bounded by a fixed polynomial of minimum ordinary Resolution paid nodes, then I(P_h)<=p(0) for all h. This **FALSIFIES** assuming arbitrary reversible polynomial-time projection-equivalent recodings preserve proof minimum. It does **not** falsify a source-authenticated invariant preserved by only the actual locally charged R_mix341 transformations.

## Four falsifiers

1. Lossless invertible polynomial coding preserves Resolution minimum: **FALSIFIED**.
2. Saving every original source sign bit forces its use in a proof DAG: **FALSIFIED**; source data can be tautological annotation.
3. Encoding E supplies a legal R_mix341 refutation of the original P_h or refutes B3: **NOT ESTABLISHED**, because the encoder is not an allowed mixed inference, and there is no polynomial proof backtranslation.
4. Encoder uses per-h advice, semantic answer oracle or nonuniform lookup: **FALSE**; one fixed program recognizes canonical PHP by exact polynomial syntactic comparison.

## Machine work and independent finite verification

Logical cost of E(P_h) is zero **paid inference nodes**, not zero construction or validation. The explicit encoder emits 16|s| signed three-literal tags for |s| raw bytes, hence Theta(|s|log|s|) output bits in these families. Parsing, source/index reads, signed byte extraction, source recognition, serialization, output checking and all-phase peak memory are nonzero and must be charged; temporarily materializing the output contributes to rho in s'<=max{rho,eta,lambda,lambda*s}. A lazy circuit format has distinct costs and must be analyzed separately.

Local Python producer and independently written Node verifier both passed 268 cases: all 256 subsets of eight signed 2-variable clauses, canonical PHP h=1,2,3, and nine malformed/edge strings. Counts: 260 valid, 8 invalid, 4 recognized PHP records (one 2-variable subset equals PHP1), 267 single-copy corrupted signed-tag rejections. Checked exact byte roundtrip, original signed model projections, both-label small SAT/UNSAT, header/malformed controls, and independent SHA256 and output-length PHP values. All-size theorem is mathematical, not an extrapolation of these tests.

## Sources and duplication audit

Read first: November 2 12:04 worst-case five-role refocus, current issue #3, AGENTS.md, CODEX.md, and .codex/skills/pnp-research/SKILL.md. Original unchanged R_mix341 grammar: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11; each RES/AND3/XOR/LOCAL-CONVERT/DEF node is charged. The literal LOCAL-CONVERT original-variable-support restriction is assessed in research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md. No arbitrary semantic recoding operation is licensed. Reviewed LSPV-3/391 interface quotient, LSPV-3/393 duplicated-source provenance, LSPV-5/335 extensional normalization, and LSPV-2/387 legal restricted affine compiler. The older ordinary Resolution recognizer-with-fallback already defeats pointwise B1; this **additional** claim concerns explicit invertible semantic representation, not global B2/B3. Academic novelty is not asserted.

Actually inspected Grok GROKPROOF/2026-11-04_1322_PROGRESS.md, blob 0850246c1a1ea9a511d12a4de041b8752f69922a. Its fully charged all-input FLMV transformation remains OPEN. Actually inspected Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67; it concerns restricted alternation trading, not B3. Older Claude-0266 at blob 694c1c81 rejects unrelated spectral-invariant proxies. Literature checked: Haken (1985 TCS 39:297-308), Cook (1976 SIGACT News 8(4):28-32), Cook/Reckhow (1979 JSL 44:36-50), Urquhart (1987 JACM 34:209-219). Queries: Haken/PHP Resolution, Cook/ER upper, Cook-Reckhow proofs, Urquhart Tseitin, project source-block, LOCAL-CONVERT, semantic normalization, previously recognized PHP. These source claims were independently scoped rather than accepted as authority.

## Published outputs and directions

- Report: research/agents/lspv-3/2026-11-04_0624_LSPV-3_LOSSLESS_SEMANTIC_RECODING_FIREWALL394.tex
- Python producer: experiments/arc/lspv3_394_lossless_php_encoding.py
- Independent Node verifier: experiments/arc/lspv3_394_independent_verify.js
- Raw ledger: results/raw/arc/2026-11-04_0624_LSPV3_LOSSLESS_SEMANTIC_RECODING394_raw.json
- Handoff: research/coordination/2026-11-04_0624_LSPV3_LOSSLESS_SEMANTIC_RECODING394_FIVE_ROLE_HANDOFF.md

The standalone extended LaTeX report compiled locally; local Python/Node controls passed. A fresh root main.tex fetch returned current blob 1dc979b912d5f3357fe92e68cd2f32176646c48c but **zero bytes**; it was deliberately left unchanged to avoid clobbering ownership. Full checkout and repository-wide preflight were unavailable because local GitHub DNS failed.

LSPV-1: distinguish reversible semantic coding from paid source-authenticated proof translations; keep uniform B1/B2/B3 quantifiers. LSPV-2: search true legal R_mix341 mixed-rule transport for conservative circuits and GF(2). LSPV-3: develop exact guarded cofactor for the ACTUAL LOCAL-CONVERT grammar, or find a legal failure. LSPV-4: charge byte access, tag stream, verification, output, peak memory. LSPV-5: audit the illegitimate implication from an encoder's polynomial work to an original-source proof.

**Next gap:** a polynomially charged, source-correct transformation covering every licensed rule in the SAME preselected R_mix341. The superpolynomial worst-case Wbar_Rmix341 lower bound and B3 are unproved; B1/B2 OPEN. P versus NP OPEN.

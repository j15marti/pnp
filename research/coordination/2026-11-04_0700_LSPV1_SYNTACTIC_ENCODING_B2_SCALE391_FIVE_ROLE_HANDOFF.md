# Five-role handoff: LSPV-1/391 syntactic-encoding B1/B3 invariance and worst-case-time scaling

November 4, 2026, 07:00 PST. **PROVED/EXACT elementary restricted metatheorems; independent specialist review pending. COMPUTATIONAL finite coding controls. P versus NP OPEN.** This note changes no schedules, enabled states, IDs, role ownership, R_mix341 rules, or weights.

## What is proved

For **the same abstract source-labelled CNF F and same fixed proof calculus R**, two canonical polynomial-time mutually convertible and polynomially length-balanced syntactic encodings e0,e1 satisfy:

$$
\overline W_{R,e_1}(N)\le\overline W_{R,e_0}(g_{10}(N)),\qquad
\overline W_{R,e_0}(N)\le\overline W_{R,e_1}(g_{01}(N)).
$$

Therefore polynomial boundedness of $\overline W$ and the truth values of B1 and B3 are invariant under these genuine reserializations. If lengths are *exactly identical* for each F, B2 is invariant too. The all-binary correctness/malformed rejection and fixed-algorithm quantifiers are included.

A single correct total uniform SAT decider with genuine charged delays at lengths $m_k=n_k^2$, $n_k=2^{10^k}$, has $T_A^{wc}(n_k)\le2^{3n_k}$ yet $T_A^{wc}(n_k^2)\ge2^{n_k^4}$. Thus $T_A^{wc}(N^2)\le\operatorname{poly}(N+T_A^{wc}(N))$ is **FALSE for arbitrary A**. This is a counterexample to an unsafe B2 *proof step*, not to B2 itself.

LSPV-3/394's lossless source-changing semantic recoding lies outside our theorem and correctly demonstrates that mere injectivity plus model projection is insufficient to preserve proof-node cost.

## Reproducibility and publication

- Full proof: research/agents/lspv-1/2026-11-04_0700_LSPV-1_SYNTACTIC_ENCODING_B2_SCALE391.md
- Python producer: experiments/arc/lspv1_391_encoding_scale.py
- Independent Node checker: experiments/arc/lspv1_391_independent_verify.js
- All 256 finite input records with SAT label, two explicit lengths and finite minimum ordinary Resolution derived-node cost: results/raw/arc/2026-11-04_0700_LSPV1_ENCODING_SCALE391.json
- Python results: 823 checks, 95 SAT, 161 UNSAT, eleven malformed rejected, max toy Resolution minimum 3.
- Independent Node checker: 768 checks, 95 SAT, 161 UNSAT.
- Raw data were regenerated independently in the GitHub write runtime and agreed with Python summary counts; symbolic DELAY runtime not executed.

## Targeted follow-ups, existing five roles only

**LSPV-1**: Own B1/B2/B3 and worst-case minimum quantifiers. Audit the assertion that B2 remains invariant under arbitrary polynomial length recodings; the present theorem proves only the equal-length case, and the time-scale inequality needed by a naive proof is demonstrably false. Keep B3 primary.

**LSPV-2**: Audit fixed canonical source parser and the exact LOCAL-CONVERT global support/public-wire grammar. Test syntax-preserving conversion separately from new source clauses or model-projection encoders.

**LSPV-3**: Compare report /394 semantic E(F) source-changing behavior against /391 genuine serialization, and identify if any proof-preserving semantic translation has a polynomial node-overhead statement valid in both directions.

**LSPV-4**: Independently check the actual binary-counter DELAY all-phase time/space accounting, malformed-string timing, and the distinction between $T_A^{wc}(N)$ and $T_A^{wc}(g(N))$.

**LSPV-5**: Red-team all quantifier orders and source-identity hypotheses, including zero-cost proof packing, p-equivalent proof representations and cross-encoding worst-case peaks. Do not promote the B2 proof-step falsifier into B2 refutation.

Preserve the established Haken ordinary Resolution PHP theorem, Cook polynomial Extended Resolution countercontrol, Braun extension-free Res(oplus) preprint scope, parity/Tseitin XOR shortcuts, and all legacy controls. The actual Grok GROKPROOF/2026-11-04_1217_PROGRESS.md and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex were read; neither proves B3. Exact paths/blobs and literature audit in the proof report. Main.tex reconciliation remains separately subject to complete current-head readback.

**Remaining:** B1, B2, B3, superpolynomial worst-case Wbar for unchanged R_mix341, and P versus NP all OPEN.

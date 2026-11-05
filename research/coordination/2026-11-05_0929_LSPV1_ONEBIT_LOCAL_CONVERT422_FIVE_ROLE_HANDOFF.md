# LSPV-1/422 Route B handoff: one-bit LOCAL-CONVERT semantic-projection barrier
**November 5, 2026, 09:29 PST.** IDEA -> SEARCH -> ITERATE. P versus NP **OPEN**. Five-role allocation retained without task edits.

## Exact result and falsifier
For the fixed ternary relation $R(a,b,c)$ defined by integer $a+b=c$ on Boolean inputs, take any positive 1-in-3-SAT instance $G=\bigwedge_j (a_j,b_j,c_j)$, introduce private $s_j$ and one common public $t$, and let
$$
Q_G(x,s,t)=\bigwedge_j R(a_j,b_j,s_j)\land R(s_j,c_j,t).
$$
The exact projection onto the **single** public bit is $\{0,1\}$ if $G$ is satisfiable as positive 1-in-3 SAT, and $\{0\}$ otherwise. All $Q_G$ are SAT at $t=0$, so deciding whether a global LOCAL-like assertion $Q_G\models t=0$ holds is **coNP-complete**. The source has only three-coordinate factors, but unbounded total original support, even with one exported bit. The exact gadget appears in `blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md`; this is an independent mathematical transfer/replay, **not** a novelty claim.

**Falsifiers tested:** wrong $t=0$ witness; $t=1$ not matching exact-one model; forged forced-zero on SAT one-clause control; historical LOCAL-CONVERT restriction to bounded source region. The last is RESOLVED AS AN EXCLUSION at the semantic level: authoritative /341 explicitly limits LOCAL to ONE already derived local factor/equation and an explicit constant-original-support truth-table implication check. Thus global Q_G bundling is ILLEGAL. Exact serialized historical selector/export bytes remain unresolved. **This is not a LEGAL historical $R_{\rm mix341}$ counterexample.** It falsifies a proposed *broadened* one-step semantic projector that hides arbitrary factor networks behind a constant-width public port, absent an explicit proof/charged checker.

## Checks and physical costs
Exhaustive Python producer checked 1,040 distinct triple-subsets, $n=4,5$, with 3,128 assertions. Counts $n=4$: one forced-zero and 15 both-output; $n=5$: 548 forced-zero and 476 both-output. A separately written Node checker with independent exact-one enumeration and 8-value ternary truth-table checks passed 1,074 assertions. Controls included malformed factor inputs and forged projection assertion; no authoritative CANON2R or historical native checker was invoked.

Literal source comprises $2m$ three-port $R$ factors, $m$ private wires, one public wire and polynomial encoded source bits. Brute-force projector costs $O(m2^n)$ bit-factor evaluations and $O(n+m)$ peak scratch beyond source, with input/output reads charged. No proven superpolynomial machine runtime follows from coNP completeness, and there is no direct lower bound on $W_R$.

## Search, duplication and provenance
Reviewed governing directive (blob `c3889a3e`), current issue #3, /341, REFEREE365, LSPV-1/421, LSPV-3/425, AGENTS/CODEX/skill, actual Grok `GROKPROOF/2026-11-05_1428_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`. Both newly mandatory repos: `konard/p-vs-np/proofs/complexity/README.md` (blob `7ee9a11e`), `blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md` (blob `b30515cc`). Other paths: `meelgroup/frat-xor/format.md` blob `986a21aa` and `openai/math/.../ExecCNFNodeSearchCosts.lean` blob `1ced21f4`. Schaefer, STOC 1978, DOI 10.1145/800133.804350 gives positive 1-in-3 SAT hardness. Direct academic PDF mirror HTTP 403; direct branded Google interface unavailable, indexed-web used.

## Route B next work
- **LSPV-1:** Do not infer the one-decider B3 bridge from semantic one-port projection. Same-fixed-$R$ B3 and a superpolynomial full-mixed minimum remain OPEN. REFEREE365's CANON2R/EF equivalence is restricted to the proposed completion.
- **LSPV-3:** Determine exact historical LOCAL public/private wire/DEF-facet grammar and prove or reject whether any global $Q_G\models(t=0)$ could be a LEGAL one-node step. If the grammar rules it out, this transfer is a negative boundary control only.
- **LSPV-5:** Red-team source-cone vs literal-port vs one-public-bit conflation; do not import coNP semantic checking as a free native rule.
- **LSPV-2/LSPV-4 Route A:** Only cross-reference this as a warning against uncharged global projections, not an FLMV lemma.

## Publication
Report: `research/agents/lspv-1/2026-11-05_0929_LSPV-1_ONEBIT_PROJECTION_GRAMMAR_BOUNDARY422.tex`.
Code: `experiments/arc/lspv1_422_onebit_projection_independent.mjs`.
Raw summary: `results/raw/arc/2026-11-05_0929_LSPV1_ONEBIT_PROJECTION422_summary.json`.
Full local artifacts: `/mnt/data/lspv1_422/{onebit_projection422.py,independent422.mjs,raw422.json}`.

Root `main.tex` was **not edited**: the connector returned blob SHA `1b8a7d9a1514b06c96501849a7902b7aa3dae2a1` with empty content on a ranged read, making an outside-region byte-preserving edit impossible. No other role's manuscript region was touched.

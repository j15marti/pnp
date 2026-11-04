# LSPV-3/395: Hereditary source-core provenance and its ceiling

**November 4, 2026, 06:51 PST.** **PROVED/EXACT** within unchanged authenticated binary-premise Rmix341, independent specialist review pending; **COMPUTATIONAL** finite controls. Neither P versus NP nor B3 is proved. No task changes.

## Mathematical theorem and counterexample

For UNSAT CNF $F=(C_i)_{i=1}^m$ and each assignment $a$, set $U(a)=\{i:C_i(a)=0\}$. Define

$$
\kappa(F)=\min\{|S|:S\subseteq[m],\ \forall a,\ S\cap U(a)\ne\emptyset\}.
$$

This is exactly the cardinality of a minimum UNSAT source core. For every sound source-explicit conservative refutation DAG in the fixed Rmix341, using at most two parent nodes per charged inference,

$$
W_{R_{\mathrm{mix341}}}(F)\ge\kappa(F)-1.
$$

Proof: the final ancestry's used sources $S_\pi$ must themselves be UNSAT by soundness and extendibility of paid conservative gate definitions, so $|S_\pi|\ge\kappa$. A connected $k$-source, $q$-paid-node ancestry graph has $k+q-1$ or more edges but at most $2q$ incoming-parent edges. Thus $q\ge k-1$. Free ideal sequence selection is included.

**Hereditary source-subset conservativity:** If $D$ is a fresh conservative definitional circuit, for every subset $S$ of original source clauses, $S\land D$ is SAT iff $S$ is SAT. Consequently $\kappa$ survives all such paid gate additions. Whole-formula equisatisfiability of an already-UNSAT formula alone does not preserve $\kappa$.

**Exact hard-subformula falsifier:** Let $P_h$ be the standard unary PHP with $h+1$ pigeons, $h$ holes, $m_h=(h+1)+h\binom{h+1}{2}$ clauses, $\Theta(h^3\log(h+2))$ indexed signed CNF bits. Haken (1985) proves every unrestricted ordinary shared-DAG Resolution refutation of $P_h$ has $2^{\Omega(h)}$ lines. $P_h$ is clause-minimally UNSAT, so $\kappa(P_h)=m_h$. Consider the **different source formula**, NOT a legal Rmix341 inference, $P_h^+=P_h\cup\{(z),(\neg z)\}$ for new $z$. Then

$$
\kappa(P_h^+)=2,\qquad
W_{\mathrm{Resolution}}(P_h^+)=W_{R_{\mathrm{mix341}}}(P_h^+)=1.
$$

Every original source is preserved verbatim, yet the bigger CNF admits a one-step proof on the added units. No source clause is itself empty, so zero paid inferences cannot refute it. This is a **family failure**, not a disproof of Haken or any unrestricted SAT lower bound. Cook's polynomial Extended Resolution PHP proofs and Gaussian elimination on odd Tseitin remain control shortcuts. No assertion of mixed-system hardness of original PHP is made.

**Ceiling:** For explicit indexed CNF size $N$, $\kappa(F)\le m\le O(N)$. Hence every lower-bound argument using only minimum source-core size plus two-parent ancestry can certify no more than a linear node bound. Discovery of $\kappa$, proof construction, encoded evidence, bit access, validation, output and peak RAM are separate.

## Reproducibility and provenance

The deterministic JavaScript producer passed 55 assertions, including exhaustive SAT/UNSAT labels and all one-source-deletion SAT controls for $P_h$, $h=1,2,3$, exact minimum-core enumeration for $h=1,2$, and corrupted pivot and source-index rejections. Original core sizes are 3 and 9 for $h=1,2$; augmented core size is 2 in each tested case. Independently implemented Python reconstructs sources and cores. Finite checks do not establish Haken's theorem or simulate arbitrary algorithms.

Exact verified artifacts:
- Formal report: research/agents/lspv-3/2026-11-04_0651_LSPV-3_HEREDITARY_SOURCE_CORE_FIREWALL395.tex ; blob 00df46b40a36a9101b2cab6fb73632baa70fce38
- JavaScript: experiments/arc/lspv3_395_source_core_ceiling.js ; blob 33a99670a2b160b448ac6e68719f56192bcf1368
- Independent Python: experiments/arc/lspv3_395_independent_core_check.py ; blob e661d2d8f4593ca552bb59de3e372978b08e6732
- Raw: results/raw/arc/2026-11-04_0651_LSPV3_SOURCE_CORE_CEILING395_raw.json ; blob e5d04850784d423f9992e916a4b2766ca6c2c90f

**Root main.tex limitation:** Both current full read and line 1-80 ranged read gave Git SHA 4527606e8c50cea75210f78aa93877edf2dd2822 with ZERO content. Raw GitHub fetch rejected the oversized file; direct git ls-remote failed DNS. Therefore the manuscript is untouched, not overwritten from a partial blob. No whole-repository preflight or LaTeX compilation was claimed.

**Corpus:** controlling Nov 2 refocus, current issue #3, AGENTS.md, CODEX.md, pnp skill, authentic fixed Rmix341 in LSPV-2/341 (blob c87acd11), LSPV-3/393 (56cab30f), LSPV-3/394 (d79f05a4), LSPV-1/390 (126f771c), LSPV-2/391 (206800eb), LSPV-5/337 and LOCAL-CONVERT grammar addendum (bbcdad9a). Actual Grok GROKPROOF/2026-11-04_1322_PROGRESS.md blob 0850246c and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727 were read and assessed; neither supplies B3. Literature checked: Haken 1985, Cook 1976, Ben-Sasson and Wigderson 2001, minimum UNSAT cores, Cook and Reckhow 1979. The source-core/hitting-set duality is standard, not claimed as new academic mathematics. Project novelty is the explicitly isolated same-grammar hard-subformula countercontrol and hereditary source condition.

## Falsifiers and specialists

F1: retaining a Haken-hard subformula forces hardness of a larger CNF. **FALSIFIED.** F2: global UNSAT semantic equivalence preserves source-core cost. **FALSIFIED.** F3: total conservative DEF additions remove source necessity. **FALSIFIED under fixed R.** F4: source-core provenance alone yields superpolynomial machine hardness or B3. **FAILED TRANSFER** because $\kappa\le O(N)$.

**LSPV-1:** preserve B1/B2/B3 quantifiers and mark this only family failure. **LSPV-2:** certify that actual LOCAL-CONVERT syntax tracks source dependencies and circuit gates without an implicit oracle. **LSPV-3:** search an invariant beyond source ancestry, falsifying it against free additional axioms, ER and GF(2). **LSPV-4:** charge proof DAG extraction, input acquisition, emitted core, verification, intermediate storage and all-phase peak memory. **LSPV-5:** audit no-empty-source proof minimum and the all-subsets conservativity condition. The next gap is a non-source-only universal invariant and an independently justified B3 for preselected R.

B1, B2, B3, a superpolynomial worst-case mixed minimum and P versus NP remain OPEN. No identities, enabled states, schedules or proof-system rules were changed.

## Post-publication malformed-input addendum

A separately committed, source-readback-verified JS parser-sidecar tests an explicit DIMACS encoding of both SAT and UNSAT sources, and rejects ten malformed inputs (wrong header count, missing terminator, out-of-range index, nonnumeric source token, malformed header, extra empty clause, clauses before header, empty input, duplicate header, trailing token). It passed 12 checks. Path: experiments/arc/lspv3_395_dimacs_malformed_controls.js ; verified blob 6db498eec92f572b42e2a60541c4e41d340d8963. These finite grammar checks augment the 55 proof/source tests but do not change the mathematical theorem or establish completeness of the production Rmix341 parser.

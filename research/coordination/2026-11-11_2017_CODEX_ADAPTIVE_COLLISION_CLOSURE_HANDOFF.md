# Adaptive collision and closure barriers

Date: 11 November 2026, 20:17 PST
Mode: reconstruction, red-team, experiment
Status: **P versus NP remains open.**

## Accomplished continuation

Tested the preceding report's growing-multiplier target for the actual minimum verified-witness benchmark:

$$
s_{j+1}\le Cs_j,\qquad H(F_{j+1})\ge H(F_j)s_j^c/B.
$$

That target would imply $H(F_j)\ge2^{\Omega((\log s_j)^2)}$ and, through the recovered all-decider bridge, exclude polynomial SAT. It remains **OPEN**.

The explicit candidate implemented here is a sequential chain of collisions in truncated keyed Feistel permutations. Each key depends on the preceding collision witnesses. Two inverse evaluations find each next collision. The canonical family has polynomial $H$, so this candidate cannot supply the target multiplier.

## Exact transfer and exclusion results

1. **Adaptive collision enumeration.** If every valid prefix extends to a next explicit shrinking map on $r_i+1$ bits with $r_i$ output bits, one algorithm has native time
   $$
   \operatorname{poly}(N)\sum_i 2^{r_i}.
   $$
   With charged construction, reconstruction, gate completion, polynomial stage count, and fixed universal simulation:
   $$
   H(F_k)\le\operatorname{poly}(N)2^{O(R)},\qquad R=\max_i r_i.
   $$
   Thus $R=o((\log N)^2)$ rules out the squared-log target. The constant-output objection was already in the October 13 note; this is its quantified adaptive extension.

2. **Nonlinear inverse control.** For a uniformly invertible permutation $P_z$ on $r+1$ bits,
   $$
   C_z(u)=\operatorname{prefix}_r(P_z(u))
   $$
   has collision $P_z^{-1}(0^r0),P_z^{-1}(0^r1)$. This stays polynomial with candidate-dependent keys and arbitrary polynomially bounded widths. Meeting the necessary output-width threshold therefore does not establish hardness.

3. **Closure small-seed lemma.** For an intersection-closed family on $m$ coordinates, an acceptance predicate represented on that family by a GF2 polynomial of degree at most $d$ accepts some model iff it accepts the closure of some seed of size at most $d$. Group monomials by their closures and choose an inclusion-minimal surviving coefficient. Closure and acceptance evaluation must be efficiently obtainable.

4. **Closure-chain bound.** Under actual selected-prefix extensibility, uniformly polynomial representation acquisition, lifting and stage count,
   $$
   H(F_J)\le\left[\operatorname{poly}(N)\sum_{j<J}B(m_j,d_j)\right]^{D_0},
   \qquad B(m,d)=\sum_{\ell\le\min(d,m)}\binom m\ell.
   $$
   Thus $H\le N^{O(d_*+1)}$ when $m_j\le\operatorname{poly}(N)$, and $d_*=o(\log N)$ rules out the squared-log target. More sharply, some stage must have
   $$
   \min\left\{m_j,\delta_j\log(e m_j/\delta_j)\right\}
   =\Omega((\log N)^2),\qquad \delta_j=\min(d_j,m_j).
   $$
   All $m_j=O(\log N)$ already gives polynomial work regardless of degree. Successful witness search can enumerate seeds until success without knowing $d$ beforehand; early rejection requires a justified degree bound.

5. **Clocked error-search obstruction.** For each fixed exponent $k$, the language of logarithmic-length programs having a same-length SAT-search error by clock $N^k$ is sparse and in NP. A polynomial counterexample table exists nonuniformly, but its uniform acquisition and correctness/reflection proofs are not free. No single total refuter polynomial in $N+k+|p|$ with a degree independent of $k$ can always produce an error when one exists: a self-quoting program repairs its returned pair and fails elsewhere. This does not rule out fixed-$k$ refuters of time $N^{O(k)}$, nor contradict $P=NP$.

All these are exact upper bounds or precisely scoped obstructions. They do not prove an unrestricted lower bound or imply an ETH conclusion.

## Computational evidence

Producer SHA-256:
9197bc468d255e7746f6d2f6c8a421c6186bce887584ef12212c8cd26c6a5ff8

Independent-audit SHA-256:
55a09519a0883617bd891b1d65cbf5ace4c3e24b33cd6723b49077d1a69edbdc

Both executions are deterministic, exact Boolean computations without a random seed. Recorded runtimes are approximately 0.245 and 0.0043 seconds.

- 4,080 permutation/inverse checks.
- 24 producer gate truth checks.
- 2,048 primary assignments exhausted on the smallest nonlinear chain, with 16 satisfying and zero semantic/CNF mismatches.
- Five compiled chains, up to 983 variables and 3,955 clauses.
- 48,642 closure-family/polynomial pairs across all 121 nonempty intersection-closed families on three coordinates, with zero mismatches.
- Independent exported DIMACS/witness check: 201 variables, 797 proper clauses, every variable occurs, all four padding assignments valid.
- Independent 96 gate/padding and 48 aliased-input checks.
- Independent 64 permutation inputs across four keys, with coordinate ANF degrees two or three.

The exhaustive primary check is not enumeration of all auxiliary assignments. Exact gate equivalences supply that part of the reasoning. Inverse-evaluation counts exclude forward validation and gate completion. These experiments do not measure minimum $H$.

## Corpus and literature reconciliation

Pinned root manuscript blob: ca1c40a11155442a7ecdf74d0e05db3f83abae9a.

Read the prior Codex transfer report, the uploaded October 13 minimum-work note, current root/governance/trackers, targeted MAIN and specialist history, the actual AFFINE-TABLE-COMPOSITION2 report, the relevant block/protection and Type-I pruning notes, and the original LSPV-1/586 report. This was a targeted survey with direct material-source reads, not an all-byte historical reread.

AFFINE-TABLE-COMPOSITION2 blob: 3809296b0a5f6ea85fc03bf1d8441b04e3017585.
Its Horn/affine algorithm and closure-basis proof are credited prior components. Primary sources confirm fixed-rank tractability. No novelty claim is made for that result.

Hubacek's 2026 NestedCollision separation is a black-box decision-tree result; it cannot be promoted to an unrestricted circuit-input machine lower bound. Mahaney's sparse-language theorem and Bogdanov–Talwar–Wan's conditional dreambreaker theorem are used with their exact quantifiers.

The reported archived /341 checker defect means raw ACCEPT cannot authenticate semantic refutations without a separate source/inference gate. This is prior evidence, not a new independently replayed checker exploit here. The positive-witness verifier used for $H$ is separate.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to a load-bearing OPEN status.

## Review and validation

Three temporary research agents supplied independent construction, clock/closure, and corpus reviews. The exact final statements were cross-checked against their findings. The independent code auditor does not import the producer.

Local report hygiene and research preflight checks passed on the partial snapshot. Additional validation checked LaTeX brace/environment balance, citation keys, required report markers, and tested-code hashes. A PDF compilation was attempted, but the environment lacks the pdflatex format file; no rendered-PDF validation is claimed.

This ordinary Codex continuation creates append-only reports, code, and results. It leaves root manuscript ownership regions, existing timestamped reports, tracker statuses, and all schedules unchanged.

## Single next target

Recover the exact witness-extension relation of the next fully specified candidate-dependent wrapper and test actual-prefix extendibility. Apply the collision and closure algorithms with all representation and lift costs charged. A surviving candidate must escape these upper bounds by proved parameters or a real compatibility obstruction. The decisive all-program $H$ amplification inequality remains to be established.

## Artifacts

- research/agents/codex/2026-11-11_2017_ADAPTIVE_COLLISION_AND_CLOSURE_BARRIERS.tex
- research/agents/codex/2026-11-11_2017_ADAPTIVE_COLLISION_AND_CLOSURE_BARRIERS_refs.bib
- research/coordination/2026-11-11_2017_CODEX_ADAPTIVE_COLLISION_CLOSURE_HANDOFF.md
- experiments/review/witness_amplifier_controls_20261111.py
- experiments/review/witness_amplifier_independent_audit_20261111.py
- results/raw/review/2026-11-11_WITNESS_AMPLIFIER_CONTROLS/witness_amplifier_controls.json
- results/raw/review/2026-11-11_WITNESS_AMPLIFIER_CONTROLS/independent_audit.json
- results/raw/review/2026-11-11_WITNESS_AMPLIFIER_CONTROLS/nested_feistel_h2_k2.cnf
- results/raw/review/2026-11-11_WITNESS_AMPLIFIER_CONTROLS/nested_feistel_h2_k2_witness.json

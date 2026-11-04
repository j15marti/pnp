# LSPV-3/382 handoff: succinct semantic-support locality is coNP-complete

**November 3, 2026, 20:24 PST.** Task: PNP Hypergraph & Proof Certificates (LSPV-3), unchanged. Do not change Rmix341, schedules, ownership or verified results. **PROVED/EXACT** theorem for explicitly defined signed fan-in-two circuits, not for the unverified full LOCAL-CONVERT syntax; **COMPUTATIONAL** finite controls; **OPEN** full-system worst-case superpolynomial minimum, B1/B2/B3 and P versus NP.

## New theorem and precise limitation

For each fixed k >= 0, decide whether a valid acyclic signed AND2 gate circuit on n named ORIGINAL inputs computes a function with at most k *essential* original input variables. This language is coNP-complete. Membership: the complement has k+1 distinct essential variable indices, each with two input assignments differing on that variable and different outputs. Hardness: from any CNF C(x), construct conservative signed AND2 gates for f_C(x,y)=C(x) AND y_1 AND ... AND y_(k+1). If C UNSAT, f_C is the zero function with zero essential support. If C SAT, all k+1 fresh original y inputs are essential. Circuit encoding and construction are polynomial. For k=3 this is an exact semantic-support restriction relevant to AND3 and LOCAL-CONVERT, **only if** the authoritative rule admits named circuits with arbitrary transitive original dependencies and tests semantic (rather than syntactic) input support. It has not been shown that Rmix341 permits this exact interface.

**Operational distinction:** LSPV-4/363 already proves P-completeness of LOCAL-CONVERT validity under syntax U restricting the circuit to <=3 original input wires, even for arbitrarily long internal gate payloads; LSPV-5/315 already disproves proof-node-count domination of encoded payload size under U. Both remain correct. The new coNP-completeness concerns *recognizing that an arbitrary many-original-input succinct circuit happens to depend semantically on <=3 variables*. A transitive syntactic-cone check is polynomial and conservative but not equivalent to an exact semantic-support check, e.g., x AND NOT x has zero semantic support. Do not silently replace the fixed calculus with either variant.

## Reproduction (authenticated current GitHub files)

- Report: `research/agents/lspv-3/2026-11-03_2024_LSPV-3_SEMANTIC_SUPPORT_CoNP_BARRIER382.tex`, blob `96963b6e4c603db2ee535e23df12c63dbce52e0f`.
- Code: `experiments/arc/lspv3_382_semantic_support_locality.js`, blob `582edeb43e223a041434638c198ca0d2637e31c4`.
- Raw: `results/raw/arc/2026-11-03_2024_LSPV3_SEMANTIC_SUPPORT_LOCALITY382_raw.json`, blob `0ddcf21c4cab8afd5aab4097d1be9aa5d5ee6178`.

The exact GitHub-readback source executed in V8 passed 149,505 checks for all 256 subsets of eight ternary clauses on three variables: 255 SAT, one UNSAT. Signed two-input AND circuits for each resulting f_C over 7 original variables were checked against a direct CNF truth table. Essential-support sizes: 0:1; 4:1; 5:6; 6:30; 7:218. 1,020 fresh-y witness pairs passed. Seven malformed circuits rejected, two sign-corruptions semantically detected. Finite observations verify fixtures, not coNP-completeness or an optimum over R.

## Four falsifiers and next obligations

F1 exact essential support equals transitive syntactic cone: false (x AND NOT x). F2 one named output implies <=3 original inputs: false (f_C when C SAT). F3 8-row named-wire truth tables suffice for arbitrary semantic-support checking: false absent restricted cone or paid equivalence certificate, by coNP-completeness. F4 this alone establishes SAT runtime hardness or B3: false, model mismatch.

Start with established Haken exponential Resolution lower bound on unary PHP: every ordinary shared-DAG refutation requires 2^Omega(h) lines, with N=Theta(h^3 log h) explicit signed bits. Cook Extended Resolution PHP and mixed odd-Tseitin linear XOR are countercontrols. Do not reverse proof-system simulation inequalities.

**Immediate ask to LSPV-2/LSPV-1:** obtain and validate the complete authoritative LOCAL-CONVERT gate payload and exported-wire grammar. Decide whether support means (i) syntactic transitive original cone, (ii) exact essential support with paid proof, or (iii) a restricted <=3-original-input grammar. Each choice must be checked against original rules without changing R. **LSPV-4:** audit bit cost and fully charged semantic-support test vs proof evidence, including all-phase rho. **LSPV-5:** adversarial audit that no proposed portable invariant assumes a free semantic support oracle.

Grok: `GROKPROOF/2026-11-04_0413_PROGRESS.md`, blob `09396ad9a5bfccfb575845a492e1a91b6c43f56b`, explicitly leaves charged all-input FLMV transfer open. Claude: `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, restricted alternation-trading, not B3. Read and evaluated, not treated as correctness authority.

Container backed preflight unavailable. Code, raw, report and this handoff were written using current-head GitHub content writes. No root main.tex modification without complete authenticated readback and ownership-safe reconciliation.

**P versus NP remains OPEN.**

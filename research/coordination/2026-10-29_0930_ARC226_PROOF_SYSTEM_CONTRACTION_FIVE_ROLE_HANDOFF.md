# ARC226 LSPV-1 proof-system coverage and strict contraction firewall
29 October 2026, 09:30 PDT. **P versus NP OPEN**. No task identity, cadence, enablement, or role ownership changes.

## PROPOSE: exact missing lemma and four falsifiable mechanisms
The missing arrow remains an **unconditional, uniform, total polynomial-cost, SAT/UNSAT-preserving one-child strict encoded-size successor** for arbitrary SAT, or a separately correct unrestricted same-machine lower-bound contradiction.

M1: existence of the specified fully paid uniform successor is merely sufficient, not necessary, for P=NP. **FALSIFIED as a logical distinction**: the *existence* is equivalent to P=NP (on SAT or an equivalent encoded class). Finding such a map independently, without assuming SAT in P, is still OPEN. Different architectures may prove P=NP without constructing this exact one.
M2: every UNSAT instance must have a polynomial ordinary-resolution certificate if SAT in P. **FALSIFIED unconditionally** by Haken's 1985 exponential PHP resolution lower bound. This is a proof-system limitation, not general SAT hardness.
M3: source-authenticated XOR/affine proofs automatically have polynomial all-UNSAT coverage. **OPEN for unrestricted proof languages**; a specific stronger DAG Res(XOR) barrier is claimed in a 2026 preprint with Lean sources, but no independent kernel replay here.
M4: OpenAI's quantum one-recursive-call unitary-synthesis skeleton yields a classical SAT contraction without evaluating its target-dependent Boolean oracle. **FALSIFIED as inference**: oracle choice/evaluation is uncharged and could be hard.

## BUILD: formal elementary equivalence
Let C have two directly solvable fixed YES/NO terminal formulas, SAT <=p C and C <=p SAT, and be closed under a fixed deterministic total polynomial-time map K. Suppose K(x) produces exactly ONE child in C, preserves the SAT answer on *both* sides, and for all physical lengths N >= N0 the actual written child has |K(x)| <= N^lambda, for fixed lambda in (0,1). Then recursion has O(log log N) levels, with all polynomial generation/access/certification/failure costs charged, and decides SAT in P. Conversely, if P=NP, reduce C to SAT and use the decider to output a constant YES or NO terminal child. Thus **existence of such K iff P=NP**. The original instruction saying the sufficient target is not necessary must be understood as 'this architecture need not be used to prove P=NP', not as a logical non-equivalence of existence. For a general C only SAT <=p C is not enough for the converse; both reductions are required. Same observation holds for a fully paid polynomial-value descending-rank SAT machine.

## Existing theorem firewall
For standard unary PHP_(h+1)^h with polynomial input length, Haken 1985 established ordinary resolution proof length 2^{Omega(h)}. Hence requiring polynomial ordinary-resolution proof coverage for every UNSAT CNF is **mathematically impossible regardless of P=NP**, and should be retired. It does not rule out a different system: Buss's short Frege proofs for PHP demonstrate the distinction. No transfer to proper strict signed exact-(2,2)-3SAT without a proved proof-preserving reduction.

Source-inspected **EXTERNAL CLAIM** (not independently kernel checked): kbr-/math-research, publications/bit-php-resolution-over-parities/sections/01-introduction.tex, Git blob db426b613cae879fd6173dd54453829b49cb5b3b; formalization/claims/BitPHPExponential.lean, blob c222191a0a0dd895530ea67148be343be886d4fd, states DAG Res(XOR) size > exp(h/(32768 ell^2)) for bit PHP, h=2^ell, ell>=32. Their readiness audit reports Lean kernel checks; this run only fetched source. No general Frege or arbitrary SAT lower bound follows.

Source-inspected OpenAI unitary synthesis: openai/math at adc7f1241b42e322a6451854ab7e4b4c146bf78a; preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/01-introduction.tex, blob 5ad06c26238e2572e93f68b380f542b2ab1845fe. It explicitly does not supply polynomial classical construction of the target-dependent Boolean oracle.

## Independent Library archive and executable
The precise Library ID libfile_a2862f0165b4819195a88d9e896a42a7 was materialized, original ZIP SHA-256 a826f34b4caa3dce1d6a060079316a462b775fe3fb1f14674ab62b2e7299dfff; original REPORT.tex/PDF and audit.py reviewed; original audit.py rerun output byte-identical to results.json (4,680 boundary, 7,191 discovery and 139 brute-force checks; all 130 sampled exact22 signed variants SAT, explicit NO controls outside exact22). The theorem n<=3b+12bq is strictly architectural fixed-static-boundary coverage, not SAT runtime lower bound.

ARC226 executable passed five exhaustive tiny PHP refutations (full source-indexed resolution DAG checked), 800 random 2SAT/brute-force controls, three forged-pivot rejections, and four toy independent-oracle-OR query controls. PROVED asymptotic statements rely on elementary proof above and established Haken theorem, NOT these finite tests. No proof assistant kernel was invoked.

## Model-native resource ledgers
One shared writable tape: includes initial input footprint, head travel, writes, crossings and peak storage. One-input-head multitape: distinct visited work cells, traffic and total output. Two writable tapes: separate total symbol changes D1/D2 and workspace, no imported D2-only bound. Indexed RAM: all parsing, source lookup, failed strategies, summary construction, simulation and output. Fixed UTM: single interpreter plus program-description, access and simulation costs. SAT and UNSAT are restrictions of ONE uniform correct algorithm, no free label bit. Do not copy restricted lower-bound exponents between models.

## Five preserved role dependencies
LSPV-1 Lead: enforce exact theorem quantifiers and prohibit assumed all-input certificate coverage. Next test locally authenticated *stronger-than-resolution* UNSAT grammar, measure discovery, then ask whether ANY answer-only successor strictly shrinks unrecognized sources.
LSPV-2 Circuit builder: test source-preserving occurrence/degree conversions from PHP and mixed instances, and whether they preserve proof complexity; do NOT assume.
LSPV-3 Moving interfaces: explore locally computable exact compatibility summaries with polynomial physical size and polynomial-value rank descent; test hostile hereditary fixed points.
LSPV-4 Resource auditor: same-program RAM, single-tape, two-tape, fixed UTM cost quantifiers, no crossing-sequence-to-RAM transport.
LSPV-5 Red team: independently audit ARC226 logical iff, Braun source-vs-kernel status and Haken original hypotheses; hunt counterexamples to proposed summary compression. None of the agents should treat a failure to find such a compiler as a separation proof.

## GitHub and Library artifacts
Full source: research/agents/lspv-1/2026-10-29_0930_LSPV-1_ARC226_PROOF_SYSTEM_CONTRACTION_FIREWALL.tex
Executable: research/agents/lspv-1/2026-10-29_0930_ARC226_proof_system_firewall_audit.py
Raw: research/agents/lspv-1/2026-10-29_0930_ARC226_raw_results.json
Bibliography: research/agents/lspv-1/2026-10-29_0930_ARC226_references.bib
Persistent Library: /PNP Formal Proof Lead/ARC226/ includes the five-page PDF and SHA-audited complete zip.
**Scientific statuses**: elementary iff PROVED; Haken theorem PROVED in established literature; specific PHP computational controls COMPUTATIONAL; Braun source claim NOT independently verified; unrestricted contraction, ARC/FLMV same-machine contradiction and P versus NP OPEN.

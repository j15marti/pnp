# LSPV-4/483 | Native FLMV hierarchy firewall and two-mode overhead audit

**November 7, 2026, 18:39 PST (America/Los_Angeles) | Route A / resource auditor | PROVED/RESTRICTED logic, PROVED/RESTRICTED arithmetic, COMPUTATIONAL finite checks. P versus NP OPEN.**

**Proof nodes:** [P2-A2] native-model language-general restriction; [P2-A4] alternating-tariff resource envelope. [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. No change to historical R_mix341 grammar, weights or five-role schedules/identities/Route allocation.

## IDEA -> SEARCH -> ITERATE

**Starting hypothesis.** LSPV-2/481 proved an obstruction to a *language-general*, code-inspecting contraction on ordinary multitape TMs but reserved a native-machine model-transfer gap. Maybe the exact FLMV indexed model permits such a generic compiler, or alternating high/low per-step resource costs can rescue it. Investigate a native deterministic hierarchy statement and independently calculate the two-mode resource envelope.

**Four falsifiers registered before searches:** (F1) FLMV does not provide the native constant-overhead simulation needed for direct deterministic self-reference; (F2) a diagonal L could be guaranteed only nondeterministic, making it unusable against a deterministic all-P-language compiler; (F3) the alternating resource envelope is algebraically incorrect or its maximum-rule branches switch at the claimed fixed point; (F4) a SAT-specific solver-intensional transformation escapes the language-general diagonal restriction even if the numerical envelope enters the FLMV region.

**SEARCH, verified primary text:** The original author-hosted Fortnow-Lipton-van Melkebeek-Viglas manuscript, *Time-Space Lower Bounds for Satisfiability*, pp. 4-5, Secs. 2.1-2.2, was inspected as a PDF with page images. Section 2.2's Theorem 2.1 is written for alternating TIME[t], but its proof explicitly says its arbitrary-number-to-fixed-number-of-tapes simulation with O(tau) runtime also holds on **the paper's indexed random-access machine**. The diagonal proof codes the opposite of a target program on arbitrarily long padded descriptions; that deterministic special case is analyzed below. Corollary 5.8, p. 18, specifies the beta(c) tradeoff for NTIME[n] on that machine and does not construct any SAT compiler. Original PDF: https://lance.fortnow.com/papers/files/tst.pdf, PDF pages indexed 3, 4 and 17.

**Continuity:** Both complete root trackers were accessed, [P2-A2], [P2-A4], [P2-A5] and [P1-01]/[P1-03]/[P1-04] identified; current issue #3 was read, along with the governing 2026-11-02 five-role handoff (blob c3889a3e514ddbd747150dcb68607013a3b2d154), AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), and .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f). Read peer LSPV-2/481 (research/agents/lspv-2/2026-11-07_1812_LSPV2_LANGUAGE_GENERAL_HIERARCHY481.md, blob bc3d966b77eb4572b8b609a5c73e4bbd54a5bd8e), LSPV-2/480, LSPV-4/482 (blob 4a6cc74288af8d75a0d29847d1c5c8a929cfded5), LSPV-3/487 and LSPV-1/492; actual GROKPROOF/2026-11-06_2316_PROGRESS.md (a20fb8b3640d7574faf238a4a83a021bb0984808) and Claude research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (79e4d4e7e0e3edff3aba8610852c45534bdde128) were read. Existing previous LSPV-4/481 and /482 resource arithmetic is retained, not claimed as novel.

**Other authenticated source files and unchanged pinned blobs:** konard/p-vs-np TOOLS_AND_METHODOLOGIES.md b3f5ceb025a75360d1956f4bb0ab6ae702761283 and scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93; meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1f; MassimoLauria/cnfgen cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; berkeley-abc/abc README.md 88a9d1a316dd9751acade746de315fd1e6e6c362; openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean 1ced21f44ad49370d1b812e862c03c3a91d7f836; anthropics/formal-math eth/MainResults.lean 1c62a550fa1e4cbec65bb7112f92ad67589afddc. These supply neither the universal same-machine transformation nor proof-system transfer. Public indexed search was available; a separately identifiable Google-branded search interface was unavailable. The new OpenAI/Anthropic October 2026 subexponential k-CNF algorithms are presently external formally supported *claims*, not independently replayed here, and do not imply SAT in P.

## Theorem 483.A: language-general one-shot contraction cannot preserve the native FLMV machine (PROVED/RESTRICTED)

Let DTIME_FLMV[t] denote the languages decided on the *same* deterministic indexed random-access machine of FLMV Section 2.1, with arbitrary fixed finite tapes, with no space restriction. Specialize the proof of FLMV Theorem 2.1 to deterministic target programs. Using its stated O(tau) fixed-tape simulation and padded codes for programs, define a total deterministic diagonal machine D that on input x interprets x as a code for a deterministic target program and, within a clock t(n)=n^2, returns the **opposite** of that program's answer, with a fixed default if the simulation has not finished. D runs in O(n^2) on the very same machine.

If a deterministic machine M decided L(D) in time o(n^2), infinitely many padded descriptions x of the *opposite-program representation of M* would exist. On a sufficiently long such x, the FLMV constant-overhead simulation terminates before D's clock, so D(x)=1-M(x), contradicting correctness. Thus

$$
{\rm DTIME}_{\rm FLMV}[n^2]\not\subseteq {\rm DTIME}_{\rm FLMV}[o(n^2)].
$$

Here the deterministic diagonal specialization and the encoding/padding argument are explicit **derived corollaries** of the primary source's model-specific simulation sketch, not a verbatim separately numbered theorem in FLMV. We do not assert native instruction-by-instruction replay of their simulator. The native-model premise and unbounded-workspace class must be preserved.

Suppose a **language-general** code-aware program transformer C, on *every* correct total deterministic polynomial-time decider A for *any* binary language L, outputs a correct total decider for the same L on the same native machine with the all-input exponent bound

$$
t(C(A))\le \max(11/10,\,3/5+t(A)/2).
$$

Apply C to the native diagonal machine D, whose exponent is 2. The output would have exponent at most 8/5, hence time O(n^(8/5+o(1)))=o(n^2), contradicting the native deterministic hierarchy. Only ONE compiler application is needed; recursive closure and its space accounting are not needed for this no-go.

**Essential scope:** This does **not** exclude a compiler promised *only for correct SAT deciders*, using SAT-specific self-reduction or source semantics. It does not exclude a language-specific nonuniform shortcut; those remain disallowed for the intended proof for separate reasons. It does not prove a new lower bound on SAT. The arbitrary-language promise is a stronger premise than Route A [P2-A2], which is still OPEN. This result strengthens the scope of peer LSPV-2/481 from its standard multitape witness to the original native FLMV model, using text on FLMV PDF pages 4-5. If a claimed A-to-Phi(A) argument uses nothing about SAT beyond a black-box language-decision interface, it must explicitly confront this barrier.

## Theorem 483.B: two-stage periodic resource tariff (PROVED/RESTRICTED)

An independent audit of the /482 constant simultaneous four-parameter tariff considers one *expensive* phase with common exponent surcharge h followed by one *nominal* phase of surcharge zero. Let

$$
f_d(t)=\max\{11/10+d,\,3/5+d+(1/2+d)t\},\quad
g_d(s)=\max\{1/2+d,\,(1/2+d)s\}.
$$

An even-index state is updated by (t,s)->(f_0(f_h(t)),g_0(g_h(s))). For 0<=h<=1/100, both maps are contractions in their arguments, with Lipschitz factor (1/2)(1/2+h)<1. The fixed point is

$$
c_h=(9/5+h)/(3/2-h),\qquad e_h=1/2.
$$

Direct substitution verifies each max-branch at that point. By uniqueness of a fixed point for a contraction, all finite starting exponents converge to (c_h,e_h). The odd-phase fixed state is (2c_h-6/5,1/2+h), which has weakly larger time and space.

The **even-phase FLMV margin** is

$$
G_2(h)=\beta(c_h)-1/2
=\frac{500h^3-2250h^2+14265h-54}
{20(2h-3)(5h+9)^2}.
$$

On [0,1/100] the denominator is negative. Its numerator strictly increases (derivative 1500h^2-4500h+14265>0) and crosses zero exactly once:

$$
h_*=0.0037877499958675667723364212993657767392813976152437\ldots .
$$

Thus, for **every finite initial pair** of exponents, the periodic **upper-envelope equality recurrence** eventually enters the strict forbidden region at an even stage iff 0<=h<h_*. For recurrence inequalities, h<h_* is sufficient, not necessary. At/above h_*, the exact periodic fixed-point trajectory is a counterexample to any universal *envelope* guarantee. It does not preclude an actual better solver.

This is roughly 3.34159 times the /482 common surcharge threshold 0.00113351590406, since the expensive penalty is paid only at alternate stages. The stronger arithmetic allowance cannot excuse any native input/guest conversion cost: two fully specified recursively composable compiler modes and their real same-machine T/S ledgers remain OPEN. There is no claim of an actual SAT algorithm or computable overhead policy.

## Established 3-CNF family / theorem / known shortcut ledger

**Original authenticated family:** Cubic graph Tseitin sources. For connected 3-regular G with H vertices and E=3H/2 edges, assign Boolean x_e to each original edge; vertex v demands XOR_{e incident to v} x_e = b_v. Encode the XOR equation as exactly four proper signed width-3 clauses, one forbidding each wrong-parity local triple. The binary source has 4H clauses, 3H/2 variables, encoded size N=Theta(H log H). XOR of charges is odd iff the connected system is UNSAT; otherwise it has 2^{E-H+1} models. Established Urquhart/Ben-Sasson-Wigderson exponential *ordinary Resolution* proof-size bounds require expanding cubic graphs and their precise lower-bound hypotheses, and do NOT apply to any arbitrary decision algorithm or automatically to the mixed R_mix341 system. Known shortcut: GF(2) Gaussian elimination or global parity summation decides this family efficiently. K4 is the finite control, **not** an asymptotically hard certified instance. Existing resolution/ER/branch/shared and affine shortcuts remain candidate legal upper bounds wherever native rules allow them.

**Remaining transfer:** [P2-A2] must exploit SAT-specific semantics in an all-input effective recursively iterable transformation. [P2-A4] must charge physical source/INDEX/WORK heads, address computation, child construction versus lazy bit generation, q guest executions, repeated resets, cache, materialized ancestor/child buffers, output, computation discovery and failed policies, time, all-phase peak space and verification. [P2-A5] must preserve the same native machine on every iteration. Any 3-CNF lower-bound transfer from Resolution to a stronger calculus requires an actual simulation direction and encoded overhead, not equisatisfiability.

## Independent checks, exact cost and trust boundary

**Python exact Fraction runner** (/mnt/data reproducibility archive): 6,123 assertions, including 101 exact-rational factorization/fixed-point cases, 28 high/low periodic trajectories of 100 periods, 16 original signed K4 sources with 8 SAT/8 UNSAT, and six hostile malformed originals. Exact rational bracket of h_* has width 1/(100*2^120). Host process time about 0.28 s; tracemalloc peak tracked Python allocations 64,834 bytes. These are *host-language measurements*, not native FLMV time/space.

**Independent JavaScript verifier:** 666 checks on 501 different h factorization points, 36 trajectories, 16 signed K4 original 3-CNF inputs and six malformed controls; zero failures. The complete executable was published at experiments/arc/lspv4_483_periodic_tariff_independent.js, and the exact published file was read back. No arbitrary input CNF-SAT decider, native compiler, Lean replay, R_mix341 certificate, or literal machine trace was constructed.

**Resource accounting:** The two recurrence theorems charge abstract exponents rather than runtime steps; no physical compiler costs are bounded by these assertions. The native diagonal impossibility needs only full time, hence does not pretend to bound its work space. For implemented upper bounds, construction, machine-code interpretation, source parsing, INDEX contents/heads, guest guest-work high-water, conversion, output, cache/retrieval/recomputation, buffer overlap, repeated failed searches, certificate evidence bits, checking and final label costs remain mandatory. No logical proof-inference nodes are constructed and no change to fixed proof weights is made. Neither finite tests nor the restricted hierarchy corollary prove P!=NP.

## Publication and handoff

Report (this file), independent JS verifier, compact raw result JSON and five-role handoff are role-owned and publicly readable. Full Python exact-rational script and detailed cases are available as a conversation reproducibility archive, not misrepresented as native FLMV execution. No root main.tex modification absent safe complete-file authentication. Update only [P2-A2] and [P2-A4] with restricted evidence if the current whole trackers' SHA/readback guard succeeds; otherwise record the blocker. Post affected node IDs to coordination issue #3.

**Actual advance:** FLMV-native language-general time hierarchy firewall and an exact alternating-stage resource tolerance criterion. **Remaining gap:** a *SAT-specific*, solver-intensional, exponent-oblivious, all-input, same-machine, recursively iterable contraction, and separately the historical fixed R_mix341 mixed lower-bound/B3 transfers. **P versus NP OPEN.**

# LSPV-2/482 | Transparent dual-padding elision: one-step success and recursive-closure failure
**November 7, 2026, 19:18 PST | LSPV-2 | Route A primary | PROVED/RESTRICTED and COMPUTATIONAL. P versus NP OPEN.**

**Proof-chain nodes:** [P2-A2] universal all-input code-aware SAT contraction OPEN, [P2-A4] charged native resources OPEN, [P2-A5] recursive closure OPEN. [P1-01], [P1-03], [P1-04], and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

## IDEA -> SEARCH -> ITERATE, with falsifiers
Initial proposal: extend the original-input trace-first delay-padding objection into a black-box prefix bound. Falsifiers F1 prior work already handles delay, F2 code inspection can remove synthetic padding, F3 a solver can use smaller queries, F4 finite prefix budgets cannot be chosen independently of unknown exponents. Search established F1 from LSPV-2/470 and F2/F3 as real exceptions; LSPV-2/478, /479, /480, /481 and peer LSPV-4/483 supply overlapping barriers. We do not rebrand these as new.

Revised idea: explicitly construct a **positive code-intensional** restricted one-step compiler stripping only authenticated syntactic time and space padding. Falsifiers R1 stripping might change SAT/UNSAT/malformed, R2 removing time padding might automatically suffice for space, R3 one-step success might imply recursive applicability. R1 is disproved by operational equivalence; R2 and R3 are false, with exact counterexamples.

## Theorem 482.1: exact dual-padding threshold (PROVED/RESTRICTED)
Assume a fixed, uniform, total, all-binary-input SAT/UNSAT/malformed polynomial-time decider A with actual worst-case exponents t>11/10 and s>1/2, on ONE fixed machine, attained up to subpolynomial factors. The existence of A is hypothetical. An authenticated source-program grammar contains only an explicitly typed wrapper PAD(k,h,A), k,h fixed nonnegative integers, whose exact semantics on N-bit input x is: densely write N^h scratch cells, release them, perform N^k real input-blind clock steps, then invoke unchanged A(x) and return its classification. There is NO semantic oracle recognizing arbitrary dead code. A syntax-directed compiler Strip(PAD(k,h,A))=A uses O(code length) offline transformation work, not a cost-free per-input oracle.

The wrapper has worst-case time and writable peak-space exponents

$$
T=\max\{t,k,h\},\qquad S=\max\{s,h\}.
$$

Dense scratch construction and every clock step are charged; scratch is sequential with the core and does not change its classification. The original parser, source/index reads, output, and core computation remain charged to A. The controller has O(log N) scratch excluding its dense payload. The time and space maxima reflect sequential phases, not the sum of asymptotic exponents.

For t>11/10 and s>1/2, the Route A one-step inequalities

$$
t\leq\max\left(\frac{11}{10},\frac35+\frac T2\right),\qquad
s\leq\max\left(\frac12,\frac S2\right)
$$

hold **if and only if**

$$
\boxed{T\geq2t-\frac65\quad\land\quad S\geq2s.}
$$

Proof: since both output exponents exceed the fixed constant branches, each inequality has only its linear branch available; rearrange both. Exact syntax removal preserves A(x) for EVERY binary x, including malformed inputs. QED within the source grammar and the conditional base-program premise. No arbitrary-machine SAT hardness follows.

Example: t=3, s=2, k=5, h=4 gives T=5, S=4; stripped t=3,s=2 satisfies bounds 3<=3.1 and 2<=2. With k=5,h=3, time passes but space fails. With k=4,h=4, space passes but time fails. The programmer of Strip need not extract t,s from source code; the inequality is an external proof obligation for this specified subclass, not a universal success guarantee.

## Theorem 482.2: bare-core obstruction (PROVED/RESTRICTED)
The stripping compiler is NOT recursively iterable on every polynomial SAT decider: it maps a wrapped source to bare A, then cannot remove more typed wrapper nodes. Returning A unchanged at the next step violates the target if its exact core time exponent t>6/5 or space exponent s>1/2: f(t)<t and g(s)<s. Leaving Strip undefined instead violates effective recursive applicability. Any compiler confined to eliminating these typed syntactic padding wrappers has the same arbitrary-core floor. A stronger compiler that actually transforms the core is not excluded. In particular this neither closes [P2-A2] nor [P2-A5], and it does not establish P versus NP.

## Independent implementation and finite falsifiers
Code: experiments/arc/lspv2_482_clock_strip.py and independently written experiments/arc/lspv2_482_independent.cjs. Raw: results/raw/arc/2026-11-07_1918_LSPV2_482_RESULTS.json. Python used exact Fraction rational comparisons, verified 25,658 checks, physically filled finite bytearray scratch and executed finite clocks for signed K4 3-CNFs. Independent Node used integer quarter-unit exponent arithmetic rather than importing Python and passed 25,643 checks. Both independently constructed all 16 charge patterns on original six-edge K4 strict proper 3CNF: 8 SAT and 8 UNSAT. Five malformed controls rejected in each implementation. This is a finite brute-force test for a *fixed six-variable family*, not a general polynomial SAT algorithm or native FLMV execution. No historical R_mix341 checker was executed or modified.

**Family, theorem, encoding and known shortcuts ledger.** Odd-charge Tseitin formulas on cubic expander graphs give 4H original strict-ternary clauses on 3H/2 edge variables. Ben-Sasson--Wigderson prove exponential ordinary Resolution hardness under expansion assumptions, not all-algorithm hardness. GF(2) elimination and the project's authenticated parity-defect DP provide explicit upper controls; code-padding removal here is a PROGRAM-class control, not a proof of a new hard 3-CNF family. Native rule simulation and lower-bound preservation remain separate obligations.

## Actual corpus and reference checks
Read full proof1.txt (18,553 characters, Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and full proof2.txt (301,483 characters, blob 70b3f85c70cdfd553cda733f44c5c201d20b5903), governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md blob c3889a3e514ddbd747150dcb68607013a3b2d154, current coordination issue #3 including LSPV-2/481B and peer LSPV-4/483, AGENTS.md blob 19656af102604d5f0a721d548cf2e4e72a063561, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef and .codex/skills/pnp-research/SKILL.md blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f. Reused LSPV-2/470 (b1567c0427155e68fe82ffa8fb45a6fcfb94fe8b), /478, /479, /481 (bc3d966b77eb4572b8b609a5c73e4bbd54a5bd8e); LSPV-4/477 and /483 (f7821a3d28cbc2c02dd8b7a4bc42b7bd7fd8f722), GROKPROOF/2026-11-08_0118_PROGRESS.md (4fbcd3a1725be91c74d15f0c7fce7367ba40c82d) and research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (b7150bb9ed964affd5fb90ecd24b0aa35d600bf9).

Primary public web search: Fortnow, Lipton, van Melkebeek, Viglas (JACM 2005; DOI 10.1145/1101821.1101822) with the original indexed random-access machine lower bound; Ben-Sasson and Wigderson (JACM 2001) for ordinary Resolution hard-family control. No new PDF-page analysis or original FLMV native replay was performed; separate Google-branded search was unavailable, ordinary public search was available. Required current external sources inspected: konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95), scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2): finite-machine P subset NP scope; blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93): uniform plan acquisition missing; MassimoLauria/cnfgen cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); berkeley-abc/abc README.md (88a9d1a316dd9751acade746de315fd1e6e6c362); openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae); anthropics/formal-math eth/MainResults.lean (1c62a550fa1e4cbec65bb7112f92ad67589afddc, declarations not their full proof). None gives the universal compiler.

**Publication safeguard:** TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex returned zero readable characters at nonempty blob 68188a24badda635a5983fda1c381cdb694fd497, so it was not changed. Five role IDs, task schedules, enabled states, two Route A / three Route B allocation, historical R_mix341 grammar and fixed weights remain unchanged.

**Actual advance:** exact two-resource restricted code-class threshold plus explicit recursive core obstruction. **Verification:** independently tested symbolic arithmetic and finite K4 both-label/malformed controls. **Remaining gap:** native same-machine all-input, solver-dependent, exponent-oblivious, recursively iterable transformation for arbitrary-core deciders; every real phase charged. **P versus NP OPEN.**

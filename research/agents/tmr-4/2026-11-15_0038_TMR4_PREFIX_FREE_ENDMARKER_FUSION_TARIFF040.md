# TMR-4/040 | ENDMARKER074: prefix-free positive-source ingress and terminal-fusion tariff

**2026-11-15 00:38 PST | PNP Cost-Sound Abstraction | America/Los_Angeles**

**Status:** PROVED/RESTRICTED for the exact read-only local-head deterministic multitape model and strict 3-CNF encoding below; independent mathematical review OPEN. Executed finite V8 audit COMPUTATIONAL. No superpolynomial SAT lower bound. **P versus NP OPEN.**

## 1. One candidate and four falsifiers fixed before source and literature review

**Candidate:** Strengthen TMR-3/039's genuine opposite-SAT last-bit ingress result by using the compulsory *right endmarker*, rather than merely the final source bit, on every accepted valid source in a strict prefix-free grammar. Prove a complete actual-machine step simulation for a source-aware ghost frontier, compute the precise seven-column tariff and two-weight cone, and explicitly test whether reading the endmarker and accepting can occur in the same paid transition.

Falsifiers: (F1) a strict extension of the positive source is still accepted as a valid 3-CNF or has the same YES label; (F2) the input interface has uncharged lookahead, direct length queries, random-access jumps, initially prepositioned heads, or source-length advice; (F3) the source/endmarker scan and halt are double-charged despite a legal one-transition fusion; (F4) the new linear obstruction is improperly promoted to a superpolynomial lower bound, or a hardwired per-length program is confused with one uniform algorithm.

## 2. Exact machine system and source set

Use the *same* source parser as TMR-3/039: unary width 1^b0, unary clause count 1^M0, and exactly 3M fixed-width signed literal records, each of b variable-ID bits and one polarity bit. Each clause has three different nonzero IDs. **No trailing bits are legal.** Therefore, for every valid source bitstring x, its strict extension x0 is invalid, hence a NO instance of the total Boolean SAT language under the specified malformed-input convention. The bitstring occupies cells 0,...,N-1 and the right endmarker occupies cell N.

A is any one fixed finite total deterministic correct SAT machine: one or a fixed number of left-initialized, locally moving read-only input heads, fixed finite alphabet, any fixed number of ordinary writable work tapes, arbitrary control, cache, rereads, sharing, recomputation and work space. In each paid transition, the scanned input symbols are read and each head moves by at most one cell; scanning is before motion. Each physical transition costs exactly one. No simulated logical inference is presumed a unit transition.

Let S be the explicitly polynomial-recognizable **SAT** family F_m^+ from TMR-3/039, for all m>=3: a proper 3-CNF encoding of a cubic prism's H=2m four-clause XOR blocks, with the last positive literal flipped. The complete odd-charge source F_m^- is UNSAT, while all-zero satisfies F_m^+. Their source encodings differ in one final bit. Let

\[
b_m=\lceil\log_2(3m+1)\rceil,\qquad
N_m=(24m+1)(b_m+1)+8m+1.
\]

All original input, machine program/control, head positions, work tapes, writable symbols, result, paid history and the immutable source remain in the concrete state. Extend this by the **ghost ledger** r(C), the maximum original input position actually inspected on the current run, including cell N's endmarker and capped at N, with initial r=-1. This observer does not give the executing program access to a previously unobserved symbol.

## 3. New theorem ENDMARKER074-A: all-positive-input physical ingress

**Theorem.** Let x be *any* valid SAT-YES bitstring of length N in the declared prefix-free grammar. For every fixed correct total deterministic locally moving SAT decider A, every accepting execution on x must physically inspect the right endmarker at input position N, and

\[
\boxed{T_A(x)\ge N+1.}
\]

**Proof.** The strict extension x0 is invalid and has Boolean answer NO. Until some input head inspects cell N, the two source tapes provide identical scanned symbols, since cells 0 through N-1 are equal. Determinism and initially identical blank work tapes, control and head positions force the two runs to have exactly the same transition history up to that first inspection, including any number of rereads, control changes and cache operations. If A accepted x before an input head inspected cell N, it would also accept x0, contradicting correctness on malformed inputs. Thus an input head must inspect position N. A locally moving head starting at position zero cannot scan position N before transition N+1, when scanning precedes motion. QED.

This is a *general positive-input theorem* for the chosen strict encoding, not merely the special opposite-label prism pair. It exceeds TMR-3/039's all-machine N-floor by one transition on each SAT member F_m^+. No corresponding generic endmarker conclusion is claimed for the UNSAT member: rejecting it and rejecting a malformed extension may have the same Boolean label.

## 4. Source-aware reduced product and complete one-step simulation

For a concrete state C on immutable source F, define s(F)=1 if F belongs to authenticated S, otherwise zero. Let h(C) indicate halt. The ghost reduced-product components, in the directive's ordered seven-column convention, are

\[
p(C)=(0,0,0,0,0,\ s(F)\max(0,N-r(C)),\ s(F){\bf1}[\neg h(C)]).
\]

On nonmembers these components are zero, so no false constraint is imposed on other inputs. Membership s(F) is a **mathematical observer** computed from the original source, not a free symbol available to A. S has a direct polynomial grammar recognizer, so this is not a hidden SAT oracle. All standard machine steps cost one; the authentic zero-cost SCC quotient and directed cl0 are both the identity.

The abstraction retains the exact immutable source-membership tag, length N, inspected frontier r, halt flag and output label, while it existentially forgets the complete machine control, tapes and cache. The concrete/abstract relation is this projection. Every actual paid transition has a one-edge abstract simulation of cost **exactly one**: with fixed left-started locally moving input heads, the maximum inspected position increases by at most one, irrespective of concurrent work/output operations or the number of other heads. An input reread, arbitrary work operation, failed test, compaction, caching, learning or recomputation has interface discharge zero unless it actually first scans the next frontier cell.

At a completed goal on a source F in S, total correctness plus ENDMARKER074-A forces r>=N, so the interface component is zero; the machine component is zero by halt. Nonmembers have zero potential by definition. Thus *all accepting and rejecting completed goals on all input strings* have p=0 in the relation to globally correct A. Excluding a purported accepting state with s(F)=1 and r<N is justified by the proved indistinguishability contradiction, not an ad hoc CEGAR deletion. For a machine that is not globally correct this terminal condition need not hold.

## 5. Exact physical transition tariff and LP

After collapsing duplicate zero rows, the full relevant seven-column price matrix contains the following authentic representative discharge pairs (interface, machine):

| Physical rule class | Price | Discharge |
| --- | ---: | ---: |
| Reread, cache, work, syntax check, output, recomputation | 1 | (0,0) |
| First inspection of one new frontier cell | 1 | (1,0) |
| Halt after endmarker was previously inspected | 1 | (0,1) |
| **First inspection of endmarker and accept in the same step** | 1 | **(1,1)** |
| Any local step on a source outside S | 1 | (0,0) |

All other five obstruction coordinates are zero **only for this ingress-only projection**. No unrestricted CNF/fusion obstructions are claimed absent. The authentic fused final row is realizable: for any **fixed** m, one finite program A_m compares the source online against the hardcoded SAT-YES F_m^+; on its exact match it accepts on scanning the endmarker, and on a mismatch it resets its head and uses exhaustive general SAT search with complete malformed-input parsing. This is one correct total program across all binary inputs for that *fixed* m, not a nonuniform SAT algorithm for all lengths. Its matching path has the literal transition with discharge (1,1) at price one.

The complete nonnegative uniform two-coordinate tariff cone for these classes is therefore

\[
\boxed{\lambda_{\rm interface}\ge0,\quad
\lambda_{\rm machine}\ge0,\quad
\lambda_{\rm interface}+\lambda_{\rm machine}\le1.}
\]

Necessity follows from the genuine fused row and sufficiency follows because both coordinates decrease by at most one on any actual step. In the seven-column notation, the exact integer witness is

\[
\boxed{\lambda=(0,0,0,0,0,1,0)}.
\]

It gives \(\Phi(C_0)=N_m+1\) and \(\Phi(\mathrm{goal})=0\), hence by all-step telescoping \(T_A(F_m^+)\ge N_m+1\). For the linear objective \((N_m+1)\lambda_{\rm interface}+\lambda_{\rm machine}\), the dual has the exact certificate \(y=N_m+1\) on the fused-row constraint, verifying the optimum \(N_m+1\). Assigning both coordinates unit weight is **FAIL**: the one-step fused transition would discharge two units of tariff at price one. The machine flag does not provide an independent extra transition.

This lower bound is exact for a **fixed** positive source if one minimizes over all possible correct total machines, because the hardcoded comparator with brute-force fallback accepts that source in exactly N+1 steps. That per-source optimizer does not share a uniform finite program as m grows and is **not** a P versus NP argument. TMR-3's earlier *single fixed* polynomial family recognizer independently shows this explicit family cannot support a superpolynomial bound valid for every correct A.

The general program may query and reuse the original input adaptively; these operations remain legal. A new random-access or prepositioned-head model requires a new transfer and may falsify the geometric inequality. A genuine zero-cost oracle or extension-algebra operation must remain as a MAY edge in a broader abstraction, not be CEGAR-pruned.

## 6. Reproduction and hostile-control results

Exactly executed native V8 function serialized into the published standalone JS source:

- 10 prism pairs, m=3,...,12, input lengths 390 through 2120 bits.
- Exact proper 3-CNF parser, SAT all-zero witnesses, complete UNSAT assignment enumeration for m=3,4,5, and valid/invalid strict-extension controls.
- **23,516 complete finite abstract step rows**, containing first reads, work/cache/rereads, post-endmarker halts and final read-plus-accept fusion.
- **123,088 assertions**, zero failures; rational-grid checks for denominators 1,...,16 independently recover exactly the simplex constraint above.
- Finite controls are COMPUTATIONAL; the all-length positive-input theorem is a separate symbolic proof.

Published evidence:
- executable: experiments/tmr/tmr4_endmarker074.js
- exact raw JSON: results/raw/tmr/2026-11-15_0038_TMR4_ENDMARKER074_V8_RAW.json
- complete finite seven-column CSV: results/raw/tmr/2026-11-15_0038_TMR4_ENDMARKER074_TARIFF_ROWS.csv

The executed V8 function is byte-identical, by JS function serialization, to the function embedded in the published script. The standalone Node wrapper has not separately been executed. The 1,179,764-character CSV exceeds the normal GitHub file-content read window; its **complete** blob was recovered by Git blob SHA ea087e64a04ff9ea9825571f75bd0f9b9c4fc701 and checked for length, header, terminal rows and last newline. No independent native TM compiler has been executed.

**Hostile mechanisms:** affine/Gaussian, Horn and dual-Horn, 2-SAT, separator DP, autarky, equality/union-find, extension variables, compact circuits, preprocessing, learned lemmas, shared DAGs and alternate proof systems do not increase this *linear* input-interface lower bound, nor are they ruled out from completing the SAT decision in polynomial time. The all-zero witness and parity-source recognizer are real cheap controls. Any semantic cofactor, interpolation or proof-length tariff charged in addition would require a new fusion-safe joint row proof. Invalid trailing-byte acceptance, free endmarker lookahead and one-step nonlocal jumps are explicit model-changing falsifiers.

## 7. Corpus, sources, comparison and gaps

Read FIRST the approved fusion directive (SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6), then the 2026-11-13 replacement, root proof1 (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), full proof2 (SHA 930c5eeddafce656717f28055a7a9a755f44737c), full main.tex (SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34), issue #3 through TMR-3/039, AGENTS.md, CODEX.md, project skill, and five current handoffs. The two large roots were retrieved by authentic full Git blobs because ordinary contents fetch can return an empty body. Original lead/0029 Lipschitz audit, TMR-4/035/037/039 and code, TMR-3/038/039 and original JS source, TMR-1/037-039, TMR-2/039, TMR-5/035 and original hostile evidence informed the audit. Historical /341 remains FAIL as a full UNSAT authority and /386 remains RESTRICTED. Root reports and sources were not modified.

Methodological primary literature: P. Cousot and R. Cousot, "Abstract Interpretation", POPL 1977 pp.238-252, https://doi.org/10.1145/512950.512973; S. Cook and R. Reckhow, "The Relative Efficiency of Propositional Proof Systems", Journal of Symbolic Logic 44(1), 1979 pp.36-50, https://doi.org/10.2307/2273702. No new lower-bound exponent is imported from either paper. TMR-3/039 is the direct project predecessor. Full preflight script and native physical-machine compiler were not executed in this connector-only run; the original repository content and native V8 arithmetic/grammar tests were read or executed as stated.

**What is genuinely new:** TMR-3/039 compelled the **last data bit** on both opposite-label sources, yielding T>=N. This run proves the extra endmarker inspection for **every valid SAT-positive input of a strict grammar**, models it as a genuine all-machine one-step abstraction, and proves the exact fused terminal/input tariff cone. It neither repairs historical authority failures nor adds a superpolynomial potential. The unchanged blockers remain an intrinsically nonaffine fusion-safe multiscale initial gap and a fully general same-system computational obstruction beyond input ingress.

**Peer requests:** TMR-3 independently audit scanning-before-move, malformed suffix semantics and left-started multiple heads; TMR-5 build the hardcoded correct total comparator and attack fused-halt reachability; TMR-1 check the exact abstract source family and all-machine quantifiers. **Next TMR-4 target:** combine this physical-ingress observer with a *genuine* source-complete deterministic constructor's paid control/tape/output transitions, without assuming preloaded proof scripts and without adding output, branch or inference charges twice.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root proof1/proof2/main.tex edit is justified. No scheduled tasks changed. **P versus NP remains OPEN.**

END_OF_REPORT::TMR4::040::2026-11-15_0038_PST

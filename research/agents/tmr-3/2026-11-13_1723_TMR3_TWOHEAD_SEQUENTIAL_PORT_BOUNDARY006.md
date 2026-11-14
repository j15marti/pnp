# TMR-3/006: Two local read-only input heads defeat a head-count-independent crossing product

Date: 2026-11-13 17:23 PST (America/Los_Angeles). Repository: j15marti/pnp, main.
Status: NEW CANDIDATE pending independent TMR-5 mathematical review; finite tests COMPUTATIONAL. P versus NP and the unrestricted all-exponent SAT lower bound OPEN.

## Exact theorem candidate TH6

Let E_n(a,b) be the original strict proper 3-CNF equality encoding from TMR-2/001 and original TMR-3/002, for n>=1 and a,b in {0,1}^n. Its first n four-clause blocks force x_i=a_i, the second n blocks force x_i=b_i; hence SAT iff a=b. For w=max(1,ceil(log_2(5n))), header h=13n+2 and block width g=12(w+1), the actual binary source length is L=h+2ng=Theta(n log(n+1)).

**Claim:** One fixed finite, total, correct, deterministic all-input 3-SAT machine D_2 with TWO independently moving read-only heads on the same binary source tape, ordinary sequential work tapes, no INDEX and no free copied source, has on every E_n(a,b):

$$
T_{D_2}(E_n(a,b))=O(L),\qquad S_{D_2}(E_n(a,b))=O(\log(L+2)).
$$

All head movements, work counters, indexes, parser buffers, output and fallback are charged. The extra head is a declared modification of the input interface, not part of TMR-3/002's ONE-head model.

## Constructive proof and source binding

Head H1 authenticates the unary 1^(5n) 0 1^(8n) 0 header, leaving H1 at h. Head H2 starts at cell 0. Compute d=h+ng using O(log L) work cells and O(log^2 L) bit operations. Advance H2 by exactly d individually charged adjacent movements using a least-significant-bit-first binary countdown. The decrement from t to t-1, including head return, costs O(1+nu_2(t)); summing t=1..d gives O(d). Reject family recognition if the endmarker appears early.

Now H1 is at h, H2 at h+ng. Advance both heads together through n pairs of blocks. For i=0..n-1, verify all four original signed 3-literal clauses at each head. First variable ID is i, auxiliary IDs are z_1=n+2i on H1 and z_2=3n+2i on H2, with all four ordered u,v choices, within-block identical sign and exact binary literal fields. Scan expected identifiers on work tapes at O(w) time per record, resetting their physical heads; counters, field state and mismatch flag take O(log L) writable cells. Compare the two bank signs once per i. Every actual bit is authenticated: header and first bank by H1, second bank plus right endmarker by H2. Acceptance is permitted ONLY on exact whole-source family match and iff every pair sign agrees. Nonmembers, malformed sources and non-family formulas enter a fully charged, total, correct exhaustive general SAT parser/decider; no fast nonfamily runtime is asserted.

The total number of individual source-head moves on a family input is exactly

$$
h+(h+ng)+2ng=2h+3ng\le 2L.
$$

Binary source/header counting has O(L) amortized transitions; literal-field verification is O(nw)=O(L); positioning arithmetic is O(log^2 L)=O(L). All simultaneous live writable cells total O(log L), including binary counters, expected IDs, head-position downcounter and output. Therefore the same actual machine has the claimed joint upper bounds.

Consequently on every family member, including all SAT diagonals,

$$
T_{D_2}(F)(S_{D_2}(F)+1)=O(L\log L)=o(Ln).
$$

**Falsified extrapolation:** The T(S+1)=Omega(Ln) lower bound from TMR-3/002 cannot be generalized without modification to arbitrary fixed numbers of sequential input heads. TMR-3/002 explicitly requires ONE physical two-way source head, so its reviewed restricted theorem is **NOT refuted**. Adding a second local source head alters crossing-splice transcripts and permits simultaneous observation of separated banks. A standard one-input-head multitape machine can copy input to writable tape, but that consumes Theta(L) writable cells and does not preserve our O(log L) space.

## Independent TMR-1/005 review and original literature

Inspected the actual TMR-1/005 mathematical report and complete original JavaScript source. Its hybrid erasing-INDEX argument is mathematically consistent at its expressly different indexed-input model: exactly 2n indexed jumps, writing O(log L) address bits each, in addition to O(L) normal adjacent scan moves and O(nw) field work, yield O(L) same-input family time and O(log L) writable space. This is a favorable independent **symbolic** review, not instruction-level replay of its code.

Verified Section 2.1, physical page 4, of Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, Journal of the ACM 52(6), 2005, original author PDF https://lance.fortnow.com/papers/files/tst.pdf . Its INDEX tape is erased after a jump, but ordinary non-index input-head movement is not forbidden. The paper's polynomial time-space exclusion is conditional on a simultaneous small-space exponent and does NOT cover every polynomial workspace or every runtime exponent. TMR-5/004's slower O(L log L) erasing-index implementation remains a valid nonoptimal upper, not a lower bound.

Read original historical TMR-3/002 (research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md) and TMR-3/003 (batch frontier) with their precise one-head assumptions, as well as all newest TMR handoffs, AGENTS.md, CODEX.md, pnp-research skill, the 12:49 PST directive, current issue #3, recovered root main.tex and full proof1/proof2 trackers. Earlier LSPV crossing evidence is used only at reported restricted model scope, not claimed as an unrestricted transfer.

## Actually executed controls

Native OS Node v22.16.0 executed the new standalone source and wrote an immutable JSON result. The source was independently authored, not a wrapper around TMR-1/005 or TMR-5/004. It performs local read-head movements and field checks, with NO index-port operations:

- 1,428 real original encoded E_n(a,b) cases, all 4^n pairs for n=1..5 and eight seeded trials for n=8,16,32,64,128,256,512,1024. SAT 126, UNSAT 1,302.
- 9,996 deliberately malformed or structurally modified original sources rejected by family recognizer, including headers, identifiers, inconsistent signs, truncation and suffix padding.
- Twenty small-n original-CNF brute force classifications checked separately.
- 9,619,896 counted local head movements, 6,315,408 source read events, 22,692 comparisons, largest L=357,378, maximum movement/L 1.567568. Zero failed assertions.

Executed exact source: experiments/tmr/tmr3_twohead_sequential_006.cjs.
Immutable raw: results/raw/tmr/2026-11-13_1723_TMR3_TWOHEAD_SEQUENTIAL006_RAW.json.

The finite emulator uses JavaScript strings and Number arithmetic; it does NOT instruction-simulate the full physical multitape machine, its fallback or the true work-tape head travel. The mathematical O(L) processing bound is justified separately by explicit amortized counters and O(w)-per-record work. The emulator's workProxy is only a conservative local-source metric, not a certified machine instruction count. No native full SAT fallback, proof assistant, report validator or LaTeX compilation was executed. Horn, 2-SAT, XOR/Gaussian elimination, bounded treewidth, products, renaming, padding, auxiliary extensions and caching are not lower-bound claims and were not separately benchmarked.

## Scope, quantifiers and next review

This is one fixed two-head machine for an easily authenticated family, not a polynomial general SAT algorithm. The team target remains for every correct fixed single-model A, k>=1, C>0 and L0, a valid F of size >=L0 with T_A(F)>C(|F|+1)^k. Neither the new upper bound nor any cited restricted time-space result establishes that. Same-machine S<=O(T) does not close the missing all-exponent implication.

TMR-5 should independently audit the second-head initial seek, the endmarker, all clause bits, the fully charged O(L) binary countdown and absence of any hidden INDEX use. TMR-1 should keep input-head multiplicity explicit. TMR-4 should record both head positions in full-configuration abstractions. All unrestricted computational-bottleneck arrows remain OPEN.

TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex unchanged for TMR-5 whole-document ownership. No schedules/tasks created, altered or revived.

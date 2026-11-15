# TMR-3/044: Same-output early/late fusion tariffs and a physical head-return transfer firewall

**2026-11-15 05:31 PST (America/Los_Angeles).** TMR-3, PNP Time-Space Tradeoffs. Governing user-approved directive: research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6.

**Status:** PROVED/RESTRICTED exact symbolic theorems in stated source-authenticated physical services; independent mathematical review OPEN. Finite native V8 test COMPUTATIONAL. No unrestricted SAT-machine inference. P versus NP OPEN.

## 1. Candidate and falsifiers, fixed before targeted literature/corpus work

**Candidate.** The actual physical head-return tariff calibrated in TMR-1/044 is not a lower bound for every finite-control machine producing the identical final tape layout. An alternative machine may write the final header and all output markers early, stream the remaining records, inspect the original EOF and halt in linear time without returning its work head. More strongly, two programs with the same starting tapes, identical final physical outputs and identical actual runtime can have different local tariff cones because the output-marker writes are fused with different physical steps.

Four falsifiers: (F1) the alternative writes two cells on one tape, jumps a head, uses length-dependent advice or omits EOF; (F2) it omits, aliases or duplicates one mandatory gate or marker identity; (F3) its final output differs from TMR-1/044 in any required physical W or output cell; (F4) a potential calibrated for EARLY is incorrectly claimed all-program sound despite the genuinely legal LATE EOF+output+HALT step. F1-F3 are disproved by the explicit transition tables and trace audit. F4 is confirmed as an exact failed transfer.

## 2. Source recovery, provenance and prior-work firewall

Read first the fusion directive, then the TMR replacement directive; both root trackers, root main.tex, issue #3, AGENTS.md, CODEX.md, repository skill, all five current TMR handoffs, and materially relevant original TMR-1/044, TMR-3/043, TMR-5/040 and TMR-4/044 reports, their executed code and tariff matrices, TMR-2/043's compact NAE family, and historical LEAD-0029 Lipschitz audit. Root proof1.txt has SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 characters). The authentic full proof2.txt blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters) and root main.tex blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 characters) were recovered directly from Git blobs, because oversized ordinary content responses are empty. No empty replacement was inferred.

The TMR-1/044 theorem for its **one prescribed program** gives precisely 2n+2 native transitions and a matching fixed-program potential. TMR-3/043 and TMR-5/040 already established nonterminal batch activation and simultaneous marker writes. The new contribution is a **different pair of fixed genuine machines with the same final physical tape contents**, an exact early/late local-tariff collision, a matched complete final-state-service minimum, and an independently proved geometric lower bound for the stronger ordered-activation service. No prior theorem is said to be false in its original model.

Primary machine-model literature: F. C. Hennie and R. E. Stearns, "Two-Tape Simulation of Multitape Turing Machines," Journal of the ACM 13(4), 533-546 (1966), DOI https://doi.org/10.1145/321356.321362; J. Hartmanis and R. E. Stearns, "On the Computational Complexity of Algorithms," Transactions of the AMS 117, 285-306 (1965), DOI https://doi.org/10.1090/S0002-9947-1965-0170805-7. These are contextual primary sources for finite-tape time accounting, **not** sources of the elementary new construction.

## 3. Complete concrete model and two fixed physical programs

Fix any **m >= 1** before compiling a program. Input is one immutable read-only tape with symbols 1^n#, n >= 2, scanned by exactly one initial-left head, with # the authentic right endmarker in physical cell n. One writable staging tape W, initially blank, has head initially at cell 0 and alphabet {blank,0,1,g}. There are m **distinct** initially blank one-head writable marker output tapes O_1,...,O_m, each at cell 0. The complete configuration includes the actual program/control, input, source and output tape contents, every tape-head position, the paid identity of each physical g record, the input-read history and all output/terminal obligations. All physical transitions read the scanned finite alphabet tuple, rewrite at most one cell **per distinct tape**, and move each head by at most one cell. One genuine physical step costs 1, independent of simultaneous actions on separate tapes. The finite control is independent of n. There are no authentic cost-zero transitions. Zero-cost closure is identity, all zero SCCs singleton. Optional VIEW metadata must leave the vector invariant.

The **FINAL-STATE SERVICE** accepts completion exactly when the original # has actually been inspected, W[0]=1, W[j]=g for 1<=j<=n-1 with each identity minted once, O_i[0]=@ for every i, and true HALT. Output records are literal physical cells, not an exponentially unfolded semantic DAG. No requirement of an earlier 0 header, after-staging activation, or distinct HALT instruction is imposed by this final-state service. The full machine has no external command stream, oracle, free source copy, random access, or input-size-specific control. These are unary service machines, **not SAT deciders**. Malformed inputs use a rejecting-sink extension and are outside the successful-source theorem; unexpected 1/# patterns are not treated as a valid SAT certificate.

The successful-promise physical transition inventory is:

| Rule | Exact concrete precondition | EARLY program microstep | LATE program microstep | Cost |
|---|---|---|---|---:|
| INIT | START; scanned first source 1 and blank W[0] | inspect 1, write W[0]=1 and every separate O_i[0]=@, move input and W right, enter SECOND | inspect 1, write W[0]=1, move input and W right, enter SECOND | 1 |
| GATE | SECOND or STREAM; source 1 and W head on blank cell | inspect 1, write one distinct g at current W cell, move both heads right, enter STREAM | identical | 1 |
| EOF_HALT | STREAM; source head actually scans # | inspect #, HALT immediately | inspect #, simultaneously write @ to each of the m distinct O_i cells and HALT | 1 |

SECOND enforces at least a second 1 before authentic successful EOF. Both machines use one header write, n-1 distinct source-derived gate records, m physically distinct marker writes and one real terminal entry. Source EOF and successful HALT are genuine, not proof-authority shortcuts. Both programs finish with **identical complete output tape contents**, not merely semantically equivalent representations. Their input and W final heads are at index n; each marker head remains at 0. On their successful paths, each authentic source cell from 0 through n is inspected exactly once. The original peer M_STAGE_OUTPUT_m shares the final output layout, but additionally enforces ordered staging, activation at the left header after all gates, and a separate HALT.

## 4. Reduced-product component and exact tariff matrices

For both programs define q(C) as the number of missing literal g records at W[1..n-1]; u(C) as the number of **original source positions 0..n not yet inspected**; o(C) as the number of marker cells O_i[0] not equal @; h(C)=1 until actual HALT, otherwise zero. The authenticated fixed source is known to the theorem, not to the machine as free numerical advice. The exact seven-component vector is

$$
p(C)=(0,0,0,0,q(C),u(C)+o(C),h(C)).
$$

Thus the Gamma coordinate counts physical record obligations and the interface coordinate combines **read** and **output-marker** obligations, explicitly preserving the two separate counts in the concrete state. No charge is assigned to raw graph-activation connectivity or semantic rank. Initially

$$
p(C_0)=(0,0,0,0,n-1,n+1+m,1),
$$

and completed goals have the zero vector. With active component order (Gamma, Interface, Machine), the genuine signed discharge matrices are

| EARLY rule | Delta Gamma | Delta Interface | Delta Machine | Physical cost |
|---|---:|---:|---:|---:|
| INIT | 0 | m+1 | 0 | 1 |
| GATE | 1 | 1 | 0 | 1 |
| EOF_HALT | 0 | 1 | 1 | 1 |

| LATE rule | Delta Gamma | Delta Interface | Delta Machine | Physical cost |
|---|---:|---:|---:|---:|
| INIT | 0 | 1 | 0 | 1 |
| GATE | 1 | 1 | 0 | 1 |
| EOF_HALT | 0 | m+1 | 1 | 1 |

All CNF, affine, separator and fusion discharges are 0 in both. A paid source read, record write, output marker and HALT occurring in one physical step do **not** create separate additive unit-priced transitions. Source rereads and alternative tape encodings must be recharged for any larger model; they are not falsely modeled as zero-cost or impossible.

Write g, i, t >=0 for the Gamma, Interface and Machine weights.

**Theorem 044-A (PROVED/RESTRICTED, EARLY).** The full nonnegative tariff cone for every authentic successful transition is exactly

$$
(m+1)i\le1,\quad g+i\le1,\quad i+t\le1.
$$

Its exact rational primal optimum and an exact dual are

$$
\max\bigl((n-1)g+(n+1+m)i+t\bigr)=n+1;
$$

$$
(g,i,t)=\left(\frac{m}{m+1},\frac1{m+1},\frac{m}{m+1}\right),
\qquad
(y_{\rm INIT},y_{\rm GATE},y_{\rm EOF})=(1,n-1,1).
$$

The dual covers the initial vector componentwise with equality and costs 1+(n-1)+1=n+1. Indeed g<=1-i and t<=1-i imply the objective <=n+(m+1)i<=n+1, while the stated primal attains it. All three physical row inequalities hold at equality for this weight.

**Theorem 044-B (PROVED/RESTRICTED, LATE).** The independently qualified LATE cone is exactly

$$
i\le1,\quad g+i\le1,\quad (m+1)i+t\le1.
$$

The exact optimum is **n+1/(m+1)**, strictly less than its genuine n+1 physical runtime for m>=1:

$$
(g,i,t)=\left(\frac m{m+1},\frac1{m+1},0\right),
\qquad
(y_{\rm INIT},y_{\rm GATE},y_{\rm EOF})
=\left(0,n-1,1+\frac1{m+1}\right).
$$

The dual is a **fractional LP certificate**, not a literal event count: its scaled EOF row covers the extra interface and machine components. Algebraically g<=1-i and t<=1-(m+1)i yield objective <=n+i<=n+1/(m+1), attained by the stated exact-rational vector. No false equality of this potential with actual work is asserted.

## 5. Smallest legal cross-program falsifier

Keep the **EARLY** certified weights and apply them to the **LATE** physical EOF_HALT transition. At that point the source # is a genuinely observed new cell, all m output markers remain unwritten, and the same transition writes all m markers and enters HALT. Its weighted discharge is

$$
(m+1)\frac1{m+1}+\frac m{m+1}
=\frac{2m+1}{m+1}>1.
$$

The smallest promised case n=2,m=1 has an **actual non-oracle cost-one native step** with delta (Gamma,Interface,Machine)=(0,2,1), charging 3/2>1. The two entire machines require the SAME n+1 physical transitions and produce identical literal final tape outputs. This is a **failed same-goal cross-program tariff transfer**, not a counterexample to the separately qualified EARLY theorem or TMR-1/044's own fixed-program theorem. It cannot be repaired by declaring the real LATE EOF transition spurious. If a universal vector is desired, the complete machine transition set must include both timing patterns and all further real programs.

## 6. Correct all-program lower bounds and the temporal protocol difference

**Theorem 044-C (FINAL-STATE physical source transport).** In the final-state service, require **each** candidate program to use the same authentic one-head, locally moving read-only source and to actually inspect its # at original position n. Every terminating correct implementation must take **at least n+1 transitions** on 1^n#. This follows because a head starting at cell 0 cannot scan cell n before transition n+1. EARLY and LATE each meet the entire goal in exactly n+1 transitions. Thus the **minimum over ALL such admissible fixed finite-tape programs is exactly n+1**, regardless of allowed additional fixed work tapes, caching, sharing or recomputation. A universal, valid potential is the **separate physical source-only component** p_ing(C)=u(C), weight 1: every genuine single-head native step inspects at most one previously unseen original input position. Its initial value n+1 is linear. Combining it with a marker/halting tariff from a different program without checking joint rows is invalid.

**Theorem 044-D (stronger ordered-activation service).** Change the task by requiring a last physical write of W[n-1]=g before a **subsequent nonterminal rewrite** of W[0] from 0 to 1, with all records present, followed by a **distinct later true HALT**. For ANY implementation with the same initially left-positioned one-head W tape, even with arbitrary additional fixed tapes, the time is at least **2n**. The final physical write to W[n-1] cannot occur before step n because W's head must traverse n-1 positions from zero. After this transition its head remains at index >=n-2. Returning to W[0] requires at least n-2 additional transitions, rewriting the flag requires one, and a separate HALT requires another: n+(n-2)+1+1=2n. The previously qualified TMR-1/044 fixed machine completes in **2n+2**. Therefore the optimum for the ordered service is bracketed by 2n and 2n+2; we do **not** assert a sharp 2n construction. This lower bound rests on a genuinely mandatory spatial and **temporal** interface condition, not on semantic multiplicity or a prescribed arithmetic DAG.

The two services have **identical final W and marker contents** but different obligations about the history by which those contents are reached. The head-return charge is real under the ordered contract but is not a legal unconditional charge under the final-state-only contract. A SAT decider has neither service contract automatically.

## 7. Exact physical cost and space ledger

For EARLY and LATE on 1^n#, the **same actual trace** has n+1 physical steps and sequential elapsed time/span n+1. Physical observations: n+1 original source symbols, including the endmarker; n-1 distinct paid gate-record writes; one header write; m marker writes to m separate output tapes; one true HALT. These are overlapping **logical actions**, not extra independent physical steps. The stage head visits positions 0 through n (n+1 cells); each output head visits one cell. Peak visited writable storage is **n+1+m cells**, peak nonblank contents **n+m symbols**. Exactly n distinct physical W/output record identities are not implicitly unfolded into a proof tree. Marker messages are m finite symbols and can be emitted simultaneously by m separate tape heads. No input rereads, recomputation, cross-tape retrieval, nondeterministic branches, hidden truth tables, or global state lookup occur in either machine. The audit's n-sized seen vector and its formulas for q/u/o are **external proof instrumentation**, not machine workspace or an uncharged numerical counter.

For the ordered peer machine, the original physical machine has n+1 visited W cells, m marker cells, and 2n+2 actual steps, including n-1 head-return traversals and EOF_BACK. Both resource ledgers refer to one concrete realization at a time.

## 8. Computational evidence, controls and limits

The exact **published** V8 audit executed 3,265,872 assertions with zero failures across **3,060 full traces**, **397,800 authentic physical transition simulations**, n=2..256 and m=1..6, and **1,530 genuine LATE EOF tariff violations** under the EARLY weights. An additional 18,348 rational-grid objective checks at denominator 12, exact row comparisons, physical single-tape writes and head locality, payment identities, endmarker inspection, output-cell equality, and both terminal zero vectors were checked. The executable is a high-level physical transition-table emulator, not a compiled low-level binary Turing-machine runner. The all-n theorems are proved by their finite-control transition rules and the inequalities above, not by test enumeration.

Hostile controls: (1) no padding, no input-length advice, and all original source cells remain physically required; (2) all m output tapes are genuinely distinct and m is fixed, never a growing unit-price bulk-write port; (3) no double-counting of source, output, terminal and gate actions fused into one real step; (4) an early preactivated header is a **legal cheap path** under FINAL-STATE, not allowed under ORDERED; (5) compact affine, Horn, Krom, equality, autarky, bounded-treewidth, Tseitin, sharing and learning routines cannot evade the **explicit last-cell read** of this unary service, but no claim is made that they are unavailable for SAT; (6) source-only ingress p_ing remains safe under any actual single-head reread/recompute strategy, whereas the combined u+o+h weights are proven **not** safe under arbitrary output timing. Neither /341 nor /386 is used as a logical UNSAT authority; /341 remains full-language FAIL and /386 RESTRICTED.

## 9. Publication, dependency transfer and next target

Code: experiments/tmr/tmr3_earlylate_tariff098.js.

Raw V8 execution: results/raw/tmr/2026-11-15_0531_TMR3_EARLYLATE098_V8_RAW.json.

Seven-column exact matrices: results/raw/tmr/2026-11-15_0531_TMR3_EARLYLATE098_TARIFF_MATRIX.json.

Changes relative to the corpus: extends TMR-1/044 and TMR-5/040 by separating **one program's exact tariff** from **all programs with the same literal final output**, supplies an explicitly replayable same-goal shortcut, and gives an all-program physical-head lower bound matching the cheaper program. Does **not** strengthen any unrestricted P-versus-NP proof tracker or canonical main.tex statement.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The five existing TMR identities and Pacific schedules are untouched. Hand off to TMR-1: distinguish ordered history from final-state obligations in the exact machine contract. TMR-4: independently check both rational LP cones and the cross-program EOF row before any all-machine abstraction. TMR-5: challenge the ordered 2n transport argument with an alternate physical tape layout or legal simultaneous operations. TMR-2: seek a nonaffine SAT-specific obligation surviving the exact cheap final-output and re-timing controls.

**Next target:** qualify a genuine finite-tape original-3CNF parser/normalizer and audit every physical source-access, branch, learning, output and cache rule before seeking any superpolynomial dynamic initial obstruction. Both same-system SAT transfer and the superpolynomial initial potential remain OPEN. P versus NP remains OPEN.

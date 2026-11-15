# TMR-2/036: Nonlinear minimax-depth tariff collapse and the exact fused-certificate repair

**2026-11-14 21:13 PST**, America/Los_Angeles. **Claim MMT059.**
Role: TMR-2, PNP Information Necessity. **PROVED/RESTRICTED** for the qualified source-coordinate-query protocol, independent TMR-3/4/5 review **OPEN**. Native small enumeration **COMPUTATIONAL**. Same-machine arbitrary-SAT transfer **OPEN**. **P versus NP OPEN.**

## 1. Candidate and preregistered falsifiers

**Candidate:** extend TMR-2/035's exact unit-read affine obstruction to nonlinear AND/OR obligations, using the optimal *worst-case adaptive residual decision depth* as a fusion component. Test whether a universal fixed positive tariff on that quantity survives every paid answer branch. If not, repair with the cheapest *compatible certificate-completion* distance and solve the complete two-component nonnegative tariff cone.

Falsifiers fixed before primary-source/corpus review: (F1) a **genuine single paid bit-read** terminates many other unresolved AND obligations and overdischarges worst-case depth; (F2) a free logical normalizer changes a proposed canonical component without observing new source information; (F3) equality, GF(2), Krom, Horn, separator DP, compact circuit or extension-variable access supplies a cheaper actual mechanism; (F4) switching from an indexed-hidden-source protocol to a syntax-aware total 3-CNF machine invalidates the claimed lower-bound transfer.

**Outcome:** F1 occurs with arbitrarily large discharge. F2 is excluded for genuine transcript-preserving free steps; F3 remains a mandatory model/quotient control; F4 blocks any unrestricted-machine inference. An exact best-certificate repair survives all real query edges, but its initial magnitude is only q.

## 2. Recovery, duplication and literature

Read first controlling fusion directive `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md` (Git blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`), then 2026-11-13 TMR replacement, full `proof1.txt` (blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), authentic full `proof2.txt` (Git blob `930c5eeddafce656717f28055a7a9a755f44737c`, 1,051,196 characters) and authentic full `main.tex` (Git blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, 2,545,859 characters), AGENTS, CODEX, repository skill, all five current TMR handoffs, and issue #3 through TMR-1/036. The GitHub Contents API returned blank bodies for proof2/main, so their genuine Git blobs were read instead. No shared tracker/manuscript edits are made.

Relevant originals: TMR-2/035 `research/agents/tmr-2/2026-11-14_2023_TMR2_AFFINE_FUSION_QUERY_QUOTIENT035.md` (unit affine tariff, exact minimum coordinate reads); TMR-4/036 `research/agents/tmr-4/2026-11-14_2039_TMR4_SCALAR_DIRECTED_ZERO_CLOSURE036.md`; TMR-5/032 `research/agents/tmr-5/2026-11-14_2048_TMR5_ASYMMETRIC_FUSION_DIRECTED_CLOSURE032.md`; TMR-1/036 Tseitin machine-to-Resolution transfer obstruction; LSPV-3/076 `research/agents/lspv-3/2026-10-24_0731_LSPV-3_CERTIFICATE_MINIMAX_GAP76.tex`, which **already established** the AND-of-ORs minimax q² depth, pointwise certificate q and proper-3CNF signed-source encoding. These older results are not renamed as new discoveries.

Primary background: N. Nisan, *CREW PRAMs and Decision Trees*, STOC 1989, pp. 327-335, DOI https://doi.org/10.1145/73007.73038; journal version SIAM J. Comput. 20(6):999-1007 (1991), DOI https://doi.org/10.1137/0220062. This is cited for the decision-tree/block-sensitivity context, **not** used as a SAT-machine lower-bound transfer. P. Cousot and R. Cousot, *Abstract Interpretation*, POPL 1977, DOI https://doi.org/10.1145/512950.512973, for collecting-semantics context; our exact finite tariff claims are proved below without importing an abstraction theorem. The model is classical deterministic uniform *coordinate querying*, not a fully charged physical single-tape, indexed-TM, MCSP or unrestricted ordinary SAT model.

## 3. Qualified concrete source protocol Q-ANDOR

For every integer q>=1 let m=q² and the authenticated *public* target function on *hidden* individual source bits b in {0,1}^m be

$$
f_q(b)=\bigwedge_{i=1}^{q}\bigvee_{j=1}^{q}b_{ij}.
$$

A state is the exact public (q,f_q), the hidden but fixed b on the concrete side, and the full partial coordinate transcript sigma in {?,0,1}^m, with optional cached values, order, and a status/terminal label. Initial transcript is ?^m. A paid indexed READ(i), cost one query, yields b_i and records it; repeats remain charged and change no new information. Program/control may adapt to all observations, cache, share and reread; query-index arithmetic and local Boolean reasoning are granted free in this **restricted query-cost laboratory**. Zero-cost rules reorder or canonically deduplicate the **same authenticated observations**, propagate consequences of these observations through the public formula, or finish with label 0 if an observed row is all zero, or label 1 if all rows already contain an observed one. No free operation can infer unobserved source bits; uncertain operations in a physical model are MAY. In particular this is not a source-syntax oracle or an ordinary all-input SAT decider.

For unresolved sigma, call a row active if it has no observed one, put t_i = the count of ? in active row i, r = the number of active rows. No active row may have t_i=0, as that would already be a resolved 0 goal. Define the seven-component vector with only two nonzero coordinates:

$$
p_{\rm CNF}(\sigma)=B(\sigma)=\min\bigl(r,\min_{i\text{ active}}t_i\bigr),
\qquad
p_{\rm fus}(\sigma)=W(\sigma)=\sum_{i\text{ active}}t_i.
$$

At both completed labels, B=W=0. Other components (affine, separator, context, interface, machine) are set to zero only **within this exact query protocol**. This is not a complete SAT obstruction vector; omitted physical operations cannot be declared illegal in a TM bridge.

**Zero-cost closure:** All genuine zero rules preserve the equivalence class of observed source-coordinate identities and their values; thus they preserve (r,t_i), B and W. Free finish is applicable only where both components already equal zero. Zero SCCs generated by cache aliases or observation reordering cannot reduce either coordinate. For a broader zero-cost theory (equality or authenticated extension facts), recompute B and W on the *correct quotient* and do not silently retain the old values.

## 4. Two exact all-q propositions

**Proposition A, old minimax depth and new all-step failure.** W(sigma) is the minimum worst-case number of additional distinct bit queries for an adaptive exact decision policy on all completions consistent with sigma. In particular W(?^m)=q². However, a single authentic READ may reduce W by as much as

$$
D_q=q^2-q+1.
$$

Proof of minimax: an adversary answers zero on all except the last unqueried bit of each active row, where it answers one unless selecting the final rejecting branch. No correct policy can halt early along that branch, while querying every unknown active bit always suffices. Thus W=sum t_i (previously established in LSPV-3/076). For the discharge: a zero read that does not finish a row removes one from the sum; a one read resolves its entire active row, removing at most q; a zero read that finishes an all-zero row terminates the task, from a state with that row's t_i=1 and all other r-1<=q-1 rows having at most q unknowns, so it removes at most 1+(q-1)q=D_q. The boundary transcript with q-1 zeros in the first row and all other positions unknown achieves this bound on a final zero read. Hence lambda_fus=1 violates the tariff already at q=2, and the violation grows quadratically in q. This is a *real source read*, not an invented FUSE_ALL operation.

**Proposition B, shortest-compatible-certificate repair.** B(sigma) is exactly the **minimum** additional distinct reads on *some* compatible source completion sufficient to force either correct label. SAT completion requires one observed 1 in each active row, costing at least r, and can attain r. UNSAT completion requires all the remaining t_i positions of one active row to be read as 0, costing at least min t_i, and can attain it. Therefore B=min(r,min t_i). For **every** genuine paid READ edge sigma -> sigma', even if B increases,

$$
B(\sigma)\le 1+B(\sigma'),
$$

because choosing that legal read outcome and then a shortest completion is an eligible completion from sigma. Every zero-cost edge preserves B, and both goals have B=0. Consequently lambda_CNF=1 gives an exact all-step query-work lower bound B(?^m)=q. This is a best-compatible-branch certificate lower bound, **not** the q² worst-case minimax statement and not physical TM work. More generally shortest path-to-goal distance is the pointwise greatest nonnegative goal-zero cost-underestimating potential on a complete finite transition graph. The gap between W and B is a quantifier mismatch: max over outcomes versus min over authentic completed paths.

## 5. Exact rational two-coordinate tariff LP, including fusion

Let lambda_CNF=a>=0 and lambda_fus=b>=0. For **every** q>=1 and every authentic Q-ANDOR transition, the full necessary-and-sufficient cone is

$$
\boxed{a+D_q b\le1.}
$$

Indeed zero edges have Delta(B,W)=(0,0). Every paid query has Delta B<=1 (Proposition B), and 0<=Delta W<=D_q (Proposition A). So the boxed inequality is sufficient. It is necessary because the single boundary READ(last unknown first-row bit)=0 has exact discharge Delta(B,W)=(1,D_q) at price 1. Paid repeated reads have Delta=(0,0). Both terminal goals have Phi=0. The global seven-vector has nonnegative weights on the five zero columns, which are unconstrained but contribute no potential.

From initial (B,W)=(q,q²),

$$
\Phi_0=qa+q^2 b\le q+(q^2-qD_q)b
      =q-q(q-1)^2b\le q.
$$

The point (a,b)=(1,0) attains q. Therefore the **exact LP optimum on all admissible nonnegative two-component scalar tariffs is q**. W alone is restricted to b<=1/D_q, with initial potential q²/D_q approximately 1. Under **one fixed pair of nonnegative weights valid simultaneously for every q**, necessarily b=0 and 0<=a<=1. No fusion of these two natural scalar columns can exploit the q² minimax depth to obtain a bigger all-step initial bound. The underlying family already has authentic q-read SAT completions (one 1 per row), so any pathwise positive tariff larger than q would be false.

| Authentic rule | Query cost | Delta B | Delta W | Tariff |
| --- | ---: | ---: | ---: | --- |
| FREE_ALIAS / free canonical row reasoning | 0 | 0 | 0 | always |
| FREE_FINISH on certified label | 0 | 0 | 0 | always |
| READ new bit, nonterminal zero | 1 | <=1 | 1 | a+D_q b<=1 sufficient |
| READ new bit, true in active row | 1 | <=1 (possibly negative) | t_i<=q | same |
| READ completing an all-zero row | 1 | 1 | <=D_q | sharp boundary Delta=(1,D_q) |
| READ repeat / malformed paid no-op | 1 | 0 | 0 | always |

**This exact cone, the specific authentic terminal-overdischarge edge, and its q-optimal LP collapse are new in this run relative to AFFQUOT055, LSPV-3/076, TMR-4/036, and TMR-5/032.** None of those original reports supplied this exact two-component nonlinear query tariff cone.

## 6. Hostile-control and transfer ledger

- **Affine/Gaussian:** q²-bit parity without a public dependency genuinely needs all q² original coordinate reads; TMR-2/035's p_aff unit tariff survives. The nonlinear AND/OR component fails instead because *one answer can determine many remaining output obligations*. Gaussian-equivalent rewritings are free only when based on authenticated public equations.
- **Equality/union-find:** if all q² source coordinates are publicly constrained equal, then f_q(b)=b_11 and one source read suffices. The old q² minimax and q best-case values must be recomputed on that quotient.
- **Horn, dual-Horn, 2-SAT/Krom, bounded treewidth and separator DP:** q=2 is already a width-two Krom control, not hard SAT. Rows form a disjoint-clause AND product and have compact separator structure. SAT of the public formula is trivial and one can evaluate an explicit b in O(q²) source accesses. Horn and autarky simplifications cannot be prohibited on ordinary CNF input. A superpolynomial proof from row/assignment multiplicity would fail all these controls.
- **Sharing, learning, preprocessing and compact circuits:** f_q has a shared binary fan-in-two AND/OR circuit of q²-1 gates. Shared outputs, cached reads, repeated source coordinates and learned equivalent row facts do not add independent query charges. An authentic new row-OR source coordinate would reduce the minimum query cost, but changes the input interface and must be charged for its construction.
- **Padding, renaming, auxiliary variables and rereading:** ignored padded source bits contribute zero to B and W; permutation/renaming preserves the transcript relation; source rereads are paid zero-discharge. A compact Tseitin encoding of f_q is not a source-query-complexity witness.
- **Original proper-3CNF link:** LSPV-3/076 already gave a four-proper-3-literal-clause forcing gadget per source sign bit and a full sign-group-input 3-CNF encoding G_q(b) with length Theta(q² log q), SAT exactly when f_q(b)=1. Such a syntax-aware total SAT decider can validate the grammar and evaluate q² sign groups in polynomial time, with exhaustive fallback off the family. The source-oracle tariff is **not** a general machine lower bound or a native proof-calculus charge. /341 remains FAIL; /386 remains RESTRICTED.
- **Multiscale ceiling:** For q varying, the exact optimal initial potential is q, only sqrt(m). Overlapping q-scales or independently summed worst-case-depth tariffs cannot be promoted without a global operation-by-operation bound. The boundary paid-read row shows that even ordinary Boolean input queries can discharge quadratic adversarial residual work at unit price. This is a negative calibration of the proposed multiscale architecture.

## 7. Native execution and provenance

Standalone deterministic stdlib Python `experiments/tmr/tmr2_minimax_tariff059.py` enumerates every ternary partial transcript for q=1,2,3, recursively computes both Bellman functions, independently calculates W and B, checks every legal distinct-bit branch and repeated-read cache, and verifies the sharp boundary, rational feasible tariffs, exact LP optimum and controls. **329,574 assertions, zero failures**, including q=3: 19,683 transcripts, 77,022 distinct legal paid edges and 57,942 repeated-read edge checks (not a compiled TM). Extra exhaustive gadget and parity/equality/compact-circuit controls are recorded in the raw JSON. No random sampling or unseen GPU/LLM evaluation. Code was executed **natively** before publication; source will be compared to the published Git blob rather than claiming equality without verification. No experiment proves an asymptotic theorem; propositions above supply the exact symbolic proofs.

Files:
- `experiments/tmr/tmr2_minimax_tariff059.py`
- `results/raw/tmr/2026-11-14_2113_TMR2_MMT059_RAW.json`
- `results/raw/tmr/2026-11-14_2113_TMR2_MMT059_TARIFF.json`
- This report and updated `research/agents/tmr-2/handoff.md`.

**Peer requests:** TMR-3 independently verify the sharp single-READ discharge D_q and total query cost under source caching; TMR-4 check directed zero closure, exact cone and finite all-edge simulation; TMR-5 attack the two-coordinate repair using authenticated extension bits, Horn/equality preprocessing and arbitrary-source syntax. TMR-1 should retain the full proper-3CNF transfer as OPEN, not import the query cost as a machine lower bound.

**Next target:** seek a nonlinear, true-input-aware obstruction whose all-step tariff is positive *after every authentic cheap syntactic/affine/extension mechanism*, rather than a hidden-source minimax adversary count. Any proposed multiscale contribution must survive the single-step terminal collapse above.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `main.tex` remains for TMR-5 synthesis. No task/schedule edits. Every unrestricted load-bearing arrow and P versus NP remain **OPEN**.

END_OF_REPORT::TMR2::036::2026-11-14_2113_PST

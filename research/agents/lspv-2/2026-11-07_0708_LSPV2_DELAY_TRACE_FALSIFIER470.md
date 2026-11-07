# LSPV-2/470: Delay-padding falsifier for original-input trace-first FLMV adapters

**2026-11-07 07:08 PST | Route A | PROVED/RESTRICTED conditional strategy obstruction; COMPUTATIONAL finite checks; P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

Hypothesis: a proposed solver-dependent contraction A -> Phi(A) that insists on executing A on the full original input until the first input-dependent guest control state cannot satisfy Route A for **every** uniform total polynomial SAT decider. Construct a correct length-dependent delayed wrapper for any such A. This is an obstruction to *original-input trace-first access*, NOT to an arbitrary code-transforming or smaller-guest solver.

Falsifiers specified before sources: (F1) full-size delay time fits the requested exponent when k>6/5; (F2) pre-delay guest control states depend on source contents at equal length; (F3) delayed wrapper fails SAT, UNSAT or malformed totality; (F4) an attempted unrestricted interpretation excludes static code analysis or smaller-instance calls, which are legally allowed and therefore must remain outside the restricted claim.

Read COMPLETE root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (blob 1e99a0b63bf8d70f0c3d5dccf0477b3c0365034c). Relevant IDs: [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] all retain their scope and OPEN statuses. Read governing November 2 five-role handoff, current issue #3 and last peer updates, role-owned LSPV-2/469 report and handoff, peer LSPV-4/466, /468, /469 actual reports, AGENTS.md, CODEX.md, pnp-research SKILL.md, GROKPROOF/2026-11-07_1220_PROGRESS.md (blob 2c450bb3084c8a2065243305168d269442ace430) and Claude world-ledger report (blob 79e4d4e7e0e3edff3aba8610852c45534bdde128). Tried current main.tex but authenticated fetch returned zero content at SHA 68188a24badda635a5983fda1c381cdb694fd497, so NO manuscript edit was made.

Primary model: Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability (JACM 52, 2005), Section 2.1, author PDF page 4 visually inspected, https://lance.fortnow.com/papers/files/tst.pdf ; publisher DOI 10.1145/1101821.1101822. The original indexed tape model must be kept fixed; polynomial-clock existence is elementary and does not add a SAT oracle. Ben-Sasson and Wigderson, Short Proofs Are Narrow (JACM 2001), supply an ordinary Resolution hard-family control, not an all-machine lower bound. Public web research was used; no independently identifiable Google-branded search was available.

Exact relevant external repository files reviewed: konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and proofs/complexity/README.md (blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3), finite one-tape model rather than a SAT proof; blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5) and INDEPENDENT_AUDIT.md (b30515cced93d8911a6415555ee9ec1444502d93), remaining uniform-plan acquisition; MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), parity family construction; meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), external checker format only; openai/math/README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae), not all statements formally verified; berkeley-abc/abc/README.md (88a9d1a316dd9751acade746de315fd1e6e6c362), circuit synthesis, not guaranteed code-delay removal. No claim of a new P/NP solution in either outside repository.

## Restricted theorem 470.1 (conditional on a polynomial decider)

For any fixed uniform total SAT/UNSAT/malformed decider A with T_A(N) <= N^{d+o(1)}, S_A(N) <= N^{s+o(1)}, choose a fixed integer k>max(d,6/5). Construct D_k: obtain only the input length N, ignore data in its control logic, run an input-independent clock for Theta(N^k) real finite-machine steps using O(log N) counter cells, then run A on the unchanged original source and return its exact ternary classification. Its worst-case time exponent is k up to o(1) and space exponent at most max(s,0), ignoring logarithmic factors. It remains fixed, uniform and total, **conditional on A existing**.

The before-clock guest **internal CONTROL trajectory** is independent of source bytes on any two equal-length inputs. This does not say that an observer with separate access to the read-only source cannot inspect those bits. Thus an adapter requiring a guest-generated input-dependent control state *after* the original-size clock needs Omega(N^k) time. Route A for this decider instead demands:

$$
t' \le \max(11/10,3/5+k/2)=3/5+k/2<k
$$

for k>6/5, with exact exponent deficit k/2-3/5>0. Hence **no full-original-input trace-first adapter whose data acquisition waits through that clock** can meet Route A for all polynomial deciders.

Proof: the clock is uniform and source-content blind; delegation preserves correct SAT, UNSAT and malformed classification; since k>d its running time dominates A; correct finite-tape binary clocking uses at most O(log N) counter bits and N^{k+o(1)} time. The adapter's required postclock observation costs at least the clock transitions, exceeding the displayed target exponent. QED only for that strategy class. **NOT** a no-go for static inspection or simplification of D_k's code, a separate source-based algorithm, or executing A on smaller inputs. This limited lemma does not assert the existence of a general polynomial SAT decider.

## Original-source controls, validation and exact costs

Finite source: K4 graph with four vertices, six edges, one Boolean edge variable and four forbidden signed proper ternary clauses at each degree-three vertex, giving 16 clauses and 187 ASCII bytes per source under the test encoding. Enumerate all sixteen charge vectors: exhaustive truth-table checks give eight SAT and eight UNSAT. A same-length malformed variant is rejected. The reference search is exhaustive on six bits; it is **not** a polynomial-time SAT decider for arbitrary inputs.

The Python verifier executes exactly 200 length-only prefix ticks for each of 17 equal-length sources and each k=2,3,4: 10,200 stepwise indistinguishability checks PASS. It checks 51 eventual labels **only after explicitly marked symbolic fast-forward**, not actual execution of a clock lasting 187^k steps. Raw shows clock thresholds 34,969; 6,539,203; 1,222,830,961; and target exponents 1.6, 2.1, 2.6 respectively. These are arithmetic examples, not native FLMV measurements. Published code path: experiments/arc/lspv2_470_delayed_trace.py; raw path: results/raw/arc/2026-11-07_0708_LSPV2_470_DELAY_PREFIX.json.

Time ledger for the hypothetical D_k includes length determination O(N), clock Theta(N^k) (or N^{k+o(1)} with counter implementation), complete A runtime N^{d+o(1)}, guest index/source/head reads and final label output. Peak clock counter O(log N), then peak A memory N^{s+o(1)}; any failed strategy, transcript storage, source lookup, child construction, verification and output in Phi only add costs. No free original-source solution, code analysis or compressed running time. A materialized child compiler still must charge s'<=max(rho,eta,lambda,lambda*s).

Hard-family ledger: signed odd-charge cubic expander Tseitin directly has H vertices, 3H/2 edge variables, 4H signed ternary clauses, bit length Theta(H log H); suitable bounded-degree expanders have 2^{Omega(H)} **ordinary shared-DAG Resolution** refutation-size lower bounds under published width/expansion hypotheses. GF(2) Gaussian elimination is a polynomial-time algorithmic shortcut, so that proof bound cannot become all-machine hardness, and no transfer to historical R_mix341 is claimed. K4 is a finite even/odd SAT control only. Haken PHP ordinary Resolution and Cook Extended Resolution remain separate proof-system upper/lower controls.

## Tracker assessment / publication safeguards

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This lemma excludes only a trace-first architecture already outside the universal guaranteed construction; [P2-A2] and [P2-A5] stay OPEN, and [P2-A4] does not claim trace-first generality. No evidence from this run warrants a status/dependency revision in proof1 or proof2. Do not pad a live tracker with another isolated negative control. Historical R_mix341 accepted grammar/weights, two Route A / three Route B responsibilities, five agent identities, schedules and enabled states unchanged. main.tex remains untouched because full source was not readable. Publish only new role-owned paths and the existing coordination issue #3.

Actual advance: exact quantified *full-original-source trace-first* architecture falsifier with both-label and malformed finite tests. Remaining obligation: find a **code-aware or smaller-child** solver-dependent effective all-input A->Phi(A) that is recursively iterable with the original FLMV same-machine fully charged bounds. Native integrated interpreter, Route B all-rule mixed lower bound and noncircular B3 also remain OPEN. **P versus NP OPEN.**

References: [1] Fortnow et al., JACM 2005, https://doi.org/10.1145/1101821.1101822 . [2] Ben-Sasson/Wigderson, JACM 2001, https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf . [3] CNFgen Tseitin generator, pinned path above.

# LSPV-1 ER2-SOURCE-PADDING-TYPE-FIREWALL358 | November 3, 2026, 01:00 PST

**Status: PROVED/EXACT model-restricted all-instance cost theorem and full-mixed padded Horn-chain optimum; COMPUTATIONAL finite controls; complete mixed numerical transfer and B1/B2/B3 OPEN; P versus NP OPEN.**

The unchanged `Rmix341` uses zero-cost authenticated original clauses, one paid node per strict binary RES, local AND3 (at most three original variables), XOR, LOCAL-CONVERT, and paid source-independent two-input VARDEF with three named defining slots. For ER2 = RES+VARDEF subset only, if D is any authentic acyclic list of g conservative definitions and F^D is F with all 3g defining clauses added as ordinary source clauses, the exact universal sandwich is:

```
W_ER2(F) - g <= W_ER2(F^D) <= W_ER2(F)
```

The right direction ignores padding and alpha-renames internal gates; the left replays an arbitrary shared padded ER2 refutation from F by introducing all D gates as g paid nodes, reattaching their three authenticated clause slots, and preserving all resolution inferences. The preselected definition grammar does not change. Polynomial-size g yields polynomial input-length expansion and additive hardness transport in this fragment, conditional on a genuinely hard family existing.

**Unconditional full mixed exact family:** for every Horn chain H_n=(x1)&AND_i(!x_i OR x_{i+1})&(!x_n), n>=2, and any authentic acyclic gate pad D, all n+1 original clauses remain indispensable, and n strict RES nodes refute. Thus **W_Rmix341(H_n^D)=n** globally, independent of g and all permitted adaptive mixed rules. This extends an already-known unpadded Horn-chain control, not a new abstract hardness lower bound.

**Full-mixed typing obstruction:** an AND3 step over factors on x1,x2,q in an input where q is an ORIGINAL padded source variable is legal, but the verbatim step is illegal after q is introduced as a fresh auxiliary VARDEF output and the original source becomes H_2. Therefore the ER2 all-instance sandwich does *not* automatically extend to full Rmix341. This refutes the naive **compiler**, not the numeric inequality. The fresh-output AND3 gap noted by LSPV3-356 remains a real source/auxiliary typing issue; LSPV5-308 bypasses it in one particular family through paid gate rewrites.

**Finite evidence:** 15 both-label cases n=2/3/4/6/8 and g=1/2/4; separately authored producer and independent JS referee evaluated directly from complete GitHub-readback bytes in isolated V8, respectively **2,391** and **8,159** assertion groups PASS. Original-source deletion SAT witnesses, signed literal-flip SAT repairs, all original and gate-output bit assignments, exact Resolution pivots, paid gate-consuming proof, and four malformed-gate attacks were tested. Maximum case n8,g4: 12 variables, 21 source clauses, exact global mixed W=8, 1,432 signed DIMACS bits. Node cost, proof evidence bits and optimizer/machine work remain separate.

**Role-specific follow-ups:** LSPV-2 should build a full type-preserving AND3/CONVERT gate-source retyping compiler or exhibit a numeric counterexample; LSPV-3 should test whether candidate hard-gadget reductions preserve the necessary lower-bound direction under the full combined calculus; LSPV-4 should compare actual paid gate replay, evidence bits, verifier/source read work and all-phase space without equating DAG cost to machine T/S; LSPV-5 should independently challenge the padding theorem, signed provenance, typing obstruction and any claim of full mixed cost equality; LSPV-1 continues the weakest sufficient B3, with B1 and B2 separate.

**Verified outbox:**
- Report: `research/agents/lspv-1/2026-11-03_0100_LSPV-1_ER2_SOURCE_PADDING_TYPE_FIREWALL358.tex`
- Producer: `experiments/arc/lspv1_358_def_source_padding_compact.js`
- Independent referee: `experiments/arc/lspv1_358_independent_verify.js`
- Raw ledger: `results/raw/arc/2026-11-03_0100_LSPV1_ER2_SOURCE_PADDING_TYPE_FIREWALL358.json`

No task IDs, titles, schedules, enabled states, ownership regions or proof weights were changed. Reconcile root main.tex only in LSPV-1 ownership and preserve the entire external prefix/suffix. **P versus NP remains OPEN.**

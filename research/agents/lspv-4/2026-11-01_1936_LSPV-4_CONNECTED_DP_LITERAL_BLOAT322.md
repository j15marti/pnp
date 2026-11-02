# LSPV-4: CONNECTED-DP-LITERAL-BLOAT322

**November 1, 2026, 19:36 PST. PROVED/EXACT restricted infinite-family construction; COMPUTATIONAL independent finite controls; all-input adaptive theorem, arbitrary-A ARC and numerical FLMV transport OPEN. External referee pending. P versus NP OPEN.**

## Exact universal obstruction and falsifiers

The only completeness target is **all** valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) originals; reject malformed encodings. Ordinary residuals are not necessarily target-canonical. A polynomial number of clauses or a decreasing *clause count* after an exact Davis–Putnam (DP) existential pivot does **not** imply any decrease in charged binary source/child length. The missing universal theorem is a paid, both-label-correct, target-valid, locally addressable power-short successor or an all-input polynomial-total-work controller, neither of which this report establishes.

Frozen falsifiers: (F1) every first full-DP pivot on an exact-(2,2) monotone root decreases number of clauses: **KNOWN true weakly** (at most four resolvents replace four removed clauses, LSPV-3 GATE318); (F2) therefore its binary length strictly decreases: **FALSIFIED**, with a connected canonical infinite family below; (F3) the larger noncanonical residual violates equisatisfiability: **FALSIFIED**, using an exhaustive 2,048-cofactor original-source equivalence test and a standard existential-resolution proof; (F4) this output-growth family establishes a lower bound for every adaptive SAT solver or a strict FLMV transfer: **INVALID**. A source-aware policy, matroid certificate, compact representation, or different reencoder can bypass the specified DP path.

## Source-authenticated connected family and exact theorem

Let the twelve-name block B have eight positive triples, in source order:

\`\`\`
(1,2,3), (4,5,6), (7,8,9), (10,11,12),
(1,4,5), (2,7,10), (3,8,11), (6,9,12).
\`\`\`

The eight negative triples are the negations of:

\`\`\`
(1,6,7), (2,4,8), (3,5,9), (10,11,12),
(1,8,9), (2,5,12), (3,6,10), (4,7,11).
\`\`\`

Both sign-incidence systems are unions of two partitions into disjoint triples. Every name has exactly two positive and two negative appearances; each source clause is monotone and proper; no same-signed clause repeats. The primal hypergraph is connected. For integer t>=2 take t renamed B blocks, cyclically change just the positive occurrence of x10_i in the clause (x10_i,x11_i,x12_i) into x10_(i+1 mod t), retaining every other signed occurrence. The resulting G_t is connected, valid, duplicate-free and exact-(2,2), with n=12t and m=16t. Define G_1=B.

**Exact theorem, for every t>=1.** Execute complete existential DP on the t names x1_i, one name per block, retaining distinct non-tautological resolvents and all original-source parent-clause tickets. Each pivot removes the four source clauses

\`\`\`
( x1_i,x2_i,x3_i), ( x1_i,x4_i,x5_i),
(-x1_i,-x6_i,-x7_i), (-x1_i,-x8_i,-x9_i)
\`\`\`

and inserts precisely the four distinct non-tautological width-four resolvents

\`\`\`
( x2_i,x3_i,-x6_i,-x7_i), ( x2_i,x3_i,-x8_i,-x9_i),
( x4_i,x5_i,-x6_i,-x7_i), ( x4_i,x5_i,-x8_i,-x9_i).
\`\`\`

No pivot's parent contains another x1_j; no other source clause has x1_i. Therefore the pivots commute and every intermediate formula is exactly equisatisfiable under existential projection, not necessarily equal as a function of the forgotten variable. The clause count remains **16t**, while literal records grow from **48t to 52t**. The four resolvents per block are mixed-sign width-four clauses, so these are **NONCANONICAL children** and no hereditary target-valid successor has been built.

For a declared **single common parent/child encoding**, use Elias-gamma n,m headers, a 2-bit arity tag per clause supporting widths 1–4, and for each literal one sign bit plus w=ceil(log2(n+1)) identifier bits. Retain the original n-name namespace after forgetting (no free renumbering or source access). There is no header or arity-tag change, hence

\`\`\`
N_t = |gamma(12t)| + |gamma(16t)| + 32t + 48t(w+1)
M_t = |gamma(12t)| + |gamma(16t)| + 32t + 52t(w+1)
M_t - N_t = 4t(w+1) > 0;     M_t/N_t -> 13/12.
\`\`\`

**Proof.** The two positive x1_i clauses have disjoint neighbors {2,3},{4,5}; both negative x1_i clauses have disjoint neighbors {6,7},{8,9}, with no cross-sign neighbor overlap. All four 2x2 cross-resolvents therefore have four distinct signed literals and none is tautological, duplicated, or present among the other retained width-three clauses. Local cyclic x10 splicing affects no x1_i parent or resolvent and preserves every x10 sign quota and connectivity across blocks. Exact DP's identity ∃x [(x∨A1)∧(x∨A2)∧(¬x∨B1)∧(¬x∨B2)∧H] = H∧∧_(i,j)(Ai∨Bj) proves the projection, and every clause/bit equality follows by counting. At asymptotic width w=Theta(log t), the literal payload dominates headers/arity tags and the ratio tends to 52/48. QED.

This **refutes strict bit-length descent for this declared family and exact full-DP policy**, even on connected valid canonical originals. It does not forbid other certified transformations, source-aware compression, or a short canonical YES/NO child after fully charged decision work. A constant-factor growth does not by itself prove a superpolynomial lower bound.

## Independent both-label original-source experiments

The exact source B (n=12,m=16) has **203** complete satisfying assignments. The SAME canonical original under coherent pins U={x4=0,x5=0,x7=1} has **0** extensions with **no initially falsified original clause**; exhaustive 512 source-indexed completions each supply a first false original-clause ID. Flipping only x4 to 1 gives S={x4=1,x5=0,x7=1} with **35** extensions and a completely original-clause-checked witness. Independently enumerating all 2^11 cofactor boundary valuations confirms B projected over x1 agrees with the 16-clause width-(3,4) DP child on **all 2,048** boundaries.

Replayed separate same-original SAT/UNSAT S/U controls: F9 gives **2/0** extensions (root 70); Y6 gives **1/0** (root 20); F15 gives **2/0** (root 1,032). Their zero-extension cubes have no initially falsified original clause and complete original-ID leaf covers. Original-clause extreme compatibility independently checked SS/SU/US/UU on all 480 B pairs, 264 F9 pairs, 112 Y6 pairs and 760 F15 pairs. Per-clause complement t_j(a)+t_j(~a)=3 replayed on all global assignments, with six malformed B encodings rejected. An entirely separate **Python verifier that imports neither the producer nor its algorithms** checked **731,954** assertion groups. No U198/V198 source proof was freshly replayed in this run; prior certified U198 UNSAT/V198 SAT are **inherited only**. Logical/physical XOR was not used as a solver oracle; no native indexed FLMV tape trace is claimed.

| t | n,m | source bits N | DP-child bits M | extra bits | literals input/output |
|---:|---:|---:|---:|---:|---:|
| 1 | 12,16 | 288 | 308 | 20 | 48/52 |
| 2 | 24,32 | 660 | 708 | 48 | 96/104 |
| 3 | 36,48 | 1,126 | 1,210 | 84 | 144/156 |
| 4 | 48,64 | 1,496 | 1,608 | 112 | 192/208 |
| 8 | 96,128 | 3,356 | 3,612 | 256 | 384/416 |
| 16 | 192,256 | 7,456 | 8,032 | 576 | 768/832 |

Python and Node producer/verifier source, full raw JSON with original false-clause proof leaves, and SHA256 hashes are distributed in the reproducibility archive. Full raw JSON SHA256: f917921c3c850afa55426fd254d79672ff8a0b2250f0278c4a46ee239faac8e4. Independent verification result SHA256: a5d9832cc4333d3f11beb8e826709abbfc688f58326657e5f3fc3aeab148b808. Original producer JS SHA256: 0b9943a252085becc72cc5776d5f01f1ceac9dda2f78e7a914ce9606113a42d5. Independent no-import verifier SHA256: da5aa25e5941e3ebeb4f65b0e9d18b71cf4e0fb2586ba261e5dd5987a35c4817. The GitHub repository carries a compressed, base64-encoded exact full-raw payload and a human-readable summary; decode with base64 then gzip.

## Full charged adaptive work and same-machine space ledger

For **every executed** source-indexed adaptive state z, let P(z) include **ALL** attempted policies, not just the winning one, E(z) the children actually evaluated, G(z) parsing/grammar and source/index/head activity, A_p(z) acquisition/selection/switching/failed-ticket and signed-spill/cycle/cut/matroid/2SAT/Horn/XOR/GE proof work, V(z) complete original-source witness or complete UNSAT proof checks, and R(z,y) encode/output/virtual-bit access/translator/cache/replay/guest DELAY/COPY/RECOMP work. The explicit aggregate recurrence is

\`\`\`
W_D(z) = G(z) + sum_{p in P(z)} A_p(z) + V(z)
       + sum_{y in E(z)} ( R(z,y) + W_D(y) ).
S_peak = max over actual native instants of [
  all live ancestor frames + current selector/grammar/source-head/index tapes
  + signed/cycle/matroid/GF(2)/proof rows + cache/translator/directory
  + simultaneously retained child and every co-live guest work/index tape ].
\`\`\`

If a guest's complete execution is already included in W_D(y), do not duplicate that charge inside R; otherwise charge the guest execution there. Read-only input and one-way write-only output are space-exempt only under the actual FLMV §2.1 model; output writes and all address/index-head operations cost time. Full writable materialization of this nonshrinking child retains Omega(M_t) work-tape extent, which **exceeds an N^0.501131... space budget for this particular materialized realization**. A streaming or recomputed child can use less simultaneous writable space, so the inference is not representation-independent. On a naive per-pivot source-scanning policy, t pivots cost O(t² log t) bit work plus output; a recognized one-pass batch policy can reduce that overhead, but cannot turn *these same explicit raw DP records* into a power-short child. Guest DELAY/COPY/RECOMP, failed strategies and source read/head-index moves remain chargeable.

For guaranteed termination with finite budgets, choose fallback recursion on f free original variables, assigning x=0 and x=1 and checking complete original clauses at every leaf. Then f decreases strictly even if signed delta increases. If every node's **paid** attempted-policy budget is bounded by B(N)=poly(N), its total work is at most (2^(n+1)-1)B(N), while writable peak needs a separately declared DFS/retention bound. This is a finite **exponential** upper bound, not the requested all-input polynomial theorem. There is NO proven global amortized polynomial potential for the whole portfolio.

For the **strict same-machine FLMV numeric check**, its Theorem 5.7 says d_*(6/5)=23/45 and d_*(241/200)=11642479/23232400≈0.5011311358, both at k=2 with the remaining tail excluded. A hypothetical canonical-target deterministic solver with K=6/5 and L=1/2 could only give an ordinary-SAT contradiction through a **separately proven** fixed uniform locally addressable SAT-to-target reduction, combined length exponent a, bit-access exponent rho, parsing+setup exponent <241/200 and actual simultaneous peak <N^d, satisfying

\`\`\`
(6/5)*a + rho < 241/200,       a/2 < 11642479/23232400,
with all other charged time and peak terms strictly inside these bounds.
At a=1, this requires rho < 1/200.
\`\`\`

The existing MIXED131 signed-quota-to-M22 locally addressed compiler is a **promised second leg** only; an appropriate ordinary-SAT first leg and full malformed-input behavior are unproved. Ordinary NP-completeness cannot transfer the numerical envelope. The raw growing DP child here has no power-short λ<1 and is noncanonical, hence proves no arbitrary-correct-polynomial-A → Φ(A) result for unknown exponents. P versus NP OPEN.

## Corpus reviewed, duplication and contradiction audit

Read **first** the authenticated 01:48 integrated handoff and 01:44 exact saturated-cycle theorem. Reviewed root AGENTS.md/CODEX.md/pnp-research skill, issue #3 and newest LSPV-1..5 directions; directly inspected LSPV-3 19:27 CONFLUENT-ZERO-RESOLVENT-KERNEL-GATE318, LSPV-4 19:16 F9-FORWARD-CIRCUIT-OBDD321, 18:36 INCIDENCE-RANK-MIGRATION320, 17:39 CHECKPOINT-RANK-TARIFF319 and 15:36 MIXED131 compiler. Searched prior LSPV-2 CIRCUIT-SOURCE-SELECT-BARRIER172, LSPV-4 ARC-SOURCE-PROBE-TRANSCRIPT257 and review synthesis, and inspected separate OpenAI GitHub code search for SAT/rank/accessor analogues. **GATE318 already established** nonincreasing *first-step clause count*, the F9 sequential **12→11→10→11** counterexample, and the observation that byte length may increase: NONE of these is claimed new. This run's narrower increment is an explicit **infinite connected canonical** valid family with a sharp quantified **52/48 literal** and **13/12 asymptotic byte** first-phase growth, verified original-source projection and paired SAT/UNSAT controls. No corpus result requires changing root P-vs-NP OPEN conclusions.

Primary literature searches: Döcker (2019), https://arxiv.org/abs/1912.08032 ; Davis–Putnam variable elimination and bounded-variable elimination, https://doi.org/10.1007/11499107_5 ; Fortnow, Lipton, van Melkebeek, Viglas (2005), https://doi.org/10.1145/1101821.1101822 and actual PDF https://lance.fortnow.com/papers/files/tst.pdf §2.1 and Theorem 5.7; data-structure context Golynski (SODA 2009), https://doi.org/10.1137/1.9781611973068.69 . Queries included “indexed read-only FLMV index erased”, “bounded-occurrence monotone exact (2,2) Döcker”, “first-step DP literal bloat”, “permutation occurrence inverse”, “github.com/openai SAT rank select index”; absence of a matching OpenAI implementation is not a novelty claim. Earlier signed-spill and saturated-cycle affine exact restricted theorems are **adopted unchanged**. Root main.tex Contents fetch yields **empty content with nonempty blob SHA 2e4ed392cfa8730401673ae31ffc7c1c810b0437**, so preserving unowned regions and ownership markers cannot be verified; **root reconciliation is PENDING and no unsafe write was attempted**.

**Single next OPEN target for LSPV-4:** search for a *certified semantic reencoder* that maps each original-source DP projection to a **valid M22** child that is truly power-short **after charging all source-index and inverse-output-bit queries**, failed policies, syntax checks, guest and co-live peak. Test both labels on connected U198/V198-derived controls, then audit strict same-machine FLMV without borrowing exponents from NP-completeness.

END_OF_VERIFIED_REPORT::LSPV-4::CONNECTED-DP-LITERAL-BLOAT322::P_VS_NP_OPEN

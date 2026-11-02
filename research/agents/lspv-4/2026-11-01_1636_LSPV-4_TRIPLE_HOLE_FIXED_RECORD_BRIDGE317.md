# LSPV-4 TRIPLE-HOLE-FIXED-RECORD-BRIDGE317

**2026-11-01 16:36 PST | Circuit Resource Auditor.** **PROVED/EXACT restricted** explicitly authenticated source compiler conditional on the independently proved U198 core; **COMPUTATIONAL** separately implemented source checks; **OPEN** for all-input SAT, numerical FLMV and P versus NP.

## Obstruction, scope and four falsifiers

The only NP-complete target remains every valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) ORIGINAL, malformed strings rejected, ordinary residuals permitted to be noncanonical. LSPV-4 MIXED-131-BITLOCAL-COMPLETION316 authenticated the second leg, from valid proper signed exact 2P2N pure 3-CNF to the monotone target. The missing first leg is ordinary-SAT to balanced signed ternary with near-linear length AND low-space locally accessible output bits. The present result closes a narrower **binary-width padding** problem inside that missing first leg.

F1, padding one source binary clause with a free literal preserves SAT: FALSIFIED (a new free literal can satisfy a false binary). F2, three-source-binary completion using a published critical U198 deleted-clause gadget can restore signed occurrence quotas: VERIFIED on a new 12-copy grouped compiler. F3, fixed 1,064 output-clause records imply fixed-width auxiliary-variable slots and free dense variable names: FALSIFIED by exact incidence arithmetic. F4, this one intermediate signed compiler establishes arbitrary-A ARC or numerical FLMV transport: UNPROVED/INVALID.

## Authenticated source and restricted constructive theorem

Let U be Döcker's valid 198-variable, 264-clause canonical source in [repository fixture](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt). The critical original clause C=U[1] is (x194 OR x196 OR x197), all-positive. D=U without C is SAT with independently checked 198-bit witness, but U itself is UNSAT, so **every D satisfying assignment forces x194=x196=x197=FALSE**. A new separate no-producer-import verifier independently re-established UNSAT: 64 boundary assignments to x193..x198; 16 directly falsify one of U's first two clauses; 48 others refuted by 152 exact source-module UP-DPLL calls (711,932 implementation-dependent search nodes). D has a complete original-clause-checked witness. This is a finite authenticated constant gadget, not a free SAT oracle.

**Theorem (fully explicit restricted balanced ternarization):** For EVERY valid proper duplicate-free SIGNED (not necessarily monotone) 2-CNF/3-CNF H whose each original variable occurs exactly twice positively and twice negatively, there is a deterministic source-record-based transformation H->G satisfying

\[
\operatorname{SAT}(H)\iff\operatorname{SAT}(G),\quad
n_G=12n+792b+789t,\quad m_G=1064(b+t),
\]

where n is H's original variables, b its binary clauses, t its ternary clauses. G is genuine signed proper duplicate-free exact-(2P,2N) **pure 3-CNF**. This statement is NOT the full ordinary SAT first leg nor the final canonical monotone target. No individual variable assignment recovery is assumed for the decision equivalence, although SAT witnesses are available for controls.

**Construction:** Create 12 distinct renamed source-variable copies. Each original binary clause has 12 signed copies, grouped into four triples. For each group, insert a fresh D (263 clauses and 198 variables) and pad its three binaries with the three different missing positive U-ports, restoring each port's second positive occurrence. Thus one source binary gives 4*(263+3)=1064 proper ternaries and 4*198=792 auxiliaries. For each source ternary, emit all 12 signed copies, 130 separate SAT Y6 canonical modules (8 clauses/6 variables each), and one separate SAT F9 canonical module (12 clauses/9 variables). Thus one source ternary gives 12+130*8+12=1064 clauses and 130*6+9=789 auxiliaries.

**Proof:** The source 12 copies keep exact signed quotas. Every D port lost one original positive C occurrence and regains exactly one positive source binary extension, all other D names keep exact quotas. Y6/F9 fillers keep quotas. All clauses have three distinct names; auxiliaries and copies are disjoint, so no duplicates. Since D forces the three padding ports false and has a compatible witness, existentially eliminating D from every group reproduces exactly the three original binary conditions. Ternary fillers always have witnesses. Hence G SAT iff H SAT. All source names remain signed 2P2N. Source incidence 2b+3t=4n yields 3m_G=4n_G as a check.

## Exact variable-slot rank tariff

In any **independent local-block** incidence-preserving construction with R disjoint source copies and C ternary output clauses per source clause, the fresh variables in a width-w block must satisfy

\[
3C-Rw=4a_w,\quad w\in\{2,3\};\qquad R=4(a_2-a_3).
\]

Thus any such uniform record-slot architecture requires R divisible by four, and the binary block necessarily contains R/4 MORE fresh variables than the ternary block. Three-port grouping also requires R divisible by three; R=12 is the first compatible positive replication factor in this architecture. Actual numbers: 3*1064-2*12=4*792 and 3*1064-3*12=4*789. This statement is restricted to block-disjoint, signed-occurrence preserving local compilers; no global gadget impossibility is claimed.

Although output clause-record q maps directly to source clause floor(q/1064), the j-th block's dense fresh-variable base is

\[
12n+789j+3\#\{i<j: |C_i|=2\}.
\]

The prefix **binary-width rank** requires paid source reads or an acquired rank/select index. A naive fresh prefix rescan per guest bit query incurs up to Theta(m) source-record probes. **New independent arbitrary-record oracle check:** [bitlocal317.py](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_317/bitlocal317.py) compared each of all 13,832 output clause records against separately built source-indexed clauses, with **zero mismatches**. Under its explicitly uncached arbitrary-query protocol it performed **82,992 source clause-width prefix inspections**, **13,832 individual source-clause reads** and **13,676 fixed-gadget record lookups**. An ordered sweep can reuse a rolling prefix rank; this measured cost is NOT a lower bound on arbitrary future guest query patterns nor a native FLMV TM count. A full eager child copy retained for a guest occupies Theta(M) actual host writable bits plus translator/index/caches, not a free read-only guest tape. Therefore neither polylog arbitrary output-bit access nor FLMV half-power guest workspace follows from the uniform 1,064 clause slots.

## Same-original SAT+UNSAT and S/U controls

Construct valid signed balanced width-(2,3) H from the canonical F9: replace positive F9 clauses (1,5,6) and (2,3,8) by (1,2),(5,3),(6,8), leaving its other ten source clauses. F9 has 70 models. H has 9 variables, b=3,t=10, exactly 37 full models, independently enumerated across all 512 complete assignments. Same-original coherent pins pS={x1=0,x2=1,x3=0,x4=0,x5=1} give 6 satisfying completions; pU={x1=x2=x3=x4=x5=0} give 0. Exact source-pair local extremes SS/SU/US/UU: all 264 F9 modes and all 312 H modes passed brute-force checks. H endpoints 0^9 and 1^9 respectively have four-category true-literal-count histograms (7,0,0,6) and (6,0,3,4), neither is an UNSAT proof. Eight malformed source grammars reject.

The standalone producer emitted G(H) with **10,374 variables and 13,832 original signed pure-ternary clauses**, checked all 2P2N quotas and duplicate-free properness. A 10,374-bit satisfying witness satisfies ALL 13,832 compiled clauses. A separately implemented Python verifier imported no producer functions, reconstructed U198's UNSAT source certificate, checked D's SAT source witness, and repeated all the original source SAT/UNSAT, S/U and malformed checks. The complete executables, compiled formula, witness, SHA256 and source proof appear in the downloadable reproducibility archive. Compiled UNSAT was logically proved by the port quantifiers, not incorrectly claimed as 2^10374 brute-force enumeration.

## Full resource and FLMV ledger

For every adaptive node z, charge grammar/source/index/head, acquired policies including failed and switched candidates, GF(2)/matroid/cut and proof verification, all cache/rank discovery and replay, child/output/bit translation, and every guest step. Total recursion includes the sum over **all evaluated** children; peak writable/index space is the maximum *simultaneously live* ancestor/certificate/matrix/translator/guest/index/cache/temporary buffers. XOR logical flux is OFFLINE unless actually computed by the solver. Native FLMV indexed moves erase index *contents* but still charge all set-up/head operations. Arbitrary DELAY/COPY/RECOMP guests are hostile. The complete fallback decreases number of free source variables but can be exponential, even if signed delta increases.

Previously independently verified FLMV Theorem5.7 values: d*(6/5)=23/45 and d*(241/200)=11642479/23232400, k=2 uniquely maximizing. A desired model-matched transport from hypothetical (time,space)=(6/5,1/2) needs (6/5)a+rho<241/200 and a/2<11642479/23232400; at a=1, rho<1/200 and a<1.00226227165. The rank-rescan implementation does NOT meet that access guarantee. Ordinary SAT to promised signed-balanced mixed-width is missing; unknown-exponent arbitrary-decider power-short A->Phi(A), canonical children and strict numerical same-machine FLMV transport remain OPEN. NP-completeness alone proves none of these.

## Preflight, prior work and safeguarding

First read 01:48 integrated five-role handoff (blob 668212dfa2eff3bdd639563e5308ea4be5e8b549), 01:44 saturated-cycle-affine theorem (blob 3c05146b10ffd597f922f395c967dd4b2dd89875), then latest issue 3 and roles 1–5, AGENTS, CODEX and pnp-research skill. Project GitHub searches: LOCAL-COOK-MONOTONE22STAR1, signed 2P2N first leg, U198 critical clause pad binary, index tape erased guest. Separately github.com/openai searched SAT Lean indexed machines. Primary literature: Döcker 2019 arXiv:1912.08032; FLMV JACM 2005 DOI 10.1145/1101821.1101822; Berman-Karpinski-Scott ECCC TR03-022. Prior LSPV-5 REFEREE256/257 had rejected **minimum one-variable raw-cofactor closures**, a different architecture; no conflict or novelty-by-search-absence claim. Source U198 canonical fixture was found after tmp/doecker61_source.txt returned GitHub 404.

**Root main.tex readback failure:** fetched blob SHA 61d2911f67f5da729e0fa02ad4f8a01732674306 but the GitHub connector returned EMPTY content. No LSPV-4 marker edit or potentially destructive overwrite was attempted; root reconciliation PENDING. All five existing identities, titles, enabled statuses and hourly Pacific stagger are preserved. Report, code and summary are published under LSPV4 ownership with exact GitHub readback; issue 3 and handoff notified. **P versus NP OPEN.**

END_OF_VERIFIED_REPORT::LSPV-4::TRIPLE_HOLE_FIXED_RECORD_BRIDGE317::P_VS_NP_OPEN

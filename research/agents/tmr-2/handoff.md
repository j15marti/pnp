# TMR-2 CURRENT handoff | 2026-11-15 11:19 PST | DYNAMIC-PREFIX-RANK050 /050

**GOVERNING FIRST:** SAT compression/circuits directive on main SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a; replaces Allender-first and fusion-first priorities. Track A dynamic multi-cut/representation and DISJ hostile controls. Five existing identities, Pacific hourly schedules, ownership and enabled states unchanged. P versus NP OPEN.

**NEW PROVED/RESTRICTED (peer review OPEN):** Exact strict proper-3CNF family E_k on 2k+3 variables and 7+3k 3-literal clauses. A seven-clause global pin gadget P forces z=a=b=0; k equality pairs constrain x_i=y_i and k pin clauses constrain x_i=0, giving exactly one full assignment (allzero). On fixed x:y partial assignment evaluation matrices, BAD prefix order (equality first) produces exact Q/GF2 rank 2^k, while GOOD order (x pins first) has **rank one at every prefix**. Every full assignment cut of unique-solution formula is rank one. Fixed all-input correct SAT decider checks allzero in O(N) time, O(log N) space on this family, with exhaustive fallback elsewhere. Strict ternary DISJ D_k retains rank 2^k and 3^k witnesses after every ordering but admits O(k) circuit and same cheap SAT path. Explicit width-three cube Q3/Petersen all-negative Horn graph controls preserve ranks; reported Q/GF2 cuts Q3 [7,7,6], Petersen [6,12,11]. Walsh H D H^T has Q rank2 but GF2 rank1: H not invertible GF2.

**COMPUTATIONAL:** The published self-contained JS was actually executed in V8 with BigInt exact fractions and separate GF(2) bit-row elimination; EQPIN k=1..5 complete sources exhaustively verified unique, DISJ rank and counts k=1..5, 6 specified graph cuts, a field-change falsifier. Zero failed assertions. Dynamic rank is evaluated on fixed-formula assignments, NOT SAT decision on encodings or a necessary physical computation. Benchmark full matrices are exponential-memory intentionally and are NOT the witness solver.

**FILES:** 
- research/agents/tmr-2/2026-11-15_1119_TMR2_DYNAMIC_PREFIX_RANK_ORDER_FIREWALL050.md
- experiments/tmr/tmr2_dynamic_prefix_rank050.js (blob 9a527541ee4d0432cc949ae43730a6d42bc4fcac)
- results/raw/tmr/2026-11-15_1119_TMR2_DYNAMIC_PREFIX_RANK050_V8_RAW.json (blob 7e7dd0913f1b49f97808c5bac3332855fa87124b)
- this full-history-preserving handoff.md.

**FOUR GATES:** DISJ PASS as falsification of rank-to-general-circuit transfer; relativization N/A for scoped rank identities, nonrelativizing transfer OPEN; simultaneous DTISP N/A for rank, unrestricted transfer OPEN; configuration-counting PASS only as time upper-bound guard. No unrestricted P vs NP inference.

**PEER HANDOFF:** TMR-4 analyze whether an exact rank/width transfer can survive only for fixed-order OBDDs; TMR-3 charge same-execution time/space of any implied machine; TMR-5 independently reproduce the 7-clause pin gadget and unique-solution order gap; TMR-1 preserve Track C algorithmic premises and distinguish #SAT and SAT. Explicit all-zero shortcut must remain legal.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE:** proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 visible; proof2 SHA 930c5eeddafce656717f28055a7a9a755f44737c and main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 body not independently recovered (connector empty), so no root write. Repository preflight/CI and native Node CLI not executed; hosted V8 used. /341 FAIL full UNSAT, /386 RESTRICTED. P versus NP OPEN.

**NEXT:** Prove fixed-variable-order OBDD width >= Q rank of a declared communication matrix at matching cut, with an exact same-realization node/edge ledger and DISJ as a *restricted* expected-hard control. Show why unrestricted circuits evade it.

END_OF_HANDOFF::TMR2::2026-11-15_1119_PST

---

# TMR-2 CURRENT handoff | 2026-11-15 10:07 PST | ALLENDERGUARD049 /049

**GOVERNING FIRST:** 2026-11-15 Allender MajMajSAT integration directive, blob 1760aefab5944a063f64b62142e358fbd2b94235. Existing TMR-2 identity, hourly PST schedule, ownership and other four TMR agents unchanged. P versus NP OPEN.

**NEW PROVED/RESTRICTED, independent mathematical review OPEN:** Inherit TMR-1/049 and Allender Section 3.2 unique-extension balancing, and give a **literal CNF** implementation without uncharged new counted variables. For an ell-outer/n-inner circuit C with g functional Tseitin gate variables Z, let T_C consist of gate equivalences plus output=1 and define G_C=(AND_{D in T_C}(t OR D)) AND (NOT t OR b1 OR OR_j z_j). Exact fixed-outer count H_a=2^(n+g)-2^(n-1)+S_a of 2^(n+g+1), so **both inclusive majority blocks and ties** survive; normalized bias shrinks by 2^-(g+1). At most 4g+2 clauses and 17g+4 literal occurrences, max width max(4,g+2). Streaming generator bit-length O(g log V), O(log V) auxiliary workspace under explicit append-only/read-only interface, excluding materialized query.

**NEW SHARP FIREWALLS:** (1) Both existential SAT(G_C) and SAT(NOT G_C) are YES for **every** source circuit, using fixed selector witnesses. Direct SAT answers reveal zero majority information. (2) For g>=3 NO 3-CNF over the same variables represents G_C, because t=1 restricts it to prime (g+1)-literal OR. More sophisticated 3CNF counted gadgets OPEN. (3) Minimal n=g=1 tie C=b1 gives H=4/8 inclusive YES; add one counted forced-zero variable and the same 4 solutions become 4/16 NO. Post-balancing unique-extension CNF re-encoding breaks majority. These are mathematically exact scoped claims, not an assertion no MajMajSAT-to-SAT reduction exists.

**V8 EXECUTED:** 108 exact gate circuits, 324 fixed-outer cases, 7,056 unique-extension checks, 14,112 CNF evaluations, 64 width-three clause attempts, 22,638 assertions, **zero failures**. Finite tests COMPUTATIONAL; standalone Node and independent mathematical review OPEN. Real SAT machine tariff/same-system transfer OPEN.

**PUBLICATION:** research/agents/tmr-2/2026-11-15_1007_TMR2_ALLENDER_GUARDED_CNF_FIREWALL049.md; experiments/tmr/tmr2_allender_guarded_cnf049.js; results/raw/tmr/2026-11-15_1007_TMR2_GUARDEDCNF049_V8_RAW.json; results/raw/tmr/2026-11-15_1007_TMR2_GUARDEDCNF049_RESOURCE_LEDGER.json; this handoff. Branch/merge and full readback verification REQUIRED.

**PEER QUANTITATIVE HANDOFF:** TMR-3/4 charge exact materialized/virtual input access and all writable space, preserve the shrunken bias (not bounded-error by assumption), test compact circuit re-encoding. TMR-5 verify prime implicate width and minimal one-variable tie break independently. TMR-1 retain LCH2 -> MajMajSAT original reduction direction, and separate from any hypothetical MajMajSAT -> SAT compiler. Allender small-space unbounded-error theorem KNOWN; quantum extension bounded-error only. /341 full logical authority FAIL; /386 RESTRICTED.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 full blob 930c5eeddafce656717f28055a7a9a755f44737c; main.tex full blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. All five scheduled agents unchanged. P versus NP OPEN.

**NEXT:** A genuinely decision-preserving, exact and fully charged MajMajSAT to SAT-oracle reduction, or a sharply delimited black-box no-go; no assumption that counting threshold equals existential SAT.

END_OF_HANDOFF::TMR2::2026-11-15_1007_PST

---

# TMR-2 CURRENT handoff | 2026-11-15 09:18 PST | CARTESIAN048 /048

**GOVERNING:** Approved 2026-11-14 Fusion-Lipschitz tariff directive, first-read blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. TMR-2 identity/title, ownership, five enabled Pacific hourly schedules unchanged. P versus NP OPEN.

**NEW PROVED/RESTRICTED, independent mathematical review OPEN:** For r>=2 disjoint odd-charge circular-ladder proper 3CNF sources B_m (m>=2) in one honest signed binary source F_(r,m), each copy has q=48m original sign positions. Every tuple of ONE independently chosen sign per copy yields a valid SAT mutant, so q^r explicit r-bit SAT alternatives exist. Yet no single source *sign* flip makes the whole formula SAT. For any correct total deterministic SAT decider with ONE authentic local binary original-source head, observed-read history R leaves u_i unread critical signs in copy i. The exact Cartesian-mutant read-hitting number is p_SEP=min_i u_i; additional exact components p_FUS=1[all u_i>0], p_Interface=product_i u_i. The authentic zero-price VIEW quotient preserves all three and every correct rejecting HALT has all zero. A genuine physical scan's last-first-copy sign read jointly discharges (SEP,FUS,Interface)=(1,1,q^(r-1)) in ONE paid transition. The COMPLETE three-coordinate nonnegative tariff cone is lambda_SEP+lambda_FUS+q^(r-1)*lambda_Interface<=1. Initial (q,1,q^r) has exact primal/dual optimum **q=48m**. Every correct total decider must visit all q original signs in AT LEAST ONE component. True same-system local-head physical read lower bound, not superpolynomial. Gaussian elimination and separator DP decide this family polynomially. r=m gives superpolynomial q^r semantic SAT mutants but only q tariff.

**EXECUTED PUBLISHED V8:** m=2..6,r=2..6, 25 pairs, **781,024 assertions, 0 failures**, 11,616 actual independently constructed SAT mutants (all 9,216 pairs at r=m=2), 159,504 physical source-read effects, 159,504 zero-change ledger VIEW controls, 20,480 exhaustive original component assignments; native physical TM compiler absent. Symbolic theorem pending peer math review.

**PUBLISHED paths (branch readback then merge/readback required):**
- research/agents/tmr-2/2026-11-15_0918_TMR2_CARTESIAN_HIGHER_ORDER_MUTANT_TARIFF048.md
- experiments/tmr/tmr2_cartesian_mutant_tariff048.js
- results/raw/tmr/2026-11-15_0918_TMR2_CARTESIAN048_V8_RAW.json
- results/raw/tmr/2026-11-15_0918_TMR2_CARTESIAN048_TARIFF_MATRIX.json
- preserved previous full handoff.md (this file)

**PEER QUANTITATIVE HANDOFF:** TMR-3/4 audit authentic price-one joint (1,1,q^(r-1)) row, all paid rereads and direct physical-read dual. TMR-5 independently replay sign tuple witness, source validity, and all-unread trace contradiction. TMR-1 keep strict one-original-head and polynomial affine-shortcut guards. The near-q-Horn 2P2N radius remains restricted; /341 full authority FAIL, /386 RESTRICTED.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** proof1 original full SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 authentic full SHA 930c5eeddafce656717f28055a7a9a755f44737c; canonical main.tex full SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. All existing five schedules untouched. P versus NP OPEN.

**NEXT:** Test source-observation certificates after all algebraic, definitional, shared circuit and family-recognition shortcuts; require physical read-transfer separately from computation lower bound.

END_OF_HANDOFF::TMR2::2026-11-15_0918_PST

---

# TMR-2 CURRENT handoff | 2026-11-15 08:20 PST | SIGNFUSION047 /047

**GOVERNING:** 2026-11-14 Fusion-Lipschitz five-agent directive SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; TMR-2 identity/title, five existing hourly Pacific schedules, ownership and enabled states unchanged. P versus NP OPEN.

**NEW EXACT PROVED/RESTRICTED PHYSICAL TARIFF (independent math review OPEN):** On TMR-1/045's honest odd-charge circular-ladder original proper-3CNF F_m (H=4m cubic vertices, 4H clauses, 12H=48m signed literal occurrences, length N_m=Theta(m log m)), every original polarity bit is pivotal: each single-bit flip gives a valid SAT mutant with a connected G-v spanning-tree GF(2) witness. The existence of pivotal signs and completed input trace is historical LSPV-4/499,/506, TMR-2/021 prior art, NOT a new SAT lower bound. What is new here is the simultaneous seven-vector **all-correct-total-SAT-program physical fusion tariff** for four nested genuine obligations: p=(0,0,0,unread_vertex_packets,unread_clause_packets,unread_critical_signs,unvisited_source_frontier). Initial p=(0,0,0,H,4H,12H,N_m); completed correct UNSAT goal all zero. Physical microsteps price1 with ONE initially-left local read-only source head; actual zero-price closure identity/VIEW preserving read history.

**EXACT COMPLETE ALL-STEP CONE AND DUAL:** A genuine single vertex-last source-bit read has signed four-active discharge (1,1,1,1) for ONE paid step. All other genuine rows discharge subsets of these four or zero. Therefore exact all-state nonnegative cone is lambda_FUS+lambda_Gamma+lambda_Interface+lambda_Machine<=1. Initial exact optimum **N_m**, primal lambda=(0,0,0,0,0,0,1), exact dual y=N_m on the vertex-last row. Four correlated scales CANNOT be added as separate unit tariffs. Same-system all-correct-decider source acquisition lower bound is linear N_m, not superpolynomial; arbitrary programs/GF2/circuits/learning/rereads remain fully allowed.

**EXECUTED FINITE V8:** m=2..15, 5,712 signed one-bit SAT mutants explicitly witnessed via graph-minus-vertex tree construction, 42,796 exact first-read tariff rows, 4,096 exhaustive original assignments at m2; **358,102 assertions, zero failures**, plus 700 identity/revisit bookkeeping checks (not compiled TM). Scientific tests COMPUTATIONAL, all-m symbolic theorem peer review OPEN. The source has bounded primal treewidth <=17 and polynomial affine shortcut, a deliberate hostile easy control. /341 FAIL full logical authority, /386 RESTRICTED.

**PUBLISHED paths:**
- research/agents/tmr-2/2026-11-15_0820_TMR2_PHYSICAL_SIGN_FUSION_TARIFF047.md
- experiments/tmr/tmr2_sign_fusion047.js
- results/raw/tmr/2026-11-15_0820_TMR2_SIGN_FUSION047_V8_RAW.json
- results/raw/tmr/2026-11-15_0820_TMR2_SIGN_FUSION047_TARIFF_MATRIX.json
- preserved historical handoff.md (this file)

**PEER QUANTITATIVE HANDOFF:** TMR-3/4 add the cost-one physical vertex-last joint row and enforce lambda_FUS+lambda_Gamma+lambda_Interface+lambda_Machine<=1; TMR-5 independent mutant proof and width-17 decomposition audit; TMR-1 retain physical all-decider transfer and polynomial family-recognizer ceiling. No all-program superpoly initial potential or alternate-port transfer; P versus NP OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; authentic full proof2 SHA 930c5eeddafce656717f28055a7a9a755f44737c; root full main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. No agent schedule changes.

END_OF_HANDOFF::TMR2::2026-11-15_0820_PST

---

# TMR-2 CURRENT handoff | 2026-11-15 07:08 PST | BATCH116 /046

**GOVERNING:** User-approved Fusion-Lipschitz five-agent refocus, original main SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. TMR-2 identity, title, hourly Pacific schedule, five roles and ownership retained. P versus NP OPEN.

**NEW PROVED/RESTRICTED EXACT GENERAL THEOREM, independent mathematical review OPEN:** In a separately qualified *preauthenticated shared-gate record calculus* on the original TMR-2/045 overlapping Feistel CNF scales j=5..m (rank R_j=4^j), globally paid gate set P, pending scale set U, paid nonterminal ACTIVATE_BATCH(S) for S in an explicit covering family E, and separate paid HALT, dynamic per-scale component p_j=(4^j-1)1[j in U] is exactly invariant on authentic free VIEW SCCs. Each batch discharges precisely its still-pending scale ranks. The **complete nonnegative tariff cone** is lambda_GAMMA<=1, lambda_MACHINE<=1 and sum_(j in S)(4^j-1)lambda_j<=1 for every allowed batch S. The exact optimal initial linear-tariff potential is **G+1+tau_fractional(E)** by fractional set-cover LP duality, while exact required record work is **G+1+tau_integer(E)**. These can differ.

**NEW STRICT EXACT GAP:** Seven Fano-plane batches on seven shared nonlinear interface scales have tau_fractional=7/3 via theta_j=1/3 and y_batch=1/3, while true minimum batch count is 3. Thus potential G+10/3 < true record cost G+4; any linear tariff is intrinsically non-exact even for the authenticated model. Three-scale triangle gives 3/2 versus 2; genuine full-batch shortcut forces tau*=1, exactly the original TMR-2/045 authority. General covered q-scale hypergraphs satisfy tau*<=q, so with G_m=O(m^3), q=m-4 this entire candidate cannot provide superpolynomial initial tariff.

**EXECUTED computational evidence:** Exact self-contained V8 source 62,102 assertions, 24,730 genuine legal tariff edges, 12,560 zero-cost edges, four batch families, zero failures. Exact rational integer-numerator primal/dual and exhaustive finite pending/paid/goal state checks. No physical multitape implementation/OS Node/preflight. Report research/agents/tmr-2/2026-11-15_0708_TMR2_FRACTIONAL_BATCH_FUSION_COVER_GAP046.md; executable experiments/tmr/tmr2_fractional_batch_fusion116.js; raw results/raw/tmr/2026-11-15_0708_TMR2_BATCH116_V8_RAW.json; complete seven-column-expanded-per-scale matrix results/raw/tmr/2026-11-15_0708_TMR2_BATCH116_TARIFF_MATRIX.json.

**GUARDS / TRANSFER:** This is a deliberately different restricted record authority, NOT a modification of TMR-2/045 and NOT an all-SAT-machine lower bound. A real full activation, compact shared circuit, affine Gaussian/definition/learning, equality, Horn/2-SAT, treewidth, autarky, rereading, caching, and recomputation remain MAY in physical machines. Fixed correct total SAT decider recognizes the original family and constructs a polynomial witness. Same-system machine transfer and superpoly gap OPEN. /341 full-language logical FAIL, /386 RESTRICTED. All five schedules untouched.

**PEERS:** TMR-3 audit batch charging and global shared-gate ledger; TMR-4 replay primal/dual exact cone and zero-cost quotient, retain any real full-batch MAY; TMR-5 independent Fano/triangle dual and integral-cover gap; TMR-1 prevent model substitution into SAT-machine theorem. **TRACKERS REVIEWED; NO MATERIAL CHANGE** (proof1 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 930c5eeddafce656717f28055a7a9a755f44737c; main 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). P versus NP OPEN.

**NEXT:** Find a program-independent computational obligation, not a declared batch service, that survives all authentic compact/fused SAT decider operations.

END_OF_HANDOFF::TMR2::2026-11-15_0708_PST

---

# TMR-2 CURRENT handoff | 2026-11-15 06:09 PST | MULTISCALE105 /045

**GOVERNING:** Fusion-Lipschitz five-agent directive on main, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. No task/role/schedule changes. P versus NP OPEN.

**NEW PROVED/RESTRICTED, peer mathematical review OPEN:** Explicit growing source F_m for m>=5, proper signed 3-CNF, globally structural-hashed shared AND/XOR gate DAG, common original X,Z, overlapping nested scales j=5..m, each with nonfactorizing nonlinear two-shear permutation interface and exact rational rank/one-rectangle-cover 4^j. Each scale is simultaneously projectable because all other scale gates admit unique extensions for every X,Z; all scale sources have a single polynomially constructible witness. The circuit size is G_m<=sum_(j=5)^m(2j^2-2)=O(m^3); actual global sharing verified. Scale ranks are correlated and cannot be multiplied.

**COMPLETE RESTRICTED RECORD COST AND NONTERMINAL TARIFF:** Authenticated (F_m,DAG,P,a,h,view) with reversible zero-cost VIEW SCC, one-price CHECK_ID for each truly distinct gate, one-price **nonterminal** ACTIVATE only after all checks, and one-price HALT. Seven-vector p=(0,0,(1-a)S_m,1-a,G_m-|P|,0,h), S_m=sum_(j=5)^m(4^j-1)=(4^(m+1)-4^5)/3-(m-4). ACTIVATE discharges **all** S_m rank units in ONE PAID nonterminal step while h=1, without any shared gate being double-counted. Exact cone lambda_Gamma<=1; S_m*lambda_SEP+lambda_FUS<=1; lambda_machine<=1; lambda>=0. Exact initial LP optimum **G_m+2**, attained by weights (0,0,0,1,1,0,1) and G_m CHECK + ACTIVATE + HALT. For individually weighted scales, sum_j (4^j-1)*lambda_j+lambda_FUS<=1, so **total rank sector<=1**, no exponential or superpoly joint tariff. A uniform positive raw rank weight fails. This is NOT an unrestricted SAT-TM work result.

**INDEPENDENT CHEAP REAL DECISION PATH:** Canonical family is polynomial-time printable and recognizable; one fixed total correct SAT decider can compare input against all poly-many possible generator indices <= input length, emit a known witness on match and otherwise use exhaustive fallback. This recovers the earlier LSPV-1/392 recognized-family patch principle and is not a new general SAT algorithm.

**EXECUTED and READ-BACK SOURCE:** experiments/tmr/tmr2_multiscale_activation105.js, blob 5765946d4ac916ad6c529de51b688643a9e63516. Fresh V8 replay **179,822 assertions, zero failures**, m=5..9, exact per-scale projections through j=7, whole-source m=5,6 exhaustive; other sample controls, all checks COMPUTATIONAL. Gate counts 48,107,186,288,416; actual record costs 50,109,188,290,418. Report research/agents/tmr-2/2026-11-15_0609_TMR2_OVERLAPPING_FEISTEL_NONTERMINAL_ACTIVATION045.md; raw results/raw/tmr/2026-11-15_0609_TMR2_MULTISCALE105_V8_RAW.json; matrix results/raw/tmr/2026-11-15_0609_TMR2_MULTISCALE105_TARIFF.json. Each artifact needs main-readback after merge.

**PEERS:** TMR-3 review physical implementation and sharing cost, TMR-4 the coupled exact rational LP and authentic nonterminal ACTIVATE MAY, TMR-5 independent projection/zero-SCC/shortcut replay, TMR-1 audit fixed-family machine quantifiers and same-system bridge. /341 full logical UNSAT authority FAIL, /386 RESTRICTED. No all-decider SAT transfer, no superpoly initial potential. **TRACKERS REVIEWED; NO MATERIAL CHANGE:** proof1 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 authentic complete blob 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic complete blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Five existing schedules untouched. P versus NP OPEN.

---

# TMR-2 CURRENT handoff | 2026-11-15 05:14 PST | FEISTEL096 /044

**GOVERNING:** Fusion-Lipschitz directive blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; TMR-2 identity, title, hourly Pacific schedule, all peers untouched. P versus NP OPEN.

**NEW PROVED/RESTRICTED symbolic theorem, independent mathematical review OPEN:** For every m>=5, explicitly construct a signed proper 3-CNF on exactly 4m^2-2 variables and 9m^2-m-8 clauses, encoding a 2m-bit, genuinely coupled reversible nonlinear two-shear mapping with 2m^2-2 shared AND/XOR gate identities, N_m=Theta(m^2 log m). Exact existential input/output matrix is a permutation matrix of rational rank and all-one-rectangle-cover **2^(2m)**. Unlike previous TMR-2/043 NAE block products, the projected graph has FULL affine hull GF(2)^(4m), fails Horn/dual-Horn/bijunctive/affine closure, has a connected essential input/output dependency graph and no disjoint-coordinate block decomposition. The original source has K_m primal clique and treewidth at least m-1, no pure variables; both all-zero and all-one assignments fail. All statements proved symbolically, peer review OPEN.

**REAL POLYNOMIAL UNIFORM SAT COUNTERCONTROL:** One fixed correct total decider recognizes the exact canonical family, constructs a satisfying witness with about half the X bits set, verifies the entire CNF, and falls back to exhaustive SAT outside the family. Genuine polynomial shared circuit and witness invalidate any supposed compulsory SAT-decision work inferred solely from exponential projected rank and those structural properties. Arbitrary renamings/sign flips preserve satisfiability but the published recognizer's polynomial claim is canonical only.

**EXACT RESTRICTED TARIFF:** Separate preauthenticated GATE-CHECK record system with free reversible VIEW/NOP, one paid unique-gate CHECK, mandatory G=2m^2-2 identity checks, and paid terminal HALT. p=(0,0,(2^(2m)-1)h,0,G-|P|,0,h). Exact cone lambda_GAMMA<=1 and (2^(2m)-1)lambda_SEP+lambda_MACHINE<=1; optimum G+1, dual authentic G CHECK+1 HALT. Uniform positive rank weight FAILS via HALT. No model transfer to physical SAT lower bounds.

**EXECUTED AND PUBLISHED:** Identical V8 audit function serialized to experiments/tmr/tmr2_dense_feistel096.js: **16,088 assertions, zero failures**, exhaustive 1,024/4,096 graph inputs and full affine hull checks for m=5/6; structural and sampled checks through m=9. Raw results/raw/tmr/2026-11-15_0514_TMR2_FEISTEL096_V8_RAW.json. Tariff results/raw/tmr/2026-11-15_0514_TMR2_FEISTEL096_TARIFF.json. Full proof research/agents/tmr-2/2026-11-15_0514_TMR2_DENSE_NONLINEAR_FEISTEL_FIREWALL044.md. Finite COMPUTATIONAL, symbolic PROVED/RESTRICTED, peer review OPEN, physical compiled machine not run.

**NEXT:** TMR-3 charge a physical parser/witness path; TMR-4 verify exact CHECK/HALT LP and preserve compact-circuit MAY; TMR-5 independently audit all-m affine-hull and nonproduct proof; TMR-1 keep all-decider transfer OPEN. TMR-2 seek dynamic history-dependent obstruction surviving *all* these shortcuts. /341 logical UNSAT FAIL full language, /386 RESTRICTED.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1 full SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; authentic proof2 full blob SHA 930c5eeddafce656717f28055a7a9a755f44737c; authentic root main.tex full blob SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Five schedules untouched. P versus NP OPEN.

---

# TMR-2 CURRENT handoff | 2026-11-15 04:20 PST | NONLIN093 /043

**GOVERNING:** Fusion-Lipschitz directive SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6, TMR-2 identity and all five Pacific hourly schedules preserved. P versus NP OPEN.

**NEW PROVED/RESTRICTED symbolic theorem, independent mathematical peer review OPEN:** For k=3b>=3, augment TMR-2/042's entire nonpeelable proper-3CNF R_k by b disjoint original-variable NAE3 constraints on X triples to get S_k. Signed incidence degree>=2 for EVERY variable, source primal K_k/treewidth>=k-1, all source clauses width three; encoded L=Theta(k^2 log k). Its exact existential X/Y projection is y_i=not x_i AND b disjoint NAE3(X) blocks, which is now **non-Horn, non-dual-Horn, non-bijunctive and non-affine even after projected affine anti-equality elimination**, unlike R_k's affine projected relation. Rank_Q and exact one-rectangle cover are both **6^b**. NAE3 has full affine hull, so Gaussian alone cannot eliminate the nonlinear blocks.

**LEGAL POLYNOMIAL SHORTCUT:** A fixed correct total SAT decider parses and authenticates the high-degree signed NAE triple partition, signed-twin and guarded u/a/b motifs, chooses each three-high NAE witness locally, reconstructs all remaining signed variables in constant-size checks and verifies the ENTIRE CNF, with exact exhaustive fallback otherwise. Canonical, renamed, sign-flipped, shuffled, duplicate-padded S_k recognized. All operations physically chargeable polynomially in L; no uniform worst-case polynomial SAT algorithm claimed. Disjoint NAE blocks and compact shared representation defeat compulsory rank-based work.

**NEW EXACT RESTRICTED RECORD TARIFF:** Typed authenticated CHECK-one-disjoint-NAE-block record calculus with paid price1 per CHECK and free VIEW/NOP/GOAL, all b AND obligations required. p=(0,0,6^v-1,0,v,0,0) for v unchecked. CHECK row Delta=(0,0,5*6^(v-1),0,1,0,0), others zero. Fixed-b exact rational cone 5*6^(b-1)*lambda_SEP+lambda_Gamma<=1, initial LP optimum **b** attained by (lambda_SEP,lambda_Gamma)=(0,1) and b real checks. Uniform positive rank weight FAILS. Different physical terminal-masked source rank also fails at genuine cost-one HALT. This is NOT a physical machine transfer.

**EXECUTED/PUBLISHED:** Exact audited V8 function serialized as experiments/tmr/tmr2_nonlinear_projection093.js, 5,004 assertions/zero failures; 4,160 exact locally independently eliminated projection matrix cells, 112 renamed/signed/shuffled/duplicate controls, k=3,6,9,12 and symbolic rank proof; 10 record tariff rows. Raw results results/raw/tmr/2026-11-15_0420_TMR2_NONLIN093_V8_RAW.json. Tariff JSON results/raw/tmr/2026-11-15_0420_TMR2_NONLIN093_TARIFF.json. Report research/agents/tmr-2/2026-11-15_0420_TMR2_NONLINEAR_PROJECTED_NAE_RANK_FIREWALL043.md. Finite tests COMPUTATIONAL; physical SAT machine binary and OS Node not executed.

**PEER/NEXT:** TMR-3 charge genuine physical recognizer/witness verification; TMR-4 replay exact CHECK cone, retain all cheap legal MAY paths; TMR-5 independent projected-rank and signed recognizer review; TMR-1 no illicit system transfer. Next TMR-2 seek a truly nonfactorizing dynamic fusion obstruction after affine, local-NAE, autarky, circuit and sharing quotients. /341 full FAIL, /386 RESTRICTED. Superpolynomial gap, unrestricted same-system transfer and P versus NP OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 full Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex full Git blob SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Root files and all five schedules unchanged.

---

# TMR-2 CURRENT handoff | 2026-11-15 03:12 PST | NAE2CORE087 /042

**GOVERNING:** 2026-11-14 fusion-Lipschitz directive SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. TMR-2 identity/title/hourly Pacific schedule and all other existing agents unchanged. P versus NP OPEN.

**NEW PROVED/RESTRICTED symbolic theorem, independent peer review OPEN:** Explicit proper 3-CNF R_k with 3k+3*C(k,2) variables, 4k+6*C(k,2) original clauses, L=Theta(k^2 log k); every signed NAE hyperedge variable has degree >=2 (there is NO legal edge-leaf PEEL), and the canonical TMR-4 leaf core is the entire source. Primal graph contains K_k. Full satisfaction relation is non-Horn, non-dual-Horn, non-bijunctive, non-affine via NAE3 existential projection. Nonetheless exists(Z,U,A,B)R_k(X,Y,...) equals AND_i(x_i!=y_i), with **EXACT rank_Q and 1-rectangle cover 2^k** across X/Y; yet exists(Y,Z,U,A,B)R_k(X,...)=TRUE. Explicit witness x=0,y=1,z=0,u=1,a=0,b=1. A single fixed correct total finite-tape SAT decider recognizes signed NAE twin/guard motifs with polynomially charged parser, deterministic constant-size local witness search, complete source verification and fallback. Source renaming, global variable flips, clause shuffling, exact duplicates preserve the witness shortcut. This extends TMR-2/041's private-leaf control by removing every degree-one variable.

**NEW exact symbolic source-static HALT tariff no-go:** In physical cost-one-per-step deterministic multitape model, authentic cl0 is identity. p=(0,0,(2^k-1)*1[live],0,0,0,1[live]) along every same-source R_k execution, and p(goal)=0. The final genuine paid HALT row is Delta=(0,0,2^k-1,0,0,0,1), price1. Uniform nonnegative tariff requires lambda_SEP=0 and lambda_MACHINE<=1. Rational certificate (0,0,0,0,0,0,1), initial potential 1. A fixed positive SOURCE rank weight FAILS; dynamic history-sensitive alternatives are not excluded.

**EXECUTED/PUBLISHED:** Exact V8 audit() serialized to experiments/tmr/tmr2_nae_2core_gauge087.js, **3,390 checks, zero failures**, k=2..10, 270 seeded complete-variable gauge/renaming recognizer and witness controls, exact BigInt determinants k=2..4, all X witness subsets through 64 per k. Raw results results/raw/tmr/2026-11-15_0312_TMR2_NAE2CORE087_V8_RAW.json. Matrix results/raw/tmr/2026-11-15_0312_TMR2_NAE2CORE087_TERMINAL_TARIFF.json. Report research/agents/tmr-2/2026-11-15_0312_TMR2_NAE_2CORE_RANK_GAUGE_FIREWALL042.md. Finite testing COMPUTATIONAL; no physical TM binary compiled, no superpoly gap or unrestricted transfer.

**PEER/NEXT:** TMR-3 audit charged bounded-loop recognizer; TMR-4 include real witness path in MAY and veto source-static terminal mask; TMR-5 independently replay rank, non-Schaefer projection, signed twin motif; TMR-1 keep same-system gate OPEN. TMR-2 next find a dynamic interface charge that survives no-leaf guarded extensions plus affine/twin reduction, autarkies, learning and compact circuits. /341 FAIL on full accepted language; /386 RESTRICTED. **TRACKERS REVIEWED; NO MATERIAL CHANGE:** proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 recovered full blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, root main.tex recovered full blob SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. Root files and schedules untouched. P versus NP OPEN.

---

# TMR-2 CURRENT handoff | 2026-11-15 02:13 PST | LEAF081 /041

**GOVERNING:** Fusion-Lipschitz directive on main SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; MCSP secondary; all five current TMR identities/schedules retained. P versus NP OPEN.

**NEW PROVED/RESTRICTED, independent peer review OPEN:** Exact signed paired-NAE *edge-leaf* existential quotient: a source-authenticated complementary-clause-pair hyperedge with a variable of remaining incidence degree one can be deleted while preserving the full existential projection on surviving variables; reverse signed-pivot reconstruction extends ANY core witness. For TMR-2/040's proper 3-CNF Q_k, each NAE edge has an initially private variable outside X. Thus **for every X assignment** there is a satisfying Y,W,Z extension, i.e. exists(Y,W,Z) Q_k = TRUE, despite the already proved evaluation matrix rational rank and rectangle cover exactly 2^k and primal clique K_k. The property survives independently chosen per-edge literal signs. Exact rank persistence is asserted only for consistent global variable flips/relabeling, not arbitrary edge gauges.

**NEW AUTHENTIC TYPED RECORD CALCULUS (NOT physical SAT machine):** Complete NAE source authenticated initially, remaining edges U, restore stack S, active flag h. Five legal transition classes: zero NOP, zero phase switch, cost-one PEEL (U decreases, S increases), cost-one RESTORE, cost-one HALT. Reduced product p=(0,0,0,2|U|,|S|,0,h), exact rational lambda=(0,0,0,1,1,0,1). PEEL weighted discharge 2-1=1, RESTORE 1, HALT 1, zero rows 0. Completed goals p=0; minimum record-event cost **2m+1** for m distinct edges, versus initial potential exactly 2m+1. On Q_k, m=k(k+1)/2, so the entire bound remains O(k^2), not superpolynomial. Source parsing, dedup, witness verification, input reads and finite-tape computation are separately charged in a fixed correct total SAT decider with exhaustive fallback, yielding a polynomial upper bound on this family. No arbitrary-machine transfer.

**ACTUALLY EXECUTED:** Exact V8 function serialized to experiments/tmr/tmr2_signed_leaf_autarky081.js: **14,057 assertions**, zero failures; 190 signed/renamed/reordered/duplicate-padded Q_k examples through k=11; 625 exhaustive four-variable signed-edge subinstances; 1200 seeded six-variable signed hypergraphs; malformed, nonpeelable unsatisfiable K5 and modular rank k=2..5 controls. Code, raw and tariff independently readback required.

**FILES:** research/agents/tmr-2/2026-11-15_0213_TMR2_SIGNED_LEAF_AUTARKY_RANK_FIREWALL041.md ; experiments/tmr/tmr2_signed_leaf_autarky081.js ; results/raw/tmr/2026-11-15_0213_TMR2_LEAF081_V8_RAW.json ; results/raw/tmr/2026-11-15_0213_TMR2_LEAF081_TARIFF.json.

**PRIMARY/CORPUS:** Schaefer 1978, Kullmann 2011 autarkies, Ordyniak-Paulusma-Szeider 2013 structural SAT; original TMR-2/040, TMR-5/037, TMR-2/039, LEAD/0029, NAECOMPANION1 and LSPV-2/284; both trackers, main.tex and all five current handoffs. This strengthens a project-specific signed/private-leaf shortcut, not the historically known private-variable trick.

**PEERS:** TMR-3 costed physical compiler; TMR-4 exact typed zero-cost SCC/LP and negative PEEL stack discharge; TMR-5 independently test arbitrary edge signs and double-companion parser; TMR-1 qualify model transfer. **NEXT:** identify a nonleaf nonaffine fusion interface surviving actual cheap quotient and legal shortcuts, then prove a genuinely dynamic all-step bound. **TRACKERS REVIEWED; NO MATERIAL CHANGE**; /341 FAIL full language, /386 RESTRICTED; P versus NP OPEN.

---

# TMR-2 CURRENT handoff | 2026-11-15 01:13 PST | NAERANK075 /040

**GOVERNING:** Fusion-Lipschitz five-agent refocus SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6, MCSP secondary; all five existing schedules/identities untouched. **P versus NP OPEN.**

**NEW PROVED/RESTRICTED construction, independent mathematical review OPEN:** Proper signed 3-CNF Q_k=AND_i NAE(X_i,Y_i,W_i) AND_(i<j) NAE(X_i,X_j,Z_ij) has n=3k+binom(k,2), k(k+1) proper clauses, L=Theta(k^2 log k), primal K_k, no pure variables, neither all-zero nor all-one SAT, and a full satisfaction relation projecting onto NAE_3 (not Horn/dual-Horn/bijunctive/affine). Across X versus all remaining variables, its 0/1 communication matrix has **exact rational/real rank 2^k** and **exact all-one rectangle-cover number 2^k**. Rank proof aggregates all Z with W=0 to the invertible weighted product of B=[[0,1],[1,1]]. Exact 2^k-size fooling set proves rectangle cover.

**Genuine uniform cheap SAT execution:** D deduplicates source clauses, counts occurrences of variables, sets those occurring >2 times to 0 and others to 1, checks the assignment, and else exhaustively solves. The source X each occur 2k times, all U variables twice, so every Q_k and every bijective-renaming/clause-reordering/duplicate-clause variant is accepted in a conservative O((L+1)^8) paid multitape transition upper bound. Therefore any all-step sound rank-only initial potential with fixed coefficient lambda>0 would demand lambda(2^k-1)<=poly(L), impossible for large k. This is a FALSIFIED proposed positive source-rank tariff, not a universal lower bound or full physical transition-matrix proof. Degree witness is a paid shortcut, not a free abstract oracle.

**EXECUTED:** 11,749 assertions, zero failures in exact V8 ES2020 function: rational BigInt rank and complete row sums k=2..4, all fooling pairs k=2..7, witness/class controls including permutations, variable renaming and duplicate source clauses. Source serialized to JS file; standalone Node wrapper not independently executed, no full TM compiled. Original raw is separately preserved. Finite tests COMPUTATIONAL.

**FILES:** research/agents/tmr-2/2026-11-15_0113_TMR2_NAE_RANK_FOOLING_DEGREE_FIREWALL040.md ; experiments/tmr/tmr2_nae_rank_fooling075.js ; results/raw/tmr/2026-11-15_0113_TMR2_NAERANK075_V8_RAW.json ; results/raw/tmr/2026-11-15_0113_TMR2_NAERANK075_AGGREGATE_TARIFF.json.

**NOVELTY LEDGER:** Prior LB-0012/H22-RANK and LSPV-3/GATE323 already refuted generic rank-to-SAT-runtime inference; TMR-2/039 refuted cofactor/interpolant inference. This adds the **simultaneous NAE non-Schaefer + complete primal clique + exact Q-rank + exact fooling cover + renaming-robust degree-witness** control. Historical /341 FAIL full authority; /386 RESTRICTED preserved.

**PEERS:** TMR-3 audit physical time bound, TMR-4 insert paid degree shortcut in MAY transitions, TMR-5 independently check rank/fooling/projection, TMR-1 validate family scope. **NEXT:** find a source-and-history-aware *dynamic* obstruction whose actual processing tariff survives all polynomial witness/circuit shortcuts. Same-system general transfer and superpolynomial initial potential OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

---

# TMR-2 CURRENT handoff | 2026-11-15 00:20 PST | EQUALJ072 /039

**GOVERNING:** 2026-11-14 fusion-Lipschitz directive Git blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6; MCSP secondary, all five existing TMR schedules/identities unchanged.

**NEW PROVED/RESTRICTED, peer review OPEN:** For any UNSAT private CNF F and k>=2, define I_k(X,Y,Z)=EQ_k(X,Y) AND EXACTONE_3(Z), A=AND_{D in CNF(I),C in F}(D OR C), and B as a gate-authenticated O(k)-size Tseitin CNF projecting to NOT I. A and B are separately SAT, jointly UNSAT, and every common-variable Craig interpolant is exactly I_k with O(k) circuit size. Yet I_k has 2^k nonzero, pairwise distinct local X cofactors and is semantically non-Horn, non-dual-Horn, non-bijunctive and non-affine. Restrict X=0,Y=e1,Z=e1 and B private gates to their forced values: the entire source becomes F, so S_RES(A AND B)>=S_RES(F). For F on odd-charge 3-regular expanders, BSW Theorem 4.1/Cor 4.1 gives native Resolution size 2^Omega(k) at guarded L=Theta(k^2 log k), while a fixed total syntax-authenticating SAT machine recognizes the parity contradiction and rejects those same sources in polynomial time. Thus fixed positive local cofactor tariff fails for the direct unrestricted SAT-machine route; the native Resolution result remains restricted. No sound superpolynomial dynamic potential or same-system bridge proved.

**EXECUTED:** Exactly serialized V8 verifier 92,807 assertions, zero failures, k=2..6; B complements authenticated over all shared assignments, A projection and joint UNSAT exhaustively through k=4; corrupted B gates rejected, all cofactor witnesses and source restrictions checked. Finite status COMPUTATIONAL. Files: research/agents/tmr-2/2026-11-15_0020_TMR2_EQUALJ_INTERPOLANT_COFACTOR_FIREWALL039.md; experiments/tmr/tmr2_equalj_guard_cofactor072.js; results/raw/tmr/2026-11-15_0020_TMR2_EQUALJ072_V8_RAW.json. Primary BSW ECCC 1999 p10 screenshot checked. No new proof system or machine theorem claimed.

**PEERS:** TMR-1 verify exact unique interpolation/restriction; TMR-3 validate finite-tape parsing costs; TMR-4 add compact comparator/extension gate MAY rows; TMR-5 independently replay and check the expander length/scoping. **NEXT:** characterize one branch-aware dynamic interface state that assigns cost to already performed, source-specific computation without equating number of local cofactors with actual work. Preserve all cheap parity and equality paths. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** P versus NP OPEN.

---
# TMR-2 CURRENT handoff | 2026-11-14 23:21 PST | COFSEP066 /038

**GOVERNING:** fusion-Lipschitz refocus Git blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. MCSP secondary. Five TMR tasks/schedules unchanged.

**NEW PROVED/RESTRICTED, peer mathematical review OPEN:** Proper 3-CNF F_k on 3k variables with 3k+binom(k,2) clauses, encoded L_k=Theta(k^2 log k), has 2^k pairwise distinct global satisfaction cofactors after assigning X, and a K_k clique on Y, even though all variables occur in both signs and the full relation is semantically non-Horn, non-dual-Horn, non-bijunctive and non-affine. Nonetheless all-one satisfies every clause, and certified Y=Z=1 autarky removes every clause. One fixed complete correct total SAT decider recognizes all-positive-clause inputs in O(L^3), then falls back to exhaustive search. Hence any sound nonnegative all-step potential whose initial raw cofactor component carries lambda_sep>0 must obey lambda_sep*(2^k-1)<=O(L_k^3), impossible uniformly at fixed positive lambda_sep. If autarky elimination is authentically free *with already available certificate* in a separate qualified calculus, closed initial cofactor potential is zero; do not graft free certificate discovery onto physical SAT machine.

**ADDITIONAL ALL-UNSAT FIREWALL:** The full satisfaction relation of every UNSAT formula is zero, so its distinct *global* cofactors count is identically one and minus-one obstruction identically zero. Local pre-AND-join relations remain a separate OPEN target.

**EXACT V8 EXECUTION:** Published ES2020 script 20,682 assertions, zero failures, k=3..30 controls, cofactor signatures exhausted through k=10 and full assignments through k=4. No native TM compilation claimed. Source and original raw stored separately.

**FILES:** research/agents/tmr-2/2026-11-14_2321_TMR2_NONAFFINE_COFSEP_AUTARKY_FIREWALL038.md; experiments/tmr/tmr2_cofactor_autarky_firewall066.js; results/raw/tmr/2026-11-14_2321_TMR2_COFSEP066_V8_RAW.json.

**PEER REQUEST:** TMR-3 charge all-positive grammar/parser/halt path; TMR-4 audit autarky closure versus physical charges and exact tariff row; TMR-5 independently verify semantic non-Schaefer witnesses; TMR-1 retain local-versus-global UNSAT relation distinction. New TMR-2 target is a locally authenticated branch-aware fusion component surviving real cheap mechanisms.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 930c5eeddafce656717f28055a7a9a755f44737c; main.tex 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. P versus NP OPEN.

**PREVIOUS HANDOFF HISTORY PRESERVED BELOW.**

---

# TMR-2 CURRENT handoff | 2026-11-14 22:12 PST | GENCERT063 /037

**GOVERNING PRIORITY:** Fusion-Lipschitz five-agent refocus blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. MCSP/FLMV supporting, all five TMR identities and schedules preserved.

**NEW PROVED/RESTRICTED, independent mathematical review OPEN:** For every total public Boolean f on n immutable hidden individually readable source coordinates, and every compatible partial transcript, D_x is shortest actual source-consistent certificate completion, B=min_compatible_x D_x, and W is optimal worst-case residual online deterministic query depth. On the fixed-source graph the **pointwise greatest** nonnegative all-paid-step 1-Lipschitz goal-zero potential is D_x; on the source-forgetting MAY graph it is B. The authentic paid Bellman envelopes of seed W coincide with D_x and B respectively for **every f**, extending TMR-4/037 and TMR-5/033 beyond AND-of-ORs. Omniscient shortest certificate path does not imply a uniform online algorithm.

**NEW exact universal three-column cone:** Uniformly across ALL total n-bit Boolean f, fixed x and real paid READ edges, a nonnegative weight triple on vector (B,W,D_x) is valid iff lambda_B+n*lambda_W+lambda_D<=1. Sufficiency: each READ drops B<=1, D_x<=1 and W<=n; necessity: OR_n source with first bit 1, first paid READ discharges (1,n,1). Witness (1/4,1/(2n),1/4). Length-independent coefficients across all n force lambda_W=0. At OR_n maximal initial potential 1 versus W=n; all initial potentials <=n, so source-query-only multiscale obstructions cannot produce superpolynomial initial gaps. True independently readable parity-summary hints are changed-model falsifiers, not CEGAR-spurious paths.

**EXACT V8 EXECUTION:** published source re-fetched from branch and executed byte-identically in native V8 isolate: **179,821 checks, zero failures**, all 256 3-input Boolean functions, nine four-input affine/Horn/Krom/equality/ANDOR/majority controls, 7,641 transcripts, 18,688 compatible fixed-source states, 15,768 authentic paid edges, integer-rational three-column witness; OR_n symbolic rows n=1..25. No Node/compiled TM or SAT-model execution claimed; finite evidence COMPUTATIONAL.

**FILES:** research/agents/tmr-2/2026-11-14_2212_TMR2_GENERAL_CERTIFICATE_ENVELOPE037.md; experiments/tmr/tmr2_general_certificate_envelope063.js; results/raw/tmr/2026-11-14_2212_TMR2_GENCERT063_V8_RAW.json; results/raw/tmr/2026-11-14_2212_TMR2_GENCERT063_TARIFF_SCHEMA.json.

**PREFLIGHT:** latest Nov14 refocus FIRST and rechecked, Nov13 replacement, both complete proof trackers and canonical main.tex recovered via authentic Git blobs (proof1 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 930c5eeddafce656717f28055a7a9a755f44737c, main.tex 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34), AGENTS/CODEX/skill, issue #3 and all five handoffs, original TMR-2/036, TMR-4/037, TMR-5/033, TMR-1/037, TMR-3/036, LEAD-0029, scholarly certificate/abstract-interpretation literature. **TRACKERS REVIEWED; NO MATERIAL CHANGE**; root main.tex unchanged. Historical /341 FAIL and /386 RESTRICTED unchanged; P versus NP OPEN.

**PEER:** TMR-4 audit all-function Bellman and n-dependent cone; TMR-3 price correlated simultaneous outputs on one real step; TMR-5 attempt public parity hint and model-transfer counterexample. **NEXT:** source-authenticated original-CNF residual across separators surviving full paid parsing, Gaussian, Horn/Krom, autarky, learning and compact circuit MAY operations. Unrestricted same-system transfer and superpolynomial initial gap OPEN.

**PREVIOUS HANDOFF HISTORY PRESERVED BELOW.**

---

# TMR-2 CURRENT handoff | 2026-11-14 21:13 PST | MMT059 /036

**Controlling fusion directive** `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`; all five TMR schedules/identities retained. MCSP and FLMV remain secondary.

**NEW PROVED/RESTRICTED (independent TMR-3/4/5 review OPEN):** For the *qualified, hidden-indexed-source AND-of-q OR-of-q query protocol*, let W(sigma)=sum of unread fields over active rows (known prior minimax depth q^2 at the initial transcript) and B(sigma)=min(number active rows, minimum unread fields among active rows) (cheapest compatible goal-certificate completion). Genuine free transcript normalization preserves both. Every paid source READ has Delta B<=1 and Delta W<=D_q=q^2-q+1. One *authentic final zero bit read* after q-1 zeros in a row, while other rows remain unknown, achieves Delta(B,W)=(1,D_q) at price1. Therefore the complete exact nonnegative all-step two-column tariff cone is lambda_CNF + D_q*lambda_fus<=1. At initial (B,W)=(q,q^2), the exact maximum lambda-weighted potential is **q**, achieved by (1,0). With weights fixed for all q, lambda_fus=0. This falsifies a direct extension of the unit affine-read minimax-depth tariff to nonlinear Boolean obligations; it is a real paid read, not an invented shortcut, and does NOT contradict prior worst-case q^2 query depth.

**Executable verification:** byte-identical published native CPython script, 329,574 exhaustive checks, zero failures; q=1..3 enumerated all 3^(q^2) partial transcripts and checked 77,022 distinct paid edges at q=3, exact Bellman recurrences and zero/repeat controls. Proper 3-CNF forcing-gadget, equality, affine and compact-circuit controls also tested, though physical Turing-machine soundness is not established.

**Files:** `research/agents/tmr-2/2026-11-14_2113_TMR2_NONLINEAR_MINIMAX_TARIFF_COLLAPSE036.md`, `experiments/tmr/tmr2_minimax_tariff059.py`, `results/raw/tmr/2026-11-14_2113_TMR2_MMT059_RAW.json`, and `results/raw/tmr/2026-11-14_2113_TMR2_MMT059_TARIFF.json`.

**Peer request:** TMR-3 audit charged query edges including repeats; TMR-4 verify closure/LP; TMR-5 test extensions, cheap control algorithms and transfer. **Next target:** a syntax-aware, temporal-order-invariant SAT obstruction surviving affine/learning/compact computation. Same-machine transfer, superpolynomial initial gap and P versus NP remain OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left for TMR-5, all schedule identities preserved.

---

# TMR-2 CURRENT handoff | 2026-11-14 20:23 PST | AFFQUOT055 affine fusion query quotient /035

**GOVERNING DIRECTIVE:** research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. MCSP/FLMV secondary; all five TMR identities/schedules unchanged.

**NEW AFFQUOT055 PROVED/RESTRICTED (independent TMR-3/4/5 review OPEN):** Qualified public affine promise Hx=h over hidden, individually paid-readable binary source coordinates, jointly required affine outputs Bx+c. Let U=row(H), V=row(B), E_Q=observed coordinate span. Define p_aff(C)=min{|R|:V subset U+E_Q+E_R}. This exactly equals the minimum additional distinct **coordinate reads** needed for any correct deterministic adaptive query algorithm on every consistent observation transcript. If insufficient, a kernel witness z gives two allowed sources that agree on all actual reads yet require different outputs. Every authentic zero-cost Gaussian/alias/equivalent-output step preserves p_aff; every paid READ(i) has Delta 0 or 1. Thus lambda_aff=1 satisfies the complete local query tariff and goals have p_aff=0. This is a **restricted source-query model**, not actual Q-TM transition simulation, general CNF solving, /341 or /386.

**FUSION AND HOSTILE CONTROLS:** Two parity outputs x1+x2, x2+x3 have separate costs 2+2 but fused cost 3; free public equality x1=x3 reduces fused cost to 2. Repeated identical output 100 times remains one source read. Public 3-XOR Tseitin 4-clause encoding checked against all 8 assignments for both parities; Horn/Krom/tw1-DP/autarky/equality, padding/renaming controls separately checked. Adding an independently queryable extension bit t=sum(x_i) makes a six-read parity goal one-read **only after changing the source interface**. PARITY_n has p_aff=n and explicit n-read completion; every multiscale potential on this fully queryable affine-only protocol obeying all-step and terminal tariffs is <=n. Hence source-only affine query mass cannot yield superpolynomial initial potential. General SAT/Q-TM same-system bridge **OPEN**.

**RELATION TO PREDECESSORS:** TMR-4/035 already had an exact two-bit parity query system and SCC/LP; TMR-3/034 and TMR-5/031 already falsified occurrence double-counting in shared cache/message updates. New scoped project contribution is general public affine rowspaces, fused multi-output necessary/sufficient query characterization, and explicit linear ceiling. LEAD-0029 already warned that semantic mass and entropy fail. LSPV-3 GATE284's exact-2P2N matching repair rho=|U|-nu(G) remains separately **RESTRICTED** for local radius, not a SAT-work theorem.

**ACTUAL NATIVE CPython:** locally executed /mnt/data/tmr2_affine_quotient055.py, seed 20261114, 1,133 assertions, 0 failures, 90 small affine profile trials, 315 paid rows, 180 free equivalent-row checks, 36 independent separating nullspace witnesses. Published refactored source experiments/tmr/tmr2_affine_quotient055.py was not re-executed byte-for-byte. Raw original native output results/raw/tmr/2026-11-14_2023_TMR2_AFFQUOT055_RAW.json. Full report research/agents/tmr-2/2026-11-14_2023_TMR2_AFFINE_FUSION_QUERY_QUOTIENT035.md. Finite tests COMPUTATIONAL.

**PREFLIGHT:** fusion directive FIRST and rechecked; Nov13 replacement; both trackers (proof1 blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, authentic proof2 blob 930c5eeddafce656717f28055a7a9a755f44737c, 1,051,196 chars); full canonical main.tex Git blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34, 2,545,859 chars; AGENTS/CODEX/skill, issue #3 and all current peer handoffs; relevant original Lipschitz, q-Horn, exact-2P2N, affine, fusion, /341 soundness-fail evidence; primary Schaefer STOC 1978 and Cousot-Cousot POPL 1977. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex unchanged. /341 FAIL, /386 RESTRICTED. P versus NP OPEN.

**PEER REQUEST:** TMR-3 price each fused row/source interface, TMR-4 insert this exact component into zero-SCC/tariff matrix and audit full transition closure, TMR-5 seek a real compact source-derived parity key or changed-interface bypass. **NEXT TMR-2:** find a syntax-aware separator/fusion obstruction remaining after Horn/Krom/Gaussian, autarky, equality, treewidth DP and circuit sharing, then test its cheapest paid discharge and same-system transfer.

END_OF_HANDOFF::TMR2::035::2026-11-14_2023_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 19:20 PST | EDGE-QUANTILE050 typical-YES two-sided MCSP input probe frontier034

**SCIENTIFIC STATUS: PROVED/RESTRICTED, TMR-3/TMR-5 independent mathematical review OPEN; P versus NP OPEN.** Source attribution correction: MAGRED-EDGEADAPT8 (2026-10-18) ALREADY proved the full adaptive source query coupling E q >=(1-2delta)(N-log|Y|) when averaged over exact ordinary MCSP YES. **New in /034** is the explicit typical-YES quantile: for t>0 at least fraction 1-log2|Y|/t of YES tables have expected charged source reads >=(1-2delta)(N-t). With s=floor(N^mu), t=N^(1-(1-mu)/2), a 1-o(1) fraction of YES requires (1-2delta-o(1))N source bit reads even for two-sided constant-error, fully adaptive, random-access machines with arbitrary workspace. The original edge theorem is NOT claimed as new. This is still only exponent one, not CHMY small-mu1 N^1.01 decision lower bound.

**NEW HOSTILE COUNTERCONTROL:** Exact enumeration of <=2 unrestricted binary-gate functions on n=3 inputs yields 152 YES strings; constant-zero table has all eight single-bit neighbors YES and ZERO opposite-label one-bit neighbors. The old MAGRED tiny NAND tests were basis/threshold restricted and do not justify an all-YES singleton-neighbor lemma. TMR-2/033 all-YES one-sided acceptance-fiber theorem remains separate and stronger under zero false positives.

**NATIVE CPython:** original executed experiments/tmr/tmr2_edge_boundary_audit050.py (Git blob 8ee44ed7f31647e307840fea4c3d5d129390afbf); raw results/raw/tmr/2026-11-14_1915_TMR2_EDGE_BOUNDARY050_RAW.json (blob 6fbc8ba7387e50246a73198602dae46ae17bf60d); 66,479 assertions, zero failures, exhaustive all 65,790 nonempty induced subsets of 3/4-dimensional Boolean cubes plus exact tiny-gate classes. Report research/agents/tmr-2/2026-11-14_1920_TMR2_MCSP_EDGE_QUANTILE_COUNTERCONTROL034.md. Finite tests COMPUTATIONAL, not compiled TM execution or asymptotic proof.

**PREFLIGHT:** Controlling Nov14 MCSP directive FIRST and rechecked SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, Nov13 replacement, AGENTS/CODEX/skill, issue #3, five latest peer handoffs, both proof trackers, canonical main and original MAGRED/TMR/Claude/Grok/legacy counterexamples; CHMY STACS2021 primary Theorems 1-2 and MMW STOC2019 primary original inspected. proof1 complete SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 authentic 1,051,196-char blob 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic 2,545,859-char blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. **TRACKERS REVIEWED; NO MATERIAL CHANGE**; canonical main.tex and existing schedules untouched.

**NEXT/PEER:** TMR-5 audit quantile proof and basis-sensitive falsifier; TMR-3 audit source-bit total work and max K parallel elapsed-time transfer; TMR-4 check exact both-label syntax-aware SAT-to-small-mu ordinary MCSP bridge; TMR-1 verify theorem thresholds and N vs L encoding. General MCSP post-ingress N^1.01 time premise OPEN.

END_OF_HANDOFF::TMR2::034::2026-11-14_1920_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 18:14 PST | ONE-SIDED ORDINARY-MCSP ACCEPTANCE FIBERS033

**NEW ACCEPT-FIBER49 PROVED/RESTRICTED, independent TMR-5/TMR-3 mathematical audit OPEN:** For ordinary exact MCSP on arbitrary full truth tables $N=2^n$, $s=\lfloor N^\mu\rfloor$, $0<\mu<1$, let $Y\le D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s$, $\log_2 D=o(N)$. Any fixed randomized *bit-access* decider with NO false-positive acceptance on MCSP NO inputs, and YES acceptance probability at least $1-\delta$, must on **each YES input** read at least $N-\lfloor\log_2D\rfloor$ distinct bits with probability at least $1-\delta$, giving expected bit reads $(1-\delta-o(1))N$. This extends the prior deterministic exact FIBER27/TMR-2/026 result to **one-sided randomization** without TMR-3/032's physical one-way input-head assumption, but does **not** apply to constant two-sided error and does **not** prove $N^{1.01}$ MCSP decision time.

**NEW FALSE-ACCEPT49 quantitative error/read law:** For false-positive probability $\epsilon$ on each MCSP NO input and YES $x$, whenever $2^{N-q}>Y$, the probability of accepting $x$ after at most $q$ distinct reads is at most $\epsilon(2^N-Y)/(2^{N-q}-Y)$. In particular if $\epsilon_N\le2^{-\gamma N}$ and YES acceptance is $\ge1-\delta$, $\liminf E q/N\ge(1-\delta)\min(\gamma,1)$ for every sequence of YES inputs. Fully adaptive read transcripts and global random tapes are allowed; all source-aware reads charged. **This is a certificate/ingress lower bound, not post-read computational hardness.**

**EXECUTED NATIVE CPython:** experiments/tmr/tmr2_one_sided_fiber049.py, immutable raw results/raw/tmr/2026-11-14_1814_TMR2_ONE_SIDED_FIBER049_RAW.json. 3,896 assertions, zero failures, 3,712 exhaustive YES-table/observed-set cylinders and exact certificate search on 22 tables at $n=2,3$, $s=1$. At $n=3$, 14/14 YES functions require all eight source bits for a deterministic accept certificate. Finite evidence COMPUTATIONAL. Full proof/model/primary-source details: research/agents/tmr-2/2026-11-14_1814_TMR2_ONE_SIDED_ACCEPT_FIBER033.md.

**PREFLIGHT:** Nov14 MCSP directive read FIRST and rechecked SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, then Nov13 replacement, AGENTS/CODEX/repo skill, five newest TMR handoffs, issue #3, original TMR2/032 TMR3/032 TMR1/032 TMR4/033 TMR5/029, prior sparse FIBER/GAPCYL, Claude ONETAPE/DIRECTPRODUCT and compact-representation controls; CHMY STACS2021 Theorems 1-2 and MMW STOC2019 Theorems 1.2-1.3 publisher/author originals. Full root proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; authentic full proof2 Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; canonical main.tex Git blob 2,545,859 chars SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex remains TMR-5-owned, untouched; schedules unchanged. P versus NP OPEN.

**NEXT / PEER:** TMR-5 audit measure-one random-tape union and $\epsilon$ numerator, TMR-3 check arbitrary input-head physical charge, TMR-4 attack syntax-aware reduction, TMR-1 enforce small $\mu_1$ threshold. Next pursue/falsify an **additional post-ingress work lower bound**, not a stronger input-inspection certificate alone.

END_OF_HANDOFF::TMR2::033::2026-11-14_1814_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 17:20 PST | EXACT EXPECTED SPARSE-ORACLE MINIMAX032

**NEW EXPECTSPARSE46 PROVED/RESTRICTED; TMR-3/TMR-5 mathematical review OPEN:** For randomized adaptive opaque source-oracle decision distinguishing zero from exactly r positives among M coordinates at two-sided worst-case error δ<1/2, with arbitrary shared local work, the **exact minimum expected distinct reads on zero** is (1-δ) h_{M,r}(δ/(1-δ)), where h is the inverse of the piecewise-linear hypergeometric no-hit curve H(q)=C(M-q,r)/C(M,r). Lower bound conditions on correct zero-source transcripts, applies Jensen on that fraction, and minimizes the convex-inverse perspective; upper bound is a matching mixture of immediate incorrect guessing and uniformly random q/q+1 probes. New objective vs TMR-2/031's fixed worst-case cap.

**NEW ORDINARY-MCSP SHARPER INPUT-INGRESS RESTRICTED TRANSFER:** With full table N=2^n, s=floor(N^mu), 0<mu<1, r=ceil(Ks), K>2mu/(1-mu), and sparse-neighbor YES probability epsilon<=D(n,s)/C(N,r), every YES table and δ-error randomized charged point-bit decider satisfies E[q] >= (1-δ) h_{N,r}((δ+(1-δ)epsilon)/(1-δ)); asymptotic coefficient is (1-δ)log((1-δ)/δ) N/r, versus prior TMR-5/028 log(1/(2δ)) N/r. At δ=1/3: 0.4620981204 vs 0.4054651081, +13.9674%. STILL O(N^(1-mu)), no N^1.01 work bound, no SAT lower bound.

**EXECUTED NATIVE CPython:** experiments/tmr/tmr2_expected_sparse_query046.py, Git blob d639a6859ecacf1a0ff8827669806a39e0d8d1e8, actual immutable raw results/raw/tmr/2026-11-14_1720_TMR2_EXPECTED_SPARSE_QUERY046_RAW.json, blob ceea4556c40851b341604bd7bdeca6c7a7779dfb. 6,524 assertions, 325 independent HiGHS LP optima, 132,242 exhaustive support/query operations, zero failures; finite evidence COMPUTATIONAL. Full report research/agents/tmr-2/2026-11-14_1720_TMR2_EXPECTED_QUERY_MINIMAX032.md.

**PREFLIGHT/CORPUS:** Controlling Nov14 directive FIRST, Nov13 directive, entire root proof1 and recovered authentic large proof2/main Git blobs, AGENTS/CODEX/skill, five handoffs and issue #3 through TMR-1/031. Original CHMY STACS2021 Thm1/2 publisher page 23:3; MMW STOC2019 Thm1.2/1.3 original page 2; original TMR-2/031, TMR-3/031, TMR-5/028 and code/raw, Claude ONETAPE/DIRECTPRODUCT, TMR-4 Walsh moments, TMR-5 syntax forcing. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex unchanged TMR-5-owned; schedules untouched. P versus NP OPEN.

**PEER/NEXT:** TMR-5 audit good-branch convexity and exact sampler; TMR-3 all source-aware network reads; TMR-4 syntax-aware/compact-algebra countercontrols; TMR-1 threshold mu1/mu2. Next find or falsify an invariant of charged unavoidable **post-input computation** that survives full syntax, sharing, input rereading and recomputation.

END_OF_HANDOFF::TMR2::032::2026-11-14_1720_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 16:18 PST | RANDOMIZED FULLY SHARED SPARSE ORACLE MINIMAX031

**NEW RMINIMAX42 PROVED/RESTRICTED symbolic; TMR-4/TMR-5 independent review OPEN:** For a fully shared randomized adaptive **one-bit** source-evaluation algorithm promised zero on M coordinates or exactly r ones, with at most q probes on each random-coin zero transcript, define U=binom(M-q,r)/binom(M,r). Its **exact minimax worst-case error** is U/(1+U); δ-error is possible iff U<=δ/(1-δ), and zero error iff q>=M-r+1. This extends the previous r-sparse independently restarted **output-distance** bound to arbitrary shared adaptive randomized decision. Proof conditions on the zero transcript, counts missed r-sets, and matches using a uniform q-subset sampler with optimally balanced auto-YES probability. **No source syntax, machine-time charge or unrestricted SAT/MCSP proof.**

**ACTUALLY EXECUTED hosted V8:** exact source experiments/tmr/tmr2_shared_sparse_minimax042.js, raw results results/raw/tmr/2026-11-14_1618_TMR2_RANDOM_SHARED_MINIMAX042_RAW.json; 29,612 assertions, 348,502 support/query-set pairs, 16,208 adaptive cases, 4,052 sharpness checks, zero failures. All finite evidence COMPUTATIONAL. Report research/agents/tmr-2/2026-11-14_1618_TMR2_RANDOM_SHARED_SPARSE_MINIMAX031.md. Read controlling Nov14/Nov13 directives, AGENTS/CODEX/skill, current issue #3, five TMR handoffs, prior original TMR/code/raw, Claude ONETAPE, Grok/compact controls, entire proof1, authentic full Git blobs proof2/main, CHMY/MMW primary PDF theorem pages. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No schedules changed, P versus NP OPEN.

**Peer request:** TMR-5 audit minimax and tightness; TMR-4 test formula-syntax and full-table transfer; TMR-3 audit sampler cost before any physical time bound. **Next:** attempt a paid syntax-aware continuation invariant surviving Horn/2-SAT, XOR, bounded-treewidth and clause-forcing controls.

END_OF_HANDOFF::TMR2::031::2026-11-14_1618_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 15:21 PST | R-SPARSE HYPERGEOMETRIC ORACLE LOCALITY030

**NEW RSPARSE38 PROVED/RESTRICTED (TMR-4/TMR-5 peer review OPEN):** Generalizes PRIOR TMR-2/029 adaptive shared-preprocessing singleton query theorem to arbitrary r-sparse source witnesses. Let M=2^v, Q0 the all-zero preprocessing query set, b0=|Q0|, B=M-b0, 1<=r<=B. Then for N independently restarted target-bit routines each querying <=q further oracle coordinates, the mean normalized Hamming distance from the target zero image over all r-subsets outside Q0 is bounded by 1-C(B-min(q,B),r)/C(B,r). It is SHARP as a distance-to-reference statement: make outputs OR the source coordinates indexed by all q-subsets. It recovers TMR-2/029 at r=1. Zero mapped to Gap-MCSP-Ham YES with every r-sparse source promised eta-far NO requires C(B-min(q,B),r)/C(B,r)<=1-eta, implying q>=eta B/r. This is **source-independent black-box evaluation-query** only, not physical MCSP time, nor arbitrary SAT. Arbitrary cross-output sharing or formula syntax escapes these premises. A syntactically trivial proper-3-CNF clause-forcing family provides a hostile shortcut.

**ACTUALLY EXECUTED native CPython:** experiments/tmr/tmr2_sparse_hypergeo038.py (Git blob cde6d9abaebe1924840c503a6f03d1117de45513, SHA256 94a07e8fd31f23506c346fc144287926e8c2d3f20cf4abce48db00de9f9c10fb); raw results/raw/tmr/2026-11-14_1521_TMR2_RSPARSE_HYPERGEO038_RAW.json (blob 06a0d3e5a66e0befb6fbd0496362a5f02cd926b6, SHA256 7edeb4ac6a27f720c9cb0d03359fa48f70f46235294a22081d0d30971e27694a). 27,316 assertions, zero failures, 1,104 adaptive configurations, 12,480 r-sparse source executions, 81,223 output comparisons, 308 sharpness parameter cases, 12,172 all-subset equalities, 42 proper-3CNF syntax controls. An initial local test counted the wrong binomial orientation for sharpness and failed; corrected before the final successful native run. Finite checks COMPUTATIONAL only, not a finite-alphabet TM execution.

**FULL REPORT:** research/agents/tmr-2/2026-11-14_1521_TMR2_RSPARSE_HYPERGEOMETRIC_QUERY030.md. Controlling Nov14 MCSP directive read FIRST/rechecked SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, Nov13 replacement, root AGENTS/CODEX/pnp skill, issue #3 and five TMR handoffs, original TMR/Claude/Grok/legacy sources. Full proof1 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 1,051,196 chars blob 930c5eeddafce656717f28055a7a9a755f44737c; canonical main.tex 2,545,859 chars blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. TRACKERS REVIEWED; NO MATERIAL CHANGE, canonical main.tex unchanged TMR-5-owned. No schedule/task changes.

**NEXT / PEER REQUEST:** TMR-4 check syntax-aware global reduction and r-sparse promises; TMR-5 independently check hypergeometric zero-path, exact OR sharpness, output arity and Hamming-Gap class; TMR-3 check fully shared machine source costs; TMR-1 check CHMY parameter/exponent. TMR-2 next target: fully shared adaptive source-query transducer with complete input/output work accounting. CHMY low-mu one-work-tape ordinary-MCSP N^1.01 lower-bound premise OPEN. P versus NP OPEN.

END_OF_HANDOFF::TMR2::030::2026-11-14_1521_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 14:17 PST | SHARED ORACLE PREPROCESS032

**NEW SHAREDPREP32 PROVED/RESTRICTED elementary theorem (TMR-4/TMR-5 independent review OPEN):** For a fixed source-independent evaluation oracle `f:{0,1}^v -> {0,1}`, `M=2^v`, deterministic adaptive global preprocessing making `b` queries, followed by `N` *independently restarted* per-output local adaptive routines making at most `q` queries each, let `Q0` be the actual global zero-oracle queried-coordinate set, `b0=|Q0|`. For singleton functions `f_a`, source zero `f_0`, and output `Y(f)`, the **NEW conditional-on-global-state** bounds are
$$
\sum_{a\notin Q0}d_H(Y(f_a),Y(f_0))\le Nq,\qquad \sum_a d_H(Y(f_a),Y(f_0))\le N(b0+q).
$$
If `M>b0` then some singleton outside `Q0` has relative output distance at most `q/(M-b0)`. Thus to map zero to **ordinary Hamming-gap MCSP YES** and every singleton to promised NO at relative gap `eta>0`, it is necessary that `q >= eta(M-b0)`. In particular local `q=0` demands global `b0=M`. **SHARP:** Global OR on b source positions and cyclic q-query local OR on remaining M-b, with N divisible by M-b, meets BOTH inequalities with equality. This generalizes PRIOR TMR-4/029 (`b=0`) while correctly charging global shared oracle queries. Complete arbitrary cross-output sharing instead yields a total-query zero-path coverage condition of M, but this is NOT a SAT / one-tape time bound.

**ACTUALLY EXECUTED native CPython:** `experiments/tmr/tmr2_shared_oracle032.py` (SHA256 a931f06af1511aeb223ae01114fa7253ecc9b350194c3ee91d7468f2fb7345fa; Git blob 253273032fc90f1623c1c39dccdd5f01139737ab); immutable native stdout `results/raw/tmr/2026-11-14_1417_TMR2_SHARED_ORACLE032_RAW.json` (SHA256 fd5b80375dc71f56cd6f50a5c77a3158f16490fce7216e9e4f8a3dcf208dec9c; Git blob a714249c17a48f1c175665f452070838c0cd9149). 328 global/local adaptive cases, 4,784 singleton executions, 89,590 output-coordinate checks, plus 82 equality cases and 84 q=0 controls; zero failures. **COMPUTATIONAL** finite evidence, not a compiled TM. Original restricted proof in `research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md`.

**PREFLIGHT:** Nov14 MCSP directive FIRST; Nov13 role replacement, both full root proof1 (28,714) and proof2 (1,051,196 via genuine blob) and canonical main.tex (2,545,859 via blob), AGENTS/CODEX/pnp skill, newest issue #3, all five current handoffs and original TMR4/029 code/raw, Claude ONETAPE and October affine/query controls. CHMY STACS21 publisher PDF Theorems 1-2 p23:3 and MMW STOC19 author PDF Theorems 1.2-1.3 visually reviewed. Root **TRACKERS REVIEWED; NO MATERIAL CHANGE**; TMR-5 owns main.tex; no tasks changed. **P!=NP OPEN**.

**NEXT / PEER REVIEW:** TMR-4 audit global-state conditioning, tight cyclic OR, and syntax scope; TMR-5 independently reproduce equality and test fully shared transducers; TMR-1 check low positive mu theorem premise, TMR-3 audit physically charged source and output. The required unrestricted SAT-decider bridge / ordinary MCSP small-mu one-work-tape N^1.01 lower bound remains OPEN.

END_OF_HANDOFF::TMR2::029::2026-11-14_1417_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 13:22 PST | PERIODCODE28 GROWING-THRESHOLD YES CLASS

**NEW PERIODCODE28 PROVED/RESTRICTED symbolic countermodel, pending TMR-1/TMR-3/TMR-5 mathematical audit:** Fix rational 0<nu<.01 (e.g. 1/200), N=2^n, k=2^floor(nu*n). The code C_n consists of all length-N binary tables repeating their first k-bit block. Exact |C_n|=2^k, minimum distance N/k; every codeword is an n-input Boolean function of circuit gate size <=3(k-1)+floor(nu*n) in free-constant fan-in-two AND/OR/NOT basis, hence C_n subset MCSP[N^mu] YES for all fixed mu>nu eventually. Every exact deterministic adaptive coordinate-query decider for the **special language C_n** must query all N positions on every YES codeword; the previously proved CODEDIST27 also gives N-r+1 for promise distance r<=N/(2k).

**NEW UNIFORM COUNTERMODEL, NOT FULL MCSP:** A single finite one-way-read-only-input and one **physical** two-way work-tape machine, without length header or advice, copies input N bits, detects N=2^n by O(N log N) marker-halving passes, computes k, and shifts a length-k reference template across stored consecutive k-bit blocks. Cost O(N log N+Nk)=O(N^(1+nu)) time and O(N) writable cells, hence for nu=1/200 time O(N^1.005)<O(N^1.01). This decides BOTH labels of the periodic special language but **does NOT decide ordinary MCSP nor preserve its NO label**. It concretely retires any proposed inference from a superpolynomial number of low-gate YES tables plus maximal deterministic query depth alone to the CHMY one-work-tape N^1.01 lower-bound premise.

**EXECUTED native CPython:** experiments/tmr/tmr2_periodic_code028.py, Git blob a2567dfc9c4755b00ec232893b18b9d961ca7222, local identical git hash and SHA256 37dd60c73a19128b7c1f5766a1f40659e58504ff78da502f824c3d9abdbcd455. Raw results/raw/tmr/2026-11-14_1322_TMR2_PERIODIC_CODE028_RAW.json, Git blob 4f45b3d676a10217631c8df3553672be10d96ccf, local identical git hash and SHA256 7fbfe34fd6ca7a5baea8bac607f7deb586ace3948bddf4de45a5f962cd7890be. Charged tape/head proxy: 2,367 cases, 8,189,818 operation units, 78,834 one-cell template shifts; 2,920 flip controls, 39 malformed lengths, 5,368 recorded check groups, zero failures. **Finite oracle-free symbolic proxy, NOT compiled native finite-state TM execution**, and short tests use denominator 2,3,4 rather than n>=200; asymptotic proof independent of finite tests.

**REPORT:** research/agents/tmr-2/2026-11-14_1322_TMR2_GROWING_MCSP_PERIODIC_CODE028.md. PRIMARY SOURCE checked publisher CHMY STACS 2021 Thms 1-3 p23:3-4 with PDF screenshot and MMW STOC2019 Thms1.2-1.3 original; CHMY low-mu ordinary MCSP DTIME_1[N^1.01] exclusion remains OPEN. Earlier CODEDIST27, ODOMETER27, TMR-4 fixed-gate/TMR-5 bounded envelope and 2026-10-18 affine-kernel works credited. Nov14 MCSP directive read FIRST SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, Nov13 directive, issue #3 latest, all handoffs, original Claude ONETAPE/TPORT, authentic proof1 28,714, proof2 recovered 1,051,196 and main 2,545,859 characters. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex unchanged; no schedules changed; P versus NP OPEN.

**NEXT:** Prove or falsify unavoidable *post-acquisition computation* on the ENTIRE low-positive-mu ordinary MCSP both-label language, not a code subset. TMR-3 review physical marker-halving/compiler time; TMR-1 verify multiplexor gate count and mu>nu constants; TMR-5 independently replay and check strict all-label separation.

END_OF_HANDOFF::TMR2::028::2026-11-14_1322_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 12:21 PST | CODEDIST27 AND ODOMETER27

**NEW CODEDIST27 PROVED/RESTRICTED**, mathematical peer review pending: for a finite N-bit code C with minimum pairwise Hamming distance d, promise YES=C, NO=distance at least r, and 1<=r<=d/2, **every YES** deterministic adaptive coordinate-query accepting path uses at least N-r+1 distinct queries. Fixed-coordinate querying N-r+1 plus any codeword-consistency check decides the promise, so the lower bound is exact in the unlimited-off-query-computation model. For MCSP[0], C consists of constants and n positive input projections with d=N/2 (n>=2). Thus for every 0<eta<=1/4, exact eta-Gap-MCSP[0] deterministic YES query depth is N-ceil(eta N)+1. At eta=1/4, this reproduces PRIOR TMR-2/026's 3N/4+1, not an external novelty claim.

**NEW ODOMETER27 PROVED/RESTRICTED, TMR-5/TMR-3 audit requested:** TMR-5/023 already gave a fixed uniform length-blind one-way-input/one-work-tape MCSP[0] decider using O(log N) space and O(N log^2 N) transitions. Independent TMR-2 construction stores each binary source-counter bit **co-located** with its positive-projection match flag and updates carry, comparison and flag in ONE work-tape forward sweep, then one return sweep per input bit. Newly introduced high-bit candidate is initialized from the all-zero prefix flag; endmarker excludes the freshly created high bit for valid length N=2^n. Thus **O(N log N) time and O(log N) visited writable cells** on the SAME machine, no length advice, free oracle or input rereading. This is a threshold-zero *upper bound*, not the positive-mu CHMY magnification lower bound.

**ACTUAL EXECUTION:** native CPython completed 65,812 exhaustive full truth tables (18 YES, 65,794 NO), 192 random larger, 40 malformed lengths, 38 code/radius instances, 15,292 distinct r-bit far-NO adversarial flips, and seven (n,r) complete promise classifications with 0 failures. Published source experiments/tmr/tmr2_odometer_stream027.py, SHA256 667bea8c98b18cb1a092ec774931504294d9834562036e33f442add7757d60de; published exact JSON results/raw/tmr/2026-11-14_1221_TMR2_ODOMETER_CODE027_RAW.json, SHA256 8c94a1c4baa2627bb31807f2c300147670d25aa8215bc52302a6912443047767. Finite proxy not native formal TM execution.

**REPORT:** research/agents/tmr-2/2026-11-14_1221_TMR2_ODOMETER_CODE_CERTIFICATE027.md. Nov14 MCSP directive read FIRST, Nov13 replacement, issue #3, AGENTS/CODEX/skill, all TMR handoffs, relevant TMR/Claude/legacy original paths, complete proof1 28,714 chars and recovered complete proof2 1,051,196 and canonical main.tex 2,545,859 chars. Primary CHMY STACS2021 Theorems1-2, MMW STOC2019 Theorems1.2-1.3 and OPS/Chen scope checked. **TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex untouched.** No schedule changes. P versus NP OPEN.

**NEXT:** source-dependent uniform representative-update at s>=1 or growing s=N^mu; explicitly try compact decision algorithms and test whether any post-scan bottleneck genuinely binds CHMY's exact small positive mu. TMR-5 audit binary carry flag invariant and endmarker, TMR-3 verify physical sweeps, TMR-1 check threshold/query scopes.

END_OF_HANDOFF::TMR2::027::2026-11-14_1221_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 11:23 PST | GAP-MCSP HAMMING CYLINDER AND QUERY CONTRAST026

**NEW GAPCYL26 PROVED/RESTRICTED elementary theorem, TMR-5/TMR-1 peer review requested:** For ordinary size-s circuit YES set C on full N=2^n truth-table bits, M=|C|<=D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s. In eta-approximation-promise MCSP, every deterministic adaptive exact **point-query** decider must query on EVERY YES source x at least N-log2(D(n,s))-log2(V(N,ceil(eta*N)-1)) distinct positions, where V is Hamming-ball volume. Proof: accepting q-query cylinder of size 2^(N-q) must fit within the union of M radius-r Hamming balls; otherwise a promised far-NO shares the entire adaptive transcript. For eta=N^(-lambda), s=N^mu, 0<mu,lambda<1, this is N-o(N) YES queries. **Not** a one-work-tape superlinear runtime bound. Earlier October 20 FIBER27 proved the exact ordinary-MCSP sparse-fiber near-N barrier; novelty is the Hamming-gap cylinder extension and randomized contrast, not the old exact argument.

**NEW exact all-length threshold-zero contrast:** At s=0, YES comprises constants and n projections, mutually separated by >=N/2; for eta=1/4 every YES source requires exactly 3N/4+1 deterministic query observations along its accepting branch. A randomized random-access sampler plus full candidate enumeration accepts YES certainly, rejects eta-far NO with error <=D exp(-eta*q), using q=O(log n+log(1/delta)) queries for s=0. For s=N^mu and eta=N^(-lambda), q=O(N^(mu+lambda) log N), sublinear for mu+lambda<1. Enumeration/update time is **exponential in s**, so no polynomial-time algorithm or CHMY/MMW magnification premise established. Uniform one-way physical input requires a separate costed compiler.

**Independent TMR-1/025 audit, favorable RESTRICTED:** Delta_(n+t,s)(E_t f)=Delta_(n,s)(f) by extending an optimum and restricting all padded-circuit z-slices; valid for matching integer threshold, named inputs and free constants. Promises with changed length-dependent Hamming gaps must be handled separately. Atserias-Müller 2025 Theorem 27 concerns P-uniform circuits on approximation-promise MCSP and concludes P!=NP^(oplus P), NOT P!=NP. CHMY Theorem1 still needs small-mu deterministic one-work-tape N^1.01 exclusion; known N^1.99 is at different large mu. No variant transfer.

**ACTUALLY EXECUTED native CPython COMPUTATIONAL:** exact source experiments/tmr/tmr2_gap_certificate026.py, SHA256 bcfb9b1b503e3ff47ad3eacfb2be037ac70518cf6335c3a87701991cce2dfc22, Git blob ae40c89df048363a1ab1177b7d14444a093877d7; raw results/raw/tmr/2026-11-14_1123_TMR2_GAP_QUERY026_RAW.json, SHA256 2a90682e1e664d273ed8c8c48152028eda9ff6544c23377236a25b1a424fd4f4. Exhaustively classified 65,536 n4/s0 tables (six YES, 61,354 far NO), computed all six accepting-certificate minima 13, checked 1,820 four-bit hostile supports and 544 padding-gap equalities; maximum q20 random-sample union error bound 0.009516496839751198. ZERO failed assertions. Finite only.

**REPORT:** research/agents/tmr-2/2026-11-14_1123_TMR2_GAP_MCSP_HAMMING_CYLINDER026.md. Full latest Nov14 MCSP directive first, Nov13 replacement, proof1/proof2/main.tex authentic full Git blobs, issue #3 latest TMR1/025, all role handoffs, original October FIBER27, representative maintenance, TMR2/025, TMR1/025, TMR5/022, original Claude/Grok controls, CHMY/MMW/Atserias-Müller primary papers reviewed. TRACKERS REVIEWED; NO MATERIAL CHANGE; main.tex unchanged; tasks untouched. P versus NP OPEN.

**NEXT:** TMR-5 independently review Hamming-cylinder count and exact s0 transcript; TMR-1 audit approximate threshold and uniform magnification. TMR-2 work on **uniform post-full-scan update-time hardness** with compact circuit alternatives and charged physical tape cost, not further source-query-only bounds.

END_OF_HANDOFF::TMR2::026::2026-11-14_1123_PST

---

# TMR-2 CURRENT handoff | November 14, 2026, 10:24 PST | MCSP NO-CERTIFICATE CYLINDER SANDWICH025

**NEW CYL25 CANDIDATE/RESTRICTED pending TMR-5/TMR-1 independent review:** Fix ordinary MCSP_n[s] with N=2^n explicit truth-table bits, fan-in-two AND/OR/NOT circuits, free constants, unbounded fanout, gate count s>=n. Let r=floor((s-n+1)/n), D=(s+1)(n+s+2)[3(n+s+2)^2]^s. EVERY arbitrary q<=r labeled subset of truth-table coordinates has a YES completion via shared-negation sparse DNF of size at most n+nq-1. Hence EVERY NO MCSP[s] source needs >r distinct bit queries in ANY exact deterministic adaptive point-query decider, unlimited memory allowed. If D<2^N, ANY t=floor(log2 D)+1 fixed coordinates admit some absent YES trace; a NO table exists with a t-bit negative certificate. For s=floor(N^mu), fixed 0<mu<1, every NO has certificate Omega(s/n), and some NO has certificate O(s log N). These are DIFFERENT source quantifiers. Neither gives a CHMY N^1.01 one-tape small-threshold bound or the MMW simultaneous uniform poly(s)-update/poly(s)-space streaming-search exclusion. No free post-acquisition time or physical source access imported.

**EXECUTED native CPython 0.93s COMPUTATIONAL:** 42,371 exhaustive prescribed partial labelings at (n,s,r)=(3,9,2),(4,12,2),(5,20,3), zero failures; complete n=4 AND/OR/NOT size 0,1,2 circuit enumeration produced 6,22,90 YES truth tables; n=4 s=1 gives D=2058 and a valid missing 12-bit NO cylinder; n=4 s=2 gives a 7-bit counting guarantee and one NO table with exact minimum 4-query negative certificate [0,1,2,4]. Source SHA256 eb237f23b9f5cc107cd6522ffccc31718407d6c2e4699cd98eed98226dcd1b89; raw SHA256 bd1bdd91002cb4555377986ba35edd0913f51f893d5cc96c82a92d8a51679862. Exact executed Git blob SHAs: source 7fce402abc02c26905e27f24fdc646b182df5f9f, raw 7a6ed8b47c67a41d341a292e9547cc22b92c1347.

**VERIFIED REPORT / CODE / RAW:** research/agents/tmr-2/2026-11-14_1024_TMR2_MCSP_CERTIFICATE_CYLINDER_SANDWICH025.md ; experiments/tmr/tmr2_mcsp_certificate025.py ; results/raw/tmr/2026-11-14_1015_TMR2_MCSP_CERTIFICATE025_RAW.json. Source-sensitive information bounds, not a physical one-tape compiler or new SAT decider. Prior TMR-2/024 all-cut residual and October 19 small-space expensive-update results explicitly credited.

**PREFLIGHT:** Nov14 MCSP priority first and rechecked SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a; Nov13 replacement; full proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2 Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; full canonical main.tex Git blob 2,545,859 chars SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34; issue #3 through TMR-1/024, all five TMR current handoffs, AGENTS/CODEX/skill, source reports and original CHMY/MMW papers. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex TMR-5 ownership untouched. No scheduled tasks changed.

**ONE NEXT TARGET AND PEER REQUEST:** TMR-5 audit adversarial query quantifiers and actual all-NO/exists-NO distinction; TMR-3 check physical one-tape transfer gap; TMR-1 verify basis and parameter. TMR-2 next test ALL uniform poly(s)-memory representative-update methods, allowing noncanonical summaries and cache/recompute. Both P=NP and P!=NP OPEN.

END_OF_HANDOFF::TMR2::025::2026-11-14_1024_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 09:27 PST | MCSP ALL-CUT RESIDUAL WIDTH AND UPDATE-COST FIREWALL024

**NEW RES24 CANDIDATE/RESTRICTED pending TMR-3/TMR-5 review:** For ANY finite nonempty Y subset {0,1}^N with M=|Y|, any fixed source-coordinate order and every read cut, the full collection of all prefix right residuals has <= M+1 distinct classes. This gives a nonuniform correct all-label ordered read-once BP of width <=M+1 and <=(N+1)(M+1) layer states. Proof: at most M prefixes occur among positive sources; all other prefixes share empty residual; residual equality is stable under either next bit. For fixed-threshold ordinary MCSP[s], positive descriptions M<=D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s, so residual state information <=O(s log(n+s)) bits. This **falsifies prefix-count-only superpolynomial-in-s memory claims**, NOT the uniform update-time question or physical one-work-tape lower bounds. Earlier October 19 representative-maintenance already gave uniform O(s log s) space with exponential updates, explicitly credited.

**NATIVE CPython COMPUTATIONAL, independent code:** experiments/tmr/tmr2_sparse_residual024.py (Git blob 6dff0727016566de14dedb1e438553e636ad96ba, SHA256 3a1ad5358f557f5deef29219c8c7aae45efb2dda9b0a0c0c4cc7b2d8ebf426d0); 12 n=2,3,4 and s=0..3 circuit grammar cases plus 4 source-bit-order controls. 525,376 exhaustive terminal source classifications, 1,050,720 both-edge prefix checks; zero failures. n3/s2: 40 YES, max minimized width16; n4/s2: 90 YES, width43; odd-even input order width45. Published raw lossless gzip/base64: results/raw/tmr/2026-11-14_0927_TMR2_MCSP_RESIDUAL024_RAW.json.gz.b64, decoded original JSON SHA256 19fa1d9745a9c5588488385aa4866a8d464a230b977f3e96b29a11da44a7bbf7. Report: research/agents/tmr-2/2026-11-14_0927_TMR2_MCSP_RESIDUAL_WIDTH024.md.

**MCSP PRIMARY SCOPE:** CHMY STACS 2021 Theorem 1 requires a small-mu fixed-threshold deterministic one-way-input + one-work-tape lower bound N^1.01 for P!=NP. Existing near-N^1.99 randomized lower bound concerns DIFFERENT larger-mu MCSP. MMW STOC 2019 Theorem 1.3 requires **simultaneously** poly(s) workspace AND poly(s) update lower-bound for uniform full one-pass search-MCSP with suitable PH oracle, not an information-only one-pass BP. OPS Gap-MCSP, MKTP and read-once co-nondet full-MCSP BP lower bounds have other promises/models. No transfer to arbitrary multi-tape SAT deciders. P versus NP OPEN.

**REVIEWED:** Nov14 latest MCSP priority first, Nov13 TMR replacement, both root proof1 (28,714) and full Git-blob proof2 (1,051,196), full main.tex authentic Git blob (2,542,866), current issue #3, AGENTS/CODEX/skill, all current TMR handoffs, TMR1/023, original Oct18-20 MCSP/MKTP/threshold/no-go cases, original Claude and CHMY/MMW/OPS primary literature. TRACKERS REVIEWED; NO MATERIAL CHANGE. Main.tex reserved for TMR-5. Schedules untouched.

**ONE NEXT TARGET / PEER REQUEST:** TMR-3 validate real one-work-tape serialization costs; TMR-5 independently prove all-cut residual congruence and check MMW search-update versus CHMY low-mu requirements. TMR-2 should now propose/falsify a genuine **uniform representative-transition computation** lower bound that survives poly(s) memory, factored circuits, caching and source rereads, not another prefix-count bound.

END_OF_HANDOFF::TMR2::024::2026-11-14_0927_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 08:23 PST | MAXSAT SIGN DISTANCE AND WALSH-FLAT UNSAT022

**NEW SRG22 CANDIDATE/RESTRICTED; elementary complete all-length argument, TMR-1/TMR-5 review requested.** On a proper 3-CNF ordered clause-occurrence list with fixed variable IDs and editable polarity bits, exact minimum legal sign-bit Hamming distance to any SAT input equals min_a(number of clauses violated by a) = m-MAXSAT(F). Since each proper clause is falsified with probability 1/8 on a uniform random assignment, distance <=floor(m/8), sharp for repeated complete sign cubes U_r. For clause i with falsifying triple eta_i, define signed Walsh moments M_F(S)=sum_{i:S subset V_i}prod_{v in S}eta_{i,v}, |S|=1..3. Then 8v_F(x)=m+sum_{S neq empty}M_F(S)chi_S(x). Therefore exact maximum robustness d=m/8 holds iff every nonconstant moment vanishes. Checking at most 7m integer contributions is a deterministic polynomial-time physically charged UNSAT recognizer when m>0; on failure run a paid correct general SAT fallback. This is a compact algebraic global invariant, not a general polynomial SAT algorithm or computational necessity.

**INDEPENDENT mathematical peer audits:** TMR-5/019 corrected U_r result survives: d=r, 8*3^r nearest SAT sign edits, individual sensitivity zero for r>=2, block sensitivity exactly 24 (not the retracted 8), with explicit 24 disjoint r-bit blocks and matching edit-distance upper bound. TMR-1/022 also receives favorable restricted symbolic audit: C0(U_{k,r})=k2^k; for nearest SAT V and r>=2, C1=m, because every untouched clause permits a one-clause UNSAT completion; at r=1, two duplicated complete k-bit signatures provide a cheaper 2k-bit certificate (six vs eight for k=3). These distinct sign distance, legal certificate and charged runtime measures must not be conflated. Peer review of this run's new Walsh result remains pending.

**ACTUALLY EXECUTED hosted V8 exact published source; COMPUTATIONAL:** 15,585 formulas, 203,992 full-assignment Walsh equalities, 12,870 exhaustive 3-variable signature multisets m<=8, 2,700 seeded n4/n5/n6 sources, seven explicit controls (Horn-like, XOR, auxiliary lifted 2-SAT, path, products, duplicates, renaming), 192 sensitive-block checks, 63,471 exhaustive Hamming neighbors U1..U3, 312 nearest SAT neighbors, zero failed assertions. NO native Node, independently authored CPython, generic charged TM compiler, specialized Horn/XOR/DP solver, full repo preflight or TeX compilation.

**GitHub main VERIFIED report/source/raw:**
- report research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md (blob 073107a28b0bfade2095af498e9c4d4143a8c61b);
- executable experiments/tmr/tmr2_walsh_sign_robustness022.cjs (blob b38366925c045f91d3c036849939b606fc707f5c);
- raw results/raw/tmr/2026-11-14_0820_TMR2_WALSH_SIGN_ROBUSTNESS022_RAW.json (blob 984e21330b126d74f1826d061717048f24b58957).

**Original Claude reviewed:** newest directly named standalone Claude files under research/agents/claude/ are dated 2026-10-28: ONETAPE, TPORT-0001/0002 and DIRECTPRODUCT. The crossing-sequence bounds are sequential-access and even apply to nondeterministic one-tape computation; TPORT barrier applies only to the specified alternating proof rules/random-access small-space model. No unrestricted transfer. Primary O'Donnell 2014 Boolean Fourier and standard 7/8 Max-E3SAT averaging checked; FLMV 2005 exact small-space/time scope verified.

**Integrity:** authoritative directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 read first/rechecked, root proof1 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, authentic root proof2 1,051,196 chars via blob 930c5eeddafce656717f28055a7a9a755f44737c, root main.tex full 2,542,866 chars via blob 5ec8fffb16ec9a7f262e60321bf5aad172d153d8. AGENTS/CODEX/skill, issue #3 through TMR1/022, all TMR handoffs, original TMR5/019, TMR1/022, TMR2/021 and relevant Claude sources read. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex left for TMR-5. No task modification.

**ONE NEXT TARGET:** independently falsify any proposed all-machine post-acquisition charge against the Walsh-flat polynomial recognizer plus TMR-1/022 valid-source certificates. The arbitrary all-exponent deterministic 3-SAT processing lower bound and P versus NP are OPEN.

END_OF_HANDOFF::TMR2::022::2026-11-14_0823_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 07:25 PST | GENERAL PROPER-3CNF POLARITY DICHOTOMY021

**NEW TMR2-SCB21 CANDIDATE/RESTRICTED, independent TMR-1/TMR-5 review requested.** For arbitrary ordered proper 3-CNF F with three distinct variables per clause, let H_i=F without occurrence C_i. Exact one-original-sign-bit SAT/UNSAT sensitivity:

* If F is **UNSAT**, all three polarity bits of C_i change the formula to SAT iff H_i is SAT; otherwise none do. Thus s(F)=3e(F) for the number e(F) of deletion-essential clause occurrences, and s(F)<=3 min(m,2^n,8 binomial(n,3)). This strengthens earlier TMR2/020 G20 bound from inequality to **exact equality**.
* If F is **SAT**, flipping the jth polarity in C_i creates UNSAT iff H_i entails literal j TRUE and the other two original literals FALSE. Thus C_i is logically implied by H_i, the three clause variables are backbone-fixed, and **at most one sign bit per clause** is pivotal: s(F)<=m. In particular if F has <3 backbone variables, s(F)=0. This is an exact all-length combinatorial theorem in the declared polarity-edit interface, not an all-machine processing bound.

**Proof:** For UNSAT F and H_i SAT, every H_i-model must falsify all three C_i literals, so flipping any one makes SAT. SAT F plus flipped UNSAT iff every H_i-model falsifies the flipped clause, equivalent to the stated fixed selector triple; two such distinct selector triples cannot simultaneously hold on a nonempty model set. Witnesses of distinct deletion-essential clauses are distinct full assignments. Original source-bit sensitivity forces any correct fixed locally moving input-tape decider to physically read those bits by same-input opposite-label trace coupling, but produces **no superlinear computation charge**.

**EXECUTED and PUBLISHED hosted V8 exact source:** 43,758 exhaustive E3 clause multisets m<=10, plus 5,000 deterministic random n=4,5,6 clauses sets and 4 hostile cube/product controls. 48,762 sources, 1,379,646 flips, 6,290 pivotal SAT, 13,041 pivotal UNSAT, 4,347 essential occurrences, 300 renamings, 0 failures. Distinct native CPython LOCAL-ONLY implementation: 53,468 sources, 1,586,727 flips, 4,674 deletion witness checks, 0 failures; local-only Python/JSON not presented as repository artifacts. Both finite tests COMPUTATIONAL.

**Readback-verified main paths:** report research/agents/tmr-2/2026-11-14_0725_TMR2_GENERAL_POLARITY_PIVOTAL_DICHOTOMY021.md (blob 428ba8d10bc419fbd4187b4055ae9032c7a6ef56); V8 source experiments/tmr/tmr2_sign_dichotomy021.cjs (blob fbe23cfe6ff77ad478d1b550b91eb710804eee9b); raw results/raw/tmr/2026-11-14_0722_TMR2_SIGN_DICHOTOMY021_RAW.json (blob df478891e4bba224527b9fcd924604cb3118f84d). Direct primary context: Kullmann 2000/2011 minimal UNSAT; Kiesl et al. 2018 clause redundancy; Dubois and Dequen 2001 backbone; Nisan-Szegedy 1994 sensitivity (all cited and carefully scoped in report).

**Corpus:** directive unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic Git blob 2,539,489 chars SHA f80790efd768574555a85703a14820e1bed56b70; issue #3 through TMR-1/021, AGENTS, CODEX, repo skill, all five latest handoffs, original TMR-2/019-/020 reports/source/raw, TMR-1/021, TMR-3/019, TMR-5/018. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex not modified. No schedules touched. General P versus NP remains OPEN.

**NEXT:** TMR-5 independently challenge the selector-triple iff and clause-essential equality; then seek a compulsory post-acquisition SAT/UNSAT processing charge robust to a finite-state E3 mask, unrestricted caching, sharing, Horn/2-SAT/GF(2), repeated input rereads and arbitrary polynomial work space.

END_OF_HANDOFF::TMR-2::2026-11-14_0725_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 06:24 PST | EXACT THREE-VARIABLE CUBE SIGN ASYMMETRY020

**TMR2-CUBE20 CANDIDATE/RESTRICTED (TMR-1/TMR-5 review requested):** For the actual 3-bit-per-clause proper-3CNF fixed-three-variable sign language E3, clause signature sigma excludes exactly assignment sigma. With multiplicities c_sigma, formula UNSAT iff all eight signatures occur. Exact number of valid SAT/UNSAT label-changing singleton sign flips:
- UNSAT: s=3 times the number of singleton signatures, at most 24 irrespective of clause count; all eight once gives s=24, all twice gives s=0.
- SAT with two or more missing signatures: s=0.
- SAT with unique missing signature a: s=sum_j c_(a xor e_j)*1[c_(a xor e_j)>=2].
**Explicit infinite SAT family:** six signatures 010..111 each once, plus R+1 copies of 001 ordered last; missing 000. L=3(R+7), s=R+1, last physical bit sign flip yields valid UNSAT, so every correct original-input-local deterministic decider physically reads that last bit and spends at least L steps. A fixed finite-control 8-bit mask scanner classifies ALL E3 sources in O(L) time and ZERO visited writable work cells. Thus Theta(L) valid-label acquisition does not force superlinear semantic SAT processing.

**NEW G20 CANDIDATE/RESTRICTED:** On arbitrary UNSAT proper width-3 CNF with n variables, m occurrences, a sign-pivotal clause must be deletion-essential. Choose for each essential occurrence a distinct witness satisfying all other clauses, which injects essentials into the 2^n assignments. Duplicates are nonessential and only 8*binom(n,3) distinct proper clauses exist. Therefore s_UNSAT,sign<=3*min(m,2^n,8*binom(n,3)). At n=3,m=8 this is tight (24). This does NOT bound multi-bit changes, proof work, or unrestricted decision time.

**ACTUAL native CPython, published exact code/raw and verified Git blobs:** 125,970 count multisets for m=0..12, 4,031,040 actual one-sign mutation comparisons, 125,475 SAT and 495 UNSAT signature multisets, 880 independent literal-evaluation checks, 180 order shuffles, 48 symmetry controls, 8 2-SAT auxiliary controls, Horn/XOR/product controls, 9 malformed tests, all zero failed assertions. One 18.022-second process; finite evidence COMPUTATIONAL and no universal TM compiler.
- Report: research/agents/tmr-2/2026-11-14_0624_TMR2_CUBE_SIGNATURE_ASYMMETRY020.md
- Exact natively executed: experiments/tmr/tmr2_cube_signature020.py (Git blob 86de36517fd9e4c24d4a7ac99e1f0f2d6cef74ea)
- Immutable raw: results/raw/tmr/2026-11-14_0622_TMR2_CUBE_SIGNATURE020_RAW.json (Git blob 2dd51dc27ac95e95e20d32bcc8339dd14f560659)

**CORPUS:** TMR replacement directive first/rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Complete proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 1,051,196 chars via exact Git blob 930c5eeddafce656717f28055a7a9a755f44737c, canonical main.tex 2,536,131 chars via blob f0054c990e11602b4b60ead3bccffa73f11d0d7b; AGENTS.md, CODEX.md, skill, issue #3, all 5 new TMR peer handoffs; original TMR-2/017/019, TMR-3/018, TMR-5/017, TMR-1/020; Nisan 1991, Buhrman-de Wolf 2002, Kullmann-Zhao 2013. Older assignment rules superseded, verified history retained. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex reserved for TMR-5. NO task changes.

**NEXT:** TMR-5 independently audit U20/S20/G20 and local-head last-bit charge; find an unavoidable SAT semantic-processing invariant robust to complete acquisition, cache/recompute, Gaussian elimination, Horn/2SAT, alternate encodings and polynomial workspace. Full 3-SAT superpolynomial all-exponent bound and P versus NP remain OPEN.

END_OF_HANDOFF::TMR-2::020::2026-11-14_0624_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 05:12 PST | ORDINARY VALID-LABEL SIGN SENSITIVITY019

**NEW TMR2-HSS19 CANDIDATE/RESTRICTED pending TMR-5/TMR-1 review.** For one fixed explicitly encoded proper 3-CNF grammar E with unary n and c headers and fixed-width signed occurrence IDs, construct an unbounded n=9 family F_m with 12 four-clause forcing gadgets and m repeated pivots (x OR y OR z), with z=1, x=y=0 forced. All formulas F_m are SAT, and flipping *one distinct sign bit* of the z occurrence in any pivot produces a **valid, same-length UNSAT** proper 3-CNF. Encoded bit length L=203+16m. By complete-configuration deterministic input-aware coupling, EVERY correct one fixed total uniform multitape SAT decider must read all m pivotal positions, Q_A(F_m)>=m=(L-203)/16, and the last pivot sign at position L forces at least L locally moving source-head steps. No online/one-pass assumption and NO syntactic padding or malformed neighbor.

**TIGHTNESS / IMPORTANT LIMIT:** ONE fixed total correct uniform general SAT decider recognizes n=9 and solves every such valid formula by 512 complete charged scans in O(L) time, using O(L) physically visited work cells for unary clause validation. For n!=9 it uses general paid exhaustive search, potentially exponential. Thus ordinary-formula, valid SAT-vs-UNSAT, linear *single-bit* necessity still imposes NO superlinear processing work or all-polynomial-exponent exclusion. This strengthens the honest-encoding/valid-neighbor controls relative to TMR-2/017 zero singleton sensitivity and TMR-2/018 exponential syntax padding. It is not an unrestricted machine-resource lower bound.

**ACTUALLY EXECUTED hosted V8 COMPUTATIONAL:** 11 families through m=48; 156 distinct valid opposite-label single-sign flips; 234 comparisons of straightforward 512-assignment enumerator against independent 512-bit BigInt mask solver; 66 renamed SAT/UNSAT controls; 44 malformed controls; 16 forcing-gadget truth cases; 16 XOR parity cases; one Horn control; zero failures. Source prints exact raw JSON under Node. No OS Node/native CPython, full TM instruction simulator, general Gaussian solver or complete repo checkout/preflight executed.

**GitHub MAIN readback VERIFIED:**
- report research/agents/tmr-2/2026-11-14_0512_TMR2_HONEST_VALID_LABEL_SENSITIVITY019.md (blob 7499862d53991d132390e9fc1cb1fb07c47d0395)
- source experiments/tmr/tmr2_honest_valid_sign_sensitivity019.cjs (blob aa7c249ef0884e2d46579cf6d81f3eca17cda444)
- raw results/raw/tmr/2026-11-14_0512_TMR2_HONEST_SIGN_SENSITIVITY019_RAW.json (blob 529066c130e7ac899576c79aa5275ed95e6400a6)

**READ/PRESERVE:** New TMR directive read first/rechecked; complete proof1 (28,714 chars, 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2 (1,051,196 chars, 930c5eeddafce656717f28055a7a9a755f44737c) read via file/blob, canonical main.tex (2,533,636 chars, 867c9b7512a51d59a50c479e81dda6c65615026f) via Git blob, AGENTS.md/CODEX.md/repo skill, latest issue #3 through TMR-5/016, all five peer handoffs, original TMR2/017-/018 and TMR1/018 and TMR5/016. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left untouched for TMR-5 synthesis. NO task mutation. Primary query-model sources checked: Nisan SIAM J. Comput. 1991 doi:10.1137/0220062; Buhrman/de Wolf TCS 2002 doi:10.1016/S0304-3975(01)00144-X.

**PEER TARGETS:** TMR-5 audit 12-gadget forcing, exact last-bit offset and actual charge of n=9 512-sweep decider. TMR-1 audit all-length totality and encoding. TMR-3 audit T=Theta(L) same-run charges. TMR-4 test source-aware abstract continuation and retention. One next objective: a compulsory SEMANTIC processing charge immune to constant-variable sensitivity, copied input, Horn, 2SAT, affine XOR and bounded-treewidth shortcuts. P versus NP OPEN.

END_OF_HANDOFF::TMR-2::2026-11-14_0512_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 04:20 PST | SYNTACTIC PADDING CERTIFICATE018

**NEW TMR2-SYN18 CANDIDATE/RESTRICTED (proof given; independent TMR-5/TMR-1 review pending):** For any fixed total correct physical deterministic single-input-head decider of the exponentially padded syntax p(x)=1^L 0 x 0^(2^L), N=2L+1+2^L, all 2^L dummy-zero suffix cells MUST be read on EVERY valid input if SAT, UNSAT and MALFORMED are three distinct labels. Each one-bit suffix corruption is same-length MALFORMED, so source-aware deterministic replay forces its bit to be read. Thus Q>=2^L=N-O(log N), T>=N on the physical locally moving head. With ordinary yes/no membership (malformed rejected), the same necessity holds for valid SAT padded sources, but NOT necessarily UNSAT padded sources.

**INDEPENDENT TMR-1/018 mathematical peer audit:** Its fixed-total polynomial-N exhaustive padded decider is legitimate for this non-honest representation: 2^r<=2^L<=N occurrence assignments; fully charged syntax parsing and assignment checks cost O(N poly(log N)) and O(log N) work space. Unpadded-to-padded mapping costs Omega(2^L) output transitions, so NO polynomial-time standard 3SAT algorithm or separation follows. Query certificates can be dominated by syntactic validity rather than SAT processing. Both the TMR-1/018 honest-polynomial-translation safeguard and earlier TMR-2/017 source-aware transcript lemma survive this independent argument; all-exponent standard-3SAT bottleneck remains OPEN.

**ACTUALLY EXECUTED native CPython, exact source and raw published/readback:** 511 valid payloads (17 SAT / 494 UNSAT); 6,613 suffix-bit corruptions; 1,533 length/delimiter invalid controls; 30 separate exhaustive proper-three-distinct-variable CNF gadget checks; 95,064 physically current-cell reads on valid sources, 631,526 on corruptions, zero failed assertions. The semantic parser/brute evaluator is Python, not a full physical arbitrary-A TM compiler; finite evidence COMPUTATIONAL only. Exact raw/source local Git blob hash matched GitHub fetched SHA.

**Verified GitHub files:**
- research/agents/tmr-2/2026-11-14_0420_TMR2_PADDING_SYNTAX_CERTIFICATE018.md (blob 58b9899d042b9f34f39f08aa8eed6296e32427ae).
- experiments/tmr/tmr2_padding_certificate018.py (blob a963cef2dab1d53aa5dc887f29b002432ca89e9b).
- results/raw/tmr/2026-11-14_0420_TMR2_PADDING_CERTIFICATE018_RAW.json (blob e6ad24dafe2f8780b08fd44051e5a3d04e11367b).

**Required reads and preservation:** Replacement directive unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; root proof1 complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; root proof2 complete blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c despite blank contents endpoint; root main.tex complete blob 2,530,965 chars SHA 91b4e582c16cb7f60c9aa1ea2aebf09cd4caa2c6. All five handoffs and issue #3 through TMR-1/018; AGENTS/CODEX/skill, original TMR-1/018, TMR-2/017, TMR-4/018 and TMR-5/015; primary Buhrman/de Wolf 2002 and Berman/Hartmanis 1977. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No main.tex or schedule changes.

**One next target:** an unavoidable cost of processing SAT/UNSAT after normalizing to a polynomially balanced, honest bit encoding, impervious to once-copied input, arbitrary polynomial workspace, cheap Horn/GF(2)/2SAT global summaries, and speculation. Request TMR-5 to audit SYN18 and encoding quantifiers; P versus NP OPEN.

END_OF_HANDOFF::TMR-2::2026-11-14_0420_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 03:26 PST | DISJOINT SIGN-BLOCK QUERY CERTIFICATES017

**NEW TMR2-SBC17 CANDIDATE/RESTRICTED pending TMR-5/TMR-1 independent review:** For any ONE correct, fixed total uniform one-source-head deterministic 3-SAT machine A and source x, the complete actual set Q_A(x) of physically READ data cells is a deterministic decision certificate: every equal-length y agreeing on those cells induces the exact same full execution and terminal label. If opposite-label y_j differ from x only within pairwise disjoint bit blocks B_j, then Q_A(x) must hit ALL B_j. This is a source-aware theorem from shared initial states, not a false inference about arbitrary merged intermediate workspaces.

**EXPLICIT INFINITE PROPER-3CNF FALSIFIER:** Expand minimally unsatisfiable Horn 2-CNF chain (x1), (not x_i or x_{i+1}), (not x_n) into private-auxiliary proper three-distinct-variable clauses. H_n has N=2n+3 variables, m=2n+6 clauses. EVERY clause contains one designated auxiliary-sign bit whose flip makes H_n SAT. Repeat each clause r times (r=2 or 3); the resulting F_n,r remains UNSAT, EVERY singleton sign flip remains UNSAT, yet for each of m disjoint r-bit blocks, flipping all copies of the chosen clause yields a genuine SAT source. On the fixed gamma-header/fixed-width literal binary grammar L=Theta(rn log n), these are m disjoint opposite-label blocks, forcing >=m=Omega(L/log L) distinct input reads for fixed r. A late block also forces head travel Omega(L) from the physical left marker. All these lower bounds remain at most LINEAR and are compatible with an all-input correct fixed SAT decider that recognizes this simple Horn-gadget family and its block flips in polynomial time, otherwise uses general exhaustive SAT. ZERO singleton sensitivity does not imply ZERO block certificate complexity, nor exponential decision cost.

**EXECUTED AND SHARED GitHub main:** report research/agents/tmr-2/2026-11-14_0326_TMR2_SIGN_BLOCK_CERTIFICATE017.md; exact hosted-V8/Node-compatible source experiments/tmr/tmr2_sign_block_certificate017.cjs; raw results/raw/tmr/2026-11-14_0324_TMR2_SIGN_BLOCK017_RAW.json. Hosted V8: n=1..14,r=1,2,3, 882 independent SAT block witnesses, 588 singleton-UNSAT controls, 511 DPLL tests (n<=7), 42 parser roundtrips, 3822 work checks, zero failures. Independent native CPython LOCAL-ONLY: 882 block witnesses, 588 singleton controls, 511 DPLL checks, zero failed assertions in 0.179 seconds. Finite evidence COMPUTATIONAL. Complete all-n symbolic argument in report, peer review pending.

**CORPUS/STATUS:** superseding directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, complete proof1 28,714 chars, complete proof2 Git blob 1,051,196 chars, main.tex Git blob 2,528,412 chars; issue #3 through TMR-1/017; AGENTS/CODEX/skill; all TMR handoffs; original TMR-2/016 report/code/raw, TMR-2/015, TMR-1/017, TMR-3/015, TMR-4/017, TMR-5/014, historical affine factored-compatibility source. Literature Nisan 1991 and Buhrman/de Wolf 2002 QUERY-model scope only. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex unchanged under TMR-5 synthesis ownership. No tasks changed. P versus NP OPEN.

**ONE NEXT TARGET:** a genuinely compulsory computational-processing distinction that survives full source acquisition, cheap auxiliary-variable elimination, caching/rereads and all polynomial workspace. TMR-5 independently review SBC17 sign blocks, physical bit offsets and copy-major encoding; TMR-3 charge same-machine retrieval; TMR-4 audit all-transition source-bound abstraction.

END_OF_HANDOFF::TMR-2::2026-11-14_0326_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 02:18 PST | SOURCE-AWARE CHECKPOINT REACQUISITION016

**NEW TMR2-CR16 CANDIDATE/RESTRICTED pending independent TMR-5/TMR-1 audit:** On any one fixed total correct single-original-input-head decider, if two opposite-label equal-length inputs x,y reach checkpoints with identical finite control, all writable tape contents/heads and source-head position p, both continuations must read a source position in D={j:x_j!=y_j}; otherwise determinism forces the same terminal label. With locally moving head and current-cell reads, both pay at least 1+min_{j in D}|j-p| remaining transitions. This is a CONDITIONAL geometry necessity, not compulsory merging of arbitrary solver runs.

**NEW TMR2-WASH16 CANDIDATE/RESTRICTED all-input wrapper:** For every fixed eligible A, compile one fixed B_A which physically reads every one of L source bits during one complete outward sweep, returns input head to left, discards any observed finite-control information and executes A unchanged. Exact same-source T_B=T_A+2(L+1), S_B=S_A. At the post-prepass checkpoint the **entire internal state excluding immutable source is identical** across all inputs, including opposite-label ones, yet B_A remains correct by rereading source. This precisely falsifies source-blind internal-state indistinguishability, while demonstrating why the source must be bound in an abstraction.

**EXACT opposing labels at an unbounded late source cell:** fixed 3-variable proper-clause sign-stream instances [0,1,2,3,4,5,6] + r duplicate zeros + final mask 6 (SAT) versus 7 (UNSAT) differ ONLY at bit L=24+3r. They hit the same erased checkpoint at physical head position 0. Hence a post-checkpoint correct distinction costs at least L+1 transitions. One fixed 8-mask finite-state two-sweep controller decides SAT/UNSAT/MALFORMED for all sign-stream lengths in T=4(L+1)+1 and S=0. Restricted regular family, not unrestricted 3-SAT.

**INDEPENDENT TMR-3/014 peer check:** The locally moving original-input-head two-crossing projection c_i=(x_i,parity(x)) and its sharp one-crossing suffix-dependence impossibility withstand a separate mathematical argument, at **PROVED/RESTRICTED physical single-head scope**. No general crossing-code normalization or all-exponent SAT lower bound follows. Original TMR-3 report, its Python source and raw data, plus original TMR-4/016 and TMR-5/013, were read.

**NATIVE CPython source, exact Git blob 59b068d55aabdab6337df8ee6a497c84451f75e9:** experiments/tmr/tmr2_checkpoint_reread016.py. **RAW exact Git blob 26a22a1daffa6c44a80b2ca52f567b5a03acc08e:** results/raw/tmr/2026-11-14_0218_TMR2_CHECKPOINT_REREAD016_RAW.json. One 1.64-second native OS run: 8,191 exhaustive binary strings length 0..12; all 40,320 eight-mask UNSAT permutations; 129 last-bit SAT/UNSAT sibling pairs through L=408; 4,697,933 charged transitions; 2,227,044 physically positioned data-cell reads; 180,228 separate two-crossing-prepass events; ZERO failed assertions. Finite evidence COMPUTATIONAL.

**Verified report:** research/agents/tmr-2/2026-11-14_0218_TMR2_CHECKPOINT_REREAD_NECESSITY016.md, blob dee0b280f04cdd0907ef6c5cf18e906ed91cbf01. Code and raw readback matched exact locally tested Git blobs. Primary context: Buhrman/de Wolf 2002 DOI 10.1016/S0304-3975(01)00144-X; Hennie 1965 original off-line crossing sequence work. Do not infer an unrestricted SAT lower bound from either.

**Corpus/edits:** Superseding replacement directive reread unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; complete proof1 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; complete authentic proof2 Git blob 1,051,196 chars 930c5eeddafce656717f28055a7a9a755f44737c; complete authentic main.tex Git blob 2,525,134 chars d3db01d221df39f096f31237643268132edfcd87; issue #3 through TMR-5/013, AGENTS, CODEX, skill, all newest peer handoffs. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex left for TMR-5 synthesis. No tasks/schedules modified. P versus NP OPEN.

**NEXT ONE TARGET:** attempt an unconditional source-aware distinction cost for arbitrary solver traces *without* postulating equal-state checkpoints, preserving compact algebra, all-length uniformity, adaptive rereading and arbitrary polynomial workspace. TMR-3 to test same-trace charges, TMR-4 to model immutable source binding, TMR-5 to independently falsify or verify CR16/WASH16.

END_OF_HANDOFF::TMR-2::2026-11-14_0218_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 01:18 PST | PHYSICAL FULL-SUFFIX CROSSING NO-GO015

**NEW TMR2-PC15 CANDIDATE pending TMR-5/TMR-3 peer review:** For ANY one fixed correct total uniform local-input-head 3-SAT decider A, a single fixed B_A physically computes XOR parity P of all L encoded source bits by one rightward scan, returns left, optionally repeats a full roundtrip when P=0, then runs A from its unchanged initial configuration. Exact same-input costs are T_B=T_A+2(L+1)(1+[P=0]) and S_B=S_A. All outputs, including malformed, are preserved; prepass is 2 or 4 genuine local crossings at EVERY original cut, globally correlated by one parity bit. At a cut just after a selected free sign bit X_i, the tagged forward/backward crossing-state projection c_i=(X_i,P) is conditionally prefix-free and depends on EVERY future free sign bit X_j; for K free original sign bits from valid authenticated G_r sources, all R_i=K, so interval depth D=K=Theta(L/log L) for this natural physical crossing-code projection. This **falsifies any universal small-future-dependence inference from independent source blocks, local heads, read-only source or both-label correctness alone**, NOT TMR-5/012 ID12 and NOT every possible crossing-record normalization. Useless prepass can be normalized only with separately proved cost-soundness, not by assertion. General SAT processing lower bound remains OPEN.

**INDEPENDENT PEER MATHEMATICAL VERDICT: TMR-5/012 ID12 PROVED/RESTRICTED CODING SCOPE.** Conditional prefix-free Y_i=2^(q_i-|c_i|) has E[Y_i|past]<=1. Greedy coloring of intervals [i,R_i] into D nonoverlap classes, iterated conditional expectation, Holder and Markov prove Pr[sum|c_i|<sum q_i-b]<=2^(-b/D). Exact coding premise reviewed; NO transfer to all correct two-way SAT crossing codes established.

**ACTUALLY EXECUTED:** Exact published standalone hosted V8 executable checked all 2,047 binary inputs lengths 0..10 plus 259 24-bit SAT/UNSAT source fixtures (2,306 total), 18,434 bitflips, 18,434 conditional prefix-free code fibers, 18,434 actual crossing-code projections, 109,156 counted local transitions; SAT 842, UNSAT 2, MALFORMED 1,462, ZERO failed assertions. Independent native CPython implementation, locally executed, checked 2,306 different deterministic test fixtures, 18,434 bitflips/fibers, 109,856 counted transitions, ZERO failures. Source/fixtures differ across V8 and Python; the native Python artifact is LOCAL-ONLY. Both finite runs COMPUTATIONAL, not an arbitrary-machine SAT compiler.

**VERIFIED GITHUB MAIN:**
- Report research/agents/tmr-2/2026-11-14_0118_TMR2_PHYSICAL_SUFFIX_CROSSING_PEER015.md, Git blob a681982e194cfc2d2da6fb80e9d6d3f886d383b5.
- Exact executed JS experiments/tmr/tmr2_physical_suffix_crossing015.cjs, Git blob dc1e65f3f39b7eb45c9f7d83ffd727dec6dd926b.
- Immutable raw results/raw/tmr/2026-11-14_0116_TMR2_PHYSICAL_SUFFIX015_RAW.json, Git blob 0cf0d5be1b4a594b1fd1cea58e804083914b26e2.

**Corpus:** Current 12:49 PST directive first and rechecked unchanged blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 full 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 recovered authentic full Git blob 1,051,196 chars 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic full Git blob 2,522,180 chars 903092cd483c0b17694c9f500fa03b5a703508cc; AGENTS, CODEX, project skill, issue #3 through TMR-1/015, all newest TMR handoffs, original TMR-3/012,/013, TMR-5/012, TMR-4/015, TMR-1/015, TMR-2/014 and primary Hennie 1965, McMillan 1956. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex left for TMR-5. No scheduled tasks modified. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 independently review PC15's genuine phase-tagged crossing projections and attempt a fully charged canonical-normalization theorem; TMR-3 seek a representation-independent physical causality property surviving the O(L) parity wrapper. All-exponent SAT resource arrow OPEN.

END_OF_HANDOFF::TMR-2::2026-11-14_0118_PST

---

# TMR-2 CURRENT handoff | 2026-11-14 00:17 PST | SEVEN-CERTIFICATE EXTREMAL PEER AUDIT014

**Peer verdict PROVED/RESTRICTED:** TMR-5/011's inclusion-minimal seven-original-sign-query theorem holds on the authenticated eight-mask G_r promise. Independent Hall analysis shows every such query set is exactly four equal coordinate/value one-bit observations plus three equal observations on a second, distinct coordinate, all in different clause rows; an UNSAT permutation completion is available after deleting any one observation. The original TMR-5/011 exact M7 intersection-count formula survives. Neither a general SAT processing lower bound nor a compulsory storage statement follows.

**NEW TMR2-M7MAX-014 CANDIDATE pending TMR-5/TMR-1 review:** For all ordered eight-mask tuples, M7 <= 1680, equality iff all eight masks identical. For coordinate-balanced eight-mask tuples, M7 <= 48, equality iff all three binary columns are pairwise equal or complementary. Exactly 280 balanced ordered tuples attain 48. Analytic proof: each of six ordered distinct coordinate pairs contributes at most C(8,4)C(4,3)=280, and balanced two-column intersection t contributes g(t)=4[C(t,3)+C(4-t,3)] in {0,4,16} per unordered pair.

**Actual independent native CPython:** 343,000 balanced tuples exhaustively swept; 4 fixtures x C(24,7)=346,104 seven-bit query sets, each tested against 40,320 explicit UNSAT mask permutations through compatibility bitsets and deletion checks; 1,384,416 direct query classifications, 0 failures. Native runtime 9.28 seconds, no wrapper or TMR-5 code import. Observed M7=48 for (0,0,0,0,7,7,7,7); 1680 for (7 repeated eight times); 16 for (0,0,1,1,6,6,7,7); 0 for UNSAT (0,1,2,3,4,5,6,7). These finite tests are COMPUTATIONAL and are NOT a physical all-length SAT machine.

**Verified GitHub main paths:** report research/agents/tmr-2/2026-11-14_0017_TMR2_M7_EXTREMAL_PEER_AUDIT014.md (blob 3830707e1068e44fd692828d69ca9d4ff854044d); exact published/native-tested executable experiments/tmr/tmr2_m7_independent014.py (blob 35bf642a99b6d5e6718f1844f206b8222083f2eb); native-exact raw results results/raw/tmr/2026-11-14_0017_TMR2_M7_EXTREMAL014_RAW.json (blob 54e8db04619f8c038150d66aa9cfdf232ae4fcf8).

**Preflight:** Superseding TMR directive rechecked unchanged blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4. proof1.txt recovered full 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered full authentic Git blob 1,051,196 chars 930c5eeddafce656717f28055a7a9a755f44737c; main.tex recovered authentic complete 2,518,238 chars blob 0233cb0ca16a63a2a63a83af6a61ffe985632945. AGENTS.md, CODEX.md, repo skill, latest issue #3, five peer handoffs and relevant TMR/historical original papers reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex unchanged, owned by TMR-5. No schedules touched. All-exponent P versus NP processing bottleneck OPEN.

**ONE NEXT TARGET:** TMR-5 independently audit sharp maximum/equality cases; thereafter seek a noncircular, program-specific, full-configuration processing cost after input copying, allowing cached representations, GF(2), recomputation, rereads and polynomial space.

END_OF_HANDOFF::TMR-2::2026-11-14_0017_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 23:12 PST | ALL-MASK SIX-CERTIFICATE FORMULA013

**NEW TMR2-ALL6-013 CANDIDATE pending TMR-5/TMR-1 independent mathematical review.** For every arbitrary ordered eight-row 3-bit mask source a in the full strict original G_r template, WITHOUT balancing, let f_m count full-mask occurrences, f_{J,v} count equal two-coordinate projections, and n_{j,b} count rows with a given polarity coordinate/value. The exact numbers of SAT-forcing original-sign certificates of sizes five and six are

$$
N_5(a)=\sum_{j,b}\binom{n_{j,b}}5
$$

and

$$
N_6(a)=\sum_m\binom{f_m}2+
\sum_{|J|=2,v}\binom{f_{J,v}}3+
\sum_{j,b}\left[\binom{n_{j,b}}6+(24-n_{j,b})\binom{n_{j,b}}5\right].
$$

The three disjoint six-query types are two identical fully observed masks, three matching two-bit projections, and six-position supersets of a five-row single-halfcube certificate. Direct Hall violation classification handles every row subset size 1..8, including the unbalanced five- and six-row deficiencies. **TMR5-SIX10 independently reviewed PROVED/RESTRICTED:** under coordinate 4/4 balance, n_{j,b}=4 and the new third term vanishes, yielding precisely the peer formula. The prior unbalanced tuple (1,2,3,4,5,6,7,7) has N_5=3 and N_6=61, partitioned 1+3+57; the balanced-only formula would incorrectly give 4. Source-bit acquisition and post-acquisition computing remain distinct; no superpolynomial 3-SAT lower bound.

**Actual independently authored native CPython audit, not Hall or peer matching code:** all 8!=40,320 UNSAT completions were encoded as compatibility bitsets; for EACH of eight control tuples every binom(24,5)=42,504 and binom(24,6)=134,596 source-query subset was replayed against all possible UNSAT completions. 1,416,800 five/six query subsets, 8.154 seconds, ZERO failed assertions. Exact source Git blob 8b78e6a7ba4f91547d165d09e7d4de19496bc61e matches natively executed file; exact full native JSON Git blob fa08876bf8ce1fd0e235ff8d7c22613e4a61b2e1. This is COMPUTATIONAL for finite cases plus a separate mathematical scoped proof, not an arbitrary physical SAT-machine simulation.

**Readback-verified on main:**
- Report: research/agents/tmr-2/2026-11-13_2312_TMR2_ALL_MASK_SIX_CERTIFICATE_FORMULA013.md, blob b807fc16e9f8e5acd415beebfa8917626464ba2f.
- Executed native source: experiments/tmr/tmr2_all_masks_c6_013.py, blob 8b78e6a7ba4f91547d165d09e7d4de19496bc61e.
- Immutable exact native raw output: results/raw/tmr/2026-11-13_2312_TMR2_ALL_MASK_C6_013_RAW.json, blob fa08876bf8ce1fd0e235ff8d7c22613e4a61b2e1.

**Corpus:** controlling directive first/rechecked unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c despite empty normal fetch; root main.tex recovered authentic Git blob 2,515,087 chars SHA c9944b36cc043c7a0c1808b8ffbbacc19ea4350b; issue #3 through TMR-1/013; AGENTS/CODEX/skill, five current TMR handoffs, ORIGINAL TMR-2/010,/011,/012 and TMR-5/010 proof/code/raw, and primary Hall 1935 and Buhrman/de Wolf 2002. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex not edited; no tasks/schedules altered. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5/TMR-1 independently audit unbalanced s=5/6 Hall cases and no-double-count certificate partition; then search for representation-independent processing necessity after a full input copy that survives arbitrary polynomial workspace, compact algebra, sharing and recomputation.

END_OF_HANDOFF::TMR2::2026-11-13_2312_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 22:15 PST | BALANCED MASK CERTIFICATE DICHOTOMY012

**NEW TMR2-BC12 CANDIDATE pending independent TMR-5 review.** Exact promise sign-bit certificate size for EVERY SAT block of TMR-2/010's original strict-proper all-declared-ID-used 8-mask 3-CNF grammar is **5** if any sign coordinate is biased at least 5-to-3, otherwise **6** if all three sign coordinates balance 4-to-4. SAT product complexity is the SUM of block costs; every UNSAT source still has certificate size 24. Five-query characterization proved by Hall matching: only five different rows querying the identical one-bit/value half-cube can defeat an eight-mask permutation. Every SAT row tuple contains a duplicate complete mask, giving a six-bit upper certificate.

**Concrete balanced family:** each of r core blocks has (0,0,3,3,5,5,6,6), so exact certificate 6r and sign-only Hamming radius four to UNSAT. No robustness claim for arbitrary identifier edits. Any fixed correct h-original-input-head total deterministic decider must observe 6r distinct original source sign bits on this SAT input, hence T>=ceil(6r/h)=Omega(L/log L); no workspace/online/one-pass assumption. TMR-2/010 polynomial authenticated mask-classifier defeats any superpolynomial processing inference.

**EXECUTED published-exact native Python 3.13.5:** 55,455 old SAT tuple query subsets of sizes <=5, 190,051 balanced tuple subsets of sizes <=6; old 3 five-bit certificates, new 0 certificates <=5 and exactly 4 six-bit certificates; 144 sign-distance-four UNSAT neighbors, none closer; r=1,2,3,8,64 product mask controls, zero failures. Independent LOCAL ONLY bit-parallel Python tested all 40,320 permutation completions against all 55,455 balanced <=5-bit queries, zero failures. No physical TM or new full binary source parsing.

**GitHub readback-verified artifacts:**
- Report research/agents/tmr-2/2026-11-13_2215_TMR2_BALANCED_MASK_CERTIFICATES012.md, blob 8616da950d8afac88fa43ed5079de6b10602ad00.
- Exact native code experiments/tmr/tmr2_balanced_mask012.py, blob b1ec9df7174b8f72c1f04c854dff4decb0488978.
- Immutable raw results/raw/tmr/2026-11-13_2215_TMR2_BALANCED_MASK012_RAW.json, blob 9b04d3d3e0e4557ac7d32dce5ef8d2031dd481bb.

**Corpus:** First read current superseding TMR directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 complete SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 full authentic 1,051,196-character Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex full authentic 2,511,782-character blob SHA c04a02a97492f88938791f363ff91d99b67cd78b, issue #3 through TMR-1/012, AGENTS/CODEX/skill, current five TMR handoffs and original TMR-2/010,/011, TMR-5/007, TMR-1/010, TMR-4/008 handoff. Primary Hall 1935 and Buhrman/de Wolf 2002 checked. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No canonical main.tex or scheduled task edit. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 independently verify the five-query Hall uniqueness and 6r additivity; then identify and red-team a true post-input-acquisition computational-work potential valid for arbitrary polynomial workspace and compact algebra.

END_OF_HANDOFF::TMR2::2026-11-13_2215_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 21:15 PST | EXACT MASK CERTIFICATE011

**New TMR2-CERT11 CANDIDATE pending TMR-5 peer review, complete symbolic proof in report; independently executed native Node and Python COMPUTATIONAL.** In the same strict all-ID-used 3-CNF authenticated two-label mask superclass G_r from TMR-2/010, take z_r with each block mask list (1,2,3,4,5,6,7,7). The exact **promise sign-bit certificate complexity** is C_G(z_r)=5r, and for **every UNSAT** template source u, C_G(u)=24, independent of r. Every observation set of <=4 bits on any eight-row mask block can be completed to an UNSAT 8-mask permutation by Hall's matching theorem, while observing bit 0 of rows 0,2,4,6,7 makes such a permutation impossible (five 1-valued row bits, only four such distinct masks). All SAT blocks require independent certificates, whereas a single full UNSAT block requires exactly all its 24 sign bits. These are original bit-position certificates, not compulsory solver memory.

**Machine-transfer lemma:** On a fixed total correct finite deterministic multitape SAT decider A with h physically charged original-input heads, replay any other same-length input agreeing on ALL actually observed positions: the entire halting execution is identical, with arbitrary rereads/work tapes and no online assumption. Therefore T_A(z_r)>=ceil(5r/h)=Omega(L/log L) for fixed h, strictly strengthening prior r triple supports in the source-observation count, but **not** post-acquisition processing or P != NP. The TMR-2/010 polynomial authenticated full two-label mask classifier remains a representation-aware hostile control. TMR-4/009 spatial Omega(L) may dominate under local left-aligned heads.

**Executed:** published-exact native Node v22.16.0 matching verifier audited all 12,951 subsets of <=4 sign positions, all 42,504 five-subsets (three certificates), 24 UNSAT one-bit flips, 500 deterministic local semantic checks, zero failures. Independently authored native Python 3.13.5 enumerated all 8!=40,320 full UNSAT permutations using bit-parallel intersection over all 55,455 subsets of 0..5 queried bits, identical counts and zero failures. These are source/query models, NOT physical TMs or all-length machine compilers.

**Verified main publication, exact local-executed blob matches:**
- report research/agents/tmr-2/2026-11-13_2115_TMR2_EXACT_MASK_CERTIFICATES011.md (blob 8540aea195ba565b0938d46d59d4240ed070cf8b).
- Node experiments/tmr/tmr2_exact_mask_certificate011.cjs (blob 59bf20cd2a9a9399e0e3edebf52047619495d8ba); raw results/raw/tmr/2026-11-13_2115_TMR2_EXACT_MASK_CERT011_RAW.json (blob 58bf29fc2012badef7e1e0dbd54391d8be8377f4).
- independent Python experiments/tmr/tmr2_mask_certificate_independent011.py (blob 9684e5673ce1c2236844b0b2277d8dc48572081c); raw results/raw/tmr/2026-11-13_2115_TMR2_MASK_CERT_INDEPENDENT011_RAW.json (blob 332c1079a0d0a9d30f1c68622a897acaa18dec7d).

**Corpus:** 12:49 TMR replacement directive read first and rechecked, proof1 complete 28,714 chars; proof2 authentic complete 1,051,196-char Git blob (normal fetch blank), root main.tex authentic 2,507,300-char blob (normal fetch blank), latest issue #3, AGENTS/CODEX/skill, all newest five TMR peer handoffs, original TMR-2/010 report+JS, TMR-4/008, TMR-5/007, TMR-1/010, TMR-4/009, historical TMR-2/009; verified primary P. Hall 1935 and Buhrman/de Wolf 2002. TRACKERS REVIEWED; NO MATERIAL CHANGE. No authorized main.tex edit and no tasks modified. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 independent review of Hall's any-four-bit matching argument and full r-block logical product. Then identify an input-aware **processing** necessity that cannot be satisfied by the authenticated mask-table classifier, algebraic shortcuts, caching or recomputation.

END_OF_HANDOFF::TMR-2::2026-11-13_2115_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 20:17 PST | TWO-LABEL STREAMING MASK CLASSIFIER010

**NEW TMR2-SCAN10 CANDIDATE pending TMR-5/TMR-1 independent full-machine review. Restricted structural SAT theorem symbolically established; native source tests COMPUTATIONAL.** The exact strict-proper-3CNF, all-declared-ID-used template includes every core sign pattern on r disjoint eight-clause, three-variable blocks with fixed even-parity IDs and canonical all-positive spare-ID fillers: 2^(24r) distinct same-length sources, both SAT and UNSAT. The answer is UNSAT iff some block's eight polarity masks cover all eight possible 3-bit tuples. With unary counts N,M, derive r=(M-ceil(N/3))/7. A ONE fixed total correct deterministic finite multitape machine with ONE adjacent-moving input head can authenticate and decide all template sources in candidate O(L(1+log L)^2) transitions, O(log L) visited writable cells, with a fully charged exhaustive fallback elsewhere. This strengthens prior unspecified polynomial mask-table shortcut into a quantified near-linear and small-workspace *same-machine* escape. The concrete all-length compiler/transition table is not executed, so bound awaits independent review.

The TMR-5/007 and TMR-1/010 SAT source z_r with duplicated mask 7 and all r triple-sign UNSAT neighbors lie INSIDE this efficiently decidable two-label class. Source first-read indistinguishability still proves only T_A(z_r)+1 >= ceil(r/h) = Omega(L/log L) for every correct h-local-head machine. No post-acquisition all-exponent superpolynomial time implication is available. Independent peer audit supports TMR-1/010 full literal-field radius-two SAT claim at its exact grammar scope, including same-target two-ID edits; the new streaming decoder is not a P=NP algorithm.

**Actually executed NATIVE:** Node v22.16.0 exact published code and byte-identical raw: 2,260 template sources (1,635 SAT, 625 UNSAT), 1,400 brute core assignment comparisons, 52 valid triple-sign UNSAT neighbors, 32 rejected noncanonical inputs, 2,904,533 monotonically ordered source-bit reads, 0 failures, max L=4,004. Independent Python 3.13 code: all 7,140 distinct 2-field-bit mutations for r=1, plus 2,988 random r=2 and 498 random r=3; 8,626 valid SAT witness cases, 2,000 invalid, 0 failures. Not physical TM execution; all-length upper is a symbolic construction.

**READBACK VERIFIED MAIN:**
- Mathematical report: research/agents/tmr-2/2026-11-13_2017_TMR2_STREAMING_MASK_CLASSIFIER010.md, blob 0d5abb7497284ae742e5e761781dff3c069e8b46.
- Native Node exact executable: experiments/tmr/tmr2_stream_mask010.cjs, blob 897deea5c24e63f0af346dfce6adc4b189052235.
- Native Node exact raw: results/raw/tmr/2026-11-13_2015_TMR2_STREAM_MASK010_RAW.json, blob 6c09827486489390f15cf9af9170afc790dd985a.
- Independent native Python: experiments/tmr/tmr2_independent_crosscheck010.py, blob d0f177777590aea88726bd8df9e9ca3f7a3f35c9.
- Python exact raw: results/raw/tmr/2026-11-13_2015_TMR2_CROSSCHECK010_RAW.json, blob 8ff88f00ce0104c6056b4c75a8c286c0677fd925.

**Corpus:** directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 complete 28,714 chars, proof2 authentic blob SHA 930c5eeddafce656717f28055a7a755f44737c complete 1,051,196 chars; main.tex authentic blob SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064 full 2,504,241 chars; latest issue #3 through TMR-1/010, five peer handoffs, operating guides, original TMR-4/008/TMR-5/007/TMR-1/010 reports/code/results and historical legacy counterexample, primary Nisan 1991, Buhrman-de Wolf 2002 and FLMV 2005. TRACKERS REVIEWED; NO MATERIAL CHANGE. No main.tex or schedules edited. No repository checkout/preflight or physical TM table executed.

**ONE NEXT TARGET:** TMR-5 independent finite-multitape streaming-compilation and two-label authentication audit, seeking any missing charge; then search for a necessary global processing operation that a compact algebraic representation and input rereads cannot avoid. Unrestricted P versus NP still OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_2017_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 19:20 PST | DOUBLE-OCCURRENCE SOURCE SENSITIVITY009

**New TMR2-DO9 CANDIDATE pending TMR-5 audit; actual native Node source/witness controls COMPUTATIONAL. Unrestricted all-exponent uniform deterministic SAT time lower bound and P versus NP OPEN.**

**New scoped mathematical result:** Under the strict unary-header proper-3CNF grammar where **every declared variable must appear at least twice**, start with any clause-minimally UNSAT proper 3-CNF having >=3 occurrences of every core variable. Embed core ID $i$ by even-binary-parity $\rho(i)=2i+\operatorname{popcount}(i)\bmod 2$. For the $u$ complementary dummy IDs, use $K=\lceil2u/3\rceil$ distinct positive proper triples, obtained from consecutive cyclic triples (if $3\nmid u$) or two staggered disjoint partitions (if $3\mid u$). Every dummy appears >=2 times. Any original sign flip satisfies a previously falsified minimal core clause; any original identifier-bit flip targets an odd-parity dummy, which can satisfy the changed literal while other filler variables remain true. Original core occurrence decreases by at most one, so **every neighbor is still min-occurrence-two valid**. All $Q=3M(w+1)$ original literal-field bits have valid same-length SAT neighbors. Every correct h-local-binary-read-only-head deterministic SAT decider must observe all Q on the UNSAT input, yielding $T_A(F)+1\ge Q/h$. No storage bound. This is ONLY linear acquisition, not processing.

**Density:** for unbounded cores with $t\to\infty$ and min core occurrence >=3, $\liminf Q/L\ge1/3$. For the odd-charge cubic-prism 3-XOR Tseitin core with $t=3r$, $M=8r$, min core occurrence 8, $\liminf Q/L\ge4/7$. The weaker density versus TMR-5/006's $8/11$ buys a stronger grammar requiring *two* occurrences of each ID. The XOR family retains a cheap global parity algorithm, defeating any superlinear inference from sensitive input bits alone.

**Independent favorable peer mathematical review:** TMR-5/006 and TMR-1/009 one-occurrence filler arguments are valid as stated for their exact grammar, subject to standard clause-minimally UNSAT core hypotheses. This is not a general machine-time theorem. TMR2-DO9 is a distinct new construction awaiting TMR-5/TMR-1 review.

**Executed native Node.js, original code and exact results Git-blob readback verified:** 10 odd-charge strict source cases, 528 clause-deletion witnesses, 11,328 valid one-bit SAT neighbors (1,584 sign + 9,744 identifier), 11,328 min-two grammar checks, 10 filler-mutation negative controls, 5 even-charge SAT controls, 512 exhaustive small-base UNSAT assignments, zero failures. Max L=4054, Q=2304. No full physical Turing-machine instruction simulator or general fallback executed.
- Report: research/agents/tmr-2/2026-11-13_1920_TMR2_DOUBLE_OCCURRENCE_SOURCE_SENSITIVITY009.md, blob 392b7179fa96ab7ddbbfb20d887938cc0481dd5c.
- **Exact native Node source**, matched local git hash: experiments/tmr/tmr2_double_occurrence009.cjs, blob ee1d4b6eb7a0c0ebc8ebac7ddc936a85c04d89ec.
- **Exact raw JSON**, matched local git hash: results/raw/tmr/2026-11-13_1920_TMR2_DOUBLE_OCCURRENCE009_RAW.json, blob 864b08312c04bf96b3b6a2f4b8b5df0acb384f81.

**Repository state:** 2026-11-13 12:49 PST directive read first and rechecked unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 28,714 chars read; proof2 **full 1,051,196 chars** recovered via GitHub contents endpoint after empty ordinary tool output; main.tex **full 2,502,146 chars** recovered from authenticated Git blob after empty ordinary output; AGENTS.md, CODEX.md, research skill, all five TMR handoffs, original TMR-1/009, TMR-5/006, TMR-2/008 and relevant source/raw, latest issue #3, and primary Nisan 1991/Buhrman-de Wolf 2002/FLMV 2005 scopes. **TRACKERS REVIEWED; NO MATERIAL CHANGE**. Root main.tex left to TMR-5. No schedules created or modified.

**Next single target:** independently audit the new positive two-occurrence filler for all $u\bmod3$ and pursue a cost of computational processing beyond $O(L)$ acquisition that survives compact algebra, rereads, sharing and recomputation. All unrestricted lower-bound arrows OPEN.

END_OF_HANDOFF::TMR2::2026-11-13_1920_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 18:23 PST | DENSE-SOURCE-BIT-SENSITIVITY008

**New EPI8 embedding CANDIDATE pending independent TMR-5/TMR-1 review; native Node finite tests COMPUTATIONAL. All-exponent general SAT machine lower bound and P versus NP OPEN.**

**Substantive advance:** TMR-2/006 showed every literal polarity bit individually sensitive on clause-minimally UNSAT 3-CNF. EPI8 explicitly recodes *every occurring variable* i to the nonzero even-parity identifier $\rho(i)=2i+\operatorname{popcount}(i)\bmod2$, declares $N=2^w-1$ variables with $w=\lceil\log_2(2t+2)\rceil$ for t occurring variables, and leaves odd-parity IDs unused. For any clause-minimally UNSAT proper 3-CNF, changing ANY one of its $Q=3M(w+1)$ original literal-field bits, sign OR identifier, produces a valid same-length SAT instance. On a one-source-head input, $T_A(\widehat F)+1\ge Q$, and $Q/L=1-o(1)$ as t increases, under the stated fixed explicit grammar permitting unused declared IDs. No workspace restriction or online input is imposed. The result is a stronger **linear observation bound**, NOT a superlinear computational cost.

**Explicit cheap hostile family:** odd-charge cubic prism Tseitin, $t=3r$, $M=8r$, $L=2^w-1+8r+2+24r(w+1)$, with canonical clause order. One fixed total SAT machine can authenticate this source and accumulate global parity in candidate symbolic $T=O(L)$, $S=O(\log L)$ on the family, with charged general exhaustive fallback off-family. No all-input P claim.

**Actually executed:** native OS Node.js independent GF(2) and full-source parser verifier, 10 odd-charge prism cases, 528 unique-false-clause witnesses, 11,328 valid one-bit SAT neighbors (1,584 sign + 9,744 ID), 512 brute-force original UNSAT checks, 513 negative controls; 0 failures. Maximum tested $L=2529$, $Q=2304$. These are source-level computational tests, not physical Turing-machine simulations. No Horn, 2-SAT or arbitrary fallback tests executed.

**Verified main artifacts:**
- research/agents/tmr-2/2026-11-13_1823_TMR2_DENSE_SOURCE_BIT_SENSITIVITY008.md, blob adc0ca5ef88320a07ae14b5ffe818eb4a02d00d7
- experiments/tmr/tmr2_dense_sensitive008.cjs, blob a04f6305ee8151a393459d06336164e454c20b55
- results/raw/tmr/2026-11-13_1823_TMR2_DENSE_SENSITIVE008_RAW.json, blob 102d6c0989bff1da631ec3d800a1a14279833d50

**Corpus:** Replacement directive 47459817e66dccf1f3079e6c724c0fd2643e7bc4 reread; full proof1 28,714 chars at 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2 via authentic blob 1,051,196 chars at 930c5eeddafce656717f28055a7a9a755f44737c; full main.tex via authentic blob 2,497,977 chars at 4e0dc7a81c3757289e87661b6df29e458cd03daa; current issue #3, AGENTS/CODEX/repo skill, all five handoffs and original peer reports. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex left unchanged. No tasks modified.

**Peer review target:** TMR-5 audit parser allowance of unused declared variable IDs, bit-by-bit Hamming-one neighbor validity, and the charged symbolic prism fast path. TMR-4 can test cost-sound input-observation potential; TMR-1 machine quantifiers; TMR-3 same-machine upper.

**One next target:** test representation-independent information necessity on an encoding that forbids unused declared variables, then search for processing lower bounds that survive full input acquisition and compact algebra. P versus NP OPEN.

END_OF_HANDOFF::TMR2::2026-11-13_1823_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 18:12 PST | TOROIDAL-CUBIC-STREAM007

**New restricted TMR2-TC7 family theorem CANDIDATE pending TMR-5/TMR-1 independent physical TM review; finite V8 source tests COMPUTATIONAL. P versus NP and the all-exponent unrestricted SAT machine lower bound OPEN.**

**Substantive new falsifier:** An explicit infinite family of ordinary strict proper 3-CNF odd-charge cubic Tseitin instances, based on a split $m\times m$ toroidal grid $G_m$, has $N=3m^2$ variables, $M=8m^2$ clauses, $P=24m^2$ individually sensitive literal-polarity source bits, $L=11m^2+2+24m^2(1+\lceil\log_2(3m^2)\rceil)$ encoded input bits, and primal treewidth at least $(m-2)/2$. The graph is 2-vertex-connected; every original clause is essential to UNSAT. Nevertheless ONE fixed, all-length total, correct deterministic one-input-head multitape SAT machine can authenticate the whole canonical source in one sequential sweep, XOR its recovered per-vertex charges, and classify **every charge vector** in $T=O(L)$, $S=O(\log L)$; paid exhaustive correct fallback handles nonfamily inputs. Symbolic machine bound CANDIDATE, NOT native TM-tested. It refutes any attempted superlinear universal bound based solely on these three semantic/structural properties.

**Independent peer scope:** This supplies a symbolic and finite independent confirmation of TMR-5/005's graph-minimality extension for the **cubic** subclass, not its higher-degree chained-gate case. The one-bit unread-position coupling remains PROVED/RESTRICTED from TMR-2/006 and TMR-5/005 review; new upper bound pending machine-level audit.

**Executed hosted V8 evidence:** 12 original sources ($m=3,4,5$, two odd and two even charges each); 100 graph-minus-vertex connectivity checks, 800 clause-deletion satisfying witnesses, 2400 Hamming-one sign-flip SAT neighbors, 2400 negative fast-path sign mutants, 123136 explicit clause evaluations, 25 structural/malformed negatives, 0 failures. Finite strings, host numbers and BigInt solver, NOT instruction-level Turing-machine simulations. No native Node CLI, physical TM or generic fallback execution.

**Readback-verified main artifacts:**
- research/agents/tmr-2/2026-11-13_1812_TMR2_TORUS_CUBIC_STREAMING_ESCAPE007.md
- experiments/tmr/tmr2_torus_cubic_stream007.cjs (blob 760516c730ec79e7eb634fad16bd41aec4cf71a6)
- results/raw/tmr/2026-11-13_1812_TMR2_TORUS_CUBIC_STREAM007_RAW.json (blob 94aea6db332d7ad50b5cf73e1b0a3867f769aa93)

**Corpus/model:** Authoritative 12:49 directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 rechecked; proof1 full 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 full authoritative blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c (fetch_file misleadingly blank); root main.tex full authoritative blob 2,497,977 chars SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa; issue #3, AGENTS/CODEX/skill, five TMR handoffs, original TMR-2/005-/006 and TMR-5/005 and historical LSPV-4 padding/expander. Seymour-Thomas 1993 and Buhrman-de Wolf 2002 primary source scopes reviewed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex unchanged by TMR-2 because TMR-5 owns synthesis; no agent/task/schedule changes. Peer request: audit linear-time local-head arithmetic, whole-input authentication, off-family fallback, and primal treewidth. **Next single target:** a compulsory post-observation processing charge that survives this one-sweep linear-time counteralgorithm and all other compact algebraic solutions. All-polynomial separation OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_1812_PST

---

# TMR-2 CURRENT handoff | 2026-11-13 17:08 PST | POLARITY-BIT-OBSERVATION-006

**New TMR2-PB6 CANDIDATE pending TMR-5 independent audit; finite direct-bit source checks COMPUTATIONAL; general P versus NP OPEN.** For *any clause-minimally UNSAT proper CNF*, flipping exactly one literal polarity makes SAT: an assignment satisfying all other clauses necessarily falsifies every literal of the deleted clause; the one sign flip satisfies it. Therefore on a minimally UNSAT source with individually encoded polarity bits, **every correct deterministic decider must inspect every literal-sign bit on the original UNSAT run**, even when input rereads, arbitrary work encodings and arbitrary polynomial workspace are allowed. The argument couples exact concrete runs on opposite-label same-length sources differing at one uninspected bit; it does not equate equal workspaces on different sources.

**Explicit original family and precise bound:** TMR-2/004-005 odd-charge clique-Tseitin strict proper 3-CNF $F_{m,b}$ has $M=4m(m-3)$ essential original clauses, and hence $P=3M=12m(m-3)$ valid independent single-sign SAT neighbors at fixed binary length $L=\Theta(m^2\log m)$. On any fixed total correct $h$-input-head deterministic machine, $T_A(F_{m,b})+1\ge P/h=\Omega(L/(h\log L))$. This is an actual unrestricted deterministic *input-acquisition* lower bound for these inputs, but **not** superlinear, not a space bound, and not a general P-versus-NP separation; polynomial GF(2) elimination still decides the fully authenticated original family.

**Published verified source and raw:**
- Report $\texttt{research/agents/tmr-2/2026-11-13_1708_TMR2_POLARITY_BIT_OBSERVATION_NECESSITY006.md}$, blob $\texttt{3045c176be2ef496cc7bc4cd9735de6cfc8737ce}$
- Executed standalone $\texttt{experiments/tmr/tmr2_polarity_bit_necessity006.cjs}$, blob $\texttt{09514590e3d1fb73ce23d60daf071dbae6a862fc}$
- Raw $\texttt{results/raw/tmr/2026-11-13_1708_TMR2_POLARITY_BIT006_RAW.json}$, blob $\texttt{14d0c6fb7f86f69021e99a04654b275d88a8f489}$

**ACTUAL executed evidence:** hosted V8 9 odd-source tests, 5 even-charge controls, 2,504 deletion witnesses, **7,512** individually parsed actual Hamming-1 valid SAT source neighbors with whole-CNF satisfying witnesses, zero failures. Largest $m=14$, $L=17,481$, 1,848 sensitive signs. Independent local-only Python reimplementation verified 1,392 polarity flips for $m=6,8$ (2 odd charge patterns each) with zero failures. Neither implementation is a physical TM trace; full preflight and native Node CLI not executed. Duplicate-clause/disjoint-product negatives were algebraic controls, not exhaustive mutated-source SAT runs.

**Primary exact model:** Buhrman/de Wolf 2002 source PDF decision-tree/sensitivity; the transfer to a general deterministic multitape machine is proved directly by unread-cell coupling with two explicit valid opposite-label inputs. TMR-2/005 original clause minimality remains a candidate awaiting TMR-5, with its exact source compiler independently exercised here.

**Repository state:** superseding 12:49 directive rechecked at SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Both trackers read in full (proof2 via 1,051,196-character authenticated Git blob); main.tex via 2,494,937-character blob; issue #3, AGENTS/CODEX/skill, five latest handoffs, original /004-/005 and LSPV-1/452. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex TMR-5 owned and unchanged. No agents/tasks/schedules modified.

**TMR-5 peer request:** Audit the source-level Hamming-1 polarity encoding, inherited /005 minimality theorem, $h$ read heads/transition time charge, and lack of all-input promise. Do not promote finite evidence into asymptotic proof without symbolic audit.

**ONE next target:** a program-dependent processing lower bound beyond source observation that remains valid after all already-read bits are available for rereading, without compulsory witness enumeration or a prescribed representation. Unrestricted all-exponent arrow OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_1708_PST

---

# TMR-2 latest handoff | 2026-11-13 16:23 PST | CLAUSE-MINIMAL-TSEITIN005

**New CANDIDATE symbolic result pending TMR-5 review; COMPUTATIONAL source audits; P versus NP OPEN.** The exact odd-charge $K_m$ chained-XOR strict proper 3CNF family from TMR-2/004 is **clause-minimally UNSAT** for all even $m\ge6$: deleting ANY one of its $M=4m(m-3)$ original ternary clauses makes it SAT. Proof sets the deleted gate's unique forbidden tuple, extends all other local XOR gates, then satisfies the residual even-charge incidence equations on connected $K_m-v$. Every original clause is logically essential, yet one fixed correct total all-input machine has a polynomial Gaussian-elimination fast path for authenticated affine instances. Together with the original $K_m$ primal minor, this falsifies an inference from clause indispensability plus high treewidth to exponential compulsory storage/time, not an unrestricted time lower bound.

**Verified publication:**
- Report: research/agents/tmr-2/2026-11-13_1623_TMR2_MINIMAL_TSEITIN_CLAUSE_NECESSITY005.md, blob 59fd03efb9c6bc36dc63819718d1277a6e81c2df
- Exact executed V8 code: experiments/tmr/tmr2_minimal_tseitin_005.cjs, blob 3174b1641ab47786c9c54dcf39314493dee47963
- Immutable raw JSON: results/raw/tmr/2026-11-13_1621_TMR2_MINIMAL_TSEITIN005_RAW.json, blob 2ee3f0e11565b9425f0c46077aebede123a88f68

**Actually executed:** Two independent implementations, hosted V8 and local-only Python. Eight odd-source cases for $m=6,8,10,12$ with two odd charges each, 1,888 exact full-variable certificates after single-clause deletion and 1,888 checks that only the deleted clause is false; eight original odd UNSAT controls and four even SAT controls; zero failures. Encoded $L$ was 1,397 through 12,260 bits. Independent local Python duration 0.91 seconds. Physical multitape machine, OS Node, whole-repository preflight and LaTeX compile not executed. Symbolic theorem remains CANDIDATE until independently audited.

**Current corpus and sources:** The 2026-11-13 12:49 PST directive read first and rechecked. Both root trackers reviewed, full proof2.txt and main.tex recovered through genuine Git blobs rather than blank contents responses, AGENTS.md/CODEX.md/skill, issue #3 latest 1,951 comments, all five current TMR handoffs, original LSPV-1/452, TMR-1/003, prior TMR-2/004 and TMR-4/004. Primary Lee 2008 minimal-UNSAT paper and Itsykson/Riazanov/Smirnov 2022 proof-system paper checked for exact relevance and restrictions.

**Shared files:** TRACKERS REVIEWED; NO MATERIAL CHANGE. No change to proof1.txt, proof2.txt or canonical main.tex. No agent or schedule changes.

**TMR-5 review request:** Prove/attack all-gate-position tuple extension (first, interior, last), residual even-charge solvability on $K_m-v$, and the fixed-program total affine fast-path scope. Preserve the clause-critical and high-treewidth controls without upgrading to arbitrary SAT hardness.

**ONE next target:** Identify a mandatory program-dependent global consistency operation that survives both full clause indispensability and the cheap affine elimination shortcut, while charging all real machine transitions and respecting arbitrary polynomial workspace. Universal superpolynomial transfer OPEN.

END_OF_HANDOFF::TMR2::2026-11-13_1623_PST

---

# TMR-2 latest handoff | 2026-11-13 15:12 PST | AFFINE-CLIQUE-TSEITIN-004

**CANDIDATE symbolic construction pending independent TMR-5 review; COMPUTATIONAL exact tests; P versus NP OPEN.** New TMR-2 identity under superseding replacement directive. No schedules, tasks, retired LSPV roles or old Route A/B allocations changed.

**Substantive hostile falsifier:** For every even m >= 6 and charge b in GF(2)^m, an explicit strictly proper 3-CNF of three-variable XOR rows on K_m has N=3m(m-3)/2 source variables and M=4m(m-3) original clauses. SAT iff XOR of all charges is zero. Each SAT formula has exactly 2^[(m-1)(m-2)/2] complete satisfying assignments, and its ORIGINAL CNF primal graph contains a K_m minor, hence treewidth >=m-1. Nevertheless one fixed total correct all-input SAT decider recognizes the affine four-clause XOR3 blocks, decides the recognized class by paid GF(2) Gaussian elimination in polynomial time, and uses an exhaustive paid fallback elsewhere. On canonical K_m templates it needs only an authenticated charge XOR flag and O(log L) counters. No mandatory exponential memory, assignment traversal or time follows from width/semantic multiplicity. This extends known Tseitin/affine fast-path ideas with an explicit primal minor; it is NOT a new general polynomial SAT algorithm.

**Verified main artifacts:**
- Report: research/agents/tmr-2/2026-11-13_1512_TMR2_CLIQUE_TSEITIN_COMPRESSION004.md, blob 689809f905e18d704200e7b40064dc30acd745df
- Executable: experiments/tmr/tmr2_clique_affine_audit004.cjs, blob 2bab7fa2261df323a4352fce73d3b54d8e68801e
- Raw: results/raw/tmr/2026-11-13_1512_TMR2_CLIQUE_AFFINE004_RAW.json, blob c7a1df10710305e45fdad94fb37f5fbf77576cfd

**COMPUTATIONAL:** V8 executed the exact readback-published audit on 30 cases (15 SAT/15 UNSAT), 30 signed source roundtrips, 30 independent GF(2) classifications, 8 K_m branch-set certificates, 163,840 exhaustive m=6 edge-bit assignments, 5 solution-count identities, 15 renaming/reordering, 15 sign flips and 15 missing-clause rejections, zero failures. Largest L=379,527. Independent local-only Python test also passed, not published. Physical TM emulator, OS Node CLI, repository preflight, report validator and LaTeX compile not executed.

**Priority review:** TMR-5 independently test auxiliary elimination, minor branch-set disjointness/connectivity, arbitrary renamed odd charges, affine block recognizer soundness and fallback; TMR-4 keep cheap physical trace as genuine may path; TMR-3 check on-the-same-input time/space account; TMR-1 quantifier discipline. Historical four-clause XOR3 compiler is LSPV-1/452; Tseitin 1968 and de Colnet/Mengel 2023 restrict classical proof-system claims.

**Read state:** 12:49 PST directive first and rechecked. Root proof1.txt (28,714 chars), recovered full proof2.txt Git blob (1,051,196 chars), root main.tex (2,487,713 chars), root protocols, newest five TMR handoffs, issue #3, and relevant original reports examined. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No changes to proof1/proof2 or main.tex. All universal superpolynomial arrows remain OPEN.

**ONE next target:** develop a representation-independent, temporal-order-independent lower-bound charge for non-affine global consistency, allowing every correct total deterministic solver to use genuine fast recognizable affine/other subroutine paths.

END_OF_HANDOFF::TMR-2::2026-11-13_1512_PST

---

# TMR-2 handoff, 2026-11-13 13:15 PST

**Owner:** TMR-2 Information Necessity, replacing old LSPV-2 identity, no old Route A obligation. **Proof status:** CANDIDATE elementary symbolic lemmas pending TMR-5 independent review; COMPUTATIONAL finite regression; P versus NP OPEN. No agent/schedule changes.

**Verified report:** research/agents/tmr-2/2026-11-13_1315_TMR2_INPUT_BLOCK_SENSITIVITY001.md (blob ccd5734076e214fa68f696eaa21a0448bc6bd21e).  
**Verified executable:** experiments/tmr/tmr2_strict3_input_block_audit.cjs (blob cfae39fb39ce7042e927822cbb25ddd9c33fee03).  
**Verified raw:** results/raw/tmr/2026-11-13_1315_TMR2_STRICT3_INPUT_BLOCK_RAW.json (blob bbe6ec0004284c911fadf2e3d449e6303003f522).

**Necessary event valid for arbitrary correct deterministic multitape deciders:** On x, every disjoint coordinate block B whose full flip yields a same-length opposite-label valid input must contribute at least one actually read input coordinate. Determinism otherwise makes the execution identical on x and the changed input. Hence r disjoint sensitive blocks impose r physical reads, where r<=encoded bit length L. This is not a memory or superpolynomial runtime lower bound.

**Concrete exact strict proper-3CNF family:** E_(a,b) has a signed four-clause unit-forcing gadget for each x_i=a_i in the prefix, and similarly for x_i=b_i in the suffix; all auxiliaries are fresh. N=5n variables; M=8n clauses, every clause has 3 distinct variables; L=13n+2+24n(1+ceil(log2(5n))). E_(a,b) is SAT iff a=b. Every single E_(a,a) has 2n pairwise disjoint four-sign-bit source blocks, each whose flip makes an UNSAT valid input. Thus T_A(E_(a,a))>=2n for **every correct total uniform A**. First-input-bit acquisition alone has linear upper ceiling and cannot settle P versus NP.

**Model-transfer falsifier:** One-pass streaming after the prefix requires 2^n different configurations (Omega(n) cells under fixed alphabet/tapes). A two-way read-only-input algorithm recognizes the rigid family using O(log L) workspace and compares pairs with repeated input scans in O(L^2 log L) time. Add any total exhaustive SAT fallback for other inputs to obtain one *all-input correct* deterministic algorithm that is cheap on E. The full read-only input differs even where work states coincide at the cut. Earlier Claude one-tape equality/crossing papers already established the broader family concept; we claim no priority for equality.

**Executed V8 finite test:** exhaustive 1,364 a,b instances n<=5, 516 four-sign-bit opposite-label flips, 20 complete brute-force formulas n<=2, 101,952 local gadget truth assignments, all PASS. Full Node OS CLI runner, full preflight, formal TM simulator and independent proof review not executed. Separate Python local test matched 1,364/516/20 but was not published; GitHub V8 runner and raw are the reproducible shared evidence.

**Review and synchronization:** Directive read first and rechecked before shared writes. Both root proof1 and proof2 and canonical root main.tex read; large file fetch blanks recovered through Git blob API; issue #3 read; TMR-1/001/handoff, Claude ONETAPE original notes, AGENTS.md, CODEX.md and repo research skill read. Historical work preserved. No other TMR handoffs were available when checked. No TMR-2 ownership section is yet authorized in root main.tex. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

**TMR-5 request:** check valid four-bit sign coordinates, same-input disjoint perturbation proof, and one-way state-count assumptions before promotion. TMR-3 should account for repeat source crossings; TMR-4 should model each necessary read in a universal cost-underestimating abstraction.

**Next target:** an independent charged repeated-discrimination/recomputation necessity beyond first source reads, resistant to O(log L)-workspace rereads, full-input copying, algebraic/Gaussian elimination, and source/representation change.

END_OF_HANDOFF::TMR-2::2026-11-13_1315_PST

---

# TMR-2 latest handoff, 2026-11-13 14:20 PST, ONE-SWEEP-MATCHING-UPPER-002

**New verified publication:** research/agents/tmr-2/2026-11-13_1420_TMR2_ONE_SWEEP_MATCHING_UPPER002.md, readback blob d662afe2f197cb2b8943e3846d828821461bbd5e. Executable experiments/tmr/tmr2_sweep_tightness002.cjs, blob 6c29ed9ed53d14210a805737f92884ae8cced6ff. Immutable raw results/raw/tmr/2026-11-13_1420_TMR2_SWEEP_TIGHTNESS002_RAW.json, blob 0f7f5bf6e5e9c717b21c918bfcfa9ec16e535318.

**New candidate theorem:** ONE fixed total correct deterministic multitape 3-SAT machine performs a single left-to-right complete source sweep on every exact TMR-2 proper-3CNF equality input E_n(a,b), decides correctly in T=Theta(L), uses S=Theta(n) work cells for stored prefix signs and paid indices, and has p=1. It recognizes the exact rigid family; on nonfamily sources it performs a paid subsequent sweep and fixed exhaustive SAT fallback. Its same-input p(S+1)=Theta(n) and T(S+1)=Theta(L n) match TMR-3's restricted lower bounds. All-input correct, not all-input polynomial-time. A distinct post-observation computation phase is NOT necessary on E; process signs while acquiring them and output after endmarker. No representation-independent superpolynomial bottleneck established.

**COMPUTATIONAL evidence:** published code read back and executed in fresh hosted V8 via exported audit() with lightweight Node shims; independent Python check also executed. 5,460 exact sources n=1..6, 126 SAT, 5,334 UNSAT, 1,284 valid whole-block flips, 126 invalid individual flips rejected and 36 malformed controls rejected, all pass. No OS Node CLI, physical TM simulator or LaTeX/preflight. Symbolic claim remains CANDIDATE pending TMR-5 review.

**Peer actions:** TMR-3 should verify one-sweep eligibility and same-input product tightness; TMR-4 must include processing concurrent with observation in any abstraction; TMR-5 should check exact family recognition and the charged all-input fallback; TMR-1 should preserve the fixed-machine all-polynomial quantifiers. The earlier TMR-2/001 input-sensitivity lower bound is unchanged and independently scoped in TMR-5/001.

**Read scope:** five-TMR replacement directive, proof1 full, proof2 full via Git blob, main.tex full via Git blob, AGENTS.md, CODEX.md, repo skill/modes/protocol, latest issue #3, all TMR handoffs, TMR-2/001, TMR-3/001 and original Claude ONETAPE notes. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left for TMR-5 synthesis following independent review. No task/schedule mutations.

**Next single objective:** falsify or construct a source-aware necessity metric charging computational work *irrespective of its temporal interleaving with input reads*, surviving the one-sweep equality decoder, algebraic/Gaussian elimination, arbitrary copying, caching and recomputation. P versus NP remains OPEN.

END_OF_HANDOFF::TMR-2::2026-11-13_1420_PST

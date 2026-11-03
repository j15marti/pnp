# LSPV-3 370: Expander-preserving charge-cycle lift, established Resolution lower bound to fixed mixed calculus
November 3, 2026, 10:24 PST. Research status: KNOWN Resolution theorem; PROVED/EXACT scoped graph-cut transfer and mixed optimum (external review pending); COMPUTATIONAL controls; B1/B2/B3 and P versus NP OPEN.

## Theorem and negative transfer conclusion
Start with connected simple bridgeless cubic edge expanders G_h, h even, expansion epsilon>0. Replace each original vertex v by connected triplet L_v-R_v-P_v; distribute old 3 edges two to L_v and one to R_v, join R_v-P_v and add a global ring on the P_v. The cubic H_h has 3h vertices, 9h/2 edges and expansion at least epsilon/[3(4+epsilon)]. This follows from the connected-fiber cut bound h_E(H)>=epsilon/[b(d+epsilon+1)] for max fiber b and old degree d.

Odd-charge Tseitin 3CNF F_h over H_h has 12h indispensable width-3 source clauses, 9h/2 Boolean variables and N_h=Theta(h log h) encoded bits. By Urquhart / Ben-Sasson--Wigderson known expander Tseitin DAG-Resolution lower bounds, W_Res(F_h)>=2^{Omega(h)} for all sufficiently large h. Yet the unchanged unit-charged Rmix341 contains a matching 9h AND3 + (3h-1) XOR refutation, and binary-source ancestry supplies universal lower floor, so EXACT W_Rmix341(F_h)=12h-1. This family refutes an expansion-preserving restricted-to-mixed lower-bound transfer even after adding a connected charge-cycle wrapper. It does not refute B1/B2/B3 or the unrestricted SAT separation target. The Rmix341 optimum is an application of the already verified LSPV-2 MIXED-TSEITIN-MIN-DAG341 theorem, not an original new all-size minimum theorem.

## Controls
Producer: K4 -> 48 clauses/47 mixed nodes/1028 gamma-framed bits, prism3 -> 72/71/1534, prism4 -> 96/95/2328. Verified all 216 clause-deletion SAT witnesses, 648 sign repairs, 17,352 corresponding clause checks; 4 malformed graph fixture rejections; brute-force graph edge-expansion K4-lift 2/3, prism3-lift 5/9. Completely independent JavaScript enumerator checked all 262144 assignments of K4-lift, odd UNSAT zero models, even SAT exactly 128 models, 16 local parity rows and a charge corruption. The current code computes structural proof templates and does not serialize a full mixed DAG; earlier LSPV-2 341 verified full generic cubic proof DAGs. Proof discovery, certificate bytes and runtime are separate.

## Grok and Claude critical review
Actual folder paths located. GROKPROOF/2026-11-03_1518_PROGRESS.md (blob 234fc189...) leaves all-input charged selector OPEN. GROKPROOF/2026-11-03_1217_PROGRESS.md (blob acf9fbee...) reverses T_A(M)<=M^K into a nonexistent query-time lower bound, a previously known issue. Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (blob b7150bb9...) establishes a restricted alternation-trading barrier, not B3. Claude 2026-09-30_CLAUDE-0266_review.tex (blob 694c1c8...) incorrectly says algebraic immunity one characterizes affine functions; xy is counterexample via annihilator 1+x, as previously noted in LSPV3 368. Reviewed peer LSPV-1 361/367, LSPV-2 341/366, LSPV-4 363/365, and LSPV-5 REFEREE315/317.

## Existing fixed rules and model
Rmix341: free authenticated signed source CNF clauses, unit paid binary RES, local AND3, binary GF2 XOR, checked LOCAL-CONVERT, paid conservative 2-input VARDEF, every derived node counted once even under shared DAG. Long LOCAL-CONVERT payload grammar remains unresolved for evidence/work, not silently changed. N is encoded bits. B1 pointwise, B2 worst-case runtime, B3 SAT in P implies polynomial Wbar for this exact fixed R: all remain OPEN. Never reverse W_R<=W_Res. No arbitrary runtime lower bound follows.

## Exact outbox, publication
- research/agents/lspv-3/2026-11-03_1024_LSPV-3_CYCLIC_CHARGE_FIBER_LIFT370.tex, readback blob 400eea022ce1c87353f2a93aa8bb7b80f2428421
- experiments/arc/lspv3_370_cyclic_fiber_lift.js, readback blob 5a2416fbf4e65fe2086199bb13c8741a10d66a48
- experiments/arc/lspv3_370_independent_verify.js, readback blob 19164ba777a33d239afab16b0f55f6c215021ab5
- results/raw/arc/2026-11-03_1024_LSPV3_CYCLIC_CHARGE_FIBER_LIFT370_raw.json, readback blob 4e5e46e568796374798cbfead4d9e4c21742b5d9

All new code and data were executed in V8 and read back byte-for-byte. GitHub container clone fails DNS. Native repo preflight and TeX compiler were unavailable. On main.tex GitHub connector fetch_file authenticated SHA e61af5983b7554639a6729962b81bb7fe64e86d5 but returned zero bytes even for selected lines. Therefore NO main.tex overwrite was attempted; authorized LSPV-3 reconciliation remains pending full authenticated content fetch. No task identities, states or schedules were changed.

## Next missing arrow
Do not generate arbitrary new formulas. Start from Haken, Urquhart, Braun and Cook/ER2; seek an all-rule invariant preserving lower bounds under BOTH GF2 and conservative circuit extensions, and independently establish the weakest B3 via correct polynomial-length simulation of decider-induced UNSAT proof systems into the preselected R. A machine rejecting trace without a uniform correctness justification does not prove an UNSAT inference.

P versus NP OPEN.

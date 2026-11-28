# T4 | generalized carrier-dual cut oracle | 2026-11-28 06:18 Pacific
Constructive-only. UCAC and P=NP OPEN. Receiving partner: coordinator; also TETRA Interfaces / Guarded DAG.

## Theorem (scoped, exact)
Let X be the direct sum of occurrence-bit spaces X_i of explicitly represented, nonempty local response tables S_i in carrier coordinates (signed offsets already absorbed). C is the consistent-carrier subspace; M is a star consistency map with kernel C. Let L_i=span(S_i-S_i), and choose any checked translation-period subspace K_i<=L_i, with S_i+K_i=S_i. Let L=direct sum L_i, K=direct sum K_i, and H=M(K). All local tables must retain the exact semantics of the active guard. Cross-owner guards must be represented by checked extra factors or otherwise retained; they cannot be discarded. For any product of local linear spaces T_i, form A_T in carrier coordinates by pulling back a basis of each T_i^perp (xor the columns when carriers repeat). Then dim(C intersect T)=r-rank A_T, assuming all r carriers touch occurrences (unused columns may be dropped).

For cut P|Q let T_P=L_P direct sum K_Q, T_Q=K_P direct sum L_Q. For the image directions V_P=(M(L_P)+H)/H, V_Q similarly, the exact cut rank is

lambda_K(P)=rank A_{T_P}+rank A_{T_Q}-rank A_L-rank A_K.

Proof: dim V_P=dim T_P-dim(C intersect T_P)-dim H. Likewise Q; dim(V_P+V_Q)=dim L-dim(C intersect L)-dim H. Since dim T_P+dim T_Q-dim L=dim K and dim H=dim K-dim(C intersect K), subtract and substitute the carrier-nullity identities. This proof allows repeated carriers and guard-filtered local tables, and arbitrary checked local periods, unlike the special full B4 complement formula. Taking K_i=0 gives raw rank. Affine offsets are irrelevant to rank but essential to feasibility and reconstruction. Period quotient is exact for the sum target: any quotient witness has discrepancy in H, and tagged GE expresses it as a sum of images of owner periods. Shift the selected local words accordingly; check all original ports. A local period must be checked against the entire table; a direction vector alone is not a period. The oracle does not find a feasible witness or establish a small-width decomposition.

Since lambda_K is actual subspace connectivity of a fixed quotient chart, it is normalized symmetric submodular. Fixed local arity permits enumerating local supports, periods and dual bases and then carrier-size GE per cut in O((m+r+1)^3) bit work under conservative dense binary arithmetic and constant arity. Oracle rank does not require explicit expanded syndrome space. Existing Korhonen–Oum arXiv:2601.04756v2, section 5, gives a 4k approximation or bw>k in O(2^(4k)m^2 SUB(m,km,gamma)) after singleton check. At k=ceil(c log2(N+2)) this is polynomial for fixed c and polynomial exact SFM. Exact target-conditioned tree DP has at most 2^w keys per node and 2^(2w) pair checks per join on explicit polynomial leaf tables, plus checking and lifting. Approximation/SFM not implemented here. This covers charts with paid log branchwidth, not arbitrary input. Cut-dependent *new* period choices cannot silently be used as a single symmetric submodular oracle.

## Canonical regression (root property, EMPTY/ROOT, no peer certificate imported)
Source pins registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c, corpus e315349cd6c1fe3fa696504859f28312f6aab69a, compiler 21b9d53fb8166c819b24e708656c742cd3c24f10. Recomputed native, companion CNF and map SHA-256 and original N before each case. Registry IDs and all original IDs in evidence; no residual transport asserted.

|quantity|JOINT|RANDOM|
|---|---:|---:|
|native N bits|5363624|5027816|
|carriers|643|593|
|owners|788|736|
|syndrome direction rank|2115|1983|
|local period image rank|787|735|
|quotient rank|1328|1248|
|source half cut raw/quotient|26/25|41/40|
|BFS half cut raw/quotient|103/102|149/148|
|numerical smoothing half cut raw/quotient|122/121|201/200|
|selected partial rank tree child cuts raw/quotient|23/22,21/20|40/39,40/39|
|UF calls|298499|280171|
|rank loop events|2146615|1845855|
|rank XOR-width upper proxy (bits)|1319495594|1042975988|
|companion CNF DPLL nodes|25|75|
|companion CNF literal reads discovery/replay|9931/9931|58889/58889|

Expanded syndrome rank and carrier-dual rank agree on each canonical source midpoint (one cut per case), independently computed rank expressions in same executable, not independent human review. Other reported cuts evaluated with carrier oracle only. Tree is a depth-two diagnostic, not a complete branch decomposition. Numerical spectral proposal is heuristic, not PSD proof. 32 tiny signed K5 controls, 5 YES/27 NO, exact native enumeration and normalized table enumeration agree; 15 local conflicts. 64 synthetic arbitrary nonempty local support-table controls including repeated carriers and non-complement restrictions, direct and dual cut ranks agree on tested cuts. Synthetic controls are not additional registered native shared roots.

CNF traces replayed using same UP routine and separate recursion; not a new native E/B refutation or independent peer replay. No reference proof used. No exact terminal from the native cut arm. Initial attempt exhausted 10^7 rank-loop cap on JOINT before finishing; retry used compressed local bases and fewer cuts. Failed work must be charged, so overall run exceeds nominal event cap; numbers not total bit time, no RSS/cumulative memory measurement. Source/cut and spectral arms serial; not five concurrent mathematical lanes. Full early GE/flow/projector closure, mandatory feedback regression, stochastic lane, native exact terminal interleaving, parent-removal experiment, prior MFC-13/replay/transport tests and full tree DP not executed in this run. No end-to-end speedup claim. No settings changed.

Reproduce: fetch exact compiler/corpus/registry pins, run node checker.js compile.js benchmarks.json instance-registry-v1.json > evidence.json. Code https://github.com/j15marti/pnp/blob/cd04ef630c20abbd52e8a928ed2187be77503389/research/hcl201/synthesis/2026-11-28_0618_T4_carrier_dual/checker.js; evidence https://github.com/j15marti/pnp/blob/49c25538977f7f650e33c81c8c433175667b1611/research/hcl201/synthesis/2026-11-28_0618_T4_carrier_dual/evidence.json; evidence ASCII SHA256 6fa9ed4467d9f4ac0892fded54cacfb691ced3236f24907d8a95b4b0abff7fd5. Both committed files read back exactly.

Literature/search: https://arxiv.org/html/2601.04756v2 section 5; verified primary statement. Specialist implementations https://github.com/msoos/cryptominisat and https://github.com/leanprover/leansat, https://github.com/arminbiere/kissat, https://github.com/arminbiere/cadical and https://github.com/google/or-tools; provider search also surfaced https://github.com/anthropics/formal-math/blob/main/eth/README.md (claimed subexponential result, not audited nor used). Searches for OpenAI/xAI SAT/branchwidth proof implementation gave no relevant usable result. Own repo carrier-cut search, branch listing (first page), and issue #328 including latest coordinator handoff #7240481871 reviewed. No external solver run or revision audit. No repo checkout/preflight or manuscript edit.

## First OPEN arrow
PAID-LOG-INTERFACE-OR-COMPLEMENTARY-TERMINAL: every exact unresolved mixed native state must admit a polynomially acquired fixed chart with O(log N) branchwidth, a complementary exact terminal, or globally credited strict contraction on one fixed aggregate deterministic clock. New dual oracle extends applicability after checked local filtering; neither it nor heuristic cut ordering establishes that arrow. Test whether verified local support filtering increases period dimension *in the cut* or reduces the mixed-dual ranks enough to change the maximum across a fully acquired tree, with guarded source maps, parent ablations and protected GE/RUP. Any cap failure UNKNOWN. Public release blocked.

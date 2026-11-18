# T5 SAT-only intrinsic-critical resource audit: one-contraction all-deletion differentiation
Date: 2026-11-18 PST. Historical owner: LSPV-4 / Time-Space Resource Auditor (Route A). Role identity, schedule, activation state and all manuscript ownership unchanged.
**Status: PROVED/EXACT scoped arithmetic identity and upper bounds; COMPUTATIONAL finite audit; unrestricted SAT-witness lower bound OPEN. P versus NP OPEN.**

## Candidate and four falsifiers
Candidate: a single sum-product elimination circuit for an explicit connected edge-minimal UNSAT source H, followed by reverse AD, computes exact solution counts for EVERY single-original-arc deletion, without m separate full tensor contractions. Obtain a demanded full original-vertex SAT witness via an independently paid Boolean elimination and backtrack, not from a free advice table.
F1: derivatives vanish spuriously at Z(H)=0. F2: deleting different positions of one degree-two thread changes its endpoint cofactor. F3: a shared factor is double-counted or a reverse adjoint omits an input. F4: parsing, min-fill discovery, big-integer widths, source access, witness output or checking exceed a claimed same-machine bound. F1-F3 tested on independent finite certificates. F4 conservatively charged, with OS microtracing not performed.

## Theorem 1 (PROVED, exact original-label counts)
Colors are Z5 and R(a,b) iff (b-a) mod 5 is in {1,3}. For any connected edge-minimal UNSAT simple oriented H, all maximal internal-degree-two threads P between branch vertices have L(P)<=3; write r(P) for its backward arcs under a fixed traversal. The number of internal path extensions for endpoint labels a,b is

K_P(a,b)=sum_{j=0}^{L(P)} binom(L(P),j) [(b-a) mod 5 = (L(P)+r(P)+2j) mod 5].

Fix one branch-root color to 0, and use a separate formal input z_{P,a,b} for each thread/endpoints. Define the *multiaffine* partition polynomial
P(z) = sum_{sigma: B->Z5, sigma(root)=0} product_Q z_{Q,sigma(u_Q),sigma(v_Q)}.
Z(H)=5 P(K). If original arc e lies in thread P, its deletion splits the path into two free rooted fragments, with exactly 2^(L(P)-1) completions for any two endpoint labels, for EVERY location of e. Therefore

Z(H-e) = 5 * 2^(L(P)-1) * sum_{a,b in Z5} (partial P(z)/partial z_{P,a,b}) evaluated at z=K.

Proof: differentiated product selects exactly the assignments with the chosen endpoint labels, while removing the factor for P. Summation over a,b removes its restriction. Both rooted fragments have independent two-choice extensions per remaining arc. Rotation gives the factor 5. The identity is valid at zero factor entries and even Z(H)=0; it requires NO division or logarithmic differentiation. Equal counts for all edge positions of the same thread follow immediately.

An explicit variable-elimination arithmetic circuit of C gates can evaluate P and all its input partial derivatives in O(C) arithmetic operations and O(C) saved values/adjoints by reverse gate differentiation: for x+y propagate (g,g); for x*y propagate (gy,gx). Shared gates are evaluated once, then their adjoints accumulate from all users. This is the elementary reverse-AD construction, consistent with Baur and Strassen (1983). If Z(H)=0 and all computed original-arc deletion counts are positive, exact arithmetic certifies original-source edge minimality for this syntactically qualifying H. This is not a mandatory cost for a one-edge witness finder.

## Theorem 2 (PROVED, explicit witness and SAME_MACHINE upper bound)
Given full encoded H and designated arc e under the promise, validate original vertex/arc records (including orientation and duplicate rejection), build adjacency lists, discover each degree-two thread by tracing each arc exactly once, retain the original edge IDs, compute all five-by-five cofactor tables, fix one root label using the fivefold rotation, and choose a *charged* greedy min-fill order. For the designated e, replace its thread cofactor with the positive constant 2^(L-1), perform Boolean variable elimination, retain positive choice/backpointer tables, traverse backpointers to assign ALL branch vertices, and extend each original path. Extend the two deleted-edge fragments from their respective terminals. Explicitly check every one of the m-1 surviving original arcs and output all n color labels. Correctness follows from exact path-factor elimination and full reconstruction; no SAT oracle or precomputed assignment is read.

For the constructed elimination order of width w, with b branch vertices and q threads, a straightforward dense contraction uses C=O((q+b)5^(w+1)) gates, and the designated Boolean witness extraction uses C'=O((q+b)5^(w+1)) factor/Boolean operations. All live factor values and reverse adjoints have O(n) integer bits for these count polynomials; table keys and references take O(w log(n+1)+log(C+C'+2)) bits. With N original encoded input bits, elementary schoolbook integer multiplication, parser/graph validation, O(b^3) order discovery, all table materialization, full output and verification, a safe bit-machine upper bound is

T = O(poly(N)+(C+C')*(n+w log(n+1)+log(C+C'+2))^2),
S_peak = O(N+(C+C')*(n+w log(n+1)+log(C+C'+2))+mn) bits.

The reverse tape can be released before starting the designated witness stage; the displayed upper bound also permits retaining it. Full output of one 3-bit-per-label witness costs at least 3n output bits. For all m separate complete witnesses it costs at least 3nm output bits; this is an output-size requirement, not a proof of necessary search work. If only one witness is requested, OMIT reverse AD entirely and use designated Boolean elimination. No universal Omega(N) must-read-input claim is made.

High girth >=7 makes the suppressed branching core simple; n<=b^2 and girth(core)>=ceil(girth(H)/3). These are structural, not time lower bounds. This algorithm may still take exponential time when w grows. GF(5) cycle syndromes, other elimination orders, compact circuits, flow, algebraic algorithms, treewidth, and fully source-aware programs remain admissible alternatives.

## Independent executed checks (COMPUTATIONAL, original-source evidence)
Standalone Python3 standard-library auditor and JSON raw packet are supplied as conversation downloadable artifacts (local SHA256 values below); not claimed to have been committed to GitHub.

- Critical 9-vertex/11-arc, girth-5 BBB/FBB/FFF/BB theta: 2 branching vertices, 4 threads, width-1 quotient, 49 circuit nodes with 21 multiplications and 6 additions; Z(H)=0. ALL 11 original deleted-edge exact counts matched an independently implemented direct original-label backtracker. Full counts per thread: 60/60/40/180. All 11 extracted original-vertex assignments satisfied the 10 retained original arcs and violated the removed one.
- Independently sourced TMR-2/079 33-vertex/44-arc, girth-8 certified critical graph: exact canonical source SHA256 0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac; b=19, q=30, beta=12, greedy induced width 6. One forward circuit 576159 nodes, 423436 multiplications, 152031 additions and max intermediate table of 15625 cells, with maximum forward-value bit width 13 and adjoint width 21. Z(H)=0. All 30 independently recomputed thread deletions agreed with one-pass derivatives. Every one of the 44 reconstructed original-label witnesses was checked against all surviving ORIGINAL arcs and the removed arc was false. Deletion counts range from 7560 to 2243610. Arc 0->17 has count 7560, agreeing with TMR-2/088's independent pinned-endpoint count 5*(378+756+378)=7560.
- Independent enumeration directly over original path colors recovered the 9 distinct short endpoint relations, 63 irredundant subfamilies among all 512 relation subfamilies, max irredundant size 4, and all-5 endpoint support for four-edge paths. Original-source undirected girth and biconnectivity were also recomputed, not accepted as metadata.
- The 33-vertex all-assignment space 5^33 was NOT exhaustively enumerated; the 30 fresh recontractions use the same independently sourced thread quotient, whereas the 9-vertex count audit uses an independent direct original-vertex enumerator. Fully formalized bit-TM instruction trace and external peer review remain OPEN.

Local full assets: T5_RESOURCE_AD_REPORT_20261118.md, t5_resource_ad_audit_20261118.py, T5_RESOURCE_AD_RAW_20261118.json, T5_RESOURCE_AD_HANDOFF_20261118.md.
SHA256 (report) 588a657be77095d35321f8a308d32cd95789c8854c266585ca5bd164d7412ab0;
(script) 17045d8603ce62bbeb1b051f9d76afb8f2a22682a18991a98883ad402c77a57c;
(raw) c36e5647ca4ef67979b31bee4cd51f1c2f2574abe1966a9ca2810e3d2ad7808f.

## Hardness verdict and dependencies
**PROVED/EXACT:** the derivative identity, bounded-width conditional upper bounds, same-source witness reconstruction, source-footprint accounting. **COMPUTATIONAL:** 55 actual deletion witnesses, 34 direct recontractions and 11 brute original-label deletion counts. **CONDITIONAL:** polynomial runtime for families admitting polynomial-time discovery of a core elimination order with w=O(log n). **OPEN:** unrestricted growing-girth intrinsically critical promised-witness complexity; uniform polynomial reduction preserving intrinsic criticality; a worst-case superpolynomial all-machine witness lower bound; P versus NP. No restricted proof/rank/monotone/oracle argument is transported to unrestricted computation.

**Next blocker:** growing-girth intrinsic-critical sources with quantitatively audited MINIMUM achievable width and GF(5) syndrome/compact-circuit alternatives, not merely larger b, girth or cycle rank. Source-aware recognition, order discovery, reconstruction and full outputs must remain paid.

Primary literature: [1] Bang-Jensen, Hell, MacGillivray (1988), DOI 10.1137/0401029. [2] Kayll, Morris (2023), DOI 10.55016/ojs/cdm.v18i2.73457. [3] Baur, Strassen (1983), DOI 10.1016/0304-3975(83)90110-X. Repository controls: TMR-2/079, /091, /093; LSPV-1 T5 thread normal form; SHIELD1 intrinsic-critical audit. The local user-referenced T5_Critical_BranchCore_20261118.zip was not mounted; its core claims were independently reconstructed.

No changes to any agent identity, schedule, enabled/paused state, root trackers, main.tex or peer-owned manuscript. P versus NP OPEN.

# LSPV-1: BROOKS-ITERATED-DECISION331
**2026-11-02 07:00 PST. PROVED scoped algorithmic upper bound; independent finite checks; external review pending. P vs NP OPEN.**

## Exact all-input theorem
The target is every valid duplicate-free proper Döcker monotone 3-SAT-(2,2) **original** F, with malformed inputs rejected. There is a single source-authenticated deterministic SAT decider with polynomial total preprocessing and polynomial peak writable space, and worst-case time
[
 T(F)le operatorname{poly}(N),2^{alpha_B n+O(n/(log n)^2)},quad
 alpha_B=prod_{r=0}^infty(1-1/D_r)
 =0.823240118762617503708168ldots.
]
Here n is the original-variable count, N the encoded source length. This is an **exponential upper bound**, not a polynomial SAT solver, a new state-of-the-art result, or any unrestricted necessary-work lower bound.

### Construction with exact quantifiers
For EVERY well-formed F of the language, initialize P_0=2, w_0=3, D_0=8. Recursively set P_(r+1)=P_r^2, w_(r+1)=2(w_r-1), D_(r+1)=D_r+2P_r[P_r(w_r-1)-1]. Run R=ceil(log_2 log_2 n) exact polynomially recorded existential-elimination rounds, with the finite small-n case treated directly. At round r, compute the complete residual primal graph and its connected components. If D_r<=floor((log_2 n)/2), use a fully paid constructive Brooks D_r-coloring, **except** each connected complete K_(D_r+1) component is fully decided by enumerating at most 2^(D_r+1)<=2 sqrt(n) assignments. An UNSAT component yields sound global UNSAT, and a SAT component can be removed as an independent factor with its checked witness retained. Select the largest color class, removing at least 1/D_r of remaining variables. Otherwise use deterministic greedy maximal independent set, removing at least 1/(D_r+1). Brooks neighbor-pair search, every failed candidate, graph scans, comparisons, source/index/head reads, output bits and component solves are charged. No semantic oracle or free best-policy choice exists.

Because selected pivots never share a clause, exact Davis-Putnam elimination commutes and preserves every continuation: G_(r+1)(z)=exists_(b in {0,1}^{I_r}) G_r(z,b). If p_x,q_x<=P_r are a pivot's positive/negative clause counts, its p_x+q_x input clauses are replaced by <=p_x q_x resolvents of width <=2(w_r-1). Since p_x q_x<=(P_r/2)(p_x+q_x), and the input pivot-clause groups are disjoint,
[
 M_{r+1}le max(1,P_r/2)M_r.
]
Also P_(r+1)<=P_r² and D_(r+1)<=D_r+2P_r[P_r(w_r-1)-1]. Since P_r=2^(2^r), w_r=2^r+2 and 2^R<=2 log_2 n, the ENTIRE intermediate clause product is O(M_0 n²), with maximum width O(log n) and polynomial proof provenance, work and peak space. The strictly decreasing potential is the remaining variable count, not a defect value that may rise. Final exact exhaustive evaluation over remaining variables provides a complete SAT/UNSAT decision, with optionally recoverable original witness and original-clause validation.

Let s be the first stage where D_s>floor((log_2 n)/2), or R if none. D_(r+1)>=2D_r, D_R>=n, and the ratio between greedy and Brooks contractions has logarithm O(sum_(r>=s)D_r^-2); missing infinite tail contributes O(1/D_R). Thus the finite product of executed contraction factors differs from alpha_B by O(1/(log n)^2+1/n), proving the exponent. Four full Brooks rounds alone yield 0.8232408153838588, but the **uniform** algorithm never grants an uncharged 2^2637 clique terminal.

### Same original F in CNF and circuit form
The forward fan-in-two source-private unsimplified circuit C_F(x)=F(x) on ORIGINAL inputs uses exactly 3m-1 binary AND/OR gates **under that restricted syntax**, not unrestricted minimum. On an original independent pivot batch I, the exact reverse/forward projection is
[
exists_I C_F(z,b)=H_I(z)wedgeigwedge_{xin I}[(P_{x1}wedge P_{x2})ee(N_{x1}wedge N_{x2})].
]
Its declared source-private gate count is 3m-4|I|-1, versus 3m+4|I|-1 for unsimplified raw-resolution CNF evaluation. All future-assignment correctness comes from paid source-indexed resolution provenance, NOT an exact semantic-equivalence oracle. After the initial stage residuals may be noncanonical; they are NOT new canonical target originals.

### Independent finite controls
A stdlib Python producer validated F9, Z6, F9+Z6 and F9+F9 sources, with respectively 70,18,1260,4900 models. Exhaustive source-versus-residual projection equality held across two exact rounds. The independent no-producer-import Node verifier passed **23,370 assertions**. A separate seeded selector stress test checked 13,356 bounded-degree graphs and 71,370 node instances. Same ORIGINAL F9 common pins (x3,x5,x6,x7,x8)=(0,1,0,0,0), pivot x1=0/1, give SAT2 versus UNSAT0; the UNSAT branch has eight falsified original-clause completion leaves. Eight malformed source controls rejected. No U198/V198 fresh replay or native FLMV machine trace this run.

### Full work and status
For each actually executed step charge grammar, source/index/head, acquired graph/degree coloring and failed choices, candidate switches, terminal clique checking, every resolvent/output-bit/proof record, cache/GE/semantic checks if invoked, child access, guest DELAY/COPY/RECOMP if invoked, and simultaneous peak ancestor/residual/index/proof/guest writable space. The specified decision algorithm does NOT invoke guest/GE/semantic comparison, so their executed charges are zero, not free external services. Offline XOR tracing has no algorithmic role.

**Falsifiers:** F1 large clique invalidates Brooks coloring (confirmed, charged bounded terminal); F2 repeated projection forces superpolynomial intermediate CNF (falsified for R rounds); F3 a free semantic quotient is necessary (falsified for this exact syntactic route); F4 polynomial total SAT work follows (false, exponential enumeration remains).

**Exact gaps:** neither polynomial total-work on every canonical original nor unrestricted arbitrary-decider lower bound, unknown-exponent A->Phi(A) power-shortening or strict numerical SAME-MACHINE FLMV transfer is proved. Restricted fast recognizable families remain counterexamples to pointwise hardness. **P versus NP OPEN.**

**Sources and duplication:** Döcker 2019 (arxiv:1912.08032), Brooks 1941, Davis-Putnam 1960, Bryant 1986, Fortnow-Lipton-van Melkebeek-Viglas JACM 2005 (doi:10.1145/1101821.1101822). Previous LSPV-1 327 and 330 and current five-role handoff read by authenticated GitHub. Web queries: D"ocker monotone (2,2), existential projection, FLMV. GitHub code search in j15marti/pnp returned no matches for the narrow term; OpenAI code results were unrelated arithmetic circuits; no novelty inferred from these outcomes. Direct web open of handoff failed 404, connected GitHub file read succeeded.

Full Python source, no-import JS verifier, raw JSON, Brooks stress cases, this complete report and hash manifest are in the local reproducibility archive. The compact GitHub numerical reproducer is a reference check, not a substitute for the full archive. Root main.tex deliberately left untouched to avoid concurrent role writes.

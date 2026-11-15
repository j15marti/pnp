# TMR-2/038: Nonaffine high-treewidth cofactor mass collapses under a certified autarky and a real SAT shortcut

**2026-11-14 23:21 PST | COFSEP066 | PNP Information Necessity**

**Status:** PROVED/RESTRICTED for the explicit family and conditional tariff failure. Independent mathematical peer review OPEN. Finite checks COMPUTATIONAL. Universal machine-to-abstraction transfer, superpolynomial sound initial potential, and P versus NP OPEN.

## 1. Candidate and falsifiers fixed before source review

**Candidate under test:** Pairwise inequivalent full Boolean cofactor relations across a cut, even after excluding syntactic Horn, dual-Horn, Krom, affine and low-treewidth cases, might admit a fixed positive fusion-Lipschitz tariff weight.

Four preselected falsifiers: (F1) a real syntax-aware fixed SAT decider accepts the family in polynomial time; (F2) a certified autarky eliminates all clauses; (F3) compact shared representations make exponential cofactor multiplicity cheap; (F4) the full Boolean relation is identically zero for UNSAT formulas, leaving no distinct global cofactors. F1, F2 and F4 hold. This is a negative test of this *specific* proposed separator component, not a general impossibility theorem for dynamic, locally authenticated and AND-aware interface measures.

This differs from prior TMR-2/037's arbitrary-hidden-source certificate ceiling and TMR-5/034's affine source-bound minimum core. The new witness uses proper 3-CNF, high primal treewidth, semantic non-Horn/non-dual-Horn/non-Krom/non-affinity, and a correct fixed all-input SAT-machine bypass.

## 2. Fully specified family and encoded length

For integer k>=3, use X_1,...,X_k; Y_1,...,Y_k; Z_1,...,Z_k. Define F_k with the following proper three-distinct-variable clauses:

$$
A_i^+=(\neg X_i\lor Y_i\lor Z_i),\quad
A_i^-=(\neg X_i\lor Y_i\lor\neg Z_i),
$$

$$
B_i=(X_i\lor Z_i\lor\neg Y_i)\quad (1\le i\le k),
$$

$$
D_{ij}=(Z_1\lor\neg Y_i\lor\neg Y_j)\quad (1\le i<j\le k).
$$

Every clause has exactly three distinct variables and at least one positive literal. Each of the 3k variables occurs in both signs, so the ordinary pure-literal shortcut does not directly apply. There are m=3k+binom(k,2) clauses.

Use one-based IDs 1..3k. Let b=ceil(log_2(3k+1)), h=ceil(log_2(m+1)). The concrete binary source uses unary 1^b 0 followed by b-bit variable count, unary 1^h 0 followed by h-bit clause count, then exactly 3m literals, each a sign bit plus b-bit variable ID. The parser rejects malformed headers, IDs, clause arity, trailing bits, or duplicate-variable clauses. The exact length is

$$
L_k=2b+2h+2+3m(b+1)=\Theta(k^2\log k).
$$

A single fixed finite-alphabet deterministic multitape machine can parse, compare IDs, and validate the all-positive-clause property with a conservative O((L+1)^3) transition bound; malformed handling and complete fallback SAT search are part of the fixed program. No nonuniform advice, unbounded-word arithmetic or free formula syntax oracle is used.

## 3. Exact cofactor theorem and wide primal graph

For a in {0,1}^k, let R_a(Y,Z) be the full Boolean satisfaction relation of F_k after assigning X=a. Define the candidate raw input component

$$
p_{\mathrm{sep}}(F_k)=\lvert\{R_a:a\in\{0,1\}^k\}\rvert-1.
$$

For each j let Y^(j) have every coordinate 1 except Y_j=0; set all Z=1. Direct substitution into every clause proves

$$
R_a(Y^{(j)},\mathbf 1)=1-a_j.
$$

The vector of these k evaluations is the bitwise complement of a. Therefore the 2^k residual relations are pairwise distinct, even using the SAME Z=1 slice for every a:

$$
\boxed{p_{\mathrm{sep}}(F_k)=2^k-1
=\exp(\Omega(\sqrt{L_k/\log L_k})).}
$$

All pairs (Y_i,Y_j) co-occur in D_ij, so the primal graph contains the clique K_k and has treewidth at least k-1. This width is not itself a lower bound.

**Global-UNSAT cofactor firewall:** On ANY UNSAT F, the global satisfaction relation is the constant-zero function; every full-formula restriction F|_{X=a} is the same constant zero. Thus a distinct-full-cofactor-minus-one component is IDENTICALLY ZERO for every UNSAT source, irrespective of alleged source hardness. Local subformula/interface relations before AND-join may differ, but cannot be identified with this global component.

## 4. Explicit semantic Schaefer controls and autarky

The all-one total assignment is a satisfying witness, since every clause has a positive literal. In fact the partial assignment Y_i=Z_i=1 for every i, leaving all X_i unassigned, touches and satisfies EVERY clause. It is a certified 2k-variable autarky: authenticated autarky elimination removes the whole formula.

The full satisfying-assignment relation is semantically outside each of the common tractable closure classes (for all k>=3), not merely syntactically mixed. In the following models all unspecified X,Y are zero, all Z_i for i>1 are one, and e_i is the i-th unit Y-vector:

* Non-Horn: H1=(X=e1,Y=e1,Z1=0) and H2=(X=0,Y=e1,Z1=1) are satisfying; their bitwise AND violates B1.
* Non-dual-Horn: A=(X=0,Y=e2,Z1=0), B=(X=0,Y=e3,Z1=0) are satisfying; their bitwise OR violates D_23.
* Non-bijunctive: C=(X=0,Y=e2+e3,Z1=1) also satisfies, but coordinatewise majority(A,B,C) violates D_23.
* Non-affine: E=(X=0,Y=0,Z1=0) also satisfies, but coordinatewise XOR(A,B,E) violates D_23.

Thus the relation is not preserved by AND, OR, majority, or ternary XOR, respectively. This does not assert that any of those syntactic/semantic failures makes SAT hard. The verified autarky is the relevant cheap mechanism. Equality/union-find, caching, learning, extension variables, circuit shortcuts, and Gaussian closure must remain permitted; none is needed to beat this explicit example.

## 5. Quantitative all-step tariff falsification

**Qualified system A, actual SAT machine:** complete concrete configurations include authenticated full formula input, ONE fixed correct total deterministic SAT decider, finite control, work tapes, heads, buffers and terminal status; each actual machine transition costs one. Zero-cost closure is identity.

Choose a total SAT decider that first authenticates a proper 3-CNF and scans for at least one positive literal in EVERY clause. If all clauses pass, accept by the all-one witness. Otherwise run a complete fallback SAT search. This is correct on all well-formed inputs and accepts F_k in W_A(F_k)<=c(L_k+1)^3 transitions for one fixed c, independently of k. On the easy path, there is no proof-calculus borrowing.

If a naive source-locked component equals p_sep(F_k)=2^k-1 until terminal acceptance and is then masked to zero, the one-price final halt has the exact tariff row

$$
(\Delta_{\mathrm{sep}},w)=(2^k-1,1),
\qquad \lambda_{\mathrm{sep}}\le \frac1{2^k-1}.
$$

This is a new explicit **family** instantiating TMR-1/035's known general terminal-mask firewall, not a newly invented terminal theorem.

For ANY state-dependent nonnegative all-step-sound potential whose initial vector contains raw p_sep with nonnegative weight lambda_sep and whose completed goal has Phi<=0, telescoping along this genuine machine run gives

$$
\lambda_{\mathrm{sep}}(2^k-1)\le\Phi(C_{0,k})
\le W_A(F_k)\le c(L_k+1)^3.
$$

Consequently,

$$
\boxed{\lambda_{\mathrm{sep}}\le
c(L_k+1)^3/(2^k-1)\longrightarrow0.}
$$

There is no length-independent positive weight for this raw full-cofactor feature on a potential valid for this machine and all its inputs. This is stronger than merely finding a source-only query shortcut.

**Qualified system B, different zero-cost authority:** If a separately specified proof/abstraction system genuinely receives the *already authenticated* Y=Z=1 autarky as available zero-cost data, its authentic zero closure removes all clauses. The closed initial p_sep is zero, not 2^k-1. This is a distinct model and cannot be treated as a free SAT-machine operation: constructing, reading and verifying an autarky costs physical work. In either qualified interpretation the raw cofactor initial gap fails, for different reasons.

This does NOT falsify an obstruction restricted to some hard UNSAT family, a genuinely dynamic locally authenticated relation, or a full reduced-product potential that stores all outstanding AND obligations and pays for every actual transition. No seven-column all-SAT-machine tariff or general algorithm-to-proof transfer is claimed.

## 6. Evidence, controls, and exact dependency status

Executed original V8/ES2020 verifier:

- Code: experiments/tmr/tmr2_cofactor_autarky_firewall066.js
- Raw: results/raw/tmr/2026-11-14_2321_TMR2_COFSEP066_V8_RAW.json
- Result: **20,682 assertions, zero failures**.

Checked k=3,4,5,6,7,8,10,12,16,20,30 for grammar, dual-sign incidence, positive-literal all-one witness, authenticated autarky, Y-clique, and AND/OR/majority/XOR semantic closure falsifiers. Exhaustively enumerated all complete assignments at k=3 and k=4 for SAT control. Independently checked all 2^k distinguishing cofactor signatures for k<=10. At k>10 cofactor counts are symbolic conclusions of the all-k proof, not claims of exhaustive 2^30 execution. Native Turing-machine compilation was not executed.

| Component | Status |
| --- | --- |
| Proper CNF encoding and 2^k distinct cofactor relations | PROVED/RESTRICTED |
| Wide primal graph and semantic non-Horn/non-dual/non-bijunctive/nonaffine | PROVED/RESTRICTED |
| Certified autarky and polynomial correct SAT-machine path | PROVED/RESTRICTED |
| Positive uniform raw full-cofactor tariff | FALSIFIED for the specified all-input SAT machine |
| Nontrivial UNSAT potential from global full-formula cofactor count | FALSIFIED, identically zero |
| Fusion-safe local relation/branch/context component | OPEN |
| Superpolynomial initial gap and unrestricted machine transfer | OPEN |

**Peer targets:** TMR-3 should charge the actual finite-alphabet all-positive scan and final halt. TMR-4 should replay this legal autarky under an explicitly qualified zero-cost closure, without deleting the cheap path by CEGAR. TMR-5 should audit the four semantic closure witnesses and source-length bound. TMR-1 should distinguish the globally zero UNSAT satisfaction relation from local authenticated pre-join clause relations. Next TMR-2 target: build local interface/cofactor components that remain nontrivial before conjunction, track shared source identities and all AND joins, and survive certified autarky, cheap algebra and compact circuit controls.

## 7. Provenance and primary sources

Prior original project reports read: TMR-2/037 general certificate envelope, TMR-5/034 affine mincore, TMR-4/038 XOR ancestry, LEAD-0029 Lipschitz audit, LSPV-3/453 treewidth correction noting earlier stronger /361, and LEAD 2026-10-08 TWIN-AUTARKY. Prior /341 stays FAIL as full logical authority; /386 stays RESTRICTED. The new results do not amend either system.

1. Schaefer TJ. The complexity of satisfiability problems. STOC 1978:216-226. https://doi.org/10.1145/800133.804350 . Background for Boolean relation tractability classes, not a source for the explicit witness proof.
2. Bryant RE. Graph-based algorithms for Boolean function manipulation. IEEE Trans Computers. 1986;35(8):677-691. https://doi.org/10.1109/TC.1986.1676819 . Cofactor and OBDD context; no lower bound imported.
3. Kullmann O. Investigations on autark assignments. Discrete Applied Mathematics. 2000;107:99-137. https://doi.org/10.1016/S0166-218X(00)00262-6 . Autarky background; the certificate is explicitly verified here.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1 fetched completely, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343. proof2 and main.tex initially returned empty Contents bodies but were fully recovered using authenticated Git blobs 930c5eeddafce656717f28055a7a755f44737c and 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. All five TMR handoffs, issue #3, AGENTS, CODEX, skill, and controlling directives inspected. No root tracker/manuscript write or schedule change. **P versus NP OPEN.**

END_OF_REPORT::TMR2::038::2026-11-14_2321_PST

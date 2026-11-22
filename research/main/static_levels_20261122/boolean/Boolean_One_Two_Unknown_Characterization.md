# Independent Boolean one-unknown and two-unknown characterizations

Research date: 22 November 2026, America/Los_Angeles.

Status: PROVED/EXACT for the stated finite Boolean residual classes and binary-resolution proof measure. COMPUTATIONAL checks concern normalized clauses only. No unrestricted time lower bound or strict T_q transfer is asserted. The generic cube-cover and certificate viewpoints are established methods, not novelty claims.

## 1. Independent input at each level

For each r analyze a separate instance I_r=(F,U,rho), where F is a Boolean k-CNF, U is a declared set of r unknown variables, and rho fixes all others. A solver starts afresh from this input. It receives no earlier execution state, verdict, or certificate. Correctness is required for both labels in the declared input class even when the analyzed instance is UNSAT.

Let G=F restricted by rho: discard clauses satisfied by fixed literals, delete false fixed literals, remove duplicate literals, and discard tautologies. This is a semantic normalization for the theorem. Raw-input normalization and access remain charged in an implementation.

For a residual clause C put

\[
B(C)=\{a\in\{0,1\}^r:C(a)=0\}.
\]

Then G is UNSAT exactly when the B(C) cover the assignment cube. Define

\[
\mu(G)=\min\{|H|:H\subseteq G,\ \bigcup_{C\in H}B(C)=\{0,1\}^r\}.
\]

This measures the fewest residual source clauses that positively certify UNSAT. It is not the cost of locating those clauses, a claim that all algorithms construct this certificate, or the information content of the one-bit output. Each selected residual clause can be traced to an original clause; certifying its residual type also requires checking its literals and the relevant supplied values.

The established correspondence between minimal UNSAT clause sets and irredundant covers of the Boolean cube is explicit in Kullmann and Zhao [1]. The distinction between minimum consistent certificates and optimal worst-case decision-tree depth is explicit in Buhrman and de Wolf [2]. Our special-case arguments below are direct and self-contained.

## 2. One unknown: complete characterization

For U={x}, nontrivial normalized clauses have exactly three possible types: empty, x, and not-x. Let E, P_x, N_x denote presence of these types. Then

\[
\operatorname{UNSAT}(G)=E\lor(P_x\land N_x).
\tag{1}
\]

Proof: an empty clause fails for both x-values. Otherwise x=0 is blocked exactly when x is present, and x=1 is blocked exactly when not-x is present. Both assignments are blocked exactly when both units occur.

Thus every minimum source core has size one (an empty clause) or two (opposite units). If the original complete assignment falsified exactly one clause and one of its variable values is removed, that clause becomes a unit. On an actually globally UNSAT source, either a still-empty clause exists or an opposite active unit must exist. The solver is not given global UNSAT as a promise and must acquire the evidence.

An active clause is an original clause whose fixed literals are all false. Longer original clauses change the cost of checking activity but do not add new residual types at r=1.

## 3. Two unknowns: all twelve prime core types

For U={x,y}, the normalized types are empty, x, not-x, y, not-y, and the four binary clauses. Let E,P_x,N_x,P_y,N_y be their presence flags. For a,b in {0,1}, let B_ab be the presence flag for the binary clause falsified only by x=a,y=b:

| Flag | Clause | Blocked assignment |
|---|---|---|
| B_00 | x OR y | 00 |
| B_01 | x OR not-y | 01 |
| B_10 | not-x OR y | 10 |
| B_11 | not-x OR not-y | 11 |

A unit blocks one edge of the square; a binary clause blocks one point; an empty clause blocks the whole square. The exact monotone presence DNF is

\[
\begin{aligned}
\operatorname{UNSAT}(G)={}&E
\lor P_xN_x\lor P_yN_y\\
&\lor P_xP_yB_{11}\lor P_xN_yB_{10}
\lor N_xP_yB_{01}\lor N_xN_yB_{00}\\
&\lor P_xB_{10}B_{11}\lor N_xB_{00}B_{01}
\lor P_yB_{01}B_{11}\lor N_yB_{00}B_{10}\\
&\lor B_{00}B_{01}B_{10}B_{11}.
\end{aligned}
\tag{2}
\]

Juxtaposition in (2) means Boolean conjunction. These are exactly its twelve prime positive terms: one singleton, two pairs, eight triples, and one quadruple.

### Proof of completeness

If an empty clause exists it is a singleton core. If opposite units exist they form a two-clause core. Otherwise the units are consistent. Let t be the number of variables pinned by the units, so t is 0, 1, or 2. Exactly 2^(2-t) assignments survive them. Every binary clause blocks one assignment.

If t=0, all four binaries are required. If t=1, the two assignments on the surviving edge require two binaries, giving a three-clause core. If t=2, the single surviving assignment requires its binary blocker, again giving a three-clause core. Any further clause is redundant in a minimal core. These are precisely the terms in (2).

Every term is prime because removing any one of its clauses uncovers an assignment. Each term can occur by itself, so none is redundant in the DNF. For any UNSAT clause set, mu(G) is the size of its smallest true term.

Up to renaming and negating variables, the five core shapes are:

| Shape | Representative | mu |
|---|---|---:|
| Empty | empty | 1 |
| Opposite units | x, not-x | 2 |
| Two compatible units plus a blocker | x, y, not-x OR not-y | 3 |
| One unit plus the opposite edge's two blockers | x, not-x OR y, not-x OR not-y | 3 |
| All four point blockers | All four binary clauses | 4 |

The largest possible minimum source core is exactly four. Original clause width k>=2 suffices to realize these residual types. For exact-k source clauses, fixed-false padding can realize them when permitted by the declared source grammar; no bounded-occurrence or strict-template closure is inferred.

## 4. Exact shortest binary-resolution refutation

For an UNSAT Boolean residual formula with r<=2,

\[
\boxed{\text{minimum binary-resolution inference count}=\mu(G)-1.}
\tag{3}
\]

Input clauses are counted separately. Residual normalization steps and literal/pin acquisition are excluded from this proof measure.

For the upper bound, an empty clause needs zero steps and opposite units need one. The core x,y,(not-x OR not-y) resolves in two steps. The core x,(not-x OR y),(not-x OR not-y) resolves the binary pair to not-x and then resolves with x, also in two. Four binaries resolve two pairs to opposite units, then those units to empty, in three steps.

For the lower bound, retain the root-connected ancestor DAG of a refutation. If it has g binary-inference nodes and b distinct source-clause leaves, it has at most 2g premise edges and is connected as an undirected graph. Therefore 2g>=b+g-1, giving b<=g+1. Its used source clauses must be UNSAT by soundness, hence b>=mu(G). Consequently g>=mu(G)-1.

This characterizes the shortest path inside a specified proof calculus. It is not an unrestricted instruction lower bound. An arbitrary machine may combine operations differently, and finding the displayed shortest proof is a separate problem.

## 5. Output, certificate, and complete profile are different quantities

The decision output is one bit. A source-clause certificate has size mu(G), at most two or four at the respective levels. A complete continuation-safe profile is the satisfying-assignment support S(G) subset of {0,1}^r.

For r<=k in unrestricted Boolean residual CNF, every support subset is realizable: exclude each unwanted assignment by its corresponding full-width residual clause. If S differs from T, pin all r variables to any assignment in their symmetric difference; this future context distinguishes the supports. Thus an exact source-free summary sufficient for every allowed pinning or added-clause context has 2^(2^r) distinct states and requires 2^r fixed bits.

| Unknowns | Complete support states | Complete support bits | Maximum minimum source core | Maximum minimum binary-resolution steps |
|---|---:|---:|---:|---:|
| 1 | 4 | 2 | 2 | 1 |
| 2 | 16 | 4 | 4 | 3 |

The state lower bound also applies to a deterministic one-pass residual-clause stream whose retained state alone must handle any legal future clause suffix. It does not require every unrestricted offline solver to materialize a truth table. A separately specified promise can reduce the set of legal supports and must not be silently changed.

## 6. Exact residual-record query cost

Fix a deterministic algorithm correct on both SAT and UNSAT residual clause lists before selecting the input. One query reveals one complete normalized residual clause record, at an index selected adaptively. Duplicate records are allowed, as in ordinary CNF lists. This model isolates discovery from raw normalization.

The worst-case query count is m, attained even on UNSAT inputs in nontrivial subclasses. The upper bound is a single scan with a two-bit or four-bit support mask.

For r=1 and m>=2, answer the first m-1 distinct queried positions with x and the last with not-x. Before the last query, a SAT completion using only x and an UNSAT completion with an opposite unit in an unqueried position are both legal. A correct algorithm cannot halt before the last query. The resulting UNSAT input has a two-clause certificate. Repeated queries cannot reduce this bound.

For r=2 and m>=4, use only the four binary types. Answer the first m-3 distinct queries with B_00, and the final three distinct queries with B_01, B_10, and B_11. Before the last query, the observations admit both a SAT completion omitting a point blocker and an UNSAT completion supplying all four types. Thus the last record is necessary on the resulting UNSAT input. Its minimum core has size four.

These are valid adversary arguments because the algorithm is deterministic, the final transcript specifies one fixed legal input, and correctness is required on the SAT alternatives too. They do not use an all-UNSAT promise. If a different input grammar forbids duplicates, the lower-bound family must be separately embedded in that grammar; it is not automatically inherited.

The same linear discovery lower bound can respect a promise that a fixed reference assignment violates exactly one row, while retaining both possible decision labels. For r=1 use reference x=0, return x on the first distinct query, a true residual row on every intermediate query, and not-x on the final query. Both the resulting UNSAT list and the SAT alternative replacing the last row by true have exactly one row false at the reference. True residual rows are possible in the original partially assigned source. For r=2 use reference 00, return B_00 once on the first distinct query, B_01 on distinct queries 2 through m-2, B_10 on query m-1, and B_11 on query m, for m>=4. Only B_00 is false at the reference; replacing the final B_11 by B_01 gives the SAT alternative. These are normalized-record adversaries. They do not assert that the source is promised globally UNSAT or that original positions and normalizations are free. Fixed-false padding realizes units/binaries in ordinary exact-k CNF with supplied guards when that source grammar permits it; a supplied-true guard realizes a true residual row.

The record-query conclusion is Theta(m), not an unqualified Theta(N) bit-time theorem. Raw word size, encoding, pin lookup, locality, normalization, and retained input all require the actual charged model. Neither this query upper bound nor its lower bound crosses an unrestricted SAT forbidden region merely because the original input was an NP-complete syntax.

## 7. Comparison across independent levels

For general r,

\[
\mu(G)\le\min(m,2^r).
\tag{4}
\]

Choose one violated clause for every assignment. Their union covers the cube and uses at most 2^r clauses. Alternatively, each clause of an inclusion-minimal UNSAT core has a private assignment that violates it and satisfies every other core clause; these assignments are distinct.

If some supplied values are erased and both resulting residuals are UNSAT, mu cannot decrease: a source-clause subset refuting the less restricted instance also refutes the more restricted one. This is a comparison of mathematical inputs. It neither presumes shared solver memory nor adds runtime across the independently started executions.

Since mu<=m, source-core cardinality alone cannot establish a superpolynomial time lower bound in the complete source length. Discovery, computation, or access must carry any stronger conclusion. A complete support table is only one permissible representation, so its 2^r size is not an unrestricted space lower bound.

There is a stronger width-sensitive ceiling. Every distinct normalized non-tautological clause has j distinct variables and one sign per variable, with 0<=j<=min(k,r). The total number of such types is

\[
L_k(r)=\sum_{j=0}^{\min(k,r)}2^j\binom rj.
\]

A minimal core cannot contain two identical residual clause types, because one would be redundant. Hence

\[
\boxed{\mu(G)\le\min\{m,2^r,L_k(r)\}.}
\tag{5}
\]

For fixed k, L_k(r)=O(r^k). In particular,

\[
L_3(r)=1+2r+4\binom r2+8\binom r3=O(r^3),
\]

where binomial coefficients with j>r are zero. Thus the values mu_1=2 and mu_2=4 do not imply repeated doubling at every level in fixed-width 3-CNF. This polynomial ceiling is on the number of clauses in the core, not on the difficulty of recognizing, finding, or proving that the core is UNSAT. A polynomial-size clause set can still pose the original decision problem. Equation (3)'s matching resolution upper bound is established only for r<=2, although its inference-DAG lower bound applies generally.

For a q-element finite domain, the general cover statement and mu<=min(m,q^r) remain valid for arbitrary constraints. The exact Boolean core classification and the necessity of all q^r support bits do not automatically transfer to strict T_q. The actual relation must determine which forbidden sets and separating contexts are realizable.

## 8. Executed evidence and scope

An exploratory inline Python run enumerated all 512 two-variable clause-type subsets. It observed 417 UNSAT subsets, minimal-core counts {1:1,2:2,3:8,4:1}, and minimum-core-size distribution {1:256,2:112,3:48,4:1}. No wall-time claim is derived from the tool's near-zero reporting field.

The companion standalone script is saved for reproducibility. A single bounded rerun of that complete script additionally checks all eight one-variable type subsets, and compares direct assignment evaluation against the exact DNF and minimum-core definitions. Its raw output is boolean_static_results.json. This rerun is necessary to attach reproducible source and raw artifacts to the previously inline exploration; it does not test an asymptotic hypothesis.

The script uses no random choices. Normalized clause types, direct truth evaluation, presence DNFs, and source-core cardinalities are the entire executed scope. The script does not test a native input parser, raw pin lookup, a physical machine, resource exponents, a proof kernel, or strict T_q. Equation (3) is proved symbolically and is not a separate executable resolution-search test.

## References

1. Oliver Kullmann and Xishun Zhao. Parameters for minimal unsatisfiability: Smarandache primitive numbers and full clauses. Author research manuscript, arXiv:1505.02318. https://arxiv.org/pdf/1505.02318 . Abstract and section 1 explicitly establish the cube-cover interpretation and define minimal UNSAT clause sets. Retrieved and read for this task on 22 November 2026.
2. Harry Buhrman and Ronald de Wolf. Complexity Measures and Decision Tree Complexity: A Survey. Author-hosted manuscript dated 13 December 1999; journal publication Theoretical Computer Science 288(1), 21-43 (2002). https://homepages.cwi.nl/~rdewolf/publ/other/tcs.pdf . Sections 3.1 and 4.1 define deterministic query complexity and consistent certificate complexity. Only these definitions and their distinction are used, not historical open-problem claims in the survey. Retrieved and read for this task on 22 November 2026.

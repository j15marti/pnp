# TMR-2/040: NAE clique rank, fooling-set and uniform degree-witness firewall

**2026-11-15 01:13 PST | NAERANK075 | PNP Information Necessity | PROVED/RESTRICTED symbolic construction, independent review OPEN; finite V8 tests COMPUTATIONAL. P versus NP OPEN.**

## 1. Candidate, model and preselected falsifiers

Candidate under attack: after removing easy affine, Horn/Krom and equality summaries, an exponentially high rank or rectangle-cover of a **non-Schaefer proper 3-CNF** relation with large primal treewidth might provide a positively weighted source-derived fusion/separator obstruction even for an arbitrary correct deterministic SAT machine.

Preselected falsifiers: (F1) a polynomially discoverable complete satisfying assignment without enumerating the separator matrix; (F2) a polynomial shared circuit despite exponentially many real-rank or 1-rectangle obstructions; (F3) an affine, autarky, structural or degree-profile quotient overlooked by the proposed rank feature; (F4) renaming, clause ordering or duplicate clauses corrupt a supposed uniform early decision. F1, F2 and F3 are realized; F4 is tested and repaired by duplicate removal.

The **qualified SAT decision system** is a fixed finite-alphabet total deterministic locally moving multitape machine reading a fixed binary encoding of proper three-distinct-variable CNF. The source length is L bits; all parsing, clause comparison, input rereads, auxiliary storage, witness evaluation and fallback search are charged. The source function's communication matrix is a separate **function-evaluation** object, not a transition lower bound for SAT decision. No external truth-table oracle is provided.

## 2. Explicit NAE source family

For k >= 2, introduce distinct X_i,Y_i,W_i for i in [k] and Z_ij for 1 <= i < j <= k. Let NAE(a,b,c) be the conjunction of the two proper three-literal clauses

$$
\operatorname{NAE}(a,b,c)
=(a\lor b\lor c)\land(\neg a\lor\neg b\lor\neg c).
$$

Let E=binom(k,2) and define

$$
Q_k(X,Y,W,Z)=
\bigwedge_{i=1}^k\operatorname{NAE}(X_i,Y_i,W_i)
\land
\bigwedge_{1\le i<j\le k}\operatorname{NAE}(X_i,X_j,Z_{ij}).
$$

It has n_k=3k+E variables, 2(k+E)=k(k+1) distinct proper source clauses and L_k=Theta(k^2 log(k+2)) bits in standard unsigned-index binary literal encoding. The primal graph contains K_k on X, so its treewidth is at least k-1. Every source variable appears in **both polarities**, and the all-zero and all-one assignments each violate every NAE block.

The complete relation of Q_k is neither Horn, dual-Horn, bijunctive nor affine: its existential projection onto any (X_i,Y_i,W_i) triple is *exactly* NAE_3. To extend a NAE-valid triple, put all other X_j=0, Y_j=1, W_j=0, and set Z_ij=1-X_i if the two endpoint X bits agree, otherwise Z_ij=0. NAE_3 is not closed under AND, OR, coordinatewise majority or ternary XOR, respectively. These four closure properties are preserved by projection, contradicting each of the four tractable relational classes. This does not assert that the *single explicit family* is NP-hard.

## 3. Exact rank and rectangle-cover theorem

Partition variables into X versus U=(Y,W,Z). Let M_k be the Boolean 2^k-by-2^(2k+E) matrix

$$
M_k(x,u)=Q_k(x,u).
$$

**Theorem NAERANK075-A (PROVED/RESTRICTED, peer review OPEN).** Over the rationals (equivalently the reals),

$$
\operatorname{rank}_{\mathbb Q} M_k=2^k.
$$

Moreover the exact minimum number of all-1 combinatorial rectangles covering the 1-entries is 2^k. In particular, there are 2^k distinct, nonzero X-cofactor rows.

**Rank proof.** Fix W=0, and sum M over all Z assignments. For x containing t ones, precisely t(k-t) edge pairs have unequal X endpoints. On an unequal pair either Z value satisfies NAE, while on an equal pair exactly one does. Also NAE(x_i,y_i,0) is x_i OR y_i. Thus the following exact column aggregation is a linear transform of M:

$$
K_k(x,y)=\sum_z M_k(x,y,W=0,z)
=2^{t(k-t)}\prod_{i=1}^k(x_i\lor y_i).
$$

Let B be the two-by-two matrix with rows/columns ordered 0,1:

$$
B=\begin{pmatrix}0&1\\1&1\end{pmatrix}.
$$

Then K_k=diag(2^{t(x)(k-t(x))}) B^{\otimes k}. Every diagonal factor is positive and det(B)=-1, so K has full row rank 2^k over Q. Rank(K)<=rank(M)<=2^k, proving equality. **Field warning:** this aggregation argument is over Q/R, not automatically over GF(2), since the positive row factors can be even.

**Rectangle proof.** For each a in {0,1}^k let c_a have Y=NOT a, W=0 and Z_ij=1-a_i if a_i=a_j (otherwise 0). Then M(a,c_a)=1. For a != b, some coordinate differs. If a_i=0,b_i=1 then M(a,c_b)=0, since its cross NAE block is NAE(0,0,0); in the opposite direction M(b,c_a)=0. Therefore the 2^k diagonal pairs form a 1-fooling set: a 1-rectangle can contain at most one. Conversely, all 1-entries can be covered by the 2^k row rectangles {a} x {u:M(a,u)=1}. The cover number is exactly 2^k. These are evaluation/communication measures, not an unrestricted SAT-machine time bound.

## 4. Charged uniform, renaming-robust polynomial SAT shortcut

For canonical Q_k, each X_i occurs in exactly k NAE blocks, hence in 2k source clauses. Each Y_i,W_i,Z_ij occurs in exactly one NAE block, hence twice. Since k>=2, X_i are exactly the variable identifiers with **more than two occurrences**.

Define ONE fixed total correct SAT decider D on arbitrary encoded CNF:
1. Authenticate the source grammar and reject malformed encodings according to the fixed parser.
2. Canonicalize and deduplicate identical original clauses, counting the cost of comparisons and working storage.
3. Set each source variable occurring more than twice to 0, every other variable to 1, and **evaluate all original clauses**. If this is a witness, accept.
4. Otherwise use an ordinary exhaustive exact SAT decider, with charged workspace and termination.

Correctness on *all* inputs is immediate: the early branch accepts only after actual clause evaluation; exhaustive fallback decides the rest. On every Q_k, all X are assigned 0 and all other variables 1. Every cross NAE becomes NAE(0,1,1), and every edge NAE becomes NAE(0,0,1), so D accepts in polynomial time. With a conventional fixed locally moving finite-tape implementation, repeated source scans, binary-ID comparisons and counters give a deliberately conservative bound T_D(Q_k)<=c(L_k+1)^8, with one constant c independent of k. No arithmetic on unbounded unit-cost words is assumed.

Clause reordering, literal reordering, **arbitrary bijective variable renaming** and arbitrary exact-clause duplicates preserve this early acceptance after charged canonical deduplication. Arbitrary unrelated new clauses or non-bijective variable merging are not included; the decider remains correct by falling back. The simple degree signature is a *witness-producing cheap quotient*, not a source oracle or a free zero-cost computation.

The source relation has a uniform O(k^2) shared Boolean circuit simply by evaluating each pair of three-literal NAE clauses once and ANDing the block results. Thus both rectangle rank and rectangle cover can be exponential despite compact representation.

## 5. Precise failure of the proposed tariff inference

Consider a nonnegative all-step cost-sound potential Phi for D's exact physical transition graph, zero/nonpositive at every completed goal, and suppose its **initial** value on Q_k includes a fixed positive coefficient lambda_rank on the unquotiented rank-minus-one source signature, without cancellation by other nonnegative components:

$$
\Phi_D(C_0(Q_k))\ \ge\ \lambda_{\rm rank}(2^k-1).
$$

Telescoping along D's authentic cheap accepting execution requires

$$
\lambda_{\rm rank}(2^k-1)
\le \Phi_D(C_0(Q_k))
\le T_D(Q_k)
\le c(L_k+1)^8.
$$

For any length-independent lambda_rank>0 this fails for all sufficiently large k. Consequently, **a positive fixed rank/rectangle-count tariff on this particular growing family is FALSIFIED/RETIRED** unless its claimed initial value is reduced by an authentic cheap-mechanism quotient. A source-independent terminal mask does not repair the final paid-step overdischarge already observed in TMR-1/035. In an ordinary physical Turing machine every transition is paid, so zero-cost closure is the identity; it does not license a free degree witness. One may add the real polynomial witness-finding operations to the graph and pay for them, after which telescoping still caps the initial potential.

The complete native-machine rule-by-rule tariff matrix has **not** been constructed here. The published companion JSON is an *aggregate necessary path inequality and counterexample record*, NOT a fictitious full transition inventory or certified LP. This counterexample does not exclude another hard SAT family, a more sophisticated dynamic computation-aware potential, or the target quantified P!=NP separation.

## 6. Hostile mechanism and provenance ledger

| Control | Observed or proved consequence |
|---|---|
| Gaussian/Tseitin | Projection NAE_3 is non-affine, yet affine-only resistance does not imply hard SAT |
| Horn, dual-Horn, Krom/SCC | Projected NAE_3 violates their closure classes; their inadequacy alone is not a lower bound |
| Bounded-treewidth separator DP | Primal K_k forces treewidth >=k-1, but degree witness decides the family |
| Certified autarky | The complete cheap witness is a total satisfying autarky, so a sound discovered-witness quotient erases the difficulty |
| Equality/union-find | This is not the EQ_k interface of TMR-2/039; pairwise NAE still admits a shared compact circuit |
| Compact circuits/extension/learning | O(k^2) evaluator exists, and no alternate short proof/witness path may be removed from a sound MAY abstraction |
| Sharing/recomputation/cache | A single degree-based witness is shared by all blocks; no per-row or per-block charge is compulsory |
| Padding/source size | Explicit L_k=Theta(k^2 log k), not a hidden exponentially long table |
| Renaming, clause order, duplicate clauses | Verified degree recognizer survives bijective renaming, reordering, and canonical deduplication |
| Zero-price closure | No physical zero-price TM transition; invented free closure forbidden |
| Historical checker | /341 FAIL as unrestricted logical authority; /386 RESTRICTED, neither used |

## 7. Original related work, primary sources, execution and novelty

Project comparison, read at original paths: H22-RANK in 'research/manuscripts/LB-0012-H22-RANK/main4_addition.tex' already established exponential compatibility rank plus a cheap SAT witness on disjoint clean-core blocks. LSPV-3 GATE323 ('research/agents/lspv-3/2026-11-02_0049_LSPV-3_CONNECTED_RANK_FORWARD_REVERSE_ESCAPE_GATE323.md') already built a connected rank-hard / decision-easy exact-(2,2) instance. LSPV-5 COMMUNICATION-POLARITY168 and TMR-2/038-039 already demonstrated communication/cofactor/guarded-interpolant model gaps. TMR-5/036 SHUFFLED-GAUSS showed a different affine-core polynomial shortcut. Historical NAEGAUGEHIGHGIRTH1 addresses gauge codes, UNSAT and local independence, not this rank/fooling/degree-witness construction.

**New relative to those sources:** one proper signed NAE3 family *simultaneously* has exact full real separator rank, exact 1-fooling/rectangle-cover number, non-Schaefer existential projection, linear primal clique width, absence of pure variables and uniform endpoint assignments, and a **single polynomial degree-witness decider robust to variable renaming, clause order and duplicate sources**. The proof is elementary and independent; no novelty is claimed for the general observation that communication rank does not imply SAT time hardness.

Primary background, used at exact scope:
- Thomas J. Schaefer, 'The Complexity of Satisfiability Problems', STOC 1978, pp. 216-226, DOI https://doi.org/10.1145/800133.804350. Relational tractability framework only; the four closure violations above are proved directly.
- Eyal Kushilevitz and Noam Nisan, 'Communication Complexity', Cambridge University Press 1997, Sections 1.3 and 1.4 (fooling sets, matrix rank). Accessible excerpt: https://assets.cambridge.org/97805210/29834/excerpt/9780521029834_excerpt.pdf. Rectangle and rank calculations are independently proved here.
- The controlling directive 'research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md', SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6.

**Actual execution:** one V8 ES2020 function, serialized to 'experiments/tmr/tmr2_nae_rank_fooling075.js', completed 11,749 assertions, zero failures. It exhaustively verifies exact row sums and rational BigInt rank of the 2^k-by-2^k aggregated K for k=2..4; all diagonal/cross fooling conditions and source/witness/renaming/duplicate controls for k=2..7. The original machine-readable stdout is 'results/raw/tmr/2026-11-15_0113_TMR2_NAERANK075_V8_RAW.json'. The standalone Node console wrapper has NOT been separately executed; no physical TM compiled. Numerical rank tests and finite controls are **COMPUTATIONAL**, not asymptotic proof. The symbolic proofs above cover every k>=2.

**Peer requests:** TMR-3 check the conservative finite-tape O((L+1)^8) bound and the degree-counting algorithm under exact source grammar. TMR-4 add an honest paid degree-witness MAY path to the reduced-product/rule matrix and test the resulting rank tariff. TMR-5 independently verify rank/rectangle and NAE projection, and test if renaming or duplicates truly preserve the early branch. TMR-1 audit family quantifiers and same-system transfer.

**Next exact target:** identify and test a *dynamic*, source-and-history-aware fusion interface component which cannot be cheaply discharged by the degree-witness and other known polynomial recognizers, and give its first all-transition row with TMR-3/4. The unrestricted superpolynomial initial gap and algorithm-transfer arrows remain OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt (full, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343); proof2.txt (full recovered by Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c); root main.tex (full recovered by Git blob SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34); latest issue #3, AGENTS.md, CODEX.md, skill and current five TMR handoffs reviewed. Root files unchanged; no scheduled agents changed. P versus NP remains OPEN.

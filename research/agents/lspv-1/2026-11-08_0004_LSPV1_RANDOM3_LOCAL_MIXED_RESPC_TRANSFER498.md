# LSPV-1/498 | Established random proper 3-CNF is exponentially hard for a precisely defined local-affine mixed fragment

**2026-11-08 00:04 PST | Route B | PROVED/RESTRICTED, conditional on the cited 2026 preprint theorem; finite syntactic checks COMPUTATIONAL | P versus NP OPEN**

**Material evidence node [P2-L1-498].** Refines the model-transfer ledger at [P2-B1] and [P2-C3]. [P2-D1] historical grammar and [P2-B2] same-calculus B3 are OPEN. Unlike the earlier source-essentiality linear bound [P2-F3], the following is an exponential lower bound for one *separately fixed*, sound, complete, effective, mixed-rule proof system. It is NOT claimed for historical R_mix341.

## IDEA and falsifiers, prior to literature review

Hypothesis: The published random proper signed 3-CNF family, hard in syntactic Res(PC_1/F2), stays exponentially hard if ordinary shared-DAG Resolution is supplemented with a sound local three-variable affine extraction rule and unrestricted shared GF(2) addition of its extracted equations. These operations may be syntactically simulated in Res(PC_1/F2) with constant-factor node overhead.

Falsifiers: (F1) the source family is not actually proved hard in Res(PC_1/F2) for the original with-replacement signed proper 3-CNF; (F2) a permitted local extraction cannot be implemented by syntactic rules using only the cited premises; (F3) global binary affine XOR cannot be translated with constant cost and original-source authentication; (F4) the proposed simulation silently admits derived affine-to-CNF conversion, fresh definitions, branching discharge, or unbounded-support local inference. F1-F3 were addressed under the exact conditions below; F4 is a genuine boundary and is deliberately EXCLUDED from the restricted theorem, not from historical R_mix341.

## Exact family and primary lower bound

For integer n >= 3, independently sample m=8n clauses uniformly with replacement from all 8*binom(n,3) proper signed three-variable clauses on n variables. This is Pang's F(n,3,8n). Each clause contains three distinct original variables and three polarity bits. The source bit length N is O(n log(n+2)) using explicit indexed literals, with m=8n records. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), Section 7.1, Theorem 7.2(a), states that with probability 1-o(1), every shared-DAG syntactic Res(PC_r/F_p) refutation has exp(Omega_{p,r}(n)) nodes, for every fixed prime p and r >= 1. The input random 3-CNF is UNSAT asymptotically almost surely. This relies on the random-CNF linear PC degree theorem of Alekhnovich--Razborov (2003). See https://arxiv.org/html/2610.00837v2 , specifically Fact 7.1, Theorems 1.1 and 7.2(a). This is a preprint-level external asymptotic theorem; no independent Lean or theorem replay was executed here.

Choose the fixed parameters p=2 and r=1. Source clauses are interpreted as disjunctions of linear equations x_i=0 or x_i=1. The cited bound applies to the ORIGINAL proper signed 3-CNF, without a 3-CNF encoding transfer.

## Fixed separate proof system R_loc3 (NOT historical R_mix341)

The proof DAG starts with exactly the original signed CNF source clauses and original variable names, and may use any finite sharing/reconvergence. Its paid unit-weight rules are:

1. RES: ordinary sound binary Resolution on original or previously derived *ordinary CNF clauses*, with correctly oriented complementary pivot literals and ordinary factoring. Derived width is unrestricted.
2. LOCAL3: from any collection of already available *ordinary proper width-three clauses with the SAME three-variable support*, derive a nonconstant affine equation L(x_i,x_j,x_k)=0, provided their conjunction logically entails this equation. The entailment is checked by the complete eight-row truth table, requiring no SAT oracle. Duplicate premises are irrelevant and at most eight distinct signed clauses exist on one triple. The output is an affine UNIT equation; it may NOT be converted back into ordinary CNF by this rule.
3. XOR: from two previously derived affine UNIT equations f=0 and g=0 derive (f+g)=0 over GF(2), including a contradictory 1=0 conclusion. Global affine rows and shared subproofs are permitted without a support-width restriction on XOR.

The source clauses are free leaves, with at least unit cost for every paid inference. There are no paid/free extensions, definition facets, LOCAL-CONVERT, assumption-split/discharge, affine equation-to-clause rules, generalized nonlinear factors, or arbitrary new axioms. This distinct calculus is sound, complete (RES alone is complete on UNSAT CNF), effective, uniform, and independent of n and F. It is intentionally weaker than any historical calculus that supplies all these additional rules.

## Theorem 498.1: linear-node syntactic simulation

Every q-paid-inference original-source-authenticated refutation DAG in R_loc3 of F with m source clauses and n variables yields a syntactic Res(PC_1/F2) refutation of the SAME original F with at most

$$
S_{\mathrm{Res(PC_1/F_2)}}(F)\le C(q+m+n+1)
$$

nodes for an absolute constant C. Original source clauses are preserved as source axioms, and shared DAG ancestors are translated only once.

Proof: For RES, represent positive/negative Boolean literals as linear equations and use Pang's syntactic linear-combination rule on the complementary pivot equations, then delete the derived false constant equation; this costs at most two nodes per step. For LOCAL3, the antecedents and consequence involve at most three original variables, and their semantic implication is authenticated by an exhaustive eight-row truth table. Pang's exact syntactic Fact 7.1 constructs the target consequence from these particular CNF antecedents using O(2^3*3) operations independent of n, with no semantic target inference rule. The target subproof attaches to the already translated antecedents, and its Boolean axioms are native target axioms. XOR is one application of the permitted syntactic linear-combination rule to two UNIT affine equations; final 1=0 deletion is another target step. Every translated edge respects the target grammar, and no local assumptions or unrelated-source clauses are introduced. Summing bounded gadgets over a shared source-bound DAG yields the stated bound. If target source/Boolean axioms are counted as nodes, the m+n additive term covers them.

By Pang Theorem 7.2(a), there exists kappa>0 such that with probability 1-o(1) over F~F(n,3,8n),

$$
W_{R_{\mathrm{loc3}}}(F)\ge \frac{\exp(\kappa n)}{C}-9n-1=\exp(\Omega(n)).
$$

Consequently for an unbounded sequence of original encoded lengths N=O(n log n), the worst-case restricted minimum grows at least exp(Omega(N/log N)). This is a genuinely *mixed* system with unrestricted shared ordinary Resolution, locally extracted affine equations, and global GF(2) summation, but NOT all historical mixed operations. Unlike finite SAT solver difficulty, this is an asymptotic proof-size conclusion at precisely the cited and simulated proof-system scopes.

## Source-local exact syntactic certificate and independent finite controls

An independently implemented Python checker and a separate Node.js checker replayed only the syntactic Res(PC_1/F2) operations: original source leaves, Boolean disjunction axioms, ordinary syntactic weakening, the stated linear-combination rule, and false-constant deletion. For every subset of the eight proper signed clauses on a single triple, and every nonconstant affine equation over that triple, entailment was exhaustively decided, and the exact source-to-equation proof was generated and replayed where applicable.

Both implementations tested all 256 original clause subsets and 14 nonconstant affine predictions. Exactly **224** implications hold. The generated certificate collection contained **8,224** target proof-node records, all accepted by the separate syntactic replay checks. The largest individual local certificate has **49** nodes including source leaves and three shared Boolean axioms. Both signed three-bit parity gadgets compile to **45** nodes each (4 source, 3 Boolean axiom, 16 weakenings, 15 combinations, 7 false-equation deletions). Python rejected seven hostile mutations; Node.js rejected six (corrupt premise/reference, false deletion, bad combination, wrong affine conclusion). The complete finite checks support the local construction, not the external asymptotic theorem or historical byte-level checker.

Published independently executable code: experiments/arc/lspv1_498_local_respc_sim.js; raw results: results/raw/arc/2026-11-08_0004_LSPV1_498_LOCAL_RESPC_RAW.json. An independent Python implementation and detailed raw results are also available as local conversation artifacts.

## Work, span, evidence, and transfer limitations

Logical node cost is the sum of distinct paid native inference nodes. Parent sources and shared lemmas are each referenced by ID and never copied as additional discovery steps in the ideal minimum. The translation has O(q+m+n) target inference nodes but explicit affine row masks can require Theta(n) bits and node-reference indexes require O(log(q+m+n)) bits. A conservative explicit target serialization budget is O((q+m+n)*(n+log(q+m+n))^2) bits, with polynomial construction and checking time, and no machine-time lower bound inferred. The eight-row truth table is constant work per local inference. Weighted span, storage retention/recomputation, parsing, source-index reads, verification, output, and failed search are separate physical costs, not equated with logical W. No all-input Route A or FLMV resource theorem follows.

**Missing full mixed transfer [P2-C3]:** LOCAL3 prohibits the strongest historical-looking features: AND3 accumulation of nonaffine factors, LOCAL-CONVERT, RES-generated clause-to-AND3 eligibility beyond this narrow macro, paid definitions/facets, affine equation-to-CNF feedback, explicit AND case-splitting with assumption discharge, and any stronger branching/shared lemma rules. The historical R_mix341 parser, grammar, weights, and accepted bytes are NOT authenticated by this separate calculus. Enlarging the rules can only lower the optimum and invalidates a direct lower-bound transfer. Haken's Resolution lower bound, Cook's ER polynomial PHP proof, and Tseitin GF(2) shortcuts remain mandatory opposite controls, not exceptions to exclude.

Search continuity: both full live trackers, governing November 2 five-role handoff, current issue #3 and actual newest LSPV-3/492 and LSPV-5/428 reports, Grok GROKPROOF/2026-11-08_0320_PROGRESS.md, Claude research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; external konard/p-vs-np README and scripts/proof_status.json, blkph0x/p-vs-np-proof-research README/METHOD_INDEX/PROOF_PORTFOLIO_BRIDGE_REPORT, meelgroup/frat-xor, peitl/short-proof and openai/math README. All give model-specific controls, not the missing all-mixed transfer. Primary source Pang 2026 v2 was read at actual theorem and native-rule lines. Branded Google UI and external Lean replay were not used; web search, GitHub contents and local Python/Node execution were used.

**Status:** PROVED/RESTRICTED, assuming Pang's stated preprint Theorem 7.2(a), with independently replayed finite syntactic evidence. This is material new restricted-family and transfer evidence [P2-L1-498], NOT a proof of [P2-B1] for historical R_mix341 or [P2-B2]/B3. [P2-D1] and [P2-C3] remain OPEN. P versus NP remains OPEN.

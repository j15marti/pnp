# LSPV-4/379: Guard restriction is P-complete even with one public wire

November 3, 2026, 23:36 PST. PNP Time-Space Resource Auditor.

**Status:** PROVED/EXACT by reduction from the KNOWN P-complete Circuit Value Problem (CVP), COMPUTATIONAL finite controls, CONDITIONAL logspace-normalizer barrier. B1/B2/B3, full mixed-calculus lower bound, and P versus NP remain OPEN. This is a theorem about a specified gate-value query, not a lower bound on all proof converters.

## Established hard family and limits

For unary pigeonhole PHP(h+1,h), there are h(h+1) Boolean variables, h+1 positive width-h pigeon clauses, and h*binom(h+1,2) negative collision clauses. The explicit signed indexed DIMACS encoding has N_h=Theta(h^3 log(h+2)) bits. Haken (1985) proves: there exist c>0 and h0 such that for every h>=h0 and every **ordinary unrestricted shared-DAG Resolution** refutation pi of PHP(h+1,h), pi has at least 2^(c h) lines. This does NOT apply to Extended Resolution, Res(XOR), R_mix341 or arbitrary uniform SAT deciders. Cook's polynomial Extended Resolution PHP proofs and linear paid GF(2) refutations of odd Tseitin remain obligatory escapes.

The preselected R_mix341 still has free original indexed clauses and charged unit-cost RES, AND3, GF(2) XOR, typed LOCAL-CONVERT and conservative two-input signed definitions. The present task is the computation arising when the signed-AND2 DEF fragment is **restricted by t=1** in LSPV-2/381. No inference rule or weight changes.

## Exact theorem

Let the source be ONE original Boolean wire t and an acyclic ordered list of q paid conservative signed-AND2 definitions:

$$ z_i = \ell_{i,1}\wedge\ell_{i,2}\quad(1\le i\le q). $$

Each signed input literal references t or an earlier gate. The output is one signed reference o. Gate IDs, polarities and order are authenticated. Restrict t=1 and define GCONST1(D,o) as its resulting one-bit output. With fixed-width binary gate indexes, input length M=Theta(q log(q+2)).

**Theorem (PROVED/EXACT from known CVP P-completeness).** GCONST1 is P-complete under uniform logarithmic-space many-one reductions, even with one external wire and only signed-AND2 gates.

**Proof.** P membership follows from topological evaluation and caching q Boolean gate values. Reduce the P-complete Circuit Value Problem on an arbitrary acyclic AND/OR/NOT circuit with a supplied input assignment. Encode source bit 1 by t and 0 by NOT t. Implement AND(a,b) as one new signed-AND2 gate z=a AND b. Implement OR(a,b) as one signed-AND2 gate z=(NOT a) AND (NOT b), and use the signed output NOT z. Implement NOT(a) simply by toggling the sign of the reference. Gate indices are monotone, and every output refers only to earlier nodes. Induction on the original circuit proves output equivalence at t=1. The mapping is computable in logspace using a gate counter, polarity bit and repeated scans to follow NOT aliases and recompute indices. Consequently the full P-hard CVP reduces to GCONST1. QED.

**Corollary (CONDITIONAL).** A uniform O(log M)-writable-bit transducer generating the final constant value or a correct complete per-gate constant-annotation record from arbitrary unannotated D would yield L=P. This is NOT an unconditional space lower bound, since L vs P remains open.

## Verification and machine-resource ledger

An eager indexed evaluation uses a q-bit cached array. A conservative fully charged bound is T=O((M+2)^3) bit operations and S=O(M) peak writable bits, including parsing, source and index reads, gate materialization, arithmetic and output. With a claimed Boolean value supplied **on a read-only input** for every gate, a separate deterministic checker uses repeated scans and O(log M) writable bits to authenticate every gate and the final output in O((M+2)^3) bit steps. Constructing the annotations is not included in verification and is not a free oracle. If the annotations are materialized on writable tape, that particular implementation uses Omega(q) writable bits.

Alternatively a lazy uncached recursive evaluator of depth d uses O(d log(M+2)) scratch bits with up to O(2^d (M+2)^3) bit operations. A chain z_i=z_(i-1) AND z_(i-1) has exponentially many expanded dependency walks, but cached evaluation takes polynomial time. These are **upper bounds for specified schedules**, not universal lower bounds. The output of q annotations itself costs Omega(q) write operations.

The corrected all-phase iterative ledger is:

$$ s' \le \max\{\rho,\eta,\lambda,\lambda s\}. $$

Here rho includes every preprocessing/materialization, index/source lookup, conversion, validation and output-buffer phase. Eager q=Theta(M/log M) cached bits means rho=1 at exponent resolution for that implementation; freeing the cache before recursion does not erase the peak. Lazy access must charge rereads and recomputation.

## Four falsifiers

F1: One public input wire makes full constant normalization trivial or automatically logspace. False as a generic complexity claim: this query is P-complete. No L!=P claim is made.

F2: Supplying a complete gate-value trace proves that generating the trace is cheap. False: verification is logspace with read-only annotations, while generation is P-complete.

F3: Exponentially many DAG dependency walks impose exponential actual machine work. False: shared eager evaluation is polynomial.

F4: This P-completeness invalidates LSPV-2/381's polynomial-time O(M)-space guard restriction, or establishes unrestricted SAT hardness. False. That existing resource bound is consistent with P-completeness.

## Exact checks and source review

The reproducible Node program uses deterministic seed 20261103, 166 three-input source circuit DAGs and all eight assignments per DAG: 1,328 instances. Each has two opposite forced-output CNF controls. Exhaustive enumeration found exactly 1,328 SAT and 1,328 UNSAT labels across 2,656 forced formulas, inspected 4,384 signed paid AND2 gate records, rejected nine malformed gate records and completed 5,322 assertions. The K4 Tseitin even/odd controls have respectively eight and zero solutions. These are COMPUTATIONAL controls only.

Read: November 2, 12:04 five-role refocus (blob c3889a3e514ddbd747150dcb68607013a3b2d154); issue #3; AGENTS.md, CODEX.md, pnp-research skill; LSPV-2/381 path research/agents/lspv-2/2026-11-03_2312_LSPV-2_GUARD_DEPENDENT_AND2_RESTRICTION381.tex (blob 671d56bfb6448ee6867b053169967e4e2bdb01b6); LSPV-3/386 path research/agents/lspv-3/2026-11-03_2324_LSPV-3_LOCAL_IMPLICATE_GUARD386.tex (blob 6cfe61a3d3f3fe11a52b3edbe986de861d08c1e9); Red Team/330 path research/main/2026-11-03_2248_MAIN_GUARDED-ENTAILMENT-DECISION-SEPARATION-REFEREE330.md (blob afc4b5ecf8034322634e1423ad90be12f1f7bd35).

Grok actually located: GROKPROOF/2026-11-04_0720_PROGRESS.md (blob 06304e87e03b707fd7930f3b2c5a43d0c9c0cf9b), explicitly leaves all-input fully charged contraction OPEN. Claude actually located: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a). Their restricted portfolio/sequential model claims do not prove B3. Prior LSPV-4/377 already established P-completeness for 3-wire port-map extraction; the present result specializes to the guard-dependent signed-DEF normalizer actually used in the newest exact proof lift, with a distinct work/space ledger. No novelty is claimed for generic CVP.

Searches: Haken resolution PHP, Cook Reckhow proof systems, Ladner circuit value P-complete, github.com/openai SAT proof checkers and repository Grok/Claude/peer filenames. Root main.tex reported blob 491477d17dfb5fef794bb2963a8c55118fd5f10a but empty body on authenticated bounded fetch, so no unsafe overwrite was attempted.

## Quantifiers and next missing bridge

B1: for every total correct fixed uniform SAT decider A, there is p_A such that every UNSAT F has W_R(F)<=p_A(|F|+T_A(F)). B2: for every A there is p_A such that all N obey Wbar_R(N)<=p_A(N+T_A^wc(N)); the worst-case runtime is over ALL binary strings of length <=N. B3: SAT in P implies Wbar_R_mix341(N) polynomial for that SAME fixed R. B1=>B2=>B3, all OPEN. Polynomial gate acquisition does not transfer Haken or prove a superpolynomial mixed minimum. Next exact obligation is a complete, type-preserving treatment of guard restriction across AND3, GF(2), named-wire LOCAL-CONVERT, including annotated evidence acquisition and all-phase machine work. P versus NP remains OPEN.

## References

[1] R. Ladner, The Circuit Value Problem Is Log Space Complete for P. SIGACT News 7 (1975), 18-20.
[2] A. Haken, The Intractability of Resolution. Theoretical Computer Science 39 (1985), 297-308.
[3] S. Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution. SIGACT News 8(4) (1976), 28-32.
[4] S. Cook and R. Reckhow, The Relative Efficiency of Propositional Proof Systems. JSL 44 (1979), 36-50.

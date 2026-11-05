# LSPV-2/426 | Partial extractor diagonal for solver-dependent Route A

**2026-11-05 13:12 PST | LSPV-2, Route A PRIMARY | PROVED/RESTRICTED conditional on SAT in P; finite controls COMPUTATIONAL | P versus NP OPEN.**

## IDEA, falsifiers, and precise predecessor

Hypothesis: the earlier project theorem [EXPONENT-EXTRACTOR-FIREWALL21](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-20_1848_MAIN_EXPONENT_EXTRACTOR_FIREWALL21.md), blob 982f7b0c, only excludes TOTAL computable extraction of polynomial resource exponents. Would a PARTIAL extractor, allowed to diverge on arbitrary machines but required to halt on **every correct total polynomial-time SAT decider**, bypass the barrier? Falsifiers: (F1) such partial divergence defeats self-reference; (F2) bounded simulation of the extractor makes the diagonal machine superpolynomial; (F3) padding corrupts SAT/UNSAT/malformed labels; (F4) this establishes impossibility of the proposed exponent-oblivious all-input contractor itself. F1-F3 fail under the precise construction below. F4 is a genuine limitation on this result: no contractor is refuted.

## Theorem 426.1 (PROVED/RESTRICTED; SAT instantiation CONDITIONAL)

Let L be any fixed language in P and let $\mathcal P_L$ contain all program indices of uniform, total, correct polynomial-time deciders of L, including padded implementations. There is **no partial computable** function E that (a) halts on every $e\in\mathcal P_L$ and returns a natural pair $(C,k)$ and (b) always correctly certifies $T_e^{wc}(n)\le C(n+1)^k$ for all sufficiently large n. The same holds for extraction of a correct peak writable-space exponent. For L=SAT this is conditional on SAT in P.

**Proof.** Fix a correct polynomial-time decider $A_0$ of L. By effective program self-reference (Kleene fixed point and parameterization), construct a machine D with its own code index d. On any input x of length n, D simulates E(d) for **at most n steps**. If a pair (C,k) is returned, D physically executes at least $(n+1)^{k+2}$ additional transitions; otherwise it performs no padding. Finally it runs $A_0(x)$ and outputs its exact answer. The bounded extractor simulation costs $n^{O(1)}$ on the fixed simulator. If E(d) never halts, D is polynomial by this bound and $A_0$. If E(d) halts at fixed time $\tau$ and produces fixed k, D is also polynomial, with exponent at most $\max\{O(1),k+2,\deg A_0\}$. Thus **in either case** d belongs to $\mathcal P_L$, so E(d) must halt. For every sufficiently large $n\ge\tau$, D uses at least $(n+1)^{k+2}>C(n+1)^k$ steps, a contradiction. The fixed-point implementation is intensional: D itself runs the padded code, not merely an extensionally equivalent function. QED.

**Space variant.** After E(d) returns a purported space exponent k, physically visit and modify $(n+1)^{k+2}$ distinct writable cells. This retains polynomial TIME on every fixed D, including the nonhalting-extractor case, but violates the alleged peak-space bound. Allocation-and-free cannot evade the simultaneous peak charge.

**Scope guard:** This excludes *a prerequisite that computes resource exponents from arbitrary promised solver code*. It does NOT exclude a computable but exponent-oblivious mapping $A\mapsto\Phi(A)$ whose constants are established **nonconstructively** afterward for each fixed A. This distinction was already central to /21 and remains essential to Route A.

## SEARCH | actual provenance and external scrutiny

Governing handoff first: research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, blob c3889a3e; issue #3 through LSPV-4/421; AGENTS.md blob 19656af1, CODEX.md 754999f5 and the pnp-research skill. Reviewed LSPV-2/424 blob 95ed3931, LSPV-2/425 blob adb44cd7, peer LSPV-4/420 blob e24528e3 and LSPV-4/421 blob a3610cde (correct filenames established by directory listing after two 404 path guesses). Read actual GROKPROOF/2026-11-05_1913_PROGRESS.md blob 8a004bf4 and Claude TPORT-0002 blob 1f9fc727: neither resolves all-input contraction.

Required external repositories actually inspected: konard/p-vs-np proofs/complexity/README.md blob 7ee9a11e (finite one-tape model, not matched FLMV); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea and ADAPTIVE_FRAGMENT_SYNTHESIS_REPORT.md blob b4ef7e87 (capped semantic projections, no universal contractor); MassimoLauria/cnfgen cnfgen/families/tseitin.py blob 4bb5fd19; openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4 (fixed costed bit program, not a theorem for all SAT-decider callbacks).

Web queries included 'partial computable time bound extractor defined on all polynomial time programs recursion theorem', 'Kleene recursion theorem partial computable program time complexity exponent', 'Blum 1967 machine independent theory', 'Tseitin 3-CNF Urquhart expander'. **Direct Google-branded search unavailable**; indexed web search used. Primary sources: Blum JACM 1967 DOI 10.1145/321386.321395; Kleene classical recursion theorem; FLMV JACM 2005 DOI 10.1145/1101821.1101822. Haken ordinary Resolution, Urquhart JACM 1987 DOI 10.1145/7531.8928 and Ben-Sasson/Wigderson JACM 2001 DOI 10.1145/375827.375835 remain certified restricted-system hardness controls, not input-decider complexity theorems.

## Established 3-CNF family ledger and verification

Cubic odd-charge Tseitin over a connected graph with H vertices: $3H/2$ edge variables, four forbidden-parity width-3 clauses per vertex (4H total), $N=\Theta(H\log H)$ ordinary sequential-ID encoded bits. Odd charge certifies UNSAT; even certifies SAT. Suitable expander sequences require $2^{\Omega(H)}$ ordinary shared-DAG Resolution refutations, but historical LSPV-2/341 gives a legal fixed mixed AND3/GF(2) refutation using 4H-1 paid nodes on bridgeless cubic instances. No computational lower bound transfer is claimed. Case splits must discharge all cases; assumption-local reasoning must not leak across incompatible branches. The new theorem needs no branch rule.

**COMPUTATIONAL controls:** finite K4 and cube Tseitin 3CNF instances only, not certified infinite expander families. K4: 6 edge variables, 16 clauses, 163 ASCII source bytes, odd UNSAT/even SAT, all 16 clauses and all 48 polarity positions pivotal. Cube: 12 variables, 32 clauses, 340 bytes, odd UNSAT/even SAT, 32 clauses and 96 polarity positions pivotal. These source-sensitivity controls are **already known** from LSPV-2/341 and /399. Malformed-source tests rejected. Python producer: 128 assertions. Independently implemented JavaScript checker: 229 assertions and 2 deliberately corrupted summary controls rejected. The independent checker in the repository was published with exact readback; its locally executed predecessor is in the attached reproducibility archive, and the published compact file has NOT been executed verbatim.

63 algebraic finite shadow cases check the padded exponent growth; exactly 5 small dummy loops (25,49,81,125,216 iterations) were actually executed. **Do not infer that the self-referential universal machine was built or run.** Its mathematical existence follows from the fixed-point proof, not from tests. The Python/JS exhaustive checker materializes input/work and is not an FLMV upper-bound implementation.

## ITERATE and remaining transfer

The proposed *partial* exponent-extractor repair fails. The genuinely viable interpretation is to construct an **exponent-oblivious** all-input, both-label, malformed-aware, recursively iterable $A\mapsto\Phi(A)$ and prove resource inequalities after fixing any correct polynomial decider. The target is still

$$
t'\le\max(11/10,3/5+t/2),\qquad
s'\le\max(1/2,s/2).
$$

For materialized children, peak must obey $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$, with all-phase $\rho\le1/2$ including preprocessing, output, temporary allocation, source/index-head access, guest simulation, shared caches and recomputation. No such universal contractor has been produced; the same-machine FLMV strict $1/90$ gap remains a **conditional** objective.

Artifacts: experiments/arc/lspv2_426_independent_verify.js; results/raw/arc/2026-11-05_1312_LSPV2_PARTIAL_EXPONENT426_raw.json; five-role handoff 2026-11-05_1312_LSPV2_PARTIAL_EXPONENT_ROUTE_A_HANDOFF426.md. Complete separately executed producer, independent checker, raw results and integrity manifest in the user-facing reproducibility archive. No task, role, schedule, R_mix341 grammar/weights or unauthorized manuscript region changed. Root main.tex was not written because GitHub returned blob 1b8a7d9a... with ZERO readable characters, making safe ownership-preserving reconciliation impossible. P versus NP OPEN.

# TMR-5/066: Exponential implicit-witness firewall under NP = coNP

Date: November 16, 2026 PST. TMR-5 / PNP Machine Bottleneck Redteam.
Status: PROVED/EXACT CONDITIONAL for authentic exponentially indexed Jahanjou-Miles-Viola (JMV) 3CNFs, with external independent mathematical review OPEN. P versus NP remains OPEN.

## Candidate, quantifiers and falsifiers

Fix any binary H in NTIME(2^n) \ NTIME(2^(n/2)), and its fixed uniform JMV Theorem 1 reduction at T=2^n and r=2. On n-bit source x the reduction produces a poly(n)-constructible decoder D_x mapping all 2^ell authentic addresses to 3-clauses using v-bit variable names; ell=n+O(log n) and v=Theta(ell). Under NP=coNP, claim there exists epsilon>0 such that for infinitely many lengths n some YES source x has NO satisfying implicit assignment represented by a shared fan-in-two circuit A on v bits with at most floor(2^(epsilon*n)) gates.

Falsifiers: (F1) the original decoder may not be constructible in poly(n) time, or may omit genuine addresses; (F2) the actual circuit-to-address interface may require materializing all 2^v assignment entries; (F3) zero violated addresses may not have polynomial-size NP certificates in the actual B_A encoding even assuming NP=coNP; (F4) an exponential-size guess and verifier might exceed 2^(n/2) on every positive epsilon after honest bit-machine costs. The original JMV theorem, TMR-1/068 and the actual source/circuit interfaces were inspected before the independent strengthening.

## Conditional theorem and proof

**Theorem C1f-EXP-WITNESS-FIREWALL.** Assume NP=coNP. For some fixed epsilon>0, for infinitely many n there is x in H intersect {0,1}^n such that every fan-in-two shared Boolean circuit A:{0,1}^v -> {0,1} of at most floor(2^(epsilon*n)) gates violates at least one authentic clause address of Phi_x. This is a lower bound on circuit representations of satisfying assignments of particular exponentially large *succinct* YES 3CNFs, not on ordinary explicitly encoded SAT solvers, and not a consequence of the unverified Anthropic count theorem.

**Proof.** Under NP=coNP the ordinary CIRCUIT-UNSAT language is in NP. Choose one fixed nondeterministic certificate verifier V_U with polynomial certificate bound and deterministic verification time O(L^d) for encoded circuit input length L and some integer d>=1. Let d_C be one constant bounding the degrees of the polynomial-time original JMV decoder generation, complete source authentication, optional O(poly(n))-query low-weight junta discovery and actual shared circuit composition. Let D=max(4,d,d_C) after absorbing polynomial composition overhead, and select a fixed rational 0<epsilon<1/(8D).

On input actual source x of length n, construct and authenticate D_x, charging the original poly(n) source generation. Nondeterministically guess one complete, topologically ordered, shared, unrestricted fan-in-two circuit A with s<=floor(2^(epsilon*n)) gates on v-bit names. Parse its full gate tables, indices and output. Construct the actual ell-bit shared violation circuit B_{x,A}(z): decode the authentic 3-clause at z using D_x, apply three correctly signed evaluations of the *same* A on its three v-bit variable names, and output 1 precisely if all three literals are false. Each original gate and copy is charged once; no 2^ell clauses and no 2^v assignment table are materialized. Repeated addressed clauses do not affect the zero predicate. For every A,

   B_{x,A} is UNSAT iff A's single implicit assignment satisfies every clause of Phi_x.

The source and B_A have L=O((n+s+1)poly(n+log(s+2))) encoded bits. Therefore L=2^(epsilon*n+o(n)) for all bounded guesses. Under NP=coNP, guess a certificate pi of UNSAT for the actual B_A and run V_U, rejecting malformed inputs or invalid pi. A SINGLE physical nondeterministic branch pays source acquisition, decoder generation, all optional Q=sum_{j<=w} binom(ell,j)=poly(n) full-vector queries, circuit guessing and parsing, actual shared-gate construction, certificate guessing, deterministic verification, addresses, retained buffers, output and every failed check. With the same choice of D, its time and peak live writable workspace satisfy

   T_branch <= poly(n)+O(L^D) <= 2^((D*epsilon+o(1))*n) < 2^(n/2)
   S_peak,branch <= poly(n)+O(L^D)

on all sufficiently large lengths. The certificate is guessed on ONE branch, not provided for free, and alternate branches are not summed as sequential work. This is a bona fide one-machine NDTM, not a network or unit-cost oracle construction.

Suppose no such infinitely many hard YES sources existed. From some n0 onward, every x in H of length n would have an A within the bound. Then at least one branch accepts every YES x using A and a sound UNSAT certificate. If x is NO, the JMV iff statement makes Phi_x unsatisfiable; every A violates a clause, so B_A is SAT, and no false UNSAT certificate can pass V_U. Hardwiring the finitely many shorter sources yields a single machine for H in NTIME(2^(n/2)), contradicting the original nondeterministic time hierarchy. QED.

This independently strengthens TMR-1/068's conditional no-polynomial-size implicit-witness theorem to a *fixed exponential* lower bound, but only under the conditional assumption NP=coNP. It neither assumes nor challenges the Anthropic main counting theorem. The constant epsilon depends on the verifier and compiler polynomial exponents, and is not advertised as numerically optimal. The result is consistent with hypothetical P=NP, which implies NP=coNP.

## Exact end-to-end resource ledger

| Stage | Charged object | Bound on same branch |
|---|---|---|
| Source and JMV construction | All n source bits, actual poly(n)-size shared decoder and malformed-source controls | poly(n) |
| Optional local-support discovery | Q=sum_{j=0}^w binom(ell,j) actual full-vector decoder calls, each source access and reply | poly(n), fixed w at r=2 |
| Nondeterministic guess | Shared A with s<=2^(epsilon*n) gates, v inputs, gate tables, labels, wires, parser | O((s+v+1)log(s+v+2)) description bits |
| Source-derived violation circuit | One D_x, three A references, signs, complete authentic ell-bit address domain | L=2^(epsilon*n+o(n)) bits |
| No-violations check | Materialized polynomial-in-L certificate and deterministic V_U | O(L^d) steps, no external oracle |
| Decision output | Accept iff certificate valid; reject all malformed/false candidates | Included |

The class consequence is about the infinitely often *YES* subset of the original nondeterministic hierarchy H. This does not give NP circuit hardness, and does not convert a lower bound for a succinct formula representation into a lower bound for all SAT algorithms. Functional Tseitin and the Anthropic promised #SAT normalization are unnecessary to this decision-only conditional implication, and are not silently charged as if used.

## Mandatory gates and hostile controls

DISJ sanity: **PASS restricted**. Interleaved DISJ, Horn/dual-Horn, 2SAT, affine/Gaussian, bounded treewidth, equality, autarkies, product and easy circuit classes remain legal cheap paths; no static rank or assignment mass gives universal work hardness.

Relativization: **OPEN for any oracle-lift; NOT APPLICABLE to a claimed P versus NP separation**. The proof is conditional on NP=coNP and the ordinary authentic JMV compiler. No claim that JMV's particular source interface works unchanged with an oracle; algebrization and Natural Proofs gates remain live for future NP promotion.

Simultaneous DTISP: **PASS for one restricted same-branch upper ledger; NOT APPLICABLE to a forbidden deterministic region**. Both T and S refer to one realized nondeterministic branch; no separate time/space machines.

Deterministic configuration counting: **NOT APPLICABLE to the nondeterministic hierarchy conclusion**. For fixed deterministic subroutines the standard total-machine T<=2^O(S+log L) remains an *upper* consistency check, not a work lower bound or an automatic quantum/randomized result.

Local bases and fields, unique-solution rank one, charged isolation, auxiliary/padding/selector/count normalizers, caching and recomputation are not prohibited. No majority, quantum amplitude or error-model theorem claimed. Historical /341 remains FAIL as full UNSAT authority; /386 remains RESTRICTED.

## Ranked track dependencies and one next target

1. TMR-1 source/solver/hierarchy: NEW conditional C1f witness firewall above; independent pinned Anthropic Lean 4.33.1/Mathlib axioms/nanoda and then matched physical/hierarchy verification remain OPEN. TMR-1/067's different all-witness bound assumes the pinned counting theorem; this result does not.
2. TMR-2 source transformation: D2/065 cancellation-certified quadratic spectral count is PROVED/EXACT RESTRICTED, independent review OPEN; arbitrary encoded SAT necessity/circuit lower-bound transfer OPEN.
3. TMR-3 checkpoint provider/evaluator: authenticated restricted models exist, generic adaptive reachable checkpoint provider plus improved nonassociative evaluator and complete Q,T,S ledger OPEN.
4. TMR-4 cost-sound compiler: restricted shared-core/OBDD source compilers exist; unrestricted reconvergent model transfer and reverse necessary-cost implication OPEN.

**ONE highest-value next target:** successful independent Lean 4.33.1, transitive axioms and nanoda replay of the pinned Anthropic MainResults/ETH proof on a functional Linux executor, followed by separate physical and E^NP consequence review. Previous runner jobs failed before proof execution; no blind extra retry.

## Evidence and verification status

Primary source [1]: Jahanjou, Miles, Viola, Local reductions, ECCC TR13-099 rev.3 (2014), https://eccc.weizmann.ac.il/report/2013/099/revision/3/download/, original Theorem 1 and Corollary 3(1') directly inspected including printed PDF page.
Project peer source [2]: research/agents/tmr-1/2026-11-16_TMR1_NPCOLLAPSE_SUCCINCT_WITNESS_FIREWALL068.md on draft tmr1-20261115-independent-lean060, blob ba5206856e6a46974b56586772f0bebc401232db, and /067 source blob a9d5a5693938fe789c67a723bf15352c158d6706.
Mathlib pinned source [3]: Computable.lean blob 7779a00f0c3c3909923a5f1bde6b3120b5c2d28a and StackTuringMachine.lean blob 916694942a3bfefa0bd9085e2f48735dbe8e0f5b at Mathlib commit 0df444a360eaa60ab8c11dca51a86af692955474, consulted for the distinct physical-machine dependency, not premises of this firewall.
Anthropic formal source [4]: pinned commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, still independently unrebuilt and not a premise of this firewall.

Actual work this run: source inspection, independent unbounded symbolic proof, dependency and gate audit. No numerical tests or raw evidence are claimed. No local checked-out pnp repo, so preflight was NOT run. No new kernel, nanoda, physical Turing microcode or complete main5 LaTeX compilation. No external independent mathematics review.

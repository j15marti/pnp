# REDTEAM37 | 2026-10-20 16:36 KST | EXP-WITNESS-FIREWALL
P versus NP OPEN. Exactly two active routes: (1) MCSP/MKTP, (2) arbitrary SAT-decider ARC/FLMV. Compact-history is diagnostic only; five roles :00/:12/:24/:36/:48 retained.

## Four falsifiers proposed before literature
F1 quantifier swap: forall-i exists-W_i vs exists-shared-W forall-i.
F2 long deterministic unique trace vs indexed circuit compactness; modular increment/DELAY control.
F3 under P=NP, universal small-W for deterministic exponential-time accepting tableaux versus deterministic time hierarchy.
F4 ordinary source-dependent query vs a short source pointer, hidden memory or nonuniform advice.

## CONDITIONAL THEOREM (exact)
Let L be a fixed language in EXP minus P (deterministic time hierarchy), accepted by deterministic M in time 2^{n^c}. Uniform indexed Cook-Levin encodes the accepting tableau on input x as exponential-size 3CNF F_x, with polynomial(n) local clause generator and poly(n)-bit clause/variable indices. On YES inputs essential tableau bits are the unique deterministic trajectory.

Assume P=NP. For EVERY fixed d, there are infinitely many YES x in L for which NO Boolean circuit W_x of size <=n^d indexes a satisfying assignment of F_x.

PROOF: If all but finitely many YES x had such a W, decide L in Sigma_2^P by guessing W of <=n^d gates and universally checking each indexed clause i in polynomial(n) time using W for its three literals. UNSAT instances have no such W, and finitely many missed YES instances can be hardcoded. P=NP implies Sigma_2^P=P, yielding L in P, contradicting the deterministic time hierarchy. Thus there are infinitely many bad YES inputs for every fixed d. This is NOT an unconditional circuit lower bound, and it does NOT exclude compact W for the project's PARTICULAR diagonal/self-padded YES family. It disproves only blanket inference from short deterministic program, unique accepting trace, or P=NP to universal compact indexed W.

F1 exact: (z) and (not z) are each separately satisfiable but not together; forall i exists W_i != exists W forall i.
F2 exact: for T=2^n, f(v)=v+1 mod 2^n has T-step orbit yet W(t,b)=bit_b(t) and final DELAY flag 1[t=T-1] have O(n) gate circuits; pointer-chasing t-query lower bound for arbitrary table oracle cannot be transported to a short explicit circuit.
F4 exact: (N,j) alone cannot distinguish sources with opposite x_j values. Ordinary Sigma3/MKTP queries need actual encoded semantics, with source acquisition charged.

## Primary theorem and model audit
Papadimitriou-Yannakakis 1986 DOI 10.1016/S0019-9958(86)80009-2; indexed succinct Cook-Levin detailed in Williams NEXP circuit-lower-bound literature, https://www.cs.toronto.edu/~toni/Courses/PvsNP/Lectures/lecture10.pdf . MMW STOC19 Theorem 4.2 https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf is a one-pass MKTP streamer with O(Mp) time, O(p) space, length-O(p) Sigma3 SAT queries on an ALREADY PRESENT target; not an ordinary SAT-to-MKTP generator. FLMV JACM05 https://lance.fortnow.com/papers/files/tst.pdf concerns deterministic random-access machines and same-realization time/space. Ilango SIAM J Comput 2026 DOI 10.1137/24M1652568 uses random oracle, not unconditional deterministic standard-model R_k.

## Bounded test
Local independent Python checker: 20,534 assertions, zero failures. Exhaustive checks of two opposite unit clauses; n=2..10 modulo-clock transitions up to 1024 time steps (short W projection+equality); 55 source-pointer opposite-label pairs. These do not computationally verify the asymptotic conditional theorem.

## Proof ledger and next arrow
ESTABLISHED: deterministic time hierarchy, locally computable exponential Cook-Levin tableau, P=NP => PH=P, MMW and FLMV in their own machine models.
PROVED CONDITIONAL: Under P=NP, no fixed polynomial shared-indexed-witness bound for all YES deterministic exponential-time tableaux.
COMPUTATIONAL: finite controls as above.
OPEN MCSP: uniform deterministic total both-label SAT-to-ordinary-MKTP R_k with fully charged short queries and target semantics; keep CHMY/OPS/Ilango hypotheses distinct.
OPEN ARC: hereditary arbitrary-decider A->Phi(A) with correct all-input gluing and simultaneous native FLMV time+space; materialized g<21/200 is a sufficient budget only for an unbuilt compiler.
OPEN compact diagnostic: same W existence for the SPECIFIC diagonal/self-padded YES family, not for general tableaux.

Handoff :00 reject ordinary pointer-as-query; :12 do not infer W from PH collapse or shortest program; :24 test EXP tableau against global witness assumption and charge buffers; :36 target family restriction vs EXP completeness; :48 preserve two routes and conditional proof status.
P versus NP OPEN.

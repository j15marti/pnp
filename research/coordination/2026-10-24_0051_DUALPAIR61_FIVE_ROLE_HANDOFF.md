# DUALPAIR61: LSPV-2 reverse-SAT handoff

Date: 2026-10-24 00:51 KST (2026-10-23 08:51 PDT). Status: PROVED/EXACT only within the specified canonical pairing calculus, independent review pending. P versus NP OPEN.

## Exact result and provenance

For proper unique signed exact-(2,2) source 3CNF with n variables, m clauses, 4n=3m, let p_S and q_S count all-positive and all-negative 3-clauses on unsigned support S. Paired supports consume one of each and require each variable in at most two paired supports. The **minimum number of leftover source clauses in this explicit calculus** is t_min=m-2 sum_S min(p_S,q_S). Proof: all local maximum pairs can be chosen simultaneously because every source variable has exactly two occurrences of each polarity, so no variable occupies more than two paired supports. Discovery, multiplicity certificate, signed-source readback: O(m log(m+2)) word time, O(n+m) words. Mixed-sign clauses may remain; t_min is even because m is a multiple of four.

Two **equal-input-length** strict signed exact-(2,2) SAT families have opposite defect extremes:
- P_q, a signed paired-NAE cubic prism: n=3q, m=4q, (t_min,delta)=(0,4q), construct a witness from cycle/rung edges.
- Q_q, two paired pivot implication cycles: n=3q, m=4q, (t_min,delta)=(4q,0), exactly 4*2^q models, all-zero witness.

At q=60, both have n=180, m=240, N=14,430 bits, w=15. For both, a polynomial, source-checkable direct algorithm bypasses the exponentially large optional branch count. The earlier Role-1 matching-cover solver and Role-2 blossom continuation, along with MAIN101's lockstep portfolio, remain exact upper bounds, not lower bounds.

## Reproducible controls

Full stdlib audit: seed 202610230838, SHA-256 1a1a8a4a7ee504e5e1069d3b9efdd887f234304079b84935577ed82f8f7db04e; 1,375 assertions, zero failures; 60 random strict-regular formulas; 44 small exhaustive checks; 863 bounded-degree hypergraph two-pin tests; two SAT/UNSAT proper-3CNF controls outside exact-(2,2). The full original 198/264 strict regular UNSAT source and matched SAT mutation from DOCKER-QUOTIENT59 were not reimported during this run. **Two-pin extendibility remains CANDIDATE/OPEN** after finite tests; no t<=2 all-input theorem follows.

## Inter-role use

Role 1: Treat t_min as an independently and optimally computed restricted defect, but test every claimed universal cost bridge against P_q and Q_q and direct template recognition.

Role 3: Try the exact source-labelled versus detached-source transport on the two equal-length instances. Source names may not be independently copied across clauses. Confirm root-label equality does not force optional pairing output.

Role 4: Seek a genuine strict signed-regular both-label adversarial family with large t_min and delta, using the source-verified DOCKER-QUOTIENT59 records. Test source permutations and signed-preserving SAT mutations.

Role 5: Integrate the exact restricted pairing optimum, not a compulsory representation requirement. MAIN101's portfolio remains valid; update only after independent reproduction.

## First missing lemma

Prove or falsify: every prescribed 2-source-bit assignment extends to a satisfying assignment of every 3-uniform paired-NAE hypergraph of support degree <=2. If false, publish minimum source-labelled counterexample. Neither outcome settles the universal rich-representation-versus-alternative-cost question.

Verified report: research/agents/lspv-2/2026-10-24_0051_LSPV-2_DUALPAIR61.tex
Executable reproduction: research/agents/lspv-2/2026-10-24_0051_DUALPAIR61_minirepro.py
Raw summary: research/agents/lspv-2/2026-10-24_0051_DUALPAIR61_raw_summary.json
Owned root main.tex region reconciled.

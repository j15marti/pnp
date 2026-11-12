# LSPV-1/592: Conditional Extended-Resolution strength barrier

**2026-11-12 07:03 PST | General SAT Lower-Bound Lead | historical Route B.**  
Status: PROVED/CONDITIONAL theorem in explicitly hypothesized all-source calculus; COMPUTATIONAL finite illustration. Historical R_mix341 application OPEN. P versus NP OPEN.

## Candidate and four falsifiers

CANDIDATE: If the native calculus admits arbitrary authenticated CNF sources, arbitrary fresh paid AND2 definitions with all three free defining clauses, and unrestricted strict Resolution between sources/facets/derived clauses, with fixed nonnegative constant weights and global shared-DAG payment, then the native system linearly simulates AND2-normalized Extended Resolution (ER). Thus a superpolynomial optimal-work lower bound for that full native system entails a superpolynomial ER, hence Extended Frege (EF), proof-size lower bound for the same family.

F1: Historical original-SOURCE grammar does not admit arbitrary CNFs (the recovered /386 sibling allows only cubic odd-charge Tseitin graph sources). F2: Native DEF cannot introduce every fresh AND2 owner with all three facets, or facet acquisition has extra positive/nonconstant cost. F3: Native Resolution cannot consume every legal source, facet or prior RES output with needed branch scope. F4: Fresh/exported/private wire, assumption discharge, guards or wrapper constraints prevent polynomially compiling arbitrary ER proofs. These falsifiers are OPEN for full R_mix341 and are not repaired by splicing distinct /341 and /386 surviving checkers.

## Theorem 592.1 (exact conditional simulation)

Fix a single calculus R and fixed weights w_D,w_R before selecting formulas. Assume that for EVERY signed CNF F, all SOURCE occurrences can be copied exactly under an independent external root; each fresh definition z <-> (a AND b), with signed earlier literals a,b, creates exactly one paid R owner at charge w_D and grants its clauses (-z OR a), (-z OR b), (z OR -a OR -b) without extra logical charge; every exact binary ER Resolution can be compiled into one R Resolution at charge w_R, permitting arbitrary whole-proof DAG sharing and arbitrary legal chronological parent reuse, no additional paid conversions, and a completed empty-clause refutation.

Then for every UNSAT F and every AND2-normalized ER refutation P of F, containing g(P) extension owners and r(P) Resolution inferences, a legal R refutation Q exists with

$$
W_R(Q)=w_D g(P)+w_R r(P).
$$

Consequently

$$
\overline W_R(F)\leq \min_{P\in ER(F)}(w_Dg(P)+w_Rr(P)).
$$

If weights are fixed positive constants and a family F_n has superpolynomial full-R minimum work relative to encoded length |F_n|, the same family requires superpolynomial ER proofs. Standard ER and EF p-simulate one another, so EF also has superpolynomial proofs for that family. General ER extension formulas can be converted to bounded-fanin AND/NOT circuits with polynomial overhead. If native translation has polynomial rather than unit overhead, the superpolynomial implication survives PROVIDED the uniform polynomial upper bound is authenticated.

PROOF: Copy each original authenticated SOURCE occurrence. Traverse the ER derivation in topological order; translate each fresh gate to the native paid definition and its three facets, and each exact RES inference to a native RES inference with the same signed pivot and two preexisting parent references. Induction verifies every clause and all ancestor/freshness identities. Owner fanout is free, each owner and each paid RES step is charged exactly once. The last record is empty. Sum the charges; minimize over unrestricted ER proofs. A polynomial ER proof family would compile to polynomial native work and contradict a purported superpolynomial all-native minimum. The standard ER/EF p-equivalence gives the final conditional conclusion.

The statement is NOT proof that historical R_mix341 p-simulates ER. The original /341 checker implements SOURCE/AND3/XOR only. The original /386 checker implements graph-restricted SOURCE/RES/DEF only, with guard and negative-test sentinel restrictions. Neither checker authenticates the missing native cross-rule interface. It would be an invalid source substitution or model switch to call these one system.

## Executed concrete reference-grammar illustration

Independent source F=(x) AND (y) AND (NOT x OR NOT y), one declared owner z=(x AND y), all three facets, five strict paid Resolution records, empty terminal. Exact reference logical work W=1+5=6. Local standalone Python 3 script executed source/facet/pivot/chronology/charge validation and all 8 Boolean gate assignments (36 assertion groups), established original UNSAT by 4 assignments, and rejected 12 hostiles: source forgery, caller-root substitution, missing owner, free owner, wrong facet, wrong pivot, forward parent, missing original source, fake LOCAL-CONVERT, nonfresh wire, undefined owner input, bad terminal. This is NOT an original R_mix341 accepted-byte certificate.

Code: experiments/arc/lspv1_592_er_simulation_firewall.py.
Raw: results/raw/arc/2026-11-12_0703_LSPV1_592_ER_STRENGTH_BARRIER_RAW.json.

## Dependency ledger and P-versus-NP firewall

P2-D1 OPEN: Authenticate original-source/general-DEF/defining facets/RES and all other genuinely accepted operations before applying simulation. P2-C3 OPEN: Every genuine translated ER shortcut is a legal MAY path and cannot be pruned as abstractly spurious. Preserve paid owner identities, context, assumptions, and entire shared DAG. P2-B1 OPEN: A superpolynomial lower bound for a native system satisfying these assumptions requires a superpolynomial ER/EF lower bound, a much stronger target than standard Resolution expander lower bounds. P2-B2/B3 separately OPEN: Even an EF proof lower bound does NOT establish P != NP without a noncircular same-calculus transfer from polynomial SAT decision. Likewise SAT in P does not automatically supply polynomial EF or this historical native work.

TRACKERS REVIEWED; NO MATERIAL CHANGE. Both root proof trackers and issue #3 were read. Root main.tex was deliberately NOT edited: current GitHub blob SHA was retrievable, but file content was empty, making safe full-content ownership-only replacement unverifiable. Relevant peer handoffs and reports: LSPV-1/539, /544, /549, /591; LSPV-2/575; LSPV-3/589; LSPV-4/562; LSPV-5/504, plus /341 and /386 original checker code. Instructions reviewed: AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Independent LSPV-5 falsification requested.

## Primary sources

1. Cook and Reckhow (1979), Relative Efficiency of Propositional Proof Systems, https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf
2. Reckhow, thesis, section 5.6.3, ER and EF p-equivalence, https://www.cs.toronto.edu/~sacook/homepage/reckhow_thesis.pdf
3. Krajicek, The Cook-Reckhow Definition, Theorem 2.2(3), https://www2.karlin.mff.cuni.cz/~krajicek/cr.pdf
4. Cousot and Cousot (1977), abstract interpretation, https://doi.org/10.1145/512950.512973
5. Clarke et al. (2000), CEGAR, https://doi.org/10.1007/10722167_15
6. Pich and Santhanam (2026), Towards P!=NP from Extended Frege Lower Bounds, JACM, https://doi.org/10.1145/3801091

All five original role identities, ownership boundaries, fixed weights, hourly Pacific schedules and two Route A/three Route B labels unchanged. No automation mutation. **P versus NP OPEN.**
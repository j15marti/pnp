# Finite crossing phases require an endpoint-information debit

22 November 2026, 00:05 PST. PNP Lower Bound Connections.
**DYNAMIC-PHASE-ENDPOINT-DEBIT1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT conditional lemma**; **FALSIFIED/RETIRED** for unrestricted truncation without endpoint information. Independent review pending. P versus NP **OPEN**.

Recovery revision: 5c68647aae3b7e5295990235bc8313732edeb04b. This closes one precise missing implication from the 23:07 Bounds report: how a complete-suffix conflict argument can be shortened to an actual finite phase. The price is retained endpoint information. No theorem that this price is small on hard SAT inputs is supplied.

## Model, quantifiers and four falsifiers

Fix any total correct deterministic Boolean compatibility decider A first. Use the transport model: one finite-alphabet writable tape, one local head, all source/work/cache/address cells charged, no external clock or source oracle, and fixed-origin output and termination convention. Write ell=ceil(log2 Q) for its Q>=2 states and g=ceil(log2 |Gamma|) for its alphabet. Physical CM sums origin-anchored occupied spans; minimum-description CM sums shortest complete-configuration descriptions conditional on A, without free input or time.

The exact original encoding remains unary n and delimiter, gamma(m+1), ordered signed triples, two n-bit assignments and a w-bit release identifier, where w=ceil(log2(n+1)) and

    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

The theorem concerns Boolean decision, not strict symmetric C, ordered R, S/Q or an exact count map.

For any finite family of actual UNSAT checkpoints C_v of A, suppose all share starting control and head h<=c for a fixed cut c. Define conflicts as in the prior report: {u,v} is an edge of G only when one orientation of their mixed left/right tape configuration, with the common control/head, is actually reachable on a valid SAT input. Full retained tapes, including relocated input and caches, enter this definition. Reachability is a premise, not a syntactic test.

Choose a public endpoint predicate: first occurrence after the start of the fixed pair (q_end,h_end), with h_end<=c. Require that every listed run reaches this endpoint before halting. Neither start is already an endpoint. This is a restricted checkpoint hypothesis, not a requirement imposed on all solvers. Let D_v be the endpoint configuration, Z_v the chronological crossing-state sequence during this finite phase, and R_v its entire endpoint tape strictly right of c, including blank positions and support. Let E(v) be exactly this phase's crossing transitions. Public B gives A, the finite family, cut, endpoint predicate, index order and distribution, but not the sampled index or its selected tape.

Four falsifiers: an unreachable opposite-label hybrid; an omitted retained cell or endpoint head/control field; an endpoint rule depending on hidden index or global elapsed time; or overlapping event sets charged with reuse one. These are explicitly excluded hypotheses, not inferred facts.

## Finite-phase splicing and decoder

**Lemma.** Every fiber of the pair (Z_v,R_v) is an independent set of G.

Suppose adjacent u,v have the same Z and R. Starting from the mixed configuration with left tape from C_u and right tape from C_v, alternate the actual donor excursions. Matching arrival states and local deterministic transitions preserve each donor half. The endpoint predicate is on the left, so its first occurrence is determined by the corresponding left excursion. Neither donor halts before that point. Equal complete phase sequences, starting and ending on the left, synchronize the number of right excursions. The mixed endpoint consequently has the left half of D_u and right half of D_v, with the common endpoint control and head. Equality R_u=R_v makes this exactly D_u.

If that orientation of the mixed start is reachable on a SAT input, correctness is contradicted: its continuation from D_u is UNSAT. The reverse orientation is handled by interchanging u and v. Thus the asserted fiber is independent. No synchronization of wall-clock times or forced revisiting of an original cut was used.

An actual external list decoder simulates A from every C_v until the specified endpoint, computes (Z_v,R_v), and lists the matching indices. It terminates by the endpoint premise. Its list size is at most alpha(G). It uses a public finite codebook, not a sampled source furnished for free to A. Its enumeration/simulation may be very expensive; no efficient solver or cheap algorithmic decoder is asserted. For alpha=1 it is an exact index decoder.

Choose a public integer W bounding how many cells from c+1 through the rightmost nonblank cell at any endpoint are needed; all later cells are blank. Encode R in gW fixed bits, explicitly including blanks. Let L=|E| and define

    Pi*=gamma(L+1) || ell-bit states in Z || gW endpoint bits.

Conditional on B this is prefix-free, with length ell L+h+gW, where h=2 floor(log2(L+1))+1. Directions alternate; cut and endpoint head are public, so no uncharged variable address field is omitted. The endpoint annotation is NOT data transferred by these crossing events. Its cost is a debit, not a new event.

Consequently

    ell E|E| >= H(U|B)-log2 alpha(G)-E[h]-gW.

A sharper information form is

    ell E|E| >= H(U|B)-log2 alpha(G)
                 -H(R|Z,B)-E[h].

Indeed H(U|Z,R,B)<=log alpha, so H(U|Z,B)<=H(R|Z,B)+log alpha. Subtract from H(U|B), and use I(U;Z|B)<=H(Z|B)<=E[ell L+h]. This proof also shows why simply asserting an exact decoder from Z is wrong. When alpha>1 the list index is further missing information and is not an actual event.

For a random public context apply each inequality conditionally and average its alpha and W terms. For multiple obligations on one distribution of original inputs and the SAME execution, with each transition in at most rho crossing sets,

    E[T] >= max(0,
      sum_j (H(U_j|B_j)-E[log2 alpha(G_j)]
             -H(R_j|Z_j,B_j)-E[h_j]) / (ell rho)).

Use the coarser g E[W_j] debit when only endpoint storage bounds are proved. Disjoint time phases have rho=1, but they still need new actual reachable families and the endpoint hypothesis. There is no telescoping cancellation of endpoint debits without a separate coupling theorem. This is the corrected short-phase implication, not a recurrence theorem.

## Exact counterexample to deleting the debit

Take the transport permutation inputs I_(pi,sigma)=L_pi M_r R_sigma, r>=3. They are UNSAT iff pi=sigma and SAT otherwise. Their exact counts are n=8r-1, m=10r, w=ceil(log2(8r)), and the N above, which is Theta(r log r). Choose any cut inside the public middle block.

Fix A to be the baseline globally correct authenticated permutation fast-path solver with exhaustive fallback, preceded by one extra origin transition. This transition leaves the scanned symbol unchanged, stays at the origin and changes a fresh START state to the original start state END. The model allows movement by at most one. END is the first phase endpoint. This fixed solver is total and correct on every valid input before choosing r or the distribution.

On all r! diagonal initial checkpoints, G is a clique: every unequal mixed input is a valid SAT input. Yet the one-transition phase crosses the cut zero times. Thus Z is constant and H(U|B,Z)=log2(r!) for a uniform diagonal index. A purported phase-only exact decoder would claim positive information from no observations, even though all opposite-label hybrids really are reachable.

The complete right endpoint tape still contains the distinct R_pi; hence H(R|Z,B)=log2(r!). The corrected net demand is zero before framing, exactly as required. This counterexample does not rely on an all-UNSAT correctness promise. It uses a globally correct solver and genuine SAT hybrid inputs. It isolates endpoint retention as the obstruction even BEFORE preprocessing or caching. More complicated paid prefixes can create the same issue.

The extra phase costs T=1, S=Theta(N), physical CM=Theta(N) under the span convention, and minimum-description CM<=O(N) separately. It supplies no lower bound on the latter. Following it, the original control algorithm retains O(N^2) total time, O(N) peak span and O(N^3) physical CM; replay gives the same descriptive upper order. Parsing/authentication and failed recognition are paid by that original solver. No input or reduction has changed. This is a symbolic counterexample for every r, not an extrapolation from a finite test.

## Current candidate, same-execution costs and open consequence

Discovery's 23:51 matching shortcut is compatible with the lemma. Its original code/raw, report and declared polynomial ledger were recovered at the revision above; the experiments were not rerun. On its admitted canonical degree sources it supplies a fixed O(N^4)-time, O(N)-span decision path, with separately O(N^5) physical/descriptive upper bounds. After paid erasure and normalization, all same-label READY configurations coincide. Their conflict graph has no edges, so alpha already removes the index demand. Before erasure the retained endpoint tape can instead account for unresolved index information. Neither circumstance forces repeated matching or residual-query service. This run does not independently certify the matching implementation or promote its class to general SAT.

All parsing, source authentication, discovery, rejected candidates, representations, adaptive switches, cache construction, copies, address manipulation, retained source, recomputation and output belong to the actual A execution. E selects real crossings from that execution. The proof does not make A physically write Pi*; endpoint serialization and decoding are external proof operations and their information is explicitly subtracted. A literal serialization could be produced by enumerating the public family and simulating the fixed machine, with no useful runtime guarantee. Thus there is no hidden claim of polynomial decoder overhead.

For a proposed fixed cap T<=K N^a, a>=1, the NET numerator, including endpoint debit and framing, must exceed ell rho K N^a to contradict the cap. S=O(N^a), physical CM=O(N^(2a)), and minimum-description CM=O(N^(a+1)) remain distinct ceilings. No new CM lower bound is obtained by multiplying unrelated time and space maxima. The O(N^a log N) count-map circuit ceiling has no decision consequence here. The static permutation demand ceilings N^2/8 and N^3/27 and its internally reviewed single-tape scope remain unchanged. Defeating one exponent would not exclude every fixed polynomial exponent.

The genuine unresolved premise is a family of later reachable conflicts with low endpoint conditional entropy, low ambiguity and bounded reuse, for every fixed solver under the tested cap. Equivalently, a constructive safe summary might eliminate the need for those conflicts; nothing here rules out a uniform polynomial algorithm. No all-input constructive coverage theorem is proved either.

## Sources, recovery and bounded search

The current directive, transport, AGENTS.md, CODEX.md, repository research skill and applicable T5 handoff definitions were recovered at the revision above, together with the latest Bounds report, its original audit/raw, local-obligation continuation, Discovery matching report/code/raw and issue 324. Own [prior report](PNP_Charged_bounds_2026-11-21_230700_Hybrid_Conflict_Code.md) already warned that complete-suffix records cannot simply be truncated. This run proves a sufficient endpoint condition and its exact entropy debit. No earlier experiment was repeated. The selected workspace is not a full checkout, so full-checkout preflight and manuscript compilation were not run. No historical TMR ownership is acquired.

Primary literature queries: “Hartmanis 1968 one tape Turing machine crossing sequences splicing computations pdf” and “one tape crossing sequence partial computation endpoint tape splicing lemma”. Read Hartmanis, *Computational Complexity of One-Tape Turing Machine Computations*, JACM 15(2), 1968, 325-339, original pp.326-327, crossing sequence definition and Lemma 1. Its local deterministic one-tape splicing mechanism is applicable; its regular-language and time theorems are not imported. The finite-phase endpoint statement above is proved here. [Primary paper](https://cse.iitkgp.ac.in/~goutam/toc/readingMaterial/computational-complexity-one-tape-Hart.pdf).

Fresh GitHub query '"crossing sequence" "Turing"' covered anthropics, openai, xai-org, google, google-research and google-deepmind. All returned no hits; xAI succeeded after a transient 429 retry. Two web fallback queries covered those six official namespaces and found no applicable official result. No external code or commit is imported. Official ownership references recovered in the immediately preceding project run are the verified Anthropic/OpenAI profiles, x.ai/news/grok-os, opensource.google/documentation/reference/github/where, research.google/resources, and deepmind.google/research/publications/22295. These are bounded negative searches, not absence claims.

Project query '"endpoint" "crossing" "phase"' returned the historical TWOWAY_CROSSING_TRADEOFF002 excerpt, which records entire writable configurations in a different multitape/read-only-input model, and an unrelated exponent-route report. Neither supplies the missing one-tape finite-phase decoder or licenses mixing models. The complete historical theorem was not imported.

DISJ/equality sanity PASS within the explicit permutation control. Same-execution DTISP and configuration consistency PASS for the conditional proof. Relativization remains a barrier to unrestricted promotion: arbitrary nonlocal oracle transitions do not obey this splicing rule. No Natural Proofs or algebrization bypass is claimed. Affine/Tseitin, complement, private-leaf, forced-domain, decision-witness, caching and relocation controls remain legal; no width or fixed-DAG necessity is inferred.

**One next dependency.** Accounting and Bounds should supply a concrete postpreprocessing reachable family whose endpoint conditional entropy is strictly smaller than its index demand after ambiguity/framing, on disjoint actual phases. Redteam should attack the endpoint stopping rule and the complete retained-right snapshot. Construction/Synthesis receive the exact debit before any renewed demand is summed. Independent review requested. Universal recurrence and P versus NP remain OPEN.

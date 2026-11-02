# LSPV-2 PAIRED-COFACTOR-CERTIFIED-EQ331

**2026-11-02 02:15 PST.** **PROVED/EXACT restricted corollary** of known pinned graph-factor algorithms; **COMPUTATIONAL** independent source/circuit verification; **P versus NP OPEN**.

## Exact obstruction and falsifiers

A short fan-in-two forward evaluator for a valid canonical Döcker monotone 3-SAT-(2,2) original F does not decide existential Circuit-SAT. Exact cofactor equivalence may be coNP-hard on arbitrary canonical sources, and no correct SAT decider is compelled to compute it. This run tests whether such equivalence can be **acquired and certified in polynomial work on a recognizable easy subfamily**. Falsified: (1) equal SAT labels imply future equivalence, (2) equal model counts imply future equivalence, (3) every semantic-equivalence comparison requires unrestricted Circuit-SAT. Invalid inference: this restricted tractability supplies arbitrary-decider hardness.

## All-canonical exact source clause-falsification theorem

Let p,q be coherent original-variable pins with the **same domain D**, and let Δ be the k original variables whose pinned values differ. Let Γ(Δ) contain source-clause IDs touching Δ. The exact (2+,2−) quota gives |Γ(Δ)| ≤ min(m,4k), with m=4n/3.

For each j∈Γ(Δ), define ρ(j,q) as the partial assignment that makes all unpinned literals of C_j false, unless a pinned literal already makes C_j true under q. Then

    exists z [F(p,z)=1 and F(q,z)=0]
       iff
    exists j∈Γ(Δ) with feasible ρ(j,q)
       and SAT(F restricted to p union ρ(j,q)).

The opposite direction swaps p,q. Consequently, semantic continuation equivalence reduces to at most 2 min(m,4k) original-source SAT subqueries. **For one changed original pin, at most two candidate clauses per direction and four total subqueries** suffice. This theorem holds for *every* valid canonical source, but does not render the subqueries polynomial generally. The proof is exact: any source clause false at q,z but true at p,z must contain a changed pinned variable; conversely, any source model under p and the q-falsity cube distinguishes the cofactors.

## Paid paired-NAE corollary

If every positive original clause has its exact negative counterpart, each pair enforces NAE on three original names. The known source-labelled (g,f)-factor / Tutte perfect-matching construction from BLOSSOM-FACTOR60 and GENERAL-PINNED-NAE-TUTTE330 solves **every coherent pinned restriction** with polynomial acquisition and a source-checked witness or an explicit local / Tutte odd-component UNSAT certificate. Applying it to each clause-falsity subquery makes exact pairwise continuation equivalence and directional implication polynomial **on this recognized subclass**. Full equality is certified by the complete set of refuted directional source-clause cubes. The matching and semantic acquisition are not free oracles. Nonpaired valid originals return UNRESOLVED under this terminal, not UNSAT.

## Independent, exact source controls

The no-producer-import verifier independently reproduced **all 729 coherent ternary Z6 original pin cubes**, **15,625 ordered same-domain pairs**, and the exact quotient: 729 source syntactic pin records, 344 pointwise continuation classes summed across domains, and only 94 current SAT-label classes. There are 5,893 equivalent ordered pairs, 9,025 same-label pairs, **3,132 false merges** if current-label equality is reused as future equivalence, and 6,600 opposite-label pairs. The experiment charged **470 unique pinned factor decisions**, **572 matching calls** including Tutte extraction, **26,292 tested directional source-clause false cubes**, 128,194 original clause-header visits and 150,000 source-index incidence reads across the 15,625 comparisons. The full two-scan loose upper bound would be 238,336 clause-header visits, before index reads.

On the **same canonical Z6 original**, x1=0 and x1=1 both admit nine source satisfying completions but have different future cofactors. The two configurations (x3,x4)=(0,1) and (1,0) have identical satisfiable continuation functions with two completions each; eight source-directed subquery branches carry valid UNSAT certificates. Pins (x4,x5,x6)=(0,0,0) versus (1,0,0) give source UNSAT0/SAT3 with a verified Tutte obstruction and satisfying assignment. The complete 8×8 syntactic, current-decision, exact-continuation and directional-implication matrices on domain {x4,x5,x6} are recorded in the raw reproducibility archive.

The independent verifier passed **15,625 full same-domain comparisons, 34,176 source-versus-circuit input rows, 2,167,936 fan-in-two gate events, nine separately reconstructed Tutte odd-component certificates, fourteen original-clause-indexed directional proof branches, 264 F9 SS/SU/US/UU modes, 6,144 F9 complement identities, and six malformed-source rejects**. K33's 512 pair comparisons are sampled, not exhaustive; its complete offline quotient count is 19,683/7,959/819 syntactic/continuation/current-decision states. All F9/Y6/F15 small forward evaluators were exhaustively checked; U198/V198 were sampled, and a fresh independent U198 UNSAT/V198 SAT proof replay checked 384 boundary cases and 19,488 DPLL nodes.

Direct original-CNF UP-DPLL vs noncanonical output-one Circuit-SAT on identical pins (literal inspections; compilation excluded): Z6 UNSAT 61/1,947, Z6 SAT 55/2,037, F9 SAT 74/7,922 and F9 UNSAT 56/7,629. The circuit is a forward evaluator, not a SAT decision procedure.

## Full resource firewall

The single-pair algorithm charges grammar and support pairing, 4n signed source-index construction, pin difference discovery, all changed-clause index/head reads, each candidate literal and pin check, each positive and failed matching/proof query, proof acquisition and independent source verification, cache/replay, strategy switching, child/output bit access, and any live ancestors and DELAY/COPY/RECOMP guest buffers in simultaneous peak writable space. Streaming one pair needs polynomial space; compiling **all** semantic quotient classes can remain exponential. Logical XOR is offline. Host counters are not native FLMV machine transitions.

**Prior art / duplication:** Döcker (2019); Tutte (1947); Edmonds (1965); Gaspers et al. (2014) on backdoors; the project's LSPV-1 DIRECTIONAL-COFACTOR-DOMINANCE320, LSPV-3 GATE317 and LSPV-2 TUTTE330 already contain the source-difference or matching ingredients. The scoped increment is their indexed **fully charged two-state semantic equivalence composition**, source-certified finite implementation, transfer matrices, and independent test. No universal polynomial-total-work adaptive controller, hereditary arbitrary-decider power-short A→Phi(A), or strict numerical SAME-MACHINE FLMV transfer is established. **P=NP and P≠NP remain OPEN.**

**Reproducibility:** Full self-contained producer, independent verifier, source fixtures, complete proof bundles, original-source circuit DAGs, raw JSON, LaTeX/BibTeX report, and SHA-256 manifest are retained in the run archive. Compact public code and summary below are limited substitutes, not the complete archive. Root main.tex is modified only if exact authenticated nonempty content and owned markers permit it.

References: https://arxiv.org/abs/1912.08032 ; https://ojs.aaai.org/index.php/AAAI/article/view/9111 ; https://doi.org/10.1145/1101821.1101822 ; https://github.com/j15marti/pnp/issues/3 .

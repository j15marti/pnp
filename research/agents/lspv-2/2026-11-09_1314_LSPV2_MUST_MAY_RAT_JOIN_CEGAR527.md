# LSPV-2/527: A cost-sound MUST/MAY abstract RAT transition and an exponentially branching spurious join
**2026-11-09 13:14 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected proof-chain node:** [P2-L2-527] (new, restricted evidence), refining [P2-L2-526], [P2-L2-524], [P2-L2-525]. **OPEN:** [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. No theorem about all SAT solvers or native R_mix341 is claimed.

## IDEA -> falsifiers -> SEARCH -> ITERATE
**Candidate:** An interval of current DRAT-minus clause databases, recording definitely present clauses M and possibly present clauses U, can safely OVERapproximate every RAT/RUP addition and deletion, even though RAT changes the satisfying assignments and deletion changes the RAT side-condition.

Falsifiers checked: (F1) a legal concrete RAT step fails the projected interval guard; (F2) an interval deletion loses a concrete successor; (F3) the coarse interval spuriously permits a candidate but the exact states actually permit it; (F4) the observed exponential number of branches forces exponential execution even when a compact correlation representation exists.

SEARCH: Buss–Thapen (LMCS 2021) distinguish DRAT-minus with deletion from RAT-minus without deletion and clarify satisfiability-preserving non-entailment moves [1]. DRAT-trim README, blob `eb6ffcc4`, authenticates external syntax but is not the historical R_mix341 grammar [2]. Chew–de Colnet–Slivovsky–Szeider (AAAI 2024) give exponential ordinary Resolution size for random reordered parity; Chew–Heule (SAT 2020) give short DRAT certificates [3,4]. D'Silva–Haller–Kroening (POPL 2013) and Giacobazzi–Ranzato–Scozzari (JACM 2000) guide overapproximation and completeness/refinement [5,6]. These are model controls, not an inferred unrestricted reduction.

Actual change from /526: instead of prohibiting non-RUP RAT transitions, the new abstract guard retains them soundly, allows true shortcuts and exposes one precise join-induced spurious path. The scope remains a distinct explicitly specified calculus.

## Exact restricted transition system and abstract domain
Fix a source-authenticated proper signed 3-CNF F on its original n variables, parsed from complete ASCII DIMACS bytes. A concrete database D is a finite set of clauses over those original variables. Initial D=F. Legal actions:
1. **DEL(D,C)** removes C, with zero paid *addition* records; separate record bytes and checker/machine work are not zero.
2. **RUP(D,C)** adds C if unit propagation on D plus the unit assumptions negating every literal of C conflicts.
3. **RAT(D,C,p)** for nonempty C and p the explicitly chosen first literal: for each D_i in D containing -p, the non-tautological resolvent (C\\{p}) union (D_i\\{-p}) is RUP in D. Add C if all succeed. RAT is satisfiability preserving, not necessarily consequence preserving. The empty-clause goal is permitted only by RUP.

There are no fresh variables, branching/split-discharge rules, GF(2) commands, native R_mix341 inference weights, or claims about a complete solver in this experimental calculus. Extension, algebra and arbitrary fallback are *excluded* and must not be silently subsumed into its lower bounds.

Abstract state I=(M,U), meaning M subseteq D subseteq U. A join uses M=intersection(M_i), U=union(U_i). After addition of C, both bounds gain C; after deletion both bounds lose C. Two abstract permission guards are:
$$
\\mathrm{mayRUP}(M,U;C) := \\mathrm{UPconflict}(U,\\neg C).
$$
$$
\\mathrm{mayRAT}(M,U;C,p) :=
\\bigwedge_{E\\in M:\\,-p\\in E}
\\left[
\\mathrm{taut}(\\mathrm{res}_p(C,E))
\\lor
\\mathrm{UPconflict}(U,\\neg\\mathrm{res}_p(C,E))
\\right].
$$
For the empty clause, use mayRUP, not RAT. The guards are *necessary*, not sufficient, for an actual step. This is intentional for a MAY abstraction.

**Theorem 527.1 (PROVED/RESTRICTED).** For EVERY concrete D with M subseteq D subseteq U, any legal concrete RUP step satisfies mayRUP, and any legal concrete RAT step satisfies mayRAT. The interval updates after addition/deletion and the intersection/union join contain all corresponding concrete successors. **Proof:** Unit-propagation contradiction is monotone under adding source clauses: D subseteq U. For RAT, every opposite-pivot clause E in M is present in concrete D, and every non-tautological resolvent against it is RUP under D, hence under U. Clauses in D\\M introduce no extra necessary constraints. Addition and deletion preserve the interval containments by set algebra. The same holds for arbitrary finite joins. Therefore all budget-bounded concrete proof-log paths stay represented if record-count budgets are carried monotonically; no claimed nonreachability may rely on rejection of a path by this abstraction without proving the abstract reachability invariant. This theorem does not lower-bound machine time or storage.

## Parameterized spurious low-cost RAT path
For any k>=1, use distinct original variables a,b_i,c_i,d_i and proper signed clauses:
$$
D_i=(\\neg a\\lor b_i\\lor c_i),\\quad
E_i^+=(a\\lor b_i\\lor d_i),\\quad
E_i^-=(\\neg d_i\\lor b_i\\lor c_i).
$$
Let F_k contain all 3k clauses. It has 3k+1 variables and is SAT (set all b_i=true). The proposed candidate is the original-variable unit C=(a).

**Legal shortcut control:** On full F_k, RAT(a) is valid. For each opposite-pivot D_i, assuming not b_i and not c_i yields not a from D_i, not d_i from E_i^-, and a from E_i^+; conflict. Yet RUP(F_k,a) is false. The live shortcut is NOT excluded.

**Restricted policy:** First delete EXACTLY ONE of E_i^+ and E_i^- for each i; no additions until these k deletions have occurred. The resulting concrete databases D_s are indexed by s in {0,1}^k, with D_i always present and exactly one E_i^+/E_i^- retained. Under assumptions not b_i, not c_i, the remaining one-sided gadget cannot generate a contradiction by unit propagation. Clauses in other gadgets do not complete the missing propagation. Therefore RAT(D_s,a) is FALSE for ALL 2^k concrete branches.

Their single coarse join is
$$
M=\\{D_i:1\\le i\\le k\\},\\qquad
U=F_k.
$$
The abstract mayRAT guard is TRUE, because U contains BOTH E_i variants. Thus the joined abstract state admits one spurious low-cost RAT(a) addition although no concrete state does. A precise CEGAR replay on each D_s rejects it. Splitting into exact singleton interval states eliminates the false transition while retaining the genuine pre-deletion RAT shortcut.

**Theorem 527.2 (PROVED/RESTRICTED).** This is a parameterized spurious MAY path after the specified k-deletion policy for every k. It demonstrates insufficiency of the coarse join, **not** a lower bound for unrestricted DRAT or SAT. The 2^k concrete branches possess a compact O(k)-bit correlation invariant: each pair (E_i^+,E_i^-) has exactly one present member. Thus no inference from exponentially many concrete states to exponential memory/time is permitted.

## Reproducible verification and resource accounting
Primary Node.js original-source test: `20,051` assertion groups, 198,002 scans and 8,029 unit assignments in its explicit UP implementation, 7 malformed-source rejections. For k=1..8 it enumerated 510 exact post-deletion states, verified that none allows RAT(a), the coarse MAY guard allows it, an exact refined interval rejects it, and the full source genuinely permits RAT(a). Original-source SHA256 hashes were computed for all eight parameter sizes. A separately authored Python oracle checked `19,044` small interval/candidate cases, `126,796` individual assertions, all soundness coverage tests passing. An additional independent JavaScript checker (published) passed `804` assertion groups for k=1..7, covering 254 concrete post-deletion states, malformed rejection and CEGAR replay. These test counts are not same-FLMV-machine bit-cost or peak-space upper bounds. Relevant exact local files are in the reproducibility ZIP. Independently authenticated CHECKER CLASS is **experimental DRAT-minus**, NOT R_mix341.

Logical post-policy budget: k deletion records then one proposed RAT addition; vector (#deletions,#additions)=(k,1). The spurious path is impossible under the policy, and real full-source RAT(a) at one addition is retained. Physical lower bounds on parsing, source/index reads, UP scans, clause references, deletion records, joins, cache retention, recomputation and peak simultaneous memory have not been derived. The enumerator uses O(k2^k) host operations to replay all states; the compact O(k)-bit correlation representation invalidates any assertion that this cost is unavoidable.

## Corpus and continuity
Read the 2026-11-09 abstract-negative five-role handoff (Git blob 8a6fd9f5), both complete root trackers (proof1 blob 96aefb3d; proof2 prewrite blob 3298a3fc), issue #3 and latest comments, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; actual /526, LSPV-5/467 sponsor-flow report, Grok 2026-11-09_2015_PROGRESS, Claude WORLD-LEDGER-0001 and MODELBRIDGE-0010. Change-aware checks: konard/p-vs-np README 0e0ec77f, scripts/proof_status.json 93b77ed3; blkph0x/p-vs-np-proof-research README f397a774, METHOD_INDEX 18d693ea; openai/math README cc5b0a03; meelgroup/frat-xor README 38a137bc; DRAT-trim README eb6ffcc4. Original repository code was inspected, not equated to this project's checker. No Google-specific direct index access was claimed: web literature searches were used.

The published code is `experiments/arc/lspv2_527_must_may_rat_independent.mjs`, results `results/raw/arc/2026-11-09_1314_LSPV2_527_MUST_MAY_RAT_RAW.json`, handoff `research/coordination/2026-11-09_1314_LSPV2_MUST_MAY_RAT_FIVE_ROLE_HANDOFF527.md`. See ZIP for primary Node.js/Python scripts and complete raw output.

## Implication and remaining gap
The MAY RAT guard is safe for budgeted *proof-log* abstraction; interval joins require correlation-sensitive refinement to remove spurious candidates. Neither theorem constructs a SAT decider, proves original-source proof-work superpolynomial growth, quantifies over all adaptive solvers or supplies any recursively iterable same-machine FLMV contraction. [P2-A2], [P2-A4], [P2-A5], R_mix341 [P2-D1]/[P2-C3] and noncircular [P2-B1]/[P2-B2] remain OPEN. **P versus NP remains OPEN.**

## References
[1] Buss S, Thapen N. DRAT and Propagation Redundancy Proofs Without New Variables. LMCS 17(2), 2021. https://lmcs.episciences.org/7400
[2] marijnheule/drat-trim, README.md, blob eb6ffcc4, https://github.com/marijnheule/drat-trim
[3] Chew L et al. Hardness of Random Reordered Encodings of Parity for Resolution and CDCL. AAAI 2024. https://arxiv.org/abs/2402.00542
[4] Chew L, Heule MJH. Sorting Parity Encodings by Reusing Variables. SAT 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7326471/
[5] D'Silva V, Haller L, Kroening D. Abstract Conflict Driven Learning. POPL 2013. https://ora.ox.ac.uk/objects/uuid:6102a023-3bb9-4e17-aee4-505cd29b4524
[6] Giacobazzi R, Ranzato F, Scozzari F. Making Abstract Interpretations Complete. JACM 47(2), 2000. https://experts.arizona.edu/en/publications/making-abstract-interpretations-complete/

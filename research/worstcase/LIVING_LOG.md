# Worst-case derivation-cost programme: living log

Shared objective (user directive, scheduled prompt):
W̄_R(N) = max over UNSAT F with |<F>| <= N of min over refutations pi of F in R of cost_R(pi);
target bridge  B(R):  SAT in P  =>  W̄_R(N) <= poly(N).
Status of everything below: P vs NP remains OPEN. No lower bound on W̄_R and no bridge B(R) is proved here.
Entries are append-only; newest last. Status labels: PROVED/EXACT, KNOWN THEOREM, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

---

## Entry 1: 2026-11-10 (scheduled run, single session covering the five roles)

### Corpus reviewed
AGENTS.md; GROKPROOF/README + 2026-11-10_1221 note; repo tree; grep for prior "worst-case derivation"/W̄_R work
(only LSPV-1/5 restricted-fragment reports and PROOF2 outbox items surfaced; no prior file states this exact B(R) programme,
so this log opens it). Root main.tex and LSPV ownership regions were NOT edited (this run is outside the LSPV roles).

### 1. Free strategy search is harmless, and W̄_R is a Cook–Reckhow measure  [PROVED/EXACT, folklore]
If cost_R is polynomially equivalent to proof size (true for tree/DAG size in Resolution, Frege, eFrege, PC, CP, ...),
then min_pi cost_R(pi) is exactly the shortest-refutation size, and "W̄_R poly" means exactly "R is polynomially bounded".
Granting the optimal sequence for free loses nothing for a lower bound. But it also fixes the logical type of the target:
W̄_R <= poly is a statement that UNSAT has short R-certificates, i.e. an NP-vs-coNP statement, not a deterministic-time one.
(Cook–Reckhow 1979: NP = coNP iff some proof system is polynomially bounded.)
With the time–space cost (peak memory) the same holds for the pair (size, clause/variable space); pebbling-formula
correspondence (Nordström, LMCS 2013, arXiv 1307.3913) gives the model for charging space and the known size–space tradeoffs.

### 2. The bridge is vacuous-equivalent to P != NP once a lower bound is granted  [PROVED/EXACT, new bookkeeping lemma]
Lemma 1. For any fixed R, B(R) <=> (SAT not in P) or (R is poly-bounded).
Proof. B(R) is the implication A => C with A = "SAT in P", C = "R poly-bounded"; material implication. QED.
Corollary 1. If W̄_R is superpolynomial (LB(R)), then B(R) <=> SAT not in P. So "prove LB(R) and B(R)" is not two
independent halves: the second half is *exactly* P != NP. Conversely B(R) alone is implied by P != NP.
Consequence: a bridge can only count as progress if it is proved by a *simulation* argument that does not pass through
the truth value of A (i.e. a uniform transfer: any poly-time SAT decider yields short R-derivations). Anything shaped
"assume the lower bound, deduce hardness" is circular. [This is the status test every candidate bridge must pass.]

### 3. What a genuine (non-circular) bridge must contain  [KNOWN THEOREM / CONDITIONAL, from literature]
A uniform bridge says: from any correct poly-time decider M for SAT one extracts poly-size R-refutations. Since M's
correctness is itself the statement "forall F: M(F)=1 => F satisfiable" (a coNP-type, tautology-family statement),
R must have poly-size proofs of the reflection/correctness tautologies of M. Standard facts to build on:
- If a theory (PV / S^1_2) proves M correct, translation gives poly-size eFrege proofs of the n-instances (Cook; Krajíček).
  CONDITIONAL on provability; unconditional provability is not known and is not implied by M merely being correct.
- The existence of an *optimal* proof system (one that p-simulates all) would give B(R) for that R, because under
  P = NP the machine-trace system is poly-bounded and R would simulate it. Existence of an optimal system is OPEN
  (Krajíček–Pudlák 1989 give it under NE = coNE); Frege/eFrege are not known to be optimal (Cook–Reckhow survey,
  arXiv 1909.03691 "The Cook-Reckhow definition").
- A 2025 arXiv paper ("The Proof Analysis Problem", arXiv 2506.16956) is reported to show: if P = NP then a
  polynomially bounded and p-optimal system exists. That is consistent with Lemma 1 but its Q* is defined *by cases on the
  truth of P = NP*, so it is not an explicit fixed R with B(R) proved. [Reported by search snippet; full text NOT yet read by
  this run. Verify before citing as a load-bearing fact.]
Net: B(R) for an explicit, hand-built R (resolution+XOR+DAG sharing+..., e.g. the repository's R_mix341) is equivalent
to a new optimality/reflection theorem for R. For the weak systems the project can actually analyse (Res, PC, CP, mixed
clause/XOR) B(R) is *false-looking*: those systems have known superpoly lower bounds yet P = NP is not refuted, so for them
B(R) is just P != NP in disguise (Corollary 1) — no route to it except through the open optimality problem.

### 4. Where the programme can still make unconditional progress  [CANDIDATE]
(a) Keep LB(R) work as *restricted-model evidence* (lower bounds for R of increasing strength), labelled as not implying
    SAT not in P, per Lemma 1.
(b) Replace the global bridge by a *restricted* one that is provable: for a restricted decider class D (e.g. DPLL/CDCL-with-
    learning, algebraic, bounded-width), prove "D decides SAT in poly time => R_D poly-bounded" by explicit trace-to-proof
    translation. These are the genuine Cook–Reckhow-style simulations (CDCL <-> Res, Pipatsrisawat–Darwiche / Atserias–Fichte–
    Thurley). They give lower bounds against D, not against arbitrary algorithms.
(c) Target the weakest hypothesis that is not circular: "eFrege/R proves Ref_M for every correct poly-time M"
    (an optimality-for-P statement). Record it as the single candidate bridge BR-OPT; falsification-first test: find a
    relativized world with P = NP where R is not poly-bounded (an oracle separation would show BR-OPT is non-relativizing-
    provable, hence needs new techniques). Egidy–Glaßer (STOC 2025, arXiv 2602.02294 follow-up) oracle constructions for
    optimal systems are the starting literature. OPEN.
(d) Space/time: use pebbling-formula correspondence to ask whether the *space* component of cost_R yields a bridge
    through Williams-type time–space SAT bounds (ARC/FLMV spine); the corpus's existing Buss–Williams barrier (ledger row L13)
    applies. OPEN, to be assigned.

### 5. Role assignments for next runs (suggested, additive)
- Lower-Bound Lead: formalize Lemma 1 / Corollary 1 as the circularity test in main-tex-facing language; state BR-OPT precisely.
- Reduction Builder: certify shortest-derivation DAGs for the fixed combined system on small instances; extract exact W̄_R(N) for tiny N
  by exhaustive search as COMPUTATIONAL data (not a bound).
- Hypergraph/Certificates: hard UNSAT families, check survival against Res/PC/CP/mixed sharing.
- Resource Auditor: audit cost_R definition for (size, space) and verify polynomial equivalence to proof size.
- Red Team: attack Lemma 1 usage (any claimed bridge that implicitly assumes the lower bound), and attack Section 3 claims against full texts.

### Literature checked this run
Cook–Reckhow definition survey (arXiv 1909.03691); Proof Analysis Problem (arXiv 2506.16956, snippet only); Egidy–Glaßer
(arXiv 2602.02294, snippet only); Nordström pebble games survey (arXiv 1307.3913). No result found that proves a lower bound
for W̄_R against a strong fixed system or an unconditional bridge. Nothing in the literature checked changes the status: OPEN.

### Status
P versus NP remains OPEN. Load-bearing open arrows: (i) superpolynomial LB(R) for a sufficiently strong fixed R;
(ii) a non-circular bridge B(R) (equivalent to optimality/reflection for R). One OPEN arrow suffices: P != NP is not proved.

% END_OF_ENTRY::WORSTCASE-LOG::2026-11-10-1

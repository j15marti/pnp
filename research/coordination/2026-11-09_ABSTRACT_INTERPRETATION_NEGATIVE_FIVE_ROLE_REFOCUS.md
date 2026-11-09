# Abstract interpretation for negative proofs: five-role research refocus

Date: 2026-11-09, America/Los_Angeles (PST).
Authority: the user's request to search the literature and redirect all five existing research agents toward using abstract interpretation to prove a negative.
Status: research directive and standard conditional proof schemas; the project-specific lower-bound applications are CANDIDATE/OPEN. This document does not prove P != NP or promote any tracker node.

## 1. Priority and continuity

Make cost-sound abstract interpretation the common PRIMARY methodology across the five existing agents. Preserve LSPV-2 and LSPV-4 as Route A and LSPV-1, LSPV-3 and LSPV-5 as Route B. This methodological refocus supersedes conflicting older topic priorities, including continuing knot-specific or guest-cutoff calculations merely because they were the previous experiment. Reuse those results when they directly test the new abstraction. Preserve all verified mathematics, exact historical R_mix341 rules and weights, proof-status safeguards, ownership, identities, titles, schedules, time zones and enabled states. Create no new agents and reactivate no dormant agents.

The principal negative target is: no legal source-authenticated refutation of an established UNSAT family has cost at most B(n), with B growing superpolynomially in the original encoded input length. A second, separately scoped target is an impossibility or time-space lower bound for a precisely specified class of abstract SAT procedures. Neither target automatically quantifies over every SAT algorithm.

Do not turn this project into an indefinite catalog of weaknesses of individual abstractions. Seek a parameterized invariant, a cost-preserving simulation, a reusable completeness/refinement obstruction, or an explicit legal shortcut that materially changes the candidate theorem. Begin with established families and known shortcuts, not a new supposed hard distribution.

## 2. Distinguish two uses of abstraction

(A) ABSTRACT SOLVER: an abstraction of assignments or solver states may fail to establish UNSAT. That alone is an inconclusive analysis, not a proof that the formula lacks a short refutation or that every algorithm is slow.

(B) ABSTRACT ALL LOW-COST PROOF CONSTRUCTIONS: represent every legal way of building a proof within a resource budget. Soundly overapproximate this transition system. If even the overapproximation cannot reach a completed refutation within budget, the concrete system cannot do so. This is the preferred direct negative-proof architecture.

Overapproximation adds possible behaviors; it must not silently remove legal shortcuts. Missing historical rule semantics must be authenticated or conservatively overapproximated. An abstraction of a convenient subcalculus is a result about that subcalculus only.

## 3. Budgeted nonreachability schema

Fix a fully specified calculus R and original formula F. A concrete configuration records the partial shared proof DAG, original-source identities, active assumptions, auxiliary definitions and freshness, available conclusions, paid-node identities and cumulative cost. A transition adds any legal inference or performs another explicitly permitted action. A complete finite acyclic proof can be constructed in topological order. Charge a distinct inference once; using a previously available node does not pay for its derivation again. Reference costs, if any, remain exactly those of R.

Let I be the initial configuration set, G the completed-refutation configurations and Post_B the transition relation restricted to cumulative cost at most B. Let gamma map an abstract element to represented concrete configurations. Require a monotone abstract transformer with

$$
\operatorname{Post}_B(\gamma(a))\subseteq\gamma(\operatorname{Post}^{\#}_B(a)).
$$

Find an independently justified abstract invariant a_* satisfying

$$
I\subseteq\gamma(a_*),\qquad
\operatorname{Post}^{\#}_B(a_*)\sqsubseteq a_*,\qquad
\gamma(a_*)\cap G=\varnothing.
$$

Induction on concrete transitions then excludes every refutation of cost at most B. With an attained discrete minimum this gives W_R(F)>B; if using an infimum, state the strictness qualification accurately. Soundness is sufficient for this inference. Complete abstraction is not required, although precision is necessary to obtain useful certificates.

The invariant cannot be defined circularly as 'all states lacking a cheap refutation' without an independent construction or proof. Goal exclusion and transition soundness must be proved from explicit syntax/semantics, not a hidden SAT, equivalence or shortest-proof oracle. Zero-cost transitions and closures need sound treatment; budget is not automatically a bound on the number of transitions. Do not silently bound auxiliary counts, identifiers, rule arity, widths or intermediate encodings.

Equivalent weighted-relaxation formulation: every concrete proof-construction path maps to an abstract path with no greater total cost and every concrete goal maps to an abstract goal. Then

$$
d^{\#}(\alpha(s_F),G^{\#})\le W_R(F).
$$

Proving a large abstract distance gives a lower bound. Restricting to a fixed proof-search policy gives the opposite danger: it may exclude a cheaper legal proof.

## 4. Cost potentials and shared work

A candidate potential V on complete configurations can certify a lower bound if V(s_F)=0, every goal has V>=H(F), and every legal transition e:s->s' obeys

$$
V(s')-V(s)\le w(e).
$$

Telescoping gives total cost at least H(F). The difficulty is finding a noncircular potential that survives all rules, not the telescoping algebra. A potential over a single branch or formula description is insufficient unless its correspondence to whole shared configurations is proved.

Investigate cost partitioning from abstraction-based planning. If abstractions i receive nonnegative transition charges c_i(e) with

$$
\sum_i c_i(e)\le w(e),
$$

and each component lower-bounds the cost of the projected concrete path, their bounds can be added without double-counting. Prove the path/configuration mapping, particularly for shared lemmas and branch joins. Independent per-goal minima cannot simply be summed.

Keep ideal logical proof cost, actual sequential time, evidence bits, parallel span and peak space distinct. A mathematical lower-bound certificate may be expensive to discover; this does not invalidate it. Any claimed implemented algorithm or uniform compiler must charge discovery and all other phases.

## 5. Counterexample-guided refinement

Adapt CEGAR to cheap proof paths. When a coarse abstraction admits a low-cost refutation, attempt original-source-authenticated concrete replay. A real legal cheap proof falsifies the proposed lower bound. A spurious path identifies a lost constraint, such as context compatibility, global wire freshness, source identity, dependency, or cost accounting; refine that constraint and prove the revised transformer sound. An infinite or unsuccessful refinement search establishes no lower bound by itself.

Use reduced products of complementary domains only with an explicit sound reduction operator. Candidate components include clause/width information, exact affine GF(2) relations, source-provenance sets, active contexts, interface dependencies, and paid-node/cost summaries. An affine component must expose the easy Tseitin parity shortcut rather than hide it. A complicated or high-rank semantic domain is not itself a computational lower bound.

## 6. Literature with exact intended uses

[1] Cousot P, Cousot R. Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints. POPL 1977, pp.238-252. Author source: https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml . Foundation for sound fixed-point overapproximation. The application to all budget-bounded proof configurations still needs explicit project semantics.

[2] D'Silva V, Haller L, Kroening D. Abstract Conflict Driven Learning. POPL 2013. https://www.kroening.com/papers/popl2013.pdf . Generalizes CDCL through lattice-based over- and underapproximation. Learning and implicit treatment of disjunction are essential controls, not optional shortcuts to omit.

[3] D'Silva V, Haller L, Kroening D. Abstract Satisfaction. POPL 2014, pp.139-150. DOI 10.1145/2535838.2535868. https://www.kroening.com/papers/popl2014.pdf . Deduction, abduction, quantification and fixed-point semantics for a broad collection of SAT/SMT procedures. It does not assert that every polynomial SAT algorithm belongs to one bounded abstract-domain architecture.

[4] Giacobazzi R, Ranzato F, Scozzari F. Making Abstract Interpretations Complete. JACM 47(2):361-416, 2000. https://www.math.unipd.it/~ranzato/papers/jacm00.pdf . Complete shells/cores under stated continuity hypotheses. Least complete refinements do not exist under every formulation, especially general fixpoint completeness. Seek a precise refinement/precision obstruction for a fixed operator family; do not assume universal existence or equate domain cardinality with representation cost.

[5] Clarke E, Grumberg O, Jha S, Lu Y, Veith H. Counterexample-Guided Abstraction Refinement for Symbolic Model Checking. JACM 50(5):752-794, 2003. https://www.cs.cmu.edu/~emc/papers/Papers%20In%20Refereed%20Journals/Counterexample-guided%20abstraction%20refinement.pdf . Use concrete replay of apparent cheap proofs to guide refinement. This proposed proof-cost application is not a theorem already supplied by the paper.

[6] Keller T, Pommerening F, Seipp J, Geisser F, Mattmuller R. State-Dependent Cost Partitionings for Cartesian Abstractions in Classical Planning. IJCAI 2016, pp.3161-3168. https://ijcai.org/proceedings/2016/448 ; PDF https://ijcai.org/proceedings/2016/0448.pdf . Abstraction distances and cost partitioning provide admissible lower estimates in weighted transition systems. Transfer requires representing full proof configurations, not treating a shared AND/OR DAG as a tree.

[7] Atserias A, Dalmau V. A Combinatorial Characterization of Resolution Width. CCC 2003; final JCSS 74(3):323-334, 2008. Author conference version: https://www.cs.upc.edu/~atserias/papers/width/ccc03.pdf . Existential pebble-game characterization supplies a rigorous restricted negative-proof baseline. State exact width/game parameters from the paper. It is not already a mixed-calculus or all-machine theorem.

[8] Ben-Sasson E, Wigderson A. Short Proofs Are Narrow: Resolution Made Simple. JACM 48(2):149-169, 2001. https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf . Use the precisely parameterized Resolution width-size theorem as an initial baseline, then test what changes under stronger legal rules.

[9] Henry J, Monniaux D, Moy M. Succinct Representations for Abstract Interpretation. 2012. https://arxiv.org/abs/1206.4234 . Symbolically represented path families warn against turning exponentially many abstract states, disjuncts or paths into an unavoidable runtime or storage claim.

Primary paper text and representative PDF pages for [2]-[8] were inspected for this literature-to-method handoff. [1] was read on its authors' publication page and [9] in available full text. An additional 2026 preprint, D'Silva et al., A proof-theoretic approach to abstract interpretation, arXiv:2605.26591, was available only at abstract level; it is not a load-bearing source here.

## 7. Role-specific work and first deliverables

LSPV-1, Lead, Route B: formalize the budgeted abstract-proof semantics, quantifiers and simulation direction. Produce one candidate family-level invariant/potential or a precise legal counterexample to it. Keep the same-R computational bridge separate. Examine a fixed-r quasipolynomial bridge as an optional sufficient target, not an established consequence of soundness. Coordinate one common domain/interface with LSPV-3 and LSPV-5.

LSPV-2, Builder, Route A: implement a minimal reproducible abstract-satisfaction/ACDCL or cost-annotated solver-transition prototype covering an explicitly specified algorithm class. Test a parameterized abstraction/refinement obstruction or an adaptive decomposition construction. Map its result to the universal same-machine transformation obligations rather than assuming all SAT algorithms are ACDCL. First deliverable: exact concrete/abstract transition correspondence, both-label controls, and at least one replayable real/spurious cheap path or symbolic class-relative theorem.

LSPV-3, Hypergraph and Certificates, Route B: construct source-authenticated abstract transformers for every authenticated native rule, including assumptions, sharing, GF(2), AND3, definitions and LOCAL-CONVERT. Prove soundness rule by rule and expose unknown historical grammar instead of silently excluding it. First deliverable: a checker-readable inductive-invariant certificate or a minimal legal transition that defeats the proposed invariant, including reconvergent and incompatible-branch controls.

LSPV-4, Resource Auditor, Route A: develop independent cost-partitioned potentials and native-machine resource annotations. Audit all-phase bit-time/space, acquisition, lookup, caches, replay, retention/recomputation, zero-cost closures and input/output. First deliverable: a cost-nonexpanding simulation theorem for one stated interface, or a concrete cost counterexample, with all resource quantities matched to the same realization. Do not count representation cardinality as physical cost.

LSPV-5, Red Team, Route B: independently attack the orientation and universal coverage of the abstraction, legal shortcut coverage, goal exclusion, inferred computational bridge and completeness assumptions. Replay LSPV-1/3 certificates or independently reimplement with explicit trust boundary. First deliverable: a minimal actual shortcut/spurious-path diagnosis or independent validation of a parameterized lemma, not only generic warnings.

## 8. Staged acceptance criteria

Stage I: reproduce a published restricted lower-bound mechanism, such as Resolution width/game reasoning, with explicit source encodings and known easy controls. This is validation, not novelty.
Stage II: admit the actual mixed rules, allowing known algebraic and extension shortcuts. Prove soundness for all transitions. Identify exactly why the old invariant survives or fails.
Stage III: obtain a nontrivial parameterized full-calculus lower bound beyond an already-known indispensable-source counting result. Finite minimum-cost checks support a theorem but do not establish its asymptotics.
Stage IV: prove a separate computational transfer or direct all-decider machine theorem. Without it, report a proof-system or algorithm-class lower bound, not unrestricted SAT time.

The exact desired general decision claim is that every fixed uniform total correct SAT decider fails every fixed polynomial worst-case bound. Keep the quantifier order explicit. A single fast recognizer for one hard-in-Resolution family need not be a fast worst-case SAT algorithm; conversely, that family's restricted proof hardness cannot be declared arbitrary-machine hardness.

## 9. Preserved mathematical contracts

R is fixed before inputs and sizes. W_R(F) minimizes the nonnegative weights of distinct paid nodes over ALL legal source-authenticated branching/shared refutation DAGs. Wbar_R(N) is the worst such minimum over valid UNSAT binary sources of length at most N. Free optimal proof choice is intentional. Actual algorithms pay construction, failed search, verification, source/index reads, references, caches, output and simultaneous peak space.

Retain B1 pointwise proof-to-time, B2 cumulative worst-case proof-to-time and B3 SAT-in-P implies polynomial Wbar_R for the SAME calculus as distinct implications. Neither soundness, completeness, a proof checker, nor existence of some other proof system proves B3. A candidate bridge Wbar_R(N)<=exp(C_A*(log(N+T_A^wc(N)+2))^r), fixed finite r, remains OPEN; coupled to a suitable same-system exponential proof lower bound it would imply a superpolynomial runtime lower bound. Do not assume either premise.

Route A still requires every total correct polynomial SAT decider, unknown finite exponents, all SAT/UNSAT/malformed inputs, recursive applicability and the same FLMV machine. Preserve the candidate inequalities t'<=max(11/10,3/5+t/2) and s'<=max(1/2,s/2), including all-phase s'<=max(rho,eta,lambda,lambda*s), without assuming their realization. Do not use the retired unrestricted cosine endpoint or cross-machine resource borrowing. A time-only guest bound does not imply polynomial space; state guest space separately. Guest algorithm upper bounds remain conditional unless independently justified and never become lower bounds by optimizing an upper estimate.

P2-D1, P2-C3, P2-B1, P2-B2, P2-A2, P2-A4, P2-A5 and the P=NP algorithm nodes remain OPEN unless actual evidence closes their complete obligations.

## 10. Mandatory workflow, publication and continuity

Every run read BOTH proof1.txt and proof2.txt, this handoff, current issue #3, governing repository instructions and materially relevant original peer/Grok/Claude artifacts. Survey current state and search historical duplication; do not assume local scratch survives. The prior report research/review/reports/model_bridge/2026-10-11_1155_MODELBRIDGE-0010.tex already identifies all-program normalization and reachability obstacles. This new focus is not permission to repeat a retired generic compiler argument. No claim that every corpus file or local preflight script was executed is made by this handoff.

Before searching, state one precise candidate and 2-4 falsifiers. Search primary literature and relevant GitHub implementations, inspect actual statements/assumptions, then construct, prove, falsify or independently verify something substantive. Distinguish directly transferable theorems from candidate mappings. Do not treat paper titles, abstracts, repository badges, admitted formal theorems, or finite tests as proof of the target.

Continue targeted or change-aware review of konard/p-vs-np and blkph0x/p-vs-np-proof-research as hypothesis/critique sources, not authorities. Retain relevant rotating coverage of meelgroup/frat-xor, tanyongkiam/cake_lpr, CakeML/cakeml, peitl/short-proof, marijnheule/drat-trim, digama0/frat, pysathq/pysat, arminbiere/cadical, arminbiere/kissat, msoos/cryptominisat, MassimoLauria/cnfgen, uds-psl/coq-library-complexity, uds-psl/cook-levin, cslib-community/complexitylib, leanprover/lean4 and current LeanSAT successors, berkeley-abc/abc, lsils/mockturtle, kbr-/math-research, openai/math and anthropics/formal-math. Document unavailable searches rather than claiming access.

Hostile controls include Horn/2SAT, parity/Tseitin with Gaussian elimination, bounded-width dynamic programming, renaming/padding, auxiliary definitions, shared reconvergence, incompatible assumptions, tiny UNSAT cores, sparse versus dense and lazy representations, malformed/corrupt inputs and certificates, and DEAD/COPY/DELAY/INTERP/RECOMP wrappers where relevant. Never label small finite graphs certified expander-hard without the actual family theorem.

Publish dated role-owned report, reproducible code/raw results and a concise handoff. Read current complete tracker content and SHA before any change, preserve other entries, merge conflicts and verify full readback. Update trackers only for material status/dependency/evidence/gap changes; otherwise write TRACKERS REVIEWED; NO MATERIAL CHANGE in the report. Post exact affected IDs to issue #3. Preserve root main.tex ownership; never overwrite a partial/unreadable root or tracker. If publication fails, preserve a durable exact artifact and state the limitation.

Use Pacific timestamps. Use $...$ and $$...$$ in Markdown files and simple ordinary LaTeX in chat. Keep exact proof statuses. End research reports with actual advance, validation, publication status and precise remaining gap. No P-versus-NP resolution is claimed by this refocus.

<!-- END ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS 2026-11-09 -->

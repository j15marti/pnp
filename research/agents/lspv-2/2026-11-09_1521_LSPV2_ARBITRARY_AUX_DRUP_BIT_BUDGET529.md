# LSPV-2/529: Cost-sound bit-budget lower bound for deletion-enabled auxiliary-variable RUP logs

**2026-11-09 15:21 PST | LSPV-2 Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected:** new evidence [P2-L2-529], extending [P2-L2-524] and [P2-L2-525], challenging the restrictive original-variable assumption. Still OPEN [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. The historical R_mix341 rule grammar and weights are unchanged.

## IDEA, falsifiers, SEARCH and actual iteration

**Initial candidate.** A total *proof-bit* budget, rather than the original source variable count, can make the prior RUP-to-Resolution abstract simulation cost-sound even when proofs contain arbitrary **fresh variable names**, wide learned clauses, repeated shared lemmas, restarts and deletion records. There is no bound on the magnitude of an auxiliary identifier except its explicit encoding bits.

F1: a legal non-tautological RUP addition needs more than one binary Resolution node per variable appearing anywhere in the authenticated source/proof. F2: retaining all deleted clauses invalidates some later RUP check. F3: weakening elimination fails for shared/reconvergent Resolution DAGs. F4: RAT, GF(2), extension definitions or a solver's unlogged UNSAT test silently enter the claimed proof class. F1-F3 are resolved for the precisely declared class below by an explicit structural proof, based on the predecessor /524; F4 is a **hard class boundary**, with a genuine RAT counter-control reproduced.

Read the November 9 five-role abstract-negative handoff (blob 8a6fd9f5), both current root trackers, issue #3 including latest peer comments, AGENTS.md, CODEX.md, the project research skill, original LSPV-2/524-/525-/527-/528 reports, LSPV-5/469, Grok GROKPROOF/2026-11-09_2015_PROGRESS.md and Claude WORLD-LEDGER-0001, plus MODELBRIDGE-0010. The former restricted /524 bound assumed v source variables; /525 allowed deletion and sharing but still no new variables. This run removes that restriction **only for the RUP-only certificate class**, by paying for the entire written proof.

Primary source inspected: Ben-Sasson–Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 2001, Definition 4.1 and Theorem 4.4/Corollary 4.5 (Urquhart attribution), including the actual theorem page in the paper. DRAT-trim README explicitly bans tautological and repeated-literal clauses, describes RUP via UP and permits deletions. D'Silva–Haller–Kroening, *Abstract Conflict Driven Learning*, POPL 2013, supplies methodology, not an all-decider theorem. The Giacobazzi–Ranzato–Scozzari complete-shell and CEGAR literature remains methodological context. Change-aware actual-file reads: konard/p-vs-np scripts/proof_status.json (blob 93b77ed3); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (blob 18d693ea); marijnheule/drat-trim README.md (blob eb6ffcc4); MassimoLauria/cnfgen cnfgen/families/tseitin.py (blob 4bb5fd19); openai/math README.md (blob cc5b0a03). None establishes the universal SAT decider-to-FLMV transformation. Web primary search was performed; no standalone Google indexing service or native DRAT-trim/FLMV checker execution is claimed.

## Declared concrete calculus and budget

Fix an authenticated original signed CNF F on n variables, with its complete immutable original encoding and clause multiset. A proof is a chronological **DRUP-only** sequence of additions and deletions. Every addition is a proper non-tautological nonduplicate-literal clause C, accepted iff unit propagation on the then-active database with all negations of C yields conflict. Deletion must identify an extant occurrence, but may remove source or previously learned clauses. Every learned clause name is explicitly represented, may use any new Boolean variable, may be of any finite width, and may be reused on later steps; there is no RAT, PR, SR, resolution-with-extension axioms, GF(2) inference, answer oracle or unlogged alternate UNSAT termination. The goal is a final RUP-valid addition of the empty clause. All output bytes, including the names and deletions, count in the certificate budget. This is a distinct deliberately generous DRUP semantics, **not a claim about particular DRAT-trim accepted bytes** or historical R_mix341.

Let L be the total proof encoding *bit count*, r the number of additions and v the number of distinct variables occurring in the source or proof. An explicit binary record grammar yields r <= L and v <= n+L. Whitespace ASCII DRUP is an even less compact example; counting its total bytes as B also yields r <= B and v <= n+B. Names with enormous numerical indices do not represent free new variables: their written digits are charged.

## Theorem 529.1: deletion/fresh-variable budget lift (PROVED/RESTRICTED)

For every original CNF F and every legal DRUP-only refutation of written length L bits as above,

$$
W_{\mathrm{Res}}(F)\le r v\le L(n+L).
$$

**Proof.** Erase every deletion from the chronological log and retain every original/source and RUP-added clause. RUP is monotone under adding premises: an existing UP conflict remains reproducible when additional clauses are retained, so every addition stays RUP-valid. For each addition C, fix the actual finite UP witness from the enlarged database under negations of C. Resolve the conflict clause backwards along the propagated reason clauses; each variable is propagated at most once before the conflict, so this produces a Resolution derivation of a subclause C' of C using at most v binary inferences. Add C as a temporary weakening of C' where needed to preserve all exact later interface references. These additions are chronological, so their internal proof expansions form one acyclic source-authenticated shared DAG. The standard strengthening induction from [P2-L2-524] removes all temporary weakenings without adding Resolution nodes: propagate stronger parent clauses through each resolvent, reusing a pivot-free stronger parent if a pivot disappears. The terminal strengthened subclause of empty is empty. Therefore a genuine ordinary DAG Resolution refutation of F exists using at most rv paid inference nodes. Finally r<=L and v<=n+L. The proof makes no assumption that auxiliary literal indices are bounded by n, and it charges their syntax through L. QED.

Equivalent **cost-sound abstract nonreachability**: for a fixed bit budget B, overapproximate every legal RUP-addition transition by an arbitrary block of at most n+B ordinary Resolution inferences plus its free temporary interface weakening, and make deletion stutter. Each genuine concrete goal path of budget <=B has an abstract source-rooted refutation of at most B(n+B) distinct Resolution nodes. Hence an independently established W_Res(F)>B(n+B) **excludes every concrete DRUP refutation in budget B**. Crucially the abstract system is MAY/overapproximate; it is not an exact proof checker, and logical nodes and physical proof bits are separate resource measures.

## Established 3-CNF hard-family transfer, with exact scope

Take a connected 3-regular edge-expander G_h on even h vertices, one source variable x_e for each of the 3h/2 edges, and a fixed odd-weight charge vector. At each degree-3 vertex, encode its XOR parity equation by all four proper signed 3-clauses falsified exactly by the wrong-parity incident assignments. The original has m=4h clauses, n=3h/2 variables, source encoding N=Theta(h log(h+2)) for canonical binary indexed representation. Odd total charge is certified UNSAT by summing all vertex equations over GF(2).

Ben-Sasson–Wigderson's general shared-DAG ordinary Resolution lower bound gives W_Res(F_h)>=2^(c h) for some c>0 along a qualifying expander family. Consequently every above DRUP-only log, allowing arbitrary fresh variable names, deletions and shared reuse, satisfies

$$
L(3h/2+L)\ge 2^{ch},\qquad
L=2^{\Omega(h)}=2^{\Omega(N/\log N)}.
$$

This is a parameterized **proof-certificate output-bit lower bound** and therefore a lower bound on any algorithm *required to emit such a log* (at least one bit-output action per bit on a sequential bit-output model). It is NOT an arbitrary SAT decision-time lower bound. GF(2) Gaussian elimination immediately solves the vertex-charge parity contradiction in polynomial time, and native RAT/ER/other shortcuts are explicitly outside the DRUP-only calculus. No lower-bound preservation through an outside-3CNF reduction is assumed: the hard family already has native proper signed 3-CNF clauses.

## Genuine short paths, RAT failure and exact finite replay

A genuine RUP lemma can introduce a fresh variable as a **weakened** consequence: choose a nontautological resolvent C of two K4 source clauses, add (C OR y) for y=1000003 (not in the source), delete that learned occurrence, then complete the underlying ordinary variable-elimination RUP refutation. The auxiliary name occurs in the written log and in the variable budget; deletion is explicitly replayed. For the eight odd K4 charge configurations, the base transcript has 31 RUP additions, and the augmented transcript has 32 additions and one deletion, seven distinct used variables. An even-charge K4 source is SAT; concrete UP rejects the spurious final empty clause.

Deletion can change **RAT** eligibility in the opposite direction: with D={(NOT a OR b),(NOT b)}, addition (a) is not RAT because resolvent (b) fails UP; after deleting the first clause there is no opposite-pivot clause, so (a) is RAT vacuously, although it remains non-RUP. Therefore no deletion-erasure theorem is asserted for DRAT/RAT.

Python strict-source + DRUP replay: 96 assertion groups, 16 original K4 3CNFs (8 SAT and 8 UNSAT), five malformed and three invalid-record controls, all odd cases with a fresh variable/deletion and 31 base additions. Independent Node.js implementation: 84 assertions, same 8/8 labels and 31/32 additions, with 16 source SHA-256 fingerprints (odd mask 1: ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096). Separate published pure-JavaScript implementation passed 99 assertions in V8 before publication and again after exact GitHub source readback, including an explicit RAT deletion nonmonotonicity control. These are finite **COMPUTATIONAL** controls, not a native proof of the asymptotic source theorem or native checker authority. No executable general source-DAG Resolution compiler was mechanically verified for all auxiliary-variable cases; that part is the written structural argument based on /524.

Representative augmented UNSAT trace: 32 additions, one deletion, 347 ASCII proof bytes, 7 variable names, 642 UP clause scans and 60 forced assignments under the Python scan policy. Host resource controls: Python 0.66 s/96,392 KiB max RSS; Node 0.04 s/33,392 KiB max RSS (process-level, includes interpreter/runtime and output, not a same-FLMV-machine measurement). The maximum tested augmented proof has 349 bytes. Peak shared-ancestor space and arbitrary program compilation are **not bounded by this certificate theorem**. Source acquisition, parsing, UP scans, ephemeral caches, indexing, output and verification all cost nonnegative real machine resources, but the output-bit lower bound alone suffices for this **proof-emitting** class.

Published executable: experiments/arc/lspv2_529_aux_drup_bit_budget.cjs (blob a2dfd60b0e3cec4fa1781830c4c85012184a3470). Python and independently written Node scripts and full raw records are supplied in the standalone reproducibility archive attached to this run. Public summary raw JSON at results/raw/arc/2026-11-09_1521_LSPV2_529_AUX_DRUP_RAW.json.

## Route A transfer and open gaps

Nothing here converts an arbitrary fixed total correct polynomial-time SAT decider A into a DRUP-outputting solver with polynomial overhead, nor constructs a uniform solver-dependent recursively iterable all-input Phi(A) with the same-machine FLMV inequalities

$$
t'\le\max(11/10,3/5+t/2),\qquad s'\le\max(1/2,s/2).
$$

In particular, RUP-log size is an output resource of one restricted algorithm architecture, not a generic lower bound on SAT decisions or arbitrary proof systems. Historical R_mix341 rule authentication, all-rule cost-sound transport and noncircular same-calculus B3 are untouched. [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN; P versus NP OPEN.

**Next:** determine whether any proposed universal solver-intensional Phi has a *certified* DRUP-output interface; absent such an interface, do not transfer the bit bound. Retain the actual GF(2), RAT, ER and early-RUP shortcuts as red-team controls. All five existing roles, schedules, 2 Route A / 3 Route B allocation and historical weights are preserved.

**References:** Ben-Sasson–Wigderson (2001), https://doi.org/10.1145/375827.375835 ; https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf ; DRAT-trim original-format README https://github.com/marijnheule/drat-trim/blob/master/README.md ; D'Silva–Haller–Kroening (2013), https://doi.org/10.1145/2429069.2429087 .

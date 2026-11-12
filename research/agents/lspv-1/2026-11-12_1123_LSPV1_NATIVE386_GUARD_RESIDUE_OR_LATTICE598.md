# LSPV-1/598: Exact guard-residue OR lattice in original native /386 Resolution

November 12, 2026, 11:23 PST. General SAT Lower-Bound Lead, historical Route B. **PROVED/RESTRICTED** fixed-DAG theorem plus **COMPUTATIONAL** original checker replay. **P versus NP OPEN**.

## Target and four falsifiers

Candidate: On the same original signed guarded odd-K4 SOURCE and exact 27-inference non-guard Resolution DAG, selected guarded SOURCE leaves can be replaced by genuine, terminal-live, paid guard-elimination Resolution ports. The guard residue at every derived node obeys Boolean OR, and the final guard pivot can disappear exactly when all 16 source leaves are ported.

F1: a proper subset removes the guard from the body root. F2: the unchanged original checker rejects a correctly charged partial-port certificate. F3: a selected paid port becomes terminal-dead or shared paid ownership is charged incorrectly. F4: a forged original source, signed pivot, ordered parent, terminal, guard or charge is accepted. F1 is excluded symbolically and by exhaustive 65,536 source-port guard assignments, and F2-F4 are addressed by 47 accepted and six rejected original-checker controls.

## Exact authenticated original sources

Original unchanged archived /386 checker: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. Exact original signed source-bound seed: results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json, blob 4177ec15a0c7253378d5652a6b13b7152601d300. Previously accepted all-sixteen-terminal-live port certificate LSPV-1/597: results/raw/arc/2026-11-12_1100_LSPV1_597_NATIVE386_LIVE16_W44_ACCEPTED.json, blob a9514ed6d28d19403d745a583c3096d36cd1a399.

The seed has 16 authentic signed clauses D_i = C_i OR NOT g, one authentic unit g, 27 paid non-g-pivot RES nodes deriving NOT g, a final paid pivot on g deriving empty, one once-paid historical CLI-sentinel AND2 owner, and one free terminal-dead DEF view. There are 17 mandatory original SOURCE occurrences, 28 paid RES occurrences, 46 total records, and W=29. Every one of the 16 guarded SOURCE leaves is a terminal ancestor in the original 27-RES body.

## Theorem 598.1: guard residue and exact conditional cost

Fix that precise original signed 27-node DAG, preserving every original SOURCE, the owner tuple, ordered parent topology, signed pivots and shared identities. For EACH subset S of the 16 guarded source leaves, introduce one distinct paid native Resolution record Q_i = Res_g(g,D_i) = C_i for each i in S and replace every use of the original D_i by Q_i; recompute every signed body conclusion with the same chronological parent wiring and non-g pivot. If S is proper, append the original final guard-resolution step. If S includes all 16 leaves, the body itself already ends at the empty clause.

The body concludes NOT g if S is proper, and the empty clause if S is full. Every new Q_i remains terminal-live. With k=|S|, the complete count-once native logical charge is:

    W(S) = 1 + 27 + k + 1[S is not the full 16-element set].

Therefore W(S)=29+k for k=0..15, while W(full)=44. For k=15 the proof costs W44 and still retains the final guard pivot; for k=16 it costs W44 but dispenses with that pivot. Exactly all 16 port replacements are necessary to remove the guard in THIS FIXED SKELETON and direct-port construction.

**Proof.** Let rho_g(C) be 1 iff clause C contains NOT g. None of the 27 body inferences pivots on g; no body parent contains positive g. Hence for every original or recomputed signed non-g-pivot Resolution, rho_g(Res_p(A,B)) = rho_g(A) OR rho_g(B). Removing NOT g from one or both parents cannot change the nonguard signed resolvent or create a tautology. Therefore the derivation remains legal after each substitution, by induction in the historical chronological order. Every unported original leaf contributes rho=1, while each true paid port Q_i contributes rho=0. Because all 16 leaves reach the original terminal body node, its resulting guard bit is the OR of their 16 indicators and equals zero iff S is full. The nonguard projection of the full body's signed clauses is unchanged and ends at the empty clause, as in exact witness /597. Thus the replayed body ends at NOT g for a proper S and empty for full S. The original g unit closes the former with exactly one final RES. All selected ports are terminal ancestors, not discarded paid padding. The 27 body RES identities and one owner each stay charged exactly once. Adding k paid port IDs and, for proper S, the final guard RES gives the displayed W formula. No SOURCE substitution, oracle, assumption erasure, hidden model switch or extra free rule is used.

This is **NOT** a lower bound for all proof DAGs: the SAME original source admits the original cheaper W29 proof. It does not establish a general SAT lower bound, optimal discovery cost or historical mixed-calculus legality.

## Reproducible tests and evidence

Executed the unchanged original archived /386 checker body directly in hosted V8, using only I/O, arguments, hash-output and cloning adapters. All **47 DISTINCT** constructed native signed certificates were accepted by the original checker and passed its eleven bundled self-corruption tests, for **166,687 native assertion groups**. The 47 masks comprise 17 prefix masks k=0 through 16, all 16 singleton masks, and all 16 co-singleton masks. Every chosen port was checked as a terminal ancestor. Exhaustive Boolean guard propagation on the ORIGINAL 27-node parent graph was evaluated for ALL **65,536 subsets**: exactly 65,535 left the guard and one erased it. Six additional hostile packets were rejected (SOURCE, signed pivot, payment, terminal, guard and parent orientation).

Raw complete case ledger: results/raw/arc/2026-11-12_1123_LSPV1_598_GUARD_RESIDUE_LATTICE_HOSTED_RAW.json, Git blob 46753fafea8d71bab12829cd5a4e9a2b0514280b. Reproducible script: experiments/arc/lspv1_598_guard_residue_lattice.cjs, Git blob e260d525be401eb4790c3559f6d99c53915e1e6f. The script is set up to run the unchanged original checker in real Node OS subprocesses and compares its k=0 and k=16 outputs exactly to the previously authenticated seed and /597 witness. **That OS subprocess script was not independently executed in this run.** Observed tests used hosted V8 only. The local repository preflight, LaTeX compilation and independent LSPV-5 review remain pending. No machine runtime, evidence-bit, span or physical peak-space bound follows from W or assertion counts.

## Proof spine, precedence, and hostile model controls

**P2-D1 OPEN**. The actual /386 checker authenticates SOURCE/DEF/RES only, whereas the disjoint /341 checker authenticates its own SOURCE/AND3/GF(2) fixtures. Neither is one complete, authoritative, externally source-bound R_mix341 dispatcher accepting an authentic RES-to-AND3 or DEF-to-LOCAL-CONVERT transition. Unauthenticated branching, weakening, assumptions, discharge, contexts, deletion, joins, private/exported wires, algebraic operations and their correct historical weights remain conservative MAY transitions, never replaced by CANON1/2/2R.

**P2-C3 OPEN**. The precise OR transfer is a valid restricted invariant; the complete alpha/gamma relation and cost-sound transformers for EVERY native rule remain unproved. An abstract model must preserve the full source-authenticated shared DAG, paid IDs, guard state, provenance, owners and assumptions. Real cheap paths may not be removed as spurious CEGAR paths. Abstract charge must be no greater than the corresponding concrete charge, with completed-refutation preservation.

**P2-B1 OPEN**. This easy finite K4 construction is not a hard asymptotic family. All legal GF(2), extensions, learning, sharing, branching, algebraic and circuit shortcuts must be admitted to a proposed superpolynomial all-rule minimum. **P2-B2/B3 separately OPEN**. Polynomial SAT decision, proof-system checking and proof work in another system are not the required noncircular same-calculus transfer. P1-01/P1-03/P1-04 and P versus NP remain OPEN. Logical work, byte evidence, discovery, actual runtime, span and peak RAM are distinct.

Corpus surveyed: both root proof trackers, current issue #3, AGENTS.md, CODEX.md, repository research skill, root main.tex, original /341 and /386 checkers, current five-role handoffs, LSPV-1/597, LSPV-2/579, LSPV-3/593A, LSPV-4/566 issue finding, LSPV-5/508, historical LSPV-1/539, LSPV-2/549, LSPV-3/549, LSPV-4/539 and /549, and 539-549 related reports. LSPV-3/593A already created terminal-DEAD native source ports, LSPV-1/597 already made all 16 terminal-LIVE; the incremental result HERE is the exhaustive subset guard-residue theorem and cost plateau. No old result is misrepresented as a new asymptotic theorem.

Primary references: Cook and Reckhow, Journal of Symbolic Logic 44 (1979), 36-50, DOI 10.2307/2273702, for proof-system-specific work. Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973, for sound abstract interpretation. Clarke et al., CAV 2000, DOI 10.1007/10722167_15, for CEGAR. None recovers the missing original mixed byte grammar.

**TRACKERS REVIEWED; NO MATERIAL CHANGE**. proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2.txt blob ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe retain OPEN proof statuses. All five pre-existing roles, schedules, historical rule weights, ownership and TWO Route A / THREE Route B remain unchanged. Independent LSPV-5 OS checker replay of fifteen versus sixteen ports and discovery of one authoritative mixed-rule consumer are the exact next falsifiers.

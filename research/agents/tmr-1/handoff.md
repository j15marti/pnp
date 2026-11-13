# CURRENT TMR-1 handoff, 2026-11-13 14:07 PST | SAME-MACHINE-PRODUCT-CEILING002

**Superseding authority:** research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, reread on main. New five TMR identities, no LSPV reactivation or task mutation. **P versus NP remains OPEN.**

**New full report (Git blob a21269c0878e325d474c76623d0ab03428c63f51):**
research/agents/tmr-1/2026-11-13_1407_TMR1_SAME_MACHINE_PRODUCT_CEILING002.md

**Reproducible Python (blob 16dafc5be8764bece6066d1d313c2dac4b5a8375):**
experiments/tmr/tmr1_time_space_bridge_audit.py

**Immutable raw output (blob 033f08ad8b5fa41cc4e1cae72c54e73e50001c69):**
results/raw/tmr/2026-11-13_1402_TMR1_TS_BRIDGE_RAW.json

**TMR1-R1, CANDIDATE pending TMR-5:** For one fixed b-tape deterministic multitape decider on the *same actual input/trace*, S<=b(T+1). If T^alpha(S+1)^beta>=G(L), with alpha,beta>=0 fixed and alpha+beta>0, then T>=(G(L)/(2b+1)^beta)^(1/(alpha+beta)) for T>=1. All time/space and costs are from the same realization, no cross-machine pooling.

**TMR1-R2, quantified no-go:** TMR-3's exact *restricted complete-sweep* T(S+1)>=c L n, L=Theta(n log n), even under a hypothetical unrestricted transfer, implies merely T=Omega(L/sqrt(log L)) through the b-tape occupancy bound. This is below linear as an extracted growth lower bound, not a superpolynomial time bound. The real complete-sweep restriction separately forces T>=L. No unrestricted transfer has been proved.

**TMR1-R3, independent second review of TMR-5 O1:** Correct graph theorem for the full observation-only MAY abstraction: all real-valued potentials satisfying Phi(U)<=cost(U,V)+Phi(V) on *every* graph edge and Phi(empty)<=0 have Phi(initial)<=tau(D)<=L, and tau itself attains the maximum. **PROVED/RESTRICTED at precisely that graph scope, after TMR-1 and TMR-5 independent symbolic audits.** This is not a time upper bound or a proof that more expressive abstractions fail.

**Executed verification:** One published Python run 2.26 sec, 494,590 deterministic check groups, zero failures. Includes 132 source lengths, 1056 minimal-T checks, 528 same-machine domination, 120 polynomial resource witnesses, 230917 exhaustive integer implications, 6939 independently computed MAY graph optimality families and 254898 all-edge inequalities. Only integer/finite graph audits, not physical TM simulation or a general SAT solver. Node, repo-wide preflight and LaTeX compile not run. Source and raw fully readback-verified on GitHub.

**Dependencies and peer requests:** TMR-2 construct a truly post-observation necessary processing charge, not first-bit reads. TMR-3 derive a superpolynomial-strength tradeoff *and* a genuine unrestricted multitape transfer. TMR-4 require initial, every-step, terminal and source-binding cost soundness for any new abstraction. TMR-5 independently test R1/R2, and integrate the qualified second verification of O1. Recognizable islands and earlier equality/crossing arguments are historical prior art, not claimed novel here.

**Root status:** Full proof1/proof2 reviewed; no P=NP or P!=NP central proof obligation closed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left to TMR-5 synthesis; no old region overwritten.

**Single next target:** Formulate a non-tautological post-input-acquisition lower-bound invariant with charged operations and quantifiers sufficient to exclude *every* polynomial deterministic time exponent, or construct a correct compact-invariant counteralgorithm.

END_OF_HANDOFF::TMR-1::2026-11-13_1407_PST

---

# TMR-1 handoff, 2026-11-13 13:08 PST

**Current role:** TMR-1 Machine Model Lead; superseding replacement directive research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md. **P versus NP remains OPEN.** No schedule or legacy checker ownership changes made.

**Latest report:** research/agents/tmr-1/2026-11-13_1307_TMR1_MACHINE_SLICE_FIREWALL001.md (verified Git blob 0986c5a4889360c05ce777e6fd4a501d0ccba53d). Results are CANDIDATE pending TMR-5 independent mathematical review; the finite checks are COMPUTATIONAL. The report states the full fixed-uniform-machine target, encoding, dependency DAG, exact quantifiers and explicit all-polynomial-space requirement.

**Two testable mathematical counterexamples:**

1. For each length L, hardwire the full length-L truth table into the finite state of a *different* total decider A_L, with exhaustive correct fallback off that length. Therefore the pointwise minimum over deciders separately at every L has time <=L+O(1), regardless of P versus NP. This cannot be substituted for one uniform fixed A across lengths.
2. For every fixed total multitape decider A, a fixed B with one additional work tape copies the input once, then simulates A from that charged copy. Source-head movement O(L), while time O_A(L+T_A) and space S_A+L+O_A(1). Thus counting physical original-input rereads alone cannot yield an all-algorithm superlinear lower bound.

**Same-execution bridge:** If A has b work tapes, S_A(x)<=b(T_A(x)+1). A sufficient but still OPEN candidate is a genuine trace-observable charged distinction cost d_A(x)<=T_A(x), independently forced beyond every polynomial budget, for each correct fixed A and arbitrarily large valid x. Taking d_A=T_A is only a restatement. A forall-k simultaneous space<=B(L+1)^(k+1) / time>B(L+1)^k exclusion would suffice but is equivalent-in-aggregate to the open separation target.

**Reproducer:** experiments/tmr/tmr1_slice_counterexample.py, Git blob 8771602044547ccd3770c8314cf6e5c53ee9cb3f; raw results/raw/tmr/2026-11-13_1303_TMR1_SLICE_RAW.json, blob cff36a57d85d9bd12f26fb0ec559613a842800d2. Executed Python 1.10 seconds, all 32,768 length-15 binary words, 48 wellformed SAT; controls for complete 8-clause UNSAT, 2SAT, Horn, XOR, products, padding, renaming/polarities and malformed pass. Does not physically simulate the literal full-state TM or prove an asymptotic SAT lower bound.

**Specialist requests:**
- TMR-2: identify a nontrivial input-aware distinction that survives copying and arbitrary algebraic summaries, or give a smallest counterexample. First-read bits <=L cannot suffice.
- TMR-3: formulate/test a same-machine all-polynomial exponent tradeoff with all read, write, recompute and work-tape charges. Fixed small-space exponents cannot suffice.
- TMR-4: show complete all-transition cost-sound map of actual configurations; include all labels and genuine cheap computations.
- TMR-5: independently check the finite-control A_L construction, the input-copy transition simulation, all quantifiers, and the fact that the suggested forall-k budget lemma has not been proved.

**Tracker and manuscript:** full proof1/proof2 read; TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex read via blob API; no TMR-1 ownership markers established, so no edit. Ordinary file fetch returns blank for large tracker/manuscript despite nonempty blob hashes; never reconstruct or overwrite these.

**Next TMR-1 step:** formal transition-by-transition proof of N2 with exact state mapping, then seek a genuinely nontrivial candidate d_A not defeated by the copy/compact-invariant controls.

END_OF_HANDOFF::TMR-1::2026-11-13_1308_PST


---

# TMR-1 latest handoff | 2026-11-13 about 15:00 PST | POLY-SHORTCUT-CORE003

**New CANDIDATE symbolic negative theorem, independently review before promotion.** If a valid 3-SAT subset `K` is P-recognizable and its SAT labels on `K` are P-computable, one fixed all-input correct total decider first recognizes/solves `K` in polynomial time and otherwise runs a paid exhaustive fallback. Hence a statement that EVERY correct decider has superpolynomial time on this same `K` is false. Generalizes to any polynomial-time sound YES/NO/UNKNOWN partial classifier. This does not construct a general polynomial-time 3-SAT decider, and does not exclude algorithm-dependent or hard-to-recognize hard families.

**Concrete connected high-width proper-3CNF falsifier.** `F_n` consists of all positive triples over `x1..xn`, and eight clauses forcing simultaneously `x1` and `not x1` using four auxiliaries. Every `F_n` is UNSAT and has primal `K_n` (treewidth >= n-1) with a polynomial-time recognizable constant-size contradictory core. Signed variable relabelings, within-clause order, and full clause reordering do not defeat recognition. Removing any one of the eight clauses makes the formula SAT. Thus growing primal treewidth alone, even for connected strict-proper UNSAT inputs, cannot entail an all-algorithm SAT runtime lower bound.

**Published/readback:** report `research/agents/tmr-1/2026-11-13_1500_TMR1_POLY_SHORTCUT_CORE003.md` SHA `e2930a35ece2cd0a3263fcf1f6a4d74179b91b55`; executed V8 source `experiments/tmr/tmr1_poly_shortcut_core003.cjs` SHA `93dd19216e51d8da27105945f972996aee585981`; raw `results/raw/tmr/2026-11-13_1500_TMR1_SHORTCUT_CORE003_RAW.json` SHA `8f4ca4975e2a1d3aa725b2570fedb3dc7ea8d111`. 273 deterministic assertions, 0 failures, including 30 permuted negated UNSAT cases, 48 minimal-core deletion SAT cases, n<=8 exhaustive semantic controls and n=50 431432-bit source. Finite status COMPUTATIONAL; no physical TM, OS Node CLI or preflight run.

**Primary literature check:** Nancy Lynch (1975) JACM, section 3, complexity-core existence conditional on language not in P, original author-hosted PDF https://groups.csail.mit.edu/tds/papers/Lynch/jacm75.pdf. Our easy-promise shortcut is elementary and does not claim priority.

**Review assignments:** TMR-5 independently check both-label total fast-path proof, recognizer complexity, eight-clause contradiction and algorithm-dependent quantifier limitation. TMR-2 test proposed necessary information charges against this fast UNSAT island. TMR-3 test simultaneous same-machine costs, and TMR-4 keep fast-path concrete transitions in every MAY abstraction.

**Status:** Current directive, proof1/proof2, large main.tex, issue #3, protocols, and peer handoffs reviewed. TRACKERS REVIEWED; NO MATERIAL CHANGE. No root main.tex editing, no agent/task changes. P versus NP remains OPEN. One next target: derive or falsify a temporal-order-invariant processing charge that remains positive under every polynomial-time sound partial classifier and under arbitrary general machines.

END_OF_HANDOFF::TMR-1::2026-11-13_1500_PST

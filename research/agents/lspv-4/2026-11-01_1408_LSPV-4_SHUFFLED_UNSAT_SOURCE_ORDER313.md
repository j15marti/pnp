# LSPV-4 SHUFFLED-UNSAT-SOURCE-ORDER313
**November 1, 2026, 14:08 PST | Circuit Resource Auditor**

**Proof status:** PROVED/EXACT restricted source-record observation theorem by a classical decision-tree adversary, external mathematical referee pending; COMPUTATIONAL independent same-original both-label controls; KNOWN FLMV Theorem 5.7; all-input adaptive progress, universal ARC, numerical transfer and P versus NP OPEN.

## Exact obstruction and duplication audit

The all-input controller needs representation-independent actual SAT/UNSAT decision work, rather than a requirement to reconstruct variable assignments, retain a syntactic key, or enumerate nominal states. One previously verified uniform machine recognizes a fixed contradictory U198 subformula appearing at the beginning of a valid canonical source and rejects without inspecting its long suffix (LSPV-1 UNSAT-PREFIX-DECISION311, 13:55 PST). Does this pointwise polylogarithmic source-access cost persist after a valid permutation of original clause records? We show that it does not.

We fixed four falsifiers. (F1) Every valid UNSAT input forces a complete scan: FALSIFIED already by the ordered U198-prefix machine. (F2) The ordered-machine low probe bound survives all legal source permutations for every correct decider: FALSIFIED by the restricted theorem below. (F3) Many partial assignments or lossless keys are necessary to prove the probe lower bound: FALSE; only an opposite-label pair is required. (F4) A linear source-record probe bound establishes superlinear arbitrary-SAT time or nontrivial writable-space hardness: INVALID inference.

The method is a known coupled-input/adversary argument, not new general decision-tree theory. It is distinct from the previous LSPV-4 SORTED-ACCESSOR302 lower bound on one sorted OUTPUT bit because this theorem concerns genuine SAT versus UNSAT source decision. It also adopts LSPV-4 FULL-PAYLOAD-VALID-NEIGHBOR310 and LSPV-1 RANDOMIZED-QUERY309 rather than claiming their results as new.

## Authenticated canonical SAT and UNSAT family

Let U denote the 198-variable, 264-clause canonical duplicate-free proper monotone 3-SAT-(2,2) UNSAT source from the repository's original Döcker fixture. Let V be obtained by swapping positive third variable IDs 197 and 196 between zero-based clause records 2 and 44. Both are valid canonical originals of identical length. Their exact source signed-clause lists differ in only TWO records, but their SAT labels are opposite. V has a separately archived complete 198-bit assignment satisfying all 264 original clauses. U admits a complete proof by all 64 boundary cubes: 16 directly falsify an original boundary clause and the other 48 are each refuted in one of six source-private modules, with 152 complete module calls. Independent verification for this report visited 17,343 deterministic UP-DPLL nodes in those calls.

Let F9 denote the valid 9-variable, 12-clause canonical source with exactly 70 full satisfying assignments. For each integer t>=0 define U_t as U plus t variable-disjoint renamed copies of F9, and V_t analogously with V instead of U. Then U_t is UNSAT and V_t SAT, both original inputs have n_t=198+9t variables and m_t=264+12t clauses. Signed (2+,2-) occurrence quotas, three-distinct-literal monotonicity, unique clauses and malformed-input rejection are preserved. Only two original source records differ between U_t and V_t.

Use Elias-gamma n,m headers followed by m source records containing one sign bit and three fixed-width unsigned original-variable IDs of width w_t=ceil(log2(n_t+1)). Let R_t=1+3w_t and N_t=|gamma(n_t)|+|gamma(m_t)|+m_t R_t=Theta(t log t). The complete-language grammar accepts any permutation of original clause records; it does not require lexicographic record order.

## Theorem 313A: exact deterministic all-input SAT decision, valid UNSAT side

**Theorem (restricted, exact).** For every t>=0 and every total deterministic exact all-binary-input decider D for the canonical target language, let Q_D(X) count distinct original clause-record locations from which D actually observes one or more source bits during its complete execution on X, including preprocessing and guest calls. Let pi range uniformly over all permutations of the m_t clause-record positions. Then

    E_pi Q_D(pi(U_t)) >= (m_t+1)/3,

and for some legal pi,

    Q_D(pi(U_t)) >= m_t-1.

**Proof.** Couple D on pi(U_t) and pi(V_t), using the same clause permutation. Headers and all source positions outside two exceptional records are identical. Until D actually reads a bit from either exceptional record, the entire deterministic observation transcript and all adaptive choices are identical. D cannot correctly halt on UNSAT pi(U_t) before a differing record is touched, or it would halt with the same answer on the valid SAT pi(V_t). The two exceptional record locations form a uniformly random pair of m_t positions under the random source permutation. Conditioned on no exceptional location yet observed, every previously uninspected row is symmetric. If T is the number of distinct record locations queried until the first exceptional hit, then for 0<=q<=m_t-2,

    Pr(T>q) = C(m_t-2,q)/C(m_t,q)
            = (m_t-q)(m_t-q-1)/(m_t(m_t-1)).

The mean minimum of two random distinct ranks is E(T)=(m_t+1)/3. Since Q_D>=T on the UNSAT execution, the first inequality follows. If D could halt without ever touching more than m_t-2 records on every legal permutation, there would exist a permutation with both exceptional records uninspected, contradicting exact correctness; hence the second inequality. QED.

This theorem does not assume recovery of original values or a memo key, nor impose a restricted SAT strategy. It is a lower bound on ACTUAL source-record observations across valid input orders, not on the number of possible residuals.

## Theorem 313B: bounded-error randomized cap

Suppose a randomized total decider errs with probability at most epsilon<1/2 on each valid input and, on every run of pi(U_t), touches at most q distinct source clause records. Couple the algorithm's runs on pi(U_t),pi(V_t) using the same coins and pi. Their outputs must differ with probability at least 1-2epsilon; they cannot differ without touching one of the two exceptional records. Thus

    1-2epsilon <= Pr(hit changed record)
              <= 1-C(m_t-2,q)/C(m_t,q)
              <= 2q/m_t.

Hence q >= (1-2epsilon)m_t/2, in particular q>=m_t/6 when epsilon=1/3. This is a *worst-run probe-cap implication*, not an assertion of expected SAT runtime or a lower bound on live workspace.

## Contrasting charged upper bounds and label asymmetry

On the specially ordered family U_t, the previously certified ONE fixed uniform all-input decider reads two gamma headers and the fixed first 264 source records; the bit count is exactly |gamma(n_t)|+|gamma(m_t)|+264R_t = O(log N_t). It then returns the membership output NO, which is correct even if the unobserved suffix is malformed because the first 264 records already form a contradictory subformula. A distinct MALFORMED diagnostic rather than the ordinary NO membership result would require a different fully checked parser.

On shuffled U_t, a fully specified safe decider may first attempt the ordered prefix check and then scan the source once for each of 264 fixed U records to verify that all are present, followed by immediate sound UNSAT rejection. This costs O(N_t polylog N_t) charged native time and O(log N_t) live writable/index space along that recognized UNSAT path, with all passes and source-head motions paid. If recognition fails, perform full grammar checking and exhaustive exact SAT search. This program is uniform and total, with no oracle providing the clause permutation, the label, or the best policy. Source order is irrelevant to the logical label but crucial to realized work.

## Independent finite controls, provenance and numerical ledger

The independent V8 source checker loaded GitHub's authenticated original U fixture blob f9dda41a810ad8e02bd553f2711a26a4050861f9 and independent V witness source blob 50bd21f4392043e132b660c3cd37621cf384520a. It passed **10,126 assertions**. Its original U proof exhausted all 64 boundary assignments with 16 direct contradictions, 48 modular UNSAT proofs, 152 module calls and 17,343 counted UP-DPLL recursive nodes. Its exact V witness satisfied every original source clause. It checked F9's 70 models, same-F9 original SAT and UNSAT coherent residuals with 2 and 0 extensions, all 264 four-way SS/SU/US/UU original clause-pair modes, 6,144 complement-clause identities and six malformed-control rejects. No timeout was an UNSAT proof.

A separately written standard-library Python mathematical verifier with NO SAT fixture import exhaustively enumerated every pair of hidden record positions and each prefix observation budget for m in {3,6,9,12,24,48,264}, passing **36,613 checks** of the rank distribution and probability formula. Exact independent rational arithmetic verified FLMV Theorem 5.7 points below. The full source-based checker is published in experiments/arc/lspv4_313/shuffled_unsat_order313_compact.py for execution in a project checkout; the connector-backed V8 replay was actually executed in this run because the local sandbox lacked the original source fixture.

Representative source lengths and necessary shuffled-record observations:
- t=0: n=198, m=264, N=6632 bits, ordered 6632 source bits, shuffled expected at least 265/3 records and some permutation at least 263.
- t=16: n=342, m=456, N=12802, ordered 7426 bits, shuffled expected at least 457/3 records and some permutation at least 455.
- t=64: n=774, m=1032, N=32032, ordered 8224 bits, shuffled expected at least 1033/3 records and some permutation at least 1031.
- t=256: n=2502, m=3336, N=123478, ordered 9814 bits, shuffled expected at least 3337/3 records and some permutation at least 3335.
- t=16384: n=147654, m=196872, N=10828030, ordered 14590 bits, shuffled expected at least 196873/3 records and some permutation at least 196871.

## Native indexed FLMV charging and total-work recurrence

One distinct clause record touched entails at least one actual read-only input-bit observation. Native deterministic indexed read-only-input time must therefore exceed the measured record-query lower bound, but index tape write/head move, address preparation, atomic index-tape erasure and access constitute EXTRA paid operations. Sequential source scanning can avoid per-record readdressing. No Omega(m log N) native-time lower bound and no Omega(m) writable-space lower bound follow. Logical Gray/XOR traces are OFFLINE unless executed and charged by the SAT machine.

A fully paid adaptive total-work recurrence for a source-authenticated state z is

    W_D(z) = C_grammar/source/index/head(z)
           + SUM_all_attempted_policies C_discover/select/switch/failed(z,policy)
           + C_GE/matroid/proof/cache/replay/output(z)
           + SUM_executed_children [C_child_translation/bit/guest(z,y) + W_D(y)].

The exact Shannon fallback decreases free original-variable count even if the signed saturation delta increases, but its total node count may be exponential. Peak space is the MAXIMUM SIMULTANEOUS total live writable/index/ancestor/proof/matrix/cache/selector/guest/child-buffer work state. Arbitrary guest DELAY/COPY/RECOMP and read/head costs remain hostile controls. Neither syntactic-key cardinality, finite certificate size nor selected-work Python proxy provides an all-input proof.

## FLMV Theorem 5.7 exact numerical audit

For c>1, define f0=1, fk=c f_(k-1)/(1+f_(k-1)) and dk(c)=min((1/fk-c)/k,c^(-k)). Independently computed exact rational envelopes:

    d*(6/5)=23/45; d*(241/200)=11642479/23232400.

The unique maximizing term is k=2 at both points; all k>=4 are strictly smaller since dk(c)<=c^-4<d2. Strict forbidden boundary does not include equality. Any proposed numerical transfer remains conditional on a correct and fully locally addressable SAT-to-Doecker reduction on the MATCHED deterministic indexed machine or a direct applicable lower bound. Neither this source-query lower bound nor target NP-completeness transfers the numerical FLMV region. No universal arbitrary-A to Phi(A) hereditary target-valid power-short transformation exists in this work.

## Literature, GitHub searches, and access failures

Primary literature: Nisan, CREW PRAMs and Decision Trees, SIAM J. Comput. 20 (1991), DOI 10.1137/0220062; Yao, Probabilistic Computations, FOCS (1977), DOI 10.1109/SFCS.1977.24; Döcker, Monotone 3-Sat-(2,2) is NP-complete, arXiv:1912.08032; Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52 (2005), DOI 10.1145/1101821.1101822. Web searches included "indexed random access read-only input sorting minimum finding query complexity", "Fortnow Lipton van Melkebeek Viglas theorem 5.7", "Döcker monotone 3-SAT-(2,2)", "Nisan CREW PRAMs decision trees", "Yao 1977 randomized distribution lower bound", "Munro Paterson limited-storage sorting". Original FLMV Theorem 5.7 PDF page was visually inspected.

Project GitHub searches included "U198 V198 shuffled rows decision read", "randomized valid-only U198 V198 bound", "U198 V198 scan lower bound padding", "valid only scrambled clause order SAT UNSAT lower bound", "grammar quota block cache time space tradeoff" and "canonical self-reduction"; separately searched github.com/openai for "SAT random access reductions" and "branching program SAT". No novelty inference follows from absent hits. Project earlier SORTED-ACCESSOR302, FULL-PAYLOAD310, PROBE286, LSPV-1 QUERY309/PAYLOAD310/UNSAT-PREFIX311, LSPV-2 transfer305/dynamic313, LSPV-3 GATE310/311 and LSPV-5 GAUGE273 were cross-checked for scope/duplication.

## Publication, ownership and remaining gaps

The integration handoff and delta-zero theorem were read FIRST. AGENTS.md, CODEX.md, the pnp-research skill, governance REDIRECT1 and CONTRACT1, latest issue #3 and cross-role reports were reviewed. GitHub returned EMPTY content for its nonempty root main.tex blob SHA 8b794e9e32eb165a27e731130a356118ac109105 (even when a limited line range was requested). Therefore a safe marker-confined LSPV-4-only root reconciliation cannot be verified; **ROOT REMAINS UNCHANGED AND RECONCILIATION PENDING**, rather than risking a destructive write. Role-owned report, code, raw and five-role handoff are published with exact GitHub readback. No existing task or scheduling changes.

**Next:** Establish a genuinely representation-independent bound on FULL computational work, stronger than linear input observation and surviving arbitrary source reorder, paid adaptive indexed rereads, semantic transfer, AND decomposition and guest DELAY/COPY/RECOMP. Separately close the all-input arbitrary-A hereditary reduction and strict numerical same-machine FLMV gap. **P versus NP remains OPEN.**

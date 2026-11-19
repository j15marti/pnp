# RECOVERY-PATH3: wrapper, selector, row reuse, and correct-path resources

19 November 2026, Asia/Seoul. Prior-work recovery and reconstruction. P versus NP OPEN. External independent mathematical review pending.

## Target and result

The current user directive is the row/block UNSAT specialist with matched SAT search; T5 is a control. The pipeline is explicit CNF/layout -> authenticated row residuals -> selector/certificate acquisition -> sound verification -> output -> compatible simultaneous time-space comparison.

PROVED: a uniformly clocked one-sided deterministic specialist complete on its designated polarity already gives a total decision algorithm by timeout. Likewise, a sound verifier with a bounded k-bit certificate gives a deterministic decider by exhaustive certificate enumeration, with the certificate and replay costs below. Consequently free polarity routing, existential certificates, and alternating strategies must be analyzed as three different interfaces.

Falsifiers used: a wrong certificate accepted on the opposite polarity; an accepted single row substituted for all rows; random-access guess storage omitted; an unbounded seed exponent silently replaced by 1.33. Finite controls found 126 layouts where a refutable block on one row coexists with a satisfiable formula, falsifying single-path-as-global-UNSAT reasoning.

## Recovered project ledger

All paths are in j15marti/pnp; complete bodies were retrieved except where explicitly identified as a search lead.

| Original source | Status recovered | Integration |
|---|---|---|
| research/agents/cross-track/2026-11-18_1825_ROW_BLOCK_SPECIALIST72_STATUS.md; blob f659e25c8cd77e67d5dc10b25c39523b2dae95dc | PROVED supplied-layout logic; CONDITIONAL seed recurrence | Exact row-dependent selector, child calls of both polarities, 1.33 threshold, witness extraction overhead. |
| research/agents/lead/2026-10-06_1436_LEAD-0023_WRAPPER_AS_SAT_QUANTIFIER_AUDIT.md; blob 89daf73166f90772800e1ad6e713fd0d60b2feab | PROVED under polynomial-decider hypothesis | Encode actual NO computations, not free negative semantic bits; existential route is not all-route correctness. |
| research/agents/lspv-3/2026-10-05_0235_LSPV-3_ORBITBATCH1.tex | PROVED restricted address identity | Invertible orbit maps have the same address union; repeated consumers do not force repeated acquisition. Retained tables and emitted outputs remain charged. |
| research/main/2026-10-20_2048_MAIN_ARC_SELECTOR_SPACE_FIREWALL23.tex | PROVED restricted circuit-materialization obstruction | Explicit source access bypasses a large materialized selector circuit. No RAM lower bound follows. |
| research/review/reports/wrapper/2026-11-01_0133_WRAPPER_CONNECTED_SHALLOW_BOUNDARY1.md | Scoped report recovered | Source cofactor structure and conditional composition do not supply a hereditary arbitrary-CNF compiler. |
| research/agents/redteam/2026-11-19_0913_T5_THREAD_POLY1/ | Existing finite witness control | This run checked the locally recovered complete witnesses against source079.t5, including all rotations. No new T5 discovery bound. |

The five TMR manuscript ownership slots do not assign a manuscript to Prior-Work Recovery. This is an additive recovery report, not a claim of manuscript reconciliation. No local checkout exists; repository preflight/LaTeX compilation were not run. Governance and relevant original reports were read through the connector. Unmerged drafts and all peer handoffs were not exhaustively audited.

## Supplied layout and fully paid scan

Let F(z,y)=AND_i F_i(z,y_i), with disjoint private variable sets after fixing z, R complete shared assignments, B blocks, and block encoding length at most ell. Then

    SAT(F) iff exists z, for every i there exists y_i: F_i(z,y_i).
    UNSAT(F) iff for every z there exists i, for every y_i: not F_i(z,y_i).

The NO block may depend on z. A sound uniform scanner, given a total exact child decider, scans blocks until it gets NO in each row; a row with all YES proves SAT. Failed probes include SAT children and are charged. With the supplied indexed layout, sequential residual construction, and compatible validation costs:

    T <= P + R*B*(ell + T_seed(ell));
    S <= layout live state + O(ell) + S_seed(ell) + counters.

For R=n^.195, B=n^.65, ell=n^.35, the recovered favorable local cost is n^1.195 and the seed-dependent exponent is max(1.195,.845+.35t). The workspace exponent is max(.35,.35s), only when retained layout/source indices also fit. Thus t<=97/70 and s<=10/7 are necessary for this particular one-step upper estimate to reach (1.33,.5). They are not necessary conditions on every possible solver. A seed n^K for unrestricted fixed K does not suffice for that estimate.

If every child admits the same paid construction, the formal time recurrence tends to 1.30. Heredity and uniform construction are unproved for arbitrary CNFs. Neither a recurrence fixed point nor P=NP alone supplies the construction. A small shared separator and small independent blocks are substantive structural hypotheses. Counting only some shared assignments is invalid unless a complete row cover is separately proved.

Conventional witness bit-pinning adds up to B*ell child queries on a successful row. Rewriting ell-sized queries alone gives n^1.35 work. Incremental or source-aware witness methods may improve this, so this is an implementation obstruction, not a witness lower bound.

## Three correct-choice models

1. **Free polarity routing.** Giving p=SAT(F) settles decision immediately. The remaining meaningful tasks are outputting a satisfying assignment or an authenticated UNSAT certificate/row-selector result. Decision lower bounds do not apply to that advised decision interface. An index of a bad block still requires proving it is bad. A free list of exact child answers can remove discovery work only by assumption.

2. **Uniform deterministic specialist.** D_p(F) may output a valid p-certificate or abstain; it must never output a false p-certificate. Suppose a known computable clock T(n) and space cap S(n) guarantee success on every input of polarity p. Simulate to that clock, abort on exceeding the space cap, verify any output, and return p exactly on success. Opposite-polarity inputs cannot succeed by soundness; intended inputs succeed by completeness. This is a total deterministic decider in O(T+verification) time and O(S+verification workspace+log T) space. This applies even if D_p diverges on the other polarity. Without a uniform clock or soundness, the conclusion does not follow. A partial 2-CNF specialist remains only partial for general CNF.

3. **Verifiable k-bit correct path.** Let V_p(F,w), |w|<=k(n), be deterministic, universally sound on every w and complete for polarity p. Include every nested child, query validation, preprocessing, failed replay step and output check in bounds v(n),s(n). Padding gives at most 2^(k+1) candidates. Deterministically store each candidate, replay V, accept p if any verifies, otherwise return the opposite polarity. The resulting bounds are

    T_enum = O(2^k*(v+k+1)),
    S_enum = O(s+k+log(v+k+n)).

This theorem covers adaptive deterministic paths: a transcript of every binary choice determines that path. It does not cover unverified semantic answers or universal branches. Counting chosen block indices but omitting their NO verification understates v and possibly k.

An external read-only random-access certificate can reduce the verifier's writable space to s, but deterministic enumeration stores k bits, and a standard nondeterministic simulation that rereads guesses must also retain them. One-way guesses consumed once can avoid that storage, provided the verifier actually works in that model. Re-guessing on rereads without consistency checks is unsound. Read-only input access and address costs are charged; arbitrarily large unit-cost words are not assumed.

If k=alpha*log2(n)+O(1), v=n^(c+o(1)), and s=n^(sigma+o(1)), enumeration costs n^(c+alpha+o(1)) time and n^(sigma+o(1))+O(log n) space. If k=log^2 n, the generic enumeration is quasipolynomial; if k=n^a, it is exponential in n^a. These are upper bounds, not unavoidable enumeration costs.

## Whole strategy and row reuse

For UNSAT the selector is a function i(z), not one index. An explicit selector table has R*ceil(log2 B) bits before any refutation data. A succinct program/circuit for i may be smaller, but must be acquired, parsed, evaluated and validated over every row. For each row, verify the selected block is UNSAT; a branch accepting on only one row is insufficient. A general alternating computation requires all universal branches to succeed, with existential choices allowed to depend only on their preceding history. Bound the entire strategy description, or charge traversal of its universal branches and the required retained state. A k-bit root-to-leaf path need not specify that strategy.

Exact reuse theorem: for a fixed deterministic child solver and an authenticated exact key for each residual, Q calls whose residual encodings have D distinct values can be serviced by D child computations plus all key-construction, lookup, replay and consumer/output work. Proof: cache the first exact result for each key, and reuse it only on exact identity; induction on the call sequence preserves answers. Hashes require collision checks. Space includes stored keys, answers and any certificates; eviction causes recomputation. No multiplicative Q child-work lower bound survives unrestricted caching.

This specializes the earlier ORBITBATCH address lesson to the row scan. Private-variable renaming can share semantic decision results only after paid canonicalization and verified witness translation. Arbitrary semantic equivalence is not a free key. For an ideal supplied selector, R rather than RB child checks suffice, but its acquisition/verification cost remains. Even for identical source blocks, dependence on z may destroy reuse; no universal D bound follows from R,B,ell alone.

## Primary-source simultaneous exclusions

Input parameter n is encoded formula length. The references use uniform random-access machines with charged bounded-bit computation (or standard polylog-overhead RAM simulations), read-only input, and writable working memory. Arbitrary unit-cost big integers, nonuniform per-input advice, and free external certificate tapes do not inherit the exclusions automatically. Use exponent slack when simulating models or reductions.

| Polarity/model | Sourced exclusion and scope |
|---|---|
| Deterministic SAT decision; deterministic UNSAT decision by complement | Williams/Buss-Williams: c<2cos(pi/7)=1.801937... with n^o(1) space is excluded. Buss-Williams journal Figures 8.2–8.3 explicitly certify (c,epsilon)=(1.34070,.5); hence (1.33+o(1),.5+o(1)) is excluded in their convention. |
| Nondeterministic UNSAT (equivalently conondeterministic SAT; DNF tautologies via negation) | Diehl–van Melkebeek–Williams Theorem 1: for every c<cuberoot(4)=1.587401... there exists e>0 excluding simultaneous n^c time and n^e space. In particular n^o(1) space is excluded below that exponent. The existence of e does not set e=.5. |
| Explicit positive-space NO-side example | FLMV Corollary 6.5 gives d(c)=(1+c)/c^2-c for the coNTIME simulation, transferring with slack to nondeterministic UNSAT. At c=1.10, d=0.635537..., so time n^(1.10+o(1)) and space n^(.5+o(1)) are excluded. These verified NO-side statements alone do not establish exclusion at (1.33,.5). |
| Nondeterministic SAT | The preceding NO-side bounds do not apply. Guessing a complete assignment and verifying it takes near-linear time with linear writable assignment storage in the ordinary model. With a supplied random-access read-only assignment the verifier needs only logarithmic auxiliary workspace; that is a different certificate-access model. No corresponding (1.33,.5) nondeterministic SAT exclusion is asserted here. |
| Proof-system-specific refutations | A short refutation verifier is a NO-side certificate interface. A Resolution size lower bound restricts Resolution certificates, not all correct paths or unrestricted algorithms. A generic machine exclusion applies only after the proof checker and proof access are simulated with the stated time-space costs. |

Sources: [Buss–Williams journal manuscript](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf), definitions pp.1–3 and Figures 8.2–8.3; [FLMV manuscript](https://lance.fortnow.com/papers/files/tst.pdf), Corollary 6.5 and SAT completeness discussion; [Diehl–van Melkebeek–Williams](https://www.ias.edu/sites/default/files/math/csdm/08-09/sdiehl_an_improved_time_space_lower_bound_for_tautologies.pdf), Theorem 1 and Section 2.1. The last explicitly denies free two-way access to guessed bits. Search snippets that described FLMV's opposite-polarity result merely as 'nondeterministic SAT' were corrected against the full original text.

NEW COROLLARY, PROVED conditional on the cited exclusion and model match: on all CNFs, neither polarity admits a universally sound, complete k-bit verifier with v=n^(1.33+o(1)), s=n^(.5+o(1)), and k<=alpha log2 n for any fixed alpha<0.01070. Enumeration would contradict the deterministic (1.34070,.5) exclusion. This is a lower obstruction to that joint certificate-length/verification interface, not a lower bound on certificates alone. For a promised subset such as intrinsic-critical T5 deletions, the conclusion requires a compatible reduction and cannot be imported directly.

## Executed controls and limits

path_audit.py exhausts all 256 two-row/two-block Boolean tables with disjoint one-bit private assignments: 207 SAT, 49 UNSAT. All 1,024 complete selector candidates were checked; none falsely accepted a SAT table, and each UNSAT table had a valid selector. There were 126 SAT tables with some refutable row/block, exposing the universal-row error. These tables can be represented by CNF by excluding forbidden local tuples; no oracle complexity is inferred.

The recovered H33 data were source-hash checked. All 44 deletion witnesses and their five rotations passed 9,680 original-arc checks, with exactly the designated arc false in each. This tests free supplied-path verification, not acquisition. The compact rotation quotient removes a factor five, not the whole search. A native T5 witness stores n colors (or ceil(n log2 5) densely encoded bits); read-only verification scans original arcs. Neither high girth nor branch count supplies a lower bound against that verifier.

Exact rational tests recovered thresholds 97/70, 10/7, fixed point 13/10, and logarithmic-certificate slack 107/10000. No current-run external peer audit, formal proof-assistant check, or arbitrary-CNF splitter construction was performed.

## Status and next dependency

PROVED: timeout conversion; bounded-certificate enumeration; exact-identity cache reuse; supplied-layout quantifiers. CONDITIONAL: seed recurrence and the certificate-interface exclusion under the cited model. FALSIFIED: one accepting row/path certifies all-row UNSAT; generic polynomial seed alone meets the one-step target; external read-only certificate space equals standard guess storage. OPEN: arbitrary-CNF hereditary compiler, paid uniformly sound NO selector with verified child costs, square-root-space NO-side exclusion at 1.33 from the sources reviewed, independent peer audit, P versus NP.

DISJ: PASS, no rank-to-time inference. Relativization: constructive simulation only; separation bridge OPEN. Simultaneous DTISP: PASS for displayed charged conversions, arbitrary-CNF construction OPEN. Configuration counting: upper-bound consistency only, not used for necessity. Algebrization/Natural Proofs: no circuit separation claimed.

Next lemma: construct a source-authenticated row-selector verifier with explicit whole-certificate length k(n), charged child NO verification v(n), and replay workspace s(n); then apply the appropriate certificate-access conversion before comparing any exponents. No schedule, title, ownership or enabled-state change.

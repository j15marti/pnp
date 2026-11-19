# Cross-Track Synthesis 74 | Native Resolution certificate for arbitrary bad-block selectors
**2026-11-18 20:30 PST. Status:** PROVED/EXACT restricted source theorem; COMPUTATIONAL audited certificates; CONDITIONAL resource consequences; P versus NP OPEN.

## Order and reviewed work
Four integration targets were fixed before searches: (1) correct-path quantifiers and certificates, (2) charged answer-only recursive simulation, (3) actual proof-system transport, and (4) original-source T5 controls. Then read current j15marti/pnp GitHub main and issue #3; TMR-1 /059v2 and TMR-3 /049 Resource Contraction handoffs; LSPV-5 /530 selector-realization red-team and LSPV-2 20:07 virtual-child handoff for Nonrelativizing Simulation; TMR-2 /094 source/correct-path for Universal Obstruction; TMR-4 /062 and current unmerged PR #313 /097 for Proof Transport; SIGMA35; project Library search; Google Drive project living log and historical MAIN; and primary SAT time-space papers. Earlier selector realization is due to LSPV-1/626 and LSPV-5/530, not an invention of this run.

## Theorem CT74-A: uniform source-aware native Resolution refutation
Let h>=1, R=2^h and any f:{0,1}^h -> [B]. For every s, define the full-sign clause C_s = OR_i(x_i if s_i=0 else NOT x_i), false at exactly x=s. Create a fresh private u_s belonging only to block f(s), and insert the two source clauses (C_s OR u_s), (C_s OR NOT u_s). Under x=s, exactly block f(s) is UNSAT; all other private blocks are SAT. The whole original source is UNSAT. Deleting the two clauses for t makes it SAT with unique shared assignment t (not unique full assignment).

**Exact proof:** take all 2R original clauses as axioms, resolve each pair on u_s to obtain every C_s (R resolutions), and repeatedly resolve complementary full-sign clauses on x_h,...,x_1 (R-1 further resolutions). The final clause is empty. This is a genuine **4R-1-record** binary-Resolution refutation, maximum clause width h+1, independent of f. No weakening, extension variables in proof, oracle or hidden correctness bit is used. A source-authenticating recognizer for this paired grammar can output a checked SAT missing-mask witness, the checked UNSAT proof, or UNKNOWN for nonmembers. This is a restricted theorem, not an all-CNF algorithm.

Source input has 2R clauses of length h+1, ordinary bit length L=Theta(R h log(R+B)) to standard encoding factors. Source parsing, equality/pair checks, mask generation, output and proof verification are paid. The executed Python verifier holds proof history in writable memory and does not prove optimal native RAM peak. Selector complexity/entropy, one-bad-block-per-row or independent-oracle RB decision-tree cost do NOT imply lower bounds against source-inspecting arbitrary algorithms.

## Exact quantifiers / paths
For F(z,Y)=AND_b F_b(z,Y_b) with pairwise disjoint private Y_b:
SAT(F) iff EXISTS z FORALL b EXISTS Y_b F_b.
UNSAT(F) iff FORALL z EXISTS b FORALL Y_b NOT F_b.
The refutable block may depend on the same z; all rows are necessary. A successful YES path needs common z and separately checked private witnesses. A successful NO path needs verified negative evidence for one real block on every row, or charged exact child decisions. Forged/missing paths yield UNKNOWN. Free correct polarity is answer advice; a single favorable adaptive branch is not a complete universal strategy. Uniform k-bit paths checked on ALL inputs with capped verifier T_v,S_v can be enumerated in O(2^k(T_v+poly(N+k))) time and S_v+O(k+log N) writable space only if the verifier is sound on EVERY path and complete for BOTH labels.

## Charged time-space
R<=N^.195, B<=N^.65, L_guest<=N^.35 entails up to N^.845 child decisions. A fully materialized schedule has N^1.195 source/output bit activity; naive upper time exponent max(1.195,.845+.35p) for seed exponent p, with authenticated source/space conditions. N^1.33 requires p<=97/70=1.385714..., not arbitrary polynomial-time p. For a uniform hereditary exact-answer-only all-CNF controller with local exponent lambda<1.34070, workspace <=N^.5+o(1), q=.845 and beta=.35, recursive self-simulation gives q+beta*1.34070=1.314245<1.34070, conflicting with Buss-Williams' deterministic random-access DTISP exclusion. This does not prohibit a promise-only layout or a solver-internal/non-extensional interface without separately charged simulation.

**Literature polarity correction:** FLMV (2005), Theorem 1.2 is a **co-nondeterministic SAT** / nondeterministic UNSAT result for c<sqrt2 and some d(c)>0, NOT a nondeterministic SAT theorem as incorrectly characterized in LSPV-5 /530. It does NOT exclude time N^1.33 with space N^.5. Fortnow's 1997 nondeterministic SAT near-linear regime and Diehl-van Melkebeek-Williams nondeterministic TAUT small-space regime are distinct. Resolution-specific hardness never becomes an unrestricted SAT lower bound without a machine-to-proof transport theorem.

## Hostile executed controls and reproducibility
Standard-library Python, fixed seed 202611182022: 107 selector maps, **10,733 full original-source Resolution proof records**, **3,980 assertions**, **zero failures**. Exhaustive small maps, dense affine and random maps, deleted-row SAT, malformed UNKNOWN. Independently implemented checker reading a saved h=5 source and certificate passed **127 records = 64 actual axioms + 63 legal resolutions**, max width six, empty clause. T5 H9 four path offset supports have empty total intersection, all three-path subfamilies SAT; native TMR-4 T5 four-vertex UNSAT/SAT pair had 0/40 assignments. Finite controls do not establish general asymptotic hardness.

Local bundle: `2026-11-18_2030_SOURCE_RESOLUTION_SELECTOR74_BUNDLE.zip`, SHA-256 `ad6a0801361098f41afe62f923b21a4ffbb762e1fe80e3ff50703d970cde2439`, with full 16K report, preregistered research targets, two Python checkers, saved complete native source/certificate, results JSON, SHA-256 manifest. ZIP CRC verified. The local executables are not claimed to be GitHub-published.

## Proof DAG
**ESTABLISHED:** source quantifier identity; appropriate primary-source model-specific lower bounds.
**PROVED/RESTRICTED:** one bad block for every z but 4R-1 native Resolution certificate; source-aware correct SAT/UNSAT/UNKNOWN interface.
**COMPUTATIONAL:** 107 cases, 10733 records, 3980 assertions, independent 127-record replay, native T5 controls.
**CONDITIONAL:** charged block scan, all-input hereditary answer-only self-simulation and seed p threshold.
**FALSIFIED INFERENCE:** selector entropy/independent-oracle decision tree forces hard SAT or Resolution on actual encoded source.
**OPEN:** hereditary arbitrary-CNF compiler, paid whole-NO proof acquisition, uniform correct-path resource claim, indispensable nonrelativizing WRAPPER hinge, same-input universal UWI, algorithm-to-Resolution lower-bound transport and P versus NP.

## Specialist assignments
1. **Resource Contraction:** authenticate an N-bit compressed guest ABI, account for source access, generation, failed children, proof emission, peak work and recursion; distinguish n as layout parameter from true source length.
2. **Nonrelativizing Simulation:** isolate an indispensable WRAPPER step surviving this source-aware relativizing proof; no free solver trace or polarity.
3. **Universal Obstruction:** find a mixed SAT/UNSAT same-input family surviving direct source-refutation shortcuts, with common clocks and correct FORALL z EXISTS block quantifiers; use H9 and critical deletions as negative controls.
4. **Proof Transport:** independently check 4R-1 line construction; seek actual reverse proof transport for named high-girth gadgets, without interpreting Resolution lower bounds as arbitrary-algorithm lower bounds.

**Sources**
[1] Buss and Williams (2015), Figure 8.2: https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf
[2] Fortnow, Lipton, van Melkebeek and Viglas (2005), Theorem 1.2: https://lance.fortnow.com/papers/files/tst.pdf
[3] Fortnow (1997): https://doi.org/10.1109/CCC.1997.612300
[4] Diehl, van Melkebeek and Williams (2011): https://doi.org/10.1007/s10878-009-9286-x

Independent mathematical peer review and physical RAM microstep replay remain OPEN. No other agent files, automation identities or schedules changed. **P versus NP OPEN.**

# LSPV-4 367 five-role handoff: general-CNF source-exact library barrier

**November 3, 2026, 11:36 PST. PROVED/EXACT within a declared fixed-witness, auxiliary-only syntactic restriction model, external specialist review pending. COMPUTATIONAL independent controls. B1/B2/B3, superpolynomial full Rmix341 minimum and P vs NP OPEN.** No schedule, task, identity, enabled state, proof-system rule or weight changes.

## Established starting point and why transfer is missing
Haken (1985) gives exponential **ordinary DAG Resolution** proof length for standard PHP, but polynomial Frege / Extended Frege proof constructions defeat a direct transfer to the unchanged stronger mixed Rmix341. Odd expander Tseitin likewise has an exact linear paid AND3 + GF(2) proof in Rmix341. This run instead tests an alternative **universal reflection** route. Existing LSPV-1 367 / LSPV-5 REFEREE318 use exact syntactic restrictions from a universal UNSAT wrapper to proper **3-CNF** originals. This property cannot be assumed for arbitrary-width general CNF with the same clause-source interface.

## New scoped theorem and proof
Fix a set of n original witness variables Y that must all remain unassigned, and let H_n(Y,Z) be a single **explicit** CNF source. Restrict only auxiliary Z variables, allowing satisfied source clauses to disappear and false auxiliary literals to be deleted. For every nonempty proper signed clause C over Y, define the minimally UNSAT source F_C = C AND (AND over literals l in C of not l). Every F_C has encoded length O(n log n), and single-source deletion or sign flipping makes it SAT.

If H_n|rho_C must be **literally** F_C for every C, then H_n contains at least **3^n - 1 distinct source clauses**. Proof: any source clause D has a fixed Y-literal projection D_Y, and after auxiliary-only restriction D either vanishes or becomes exactly D_Y; different C require different D. There are 3^n-1 nonempty signed clauses because each Y variable is absent, positive or negative. In terms of N_n = Theta(n log n) encoded input bits, this requires exp(Omega(N_n/log N_n)) explicit clause records and output time. A linear-prefix one-hot selector source plus guarded C and opposite units attains O(n3^n) records under the same model.

**Firewall:** This is a proof about a _literal source dictionary_ for a universal syntactic-restriction wrapper, NOT a bound on minimal Rmix341 inference nodes, polynomial-time SAT decision, proof search, or writable space for a streaming writer. Signed substitutions, original-variable restrictions, arbitrary circuit replacements, semantic backtranslation and 3-CNF normalization are outside the theorem. Proper width-three clauses number only 8*binom(n,3), so existing width-three wrappers escape. The exact full-mixed **normalization-to-original** proof backtranslation remains OPEN.

## Finite verification
Independent Python and Node.js enumerated 1,086 UNSAT clause-minimal sources for n=1..6, 5,096 deletion SAT witnesses, 8,020 sign-flip SAT witnesses. They verified 36 source-exact sequential-selector specializations for n<=3. Independent Node: 14,279 assertions. Malformed DIMACS: 11 rejected. K4 parity: odd 0 and even 8 models. Host Python peak RSS: 96,144 KiB, not an FLMV space bound. Optimizer discovery was neither charged to W nor silently counted as an inference.

## Actual external and peer assessments read
- GROKPROOF/2026-11-03_1912_PROGRESS.md SHA `dbec4959d96f19554061511cd240745f398272ec`: the all-input FLMV construction remains open. Earlier 12:17 UTC query-cost reversal was invalidated separately by LSPV-4 364.
- research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex SHA `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`: one-tape/sequential-access limitation, not an indexed-machine or B3 bound.
- research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex SHA `1f9fc727d3e2b009cba7afec2a93beb62959dd67`: restricted alternation-trading portfolio rule system.
- research/agents/lspv-1/2026-11-03_0956_LSPV-1_RESTRICTION_STABLE_REFLECTION367.tex SHA `64f4e87aa7c6050d088bb599ec4919aa119ba10e`: 3-CNF source-exact reflection; does not supply general-CNF width backtranslation.
- research/agents/lspv-2/2026-11-03_1112_LSPV-2_SOURCE_EXACT_MIXED_ESCAPE368.tex SHA `a4f5298f6f762b3458094a8535c0981cec8c3f7b`: mixed parity escape even when the wrapper is source-exact.
- research/main/2026-11-03_1048_MAIN_REFLECTION-FAMILY-EQUIVALENCE-REFEREE318.md SHA `d5164f4e977aac7c2b420c0989f26b972ba6d902`: neither correct decider clock nor source-exact restriction gives short mixed proofs.

## Ownership-safe artifacts
- [LSPV-4 formal report](../agents/lspv-4/2026-11-03_1136_LSPV-4_SOURCE_EXACT_GENERAL_CNF_LIBRARY_BARRIER367.tex)
- [Compact independently checkable executable](../../experiments/arc/lspv4_367_source_exact_library_compact.js)
- [Raw public ledger](../../results/raw/arc/2026-11-03_1136_LSPV4_SOURCE_EXACT_LIBRARY367_public.json)

A full independent Python producer and separate JS referee, detailed raw results, and SHA-256 manifest are available as the conversation reproducibility archive. No unsafe root main.tex modification was attempted: an authenticated ranged read returned zero bytes for a nonempty main.tex blob SHA.

**Next exact bridge:** Prove a polynomial-cost, grammar-preserving source-authenticated translation from any Rmix341 refutation of polynomial-size 3-CNF normalization N(F) back to a refutation of the **same original general-CNF F**, including DEF/LOCAL-CONVERT and all provenance/weights; alternatively build a different non-source-exact universal reflection with an independently proved sound transfer. A generic SAT-to-3SAT many-one reduction alone does not provide the necessary proof-cost inequality.

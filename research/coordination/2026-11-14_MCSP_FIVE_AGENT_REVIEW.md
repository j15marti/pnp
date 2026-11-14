# MCSP review and transfer investigation for all five TMR agents

LATEST USER PRIORITY, 2026-11-14 America/Los_Angeles: All five existing TMR agents must review previous work and primary literature for applications of the Minimum Circuit Size Problem (MCSP) to the P versus NP project. This supersedes competing scientific priorities and obsolete first-deliverable instructions, while preserving TMR identities, existing schedules, scientific safeguards, ownership and historical evidence. Do not create additional scheduled agents.

Read this handoff first, then the 2026-11-13 TMR replacement directive and existing required preflight sources. Review BOTH proof1.txt and proof2.txt, canonical main.tex, latest issue #3, all TMR handoffs, and relevant ORIGINAL reports/code/data from TMR, Claude, Grok and legacy LSPV work. Survey/search the corpus for MCSP, MKTP, hardness magnification, one-tape, crossing sequences, streaming, circuit minimization, natural proofs, locality barriers, semantic composition, DIRECTPRODUCT, TPORT, ONETAPE, Walsh/moment and certificate results. Review earlier failures and cheap algebraic/compact-summary controls, not only recent positive results. Do not treat chat claims as verified theorems.

Search fresh primary literature and follow original references and later corrections/improvements. Starting points, to be verified rather than assumed:
- Cheraghchi, Hirahara, Myrisiotis and Yoshida, One-Tape Turing Machine and Branching Program Lower Bounds for MCSP, STACS 2021: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23
- Locate the original McKay-Murray-Williams STOC 2019 and Allender-Hirahara magnification results cited there.
- Locate relevant Oliveira-Santhanam hardness-magnification work and Chen et al. locality-barrier work, and current extensions.
- Compare ordinary MCSP, Gap-MCSP, partial/succinct variants and MKTP only under their exact definitions and proved reductions.

For EVERY used theorem record paper/version/theorem or page, exact statement, input measure, model, uniformity, promises, circuit threshold, exponent, hypotheses and conclusion. Keep truth-table length N=2^n separate from circuit input arity n and source SAT encoding length L. Preserve threshold constants: a stronger-looking lower-bound exponent at a different circuit-size parameter does not automatically meet a magnification hypothesis. Do not assume ordinary MCSP is NP-complete, or transfer hardness results between variants without proof. Distinguish P != NP from stronger/different nonuniform conclusions. Label assumptions such as ETH/SETH or cryptographic hardness as conditional.

The user's motivating model is multiple single-tape deterministic machines, one reading another's output, asking whether polynomial elapsed time requires superpolynomially many machines or polynomially many machines require superpolynomial elapsed time. Charge all interfaces and show model simulation before importing a bound. Preserve adaptive state-dependent algorithm behavior, sharing, preprocessing, switching, cache/recompute, input rereading and arbitrary polynomial workspace. Do not confuse transport overhead with logical hardness or expensive selected representations with unavoidable computation.

FIRST MCSP deliverable for EACH agent: (1) relevant prior-work ledger with original paths and statuses; (2) a primary-source theorem table; (3) one specific proved transfer, scoped conditional lemma, falsification, or precise failed implication; (4) exact remaining gap to an unrestricted P-vs-NP proof; (5) one concrete next target and peer-review request. Later runs advance those targets instead of repeating surveys. Each report must say what is genuinely new relative to previous work. Experiments are finite evidence, not asymptotic proofs.

Publish under existing research/agents/tmr-i/ paths with Pacific timestamps, preserve handoff.md, and retain original code/raw evidence separately. Verify publications by readback and coordinate in issue #3. Apply existing conflict-safe ownership and proof-status rules; no tracker/main promotion with an OPEN load-bearing arrow. This directive changes research assignments, not mathematical proof status.

## Complementary assignments

### TMR-1

Lead: reconstruct the exact MCSP hardness-magnification implication chain from primary papers. Make a theorem/hypothesis matrix with exact problem variants, size thresholds, models, exponents, and conclusions (P != NP, NP not in P/poly, or other). Identify the weakest missing lemma that our existing results could plausibly supply. Coordinate one explicit candidate chain; no assertion that restating a separation is progress.

### TMR-2

Information: review crossing-sequence, communication, streaming, Kolmogorov-complexity, hitting-set and pseudorandomness techniques for MCSP/MKTP. Test whether prior information/certificate/continuation arguments yield the specific lower-bound property required by a magnification theorem. Audit full-input rereading, short summaries and natural-proofs/locality barriers. Produce one exact transfer or concrete counterexample.

### TMR-3

Resources: analyze one-tape MCSP lower bounds and the user's network of single-tape machines reading one another's outputs. Charge uniform construction, input distribution, messages, work, elapsed time, storage, and simulation overhead. Distinguish one tape total from one work tape plus one-way/read-only input. Determine whether established or candidate tradeoffs reach the exact magnification parameter regime; report numerical/exponent gaps explicitly.

### TMR-4

Abstraction and reductions: construct or falsify a cost-sound bridge from prior SAT constructions, semantic composition, signed/hypergraph encodings, circuit representations or Walsh/moment summaries to an MCSP-family target. Specify reduction direction, source/target lengths, promises, threshold and runtime blowups. In particular, distinguish a succinct SAT description from a full truth table of length N=2^n; no free exponential expansion or circuit-minimization oracle. If a promising exact finite construction exists, implement and independently check it against exhaustive small cases.

### TMR-5

Redteam and synthesis: independently audit the other four MCSP transfer chains, plus the prior chat's single-tape claims, against original proofs. Target mismatched thresholds (including distinct constants in magnification versus lower-bound theorems), input access, promises, uniformity, quantifiers, and hidden hardness assumptions. Rank surviving routes by weakest unresolved lemma and evidence; publish an integrated dependency map and explicit retirements. Update canonical main.tex and proof trackers only when warranted by verified material results under existing ownership rules.

## Scheduler registry

- TMR-1: 6af778ef5544819198f0a4059b2bdec6; existing hourly minute 00, America/Los_Angeles.
- TMR-2: 6af77909e2ec819183ae8b040f494abc; existing hourly minute 12, America/Los_Angeles.
- TMR-3: 6af77924af388191bb6c92ea9b21aef7; existing hourly minute 24, America/Los_Angeles.
- TMR-4: 6af7793bda988191a8a07813a0adbeec; existing hourly minute 36, America/Los_Angeles.
- TMR-5: 6af77956fd1c8191ab6054070636b1e5; existing hourly minute 48, America/Los_Angeles.

This file records the requested assignment. Successful scheduler updates are verified separately; the file alone is not evidence of delivery to already-running executions.

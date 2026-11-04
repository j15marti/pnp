# LSPV-4/391: Canonical Cook gate proof streaming and fully charged evidence costs

November 4, 2026, 10:00 PST. PNP Time-Space Resource Auditor.

**Status: PROVED/RESTRICTED** for the declared canonical typed Cook-Extended-Resolution certificate, given on immutable indexed read-only input, and authenticated binary DEF+RES fragment of the **unchanged R_mix341**. Full mixed-grammar byte validation, B1/B2/B3, superpolynomial full-mixed cost and P versus NP remain OPEN. The already-known ER2 embedding and polynomial PHP mixed proof are NOT new results.

## IDEA, SEARCH, ITERATE

**Initial idea:** show that a Cook extension q = a OR (b AND c) can be simulated in R_mix341 by paid binary conservative gates; expect five paid nodes. Falsifiers: invalid gate truth table; missing gate facet; illegal pivot; missing source; memory used for a proof-index table; free acquisition of a supposed short ER proof.

**SEARCH and correction:** Original fixed calculus is LSPV-2/341 (Git blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). The one-way ER2-to-R_mix341 simulation was already proved in project REFEREE299, research/main/2026-11-02_1648_MAIN_EXTENSION-SIMULATION-BARRIER-REFEREE299.md; polynomial PHP R_mix341 proofs already appear in LSPV-3/346 and LSPV-3/384. Previous LSPV-4/373 had a related strict source-gate logspace lift but did not write out this Cook nested-gate/view-index streaming macro. Red Team REFEREE336 identifies the full mixed grammar gap. Search queries included: Cook 1976 extended resolution pigeonhole; Cook PHP definition q=a or b and c; ER proof translation logspace; Haken PHP shared DAG resolution; project ER embedding, ER simulation Rmix, logspace source gate lift; connected github.com/openai resolution, pigeonhole, certificate checker. The OpenAI searches did not reveal a SAT proof translator. Read the OpenAI math Snaky in 21 Maker moves Sept 2026 certificate-checker README only as a process analogy, not a complexity theorem. Direct Google-branded search was unavailable, so general web and authenticated GitHub were used. The MDPI Sonobe full page returned HTTP 429; the four-clause extension was independently derived and checked.

**Outside review, actual paths:** GROKPROOF/2026-11-04_1518_PROGRESS.md (SHA 4e2bb9d941295f620a64e078117d29244caf4fba), research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (SHA 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a), research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (SHA 1f9fc727d3e2b009cba7afec2a93beb62959dd67). Grok retains the fully charged all-input ARC transformation as OPEN. Claude addresses restricted one-tape and portfolio alternation trading, not B3. Five-role November 2 handoff, active issue #3, AGENTS.md and CODEX.md also inspected.

**ITERATE:** abandon novelty claim for ER embedding; prove the narrower explicit uniform indexed-rescan resource upper bound, with no retained proof-index table.

## Corrected restricted theorem

Let F be the original source CNF, and let E be a supplied well-formed chronological Cook-style Extended Resolution script, with total input encoded length M. Every extension has fresh named q, signed existing a,b,c, and exact four named clause views for q = a OR (b AND c). Other events are binary Resolution from original source IDs, previous extension slots, or earlier RES nodes. Names are canonical integers of polynomial magnitude in M. All source, typing, pivot, dependency and final contradiction checks are required.

Introduce t = b AND c as one paid conservative DEF with authenticated clause slots

    (NOT t OR b), (NOT t OR c), (t OR NOT b OR NOT c).

Introduce q = a OR t as another paid conservative DEF with authenticated slots

    (NOT q OR a OR t), (q OR NOT a), (q OR NOT t).

The Cook extension views are

    (q OR NOT a),
    (q OR NOT b OR NOT c),
    (NOT q OR a OR b),
    (NOT q OR a OR c).

The first is already a DEF view. The other three are each a single paid binary RES from the two DEF sets on t. Thus every Cook extension costs exactly **two DEF plus three RES**, and every original RES event is copied once. For e extension events and r RES events the resulting valid *same-original-source* R_mix341 refutation has <= **5e+r paid logical nodes**, preserving all shared dependencies and final contradiction.

A single fixed deterministic transducer uses read-only indexed access to the supplied M-bit input and append-only output. It recomputes the output node index for event j by rescanning earlier input events and adding 5 per Cook extension and 1 per RES event; maps each Cook slot to the direct OR gate view or one of the three subsequent RES nodes. It checks legal source references, fresh names, signed pivots, chronological types and final empty clause with O(log(M+2)) writable counter bits. Nested rescanning costs at most **O((M+2)^6)** conservative bit steps, and the canonical output has at most **O((M+2)^2)** bits (loose bound). No uncharged source/proof lookup, mutable indexing table, or semantic SAT oracle is present. This is a proof *converter*, not a SAT solver; the supplied ER proof might itself have required much more work to acquire.

The initial gate embedding duplicates earlier project work. The separately explicit *rescan-output schedule for this declared Cook grammar* is the narrow resource lemma submitted for review; no claim that it is first in the literature.

## Established hard-family theorem, exact model

Unary PHP(h+1,h) has h(h+1) Boolean variables, m_h = (h+1) + h*binom(h+1,2) source clauses, and explicitly signed ASCII-DIMACS encoded length N_h = Theta(h^3 log(h+2)). Haken (1985) establishes: there exist c>0 and h0 such that, for every h >= h0, **every ordinary unrestricted shared-DAG Resolution refutation** of the original unary PHP CNF has at least 2^(ch) proof lines. This is a proof-system lower bound, not a lower bound for Extended Resolution, R_mix341, Res(XOR), or arbitrary SAT machines. Cook (1976) gives O(h^4) Extended Resolution proofs; prior REFEREE299 already translates binary-gate ER into R_mix341. Thus PHP is not a superpolynomial-hard mixed-calculus family. The indispensable-source arity count yields the known m_h-1 mixed lower bound in this at-most-two-premise model, polynomial rather than exponential.

## Finite independent controls and all-phase work

Primary complete Python reproducer: 207 assertion groups, three signed gate-name mappings, 11 paid-node checked UNSAT refutation from named slots, 13 malformed or illegal pivot controls and five invalid stream records rejected; same-original-source SAT deletion sibling; PHP h=1..4 with 3,9,22,45 clauses respectively, each UNSAT and every single-clause deletion SAT; odd/even K4 Tseitin 0/8 models. Independently coded no-import Node verifier: 239 checks, complete 32-case gate truth tables under 3 variable mappings, h=1..3 PHP and all deletions, corrupted pivot and K4 parity controls. All checks passed. The local ZIP includes full Python source, Node script, raw results, stdout and SHA-256 manifest. Finite host tests do not measure native indexed-TM time or space and do not reconstruct Cook's full all-size PHP proof.

A verifier supplied the original ER evidence as *read-only* input can use O(log M) scratch by rescanning. A solver constructing/writing this evidence incurs its generation, bit access, validation, output and any simultaneous materialization costs. If it materializes the M-bit proof in writable memory, all-phase peak S >= M for that implementation; if streamed, output work remains unavoidable. All guests, failed selectors and conversions must be charged. In the FLMV resource contract s' <= max{rho,eta,lambda,lambda*s}, rho covers every local phase including proof acquisition and temporary buffers. No rho <= 1/2 relative to original CNF input N is established. Exponentially long intermediate representations are not excluded but would carry their actual explicit access/output costs.

## Transfer quantifiers and next gap

B1 requires, for every fixed uniform total correct SAT decider A, a polynomial p_A bounding W_R(F) by p_A(N+T_A(F)) for every UNSAT F. B2 replaces pointwise time with max T_A(x) over ALL binary strings x of length <= N. B3, weakest sufficient, is SAT in P implies Wbar_Rmix341(N) polynomial for the **same preselected fixed R_mix341**. The supplied-proof compiler establishes none of these. An accepting/rejecting trace alone is not a valid all-input machine-correctness certificate.

**B1, B2, B3 and P versus NP OPEN.** Next: precise fully typed raw parser for R_mix341 and, independently, a source-only arbitrary-decider-to-proof bridge. No original task or schedule changed. Root main.tex not modified due concurrent-edit risk.

References: Haken, TCS 39:297-308 (1985), DOI 10.1016/0304-3975(85)90144-6; Cook, SIGACT News 8(4):28-32 (1976), DOI 10.1145/1008335.1008338; Grosof, Zhang, Heule, arXiv:2207.11284 (2022); Sonobe, Algorithms 15(12):479 (2022).

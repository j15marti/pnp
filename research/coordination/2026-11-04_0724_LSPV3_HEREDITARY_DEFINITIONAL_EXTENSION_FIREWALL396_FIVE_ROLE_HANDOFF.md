# LSPV-3/396: Hereditarily conservative definitions collapse ordinary Resolution hardness
**November 4, 2026, 07:24 PST.** Unchanged R_mix341, task identities, enabled states, schedules, weights and governance safeguards. PROVED/EXACT given published Haken and Cook theorems, specialist referee pending. Finite controls COMPUTATIONAL. P versus NP OPEN.

## Exact theorem and restricted scope
Let P_h = unary PHP(h+1,h), with h(h+1) Boolean variables, m_h=h+1+h*binom(h+1,2)=Theta(h^3) original CNF clauses, and N_h=Theta(h^3 log(h+2)) explicit signed binary-index bits. Haken (1985) proves: there exist c>0,h0 such that for every h>=h0 and every unrestricted shared-DAG ordinary Resolution refutation of precisely P_h, the proof has at least 2^(c h) lines. This does not concern Res(XOR), Extended Resolution, R_mix341, or arbitrary SAT deciders. Cook (1976) gives a uniform constructive polynomial-length Extended Resolution refutation of precisely P_h using acyclic Boolean definitions and ordinary Resolution.

For every h, let D_h be all definitions in Cook's proof, treated as **additional free source clauses in a new CNF input** E_h=P_h union D_h. Every old source clause is retained verbatim. D_h has a unique satisfying extension for every valuation of old variables. For every subset S of original clauses, projecting models of S union D_h to the original variables gives exactly the models of S. Thus all original clause deletion and sign-flip satisfying witnesses survive. Yet W_ordinaryRES(P_h)>=2^(c h)-m_h while W_ordinaryRES(E_h)<=poly(h). Move Cook's definitional clauses to the front of the source list and replay his Resolution derivation. Therefore no polynomial-output backward translation can generally take a polynomial ordinary-Resolution proof of E_h to an ordinary-Resolution proof of P_h, even with unlimited proof-search computation. The output grammar alone requires exponential lines.

**Scope firewall:** Free input augmentation P_h -> E_h is not a zero-cost in-proof transformation in R_mix341. In the unchanged mixed calculus, paid conservative DEF already gives the original PHP a polynomial proof. This result shows a failure of representation-invariant proof-cost reasoning from old source-subset semantics, NOT an all-algorithm lower bound and NOT a B1/B2/B3 counterexample for the fixed R_mix341. Unlike LSPV-3/394, it inserts no empty clause, no syntactic PHP recognizer, and no hardcoded UNSAT answer; all originals remain active.

## Test and resource ledger
Independent Python/Node tests generated only the first Cook gate stage q(i,j)=p(i,j) OR (p(i,h) AND p(h+1,j)). They checked h=1,2,3, full old-variable assignment spaces of 4,64,4096, and all 8/512 original source subsets for h=1/2. They verified 32,800 source-subset/assignment projection cases, unique gate extension, SAT/UNSAT controls, and corrupted-gate rejection. The GitHub Python producer counts 65,838 assertions, the independent Node verifier 65,801. An earlier local Python implementation counts 61,709 under a different assertion convention. Three malformed DIMACS strings were rejected by the Python producer. These are finite first-stage checks, NOT independent validation of Cook's full all-size proof, and no global proof optimum was computed.

Count paid logical DAG nodes separately from input bytes, gate and source parsing, construction, output serialization, validator work and all-phase peak space. Cook's uniform explicit generator is polynomial in bit time and storage. A required explicit backward Resolution proof has exponential output size. Neither implies unrestricted SAT decision time.

## Published paths
Formal theorem: research/agents/lspv-3/2026-11-04_0724_LSPV-3_HEREDITARY_DEFINITIONAL_EXTENSION_FIREWALL396.tex
Python experiment: experiments/arc/lspv3_396_conservative_php.py
Independent Node checker: experiments/arc/lspv3_396_independent.js
Raw data: results/raw/arc/2026-11-04_0724_LSPV3_HEREDITARY_DEF_EXTENSION396_raw.json
Handoff: research/coordination/2026-11-04_0724_LSPV3_HEREDITARY_DEFINITIONAL_EXTENSION_FIREWALL396_FIVE_ROLE_HANDOFF.md

Read November 2 refocus (blob 033b54b8), issue #3, AGENTS.md, CODEX.md, repo skill, original LSPV-2/341 (blob c87acd11), LSPV-3/394-/395, LSPV-1/386, LSPV-2/387, LSPV-5/335, and primary Haken/Cook/Grosof sources. Grok source GROKPROOF/2026-11-04_1518_PROGRESS.md (blob 4e2bb9d9) still lacks the universal charged FLMV transfer. Claude source research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727) is restricted alternation trading; Claude-0266 (blob 694c1c81) cautions against recoding-dependent semantic invariants. Neither proves B3. No contradiction with these peer results.

Root main.tex latest seen SHA 1652d76707fb55d51e679eb4b40551b0eec07adf returned zero bytes even on line-ranged fetch. Leave it unchanged rather than risk partial overwrite. Full repository preflight unavailable because local GitHub DNS failed. Local standalone report compiled, no full-repo build asserted.

## Next gap and specialist requests
LSPV-1: keep uniform B1/B2/B3 quantifiers and forbid a changed-input theorem as a mixed-system hardness claim. LSPV-2: charge every DEF when translating Cook internally, retain exact original LOCAL-CONVERT grammar. LSPV-4: measure bit access, output verification and peak space; output-length lower bounds apply only to explicit original Resolution proof grammar. LSPV-5: audit all-subset projection and Cook uniformity, attack the proposed charged invariant. LSPV-3 next: locate a stronger definition-charge-aware signed-hypergraph invariant that survives actual LOCAL-CONVERT/DEF rules, or produce a legal mixed inference counterexample.

Superpolynomial worst-case Wbar_Rmix341, B1, B2, B3, and P versus NP remain OPEN.
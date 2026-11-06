# LSPV-2/434: Source-authenticated mixed-sign autarky and charged virtual core port

**2026-11-05 21:12 PST | Route A LSPV-2 | PROVED/RESTRICTED + COMPUTATIONAL | Universal FLMV contraction OPEN; P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE (four original falsifiers)

Initial hypothesis: extend already established LSPV-4/429 all-positive private-tail source projection to tails with **both signs and references to core variables**. Use one **global** computable assignment to private variables to authenticate exact projection, so solver computation can be shared across children. Falsifiers: F1 inconsistent private assignments across clauses; F2 a tail that still restricts a core assignment; F3 enormous sparse IDs, duplicate literals or malformed clauses defeating low-space source authentication; F4 false transfer from a special-case port to universal FLMV contraction or historical mixed proof rules.

**Corpus correction:** LSPV-4/429 already proved a source-authenticated private-tail port for disjoint, positive private tails, LSPV-2/433 proved a certified inert-read-scan erasure, and MODELBRIDGE-0010 already established undecidability of exact reachability analysis on polynomial-time fixed-language deciders. No novelty is claimed for those results. The exact signed and core-interacting extension below is a concrete **known-autarky** instantiation with new typed controls, not a new general SAT-hardness theorem.

## Exact mathematical claim (PROVED/RESTRICTED)

For original CNF source F=G(X) & T(X,Y), X and Y disjoint, assume a single fixed assignment h:Y -> {0,1} such that **every** T-clause contains at least one Y-literal true under h. Other literals in T may be on X or Y and have either polarity. Then

$$
\forall a\in\{0,1\}^{X},\quad F(a,h)=G(a),\qquad
\operatorname{SAT}(F)\Longleftrightarrow\operatorname{SAT}(G).
$$

Every tail clause is true independently of a, so G(a) implies F(a,h). Restriction of any F-model to X proves the converse. This is the standard autarky argument with a globally consistent h. It preserves both SAT and UNSAT; it is **not** a branch-local inference with assumptions discharged for free.

### Typed read-only source format and check

Test format, **distinct from the fixed historical R_mix341 grammar**: magic bits `10101110`; unary threshold `1^b0`, b>=1; at least one proper three-literal core clause tagged `10`; then any number of proper three-literal tail clauses tagged `11`; terminal `00` and no trailing bits. Each literal is a sign bit (0 positive, 1 negative), unary identifier length `1^k0`, k>=1, then exactly k canonical ID bits beginning with 1. Three variables in each clause must be distinct. The **core** clause ID lengths are <=b, while **private** Y IDs have lengths >b. Tail clauses may contain both core and Y IDs.

Define the fixed assignment h(y)=bitlength(id(y)) mod 2. A tail is accepted only if at least one private literal is satisfied under h, namely a positive Y-literal with odd-length identifier or a negative Y-literal with even-length identifier. All other literals may have either sign. The scanner rejects missing tail witnesses, noncanonical IDs, duplicate identifiers, core clauses following tails, core/private alias attempts, incorrect markers, truncation and other malformed encodings.

To compare identifiers the scanner retains only their start offsets and lengths, and rereads the original read-only input; it does **not** store integer IDs. Three comparisons per clause imply O(N) bit-symbol examinations up to constant factor. Dense packed index registers, counters and offsets use O(log N) *highest-position writable space*. On FLMV's read-only indexed-input machine, include each source query, address/index write and clearing cost: deterministic parsing is O(N polylog N) time and O(log N) work/index space. This matches the machine description in FLMV 2005, section 2.1; this is a symbolic bit-cost construction, **not** a physical machine benchmark of the host-language Python experiment.

The exact authenticated child is source prefix through the last core clause, followed by `00`. With cut offset p its i-th bit is source[i] when i<p, constant 0 when p<=i<p+2, and the endmarker after p+2. Each virtual child-bit query requires polylog(N) native indexed steps and O(log N) dense writable scratch. No linear-size child is materialized.

## Qualified solver sharing and work/space ledger

For a fixed uniform total correct guest A for **this precise encoding** (including malformed policy), one verified projected child of length L=p+2 costs

$$
T_{\rm proj}(N)=O(N\operatorname{polylog}N+T_A(L)\operatorname{polylog}N),
\qquad
S_{\rm proj}(N)=O(\log N+S_A(L)).
$$

Given an **already constructed** stream of q source-authenticated children of length <=L all having the **same projected core bytes**, parse each, compare the core **exactly**, and invoke A once for all their labels. Time O(qL polylog N + T_A(L) polylog N); all-phase physical workspace O(log N + S_A(L)), with one live source reference, one parser and one guest frame, and streaming output. Malformed/unsupported sources are rejected or handled by a charged general-decider fallback, not silently treated as valid autarkies. All parse failures, source reads, indexed-head erasure, candidate comparisons, output, guest entry and cleanup are charged. A cached hash alone is not an authenticated equality proof.

If q<=N^(3/5+o(1)) and L<=N^(1/2+o(1)), this **conditional sharing stage** has exponent bound t'<=max{11/10,t/2} and s'<=max{1/2,s/2}. These preconditions, especially the **all-input child generator, legal join and recursive applicability**, are NOT established. A single full-source core may have L=Theta(N), so the actual finite controls below do not satisfy this asymptotic child-size condition. The stage cannot be advertised as an all-input FLMV contraction, and its local sharing is not an R_mix341 split or proof rule.

## Published-hard-family ledger, controls and transfer

**Established model-specific hard family:** odd-charge Tseitin on a growing family of connected **cubic edge expanders** with H vertices. A variable per edge gives 3H/2 variables; each vertex with charge c_v contributes four proper width-three clauses forbidding the four three-edge assignments with parity different from c_v. There are 4H clauses and an explicitly indexed encoding of length Theta(H log H). Summing all parity equations proves UNSAT iff the total charge is odd for connected graphs. Urquhart 1987 (JACM 34:209-219), Ben-Sasson and Wigderson 2001 (JACM 48:149-169) establish 2^Omega(H) **ordinary shared-DAG Resolution** lower bounds under expander-family assumptions, not for all algorithms or stronger proof systems. This encoding is *already* proper 3-CNF on cubic graphs, so no lower-bound-preservation reduction is assumed. CNFgen's `cnfgen/families/tseitin.py` implements the parity construction.

**Strong shortcut control:** Gaussian parity cancellation decides this odd-charge family efficiently; the prior project LSPV-2/341 reports a 4H-1 mixed AND3/GF(2) paid-node upper derivation on eligible bridgeless sources. That historical native checker was not rerun here; the result is retained at its reported scope, not promoted into a universal transfer.

**Finite reproductions, not growing hard expanders:** K4 H=4 (6 variables,16 core clauses); cube H=8 (12 variables,32 clauses); Petersen H=10 (15 variables,40 clauses). Six odd/even charge groups, each with 12 distinct signed-tail original-source encodings, including an odd 1025-bit sparse identifier, positive/negative private literals and core-containing tails. The odd groups are UNSAT by parity, even groups SAT. Host Python enumerated core assignments and generated 72 bit-authenticated samples: 248 assertion groups, 14 malformed or false-witness rejections, and 66 exact-core reuses (72 baseline calls -> 6 projected guest calls). Independent Node parser and truth verifier passed **74,454** assertions, including exhaustive 15-variable projected core valuations, original-string SHA checks and corrupt-label/hash controls. A separately executed compact Node semantic control passed **73,927** assertions. Largest source was 3,389 bits. The host brute-force SAT verifier is NOT a polynomial all-size algorithm or native FLMV measurement.

## Research sources and exact provenance

Read governing five-role handoff (2026-11-02, historical 4e29ed7646f484707767acb6e63ec5f38afd98a8), j15marti/pnp issue #3 through LSPV-1/434 and LSPV-4/429; root AGENTS.md (blob 19656af1), CODEX.md (754999f5), .codex/skills/pnp-research/SKILL.md (b8df83a7); LSPV-2/432 (15804464), LSPV-2/433 (fae636e6), peer LSPV-4/429 (4b369eec), historical MODELBRIDGE-0010 (8a4bf75), actual Grok GROKPROOF/2026-11-05_1913_PROGRESS.md (8a004bf), and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc72). GitHub root main.tex (blob 593000bb) returned **zero readable bytes**; it was not overwritten or purportedly reconciled. Full local project preflight was unavailable without a checkout.

Actual third-party file reads: konard/p-vs-np/proofs/complexity/README.md (7ee9a11, a different finite one-tape P/NP model), konard/p-vs-np/scripts/proof_status.json (93b77ed, explicit proof scope), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693e, bounded methods), MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd), openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f, costed specialized driver), berkeley-abc/abc/README.md (88a9d1a, AIG rewriting, not a universal SAT transfer). Read primary FLMV authors' PDF (Theorem 1.1 and section 2.1), including a screenshot of PDF page 4; checked original-source Urquhart and Ben-Sasson/Wigderson lower-bound publication statements. Searched project history for `all-input read footprint undecidable`, `semantic dead code`, `Rice no universal program normalizer`, `last input bit reachability`; a contemplated reachability theorem duplicates MODELBRIDGE-0010 and was **not** claimed. Direct Google-branded search was unavailable, so indexed web and GitHub search were used.

**Artifacts:** The GitHub compact semantic tester is a subset of the locally executed suite. The complete run archive contains the executed Python bit-parser/generator, independently executed Node parser/truth verifier, 72 exact source bitstrings and raw counters, a longer report, and SHA-256 manifest. Do not call the compact tester a replay of all 72 original bytes.

**OPEN next arrow:** Construct an effective solver-dependent, source-authenticated **all-input**, recursively applicable child generator/join for EVERY fixed total polynomial SAT decider with unknown time/space exponents, preserve both labels and malformed behavior, and meet t'<=max{11/10,3/5+t/2}, s'<=max{1/2,s/2} on the FLMV same machine with all phases paid. This authenticated special subclass does not solve that arrow. R_mix341 native minimum/B3 remain separately OPEN. P versus NP OPEN.

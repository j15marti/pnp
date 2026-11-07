# LSPV-5 independent red-team report: recursive extensions defeat the parity-guard transfer

**Pacific timestamp:** 2026-11-06 23:48 PST  
**Route:** B (`R_mix341` minimum derivation and noncircular B3)  
**Classification:** exact recursive-extension representation **PROVED/EXACT**; strict-3CNF parity control **PROVED/EXACT**; finite replay **COMPUTATIONAL**; historical accepted-byte legality, all-mixed lower bound, B3, and P versus NP **OPEN**.

## IDEA -> SEARCH -> ITERATE

Initial hypothesis: the exponential ordinary-PC parity-context guard in `[P2-L5-403]` may disappear once complement literals or paid recursive definitions are admitted, so it cannot support an all-mixed lower bound without a separate representation theorem.

Falsifiers fixed before search:

1. even parity still requires `2^(k-1)` terms when guards may be arbitrary signed linear combinations of conjunctions of positive and negative literals;
2. no linear-size recursive extension circuit represents the same guard with constant-size local definitions;
3. the compact representation requires a semantic oracle rather than local checking;
4. the construction silently changes the original strict-3CNF source instead of remaining an explicitly charged proof-side object.

Search and replay **falsified item 2** and resolved item 3 for two separately specified calculi. Recursive algebraic product definitions represent the guard with `k` three-term equations, and a Boolean XOR-prefix circuit uses `k-1` locally checkable gates. Item 4 is a typing distinction, not an automatic failure: the object is a legal upper-bound control only when the fixed calculus already permits such paid proof-side definitions. Appending the definitions as source axioms changes the source and is not allowed in a lower-bound transfer. Item 1 remains deliberately unclaimed for arbitrary signed linear combinations; the located primary CNF theorem instead proves the precise no-auxiliary clause bound and auxiliary-variable tradeoffs.

## Required tracker and continuity read

Complete trackers were read at preflight:

- `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters;
- `proof2.txt` preflight blob `ca973b434a6f07ceb258ba843ac9e112b23dc8e5`, 69,460 characters.

During the run, concurrent role-owned updates moved `proof2.txt` first to `83b3edcb3cee1730c5bdc1d16e41974b00fb37af`, 70,833 characters. The complete current blob will be refetched again immediately before any tracker write. Relevant exact IDs are `[P2-D1]`, `[P2-B1]`, `[P2-B2]`, `[P2-B11]`, `[P2-F2]`, `[P2-F8]`, `[P2-F9]`, `[P2-F10]`, `[P2-F11]`, `[P2-C1]`, `[P2-C3]`, `[P2-L3-465]`, `[P2-L3-466]`, `[P2-L3-467]`, and `[P2-L5-403]`. This run materially affects `[P2-F9]`, `[P2-C1]`, and new `[P2-L5-404]`; `proof1.txt` has no material Route-B status change.

Also read the governing five-role handoff, issue #3 body, actual LSPV-1/467 and LSPV-3/467 reports, current Grok `GROKPROOF/2026-11-07_0620_PROGRESS.md`, Claude `research/agents/claude/world-ledger/README.md`, `AGENTS.md`, `CODEX.md`, and the project research instructions. Fetching the complete issue-comment history failed twice (`Transport closed` and disabled direct-page fetch); the limitation is recorded rather than disguised as review.

## Established-family and theorem ledger

| Tracker/family | Exact encoding and size parameter | Established theorem/model | Legal shortcut used | Remaining transfer |
|---|---|---|---|---|
| `[P2-F8]`, `[P2-F9]` random strict 3-CNF | `n` variables, `m=Delta n` independently sampled indexed proper signed width-three clauses; `Theta(n log n)` explicit bits | **KNOWN/PROVED-RESTRICTED:** exponential ordinary Resolution, arbitrary-field PC, and stated bounded-DNF PCR lower bounds under published hypotheses | recursive extensions, circuits, GF(2), branching and all other historical rules remain legal | no source-authenticated retraction of every historical rule into a covered system |
| `[P2-F2]` odd cubic-expander Tseitin | `h` vertices, `3h/2` edge variables, four proper signed 3-clauses per vertex, odd total charge; `4h` clauses | **KNOWN/PROVED-RESTRICTED:** exponential ordinary DAG Resolution on suitable expanders | affine XOR summation, `[P2-L3-466]` gate projection and `[P2-L3-467]` affine split retraction are short controls | historical clause-to-row bytes and arbitrary mixed normalization remain open |
| `[P2-L3-465]` XOR prefix chain | `k` original inputs, `k-1` fresh outputs, `4(k-1)` proper 3-clauses | **PROVED/RESTRICTED:** exactly `2^k` leaves in its constant-leaf Skolem model | functional XOR circuit has only `k-1` gates | historical paid-definition grammar and mixed uses remain open |
| `[P2-L5-403]` ordinary-PC parity guard | `k` branch bits; one canonical multilinear aggregate guard | **PROVED/EXACT representation barrier:** `2^k` monomials outside characteristic two | this run supplies an `O(k)` recursive extension representation | guard-normal-form cost is not an all-mixed proof lower bound |
| Emdin--Kulikov--Mihajlin--Slezkin parity CNF | parity on `k` inputs; auxiliary count `s` | **KNOWN THEOREM:** no-auxiliary CNF needs `2^(k-1)` clauses; with auxiliaries, published lower bounds include `m>=Omega(2^(k/(s+1))/k)` and a global `m>=3k` | exact prefix-XOR strict-3CNF construction below uses `2k+1` variables and `4k` clauses for even parity | this is a representation theorem, not proof-size hardness for `R_mix341` |

Certified UNSAT, proof-size hardness and empirical solver behavior are kept separate. The finite checker certifies the stated identities and encodings, not asymptotic hardness. Haken PHP/ordinary Resolution, Cook extension shortcuts, and Tseitin GF(2) remain mandatory model-qualified controls.

## Theorem 404.1: exact linear recursive algebraic representation

Let `x_1,...,x_k` be Boolean variables and work over any field of characteristic different from two. Introduce globally fresh, acyclic extension variables `y_1,...,y_k,e` with equations

$$
y_1-1+2x_1=0,
$$

$$
y_i-y_{i-1}+2y_{i-1}x_i=0\quad(2\le i\le k),
$$

and

$$
2e-1-y_k=0.
$$

Induction gives

$$
y_i=\prod_{j=1}^i(1-2x_j)=(-1)^{x_1+\cdots+x_i},
$$

so `e=1` exactly on even parity. The definitions are uniquely evaluable in topological order. Each defining polynomial has exactly three displayed monomial terms; including the output relation, the sparse evidence contains `3(k+1)` monomial occurrences. No semantic oracle is required to check the local equations.

This is the factored version of the product that expands to all `2^k` monomials in `[P2-L5-403]`. Therefore any lower-bound transfer that charges only the expanded canonical line but permits recursive paid algebraic definitions is unsound. This does **not** show that historical `R_mix341` accepts these equations: the exact fixed grammar and byte checker remain `[P2-D1]`/`[P2-C3]` **OPEN**. It also lies outside the author-corrected nonrecursive, original-variable-only, disjoint-support PC+Ext theorem in `[P2-F10]`.

## Theorem 404.2: exact strict-3CNF Boolean representation

For a fresh output `z`, the relation `z=a XOR b` is encoded by the four proper width-three clauses

$$
(a\lor b\lor\neg z),\quad(a\lor\neg b\lor z),\quad
(\neg a\lor b\lor z),\quad(\neg a\lor\neg b\lor\neg z).
$$

Chain `k-1` such gates to obtain the prefix parity output `z_{k-1}`. To enforce even parity while keeping every source clause proper width three, replace the unit `not z_{k-1}` by fresh selectors `u,v` and the four clauses

$$
(\neg z\lor u\lor v),\ (\neg z\lor u\lor\neg v),\
(\neg z\lor\neg u\lor v),\ (\neg z\lor\neg u\lor\neg v).
$$

For `k=1`, use `z=x_1` in the output gadget. The resulting even-parity source has exactly `2k+1` variables and `4k` proper width-three clauses. An input assignment extends to a model iff its parity is even; when even, all four selector assignments work, and when odd none works. As a proof-side circuit, omit the final source-selector gadget and charge `k-1` definitions / `4(k-1)` facets.

This gives an explicit upper-bound control, consistent with the published parity-CNF theorem. It is not a lower-bound-preserving reduction from a hard source, and appending it to a source is a source modification. Inside an already authenticated paid-definition grammar it can be proof-side evidence only if every facet, freshness condition, exported wire and application/reference cost is native and charged.

## Shared branching-DAG consequence

`[P2-L3-467]` proves that both affine auxiliary branches can be projected and discharged with union-of-distinct-node accounting in its GF(2)-only model. The present result supplies the complementary representation warning outside characteristic two: a small branching-state DAG may have an exponential **expanded** guard and a linear **factored** guard simultaneously. Thus neither state count nor one chosen normal form determines the true free-optimal-choice minimum.

The legal AND obligation is unchanged. If a proof actually splits on output `z`, both contexts `Gamma,z=0 |- false` and `Gamma,z=1 |- false` must be discharged. A branch-local contradiction cannot leak. A recursive definition circuit may be shared once only where its assumption-free defining context is common; the contextual terminal work remains branch-scoped unless a native discharge theorem applies.

## Executable replay and adversarial controls

Artifacts:

- `experiments/review/lspv5_404_recursive_extension_shortcut.py`;
- `experiments/review/verify_lspv5_404_recursive_extension.mjs`;
- `results/raw/review/2026-11-06_2348_LSPV5_RECURSIVE_EXTENSION404.json`.

The Python checker exhaustively tested every input through `k=14`, every recursive product equation, every XOR2 defining facet, uniqueness of each gate output, and all four strict-output selector assignments. It passed **2,523,929 assertions**. The independent Node verifier recomputed all published counts and all `2*(2^1+...+2^14)` parity/product evaluations, passing **65,725 checks**. Nine corruptions were rejected: wrong product sign, reused output, forward-reference cycle, nonfresh output, missing XOR facet, source/paid tag confusion, missing recursive definition, missing strict-output facet, and false all-mixed scope.

This is an independent checker, not execution of the authoritative historical checker. An unavailable `/usr/bin/time` wrapper failed immediately. The initial exhaustive `k=18` policy then ran for about three minutes without completing and was interrupted; the successful bound was reduced to `k=14`. Both failures are charged below.

## Resource ledger

| Phase | Charged result |
|---|---|
| logical nodes | no historical node count claimed; algebraic control has `k` definitions plus one output relation; Boolean proof-side control has `k-1` XOR2 definitions |
| explicit evidence | algebraic `3(k+1)` monomial occurrences; Boolean gate facets `4(k-1)` clauses / `12(k-1)` literal occurrences; strict even source `4k` clauses |
| construction/search | deterministic formulas and topological checks; no SAT/equivalence oracle |
| parsing/source/index/head reads | complete trackers, governing files, issue body, peer/Grok/Claude files, repository heads and actual selected files |
| successful verification | Python 2,523,929 assertions in 26.49 s wall; Node 65,725 checks in 0.008 s |
| process peak | Python `ru_maxrss` 13,184 KiB; tracemalloc peak 32,016 bytes in the final replay |
| failed policies | missing `/usr/bin/time`; interrupted exhaustive `k=18` attempt after about three minutes |
| caches/recomputation | Python materialized only one assignment/gate state at a time; Node independently reread JSON and recomputed semantics |
| output/update | code, raw JSON, report, handoff, fallback fragment, exact tracker outbox, remote writes and readbacks charged separately |
| global simultaneous peak | not measured across local processes and remote connectors; no smaller aggregate bound claimed |

No Route-A exponent, same-machine conversion, or `s'` bound is inferred.

## Primary literature and repository authentication

Primary sources read:

- Emdin, Kulikov, Mihajlin and Slezkin, **CNF Encodings of Parity**, MFCS 2022, DOI `10.4230/LIPIcs.MFCS.2022.47`: exact no-auxiliary `2^(k-1)` clause minimum and auxiliary-variable lower bounds.
- Impagliazzo, Mouli and Pitassi, **Lower Bounds for Polynomial Calculus with Extension Variables over Finite Fields**, CCC 2023, DOI `10.4230/LIPIcs.CCC.2023.7`: model-qualified finite-field PC+Ext lower bounds; corrected scope is recorded in `[P2-F10]`.
- Alekseev, **A Lower Bound for Polynomial Calculus with Extension Rule**, Theory of Computing 22(4), 2026, DOI `10.4086/toc.2026.v022a004`: arbitrary-depth algebraic extensions exist as a stronger-system control, but the hard BVP source is nonpropositional and supplies no strict-3CNF transfer.

Change-aware repository heads were unchanged from the preceding run: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, `meelgroup/frat-xor` `18cd6bc...`, `tanyongkiam/cake_lpr` `033aad53...`, `peitl/short-proof` `2c524cfc...`, `MassimoLauria/cnfgen` `24e633bd...`, `msoos/cryptominisat` `ed61e217...`, `openai/math` `4eaee875...`, and `anthropics/formal-math` `16a5ce413...`. Actual `proof_status.json` blob `93b77ed...`, `METHOD_INDEX.md` blob `18d693...`, FRAT-XOR `format.md` blob `986a21...`, CakeLPR README blob `e94f45...`, short-proof README blob `93d209...`, CryptoMiniSat README blob `763698...`, OpenAI math README blob `cc5b0a...`, and Anthropic formal-math README blob `1df53b...` were read. CNFgen `README.md` returned 404, although its repository head was authenticated. Repository claims, CI and formalization badges were not treated as P-versus-NP proofs. Google-branded search was unavailable; ordinary primary-source web search was used.

## Revised status and precise gap

**Actual advance:** `[P2-L5-403]` is now paired with an exact, linear-size legal-candidate shortcut. The same parity context needs `2^k` terms when materialized as the canonical ordinary multilinear guard, yet only `3(k+1)` sparse terms in an acyclic recursive algebraic extension circuit, or `4(k-1)` proper 3-CNF gate facets as a Boolean proof-side circuit. Any all-mixed lower-bound argument must defeat or legally retract these compact representations rather than price only the expansion.

**Still open:** authenticate the exact historical `R_mix341` paid-definition grammar, exported/private wire semantics, accepted bytes, freshness, source identity and weights; prove a lower-bound-preserving retraction covering recursive extensions and every other mixed rule, or exhibit a legal native counterexample; and prove a noncircular same-system B3 bridge. No restricted theorem here establishes superpolynomial `Wbar_Rmix341`, arbitrary-machine SAT hardness, or P versus NP.

## Publication and readback

The report, code, independent verifier, raw JSON, handoff and fallback TeX fragment were published to `main` and each received an exact full-content readback. The exact pre-write tracker outbox was saved at `research/coordination/outbox/2026-11-06_2348_LSPV5_PROOF2_404_OUTBOX.json` before the tracker mutation. `proof2.txt` was refetched at base blob `83b3edcb3cee1730c5bdc1d16e41974b00fb37af`, updated conflict-safely, and its complete 73,742-character result read back exactly at blob `8d2866225be02dc79b73f26724279f9558d3d9f5`. `proof1.txt` was not changed.

Issue #3 accepted comment ID `6704236861` naming `[P2-F9]`, `[P2-C1]` and `[P2-L5-404]`. The connector returned the ID but not the body, and two full-history readback attempts failed with `Transport closed`; therefore complete remote comment-body readback is **not claimed**. The exact posted body is preserved durably at `research/coordination/outbox/2026-11-06_2348_LSPV5_ISSUE3_404_COMMENT.md`. Root `main.tex` was a complete zero-byte blob (`68188a24badda635a5983fda1c381cdb694fd497`) and was not modified; the role-owned fallback fragment was published instead.


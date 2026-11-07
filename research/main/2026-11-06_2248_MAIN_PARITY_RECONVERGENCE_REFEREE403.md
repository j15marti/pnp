# LSPV-5 independent red-team report: parity reconvergence is representation-sensitive

**Pacific timestamp:** 2026-11-06 22:48 PST  
**Route:** B (`R_mix341` minimum derivation and noncircular B3)  
**Classification:** exact ordinary-PC guard-normal-form barrier **PROVED-RESTRICTED**; finite validation **COMPUTATIONAL**; historical mixed transfer, all-rule lower bound, B3, and P versus NP remain **OPEN**.

## IDEA -> SEARCH -> ITERATE

Initial hypothesis: a two-state parity branching DAG has only `O(k)` control states, but aggregating all compatible branch contexts into one ordinary-PC guard over characteristic not two requires exponentially many multilinear monomials.

Falsifiers fixed before search:

1. the even-parity context indicator has a polynomial-size multilinear representation over characteristic not two;
2. complement variables in PCR collapse the aggregate guard to polynomial monomial count without an affine rule;
3. a nonmultilinear representative avoids the lower bound modulo the Boolean ideal;
4. the obstruction persists over characteristic two, contradicting the expected GF(2) shortcut.

Search and peer review changed the claim. Current `[P2-L3-466]` proves that authenticated affine gate retraction is nonexpansive inside a GF(2)-only shared DAG. Primary literature authenticates uniqueness of Boolean multilinear representations and the characteristic-sensitive parity collapse. Falsifiers 1, 3, and 4 are resolved below. Falsifier 2 is intentionally left open for arbitrary PCR derivations: only the explicit leaf-guard sum is costed.

## Required tracker and continuity read

Complete trackers read at the start:

- `proof1.txt` blob `9273776e5ac0c9a4940b8c3e404d98ed5b205202`, 17,530 bytes;
- `proof2.txt` blob `d46016c3ed0ecf5c3812c3f42e668e4d02b089a2`, 60,166 bytes.

Relevant exact nodes: `[P2-D1]`, `[P2-B1]`, `[P2-B2]`, `[P2-B9]`, `[P2-B10]`, `[P2-F2]`, `[P2-F8]`, `[P2-F9]`, `[P2-C1]`, `[P2-C3]`, `[P2-L3-465]`, `[P2-L3-466]`, and `[P2-L5-402]`. This run materially affects `[P2-F9]`, `[P2-C1]`, and new `[P2-L5-403]`; `proof1.txt` has no material Route-B change.

Also read: the governing five-role handoff; current issue #3 body and latest comment page; current LSPV-1/466, LSPV-2/461, LSPV-3/466, and LSPV-4/459 reports and code; current Grok `GROKPROOF/2026-11-07_0620_PROGRESS.md`; Claude `research/agents/claude/world-ledger/README.md`; `AGENTS.md`; `CODEX.md`; and the project research instructions. No chat summary was substituted for these files.

## Established-family and control ledger

| Tracker/family | Exact encoding and parameter | Established result and model | Known shortcut/control used here | Remaining transfer |
|---|---|---|---|---|
| `[P2-F8]`, `[P2-F9]` random strict 3-CNF | `n` variables and `m=Delta n` independently sampled proper width-three clauses in the cited indexed model; explicit source length `Theta(m log n)` | **KNOWN/PROVED-RESTRICTED:** exponential ordinary Resolution and PC/PCR lower bounds under the published field/density hypotheses | branching, algebra, extensions, sharing remain legal; `[P2-L5-402]` handles one PC split | no theorem covers every historical mixed rule or arbitrary reconvergent context sharing |
| `[P2-F2]` odd-charge cubic-expander Tseitin strict 3-CNF | `h` vertices, `3h/2` edge variables, four width-three clauses per vertex, odd charge | **KNOWN/PROVED-RESTRICTED:** exponential Resolution for suitable expanders; affine summation is short in GF(2) | `[P2-L3-466]` gives nonexpansive affine-gate projection in its authenticated GF(2)-only model | historical clause-to-row bytes, mixed RES/AND/LOCAL/branch rules remain open |
| `[P2-L3-465]` XOR prefix chain | `k` original inputs, `k-1` fresh outputs, `4(k-1)` proper 3-clauses | exact `2^k` constant-section leaves despite a linear Skolem circuit | direct affine projection avoids leaf enumeration in `[P2-L3-466]` | auxiliary branch assumptions retract to parity contexts, not literals |
| this run's parity state control | `k` branch bits; two parity states per level | **PROVED-RESTRICTED:** `1+2k` states and `4k-2` edges, but exact ordinary-PC even-context normal form has `2^k` monomials in characteristic not two | over GF(2), the same indicator has `k+1` monomials | not a hard formula and not an arbitrary proof lower bound |

Certified UNSAT, proof-size hardness, and empirical difficulty are not conflated. The finite parity object is a representation/certificate control. `[P2-F8]`/`[P2-F9]` and expander Tseitin supply model-qualified proof lower bounds. No solver runtime is used as hardness evidence.

## Theorem 403.1: exact parity guard normal form

Let `E_k:{0,1}^k -> {0,1}` be the even-parity indicator. Work over a field `F` of characteristic not two, with ordinary Boolean axioms `x_i^2-x_i=0`. Every Boolean-cube function has a unique multilinear representative modulo these axioms. For parity,

$$
E_k(x)=\frac{1}{2}\left(1+\prod_{i=1}^k(1-2x_i)\right).
$$

Expanding gives coefficient `1` for the empty monomial and, for every nonempty subset `S`,

$$
[x_S]E_k=(-1)^{|S|}2^{|S|-1}.
$$

All these coefficients are nonzero in every field of characteristic different from two. Therefore the unique multilinear normal form contains exactly `2^k` monomials. Any nonmultilinear polynomial agreeing with `E_k` on the Boolean cube reduces modulo `x_i^2-x_i` to this same normal form.

Over `F_2`, by contrast,

$$
E_k(x)=1+x_1+\cdots+x_k,
$$

so the unique normal form contains `k+1` monomials. This matches the qualitative field distinction in the primary literature and the project-specific nonexpansive affine retraction `[P2-L3-466]`.

## Corollary 403.2: precise branching-DAG limitation

The layered parity state graph has one initial state and two states after each input bit: `1+2k` nodes and `4k-2` directed transition edges. The unrolled assignment tree has `2^k` leaves, half even and half odd.

Suppose a proposed ordinary sparse-monomial PC branch normalizer over characteristic not two reconverges every even branch by materializing one canonical multilinear guard line that is true exactly on the even contexts. The theorem forces that line to contain `2^k` monomial occurrences. Thus this specific normalizer cannot have overhead polynomial in the unlabelled two-state search DAG.

This does **not** prove that arbitrary PC, PCR, Extended Resolution, circuit, GF(2), or historical mixed refutations are exponential. A proof can avoid materializing the aggregate guard; extension variables can retain the factored product; GF(2) is linear; and PCR complement variables may permit a different cancellation-based derivation. The explicit PCR leaf construction from `[P2-L5-402]` uses `2^(k-1)` even path-guard monomials, but no minimality theorem for arbitrary PCR representations is claimed here.

The result therefore sharpens context accounting: a repeated search state is not automatically one reusable proof node. Either its antecedent contexts are legally discharged into a representation whose actual size is charged, or each incompatible `(context,node)` incidence remains distinct.

## Executable validation and adversarial controls

Artifacts:

- `experiments/review/lspv5_403_parity_guard_barrier.py`, SHA-256 `57c9b98a9a1c39ba12d269f6b601ce83a15e57cd2965dfccb3c6e8fe850a201d`;
- `experiments/review/verify_lspv5_403_parity_guard.mjs`, SHA-256 `e094ec0e987a8651cb4c46a250c051e92efede1cb0446c49ed53e22935b3a9be`;
- `results/raw/review/2026-11-06_2248_LSPV5_PARITY_GUARD403.json`, SHA-256 `26b23364615adfe19fd719f719934b9db63fded75ebc76d684d158c4eddd3c63`.

For every `k=1,...,16`, the Python checker:

- derived the coefficients by Boolean-lattice Mobius inversion through `k=12` and checked the closed form through `k=16`;
- evaluated the complete truth table by subset-zeta transform;
- verified all `2^k` coefficients remain nonzero modulo 3, 5, 7, and 11;
- verified the characteristic-two `k+1`-monomial form;
- checked exact state-DAG and context-tree counts.

It passed 270,448 checks. At `k=16`, the counts are 65,536 monomials outside characteristic two and 17 in characteristic two. Five corruptions were rejected: wrong coefficient, omitted monomial, omitted even context, negative exponent, and a false characteristic-two exponential claim. The independent Node verifier passed 200 checks.

This is an independent mathematical checker, not an execution of an authoritative historical checker. The first validation policy evaluated every monomial on every assignment and exceeded 30 seconds before producing an artifact; it was replaced by the exact `O(k2^k)` zeta transform. That failed policy is charged below rather than hidden.

## Resource ledger

| Phase | Charged result |
|---|---|
| logical nodes | theorem about representation; no `R_mix341` paid-node count claimed |
| explicit evidence bits | Python 6,628 bytes; Node 1,351 bytes; raw JSON 7,628 bytes |
| construction/search | deterministic coefficient generation, Mobius inversion, zeta evaluation; no SAT/equivalence oracle |
| parsing/source/index/head reads | complete trackers, governing files, peer reports/code, issue body/latest page, repository heads and selected actual files |
| verification | 270,448 Python checks; 200 independent Node checks; five negative controls |
| successful host time | Python 21.699 s recorded in raw output; Node about 0.006 s |
| failed policy | naive `4^k` truth evaluation consumed the 30 s command window and emitted no artifact |
| peak space | Python tracemalloc peak 7,842,111 bytes; process maximum RSS 35,584 KiB; Node/connector peaks not merged into this number |
| caches/retrieval/recomputation | coefficient dictionaries and zeta arrays retained during each `k`; Node recomputed every published closed-form count |
| updating/output | report, code, raw result, handoff, exact outbox, tracker write and issue comment charged as separate remote phases |
| simultaneous all-phase peak | not measured across local process and remote connector; no smaller global peak claimed |

This is not a Route-A transformation and gives no `s'<=max{rho,eta,lambda,lambda*s}` exponent claim.

## Source and repository authentication

Primary sources read:

- Gopalan, Lovett, and Shpilka, ECCC TR09-048, state uniqueness of the polynomial representation of Boolean functions over each prime field and study characteristic changes.
- O'Donnell's MIT thesis, Definition 5.5.2 and Fact 5.5.5, explicitly records unique multilinear representation, parity linearity over `F_2`, and degree `k` over the reals.
- The PC/PCR lower-bound sources already authenticated under `[P2-F9]` remain the model source for sparse monomial size; this report does not replace them with a survey assertion.

Change-aware repository review found no head changes since the previous run in the required and selected control repositories: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, `meelgroup/frat-xor` `18cd6bc...`, `tanyongkiam/cake_lpr` `033aad53...`, `peitl/short-proof` `2c524cfc...`, `MassimoLauria/cnfgen` `24e633bd...`, `msoos/cryptominisat` `ed61e217...`, `openai/math` `4eaee875...`, and `anthropics/formal-math` `16a5ce413...`. Actual `proof_status.json`, `METHOD_INDEX.md`, FRAT-XOR format, and relevant README files were reread. Repository claims and CI status were not treated as proof authority. Google-branded search was unavailable; primary-source web search was used.

## Revised status and remaining gap

**Actual advance:** the naive inference “small reconvergent search-state DAG implies a small ordinary-PC aggregate context guard” is false in characteristic not two. The exact cost is `2^k` monomials for parity, while GF(2) has `k+1`. This is a representation-aware counterexample to one proposed shared-context compilation step, not a lower bound on the optimal mixed proof.

**Still open:** authenticate the historical `R_mix341` grammar and weights; determine whether legal GF(2), paid definitions, PCR complements, or other mixed rules always supply compact context discharge on the established random strict-3CNF family; prove an all-rule superpolynomial minimum; and independently prove noncircular same-calculus B3. P versus NP remains **OPEN**.

## Publication limitation

Root `main.tex` blob `68188a24badda635a5983fda1c381cdb694fd497` returned zero content bytes. No root edit was attempted because complete outside-byte preservation was impossible. The dated Markdown report and fallback fragment are the durable publication path.

## Publication verification

The report, handoff, fallback fragment, Python checker, independent Node verifier, raw JSON, and exact pre-write outbox were created on `main` and completely read back byte-for-byte. `proof2.txt` was updated conflict-safely from blob `d46016c3ed0ecf5c3812c3f42e668e4d02b089a2` to `67fc915249a6f2667b7d85feaedc7853b884ec86`; its complete post-write content exactly matched the saved outbox. `proof1.txt` was reviewed and unchanged at blob `9273776e5ac0c9a4940b8c3e404d98ed5b205202`. Issue #3 comment `6703677402` was fetched directly and matched the exact comment outbox. No task, title, schedule, role, historical weight, or root manuscript byte was changed.

# EXPONENTIAL-OVERHEAD-TRANSFER-CEILING-REFEREE321

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 13:48 PST**

**Outcome.** A concrete inference used by the current Haken/Braun transfer program is now sharply delimited. An exponential source-system lower bound combined with a back-translation that loses an exponential factor in a paid escape budget `e <= O(q)` can force only `q = Omega(log L)`. For Haken unary PHP and Braun bit-PHP, `log L` is only `N^(1/3-o(1))` in the encoded input length. Thus these inequalities yield meaningful polynomial restricted-fragment lower bounds but, by themselves, cannot yield the required superpolynomial full-`Rmix341` minimum. This is a transfer-ceiling theorem, not a lower bound for unrestricted SAT computation. B1, B2, B3 and P versus NP remain **OPEN**.

## Fixed system, cost, and target

The preselected calculus remains source-authenticated `Rmix341`: free original CNF leaves; paid binary-premise RES, exact AND3/factor steps, arbitrary-width GF(2) row addition, LOCAL-CONVERT, and paid conservative signed AND2-VARDEF; one unit per distinct paid inference node in the shared contradiction DAG. `W_R(F)` grants free selection of the best legal DAG. Proof discovery, encoding size, checking work and scheduled machine space are recorded separately. No rule, encoding, task, state, owner or schedule changed.

The target remains a superpolynomial `Wbar_R(N)` for this same full calculus plus the weakest sufficient bridge B3:

`SAT in P  =>  Wbar_R(N) is polynomial in N`.

## Established lower bounds used first

1. **Haken (1985), KNOWN THEOREM.** For standard unary `PHP_(h+1)^h`, every unrestricted shared-DAG ordinary Resolution refutation has `2^(Omega(h))` lines. The canonical signed-DIMACS encoding has `N_h = Theta(h^3 log h)` bits. The theorem is about ordinary Resolution, not Extended Resolution, `Rmix341`, or arbitrary SAT machines. Haken's abstract also records that Extended Resolution has polynomial proofs.
2. **Braun (2026), EXTERNAL PREPRINT CLAIM.** For `n=2^ell`, `ell>=32`, every unrestricted DAG `Res(XOR)` refutation of the standard wide bit-PHP source has more than `exp(n/(32768 ell^2))` clauses, including original clauses. The source has `m=n*binom(n+1,2)` pair clauses of width `2ell` and ASCII-DIMACS length `N=Theta(n^3 ell^2)`. The paper reports Lean 4 formalization; this run did not kernel-replay it or claim external specialist review.
3. **Cook (1976) / Cook--Reckhow context, KNOWN.** Pigeonhole principles admit polynomial Extended Resolution proofs. This is the mandatory shortcut control: a lower bound for Resolution or `Res(XOR)` does not automatically survive extension rules.

Primary sources checked this run:

- Haken, *The intractability of resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`.
- Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv `2609.23015`, Theorem 1.1 as summarized on the primary arXiv page.
- Cook, *A short proof of the pigeon hole principle using extended resolution* (SIGACT News 8(4), 1976), and Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems*.

## Falsifiers posed

1. **F1: exponential source hardness plus `64^d` elimination forces superpolynomial mixed proof size.** Falsified as an inference from that inequality alone.
2. **F2: a linear paid-gate lower bound is already superpolynomial in encoded length.** Falsified: `h = Theta((N/log N)^(1/3))` for unary PHP.
3. **F3: Braun's local-profile threshold is a q-only full-`Rmix341` lower bound.** Falsified for the stated compiler: the unbounded semantic support `d_*` and named internal LOCAL-CONVERT wires are not controlled by `q`; even adding a linear control yields only `q=Omega(N^(1/3)/polylog N)`.
4. **F4: the stream-converter space result enters the square-root FLMV contradiction.** Falsified numerically: `Omega(h)=Omega((N/log N)^(1/3))` is below `N^(1/2)`. It is also a restricted proof-output converter theorem, not B3.

## PROVED/EXACT transfer-ceiling lemma

Let `Q` be a proof system and let `F_N` be an UNSAT family with

`L_Q(F_N) > 2^(H_N)`.

Suppose a restricted `R` proof `pi` of paid-node cost `q` and escape budget `e(pi)` is compiled, on the identical source, into a `Q` proof satisfying

`L_Q(F_N) <= 2^(a e(pi)) P(N,q)`,

where `a>0` is fixed, `P` is a fixed polynomial at least one, and `0 <= e(pi) <= c q` for fixed `c`. Then every such proof satisfies

`H_N < a c q + log_2 P(N,q)`.                                                    (1)

If `H_N=N^(alpha+o(1))` for fixed `alpha>0`, (1) implies only `q=Omega(H_N)`: if `q=o(H_N)`, then `log P(N,q)=o(H_N)`, contradicting (1). The inequality is numerically compatible with `q=Theta(H_N)` and `e=Theta(H_N)`; for example, when the overhead is `64^e=2^(6e)`, choosing `q=e=ceil(H_N/6)` already pays the complete exponential source lower bound. Therefore (1), without an independent sublinear escape-budget theorem or a substantially cheaper compiler, cannot exclude polynomial-size `R` proofs.

This does not assert that such proofs actually exist. It proves that the transfer inequality alone cannot rule them out.

## Applications to the current peer transfers

### Haken / LSPV-1 HAKEN-EXTENSION-BUDGET371

LSPV-1 proves in the proper ER2 subgrammar

`L_Res(F) <= 64^d (m+4q+1)`, with `d<=q`.

Together with Haken this gives `q=Omega(h)` (and more specifically a gate-budget tradeoff), hence at most

`q = Omega((N/log N)^(1/3))`

from this arrow. That is a real restricted-fragment polynomial lower bound, not superpolynomial `Wbar_Rmix341`. Cook's short ER proofs are consistent with `d=Theta(h)` or larger.

### Braun / LSPV-2 NATIVE-AFFINE-LOCAL-PROFILE370

LSPV-2 proves for its locally opaque/extensional subgrammar

`S_ResXor(F) <= 2^(b+d_*) (2m+2q+2)`.

Braun conditionally yields

`b+d_*+log_2(2m+2q+2) > n/(32768 ell^2 ln 2)`.

This is not q-only because `d_*` and full named-wire circuit payloads are not bounded by paid nodes. Even if a future typing theorem supplied `b+d_*=O(q)`, the consequence would be only

`q=Omega(n/ell^2)=Omega(N^(1/3)/(log N)^(8/3))`,

again polynomial in `N`. A superpolynomial conclusion would require a compiler whose overhead is polynomial in `q,N`, or an independent theorem forcing the escape profile to be `o(H_N)` on every short proof, and it would still cover only the rules actually compiled.

### LSPV-3 and LSPV-4

LSPV-3 BALANCED-DEPTH-NONTRANSFER373 correctly shows that a polynomial size/depth compiler from the short mixed Tseitin proofs to ordinary Resolution cannot exist. This is a nontransfer to a weaker system, not mixed hardness.

LSPV-4 HAKEN-STREAM-SPACE369 correctly derives an output-converter obstruction under read-only input, append-only unreadable output, fixed heads and standard work space. Its configuration count requires `s` to bound the entire visited/scanned work region; if `s` meant only nonblank cells, head positions would not be bounded by `(s+2)^k`. Under the standard intended definition, the result is soundly restricted and gives exponent `1/3-o(1)`, not a square-root-space contradiction.

## Grok and Claude folder audit

The actual repository folders were located and read, not guessed.

- `GROKPROOF/2026-11-03_2114_PROGRESS.md` (blob `4996f047...`) and predecessor `2026-11-03_1912_PROGRESS.md` (`dbec4959...`) explicitly keep the universal all-input fully charged FLMV transformation **OPEN**. Their numerical forbidden-region checks do not construct B3.
- `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex` (`d06a2d56...`) is a circuit-rewriting optimization study and explicitly moves no lower bound.
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`) proves sequential/one-tape crossing-sequence restrictions that do not transfer to the indexed random-access target and apply to nondeterminism as well.
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727...`) is a restricted alternation-trading portfolio theorem, not B3 or a proof-minimum compiler.
- `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` (`694c1c81...`) contains a material affine overclaim already independently countered in project history by `f(x,y)=xy` and annihilator `1+x`; it is not used here.

No reviewed Grok or Claude artifact supplies a full-rule mixed lower bound or B3.

## Current peer versions assessed

- LSPV-1 `research/agents/lspv-1/2026-11-03_1306_LSPV-1_HAKEN_EXTENSION_BUDGET371.tex`, blob `816da1eb...`.
- LSPV-2 `research/agents/lspv-2/2026-11-03_1312_LSPV-2_NATIVE_AFFINE_LOCAL_PROFILE370.tex`, blob `343d9dad...`.
- LSPV-3 `research/agents/lspv-3/2026-11-03_1324_LSPV-3_BALANCED_DEPTH_NONTRANSFER373.tex`, blob `83406eb4...`.
- LSPV-4 `research/agents/lspv-4/2026-11-03_1333_LSPV-4_HAKEN_STREAM_SPACE369.tex`, blob `87559656...`.

## Computational controls and cost ledger

The Python producer and independently written Node verifier passed:

- 29 producer assertion groups and 49 verifier checks;
- normalized Haken overhead witnesses through `H=512`;
- Braun threshold arithmetic for `ell=32,33,34,36,40` using 90-digit decimal arithmetic;
- unary PHP `h=1,2,3`: zero models, with a deleted pigeon-source clause yielding SAT controls;
- K4 Tseitin odd/even controls: `0/8` models;
- eight malformed DIMACS strings rejected.

Producer wall time was 0.0221 s and peak host RSS 9,216 KiB. These are host diagnostics, not FLMV machine bounds. The experiment does not search for proofs or certify any asymptotic proof minimum. Proof optimizer discovery remains uncharged to `W_R` by definition.

Artifact SHA-256:

- producer `77071726e8a55fee0d83c22c525757cbe17443d0b70a16ccd8db788576bf6669`;
- independent verifier `b033bff8864cb9885b9d992d6198efcd367be0079638859edae28aa28ce3e843`;
- raw JSON `4b01a7742deb0f75e7ecc08d163a51767093c80f4af325fc0b4a1c8da7e4874e`.

The repository checkout and required local preflight were unavailable in this workspace; all corpus reads used authenticated GitHub contents/blob readback. No full-repository test or native checkout benchmark is claimed. A github.com/openai search for Resolution/`Res(XOR)` proof checkers returned one unrelated cookbook notebook and no matching compiler.

## Bridge classification

| Obligation | Result |
|---|---|
| Superpolynomial full-`Rmix341` `Wbar_R` | **OPEN**; current exponential-overhead compilers top out at polynomial q lower bounds. |
| B1 | **OPEN**; no arbitrary correct decider-to-proof simulation. |
| B2 | **OPEN**; no worst-case domination for every correct decider. |
| B3 | **OPEN**; neither proof-system compilation nor Grok/Claude resource restrictions establish it. |
| P versus NP | **OPEN**. |

## Exact next gap

The next useful arrow is not another formula family. It is either:

1. a same-source compiler covering **every** full `Rmix341` rule with overhead polynomial in `(N,q)` rather than exponential in an `O(q)` escape budget; or
2. a direct invariant proving that every short full mixed proof has escape budget `o(H_N)` while controlling named internal wires and LOCAL-CONVERT; and separately
3. a noncircular proof of B3 for the same fixed calculus.

Until then, the established Haken/Braun lower bounds remain valuable restricted anchors but do not transfer to unrestricted SAT computation.

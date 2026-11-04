# PREFIX-ALIGNED-B2-INVARIANCE-REFEREE339

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 07:48 PST**

**Status:** **PROVED/EXACT, REPRESENTATION-RESTRICTED:** B2 truth is invariant under uniform, polynomial-time, canonical syntactic encodings whose valid-source prefixes are polynomially aligned in both directions. **PROVED/EXACT COROLLARY:** the square-padding code below preserves B2 despite sparse-delay counterexamples to naive same-machine time rescaling. **PROVED/FINITE:** 2,939 independent implementation assertions pass. **OPEN:** B1/B2/B3 for fixed `R_mix341`, a superpolynomial `Wbar_Rmix341`, algorithm-independent SAT hardness, and P versus NP. No task, schedule, enabled state, ownership, calculus rule, or weight was changed.

## Outcome

LSPV-1/391 correctly proved B1/B3 invariance under mutual polynomial syntactic encodings and B2 invariance at equal lengths, then correctly falsified the tempting same-program inequality

`T_A^wc(N^2) <= poly(N + T_A^wc(N))`.

That delay counterexample does **not** block B2 invariance for exact monotone padding. The repaired proof never rescales one arbitrary program's clock. It translates each arbitrary decider into one fixed wrapper decider and compares cumulative worst-case time at matched cutoffs.

The new exact result is:

> If two canonical encodings represent the same authenticated source-labelled CNF and leave the same fixed `W_R(F)`, their valid-image prefix sets align in both directions through polynomial cutoffs, and parsing/conversion is uniform polynomial time, then B2 holds for one encoding iff it holds for the other.

This is a genuine encoding-transfer theorem, but only an elementary robustness theorem. It does not prove B2 for `R_mix341`, does not transfer any Resolution lower bound to arbitrary computation, and does not support P != NP.

## Exact obstruction and four falsifiers

1. **Mutual polynomial length balance alone proves B2 invariance. — NOT PROVED.** Irregular valid-image prefixes need not align; arbitrary sparse delays forbid replacing alignment by a same-machine scaling estimate.
2. **The LSPV-1/391C delay machine refutes square-padding B2 invariance. — FALSE.** Its delayed padded cutoff appears on the padded decider's own B2 right-hand side, and transported source calls never cross that cutoff prematurely.
3. **Any semantic CNF padding is merely a syntactic recoding. — FALSE.** Adding clauses, variables, axioms, or a recognizable-family shortcut can change the authenticated source and `W_R`; the theorem requires the identical abstract source root and calculus cost.
4. **Lazy zero padding makes conversion and validation free. — FALSE.** Forward lazy access pays address translation and simulated access. Reverse validation of a materialized padded input must distinguish every one-bit corruption and therefore reads `Omega(N)` bits in the ordinary deterministic query model.

No new hard formula was generated and no published lower bound was regenerated.

## Published lower-bound anchor: exact model, encoding, quantifiers, strength

For `h` holes and `h+1` pigeons, canonical unary `PHP(h+1,h)` has Boolean variables `x_(i,j)`, one width-`h` positive pigeon clause per pigeon, and one binary negative collision clause for every pair of pigeons and hole. It has `h(h+1)` variables and `Theta(h^3)` explicit clauses. With ordered signed binary variable indices its bit length is `N_h=Theta(h^3 log(h+2))`.

Haken's theorem says that constants `c>0,h0` exist such that for every `h>=h0`, every ordinary Resolution refutation of this explicit CNF has at least `2^(c h)` clauses/lines. The proof system uses source clauses plus the binary resolution rule on a complementary pivot; arbitrary clause width, pivot choice, and DAG reuse are allowed. It does not allow GF(2) rows, extension variables, circuit gates, semantic jumps, Horn/2-SAT procedures, or arbitrary machine computation.

Thus the statement is `2^Omega((N_h/log N_h)^(1/3))` ordinary-Resolution proof hardness. It is not a `Res(XOR)`, Extended Resolution, `R_mix341`, or all-algorithm SAT lower bound. The exact reference is A. Haken, *The Intractability of Resolution*, Theoretical Computer Science 39 (1985), 297–308, DOI `10.1016/0304-3975(85)90144-6`. The theorem and standard encoding were cross-checked against Ronald de Wolf's Resolution notes, `https://homepages.cwi.nl/~rdewolf/resolutionlowerbound.pdf`, Theorem 4.13.

The relevant Cook–Reckhow distinction remains: polynomial simulations compare encoded proof systems and proof lengths; they do not make a preselected proof system polynomially simulate every arbitrary correct SAT decider.

## Four-layer separation

| layer | object | what is preserved here |
|---|---|---|
| abstract source | ordered, labelled CNF `F` | exactly the same `F` |
| logical calculus | fixed `R`, derivation DAG, `W_R(F)` | exactly the same value |
| serialization | canonical images `e_0(F),e_1(F)` and cutoff prefixes | polynomially recognizable and prefix aligned |
| computation | one uniform total decider and cumulative `T_A^wc(N)` over all strings of length `<=N` | transported by a different fixed wrapper, with every cost charged |

Conflating the last two layers caused the naive scaling failure. Conflating the first two with serialization would incorrectly admit semantic source padding.

## Theorem: bidirectional prefix-aligned B2 invariance

Fix one abstract valid-CNF domain `D`, one fixed sound effective calculus `R`, and two injective canonical encodings `e_0,e_1`. Define

`S_i(N) = { F in D : |e_i(F)| <= N }`

and

`Wbar_i(N) = max { W_R(F) : F in S_i(N), F UNSAT }`,

with the empty maximum zero. Assume:

1. each canonical image is recognizable and decodable in polynomial time, with every malformed or noncanonical string rejected;
2. fixed uniform polynomial-time converters map `e_0(F)` to `e_1(F)` and back, preserving the exact authenticated source-labelled `F`;
3. polynomially bounded functions `a,b` satisfy, for all cutoffs,
   `S_1(N)=S_0(a(N))` and `S_0(M)=S_1(b(M))`;
4. conversion, output, access translation, parsing, validation, and universal-simulation overhead are polynomial and charged;
5. `T_A^wc(N)` is cumulative over **all** strings of length at most `N`, including malformed strings.

Then B2 for `(R,e_0)` is equivalent to B2 for `(R,e_1)`.

### Direction `e_0 -> e_1`

Fix an arbitrary uniform total correct `e_1` decider `A_1`. Construct one fixed `e_0` decider `A_0`: reject malformed `e_0` strings in polynomial time; on a valid `e_0(F)`, convert to `e_1(F)` and run `A_1`.

For all inputs in the valid `e_0` prefix `S_0(a(N))=S_1(N)`, converted lengths are at most `N`. Malformed inputs are handled by the wrapper. Hence one polynomial `h`, depending on the fixed wrapper but not on `N`, satisfies

`T_A0^wc(a(N)) <= h(N + T_A1^wc(N))`.

Using B2 for `e_0` and exact source-prefix equality,

`Wbar_1(N)=Wbar_0(a(N)) <= p_A0(a(N)+T_A0^wc(a(N))) <= q_A1(N+T_A1^wc(N))`.

This has the required B2 quantifier order: for every fixed `A_1`, one fixed polynomial `q_A1` works for every `N`. There is no `A_N`, advice, or per-cutoff optimizer.

### Direction `e_1 -> e_0`

Fix arbitrary `A_0` and construct one fixed `A_1` that authenticates and decodes `e_1`, rejects every malformed string in polynomial time, and runs `A_0` on the recovered canonical `e_0` image. Prefix alignment gives

`T_A1^wc(b(M)) <= h'(M + T_A0^wc(M))`.

Apply B2 for `e_1` at `b(M)` and use `Wbar_0(M)=Wbar_1(b(M))`. Polynomial composition yields B2 for `e_0`.

This proves B2 truth-value invariance under the hypotheses, not B2 itself.

## Exact monotone-length corollary

Suppose

`|e_1(F)| = phi(|e_0(F)|)`

on all valid sources, where `phi` is strictly increasing on attained source lengths and polynomially bounded. Define

`psi(N)=max{ n attained by a valid e_0 source : phi(n)<=N }`.

Then

`S_1(N)=S_0(psi(N))`, `Wbar_1(N)=Wbar_0(psi(N))`,

and at attained cutoffs

`S_0(n)=S_1(phi(n))`, `Wbar_0(n)=Wbar_1(phi(n))`.

The prefix theorem therefore applies. Strict order reflection is load-bearing for the reverse identity. A plateau such as `phi(n)=2 ceil(n/2)` can mix source lengths `2k-1` and `2k` at one padded cutoff; sparse clock spikes then block this proof. That is a failure of the sufficient premise, not a counterexample to B2 truth.

## Square-padding corollary and exact physical charges

Let the base canonical bit string be `c` of length `n`, and define

`E(c) = 1^n 0 c 0^(n^2)`.

Its exact length is

`ell(n)=n+1+n+n^2=(n+1)^2`,

and its inverse cutoff is

`r(N)=max(0,floor(sqrt(N))-1)`.

For the same abstract source and same `R`,

`Wbar_E(N)=Wbar_0(r(N))`

for every cutoff `N`, and B2 is equivalent in the two serializations.

| phase | work/output | peak writable space |
|---|---:|---:|
| explicit encode | read `n`; write `(n+1)^2` bits: `Theta(n^2)` | `Theta(n^2)` if materialized; `O(log n)` counters if streamed |
| lazy forward view | paid region/address translation for every simulated bit access | source pointer, `n`, simulator state; no free random access |
| padded validation | `Theta(N)` deterministic scan; one flipped zero must be rejected | small parser scratch or materialized `Theta(N)` |
| decode/output | `Theta(N)` validation plus `Theta(sqrt N)` payload writes | `Theta(sqrt N)` payload if materialized |
| proof verification | unchanged logical proof, but its encoded lines, parsing, access, and checks remain charged | schedule dependent |

An exponential intermediate representation is allowed. If materialized, its complete construction/output and peak space are charged. A compact lazy alternative is also allowed, but every virtual read and update is translated and charged. Neither case turns ideal logical nodes into physical runtime automatically.

## Why sparse delays do not refute the theorem

LSPV-1/391C constructs one fixed correct decider with enormous delays at sparse lengths and thereby disproves a bound comparing the **same** arbitrary program at `N` and `N^2`. That lemma remains correct.

For the positive transfer, an arbitrary padded decider `A_E` is converted into a different fixed raw wrapper `B`. At padded cutoff `M`, the wrapper is invoked only on raw sources whose padded images have length at most `M`, so

`T_B^wc(r(M)) <= poly(M + T_AE^wc(M))`.

If `M` is a delayed length, the delay is already on the right-hand side. If it is not, the wrapper cannot call a future delayed length. In the reverse direction, all decoded source sizes are at most `r(M)`, and cumulative `T_A^wc(r(M))` includes every applicable source delay. Delays on malformed strings merely enlarge the relevant right-hand side.

Thus sparse delays falsify clock regularity, not prefix-aligned decider transport.

## Finite and independent controls

The Python producer exhaustively enumerated all 256 subsets of eight non-tautological width-one/two clauses on two variables. It computed labels by truth-table enumeration and exact minimum ordinary-Resolution inference counts by breadth-first search for all UNSAT members. Results:

- 95 SAT and 161 UNSAT formulas;
- maximum toy Resolution cost 3;
- exact `Wbar_E(N)=Wbar_0(r(N))` at every attained breakpoint and at `N-1,N,N+1` around every square cutoff;
- eight selected full encoding/decoding round trips;
- six malformed-wrapper rejection classes;
- 1,133 assertions PASS.

The independently written JavaScript verifier rebuilt the formula universe, SAT labels, Resolution closure, square code, cutoff identities, malformed controls, and clock trace: 1,806 assertions PASS.

For the physical XOR countercontrol, a 16-bit binary clock executes 65,536 ticks, has adjacent full-state XOR sum 131,070, but endpoint XOR zero. This confirms that endpoint logical/physical XOR is not runtime and that full trace instrumentation is itself charged.

Artifacts and SHA-256:

- `experiments/arc/lspv5_339/prefix_aligned_b2_invariance_referee339.py`;
- `experiments/arc/lspv5_339/verify_prefix_aligned_b2_invariance_referee339.js`;
- `results/raw/arc/lspv5_339/prefix_aligned_b2_invariance_referee339.json` — `1af42ec676657a212bc5fc48df8ea61b9c080a6521edf71d00ab4065019c30a9`.

Finite controls verify the implementation and exact finite identities. They do not prove Haken's theorem, B2 for `R_mix341`, or any unrestricted machine lower bound.

## B1/B2/B3 classification

| obligation | result |
|---|---|
| B1 under the same-source syntactic recodings | prior LSPV-1/391 **PROVED invariant** |
| B2 under bidirectional prefix-aligned recodings | this run **PROVED invariant** |
| B3 under the same-source syntactic recodings | prior LSPV-1/391 **PROVED invariant** |
| B1 for fixed `R_mix341` | **OPEN** |
| B2 for fixed `R_mix341` | **OPEN** |
| B3 for fixed `R_mix341` | **OPEN** |
| superpolynomial `Wbar_Rmix341` | **OPEN** |
| unrestricted SAT time/space lower bound; P versus NP | **OPEN** |

The theorem says that a structured syntactic representation change cannot by itself repair or destroy B2. It says nothing about semantic encodings that alter the source axioms or add shortcuts, and nothing about simulating arbitrary algorithms by `R_mix341`.

## Project, five-role, Grok and Claude review

Issue #3 was read through 795 comments before proof work. The direct precursor was:

- `research/agents/lspv-1/2026-11-04_0700_LSPV-1_SYNTACTIC_ENCODING_B2_SCALE391.md`, blob `a50564a5b95f886de2113009945fc7f8b47314ae`.

Its equal-length B2 theorem and sparse-delay counterexample are correct. All five role audits independently agreed that the exact monotone/prefix-aligned extension is valid and that the delay lemma does not contradict it. LSPV-1 checked the quantifiers and both transported machines; LSPV-2 supplied the exact square code; LSPV-3 isolated bidirectional prefix alignment and the strict-order condition; LSPV-4 charged explicit/lazy construction, validation, access and peak space; LSPV-5 attacked malformed delays and same-machine/profile confusion.

The latest Grok file actually reviewed was `GROKPROOF/2026-11-04_1518_PROGRESS.md`, blob `4e2bb9d941295f620a64e078117d29244caf4fba`. It still leaves the arbitrary-`A`, all-input, fully charged transfer open and supplies no proof of B1/B2/B3 for `R_mix341`.

Claude has no newer applicable bridge. The files actually checked were:

- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They contain restricted direct-product, alternation-trading, and one-tape analyses, not this encoding theorem and not a universal source-rooted mixed-calculus compiler. Their warnings about exact encodings are consistent with the present proof but are evidence, not authority.

## Search log

Primary-source/web searches:

- `Haken 1985 intractability resolution pigeonhole principle theorem exact model PDF`;
- `time constructible sparse delay machine arbitrary time profile theorem`;
- `padding theorem exact polynomial padding cumulative worst case complexity encoding invariance`.

Repository/GitHub searches:

- `SYNTACTIC_ENCODING_B2_SCALE391 repo:j15marti/pnp`;
- `B2 encoding invariance square padding prefix cutoff repo:j15marti/pnp`;
- `sparse delay cumulative worst case padding repo:j15marti/pnp`;
- `propositional proof certificate verifier encoding transport org:openai`.

The project search found the equal-length precursor and delay controls, but not the exact monotone-prefix extension. The `github.com/openai` query returned no relevant proof-transport implementation. Absence from search is not a novelty claim.

## Classification and next exact gap

**PROVED/RESTRICTED:** B2 truth is invariant under bidirectionally prefix-aligned, same-source, polynomial syntactic encodings. Exact strictly increasing polynomial padding, including the displayed square code and linear factor-two codes, satisfies the theorem.

**FAILED CANDIDATE OBJECTION:** sparse artificial delays do not refute exact-padding B2 invariance; they refute only the unnecessary same-program rescaling inequality.

**NOT PROVED:** arbitrary mutually polynomial encodings with irregular/plateaued valid-image prefixes. The present proof requires exact prefix alignment; a plateau demonstrates why the reverse proof can fail, but does not show B2 truth differs.

**OPEN NEXT GAP:** characterize the weakest prefix/cofinal alignment condition sufficient for B2 transport without exact length laws, then keep it separate from the real project target: proving B3 or a superpolynomial `Wbar` for the same fixed `R_mix341`. No encoding theorem supplies the arbitrary-algorithm-to-proof compiler.

**B1 OPEN; B2 OPEN; B3 OPEN for fixed `R_mix341`; P versus NP OPEN.**

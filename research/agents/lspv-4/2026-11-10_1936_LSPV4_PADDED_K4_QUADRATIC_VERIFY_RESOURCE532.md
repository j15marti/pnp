# LSPV-4/532: Exact padded-source certificate resource firewall and a quadratic-log verification upper bound

**2026-11-10 19:36 PST. PNP Time-Space Resource Auditor. Historical Route A retained.**
**PROVED/RESTRICTED** mathematical theorem for the separate, explicit canonical SOURCE/AND3/GF(2) calculus of LSPV-4/531. **COMPUTATIONAL** two implementations and V8 checker replay. Not historical complete $R_{\mathrm{mix341}}$ acceptance. **P versus NP OPEN.**

**Target:** sharpen the fully charged pair-verification upper bound of [P2-L4-531] and test an information-theoretic physical-verification lower bound with constant *logical* proof work. This is a resource firewall for [P2-D1] -> [P2-C3] -> [P2-B1]. Separate [P2-B2]/B3 remains OPEN. No theorem is transferred to arbitrary SAT algorithms.

## IDEA and preregistered falsifiers

Candidate: the /531 canonical flat proof format permits a **uniform indexed-read-only two-input verifier with $O(L^2\log L)$ sequential time and $O(\log L)$ dense writable bits**, $L=N+B$, by validating each explicit record using a constant number of read-only cursors and no derived-row cache. A fixed 15-paid-node K4 odd-Tseitin refutation can have arbitrarily long explicitly padded affine masks, each terminal byte individually necessary for correct verification. Falsifiers:

1. **Padding illegality:** /531's independently source-bound syntax rejects a declared unused variable or an E-bit affine row with correctly padded zero coordinates.
2. **Unsound source:** changing K4's parity charge to even still accepts the odd-charge proof.
3. **Premise/goal escape:** a one-bit change in any padded final contradiction row or an omitted paid inference is accepted.
4. **Resource undercharge:** computing parent rows requires storing E writable bits, or locating their byte positions incurs more than polynomial paid re-scans.

All four failed in the expressly stated test language. F4 is settled by a constructive abstract-machine algorithm and is not claimed as a host-memory measurement.

## SEARCH, precedence, limitations

Read root proof1.txt (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`), current proof2.txt (initial blob `169b1c5a7ab6cadbff28f98493918a1894d7d517`), issue #3 and most recent peer comments, AGENTS.md, CODEX.md, pnp-research/SKILL.md, abstract-negative coordination handoff, original recovered /341 code and /531 canonical checker. Relevant full reports sampled: LSPV-3/546-547, /549, /559; LSPV-2/546; LSPV-4/528, /531; GROKPROOF/2026-11-11_0315_PROGRESS.md; Claude TPORT-0001. Not all 539-549 reports were individually read. Existing result [P2-L3-547] already proves a conditional flat logspace checker; [P2-L4-531] instantiated its explicit-mask source model with a conservative **cubic** time bound. This report improves the time bound *for that exact test grammar* and exhibits a source-size/logical-cost versus evidence-length separation. It does not claim the general flat-verification theorem as new.

Primary research checked: Cook and Reckhow, JSL 1979, DOI 10.2307/2273702; Fortnow, Lipton, van Melkebeek and Viglas, JACM 2005, DOI 10.1145/1101821.1101822 (indexed random-access time/space distinction); Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973 (abstract-concrete soundness). Existing proof-complexity/solver repositories checked by actual file and blob: `konard/p-vs-np:scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research:METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor:format.md` `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr:README.md` `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `openai/math:README.md` `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; `msoos/cryptominisat:README.md` `7636988713ee16802b84fb1cdf688ea8f87da70e`. None authenticates the missing historical mixed-rule byte language. No Google search was executed separately from web research.

## Theorem 532.1: quadratic-log indexed verification, specified test grammar

**PROVED/RESTRICTED.** Fix the /531 original-source-bound canonical line syntax: input is an external signed strict 3-CNF source F of N bytes and an explicit read-only, topologically numbered proof P of B bytes; source records reconstruct exact clauses; paid AND3 records combine at most three source variables and optionally assert an E-bit parity alias; paid XOR records contain two explicitly referenced, earlier E-bit affine parents and an E-bit output row, with one RHS bit. Every paid record contains two *distinct* preceding references. Final row is explicit $0=1$. The source and proof are two read-only indexed input tapes; all writable index-tape cells, counters, intermediate flags, and scratch count as native work.

There is a deterministic checker for the **pair (F,P)** with, writing $L=N+B$,

$$
T_{\rm check}(N,B)=O(L^2\log(L+2)),\qquad S_{\rm work}(N,B)=O(\log(L+2)).
$$

The source/proof input payload $L$ is *not* free evidence; its access is charged to time. It is read-only and not included in writable WORK. For each complete input, a fixed finite number of $O(\log L)$-bit counters retains the current record location, up to two parent offsets, three local bit positions, source-clause position, and E; the AND3 truth table and three signed supports require constant space. For each derived record, scan the read-only proof/source at most constantly many times to resolve ID and field boundaries, charging $O(L)$ byte inspections; compare its E output bits against parent E-bit masks using three positional cursors, paying even $O(\log L)$ for each indexed address manipulation, for $O(E\log L)$. All canonical decimal-identifier comparisons use bounded-width counters after checking lengths, never unsafe floating-point coercion. Reject an impossible claimed E before allocating: any accepted proof's terminal row necessarily has E explicit mask digits, hence $E\leq B$. Parsing of malformed sources, duplicate/future parents, all signed source occurrences, algebraic alias truth tables, and final goal is paid within the same bound. There are $q\leq B$ paid records, so total $O(q[L+E\log L]+L)\subseteq O(L^2\log L)$ operations. A dense contiguous writable region holds all bounded counters; its maximum ever indexed writable address is logarithmic. No complete paid affine row is cached on writable WORK. This is an *algorithm existence theorem*, not a native-FLMV machine execution.

This improves /531's loose $O(L^3)$ upper bound without changing its soundness proof. It does not establish a lower bound on construction, searching, or a source-only SAT decision procedure, and does not authenticate unimplemented RES/DEF/LOCAL-CONVERT/context operations.

## Theorem 532.2: accepted bloated-source family with exact byte-query lower bound

**PROVED/RESTRICTED.** Fix the *original signed* K4 odd-Tseitin source with 16 ternary clauses involving variables 1 through 6. In its external DIMACS header declare any $E\geq 6$ variables, allowing indices 7 through E to be unused. Every clause and every actual six-variable assignment remains unchanged, so odd K4 is UNSAT; the even-charge source has exactly 8 satisfying assignments over its six active coordinates (equivalently $8\cdot 2^{E-6}$ over all declared coordinates).

Take the 15-node /531 canonical refutation: twelve paid AND3 nodes and three paid XOR nodes. Pad the four alias masks and three XOR masks with E-6 zero bits, including the last $0=1$ row. **Exact ASCII lengths** on this explicit format are

$$
N(E)=162+\operatorname{digits}_{10}(E),\quad
B(E)=7E+340,\quad
W=15,\quad R=30,\quad D=6.
$$

Every such pair is accepted by the unchanged canonical /531 checker. For each position $j\in\{1,\ldots,E\}$ of the final contradiction's all-zero row, replacing only that one ASCII `0` with `1` preserves the original source, byte length, all paid identities and all other records but makes the certificate invalid. Consequently every deterministic exact **byte-query** verifier that accepts this pair and rejects all one-byte modified packets **must read all E specified bytes on that accepted input**: an unqueried bit would make an invalid mutation indistinguishable. Thus $T_{\rm check}=\Omega(E)=\Omega(B)$ for this family, while $N=\Theta(\log E)$ and $W=15$.

This does **not** lower-bound the time to *decide SAT* or to verify a different, shorter certificate; it is a necessary-reading lower bound for the displayed supplied packets and specified byte-sensitive accepted language. A verifier that first normalizes to a short certificate must still charge reading/validating the supplied packet if it claims to accept exactly this source-bound language. Variable-declaration padding is allowed in this declared test grammar; any calculus forbidding unused variables is a different domain.

## Independent finite checks, resource ledger and adversarial scope

**Executable and raw results:** `experiments/arc/lspv4_532_padded_source_quadratic_firewall.cjs`; `results/raw/arc/2026-11-10_1936_LSPV4_532_PADDED_K4_QUADRATIC_FIREWALL_RAW.json`. The repo executable embeds the *unaltered exact source* of the /531 canonical checker (blob `b719196c6171056a629585e15010461149ced4bd`), and tests 8 accepted cases with E=6,8,16,32,64,128,256,1024 and **308 expected rejected mutations** in connected V8. Six further categories include even-charge SAT-source aliasing, malformed header, unknown rule, duplicate parent and missing goal. The repo script passes V8 syntax parse and exact Github content readback, but **the published Node OS wrapper was not run as an independent process**. A distinct, locally executed standalone Node script with an independently written source-bound verifier accepted 8 cases and rejected 300 adversarial variants. These are host-language correctness tests, not physical indexed-TM memory measurements.

| Operation | Fixed logical tariff in TEST format | Evidence and physical charges | Semantic span / retention |
|:--|:--|:--|:--|
| SOURCE | 0 | N read-only signed source bytes, exact clause authentication and ID lookup | No derived result held on WORK |
| AND3 | 1 per distinct occurrence | Two named references, O(L) lookup, at most 3 variables, up to E-bit alias row | +1 from deepest premise, constant local flags |
| GF(2) XOR | 1 per distinct occurrence | Two named references, E explicit output bits, O(E log L) bit-index work | +1 from deepest premise, no E-bit writable row |
| Shared parent retrieval | No new paid deduction in TEST format | Every reread and ID lookup charged to sequential T; no invented historical reference tariff | Parent value re-read from read-only certificate |
| Other historical rules | UNKNOWN | RES, LOCAL-CONVERT, paid DEF/facets, branches, discharge, joins, contexts, deletions, fresh/exported/private wires are **not implemented** in /531 | No all-rule C3 implication |

For the displayed K4 family, $q=15$, premise occurrence count 30, span 6 and seven explicit E-bit masks. A sound abstract resource map may retain $(W,B_{\rm explicit})=(15,7E+340)$ or the lower resource charge $E$ mandatory final-mask reads, which never overcharges the concrete accepted-byte verifier. Abstract *logical* work must remain W=15 regardless of physical rereads; joining component work lower bounds without count-once partition is invalid. Extra headers, caches, restarts or search costs are not included in the ideal shortest-refutation work.

**No full native-calculus replay occurred.** LSPV-3/559 independently proved the recovered historical /341 fixture checker has only an AND3/XOR paid-rule dispatch and a hardcoded fixed proof count; it cannot authenticate historical RES, DEF, LOCAL-CONVERT or joins. The /531 and /532 formats are **separately defined controls**. This run did not infer new accepted historical opcodes, alter their weights or exclude GF(2), extension, shortcut, learning or shared-DAG proofs.

**Actual advance:** restricted explicit-bit serial verification time sharpened from cubic to quadratic-log, with an exact constant-W certificate family forcing linearly many independent byte queries. **Verification:** two independent finite implementations, direct original /531 body replay, 308+300 negative controls; manuscript review pending. **Remaining gaps:** full historical [P2-D1], all-rule cost-sound [P2-C3], genuine all-rule superpolynomial [P2-B1] and separate [P2-B2]/B3 remain OPEN. P versus NP remains OPEN.

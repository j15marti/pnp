# LSPV-1/507: A source-indexed 19-node Resolution cancellation improves /506
**2026-11-08 08:00 PST | PROVED/RESTRICTED and COMPUTATIONAL | Route B. P versus NP OPEN.**

**Tracker IDs:** new [P2-L1-507], refinement of [P2-L1-506] and [P2-F13]; OPEN [P2-D1] historical grammar, [P2-C3] all-mixed transfer, [P2-B1] full-calculus superpolynomial minimum and [P2-B2] noncircular B3; companion [P1-01], [P1-03], [P1-04] unchanged.

## IDEA and 4 prior falsifiers
Hypothesis: the previously valid /506 *21-node* original-source Resolution proof of the three output facets is not minimum; reuse a derived output facet to save nodes. Four falsifiers: (1) any shorter candidate requires an uncharged semantic, weakening, or extension step; (2) a shared DAG contains a cycle/double count/assumption-scope leak; (3) the three facets are not exact oriented Resolution consequences of the original 16 source clauses; (4) source corruption or wrong SAT labels or false claims of native historical checker acceptance.

## SEARCH: exact research and peer sources
Both live root trackers read completely before writing (proof1 blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; proof2 initial blob `f8fb3c6162116074ab91014b0c547cfe8ac13af0`). Read actual /506 report and verifier, /341 original declared grammar, 2026-11-02_1204 governing five-role handoff, issue #3, LSPV-3/504 and LSPV-5/435, AGENTS.md, CODEX.md, and the project pnp-research skill. Current actual GROKPROOF/2026-11-08_0320_PROGRESS.md and Claude 2026-10-28_0924 world-ledger were inspected. LSPV-5/435 cautions that the recovered /341 checker so far recognizes SOURCE/AND3/XOR, not every proposed RES/DEF metadata field.

Change-aware external repository/path and blob review: konard/p-vs-np README.md `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and scripts/proof_status.json `93b77ed3d8fe456f81c690035f45f07910a247f2`; blkph0x/p-vs-np-proof-research METHOD_INDEX.md `18d693ea71dfa433370eb7afbebc3106e32f03e5` and INDEPENDENT_AUDIT.md `b30515cced93d8911a6415555ee9ec1444502d93`; meelgroup/frat-xor/format.md `986a21aa92b62f844ef1fce852193142c41b2b1f`; tanyongkiam/cake_lpr/README.md `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; peitl/short-proof/README.md `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; openai/math/README.md `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. They neither contain a proof of P vs NP nor authenticate our historical rule grammar. Primary web literature searched includes Pang 2026 Res(PC), the classic Resolution width/size paper, Buss proof-complexity tutorial, and Peitl–Szeider minimum Resolution work. Dedicated Google-branded session was unavailable.

## ITERATE: improved exact, local source certificate
Retain **exactly the same 16 original proper signed 3-CNF records in the same order as LSPV-1/506**. Variable indices: 1=x, 2=y, 3=t, 4=a, 5=p, 6=b, 7=h, with gates
$$
a=x\wedge y,\qquad p=y\oplus t,\qquad b=x\wedge p,\qquad h=a\oplus b.
$$
The published JavaScript gives every original source clause S00..S15 and all 19 topologically ordered, source-indexed, oriented RES steps R01..R19. There are **no** semantic shortcuts or new opcodes. Its three goal clauses are
$$
R07=(\neg x\lor\neg t\lor h),\qquad
R11=(x\lor\neg h),\qquad
R19=(t\lor\neg h).
$$
R19 uses R11 as a premise, so the one shared DAG handles all three facets without charging that work twice. Every one of the 16 source clauses lies in their combined ancestry. Maximum derived clause width is 4 and maximum unit-weight parallel depth is 4. This gives a 19-node *upper* certificate, **not** proof of globally minimal 19 work.

For $g$ copies with globally renamed private variables and shared original $t$, let $F_g$ denote all 16$g$ original clauses, $Q_g$ the 3$g$ derived facets, and $G$ any exposed-only CNF over $x_i,t,h_i$. Concatenating the certificates to any ordinary-Resolution refutation of $Q_g\wedge G$ proves the source-exact upper bound
$$
S_{\mathrm{Res}}(F_g\wedge G)\le19g+S_{\mathrm{Res}}(Q_g\wedge G).
$$
This improves the /506 coefficient 21 to 19 (saving 2$g$ distinct nodes or 9.52% of the macro). The original 16-clause gadget itself is SAT; the theorem is a conditional-on-downstream-UNSAT upper control, NOT a new hard family.

**Independent checks:** separately authored local Python replay: 252 assertions; local Node replay: 2,639 assertions. Both confirm all 19 exact oriented Resolution inferences, all 128 original total assignments, exactly 8 source models, all 8 SAT/UNSAT exposed-interface controls, and 4 deliberately corrupt proof tests. The published GitHub JS is a distinct patched /506 checker using the 19-step proof and should be executed/rechecked by peers; do not call it the recovered historical /341 checker.

## Family/theorem/encoding/shortcut/remaining-transfer ledger
| Established family | Source/encoding | Proved bound in specified model | Short legal controls | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | $h$ vertices, $3h/2$ edge variables, $4h$ proper signed width-three clauses, $\Theta(h\log h)$ bits | exp($\Omega(h)$) **ordinary shared-DAG Resolution** (Urquhart; Ben-Sasson–Wigderson) | GF(2) + source-local factors give the declared /341 $4h-1$ upper/minimum (at declared scope) | Native RES/DEF accepted grammar and full mixed hardness open |
| Pang proper random 3-CNF | $n$ vars, $8n$ independent proper signed 3-clauses, $\Theta(n\log n)$ bits | exp($\Omega(n)$) in syntactic Res(PC1/F2) w.h.p., arXiv:2610.00837v2 (preprint) | Existing /498–/502 restricted translations, EF/ER and GF(2) shortcuts must be tested | Full R_mix341 lower-bound transfer open |
| 506/507 cancellation control | 16 proper signed 3-clauses, 7 variables; $16g$ clauses for $g$ copies | NONE, satisfiable control only | New ordinary RES proof 19$g$ inference nodes, depth four | Historical parser and nonlocal interaction unknown |

Cook polynomial extended-Resolution PHP proofs, odd-Tseitin GF(2) shortcuts, nonlocal gates, sharing and branching remain permitted controls. The free optimal valid-derivation choice is not penalized for discovery time.

## Resources, falsification, status
Distinct logical inference nodes 19 per gadget; weighted span 4, not a simultaneous time/space schedule. Input and evidence bits $O(g\log(g+2))$ with binary IDs and fixed-width clauses. Straightforward materialization, proof generation, checking and output use $O(g\operatorname{polylog}g)$ bit operations and $O(g\log(g+2))$ simultaneous storage plus downstream supplied proof. Local independent host checks charge process startup, parsing, 128-assignment evaluations, corruptions and JSON output but do NOT establish an indexed FLMV machine bound. No actual source discovery/search overhead is removed from an implemented upper-bound algorithm; the ideal minimum intentionally grants free optimal choice.

Falsifiers (1)-(3) were disproved by independent exact checkers for the new certificate. Falsifier (4) remains a firewall: **historical R_mix341 checker was NOT run**, so no claim of native acceptance is made. Root main.tex was NOT edited because its complete byte-preserved ownership region was not read. Historical rules, all five identities, 2 Route A/3 Route B allocation, schedules, timezones and enabled states untouched.

**Actual advance:** tightened source-exact shared-DAG ordinary Resolution upper certificate from 21 to 19 nodes with the same depth and all 16 original sources. **Remaining gaps:** [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. **P versus NP OPEN.**

Sources: LSPV-1/506 predecessor (2026-11-08); Ben-Sasson & Wigderson, JACM 48(2), 2001, DOI 10.1145/375827.375835; Pang, arXiv:2610.00837v2 (2026); Buss 2014 Mini-tutorial, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/Banff2014/talkslides.pdf; Peitl & Szeider, JAIR 72 (2021).

## Published-verifier execution addendum, 2026-11-08 PST

After committing the 19-step certificate, I refetched its **exact GitHub blob** `18a3f1019b3ad9f940b58ac321de7afdcd8c70c1` and executed the returned JavaScript in an isolated V8 runtime. **650 assertions passed**, with 19 distinct paid Resolution nodes, 16 source clauses, 8 original source models, all three expected facets, weighted depth four, and three internally exercised hostile controls. This is a direct replay of the published file, distinct from the independently authored local Node 2,639-assertion and Python 252-assertion verifiers. The historical `/341` checker was still **NOT executed**.

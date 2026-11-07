# LSPV-3/479: Paid conservative OR-gate export of derived Resolution clauses

**2026-11-07 10:24 PST | PROVED/RESTRICTED + COMPUTATIONAL | Route B | P versus NP OPEN.** The result is for a distinct declared-semantic `DEF_OR+RES` completion, **not** the historical accepted-byte R_mix341 grammar. Evidence node **[P2-L3-479]** concerns still-open **[P2-D1]** and **[P2-C3]**, not an all-rule B1/B3 proof.

## IDEA, falsifiers, SEARCH, ITERATE

Hypothesis: a supplied source-authenticated legal RES derivation of a proper width-k clause can be followed by a paid, conservative OR-gate export to a justified output unit with at most 3(k-1) additional paid operations. Precise falsifiers: (1) the OR facets do not define a unique output; (2) a RES step needs unsanctioned weakening, a source oracle or missing facet; (3) a shared definition causes duplicate charges or a branch-local conclusion leaks assumptions; (4) the historical byte grammar forbids one of these view references. The explicit completion defeats falsifiers 1-3, with falsifier 4 and historical authentication still **OPEN**.

Read both complete root proof trackers (pre-run proof1 blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 blob `a2432bbb29d5d38c8d8e86f30a9f3951cbc99951`), current coordination issue #3, November 2 role handoff, `AGENTS.md`, `CODEX.md`, the research skill and current peer work. Exact historical grammar source: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`; source/AND3/XOR verifier `experiments/arc/lspv2_341_independent_verify.js` blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Read peer LSPV-5/412 blob `b99084b9e1534654207042d00d6645361dfc5863`, LSPV-3/478 blob `ad478538c8b8f385ab866f833ec79d2535706e8d`, LSPV-1/481 blob `cd2ec52e7c0fe352a44d55b8b6dab71637ff08c7`; current `GROKPROOF/2026-11-07_1815_PROGRESS.md` blob `0532370c9bf99b1204be4e0efd9ef96290454ec7`, and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`.

External change-aware checks: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (separate XOR and clause tags); `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. Web searches checked Cook's 1976 extended Resolution and Chvatal-Szemeredi's 1988 ordinary Resolution lower bounds. No separate Google-branded interface was used, and no external repo title/checker badge is treated as authority. This derived-clause OR gate pattern is standard ER-style reasoning, **not claimed academically novel**.

## Theorem 479.1 (PROVED/RESTRICTED)

Fix a distinct rule completion: (i) every derived binary RES node costs one unit; (ii) each fresh two-input `DEF_OR` node costs one unit and emits three named clausal facets accessible to RES; (iii) each definition is globally fresh and conservative; (iv) all source/branch contexts are carried on the derived clause, but facets have empty assumptions. No added SPLIT/WEAKEN/DISCHARGE and no semantic implication oracle.

For a **supplied** legal, source-authenticated derived clause
$$
D=\ell_1\lor\cdots\lor\ell_k,\qquad k\ge2,
$$
introduce fresh prefix gates $y_2\leftrightarrow(\ell_1\lor\ell_2)$ and $y_i\leftrightarrow(y_{i-1}\lor\ell_i)$ for $i>2$. Each gate $z\leftrightarrow(a\lor b)$ carries exactly the facets
$$
(\neg z\lor a\lor b),\quad(z\lor\neg a),\quad(z\lor\neg b).
$$
From $D$, RES successively against the last two facets of each new gate derives $(y_i\lor\ell_{i+1}\lor\cdots\lor\ell_k)$ and finally **the unit $y_k$**. Every pivot is oriented, every facet is paid through its producer, and every earlier-variable assignment uniquely extends to all outputs. Hence a proof of $\Gamma,F\vdash D$ yields
$$
\Gamma,F,\mathrm{DEFs}\vdash y_k
$$
using exactly $k-1$ DEF plus $2(k-1)$ new RES, i.e. **at most $3(k-1)$ additional paid inference nodes**. A deterministic translator can export selected lines of any already-given shared Resolution DAG using at most $3\sum_{D\in S}(|D|-1)$ additional paid nodes, without repeating shared definitions or charging source-clause reads as free real machine computation. This does NOT bound the time of finding the input Resolution proof.

**Type barrier remains:** a justified unit on a fresh gate is **NOT** automatically an accepted historical AND3 factor or a LOCAL-CONVERT result, because the /341 text constrains AND3 local support to three **original** variables and has no authenticated DEF-facet/export-view byte production. Thus this is **not** the historical RES-to-AND3 normalization demanded by [P2-C3].

## AND/OR shared-branch control

For $F=(\neg g\lor a\lor b)\wedge(g\lor a\lor b)$ the two assumption contexts $\Gamma_+=\{g\}$ and $\Gamma_-=\{\neg g\}$ each derive $D=(a\lor b)$ with one scoped RES. Reusing a global $y\leftrightarrow(a\lor b)$ definition but retaining two separately scoped proof chains costs **$1+3+3=7$** distinct paid nodes, not 8. The same original source admits a **better global derivation**: resolve its two clauses to $D$, then one DEF and two RES, totaling **4**. The free optimal-choice minimum can choose this shortcut; no SPLIT or branch-discharge is silently made native. Removing the assumptions from a proof obtained using only one branch clause would be unsound.

## Published family and exact original encoding

For a connected cubic graph $G$ with $h$ vertices, odd-charge Tseitin $T(G,\chi)$ uses $3h/2$ edge variables and four original signed strict-3CNF forbidden-pattern clauses per vertex ($m=4h$, indexed length $N=\Theta(h\log h)$). Summing its vertex GF(2) equations proves UNSAT. Existing published expander families have exponential ordinary Resolution lower bounds but polynomial GF(2) shortcuts in suitable algebraic systems; neither is a universal all-machine lower bound. On **original K4**, 16 source clauses with charge vector $(1,0,0,0)$ and SHA-256 `861b38239ec08050a7b38b3da04fd79c17d43624a8f755be5a1417d8f01745c8`, the original source clauses #1 and #5 yield $D=(x_2\lor x_3\lor x_4\lor x_5)$ with one RES. Three paid DEF and six further RES export its OR-gate unit: **10 paid nodes**. The odd source is UNSAT, and its even-charge counterpart has 8 SAT assignments. This is a local proof on a finite established-family instance, not a certified asymptotically hard individual instance or complete refutation.

## Evidence and resources

An independent Python producer constructed 18 source-authenticated cases: widths $k=2,\ldots,16$, both branch contexts and original odd-K4. A separately implemented Node.js checker recomputed source DIMACS hashes, verified source clauses, signed oriented RES, gate freshness/acyclicity, all three conservative DEF facets, DAG references, scope consistency, finite source-model implications where feasible and negative controls. **29,574 assertions passed and 11 malicious controls were rejected.** The independently runnable PUBLIC compact replay has **1,023 passing checks**; the separate local compact replay in the ZIP has **1,043 checks**. Width 16 uses 15 DEF, 30 export RES plus 13 pre-export RES, or 58 paid nodes. Complete local reproducibility archive includes Python producer, independent JS checker, 46,893-byte original fixture set (SHA-256 `3a99616218d77da1457e3eb934e4917a14de64b53e61e6d1c026a710d6d6a96c`) and SHA-256 manifest.

Each width-k exported OR gate needs $O(k)$ paid definitions and RES steps; each facet has at most three literals. Explicit certificate overhead $O(k\log(n+k+q))$ bits per exported proper clause with standard indexed identifiers, plus original input and proof references. Parsing, construction, verification, source reads, temporary buffers, serialization, references, caches and failed search are paid by actual algorithms, not the ideal proof minimum. Producer host wall time 0.75s, peak RSS 96,392 KiB; independent Node checker 0.13s, 45,864 KiB; no native FLMV machine exponent inferred. **The historical authoritative /341 checker was NOT run on these new DEF+RES traces.**

## Dependencies left open

**[P2-D1]**: historical accepted DEF facet references, output-view/LOCAL-CONVERT/AND3 ports and private/exported wires. **[P2-C3]**: arbitrary mixed source-preserving polynomial normalization including definitions, wide affine rows, algebra and shared assumptions. **[P2-B1]**: superpolynomial minimum across **all** historical legal rules, not sealed S. **[P2-B2]**: noncircular same-R B3. Route A all-input same-machine contraction remains open. P versus NP remains **OPEN**.

Primary literature: Stephen Cook, *A short proof of the pigeon hole principle using extended resolution* (SIGACT News 8(4), 1976), DOI 10.1145/1008335.1008338; Chvatal & Szemeredi, *Many Hard Examples for Resolution* (JACM 35(4), 1988), DOI 10.1145/48014.48016; project actual /341 declaration and external FRAT-XOR format above.

## Publication and coordination verification

The report, self-contained compact executable, raw summary and five-role handoff were published to `main` and each received a COMPLETE content-equality readback. The precise published executable was then independently evaluated from its fetched bytes, passing **1,023 assertions** (the distinct, more extensive local compact executable in the downloadable ZIP passes 1,043). The full Python/independent Node test pair also passes 29,574 checks with 11 deliberate rejected mutations. These are finite reproduction results, not an authoritative R_mix341 parser run.

**Shared trackers:** `proof1.txt` read and unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`. `proof2.txt` exact current prewrite 200,748 characters, blob `7e4dac762491ccfa07f951852ded43b33e6996e9`, saved with full equal-content readback at `research/agents/lspv-3/outbox/2026-11-07_1024_LSPV3_479_PROOF2_PREWRITE_EXACT.txt`; SHA-guarded new evidence **[P2-L3-479]** appended at commit `a125643bb585966bdcea95fccdb7f988bccaf174`; final complete readback 202,829 characters, blob **`9fe2d53f1634202a69be3195311410fde398a4c3`**, preserving all prior content. Coordination issue #3 comment **6711423803** posted and independently read back in full: https://github.com/j15marti/pnp/issues/3#issuecomment-6711423803. No other tracker node status or obligation changed. `main.tex` was not touched.

**Next exact test:** Recover an historically accepted serialized DEF-facet-to-RES and derived-clause-to-AND3/LOCAL-CONVERT chain with full source and branch provenance, or prove a legally typed obstruction for that particular transition. No new agent, schedule, weights or rule changes. **P versus NP remains OPEN.**

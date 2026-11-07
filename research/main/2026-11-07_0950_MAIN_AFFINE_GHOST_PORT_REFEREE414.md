# REFEREE414 — recovered /341 affine ghost-port audit

**Role:** LSPV-5 Independent Red Team  
**Time:** 2026-11-07 09:50 PST  
**Status:** **PROVED/EXACT within the recovered source/AND3/XOR verifier; COMPUTATIONAL exact replay.**  
**Global status:** **P versus NP remains OPEN.**

## Result

The recovered historical /341 verifier does not require an affine mask to lie in the declared edge-variable namespace. Its AND3 rule inspects only mask bits $0,\ldots,E-1$, while XOR performs full unbounded-integer XOR.

For the authenticated K4 packet, the first affine XOR has parents d2 and d5. Replacing both parent masks by

$$
m' = m \mathbin{\mathrm{XOR}} 2^H
$$

for tested $H=6,64,1024,8192$ leaves their XOR child unchanged. The exact recovered verifier accepted all four packets, retained 15 paid K4 nodes, and emitted the same 30,714-check summary hash. At $H=8192$ the certificate grew by 4,095 bytes.

This is **not** an UNSAT-soundness break and not a smaller proof. Define

$$
P_E(m)=m\mathbin{\mathrm{AND}}(2^E-1).
$$

For every nonnegative mask in this recovered verifier: AND3 reads the same low bits; $P_E(a\mathbin{\mathrm{XOR}}b)=P_E(a)\mathbin{\mathrm{XOR}}P_E(b)$; the zero-mask sink remains zero; and no node, parent, RHS, support, source clause or table changes. Applying $P_E$ to every row is therefore a cost-preserving normalization. Every mutant projected exactly to the original packet and replayed successfully.

Material consequence: [P2-D1] must distinguish the parser's accepted unbounded mask syntax from the intended declared affine namespace; [P2-D3] must not infer evidence/checking cost from logical-node weight. [P2-C3], [P2-B1] and [P2-B2] remain OPEN.

## IDEA → SEARCH → ITERATE

### IDEA and falsifiers

Hypothesis: equal out-of-range bits on row-bearing AND3 nodes d2 and d5 cancel at their immediate XOR child d12 and are accepted at unchanged node cost.

Falsifiers were: (1) all mask bits are range-checked; (2) AND3 reads the high coordinate; (3) the bit survives into d12 or the sink; (4) exact replay fails. All failed. Hostile controls succeeded: one unpaired ghost was rejected; an in-range bit outside d2's support was rejected; a malformed hexadecimal mask was rejected.

### SEARCH ledger

Project reads:

- proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b;
- proof2.txt blob 6ec35582c6abd775e026af63548ef8f31ff4c93c;
- governing handoff blob c3889a3e514ddbd747150dcb68607013a3b2d154;
- AGENTS.md 19656af102604d5f0a721d548cf2e4e72a063561; CODEX.md 754999f50de93cdb693ed37bc8110d31e9e698ef;
- project skill b8df83a7b0b1428f349b0e02ce1387d979e8db7f, red-team mode c211e9f545f94b636b119f1e721b475a31e925f9, protocol 25b38dc02bc0b0331ed03b0a4c7ff1b1e2a4ed00;
- LSPV-5/413 a80ba04046046f7b2c71aa451547474bea62d269; LSPV-1/480 b486bc329279621d96c50ea7d171c96bce7a1aaf; LSPV-3/477 325d93673b8e404dc8fe6ee5bdfcbb0ec5d751ed;
- actual Grok path GROKPROOF/2026-11-06_2316_PROGRESS.md, blob a20fb8b3640d7574faf238a4a83a021bb0984808;
- actual Claude path research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex, blob 79e4d4e7e0e3edff3aba8610852c45534bdde128.

Issue #3 body was read. Full 1,220-comment enumeration failed with Transport closed, so complete thread readback is not claimed.

External delta review:

- konard/p-vs-np at ecedd2b45f1c524d85c00b2da27a9c140025550c: proof-status manifest 93b77ed3d8fe456f81c690035f45f07910a247f2 and finite-machine model 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3. Scoped formal statements; no /341 namespace or transfer.
- blkph0x/p-vs-np-proof-research at 7dedc73f758dfbdc072e7aa29dfc08505761ebd5: METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and external audit 36780d81568b3d357c915b425d4a90002b4c8e5e. Restricted methods; no historical parser.
- meelgroup/frat-xor README 38a137bca4d4ab6443703d4c31fba5783021c581, tanyongkiam/cake_lpr README e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, and peitl/short-proof README 93d2090dba9739bc4983c65ea639a24e1f5e0fab supply format/checker or Resolution controls, not historical equivalence.
- openai/math README cc5b0a03bca6c742f045d683b6647a6f44ef2cae and anthropics/formal-math README 1df53bfc14a022088d1b5757698f692bf79390b4 require result-specific verification. Targeted github.com/openai code search returned no relevant result.

Primary literature checked: Chvátal–Szemerédi random 3-CNF Resolution hardness (DOI 10.1145/48014.48016), Urquhart expander-Tseitin Resolution hardness (DOI 10.1145/7531.8928), and Cook–Reckhow proof systems (DOI 10.2307/2273702). None specifies the byte namespace. Public web search was available; a separately identifiable Google-branded interface was not, so Google-specific execution is not claimed.

The local workspace contained replay artifacts but not a repository checkout/preflight script. Local preflight and report-check commands could not run. Root main.tex again returned an empty payload at blob 68188a24badda635a5983fda1c381cdb694fd497 and was not edited under the outside-byte preservation safeguard.

### ITERATE

The exploit hypothesis held, but the claim was revised downward after proving the projection theorem. Ghost bits can make explicit evidence arbitrarily large at fixed logical work, yet create no low-coordinate affine content and delete cost-preservingly. Repair: reject rows with mask shifted right by E nonzero, or canonicalize every row by $P_E$ before charging/checking. This is proved only for the recovered source/AND3/XOR verifier; it does not authenticate RES, LOCAL-CONVERT, DEF or assumption discharge.

## Exact witness and controls

- Checker SHA-256: 0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae.
- Base certificate: 197,514 bytes, SHA-256 12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95.
- Exact mutation: d2.row.mask and d5.row.mask each XOR $2^{8192}$.
- Mutated full packet: 201,609 bytes, SHA-256 2192cca5e56762995fd55fd17c7cb44fc8c92ced7a5c240c84713f420e25d051.
- Baseline and mutant checker output SHA-256: af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be.
- Projection reconstructs the base object and base packet exactly.

The raw ledger contains complete masks, hashes, acceptance/rejection results and exact delta, so the accepted bytes are reconstructible rather than summarized semantically.

## Work/span/resource ledger

| Resource | Baseline | $H=8192$ mutant | Meaning |
| --- | ---: | ---: | --- |
| Distinct paid K4 nodes | 15 | 15 | logical work unchanged |
| Unit-weight critical path | 6 | 6 | span unchanged |
| Certificate bytes | 197,514 | 201,609 | +4,095 |
| Checker output bytes | 1,469 | 1,469 | identical digest |
| Checker wall time | 0.188 s | 0.173 s | one replay only |

The harness charged construction, mutation, temporary output, parsing and checking; the full run took about 2.2 s. JSON/BigInt parsing, storage and retrieval grow with explicit evidence length despite fixed logical work. Peak RSS was not instrumented and is not claimed. No discovery/search runtime is inferred from ideal certificate replay.

## Established-family ledger

| Family | Encoding/size | Published theorem and model | Shortcut control | Remaining transfer |
| --- | --- | --- | --- | --- |
| Chvátal–Szemerédi [P2-F8] | $n$ variables, $6n$ indexed clauses iid over $8\binom n3$ proper signed clauses, $\Theta(n\log n)$ bits | w.h.p. UNSAT and $(1+\epsilon)^n$ ordinary shared-DAG Resolution clauses | ER, PC/PCR, XOR, branching and all mixed rules remain legal | all-rule source-authenticated retraction |
| Same random family [P2-F9] | clause polynomial encoding plus Boolean axioms | linear PC degree and exponential size consequences in stated fields/systems; bounded-DNF PCR remains restricted | GF(2), extensions, reconvergence | full historical mixed backtranslation |
| Odd cubic Tseitin strict 3-CNF | $3h/2$ edge variables and $4h$ proper clauses | exponential ordinary Resolution on expanders | authenticated affine proof has $4h-1$ nodes | unsuitable as all-mixed witness without restriction |

Certified UNSAT, restricted proof-size hardness and empirical difficulty remain distinct.

## Tracker decision

Material changes: update [P2-D1], update [P2-D3], add [P2-L5-414]. No change to proof1.txt. [P2-C3], [P2-B1], [P2-B2] remain OPEN.

## Artifacts

- experiments/review/lspv5_414_affine_ghost_port_audit.py, SHA-256 5fe2d149375a18c4d159a7e15c470a91749a1b8ac6e7b823aff59f5e2b6f0ac7;
- experiments/review/verify_lspv5_414_affine_ghost_port.mjs, SHA-256 50ab3efe2815a3360c9ccf08737c23a985e1127aad92050c7732532366828fee;
- results/raw/review/2026-11-07_0950_LSPV5_AFFINE_GHOST_PORT414.json, SHA-256 c10ab3e84803263764e9f15c34f5eacae3d0ff0036fbf7c6b79c431b503bffbc;
- independent Node replay: 37 assertions, PASS.

## Remaining gap

Recover a historically authorized full mixed parser, or one accepted trace where RES output feeds AND3, then audit all native namespaces and prove a polynomial source-authenticated all-rule retraction. Only then could restricted lower bounds address [P2-B1]; [P2-B2] separately needs a noncircular same-calculus compiler/invariant. **P versus NP remains OPEN.**

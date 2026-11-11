# LSPV-3/579: Terminal-live shared paid-owner source-copy macro in the original /386 checker

**2026-11-11 15:24 PST | Hypergraph & Proof Certificates | Historical Route B | PROVED/RESTRICTED (constructive), COMPUTATIONAL (unchanged historical core hosted V8). P versus NP OPEN.**

## Candidate and fixed pre-search falsifiers
Candidate: m original signed SOURCE clauses containing the same signed literal can all be routed through a single pair of genuine signed paid AND2 owners, a single paid false-unit RES and three additional paid RES per clause. Every new node can lie on the final proof DAG, with original source unchanged. Incremental logical cost is **3+3m** relative to a refutation with no such detour, rather than 6m from fresh two-owner/four-RES copies for each clause. No optimality claim.

F1: some shared facet, oriented RES, chronology, signed-input or owner/freshness condition fails the pinned original checker. F2: a new node is terminal-dead after replacing parent references. F3: a SOURCE clause, provenance, charged owner count or complete original source changes. F4: a wrong pivot, changed signed SOURCE, illegal facet, parent, output or underpayment is accepted. All were checked; none occurred in the finite witness.

## CORPUS REVIEWED and duplication audit
Reread both complete root proof trackers at blobs f46f6aae25571340a5fd17a5181d51c271509947 (proof1.txt) and 42943fe447c6061fb8009a526f46ac8a6684765c (proof2.txt), issue #3, AGENTS.md, CODEX.md, the required pnp-research skill, five-role current handoffs, LSPV-2/341 and /386 original checkers, LSPV-3/539-549 and /576-/578, LSPV-1/579-/582, LSPV-2/565, LSPV-4/551 and LSPV-5/496, plus source-binding, fanout and DEF-facet prior work. Repository code search for shared complementary batch copies found no identical terminal-live construction. This **extends**, not supersedes, LSPV-3/577's one-source terminal-live copy and LSPV-1/582's four-source *terminal-dead weakening* macro. LSPV-2/549 and LSPV-3/578 show that separately accepted /341 and /386 envelopes cannot authenticate a common source. No full historical R_mix341 dispatcher or exact original cross-rule bytes were located.

Primary literature: Cook and Reckhow (1979), J. Symbolic Logic 44:36-50, doi:10.2307/2273702; Cousot and Cousot (1977), POPL, doi:10.1145/512950.512973; Clarke et al. (2000), CAV, doi:10.1007/10722167_15. Neither these external results nor the restricted sibling proof authenticates missing historical mixed operations.

## Source and authenticated accepted bytes
Historical original checker: experiments/arc/lspv2_386_independent_verify.js (Git blob **338305c0ce101704205e57543756b8127074a986**), unchanged check body; original seed packet: results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json (Git blob **5edeac8fbbe39764cfd3d075acd3c6ce7b5c87fe**). The checker accepts native SOURCE, free genuine DEF facets of globally paid signed-AND2 owners and strict oriented signed RES. It does **not** authenticate AND3/GF(2)/LOCAL-CONVERT/branch/discharge or an external immutable original-source hash.

Pick the four actual terminal-ancestor SOURCE records at indices **0, 3, 5, 6**. Their clean signed clauses all contain +1; index 0 was already copied through the old /577 eight-row bridge. Reuse the existing two globally fresh paid owners z=21=(+1 AND -1), w=22=(-21 AND +1), the same truthful four zero-incremental-cost DEF facets and the single shared paid row 19 deriving [-21]. To copy each of the three other clauses C, put D=C without +1 and add:

```
RES_+1(C, [-1,21,22]) = D U {21,22}
RES_+21(D U {21,22}, [-21]) = D U {22}
RES_+22(D U {22}, [1,-22]) = C
```

The precise nine new native RES records occupy positions 25 through 33. Redirect every downstream parent of old SOURCE indices 3,5,6 to the exact new copy indices **27,30,33** and shift all preexisting later parent offsets by nine. SOURCE 0 is already redirected to original copy 24. The original signed 49 SOURCE records, their provenance, graph/charge/guard specification and all three paid gate declarations remain unchanged. All **17** bridge records 17..33 lie on the terminal empty clause's complete ancestor DAG; 49 SOURCE remain in their original relative order.

**Cost theorem for the exhibited macro:** two paid owners + one RES deriving the shared false unit + three RES per SOURCE copy give **Delta W=2+1+3m**. For m=4, Delta W=15 (vs 24 for four separately owned copies). Original W29 remains the stronger fixed-source refutation upper bound: the added copies are a paid detour, NOT proof that W44 is minimal or a superpolynomial lower bound. Shared nodes are counted once. The final 94-record packet has **49 original SOURCE, four free DEF rows, 41 paid RES, three paid global owners and W=44**, with one original unused owner already present in the W29 baseline.

## Exact original-checker results and hostile controls
Execution used the **unchanged pinned /386 original JavaScript checker body in hosted V8**, replacing only filesystem, console, diagnostic SHA-256 printing and structuredClone transport adapters. The hosted digest string is explicitly *not* cryptographic. The standalone OS Node.js reproduction program was written, source-pinned and Git-published, but **was not executed as an OS subprocess by this run**. The script permits later exact original OS CLI reruns.

- Four source-copy positive variants (m=1,2,3,4): **4/4 original-body ACCEPT**, with W=35,38,41,44; respectively 85,88,91,94 records. Each acceptance independently executes the archived checker's eleven internal destructive controls.
- All source packets retain the complete original signed SOURCE records. All new bridge records are ancestors of the terminal empty clause in every variant.
- Nine additional hostile mutations were **9/9 rejected by the original checker**, including wrong pivot, reversed oriented parents, forged SOURCE literal, false facet, future parent, underpayment, bad copied clause, falsified shared false unit and bad facet owner.
- At m=4 the accepted JSON is **6023 UTF-8 bytes** in ASCII serialization and passes **7,237 archived-checker assertions** including its own eleven negative controls. The new source-preserving terminal-live bridge contains 17 records and uses exact count-once W44.

The accepted byte packet is at [results/raw/arc/2026-11-11_1524_LSPV3_579_SHARED_LIVE_BATCH_ACCEPTED_PACKET.json](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1524_LSPV3_579_SHARED_LIVE_BATCH_ACCEPTED_PACKET.json), raw execution manifest at [results/raw/arc/2026-11-11_1524_LSPV3_579_HOSTED_V8_ORIGINAL_CHECKER_RAW.json](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-11_1524_LSPV3_579_HOSTED_V8_ORIGINAL_CHECKER_RAW.json), and standalone original Node.js CLI reproduction code at [experiments/arc/lspv3_579_terminal_live_batch_copy.cjs](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_579_terminal_live_batch_copy.cjs). These are separate from a claim of actual machine time, verifier span, evidence-bit complexity, or peak physical memory.

## What changed relative to root MAIN; adopted / rejected / retired
**New:** an accepted original-body 4-source terminal-live shared-copy DAG and a 1+3m progression, plus a concrete rejection set. **Adopted:** historical /386 byte syntax, /577 terminal-live bridge, /582 shared-owner cost accounting and /565 concrete-step inclusion discipline. **Rejected:** per-source payment of the same owner or shared false-unit RES and any claim that every accepted gate is terminal-dead. **Not upgraded:** the unauthenticated full historical R_mix341 mixed calculus, any superpolynomial lower bound, a full mixed alpha/gamma, or an arbitrary SAT algorithm transfer. No existing MAIN mathematical claim becomes invalid; MAIN could not be fully read safely, so reconciliation was blocked.

## Proof-chain and CEGAR implications
P2-D1 remains OPEN for complete historical accepted bytes, including true RES->AND3 / DEF->LOCAL-CONVERT/GF(2), branches, contexts and source binding. This is a new accepted-byte sublanguage witness, not the required full mixed grammar. P2-C3 remains OPEN: a full concrete configuration and every native abstract transformer with cost no greater than concrete remain missing. Any CEGAR invariant excluding shared terminal-live owner descendants would improperly reject these genuine paths; host-accepted paths must be retained. P2-B1 remains OPEN, with separate P2-B2/B3 OPEN and P1-01/03/04 OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** The root proof1/proof2 files were read with current SHA. No user role identity, title, Pacific schedule, historical weights, source boundary, or **TWO Route A / THREE Route B** allocation was changed. The entire original source for the /386 seed is independently pinned by Git, not by the historical checker itself. Original OS Node execution and main.tex authorized-region write remain blocked/pending, respectively.

**One next test:** independent LSPV-5 native Node OS subprocess run of the experiments/arc/lspv3_579_terminal_live_batch_copy.cjs script, then attempt authentic original-source-bound cross-rule mixed transitions against a single recovered original R_mix341 checker. P versus NP remains OPEN.

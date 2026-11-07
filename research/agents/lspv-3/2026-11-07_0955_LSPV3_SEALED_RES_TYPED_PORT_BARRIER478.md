# LSPV-3/478 | Sealed RES-to-factor port theorem for Resolution-hard 3SAT

**2026-11-07 09:55 PST | PROVED/RESTRICTED + COMPUTATIONAL | Route B | P versus NP OPEN.**

Exact nodes: [P2-D1], [P2-C3], [P2-D2], [P2-B1], [P2-B2], [P2-L5-413], [P2-L3-477]; new evidence [P2-L3-478]. Route-A [P1-01], [P1-03], [P1-04] unchanged.

## IDEA and falsifiers

Hypothesis: a *distinct* sound, complete sealed typed completion S of the historical /341 source/AND3/XOR fragment, adding binary Resolution but **no RES-derived-clause-to-factor port**, has exactly ordinary Resolution proof minima on strict 3CNFs whose original clause supports are distinct unordered triples.

Falsifiers: source factor already has an affine row; AND3 accepts union support >3; XOR consumes raw factors; some historically authorized conversion exports RES-derived clauses as AND3 factors without an explicit port. The first three are inconsistent with the recovered /341 verifier; **the fourth remains OPEN for the full historical mixed calculus**.

## SEARCH and exact family ledger

Read both full shared proof trackers, current coordination issue #3, November 2 five-role handoff, AGENTS.md, CODEX.md, research skill, LSPV-3/477 and /476, LSPV-5/413, LSPV-1/480, and current Grok and Claude files. Historical verifier experiments/arc/lspv2_341_independent_verify.js blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0 accepts source factors, AND3 with union support <=3, and XOR of two row-bearing inputs, but rejects RES, DEF and LOCAL-CONVERT tags. Historical producer blob 4081022e8a3841d79f751a3d3a7a10decbb026da; exact source/proof packet blob fe27fe1011d0021e721ccaeb747ed58da65d7464. Peer LSPV-5/413 authenticated its provenance and earlier exact finite replay, not a full mixed grammar.

Known family: Chvátal and Szemerédi, *Many Hard Examples for Resolution*, J. ACM 35(4):759-768 (1988), DOI 10.1145/48014.48016. For m=6n independently uniform random proper signed 3-clauses on n variables, UNSAT and ordinary DAG Resolution length >=(1+epsilon)^n occur with probability 1-o(1) for some epsilon>0. Probability two of the m supports collide is <=binom(6n,2)/binom(n,3)=O(1/n); encoded signed indexed binary size N=Theta(n log n). This is an *established ordinary Resolution lower bound*, not all-calculus or machine hardness.

External change-aware reviewed blobs: konard/p-vs-np/scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr/README.md e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; peitl/short-proof/README.md 93d2090dba9739bc4983c65ea639a24e1f5e0fab; openai/math/README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae. Pang arXiv:2610.00837v2 is a separate Res(PC_r) proof-system control, not a bridge. Indexed web search used, no separate Google-branded interface used. No PDF analyzed.

## ITERATE: Theorem 478.1 (PROVED/RESTRICTED)

Define **DISTINCT** proof system S, not historical R_mix341: every original proper signed 3-clause has a free authenticated clause view for ordinary unit-paid binary Resolution and a free exact three-variable factor view for AND3. RES only produces clauses; AND3 only accepts two distinct factors with support union <=3, creates a factor and may carry a checked exact affine alias; XOR requires two row-bearing premises and produces an affine line. No RES-to-factor coercion, LOCAL-CONVERT, DEF, weakening or new split/discharge rules. Proofs are source-authenticated shared DAGs charging distinct nodes once, all unit weights. This system is sound and complete because RES is sound/complete.

**For every proper strict-3CNF F having pairwise-distinct original three-variable supports:**

$$
W_S(F)=W_{\mathrm{Resolution}}(F).
$$

Proof: select the earliest factor/row paid inference in any topological ordering. RES lines remain clauses and cannot feed AND3. XOR cannot be the first affine inference because source factors have no rows. AND3 cannot be first because its two distinct original factor antecedents have union support >=4. Hence no factor or affine inference exists in any such proof. All paid nodes are RES. Every ordinary Resolution refutation is an S refutation with identical paid work, proving equality, including arbitrary legal DAG sharing. QED.

**Corollary (published hard family):** with probability 1-o(1) at density 6. Subtract at most m=6n original axioms if a cited Resolution-size convention counts source lines rather than paid inferences:

$$
W_S(F_n)\ge(1+\epsilon)^n-6n\ge\exp(\Omega(n))=\exp(\Omega(N/\log N))\quad\text{for sufficiently large }n.
$$

This proves a superpolynomial lower bound only for the explicitly **new sealed S**, **not** for the historical full R_mix341 or arbitrary SAT algorithms. It improves the interpretation of [P2-L3-477]'s *incomplete* native-fragment obstruction: a separately defined complete RES completion is also hard if it forbids an effective cross-type bridge.

## Sharp typed bridge control

Original SAT clauses with x=1,a=2,b=3,c=4:
$C_1=(x\lor a\lor b)$, $C_2=(\neg x\lor a\lor c)$, $C_3=(\neg a\lor b\lor c)$. Supports are distinct. RES(C1,C2 on x) produces $D=(a\lor b\lor c)$; a **proposed, paid PORT1**, not historically authenticated, converts this RES-derived clause to a factor. AND3(D,C3) then computes exactly

$$
(a\lor b\lor c)\wedge(\neg a\lor b\lor c)\equiv b\lor c.
$$

This uses one RES, one proposed paid PORT1, one AND3 (3 paid nodes); without PORT1 the transition is illegal in S. This local source is SAT, not an UNSAT refutation or an asymptotic shortcut proof. The exact needed historical interface is accepted RES->LOCAL-CONVERT->AND3 with original-source provenance, charged facets and assumption/port scope.

## Independent finite control and resource ledger

Python producer: n=9, m=54, seed 20261107, **distinct supports sampled without replacement**, random signs, 525-byte original DIMACS SHA256 0a3c16ac039c9ae84b0517bbba8c6a0304b54e7b2a53c98659c8879495d01542, 0 SAT over all 512 assignments. Davis-Putnam searched 18,134 RES pairs, generated 495 distinct paid intermediate RES nodes then pruned to 28 live paid RES and 23 original-source ancestors. The 28-node refutation is a legal **upper bound**, not the global minimum; n=9 is not certified hard. Python 352 assertions and 4 negative categories. Independent Node: 1,276 assertions, four corrupted/malformed/typed controls rejected. Python 0.0328 sec and RSS 96,416 KiB including interpreter; live proof JSON 3,409 bytes. Actual work charges failed candidates, temporary nodes, parsing, pruning, verification, source reads and output; ideal W excludes search by definition. No claimed optimum span/space schedule, no FLMV machine exponent bound. The authoritative historical /341 checker was NOT executed anew.

Full source/proof fixture, executable producer, separately implemented Node verifier, raw data and SHA256 manifest are in the separate LSPV3_478_SEALED_PORT_BARRIER_REPRO.zip. Public compact code below independently checks the proposed local port witness.

## OPEN obligations

[P2-D1] historically accepted full mixed byte grammar; [P2-C3] legal charged RES/LOCAL-CONVERT/AND3/DEF and GF(2) normalization across shared branch contexts; [P2-B1] whole-calculus superpolynomial Wbar; [P2-B2] same-R noncircular B3 remain OPEN. Known Haken Resolution lower bounds, Cook ER and Tseitin GF(2) shortcut controls remain admissible for testing. Root main.tex returned empty content at nonempty blob 68188a24badda635a5983fda1c381cdb694fd497, so it was left unchanged. Exactly five existing agents with the two Route A / three Route B allocation, historical rules, weights, schedules and enabled states remain unchanged. **P versus NP OPEN.**

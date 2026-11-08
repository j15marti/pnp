# LSPV-3/497: Source-only AND3 closure, duplicated inputs and support normalization

**2026-11-08 02:51 PST | LSPV-3 Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Node IDs:** [P2-L3-497] refines [P2-L3-496], [P2-L1-472], [P2-L5-412] and evidence under [P2-D1], [P2-C3], [P2-F13]. [P2-B1], [P2-B2] remain OPEN; companion [P1-01], [P1-03], [P1-04] unchanged. Historical rules, weights and five-agent allocation unchanged.

## IDEA, before search: hypothesis and falsifiers

Hypothesis: The LSPV-3/496 earliest-non-RES argument implicitly assumes distinct AND3 parents. The minimum-cost result nonetheless survives arbitrary repeated parents, and can be strengthened to sources containing up to three distinct signed clauses per unsigned support triple, if AND3 outputs retain their explicitly declared union support.

Falsifiers: F1, legal AND3(source,source) defeats the literal earliest-non-RES proof; F2, fewer than four signed width-three clauses on one triple yield an exact nonconstant affine row; F3, free semantic minimization of factor support permits cross-triple mixing; F4, the historical grammar provides RES-to-factor, LOCAL-CONVERT or DEF access omitted from the restricted calculus. F1 and F3 have explicit positive witnesses, F2 fails in exact exhaustive enumeration, F4 remains OPEN.

## SEARCH and precedence ledger

Both complete root trackers read at initial head: proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters; proof2 blob 98a1f9cd17fd62d803ab94ffc4ee5bc8bee9dbc2, 376,201 characters. Examined coordination issue #3, the November 2 governing five-role handoff, AGENTS.md, CODEX.md and the pnp-research skill. Project primary grammar: LSPV-2/341, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Compared LSPV-3/496 blob a27e0c8cf71defcadcfe8fcf685bc2958b4191c2, LSPV-1/472 blob 8170381ec26036b1029ee140b27bfb660891c93c, LSPV-1/500, LSPV-5/412 executable, LSPV-3/419 and LSPV-4/409. Prior sparse parity certificates and the specific four-source two-support XOR counterexample were already documented. Neither is claimed novel.

Actual Grok file GROKPROOF/2026-11-08_0930_PROGRESS.md and Claude world-ledger README inspected. External pinned source files reviewed: konard/p-vs-np scripts/proof_status.json (93b77ed3); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea); meelgroup/frat-xor format.md (986a21aa); tanyongkiam/cake_lpr README.md (e94f45e9); peitl/short-proof README.md (93d2090d); openai/math README.md (cc5b0a03). Their formats are not historical R_mix341 authority. Indexed web searched Chvatal-Szemeredi, Haken, Cook ER and Pang 2610.00837v2; direct Google-branded UI unavailable.

**Hard-family ledger.** Chvatal and Szemeredi, Many Hard Examples for Resolution, JACM 35(4):759-768 (1988), DOI 10.1145/48014.48016: random signed proper strict-3CNF with n variables and m=6n original clauses, binary input size N=Theta(n log(n+2)). With high probability it is UNSAT and needs exp(Omega(n)) *ordinary shared-DAG Resolution* inferences. The birthday collision probability for unsigned supports is O(1/n). This is no lower bound against ER, GF(2), historical full mixed rules, or arbitrary SAT algorithms. Haken PHP ordinary Resolution hardness, Cook ER shortcuts, Pang syntactic characteristic-two/three bounds and Tseitin GF(2) remain mandatory controls.

## ITERATE: the fixed distinct grammar and exact proof

Define R_tag,sticky as follows. An authenticated SOURCE strict proper 3-clause has clause and factor views on its declared three original coordinates. RES takes two clauses, produces clause-tagged nodes of any width. AND3 takes SOURCE/AND3 factor parents with union of *declared* original supports at most three, emits their exact pointwise conjunction while **retaining that union as output support**. A single GF(2) equation may be annotated only if exactly pointwise equivalent to the factor. XOR takes two previously authenticated row-bearing parents. There is no implicit RES-to-factor, paid DEF, LOCAL-CONVERT, case discharge or support shrinkage. All derived nodes are unit-paid in an acyclic shared DAG. Identical AND3 parent IDs are permitted in R_tag,reuse but disallowed in a separately defined DISTINCT variant. Neither is the historical calculus.

**Theorem 497.1 (PROVED/RESTRICTED).** Every SOURCE/AND3 factor has support equal to ONE unsigned source triple T and represents a conjunction of k distinct signed source clauses with support T, excluding exactly k of the 8 assignments on T. A live binary-premise DAG producing that factor needs at least k-1 AND3 nodes, attained by an ordinary conjunction tree, irrespective of repeated parents or reconvergence.

**Proof.** Source factors have three-element support. Since AND3 is allowed only if the support union has at most three variables, both parents and their output share the identical source triple. A signed proper 3-clause excludes exactly one local assignment, distinct sign choices exclude different assignments, and repetitions are idempotent. The ancestor graph containing k indispensable source leaves and q paid binary nodes is connected with k+q vertices but at most 2q premise edges, giving q>=k-1. A binary tree attains the bound. QED.

**Theorem 497.2 (PROVED/RESTRICTED).** A source-only factor has an exact nonconstant *single* GF(2) row annotation iff k=4 and its four excluded assignments form a codimension-one affine coset of F2^3. There are exactly 14 such packets, from seven nonzero masks and two RHS values. Three paid AND3 inferences are necessary and sufficient. With k<=3, no row can be annotated; k=8 produces a constantly false factor. A nonconstant affine row has four local satisfying assignments, and the conjunction has 8-k, so k=4; the hyperplane enumeration and Theorem 497.1 complete the proof.

**Corollary 497.3 (PROVED/RESTRICTED).** If every unsigned triple supports at most three *distinct signed* source clauses, then

$$
W_{R_{\mathrm{tag,sticky}}}(F)=W_{\mathrm{RES}}(F).
$$

There is no source-only affine seed, hence no XOR; AND3 factors cannot enter RES, so every live contradiction proof may be pruned to ordinary Resolution at no extra cost, and every RES proof is legal. This is a full-DAG result for the distinct fixed grammar, allowing sharing, self-pairs and arbitrary Resolution width; it is stronger than /496's pairwise-distinct-triple hypothesis. The published Resolution-hard random 3-CNF family transfers at its ORIGINAL encoding to this restricted calculus, but not to historical R_mix341.

**/496 proof repair.** The prose asserted that an earliest non-RES AND3 must have two distinct source factors. Distinctness is not automatic. The /496 JavaScript explicitly rejects identical parent IDs. In a REUSE variant, AND3(s0,s0) is legal and idempotent; such dead nodes do exist. The correct minimum-work proof is the factor-semilattice argument and pruning above, not the claim that no non-RES node can exist in an untrimmed certificate.

**Typed support-shrink obstruction.** A separate R_tag,shrink permits an AND3 output to discard inessential input coordinates. The already documented LSPV-1/472 four proper strict-3CNF clauses

$$
(x\lor y\lor a),\ (x\lor y\lor\neg a),\
(\neg x\lor\neg y\lor b),\ (\neg x\lor\neg y\lor\neg b)
$$

require only two signed clauses on each unsigned support triple. Two paid AND3 outputs normalize to x OR y and NOT x OR NOT y, both on support {x,y}; a third yields the exact affine row x XOR y=1. In STICKY mode the two intermediate factor supports remain {x,y,a} and {x,y,b}, so the final AND3 has illegal union size four. This is a legitimate *different-grammar* shortcut, NOT an UNSAT proof or general size separation. Historical support-retention vs legal LOCAL-CONVERT remains OPEN and must not be decided by convenience.

## Verification and fully charged resource boundary

Deterministic JavaScript enumerated all 256 subsets of eight signed strict-3-clauses on one triple: exactly 14 4-clause affine packets, none with k<=3. It passed 1,230 assertions and rejected five hostile controls. Independent Python computed the same classification by a separate truth-table enumeration. Both verified the unchanged /477,/496 n=9,m=54 original UNSAT source by 512 assignments; original K4 odd-charge UNSAT, even-charge 8 models, and all 16 single-clause-deletion SAT controls. Finite checks do not verify published asymptotic hardness or historical byte acceptance.

The k-source factor tree charges k-1 distinct logical nodes and has optimal unlimited-parallel unit-depth ceil(log2 k). Source references and paid gate IDs occupy O(k log(m+k+2)) explicit bits; constant three-variable truth tables require 8 bits per factor. A constructive local checker pays O(8k) truth checks plus reading, indexing and externally authenticating original signed clauses. Executed local JS wall 0.03s with 31,988 kB max RSS; Python 0.71s with 95,908 kB max RSS. Actual all-phase time/peak memory also pays source/head acquisition, discovery, failed policies, uploads, output, readback and caches. No implication from W_R to same-machine running time follows. A complete expanded independent reproduction with SHA-256 manifest is available separately.

**Artifacts:** this report; experiments/arc/lspv3_497_source_closure_public.cjs; results/raw/arc/2026-11-08_0251_LSPV3_497_SOURCE_AND3_RAW.json; research/coordination/2026-11-08_0251_LSPV3_SOURCE_AND3_CLOSURE497_HANDOFF.md.

**Actual advance:** corrected /496's hidden distinct-parent premise, exact 14-packet source closure, stronger fixed-grammar minimum-work transfer, and a support-normalization typed countercontrol. **Still OPEN:** [P2-D1] original-byte RES/DEF/LOCAL-CONVERT/AND3/GF(2) grammar, [P2-C3] all-rule normalization, [P2-B1] superpolynomial worst-case minimum for the full fixed mixed calculus, [P2-B2] genuinely noncircular same-calculus B3. P versus NP OPEN.
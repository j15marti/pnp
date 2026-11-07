# LSPV-1/463: Fixed-decider-trace disjoint-padding firewall for B3

**2026-11-06 PST, America/Los_Angeles. Route B lead.**
**Status: PROVED/RESTRICTED for ordinary shared-DAG Resolution and disjoint satisfiable circuit gadgets; COMPUTATIONAL for independently replayed finite controls; historical R_mix341, B1/B2/B3, P versus NP OPEN.**

## 1. IDEA, exact hypothesis and falsifiers

**Node IDs:** [P2-B2], [P2-B3], [P2-B6], NEW [P2-B7], controls [P2-F8], [P2-F9], [P2-D1], [P2-C1], [P2-C3], cross-chain [P1-X3]. Both /proof1.txt and /proof2.txt were read on main before this work, at complete blob SHAs edf29de056457fa806e9d5ebc7548bf6f110505a and 9f65c1936652d7e0eb298ee2516960aa88877b25.

Initial hypothesis: a *fixed-input* circuit encoding a hypothetical polynomial-time SAT decider's rejecting computation can be cheaply checked but cannot, merely by being conjoined as a satisfiable gadget disjoint in variables from the original F, bypass ordinary Resolution hardness of F.

Falsifiers stated in advance:
1. The new circuit gadget itself is UNSAT or shares original SAT-assignment variables, violating the disjoint-satisfiable hypothesis.
2. Adding such a gadget produces a shorter ordinary Resolution refutation despite legal closure under a satisfying restriction.
3. The supposed short rejection certificate sneaks in a non-original output=1 assumption and falsely calls it a source-authenticated refutation of F.
4. The proof is applied to full historical R_mix341 without rule-by-rule restriction simulation or authenticated paid definitions.

The tests rejected F3's tempting *incorrect test predicate*: a proof containing an extra BAD_OUT axiom **does** refute the augmented formula, regardless of F. The control was repaired to remove that axiom when checking the original source. The other falsifiers were excluded at exactly the restricted scope above.

## 2. Primary literature and existing-source review

* Chvátal and Szemerédi, "Many Hard Examples for Resolution", J. ACM 35(4), 759–768 (1988), DOI 10.1145/48014.48016: for fixed c=6, k=3 with c/2^k=3/4>=0.7, an indexed independent uniform proper signed 3-CNF distribution with n variables and m=6n clauses has, with probability 1-o(1), UNSAT formulas whose ordinary shared-DAG Resolution refutations use at least (1+epsilon)^n clauses for some epsilon>0. Exact source vocabulary is all 8*binom(n,3) signed proper triples; repetition permitted. Encoded source bits Theta(n log n). This is ordinary Resolution only and is not a finite per-instance hardness certificate.
* Cook and Reckhow (1979), J. Symbolic Logic 44: polynomially bounded SOME proof system iff NP=coNP, not polynomial proof bounds for the fixed R_mix341.
* Pich and Santhanam (2023), ECCC TR23-199 / arXiv:2312.08163: self-provability/witnessing and bounded-arithmetic hypotheses are significant in proof-to-circuit transfers; none supplies our historical B3.

Repository review, authenticated actual file blobs: j15marti/pnp/research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (c3889a3e514ddbd747150dcb68607013a3b2d154), current issue #3 with 1139 comments including LSPV-5/399, GROKPROOF/2026-11-06_2316_PROGRESS.md (a20fb8b3640d7574faf238a4a83a021bb0984808), research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex (79e4d4e7e0e3edff3aba8610852c45534bdde128), LSPV-1/462 clocked-B3 control (19789993c849d290e2b4368b4ba41a2ce29e83d7), LSPV-3/462 dual-section (c80c8765062961466a4fa115c16b7055bb11767b), LSPV-5/399 random-3-CNF PCR report (d54cef95ea9f367da2c0838bfaec075bcc2ae200), AGENTS.md, CODEX.md and project skill. External konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) confirms only finite-machine P subset NP; blkph0x/p-vs-np-proof-research README.md (f397a7747eaca82df3d754d0a4b4bab1fe10f814) documents scoped Reed–Muller and CDCL results rather than all-input separation; its proof_producing_cdcl_lab/PUBLIC_SAT_BASELINE.md (9e09b19aba57973ed8867794741c5006d47ed3b7) separates UNSAT proof checking from SAT discovery. meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f) demonstrates authenticated XOR steps but no equivalence with historical R_mix341; tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c) documents certified checking of its declared LPR format. openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae) warns not every manuscript is formalized. Targeted primary search via web ran; Google-specific engine was not separately accessed. No external source is claimed to prove the proposed historical transfer.

## 3. Theorem: disjoint satisfiable computation padding is Resolution-inert

Let F be any UNSAT CNF over variable set X. Let G be any SAT CNF over Y, with X intersect Y empty, and let S_RES(F) be the **minimum number of distinct unit-paid binary Resolution inferences** in a valid shared refutation DAG from F, with no free weakening or extension rules. Then

$$
\boxed{S_{\mathrm{RES}}(F\land G)=S_{\mathrm{RES}}(F).}
$$

**Proof.** Every valid refutation of F also refutes F and G by ignoring G, so the left side is at most the right. Select a satisfying assignment rho of G's Y variables. Given ANY shared-DAG Resolution refutation of F and G, restrict each clause under rho: satisfying clauses disappear and falsified literals are deleted. Standard restriction closure of Resolution yields a valid DAG Resolution refutation of F with no more inferences: after simplifying parents, each old resolution step either becomes a legal resolution step on the same pivot or its child is replaced by a surviving parent's subclause. Prune unused nodes and maintain a topological order. Original F clauses are unaffected and every original G premise becomes true. The empty final clause remains empty. Deduplicating nodes cannot increase cost. Hence S_RES(F) is at most the left side. Equality follows. QED.

This is a standard restriction principle applied as a precise B3 control, not a claimed novel lower-bound technique. The same argument works for any larger fixed calculus **only if** its entire historical grammar, sources, assumption scopes, paid auxiliary rules and node weights admit the same non-expansive restriction construction. No such extension of the theorem is asserted for R_mix341.

**Corollary (known hard strict 3-CNF anchor).** For F_n from the density-six indexed random proper-3-CNF family above and ANY satisfiable G_n on disjoint variables, with high probability

$$
S_{\mathrm{RES}}(F_n\land G_n)=S_{\mathrm{RES}}(F_n)\ge (1+\epsilon)^n-O(n).
$$

Here the O(n) harmless difference is only the conventional distinction between counting all proof clauses and paid inference nodes (at most 6n original premises). The equality itself is exact in the paid-inference model. This establishes **only ordinary Resolution** hardness for the augmented inputs; mixed extensions, GF(2), contextual branching, and extension-variable shortcuts are not covered.

## 4. Cheap deterministic trace, missing source soundness bridge

For any *fixed input* string encoding F, an acyclic fan-in<=2 Boolean circuit C computing a hypothetical SAT decider's output has a conservative Tseitin encoding G(C,F) with hardwired input bits. Its variables are fresh and disjoint from the SAT-assignment variables of F, and G is satisfiable. A standard constant-width truth-table encoding of each binary gate supplies one length-three clause enforcing the actual output bit under the actual inputs. With known input units, at most two correctly oriented Resolution steps derive the gate-output unit (one step for unary gates). Therefore for g gates and a rejecting output bit o=0, the explicit computation trace derives not-o in <=2g paid Resolution steps; assuming o as an EXTRA source axiom creates a short refutation with one more step.

**But (o) is not a legitimate original-source premise.** The rejection trace proves how C evaluates on the encoded formula; it does not by itself prove F UNSAT in the historical calculus. To establish B3 one needs a rule-specific, source-authenticated and polynomially charged bridge from the correctness assertion "F SAT implies A(F) reports SAT" to a legal derivation in **the same** R_mix341. A correctness theorem holding outside R is not automatically a polynomial native proof. If A's simulated computation instead depends on variables of F, the disjointness hypothesis fails and a separate proof is necessary.

## 5. Independent computational controls

Python producer (full separately preserved reproducibility archive) generated 8 distinct proper signed width-three clauses on three variables, each of which is uniquely falsified by one assignment. Every 7-clause deletion has an explicit SAT witness; all 8 are necessary to refute. A 7-paid-Resolution-node elimination DAG exists; the binary-source-ancestry lemma implies no refutation uses fewer than 7 nodes, so **S_RES(F)=7 exactly** for this finite control.

The disjoint trace is a six-gate XOR/AND/NOT/OR/NAND/NOT circuit using 3 fixed input units and 20 source truth-table clauses. It outputs 0. The proof derives its six gate units with 10 Resolution nodes; the spurious BAD_OUT source gives one additional contradiction node. Exact conclusion: 7 authentic source-Resolution nodes vs 11 legal steps for the **different augmented problem** with BAD_OUT. The latter is NOT a refutation of original F.

Python replay: 446 assertions, 6 corrupted certificate/source controls rejected, 0.66 s measured wall time, 96,528 KiB peak RSS. Independent standalone Node.js replay: 166 assertions, 6 adversarial controls rejected. Separate source and proof DAG hashes in fallback archive. These measurements cover these implementations, not machine-time lower bounds. No authoritative R_mix341 checker or full historical grammar replay ran. No Google-specific search or repository preflight execution was performed. Root main.tex returned blob 68188a24badda635a5983fda1c381cdb694fd497 but no contents, and was NOT edited.

## 6. Formal ledger and next proof obligations

| ID | Status | Specific effect |
| --- | --- | --- |
| [P2-B2] | OPEN | Cheap rejecting computations do not supply legal R_mix341 refutations; the exact decider-correctness-to-native-derivation bridge is still missing. |
| [P2-B7] | PROVED/RESTRICTED | New disjoint satisfiable trace-padding equality in ordinary Resolution, including the published density-six random strict-3-CNF family. |
| [P2-B1] | OPEN | The above hard family is not known hard against all historical mixed rules. |
| [P2-D1], [P2-C3] | OPEN | Native bytes, definition facets, LOCAL-CONVERT and assumption-scoped sharing still require authentication. |
| [P1-01], [P2-A2] | OPEN | This result does not construct a polynomial SAT decider or an all-input FLMV contraction. |

**Next:** LSPV-3 and LSPV-5 should test whether each historical R_mix341 rule preserves, simulates, or defeats restriction under a satisfiable disjoint trace. If any rule fails restriction stability, construct a LEGAL typed counterexample, not a fake augmented-source contradiction. LSPV-1 should separately investigate a noncircular rule-specific accepting-output bridge. Keep Cook Extended Resolution and Tseitin GF(2) as short-proof upper-bound controls.

**Actual advance:** exact, published-family-anchored Resolution-inertness of fixed-input rejecting traces with corrected source-authentication falsifier. **Verification:** symbolic proof + two independent finite implementations. **Historical mixed transfer and B3 remain OPEN. P versus NP remains OPEN.**

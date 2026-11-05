# LSPV-1/418: Arbitrary-original-CNF public-port Resolution compiler
**November 5, 2026, 06:00 PST. PROVED/RESTRICTED; finite checks COMPUTATIONAL; B1/B2/B3 and P versus NP OPEN.**

## IDEA before SEARCH
LSPV-1/411 proved a public-output clause compiler for three original variables, with an original CNF comprising canonical false-assignment blockers. Hypothesis: an actual falsified original source clause can replace each synthetic blocker, allowing *any* original CNF and k original variables. Falsifiers: accidentally importing blockers, bad pivots on aliased/reconvergent gates, forged source/facet or false target, and unratified historical exported-wire selectors.

## Fixed rule model and crucial EXTRA assumption
Keep the preselected R_mix341 semantic rules and unit weights (LSPV-2/341), but use only strict binary RES, already paid source-independent conservative two-input DEF and original CNF source clauses. Additional **unratified selector assumption:** each paid gate exposes four signed, positional defining CNF facets as individually addressable RES premises. Proposed CANON2 supports this, but historical original /341 bytes and LOCAL private/exported-wire grammar have NOT been authenticated. This does NOT establish full-native normalization or mixed consumer preservation.

## Exact restricted theorem and proof
Let F be arbitrary source-labelled canonical CNF over k>=1 originals, SAT or UNSAT; G contain t>=1 paid acyclic two-input Boolean definitions with aliased/reconvergent inputs allowed. Let C be a non-tautological clause over public outputs such that F and G entail C. There is a uniform strict binary Resolution derivation of some D subset C from **the exact original F source clauses** and the already-paid gate facets, with

$$
q_{\mathrm{RES}}\le (2t+1)2^k-1,\qquad
q_{\mathrm{all}}\le t+(2t+1)2^k-1.
$$

For each original assignment alpha, if alpha violates F use an ACTUAL original clause C_j falsified by alpha, contained in its assignment blocker B_alpha. If F(alpha) is true, evaluate the conservatively unique gate assignment; at least one target literal L_alpha is true. Take the exact facet of each necessary gate for the actual input row and resolve away at most two already-computed true gate input literals, obtaining a guarded true-output clause contained in B_alpha or L_alpha. Each satisfying assignment costs at most 2t strict RES nodes. Merge the 2^k leaves, eliminating each original variable by either inheriting an already-stronger branch clause or strictly resolving the complementary pair. At most 2^k-1 merges yield a clause contained in C. No weakening, synthetic source, source retraction, semantic oracle, or free LOCAL wire is used. Full evidence and checking have bit cost polynomial in original input and t*2^k, not polynomial solely in k-independent input length. For k=O(log N) and polynomial t, the restricted construction is polynomial-size. This is an **upper bound**, not shortest mixed proof cost.

## SEARCH and existing work credited
Read the November 2 12:04 governing handoff, current issue #3, AGENTS/CODEX/research skill, original /341, LSPV-1/411, LSPV-2/357 source splitting/gluing, LSPV-3/413 public aliases and /422 CANON2 facet-gauge, LSPV-4/413 resource checker, REFEREE361 CANON1 retraction/CANON2 repair. The present result is a hybrid extension of /411 and /357, not an academic-priority claim. Actual Grok GROKPROOF/2026-11-05_1218_PROGRESS.md, actual Claude TPORT-0002 and ONETAPE-0001 inspected, all lack B3. Indexed web research of Cook-Reckhow 1979, Haken 1985, Cook ER 1976, Atserias-Muller and Jeavons-Petke. Direct branded Google unavailable. Authenticated github.com/openai/math code queries ExecCNFNodeSearchCosts, CookLevin, LRAT, resolution checker; full-read ExecCNFNodeSearchCosts.lean (SHA 1ced21f4), not a proof translator.

## ITERATE and independently checked computation
Initial invalid approach used fabricated assignment-blockers as free sources; corrected producer chooses real F source clauses. Seed 418, 125 source/circuit cases: 57 original SAT and 68 original UNSAT; 38 deliberately non-entailed targets discarded; five malformed/false producer controls rejected. **3,873** baseline genuine RES steps (maximum 2,433), across 3,608 source assignment rows. Independent Node checker passed **175,757** assertions and rejected eight corruptions. Full raw SHA256 e139f18ed7fe10bc1c6939477a022a812885de974babb91bbfb0c72bd72baa39. Its 15 extra attempted steps arise only during negative mutations, not baseline proof costs. Full scripts and raw records are locally attached; GitHub includes a compact standalone reproducer and summary.

## B3 quantifier / physical cost firewall
Haken's exponential ordinary DAG Resolution lower bound concerns explicit unary PHP(h+1,h), N_h=Theta(h^3 log h), not Extended Resolution or mixed R. Cook's polynomial ER PHP and Tseitin's native GF2 are essential shortcuts. Bit-evidence/output, proof optimizer, verification, source/index reads, caches and peak space remain separate from q. This O(t*2^k) compilation is exponential in unrestricted original support and does NOT convert an arbitrary correct polynomial-time SAT decider into polynomial R_mix341 proofs. B1/B2/B3, native byte grammar, mixed superpolynomial lower bounds and P versus NP all remain OPEN.

**Next:** authenticate original DEF facet/LOCAL exported-wire byte selectors and a downstream mixed-rule translator or original-legal counterexample; independently seek noncircular same-R B3 proof existence.

References: Cook & Reckhow JSL 44 (1979), 36-50; Haken TCS 39 (1985), 297-308; Cook SIGACT News 8(4) (1976), 28-32; Atserias & Müller JACM 67(5) (2020); Jeavons & Petke arXiv:1401.4613.

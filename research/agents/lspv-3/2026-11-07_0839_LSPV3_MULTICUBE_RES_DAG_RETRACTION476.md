# LSPV-3/476: Coherent assumption-cube retraction in shared source Resolution DAGs

**2026-11-07 08:39 PST | Route B | KNOWN standard restriction/deduction principle, independently PROVED/RESTRICTED for the exact model below; COMPUTATIONAL full and independent replay. Historical R_mix341 byte grammar OPEN. P versus NP OPEN.**

Relevant tracker IDs: [P2-D1], [P2-D2], [P2-C1], [P2-C3], [P2-B1], [P2-B2], [P2-L3-463], [P2-L3-467]; evidence [P2-L3-476]. This is a conservative extension of LSPV-3/463's one-literal RES-only split and LSPV-2/262's complete-DPLL source blockers. No new academic originality claimed.

## IDEA and registered falsifiers

**Hypothesis.** Given a source-indexed acyclic strict binary Resolution refutation of the original CNF F together with any coherent cube Gamma of original-variable unit assumptions, compile a source-only binary Resolution DAG deriving a clause contained in the complements of Gamma. It should add no paid nodes, use no weakening, free split, semantically checked entailment oracle, auxiliary branch variables, or other historical mixed rules.

The four falsifiers were (1) a legal consistent-cube branch DAG that cannot be source-retracted; (2) any incorrect pivot/source/ancestor/branch label accepted; (3) a branch inference requiring two or more new paid source inferences; and (4) putative cross-branch sharing that disappears when live root-reachable proof nodes are counted instead of dead cached nodes.

## Theorem 476.1: strict source-Resolution cube retraction

**PROVED/RESTRICTED.** For any original CNF F with nontautological clauses, any coherent set of original-variable literals Gamma, and any source-authenticated acyclic binary Resolution refutation pi of F together with Gamma, let s be the number of distinct paid Resolution inferences in pi. The only paid native step is correctly oriented binary Resolution, original F and temporary unit assumptions have zero premise cost, and tautological derived clauses are omitted. Then there is an ordinary **source-only** Resolution DAG pi' deriving a clause D such that

$$
D\subseteq \{\neg \ell:\ell\in\Gamma\},\qquad W_{\rm RES}(\pi')\le s.
$$

This is the standard restriction/lifting idea applied explicitly to a supplied shared DAG and an arbitrary coherent cube. It is NOT a theorem for every historical R_mix341 operation.

**Proof.** Write N_Gamma for the complements of the assumption literals. Traverse the supplied proof in topological order. Maintain for each clause C either a source-derived witness E_C contained in C union N_Gamma or a SKIP marker if C contains an assumption literal itself. Temporary assumption axioms are SKIP; genuine original axioms not containing an assumption literal retain their exact original indexed source.

For an inference R=Res_p(A,B), mark SKIP if R contains an assumption literal. If R does not, **both parents cannot be SKIP**: each assumption literal in either parent would have to be the eliminated pivot, but a coherent cube cannot contain both signs. With exactly one skipped parent, the other parent has the complement of a positive assumption pivot; that complement belongs to N_Gamma. The other mapped witness therefore already lies in R union N_Gamma, and is reused without charging a step. With neither parent skipped, if both mapped witnesses retain the required complementary pivot, take their exact native resolvent, at cost one. If either witness lost its expected pivot, reuse that witness, which is already a subclause of R union N_Gamma. In this case the pivot variable was not assigned by Gamma, so the complement guard cannot undo this reasoning. Thus each input paid node becomes at most one paid output node, each original proof node is mapped only once even under reconvergence, and no weakening is used. At the terminal empty clause SKIP is impossible; the witness is contained in N_Gamma. QED.

**Two-branch corollary.** Given pi+ refuting F,x and pi- refuting F,not x, this construction derives either empty or the respective opposing unit. If both are units, one additional native RES joins them. An explicit full binary decision tree of supplied branch RES proofs similarly compiles by repeated native RES joins, charging all leaves and at most one join per internal case; this does not compress an exponentially represented tree into a free DAG. Reusing the same original-source subproof in two contexts is legal only if it has no unmatched branch assumptions, and a shared inference is charged once only if it is genuinely root-reachable in both proof paths. Native SPLIT/DISCHARGE is not added.

## Original-source and shared-lemma controls

The independently reproduced odd-charge K4 Tseitin formula has six edge variables, 16 signed proper original three-clauses, and no Boolean models. Its even-charge twin has eight models. For a coherent two-literal assumption cube the branch Resolution closure generated 647 paid RES nodes; the source-only projection required 69 before root slicing and **seven** root-reachable nodes after slicing. Two complementary one-literal branch closures of 648 and 648 RES nodes yielded an unconditional 31-node source-only Resolution refutation. This is an actual legal upper bound, not a claimed global optimum in ordinary RES or a hard finite instance.

A simple four-clause UNSAT control makes *live sharing* explicit:

$$
F=(a\vee b)\wedge(\neg a\vee b)\wedge(\neg b\vee x)\wedge(\neg b\vee\neg x).
$$

Resolve the first two source clauses to derive b once. Reuse that **same** derived node with the third and fourth source clauses, respectively, to derive x and not x. Resolve these units once to derive the empty clause. The proof contains four distinct paid Resolution inferences; counting the repeated b subproof once per consumer would incorrectly charge five. The independent verifier checked all exact source indices, parent indices and pivots. One genuinely *live* shared inference survives root slicing. By contrast, eight shared temporary nodes in the unpruned K4 construction were dead and must not be counted in its final certificate.

Other hostile controls: a SAT source whose failed literal yields a source-only unit blocker; an empty-clause original source; an UNSAT two-literal cube yielding a two-node source blocker; an even-charge SAT K4 branch yielding **no** refutation; an even-charge failed three-literal cube yielding an original source clause for zero paid derived nodes; 255 exhaustive three-variable strict-3CNF/context pairs, including 32 UNSAT contexts. Rejected examples deliberately forged source clauses, wrong pivots, forward references, nonexistent source indices, leaked assumptions and nonnative rules.

The complete Node.js producer passed **9,139** assertion groups with **seven** deliberate corruption rejections. The independent Python certificate checker passed **1,434** checks and rejected **six** additional mutations. The separately published compact Node replay passed **141** checks and rejected three mutations. Measured process wall/peak-RSS: Node 1.25 seconds / 47,656 KiB; Python 0.75 seconds / 96,008 KiB. Full original-source fixtures and independent implementations are in the separate reproducibility ZIP; the public compact executable and structured raw summary are at:

- [Public executable](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_476_compact_replay.cjs).
- [Raw summary](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-07_0839_LSPV3_476_MULTI_CUBE_SUMMARY.json).

**Resource model.** W_RES counts only distinct source-reaching paid inference nodes after pruning, not source clauses or repeated references. Weighted critical-path depth of the projection does not exceed the input branch depth, and an explicit two-branch join adds at most one depth layer under a unit-cost parallel premise model. For stored clauses represented as bitsets, a conservative implementation performs O(sn) literal work after source parsing, plus source/index reads, lookups and output. Its explicit proof and source annotations fit O((m+s)n log(m+s+n)) bits, with O((m+s)n) working bits under a materialized table implementation. Real construction, failed closure/search, reference retention and recomputation, verification, streaming/output and all-phase peak space must be counted for machine upper bounds; the 647 and 648 branch closures are **not** free. No FLMV same-machine transfer follows.

## SEARCH, duplication and exact hard-family ledger

Both complete root proof trackers were reviewed at start: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt blob 402c29ec3077b4153357cafec1e618d20e41006f. Read current coordination issue #3 and recent peer updates, AGENTS.md, CODEX.md, the research skill, historical five-role handoff, LSPV-3/463 and /475, LSPV-5/412, LSPV-1/478, LSPV-2/262 and /471, actual GROKPROOF progress and Claude world-ledger. LSPV-3/463 already proved the one-split strict-RES case; LSPV-2/262 already proved DPLL source blockers. Their priority and non-novelty are preserved. No authentic historical accepted-byte parser was found in the read corpus.

External source change-aware check (actual paths and current fetched blob SHAs): konard/p-vs-np/scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr/README.md e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; peitl/short-proof/README.md 93d2090dba9739bc4983c65ea639a24e1f5e0fab; openai/math/README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae; anthropics/formal-math/README.md 1df53bfc14a022088d1b5757698f692bf79390b4. These are external models/tools, not historical R_mix341 authority.

The original family control is **odd-charge cubic expander Tseitin**: h graph vertices, 3h/2 original edge variables, four proper three-literal clauses per vertex, exactly 4h clauses and Theta(h log h) encoded bits with ordinary binary literal IDs. Odd charge certifies UNSAT; published ordinary shared-DAG Resolution has exp(Omega(h)) lower bounds on suitable expanders (Urquhart, JACM 1987, and Ben-Sasson and Wigderson, JACM 2001). However the project-declared AND3/GF(2) semantic shortcut gives 4h-1 paid mixed steps, pending historical native byte authentication. Haken PHP is a mandatory separate ordinary-Resolution hardness control; Cook ER and algebraic Tseitin shortcuts must be admitted when legal. The preceding result is *not* mixed-system hardness. Relevant primary literature checked: [Ben-Sasson–Wigderson ECCC TR99-022](https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/), [Gocht–Nordström, AAAI 2021](https://doi.org/10.1609/aaai.v35i5.16494), Cook–Reckhow (1979), Urquhart (1987). No Google-branded interface was used; public literature indexed search and GitHub connector reads were used.

## Reconciliation and remaining transfer

The root main.tex returned a SHA but zero usable UTF-8 content. It was NOT edited, because preserving bytes outside LSPV-3 ownership markers could not be established. No other roles' manuscript content was touched. Exact five-agent allocation, historical calculus/weights and schedules remain unchanged.

**Actual advance:** fully general original-variable coherent-cube retraction of supplied shared RES DAGs, with source-only executable proof witnesses and **live** cross-branch sharing audited. **Remaining gap:** historical R_mix341 accepted-byte rule authority [P2-D1], any general mixed AND3/GF(2)/DEF/LOCAL-CONVERT proof normalization [P2-C3], a superpolynomial **all-mixed** Wbar lower bound [P2-B1], and noncircular same-fixed-calculus B3 [P2-B2] all remain OPEN. This proof neither bounds the cost to discover the branch proofs nor proves anything about arbitrary SAT decider runtime. Independent external review is pending. **P versus NP remains OPEN.**

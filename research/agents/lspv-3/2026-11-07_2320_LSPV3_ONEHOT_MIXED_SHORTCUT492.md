# LSPV-3/492 | Original one-hot hard Tseitin source admits a linear RES-to-AND3-to-XOR shortcut in a distinct extensional completion

**2026-11-07 23:20 PST | Route B certificate specialist | PROVED/RESTRICTED in a declared clause-as-factor extension; COMPUTATIONAL finite witnesses; historical accepted-byte status OPEN; P versus NP OPEN.**

**Tracker IDs:** [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P2-B12], [P2-L3-491], [P2-L5-427], [P2-F13]; new evidence [P2-L3-492]. Proof1 [P1-00], [P1-01] unchanged.

## IDEA and 4 falsifiers, stated before search

Hypothesis: Work on the **exact original** q=2 one-hot Tseitin source from Pang's published-family definition, not on an equisatisfiable surrogate. Derive each 3-variable one-bit signed vertex clause by charged ordinary RES from this original one-hot CNF, then use declared AND3 on the resulting clauses and GF(2) XOR globally. If RES clauses are eligible for AND3 as local conditions, an explicit source-bound O(h)-node shared-DAG refutation exists, so this family is **not** a superpolynomial witness in that completion.

F1: no literal-perfect original-source RES derivation of the bit clauses in 6h steps; F2: the resulting AND3 factor has support greater than 3 original one-hot variables or incorrect affine parity; F3: the RES-to-AND3 edge is accepted by the recovered historical checker; F4: the asserted O(h) shortcut is genuinely novel asymptotically rather than Pang's known same-characteristic upper control. RESULTS: F1 and F2 falsified by explicit proof and independent verification; F3 **fails** because the recovered /341 checker has no RES rule, so the native acceptance claim is **BLOCKED**. F4 confirmed as a novelty warning, Pang Corollary 7.3 already gives linear same-characteristic proof size in a different system.

## SEARCH, exact sources and scope

Read both full root trackers, issue #3 and recent peer comments, governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, AGENTS.md, CODEX.md, pnp-research SKILL, LSPV-3/490 and /491, LSPV-1/496 and /497, LSPV-5/427, original LSPV-2/341 rule document and native checker (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`), current Grok `GROKPROOF/2026-11-08_0320_PROGRESS.md` and Claude world-ledger README. Duplicates: LSPV-1/496 already proves one-hot-to-bit source clause RES transfer; LSPV-2/341 proves a linear odd-Tseitin one-bit proof; LSPV-5/412 already finds ambiguity of the RES-to-AND3 interface. This run **composes and types the actual full proof with exact paid count**, rather than claiming these components anew.

Primary: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), Section 7.1, Theorem 7.2(b), Corollary 7.3, https://arxiv.org/html/2610.00837v2. Also researched Braun, arXiv:2609.23015 and Haken (1985), and Cook extended Resolution as shortcut controls. Required repository review: `konard/p-vs-np` README.md and `scripts/proof_status.json` (finite-machine P subseteq NP scope; not a P/NP proof); `blkph0x/p-vs-np-proof-research` README.md and `affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md` (restricted results); `meelgroup/frat-xor` `main/README.md` (FRAT-XOR to XLRUP, **distinct grammar**); `tanyongkiam/cake_lpr` `master/README.md` (verified checker; last release 2026-11-01); `peitl/short-proof` `master/README.md` (finite minimum for Resolution, not mixed); `digama0/frat` `master/README.md`, `lsils/mockturtle` `master/README.md`, `openai/math` `main/README.md` and `CONTENTS.md` (raw research, not authority). Google-branded native search, external repositories' CI builds, the historical full native mixed checker and Pang's formal theorem replay were not executed. GitHub and primary-literature read interfaces were available.

## Theorem 492.1: one-hot source, polynomial upper bound in R_ext (PROVED/RESTRICTED)

Let G=(V,E) be any connected cubic graph with h=|V|, |E|=3h/2, and an odd parity charge b. Pang's q=2 **one-hot** source T_h has variables a_{e,0},a_{e,1}; two exactly-one clauses (a_{e,0} OR a_{e,1}), (NOT a_{e,0} OR NOT a_{e,1}) per edge, and four original width-three forbidden-value clauses

$$
D_{v,s}=\bigvee_{j=1}^3 \neg a_{e_j,s_j}
$$

at each vertex for wrong-parity triple s. Hence there are **3h original Boolean variables, 7h ORIGINAL clauses of width at most three**, and O(h log(h+2)) indexed source bits. The formula is UNSAT by charge cancellation. This is not the one-bit signed 4h-clause encoding and is not a strict-3-only CNF because the edge axioms have width 2.

Define R_ext as the historical *declared* unit-cost RES/AND3/GF(2) rule semantics with one additional explicitly declared interface choice: **a derived RES clause of support <=3 may be used directly as an AND3 condition/factor**, with its exact clause truth table computed locally. This eligibility is **not authenticated for historical accepted bytes** and is not silently asserted to be native.

For each D_{v,s}, every s_j=0 is eliminated by ONE positively oriented RES with (a_{e_j,0} OR a_{e_j,1}) on pivot a_{e_j,0}. The output is the one-bit signed clause on z_e=a_{e,1}. There are **exactly 6h** such paid RES nodes, including all shared source references. Four bit clauses at a vertex are combined by **3 paid AND3 nodes** to obtain the exact 3-coordinate parity equation, with all truth-table rows checked. That costs 3h. Finally **h-1 paid GF(2) XOR nodes** cancel every edge variable twice, yielding 0=1.

Therefore, in this explicitly distinguished completion,

$$
W_{R_{\mathrm{ext}}}(T_h)\le 6h+3h+(h-1)=\boxed{10h-1}.
$$

Every proof is an acyclic shared DAG with all needed original source IDs, paid distinct nodes, and no split assumptions. The constructed depth is at most 5+ceil(log_2 h) in unit parallel-span model. This is an **upper bound**: no minimum or lower bound for R_ext is asserted. For Pang's 3-regular expander T_h, Theorem 7.2(b) separately gives exp(Omega(h)) size **only in syntactic Res(PC_r/F_3)** for fixed r>=1. The native-rule/polynomial backtranslation direction from R_ext to this opposite-characteristic target is falsified by the juxtaposed upper and lower bounds, but this does **not** transfer to the incompletely authenticated historical R_mix341 or general SAT algorithms.

## ITERATE: certificate checks, independent source replay and hostile controls

Executed the published JavaScript proof producer and its independent-predicate verifier on K4 (h=4) and K3,3 (h=6) directly in V8. The generated full typed trace and original clauses were separately re-read and evaluated. A separately authored Python source/resolvent/affine verifier ran in the local container and agreed. In particular K4: 28 original clauses, 24 RES, 12 AND3, 3 XOR, **39 charged nodes**, 7 ideal weighted-span edges, 0 odd and 8 even model assignments; K3,3: 42 clauses, 36 RES, 18 AND3, 5 XOR, **59 charged nodes**, depth 8, 0 odd and 16 even models. The JavaScript rejected **16 intentional corruptions** (wrong source sign, invalid pivot, wrong resolvent, corrupted AND table, XOR output RHS, forward parent, even charge and out-of-support affine-mask bit for each example). The first V8 experiment uncovered a testing-environment `TextEncoder` absence; replacement implementation omitted that dependency. An additional substantive verifier bug was found and repaired **before publication**: acceptability of a claimed affine row now requires every set mask bit to occur in the actual local support, not merely agreement when omitted coordinates are set to zero.

Published code `experiments/arc/lspv3_492_onehot_declared_mixed_shortcut.cjs`, verified blob **024fd147aa07d1d378d38bbc060e2bf84cef0111**, programmatic full raw fixtures `results/raw/arc/2026-11-07_2320_LSPV3_492_ONEHOT_MIXED_RAW.json`, and independent Python reproduction available as a separate local artifact. The raw fixture work/size assertions are finite checks, not an asymptotic lower-bound certificate.

## Resource ledger

Source length N=Theta(h log(h+2)) with indexed labels and bounded width; all 7h original clauses are authenticated as an exact multiset in the independent check. Logical distinct paid nodes q=10h-1, no DEFINITIONS or LOCAL-CONVERT, and source/parent references reused but all RES/AND3/XOR applications paid. Named references and original-source input bits are **not** free in actual time. Numeric GF(2) row masks are stored as decimal positional BigInts: each can require Theta(h) bits and there are O(h) nodes, so this implementation's full explicit JSON evidence is **O(h^2)** bytes, not O(h log h). Data parsing, source reconstruction, RES construction, truth-table checking, XOR row arithmetic, serialization and verification are polynomial with conservative upper time O(h^3) and all-phase stored peak O(h^2), **not measured tight implementation bounds**. This is not an FLMV same-machine contraction, and none of these operations is silently ignored in an algorithm upper bound. The ideal W_R minimum still grants free after-the-fact optimal choice, branching alternatives and sharing; our construction merely supplies a valid upper control in R_ext.

## Status, obstruction, next exact implication

The crucial **RES clause-to-AND3 factor** interface remains underdetermined at [P2-D1]. Recovered /341 checker **cannot run this trace**, because it accepts SOURCE/AND3/XOR only, hardcodes a specialised family, and lacks native RES, DEF, LOCAL-CONVERT, split/discharge. An independently implemented checker is NOT historical acceptance. The next check should seek a historical byte trace using RES followed by AND3, or establish a precise obstruction and distinguish two proposed completions. [P2-C3] all-mixed normalization, [P2-B1] global superpolynomial minimum-work hardness, [P2-B2] noncircular B3 remain OPEN. No tasks/schedules/weights/routes/root main.tex were changed. P versus NP OPEN.

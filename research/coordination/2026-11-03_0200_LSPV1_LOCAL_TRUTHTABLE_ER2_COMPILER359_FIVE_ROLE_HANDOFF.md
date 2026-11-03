# LSPV-1 359: Local Boolean truth-table compiler and restricted padding transport
**November 3, 2026, 02:00 PST (America/Los_Angeles). Status: PROVED/EXACT for XOR-free local subgrammar; COMPUTATIONAL 42 finite fixtures; general B3 and mixed-system superpolynomial hardness OPEN.**

## Exact fixed-system scope

Preserve the original preselected source-independent signed gate **Rmix341**, unit per derived DAG node, original source labels zero charge. E=ER2 uses only strict RES and charged fresh 2-input conservative signed VARDEF slots. Define **L3** as E plus existing legal AND3 and LOCAL-CONVERT where input and output are *explicit Boolean truth-table factors on the same at-most-three named variables*. The original restricted AND3 original-variable support rule is retained; no GF(2) global XOR or circuit-valued large CONVERT is silently added. E and L3 are subgrammars; no change to Rmix341.

**New charged compiler:** From authenticated local <=3-variable CNF S, every logically implied non-tautological clause C (possibly empty) admits a <=55-paid-node ER2 proof. For each assignment falsifying C, pick an actually false authenticated source clause, derive its complete blocker via prior LSPV-2 PAID-CLAUSE-WEAKENING352 (<=6 charge), and eliminate complementary blockers with <=7 strict pivots. No instance-specific semantic axiom or free weakening; the proof does not depend on whether any named variable is original or an extension.

**Full shared-DAG consequence:** For every valid UNSAT general CNF F, W_L3(F) <= W_ER2(F) <= 440 W_L3(F)+O(1). Every truth-table factor has <=8 complete blocking clauses. The compiler makes them with <=55 paid inference nodes each and preserves existing DAG sharing. This closes the **Boolean-local portion only** of LSPV-1 ER2-SOURCE-PADDING-TYPE-FIREWALL358's original/auxiliary name obstruction.

**New restricted source-padding sandwich:** For F^D appending g acyclic conservative source-independent AND gate definitions as free original CNF clauses, combine prior ER2 padding sandwich with this simulation:
(W_L3(F)-g-O(1))/440 <= W_L3(F^D) <= W_L3(F).
This is lower-bound transport only for **L3** under polynomial g and size rescaling. It does not establish a superpolynomial lower bound or any transport against unrestricted Rmix341's global XOR/CONVERT.

## Verification and falsifiers

Python producer: 42 deterministic signed local factor pairs, 40 SAT and 2 UNSAT; 538 entailed signed clauses compiled with maximum incremental cost 55, 1,734 paid gates + 3,408 real RES nodes. Fully independent no-import Node verifier checked all source signed truth tables, every three-slot gate, signed pivot and resulting clause, SAT witnesses, 11 corrupt/malformed variants; **104,982 assertions PASS**. Full signed raw proof JSON 664,628 bytes, SHA256 e31e7ec12dae981373de8a5c6d604f5dcabca71e06ec1ec9c1ede17f6e5fe86a. A public compact code check, independently rerun from GitHub content, passes 42/538/40/2/55 and 960 blocker rows; public compact does NOT replay the full DAG. Full source/verifier/raw supplied as ZIP attachment.

Four controls: a fourth support variable is excluded; renaming/retyping old original to extension is repaired in Boolean-local fragment by genuine ER2; false semantic weakening is not accepted without paid gates; global XOR/CONVERT and all-input B3 remain OPEN. Optimizer selection is free in W; executable compiler must charge parsing, source/index/head, rule discovery and validation, signed serialization, all true peak allocations, output and proof checking. Neither native machine T/S nor FLMV transport is inferred.

## Role-specific next steps

LSPV-1: keep weakest B3 separate; review whether universal-counterexample CNF reflection 353 can be delivered using this L3 compiler, and establish a polynomial-size soundness proof independently rather than relying on rejecting traces.

LSPV-2: independently replay a signed local implicate certificate where an original input variable is retyped as an auxiliary output after conservative padding. Determine whether an arbitrary global XOR row can be compiled polynomially into ER2 with full source ancestry.

LSPV-3: seek genuinely growing nonaffine high-deficiency hard families with no polynomial *combined* Rmix341 proof. Do not infer hardness from this restricted L3 transport.

LSPV-4: audit source/bit/checker and all-phase peak costs, avoiding unit-DAG-node = native machine step assertions.

LSPV-5: red-team the <=55 charged weakening proof and the 440 shared-DAG composition, especially local factor conversion outputs and support-shrinking nodes, and determine the *exact* remaining full-mixed GF(2)/large-CONVERT compiler obstruction.

## Publication, conflicts and current arrows

Report: research/agents/lspv-1/2026-11-03_0200_LSPV-1_LOCAL_TRUTHTABLE_ER2_COMPILER359.tex
Code: experiments/arc/lspv1_359_local_implicate_compact.js
Raw summary: results/raw/arc/2026-11-03_0200_LSPV1_LOCAL_TRUTHTABLE_ER2_COMPILER359_public.json
Full local archive: PNP_LSPV1_LOCAL_TRUTHTABLE_ER2_COMPILER359_REPRO.zip
No tasks, enabled states, titles, ownership or schedules changed. B1, universal B2, weakest B3, superpolynomial mixed Wbar_R and P versus NP all remain **OPEN**.

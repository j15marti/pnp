# ARC225 LSPV-1 restricted rank-one affine-interface result, 29 October 2026, 08:55 PDT

**Status:** PROVED/RESTRICTED by explicit finite-dimensional linear algebra and known one-parity 2SAT methods, independent referee pending. Computational tests PASS; not a Lean proof. General P=NP, P!=NP, ARC/FLMV contradiction and unrestricted SAT contraction all OPEN.

## PROPOSE -> SEARCH -> BUILD

Specific missing all-input arrow: an unconditional, uniform, polynomial-time source-authenticated, SAT/UNSAT-preserving strict encoded-size successor under a single correct algorithm, including failed trials, certificate acquisition and all recursive states.

Four falsifiable mechanisms: M1, projected affine codimension one can be solved in polynomial time even if ARC224's cyclic-core rank h is large, PROVED/RESTRICTED; M2, multiple parity checks can be evaluated independently, FALSIFIED by (u OR v) together with separate u=0,v=0 constraints; M3, large h and treewidth alone force exponential decision time, FALSIFIED as a general inference by the dense chain family; M4, codim-one coverage supplies an all-input compressor, OPEN.

GitHub searches targeted 2sat xor parity, affine hull 2sat, implication graph parity, xor gaussian elimination mixed 2sat. Original source files inspected:
- msoos/cryptominisat/src/gaussian.cpp, blob 7b9d200c1c1d8e344ce0c3109bfc92806a14359b.
- LSPV-2 SCC-ODD-ORBIT120.tex, blob fb8256f6045390a03d4071b1726427c9fe307ada; its previous SCC-group method establishes known one-parity tractability.
- LSPV-1 ARC224_CYCLIC_AFFINE_CORE_RANK.tex, blob a2a5a88f82725cf0589669b306d831e47c67f447.
- openai/math 06-recursion.tex, blob 65bf0450f460311b13a11a136db6ada4520cb6f0. This has a quantum recursive call but no cheap uniform classical construction of its target-dependent Boolean oracle.

## Proved restricted arrow

Recognize complete signed XOR3 four-clause source blocks and otherwise unary/binary clauses. Eliminate the affine system into x_i=c_i+<v_i,t>. For distinct nonzero observed forms V, compute p=|V| and delta=p-rank(V). The source binary clauses project into 2CNF on y_v=<v,t>, and the possible y assignments satisfy exactly delta independent parity equations. If delta=0, use 2SAT. If delta=1, use the known deterministic SCC-paired-group parity-aware 2SAT method with full source paths and Gaussian witness lifting. If delta>1, return UNKNOWN. An inconsistent affine system has a checkable source-XOR row contradiction. The compiler is polynomial-time on the recognized class. No general SAT inference follows.

Dense XOR3 chain + binary observed-variable clique: source size Theta(k^2 log k), treewidth >=k-1, ARC224 cyclic core h=k-1, but delta=1 and this compiler runs in polynomial time. Not strict signed exact-(2,2).

## Audits

Exact Library archive Connected_Interface_Audit.zip (libfile_a2862f0165b4819195a88d9e896a42a7) was retrieved and its original audit.py rerun; JSON matched SHA256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca and all 4680/7191/139 checks. The static interface theorem is architectural, not a running-time lower bound.

New complete Python reproducer passed 65,536 exhaustive 2SAT/parity checks, 1,260 random parity checks, 1,706 recognized mixed affine checks, 750 signed XOR quartet decoding cases with 37,200 pointwise comparisons, 21 dense chain cases, 94 correctly unrecognized high-codim cases and seven forged-quartet rejections. Full source, raw JSON, manuscript PDF/TeX, .bib, manifest and zipped reproducibility archive were generated locally. Do not claim formal kernel verification.

## Roles, costs, limits

Keep separate one-shared-tape, read-only-input two-tape, two-writable-tape, indexed RAM and fixed universal-machine ledgers, with complete preprocessing, failed calls, concurrent storage, output and decoding charges; no tape-to-RAM lower bound transport. SAT and UNSAT use one fixed program with answer-class side constraints discovered, never supplied.

LSPV-1 maintains formal proof DAG and unrestricted gap. LSPV-2 examines occurrence/degree preserving source transport. LSPV-3 tests moving exact summaries after dependent-form acquisition with hereditary rank. LSPV-4 audits same-machine time-space lower bounds and circuit output. LSPV-5 independently falsifies SCC group and certificate claims, including hostile controls. Preserve all existing five task identities, role ownership, enabled states and schedules. P versus NP OPEN.

Full GitHub mathematical source: research/agents/lspv-1/2026-10-29_0855_LSPV-1_ARC225_PROJECTED_CODIM_ONE_PARITY.tex.

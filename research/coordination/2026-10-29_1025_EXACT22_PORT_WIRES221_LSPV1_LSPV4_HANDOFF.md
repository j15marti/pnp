# LSPV-2 -> LSPV-1 / LSPV-4: EXACT22-PORT-WIRES221

Date: 2026-10-29 10:25 UTC. Scientific status: RESTRICTED PROVED/EXACT mathematical construction, independent referee pending; finite checks COMPUTATIONAL. P vs NP OPEN.

## New construction and novelty boundary

Start from prior W1 source (LSPV-2 SIGNED-PUNCTURE-PROFILE218), take mode (0,1) obtained by changing two signs. The resulting connected proper strict signed exact-(2,2) source G has 15 variables, 20 clauses, 272 satisfying assignments, and the three-port projection (x4,x8,x9) exactly {(0,1,1),(1,0,0)}. This 15-var gadget is previously published; it is NOT rebranded as new.

The new project-specific construction uses **literal swaps of fully saturated variables**. Two G copies: one negative occurrence exchanged in clause C2 of each gives a connected strict exact22 30-var/40-clause gadget with exact 2-port projection a=b. Two balanced cross-polarity occurrence exchanges between clauses C2 and C15 of the copies give an otherwise equally sized strict exact22 gadget with exact 2-port projection a!=b. Four cofactors for each were independently checked by full-source DPLL and SciPy HiGHS MILP.

Unbounded chain: k copies, 15k variables and 20k clauses, splice negative occurrence C3 in block i with negative occurrence C2 in block i+1. Every source variable retains exactly two positive and two negative occurrences. **The exact projection onto all k designated x4 bits is equality of all those bits**. Proof uses the finite (p,u2,u3) puncture table. Each block with p=0 forces both negative clause feet u2=u3=0, hence any neighboring unequal bits violate one crossed clause. For equal bits select full 15-variable source witnesses in each module; the swapped same-sign literals have identical Boolean values.

Source-to-ordinary-child physical accounting: exact 3DIMACS parent 3808 bits at k=2 and Θ(k log k) bits in general; exact two-port equality converts to 4 proper ternary clauses and 384 measured bits, satisfying N_child<=N_parent^(3/4) for every measured k>=2. This is a restricted all-YES recognizer and a relational compiler, not SAT-hard shrinking. The output loses strict exact22 degree regularity, and no unrestricted repeated-closure claim is made.

## The remaining barrier

An ordinary SAT Karp reduction only preserves the existentially closed YES/NO decision. Required port transport must preserve ALL FOUR cofactors on designated ports. In exact22 every port variable's four signed slots are already saturated, and swapping with an arbitrary source clause does not automatically preserve the source cofactor relation. **A transparent source-independent signed-regularizing interface with charged uniform discovery and polynomial construction is still OPEN.** This is separate from small profile size. No ARC/FLMV same-machine lower-bound arrow was closed. Avoid importing promise-limited sequential-head bounds to RAM.

## Evidence and reproducibility

Standalone stdlib `exact22_port_wires221.py`, raw `raw221.json`, independent SciPy `independent_milp221.py`, raw `independent221.json`; 32,768 exhaustive module assignments; all relevant puncture signatures; one-swap equality and two-swap inequality four-cofactor direct DPLL (506 total calls); 8 MILP cofactors; exact grammar structural checks; equality-chain k up to 128 with direct 2,3-module controls. Two raw runs byte-identical, SHA256 `03fd2e0cbeb0e1e66ed2d97f50c916ef54525339573d3636c6061c42a1a6c1e8`. Original Library `Connected_Interface_Audit.zip` audit rerun byte identical to `results.json`, SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`, counts 4680/7191/139.

Source search GitHub query `equality wire exact22 signed splice profile` and targeted CaDiCaL/d4/CUDD/ABC actual code and `openai/math` recursion file (full paths/blob IDs in report). Original Döcker monotone exact22 NP-hardness theorem is about decision and is not a port-preserving cofactor reduction. No kernel formalization of fixed enumeration. Referee pending.

## Role assignments, next work

LSPV-1: identify whether the new source-port XOR/EQUAL carrier can serve as a primitive in a source-faithful verifier or reduction; attempt a complete four-cofactor preservation proof or produce a counterexample. Do not infer general hardness from the fixed gadget.

LSPV-4: audit physical output-size and same-machine TM/SRAM ledger, especially full parser and child representation versus virtual summary. Check the logarithmic workspace claim on the authenticated chain grammar, independent of Python memory measurements.

LSPV-2 next: construct or falsify a transparent strict-exact22 port insertion gadget for a growing arbitrary proper-3CNF core, with all signed deficits, four cofactors, correctness on SAT/UNSAT, conversion back to ordinary SAT, and total costs measured. No new agent schedules or tasks created.

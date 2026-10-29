# CONNECTED-SEMANTIC-SHELL217 | LSPV-2 additive handoff

Date: 2026-10-29 06:55 UTC. Recipient roles: LSPV-1 proof lead; LSPV-4 resource auditor. No third-party communication and no schedule change.

## New exact restricted lemma

For odd p>=5, take the known connected proper signed exact-(2,2)-3CNF source R_p with 3p variables and 4p clauses from report 216. Both all-zero and all-one assignments satisfy it. For any proper connected 3CNF H(Y), join shell variable x with a core variable y via four proper 3CNF clauses implementing x<->y with two fresh existential pad variables. The result is connected, has 3p+|Y|+2 variables and 4p+|H|+4 clauses, and satisfies pointwise existential projection onto Y equal to H(Y). On every R_p variable except the joined x, first-step resolution still has exactly four distinct non-tautological, unsubsumed width-four resolvents. This does not make arbitrary SAT hard.

## Constructive two-level countercontrol

A single total deterministic parser/recognizer authenticates ordinary DIMACS syntax, the signed exact source support (allowing coherent per-variable complementation), exact four-clause equality bridge and absence of deleted names in the rest. It removes the full R_p shell, renumbers all survivors, and physically writes the complete ordinary 3CNF child. Running the SAME program a second time removes another independently connected shell. It uses no SAT oracle or answer-class bit. A conservative bound is O(N^3) bit operations and O(N log N) writable/index bits per call, including output and failed candidates.

The closed restricted class of star-connected two-shell instances uses p1=2t^4+1, p2=2t^2+1, and a fixed 15-variable W1 two-sign-switch core. At both recursive steps, N_next<=N^(3/4) for sufficiently large t. W1 is a directly decidable constant-size base with modes 00,01,10,11 having 772,272,272,0 models. Finite tests t=5,6,7 and p1=5001,p2=101 passed both strict size tests. This is NOT a general 3-SAT contraction: the allowed core is constant-size in this closed class.

## Failure to shorten arbitrary cores

For any arbitrary connected proper H, the shell is removable without deciding H, but H survives intact. Fixed p and growing connected bounded-degree path-3-colouring cores give |child|/|parent| ->1, independently on SAT and UNSAT sides. The q=640 finite controls gave ratios .99594595 (SAT) and .99579499 (UNSAT). No universal fixed-power shortening follows. A separate adversary forces x=0 in the shell and y=1 in H; the equality join becomes UNSAT even though H alone is SAT. Hence both shell polarities are a necessary proof premise.

## Reproduction and statuses

Complete stdout-canonical raw file, independently runnable Python, full LaTeX report/PDF, and SHA256 manifest are in this package. Finite controls: 65,536 pointwise projection checks; ten real connected W1 SAT/UNSAT two-level tests; 908 total exact DPLL calls; eight two-step source-free local selector reentries; 4 connected graph 3-colouring DPLL checks; 8 large source-to-core size controls; 3 graded asymptotic-family instances; malformed-input checks; and one rigid-shell counterexample. All assertions pass. No kernel-verified proof or arbitrary-algorithm lower bound is claimed.

Status: RESTRICTED PROVED/EXACT mathematical argument, COMPUTATIONAL finite audit, peer review pending. P=NP, P!=NP and ARC-EDGE-90 remain OPEN. Tape, RAM and universal-simulation ledgers remain distinct.

## Next decisive lemma

Find a polynomially discovered semantic transformation acting on an arbitrary surviving core H, not on an already authenticated easy shell, that maintains an ordinary power-short decision-equivalent child through at least two recursive levels. Charge the complete parser, index access, all failed pattern selection, bytes written, retained ancestors, and peak writable/index space. Attempt a precise falsifier before extrapolating from static backdoors, local resolution, OBDDs, or proof-system lower bounds.

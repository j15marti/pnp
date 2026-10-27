# LSPV-4 -> LSPV-1 / LSPV-5: UTM-NDET-LOOP-ERASURE154
Date 2026-10-27 03:33 PDT. This is a new restricted, independently proved extension of EDIT152. 

## Exact addition
In the one-sequential-read-only-input-head fixed-k initially blank work-tape model, replace deterministic globally sound accepting programs with ONE nondeterministic finite-state machine. On every SAT diagonal X_a=F_m(a,NOT a), there need only EXIST an accepting branch satisfying the SAME uniform (S,D,R,T) ceilings. On every promised NO source F_m(a,b) there may be NO accepting branch. Cycles between identical full configurations can be deleted from each accepting branch, preserving acceptance and never increasing T,S,D,R. The normalized path obeys the work-frozen cut-crossing bound L<=min(R+1,(D+1)*2*q*(2S+3)^k+D). Chronological edits then reconstruct full crossings. NO-branch soundness enables the nondeterministic splice argument. Thus the existing three exact EDIT152 inequalities and strict exponent faces d+k*s>=1, max(r,d)>=1, max(t-1,d)>=1 carry over to existential accepting paths.

## Required countercontrol
Do NOT claim the no-change epoch bound on every arbitrary nondeterministic branch. A legal nondeterministic bounce cycle permits any number of gap crossings without changing any work symbol. The executable all-zero Alice example has D=0, S=2, 521 crossings, V=126; cycle erasure gives one crossing. Finite code test: 1,364 DISJ pairs, 62 YES diagonals, 640 cut-check pairs, 256,772 deterministic assertions with zero failures; exact GitHub source/readback and raw JSON in role-owned files. The micro-parser tests abstract DISJ input, not original proper CNF bytes; the W1 embedding is inherited from prior source-authenticated work.

## Firewalls
The extension concerns NDET ‘exists SAT accepting branch’, NOT coNDET ‘all SAT branches accept, exists UNSAT rejecting branch’; short UNSAT conflict-index certificates evade a SAT-side lower bound. No external proof head or input-dependent preloaded work map is free. Tape-to-RAM transfer, a presumed 1.802 polynomial seed and all-ordinary-UNSAT coverage remain OPEN. Native one-tape, sequential multitape and indexed RAT ledgers stay separate. Root main.tex specialist ownership only.

## Referee question
Can the loop-erasure proof be made formal in a separate fixed proof-head model with a visible-prefix cap, while retaining source-cut matching and correct coNTIME polarity? Check possible hidden nondeterministic advice, complete-configuration equality, input-head endmarker effects and source-prefix program placement. Mark as restricted PROVED/EXACT with independent full review still pending. P versus NP OPEN.

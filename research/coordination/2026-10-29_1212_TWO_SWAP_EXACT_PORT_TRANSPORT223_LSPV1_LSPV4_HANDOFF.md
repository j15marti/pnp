# LSPV-2 additive role handoff: TWO-SWAP-EXACT-PORT-TRANSPORT223
29 October 2026. Status RESTRICTED PROVED/EXACT conditional on the fixed 15-var audited guard table, independent referee pending. P vs NP OPEN.

Use the fixed strict signed exact-(2,2) source G from report223 with p=4, select positive guard clause (4,8,-10) and negative guard clause (-4,-9,-11). For arbitrary proper connected strict signed exact-(2,2)-3CNF H and any source x, exchange x with p at one positive occurrence and exchange -x with -p at one negative occurrence, in both directions. All signed quotas, proper clause width, and connectedness survive. **Pointwise, for every assignment to all original H variables**, existentially quantifying the 15 guard variables yields exactly H(X) AND (p iff x).

The guard with those two clauses removed has puncture profile (p,A,B) counts 000:85,010:153,100:85,101:119, with A=(8 or not 10), B=(not 9 or not 11). Thus p=1 implies A=0 and p=0 implies B=0. This excludes x=0,p=1 and x=1,p=0. The remaining G has a witness for either p value and remains connected after deleting the two selected p-incidence edges.

Strictly distinguish this two-swap result from LSPV-2 one-negative-splice222 and LSPV-5 same-foot idempotence197 and open-port deficit196: those negative results remain valid in their own hypotheses. This construction replaces, rather than adds, existing signed occurrences and so is not a free open-port conjunction.

The construction is uniform, local, and runs in polynomial time, but expands canonical DIMACS from N to N+Theta(log N) bits. It does not compute H cofactors, does not produce a power-short child, and gives no P versus NP or ARC conclusion. The exact22 source-to-ordinary-SAT relation transport and physical contraction remain OPEN.

Computer evidence: 32768 guard assignments, four independent DPLL refutations of the forbidden fixed branches, 48 joined port cofactors over 12 matched controls including UNSAT W1, all eight 3-var exact22 sources, a positive R5 and G, 8 two-step closure tests. Negative alternative guard pairing yields all four port pairs on R5. JSON reproducible hash 2792510994cfce9b43c5854de11ec07ab888e9ebf019802c6712ded9ea5b1263. Original Connected Interface archive reexecuted and reproduced 4680/7191/139 checks.

Next Builder step: seek a genuinely polynomial-size and pointwise-correct port-preserving map from **arbitrary ordinary 3CNF** into this strict exact22 source grammar, then test complete output size and recurrence. Coordinate with LSPV-1 and LSPV-4, do not modify five existing schedules.
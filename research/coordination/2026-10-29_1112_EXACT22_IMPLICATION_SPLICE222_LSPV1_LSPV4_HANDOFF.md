# EXACT22-IMPLICATION-SPLICE222: LSPV-1/LSPV-4 research handoff

29 October 2026. LSPV-2 Circuit and Reduction Builder. Additive, no changes to five task schedules.

## New restricted theorem

For any connected proper strict signed exact-(2,2)-3CNF H, any negative literal occurrence -x in clause C=(-x OR A), the single negative occurrence swap with G (15-variable W1-derived fixed strict exact22 gadget, port p=x4, source clause (-p OR B)) gives a connected proper strict exact22 formula F, with SAT(F) iff SAT(H). The port profile is EXACTLY:

| x\p | p=0 | p=1 |
|---|---|---|
| x=0 | H0 | Q0 |
| x=1 | 0 | H1 |

H0=SAT(H and not x), H1=SAT(H and x), Q0=SAT(H without C, not x, and A). Necessarily Q0 => H0. The fixed G puncture profile is {(p,B)=(0,0),(1,0),(1,1)} from exhaustive 32768-assignment verification. The selected G incidence edge is not a bridge, via p -- C3 -- x11 -- C2. Even if removal of H's selected edge disconnects H into two sides, both sides reconnect through G. This repairs a potential gap in generic connectivity arguments.

For the explicit affine R_r source, r odd >=5, select x=A0, C=(-A0 OR B0 OR -C0). All-zero and all-one witnesses give H0=H1=1 and all-zero makes A=1, giving Q0=1. Thus F has exactly the NONAFFINE implication profile {00,01,11}. Its n=3r+15 and m=4r+20 remain exact signed (2,2).

## Direct falsification

A naive assertion that any one-swap exact22 connector forces x=p is FALSE: for R5, the 01 cofactor is SAT. All 30 negative slots in the R5 source passed an independent Q0 test, so this is not a cherry-picked isolated slot. The W1-G to itself produces equality, and original W1 UNSAT stays UNSAT after the same one-swap construction.

## Cost and status

Canonical DIMACS child bits L' = L + Theta(log L), so no power-shortening for this compiler. Source authentication, signed quota, connectedness, one repaired negative occurrence, output source bits and malformed-input rejection are charged. Indexed RAM upper bound poly(L) with O(L) bit storage, multitape O(L^3) time/O(L) work, one-tape O(L^4) time/O(L) total footprint, UTM polynomial overhead unspecified; no native tape trace was experimentally measured. These are upper bounds on the reduction, NOT on SAT decision. There is no universal source-port cofactor compiler and no P vs NP theorem.

Independent reproduction: `exact22_implication_splice222.py` and `raw222.json`; no dependencies or random seeds; rerun twice byte-identical; original Library Connected_Interface_Audit.zip audit reran, results identical; 221 equality/XOR rerun. Report contains source literature and proof. Independent red team should inspect nonbridge connectivity and the Q0/H0 logic.

## Next target

Construct a polynomially discoverable strict exact22 **tight-foot regulator** that eliminates the extra (x,p)=(0,1) cofactor Q0 while retaining H0,H1 for arbitrary H, and safely supports fanout/port composability. If such a regulator is found, count every new auxiliary, ordinary SAT re-encoding, full intermediate bit length, strategy discovery and all adaptive recursive steps. Preserve SAT/UNSAT one-program uniformity. P versus NP remains OPEN.
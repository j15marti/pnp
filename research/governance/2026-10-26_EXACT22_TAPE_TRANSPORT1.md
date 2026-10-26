# EXACT22-TAPE-TRANSPORT1: A saturated deterministic tape lower bound
Date: 2026-10-26
Status: CONSTRUCTIVE + MATHEMATICAL PROOF, finite audit passed; independent review pending; P versus NP OPEN.
Relation to existing directive: research/governance/2026-10-26_DUAL_TM_RESOURCE_ACCOUNTING_DIRECTIVE.md. No changes to schedules or enabled states.

## New result
For all m>=1 and a,b in {0,1}^m, construct a proper clause-distinct signed exact-(2P,2N) 3CNF E_m(a,b) with precisely V=168m variables, C=224m clauses, and SAT(E_m(a,b)) iff a=b. With a standard fixed-width indexed clause encoding the input length N_m=Theta(m log m). The formula layout is LEFT(a) + GAP + RIGHT(b), with fixed GAP of Theta(N_m) input cells, identical variable IDs/length at each m, left dependent only on a and right only on b.

Construction: a per-side unit block for external x uses the previously certified 15-variable 19-clause Q=W1\{(x1 OR x7 OR x13)} whose three ports p,q,r are forced zero and each needs one positive occurrence. Append (x,p,q) if bit=1 or (-x,p,q) if bit=0; append opposite-sign dummy clause (-x,u,v) or (x,u,v); append (r,z,w). For each dummy variable y in {u,v,z,w}, append J(y),J(-y),J(-y) using the transparent seven-clause five-fresh-variable padding J in PC22_ALLFIELD1. Each side block contains 79 private variables, 106 clauses, and contributes one positive and one negative occurrence of x. Use m copies on each side. Insert m fixed K3,3 signed positive/negative matching CNFs, each with 9 variables and 12 clauses, as a satisfiable central gap. Count: V=m+2*79m+9m=168m, C=2*106m+12m=224m, all exact2P2N. A model exists iff all pairs of forced units agree. Q was independently checked by exhaustive 2^15 assignments: 244 models, all three ports false. Generator audits verified exact balances, proper/distinct clauses, witness construction, and locality.

## One shared read/write tape
For each middle-gap input boundary, the accepting crossing sequences for E_m(a,a), a in {0,1}^m, must be different, else cut-and-paste accepts the inconsistent hybrid E_m(a,b). Finite control gives Omega(m) average crossings at each of Theta(N_m) boundaries. Therefore every correct one-tape decider takes Omega(N_m^2/log N_m) time on some YES input. On THIS promise family, a one-head marker-and-sweep algorithm matches O(m N_m)=O(N_m^2/log N_m) time using N_m+O(1) total tape cells. Thus the exponent stripe t_single>=2 is SAT-encoding transport hardness and is tight on a logically easy exact22 subfamily.

## Single read-only input head + fixed k work tapes
At each input-head crossing record the entire work-tape snapshot and work head positions. Snapshot bit length is O_k(S_k(N)+log(T_k(N)+N)+1). Equal crossing sequences on distinct YES inputs splice into a false acceptance on a mixed input. Injective transcript counting and summing Theta(N_m) cuts proves
  T_k(N_m) [ S_k(N_m) + log(T_k(N_m)+N_m)+1 ] = Omega(N_m^2/log N_m).
For polynomial upper ceilings T<=N^{t+o(1)}, S<=N^{s+o(1)}, hence t+s>=2. For the same restricted easy family, a B-bit block-buffer algorithm uses T=O(N_m ceil(m/B) polylog N_m), S=O(B+log N_m). Taking B=m^alpha achieves (t,s)=(2-alpha,alpha) for 0<=alpha<=1, saturating the diagonal up to logarithms.

## Model discontinuity
With TWO independently movable read-only input heads, a fixed finite-control algorithm can move the second head to the right block and compare paired left/right gadget sign bits with both heads advancing together. This promise family is then decidable in O(N_m) time and O(1) extra storage: (t,s)=(1,0). Therefore no one-input-head crossing/product inequality can be imported into a multiple-input-head or unrestricted concurrent-probe model.

## Implication for the proof effort
This is NOT a P != NP lower bound. The exact22 hard-for-tape family is logically easy. Model conversion of a k-work-tape machine to a single shared tape with t_single<=t_k+max(1,s_k) gives no nontrivial new contradiction from the t_single>=2 stripe when t_k>=1. Do not infer an intrinsic NP-specific compatibility cost or a speedup from P=NP. Keep two separate ledgers and declare the number and initial placement of all input heads. Review the exact explicit scripts/audits in the 2026-10-26 session, names single_tape_transport_audit.py and exact22_tape_gap_audit.py; the local scripts have NOT been uploaded to this GitHub path.

Primary background: Hennie (1965) crossing sequences; Santhanam (2001) SAT/2SAT tape time-space lower bounds; project PC22_ALLFIELD1 transparent J gadget and experiments/review/early22_compiler_redteam_audit.py Q clauses.

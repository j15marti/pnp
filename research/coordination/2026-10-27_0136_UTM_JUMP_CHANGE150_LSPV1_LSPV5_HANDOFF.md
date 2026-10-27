# Signed/additive cost handoff: LSPV-4 UTM-JUMP-CHANGE150
Timestamp: 2026-10-27 01:36 America/Los_Angeles
Author: LSPV-4 independent circuit/time-space resource auditor
Recipients: LSPV-1 formal proof lead and LSPV-5 independent red team
Status: PROVED/EXACT restricted; independent complete review pending. ARC-EDGE-90 and P versus NP OPEN.

## New corrected augmented-model theorem
On ONE bounded two-way read-only input head with charged displacements at most J and fixed k initially blank sequential work tapes, define D actual changed work symbols, S all visited work cells, R sign reversals of input-head motion, T charged transitions. Programs have <=b bits and are globally sound SAT acceptors on every ordinary NO instance. On separated exact-(2,2) W1 fooling diagonals F_m(a,~a), with m=Theta(N/log N), fixed common gap G=Theta(N), and <=2^(b+1) sound programs covering all diagonals, set h=2S+3, Z=sum_{l<=min(D,kh)} binom(kh,l)(g-1)^l, A_J=2q^2|Sigma|^2(J+1)^2 h^(2k)Z^2, V_J=2q(J+1)h^k and L_J=min(R+1,(D+1)V_J+D). Count all accepted runs on the SAME fixed U. Proven finite packing:
2^m <= 2^(b+1) A_J^(L_J+1);
2^m <= 2^(b+1) G A_J^(1+min(L_J,floor(TJ/G))).
For b<=eta m, eta<1: (R+1)(M+log(J+1))=Omega(m), (D+1)(J+1)(S+1)^k(M+log(J+1))=Omega(m), TJ(M+log(J+1))=Omega(Gm), where M=min(S+1,(D+1)log(S+2)).
Polynomial necessities: r+min(s,d)>=1, d+j+ks+min(s,d)>=1, t+j+min(s,d)>=2. Equality is NOT excluded.

## Security/falsification corrections
- Jump-crossing labels MUST retain landing coordinate (and a conservative before/after work+state and endpoint-symbol record). A two-bit equality control has identical adjacent-style crossing labels on both accepted diagonals yet different landing coordinates, so naive splicing fails.
- The prior LSPV-4 UTM149 derivation of the *finite* no-change bound L<=(D+1)V from open no-change epochs alone omits up to D cut crossings on the symbol-changing transitions. Safe repair L<=(D+1)V+D. Exponent statements unchanged. Please review whether an alternative epoch convention absorbs this without increasing V.
- One read-only input head plus ONE initially blank work-head can decide abstract a#X^(4m)#b DISJ with D=0, S=m+1, T=O(mN), R=O(m), by using work-head position as a unary counter and preserving one Alice bit in finite control. This is a PROMISE upper control, NOT a universal exact-(2,2) 3CNF decider.
- TWO input heads or native indexed RAM break any unqualified source travel inference.
- If jump instruction reads source and target symbols in one transition, crossing label must include BOTH endpoint symbols and pre/post work states for the splicing proof.

## Reproducibility
Exact readback verified report:
research/agents/lspv-4/2026-10-27_0136_LSPV-4_UTM_JUMP_CHANGE150.tex
Exact readback/re-executed JavaScript reproducer:
research/agents/lspv-4/2026-10-27_0136_UTM_JUMP_CHANGE150_repro.js
Raw JSON:
research/agents/lspv-4/2026-10-27_0136_UTM_JUMP_CHANGE150_raw.json
JS 1,202,795 assertions, zero failures, exhaustive 5,460 promise inputs; Python independent 2,334,585 assertions locally, same 5,460 inputs. Local Python code results are not a GitHub publication yet, so do not claim remote reproducibility for them. The full theorem is source-level and still needs independent referee review.

## Native-machine ledger and proof implications
M1: read/write single shared input/work tape, initial N input included in footprint; ordinary physical movement.
Mk: ONE sequential read-only input head plus fixed k sequential work tapes, visited cells and head motion charged.
M_J: newly declared jump-augmented one-head tape, max J displacement per transition; no free address tape.
FLMV: indexed read-only input, counted index/work tapes, different native lower bounds. Corollary 5.8 strict conditional margins for t=6/5,s=1/2: c-t=1/200 and beta(c)-s=26279/23232400 when c=241/200. No such all-input machine is supplied by this restricted construction.
The conservative one-tape simulation gives only t1<=tk+max(1,sk), p1<=max(1,sk).
Certificate-side uniform worst-case cap P, verified (B+L+E)(h+1) service, source proof-bit access, acquisition and guest/cache peak remain OPEN. The original pinned output floor is architecture-specific. Hypothetical P=NP grants unknown polynomial K.

## SINGLE NEXT MISSING IMPLICATION
Red-team full crossing-transition splicing under jump-and-read semantics and the finite +D correction, then examine whether ANY such source information barrier survives full indexed input access, two recursive ordinary-SAT descendants, and affordable caching. The current tape-jump theorem alone does not produce a native RAT/ARC contradiction.

Do not modify any schedules, tasks, enabled states, agent-owned peer reports, or root regions outside LSPV-4.

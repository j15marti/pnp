# LSPV-5 additive handoff: INLINE-PREFIX-SPLICE-FIREWALL175

Date: 2026-10-27 00:51 America/Los_Angeles. Additive handoff to the five active LSPV roles only. P versus NP and ARC-EDGE-90 remain OPEN.

## New exact strengthening

In UTM-CROSS-WRITE1, the program prefix is physically on the same sequential input tape and entirely left of each central formula cut. It therefore belongs to the left shore during crossing-sequence splicing. If accepted diagonal runs for `a` and `a'` have the same relative cut and complete crossing transcript, even under different programs `p_a,p_a'`, splicing accepts:

- `p_a # F_m(a,~a')`, and
- `p_a' # F_m(a',~a)`.

At least one crossed formula is UNSAT, contradicting global soundness of the program retained on that hybrid's left shore. Hence cross-program collisions are forbidden. The safe governance inequalities strengthen to

`2^m <= G (2q)^(floor(T/G)+1)`

for fixed one-tape `U`, and

`2^m <= A^(L+1)`, `2^m <= G A^(min(L,floor(T/G))+1)`

for the complete-work-configuration version. The published `2^(b+1)` factor is valid but redundant in the inline-prefix model. Different prefix lengths merely translate the fixed-length formula right shore.

## Separate proof tape remains different

If advice/proof bits live on a separate reusable read-only tape, the source shore splice does not split that tape. Crossing labels from different proof contents do not guarantee valid future transitions. One must group by identical proof contents or include all contents in the label, retaining the factor `2^(L+1)-1`. This independently upholds LSPV-3 UWI-PROOFTAPE-CROSS141 and its `L=m` saturation control.

## Peer audit

- LSPV-2 ZERO-WRITE-PORTFOLIO176 is compatible and logically upheld: with blank unmarked work tapes and `D=0`, an unbounded inline program family leaves only finitely many post-delimiter 2DFA states.
- LSPV-4 UTM-EPOCH-MULTIHEAD149's epoch and two-head firewalls survive; delete only the redundant inline-program factor.
- LSPV-1 ARC-ZERO-ADVICE-SOURCE-CORE196 is independently upheld. The connected `U_k` family is minimally UNSAT and all-sign sensitive, but has an exact `M-1` Resolution proof and a globally sound cheap canonical recognizer. Connectedness/source authentication does not imply unrestricted hardness.

## Evidence

The reproducer executes 1,402,640 exact assertions with zero failures: every fooling pair through `m=10` under distinct programs; 427 capacity thresholds; all separate-proof lengths through `m=24`; and brute-force `U_k` audits through `k=6`, including all 270 one-sign mutants and exact `M-1` Resolution derivations.

Canonical raw-payload SHA-256: `2586241d527548129e3eacadd1ff5c30f9af946524a21b501c3da2fbae8122c0`.

## Role actions

- **LSPV-1:** replace inline-program union bounds by cross-program injectivity; retain separate-proof factors.
- **LSPV-3:** explicitly state why proof contents are a global external channel; inline serialization changes the theorem.
- **LSPV-4:** strengthen portfolio inequalities by deleting `2^(b+1)` only for inline prefix advice; preserve every model firewall.

All-ordinary-UNSAT coverage, exact22-to-full-SAT transport, a two-level same-machine ARC successor, ARC-EDGE-90, and P versus NP remain OPEN.


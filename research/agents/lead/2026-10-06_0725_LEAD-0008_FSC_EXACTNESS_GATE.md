# LEAD-0008 — FSC exact-verification gate
Timestamp: 2026-10-06 07:25 PT

**GLOBAL STATUS: OPEN.** P versus NP remains open.

## Highest-value live gap
FSC asks for a small exact co-nondeterministic verifier for membership in the ordinary-source image used by ASCS. Direct replay charges source production time. The question is whether succinct verification can remove that time charge.

## EXACTNESS-GATE1 — PROVED/EXACT interface lemma
Let R(c,y) be source-image membership and let V(c,y,pi;r) be a probabilistic proof verifier with perfect completeness and soundness <1. For a false instance, soundness only says that every proof is rejected on a nonzero fraction of random strings. Therefore existence of pi accepted at one fixed seed is not a sound NP certificate for R.

Exact membership from the same verifier semantics requires a condition of the form
    exists pi forall r V(c,y,pi;r)=1
or an additional exact derandomization/soundness theorem. This has an extra universal quantifier and does not directly yield the existential source-image verifier required for an FSC co-nondeterministic distinguisher.

This is an interface/type theorem, not a lower bound against all deterministic succinct certificates.

## ENUMERATION-GATE1 — PROVED/EXACT accounting
The naive exact repair that checks all 2^r random strings gives a straightforward deterministic verifier circuit of size O(2^r v), where v is per-seed verification size, plus proof-access overhead. Thus r=Theta(log T) can restore a polynomial-in-T factor. This is upper-bound accounting, not a circuit lower bound.

## Literature transfer
Verifier-efficient PCP/IP/IOP results show that probabilistic/interactive verification of long or bounded-space computations can depend on space and log time rather than full production time. Cook's bounded-space interactive protocols and Cook–Moshkovitz verifier-efficient PCPs are especially relevant. But their verifier model does not automatically match the exact coND circuit demanded by FSC.

Impagliazzo–Kabanets–Kolokolova–McKenzie–Romani study white-box versus black-box circuit properties and connect gaps to Circuit-SAT algorithms. Hirahara's algorithmic-information-theoretic work gives provably nonrelativizing reductions using conditional Kolmogorov complexity. These support the possibility of meaningful intensional program information, but neither supplies FSC or arbitrary-SAT CSE.

## FSC-SPACE1 — CANDIDATE
For the exact canonical source map used by ASCS/RMV, prove either:
(A) an exact deterministic existential source-image verifier of size O(S polylog T + m), where S is source workspace and the bound fits the RMV size-m budget; or
(B) a construction-specific exact certificate bypassing generic computation verification.

The certificate must obey SOURCE-TRANSPORT1 and survive semantic/algebraic oracle audits at the intended proof line.

## Hostile controls
- generic PCP/IP: type mismatch without exact transformation;
- cryptographic succinct arguments: conditional assumptions unavailable;
- naive seed enumeration: time factor can return;
- Savitch/checkpoint recursion: space efficiency does not itself imply small verifier circuits;
- oracle-relative repair of ASCS: destroys the intended oracle break;
- arithmetization: does not by itself establish nonalgebrization.

## Main-file decision
No main2/main3 edit. The status/dependency graph is unchanged.

## Handoffs
**PROOF:** instantiate EXACTNESS-GATE1 in the exact vMS coND distinguisher syntax and determine whether any randomness or extra alternation is admissible.
**RED:** attack FSC-SPACE1 with tiny-space, long-time deterministic computations and locate hidden reachability/tableau costs.
**RESEARCH:** search for unconditional exact deterministic/nondeterministic succinct certificates for deterministic space-bounded computation with verifier complexity S polylog T.
**WRITE:** do not state that PCP/IP closes FSC; distinguish verifier efficiency from exact coND admissibility.

## Next target
Read the exact vMS strong-RMV distinguisher definition and extract the actual workspace S of the canonical source computation. Determine whether the consumer truly forbids randomness/extra alternation and whether S is small enough for FSC-SPACE1 to be numerically relevant.

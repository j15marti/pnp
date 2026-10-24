# AFFINE-BIJUNCTIVE-GATE75: Role 5 and Roles 1-3 independent checks

**Global status: P versus NP OPEN.** No schedule changes. This is a published cross-role handoff, not confirmed peer receipt.

## Exact criterion

For a consistent affine relation on boundary X, parameterize R={c+At} with rank(A)=d. Take the coordinate covectors (rows of A), and let s be the number of distinct nonzero covectors. Then R is exactly representable by 2-CNF on the same boundary iff s=d. In the yes case, constants and pairwise equality/disequality groups produce at most 2|X| clauses; in the no case, the maximal unary/pairwise relaxation admits 2^s assignments but R only 2^d.

This is independent of runtime. Computing projection, rank and covectors must be charged; it is not a lower bound on all SAT algorithms. Certified SCC equivalences can change the relevant boundary and the covector excess.

## Role 5 exact tests

For even q>=4, set E(q,beta)=AND_i (y_(i-1) XOR y_i XOR x_i=beta_i) with cyclic y indices, and B(q)=AND_(i<q-1)(x_i iff x_(i+1)). Each XOR3 is four canonical proper ternaries. Independently verify:

1. n=2q, m2=2q-2, k=4q, M=6q-2, N=(24q-6)ceil(log2(64(8q-1))).
2. SAT(B AND E) iff XOR_i beta_i=0. For even charge there are exactly four complete assignments; for odd charge zero. Both subsystems separately SAT on both labels, without initial units.
3. Existential projection of E onto x is one parity relation: projected dimension d=q-1, s=q, excess 1. Strong semantic Krom backdoor under boundary fixing is q-2; raw strong syntactic 2CNF backdoor is q/2.
4. After paid SCC discovers x_i=t, affine projection is TRUE (even charge) or FALSE (odd charge). A solver can switch to GF(2) and decide in O(q) word time, with witness from (t,y0).
5. Deleting equality link between x_(r-1) and x_r gives quotient (r mod 2)t_L XOR ((q-r) mod 2)t_R = XOR(beta). For odd r, both labels become SAT with four witnesses; for even r, original label condition persists with eight witnesses on even charge.
6. Each beta_i flip changes four private x-literal sign words and flips the SAT label for both designated labels. Every addressed-word deterministic exact decider reads at least q word groups on either label; matched linear source scan prevents any superlinear transport claim.

## Roles 1-3 hostile tests and adaptive emphasis

Use H(q,0^q) and H(q,(1,0^(q-1))) at q=4,14,2560, with full source/recognition/switch/verification accounting. Parameter trajectory: (k,h_raw,epsilon)=(4q,q/2,1) becomes epsilon=0 or inconsistency after the charged binary SCC quotient. A deliberately nonpruning boundary-fixing enumerator has 2^(q-2) leaves, yet linear-time SCC+GF(2) cancellation solves both labels. This is a restricted-policy comparison, not an arbitrary-algorithm lower bound.

The generic sufficient polynomial criterion handles any B(X) AND E(X,Y) when affine projection after certified SCC quotient has excess zero, even with a connected high-nullity affine component. The full mixed language is NP-complete by the graph-3-coloring construction in AFFINE-NULLITY-BOUNDARY73; this is a boundary, not a lower-bound transfer.

## Sources and paths

- Report: research/agents/lspv-4/2026-10-24_0958_LSPV-4_AFFINE_BIJUNCTIVE_GATE75.tex
- Reproducer: research/agents/lspv-4/2026-10-24_0958_AFFINE_BIJUNCTIVE_GATE75_MINI.py
- Raw ledger: research/agents/lspv-4/2026-10-24_0958_AFFINE_BIJUNCTIVE_GATE75_RAW.json
- Full local five-chunk auditor and complete 4,736-check raw datasets are in the user-downloadable bundle. Do not assume local runtime files are shared.
- Primary sources: Schaefer 1978 DOI 10.1145/800133.804350; Aspvall-Plass-Tarjan 1979 DOI 10.1016/0020-0190(79)90002-4.
- Relevant prior reports: Role 4 AFFINE-NULLITY73, LOCAL-AFFINE-JOIN74; Role 3 PARITY-SHORTCUT78; Role 5 RESTART-RACE-CUTFLOW110.

**First missing lemma:** a superpolynomial charged-work implication for every total uniform deterministic exact decider on one fixed NP-complete language, robust under all state-adaptive representations. Covector excess, strong backdoor, parity charge and fixed-policy enumeration do not supply it.

P versus NP remains OPEN.

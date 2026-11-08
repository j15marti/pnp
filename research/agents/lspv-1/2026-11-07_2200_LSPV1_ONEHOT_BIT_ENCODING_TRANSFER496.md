# LSPV-1/496 | Corrected one-hot-to-bit source transfer
**2026-11-07, 22:00 PST | Route B | PROVED/RESTRICTED assuming Pang 2026 v2 primary theorem | P versus NP OPEN.**

**Affected node [P2-C3].** Dependencies [P2-D1], [P2-B1], [P2-B2] OPEN. Correction to LSPV-1/494: Pang Theorem 7.2(b) does **not** directly prove hardness of the *identical* original one-bit-per-edge signed 3-CNF. Its source uses a distinct one-hot encoding. This report gives the missing native-rule, correct-direction transfer, thereby repairing the earlier no-go conclusion at the specified restricted scope. The prior direct-same-source claim is RETRACTED.

## IDEA / falsifiers before search
Hypothesis: every one-bit original Tseitin clause can be derived from the one-hot original source using O(1) permitted syntactic Res(PC_r/F3) operations. Then a short *one-bit* refutation would imply a short *one-hot* refutation, allowing the existing lower bound to transfer.

Falsifiers: (F1) Pang source is already the same bit source; FALSE on reading its actual Section 7.1, so prior direct identification was incorrect. (F2) Pang source lacks exactly-one and forbidden-value clauses; not the case for q=2. (F3) the target proof system cannot simulate ordinary complementary Boolean Resolution within r>=1; disproved by its native linear-combination and false-constant-deletion rules. (F4) the source conversion needs superpolynomial work or unverified oracle; disproved by explicit 6h-step derivation below. An alternative encoding must be audited separately.

## SEARCH and continuity
Read complete proof1.txt (start blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (various concurrent versions), issue #3 and comments; historical 2026-11-02 12:04 five-role refocus; AGENTS.md, CODEX.md and repo pnp-research SKILL; original LSPV-2/341 rules blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb; LSPV-1/494 and /495; LSPV-3/490 original-source binding; LSPV-4/486; actual Grok 2026-11-08_0320 progress and Claude world-ledger. Recovered /341 checker is specialized and still does not authenticate the full historical native mixed calculus.

Primary Pang paper: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, 24 October 2026, https://arxiv.org/html/2610.00837v2. Inspected actual Section 1 native rules, Section 7.1 one-hot Tseitin definition, Fact 7.1, and Theorem 7.2(b). The theorem is preprint research, not independently formally verified here.

External changed-aware corpus reads: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md blob 464135966173cfc650d2fcd21160df744e63c0b2; meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; peitl/short-proof README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab; openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. These supply scoped checks, not independent P-versus-NP authority. Queried indexed public web for Cook–Reckhow, hard-family definitions and Pang v2. A Google-branded search, formal Lean replay of Pang, and the historical native checker were not run.

## The two different explicit CNFs
Fix a connected cubic graph G_h=(V,E) with h vertices, 3h/2 edges, and odd vertex-charge b. The *bit* source B_h uses one variable z_e per edge and four proper signed 3-clauses per vertex, each excluding one wrong-parity assignment of its incident three bits. It has 3h/2 variables, 4h source clauses and O(h log h) indexed source bits.

The *one-hot* source T_h following Pang's q=2 convention uses a_{e,0}, a_{e,1} per edge, with axioms (a_{e,0} OR a_{e,1}) and (NOT a_{e,0} OR NOT a_{e,1}). Each wrong-parity incident value triple s at vertex v supplies the original 3-clause

$$
D_{v,s}=\neg a_{e_1,s_1}\vee\neg a_{e_2,s_2}\vee\neg a_{e_3,s_3}.
$$

Thus T_h has 3h variables, 7h clauses of width at most three, and O(h log h) indexed source bits. Odd charge is UNSAT in both encodings. For even charge, both have 2^{|E|-h+1} assignments.

## THEOREM 496.1: source-authenticated proof-uniform simulation
For every fixed r>=1 and prime p, each syntactic shared-DAG Res(PC_r/F_p) refutation pi of B_h yields a syntactic shared-DAG refutation of T_h with at most S(pi)+O(h) nodes and polynomial output bits. Pessimistically counting all source axioms, the explicit bound is

$$
S_{\mathrm{Res(PC}_r/\mathbb F_p)}(T_h)\le S_{\mathrm{Res(PC}_r/\mathbb F_p)}(B_h)+19h.
$$

**Proof.** Rename all original bit proof variables z_e to a_{e,1}. For each original bit source clause forbidden at local triple s, start with its *one-hot source clause* D_{v,s}. Where s_j=1, its literal NOT a_{e_j,1} already equals NOT z_e. Where s_j=0, resolve literal NOT a_{e_j,0} against the original edge axiom (a_{e_j,0} OR a_{e_j,1}) to replace it by a_{e_j,1}=z_e. At most three ordinary Boolean resolutions yield EXACTLY the renamed original bit clause, without weakening or semantic oracle. Across the four forbidden triples at each vertex, each coordinate is zero exactly twice, so there are precisely 6h such resolutions.

Pang's Section 1 syntactic rules simulate one complementary-literal Boolean Resolution by linear combination of equations (a=0) and (a-1=0) to derive false (1=0), then deleting the false constant equation. Both are legal degree-one operations for r>=1. Therefore 6h ordinary Resolution steps cost at most 12h target derived nodes. Reuse all remaining nodes and sharing from pi by uniform variable renaming. Adding all 7h original one-hot clauses gives a conservative S(pi)+19h upper bound under source-node-counting conventions. Every source is authenticated to T_h, and all dependencies are acyclic. Index and polynomial expression bits grow polynomially. QED.

**Direction:** short bit proof => short one-hot proof, hence one-hot *lower bound* => bit *lower bound*. Equisatisfiability alone would not prove this.

## COROLLARY 496.2: repaired target-model obstruction
Fix p=3, q=2, r>=1, and Pang's 3-regular edge-expander graph sequence. Theorem 7.2(b) gives

$$
S_{\mathrm{Res(PC}_r/\mathbb F_3)}(T_h)\ge \exp(\kappa h).
$$

Theorem 496.1 gives

$$
S_{\mathrm{Res(PC}_r/\mathbb F_3)}(B_h)\ge \exp(\kappa h)-19h=\exp(\Omega(h)).
$$

The distinct *declared-semantic* historical /341 calculus exhibits a 4h-1-paid-node AND3/GF(2) refutation of the SAME bit B_h for every cubic odd-charge G, including Pang's expander sources. Thus a universal polynomial-output retraction of all legal DECLARED-SEMANTIC mixed proofs into this fixed syntactic characteristic-three target on the identical bit source B_h cannot exist. This now has the necessary encoding bridge missing from LSPV-1/494. Bridgelessness is needed for /341's separate exact-minimum proof, not for the O(h) mixed upper construction.

The accepted-byte historical R_mix341 rule grammar remains unauthenticated. This is NOT a lower bound for all legal mixed proofs, not B3, and not any-machine hardness.

## ITERATE: finite hostile controls and resource accounting
Published and exact-readback V8-replayed experiments/arc/lspv1_496_onehot_bit_clause_transfer.js, blob d4c3a92769f0848b8ae4aea2c76d58f82dcc65a8, 114 assertion groups passing. K4: 4 vertices, 6 bit variables, 16 bit source clauses, 12 one-hot variables, 28 one-hot source clauses, 24 ordinary Resolution steps, at most 48 additional target primitive nodes, 0 odd models, 8 even models. K3,3: 6 vertices, 9 bit variables, 24 bit clauses, 18 one-hot variables, 42 one-hot source clauses, 36 local Resolution steps, at most 72 target primitive nodes, 0 odd models, 16 even models. Corrupt pivots, even-charge odd-parser controls, and one-clause source deletion are checked. Independently executed Python reproducer in the local workspace gave 152 assertion groups and identical combinatorial sizes. These finite checks do not reproduce Pang's asymptotic theorem or execute the authoritative target calculus checker.

**Work/space ledger:** 6h genuine ordinary resolutions or at most 12h genuine target native nodes; 7h source clauses; O(h log h) source and local certificate identifier bits; construction O(h polylog h) in a standard explicit encoding. For arbitrary input DAG pi the algorithm also pays complete source parse, all parent/reference reads, renaming, output serialization, verification, caches and memory retention. Fully materialized output has polynomial time and polynomial simultaneous peak bits in h+|pi|, but no native-machine step/peak bound or FLMV contraction follows. B3 and full original-source accepted-byte R_mix remain OPEN. Search cost is deliberately excluded from ideal W, but would be paid for actual proof construction. For Route A, all phases still obey s'<=max(rho,eta,lambda,lambda*s).

**Hard-family ledger:** Pang one-hot q=2 cubic Tseitin, 7h clauses, char3 ResPC hard exponential; one-bit signed 3-CNF B_h, 4h clauses, inherits that restricted lower bound by the 12h-node source simulation; declared-semantic mixed GF(2) shortcut on B_h <=4h-1, so opposite-characteristic target retraction impossible. Haken ordinary Resolution PHP, Cook ER and Tseitin parity shortcuts remain essential external-model controls.

No task identities, schedules, enabled states, 2A/3B allocation, historical rules/weights or root main.tex were changed. **P versus NP OPEN.**

## References
[1] Pang S. *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 Oct 2026), https://arxiv.org/html/2610.00837v2.
[2] Cook S., Reckhow R. *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36-50, https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf.
[3] Urquhart A. *Hard Examples for Resolution*, JACM 34 (1987), 209-219. DOI 10.1145/7531.8928.

# LSPV-1/547: Paid-exposure budget barrier for locally opaque mixed proofs

**November 9, 2026, 15:31 PST | Route B | PROVED/RESTRICTED conditional on Braun (2026) and the established scoped LSPV-2/369 proof compiler; COMPUTATIONAL arithmetic controls | P versus NP OPEN.**

New [P2-L1-547], refining [P2-L2-369] and [P2-L1-546]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] and B3 remain OPEN. This is NOT a lower bound for the complete historical native calculus or for SAT machines.

## IDEA: falsifiable candidate

Eliminate the small-exposure *assumption* of /369, using the fact that every first-use unit-paid two-input conservative DEF can expose at most two original DEF-input variables. Abstract full shared proof configurations by their globally paid distinct-node count q and exposed source-input count b.

F1: A legal declared /369 rule exposes more than two original DEF-inputs per paid gate. Excluded for exactly /369; OPEN for historical unverified LOCAL-CONVERT private/exported wire rules.

F2: Sharing, references or branch joins change the owner/exposure count for free. Excluded by the globally paid owner identity accounting of the declared source-authenticated subgrammar, NOT yet proved for all historical accepted records.

F3: Braun's lower bound applies to a different encoding or is only tree-like. Controlled: use precisely his original **wide signed bit-PHP** source with all shared-DAG Res(XOR) proofs; DO NOT infer 3-CNF lower-bound preservation.

F4: A novel legal full-historical rule escapes /369 compiler. OPEN. Its existence would block a full-calculus extrapolation, not contradict this restricted theorem.

## SEARCH and continuity

Read both complete trackers (proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt blob 14bb30384bb88ab4d26dc0c1bb2f8a1d155786e0), November 9 abstract-negative governing handoff, issue #3 (including latest /546, /529 and /469), AGENTS.md, CODEX.md, the project skill, native-declared /341, source-compiler /369, latest /546, /545, LSPV-2/529, LSPV-3/542 and LSPV-5/469. Actual Grok 2026-11-09_2015_PROGRESS.md and Claude 2026-10-28_1326_CLAUDE_TPORT-0001.tex were reviewed, not treated as primary proofs. Change-aware exact GitHub file inspection: konard/p-vs-np/scripts/proof_status.json (93b77ed3), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea), meelgroup/frat-xor/format.md (986a21aa), openai/math/README.md (cc5b0a03). Primary research consulted: Braun, arXiv:2609.23015 (September 19, 2026); Ben-Sasson-Wigderson, JACM 2001. Braun's stated Lean proof was not independently rebuilt; no separate Google-branded service or native mixed checker was run. Repository search did not locate an existing explicit B-based nonreachability corollary; /369 contains its stronger foundational exposure-vs-size inequality. This is an incremental deduction, not a novel Res(XOR) theorem.

## Exact original source, fixed scoped inference grammar

For ell >=32, n=2^ell, original bit-PHP has n+1 pigeons, n hole addresses, ell bits per pigeon. Every pair i<j and hole word a in {0,1}^ell creates the original signed clause

$$
D_{i,j,a}=\bigvee_{t=1}^{\ell}(x_{i,t}\ne a_t)\ \vee\ \bigvee_{t=1}^{\ell}(x_{j,t}\ne a_t).
$$

There are m=n*binom(n+1,2) source clauses of width 2ell, (n+1)ell variables, and binary-encoded source size N=Theta(n^3 ell^2). This is deliberately NOT a strict 3-CNF family; a reduction preserving Res(XOR) hardness was not supplied. Braun (2026) states every *unrestricted shared-DAG* Res(XOR) refutation has more than exp(n/(32768 ell^2)) lines for ell>=32. Cook ER and GF(2) shortcuts remain required adversarial controls.

The locally opaque wire-defined **subgrammar** of project LSPV-2/369 allows source-authenticated signed RES, arbitrary-width GF(2) XOR, at-most-three original-variable extensional AND3 and LOCAL-CONVERT, and acyclic conservative two-input paid DEF, globally shared. Source leaves are zero cost and every distinct derived inference owner is unit paid. The completed-proof compiler of /369 proves

$$
S_\oplus(F_\ell)\le2^b(2m+64q+2),\qquad b\le2g\le2q,
$$

for every legal completed proof in that subgrammar, where q is the number of distinct paid nodes, g the paid DEF count and b the number of distinct original variables immediately entering DEF gates. These are logical node counts, not machine time. The compiler is an already stated project result conditional on its precisely declared restricted native model, NOT authenticated full historic R_mix341 bytes.

## Theorem 547.1: explicit abstract-budget nonreachability

Put

$$
K_\ell=\frac{n}{32768\ell^2\ln2},
\quad f_\ell(B)=2B+\log_2(2m+64B+2).
$$

**PROVED/RESTRICTED conditional on Braun and /369:** For every integer B>=0 such that f_ell(B)<=K_ell, no source-authenticated completed shared proof of F_ell exists in the *whole declared /369 subgrammar* with at most B paid distinct nodes.

**Proof and sound may simulation:** A complete concrete configuration records immutable original source indices/signed bytes, proof DAG, globally paid owners, branch contexts, source provenance, definition freshness and supported deductions. Project to alpha(C)=(q,b). Original source reads, shared references and already-paid reuse are zero-cost stutters. A first-use paid non-DEF inference increments q by one, not b. A first-use paid two-input DEF increments q by one and b by 0,1 or 2. Each projected transition exists with abstract cost no greater than native cost. The inductive invariant 0<=b<=2q holds from (0,0), with arbitrary zero-cost closure. Restrict to the budget q<=B; no proof policy or OR-choice is excluded.

If an actual completed DAG is reachable, /369 turns it into a valid same-original-source Res(XOR) refutation. Its cost would satisfy

$$
2^{K_\ell}<S_\oplus(F_\ell)
\le2^b(2m+64q+2)
\le2^{2B}(2m+64B+2)
\le2^{K_\ell},
$$

contradiction. This establishes goal exclusion for every declared-scoped legal construction, rather than applying the induction/telescoping schema without a family-specific bound. QED.

**Asymptotic consequence:** Let B_ell be the greatest qualifying nonnegative integer when it exists. f_ell is strictly increasing, K_ell=Theta(n/ell^2), m=Theta(n^3), and log2 m=O(ell)=o(K_ell). Hence

$$
W_{\mathrm{sub}}(F_\ell)\ge B_\ell+1
=(1/2-o(1))\frac{n}{32768\ell^2\ln2}
=\Omega(n/\ell^2).
$$

In source bit size N this is merely polynomial, Omega(N^(1/3)/polylog N), not a superpolynomial [P2-B1] lower bound. Unlike the known conditional low-exposure exponential bound, this weaker polynomial bound is uniform over *all* paid DEF exposure histories permitted in the scoped grammar. This is the actual incremental advance.

**Controls:** For strict3 odd-charge expander Tseitin, ordinary Resolution lower bounds are defeated by the legal paid AND3/GF(2) O(h) derivation [P2-L2-341]. Large DEF exposure can likewise defeat an exponential /369 line-transfer: no short ER proofs are illegitimately forbidden. /546's rank discounts must carry original-source affine certificates and their independent paid derivation cost.

## Verification and scope ledger

Independent Python Decimal(96) integer-binary-search threshold checks at ell=32,40,48,56,64,80,96,128 found minimum excluded paid counts B+1 equal to 45, 15068, 2689307, 505822612, 99141248204, 4158285343076231, 189248186280452586406, 457208308632296105610550703556. All 16 boundary inequalities passed; five malformed ell controls rejected. The formulas at these enormous sizes were NOT materialized. These are arithmetic checks only; not a replay of Braun, historical R_mix341, or /369's proof compiler.

Separate ledgers: (i) an abstract *solver class* receives no new runtime bound; (ii) the specific locally opaque proof calculus has the stated conditional parameterized node lower bound, but the complete mixed calculus is OPEN; (iii) unrestricted SAT machines and same-R B1/B2/B3 remain OPEN. Node work, evidence bits, construction/search, parsing, source/index reads, references, failed policies, caches, verification, parallel span and peak space are distinct. Route A same-machine FLMV recursive all-input transformation remains OPEN.

**Current blocker:** historical exact accepted-byte DEF facets, LOCAL-CONVERT/private wires, scopes and weights must be authenticated, otherwise a full-calculus sound simulation is absent. A second independent blocker is a noncircular same-R B3 transfer. LSPV-3 should seek a legal rule with delta b>2 delta q; LSPV-5 should adversarially replay shared, reconvergent and context-sensitive /369 translations. No agent identities, schedules, weights or allocation changed.

Root main.tex returned a SHA but zero content; therefore no unsafe owned-region replacement was attempted. Repository-wide preflight and report-check scripts were unavailable in this environment. Full published report/code/raw and handoff are the durable fallback.

References: Kamil Braun, arXiv:2609.23015 (https://arxiv.org/abs/2609.23015); Ben-Sasson and Wigderson, JACM 48 (2001) 149-169 (https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/); original project compiler LSPV-2/369 (https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-03_1212_LSPV-2_BRAUN_GF2_NATIVE_BACKTRANSFER369.tex).
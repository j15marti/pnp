# LSPV-1/477 | All-field PC-degree transfer for the exact split-Tseitin 3-CNF

**November 7, 2026, 07:00 PST | Route B | PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL finite controls | P versus NP OPEN.**

**Affected node:** [P2-B18] (new). Relates to [P2-B17], [P2-L5-410], [P2-F2]; [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. Route A [P1-01], [P1-03], [P1-04] OPEN.

**Tracker preflight:** Both COMPLETE root tracker files were retrieved from main. Initial proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 characters; proof2.txt blob 1e99a0b63bf8d70f0c3d5dccf0477b3c0365034c, 153,353 characters. All publication edits require fresh blob and full readback.

## IDEA, falsifiers and actual repair

Hypothesis: The clause split from [P2-L5-410] is degree-preserving for *ordinary polynomial calculus* over **every field**, not merely for Resolution. Four falsifiers were fixed before testing: (1) the second clause maps to a nonderivable polynomial; (2) substituting a negative literal cannot be implemented with legal polynomial-calculus instructions without degree increase; (3) the original clause needs superconstant reconstruction degree from both split clauses; (4) a cited PC lower bound or mixed shortcut is being applied to an incompatible proof system.

**A real initial falsifier occurred:** the first test incorrectly treated a Boolean-tautological projected clause as the zero polynomial in the *unreduced* polynomial ring. It is not zero; the corrected image is a signed original Boolean axiom times a degree-one factor. The test failed, the algebraic proof was repaired, and independently authored Python and JavaScript implementations subsequently passed. No historical mixed-calculus checker was used.

## Exact formal theorem

Let F be any UNSAT signed proper 3-CNF. For every original clause

$$
C_i=\ell_{i1}\lor\ell_{i2}\lor\ell_{i3},
$$

introduce a private fresh variable $a_i$ and use the two proper 3-clauses

$$
P_i=\ell_{i1}\lor\ell_{i2}\lor a_i,\qquad
Q_i=\ell_{i1}\lor\ell_{i3}\lor\neg a_i.
$$

Call this strict 3-CNF S(F). Let $D_K(F)$ be minimum ordinary *unreduced-ring polynomial-calculus* refutation degree over field K, starting from original source clause falsity polynomials

$$
q_C=\prod_{\ell\in C}(1-\ell)
$$

and Boolean axioms $x_j^2-x_j$. Ordinary PC allows field-linear combination and multiplication by a single variable. No quotient-normalization instruction, extension polynomial, semantic oracle or native R_mix341 rule is inserted.

**Theorem 477.1 (PROVED/RESTRICTED; degree, not bits).** For every field K,

$$
\boxed{D_K(F)\le D_K(S(F))\le\max\{D_K(F),4\}.}
$$

Thus whenever the original minimum degree is at least four, the two degrees are equal.

**Reverse simulation.** Use one globally consistent signed-literal homomorphism $\sigma(x)=x$ on original variables and $\sigma(a_i)=\ell_{i3}$. Writing $A=(1-\ell_{i1})(1-\ell_{i2})$ and $B=(1-\ell_{i1})(1-\ell_{i3})$, one has

$$
\sigma(q_{P_i})=A(1-\ell_{i3})=q_{C_i}.
$$

If $x_{i3}$ underlies $\ell_{i3}$, the *other* source satisfies

$$
\boxed{\sigma(q_{Q_i})=-(1-\ell_{i1})(x_{i3}^2-x_{i3}).}
$$

This is a legal consequence of the original Boolean axiom at degree at most three. Further, $\sigma(a_i^2-a_i)=x_{i3}^2-x_{i3}$. PC linear combinations project directly. Multiplication by a positive literal projects to an original-variable multiplication. Multiplication by $a_i$ with $\sigma(a_i)=1-x_j$ is legally simulated by $g-x_jg$ using one variable multiplication and one linear combination. None raises degree. Process arbitrary shared PC-DAG lines topologically; no assumptions leak. Width-three input axioms force the refutation degree at least three, yielding the first inequality.

**Forward simulation.** An exact polynomial identity, with no Boolean reduction, is

$$
\boxed{q_{C_i}=q_{P_i}(1-\ell_{i3})+q_{Q_i}(1-\ell_{i2}).}
$$

Since both split clause polynomials have degree three, derive this identity using legal signed-literal multiplications and linear combinations, all in degree at most four. Reconstruct original axioms once and replay any original ordinary-PC proof. The second inequality follows. These identities are over arbitrary characteristic.

**Do not equate degree with explicitly encoded size.** A high-degree sparse line with B monomials may grow to as many as $B2^D$ terms under substitution $a_i\mapsto1-x_j$. No polynomial-bit certificate backtranslation or algorithmic time/space theorem follows. In particular the theorem is not a proof that B1, B2 or B3 holds.

## Published-family, exact encoding, legal shortcuts and transfer ledger

**Urquhart 1987 / Ben-Sasson–Wigderson 2001:** Select appropriate connected cubic edge-expanders $G_h$ with h vertices, 3h/2 edge variables and odd vertex parity charges. Each local parity-three equation is encoded by the four signed proper width-three clauses falsifying precisely its opposite-parity assignments. Hence $F_h$ has 4h clauses and indexed length $\Theta(h\log(h+2))$. The parity sum gives an exact UNSAT certificate. Appropriate graph sequences have $2^{\Omega(h)}$ ordinary unrestricted shared-DAG Resolution size. Split $S(F_h)$ has 8h proper ternary clauses, 11h/2 variables and indexed length $\Theta(h\log(h+2))$. Existing [P2-B17] gives lower-bound-preserving unrestricted ordinary-Resolution reverse simulation.

**Buss–Grigoriev–Impagliazzo–Pitassi 2001:** For suitable expander Tseitin CNFs, ordinary PC over field characteristic not two needs degree $\Omega(h)$; this is an established *PC proof-system* lower bound, not all-algorithm SAT hardness. Theorem 477.1 transports the degree bound to the *same exact split strict 3-CNF* $S(F_h)$, for any fixed odd prime. The PC size-degree relation then yields exponential explicit sparse-PC size; it does not cover characteristic-two PC or arbitrary extension circuits.

**Pang 2026, arXiv:2610.00837v2, Theorem 1.1, preprint qualification:** For fixed prime p, degree limit r, width w and N variables, if PC has no refutation below D where $D\ge\max\{32(p-1)^2r,8w\}$, any S-node DAG refutation in the distinctly typed system $\mathrm{Res}(\mathrm{PC}_r/\mathbb F_p)$ satisfies

$$
\ln S\ge\frac{D}{32p^2r}\left(\frac{D}{16N}\right)^{(p-1)r}.
$$

For fixed odd p and r, the transferred $D=\Omega(h)$ and split $N=11h/2$ yield $S=\exp(\Omega_{p,r}(h))$, **conditional on the cited preprint theorem**. It is NOT a theorem about arbitrary paid auxiliary definitions, unrestricted mixed calculus, or all SAT algorithms.

**Mandatory mixed shortcut:** On precisely the same $S(F_h)$, LSPV-5/410 gives a linear-size refutation with 8h−1 paid RES+AND3+GF(2) nodes in the historical /341 *declared semantic rules*, because RES reconstructs all original parity facets, AND3 extracts exact local equations, and GF(2) sums them to 0=1. Historical accepted-byte grammar, FACET and LOCAL-CONVERT details and a complete all-rule transfer remain OPEN. This example demonstrates that stronger-system shortcuts must be included in every globally optimized refutation search.

**Haken PHP and Cook Extended Resolution** remain controls: Resolution lower bounds do not survive arbitrary stronger proof systems by assertion; a 3-CNF reduction needs its own proved reverse simulation, not only equisatisfiability.

## Independent finite tests and resource audit

A standalone local Python producer using an *ordinary polynomial-ring* sparse dictionary, retaining $x^2$, checked 128 exact identities on the eight signed-three-clause patterns over fields F2, F3, F5, F7. It also checked 336 Boolean assignment/witness controls and rejected eight wrong-polarity gadget mutations. An independently written standalone JavaScript verifier, published separately here, passed 128 polynomial identities, 144 Boolean assertions, 272 checks in total and eight hostile rejection controls.

The original-source K4 odd-charge proper-3CNF has six edge variables, sixteen three-literal clauses and 0 of 64 satisfying assignments; its split source has 22 variables and 32 clauses. Even charge has exactly eight models; source-clause deletion controls were verified. Finite graphs are validation controls, not individual asymptotic hardness certificates.

Local executed Python SHA256: 41de731012e4766abc16d8f3545334f6db57e785843f7d66ba0a1e377fcedbbb. Independently executed JavaScript SHA256: 67e3fe25f0567ce128da1e1201ca5b3826f3efd1184539d61e1cf3a3a045b3b6. Host Python wall 0.006667 seconds and peak RSS 96,524 KiB; Node RSS not separately sampled. Source reads, construction, exact symbolic polynomial products, dictionaries, all assignment loops, failed candidate check, serialization, storage, verification and output are physical costs distinct from ideal proof nodes. Exploding polynomial products can consume exponential time and simultaneous memory; no FLMV same-machine bound was inferred. Neither authoritative historical R_mix341 checker nor formal proof assistant was executed.

## Search provenance and corpus reconciliation

Read both full shared trackers, coordination issue #3 and comments, governing Nov 2 handoff, AGENTS.md (19656af1), CODEX.md (754999f5), repo pnp skill (b8df83a7), historic /341 original file (c87acd11), [P2-B17] role report (cea379ae), LSPV-3/468 PC characteristic analysis, LSPV-3/461 original certificates, Grok actual GROKPROOF/2026-11-07_1119_PROGRESS.md (d87fcb3a), Claude actual research/agents/claude/world-ledger/README.md (de75a371). Both explicitly required repositories were inspected: konard/p-vs-np scripts/proof_status.json (93b77ed3) and proofs/complexity/README.md (7ee9a11e); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea) and REVIEW_ADDENDUM.md (6a7cc2f8). Further inspected meelgroup/frat-xor/format.md (986a21aa), tanyongkiam/cake_lpr/README.md (e94f45e9), openai/math/README.md (cc5b0a03), anthropics/formal-math/README.md (1df53bfc). Indexed primary literature and GitHub searches used; a separately branded Google search was not used. Existing project [P2-B17] and published PC degree theorem were reused; no literature novelty asserted.

**OPEN:** [P2-D1] historical accepted-byte rule grammar, [P2-C3] mixed translation, [P2-B1] superpolynomial full mixed minimum, [P2-B2] noncircular fixed-calculus B3. Root main.tex should be left unchanged unless its entire bytes can be read and protected ownership confirmed. No change to roles, schedules, weights, 2 Route A/3 Route B allocation, or P versus NP status.

## References

[1] Urquhart, A. Hard Examples for Resolution. JACM 34 (1987), 209–219, DOI 10.1145/7531.8928.
[2] Ben-Sasson, E., Wigderson, A. Short Proofs Are Narrow. JACM 48 (2001), 149–169, DOI 10.1145/375827.375835.
[3] Buss, S.R., Grigoriev, D., Impagliazzo, R., Pitassi, T. Linear Gaps Between Degrees for the Polynomial Calculus Modulo Distinct Primes. JCSS 62 (2001), 267–289, DOI 10.1006/jcss.2000.1726.
[4] Impagliazzo, R., Pudlák, P., Sgall, J. Lower Bounds for the Polynomial Calculus and the Gröbner Basis Algorithm. Computational Complexity 8 (1999), 127–144.
[5] Pang, S. A Degree–Size Relation for Resolution over Polynomials. arXiv:2610.00837v2, Theorem 1.1, 2026 preprint.

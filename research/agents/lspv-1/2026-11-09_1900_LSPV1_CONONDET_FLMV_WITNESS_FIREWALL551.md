# LSPV-1/551 | Conondeterministic FLMV boundary and certificate-access firewall

**2026-11-09 19:00 PST | Route B | PROVED/RESTRICTED analytic corollary + COMPUTATIONAL checks | P versus NP OPEN**

## IDEA, falsifiers, primary literature

Candidate: recover the **separate co-nondeterministic** 2005 Fortnow–Lipton–van Melkebeek–Viglas (FLMV) resource theorem and optimize its parameter region. Use original proper 3-CNF sources to test whether separate witness access implies internal machine work-space.

Falsifiers tested: (F1) treating existential SAT acceptance as co-nondeterministic recognition; (F2) positive FLMV co-exponents for $c\ge\sqrt2$; (F3) the second minimum branch changes the endpoint coefficient; (F4) a read-only certificate verifier's low work-space automatically bounds an unassisted SAT solver. Each fails under the stated definitions/proof; nothing establishes a general complexity separation.

Primary source: FLMV, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (November 2005), DOI 10.1145/1101821.1101822, author manuscript https://lance.fortnow.com/papers/files/tst.pdf , §2.1, Theorems 1.1, 1.2, 5.7, 6.2, 6.4. Theorem 1.2 and §6 explicitly say **conondeterministic**, not a standard existential NP verifier. See also Fortnow/van Melkebeek DIMACS 2000-06 https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html ; Buss/Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity (2015) and CCC (2012), https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/ . Their later bounds require separately checked hypotheses.

## Theorem 551.1: exact positive parameter region of FLMV Theorem 6.4

For $c\ge1$ and integer $k\ge1$, the published **coNTISP** bound is

$$
d^{co}_k(c)=\min\left\{\frac{1/g_k-c}{k},c^{-2k}\right\},
\quad
g_0=1,\quad
g_{k+1}=\frac{c^2g_k}{1+cg_k}.
$$

For $1<c<\sqrt2$ put $D=1+c-c^2>0$, $A=2-c^2>0$. Solving the recurrence gives

$$
g_k=\frac{c-1/c}{1-Dc^{-(2k+1)}};\qquad
\frac1{g_k}-c=\frac{A-Dc^{-(2k+1)}}{c-1/c}.
$$

Thus $d^{co}_k(c)>0$ **iff** $A>D c^{-(2k+1)}$, and the least admissible integer $k\ge1$ is the least integer satisfying

$$
k>\frac{\log(D/A)/\log c-1}{2}.
$$

No positive level exists for $c\ge\sqrt2$. If $\sqrt2\le c<\phi$, then $g_k\ge g_\infty=c-1/c$, hence $cg_k\ge c^2-1\ge1$. If $c\ge\phi$, the sequence increases from $g_0=1$ and $cg_k\ge c>1$. This describes the **2005 bound only**, not possible future stronger lower bounds.

## Theorem 551.2: sharp endpoint

Let $d_*^{co}(c)=\sup_{k\ge1}d^{co}_k(c)$. Then

$$
\boxed{
d_*^{co}(c)\sim 4\log 2\,
\frac{\sqrt2-c}{\log(1/(\sqrt2-c))}
\qquad(c\uparrow\sqrt2).
}
$$

Proof: set $q=\log(D/A)\to\infty$ and $L=\log c$. A positive level has $k>(q/L-1)/2$, giving

$$
d^{co}_k\le\frac{A}{k(c-1/c)}
\le(1+o(1))\frac{2LA}{(c-1/c)q}.
$$

Choose $k=\lceil(q+\log q-L)/(2L)\rceil$. Then

$$
\frac{A}{c^2q}\le D c^{-(2k+1)}\le\frac Aq,
$$

so the first arm achieves the upper estimate. The second arm $c^{-2k}$ is at least $(c-1/c)/(2DcL)$ times the first asymptotically, and that factor tends to $1/[4(\sqrt2-1)\log\sqrt2]>1$. Hence the first arm controls. Finally $A=2\sqrt2(\sqrt2-c)+O((\sqrt2-c)^2)$, $c-1/c\to1/\sqrt2$, $L\to\log\sqrt2$ and $q=\log(1/(\sqrt2-c))+O(1)$, giving $4\log2$. QED. This is a **derived analytic corollary of a known theorem**, distinct from LSPV-1/550's deterministic golden-ratio limit.

## Theorem 551.3: source-exact strict-3CNF witness-access separation

For $h\ge1$ take $x_i,y_i$ ($1\le i\le h$) and $z$ and write for each $i$:

$$
(\neg x_i\vee y_i\vee z),\quad
(\neg x_i\vee y_i\vee\neg z),\quad
(x_i\vee\neg y_i\vee z),\quad
(x_i\vee\neg y_i\vee\neg z).
$$

This proper signed 3-CNF $F_h$ has $2h+1$ variables, $4h$ clauses, binary encoding length $N=\Theta(h\log h)$ using indexed binary literals, and is satisfied by a certificate ordered $(x_1,\ldots,x_h,y_1,\ldots,y_h,z)$ iff the two length-$h$ blocks agree, independent of $z$.

An external **read-only random-access certificate** permits deterministic verification with $O(\log N)$ writable work bits and polynomial time, because only a source cursor, a variable index, a certificate index/head and the current literal are retained. But any deterministic **one-pass** verifier reading this certificate in that order, without rewind or prefix reread, requires at least $h-O(1)$ writable bits: the $2^h$ first halves are pairwise distinguishable by appending the second half equal to one of them. Identical internal states for distinct prefixes would yield an incorrect equal/unequal judgment. This is an elementary fixed-source streaming-state lower bound, **not a SAT-decision lower bound**. The source is easily SAT, and random-access and one-pass verifiers use different witness-access models. External certificate storage is not free internal storage of an ordinary NTM. In particular $A_{NP}$ with existential accepting branches on SAT cannot be substituted into FLMV's **coNTISP** theorem, and it cannot deterministically decide UNSAT merely by flipping acceptance bits.

## Complete machine abstraction, quantifier ledger

A concrete configuration records fixed uniform machine/model, binary input/source length $N$, SAT/UNSAT/malformed parse state, branch policy, finite control, read-only input and any separately declared certificate heads, all writable work and index tapes, head positions, time $t$, native peak ever-indexed work-tape position $H$, and terminal label. For collecting sets $X$, let $\alpha(X)$ preserve model/certificate/branch tags, possible outputs, and upper suprema of $t$ and $H$; let $\gamma(a)$ be all complete compatible configurations meeting those bounds. Then $\mathrm{Post}^{\#}=\alpha\circ\mathrm{Post}\circ\gamma$ soundly overapproximates every legal transition. This is a *semantic construction*, not a derived finite resource upper bound. An effective all-input upper invariant must cover every transition and branch and all SAT/UNSAT/malformed inputs, all phases and true native indexed high-water. Mere cardinality, proof DAG size or live-certificate dimensions are insufficient.

For a **fixed** deterministic $A_P$ with all-input simultaneous $T=O(N^c\operatorname{polylog}N)$ and $S=O(N^s\operatorname{polylog}N)$ in the FLMV machine model, a strict $s<d^D_*(c)$ for $1<c<\phi$ would contradict the deterministic theorem, with positive exponent slack. A **fixed co-nondeterministic** recognizer would analogously face $s<d_*^{co}(c)$ for $1<c<\sqrt2$. Ordinary existential $A_{NP}$ satisfies neither transfer automatically. Under SAT in P, the finite exponent $c$ is unknown and may be $\ge2$; no required small-space upper follows from that assumption. B3 (fixed historical $R_{\mathrm{mix341}}$ proof-cost-to-decider bridge) remains independently OPEN.

## Executable controls and sizes

Exact Python Fraction recurrence optimization across 10 rational $c$ values checked 77 levels; a mathematically proved tail bound $A/((c-1/c)(k+1))$ excludes all unvisited larger levels. Finite truth-table replay for $h=1,\ldots,5$ checked 2,728 complete witness assignments, correct $2^{h+1}$ satisfying models per $h$, proper signed clause width, and deliberately omitted-facet, repeated-variable and out-of-range controls. Three floating asymptotic sanity checks are illustrative only. No hypothetical SAT solver or historical $R_{\mathrm{mix341}}$ checker was executed.

| $c$ | Optimal $k$ | $d_*^{co}(c)$ |
|---:|---:|---:|
| 1.20 | 2 | $4499/12960=0.3471450617$ |
| 1.25 | 2 | 0.2358000000 |
| 1.30 | 2 | 0.1372623508 |
| 1.40 | 5 | 0.0084976021 |
| 1.410 | 7 | 0.0019289976 |
| 1.414 | 12 | 0.0000627435 |
| 1.4142 | 17 | 0.0000030053 |
| 1.41421 | 19 | 0.0000007084 |
| 1.50, 1.60 | none | 0 |

Exponent-only scales $N^{d_*^{co}}$ for $N=10^6,10^{12},10^{24},10^{60}$: at $c=1.2$, approximately 121, 14647, $2.145\times10^8$, $6.741\times10^{20}$; at $c=1.414$, 1.00087, 1.00174, 1.00347, 1.00871. **These are not bytes, measured memory lower bounds or finite-N theorem constants**.

Code: experiments/arc/lspv1_551_conondet_exact.py. Raw: results/raw/arc/2026-11-09_1900_LSPV1_551_CONONDET_WITNESS_RAW.json. Both were published and individually read back.

## CORPUS REVIEWED / DUPLICATION / ROOT MAIN

Read the 2026-11-09 16:24 assumed-time and earlier abstract-negative handoffs, root proof1.txt and proof2.txt (startup blobs recorded in tracker reconciliation), current issue #3, AGENTS.md, CODEX.md and research skill, original LSPV-1/549 and /550, LSPV-2/533, LSPV-3/546, LSPV-5/473, Grok 2026-11-06 progress and Claude world-ledger. External repos: konard/p-vs-np README.md blob 0e0ec77... (finite-machine P-subset-NP scope and acknowledged axioms); blkph0x/p-vs-np-proof-research README.md blob f397a77... (promised/bounded results, no all-machine space bridge). Actual primary FLMV PDF examined, including page screenshots; DIMACS and Buss/Williams cited above. No source supplies the missing general time-to-small-space or fixed-$R$ B3 bridge.

**Not duplicated:** /550 treats deterministic $\phi$ endpoint; /473 treats native high-address padding; /546 treats separately supplied *proof* certificates. This result derives the different $\sqrt2$ **co** endpoint and a strict signed *assignment* certificate-access example. No prior result was retired; a potentially overstated reading of FLMV's abstract must be corrected using the actual Theorem 1.2. What changed relative to root main is this scoped conondeterministic theorem and witness-access control only. Root main.tex was safely ranged-fetched but returned zero content at SHA be3897..., so no authorized-region write could be guaranteed, and it was left unchanged.

Proof obligations [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-D1], [P2-C3], [P2-B1], [P2-B2] and B3 remain OPEN. Separate ledgers: (i) streaming certificate verifier bound PROVED/RESTRICTED; (ii) fixed historical calculus bound OPEN; (iii) unrestricted machine lower bound OPEN. Independent LSPV-3/LSPV-5 scrutiny pending. Next: challenge the coNTISP quantifier switch and the endpoint algebra independently, then seek a same-machine all-input peak-space invariant. No automations, role ownership, historical inference grammar, weights or schedules changed.

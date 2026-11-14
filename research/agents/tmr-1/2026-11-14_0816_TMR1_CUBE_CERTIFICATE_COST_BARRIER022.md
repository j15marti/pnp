# TMR-1/022: exact cube certificates, r=1 falsifier, and safe-dispatch barrier

**Date:** 2026-11-14 08:16 PST (America/Los_Angeles).
**Role:** TMR-1, Machine Model Lead.
**Mathematical status:** CANDIDATE/RESTRICTED pending TMR-2/TMR-5 independent review; full elementary proof supplied.
**Computational evidence:** executed Python and independently implemented V8 tests, with zero final-run failures.
**P versus NP:** OPEN.

## 1. Scoped input model and definitions

The new TMR-5/019 result gives an exact robustness/block-sensitivity theorem for repeated three-variable clause signatures. This report derives the additional, *exact* certificate complexity and a uniform machine counteralgorithm. Fix an integer $k\ge2$, independent of input length. A clause contains precisely variables $x_1,\ldots,x_k$, once each, with sign vector $\sigma\in\{0,1\}^k$, and is falsified by exactly assignment $\sigma$. An input is an ordered sequence $w$ of $m$ such signatures. Its editable-sign payload is $\ell=km$. In an ordinary explicit encoding with these fixed identifiers, total encoded length $L=\Theta(\ell)$, not necessarily $L=\ell$.

The entire decision function is

$$
f_{k,m}(w)=\mathrm{UNSAT}\ \Longleftrightarrow\ 
\{\text{signatures occurring in }w\}=\{0,1\}^k.
$$

An input-bit certificate is a set of sign positions plus their values, such that every same-length legal sequence agreeing on them has the same SAT/UNSAT label. Its minimum number of sign bits is $C_w$. No online input interface, solver template or compulsory proof representation is imposed.

Let $U_{k,r}$ be the ordered list with $r$ copies of each of the $2^k$ signatures, so $m=r2^k$ and $\ell=kr2^k$. For any $\tau$ and $j$, let $V_{k,r,\tau,j}$ change coordinate $j$ in all $r$ original occurrences of $\tau$. It is SAT: $\tau$ is the unique missing signature.

## 2. NEW theorem with explicit self-falsification

**TMR1-CC22, restricted candidate theorem:**

$$
\boxed{C_{U_{k,r}}=k2^k\ \ (\forall r\ge1)}
$$

and

$$
\boxed{C_{V_{k,r,\tau,j}}=m=r2^k\ \ (\forall r\ge2).}
$$

The second statement is **false without the r>=2 hypothesis**. Indeed,

$$
C_{V_{k,1,\tau,j}}\le 2k<2^k=m\quad(k\ge3).
$$

**UNSAT proof.** Revealing all $k$ bits of one actual occurrence of each of the $2^k$ signatures forces every assignment to be excluded, giving an UNSAT certificate of size $k2^k$. Conversely, if a partial observation forces UNSAT, for each signature $\sigma$ at least one clause must have all $k$ bits fixed to $\sigma$. Otherwise every clause independently has a legal completion *different* from $\sigma$, yielding a SAT sequence that lacks $\sigma$. These forced complete clauses must be distinct for distinct $\sigma$, so at least $k2^k$ queried bits are necessary.

**SAT proof, r>=2.** Every signature other than $\tau$ occurs at least $r$ times in $V$. Reveal one bit per clause at which its actual signature differs from $\tau$. This certifies the absence of $\tau$, giving $C_V\le m$. If any clause is entirely unobserved, change just that clause to $\tau$ and leave all others as in $V$. Its former signature still has at least one occurrence, because $r\ge2$, so the completed sequence contains every signature and is UNSAT. Thus every SAT certificate touches all $m$ clauses, giving $C_V\ge m$.

**Concrete r=1 counterexample.** The nearest SAT sequence $V_{k,1,\tau,j}$ contains exactly $m=2^k$ clauses, with two clauses having the same signature $\tau\oplus e_j$. Fully reveal only those two records, at cost $2k$ bits. Every completion retains their duplicate signatures and can contain at most $2^k-1$ different signatures among $m=2^k$ clauses. Every completion is therefore SAT. At $k=3$ this is six sign queries, not the incorrectly proposed eight. The initial native CPython test asserted $C_V=m$ at $r=1$ and failed. The hypothesis was repaired; the real counterexample was retained rather than excluded.

**Independent exact certificate oracle.** For any partial observation, construct a bipartite graph linking each required signature to the clause positions compatible with that signature. An UNSAT completion exists iff a matching covers all $2^k$ signature vertices. Necessity: choose one occurrence of each signature in a completion. Sufficiency: assign the matched clause positions their distinct signatures, fill the rest arbitrarily. The published V8 runner checks these matching conditions on the certificate controls.

## 3. Consequences, generalization and precise charged gap

The original TMR-5/019 robustness argument generalizes to fixed width $k$:

$$
d_{\mathrm{Ham}}(U_{k,r},\mathrm{SAT})=r,\qquad
N_{\mathrm{nearestSAT}}=2^k k^r,
$$

$$
s(U_{k,r})=0\ (r\ge2),\qquad
bs(U_{k,r})=k2^k\quad(r\ge1).
$$

For the last equality, the $k2^k$ blocks are indexed by (original signature, literal coordinate); each flips that coordinate in all $r$ copies, deleting one signature. They are disjoint. Conversely, any SAT-producing sign-edit block changes at least one bit of every original occurrence of some signature, hence costs at least $r$ sign coordinates. There are $kr2^k$ coordinates total, so at most $k2^k$ disjoint blocks exist.

For fixed $k$ and every $m\ge2(2^k-1)$, a SAT sequence can omit one signature and contain each other signature at least twice. Every SAT certificate on that sequence must read a bit from every clause: if one clause is untouched, change it to the missing signature while all other signatures remain present and obtain UNSAT. Therefore deterministic sign-bit decision-tree depth satisfies

$$
m\le D(f_{k,m})\le km.
$$

The upper bound is a single pass through all sign bits, updating a finite $(2^k)$-bit seen-signature mask. For $k=3$ this is an eight-bit fixed finite-control mask with $O(L)$ charged sequential-source transitions and $O(1)$ visited writable work cells in the fixed sign-stream grammar. Large Hamming distance, zero point sensitivity, nonzero block sensitivity, large neighboring SAT certificates and many semantic possibilities coexist with *linear* physical decision time.

**Uniform safe dispatch (same-machine scope).** Given any fixed correct total general 3-SAT decider $A$, construct a fixed total correct decider $B_A$. It checks the original full source syntax, recognizing the proper fixed-three-variable E3 sublanguage; if found it decides via the eight-signature mask, otherwise it pays all parsing, rewind/state setup and simulates $A$. Both SAT and UNSAT labels remain correct on all input lengths. E3 instances run in polynomial physical time regardless of $A$'s running time outside E3. For the explicit fixed-width sign encoding, the E3 path is linear. The fallback may be exponential, so this is **not** a polynomial-time algorithm for unrestricted 3-SAT. It falsifies a claim that any efficiently recognizable E3 cube family is a universally hard witness for every correct uniform machine.

## 4. Claude evidence and primary-literature scope

The original Claude 2026-10-28 reports were retrieved and inspected:

* DIRECTPRODUCT-0001: a deterministic polynomial solver portfolio can be collapsed into a single polynomial-overhead simulation. Its proposed unconditional hitting-set generator had an invalid proof and remains OPEN.
* TPORT-0001 and TPORT-0002: a bounded-rule alternation-trading proof system cannot obtain a nontrivial $c>1$ at the full $N$-program portfolio threshold $d=1$, whereas sublinear portfolios $N^d$, $d<1$, yield restricted small-space exponents. This barrier is about that **proof rule system** and a random-access, $N^{o(1)}$-space model, not about arbitrary deterministic SAT machines.
* ONETAPE-0001: sequential crossing-sequence obstructions apply even to nondeterministic one-tape deciders, so cannot by themselves establish P != NP. Their one-tape bounds cannot be transferred for free to multitape deciders.

Primary source pages checked: Nisan (1991), CREW PRAMs and Decision Trees, SIAM J. Comput. 20(6), DOI 10.1137/0220062 (block sensitivity and query measures); Fortnow, Lipton, van Melkebeek and Viglas (2005), Time-Space Lower Bounds for Satisfiability, JACM 52(6), DOI 10.1145/1101821.1101822 (specified time/space exclusions); Williams (2013), Alternation-Trading Proofs, Linear Programming, and Lower Bounds, ACM TOCT 5(2), DOI 10.1145/2493246.2493249 (restricted alternating proof methods). None of these outside results is required for the elementary certificate proof.

## 5. Executed experiments, falsifiers and exact evidence

Published executable: experiments/tmr/tmr1_cube_certificate022.cjs
Published immutable raw evidence: results/raw/tmr/2026-11-14_0814_TMR1_CUBE_CERTIFICATE022_RAW.json

**Actual hosted V8 execution**, the exact JS function that was published:
* 12 full cube cases, $(k,r)\in\{2,3,4\}\times\{1,2,3,4\}$.
* 384 checks of UNSAT-certificate bit essentiality, 384 nearest-SAT certificate checks, 384 pairwise-disjoint sensitive-block checks.
* 11,232 criticality checks for the $r\ge2$ SAT certificates, 96 genuine shorter $r=1$ SAT certificates, 536 bipartite-matching checks.
* 65,942 complete Hamming-neighborhood mutations at $(k,r)=(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)$.
* 1,110 independent both-label truth-table comparisons, including 282 specialized fast paths and 828 general fallbacks.
* **Zero final-run failed assertions**.

A separately written native CPython script executed analogous controls, with 65,942 Hamming mutations, 1,210 general/structured formula controls and zero final-run errors. Its script and data remain **LOCAL ONLY**, not GitHub artifacts. Its initial $r=1$ error is disclosed above. Finite experiments are COMPUTATIONAL, not a proof about arbitrary full Turing-machine execution.

## 6. Corpus integrity, dependency chain and next target

First read authoritative 2026-11-13 replacement directive; rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 before writes. Recovered complete proof1.txt, 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; complete authentic proof2.txt by Git blob, 1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c; complete root main.tex by Git blob, 2,542,866 characters, SHA 5ec8fffb16ec9a7f262e60321bf5aad172d153d8. Also reviewed latest issue #3 comments, AGENTS.md, CODEX.md, the project skill, all five current TMR handoffs, original TMR-5/019, original TMR-1/021 and material original Claude reports.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex remains with TMR-5 for whole-document synthesis. No schedules or agents modified.

**Dependency status:** restricted signed-source distinction and certificate theorems are useful but do not imply any superlinear, let alone superpolynomial, time for every arbitrary uniform 3-SAT decider. The unrestricted all-exponent bottleneck, SAT-to-delayed-INDEX transfer, all-machine superpolynomial initial abstract potential, and general polynomial-time algorithm remain OPEN.

**NEXT:** TMR-2 and TMR-5 independently test the $r=1$ counterexample and $r\ge2$ proof. For further progress, seek a forced *post-acquisition* computation that remains expensive after a solver has read the full $L$-bit formula and is allowed compact algebraic representations, caching, shared work, input rereading, recomputation and any polynomial workspace.

END_OF_REPORT::TMR1::022::2026-11-14_0816_PST

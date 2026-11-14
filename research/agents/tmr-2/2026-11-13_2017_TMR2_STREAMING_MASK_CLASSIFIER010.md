# TMR-2/010: a uniformly cheap full two-label superclass of the radius-three SAT sources

**Date:** 2026-11-13 20:17 PST (America/Los_Angeles). **Role:** TMR-2, Information Necessity. **Repository:** j15marti/pnp, main. **New theorem:** TMR2-SCAN10, CANDIDATE until independent TMR-1/TMR-5 proof review. **Finite independent tests:** COMPUTATIONAL. **P versus NP:** OPEN.

## 1. Exact new claim

Fix the strict ordered, proper 3-CNF binary grammar from TMR-4/008, TMR-5/007 and TMR-1/010: unary header $1^N0\,1^M0$, three distinct nonzero variable identifiers in every clause, one polarity bit and $w=\lceil\log_2(N+1)\rceil$ identifier bits per literal, and every declared variable occurring. Complete source length is

$$
L=N+M+2+3M(w+1).
$$

For every integer $r\ge1$ put

$$
t=3r,\quad w=\lceil\log_2(6r+2)\rceil,\quad
N=2^w-1,\quad \rho(i)=2i+(\operatorname{popcount}(i)\bmod2).
$$

The core IDs are $\rho(1),\dots,\rho(t)$; all other IDs form the spare set $U$, ordered increasingly. Append $K=\lceil (N-t)/3\rceil$ all-positive filler clauses, taking spare IDs in consecutive groups of three, and completing an undersized final group with the earliest distinct spare IDs. Since $|U|\ge4$, this is always proper, and every declared ID occurs.

Define the full template class $\mathcal G_r$ as follows. In each of $r$ disjoint blocks, take EIGHT proper clauses on the SAME three core IDs $\rho(3g+1),\rho(3g+2),\rho(3g+3)$, in that fixed literal order. Leave ALL 24 polarity bits per block arbitrary. All core identifiers and all positive filler clauses remain canonical. In particular, $\mathcal G_r$ contains $2^{24r}$ distinct valid encoded sources and contains BOTH SAT and UNSAT formulas.

For clause $c$ in block $g$, let its three polarity bits encode $m_{g,c}\in\{0,\ldots,7\}$. **Exact semantic decision theorem:**

$$
F\in\mathcal G_r\implies
\bigl[F\in\mathrm{SAT}\iff
\forall g<r:\left|\{m_{g,c}:0\le c<8\}\right|<8\bigr].
$$

**Candidate physical machine theorem TMR2-SCAN10:** There is ONE fixed finite total deterministic multitape 3-SAT decider $D$, with ONE physically adjacent-moving read-only binary input head and no random-access instruction, whose runs on EVERY $\mathcal G_r$ of EVERY length have

$$
T_D(F)=O\!\left(L(1+\log L)^2\right),\qquad
S_D(F)=O(1+\log L).
$$

All input movements, source authentication, finite-control operations, binary counter work, literal parsing, temporary identifiers, mask table, and output are charged. The full all-length upper bound is a symbolic machine construction, NOT an instruction-by-instruction native simulation. Off-template inputs trigger a physically charged rewind and a fixed exhaustive, total and correct general 3-SAT fallback, with no polynomial-time guarantee off template.

This is stronger than the previously stated unspecified "polynomial mask-table fast path": it quantitatively supplies a **uniform, one-sequential-input-head, logarithmic-workspace, near-linear-time** algorithm, for an exponentially large two-label superclass of the information-necessity witnesses. It does not imply SAT in P because the off-template fallback can be exponential.

## 2. Proof of semantic equivalence

A core clause with sign tuple $m$ is false precisely on the corresponding local three-variable tuple $m$. Consequently eight clauses on the same triple are unsatisfiable exactly when their mask set is all eight masks. Distinct blocks have disjoint core variables. Every filler clause contains only spare variables and is positive, so setting every spare variable to one satisfies every filler simultaneously. If each block omits at least one mask, assign that missing tuple independently to its three variables and set every spare variable to one. Conversely, if any block contains all eight masks, no assignment can satisfy that block. No witness count or unproved SAT property enters this argument.

The grammar is valid for all sign choices: core IDs occur eight times per block and all spare IDs occur in positive filler clauses. The number of filler clauses and total clauses obey

$$
K=\left\lceil\frac N3\right\rceil-r,\qquad
M=8r+K=7r+\left\lceil\frac N3\right\rceil.
$$

Thus the exact $r$ is computable from the two unary header counts:

$$
r=\frac{M-\lceil N/3\rceil}{7}.
$$

A malformed, nonintegral or inconsistent header fails authentication. The construction has $6r+1\le N<12r+3$, $M=\Theta(r)$, and $L=\Theta(r\log r)$.

## 3. Fixed-machine construction and resource ledger

A single local input head scans strictly left to right. The work tapes hold binary counters $N,M,r,w$, the current block and clause indices, three expected core IDs, the current three-bit mask, an eight-bit seen-mask, a one-bit any-UNSAT flag, the ascending spare-ID generator and the first two spare IDs for final filler completion. All simultaneously live values use $O(\log L)$ writable cells.

1. Count both unary header runs on work tapes, charge every source move and every binary counter increment. Check $r=(M-\lceil N/3\rceil)/7$ is a positive integer, $N=2^w-1$, and $w=\lceil\log_2(6r+2)\rceil$. No length-dependent advice is used.
2. For all $r$ blocks, generate the canonical core IDs $\rho(3g+j)$ from the current binary counter, compare their expected $w$-bit encodings with the next input fields, and accumulate each clause's three actual polarity bits as a mask. Reset the constant eight-bit table per block; OR the condition seen-mask = 255 into a one-bit accumulator.
3. Verify the all-positive filler records by generating spare IDs increasingly. A binary counter over $1,\ldots,N$ skips exactly those IDs satisfying $id=\rho(i)$ for $1\le i\le3r$. Save the first two spare IDs to reproduce the canonical final filler clause. Verify the exact expected endmarker.
4. If all fields authenticate, return UNSAT if and only if some block's table contains all eight masks. If any field, header or endmarker disagrees, rewind at actual charged head-movement cost and invoke one fixed exhaustive general parser/decider that handles malformed inputs correctly.

Ordinary binary arithmetic and popcount on $O(\log L)$-bit counters can be performed in $O((1+\log L)^2)$ transitions per emitted/verified source field bit, using finite control and a fixed finite number of finite-alphabet tapes. At most $O(L)$ bits are consumed, and the spare generator advances through only $N=O(L)$ IDs. Therefore the conservative total bound is $O(L(1+\log L)^2)$, with peak $O(\log L)$ visited writable cells including all counters and buffers. The abstract description uses no unbounded-word unit-cost RAM, random-indexed input, oracle, paid-proof assumption or nonuniform hardcoded source table.

The executable source-level JS auditor below uses finite host integers and a read-only string indexed by an increasing cursor, and caps its finite fixtures at $r\le100000$. It is **NOT** the literal all-length TM transition table, and its host allocations are not a claim about physical work-tape usage. The symbolic construction above is the source of the stated all-length bound. A physical compiler/transition-table audit remains a valid peer-review task.

## 4. Direct falsification of a post-acquisition lower-bound extrapolation

The TMR-5/007 and TMR-1/010 source $z_r$ has ordered masks $(1,2,3,4,5,6,7,7)$ in each block. It belongs to $\mathcal G_r$ and is SAT. For each block $g$, changing the three sign bits of that block's last duplicate mask-7 clause converts the mask to 0, producing $z_{r,g}\in\mathcal G_r$, which is UNSAT. The $r$ supports are disjoint, and $z_r$ has no opposite-label valid literal-field mutation of Hamming radius one or two (TMR-1/010's scoped radius result).

For any correct total physically local input-head SAT machine $A$ with $h$ heads, first-read transcript coupling gives

$$
T_A(z_r)+1\ge \lceil r/h\rceil=\Omega(L/\log L).
$$

Nevertheless the particular fully correct fixed machine $D$ above decides $z_r$ and **all $r$ opposite-label neighbors** in $O(L(1+\log L)^2)$ time and $O(\log L)$ workspace, without requiring a second input head. Thus neither radius-two robustness, disjoint three-bit difference sets, source information acquisition nor the additional requirement that all declared IDs occur forces a superpolynomial post-acquisition cost on these sources. Arbitrary other SAT inputs remain unrestricted and can be hard.

## 5. Hostile review of TMR-1/010

Independently reviewed the complete original TMR-1/010 report and source, TMR-5/007 proof and TMR-4/008 original source. The all-field Hamming-two case split withstands proof audit at its exact strict-grammar scope:

- At most two core sign edits do not cover all eight local masks.
- One bit of a core identifier always changes an even-parity core ID into a spare ID, with a consistent chosen Boolean value matching the replaced literal.
- Two core-ID edits and no sign edits are handled by all core variables zero and at most two spare variables zero. Two bits in ONE identifier can point to a different even-parity core ID, whose value is also zero. Two edits targeting the SAME spare ID both demand zero and do not conflict.
- At most two changed literal fields cannot falsify an originally all-positive ternary filler clause under these assignments. If one sign edit and one core-ID edit occur together, the core-sign-only witness is retained and the changed spare ID matches its predecessor value.

Every valid same-length two-field-bit mutant is SAT, and the explicit three-sign mutation remains UNSAT. This is favorable **independent mathematical review of TMR1-FR10 within the stated grammar**, not independent verification of a general SAT lower bound.

## 6. Actual executed evidence

Two independent programs were run in the current native container environment, not through a wrapper. No instruction-level multitape machine was run.

**Native Node.js v22.16.0, exact published JS and JSON by Git blob hash:** deterministic seed 0x61A9E23D; $r=1,2,3,4,6,8,12,16$; 2,260 structured complete sources including 1,635 SAT and 625 UNSAT, 1,400 independent full core assignment enumerations for $r\le4$, 52 three-sign UNSAT neighbors, 32 hostile canonical-template mutations that reject to fallback, 2,904,533 monotonically ordered modeled source-bit reads, zero failed assertions; maximum $L=4,004$. JS blob SHA **897deea5c24e63f0af346dfce6adc4b189052235**; raw blob SHA **6c09827486489390f15cf9af9170afc790dd985a**.

**Separately written native Python 3.13:** seed 771023, $r=1$ exhaustive 7,140 two-field-bit mutations, $r=2$ 2,988 sampled and $r=3$ 498 sampled; 8,626 valid proper full sources with explicit satisfying assignment witnesses and 2,000 invalid controls, zero failures. Its source and raw blob SHAs are **d0f177777590aea88726bd8df9e9ca3f7a3f35c9**, **8ff88f00ce0104c6056b4c75a8c286c0677fd925**. This reproduces the exact $r=1$ valid/invalid counts from TMR-1/010 but uses independent source construction, parser and brute force. Native Node and Python both use bounded fixture sizes, not physical Turing-machine instruction counts.

**Readback-verified publications:** experiments/tmr/tmr2_stream_mask010.cjs; results/raw/tmr/2026-11-13_2015_TMR2_STREAM_MASK010_RAW.json; experiments/tmr/tmr2_independent_crosscheck010.py; results/raw/tmr/2026-11-13_2015_TMR2_CROSSCHECK010_RAW.json.

## 7. Primary literature and scope

[1] Nisan, "CREW PRAMs and Decision Trees," SIAM J. Comput. 20(6), 999-1007 (1991), DOI https://doi.org/10.1137/0220062. Block sensitivity is meaningful for query/parallel access complexity but does not supply a superpolynomial unrestricted sequential SAT time lower bound.

[2] Buhrman and de Wolf, "Complexity Measures and Decision Tree Complexity: A Survey," Theor. Comput. Sci. 288(1), 21-43 (2002), DOI https://doi.org/10.1016/S0304-3975(01)00144-X. Decision-tree distinctions and physical computational processing have different cost models.

[3] Fortnow, Lipton, van Melkebeek and Viglas, "Time-Space Lower Bounds for Satisfiability," JACM 52(6), 835-865 (2005), DOI https://doi.org/10.1145/1101821.1101822. Its SAT exclusions require specified simultaneous small-space bounds; they do not exclude arbitrary polynomial-time, polynomial-space deterministic deciders.

## 8. Dependency and scope ledger

**Established restricted semantic equivalence:** the eight-mask per-block decision criterion under authenticated template syntax. **Candidate pending peer review:** the full finite multitape uniform compiler and the conservative $O(L\log^2 L)$ time, $O(\log L)$ work bound. **Computational:** both native bounded source audits. **OPEN:** any representation-independent post-acquisition processing lower bound valid for EVERY correct total uniform deterministic 3-SAT decider and excluding EVERY polynomial exponent. This work does not assume or prove P=NP or P!=NP.

**Corpus:** current 12:49 PST five-agent replacement directive, rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; full root proof1.txt (28,714 bytes, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and authentic proof2.txt blob (1,051,196 bytes, SHA 930c5eeddafce656717f28055a7a755f44737c); root main.tex authentic blob (2,504,241 bytes, SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064); AGENTS.md, CODEX.md, pnp skill, five current TMR handoffs, issue #3 through TMR-1/010, original TMR-1/010, TMR-5/007, TMR-4/008, TMR-2/009, TMR-3/008, historical LSPV-5/511 checker counterexample, and original primary literature. No mounted repository checkout, so repository preflight, full tests and LaTeX compile were not run. Earlier conflicting role ownership instructions remain superseded.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This restricted, readily decidable class supplies no new P=NP or P!=NP proof-tracker status. Root main.tex is TMR-5 synthesis owned and was not edited. No schedules or agents were created, revived or modified.

**ONE NEXT TARGET:** TMR-5 should independently realize/audit the finite multitape streaming authenticator and verify its all-length log-work bound, then attack the stronger claim that a compact representation cannot support a cheap decisive *global* processing invariant on arbitrary 3-CNF.

# CLOCKSPARSEINDEX41 | 2026-11-18 10:33 PST
**PROVED/EXACT restricted symbolic theorem, independent mathematical review OPEN; COMPUTATIONAL finite controls. P versus NP OPEN.**

## Named end-to-end dependency and falsifiers
Authentic $N=2^n$ source truth table -> source-independent ordered index schedule -> deterministic one-pass $K$-state transducer -> unpadded source/state-dependent output $y$ and terminal state $q$ -> exact two-sided Gap-MCSP image separation -> jointly fixed-PH circuit verification -> fully charged one-way-input/one-work-tape composition. **This run closes reachability acquisition only for a sparse-override dyadic-grammar schedule and shows that cheap indexed access alone does not imply SLP compression.** It does not supply a promise-pure quotient.

Pre-search falsifiers: (1) editing one occurrence of a shared grammar symbol inadvertently edits every occurrence; (2) state-dependent epsilon/variable-length output or different endpoint contexts break a globally consistent original-source witness; (3) low-circuit-complexity indexed schedules always have small SLPs; (4) acquired reachability or semantic sections automatically yield fixed-PH supplied-circuit equality or a CHMY-compatible physical machine. The first two survive correct occurrence-specific reconstruction, the third is **FALSIFIED** below, and the fourth is **OPEN**.

## 41.1 SPARSE-OVERRIDE-DYADIC-SECTION (restricted theorem)
Let a height-$n$ binary DAG grammar, all internal productions $X\to UV$ of equal-length children, generate a source-independent schedule of exactly $N=2^n$ transition-template labels. The grammar has $G$ nodes including terminals. At $d$ **fixed, source-independent** addresses, replace a label with an explicitly supplied template. Each template specifies for each $p\in[K]$ and genuine read bit $b\in\{0,1\}$ a next state and a finite binary emission (possibly epsilon). Read all original source bits $f_0,\ldots,f_{N-1}$ in order, concatenate output without timestamps, and retain terminal state.

A persistent path-copy construction represents the modified schedule by another balanced dyadic grammar of size
$
G'\le G+d(n+1).
$
For any attainable emitted string $y$ of length $m$ and terminal state $q$, a **uniform finite algorithm given the grammar, all explicit templates, $(y,q)$** computes exact output-conditioned reachability and constructs a Boolean circuit $C_{y,q}:\{0,1\}^n\to\{0,1\}$ whose full truth table $g$ satisfies the exact pair
$
(H_{\rm word}(g),H_{\rm state}(g))=$(y,q)$.
$
Writing $E=G'K^2(m+1)^2$, a conservative bounded-fan-in bound is
$
\boxed{CC(g)\le C n E\bigl(n+\log_2(E+2)+1\bigr).}
$
The offline exact dynamic program uses $O(G'K^3(m+1)^3)$ Boolean table operations, up to polynomial bit-cost factors for template descriptions, offsets, state IDs and emission comparisons. Storing the reachability bits and chosen splits takes $O(E\log(G'K(m+2)+2))$ bits, plus the explicitly charged grammar, output and template tables. This is NOT an online/one-tape complexity claim.

**Proof.** Updating one chosen occurrence of a shared dyadic grammar leaf copies at most its (n) ancestors and one leaf; other references remain unchanged. Apply the operation to all (d) fixed overrides. For every grammar node (X), states (p,r), offsets (0\le a\le b\le m), let (R_X(p,r,a,b)) assert existence of a genuine input word on that block taking (p) to (r) and emitting **exactly** substring (y[a:b]). At terminals, test both source bits against their actual explicitly supplied transition and emission. At (X\to UV), (R_X) is equivalent to
$
\bigvee_{t=0}^{K-1}\bigvee_{z=a}^{b}
R_U(p,t,a,z)\land R_V(t,r,z,b).
$
This is exact because unpadded output concatenates without deleting or permuting bits. Compute every table entry bottom-up, store the first feasible pair ($(t,z)$), and choose source bit 0 at a feasible terminal if possible, otherwise 1. Given requested original address (i), traverse the unique occurrence path from the root while updating the selected interface; repeated grammar nodes may legitimately be visited with different state/offset interfaces. Induction yields **one globally consistent source**. The stored table contains at most (E) entries, each with (O(\log(E+2))) addressable selection data. A hardwired table selector costs conservatively (O(E[n+\log(E+2)+1])) gates per one of $n$ address levels, giving the bound. All template descriptions and the construction cost must be paid by a uniform decoder. QED, subject to independent review.

**MCSP consequence.** Let $YES_s=\{f:CC(f)\le s\}), $NO_t=\{f:CC(f)>t\}), $s\le t$. If every original-source output has length at most $M$, and $s\ge Cn(G+d(n+1))K^2(M+1)^2[n+\log_2(E_{\max}+2)+1]), then (H(YES_s)=\operatorname{im}H). Every attained NO image collides with a YES image, so exact two-sided promise purity fails when NO is nonempty. For cofinal parameters (G_j+d_j(n+1)\le N^{a\lambda^j+o(1)}), (K_j\le N^{b\lambda^j+o(1)}), (M_j+1\le N^{c\lambda^j+o(1)}), and source threshold (s=N^\beta), a fixed (j) with ((a+2b+2c)\lambda^j<\beta) forces saturation, independent of any decoder clock. This is a scoped obstruction, NOT an unconditional lower bound.

## 41.2 POLY-INDEX/EXPONENTIAL-GRAMMAR CONTROL (explicit nonuniform family)
For each $n\ge2$, choose a primitive length-$n$ binary LFSR. Let $a_i$ be its output bit at time $i$ for $0\le i<2^n=N$, using the period-((N-1)) sequence and one repeated bit. Each consecutive $n$-bit window starting at a position $0\le i\le N-n$ is distinct, since it is exactly an LFSR state, and those starting positions lie within one primitive cycle.

Any **binary** SLP with $G$ concatenation rules can introduce at most $n-1$ new length-$n$ factors per rule: assign each factor occurrence to its lowest concatenation node, where it crosses the rule boundary. Hence its number of distinct length-$n$ factors is at most (G$n-1$). Therefore the schedule $a_0\ldots a_{N-1}$ requires
$
\boxed{G\ge (2^n-n+1)/$n-1$=\Omega(N/n).}
$
Nevertheless, each indexed bit $a_i$ has a **nonuniform** $O(n^3)$-gate circuit: the primitive feedback matrix and its squared powers are hardwired, then at most (n) matrix-vector applications compute (A^i v_0). Existence of a uniformly constructible primitive polynomial in deterministic poly(n) time is NOT assumed.

For a concrete two-state source-authentic streaming quotient with **no emitted bits**, set
$
q_{i+1}=q_i\oplus f_i\oplus a_i,\quad q_0=0.
$
Every nonempty interval has trivial unforced endpoint reachability (either endpoint is possible), and both terminal labels have explicit (O(n^3+n))-circuit source preimages: use $f=a$, or flip one fixed bit. Thus exponentially large SLP complexity **does not** imply large indexed transition complexity, hard reachability, hard fibers, or MCSP purity. This falsifies the attempted implication “efficient indexed schedule -> efficiently compressed grammar” without proving an unrestricted lower bound.

## Hostile executed controls and provenance
The locally executed standard-library CPython 3.13.5 audit, seed 20261118103341, examined **40** grammar/transducer models, **5,184** authentic source words (all 4/8-bit words per model; 16-bit samples), **202** distinct selected attainable short-output fibers, **1,180** canonical witness bits, **1,818** independently brute-checked interval relations, and **40** occurrence-specific grammar-edit checks. Each selected fiber had $m\le6$; all source words of length 16 were sampled, not exhausted. **Zero final failures.** A separately coded bottom-up full-word lex-witness reproducer checked **all 256** eight-bit input strings and **all 179** attainable output/state fibers of an explicitly edited, state-dependent, variable-length output machine, **435** source/fiber comparisons, zero failures. LFSR primitive periods, full (n)-factor diversity and fast index evaluation were checked for $n=2,\ldots,10$ (2,044 indexed positions), zero failures. These tests do not measure minimum circuit size or prove asymptotics.

Full audit code SHA256 **9b1bf53bbfb5b84c14965bf3885b1c60b03730105f8bdb45748e63fc9f049252**, raw JSON SHA256 **e4ba264acdc9f965025737b96892877904eda8fa0b51c02dff9f0e51549bee45**. Independent script SHA256 **4d7ca0b647171be6732a33d4ebe49ea3aeb1234a857f2ffb0e945d370157ebf4**, independent output SHA256 **99d78bef2024b38555bbaeaf6ff6d25514b7c28984638a3fe0652a535b727122**. The initial local script had a test-fixture grammar with unequal child lengths; corrected before successful tests, and no earlier failed run is counted as passing.

**Hostile guards:** A source-dependent override list is not source-independent schedule advice and is excluded. A long identity-copy output has (m=N), so the circuit-section bound is not inexpensive. A hardwired arbitrary-index equality checker may require (d=\Theta(N)) relative to a compact baseline. The LFSR schedule falsifies any transfer from small indexed circuits to small SLPs, even with easy reachability. Fixed-PH target recognition does NOT imply fixed-PH supplied-circuit equality or interval reachability. The exact DP obtains R given the *explicit* grammar, not from a compact arbitrary index circuit.

## Ledger and four gates
The grammar transformation charges index addresses, all (d) altered paths, table/template descriptions, comparisons, $O(G'K^3(m+1)^3)$ DP work, (O(E\log E)) retained bits, lookup construction, and every circuit output bit. The physical original-source compiler additionally owes full input parsing, all (N) source reads, transition/template generation, source-dependent seeds or provenance if introduced, one-way head movement, output tape representation, one-work-tape movement, failures/switching and same-run time/space. These are NOT proven by the circuit existence theorem.

DISJ **NOT APPLICABLE** (no disjointness-rank argument). Relativization **RESTRICTED/OPEN** (combinatorial section only). Simultaneous DTISP **FAIL/OPEN** for unrestricted P-vs-NP transfer, due to absent promise purity and physical machine composition. Deterministic configurations **PASS as upper-bound sanity only**. Natural Proofs/algebrization not bypassed; Partial-MCSP interpolation, seed/free-escape, affine/field, Chevalley-Warning, histogram, adaptive transcript, supplied parity, symbolic sections, binary portfolios and low-degree/mixed-core obstructions all remain. /341 full UNSAT authority FAIL; /386 RESTRICTED.

Repo evidence reviewed: current 2026-11-15 END_TO_END directive, AGENTS.md, CODEX.md, pnp-research skill; SOURCEQUERY_SYNTHESIS10, PUBLICSEED_PLOTKIN14, CLOCKSAT1, full CLOCKSLPOUT39 and CLOCKINDEXOUTPUT40, CLOCKREACHCIRCUIT33, CLOCKMASKEDINVERSE22 and CLOCKWITNESSPH23, latest clock-gate handoff and current commits; older named project IDs surveyed by code search. No local checkout, so repo preflight was not run. Clock Gate does not own the five TMR root manuscripts; none were altered, and no schedules changed.

**ONE NEXT: GENERAL-INDEX-REACHABILITY42.** Find a uniformly accessible general-index family whose exact source-bit-conditioned output reachability is not accounted for by a compact grammar/sparse edit, a cheap baseline gauge or easy affine structure, and test whether any actual source-NO image is universally excluded. Require joint fixed-PH supplied-circuit verification and fully charged one-way-input/one-work-tape composition before any P-vs-NP transfer.

### Primary sources
[1] Ganardi, Jeż, Lohrey, *Balancing Straight-Line Programs* (FOCS 2019), https://arxiv.org/abs/1902.03568 ; [2] Ganardi, *Compression by Contracting Straight-Line Programs* (ESA 2021), https://doi.org/10.4230/LIPIcs.ESA.2021.45 ; [3] Golomb, *Shift Register Sequences*, 3rd ed., 2017; primitive LFSR exposition https://debruijnsequence.org/db/lfsr ; [4] Mohri, *Finite-State Transducers* (1997), https://aclanthology.org/J97-2003/ ; [5] Cheraghchi et al., *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP* (STACS 2021), https://doi.org/10.4230/LIPIcs.STACS.2021.23 .

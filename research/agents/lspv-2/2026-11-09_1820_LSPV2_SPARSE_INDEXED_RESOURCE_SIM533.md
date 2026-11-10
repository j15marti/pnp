# LSPV-2/533: Sparse indexed-tape simulation and FLMV exponent firewall

**2026-11-09 18:20 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate, falsifiers, primary literature and corpus

**Candidate:** Build an exact sparse operational encoding of an indexed-work-tape micro-machine, proving a concrete/abstract transition correspondence with charged simulation overhead, and test whether a time-derived upper work-space exponent actually crosses the deterministic FLMV threshold.

Four falsifiers: (F1) indexed native space measures live/nonblank cells rather than the largest indexed work position; (F2) zero overwrites, blank reads, index erasure and local moves break sparse replay; (F3) dictionary lookup/shifting is silently free; (F4) an upper bound $S=O(T)$ is wrongly treated as $S=O(N^{1/2})$. Original FLMV §2.1 defeats F1, independently replayed controls defeat F2, the proved worst-case $O(E^3)$ simulator charges F3, and the strict exponent comparison defeats F4.

**Primary source:** Fortnow, Lipton, van Melkebeek and Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6) (2005), §2.1, Theorem 5.7 and Corollary 5.8, https://lance.fortnow.com/papers/files/tst.pdf . The authors already state that native high-water can be exponential in time and that suitable sparse storage can bound space by time with only polylogarithmic runtime overhead. Their result is stronger than the restricted construction below and must not be reported as a new all-machine theorem. Bennett's 1989 reversible-computation pebbling bounds are a distinct model-sensitive recomputation control.

Governing 2026-11-09 16:24 PST handoff, prior abstract-negative handoff, AGENTS.md, CODEX.md, project skill, both root trackers and issue #3 read. Relevant LSPV-2/532, LSPV-1/549, LSPV-5/472, original MODELBRIDGE-0010, Grok and Claude reports reviewed. Source actual files checked: konard/p-vs-np scripts/proof_status.json (SHA 93b77ed3...), blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea...), openai/math README.md (cc5b0a03...), berkeley-abc/abc README.md (88a9d1a3...). None provides the missing all-SAT-solver compression. MODELBRIDGE-0010's unrestricted fixed-exponent normalizer remains FALSIFIED/RETIRED.

## Exact declared machine class and transition theorem

One read-only binary source; one indexed writable bit tape with blank zero; a binary index tape; work head initially at position zero, all work/index tapes initially blank; fixed finite control. Eight legal micro-commands: i0 and i1 (append address bits), jump (move to binary index and erase index), read, w0 and w1, left clamped at origin, right. Each declared micro-operation costs one **native** transition. The native space measure is maximal indexed work position plus one; input/output tapes are excluded under the original model. Complete configurations include exact source/code, control, index content/head, work head, all work cells, parser/output/read status, cumulative native steps, indexed high-water, and all-phase peak space. If nondeterministic choices are introduced, their existential branch semantics remain explicit and do not become deterministic UNSAT.

Let $\iota(\sigma)$ encode the work tape by a finite list of positions with value 1; omitted cells represent zero. Preserve index, head, control, exact source, trace and counters. For sets $X$ of concrete configurations let $\alpha(X)=\{\iota(\sigma):\sigma\in X\}$ and $\gamma(Y)=\{\sigma:\iota(\sigma)\in Y\}$. All eight commands satisfy, by separate case analysis,

$$
\iota(\operatorname{Post}(\sigma))=\operatorname{Post}_{sp}(\iota(\sigma)).
$$

Consequently the exact collecting simulator preserves all behaviors of the **declared micro-class**; any coarser may abstraction must satisfy $\operatorname{Post}(\gamma(a))\subseteq\gamma(\operatorname{Post}^{\#}(a))$. When proving negative resource reachability, projected *lower* path cost cannot exceed concrete cost; for an upper machine-resource certificate, all native phases, work, index and output must be bounded from above. Abstract-state cardinality is not a work-space lower bound.

**Proved restricted upper simulation:** In any length-$E$ micro-execution, a generated work-head address has at most $E+2$ bits, and at most $E$ work positions are nonblank. Serialization as contiguous address/value records takes $O(E^2)$ bit cells, including address/index control and delimiters. A conservative list scan, record shift or new record construction takes at most $O(E^2)$ bit operations per native step, so simulation has $O(E^3)$ time and $O(E^2)$ **simulator** native high-water. The proof is induction on the eight operations and the number/width of modified records. This bound is weaker than FLMV's known sparse normalization, is not a full FLMV machine interpreter, and does not convert arbitrary SAT algorithms.

## Independent, source-authenticated controls

The finite strict signed 3-CNF byte grammar has magic S3C, one-byte variable/clause counts and three distinct nonzero signed literals per clause. Nine original sources: odd-charge K4 Tseitin UNSAT, even-charge K4 Tseitin SAT, single-clause SAT, all-eight-clause UNSAT, empty-clause-list SAT and four malformed controls (wrong magic, truncation, duplicated variables, zero literal). The finite SAT truth labels were computed by exhaustive Boolean enumeration, not by a hypothetical polynomial-time algorithm.

Python independently checked a dense-array work-tape reference against the sparse encoding for all $1+8+8^2+8^3+8^4=4681$ micro-programs of length at most four, plus nine far-index programs; **32,857** recorded checks passed. Independently implemented local Node.js: **9,389** checks; original source SHA-256 fingerprints agreed for all **9/9** inputs. A compact verifier published to GitHub was read back and independently run in V8: **18,751 semantic checks** passed with typed-array/crypto shims. Its SHA-256 was stubbed in this V8 run; the independent local Python and Node implementations both used real SHA-256.

For the 53-byte odd/even K4 signed sources, $N=424$ binary input bits. The program writes an index for $2^{424}$, jumps, writes 1, reads 1, overwrites zero and reads 0. The native high-water is $2^{424}+1$, while the conservatively encoded sparse-layout count is **4,285 bits** during **430** micro-steps; the separately charged list-search proxy is **3,850** units. This is a symbolic position versus a bit-size encoding, not actually allocated memory. Any source-guest execution, preprocessing, retrieval, output and recomputation must be separately charged in the unrestricted Route A hypothesis; finite brute-force labels are test controls only.

Reproducer: experiments/arc/lspv2_533_sparse_index_compact.mjs. Ledger: results/raw/arc/2026-11-09_1820_LSPV2_533_SPARSE_INDEXED_RAW.json. The complete independently implemented Python and Node suites and raw outputs are available in the conversation reproducibility archive.

## Exact FLMV space-exponent barrier

Let hypothetical $A_P$ be a **fixed uniform total correct deterministic** SAT decider on all binary strings, with unknown fixed exponent $c$: $T_P(N)=O(N^c\operatorname{polylog}N)$. Even the original paper's stronger native sparse normalization gives only a space upper $S'=O(T_P\operatorname{polylog}T_P)$ and thus upper exponent $s'\le c$, **not** $s'\le1/2$. The explicit restricted $O(E^2)$ simulator is weaker. For $c>1$, the applicable published positive deterministic $k$-level space exponents obey $d_k(c)<1<c$. Thus the upper $s'\le c$ alone is insufficient to reach $s'<d_k(c)$.

The historical $k=2$ threshold is

$$
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right),\qquad
\beta(6/5)=23/45,\qquad
6/5-23/45=31/45,\quad 23/45-1/2=1/90.
$$

The exponent-only ratios $N^{1/90}$ for $N=10^6,10^{12},10^{24},10^{60}$ are 1.16591, 1.35936, 1.84785, 4.64159; $N^{31/45}$ are about $1.3594\cdot10^4$, $1.8479\cdot10^8$, $3.4145\cdot10^{16}$, $2.1544\cdot10^{41}$. They are **not bytes or measured space**, and constants, polylogs and asymptotic quantifiers prohibit finite-size contradiction claims. The $k=2$ formula becomes nonpositive past $c\simeq1.52138$; higher 2005 levels extend to $c<\phi$, with still-distinct later tradeoffs. Neither SAT in P nor an NP verifier grants $c=6/5$, low space, or deterministic UNSAT.

## Tracking and next implication

Scope: PROVED/RESTRICTED exact micro-simulation, COMPUTATIONAL finite controls; original stronger FLMV sparse theorem KNOWN; unrestricted transfer OPEN. [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-D1], [P2-C3], [P2-B1], [P2-B2], B3 and $P\ne NP$ remain OPEN. No changes to historical R_mix341 rule grammar/weights or five-role titles, identities, task schedules, time zones, enabled states and 2 Route A / 3 Route B labels.

The all-input recursively iterable same-machine transformation with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ remains **OPEN**. Next work: a genuinely solver-intensional, fully charged simultaneous reduction in **both** exponents or an explicit counterexample to a precisely specified proposed transformation. **P versus NP remains OPEN.**

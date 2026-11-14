# TMR-5/010: independent balanced-mask certificate review and exact six-query structure

**Pacific date:** November 13, 2026, 22:55 PST (America/Los_Angeles). **Role:** TMR-5, Machine Bottleneck Redteam / whole-document synthesis. **Repository:** `j15marti/pnp`, `main`.

**Verdict:** TMR-2/012's Hall-matching **five-or-six minimum promise sign-bit certificate theorem is independently supported at PROVED/RESTRICTED mathematical scope** for the original authenticated eight-row mask grammar. New TMR5-SIX10, an exact characterization and count of *all size-six* SAT certificates of **every balanced SAT block**, is **CANDIDATE pending TMR-2 or TMR-1 independent review**. Tests are COMPUTATIONAL. An unrestricted superpolynomial 3-SAT time bound and P versus NP are OPEN.

## 1. Exact scope, original dependencies, and labels

Use the **original** full binary strict proper 3-CNF grammar of TMR-2/010 and /012: unary `N,M` header, canonical positive spare-ID filler clauses, distinct IDs within each clause, all declared IDs occurring, `r` independent blocks of exactly eight clauses on three disjoint core variables each, fixed literal and clause ordering, and 24 freely chosen ORIGINAL polarity bits per block. Other binary fields are held fixed in the promised family `G_r`. Block `a=(a_0,...,a_7)`, with each `a_i` a three-bit mask, is UNSAT precisely when its eight masks are all distinct, thus are a permutation of `0,...,7`. A product is SAT iff **every** block is SAT. This is a property of authenticated formulas, not arbitrary 3-CNF.

The exact source length is

$$
w=\lceil\log_2(6r+2)\rceil,\quad N=2^w-1,\quad
K=\lceil(N-3r)/3\rceil,\quad
M=8r+K,\quad
L=N+M+2+3M(w+1)=\Theta(r\log r).
$$

A *promise sign-bit SAT certificate* is a set of observed original polarity positions for which **every** completion inside `G_r` remains SAT. It is not an ordinary proof certificate, compulsory stored solver memory, or cost of deciding arbitrary SAT.

For one block, let `f_m` be the multiplicity of full mask `m`. For each unordered pair `J\subset\{0,1,2\}` of coordinate indices and bit pair `v\in\{0,1\}^2`, let `f_{J,v}` count rows whose projection onto `J` equals `v`.

## 2. New exact theorem candidate TMR5-SIX10

**Theorem (CANDIDATE pending second peer review).** Suppose `a` is SAT and *balanced*: on each of its three polarity coordinates, precisely four of the eight rows carry bit zero and four carry bit one. A set of **exactly six** observed row-coordinate positions is a SAT certificate iff it has **one of two forms**:

1. **Repeated full mask:** all three coordinates of each of two distinct rows whose complete masks are identical.
2. **Triple repeated projection:** the same two coordinates `J` of each of three distinct rows whose mask projections onto `J` are identical.

Consequently, the exact number `N_6(a)` of six-bit SAT certificates is

$$
\boxed{N_6(a)
=\sum_{m=0}^{7}\binom{f_m}{2}
 +\sum_{\substack{J\subseteq\{0,1,2\}\\|J|=2}}
  \sum_{v\in\{0,1\}^2}\binom{f_{J,v}}{3}.}
$$

This extends TMR-2/012's *minimum size* 6 to an exact description of *every minimum certificate*, and avoids the incorrect stronger inference that every minimum certificate must consist of two fully specified duplicate masks.

**Proof.** Given a query set `Q`, for each row `i` let `D_i\subseteq\{0,...,7\}` be the subcube of masks compatible with its observed bits. A completion to an UNSAT block is a system of distinct representatives for all eight `D_i`, so Hall's marriage theorem says that `Q` forces SAT iff some set `R` of `s` rows has union of domains of size less than `s`.

At most six queried positions, every row with 0,1,2,3 queried positions has domain size 8,4,2,1 respectively. For `s=1`, a domain is nonempty. For `s=2`, a Hall violation requires two singleton domains, consuming three queries in each row and forcing the same full mask (type 1). For `s=3`, a Hall violation requires three domains of size at most two, consuming two queries in each row, and the union has size at most two only when these domains are the *same* binary-cube edge. This is exactly type 2. For `s=4`, at least one of the four selected rows has at most one queried coordinate, whose four-mask domain already makes the union size at least four. For `s=5`, any unqueried row gives union size eight. Otherwise the allocation is one doubly queried row and four singly queried rows. A union of size at most four would require all four one-bit halfcubes to coincide and the two-bit domain to lie within that same halfcube, implying five actual rows with the same coordinate/value. This contradicts the 4/4 balance. For `s=6`, if a selected row is unqueried its domain has size eight. Otherwise six singly queried rows occur, and union size below six again requires a shared four-mask halfcube and hence six rows with the same coordinate/value, contradicting balance. For `s=7,8`, at least one selected row is unqueried and supplies all eight masks. No further Hall failures are possible.

Both displayed forms are sufficient: two singleton domains with the same mask cannot receive distinct representatives; three identical two-mask domains cannot receive three. The forms are disjoint since they use respectively two or three distinct rows. Different row choices and coordinate choices give distinct query-position sets. Counting them yields the formula. QED at the explicitly stated eight-row template level.

**Independent review of TMR-2/012:** The same Hall argument with five queries leaves only a five-row, one-bit-each Hall failure. All five one-bit domains must be identical four-mask halfcubes. Thus five queries force SAT iff some coordinate/value occurs in at least five rows; if all coordinates are balanced, every SAT block has duplicate full masks, providing six queries, and cannot have any certificate with at most five. Independent SAT products add their minimum sign-certificate sizes, while one UNSAT block's entire 24-sign pattern suffices and all 24 positions are sensitive. This independently establishes TMR-2/012's **5-versus-6 and 24** assertions **only** in the promised sign-field class. It does not certify the stated physical asymptotic upper-bound exponent for the full parser/recognizer of TMR-2/010.

## 3. Hostile minimal examples

The TMR-2/012 balanced tuple `(0,0,3,3,5,5,6,6)` has four duplicate pairs and no repeated two-coordinate projection on three rows. The formula gives `N_6=4`, matching its previous enumerator.

A separate balanced tuple `(0,0,1,1,6,6,7,7)` has four full-mask duplicate pairs **and** two three-or-more-row projections: for `J={0,1}`, the four rows with projection 00 and the four with projection 11 give `2*binom(4,3)=8` triple certificates. Therefore `N_6=4+8=12`. It is an explicit counterexample to the plausible but stronger claim `all minimal six-query certificates are duplicate full-mask pairs`.

The balanced tuple `(0,0,0,0,7,7,7,7)` yields twelve repeated-mask pairs and 24 projection triples, so `N_6=36`. The old unbalanced SAT tuple `(1,2,3,4,5,6,7,7)` has three five-bit SAT certificates and 61 six-bit SAT certificates: **the new six-certificate formula deliberately does not apply without balance**. The UNSAT permutation `(0,1,2,3,4,5,6,7)` has no SAT certificate of at most six bits.

These are valid original mask assignments in `G_1`; outside the promise class, input edits, alternate encodings, arbitrary auxiliary clauses and all general SAT algorithm strategies remain available.

## 4. Native independent verification, model and corpus

**Native CPython, independently authored, not peer-code wrappers.** A standalone augmenting-path bipartite matcher checked every one of the

$$
\sum_{k=0}^{6}\binom{24}{k}=190051
$$

query-position sets for **each of the five fixtures** above, totaling **950,255 queried subsets**, using full matching feasibility rather than assuming the new two-form characterization. Its counts for certificate sizes `k=0,...,6` were respectively:
- even-double: `0,0,0,0,0,0,4`;
- pair-projection-triple: `0,0,0,0,0,0,12`;
- two-quadruples: `0,0,0,0,0,0,36`;
- old-unbalanced SAT: `0,0,0,0,0,3,61`;
- UNSAT permutation: `0,0,0,0,0,0,0`.

Each matcher batch completed in 1.2 to 1.5 seconds and raised zero failures. A **separate** structural-counting sweep exhaustively generated all `binom(8,4)^3=343000` ordered row tuples whose three columns balance four/four. Exactly 40,320 are UNSAT permutations and 302,680 are SAT. For the SAT cases, the predicted six-certificate multiplicity distribution is:

| `N_6` | Ordered balanced SAT tuples |
|---:|---:|
| 4 | 126,000 |
| 6 | 120,960 |
| 10 | 26,880 |
| 12 | 15,120 |
| 18 | 13,440 |
| 36 | 280 |

This finite sweep verifies **structural-count arithmetic**, not 343,000 independently rerun Hall matchers. Its 4-to-36 range is COMPUTATIONAL evidence, not a separately proved global extremal theorem. The executable's internal sweep was 4.98 seconds. No physical 3-SAT Turing machine was run. All physical time/space effects retain their own restricted model status.

Published exact scripts:
- `experiments/tmr/tmr5_balanced_certificate013.py` (Git blob `6dc492cf2b4f82eb5dbf4706cb09cf7f3e25aef1`, identical to native executed source).
- `experiments/tmr/tmr5_balanced_sweep013.py` (Git blob `1e040a876abb85a347a62de069fd51d9b83a7f38`, identical to native executed source).
- `results/raw/tmr/2026-11-13_2255_TMR5_BALANCED_C6_013_RAW.json` (published case counts, distribution and commands; a fuller per-k local original remains `/mnt/data/2026-11-13_2255_TMR5_BALANCED_C6_013_RAW.json`).

This run read FIRST the superseding TMR replacement directive; independently recovered the complete authoritative `proof1.txt` (28,714 chars; SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), `proof2.txt` via its **authentic full 1,051,196-character Git blob** (SHA `930c5eeddafce656717f28055a7a9a755f44737c`), and canonical `main.tex` via its complete 2,511,782-character Git blob (SHA `c04a02a97492f88938791f363ff91d99b67cd78b` before this run). Also inspected the latest issue #3 comments through TMR-4/013, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, all five current TMR handoffs, original TMR-2/010 and /012, TMR-1/012, TMR-3/010,/011 and TMR-4/013 and historical source-model caveats. Older LSPV role priorities are superseded, not historical proof evidence.

Primary source and exact use: P. Hall, *On Representatives of Subsets*, *Journal of the London Mathematical Society* 10 (1935), 26-30, https://doi.org/10.1112/jlms/s1-10.37.26, used only for Hall's matching criterion; Buhrman and de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, *Theoretical Computer Science* 288 (2002), 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X, for query/certificate model context; Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, *JACM* 52 (2005), 835-865, https://doi.org/10.1145/1101821.1101822, **small-space and random-access** model context, not an unrestricted all-polynomial lower bound.

## 5. Dependency synthesis and exact gap

**PROVED/RESTRICTED, independently reviewed here:** The eight-mask SAT/UNSAT equivalence and TMR-2/012 five-or-six sign-certificate characterization, including `C_G(B_r)=6r` and `C_G(U)=24` for an UNSAT product, under the fixed template and original sign-query interface. Deterministic unread-input replay turns `6r` distinct demanded observations into `T_A(B_r)\ge\lceil6r/h\rceil=\Omega(L/\log L)` for each fixed total correct `h`-source-observation-per-step machine, without bounding writable memory or imposing one-pass access. This is not an exponential memory requirement.

**CANDIDATE, new TMR-5 claim:** the exact two-form classification and count of all six-bit certificates on every balanced SAT block, awaiting independent TMR-2 or TMR-1 proof review. The alternative triple-projection certificates forbid overclaiming duplicate-pair uniqueness.

**Other peer claims (strict statuses):** TMR-1/012's multihead-to-one-head copy bridge and TMR-4/013's COPY/REWIND/RUN all-transition potential transfer have mathematical support in their precise physically local models, but cannot preserve a small-space premise and cannot manufacture an unproved superpolynomial prepared-state potential. At the prepared state the source-observation potential is zero. TMR-3/010's exponential-moment Kraft inequality is PROVED/EXACT as a prefix-code fact. TMR-3/011's full physical crossing-splice/serialization premise remains CANDIDATE/RESTRICTED pending independent audit; even if proved, its same-machine time-space product has at most polynomial strength and does not exclude a quadratic-time solver with polynomial workspace. The exhaustive fallback prose defect for recognized UNSAT equality sources has an explicit repair, and it is not a general SAT algorithm.

**OPEN, still load-bearing:** Construct a noncircular, all-edge cost-sound *processing* potential for arbitrary total uniform deterministic deciders after complete input acquisition and all freely chosen compact representations, with an actual superpolynomial initial-value theorem; or exhibit one fully proved general polynomial-time SAT algorithm. No such arrow is established. The quantifiers remain for every fixed correct A, every `k>=1,C>0,L0`, some valid F of length at least L0 satisfying `T_A(F)>C(L+1)^k`. No advice, per-length lookup, free oracle or ETH/SETH assumption is introduced.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** the new restricted exact certificate classification changes neither root `proof1.txt` nor `proof2.txt` all-input proof obligations; both remain untouched. Canonical `main.tex` is to receive a TMR-5-owned status-preserving synthesis insertion only. No schedules or agents were created, revived or modified. No native repository clone/preflight or LaTeX compiler run (container network DNS blocked), and no automated project-wide test suite run.

**One next target:** have TMR-2 verify the two-form six-certificate classification; TMR-5 then independently audit TMR-3/011's physical crossing-code prefix-free serialization under read-only input copying, but prioritize a full prepared-state computational-process necessity that survives the authenticated polynomial mask-table classifier and arbitrary polynomial writable storage.

END_OF_REPORT::TMR5::BALANCED_CERTIFICATE_PEER_REVIEW010::2026-11-13_2255_PST

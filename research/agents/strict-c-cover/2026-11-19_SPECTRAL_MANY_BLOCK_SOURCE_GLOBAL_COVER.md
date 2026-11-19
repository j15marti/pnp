# Original strict-C: spectral many-block universal obstruction covers
Date 2026-11-19. Research role: independent obstruction-cover discovery. **P versus NP remains OPEN.**

## Proven source-uniform theorem

Use original strict T5: `R(a,b)` iff `(b-a) mod 5 in {1,3}`, and `C(x,y,z)` iff the three values form a directed cycle (either orientation). Exactly 30/125 triples satisfy C, and `exists h C(h,u,v) iff u != v`. Each physical clause has three distinct variable names, and every projected edge has its own globally private head.

Let a projectable original-C source have a simple, d-regular projected graph `G` on n shared vertices with adjacency matrix A. If integer t satisfies `1 <= t < d/4` and `A+t I` is positive semidefinite, then for every shared assignment z into Z5, the number M(z) of monochromatic original source edges is at least

```
a = floor(n/5); r = n mod 5
S5 = (5-r)*a*a + r*(a+1)*(a+1)
M(z) >= ceil( ((d+t)*S5-t*n*n) / (2*n) ).
```

**Proof:** Write each color-class indicator v_c as `(size_c/n) 1 + w_c` with `w_c perpendicular to 1`. Because `A 1=d 1` and `A+tI >=0`, `v_c^T A v_c >= (d+t)*size_c^2/n-t*size_c`. Sum over five colors, use `sum size_c^2 >= S5`, and observe `sum v_c^T A v_c=2 M(z)`. A monochromatic projected edge `uv` has `C(h,u,v)=false` for **all five h**, so choosing the first monochromatic physical clause is an actual deterministic, source-verifiable refutable-block selector for **every z**. If blocks hold at most s private heads, at least `ceil(Mmin/s)` distinct blocks are refutable for every z. This is a **global symbolic cover**, not a row sample or a list of block indices assuming its own completeness.

**Deterministic one-sided specialist:** On arbitrary source triples, find candidate private heads by source occurrence counts, verify simple projection and regularity, then enumerate every `t=1..floor((d-1)/4)`. Compute exact positive definiteness of `A+tI` using fraction-free Bareiss elimination and Sylvester leading-principal-minor signs. Return an UNSAT source-checkable certificate on the first success; otherwise UNKNOWN. This is sound on every input, without polarity advice, supplied successful branches, oracles or unverified virtual inputs. It is incomplete. The executed generic code requires `O(d*n^3)` big-integer operations after parsing and `O(n^2+m)` writable matrix/graph entries plus polynomial bit widths, with all failed t attempts and verification charged. It does **not** meet the proposed time `N^1.33` or writable space `N^0.5`.

**Source-only strongly regular shortcut:** If the projected graph has degree d, exactly lambda common neighbors for adjacent vertex pairs and mu for nonadjacent pairs, and `lambda=mu-1`, then `A^2+A=(d-mu)I+mu J`. A source-checked integer proof establishes `A+tI>0` if `(2t-1)^2 > 1+4(d-mu)`, `2t-1>0`, and `d>4t`. No family labels are used. A theoretical source-rescanning implementation can perform these tests in `O(log L)` writable bits and generous polynomial time on read-only canonical input of L bits; the logspace variant was not benchmarked. The fast executed version materializes graph indices.

## Materialized finite control: Paley(109)

An original strict-C source with **2,943 physical C clauses**, **109 shared variables** and **2,943 distinct private heads** has `N=3,052` used variable names. Deterministic seed 2026111904 shuffled every variable label, clause order and clause argument order. From the actual source, independent checkers recovered

```
d=54, lambda=26, mu=27, t=6
A^2+A = 27I + 27J
(2A+I)^2 = 109I + 108J
(2t-1)^2 =121 >109, d=54 > 4t=24.
S5(109)=2377; M(z)>=ceil(71334/218)=328 for EVERY z.
```

With private block size `s=floor(3052^0.35)=16`, the 2,943 physical heads form `B=184 <=3052^0.65=184.0687` blocks. **Every** one of `5^109` shared assignments has at least **21 distinct refutable blocks**. The certificate has one symbolic proof root; it is NOT one literal shared-assignment row under an explicit-row semantics. Physical incidence girth=6, not growing; **deleting any 327 original clauses still leaves UNSAT**, so the source is not clause-critical.

Independent set-based audits validated all **11,881** ordered matrix entries, **109 positive** exact Bareiss leading principal minors, and **735,750** original-C head evaluations across 50 deterministic z samples. The sample minima were 556 monochromatic edges and 174 distinct refutable blocks; sample testing supports execution, while the matrix identity supplies the universal proof. Full SAT original-C witnesses for K5 and K6-minus-one-edge were independently checked; a native nonprojectable UNSAT 3-C source correctly returned UNKNOWN. Entire Python interpreter + JSON IO + checker timings in this session: 1.48 s / 97,548 KiB peak RSS (generic exact) and 1.16 s / 98,204 KiB RSS (shortcut). These measurements are not machine-independent complexity bounds.

## Growing-girth counterexample class, using published LPS graph results

The nonbipartite Lubotzky-Phillips-Sarnak Ramanujan construction for `p=101` and suitable infinitely many large primes `q congruent 1 mod 404` supplies 102-regular simple graphs, `n=q(q^2-1)/2`, nontrivial eigenvalues bounded by `2 sqrt(101)<21`, and projected graph girth `Omega(log n)` (for the nonbipartite case use the ~2/3 log-base-p constant, not the bipartite ~4/3 constant). Project every edge by a fresh-head ORIGINAL C clause. The physical incidence girth is twice the graph girth, `m=51n`, `N=52n`, and the generic source-uniform exact positive-definiteness specialist is guaranteed to accept with `t=21`: all z have at least `n*(102-4*21)/10 = 1.8n` monochromatic physical C clauses. Grouping heads in `floor(N^0.35)`-sized disjoint blocks meets `B<=N^0.65` asymptotically and gives Omega(N^0.65) refutable blocks for each z. This conclusion uses established LPS graph theorems, not materialized LPS fixtures in this run. This family is massively redundant rather than clause-critical. **Growing incidence girth alone does not imply expensive source-uniform global cover discovery**.

## Explicit firewall and next problem

Neither the finite source nor the published high-girth family is clause-minimal UNSAT, and the proof format does not meet explicit-assignment row semantics or the proposed N^1.33/N^0.5 resources. No unrestricted SAT reduction or P-vs-NP lower bound follows. Next: find a source-uniform global selector proof retained after making strict-C sources **simultaneously clause-critical and growing-incidence-girth**, with complete bit-level acquisition, failed attempts, replay and live writable-space accounting.

Full executable Python, original physical C source, SAT controls, two independent verifiers, 50 selector samples, results and SHA-256 manifest: conversation archive `T5C_Spectral_ManyBlock_Global_Cover_20261119.zip`.

Sources consulted: (1) Lubotzky, Phillips, Sarnak, *Ramanujan Graphs*, Combinatorica 8 (1988), https://doi.org/10.1007/BF02126799 ; (2) nonbipartite LPS exposition https://math.berkeley.edu/~zstier/LPSRamanujanGraphs.pdf ; (3) prior repository work `research/agents/strict-c-cover/2026-11-19_K4_SOURCE_UNIFORM_GRID_MINOR_COVER.md` ; (4) user's `t5_strict_research.pdf` retrieved via file search, confirming strict-C private-head projection. Historical H9/H33 R-only sources were not substituted for C.

**P versus NP is OPEN.**

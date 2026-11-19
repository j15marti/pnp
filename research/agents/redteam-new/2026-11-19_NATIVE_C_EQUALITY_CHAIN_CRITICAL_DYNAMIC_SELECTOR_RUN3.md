# Independent strict-T5 red team: native equality chains, criticality, and symbolic all-z selector
2026-11-19. Status **PROVED** (explicit family, sound source-indexed certificate), **COMPUTATIONALLY VERIFIED** (complete finite independent tests), **CONDITIONAL** (one *symbolic* row semantics), **OPEN** (general SAT/UNSAT lower bound). P vs NP remains open.

## Reused established equality primitive, not a new gadget
The user's `t5_strict_research.pdf`, page 4, already proves the four-original-C primitive-positive definition
[
E(x,y;p,q,a,b)=C(x,p,q)C(y,p,q)C(p,a,b)C(q,a,b).
]
All six are distinct **variable names**. It projects to x=y, with exactly 4 auxiliary extensions per equal ordered pair, 20 models total. This uses original strict C (30/125), not historical Q/P/S. If H(u,v)={h:C(h,u,v)}, H has two heads at pentagon distance 1, those heads are distance 2 apart, and H has one head at distance 2. The two outer clauses and required p!=q force the two inner names p,q to be the two heads of a distance-1 pair. Consequently x=y. An equal-terminal witness is (x,y,p,q,a,b)=(0,0,1,4,2,3) and its shifts.

## New physically critical native-C chain (PROVED)
For every integer k>=1, introduce t_0,...,t_k, 4 fresh auxiliary names p_i,q_i,a_i,b_i per link, and one closing head h. Define
[
F_k=igwedge_{i=0}^{k-1} E(t_i,t_{i+1};p_i,q_i,a_i,b_i) wedge C(t_0,t_k,h).
]
Then F_k has exactly N=5k+2 used names and M=4k+1 **physical C clauses**. It is UNSAT, since all links impose t_0=t_k but the closing C requires t_0 != t_k. It is **physically clause-minimal UNSAT**: for any deletion inside link i, set t_0...t_i=0, t_{i+1}...t_k=2, closing h=1. Use one of four complete broken-link vectors (x,y,p,q,a,b), indexed by deleted clause 0..3:
```
(0,2,1,3,0,4)
(0,2,1,4,2,3)
(0,2,3,4,0,1)
(0,2,3,4,0,4)
```
On every intact link choose (v,v,1+v,4+v,2+v,3+v) mod 5 for v=0 or 2. If the closing clause is deleted, choose all t_i=0, all intact links (0,0,1,4,2,3), and h=0. Every retained original C clause is true and its deleted source clause is false. Independent incidence BFS establishes **girth exactly 4**, not growing. Only closing h has degree one, so this is NOT the graph private-head construction.

## Sound generic one-sided UNSAT or UNKNOWN source specialist
A physical source parser indexes co-occurring name pairs. Any two C clauses sharing names p,q and having tips x,y form a fan. Match it to another fan whose **tips** are p,q and shared pair a,b, requiring six distinct names and four distinct source clause indices. This is exactly the proven E motif and certifies x=y. Compose discovered equalities with union-find, reconstruct a BFS path of actual source-indexed motifs, and find one **original physical C** that contains two thus-equal names. Emit this path plus concluding clause as a replayable UNSAT certificate, else UNKNOWN. The independent verifier uses an unordered five-triple predicate to check 5^6 local cases, replays all four source indices of every motif, and confirms the equality path and final contradiction. No free polarity advice or skipped negative verification. Naive arbitrary-source implementation has O(m^2) fans, O(m^4) joins, O(n+m^2) writable words, and O(n+m) certificate words, not the proposed n^1.33/n^.5 resource point. On this family acquisition and explanation are structurally easy even under arbitrary source relabeling and clause reordering.

## Symbolic row/block counterexample to hardness indicators (CONDITIONAL on representation)
Group consecutive equality gadgets into B=min(k,floor(N^.65)) source blocks, put closing C in the last. Endpoints of each group are shared z; promote additional internal names into z to ensure each block contains <=floor(N^.35) private names. The private names are disjoint after z. One **symbolic row** represents all z, with an O(B)-comparison dynamic selector: return first block with unequal endpoint colors, else final block. Every unequal-endpoint block is refutable because its links imply equality; if all endpoint colors agree, the final block's closing C is refutable for all h. This is a verified global all-z cover, not a syntactic OR or a sampled certificate. Checked examples: k=32: N162/B27/max-private5/shared48; k=64: N322/B42/max-private7/shared87; k=128: N642/B66/max-private9/shared67; k=512: N2562/B164/max-private15/shared245. All obey exact numeric caps. **R=1 ONLY for symbolic-row-with-dynamic-selector semantics**. If rows are literal assignments, R=5^|z| and the N^.195 constraint fails. A materialized shared assignment can exceed the proposed N^.5 writable space; this construction does not establish that endpoint.

## Independent finite audit and minimality check
- Original strict C against an independent set-of-unordered-color-triples predicate on all 125 triples.
- Exhaustive 5^6=15,625 E assignments: 20 models, all x=y; each equality value has 4 extensions.
- Computer-assisted minimality: **no satisfiable formula with <=3 physical C clauses forces equality of two distinct names**. Every connected <=3-clause 3-uniform incidence component uses <=7 names. Enumerating all 7,175 nonempty <=3-clause subsets of 35 possible 3-name scopes on seven names (7035 SAT, 140 UNSAT) and all 147,735 satisfiable formula/namepair combinations found an unequal model for each pair. Across different components, a translation of one component separates the two names. Thus four is minimum for satisfiable equality pp-definition.
- For k=1,2,4,8,16,32,64, all 515/515 physical deletion witnesses passed, including **87,884 true retained-C** and **515 false deleted-C** checks, plus BFS incidence-girth tests.
- 60 source relabeling/argument/clause permutation trials, 15 seeds at each k=1,4,16,32, all acquired and independently replayed source-indexed UNSAT certificates. Seeds: 202611190000+100*k+r, 0<=r<15.
- The native 25-clause girth-8 critical UNSAT and intrinsic 3-clause UNSAT correctly returned UNKNOWN, as did SAT and malformed controls. The specialist is incomplete by design.
- Exact structural row/block caps tested at k=1,2,4,8,32,64,128,512; 3,275 exhaustive endpoint assignments (small cases) and 4,000 seeded full-shared assignments. No finite timing is extrapolated as a lower bound.

## Adversarial consequence
**FALSIFIED as a standalone hardness indicator**: physical clause-criticality plus a genuinely native C (non-private-head) structure and even a saturated-block/private power-law partition do not prevent cheap deterministic global symbolic UNSAT cover acquisition. **OPEN**: extending a certified obstruction beyond this low-incidence-girth equality closure to high-girth critical native C; preserving uniform total-source access and any simultaneous n^1.33/n^.5 bound; transfer from the restricted source to arbitrary 3-SAT. The earlier intrinsic girth-8 critical control is not refuted by this specialist.

Reproducible scripts and complete source-indexed witnesses: local archive `T5C_Native_Equality_Chain_Redteam_20261119.zip` (full REPORT.md, HANDOFF.md, native_chain.py, independent_verify.py, run_audit.py, layout_audit.py, raw JSON, SHA256SUMS). Reproduce: `python run_audit.py && python layout_audit.py && python independent_verify.py chain_k32.json`.

Sources consulted: user's t5_strict_research.pdf p.4 and t5_strict_research_package.zip (README and proof_resource_audit); prior repository reports `2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md`, `2026-11-19_NATIVE_STRICT_C_25_CLAUSE_GIRTH8_AND_LOG_GIRTH.md`, `2026-11-19_K4_SOURCE_UNIFORM_GRID_MINOR_COVER.md`, and `2026-11-19_ANCHORED_PARITY_PATH_GLOBAL_COVER_RUN3.md`. General literature: Jeavons-Cohen-Gyssens, JACM 44 (1997) 527-548; Buss-Williams, Computational Complexity 24 (2015) 533-600. No priority claim for the equality gadget.

**P versus NP remains OPEN.**
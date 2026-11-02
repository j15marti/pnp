# LSPV-3 GATE324: Decision-only antichains versus paid source-factor SAT/Circuit-SAT transfer

**2026-11-02 01:29 PST | PROVED/EXACT restricted theorems, independently COMPUTATIONAL | P versus NP OPEN. External referee pending.** The target remains every valid duplicate-free proper Döcker monotone 3-SAT-(2,2) original; all other valid originals are handled by the broader all-input contract, not by this family-specific terminal. Residual circuits/Tseitin are not canonical children.

## Universal obstruction and four falsifiers

A compiler's full ordered cofactor table, its maximal decision-prefix frontier, and the computational work needed to decide SAT are different resources. We tested (1) soundness of existential **coverage dominance**, (2) the conjecture that such dominance gives polynomial complete-frontier compilation for connected M22 originals, (3) whether a paid source-factor AND/OR/finite-state transfer bypasses exponential frontier construction even for pinned SAT/UNSAT, and (4) whether dominance can replace **exact continuation equivalence** under later prefix pins or preserve model counts. The first and third hold in their declared settings; the second and fourth are falsified.

## Theorem A: sound decision-only dominance (general CNF, canonical source-indexed specialization)

At a fixed variable-order prefix S, let Γ(S) be original clauses meeting both S and its unassigned complement. An **alive** prefix assignment satisfies every original clause wholly within S. Let B(a)⊆Γ(S) be the crossing clauses already satisfied by at least one source literal in S. Then for alive a,b at the SAME prefix,

```
B(a) subseteq B(b)  ==>  for every identical suffix y, F(a,y) <= F(b,y).
```

Proof: fully-prefix clauses are satisfied by both; suffix-only clauses see the same y; covered crossing clauses of a are also covered by b, and all other crossing clauses have the identical suffix literals. Consequently one may discard a in an existential SAT decision DP, retaining one representative of every **inclusion-maximal** B. The dominance relation is hereditary under identical future suffix assignments; at the last variable an alive state exists iff SAT. An UNSAT terminal can be equipped with a typed source-clause-falsification/dominance DAG, which must be acquired, output and checked at its real cost.

If c_k=|Γ_k| and A_k is the number of retained maximal masks, Sperner gives A_k<=min(2^k,binom(c_k,floor(c_k/2))). A naive materialized implementation incurs a conservative total time O(N^2[1+sum_k(A_(k-1)+1)^2]) and peak space O(N^2+N max_k A_k) bits, with additional charged proof-DAG storage/output if retained. These bounds include source/index/head record acquisition, exact mask comparisons, copies and witness representative storage; foreign failed policies, switching, caches, GE/proof, child/replay/DELAY-COPY-RECOMP and ancestor/guest peak space must be added if used. Four affected source-clause IDs per variable are *logical*, not four native machine steps. This is a bounded-work **upper** bound for one specified representation, not an all-machine lower bound.

**Important semantic firewall:** dominance preserves *existence under suffix continuation*, not Boolean cofactor equality, #SAT equality, or equivalence under a future pin revising an earlier prefix. On the same valid F9 original, prefix x1..x4=0000 has B=0x6c0 and one SAT suffix; prefix with little-endian integer 2 has B=0x6d2 and seven SAT suffixes. The former is strictly dominated, yet suffix (x5..x9)=(1,1,1,0,0) gives full original mask112 FALSE and mask114 TRUE. Cache merging these as exact continuation functions would be unsound.

## Theorem B: exact 10^t maximal frontier on connected valid M22 originals

Use the authenticated connected cyclic F9-splice family G_t from GATE323, n=9t, m=12t, with F9 clause C1's positive x5 replaced by the next block's x5. Read **all** blocks' x1..x4 before **any** x5..x9. After the first 4t original variables, there are precisely 9t crossing clauses. Each block has 14 coherent alive four-bit prefixes, 14 different source crossing-coverage masks, and exactly ten inclusion-maximal masks, certified by the complete local list:

```
0x21f 0x257 0x41f 0x447 0x49e
0x4d6 0x61d 0x645 0x69a 0x6d2
```

They are pairwise incomparable; all other local masks are dominated. No fully-prefix clause spans blocks; the next-block x5 splice remains on the suffix, while original clause-ID coverage masks have disjoint block supports. Therefore feasible coverage posets form a Cartesian product, and their maximal masks form the Cartesian product of local maxima:

```
A_(4t)(G_t, bad source order) = 10^t  (exact).
```

Any architecture **explicitly outputting this whole maximal-coverage antichain** needs >=10^t state records. This is a restricted compilation lower bound, NOT a SAT decision lower bound.

Independently checked t=1,2,3: 14/196/2744 feasible source masks, 10/100/1000 maximal masks and 2/60/1352 fully-prefix rejected assignments. Full source-indexed DP state totals: F9 34; G2 block 68 versus bad 379; G3 block 99 versus bad 3821. Peak widths G2 bad=100, G3 bad=1000; explicit inclusion tests G2 bad 16,974, G3 bad 1,721,605. The G2 bad cut has 189 distinct exact cofactor functions (prior GATE323 verified GF(2) rank 184), versus only 100 existential dominance states. All are restricted representation metrics, not physical FLMV timings.

## Theorem C: fully paid, all-coherent-pin SAT/UNSAT transfer for the recognized G_t family

In each G_t block i, the eight **private** original variables are x1..x4,x6..x9. Let s_i=x5_i and let s_(i+1) be the next-block original x5 entering C1. Every source clause of block i involves only its eight private variables and the two boundary bits s_i,s_(i+1). Private-variable sets are pairwise disjoint. Given **any coherent original-variable pins p**, acquire the four integers

```
W_i^p(u,v) = number of pinned-consistent assignments to the 8 private
             variables satisfying ALL twelve ORIGINAL block-i clauses
             with s_i=u and s_(i+1)=v.
```

Every entry is **computed** by 256 original-source trials, so 4*256=1024 source tests per block, with source clause IDs and sign provenance available. There is no SAT-label oracle. For all t>=1, including t=1 with a formal split interface constrained equal by the trace,

```
#SAT(G_t | p) = trace(W_1^p W_2^p ... W_t^p).
```

Proof: for each fixed cyclic boundary assignment, local private completions multiply because the private variables are disjoint. Sum the products over cyclic assignments to get the matrix trace. Positive trace yields a compatible 2-state cyclic path, locally stored private completions, and a complete checked original-variable SAT witness. Zero trace, combined with all checked local 2x2 cells, is a **complete polynomial-size typed UNSAT certificate**. Both cases include the full clause-source evaluation, not a post-solution constant gate.

Unpinned W=[[34,47],[23,36]] for every block, yielding exact model counts t=1:70, t=2:4614, t=3:312970, t=4:21248098. More strongly, this algorithm solves **every coherent pinned residual** of recognized G_t, including same-original opposite labels, rather than only the trivially SAT unpinned originals.

An explicit **source-authenticated** recognizer first validates the canonical M22 grammar and checks the numbered cyclic G_t template (clause and literal order may vary), otherwise reports UNRESOLVED for valid nonfamily originals. Its work is polynomial in N=Theta(t log t). Exhausting 1024t local private assignments and 12 source clauses each is O(t) bounded-word work; sequential 2x2 matrices with constant (<2^9) entries require O(t^2) schoolbook binary bit work including growing product lengths. Complete source-table verification, witness/checker output, source/index/head movement and simultaneous live table/ancestor/output memory remain polynomial; other invoked policy/guest costs are charged in the overall controller. The forward fan-in-two clause-private evaluator has 4n-1 gates **only in that declared architecture**, not an unrestricted circuit minimum.

**Stronger global-interface incompatibility control, new same-original UNSAT/SAT one-bit pair:** On connected canonical G2, fix original pins p={x8=1,x6=0,x1=0,x15=0,x11=0,x13=0}. No original clause is already falsified. Both block factors remain individually satisfiable, but their paid source-verified matrices are

```
W_1^p = [[0,7],[0,7]] ; W_2^p = [[3,5],[0,0]]
W_1^p * W_2^p = [[0,0],[0,0]] ; trace=0 -> UNSAT
```

Therefore the two blocks' locally feasible solutions have no compatible cyclic original-variable x5 interface, and the original pinned residual is UNSAT. Flip ONLY original x6 from 0 to 1, leaving all other source pins unchanged: the integer trace becomes **38**, and a complete original-clause-checked SAT witness exists. An independent verifier checked both local matrices, absence of initially falsified original clauses, both factors nonzero, zero cyclic trace, and all 38 original-source completions for the SAT sibling. This is a nontrivial **global-consistency** UNSAT certificate, not merely a source clause already false. Direct UP-first DPLL still decides it cheaply, so there is no unrestricted work lower bound.

**Same-original one-bit controls:** Pin F9 x3=x4=x5=0. x1=0 gives UNSAT0, while x1=1 gives SAT2, and all 32 UNSAT completion leaves falsify an indexed original clause. On the same connected G2, fix the entire second F9 block to checked mask75 and hold the same first-block pins; flipping only original x1 again gives UNSAT0/SAT2, with 32 independently checked original-source UNSAT leaves. Direct UP-first DPLL needs 1/2 nodes with 9/109 F9 and 9/194 G2 literal inspections (UNSAT/SAT). Compiling full frontier or transfer is not **necessary** to decide those particular easy cases.

Independent no-producer-import checker A: **269,189 assertions**, all 2^18 G2 original assignments against fan-in-two circuit C_G2, F9/Y6 full truth tables, 10^t antichain checks t<=3, every-stage brute prefix audit F9/Y6/G2 bad, 264 F9 SS/SU/US/UU modes, 6,144 F9 complement identities, malformed rejects. Independent no-producer-import transfer checker B: **65 grouped checks**, 48 random coherent pinned G2 settings compared with all original source solutions (28 SAT,20 UNSAT), plus the one-bit opposite-label controls. U198/V198/F15 were inherited, not freshly replayed. Logical XOR is OFFLINE; no native tape T,S claims.

## Duplication, literature and exact unproved arrow

General dominance, incidence/pathwidth DP and existential factorization have substantial prior art. Compare Sæther, Telle, Vatshelle, *Solving MaxSAT and #SAT on Structured CNF Formulas*, SAT 2014, https://arxiv.org/abs/1402.6485; Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE TC 1986, https://doi.org/10.1109/TC.1986.1676819; Döcker 2019, https://arxiv.org/abs/1912.08032; Fortnow, Lipton, van Melkebeek, Viglas, JACM 2005, https://doi.org/10.1145/1101821.1101822. Previous project GATE319-323 already provided source-frontier safety, OBDD/cofactor ordering, G_t communication rank >=9^t and **unpinned** W. New restricted increment: **exact 10^t decision-only maximal antichain and a separately paid polynomial two-state algorithm that decides every original-variable pinned G_t residual (SAT and UNSAT)**. Searches included primary literature and j15marti/pnp and github.com/openai (the latter found unrelated Lean antichain coding); no novelty claim from search absence.

Neither all-input polynomial aggregate acquisition/descendant work for **every** canonical original, nor arbitrary-correct-A hereditary power-short ARC, nor numerical SAME-MACHINE FLMV SAT transfer has been proved. The 10^t lower bound is specifically on *explicit antichain compilation*, not generalized necessary SAT decision work. P=NP and P!=NP remain OPEN. No agent task IDs, titles, enablement or schedules were changed.

**Verified runnable:** experiments/arc/lspv3_324/compact324_public.py. The full separate producer, two independent no-import verifiers, all raw results and full mathematical report are in the dated GATE324 user archive. Root main.tex remains untouched absent an authenticated nonempty root and byte-exact LSPV-3-only write.

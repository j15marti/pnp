# ARC-T5-ENCODED-SIZE2: thread suppression does not supply power shrinkage
19 November 2026. ARC Strengthening. P versus NP OPEN. External independent peer review pending.

## Selected dependency and result
The dependency is ARC-T5-CRITICAL-PROMISE-REENTRY1 from the 08:01 report. Candidate: replace each maximal degree-two thread of the critical completion H=G+e by its exact endpoint relation, invoke a hypothetical polynomial finder on a smaller child, then lift.
Falsifiers: incorrect boundary support; loss of criticality; encoded length failing power shrinkage; uncharged output or retained reconstruction data.

PROVED/EXACT: under the explicit record encodings below, the full thread core has length Theta(L), where L is the original critical-deletion input length. Thus this normalization alone cannot give child length O(L^theta) for any fixed theta<1 on an unbounded family. This is a lower bound on this specific representation's size, not on witness computation or arbitrary compression.

PROVED/EXACT: deleting another arc while retaining the same designated missing edge always leaves the promise. These two facts close specific failure cases of the proposed hereditary compiler.

## Recovered sources and novelty scope
Read current AGENTS.md (blob 3b5d1788aa104b10f094e7eec28d22a070118b17); current coordination/CODEX/research skill were read earlier in this conversation and remain the governing ownership constraints. ARC has no assigned TMR root manuscript.
Read prior ARC report.tex (blob 4b5e82fb3943806c43357946e1bb9dcd875bd622) and handoff, and the lead's critical-thread normal form:
research/agents/lspv-1/2026-11-18_LSPV1_T5_CRITICAL_THREAD_WITNESS_NORMAL_FORM.md
(blob 2205074cab7c8260be1b1666fccbaaa3a8c74cfa).
The exact thread-deletion equivalence, extension multiplicities, and upper-bound witness algorithm are already proved there. They are recovered, not claimed new.
The present addition is an encoded-length obstruction to the ARC power-shrink premise, plus the same-designation hereditary obstruction.

## Definitions
H is connected, simple oriented, edge-minimal T5-UNSAT, with isolated vertices excluded. G=H-e retains all original vertices and specifies e. Let n,m count H vertices and arcs. Let b be its branch vertices, q its maximal threads, each of length ell_i.
Use dense binary vertex identifiers; original encoding explicitly lists vertices and arcs and the designation:
L=Theta((n+m+1) log(n+2)).
Core encoding explicitly lists b vertices, q typed binary constraints and the deleted-thread designation:
K=Theta((b+q+1) log(b+2)).
Each of nine relation labels costs O(1). Retaining full original identities and witness reconstruction data can only add storage; the theorem already holds for the smaller renumbered core.

## Theorem: exact critical quotient, but no power shrink
The verified thread lemma gives 1<=ell_i<=3. No loop threads occur. The nine-relation intersection lemma bounds parallel threads by four. Consequently
m=sum_i ell_i, n=b+sum_i(ell_i-1),
q<=m<=3q,
b+q<=n+m<=b+5q<=5(b+q),
q<=4 binom(b,2),
n<=4b^2-3b.
Also b<=n. It follows that log(n+2)=Theta(log(b+2)), uniformly for b>=2, and therefore K=Theta(L).
For any unbounded critical family, K/L^theta grows without bound whenever theta<1. The core retains one record for every original thread, so a reduction in vertex count alone cannot establish power shrinkage.

The quotient is nevertheless semantically exact: every branch assignment satisfying the intact core relations extends independently along every intact thread. If e lies in thread P, dropping the P constraint leaves two rooted fragments, which extend for every endpoint pair. Thus H is edge-minimal UNSAT exactly when its thread CSP is constraint-minimal UNSAT. Every deletion position within P has the same feasible branch assignments. This is the lead's established normalization theorem.

This theorem contracts H first, then drops the designated thread. More aggressive elimination in G after deletion, constraint merging, algebraic coding, succinct representations, treewidth DP, cycle-syndrome DP, and alternative compilers are not ruled out. The nine-relation core also is not automatically an ordinary T5 arc input.

## Theorem: raw edge deletion is not hereditary with its designation
For EVERY critical H, EVERY e in E(H), and EVERY f!=e, put J=H-{e,f} and retain e as the missing edge. Then J+e=H-f is SAT by edge minimality. Hence (J,e) is outside the promise requiring J+e edge-minimal UNSAT.
This is unconditional at every girth. It does not say that no OTHER designation or a different compiler could restore the promise. It says a recursive call on raw smaller edge subsets cannot inherit the promised finder guarantee.

## Charged conditional recurrence
For a hypothetical fixed finder A with promised time O(L^k) and space O(L^s), normalization costs polynomial time and retains original source/mapping data for lifting. Its child language must first be supplied with a valid promise-preserving compiler. Even if that issue is granted, K=Theta(L) yields O(L^k) for one black-box call, with constants depending on k. It provides no transformation k -> theta*k with theta<1.
With O(L^eta) such calls and overhead O(L^r), the justified upper exponent is at most max(r,eta+k), not max(r,eta+theta*k) for theta<1. This does NOT prove that k is optimal. A known upper recurrence cannot become an impossibility bound.

For the direct implementation storing input, thread maps, factors, candidate and output, peak retained storage is O(L) bits up to indexing conventions, plus actual child space. A conservative sequential bit-machine implementation has polynomial preprocessing time and O(L^2) space; a tighter word-RAM scan is O(n+m) work and words. Explicitly emitted output costs Omega(n) bits. Final verifier work includes every original remaining arc.
Off-promise calls cannot use a space guarantee that holds only on promised inputs. Clocking gives a time-based space cap, but it does not make the child promise true.

Recursive use needs a separate progress proof, paid aggregate ancestor storage and successful decoding at every level. Constant-factor input shrinkage may still support useful divide-and-conquer algorithms under additional structure; the theorem rules out only the asserted power-length inference.

## Executed independent audit
The script arc_size_audit.py uses no prior project solver.
1. Exhaustive 5^8 root-normalized assignments on the sharp nine-vertex fixture verify UNSAT and every edge deletion SAT. Counts by thread are BBB:60, FBB:60, FFF:40, BB:180, matching the lead's exact multiplicities. Full witnesses are recorded.
2. All 110 ordered pairs of distinct deleted/designated edges have a checked witness for H-f, verifying the same-designation promise obstruction.
3. Authenticated source079.t5 SHA256:
0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac.
Its 33 vertices and 44 arcs suppress to 19 branch vertices and 30 constraints. Thread lengths: twenty of length 1, six of length 2, four of length 3. Original vertex-plus-arc records:77; core records:49.
This run checks source079 structure only, not its full UNSAT proof or all deletion witnesses anew.

A first draft test incorrectly compared unweighted core support counts to original witness counts and failed. The corrected check multiplies intact-thread extension counts. This correction affects the test, not the size theorem or the recovered weighted formula. The final script and raw output are the published versions.

The earlier complete path and 512-subfamily checks remain available in the conversation's independently executed recovery audit; they were not redundantly rerun. Structural arguments were checked: rotations glue at articulations; four-edge saturation eliminates long threads; parallel thread redundancy contradicts edge minimality. The Moore bounds survive but are unnecessary for the size theorem.

## Literature and hardness boundary
Kun's Theorem 1 (fixed girth parameter) and Lemma 13 (fiber decoder) support fixed-girth source/witness transport, not a compiler into intrinsic-critical deletions with growing girth:
https://arxiv.org/pdf/0706.1701
The distinction between inclusion-minimal UNSAT and arbitrary proper SAT subsets is standard in MUS research; see Bendik and Meel, Counting Minimal Unsatisfiable Subsets (CAV 2021):
https://meelgroup.github.io/publication/cav21_mus/
The project search found earlier quota-specific critical-port closure failures; those concern other syntactic families and are not used to prove this T5 theorem.
Intrinsic-critical promise NP-hardness, growing-girth uniform polynomial blowup, and unrestricted witness lower bounds remain OPEN. No contradiction follows from assuming a polynomial finder.

## Status and gates
PROVED: K=Theta(L) for this explicit thread-core representation; raw edge deletion with unchanged designation fails promise closure.
COMPUTATIONAL: n9 exhaustive audit and source079 structural trace.
CONDITIONAL: finder recurrence after a paid valid child compiler.
FALSIFIED: this normalization alone supplies uniform power shrinkage; critical-deletion promise is hereditary under raw edge deletion with the same designation.
OPEN: stronger compression, re-entry compiler, universal runtime lower bound, P versus NP.
DISJ: PASS scoped, no size-to-execution inference. Relativization/algebrization/Natural Proofs: no separation claimed; unrestricted hinge OPEN. Simultaneous DTISP: only upper costs for one implementation, forbidden-region transfer OPEN. Configuration counting: not used for a lower bound.
Independent external peer review pending. No local repository checkout, preflight or formal proof kernel build was available. Additive ARC publication only; no peer manuscript or schedule changed.

Next blocker: find a genuinely power-short encoding and promise-preserving re-entry map for the more aggressively eliminated G-kernel, paying for all constraint records and original-witness recovery. Full H-thread normalization is now excluded as the source of that power saving.

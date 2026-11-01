# WRAPPER-CONNECTED-SHALLOW-BOUNDARY1

Date: November 1, 2026, 01:33 PDT. Independent review, external mathematical referee pending.

**Status:** PROVED/EXACT restricted structural lemma (proof below), COMPUTATIONAL finite controls, CONDITIONAL ARC composition, P versus NP OPEN.

## Target and previous work

The canonical target is all valid, proper, duplicate-free clause-monotone 3-SAT-(2,2), every variable occurring twice in each polarity. A malformed encoding must be rejected. This review recovers double-WRAPPER, RECURCLOSE1, CYCLEGAIN1, STREAMCOMP1, ORBITBATCH1, WRAPPER-AS-SAT1 and arbitrary-A wrapper firewalls. It builds on LSPV-4 SURVIVOR-FRONTIER292 and LSPV-5 REFEREE260. The new result concerns raw source-identity-preserving cofactors, not arbitrary semantic or circuit compression.

## Theorem: all-b boundary lower bound

Let F be any connected valid canonical source on n variables. Assign b=k0+k1 original variables coherently, with k0 assigned zero and k1 assigned one. Form the ordinary cofactor by deleting satisfied clauses and false occurrences, with no semantic re-encoding. Let e be the number of *additional unassigned variables* that disappear, and r the number of original unassigned variable identities still occurring. Then

    e <= 2 min(k0,k1)
    r = n-b-e >= n-2b.

In a nonterminal residual, there are at most 1+5b nonempty incidence components, and the largest has at least

    ceil((n-2b)/(1+5b))

original variables when n>2b.

**Proof:** Every erased free variable loses both positive and both negative occurrences. Each deleted positive clause contains a pinned 1 and thus at most two free occurrences. There are at most 2k1 such clauses; therefore e<=2k1. Negatives analogously yield e<=2k0. For component counting, start from the connected bipartite incidence graph. Removing b pinned variable vertices of degree at most 4 increases component count by at most 3b. Every subsequently deleted satisfied clause has degree at most 2 since it originally contained a pinned literal; deleting each raises component count by at most one. At most 2b clauses are satisfied by the b pinned variables, so at most 1+3b+2b=1+5b components remain. Removing vanished isolated variables cannot increase the count. Pigeonhole on the r active identities yields the final inequality. This proof makes no assumption about SAT versus UNSAT.

**Conditional shallow-WRAPPER obstruction:** If an unresolved raw component is returned as a canonical child *injectively retaining all original variable identities*, O(log n) total assignments leave a component of size Omega(n/log n). For conventional source encoding length N=Theta(n log n), this is omega(N^lambda) for every fixed lambda<1. Thus logarithmic-depth source-faithful binary branching plus component splitting does not itself produce uniform power-short children on connected nonterminal inputs. This says nothing about semantic/noninjective re-encoding, cheap terminals, forced propagation beyond b, shared-DAG compression or arbitrary SAT algorithms.

**Necessary boundary size:** If every unresolved residual component contains at most M original variables, the inequality forces

    b >= (n-M)/(2+5M).

At M=O(N^lambda), 0<lambda<1, and N=Theta(n log n), the required number of assigned variables is Omega(n^(1-lambda)/(log n)^lambda), unless the wrapper completes early or uses semantic merging. This is *not* a lower bound on the number of binary branches, because unit propagation, dynamic programming and cached states may share work.

## Independent controls

Two independently written Python programs exhaustively evaluated all 75 positive degree-two four-triple selections on six variables times all 75 negative selections, giving 5,625 connected canonical sources. All 405,000 assignments of one or two source variables passed occurrence-erasure and component bounds. The independent implementation built a separate bipartite incidence graph. A 15-variable connected canonical F15 sample covered all 4,090 assignments with one to three pins, including a SAT source with 1,032 models, an UNSAT cube with zero extensions and neighboring SAT cube with two extensions. Canonical Y6 had 20 models. Large U198 UNSAT and V198 SAT certificates were reviewed in prior REF260 rather than re-executed here. No native FLMV physical tape XOR, guest execution, head operations or peak-space claim is made.

## Recovered WRAPPER synthesis and open arrow

- Double WRAPPER exactly computes OR over boundary assignments of AND over independent residual components; polynomial total child count, acquisition and child size remain unproved.
- Typed completed phases may contain same-scale internal steps; only the fully charged completed macro must meet the size and work contract.
- STREAMCOMP1 charges per-child addressed-bit generation. For q<=N^(beta+o(1)) children, sizes<=N^(lambda+o(1)), access<=N^(g+o(1)), and local time<=N^(a+o(1)), the conservative conditional guest transformation is K'<=max(a,beta+g+lambda K). Retained generators, source, indexes, caches and simultaneous space must also be bounded.
- At (a,beta+g,lambda,s)=(11/10,3/5,1/2,1/2), a **hypothetical** all-input hereditary same-machine implementation has formal fixed point (6/5,1/2). The implementation does not exist in verified project work.
- WRAPPER-AS-SAT1 can constrain computation/lineage but inherits its full simulation size and does not make universal path correctness an existential SAT promise.
- Hash/prime and DELAY/COPY/RECOMP/INTERP controls establish provenance and expose uncharged parent-A calls; they cannot generate an arbitrary-K-independent semantic quotient.
- A local-bit, near-linear ordinary-SAT-to-Doecker normalizer with polylog bit access and logarithmic workspace would address *numerical FLMV transport*, but the cited CONSTRUCTION-STRENGTHEN17 does not implement the final addressable strict22 emitter.
- Main next construction: an adaptive **typed macro** applying certified signed-spill forcing, saturation GF(2), Horn/2SAT/XOR, bounded-interface DP and exact AND/OR combination, with the first genuinely semantic/noninjective power-short target reencoder. Charge discovery, failed policies, all source/guest/index/child accesses, output and simultaneous writable space.

External source controls: FLMV JACM 2005 (https://lance.fortnow.com/papers/files/tst.pdf); Darmann and Doecker DAM 2021 (https://doi.org/10.1016/j.dam.2020.12.010); Doecker 2019 (https://arxiv.org/abs/1912.08032); Recursive Backdoors MFCS 2021 (https://arxiv.org/abs/2102.04707); Depth Beats Size JCSS 2024 (https://doi.org/10.1016/j.jcss.2024.103520). Fortnow-Santhanam OR-compression conditional lower bounds cannot be promoted to an unconditional contradiction under an assumed P=NP.

**Unresolved:** all-input semantic hereditary power-short ARC, arbitrary-decider A->Phi(A), exact native FLMV transport. **P versus NP OPEN.**

END_OF_VERIFIED_REPORT::WRAPPER_CONNECTED_SHALLOW_BOUNDARY1::P_VS_NP_OPEN

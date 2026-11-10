# LSPV-5 independent red team: cardinality-to-liveness firewall [P2-L5-472]

**Time:** 2026-11-09 17:48 PST (America/Los_Angeles)  
**Role:** LSPV-5 Independent Proof Red Team; historical Route B label preserved  
**Status:** **PROVED-RESTRICTED counterexamples; OPEN transfer; P versus NP OPEN**

## Outcome first

This run falsifies three tempting ways to extract a live-space lower bound from an abstract collecting semantics:

1. $2^N$ exact source-authenticated states across all $N$-bit sources do **not** force $N$ writable bits on any one run. A read-only source scanner has $2^N$ pairwise distinct source-tagged states in the collecting domain while using $O(\log N)$ charged work bits.
2. $2^N$ nondeterministic branch histories do **not** force $N$ live bits on one branch, and do not turn an NP verifier into a deterministic UNSAT decider. A branch can be generated online with an index and one accumulator.
3. An accepted AND proof DAG with $\Theta(q)$ distinct count-once nodes does **not** by itself force $\Theta(q)$ peak space. A depth-first checker of the explicit control DAG below uses $O(\log q)$ live work bits, while a materializing checker uses $\Theta(q)$.

The valid repair is narrower: fix one source, one exact machine model and one schedule, quotient immutable provenance, and prove either (i) an injection from **simultaneously live** distinguishable obligations into charged storage or (ii) a model-matched pebbling lower bound that survives legal recomputation and source/certificate rereads. Abstract-state cardinality alone measures the analyzer's semantic universe, not the analyzed machine's live memory.

## IDEA -> SEARCH -> ITERATE

### IDEA and falsifiers stated before search

**Initial hypothesis.** A source-authenticated collecting abstraction might yield a space lower bound by counting distinguishable abstract states or obligations.

**Assumptions.** Binary source length $N$; read-only authenticated input is not charged as work space; complete machine configurations and all transitions are represented; work space is simultaneous writable high-water; proof nodes are charged once for logical work but may be reread or recomputed unless the exact model forbids this.

**Prediction.** If the hypothesis were sound, exponentially many authenticated sources, histories, or proof nodes would force polynomially many simultaneously live work bits.

**Falsifiers.** (F1) the cardinality comes from varying the read-only source across runs; (F2) branch histories can be generated and forgotten online; (F3) a shared AND DAG can be checked depth first with recomputation/rereads; (F4) the proposed lower bound counts the abstract interpreter's representation rather than the target machine's writable store.

### SEARCH

Primary sources and exact scope reviewed:

- Fortnow--Lipton--van Melkebeek--Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, exact random-access machine definitions and Theorems 3.1/3.2. The displayed branch $\beta(c)=\tfrac12((c+2)/c^2-c)$ is a necessary-space exponent in its applicable deterministic theorem, not an equality defining solver space.
- Cousot--Cousot, POPL 1977: collecting semantics and sound approximations. A may-overapproximation supports universal upper facts and bottom-style exclusion only with the corresponding polarity; its carrier cardinality is not target storage.
- D'Silva--Haller--Kroening, POPL 2013: abstract conflict-driven learning is proved for completely additive reductive functions over finite powerset lattices. Its bottom-everywhere correctness statement is not a target-machine space theorem.
- D'Silva--Haller--Kroening, POPL 2014: Abstract Satisfaction develops deduction, abduction and quantification through Galois connections and refinements; representation and refinement costs remain analyzer costs unless simulated by the analyzed machine.
- Savitch 1970: reachability can trade time for space by recomputation. This is a direct control against materializing a configuration graph merely because it exists.
- Sethi 1975 and Carlson 1984: register/pebbling formulations explicitly distinguish placements (space) from moves/recomputation (time). A DAG-node count alone is not a pebbling lower bound.
- Ryan Williams, *Inductive Time-Space Lower Bounds for SAT and Related Problems* (Computational Complexity 2006): later subpolynomial-space SAT exclusions improve the time exponent beyond the original golden-ratio line (including $n^{1.7327}$ in the paper). Williams's later alternation-trading work reaches $2\cos(\pi/7)\approx1.8019$ for subpolynomial space. These are stronger **small-space exclusions**, not formulas that calculate exact $S$ from an arbitrary polynomial-time upper bound.

Required repository review, pinned at this run:

| Repository | Pinned head | Material result |
|---|---:|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | README still proves only a scoped finite-machine $P\subseteq NP$ direction and marks $NP\subseteq P$ unknown; issue 567 is a scoped residual-key counterexample, not a SAT space lower bound. |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | Public method review stresses scoped models, recomputation and representation costs; no universal memory theorem found. |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | Proof checking/logical work remains distinct from checker live-space. |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | Verified checker evidence does not supply a live-space lower bound for all solvers. |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | No relevant changed theorem or machine-space bridge found. |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | No relevant changed theorem or machine-space bridge found. |

Project continuity reviewed at current main: governing 16:24 handoff; root `proof1.txt` and `proof2.txt`; issue #3; [P2-L5-471], [P2-L1-549], [P2-L2-532], [P2-L3-545]; current Grok and Claude directories. Claude's sequential-access crossing-sequence artifact does not transfer to the required random-access model; Grok's finite circuit-rewiring artifact does not prove a space tradeoff. Query/open failure logged: the Elsevier landing page for Savitch returned HTTP 403, so the theorem scope was checked against the indexed primary abstract rather than claimed as a full-text read.

### ITERATE: revised claim

The initial counting idea is false without a liveness theorem. The revised, independently checked claim is the following.

**Lemma 472-A (source-axis cardinality firewall, PROVED-RESTRICTED).** For every $N\ge1$, there is a uniform total deterministic read-only-input machine $M_N$ whose collecting semantics over all $x\in\{0,1\}^N$ contains at least $2^N$ pairwise source-authenticated complete states, while each run uses at most $\lceil\log_2(N+1)\rceil+3$ writable bits. Hence neither $|A_N|$ nor $\log_2|A_N|$ lower-bounds per-run charged work space when $A_N$ ranges over different immutable sources.

*Proof.* Put the exact source identity in the semantic state, as source authentication requires. The scanner retains only an address $i\in[0,N]$, one parity/acceptance bit, and constant control. The input and its authenticated identity are read-only semantic components, not copied into the work store. There are $2^N$ distinct source-tagged initial (and corresponding reachable) states across sources, but the stated work bound holds on every run. $\square$

**Lemma 472-B (branch-axis firewall, PROVED-RESTRICTED).** A nondeterministic process can have $2^N$ semantic histories while using $O(\log N)$ live work bits on each branch: generate one choice bit at a time, update a constant-size accumulator and index, then forget the choice. Exact history tags in the collecting semantics are semantic provenance unless the concrete machine stores them. This does not decide UNSAT and is outside deterministic FLMV.

**Lemma 472-C (proof-work/space firewall, PROVED-RESTRICTED).** Let $q=2^h$. Form $q$ typed leaf checks that all reference one globally valid one-bit lemma, and combine their results with a balanced binary AND tree. Counting the lemma once gives $q+(q-1)+1=2q$ distinct logical nodes. A materializing checker can use $2q$ bits. A depth-first checker using read-only certificate/source access, an $h$-bit leaf index, an $h$-bit traversal counter/stack code and constant control uses at most $2h+5$ live bits. Therefore count-once DAG work does not imply peak checker space without a retention or pebbling theorem. This is a typed audit DAG, not a claim that historical $R_{\mathrm{mix341}}$ contains a new rule.

The explicit controls passed for $1\le N,h\le20$. At $N=h=20$, the collecting source/branch counts are $1,048,576$, the scanner bound is 8 work bits, and the $2,097,152$-node audit DAG has a 45-bit depth-first bound. A separate JavaScript reimplementation replayed 135 checks.

## Complete concrete and abstract machine semantics

For a fixed authenticated machine/source pair $(M,x)$, a deterministic complete configuration is

$$
\sigma=(M,\operatorname{auth}(M),x,\operatorname{auth}(x),q,h_I,I,h_W,W,h_A,A,\mathit{stack},\mathit{cache},o,p,t,s_{\max}),
$$

where $I$ is read-only input, $W$ is writable work store, $A$ is the random-access address/index state, $p$ is parser/source status, $t$ is elapsed real steps and $s_{\max}$ is the maximum simultaneous writable occupancy so far. Malformed input has an explicit parse state and deterministic rejection transition. Nondeterministic configurations add the current choice port and semantic branch-history tag $\eta$; $\eta$ is charged only if the concrete machine writes it. A deterministic transition is a partial function completed with typed halt/reject states; a nondeterministic transition is a relation. Neither silently copies all alternatives into one configuration.

Let $\Sigma$ be these configurations and $C=\mathcal P(\Sigma)$ ordered by inclusion. Use the abstract product

$$
A=\mathsf{Tag}_{M,x}\times\mathsf{MayPC}\times\mathsf{MayOut}\times\mathsf{Parse}\times
\mathsf{Int}(t)\times\mathsf{Int}(s_{\max})\times\mathsf{Int}(a_{\max})\times
\mathsf{Count}_{src}\times\mathsf{Count}_{branch}\times\mathsf{Count}_{proof}.
$$

$\alpha(X)$ retains exact authenticated tag sets, unions may-control/output/parse values, interval hulls of elapsed time, peak work and address high-water, and exact-or-capped semantic counts. $\gamma(a)$ contains exactly concrete states compatible with every component. Then $X\subseteq\gamma(\alpha(X))$ and

$$\operatorname{Post}^{\#}=\alpha\circ\operatorname{Post}\circ\gamma$$

is a sound may-overapproximating transformer for deterministic steps, nondeterministic branch union, parse/reject, read/write, allocation/free and halt. Join unions semantic alternatives and takes maxima of upper resource endpoints; it does not authorize cross-branch data reuse.

**Resource polarity.** An upper endpoint $\overline s$ with $\gamma(a)$ covering all concrete states can certify $s_{\max}\le\overline s$. A positive lower bound needs either every represented run to satisfy it or an injection/pebbling argument on a fixed run. `Count_src`, `Count_branch`, and `Count_proof` have no automatic lower-space polarity. Materializing $A$ is a cost of the analyzer unless an explicit simulation places it in $W$.

## FLMV arithmetic and the $k\to\infty$ question

For the cited branch

$$\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right),$$

$\beta(c)>0$ exactly while $c^3-c-2<0$, i.e. $c<1.521379706\ldots$. At $c=6/5$,

$$\beta(6/5)=\frac{23}{45}=\frac12+\frac1{90}.$$

This says that a deterministic random-access SAT decider with the exact theorem's time/model hypotheses cannot also have space $O(N^s)$ for $s<23/45$ (up to the theorem's asymptotic qualifications). It does **not** calculate its actual $S$. SAT in P supplies some finite exponent $c$ but does not supply $c=6/5$; for a large polynomial exponent this branch is vacuous.

For $T(N)=O(N^k\operatorname{polylog}N)$ with $k\to\infty$, the displayed function satisfies

$$\beta(k)=-k/2+O(1/k),$$

so it becomes negative and gives no positive space lower bound. One cannot repair this by taking $N$ extremely large: asymptotic exponent inequalities do not change sign. Nor does an NP verifier inherit the deterministic result. Later alternation-trading results rule out time below about $N^{1.8019}$ **when space is subpolynomial**; they still do not say what space every $N^k$-time algorithm uses for arbitrary $k$.

Illustrative exponent-only values (not bytes, constants suppressed):

| $N$ | $N^{1/2}$ | $N^{23/45}$ | ratio $N^{1/90}$ | scanner counter bound |
|---:|---:|---:|---:|---:|
| $10^6$ | $10^3$ | $1.1659\cdot10^3$ | $1.1659$ | 23 bits |
| $10^{12}$ | $10^6$ | $1.3594\cdot10^6$ | $1.3594$ | 43 bits |
| $10^{24}$ | $10^{12}$ | $1.8478\cdot10^{12}$ | $1.8478$ | 83 bits |
| $10^{60}$ | $10^{30}$ | $4.6416\cdot10^{30}$ | $4.6416$ | 203 bits |

These columns compare growth laws only. They are not estimates of RAM bytes and do not include hidden constants, word size or machine-conversion overhead.

## Independent challenge and mandatory controls

- **Could source authentication force a copy?** No. Authentication is a semantic relation/tag unless the exact machine model requires copying the source or digest into charged work memory. If such a rule is proposed, its read, hashing and storage costs must be specified.
- **Could all nondeterministic branches be live?** Not in the standard branchwise definition. A deterministic exhaustive simulation may use different time/space; it needs its own construction and cannot be smuggled into $A_{NP}$.
- **Could sharing force retention?** Sometimes, but only via the exact schedule/reference rules. The audit DAG deliberately includes a shared global lemma and AND obligations; rereading/recomputing defeats node-count inference. A model-matched pebbling lower bound is the missing premise.
- **Could proof-work lower bounds imply solver memory?** No. $W_R$, proof length, checker time, checker space, producer space and ideal minimum are different measures.
- **Tseitin GF(2), compact mod-3 adders, Cook ER/PHP and shared-DAG shortcuts:** no new family lower bound is claimed. Each remains a mandatory shortcut/control against any future transfer from proof work to live memory.

## Resource ledger for this run

| Phase | Charged result |
|---|---|
| Governing/project/source reads | complete handoff, both trackers, issue #3, current peer/Grok/Claude files, primary papers, six pinned repositories |
| Logical derivation | three restricted lemmas; no $R_{\mathrm{mix341}}$ rule or weight changed |
| Executable evidence | Python 150 assertions; independent JavaScript 135 checks |
| Evidence bits | Python 4,624 bytes; JS 2,010 bytes; raw JSON 1,904 bytes before publication |
| Construction/search | charged to this research run; not inserted into ideal $W_R$ |
| Target-machine space | only the stated per-control high-water formulas; host process memory is not a theorem about SAT |
| Retrieval/recomputation | allowed only in explicit controls; future machine claims must account for reads, references, caches and recomputation |
| Failed policy/source access | Elsevier full-text landing page returned 403; indexed primary abstract used and limitation recorded |

## Tracker review and disposition

- `proof1.txt`: [P1-01], [P1-03], [P1-04] reviewed; no material status/dependency/evidence/gap change.
- `proof2.txt`: new **[P2-L5-472]** materially narrows [P2-A1], [P2-A2], [P2-A3] and [P2-C3]: abstract/source/branch/proof cardinality is not a live-space lower bound without fixed-source liveness injection or exact-model pebbling. [P2-D1], [P2-B1], [P2-B2] remain OPEN. Peer [P2-L1-549], [P2-L2-532], [P2-L3-545] are consistent controls.

## Actual advance, verification, publication status, remaining gap

**Advance:** a formal polarity repair and three explicit counterexamples now block cardinality-based claims at source, branch and proof-DAG levels.  
**Verification:** 150 Python assertions and 135 independent JavaScript checks passed.  
**Publication:** report, code, raw results, handoff, tracker delta and issue #3 receipt are published/read back with the commit recorded in the issue.  
**Precise remaining gap:** prove, on the exact FLMV random-access model or another explicitly named model, that every relevant deterministic SAT computation for a fixed source has many obligations simultaneously live, or prove the corresponding recomputation-resistant pebbling bound. No such theorem was established here. P versus NP remains OPEN.


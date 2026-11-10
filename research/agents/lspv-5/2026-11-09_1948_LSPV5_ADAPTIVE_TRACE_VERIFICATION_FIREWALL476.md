# LSPV-5/476 — adaptive RAM trace verification is not deterministic simulation

**November 9, 2026, 19:48 PST | Independent Proof Red Team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Outcome first

A quasilinear circuit can verify a *guessed* adaptive RAM execution by receiving the chronological trace, an address/time-sorted copy, and routing choices as auxiliary input. This is not a deterministic circuit or FLMV-machine simulation that generates the machine's output from the original source alone.

The exact restricted lemma proved here is:

> Fix a deterministic random-access program $M$, a source $x$, a step bound $T$, and authenticated initial memory. Let $V_M(x,\tau,\pi)$ check (i) the initial complete configuration, (ii) every local state transition, (iii) that $\pi$ is a permutation sorting all memory events by address and time, (iv) last-write/read consistency in that order, and (v) the final output. Then $V_M$ accepts exactly one complete transcript $\tau$: the concrete run of $M(x)$ through $T$ steps. Existence and efficient verification of this unique auxiliary transcript do not supply an algorithm for acquiring it.

Ben-Sasson--Chiesa--Genkin--Tromer--Virza make precisely the auxiliary-input distinction in their TinyRAM reduction: their circuit verifies a trace and a nondeterministically routed memory-sorted copy, with size

$$
T\bigl(|C_{TF}|+|C_{MC}|+O((\log T)^2)\bigr).
$$

It is a reduction to **circuit satisfiability**, not a Boolean circuit computing the deterministic RAM output. Treating that relation as a direct evaluator silently imports the satisfying trace. The 2023 tri-state-circuit paper independently states that direct ordinary Boolean-circuit RAM simulation still pays the quadratic memory scan; its quasilinear result changes the circuit semantics to input-dependent eager firing.

This falsifies the proposed shortcut “quasilinear transcript-checking circuit + small-space circuit evaluation = small-space deterministic adaptive-RAM simulation.” It does **not** prove that no other simulator exists.

## IDEA -> SEARCH -> ITERATE

### Initial idea

Replace the quadratic read-over-write DAG from LSPV-5/475 by a sorting/routing memory-consistency circuit, then feed the quasilinear circuit to a small-space circuit evaluator.

### Falsifiers

1. The circuit only verifies a guessed transcript instead of generating it.
2. Adaptive addresses make the sorted trace and routing settings auxiliary witness data.
3. Turning unique satisfiability into deterministic output acquisition invokes search/SAT and is circular here.
4. Sorting, word width, source access, routing, construction, output, or peak storage is omitted.

### Search evidence that changed the idea

- **Ben-Sasson et al., _SNARKs for C_ (2013), Section 2.3:** arbitrary data-dependent memory is handled by adding the trace, memory-sorted trace, and routing decisions as auxiliary inputs to a circuit-satisfiability instance. The paper explicitly leverages nondeterminism. URL: https://web.eecs.umich.edu/~genkin/papers/csnark-20131007.pdf
- **Heath--Kolesnikov--Ostrovsky, _Tri-State Circuits_ (ECCC TR23-095, 2023):** $O(T\log^3T\log\log T)$ tri-state gates emulate RAM, while the paper contrasts this with quadratic ordinary Boolean-circuit scanning. URL: https://eccc.weizmann.ac.il/report/2023/095/
- **Williams, _Parallelizing Time With Polynomial Circuits_:** on the random-access TM model, $\mathrm{DTIME}[t]\subseteq\Sigma_{3a}\mathrm{SPACE}[t/a+\log t]$ and uniform polynomial-size semi-unbounded circuits of depth $O(t/\log t)$ follow. This is an alternating/circuit simulation, not a deterministic low-space same-time solver. URL: https://people.csail.mit.edu/rrw/spaa-journal-rev4.pdf
- **Cousot--Cousot (POPL 1977):** sound abstraction requires a declared concrete semantics, abstract lattice, approximation order and consistent transformers. URL: https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml
- **D'Silva--Haller--Kroening (POPL 2013/2014):** abstract conflict learning combines over- and under-approximations under explicit lattice hypotheses; abstract satisfaction characterizes models through deduction, abduction and quantification transformers. Neither result turns correctness of a model checker into a complexity lower bound or a deterministic witness generator. URLs: https://www.kroening.com/papers/popl2013.pdf and https://www.kroening.com/publications/view-publications-dhk2014-popl.html

### Revised claim

The routing construction is useful as a **certificate relation** and an abstract-satisfaction domain, not yet as the missing deterministic time-to-space transform. The acquisition step is the precise open edge.

## Exact proof of the restricted lemma

Let a complete event record be $(t,k,a,v)$, where $k\in\{R,W\}$, $a$ is the accessed address, and $v$ the read or written value. A claimed transcript contains complete control state, registers/index heads, chronological events, final output, and a permutation $\pi$.

**Soundness.** Local transition checking fixes each next control/register state once the claimed read value is fixed. Sorting/permutation checks ensure every event occurs exactly once in nondecreasing $(a,t)$ order. For each fixed address, scan its events in increasing time, beginning with the authenticated initial value. Every write changes the current value; every read must equal it. Induction over the chronological steps therefore shows that each claimed read equals the concrete last write and each next complete configuration is the actual deterministic successor. Thus an accepted transcript equals the real run.

**Completeness.** Record the real run and sort its events by $(a,t)$. Every local and memory check passes.

**Uniqueness.** Soundness maps every accepted transcript to the same deterministic run, so two accepted complete transcripts are identical up to any explicitly permitted irrelevant routing encoding. Our finite grammar uses the canonical sorted permutation, so the accepted certificate is literally unique.

This proves exact certificate semantics. It proves neither a lower bound for finding the trace nor a deterministic method that finds it in the verifier's space.

## Concrete and abstract domains

Concrete complete configurations are

$$
C=(x,h_x,q,\mathbf r,\mathbf h,\mathbf i,M,t,w,p),
$$

including authenticated read-only source $x$ and input head/index, control state $q$, registers $\mathbf r$, every work head/index $\mathbf h,\mathbf i$, the finite nonblank memory map $M$, elapsed time $t$, live writable bits/positions $w$, and all-phase peak $p$.

The concrete domain is $D=\mathcal P(C\times H)$ ordered by inclusion, where $H$ is the chronological history. Deterministic $A_P$ has one successor or a halting configuration; nondeterministic $A_{NP}$ has a set of choice-labelled successors.

The trace-relation abstract domain $D^\#$ is the conjunction lattice of:

- source hash/length and initial-memory equations;
- symbolic control/register/index values at every time;
- chronological access-event variables;
- local transition constraints;
- routing/permutation and address/time order constraints;
- last-write/read consistency constraints;
- time, live-space and peak-space counters;
- deterministic versus existential-branch tags and final-label obligation.

$\alpha(X)$ is the strongest representable conjunction true of all configurations/histories in $X$. $\gamma(\varphi)$ is the set of complete configurations/histories satisfying $\varphi$. Thus $X\subseteq\gamma(\alpha(X))$. The best sound transformer is

$$
\operatorname{Post}^\#=\alpha\circ\operatorname{Post}\circ\gamma,
$$

with separate native transformers for source read, index update, random access, ordinary work update, branch choice and halt. The certificate circuit is a finite relational presentation of the exact singleton deterministic history when all fields remain precise.

**Resource polarity.** MAY/overapproximating reachability is sound for excluding behavior only when the abstract set is empty. A nonempty abstract model does not produce the model operationally. Peak-space upper bounds require every concretization to obey the bound; peak-space lower bounds require every legal realization to exceed it. Counting abstract configurations, certificate bits or proof-DAG nodes supplies neither statement without an operational injection or simulation. Widening or a failed abstract search is inconclusive.

For $A_{NP}$, abstract satisfaction of an accepting trace correctly expresses existential SAT acceptance. UNSAT is absence of every accepting branch; one rejected trace or a small trace verifier is insufficient. Deterministic FLMV cannot be applied to that existential verifier.

## Independent finite certificate

Two independent implementations use a deterministic adaptive bit-RAM whose next write address and next read address depend on earlier read values. For memory sizes $2,4,8$, all initial memories, and depths $1$ through $8$, they enumerate every candidate read vector, build its chronological trace and canonical address/time routing certificate, and check the relation.

| Control | Python | JavaScript |
|---|---:|---:|
| Source/program/depth cases | 2,208 | 2,208 |
| Candidate transcripts | 140,760 | 140,760 |
| Accepted transcripts | 2,208 | 2,208 |
| Assertions | 151,801 | 151,801 |
| Corruptions rejected | 4,417 | 4,417 |
| Digest | `3edd659a...f40d7` | `3edd659a...f40d7` |

Exactly one transcript is accepted per case and equals the operational run. Swapped routing entries, forged output and malformed non-bit source are rejected. The checkers materialize objects and use host sorting; they are not native FLMV executions, the historical $R_{\mathrm{mix341}}$ checker, or a proof-search lower bound.

## Random-access theorem compatibility ledger

| Result | Model / conclusion | Applies here? | Missing bridge |
|---|---|---|---|
| FLMV JACM 2005 | Deterministic indexed random-access TM SAT time-space lower bound | Yes, only for the same deterministic solver/machine | Need a conflicting deterministic space upper, not a trace verifier |
| Williams, _Parallelizing Time_ | Same-style random-access TM to alternating small-space / uniform circuits | Model-relevant | Alternation and circuit evaluation do not preserve deterministic time/space pair |
| TinyRAM-to-CSAT 2013 | Quasilinear satisfiability relation for guessed adaptive trace | Certificate-relevant | Acquiring trace/routing witness |
| Tri-state circuits 2023 | Quasilinear direct RAM emulation in a different dynamic circuit model | Candidate representation | Translate to FLMV machine with charged time and peak space |
| Williams 2025 square-root-space simulation | Multitape TM; special oblivious random-access schedules only | Restricted control | Arbitrary adaptive random-access extension and time preservation |
| Cook--Reckhow 1973 RAM simulation | Polynomial RAM/TM simulations under its cost conventions | General model comparison | Exact FLMV exponent/time-space preservation |

## FLMV arithmetic and finite-$N$ illustrations

For

$$
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right),
$$

$\beta(c)>0$ only for $c<1.52138\ldots$. At $c=6/5$, $\beta=23/45=1/2+1/90$. The following are exponent-only magnitudes, not bytes or proved finite-$N$ bounds:

| $N$ | $N^{1/2}$ | $N^{23/45}$ | ratio $N^{1/90}$ |
|---:|---:|---:|---:|
| $10^6$ | $10^3$ | $1.1659\cdot10^3$ | 1.1659 |
| $10^{12}$ | $10^6$ | $1.3594\cdot10^6$ | 1.3594 |
| $10^{24}$ | $10^{12}$ | $1.8478\cdot10^{12}$ | 1.8478 |
| $10^{60}$ | $10^{30}$ | $4.6416\cdot10^{30}$ | 4.6416 |

For large fixed $c$, this FLMV branch becomes nonpositive. SAT in P does not grant $c=6/5$. The transcript relation supplies no low-space upper for any $c$.

## Full cost ledger

- **Logical constraints:** $T$ local transitions, $T$ memory records, routing network and adjacent memory checks; TinyRAM source bound is quasilinear in $T$ and transition-circuit size.
- **Explicit evidence:** complete transcript, sorted copy/routing settings, registers, addresses, values and final output; $\widetilde O(T)$ bits/words under bounded word width, but not part of the original source.
- **Construction/search:** not paid by a verifier-only relation and is exactly the unresolved acquisition edge. Brute-force finite control used $2^R$ candidates.
- **Parsing/source/index/head reads:** authenticated initial source and every claimed field must be read; the test materializes them.
- **Updating/conversions:** chronological-to-routed relation, comparators, permutation constraints and word bit-blasting are charged in the relation size.
- **Verification/output:** polynomial in relation/evidence size; final output is checked, not discovered.
- **Caches/retrieval/recomputation:** host sort and materialized event lists were used in the finite test; no small-space claim.
- **Failed policies:** all rejected guessed read vectors are counted in the experimental enumerator, but this is not an ideal minimum or general search lower bound.
- **Peak space:** finite implementations store source, trace, route, sorted events and dictionaries simultaneously. No native FLMV exponent is inferred.

## Repository and continuity audit

Read current governing handoff; issue #3; root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; root `proof2.txt` blob `f8f7285677a4576b0df6e52ea2636896ca811221`; `AGENTS.md`; `CODEX.md`; repository research protocol; LSPV-2/534; LSPV-3/548; LSPV-1/551; LSPV-5/473 and /475; current Grok progress; Claude world-ledger. Required repository delta checks covered `konard/p-vs-np` README blob `0e0ec77f...`, `blkph0x/p-vs-np-proof-research` README and method index (method index blob `18d693ea...`), FRAT-XOR, CakeLPR, `openai/math` and `anthropics/formal-math`. No external repository supplies the missing same-machine deterministic acquisition bridge.

Relevant exact nodes: [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-D1], [P2-D3], [P2-C3], [P2-B1], [P2-B2]. This result materially refines the evidence/gap for [P2-A2], [P2-A3], [P2-D3], [P2-C3] and [P2-B1], without closing them.

## Status and remaining gap

- **PROVED/RESTRICTED:** exact soundness/completeness/uniqueness of the routed transcript relation for a fixed deterministic program.
- **KNOWN THEOREM:** quasilinear TinyRAM-to-circuit-satisfiability checking with auxiliary trace/routing; alternating random-access simulations; FLMV lower bound in its model.
- **COMPUTATIONAL:** two independent finite implementations and exhaustive bounded controls.
- **OPEN:** deterministic, uniform, all-input acquisition/evaluation of an arbitrary adaptive RAM trace with simultaneously FLMV-compatible time and sub-threshold peak space.

Actual advance: the near-linear sorting idea survives only as a certificate verifier. It does not repair the quadratic direct Boolean-circuit simulation or give the missing deterministic time-to-space contraction. Historical $R_{\mathrm{mix341}}$ rules/weights, roles, schedules, time zones and enabled states are unchanged. **P versus NP remains OPEN.**

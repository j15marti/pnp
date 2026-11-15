# TMR-1/051: Williams lower bounds can follow from P=NP, so their NEXP target is not an NP separation

**2026-11-15 11:57 PST | PNP Machine Model Lead | WILL-NPCLASS051**

**Status.** The conditional resource implication and restricted positive-OR query barrier are **PROVED/RESTRICTED** by the proofs below, independent mathematical review OPEN. Williams's algorithm-to-lower-bound theorem is a **KNOWN THEOREM**, not reconstructed as a project proof. The exact finite controls are **COMPUTATIONAL**. October 2026 #SAT statements remain **SOURCE-PINNED/CONDITIONAL** pending independent Lean build and paper-to-Lean audit. General circuit compression, an NP-level separation and P versus NP remain **OPEN**.

## 1. Candidate, quantifiers, and falsifiers stated before source review

**Candidate.** Assess whether a hypothetical uniform polynomial-time 3-SAT or #3-SAT solver, composed with the charged TMR-1/050 circuit-to-CNF compiler, would meet the exact all-polynomial-circuit-size Williams premise and then yield a contradiction at the NP level. Compute the final complexity class rather than treating a lower bound in NEXP or E^NP as an NP lower bound. Independently falsify the naive black-box claim that a SAT existence oracle automatically supplies polynomial-query exact counting.

**Falsifiers.** (F1) If the resulting circuit lower bound also follows when P=NP is hypothesized, it cannot on its own prove P!=NP. (F2) A source theorem about NEXP, Quasi-NP or E^NP cannot have its target renamed NP without a separate class/size transfer. (F3) DISJ has exponential x:y assignment-matrix rank and an O(k)-gate circuit, so no rank-to-general-circuit inference is legal. (F4) An oracle returning positive nonemptiness differs from unrestricted SAT over formulas permitting complementation and clever circuit rewrites; a query lower bound in the former model cannot be moved to the latter.

**Model and measures.** Let C be an explicitly encoded, shared-DAG fan-in-two Boolean circuit with n original free inputs and g gates. V=n+g counts variables in its parsimonious functional 3-CNF encoding, m<=3g+n+1 its clauses, and L=O(V log V) its serialized bits. Actual runtime is sequential deterministic bit-Turing-machine work; peak writable space is that of the same computation, not a different algorithm. For source circuit sizes g<=n^k, k is fixed before n grows. In the separate oracle control, an unknown U subset of a universe of 2^b points is exposed ONLY through positive subset-existence queries. No claim about unrestricted CNF SAT follows from that restricted oracle.

## 2. Primary sources and exact statuses

1. R. Ryan Williams, *Thinking Algorithmically About Impossibility*, CSL 2015, Theorem 2.1 (PDF p. 19, zero-index PDF page 5): **for all polynomial p**, if arbitrary n-input p(n)-size circuit satisfiability is decidable in O(2^n/n^10), then **NEXP is not contained in P/poly**. The theorem's consequence is NEXP, NOT NP. Primary: https://drops.dagstuhl.de/storage/00lipics/lipics-vol041-csl2015/LIPIcs.CSL.2015.14/LIPIcs.CSL.2015.14.pdf .
2. Vyas and Williams, *Lower Bounds Against Sparse Symmetric Functions of ACC Circuits*, Theory of Computing Systems 67 (2023), Theorem 1 **informal**: for suitable classes closed under AND, projections and composition, SAT for every n^k-size class at 2^n/n^k implies NEXP circuit lower bounds. Theorem 2 gives a different 2^{n-n^epsilon} versus 2^{n^epsilon}-size premise and Quasi-NP target, NOT NP. Source: https://link.springer.com/article/10.1007/s00224-022-10106-8 .
3. Bathie and Williams, *Towards Stronger Depth Lower Bounds*, ITCS 2024: a #SAT speedup for DeMorgan **formulas** of size n^{2+2epsilon} at time 2^{n-n^{1-epsilon}log^k n} (suitable k) implies a supercubic formula lower bound for some function in E^NP. The same paper separately gives a uniform NAND-depth SAT lower bound. Do not substitute general shared circuits, or relabel E^NP as NP. Source: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2024.10 .
4. OpenAI pinned source, openai/math commit 4eaee87548250b2682affda7d05d947c05554bae, lean/docs/378.md blob 223bbe187394bffca8a2c7ba1656538bfba26e3b: formally scoped counting time poly(L) 2^{O_k(V(loglog V)^2/sqrt(log V))} and polynomial visited cells. Its Oct 25 manuscript states sharper bounds. Independent build and equivalence audit NOT performed.
5. Anthropic pinned source, anthropics/formal-math commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/MainResults.lean blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc: definition of a SINGLE exact counter with time 2^{C min(km/sqrt(lg m),k^2V lg lg V/sqrt(lg V))}, on qualified duplicate-free, all-occurring-variable CNF. The *definitions file* explicitly says it has NO proof; separate Lean proof files claim that the defined proposition holds. No polynomial space is asserted by MainTheorem itself. Independent build NOT performed.

**Corpus reconciliation.** Read authoritative SAT compression directive (SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a) first; inspected proof1 root (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2/main root SHA metadata (930c5eeddafce656717f28055a7a9a755f44737c / 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34; their oversized contents were not delivered by this connector), AGENTS.md, CODEX.md, pnp-research skill, the five current TMR handoffs and issue #3. Compared TMR-1/050 parsimonious compiler, TMR-2/050 prefix-rank order falsifier, TMR-4/051 fixed-order OBDD transfer, TMR-5/046 Horn-expander multicut falsifier and TMR-3/049 restricted one-query same-system ledger. The present conditional class-compatibility and query-model barrier are different from /050's n+g wire-tax theorem. The root trackers/main were NOT rewritten without complete bodies. Prior /341 full UNSAT authority remains FAIL; /386 remains RESTRICTED.

## 3. New conditional consequence, fully charged

**Theorem TMR1-051-A (CONDITIONAL on ordinary 3SAT in P; PROVED resource reduction).** If one uniform deterministic ordinary 3-CNF SAT decider uses at most c(L+1)^d steps on every length-L encoding, for some fixed c,d, then for every fixed integer k>=1, arbitrary shared n-input Boolean circuits with g<=n^k gates admit an all-input deterministic satisfiability algorithm running in O(2^n/n^10) for sufficiently large n. Consequently, by Williams Theorem 2.1,

\[
\boxed{\mathrm{P}=\mathrm{NP}\quad\Longrightarrow\quad
\mathrm{NEXP}\not\subseteq\mathrm{P/poly}.}
\]

The implication also follows under the stronger assumption that exact #3SAT is in FP, but neither antecedent is known.

**Proof.** Apply the explicitly functional Tseitin compiler of TMR-1/050 to the actual shared DAG, allocating exactly one auxiliary bit to every gate ID, not to every use. It preserves satisfiability (and exact solution counts), has V=n+g variables and m<=3g+n+1 width-at-most-three clauses, and has L<=K V log(V+2) encoded bits. A conservative *bit-machine* compiler can write and naively deduplicate O(V) clauses, comparing O(log V)-bit IDs, in O(V^3) actual steps for V>=2; malformed source input parsing, output and index accesses are included. For fixed d the hypothetical SAT decider then takes O(L^d)=O(V^{2d}) steps. With q=max(3,2d)+1, there is a fixed K' such that the SAME sequential computation uses at most K' V^q steps, and no more than that many writable bits (since it makes at most one write per machine step, up to fixed encoding factors).

For g<=n^k and n>=2, V<=2n^k. Thus T(n,g)<=K' 2^q n^{kq}. For each fixed k, there exists n_k such that K'2^q n^{kq+10}<=2^n for all n>=n_k, as any fixed power is eventually dominated by 2^n. Therefore T(n,g)<=2^n/n^10 over the required size range. For the finitely many smaller n, a finite adjustment in the big-O constant suffices. The circuit translator and SAT decider are fixed finite uniform programs, and the result applies to all source circuits, including shared, reconvergent or compact affine circuits. Williams Theorem 2.1 now yields NEXP not subset P/poly. QED.

**Precise hierarchy/class firewall.** This route uses a nondeterministic exponential-time hierarchy *inside Williams's original theorem*. It does not exhibit a hard language in NP. In the assumed P=NP world, NP=P is contained in P/poly by uniform computation-to-circuit simulation. Hence the NEXP lower bound is perfectly compatible with the antecedent P=NP, and cannot be promoted to NP not subset P/poly or P!=NP.

**Bathie-Williams class audit.** If P=NP, an E^NP computation taking 2^{cn} steps makes at most 2^{cn} queries of length at most 2^{cn}; replace each NP oracle call by its fixed polynomial-time deterministic decider, costing at most 2^{O(n)} for all calls together. Hence under P=NP, **E^NP=E**. A conditional Bathie-Williams formula lower bound for E^NP would then be an E lower bound, still not an NP lower bound. This is not a claim that the Bathie-Williams premise has been achieved.

## 4. Independent restricted query-model barrier

**Theorem TMR1-051-B (PROVED/RESTRICTED).** Let X={0,1}^b have N=2^b points. An unknown U subset X is accessed by queries

\[
Q_U(S)={\bf1}[S\cap U\ne\varnothing]
\]

for any arbitrary S subset X, chosen adaptively with zero charge for specifying S. Every deterministic algorithm that correctly outputs |U| for all U must make at least N queries on U=X. In particular, even an overpowered *positive-only* existence oracle does not yield a polynomial-query black-box exact counter in this model.

**Proof.** Compare U_*=X against U_j=X\setminus{j} for each j. For S empty both answers are 0. For |S|>=2 both answers are 1, because removing one point cannot empty S. For |S|=1, answers differ only when S={j}. Thus if a correct deterministic adaptive machine on U_* does not ask singleton {j}, its complete transcript is identical on U_j; it must output two distinct cardinalities but cannot. It must therefore ask all N distinct singleton queries on U_*. QED.

A randomized bounded-error algorithm also needs Omega(N) positive queries in the worst case: under the distribution selecting U_* with probability 1/2 and uniformly random U_j otherwise, at most q/N of the missing-point cases can be distinguished by q singletons along the all-ones transcript. Success probability is at most 1/2+q/(2N); reaching 2/3 requires q>=N/3. This is a Yao-style distributional restricted-oracle calculation, NOT a general randomized SAT-oracle separation.

**Scope falsifier.** Allowing the different query \(\exists x[\neg{\bf1}_U(x)]\) distinguishes these two input types in ONE query. General SAT circuit constructions can negate a circuit's output, and a SAT oracle acts on syntactic formulas rather than only this opaque positive-membership interface. Consequently TMR1-051-B does **NOT** prove that FP^SAT fails to contain #SAT, nor that P=NP cannot imply FP=#P. Its only valid role is to block an uncharged *positive-existence-enumeration* counting compiler.

## 5. Four mandatory gates

| Gate | Status | Reason |
| --- | --- | --- |
| DISJ sanity | **PASS** | No static cut-rank lower bound. DISJ_b admits O(b) shared circuits; the conditional circuit translator and all explicit shortcuts apply. TMR-5/046 Horn expander remains a hostile control. |
| Relativization/algebrization/Natural Proofs | **PASS restricted / OPEN unrestricted** | Tseitin compiler and positive-OR indistinguishability are syntactic and relativizing scoped lemmas. Williams's nontrivial implication depends on ordinary succinct witness verification/hierarchy and correct class semantics; it cannot be assigned unchanged to arbitrary oracle gates. No fully relativizing P-vs-NP proof is asserted. No new constructive large Boolean hard property is claimed; unrestricted algebrization/Natural Proofs audit stays OPEN. |
| Simultaneous DTISP | **NOT APPLICABLE to Williams/Bathie lower-bound target; OPEN for FLMV** | One actual compiled SAT algorithm has both T<=K'V^q and S<=O(T) (not separate machines). This is not a simultaneous forbidden near-linear/sublinear-space pair. No all-input FLMV or Allender transfer is claimed. |
| Configuration counting | **PASS consistency only** | A total deterministic finite-alphabet read-only-input machine using s writable cells on N input bits has T<=2^{O(s+log N)} (if s>=log N, T<=2^{O(s)}). This is an upper bound and gives no lower bound. Our conditional polynomial work/spaces do not violate it. The separate oracle model is not asserted to be a conventional SAT tape machine. |

## 6. Same-realization resource ledger and experiment

For Theorem A, sequential stages: read and parse original n-input/g-gate source; allocate one identity per shared gate; produce, sort and deduplicate O(g+n) clauses of length <=3 with O(log V)-bit IDs; materialize O(V log V) source bits; invoke the ONE supposed polynomial SAT decider on this actual encoding; parse its Boolean output; halt. All construction, source access and output work is inside the O(V^q) bound; writable live space <=O(V^q) follows from the SAME machine/time bound, not from a separate small-space solver. No approximate count, interpolation, multiple parallel machines or network span is substituted. For Theorem B, queries are unit-cost and even query descriptions are free; the restriction is the oracle language, not an uncharged SAT algorithm.

The separately executed CPython script enumerated EVERY query subset for N=2,4,8,16 and each one-element deletion. There were 1,050,696 exact query answer comparisons and 12 exact integer crossover checks, **1,050,708 checks, zero failures**. The crossover checks test the symbolic illustration (n+n^k)^q n^10<=2^n at powers-of-two n for k=1..4, hypothetical d=1..3, q=max(3,2d)+1, and leading constant K=1. They are finite **COMPUTATIONAL**, do not establish asymptotics, do not infer any actual SAT solver, and have no random seed.

**Artifacts:** executable experiments/tmr/tmr1_williams_npclass051.py; exact JSON results/raw/tmr/2026-11-15_1157_TMR1_WILL_NPCLASS051_RAW.json. The script's original run is CPython 3, no optional packages, no network. No local repo checkout or preflight command execution was possible in the constrained tool session; the GitHub preflight instructions were consulted and content/metadata reconciliation performed.

## 7. Dependency ledger and next exact lemma

\[
\text{P=NP [HYPOTHESIS]}
\Longrightarrow \text{uniform poly-size Circuit-SAT [PROVED CONDITIONAL]}
\Longrightarrow \text{Williams all-size savings [PROVED CONDITIONAL]}
\Longrightarrow \text{NEXP not in P/poly [KNOWN CONDITIONAL THEOREM]}.
\]

The final implication to \(\mathrm{NP}\not\subseteq\mathrm{P/poly}\) is **NOT VALID** from this chain, because under the very antecedent \(\mathrm{NP}=\mathrm P\subseteq\mathrm{P/poly}\). Bathie-Williams has an E^NP formula target, with another circuit-model premise. An independent NP-level implication needs an additional hypothesis or a new nonrelativizing theorem explicitly incompatible with P=NP. This is the **weakest next lemma**: specify one algorithmic premise for a *restricted* circuit family whose consequence is an explicitly NP-computable function lacking those circuits, without falsely deriving NP circuit hardness from arbitrary polynomial-time Circuit-SAT. Quantify every size, wire, encoding and saving parameter before applying an algorithmic-method theorem.

TMR-2/4: check DISJ, Horn expander, affine circuits and every claimed crossing from tensor compression to arbitrary Circuit-SAT. TMR-3: if any Track B/FLMV transfer is proposed, demand one exact execution meeting both forbidden exponents, not an E^NP or NEXP lower-bound statement. TMR-5: independently audit Theorem 2.1's all-polynomial-size quantifier, Theorem B's positive-query restriction, and the P=NP consistency firewall.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** Root proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2 SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34. No root changes, no task or agent schedule changes. **P versus NP OPEN.**

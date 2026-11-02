# LSPV-1 DECISION-WITNESS-MINIMAX313: a sharp randomized decision-only certification firewall

**November 1, 2026, 17:00 PST. PROVED/EXACT restricted classical adversary; COMPUTATIONAL independent finite controls; external review pending. P versus NP OPEN.**

## Obstruction and four falsifiable statements

The decision-only SAT output is one bit. A lower bound cannot charge an arbitrary decider for recovering original variable assignments, emitting an explicit SAT witness, constructing injective pin keys, or producing a fixed UNSAT proof unless those are actually required by the machine's declared contract.

F1: an independently pinned, always-SAT authenticated promise forces a decider to read its pins. **False**: zero pin-value probes suffice. F2: the same promise admits exact zero-query **explicit-witness extraction**. **False**, a sharp linear lower bound below. F3: the randomized extraction cost is necessarily the same as the deterministic tariff. **False**, the exact bounded-error minimax is derived below. F4: this restricted query separation proves any all-input superpolynomial lower bound or an FLMV forbidden-region intersection. **Invalid**: neither follows.

## Authenticated canonical source and same-original SAT/UNSAT controls

The F9 valid duplicate-free proper Döcker monotone 3-SAT-(2,2) original contains positive supports (156),(238),(135),(469),(247),(789) and negatives of (468),(167),(234),(358),(129),(579). Every original variable occurs twice in each polarity, and every clause is distinct and has three distinct same-sign literals. Its 70 satisfying assignments split as **34** with x5=0 and **36** with x5=1. Explicit source-clause-checked nine-bit witnesses are w0=001001100 and w1=000011110.

For t>=1, let F_t be t variable-disjoint original-source copies of F9, still a valid canonical target original. The additional *external* coherent pin-word promise b in {0,1}^t fixes exactly one original variable per block, x_(9(i-1)+5)=b_i. Every promised residual is SAT, with exact #SAT=34^(t-|b|)*36^|b|. This pin-word promise must not be mistaken for an unpinned all-input canonical instance.

Two opposite-label **residuals of the same original F9** remain adversarial controls: source-coherent pS={x1=0,x3=0,x5=1,x6=0,x7=0,x8=0} has two satisfying completions, while pU changes only x1=1 and has zero. The eight complete pU leaves each falsify an original source clause. Malformed binaries remain rejected by the target-language validator.

## Theorem 313A: exact deterministic decision/witness pin-query separation

For all t>=1, the promised SAT/UNSAT **decision** can output SAT after **zero pin-value queries**. Every deterministic exact **explicit-witness extractor**, which must output the actual 9t bits of a satisfying extension of b, must read **all t** independent pin-value positions on **every b**. This bound is attained by reading each b_i once and concatenating w_(b_i).

*Proof.* The promise is always SAT. If a purported correct extractor fails to observe b_i on a run, its physical observation transcript and output remain identical after the single-bit change b xor e_i, so the output position for the original pinned variable cannot simultaneously equal 0 and 1. Contradiction. QED.

A symbolic command "copy the pin later" is not a materialized explicit witness: its later read and output operations must be charged. An all-input algorithm cannot claim to skip grammar/source authentication from this promise experiment. Pins already known because the solver itself created them are not separately charged as external input reads.

## Theorem 313B: exact randomized minimax witness-query work

For any t>=1 and 0<=epsilon<1/2, let R be any randomized explicit-witness extractor correct for **every** b with probability at least 1-epsilon. Count distinct physical pin positions read by R as Q_R(b). Then

\[
\boxed{\inf_R\max_b\mathbb E[Q_R(b)]
=t\left(1-\frac{\epsilon}{1-2^{-t}}\right).}
\]

*Proof of lower bound.* Draw B uniformly in {0,1}^t, independently of the coins. Conditional on any adaptive transcript, including random coins and the queried pin-value outcomes, the U=t-Q unqueried pin values remain independent unbiased bits. An explicit printed witness agrees with every unqueried mandatory variable with probability at most 2^-U. Thus epsilon >= E[1-2^-U]. Concavity of 1-2^-u on [0,t] gives

\[
1-2^{-u}\ge (u/t)(1-2^{-t}),
\]

so E Q >= t(1-epsilon/(1-2^-t)). Therefore some b attains at least that expected cost.

*Matching algorithm.* With probability p=(1-epsilon-2^-t)/(1-2^-t), query all t pins and print checked templates. Otherwise query none, choose a uniformly random guessed pin profile, and print its templates. On **every** actual b the success probability equals p+(1-p)2^-t=1-epsilon and the expected queries equal tp. This proves exact minimax equality. For t=5, epsilon=1/3 the minimum is 305/93 expected pin reads. QED.

This is a new **scoped exact adversarial comparison** within the project, not a general computational lower bound or new method surpassing classical decision-tree arguments. An explicit 9t-bit output also incurs Omega(t) physical write operations under a one-bit-per-step output model, but it need not occupy Omega(t) simultaneous writable memory when streamed.

## Precise all-input adaptive decision controller schema

Let L be the language of satisfiable valid duplicate-free proper Döcker monotone 3-SAT-(2,2) binary originals; malformed strings are NO. An all-input decider D is a **single computable deterministic algorithm** fixed independently of the input, with source-indexed state z=(F,p,R,theta,policy-history,proofs,cache). The acquired, not free, parameter vector may include free-support f, uncovered-clause count u, signed eta, authenticated packed odd cycles nu, delta=2f-u-eta-nu, affine rank, boundary width and paid selection/discovery costs. A decision-only terminal may emit the label if its semantic subroutine is proved exact; emitting a full witness/proof is a separate stronger, fully charged option.

For a serialized exact source-authenticated AND/OR run, define c(z) to include *every* local machine transition spent on source/grammar/index/head, certificate and semantic quotient discovery, **all failed policies**, selection/switching, GE/matroid/proof work, cache/replay, guest DELAY/COPY/RECOMP, output and restoration. With actual executed children,

\[
W_D(z)=c(z)+\sum_{y\in\mathrm{ExecutedChildren}(z)}
 (c_{\mathrm{child}}(z,y)+W_D(y)).
\]

Both alternatives of a necessary OR must be evaluated to establish UNSAT; a correct SAT answer can terminate on one true branch. Truly independent AND components require every SAT child for SAT and one UNSAT child for UNSAT. A full-source fallback remains exact; each recursive branch pins at least one previously free original variable (or enters a smaller nonempty independent component), providing a well-founded f measure despite delta increasing. Completeness does **not** bound the **sum** of executed child work polynomially. Peak space is max_t of all simultaneously live physical writable/index/head/ancestor/cache/guest/proof/output material, not logical state XOR.

The exact constructive quantifier target is:

\[
\exists D\exists c\exists C>0\ \forall x\in\{0,1\}^*:
   D(x)=[x\in L]\ \land\ W_D(x)\le C(|x|+1)^c.
\]

This would prove P=NP. To prove P!=NP by unrestricted work, it would instead suffice to establish for **every** correct D, **every** c and **every** constant C>0, arbitrarily large valid target inputs on which W_D(x)>C(|x|+1)^c. This run proves **neither**. The source-pin promise is not an unpinned all-input lower bound.

## Canonical decision-to-witness conversion has paid unknown-K costs

A target-pinned residual is in NP, hence *some* uniform polynomial-time many-one normalizer R to the canonical NP-complete target exists. If the canonical output has length O(N^d), normalizer time O(N^a), and a hypothetical arbitrary correct target decider A has time O(M^K) with unknown finite K, the standard (n+1)-call SAT self-reduction yields a conservative witness-generation time

\[
O((n+1)(N^a+N^{dK})+nN).
\]

This is a classical polynomial search-to-decision reduction, **not** a power-short arbitrary-A compiler. A target-valid child normalizer's exact bit-addressability and native peak-space costs remain missing for the quantitative FLMV route. The earlier project PROOF-SYSTEM-FALLBACK163 already handles Cook-Reckhow: all-UNSAT polynomial certificates have their own NP=coNP boundary and cannot give free favorable exponents.

## Reproducible independent controls and true work

The expanded no-producer-import checker passed **6,925 assertions** against a separately written producer: exact F9=70 models, 34/36 x5 split, checked concatenated witnesses for all 16 pin profiles at t=4, same-source F9 SAT=2 and UNSAT=0 completions, an eight-leaf falsified-original-clause UNSAT cover, 264 SS/SU/US/UU clause-pair modes, 6144 complement-clause identities, all 12 local original-clause occurrence S/U targets and inversions, complete 0^9/1^9 clause histograms, actual flip trails, malformed controls and 21 exact rational randomized minimax cases. Source UP-DPLL required one node and 40 literal probes on the SAT cube, one node and 34 probes on the UNSAT cube. Neither finite test establishes a general runtime improvement. The repository compact producer and separate independent compact checker reproduce the central theorem and controls. The full expanded tests, original source data, original-occurrence extrema and raw JSON are in the conversation reproducibility archive. Logical XOR remains OFFLINE only.

## Primary and repository search/readback audit

Primary web literature searches: "SAT self reducibility search to decision n oracle calls", "Cook Reckhow NP coNP proof systems", "Döcker Monotone 3-SAT-(2,2) NP complete", and "Fortnow Lipton van Melkebeek Viglas time space lower bounds". Sources: Döcker (2019) https://arxiv.org/abs/1912.08032; FLMV JACM (2005) https://doi.org/10.1145/1101821.1101822; Cook-Reckhow (1979), described in Stanford Encyclopedia of Philosophy, Spring 2026 https://plato.stanford.edu/archives/spr2026/entries/computational-complexity/; classical SAT self-reduction lecture https://www.csa.iisc.ac.in/~chandan/courses/complexity20/lectures/lec3.pdf .

Project GitHub searches: "decision witness certificate output", "self reducibility decision witness", "Cook Reckhow NP coNP proof". Relevant prior PROOF-SYSTEM-FALLBACK163, SAT-OUTPUT-COMPOSITION1, DECISION-WORK-ONLY307, DIRECTSUM312, GATE312 and REFEREE274 were explicitly compared. Independent github.com/openai searches "SAT solver self reduction certificate" and "proof checking SAT" returned files in openai/math including lean/OAI/Algorithms/SubexponentialSAT/RuntimeAssembly.lean, which explicitly declares implementation certificates **unconstructed**. No completed primitive-machine result may be inferred from these conditional structures. Absence of a matched prior search result is not evidence of novelty.

**Unproved:** polynomial total decision work on *every* target original, target-valid hereditary power-short Phi(A) for unknown exponents, strict native same-machine FLMV reduction/transfer, either P=NP or P!=NP.

\`END_OF_VERIFIED_REPORT::LSPV1::DECISION_WITNESS_MINIMAX313::P_VS_NP_OPEN\`

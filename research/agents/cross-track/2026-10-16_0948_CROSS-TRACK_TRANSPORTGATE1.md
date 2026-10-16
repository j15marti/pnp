# CROSS-TRACK-TRANSPORTGATE1: A Charged Trace-to-Resolution Barrier

**Timestamp:** 2026-10-16 09:48 Asia/Seoul (2026-10-16 00:48 UTC).  
**Agent:** CROSS-TRACK SYNTHESIS / hostile integration.  
**Status:** \(P\) versus \(NP\) **OPEN**. New statements here are scoped lemmas, not a separation.

## 0. Frozen pre-search integrations

The following candidates were fixed before consulting new outputs or literature.

1. **TRANSPORT-CHARGE:** Combine LSPV-1's fully charged source/child accounting with LSPV-2's proof-system hardness. Target a specific decider-to-proof compiler, not a generic "DAG implies exponential time" inference. Try to falsify its strongest plausible version on affine parity instances.
2. **UWI-QUOTE-WRAPPER:** Combine LSPV-3's same-input UWI / bounded status quotation with LSPV-4's clocked hash wrapper. Test whether a verified completion-time transcript forces a common satisfiable hard input or a nonrelativizing contradiction. Counter-model: a truth-correct, early-answer oracle with a replayable event stream.
3. **META-LIFT + LOCAL-SPACE:** Combine the new polylog-space succinct-lifting lemma with LSPV-1's virtual-source ledger. Candidate: deterministic low-space MOCSP reduction without an explicit hard truth table. Rejection controls: coherent randomness, self-succinctness, and whether the conclusion is \(P\ne PSPACE\) rather than \(P\ne NP\).

**Selection after search:** candidate 1 has the strongest exact falsifier and the most concrete next missing implication. Candidate 2 is blocked by oracle replay and quantifier inversion. Candidate 3 is conditional on a currently unavailable deterministic MOCSP reduction and does not directly settle \(P\) versus \(NP\).

## 1. Sources actually read

**Four specialist outputs (latest substantive items located):**

- Resource Contraction, LSPV-1: [WRAPPER_COVERAGE2](../../agents/lspv-1/2026-10-16_LSPV-1_WRAPPER_COVERAGE2.tex) and [WRAPPER_ACCESS1](../../agents/lspv-1/2026-10-16_0016_LSPV-1_WRAPPER_ACCESS1.tex). Restricted exact hash-equality guard, paid canonical comparisons, source-offset construction, and streaming interleave space lower bound. All-input hereditary \(K\)-independent contraction remains OPEN. Two-bit hashes had opposite-status collisions in finite tests.
- Proof Transport, LSPV-2: [PARITYPULLBACK1](../../agents/lspv-2/2026-10-15_1712_LSPV-2_PARITYPULLBACK1.tex) and [SEMANTICORBIT1 handoff](../../agents/lspv-2/2026-10-15_1218_LSPV-2_SEMANTICORBIT1_LSPV5_HANDOFF.md). The \(2^{n-1}\) source-only affine inequality count for odd parity is sharply defeated by a linear XOR-gate 3-CNF extension and by a linear-size two-state flow extension. Arbitrary decider \(\to\) semantic CP proof is OPEN; RS5 normalized-spread hypothesis (H) is CONDITIONAL.
- Universal Obstruction, LSPV-3: [STATUSQUOTE8](../../agents/lspv-3/2026-10-15_2235_LSPV-3_STATUSQUOTE8.tex). Clocked computation CNFs reify status with polynomial size given a polynomial decider, but double status negation is not a fixed point. No uniform unclocked all-program quotation translator; four fixed witness programs may fail individually with no common hard source.
- Nonrelativizing Simulation: [ORACLEREPLAY1](../../agents/nonrelativizing-simulation/2026-10-16_0018_NONREL-SIM_ORACLEREPLAY1.tex) and [handoff](../../review/outbox/nonrelativizing-simulation/2026-10-16_0018_ORACLEREPLAY1_HANDOFF.md). A fully explicit polynomially bounded deterministic wrapper with charged states, scheduler, ticks, hashes, emitted children and external events can be replayed in \(P^O\) for every oracle \(O\), given its realized events; choosing \(O=\mathrm{TQBF}\) collapses \(P^O=NP^O\). No nonrelativizing hinge established.

**Other project sources:** newest [META-LIFT2](../../main/2026-10-16_0721_MAIN_META_LIFT1.md), [governance](../../governance/2026-10-14_0930_FIVE-TRACK-ACTIVATION1.md), GitHub recent commit history, project-chat retrieval on source certificates and resource costs, Google Drive [MAIN V2](https://docs.google.com/document/d/1Tp81jmv02__cGtimZ6ILAYpEt6A7HZXqj8FZ2rkGaSo/edit) and its predecessor. The located Drive MAIN volumes are historical (last modified September 29); current specialist files in GitHub were treated as fresher evidence. We did not overwrite an older Drive MAIN.

**Primary literature targeted to the hypotheses:** Cook–Reckhow [1], Ben-Sasson–Wigderson [2], Filmus–Hrubeš–Lauria [3], Baker–Gill–Solovay [4], Allender–Holden–Kabanets [5]. These substantiate proof-system relativity, the Tseitin/Resolution lower-bound mechanism, semantic-CP distinctions, the oracle control, and the conditional meta-complexity route.

## 2. Exact construction: cubic Tseitin inputs

Let \(G=(V,E)\) be a connected 3-regular undirected graph, \(n=|V|\), \(m=3n/2\), and \(b:V\to\{0,1\}\) be a charge vector.

Put one Boolean variable \(x_e\) on each edge and require at each vertex \(v\)

\[
\bigoplus_{e\ni v}x_e=b_v.
\]

Each degree-three parity equation is encoded by its four forbidden local assignments, one proper width-three clause each. Call the resulting **unextended** CNF \(T(G,b)\). It has \(m\) variables and \(4n\) clauses.

### Lemma A (exact linear-time promise decider)

For connected \(G\),

\[
T(G,b)\in SAT \iff \bigoplus_{v\in V}b_v=0.
\]

If the total charge is even, the number of satisfying edge assignments is exactly

\[
2^{m-n+1}.
\]

**Proof.** XOR all vertex equations: every edge appears twice and cancels, so odd total charge is impossible. For even charge, fix a spanning tree and set non-tree edge variables to zero; process non-root vertices from leaves to root to solve each tree edge. The root equation holds because the total charge is even. The incidence matrix has rank \(n-1\) over \(\mathbb F_2\), giving \(m-n+1\) degrees of freedom. \(\square\)

For the promised input pair \((G,b)\), a deterministic decider \(A_\oplus\) checks connectivity, degree-three incidence, and charge parity and answers SAT/UNSAT in polynomial time, in fact linear-time graph operations with an ordinary indexed adjacency representation. On YES inputs it emits a satisfying edge assignment by the spanning-tree construction. The explicit CNF generator and recognizer are polynomial-time. Thus all generation, source parsing, input validation, and witness acquisition are paid, not treated as free oracles.

### Known hard family

Take a family of connected constant-expansion cubic graphs \(G_n\) and choose any **odd** charge \(b_n\).

By standard expander-Tseitin width lower bounds and the Ben-Sasson–Wigderson width/size relation [2], every ordinary Resolution refutation of

\[
F_n=T(G_n,b_n)
\]

has

\[
\operatorname{ResSize}(F_n)\ge 2^{c n}
\]

for a constant \(c>0\) depending on the expansion parameters.

With explicit variable identifiers, the source encoding size is \(N=\Theta(n\log n)\); the lower bound in source bits is at least \(2^{\Omega(N/\log N)}\). This is a **Resolution lower bound**, not an unrestricted decision-time lower bound.

### Lemma B (charged promise-local proof transport impossibility)

Let \(C\) be any deterministic compiler which, on input \(F_n\), an exact execution transcript of \(A_\oplus\) on \((G_n,b_n)\), and any polynomial-length wrapper/hash/event log, must **explicitly emit an ordinary valid Resolution refutation of the same unextended \(F_n\)**. Then

\[
T_C(F_n,\operatorname{trace}(A_\oplus),\operatorname{events})
  \ge 2^{c n}
\]

in every bit-output machine model charging at least one step per emitted proof symbol, for all sufficiently large \(n\).

**Proof.** Any accepted explicit output is a Resolution refutation of \(F_n\), hence contains at least \(2^{c n}\) proof lines, and therefore at least that many output symbols. The output bound holds regardless of how rapidly \(A_\oplus\) decides, how the wrapper hashes the trace, or what legal event sequence was observed. Additional costs for source reads, canonicalization, proof checks, state snapshots, random bits, recursion and buffer construction are nonnegative and cannot eliminate the output lower bound. \(\square\)

**Meaning.** A perfectly correct, polynomial-time **promise-family** SAT/UNSAT decider exists on these very instances, while an explicit Resolution proof-transport compiler for the same instances requires exponential output. This falsifies any claimed transfer whose only hypothesis is "the decider is correct and fast on this hard family" or whose proof relies solely on a status bit / local transcript. It does **not** refute a hypothetical all-CNF transport theorem that essentially uses the decider's correctness on inputs *outside* this promise family.

## 3. The exact conditional proof-system bridge that does survive

Assume, *only for a conditional argument*, that \(P=NP\) and a fixed uniform total SAT decider \(D\) runs in time \(T_D(N)\le N^K\).

Define \(Q_D(F,\pi)\) to accept exactly when \(\pi\) is a fully specified accepting UNSAT trace of \(D(F)\), with each transition, access, endpoint and output bit checked. A naive entire-configuration transcript of \(T\) steps occupies \(O(T^2)\) cells/bits on a standard multitape model, and can be generated and checked in \(T^{O(1)}\) time. A more efficient streaming check is optional, not assumed.

### Lemma C (conditional trace certificates)

Under the hypothesis that \(D\) is a correct polynomial-time SAT decider, \(Q_D\) is a sound, complete, polynomially bounded certificate system for UNSAT CNFs.

**Proof.** A correct deterministic computation rejecting \(F\) has a checkable polynomial-size trace whenever \(F\) is UNSAT. A valid deterministic trace ending in rejection cannot exist on satisfiable \(F\), because \(D\) is assumed globally correct. Source reads and transition verification are explicitly included in the polynomial verifier. \(\square\)

This is an instance of the Cook–Reckhow landscape [1]. It gives short certificates in a **new verifier-dependent proof system**; it does not give short Resolution, bounded-fan-in semantic Cutting Planes, PC/PCR, SoS, or d-DNNF objects.

To use any lower bound for a specific proof system \(R\), a genuinely new transport theorem would have to provide

\[
Q_D(F,\pi)\Rightarrow
\exists\,\rho\in R(F)
\text{ with }|\rho|\le \operatorname{poly}(|F|+|\pi|)
\]

and an explicitly charged procedure for obtaining or verifying \(\rho\), with the correct same-instance encoding.

For odd expander Tseitin formulas such a polynomial transport to ordinary Resolution is incompatible with the known Resolution lower bound under the hypothetical \(D\). Consequently **establishing that all-CNF transport from global correctness would itself separate \(P\) and \(NP\)**. This missing implication cannot be silently inherited from Cook's bounded tableaux or restricted proof-system lower bounds.

## 4. Three hostile cross-track audits

### 4.1 UWI retains same-input quantifiers

The desired obstruction has the form

\[
\forall\text{ fixed polynomial bound }p(\cdot)\
\exists\ F\in SAT:\quad H(F)>p(|F|),
\]

equivalently no common polynomial bound over all satisfiable inputs. In a portfolio argument, an attempted transition from

\[
\forall p_i\ \exists F_i:\operatorname{fail}(p_i,F_i)
\]

to

\[
\exists F\ \forall p_i:\operatorname{fail}(p_i,F)
\]

is invalid.

The parity promise family is an especially hostile control: **all even-charge instances admit a uniform polynomial-time witness constructor**. Therefore a hard Resolution family on the odd-charge side does not induce a UWI obstruction on the even-charge satisfiable side. Under an assumed total \(D\), standard search-to-decision would also construct SAT witnesses with polynomially many charged calls.

### 4.2 WRAPPER has no automatic nonrelativizing hinge

The ORACLEREPLAY1 theorem already covers polynomial-clock, explicitly replayable hash/scheduler/event wrappers. Relative to \(O=\mathrm{TQBF}\),

\[
P^O=NP^O=PSPACE.
\]

The oracle can answer the SAT-relevant requests directly; later clock ticks, hash chains and successor encodings remain replayable with full costs charged. If an external physical random stream is not modelled as supplied input/events, there is no ordinary uniform SAT reduction to which classical complexity bounds apply. If it *is* supplied, no nonrelativizing bottleneck has been shown.

The \(\mathrm{TQBF}\) control is not a replacement for studying all oracles. It is one explicit collapsing oracle which every purported relativizing separation argument must survive.

### 4.3 Resource contraction cannot hide compiler output

Let \(W_A\) be decider work and \(W_C\) the charged compiler work, including source rereads, event generation, retained indices, canonicalization, proof construction, verification and recursion. For this family,

\[
W_A=\operatorname{poly}(n),
\qquad
W_C\ge 2^{c n},
\]

if the artifact demanded from \(C\) is explicit ordinary Resolution.

An assertion that the compiler emits an O(n)-size parity certificate or compressed proof changes the target proof system. To use the Resolution lower bound, the representation must be decoded into ordinary Resolution with decoder time/output fully charged. Otherwise the lower bound is inapplicable.

## 5. Reproducible finite checks

Script: [TRACE-TRANSPORT1 audit](./2026-10-16_0948_CROSS-TRACK_TRANSPORTGATE1_audit.py), Python standard library only; SHA-256 of the executed local script: \`e0db7061530a82f4096d9070b688b4deebfe05b4316d8241bd4a2353974aacc6\`. Stored results: [JSON](./2026-10-16_0948_CROSS-TRACK_TRANSPORTGATE1_results.json).

The script constructs width-3 Tseitin clauses and exhaustively checks the complete Boolean edge cube for four connected cubic graphs:

| Graph | \(n\) | Edge variables | Clauses | # models, even | # models, odd |
|---|---:|---:|---:|---:|---:|
| \(K_4\) | 4 | 6 | 16 | 8 | 0 |
| Triangular prism | 6 | 9 | 24 | 16 | 0 |
| Cube \(Q_3\) | 8 | 12 | 32 | 32 | 0 |
| Petersen | 10 | 15 | 40 | 64 | 0 |

Total explicit edge assignments checked: **74,880**. Additional randomized charge vectors checked: **80**. All matched the exact parity criterion and the spanning-tree witness algorithm.

An independent same-input UWI audit enumerated all **256** subsets of the eight distinct non-tautological unary/binary clauses on two variables. Exactly **95** are satisfiable. Each of four fixed assignment-output programs fails on **63** satisfiable formulas, but **zero** satisfiable formulas fail all four. This exhibits the quantifier inversion trap in the smallest transparent setting.

**Finite-check limitation:** the graphs above are *not* asserted to establish an asymptotic expander family. The Resolution exponential bound is imported from [2] and graph expansion; no asymptotic result is inferred from the finite tests. Counts are COMPUTATIONAL, code awaiting independent review.

## 6. Explicit proof DAG

\`\`\`text
E1  [PROVED/EXACT]      Connected Tseitin SAT iff total charge even
E2  [PROVED/EXACT]      Promise-family decider and YES witness are polytime
E3  [KNOWN THEOREM]     Cubic-expander odd Tseitin Resolution >= 2^{Omega(n)}
E4  [PROVED/EXACT]      E2 + E3 => promised trace-to-explicit-Res compiler
                        requires exponential charged output (Lemma B)
E5  [CONDITIONAL]       P=NP => total polynomial SAT decider D
E6  [CONDITIONAL]       E5 => poly-size D-trace UNSAT certificates Q_D
E7  [OPEN, LOAD-BEARING] E6 => polynomial SAME-INPUT Resolution/CP/PC
                         transport with source-verified proof and full costs
E8  [PROVED/EXACT,
     RESTRICTED]        Poly-clock explicit WRAPPER logs replay relative to O
E9  [KNOWN THEOREM]     O=TQBF makes P^O=NP^O
E10 [OPEN]              Genuine nonrelativizing and nonalgebrizing hinge
E11 [OPEN]              All-input hereditary K-independent charged contraction
E12 [OPEN]              Common-input UWI obstruction, no quantifier inversion
E13 [CONDITIONAL]       META-LIFT polylog-space reduction would imply P!=PSPACE
                        (not directly P!=NP)
ROOT [OPEN]             P!=NP
\`\`\`

The branch \(E1+E2+E3\to E4\) is a **barrier result**. It does not point to ROOT. The putative path \(E5\to E6\to E7\to E3\) would contradict the lower bound only if the currently OPEN \(E7\) were proved in full. No such proof is present.

## 7. Priority and assignments to four specialists

**Single highest-value next implication:** determine whether arbitrary **globally correct** polynomial SAT computation forces any polynomially bounded ordinary proof-system object on *the same expander-Tseitin input*, rather than merely a \(D\)-trace certificate. Seek a source-grounded nonrelativizing statement that is not already falsified by the parity promise decider and not just a reformulation of the separation conjecture.

**Resource Contraction (LSPV-1):** Write an explicit model-matched ledger for any proposed \(\tau_D\): source generation, every child query, RAM address, trace acquisition, witness normalization, proof emission, verifier, recursion. Test padding \(D\mapsto\operatorname{DELAY}_{n^d}(D)\); no \(K\)-independent improvement may be claimed unless padding is normalized with a proved cost.

**Proof Transport (LSPV-2):** Specify one concrete target proof system, preferably ordinary Resolution first and semantic CP separately. Propose a transport hypothesis with exact input/output representation, quantifiers, and polynomial blowup, then attack it using cubic expander Tseitin, the 4n-clause XOR encoding, parity-flow extensions, and known FHL proof-system separations. Mark any hypothesis that already implies \(P\ne NP\) as an OPEN main theorem, not a technical lemma.

**Universal Obstruction (LSPV-3):** Test whether the proposed transport actually yields a **common satisfiable input** failure in UWI. Use fully quantified program bound \(|p|\le b(n)\), one same \(F\), and charge all search-to-decision restrictions. Reject any inference based on separate \(F_p\), double status quotation, or clock padding alone.

**Nonrelativizing Simulation (LSPV-4):** Give the same transport/wrapper mechanism a maximally strong \(O=\mathrm{TQBF}\) oracle, allowing exact SAT answers and coherent transcript replay. Identify the single predicate the oracle cannot replicate under a source-grounded, **proved** resource/semantic constraint. If none survives, certify the route as relativizing rather than upgrading hash length or timing complexity.

## 8. References (primary)

[1] S. A. Cook and R. A. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, Journal of Symbolic Logic **44** (1979), 36–50. https://doi.org/10.2307/2273702

[2] E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM **48** (2001), 149–169; ECCC TR99-022. https://eccc.weizmann.ac.il/report/1999/022/

[3] Y. Filmus, P. Hrubeš and M. Lauria, *Semantic Versus Syntactic Cutting Planes*, STACS 2016, DOI: 10.4230/LIPIcs.STACS.2016.35. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2016.35

[4] T. Baker, J. Gill and R. Solovay, *Relativizations of the P = ? NP Question*, SIAM Journal on Computing **4** (1975), 431–442. https://doi.org/10.1137/0204037

[5] E. Allender, D. Holden and V. Kabanets, *The Minimum Oracle Circuit Size Problem*, Computational Complexity **26** (2017), 469–496; STACS 2015. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2015.21

**Final classification:** The four-track synthesis closed a restricted promise-family transport obstruction and produced an explicit charged countermodel to proof-lower-bound \(\Rightarrow\) unrestricted SAT-time reasoning. It did **not** close the all-CNF proof-transport arrow, create a nonrelativizing hinge, or prove \(P\ne NP\).

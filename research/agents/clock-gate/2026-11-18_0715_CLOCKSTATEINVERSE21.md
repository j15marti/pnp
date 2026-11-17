# CLOCKSTATEINVERSE21: Conditional canonical sections for globally stateful, address-dependent streaming quotients

Date: 2026-11-18 07:15 Asia/Seoul. Status: **PROVED/EXACT as a conditional implication in the declared streaming model; independent review OPEN**. Finite controls: COMPUTATIONAL. **P versus NP OPEN**.

## Target and four falsifiable mechanisms

End-to-end goal remains: authentic length-\(N=2^n\) truth table -> near-linear one-way-input/one-work-tape compiler -> clock-independent nonlinear semantic quotient -> jointly NP/PH-low verifier with a single stage-independent exponent -> **both-label** MCSP-promise preservation -> a rigorously model-matched lower-bound consequence.

This run tests four mechanisms: (A) source-dependent final-state/provenance might enforce hard output fibers; (B) source-address-dependent rather than stationary transitions might evade the already published finite-state section; (C) jointly PH-low reachability might make canonical preimages inexpensive under \(P=NP\); (D) bare PSPACE access to an input-position-dependent stream might suffice for PH verification. (A) and (B) fail **conditionally** under the specified collapse; (C) holds with a stronger *joint reachability* premise; (D) fails, because succinct interval reachability can encode PSPACE computation. No claim about arbitrary online-emitting transducers.

## Recovered project and duplication boundary

Read current root AGENTS.md/CODEX.md, 2026-11-15 end-to-end directive, .codex/skills/pnp-research/SKILL.md, clock-gate handoff and CLOCKSTREAMPROVENANCE20, main LOSSY_PROMISE_CASCADE6/PARTIAL_SAMPLE_WEDGE7/PROMISE_CASCADE_FIXEDPOINT8/K_ELIMINATION_TRANSFER4/CLOCKSAT1/SOURCEQUERY_SYNTHESIS10/PUBLICSEED_PLOTKIN14, and searched the current repo. **FINITE_STATE_SECTION14 (2026-10-19)** already proves unconditional canonical circuits for stationary terminal-only DFAs, and **THRES_AUTOMATICSECTION15** handles some automatic address clocks. Those results are NOT new here and are not republished. CLOCKHIST18 and CLOCKKGRAM19 cover other stationary/order summaries. The present claim is the *conditional inversion and uniform PH-reachability boundary* for **arbitrary polynomial-time address-dependent transitions with polynomially many state bits**. Savitch's reachability simulation is classical; the application and quantified boundary are scoped, not asserted to be previously unknown mathematics.

## Formal machine and reduction orientation

For each \(n\), let \(N=2^n\). A single uniform description \(d\) has \(|d|\le n^a\), for a fixed \(a\). A deterministic, **source-independent** transition algorithm \(T(1^n,d,i,q,b)\) has one polynomial time bound on combined input length, is total, and returns a \(w(n)\)-bit state, where \(w(n)\le n^a\), \(i\in[0,N)\), \(b\in\{0,1\}\). The initial state \(q_0\) is fixed by \((n,d)\). On the **actual** \(N\)-bit source \(f\), set \(q_{i+1}=T(1^n,d,i,q_i,f_i)\). Let \(H_{n,d}(f)=F(1^n,d,q_N)\), with arbitrary fixed final-state postprocessing \(F\). Source-bound provenance, global parity, address-sensitive nonlinear updates, and adaptive source-derived seed selection are allowed **if encoded in the retained state**. The model excludes source-dependent transition *program selection outside the state*, online emissions that cannot be reconstructed from \(q_N\), and uncharged external advice. If \(F\) and output serialization are polynomial-time in their explicit lengths, the actual compiler makes one source pass with \(O(N\,\operatorname{poly}(n))\) time and \(\operatorname{poly}(n)\) work bits on a single writable work tape, charging the state update and output. This is an upper bound for the declared encoding, **not** a certified CHMY compiler fusion.

Define \(\mathrm{Reach}(n,d,a,k,p,q)\) to mean that a word of exactly \(2^k\) bits, read starting at input position \(a\), takes state \(p\) to \(q\), where \(0\le a\), \(a+2^k\le N\), \(k\le n\). It quantifies over source-word choices, not over the actual source after it has been scanned. The predicate has a **single uniform PSPACE algorithm**:

\[
\mathrm{Reach}(a,0,p,q)\iff \exists b\in\{0,1\}\;T(d,a,p,b)=q,
\]
\[
\mathrm{Reach}(a,k,p,q)\iff
\exists r\in\{0,1\}^{w(n)}:
\mathrm{Reach}(a,k-1,p,r)\land
\mathrm{Reach}(a+2^{k-1},k-1,r,q).
\]

Depth \(k\le n\), a polynomial-size transition computation, and one \(w(n)\)-bit midpoint per active recursion level give polynomial space. Enumeration over all \(2^{w(n)}\) midpoint states can require exponential time; NO polynomial-time reachability is inferred.

## Exact theorem 21.1, BALANCED-PATH-SECTION

**PROVED/EXACT, unconditional as a PSPACE upper bound for the bit language.** For every \((n,d)\), every reachable terminal \(q\), and every source \(f\) ending at \(q\), there is a length-\(N\) canonical source \(g_{n,d,q}\) with the same terminal state and hence \(H(g)=H(f)\). Its bit language
\[
G(1^n,d,q,i)=g_{n,d,q}[i]
\]
belongs to PSPACE **jointly** in all four arguments, using one uniform polynomial-space bound independent of a later decoder clock \(c\).

Proof: For each feasible dyadic interval and endpoints choose the lexicographically least midpoint state \(r\) satisfying both half-interval reachability predicates. Recursively apply the same deterministic rule to each half. At a one-bit leaf choose 0 when feasible and 1 otherwise. To compute only bit \(i\), traverse the unique \(n\)-level dyadic path determined by \(i\); at each level enumerate midpoint states using the PSPACE reachability algorithm. Store the endpoints, interval position/height, and recursion/work stacks. This uses polynomial space. The concatenated word has length exactly \(N\), preserves each interval endpoint by induction and terminates at \(q\); no complete word of length \(N\) is stored.

## Exact conditional theorem 21.2, PH-REACH-INVERSE

Assume that the **joint** predicate \(\mathrm{Reach}\), including arbitrary valid \((n,d,a,k,p,q)\), lies in \(\Sigma_j^P\) or \(\Pi_j^P\) for **one fixed \(j\)** and one uniform machine/size bound. If \(P=NP\), then one uniform algorithm computes \(G(1^n,d,q,i)\) in time \((n+|d|+w(n))^K\) for some fixed finite \(K\), independent of \(n,d,q,i\) and any later clock \(c\).

Proof: Under \(P=NP\) the entire fixed polynomial hierarchy collapses to P. For a dyadic interval and a candidate prefix \(z\) of a midpoint state, ask whether there exists an extension \(r\) of \(z\) with both interval reaches. Existential quantification over the \(w(n)\)-bit midpoint preserves PH membership at some **fixed** level. One uniform polynomial-time decider exists under collapse. Find the midpoint by at most \(w(n)\) such prefix tests, repeat through \(n\) levels, and choose the final bit by a direct transition check. The result has a single uniform polynomial exponent. This is a theorem **under a stronger interval-reachability assumption**, NOT a consequence of a PH-low **target label verifier** alone.

For \(s(N)=N^\beta\), any fixed \(\beta>0\), standard time-to-circuit simulation and \(|d|+w(n)=n^{O(1)}\) yield
\[
\operatorname{CC}(g_{n,d,q})=n^{O(K)}<N^\beta
\]
for all sufficiently large \(n\). Hence
\[
H_{n,d}(Y_{s(N)})=H_{n,d}(\{0,1\}^N)
\]
**under the stated collapse and reachability hypotheses**. If source NO includes any \(f\) with \(\operatorname{CC}(f)\ge N^\gamma\), \(\gamma>\beta\), the exact YES/NO promise classes collide in its target fiber. No deterministic or randomized selector that operates only on the retained final state can separate them. A bounded portfolio of machines is covered by taking the product of their states when the combined state length and joint transition bound remain polynomial in \(n\).

## Exact conditional theorem 21.3, PSPACE-COLLAPSE-INVERSE

Without the PH-reachability hypothesis, if \(P=PSPACE\), the PSPACE bit language \(G\) from theorem 21.1 becomes uniformly polynomial-time with one exponent. The same \(n^{O(1)}\) circuit-section saturation follows for any polynomial-state, polynomial-time transition family. **This is a P=PSPACE conditional statement, NOT a P=NP conditional statement.** In particular \(P=NP\) does not imply \(P=PSPACE\). No cofinal \(K\)-absorption from this theorem reaches \(P\ne NP\).

## Hostile controls and boundaries

1. **PSPACE boundary:** Address-dependent exact-length reachability is not certified PH-low merely because each transition is easy. Encode a polynomial-space deterministic decider configuration in \(q\), ignore source bits, and simulate one step per position with absorbing accept/reject. Choose \(n=\operatorname{poly}(|x|)\) large enough that \(2^n\) steps exceed the finite configuration bound. Reachability of the accepting endpoint at time \(2^n\) decides the source PSPACE language. This establishes PSPACE-hardness of the unrestricted joint reachability problem for a suitable family, not hardness of a particular image language. The ordinary P=NP collapse cannot evaluate it.
2. **Nonstationary escape from UNCONDITIONAL DFA theorem:** A two-state address-dependent equality checker for hardwired \(h\in\{0,1\}^N\) accepts exactly \(h\). Arbitrarily hard \(h\) can occur if its entire \(N\)-bit advice is free. It is NOT an admissible small-description uniform hard section, because that advice must be charged. The finite test uses \(h=10110100\), not a circuit lower-bound witness.
3. **Online-output boundary:** Emitting the original \(N\) bits during the source pass uses constant internal state and produces an identity quotient; the output cannot be recovered from terminal state. It neither compresses nor fits the theorem.
4. **Canonical versus easiest witness:** The balanced-path choice need not minimize circuit size. The theorem finds *an* easy representative **under the collapse**; no unconditional hard-witness lower bound follows from a particular difficult canonical choice. Earlier project CANONICAL-WITNESS-TRAP9 warned about the same distinction.

DISJ sanity: PASS as a no-go control, no rank-to-circuit inference. Relativization: OPEN for any unrelativized P-vs-NP application; classical P=PSPACE simulation alone does not close it. Simultaneous DTISP transfer: FAIL/OPEN, no source lower bound or model-matched transporter. Deterministic configuration counting: PASS for the declared polynomial-state upper-bound machine, not a lower bound. Algebrization/Natural Proofs: not invoked, and unrestricted barrier audits remain OPEN.

## Computational reference

Executable: experiments/meta_lift/2026-11-18_clock_stateinverse21_audit.py. Raw: results/raw/meta_lift/2026-11-18_CLOCKSTATEINVERSE21_raw.json. Seed 202611180713. Checked all 16 two-state stationary transition tables with all 256 sources of length 8; 90 randomly sampled three-state address-dependent transition schedules with all 256 sources; 20 four-state schedules at length 16 with 100 seeded sources each; 20 two-machine product schedules with all 256 length-8 sources; and an address-dependent equality recognizer. Recorded: 4,096 stationary source cases, 25,040 inhomogeneous cases, 5,120 product source cases, 39,711 endpoint checks, 302 exhaustive reachable-endpoint checks, 3,264 canonical bit checks and 256 hostile equality controls; **zero assertion failures**. These are finite semantic checks only; the PH/PSPACE collapses are symbolic conditional implications and were not tested.

## Integration and next lemma

**PROVED/EXACT CONDITIONAL:** Polynomial-state terminal-only streams with jointly PH-low interval reachability admit tiny source sections under \(P=NP\); without that reachability premise the same follows under \(P=PSPACE\). **FALSIFIED/RETIRED:** Treating a PH-low target image verifier as equivalent to PH-low streaming interval reachability; treating arbitrary nonstationary streams as stationary finite automata; claiming high degree, global source dependence, or provenance automatically entails hard fibers. **OPEN:** Construct a full-source, genuinely order-sensitive streaming quotient with *hard inversion* beyond PH-level interval reachability while its **target label verifier** remains jointly NP/PH-low, preserving both source MCSP promises with all seed/provenance alternatives charged. Prove that its exact same-machine compiler beats the source lower bound with a real contraction, including source header, full N-bit scan, output serialization, workspace and one-tape head fusion. The interval-reachability versus output-verifier gap is now the named **INVERSION-VERIFIER-SEPARATION22** target. P versus NP OPEN.

## Primary references

[1] W. J. Savitch, *Relationships Between Nondeterministic and Deterministic Tape Complexities*, JCSS 4 (1970), 177-192. DOI: https://doi.org/10.1016/S0022-0000(70)80006-X

[2] M. Cheraghchi, S. Hirahara, D. Myrisiotis, Y. Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021. DOI: https://doi.org/10.4230/LIPIcs.STACS.2021.23

[3] M. Chrobak, *Finite Automata and Unary Languages*, Theoretical Computer Science 47 (1986), 149-158. Related finite-state results are background only.

[4] Project historical FINITE_STATE_SECTION14, THRES_AUTOMATICSECTION15, CLOCKHIST18, CLOCKKGRAM19, CLOCKSTREAMPROVENANCE20 and CANONICAL-WITNESS-TRAP9. Exact authorship and priority beyond the repo are not asserted.

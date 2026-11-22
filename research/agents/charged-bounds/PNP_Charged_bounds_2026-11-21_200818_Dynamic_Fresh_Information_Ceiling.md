# Dynamic obligations: the global fresh-information ceiling

21 November 2026, 20:08:18 PST, America/Los_Angeles. Role: PNP Lower Bound Connections.

**Named dependency:** DYNAMIC-FRESH-INFORMATION-CEILING1, an audit of DYNAMIC-COMPATIBILITY-OBLIGATION1.
**Mode:** reconstruction and transfer audit.
**Status:** PROVED/EXACT under the explicit information-history hypotheses below. Boolean cleanup is proved for the stated single-tape class permitting a per-machine fixed finite alphabet. No historical novelty is claimed.
**Review:** Two collaborating agents independently checked the derivation and cleanup qualifications. This is internal adversarial review, not external peer review or kernel verification.
**Unrestricted consequence:** OPEN. No superpolynomial SAT lower bound is proved.

## 1. Result and integration point

A repeated-erasure argument cannot obtain superpolynomial work merely by repeatedly counting globally fresh information about one N-bit input. With a single accumulated history, the sum of such information gains is at most N, even with adaptive choices, randomized records, residual decoding error, and recorded stopping decisions.

This is a ceiling on one proposed lower-bound numerator. It does not bound actual computation time, memory residence, repeated local transport, or recomputation from above.

The current charged UNSAT transport report proves quadratic time and cubic cumulative cost in its stated single-tape model. Its matching polynomial algorithm is a required calibration control. Those earlier crossing obligations survive this audit because they concern different physically restricted local views, not new entropy acquired by one global observer. [1]

State recovery found an existing output-fiber loss result and an older copy/cleanup wrapper. This run does not repeat their experiments or claim to discover cleanup. It makes the adaptive fresh-history limitation explicit for the newly assigned dynamic target and supplies the precise same-time-exponent Boolean normal form needed when importing the earlier terminal-state obstruction. [2,3]

## 2. Exact claim and four falsifiers

Let X be a random complete encoded input supported on {0,1}^N. N includes the actual formula encoding and any supplied assignment or auxiliary input. It is not the number of variables or the number of possible assignments.

Let H_0 be an initial recorded history. At stage j let A_j record the selected obligation and any newly introduced side information or randomness needed to define it. Set

\[
G_j=(H_{j-1},A_j),\qquad
U_j=f_j(X,G_j),\qquad
H_j=(G_j,P_j).
\tag{1}
\]

P_j is the subsequent information record. Histories are nested. The targets U_j are determined once the source and the pre-record history G_j are fixed. These hypotheses allow adaptive choices and arbitrary randomized records.

The four falsifiers of an attempted application are:

1. A new random target or query label is omitted from G_j, so U_j is not determined by (X,G_j).
2. The proof resets the conditioning between stages, or substitutes current erasable state for the complete accumulated history.
3. A record-to-time conversion uses free source reads, addresses, framing, stopping times, or an unproved bound on overlapping event charges.
4. A bound on globally fresh information is treated as an upper bound on computation or on transfer between separately informed local receivers.

The theorem itself does not require prefix-free records. That additional requirement enters only when converting information to charged record length.

## 3. Adaptive finite-horizon theorem

Define

\[
c_j=I(X;A_j\mid H_{j-1}),
\qquad
d_j=H(U_j\mid G_j)-H(U_j\mid H_j)
=I(U_j;P_j\mid G_j).
\tag{2}
\]

For every finite q,

\[
\boxed{
\sum_{j=1}^{q}(c_j+d_j)
\le H(X\mid H_0)-H(X\mid H_q)
\le H(X\mid H_0)\le N.
}
\tag{3}
\]

**Proof.** Conditional on G_j, the variable U_j is a function of X. Hence conditional data processing gives

\[
I(U_j;P_j\mid G_j)\le I(X;P_j\mid G_j).
\]

Applying the mutual-information chain rule,

\[
\begin{aligned}
c_j+d_j
&\le I(X;A_j\mid H_{j-1})
   +I(X;P_j\mid H_{j-1},A_j)\\
&=I(X;A_j,P_j\mid H_{j-1})\\
&=H(X\mid H_{j-1})-H(X\mid H_j).
\end{aligned}
\]

Summation telescopes. The support of X has at most 2^N elements. This proves (3). The chain rule is standard; [4, §3.1] supplies a primary-source statement. The present application is fully derived here.

If each record permits exact decoding, H(U_j|H_j)=0, then

\[
\boxed{
\sum_{j=1}^{q}H(U_j\mid G_j)
\le H(X\mid H_0)-\sum_{j=1}^{q}c_j
\le N.
}
\tag{4}
\]

If decoding leaves residual uncertainty eta_j=H(U_j|H_j), the valid expression instead subtracts eta_j. This is consistent with Accounting's existing output-fiber correction. [2]

A source-dependent choice can itself reveal information: its c_j term is nonnegative and consumes the same budget. Independent random choices do not create new source entropy. If an independent random bit is itself the target while X is constant, the theorem is inapplicable unless that bit is included among the information defining the target. That simple control explains the measurability hypothesis.

These are distributional entropy bounds, not bounds on each individual realized transcript's surprise.

## 4. Adaptive stopping

Include the continuation or termination decision in A_j or P_j. After termination has been recorded, pad subsequent choices, targets and records with fixed known symbols. All later c_j and d_j are zero.

Every finite padded prefix satisfies (3). Since the summands are nonnegative, their infinite sum also satisfies

\[
\sum_{j\ge1}(c_j+d_j)\le H(X\mid H_0)\le N.
\tag{5}
\]

Almost sure finite stopping is sufficient; finite expected stage count is unnecessary. An input-dependent stopping time is not supplied as uncharged external decoder information.

## 5. The charged consequence, and its limit

Suppose P_j is conditionally prefix-free given G_j and is supported by an actual event set E_j on the same machine execution. Suppose

\[
|P_j|\le b|E_j|+h_j,
\tag{6}
\]

with nonnegative charged framing overhead h_j. Let every real transition belong to at most rho event sets. The capacity b, reuse rho, and event membership are assumptions requiring proof for the particular construction.

The source-code bound gives

\[
d_j\le H(P_j\mid G_j)\le \mathbb E|P_j|.
\]

Therefore

\[
\sum_j d_j-\sum_j\mathbb E[h_j]\le b\rho\,\mathbb E[T].
\tag{7}
\]

With exact decoders, substitute H(U_j|G_j) for d_j. This is the desired event inequality, now with a global ceiling on its numerator:

\[
\sum_j d_j\le N.
\tag{8}
\]

For b>=1 and rho>=1, this particular lower-bound expression can never exceed N/(b rho) after subtracting nonnegative overhead. It cannot refute a superlinear polynomial time cap merely by adding more stages.

**This does not imply T<=N.** It says only that this one numerator cannot certify more work. An algorithm may perform arbitrarily much work on information already present in the global history.

The history is an analytical object; no claim is made that the solver physically stores its whole execution history. Conversely, an actual decoder cannot access that history for free. Its implementation and permitted information must be justified separately.

If H_0 already contains the full encoded input, each input-derived target has zero globally fresh entropy. Computing the target can still be difficult. Shannon uncertainty conditioned on the complete input is not an estimate of the computational effort needed to evaluate a function of that input.

## 6. Erasure and repeated-copy controls

Take uniform X in {0,1}^N and propose U_j=X at every stage. Resetting B_j to an empty value would assign entropy N at every stage and suggest qN units of new information.

With a genuine nested history, the first record can disclose X, but every subsequent globally fresh demand is zero. The total is N.

Repeated physical transmissions of X may still cost qN. To prove that cost one must establish different local information restrictions and actual unavoidable transmissions. Omitting the previous transcript from the conditioning does not by itself prove those restrictions.

Likewise, removing assigned values from a formula can enlarge the set of semantic possibilities in the problem description without forcing the solver to erase its cached conclusions. An offline decider is not required to expose a new externally visible service at each syntactic erasure stage.

The current crossing theorem does justify locality at its selected cuts, with actual crossing records and a same-execution accounting argument. It does not assert fresh global source information at every cut. [1]

## 7. Boolean cleanup without changing the time exponent

This section is an integration of known cleanup principles into the current sole-tape convention. It is not a new general theorem of computation. The earlier output-fiber report used a conservative quadratic cleanup bound for arbitrary scalar output; the present statement concerns a Boolean answer. [2,3]

Fix a deterministic total single-tape Boolean decider A. Input, workspace and output occupy one writable tape, the input is a contiguous N-bit word, output is a bit and terminator at a fixed origin, and there is no external clock or uncharged preserved transcript.

Assume each machine may use its own fixed finite alphabet. Then a constant number of marker tracks is a fixed alphabet enlargement depending on A, not on N. Original input symbols remain unexpanded, with their auxiliary tracks initially blank.

There is an equivalent total decider A_clean with

\[
T_{A_{\rm clean}}(x)=O_A(T_A(x)+N+1)
\tag{9}
\]

whose terminal configuration is a fixed function kappa(D(x)) of its Boolean answer alone: only the answer and terminator remain, and the head is at the origin.

**Construction.** Mark the origin and an interval enclosing the initialized input. An initialization scan and return cost O(N+1). Simulate A on a payload track. When a virtual head enters an interval sentinel, extend that sentinel by one cell using a bounded number of moves. This preserves the simulation with constant overhead.

At A's halt, return to the marked origin and read the Boolean output into finite control. Seek the left sentinel. Sweep to the right sentinel, erasing every payload and marker except the origin marker. Erase the right sentinel, return to the origin marker, erase it, write the canonical answer and terminator, and halt at the origin.

The marked span is O(N+T_A+1). Each final sweep is charged, so (9) follows. A one-sided tape uses its fixed left boundary in place of a removable left sentinel. Under a labeled-halting convention the output tape may instead be blank, but that is not the fixed-origin-output convention used here.

For a fixed cap T_A(N)<=K N^a with a>=1,

\[
T_{A_{\rm clean}}(N)=O_A((K+1)N^a).
\tag{10}
\]

The exponent is preserved, while constants and state count may change. A contradiction depending on the identical numerical constant K would require a separate constant-sensitive argument.

The safe same-run ceilings remain

\[
S_{A_{\rm clean}}=O_A(N+T_A+1),\qquad
CM_{{\rm phys},A_{\rm clean}}=O_A((N+T_A+1)^2).
\tag{11}
\]

Self-contained replay gives

\[
CM_{{\min},A_{\rm clean}}
=O_A((N+T_A+1)(N+\log(N+T_A+2))).
\tag{12}
\]

Thus the fixed-cap exponents remain a, 2a and a+1, respectively. No constant-factor preservation of A's original cumulative cost is claimed: persistent boundary markers may retain a wider span at intermediate times.

If one exact tape alphabet is fixed globally for all machines and the same unexpanded input encoding is mandatory, the marker-track compiler needs a separate proof. An in-place block expansion cannot simply be called constant-time overhead. That narrower convention is not silently covered.

## 8. Exact terminal-reconstruction criterion

Let B(x) and U(x) be fixed source observables. Suppose the proposed obligation says that for every correct equivalent solver there is a decoder recovering U from B and that solver's terminal configuration.

Apply the assertion to A_clean. Since C_terminal(x)=kappa(D(x)),

\[
U(x)=g(B(x),D(x)).
\tag{13}
\]

Consequently

\[
H(U\mid B)\le H(D\mid B)\le1.
\tag{14}
\]

On an UNSAT-supported distribution D is constant, so H(U|B)=0. A positive terminal source-reconstruction demand on that distribution is impossible unless additional information is supplied in B.

Conversely, if a computable g in (13) is supplied, the canonical answer can recover U together with B. This is an information/factorization criterion, not a claim that evaluating g is cheap. All earlier computation and cleanup remain paid.

No conclusion is drawn about an earlier compulsory crossing or checkpoint. Cleanup cannot undo work already performed.

## 9. Gates and same-execution ledger

| Gate | Status and scope |
|---|---|
| DISJ/equality sanity | PASS. A constant-label diagonal can have substantial local crossing costs while terminal answer information is constant. |
| Relativization | PASS as a scope audit. The entropy identity supplies no nonrelativizing separation; no unrestricted consequence is claimed. |
| Simultaneous DTISP | PASS for the stated inequalities. Event sets and reuse refer to one run; cleanup bounds refer to one transformed run. No unrelated maxima are multiplied. |
| Deterministic configurations | PASS. Canonicalization merges different input executions, not two moments of one nonhalting deterministic trajectory. External timing metadata is excluded explicitly. |

Parsing, initialization, source access, simulation, boundary extension, output reads, erasure, final writes, and head movement are charged in the cleanup proof. Decoder records require their own address, length, framing, and side-information ledger. Discovery, failed preprocessing, caches and sharing are legal and remain paid.

No Natural Proofs, algebrization, circuit, or proof-system lower bound is imported. The result applies equally to easy Horn, affine and product controls. It neither forces assignment counting nor transfers a counting lower bound to decision.

## 10. Primary literature and transfer assessment

Braverman and Rao's author-hosted paper supplies the standard conditional information identities and distinguishes whole-transcript information from information learned by separately informed parties. Its introduction also warns that a one-bit result can require costly communication. The present theorem uses only those elementary identities, with a complete proof above; it does not import a SAT lower bound. [4]

Clifford, Jalsenius and Sach encode actual transferred cells, addresses and record length, and separately establish an event-charging bound. Their online output deadlines supply services that an offline SAT decider need not perform. Their framework is a useful specification for a local decoder, but the direct transfer to this SAT task is OPEN. [5]

## 11. Recovery, searches and validation

Read the current continuation directive, transport report, applicable charged-model definitions, AGENTS.md, CODEX.md, repository PNP research skill and compatible references, all six compact handoffs, current issue 324, the latest Bounds shared-quotient report, Accounting's original output-fiber report, and the relevant original DERIVEDLEAK1 theorem. Full current handoff bodies and SHAs were recovered before publication.

Important recovered sources: OUTPUT-FIBER-LOSS1 blob 8016fe8b39464a98f845a82b689b4e2d42a27759; DERIVEDLEAK1 blob eac4f49666a446c8826bcc5e922a78a873ee0634; Bounds shared-quotient report blob 6642b77793d5f71ddf08d48fce6c330e0132cda8.

Fresh corpus searches: "fresh information telescoping", "nested history entropy", and "linear cleanup". These surfaced prior input-information ceilings, SOURCE-ENTROPY-CAP1 excerpts, and DERIVEDLEAK1. No historical novelty is claimed. A branch search for "charged" returned no matching branch; this is not a claim that every repository branch was inspected.

Fresh primary searches targeted "Braverman Rao information equals amortized communication external information transcript mutual information" and "Clifford Jalsenius information transfer online Hamming distance lower bounds cell probe pdf entropy". The author-hosted and published PDFs in [4,5] were inspected. Earlier Hartmanis/Bennett cleanup searches were discontinued after the duplicate result was recovered; reversible cleanup was not imported as an irreversible-erasure theorem.

Fresh organization-scoped searches covered Anthropic, OpenAI, xAI, Google Research, Google DeepMind and Google OR-Tools with theorem-proving, SAT, formal-verification and information-transfer terms. Anthropic and OpenAI organization pages displayed domain verification. Other organization pages and their website/release links were inspected, but no ownership-dependent theorem or code claim was imported. Google's official OR-Tools page linked its repository. No candidate repository commit was checked out, no formal kernel was run, and no verified theorem forcing the needed offline SAT service was found.

The two independent internal mathematical audits checked adaptive-choice conditioning, stopping, the difference between current state and accumulated history, the fixed-origin output convention, alphabet enlargement, and the absence of a constant-factor CM claim. No solver experiment or repeated finite audit was run; these are symbolic proofs and a transfer audit. Repository preflight and LaTeX compilation were not run because this was connected-source research without a local repository checkout or LaTeX build.

This Bounds run was executed inline after the automation's manual-start tool explicitly returned an inline execution instruction. It is not a claim that six background runs completed.

## 12. Next receiving dependency

**Owner: Accounting and Construction, with Bounds and Redteam review.**

Specify one compact, decision-sensitive family and an actual intermediate local view after paid preprocessing. Prove why every correct solver must encounter that view, why its decoder lacks the needed information under the declared access model, and why the required records cannot all be supplied by one cached representation or overlapping events.

The new target is a compulsory local transfer or recomputation theorem. Repeated global entropy, arbitrary terminal source recovery, and a virtual sequence of residual queries do not supply that theorem. P versus NP remains OPEN.

## References

1. Project report, CHARGED-UNSAT-TRANSPORT1. [Published transport report](https://github.com/j15marti/pnp/blob/2547822e9e82c914a668d9b4de2c6991e490d7f0/research/main/Charged_UNSAT_Transport_2026-11-21.md).
2. Charged Accounting, T5-OUTPUT-FIBER-LOSS1, 21 November 2026. [Original report](https://github.com/j15marti/pnp/blob/4e2beb641518f2ba66e8604a85ff6e18dbbf67aa/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-21_143800_Output_Fiber_Loss.md).
3. LSPV-1, DERIVEDLEAK1, 12 October 2026. [Original wrapper theorem](https://github.com/j15marti/pnp/blob/5781acecf5e964364f1ee5682b2c63b057832c41/research/agents/lspv-1/2026-10-12_1513_LSPV-1_DERIVEDLEAK1.tex).
4. Mark Braverman and Anup Rao. Information Equals Amortized Communication. Inspected author version dated 8 November 2010, §3.1 and introductory footnote 1. [Author PDF](https://www.cs.toronto.edu/~mbraverm/Papers/amortizedcommunication.pdf).
5. Raphaël Clifford, Markus Jalsenius and Benjamin Sach. Time Bounds for Streaming Problems. Theory of Computing 15(2), 2019, pp. 1-31. DOI 10.4086/toc.2019.v015a002, particularly §§2.3 and 3.1. [Published PDF](https://www.theoryofcomputing.org/articles/v015a002/v015a002.pdf).

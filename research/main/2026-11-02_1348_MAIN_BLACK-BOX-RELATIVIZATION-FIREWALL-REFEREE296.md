# PNP Independent Proof Red Team — REFEREE296

**Run:** 2026-11-02 13:48 America/Los_Angeles  
**Task identity/status:** preserved exactly; no task or schedule operation was performed.  
**Scientific status:** P versus NP remains **OPEN**.

## Result at a glance

This run proves a precise methodological barrier for the weakest bridge B3.
Fix an ordinary proof calculus independently of the inputs.  If that calculus
has a known superpolynomial ordinary proof lower bound, then no proof of B3 can
be **fully solver-relativizing while leaving the calculus ordinary and
unchanged**.  An oracle can put ordinary SAT in oracle-polynomial time without
changing any ordinary shortest proof in the fixed calculus.  Applying a
fully relativizing bridge would therefore make the unchanged superpolynomial
worst-case proof measure polynomial, a contradiction.

This is a **BLACK-BOX RELATIVIZATION FIREWALL**.  It does not falsify the
ordinary statement

\[
  \mathrm{SAT}\in\mathrm P\Longrightarrow
  \overline W_R(N)\le N^{O(1)}
\]

for a suitable fixed mixed calculus.  It proves only that a successful
argument must use a nonrelativizing property of an ordinary solver, its code
or its correctness, or a sufficiently strong proof-system optimality
hypothesis.  Treating the solver solely as a timed SAT-membership service is
insufficient.

The run also independently checks the concurrent LSPV-1
CLOCKED-OPTIMALITY-REFLECTION336 theorem: if the same fixed calculus is
size-optimal among ordinary Cook--Reckhow UNSAT proof systems, then the
pointwise bridge B1 follows for every ordinary total correct SAT decider.
That sufficient condition survives this audit precisely because its
unary-clock verifier is an ordinary polynomial-time verifier only for an
ordinary fixed machine.  With an oracle machine it becomes an oracle verifier,
outside the assumed ordinary size-optimality class.

No superpolynomial lower bound is proved for a representation-inclusive mixed
calculus.  B1, global B2 and B3 remain open for the desired fixed calculus.

## Fixed definitions and quantifiers

Let \(R\) be a sound, complete, effective ordinary UNSAT calculus fixed before
all inputs.  Its proofs are encoded shared contradiction DAGs, its rules have
polynomially checkable ordinary justifications, and every inference node has a
declared nonnegative weight.  Define

\[
 W_R(F)=\min_{\pi\text{ an }R\text{-refutation of }F}\operatorname{cost}(\pi),
 \qquad
 \overline W_R(N)=\max_{\substack{|F|\le N\\F\text{ valid UNSAT}}}W_R(F).
\]

The minimum grants free after-the-fact choice of the best proof.  No proof
search cost is charged.  This grant does not add a semantic rule that maps an
arbitrary UNSAT formula to contradiction in one step.

The three ordinary transfer obligations are:

* **B1:** for every total correct ordinary SAT decider \(A\), a polynomial
  \(p_A\) bounds \(W_R(F)\) by
  \(p_A(|F|+T_A(F))\) for every valid UNSAT \(F\);
* **B2:** for every such \(A\), a polynomial \(p_A\) bounds
  \(\overline W_R(N)\) by
  \(p_A(N+T_A^{wc}(N))\);
* **B3:** if ordinary SAT belongs to ordinary P, then
  \(\overline W_R\) is polynomial.

B1 implies B2, which implies B3.  None is established in general.

For this report, a **fully solver-relativizing B3 proof schema** is one whose
reasoning remains valid after replacing an ordinary polynomial-time SAT
decider by an oracle-polynomial-time SAT decider, while keeping the target
calculus \(R\), its rule verifier and \(W_R\) ordinary and unchanged.

## The exact barrier theorem

### Theorem 1 — unchanged-calculus relativization firewall (PROVED/EXACT)

Let \(R\) be any fixed ordinary calculus for which
\(\overline W_R(N)\) is superpolynomial.  There is no fully
solver-relativizing proof schema establishing

\[
  \mathrm{SAT}\in\mathrm P^O
  \Longrightarrow
  \overline W_R(N)\le N^{O(1)}
\]

for every oracle \(O\), with the same ordinary \(R\) on the right.

**Proof.** Baker, Gill and Solovay construct a recursive oracle \(O\) for which
\(\mathrm P^O=\mathrm{NP}^O\).  Since ordinary SAT is in NP and hence in
\(\mathrm{NP}^O\), ordinary SAT is in \(\mathrm P^O\).  Equivalently, for the
more elementary special case one may take an oracle that directly answers
ordinary SAT membership after ordinary parsing.

The oracle changes neither the ordinary source formulas nor any legal ordinary
\(R\)-derivation.  Therefore \(W_R(F)\) and \(\overline W_R(N)\) are exactly
the same functions as before the oracle is installed.  The antecedent of the
displayed relativized implication is true, while its consequent is false by
the assumed superpolynomial lower bound.  Hence no proof schema valid under
this relativization can establish the implication.  ∎

An explicit instance is source-axiom Resolution plus Weakening with unit node
weights.  Standard expander Tseitin formulas give superpolynomial, indeed
exponential in the graph size, ordinary Resolution refutations.  The oracle
still decides their SAT membership in polynomial oracle time, while the
ordinary Resolution DAG minimum is unchanged.

The theorem is about a proposed **method**, not the truth of ordinary B3.  It
does not show an oracle \(O\) with \(\mathrm P^O=\mathrm{NP}^O\) and a failure
of a properly oracle-augmented proof system \(R^O\).  Allowing oracle rules in
the proof system changes the system and the quantity being bounded.

### Corollary 1 — timed membership behavior alone cannot prove B3 (PROVED)

Any proposed B3 translation that uses only the input/output behavior and time
bound of a SAT solver, and whose logical checks do not inspect a
nonrelativizing property of its ordinary code or correctness proof, fails the
firewall above.  A raw accepting or rejecting trace is not ordinary logical
evidence: an oracle-answer bit may be copied into a transcript, but a
polynomial ordinary checker cannot in general validate that bit without an
independent certificate.

This corollary rejects a hidden unit-cost SAT/equivalence oracle.  It does not
reject free selection among derivations already legal in \(R\).

## Independent audit of the size-optimality route

### Theorem 2 — unary-clock simulation under ordinary size optimality (PROVED, CONDITIONAL)

Assume the fixed ordinary calculus \(R\) is size-optimal among ordinary
Cook--Reckhow UNSAT proof systems and that inference-node cost is at most
polynomial in encoded proof length.  Then B1 holds for every fixed total
correct ordinary SAT decider \(A\).

**Proof.** Fix \(A\).  Define an ordinary verifier \(Q_A\) whose certificate
for \(F\) is \((F,1^t)\).  It parses \(F\), simulates \(A(F)\) for \(t\) steps,
and accepts exactly when \(A\) returns UNSAT within that clock.  Verification
time is polynomial in the unary certificate length.  External correctness of
\(A\) makes \(Q_A\) sound; totality makes it complete for valid UNSAT inputs.
The certificate length is \(O(|F|+T_A(F))\).

By size optimality, \(R\) has a proof whose encoded length is polynomial in
that \(Q_A\)-certificate length.  The declared domination of node cost by
proof length gives

\[
 W_R(F)\le p_A(|F|+T_A(F)).
\]

This is B1.  ∎

There is no illicit instance-specific axiom: \(Q_A\) is fixed once \(A\) is
fixed.  Malformed strings are rejected by the verifier and are not UNSAT
theorems.  The theorem is conditional on size optimality, which is not known
for the desired mixed \(R\).

The proof does not fully relativize.  If \(A^O\) invokes an oracle, replaying
its clocked computation requires checking oracle answers.  The resulting
\(Q_{A^O}^O\) is polynomial-time verifiable relative to \(O\), not an ordinary
Cook--Reckhow proof system.  Ordinary size optimality of \(R\) gives no
simulation guarantee for it.  This is the exact point at which Theorem 2
escapes Theorem 1.

## Four falsifiers

1. **Treat the oracle output bit or transcript as an ordinary certificate.**
   Confirmed unsound.  The finite control accepts a forged SAT transcript
   under a deliberately transcript-only rule.  It rejects the same forgery
   only after independently recomputing membership, which is precisely the
   hidden oracle work that an ordinary bridge must justify.
2. **Give \(R\) an oracle-validation inference.** This evades the contradiction
   only by changing \(R\) to \(R^O\).  It says nothing about the original
   ordinary \(\overline W_R\), so it is rejected as a response to the stated
   bridge.
3. **Use ordinary size optimality and a unary-clock verifier.** This survives.
   Theorem 2 independently reproduces the LSPV-1 sufficient condition and
   identifies its nonrelativizing seam.  It remains conditional and supplies
   no lower bound.
4. **Conclude that the oracle countermodel falsifies ordinary B3.** Rejected.
   The ordinary antecedent \(\mathrm{SAT}\in\mathrm P\) is not obtained from
   \(\mathrm{SAT}\in\mathrm P^O\).  The result blocks a relativizing proof
   technique only.

## Finite controls

The producer implements a strict DIMACS subset with explicit header and
end-of-clause tokens.  It rejects a nonnumeric token, missing header, malformed
header, out-of-range literal, missing clause terminator and clause-count
mismatch.

Both labels are present:

* SAT: \((x_1\lor x_2)\), with a checked witness;
* UNSAT: \(x_1\land\neg x_1\);
* UNSAT: the four clauses encoding equality and inequality simultaneously on
  two variables.

After ordinary parsing, the abstract oracle decider makes one SAT-membership
query.  An honest UNSAT transcript passes an independent oracle recheck.  A
forged SAT transcript is accepted by the intentionally unsound
transcript-only rule and rejected by the recheck.  A claimed ordinary
Resolution proof with no derivation nodes is rejected.

As an independent ordinary-proof sanity control, the producer constructs full
blocking-clause Resolution+Weakening refutations on one through six variables.
The separately written verifier confirms exact costs
\(3,7,15,31,63,127\), all rule applications, final contradiction and rejection
of a corrupted terminal node.  These finite checks do not prove the
Baker--Gill--Solovay oracle theorem or any asymptotic Resolution lower bound.

## Work and peak-space ledger

For the finite producer, charged phases are strict parsing, exhaustive
finite-oracle evaluation, transcript serialization and hashing, proof
construction, rule verification, corruption tests and malformed-input checks.
The raw run records about \(9.5\times10^7\) host nanoseconds and 270 kB
tracemalloc peak; these are reproducibility diagnostics, not native-machine
complexity bounds.  The independent verifier performs 34 assertion groups
without importing the producer.

For the abstract one-query oracle decider, ordinary parsing and query
construction take polynomial time and linear or polynomial all-phase space;
the oracle answer is one bit.  This accounting deliberately exposes rather
than erases the missing cost: an ordinary derivation must provide checkable
logical evidence for that answer.  Storing or hashing an oracle transcript
does not validate its semantic contents.

For Theorem 2, constructing and checking the unary clock uses
\(O(|F|+T_A(F))\) certificate length and polynomial verification time and
space in that length.  The theorem concerns minimum proof length/node cost,
not proof discovery or a memory schedule for executing the proof DAG.
No materialized-child recursion or FLMV time-space transfer is claimed.  If
such a transfer is later proposed, the all-phase peak remains
\[
 s'\le\max\{\rho,\eta,\lambda,\lambda s\},
\]
including parsing, order discovery, conversion, generation and combination;
this run supplies none of the required exponent bounds.

## Literature and repository search log

Searches were performed before the proof was finalized.

* \`Baker Gill Solovay relativizations P NP 1975 primary paper\` found
  Baker, Gill and Solovay, *Relativizations of the P=?NP Question*, SIAM
  Journal on Computing 4(4), 1975,
  <https://doi.org/10.1137/0204037>.  The paper supplies recursive oracles
  with opposite relativized P/NP outcomes.  The present use is the standard
  relativization barrier pattern, not a novelty claim.
* \`Cook Reckhow relative efficiency propositional proof systems 1979 pdf\`
  found the primary paper,
  <https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf>.  It supplies
  the polynomially checkable proof-system framework used in Theorem 2.
* \`oracle relativized propositional proof systems optimal proof system\`
  found Ben-David and Gringauze, ECCC TR98-021,
  <https://eccc.weizmann.ac.il/report/1998/021/>, and Messner and Toran,
  ECCC TR97-026, <https://eccc.weizmann.ac.il/report/1997/026/>.
  These works analyze oracle barriers and optimal proof systems; they do not
  establish the present ordinary B3 bridge.
* A current search also found Egidy, *Recursive Proof-Theoretic Jump
  Operators Explaining the Logical Strength of Optimal Proof Systems*,
  ICALP 2026, <https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2026.71>.
  It concerns oracle/optimal-system structure and is background only.
* Project GitHub searches for \`relativization B3 proof system SAT solver
  black box\` and \`oracle optimal proof systems relativization\` found older
  black-box cautions and the current CLOCKED-OPTIMALITY-REFLECTION336 report,
  but no prior project statement of this exact unchanged-calculus firewall.
* GitHub searches restricted to \`github.com/openai\` for
  \`relativization proof complexity optimal proof system\` and
  \`Baker Gill Solovay SAT oracle proof system\` returned no relevant
  implementation or proof.  A failed repository search is not evidence of
  novelty.

## Project corpus reviewed and reconciliation

Reviewed before theorem selection:

* shared worst-case-minimum-derivation handoff through LSPV-1 result 336,
  LSPV-2 result 342, LSPV-3 results 342--343 and LSPV-4 result 342;
* issue #3 current comments;
* REFEREE294 trace-correctness firewall and REFEREE295 per-decider
  worst-case-runtime pollution audit;
* the current root synthesis and role-owned governance instructions.

**Adopted:** LSPV-1's size-optimality sufficient condition, independently
proved above; LSPV-3's warning that adding extension/XOR rules can collapse a
candidate hard family; LSPV-4's node/evidence domination requirement.

**Rejected:** raw decision traces as correctness proofs; oracle-answer bits as
ordinary inference evidence; changing \(R\) after selecting an oracle;
claiming that a relativized countermodel disproves ordinary B3.

**Retired/stale:** no earlier verified theorem is retired.  The older
pointwise-only target remains useful for B1 but is not the primary goal.
REFEREE295 remains a single-decider B1/B2 converse failure and is not promoted
to a global separation.

**What changed in the root synthesis:** add the unchanged-calculus
relativization firewall and the conditional size-optimality escape immediately
before REFEREE295.  Keep the exact labels **PROVED/EXACT METHOD BARRIER** and
**PROVED/CONDITIONAL SUFFICIENT BRIDGE**.

## Exact next gap

The remaining two-part target is unchanged:

1. select one fixed representation-inclusive mixed calculus \(R\) and prove a
   superpolynomial lower bound for \(\overline W_R\), despite XOR, circuit,
   Horn/2SAT, extension, auxiliary-definition and representation-switch
   shortcuts; and
2. prove ordinary B3 for that **same** \(R\), either through an independently
   justified size-optimality property or through a weaker direct
   nonrelativizing translation from every hypothetical ordinary
   polynomial-time SAT decider.

The first candidate theorem to attack next is whether a natural,
polynomially checkable mixed calculus can satisfy enough ordinary
size-optimality to simulate every unary-clock system \(Q_A\) without thereby
admitting a hidden semantic jump.  Both halves are OPEN.  P versus NP remains
OPEN.

## Reproducibility

* producer:
  \`experiments/arc/lspv5_296/black_box_relativization_referee296.py\`
* independent verifier:
  \`experiments/arc/lspv5_296/verify_black_box_relativization_referee296.py\`
* raw output:
  \`results/raw/arc/2026-11-02_1348_LSPV5_BLACK_BOX_RELATIVIZATION_REFEREE296_raw.json\`
* verification output:
  \`results/raw/arc/2026-11-02_1348_LSPV5_BLACK_BOX_RELATIVIZATION_REFEREE296_verify.json\`


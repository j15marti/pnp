# PNP Independent Proof Red Team — REFEREE297

**Run:** 2026-11-02 14:48 America/Los_Angeles  
**Task identity/status:** preserved exactly; no task or schedule operation was performed.  
**Scientific status:** P versus NP remains **OPEN**.

## Result at a glance

This run closes the exact finite/asymptotic analysis missing from the existing
user-directed F15 noisy-oracle experiment.  Suppose a CNF has a unique
satisfying assignment \(z\).  A proposal at Hamming distance \(d\) from \(z\)
has product weight

\[
  w_d=q^{n-d}(1-q)^d,
\]

where \(q\) is the effective probability that each bit agrees with \(z\).
Generate a weighted random permutation of all assignments—equivalently,
successively sample proportional to weight and remove every sampled
assignment, so no assignment is ever repeated.  Let \(R\) be the rank of
\(z\) in this permutation.  Then, exactly,

\[
 \mathbb E R
 =1+\sum_{d=1}^n {n\choose d}
   \frac{r^d}{1+r^d},
 \qquad r=\frac{1-q}{q},
\]

and for every \(q\in[1/2,1]\),

\[
 \boxed{\frac{q^{-n}+1}{2}\le \mathbb E R\le q^{-n}.}
\]

Therefore for each fixed \(q<1\), even perfect no-repeat conditioning leaves
\(\mathbb E R=\Theta(q^{-n})\).  It improves the iid expected proposal count
\(q^{-n}\) by at most a factor of two.  Polynomial expected rank requires

\[
 -n\log q=O(\log n),
\]

equivalently \(q=1-O(\log n/n)\) as \(q\to1\).  This is an
**EXACT SAMPLING THEOREM**, not a SAT lower bound.

The result sharpens, rather than duplicates, the existing project report
\`2026-11-02_0910_ORACLE-GUIDED-SAT-NOGOOD-EXPERIMENT.md\`.  That report
measured F15 and found large small-instance gains, but its strong no-repeat
experiment explicitly enumerated 512 residual assignments.  REFEREE297 gives
the closed form, an asymptotic threshold, and a transfer audit.

## Two meanings of “66% oracle”

The percentage must be defined before interpreting an experiment.

1. **Direct accuracy:** the supplied bit equals the target bit with probability
   \(q=p\).
2. **Oracle-else-random:** with probability \(p\) the oracle supplies the
   target bit, and otherwise a fair random bit is used.  Then
   \(q=p+(1-p)/2=(1+p)/2\).

The existing F15 experiment uses the second interpretation.  The exact
expected unique-assignment checks at \(n=9\) are:

| stated rate | direct \(q=p\) | oracle-else-random \(q=(1+p)/2\) |
|---:|---:|---:|
| 66% | 36.345 | 4.969 |
| 75% | 12.036 | 3.150 |
| 90% | 2.476 | 1.563 |
| 95% | 1.563 | 1.250 |
| 99% | 1.094 | 1.046 |

These values explain why the small F15 experiment looks extremely favorable.
The same fixed rates eventually cross one million expected unique checks:

| stated rate | direct accuracy: first \(n\) | oracle-else-random: first \(n\) |
|---:|---:|---:|
| 66% | 34 | 75 |
| 75% | 49 | 104 |
| 90% | 132 | 270 |
| 95% | 270 | 546 |
| 99% | 1,375 | 2,757 |

At 99% invocation with random fallback, \(q=99.5\%\): the exact expectation
is only \(150.26\) at \(n=1000\), yet it is still asymptotic to
\((1/0.995)^n\), not a polynomial.

## Exact proof

Give each assignment \(a\) an independent exponential clock
\(T_a\sim\operatorname{Exp}(w_a)\).  Ordering assignments by increasing clock
is the standard exponential-race realization of successive weighted sampling
without replacement.  Let \(z\) be the unique target.  For any assignment
\(a\) at distance \(d\),

\[
 \Pr[T_a<T_z]
 =\frac{w_a}{w_a+w_z}
 =\frac{r^d}{1+r^d}.
\]

The rank of \(z\) is one plus the number of other clocks that ring first.
Linearity of expectation and the \({n\choose d}\) assignments at distance
\(d\) give the displayed exact formula; independence between those rank
indicators is not required.

For \(q\ge1/2\), \(0\le r^d\le1\), hence

\[
 \frac{r^d}{2}\le\frac{r^d}{1+r^d}\le r^d.
\]

Summing and using
\[
 \sum_{d=1}^n{n\choose d}r^d=(1+r)^n-1=q^{-n}-1
\]
proves both bounds.  The polynomial threshold follows by taking logarithms.
∎

## Scope: what “logically ruled out” means

The theorem models the strongest exact form of **no repeated complete
assignments**: after a proposal is checked, it is removed from the weighted
population.  If a sound learned clause rules out an entire cube, more than one
assignment can be removed.  That is a different algorithmic resource and its
derivation, validation and storage must be charged.  The theorem does not
claim that CDCL, resolution, Horn propagation, XOR reasoning or other
source-aware reductions remove only one assignment.

Indeed, the finite control deliberately exposes this distinction.  The unique
SAT formula

\[
 U_n=(x_1)\land\cdots\land(x_n)
\]

has one model, but unit propagation finds it in linear source work.  Its UNSAT
sibling \(U_n\land(\neg x_1)\) has a one-node Resolution contradiction in any
mixed calculus containing ordinary Resolution.  Blind sampling can therefore
be exponentially worse than the shortest logical derivation on an easy
formula.  The sampling expectation is not \(W_R\), and it cannot be used as a
lower bound on \(W_R\).

## Four falsifiers

1. **No repeats make a fixed-quality oracle polynomial.** Falsified by the
   exact rank theorem: the improvement over iid sampling is at most a factor
   of two, and the expectation is \(\Theta(q^{-n})\).
2. **A 99% oracle is effectively perfect.** Falsified asymptotically.  It is
   excellent on small inputs; fixed direct \(q=.99\) already gives about
   \(23{,}163\) expected unique checks at \(n=1000\) and crosses one million
   at \(n=1375\).
3. **The oracle-else-random percentage equals bit accuracy.** Falsified:
   effective accuracy is \(q=(1+p)/2\), so a stated 66% invocation rate is
   actually 83% correct per bit.  Both interpretations are reported.
4. **Fast SAT-side witness search supplies a total SAT decider or B3.**
   Falsified as a transfer.  UNSAT has no correct witness bits.  Exhausting
   failed assignments or emitting a rejecting trace does not produce a sound
   contradiction DAG.  Acquiring witness-correlated advice is at least as
   important as using it and is not free.

## Relationship to unique SAT and known randomized algorithms

Valiant--Vazirani show that isolating a unique solution does not make SAT
generally easy: ordinary SAT randomized-reduces to the zero-versus-one-solution
problem.  This does not turn the present sampling theorem into a lower bound;
it only prevents dismissing unique-SAT as an irrelevant promise.

Schöning's algorithm uses source information: it starts randomly, selects an
unsatisfied clause and flips a variable in that clause.  Its analysis is not
blind full-assignment sampling.  PPSZ likewise exploits forced variables and
critical-clause structure.  These algorithms are controls showing why
source-aware logical inference can beat the proposal model.

Weighted sampling without replacement and exponential keys are established
sampling constructions.  The contribution here is only their elementary
specialization to the stated noisy-witness SAT experiment and the resulting
closed-form rank bound; no novelty is claimed for the sampling method.

## Both-label and malformed controls

The producer implements a strict DIMACS parser and exhaustively evaluates:

* SAT: \(U_{12}\), exactly one model, the all-one assignment;
* UNSAT: \(U_{12}\land(\neg x_1)\), zero models and a one-derived-node
  Resolution certificate;
* malformed: missing header, nonnumeric header, missing zero terminator,
  out-of-range literal, repeated variable and clause-count mismatch; all six
  are rejected.

It evaluates 60 exact rate/size rows and ten exact million-check thresholds.
The no-import independent verifier recomputes the sums and bounds and passes
269 assertion groups.

## Work and all-phase peak-space ledger

For a proposal-based implementation, each candidate requires \(n\) random or
advised bit choices and an original-clause check.  Storing \(K\) already
examined assignments explicitly costs \(\Theta(nK)\) bits, potentially
exponential.  Preenumerating the weighted population costs
\(\Theta(n2^n)\) materialized bits and violates any square-root-space local
phase contract.  More compact weighted-sampling data structures do not make
the expected number of unique candidates polynomial and still require paid
state updates.

The exact analysis grants an ideal weighted permutation and therefore relaxes
data-structure costs.  This only strengthens the negative result about
fixed-\(q\) no-repeat sampling.  It does not charge acquisition of the target
correlation, because that is precisely the missing oracle resource being
audited.

The producer charges strict parsing, complete enumeration of the two
12-variable fixtures, exact Decimal rank sums, bound checks, threshold search
and malformed controls.  The raw host run took about 3.3 seconds with a
35.7-kB traced Python peak.  These are reproducibility diagnostics, not
native-machine complexity bounds.

No materialized-child contraction or FLMV transfer is claimed.  Any such
implementation still requires the all-phase envelope

\[
 s'\le\max\{\rho,\eta,\lambda,\lambda s\},
\]

where \(\rho\) includes oracle acquisition, preprocessing, population
construction, duplicate/exclusion storage, proposal generation and
combination.

## B1/B2/B3 classification

| obligation | status after this run | reason |
|---|---|---|
| B1 | **OPEN for the desired fixed mixed \(R\)** | witness-correlated advice is not an ordinary total decider and emits no general refutation |
| B2 | **OPEN globally** | the SAT-side expected search calculation does not bound every decider's worst-case time or \(\overline W_R\) |
| B3 | **OPEN** | no ordinary polynomial all-input SAT solver or same-\(R\) proof bound is produced |

The theorem neither proves nor falsifies a superpolynomial
\(\overline W_R\).  It prevents a finite oracle experiment from being
misclassified as a bridge or lower bound.

## Literature and repository search log

Searches were performed before proof finalization.

* \`Schöning probabilistic algorithm k-SAT 1999 primary paper random walk
  pdf\` found Schöning, *A Probabilistic Algorithm for k-SAT and Constraint
  Satisfaction Problems*, FOCS 1999,
  <https://www.eecs.harvard.edu/~michaelm/CS223/schoning99.pdf>.  It gives a
  clause-guided local search, not the present blind no-repeat model.
* \`Valiant Vazirani unique SAT 1986 PDF primary\` found the primary paper,
  *NP is as Easy as Detecting Unique Solutions*,
  <https://ics.uci.edu/~vazirani/ValVaz.pdf>.  It establishes a randomized
  isolation reduction, not a deterministic lower bound.
* \`Paturi Pudlak Saks Zane unique k-SAT randomized algorithm primary paper\`
  found the Satisfiability Coding Lemma and the PPSZ line,
  <https://scholar.lib.vt.edu/ejournals/CJTCS/cjtcs-mirror/articles/1999/11/contents.html>.
  It reinforces that forced-variable/source structure matters.
* \`weighted sampling without replacement exponential race primary
  literature\` found Wong--Easton,
  <https://doi.org/10.1137/0209009>, and Efraimidis--Spirakis,
  <https://www.sciencedirect.com/science/article/pii/S002001900500298X>.
* Project GitHub query \`66% oracle random assignments SAT\` found
  \`research/main/2026-11-02_0910_ORACLE-GUIDED-SAT-NOGOOD-EXPERIMENT.md\`.
  That prior experiment is explicitly adopted and sharpened here.
* Project query \`assignment oracle biased random without replacement SAT\`
  returned no other match.  OpenAI GitHub queries for PPSZ and Schöning found
  only a bibliographic discussion in an unverified preprint under
  \`openai/math\`, not a relevant implementation or proof.  No novelty claim
  is based on search failure.

## Project corpus reviewed and reconciliation

Reviewed the current five-role handoff through LSPV-1
FINITE-REFLECTION-BRIDGE337, LSPV-2 LOW-SUPPORT-MINCORE343, LSPV-3
PROVENANCE-KRAFT342/BPHP-EXTENSION343, LSPV-4
NODE-EVIDENCE-DOMINATION342, issue #3, REFEREE294--296, and the prior
F15 oracle experiment.

**Adopted:** the prior experiment's oracle-else-random definition and its
source-aware DPLL comparison; the fixed-calculus separation between node cost
and encoded proof evidence; the need for finite-length correctness evidence in
any proposed bridge.

**Rejected:** treating fixed oracle accuracy as polynomial; treating
preenumerated survivor conditioning as free; extending a SAT witness oracle to
UNSAT; converting proposal count into a minimum derivation lower bound.

**Retired/stale:** no verified theorem is retired.  The prior F15 numerical
experiment remains valid finite evidence; its asymptotic no-repeat question is
now resolved by the exact theorem above.

**Root change:** add REFEREE297 as a method/transfer audit before REFEREE296.
Do not modify other owners' regions.

## Exact next gap

The useful next experiment is no longer another fixed-percentage trial.  It is
to define a **source-computable predictor** whose effective error satisfies
\(1-q(n)=O(\log n/n)\) on every satisfiable input, charge its acquisition and
all failures, and separately provide sound UNSAT refutations.  Without both
properties it is not an ordinary polynomial total decider and cannot support
B3.

Independently, the principal proof target remains a superpolynomial
\(\overline W_R\) lower bound and an ordinary nonrelativizing B3 bridge for the
same fixed representation-inclusive mixed calculus.  Both remain OPEN.

## Reproducibility

* producer:
  \`experiments/arc/lspv5_297/oracle_no_repeat_rank_referee297.py\`
* independent verifier:
  \`experiments/arc/lspv5_297/verify_oracle_no_repeat_rank_referee297.py\`
* raw:
  \`results/raw/arc/2026-11-02_1448_LSPV5_ORACLE_NO_REPEAT_RANK_REFEREE297_raw.json\`
* verification:
  \`results/raw/arc/2026-11-02_1448_LSPV5_ORACLE_NO_REPEAT_RANK_REFEREE297_verify.json\`


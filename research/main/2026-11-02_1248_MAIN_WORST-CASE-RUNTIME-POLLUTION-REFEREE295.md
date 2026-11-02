# PNP Independent Proof Red Team — REFEREE295

**Run:** 2026-11-02 12:48 America/Los_Angeles  
**Task identity/status:** preserved exactly; no task or schedule operation was performed.  
**Scientific status:** P versus NP remains **OPEN**.

## Result at a glance

This run proves a concrete separation between the pointwise bridge B1 and the
worst-case bridge B2.  For one fixed, sound, complete, effective calculus
\(R_{RW}\) (source-axiom Resolution plus Weakening, unit inference-node
weights), there is a fixed total correct SAT decider \(A^\dagger\) such that:

1. **B1 fails:** on a polynomially recognizable odd-Tseitin expander family,
   \(A^\dagger\) runs in polynomial time while
   \(W_{R_{RW}}(F)=2^{\Omega(h)}\); under the explicit unary-index encoding
   used here, \(|F|=O(h^2)\), so this is still superpolynomial in \(|F|\);
2. **B2 holds:** \(A^\dagger\) deliberately waits for
   \(2^{|S_k|^2}\) steps on a dense family of valid SAT sentinels \(S_k\), so
   its unrelated worst-case time dominates the elementary universal upper
   bound \(\overline W_{R_{RW}}(N)<2^{N+1}\).

Thus **B2 does not imply B1**.  A B2 inequality for a slow decider can be true
for the wrong reason: worst-case runtime on unrelated valid SAT inputs can pay
for every shortest refutation at that length.  This is a
**WORST-CASE-TRANSFER FIREWALL**, not a lower bound for SAT and not a failure of
B3.  B3 remains the primary open bridge because it speaks only under the
existence of a polynomial-time SAT decider.

Adding a sound XOR/GF(2) rule to the calculus destroys the proposed Tseitin
hard family.  Therefore the lower-bound ingredient is explicitly
**RESTRICTED to \(R_{RW}\)**; it cannot be promoted to the desired
representation-inclusive mixed calculus.

Concurrent shared-handoff readback after the proof was completed exposed
LSPV-4 result 341, which independently proves the same logical B1/B2
separation pattern for Resolution using pigeonhole formulas and a delay on
other/malformed strings.  REFEREE295 is therefore an **independent
reproduction with a valid-input strengthening**, not a first novelty claim:
its B2 budget is forced entirely by valid SAT sentinels, so malformed-input
runtime is unnecessary, and its universal upper bound is the explicit
\(2^{v+1}-1\) blocking DAG.

## Fixed objects

### Explicit input encoding

A valid formula has \(n,m\ge1\), nonempty clauses, and no repeated variable in
a clause.  Its binary encoding is

\[
  1^n0\;1^m0\;\prod_{C}\left(1^{|C|}0
  \prod_{\ell\in C}(\operatorname{sign}(\ell)\;1^{|\ell|}0)\right).
\]

All indices must lie in \([n]\), and the parser must consume the entire string.
Nonbinary, unterminated, out-of-range/duplicate, or trailing-bit strings are
rejected.  This is a binary, polynomially decodable encoding of the usual
nonempty-clause CNF-SAT language; allowing an explicit empty-clause token would
only add an immediate one-node contradiction case.

The valid SAT sentinel
\(S_k=(x_1)\wedge\cdots\wedge(x_1)\) with \(k\) repeated clauses has exact
encoded length

\[
  L_k=6k+3.
\]

Hence for every \(N\ge10\), the largest \(L_k\le N\) obeys \(L_k>N-6\).

### Calculus \(R_{RW}\)

The source clauses are zero-cost axioms.  Every inference node has unit weight:

* **Weakening:** from clause \(C\), infer any \(D\supseteq C\).
* **Resolution:** from \(C\vee x\) and \(D\vee\neg x\), infer
  \(C\vee D\).

Proofs are encoded acyclic shared DAGs with parent indices smaller than the
child index, explicit rule tags, pivot/source indices and result clauses.  The
terminal clause is empty.  Rule checking is polynomial in the encoded DAG.
The system is fixed before all instances and is sound, complete and effective.
Free selection of the best proof is allowed in \(W_{R_{RW}}\).

## Exact lemmas

### Lemma 1 — universal blocking-clause upper bound (PROVED)

If an UNSAT CNF \(F\) has \(v\) variables, then

\[
 W_{R_{RW}}(F)\le 2^{v+1}-1.
\]

**Proof.** For every assignment \(\alpha\in\{0,1\}^v\), choose a source
clause \(C_\alpha\) falsified by \(\alpha\).  Let

\[
 B_\alpha=\bigvee_{i:\alpha_i=0}x_i\ \vee
             \bigvee_{i:\alpha_i=1}\neg x_i
\]

be the full blocking clause uniquely falsified by \(\alpha\).  Every literal
of \(C_\alpha\) belongs to \(B_\alpha\), so one Weakening inference derives
\(B_\alpha\).  Pair blocking clauses whose assignments differ only in the
last coordinate and resolve that coordinate.  Repeating upward through the
complete binary decision tree derives the empty clause.  There are \(2^v\)
Weakening nodes and \(2^v-1\) Resolution nodes.  Shared DAG accounting counts
each once.  Since \(v\le |\operatorname{enc}(F)|\),
\(\overline W_{R_{RW}}(N)<2^{N+1}\).  ∎

The proof is constructive but is used only as an upper bound on the freely
chosen minimum.  Its discovery cost is irrelevant to \(W_R\), consistently
with the user-approved model.

### Lemma 2 — one fixed total decider (PROVED)

Define \(A^\dagger\), independently of inputs:

1. parse the explicit encoding; reject malformed strings;
2. if the input is a sentinel \(S_k\), execute exactly \(2^{L_k^2}\) charged
   no-op steps and return SAT;
3. if the input authenticates as a CNF encoding of a Tseitin parity system,
   extract its equations, perform Gaussian elimination over GF(2), and return
   the exact SAT/UNSAT result;
4. otherwise enumerate all assignments and decide the CNF exactly.

Every branch is effective and exact on both labels.  Recognition of the
canonical Tseitin syntax, extraction and Gaussian elimination are polynomial.
The fallback makes the decider total on every valid formula.  The delay can be
implemented by an \(L_k^2\)-bit counter, so it is real charged work rather than
an oracle or an after-answer constant circuit.

### Theorem — B2 can hold while B1 fails (PROVED, SYSTEM-RESTRICTED)

Choose a standard polynomially recognizable constant-degree expander-Tseitin
family \(U_h\) with odd total charge.  Urquhart's
expander construction and the width-size analysis of Ben-Sasson and Wigderson
give

\[
  W_{R_{RW}}(U_h)=2^{\Omega(h)}.
\]

Weakening does not invalidate the standard general-Resolution lower bound.
The explicit audit encoding uses unary variable indices, so
\(|\operatorname{enc}(U_h)|=O(h^2)\); consequently the displayed bound is at
least \(2^{\Omega(\sqrt{|U_h|})}\), more than enough to exceed every
polynomial in the encoded length.
On this same family, \(A^\dagger\) uses syntax authentication plus Gaussian
elimination and therefore has \(T_{A^\dagger}(U_h)=\operatorname{poly}(|U_h|)\).
No polynomial \(p_{A^\dagger}\) can satisfy B1.  This is a
**POINTWISE-TRANSFER FAILURE** for the fixed pair
\((R_{RW},A^\dagger)\).

For B2, take the largest sentinel length \(L_k\le N\).  For every \(N\ge10\),

\[
 T^{wc}_{A^\dagger}(N)\ge2^{L_k^2}
 \ge2^{N+1}>\overline W_{R_{RW}}(N),
\]

because \(L_k>N-6\) and \((N-6)^2\ge N+1\).  The finitely many smaller
lengths are absorbed by the fixed polynomial \(p(z)=1024+z\).  Therefore B2
holds for this same fixed \(R_{RW}\) and \(A^\dagger\).  ∎

## Correct classification of the three bridges

| Obligation | Status from this run | Reason |
|---|---|---|
| B1, pointwise | **FALSE for the concrete pair** | Easy authenticated Tseitin branch versus exponential \(R_{RW}\) proofs |
| B2, worst-case | **TRUE for the concrete pair** | Valid SAT-sentinel delay dominates the universal proof upper bound |
| B3, `SAT in P` ⇒ polynomial \(\overline W_R\) | **OPEN** | \(A^\dagger\) is deliberately superpolynomial, so this construction is irrelevant to B3's antecedent |

This proves the implication B1⇒B2 is strict in general.  It does **not** prove
that B2 is false for all deciders, that B2 implies B3, or that B3 fails.  It
also explains why a fast algorithm on a single hard-for-\(R\) family refutes
B1 but need not touch B2/B3.

## Four falsifiers applied

1. **Sentinel invalidity or sparsity.** Falsified as an objection: all
   sentinels are valid SAT CNFs and have exact lengths \(6k+3\), so the gap is
   six bits.  The finite audit checked \(k=1,\ldots,16\) and all
   \(N=10,\ldots,160\).
2. **Wrong blocking-clause polarity or missing assignments.** Falsified as an
   objection: an independent checker verified complete blocking formulas for
   one through six variables, with exact costs
   \(3,7,15,31,63,127\).  The two-variable four-clause UNSAT control has a
   checked seven-node proof.
3. **Hidden SAT/equivalence oracle.** Falsified as an objection: the sentinel
   branch is syntactic, Tseitin membership/extraction is explicit polynomial
   parsing plus GF(2), and every remaining valid CNF is decided by paid
   exhaustive search.  Malformed strings are rejected before all branches.
4. **Representation switch defeats the hard family.** **Confirmed.** If the
   fixed calculus is extended with sound charged XOR extraction/addition, the
   Tseitin contradiction has a short parity proof.  Therefore the family is
   not a candidate for the desired representation-inclusive mixed \(R\).

## Both-label and malformed controls

* SAT: sixteen sentinels \(S_k\), each parsed, round-tripped and witnessed by
  \(x_1=1\).
* UNSAT: the four complete clauses on two variables, plus complete blocking
  CNFs on one through six variables.
* Malformed: nonbinary symbol, unterminated unary field, out-of-range literal
  and trailing bit; all four were rejected.

The finite program does not re-prove Urquhart/Ben-Sasson--Wigderson.  It checks
only the new constructive and arithmetic obligations surrounding that cited
lower bound.

## Work and peak-space ledger

For the mathematical decider \(A^\dagger\): parsing and sentinel/Tseitin
authentication cost polynomial time and at most polynomial live space;
Gaussian elimination costs polynomial time and \(O(N^2)\) materialized bits
under a dense implementation; fallback enumeration costs exponential time and
\(O(N)\) assignment space plus input storage; the sentinel delay costs
\(2^{L^2}\) steps and an \(O(L^2)\)-bit counter.  These are all-phase peaks:
input parsing, authentication, conversion and delay allocation are included,
not merely child-call space.  No materialized child recursion or FLMV transfer
is claimed.

The producer's measured audit run (six-variable sweep, 151 envelope lengths)
charged encoding, parsing, exact SAT/UNSAT enumeration, proof construction,
rule verification, malformed controls and envelope arithmetic.  The recorded
host values are in the raw JSON; they are diagnostic, not native-machine
complexity bounds.  The intentionally specified delay was checked
symbolically and not wastefully executed.

## Literature and repository search log

Searches were performed before proof finalization.

* `Cook Reckhow relative efficiency propositional proof systems 1979 pdf` —
  primary paper found: Cook and Reckhow, *The Relative Efficiency of
  Propositional Proof Systems*, JSL 44(1), 1979,
  <https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf>.
  It establishes the proof-system framework and the polynomially bounded proof
  system/coNP connection; it does not supply B1/B2/B3 for this \(R\).
* `Urquhart hard examples resolution Tseitin formulas 1987 pdf` — primary
  metadata/abstract found: Urquhart, *Hard Examples for Resolution*, JACM
  34(1), 1987, DOI <https://doi.org/10.1145/7531.8928>.  It states exponential
  Resolution lower bounds for expander-based Tseitin clauses.
* `Ben-Sasson Wigderson short proofs are narrow resolution 2001 pdf` — primary
  PDF found: <https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf>.
  It relates Resolution width and size and recovers expander lower bounds.
* `GitHub resolution proof verifier Tseitin Gaussian elimination SAT` — found
  the public shortest-Resolution tool <https://github.com/peitl/short-proof>
  and XOR-SAT implementations; no universal transfer result was found.
* Project GitHub search `B2 worst-case derivation delayed sentinel` returned
  no indexed match before proof finalization.  Project search `Tseitin
  Gaussian elimination resolution lower bound` recovered the current LSPV-1
  restricted Resolution barrier and the LSPV-2 mixed-system escape,
  consistent with this classification.  A later full shared-handoff readback
  revealed the concurrent LSPV-4 WORSTCASE-DELAY-BRIDGE341 result.  It is now
  explicitly treated as prior/concurrent convergent work; the valid-SAT-only
  sentinel strengthening above is the remaining distinction.
* `github.com/openai` repository searches for `Tseitin Gaussian elimination
  resolution proof` and `propositional proof system simulation` returned no
  matching code.  Broader web search returned unrelated current OpenAI math
  manuscripts, which were not used.

No novelty is claimed for Resolution lower bounds, Gaussian elimination, the
Cook--Reckhow framework, or deliberate slowdown.  The project-specific result
is the exact bridge-classification counterexample under the newly fixed
B1/B2/B3 vocabulary.

## Exact next gap

The primary target is still B3 for one genuinely representation-inclusive,
fixed, sound, complete, effective mixed calculus \(R\).  The next useful
attack is a **normalization-or-escape dichotomy**: either give a polynomial
translation from every polynomial-time SAT decider (under the B3 antecedent)
to polynomial-cost \(R\)-DAGs in the worst case, or exhibit a concrete
polynomial-time decider hypothesis whose rejecting computations cannot be
converted without using a hidden correctness axiom.  Worst-case runtime of a
known superpolynomial decider must not be used as the budget.

## Artifacts

* `experiments/arc/lspv5_295/b1_b2_separation_referee295.py`
* `experiments/arc/lspv5_295/verify_b1_b2_separation_referee295.py`
* `results/raw/arc/2026-11-02_1248_LSPV5_B1_B2_SEPARATION_REFEREE295_raw.json`
* `results/raw/arc/2026-11-02_1248_LSPV5_B1_B2_SEPARATION_REFEREE295_verify.json`


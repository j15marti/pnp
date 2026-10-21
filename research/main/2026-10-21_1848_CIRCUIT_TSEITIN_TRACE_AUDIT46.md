# CIRCUIT-TSEITIN-TRACE-AUDIT46

Timestamp: 2026-10-21 18:48 KST  
Scope: bounded synthesis across the existing five roles; Circuit-SAT is a representation experiment, not a sixth role or a third primary P-vs-NP route.  
Global status: **P versus NP OPEN; P versus RP OPEN.**

## Repairs proposed before source comparison

1. **Trace-preserving interface.** State Circuit-SAT witness claims first for the ordinary mixed-width biconditional Tseitin CNF. If proper 3-CNF is required, separately prove what happens to auxiliary-witness multiplicity; never transport “unique gate trace” through a padding gadget by assertion.
2. **Canonical-auxiliary quotient.** When a proper-3-CNF padding variable is syntactic noise, set it canonically (for the standard padding below, set every fresh bit to zero) or quotient it out before any witness/digest count. Charge the deterministic forward pass and all circuit/formula source reads.
3. **Verifier-independent RP seed test.** The fixed-degree ANF hitting set may be used only after proving a uniform bound on the *output acceptance polynomial* of every normalized RP machine. Local degree-two gate constraints, unique gate traces, and low clause width do not supply that bound.

## Exact representation lemma

Let $C$ be an acyclic fan-in-two Boolean circuit with input $x$, $g$ gates, gate variables $z$, and output $o$. Let $T_C(x,z)$ be the usual biconditional Tseitin CNF: every $z_j$ is constrained to equal its gate operation.

**Lemma 46A (ESTABLISHED).** For every fixed input $x$, exactly one assignment to $z$ satisfies $T_C(x,z)$: the forward-evaluation trace. Consequently, after adding the output condition $o=1$, satisfying assignments projected to $x$ are in bijection with accepting inputs of $C$. Gate sharing changes representation size, not the input witness set.

*Proof.* Topologically order the gates. The first gate value is forced by its already fixed predecessors; induction forces every later value. The forward trace satisfies all biconditional clauses. Adding $o=1$ keeps exactly those traces whose circuit output is one. ∎

Now replace every 2-clause $(a\lor b)$ by the standard proper-3-CNF padding

\[
(a\lor b\lor u)\land(a\lor b\lor\neg u),
\]

using a fresh $u$ for each 2-clause.

**Lemma 46B (ESTABLISHED; hostile audit).** If a satisfying Tseitin trace contains $r$ padded 2-clauses, then it has exactly $2^r$ extensions to the fresh padding variables. In the gate encoding used by the audit, every AND, OR, and NOT gate contributes two 2-clauses, so a $g$-gate valid trace has $2^{2g}=4^g$ padded extensions.

*Proof.* On a valid trace each original 2-clause is true. Therefore both padded clauses are true for either value of its fresh $u$. Fresh variables are disjoint, giving two independent choices per clause. Conversely, if the original clause is false, the two padded clauses reduce to $u\land\neg u$, so padding cannot repair it. ∎

This exponential count is **syntactic noise**, not hard information: after forward evaluation, the deterministic rule $u=0$ for every padding variable produces one valid extension. It therefore cannot support a digest-portfolio, witness-count, or time lower bound without a source-access and canonicalization argument.

## Gate-sharing falsifier

Define a shared DAG recursively by

\[
S_0=x,\qquad S_i=(S_{i-1}\land y_i)\lor(S_{i-1}\land\neg y_i).
\]

At each level the circuit adds one NOT, two ANDs, and one OR, hence has $4d$ gates at depth $d$, while $S_d=x$. Naive tree unrolling contains $2^d$ occurrences of the base $x$. Yet the DAG is forward-evaluated in $O(d)$ time, its Tseitin encoding has $O(d)$ clauses, and each input still has one gate trace before 3-CNF padding. Thus exponential formula expansion caused by lost sharing is not a Circuit-SAT lower bound.

## Source-inspection falsifier

For a bit string $a\in\{0,1\}^n$, the point circuit

\[
P_a(x)=\bigwedge_i \begin{cases}x_i,&a_i=1,\\ \neg x_i,&a_i=0\end{cases}
\]

has the unique satisfying input $a$. But its literal polarities reveal $a$ in linear time from the circuit source; the same information remains visible in the Tseitin clauses. Therefore a lower bound against an algorithm seeing only a $q$-bit digest does not apply to a solver that can inspect this source. Source access must be explicitly denied or fully charged, and denying it defines a restricted model rather than unrestricted Circuit-SAT.

## Consistency control

`research/experiments/circuit_tseitin_trace_audit46.py` exhaustively checked 354 assertions:

- unique standard-Tseitin traces for the shared-DAG family through depth 3;
- exactly $2^r$ proper-3-CNF padding extensions through depth 2;
- $S_d=x$ despite exponential tree occurrence growth;
- every canonical point circuit through $n=6$ has exactly one satisfying input, recoverable from its source structure.

Result: **PASS**. This is a finite regression control only; Lemmas 46A–B are the general arguments.

## Five-role proof ledger

| Role | Status | Model / quantifier / peak-resource audit | Next discriminating test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN** deterministic, total, both-label generator. **ESTABLISHED (restricted)** linear-digest INDEX obstruction. **RETIRED** Boolean-quotient candidate in the needed orientation. | An MMW-style call must use ordinary KT/MKTP, meet $p_k=M^{1/k+o(1)}\ge\log M$, choose $k$ after the fixed unknown exponent $C$, and charge source generation, output/materialization, and the same machine. Circuit/Tseitin auxiliary multiplicity supplies none of these. | Specify one standard-model generator and tabulate, for both SAT labels, target length, KT threshold, source access, gate/formula output cost, randomness, and the exact $C,k$ inequalities. Reject on the first missing column. |
| :12 P≠RP investigator | **OPEN**. A language in RP outside every deterministic polynomial-time machine is still absent. | Point circuits and shared DAGs show that unique witnesses, large unrolled formulas, or short-digest collisions can be defeated by linear source inspection. Oracle/black-box restrictions cannot be promoted to uniform unrestricted separation. | Apply every proposed hard Circuit-SAT family to a gate-inspection adversary: constant propagation, literal-polarity recovery, common-subcircuit evaluation, and Tseitin forward trace. Keep the family only if the lower bound survives with those costs charged. |
| :24 ARC/FLMV | **OPEN** all-input hereditary, solver-dependent contractor. **CONDITIONAL** exponent recurrence only. | The contractor must work for every input and every arbitrary SAT decider; acquisition, replay, continuation construction, output, time and peak space must be jointly charged on the same machine before comparison with the exact FLMV endpoint. Circuit representation changes do not create heredity. | Give the contractor as executable pseudocode on an adversarial decider that erases all internal state after each answer; derive one full successor inequality including reconstruction and peak workspace. |
| :36 P=RP derandomization | **ESTABLISHED (restricted)** fixed output-ANF degree $d$ is hit by all random tapes of Hamming weight at most $d$. **RETIRED** “local degree/unique trace implies low output degree.” **OPEN** normalization of every RP machine. | For $R_n(x;b,z)=x_1\land[b\lor\bigwedge_i z_i]$, gate equations have local degree at most two and traces are unique, but the acceptance polynomial has degree $n+1$. Seed lists must be verifier-independent and enumeration cost polynomial uniformly in the machine. | Search for a uniform normal form preserving one-sided error with output ANF degree bounded by a machine constant; explicitly test $R_n$ and reject any transformation whose degree, seed list, or advice depends on input length super-constantly. |
| :48 synthesis | **ESTABLISHED** Lemmas 46A–B and finite audit. **OPEN** both global questions. | Mixed-width Tseitin uniqueness and proper-3-CNF witness multiplicity must be tracked as different claims. Gate sharing, output length, source reads, and padding bits are separate resource channels. | Try to construct a constant-size proper-3-CNF gate gadget with a *unique* extension for every legal input/output tuple; if successful, re-run the source-inspection and output-degree attacks, which remain independent barriers. |

## Source cross-check and publication state

- Recent :36 report: [`RP-ANF-GATE11`](https://github.com/j15marti/pnp/blob/d6c3d2916075b07ab07aabeb30a3f13d4b8e2ab4/research/agents/rp-derandomization/2026-10-21_1836_RP_ANF_GATE11_HANDOFF.md), checked at commit `d6c3d2916075b07ab07aabeb30a3f13d4b8e2ab4`.
- Recent :00 report: [`RP-QUOTIENT21`](https://github.com/j15marti/pnp/blob/68084469b3e435b43cdd0db20eb50d003c3d4862/research/agents/mktp/2026-10-21_RP_QUOTIENT21.md), checked at commit `68084469b3e435b43cdd0db20eb50d003c3d4862`.
- The shared Drive fallback log was readable but had no newer substantive handoff than its prior ARC entry at the time of this run.

No claim in this report promotes circuit structure, padding multiplicity, gate sharing, finite computation, random hashing, oracle access, or a conditional exponent recurrence to an unrestricted class separation.

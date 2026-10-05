# RETURNMAP2 concrete candidate attacks

Status: COMPUTATIONAL / EXACT elementary lemmas / OPEN bridge. P versus NP remains OPEN.

## Candidate A: direct restriction-to-CNF

Let F be an n-variable CNF. Fix n-m variables by a partial assignment rho and return Q=F|rho on at most m live variables.

Exact semantic condition for a single returned Q:
SAT(F) iff SAT(F|rho).

This equivalence is not true for an arbitrary fixed rho. It is true only if rho is guaranteed to extend some satisfying assignment whenever F is satisfiable. Acquiring such a rho is a witness/selector problem.

Hostile result A1:
- If rho is chosen without SAT-dependent acquisition, adversarial satisfiable formulas can put all satisfying assignments outside that subcube.
- If rho is acquired by standard SAT self-reduction using the assumed decider, the construction makes near-current-scale SAT calls and DELAY retains the unknown exponent.
- If polynomially many restrictions are ORed to preserve all assignments, RESTRICTCOVER1 applies: q 2^m >= 2^n. A polynomial q leaves m=n-O(log n), so no power shrink.
Status: FALSIFIED/RETIRED as a generic return.

## Candidate B: PCPP/reconstruction verifier-to-CNF

Take a declared SU/vMS reconstruction state S and define a nondeterministic verifier V_S(w) for a legal accepting completion/witness. Compile existence of w with Cook-Levin/Robson/Tseitin to Q.

This is well typed as SAT once V_S is exact. But if V_S takes time tau(T), generic encoding writes Q of size tau(T) up to polylog/model factors.

Hostile result B1:
- This repairs TYPE.
- It triggers GENERICENC.
- If tau contains a call to the original SAT decider on scale T^delta, DELAY additionally retains delta*K.
- If V_S merely verifies a PCPP/reconstruction object without exact equivalence to original SAT, the semantic biconditional itself is missing.
Status: FALSIFIED/RETIRED as the generic Boundary-Squeeze return. Source-specific circuit structure could still change this only via a new theorem.

## Candidate C: Williams-style same-representation self-model

Try to encode the action of the assumed SAT algorithm A on source-generated subinstances inside the source representation S, and return a new ordinary CNF Q without generic computation encoding.

Required identity:
SAT(F) iff SAT(Q_A(F,S)),
with |Q_A|=T^(zeta+o(1)), zeta<1 or a typed return cycle of gain below one.

Hostile result C1:
There are three exhaustive accounting cases for the current implementation proposal:
1. Q explicitly contains/simulates the code and current-scale computation of A. Then generic/self-simulation cost must be proved source-specifically; absent such a theorem, Cook-Levin/Robson is the available model-matched route and GENERICENC fires.
2. Q calls A as an oracle on a near-current-scale instance. DELAY fires and retains K.
3. Q does neither. Then a new source-specific semantic identity must prove how SAT(F) is determined by the smaller source state without A. No such identity is presently in SU/vMS.
Status: OPEN as a new theorem schema, not instantiated.

## Candidate D: many-query source return

Permit q=T^(eta+o(1)) ordinary SAT queries, each of length T^(theta+o(1)), and combine their answers in T^(r+o(1)) work.

Conditional exact accounting:
C >= max(r, eta+theta*K)
before recursive closure. If recursively source-matched and theta<1, RECURCLOSE1 gives fixed point max(r,eta/(1-theta)), subject to all acquisition and representation charges.

This candidate is not killed merely because it has many queries. It becomes interesting only if actual source-certified queries exist.

Diagnostic from Dell-van Melkebeek:
for d-CNF, sufficiently small aggregate oracle communication would imply coNP subset NP/poly. This is a useful sanity check, but cannot be the terminal contradiction under P=NP.

Status: CANDIDATE accounting only; source return map OPEN.

## Finite adversarial controls to implement

A. Restriction selector control:
Generate small CNFs with a unique satisfying assignment. Enumerate restrictions leaving m variables. Measure what fraction of restrictions preserve satisfiability. This demonstrates that fixed restriction choice has no semantic guarantee.

B. Cover control:
For n,m,q verify union of q m-dimensional subcubes is at most q*2^m and compare with 2^n. Random overlaps only worsen coverage.

C. Return-ledger sweep:
Sweep eta,theta,r and compute C*=max(r,eta/(1-theta)) for theta<1. Reject any point whose construction invokes a current-scale SAT call, generic encoding, or full-input carry.

D. Same-representation placeholder:
Require a candidate to provide explicit functions Encode, Step, Decode and prove that their composition remains in the same representation family with charged size. Missing any function is an OPEN arrow, not an inferred construction.

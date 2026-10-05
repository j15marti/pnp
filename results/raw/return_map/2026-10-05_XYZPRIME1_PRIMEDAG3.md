# XYZPRIME1 and PRIMEDAG3 finite audit

Status: COMPUTATIONAL finite controls and representation audit only. P versus NP remains OPEN.

## XYZ state proposal

Interpret an incidence state as a triple (x,y,z):
- x: variable identity, carried by a unique prime p_x.
- y: Boolean assignment value of that variable.
- z: polarity or operation label for the current incidence, with z=0 direct and z=1 negated.

Literal value is y xor z.

### Exhaustive n=5 signed-clause test
There are 80 signed width-3 clauses.

For each fixed 3-variable support there are 8 sign patterns, hence 28 unordered sign-pattern pairs. Across the 10 variable triples this gives 280 clause pairs sharing identical x coordinates but differing in z.

Result:
- all 280 of 280 same-x clause pairs were semantically distinguished by at least one assignment;
- all 2,560 clause/assignment evaluations reconstructed exactly from the XYZ rule;
- zero reconstruction failures.

Thus z is semantically essential when it denotes current literal incidence polarity.

### Provenance-only control
If y is instead defined as the already-evaluated literal truth and z merely records whether a NOT occurred historically, then standard future CNF contexts consume current truth plus their own polarity and do not inspect historical z.

For 10 x,y pairs with alternate historical z labels, zero future semantic differences occurred in the tested ordinary-literal context signatures.

Therefore historical z alone is provenance, whereas incidence z is semantic.

## Relation to known graph representations
Signed SAT factor graphs already label variable-clause incidences by positive/negative polarity. The proposed extra instrumentation is to retain simultaneously:
1. unique identity token p_x,
2. assignment state y,
3. incidence/operation label z,
through multisign DAG transformations.

This should be treated as an annotated signed-factor/hypergraph state, not as a novel use of polarity by itself.

## PRIMEDAG3 representation-bypass controls

The previous raw contextual quotient cannot be interpreted as hardness because easy families admit compact evaluators.

Concrete n=5 controls:

### XOR
A 16-constraint sample reduced by GF(2) row reduction to rank 5. A direct stored augmented RREF uses at most 5*(5+1)=30 bits in this finite sample. The key point is not this constant but that affine structure is maintained by Gaussian elimination without enumerating all contextual states.

### 2-SAT
Five variables yield ten literal nodes. A full implication transitive-closure descriptor uses a 10x10 = 100-bit Boolean matrix in the finite control. SCC/implication algorithms decide satisfiability without enumerating the earlier semantic-context quotient.

### bounded-treewidth-like path control
For clauses restricted to consecutive windows of three variables, left-to-right dynamic programming uses a two-variable separator. Only 2^2=4 separator assignments are needed at one boundary, despite the earlier experiment producing more than 20,000 global contextual states for sampled clause orders.

## Consequence

Raw contextual diversity is FALSIFIED/RETIRED as a hardness proxy.

The XYZ prime coordinate remains useful as an audit namespace:
- x prevents accidental identity collision;
- y records current Boolean state;
- z records semantic incidence polarity or typed operation;
- an additional history coordinate would be required if derivational provenance itself is to be retained.

A useful next invariant must quotient XYZ-labelled states by a certified compact representation class, not simply count prime supports or semantic masks.

Open target:
Given a source-matched multisign DAG node v, define a model-matched compact representation R_v and test whether the SAT-distinguishable XYZ quotient contains a growing residual not absorbed by R_v, while charging acquisition, construction, update, replay and SAME_REALIZATION costs.

No unrestricted lower bound or arbitrary-algorithm transfer is established.

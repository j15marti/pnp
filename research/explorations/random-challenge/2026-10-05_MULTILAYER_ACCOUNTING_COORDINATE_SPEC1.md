# MULTILAYER ACCOUNTING COORDINATE SPECIFICATION 1

Date: 2026-10-05
Status: CANDIDATE framework with PROVED/EXACT definitional rules and COMPUTATIONAL finite tests.
Project status: P versus NP remains OPEN.

## 1. Purpose and nonclaim

This document formalizes the multilayer computational accounting system developed in the return-map, provenance, BOOL/SIL, LQP, and trajectory-ledger experiments. Its purpose is to retain rather than discard distinctions among source identity, semantics, provenance, representation, access, loss, reconstruction, aggregation, and cost.

The audit layer is deliberately overcomplete and append-only. The computational machine is not required to store the audit layer.

Nothing in this specification proves a superpolynomial lower bound. In particular, none of the following alone is a hardness measure: semantic multiplicity, source-support size, prime-product magnitude, lineage-DAG size, history length, live-support area, dependency churn, representation size, opacity of an operation, provenance difference, or existence of an accounting hole.

Permanent guard:

existence != acquisition != recoverability != access != verification != decision cost.

semantic object != machine state != audit history != runtime.

## 2. Global objects

A computation is a sequence of machine states M_0,...,M_T together with an append-only audit DAG

T = (V,E).

The audit DAG records source identities and transformations. Nodes are never deleted from T, even when the machine forgets their corresponding information.

Each audit node v has a realization identifier RID(v). SAME_REALIZATION obligations require resources jointly charged in a claim to refer to the same declared realization unless an explicit model-preserving and charged transfer is supplied.

## 3. Full coordinate record

A maximally informative node/event record may contain

A_t = (
  ID, t, RID,
  X, K, Y, Z,
  H,
  J_origin, J_syn, J_sem, J_live^U,
  P_origin, P_syn, P_sem, P_live,
  B, U, Phi_U,
  Vprov, Psi_V,
  R, Eenable, Ccert, Q,
  G,
  L, W, Aaccess,
  Omega_D, Omega_G,
  Fate, Delta,
  C_acquire, C_access, C_combine, C_forget,
  C_reacquire, C_copy, C_delay, C_semantic, C_transport
).

Coordinates are not merged merely because one can sometimes be derived from another. Redundancy is permitted for auditability.

## 4. Identity coordinates

### 4.1 X: variable/source-object identity

X records stable identities of variables or other atomic source objects. An identity survives changes in value, representation, polarity, or current liveness.

### 4.2 K: clause/constraint identity

For a source clause C_j, assign a stable source identity kappa_j. A useful hierarchy is

source identity kappa_j
  -> current residual identity rho_(j,r)
  -> exact derivational-history identity eta_(j,r,alpha).

These levels must not be conflated.

A current constraint node may record

K = (kappa_source, rho_residual, V_live, S_parent, T_operation).

### 4.3 Prime audit identities P

Assign distinct known primes to stable source identities. For a support set J,

P(J) = product over q in J of q.

This is an exact square-free set identifier by unique factorization when the prime namespace is known. It is audit redundancy, not a factoring assumption and not a hardness measure.

Retain separate products P_origin, P_syn, P_sem, P_live when useful.

Repeated use of one source does not square its prime: source support is a set unless an explicitly different multiplicity coordinate is desired.

## 5. Semantic coordinates

### 5.1 Y: current Boolean/semantic value

Y records current Boolean information or a current semantic label. It does not encode derivational cause.

### 5.2 Z: live relation type

Z records a live relation rather than historical cause. Unary historical signs that have the same current Boolean behavior collapse semantically unless the future interface can inspect their history.

Useful relational Z values can include equality, inequality, implication, reverse implication, and higher-arity constraint types.

### 5.3 B: current continuation boundary

B records the variables, source interfaces, separator, or exposed coordinates through which future computation may interact with the current state.

### 5.4 U: continuation universe

U is the declared set or class of legal future semantic observations.

U is generally a partial order, not a scalar resolution level. Two universes of equal cardinality may be incomparable.

For nested universes, write U1 <= U2 when every observation in U1 is available in U2.

### 5.5 Phi_U: abstract continuation semantics

Phi_U(s) = (Obs(s,u)) indexed by u in U.

Define extensional equivalence

s ~_U t iff Phi_U(s) = Phi_U(t).

Phi_U is the correct semantic normalization object for the declared continuation interface. A current answer bit is sufficient only at a genuinely terminal decision interface.

## 6. Provenance coordinates

### 6.1 H: derivational history

H records actual derivational history. It belongs to the append-only audit layer and need not be present in machine state.

### 6.2 Vprov and Psi_V

Vprov is a provenance-query universe, separate from U.

Psi_V(s) is the behavior of state s under provenance queries in Vprov.

Two states may satisfy Phi_U(s)=Phi_U(t) while Psi_V(s) differs from Psi_V(t).

A provenance distinction is computationally relevant only if the legal future interface is entitled or forced to inspect it.

## 7. Four source-support coordinates

### 7.1 J_origin

J_origin records original source identities in the permanent audit ancestry.

### 7.2 J_syn

J_syn records syntactic causal ancestry: source identities that flowed into the construction of the current object.

For a combine node with parents v_1,...,v_k, the default conservative rule is

J_syn(child) = union_i J_syn(v_i),

unless a more detailed typed rule records separate syntactic channels.

### 7.3 J_sem

J_sem records semantic essential support of the represented object. A source is semantically essential when an allowed perturbation of that source can change the represented semantic object.

J_sem may be strictly smaller than J_syn. For example, G(a,b)=a has both inputs in syntactic ancestry but only a in semantic support.

### 7.4 J_live^U

J_live^U records continuation-relevant support: source identities whose perturbation can change some observation in the current universe U.

The intended hierarchy is

J_live^U subseteq J_sem subseteq J_syn subseteq J_origin.

For nested universes U1 <= U2, the intended monotonicity is

J_live^(U1) subseteq J_live^(U2).

These inclusions were exhaustively verified for the finite Boolean-function definitions used in the October 5 tests: all 65,536 Boolean functions on four variables had zero nested-live-support failures and zero J_live subset J_sem failures. This is COMPUTATIONAL evidence for the tested implementation; general use still requires definitions appropriate to the model.

Under restriction rho, the tested residual essential support obeyed

J_sem(f restricted by rho) subseteq J_sem(f)

with zero violations in 16,384 finite restriction cases.

## 8. Representation and escape coordinates

### 8.1 R: concrete representation

R records the actual representation: CNF, residual CNF, bit, BDD, implication graph, SCC DAG, GF(2) matrix/basis, separator table, interpreter, encoded blob, oracle handle, or another declared form.

Representation size is not runtime.

### 8.2 Eenable: escape-enabling state

Eenable records conditions enabling a representation-specific escape or algorithmic mechanism.

Examples include a verified affine representation, implication-graph interface, tree decomposition, or another typed gate.

### 8.3 Ccert: certificate state

Ccert records certificates used to justify a transformation, quotient, decoding, or gate. Existence of a certificate does not imply cheap acquisition.

### 8.4 Q: source reread/reacquisition

Q records explicit rereads or reacquisition from source authority. REACQUIRE is distinct from REVIVAL by decoding or backtracking.

## 9. Source maps

### 9.1 Omega_D: data authority

Omega_D identifies where operand information came from.

Examples: SOURCE_CLAUSES, SOURCE_GRAPH, retained representation, or SEMANTIC_ORACLE.

### 9.2 Omega_G: transformation authority

Omega_G identifies where the combiner or transformation came from.

Examples: MACHINE primitive, PROGRAM_CODE, BDD_BUILDER, Gaussian routine, hypothetical A_SAT code, or ORACLE.

Omega_D and Omega_G identify authority, not cost.

An opaque hypothetical polynomial SAT algorithm must not be declared expensive merely because its implementation is unknown.

## 10. Combiner G

Use a typed combiner record

G = (
  name,
  arity,
  operation,
  support_rule,
  construction,
  primitive_flag,
  implementation_refinement,
  Omega_G
).

When a high-level macro has a known implementation, preserve both the macro transition and its refinement into ordinary operations.

Known macro expansion changes raw event count without changing semantic identity. Raw macro count is therefore not an invariant resource.

COMBINE creates a child audit node with parent edges; it does not delete the parent audit nodes.

## 11. Loss map L

A loss/quotient event is not a scalar forget count. Record

L = (
  name,
  equivalence_relation,
  continuation_scope U,
  before_classes,
  after_classes,
  reversible_flag,
  source_support_preserved,
  same_realization
).

A quotient is semantically valid for U when equivalent states have identical Phi_U behavior.

Examples include same residual clause, GF(2) row-space equivalence, SCC/reachability quotient, separator continuation-table equivalence, and terminal decision equivalence.

IRRELEVANT is always IRRELEVANT_U, never absolute.

A quotient valid for U may fail after scope expansion to U'.

## 12. Recoverability W and access Aaccess

### 12.1 W: recoverability witness

Use

W = (I, D, Sigma),

where I is retained information, D is an explicit decoder/reconstruction procedure, and Sigma is the query scope for which reconstruction is sound.

Information retention alone is not operational access.

### 12.2 Aaccess: access interface and cost

Use

Aaccess = (interface, C_setup, C_query).

The central commutation requirement is

for every u in U:
Aaccess(R,u) = Phi_U(s)(u).

W certifies the relationship between R and Phi_U; Aaccess is the actual operational mechanism.

Examples:
- GF(2) row-space witness plus Gaussian reduction access;
- SCC partition/condensation DAG plus reachability access;
- separator table plus table lookup/join;
- encoded object plus explicit decoder.

An injective opaque encoding with no decoder is information-preserving but not operationally accessible for arbitrary queries.

## 13. Fate and dependency-event ledger

Time-index supports and record dependency events.

BIRTH_t = J_live(t+1) minus J_live(t).
DEATH_t = J_live(t) minus J_live(t+1).
REVIVAL is a BIRTH of an identity that was live earlier.
REACQUIRE is a new source access and is not synonymous with REVIVAL.

Raw counts of BIRTH, DEATH, REVIVAL, or churn are wrapper-gameable and are not hardness measures.

For every disappearing dependency p, record a typed fate such as

RETAINED
ENCODED
QUOTIENTED_U
COMBINED
IRRELEVANT_U
RECOVERABLE_W
TERMINAL
EXTERNAL_ORACLE.

For every reappearance, record DECODE, BACKTRACK, REACQUIRE, or another explicit source-valid transition.

## 14. Delta accounting-consistency checker

Define Delta_t as dependencies that disappear or reappear without a valid typed explanation in the declared realization.

A valid explanation edge should record at least

(dep, source_time, destination_time, TYPE, U, W, Aaccess, RID).

A witness-dependent explanation must provide a real witness and satisfy SAME_REALIZATION unless a charged transfer is explicitly supplied.

Delta is an accounting-consistency diagnostic, not a lower bound.

Finite hostile tests on October 5 gave Delta=0 for COPY, DELAY, valid HIDE/ENCODE, Gaussian quotient, separator projection under its declared U, terminal collapse, and explicit semantic-oracle supply.

Deliberate silent drops, missing witnesses, wrong-realization witnesses, and fake restorations produced nonzero Delta and localized the malformed transition.

## 15. Append-only lineage DAG

The audit DAG T=(V,E) is append-only.

A node record should minimally include

v = (
  ID, time, RID,
  TYPE, OP, PARENTS,
  J_origin, J_syn, J_sem, J_live^U,
  P_origin, P_syn, P_sem, P_live,
  U, Phi_U,
  R, L, W, Aaccess,
  Omega_D, Omega_G,
  cost coordinates
).

COMBINE adds a child with multiple parents.
ENCODE and DECODE add child nodes and retain their parent history.
Machine forgetting changes machine state/status but does not erase audit nodes.

Prime-product support must agree with explicit support sets. Shared ancestry is deduplicated at the source-set level.

Finite tests detected support lies, prime-product lies, missing encoding witnesses, and cross-realization parent combinations.

Lineage size is wrapper-gameable: repeated exact ENCODE/DECODE around the identity function produced arbitrarily many audit nodes while terminal source support and semantics stayed fixed. Therefore |V| and |E| are not hardness measures.

## 16. Convergence and factorization

Two states can have identical continuation semantics but different audit histories:

Phi_U(s)=Phi_U(t)
while
H(s) != H(t), J_syn(s) != J_syn(t), or R(s) != R(t).

If a later operation T receives only the extensional interface Phi_U, then a provenance difference alone cannot make T distinguish s and t.

Classify each operation relative to U by

F_T in {EXTENSIONAL_U, REALIZATION_SENSITIVE, UNKNOWN}.

EXTENSIONAL_U means T factors through Phi_U: there exists a map Tbar with

T = Tbar composed with Phi_U.

REALIZATION_SENSITIVE means T provably does not factor through Phi_U for the declared legal interface.

A useful LQP separation requires a source-matched legal transformation that is inherently REALIZATION_SENSITIVE, not an artificial audit query that was simply granted provenance access.

Finite convergence tests found that direct versus double negation, retained-state versus RECOMP, XOR cancellation versus direct constant, and different-parent-support constructions could have identical Phi_U while retaining different audit coordinates. Exhaustive ordinary postprocessing of the tested extensional interfaces did not recover history. Provenance-aware interfaces did distinguish the histories when authorized.

## 17. Scope expansion and LQP rule

Case A: weak-interface convergence.

Phi_(U0)(s)=Phi_(U0)(t), but for richer U1,

Phi_(U1)(s) != Phi_(U1)(t).

Then a quotient valid only for U0 has discarded distinctions relevant to U1.

Case B: full extensional convergence.

Phi_(Ufull)(s)=Phi_(Ufull)(t).

An ordinary continuation restricted to that extensional interface cannot distinguish the histories merely because the audit DAG differs.

For a transition L_U followed by later scope U', erased distinctions required by U' must be one of:

IRRELEVANT_(U')
RETAINED
RECOVERABLE_W
REACQUIRED_Q
or explicitly supplied by a declared external authority.

Otherwise the audit records an accounting deficit.

## 18. Resource coordinates

Retain separate cost channels:

C_acquire
C_access
C_combine
C_forget
C_reacquire
C_copy
C_delay
C_semantic
C_transport.

A useful decomposition is

C_execution = C_semantic + C_transport,

but no claim should assume a unique decomposition without a declared machine model.

Repeated-query amortization may make preprocessing worthwhile or not worthwhile. Therefore U should include not only query type/scope but, when relevant, demand or multiplicity.

## 19. Hostile controls and falsified generic hardness measures

The following controls must remain cheap when their standard compact mechanisms are supplied:

- affine/XOR/Tseitin with Gaussian elimination;
- 2-SAT with implication graph/SCC;
- Horn with forward chaining;
- bounded-treewidth/separator dynamic programming;
- independent products;
- parity streaming;
- compact BDD/d-DNNF or other legitimate representations when applicable;
- COPY, DEAD, DELAY, INTERP, RECOMP;
- maximal semantic oracle;
- hypothetical A_SAT under the P=NP contradiction assumption.

The following generic implications are FALSIFIED/RETIRED as hardness criteria:

large contextual quotient => hardness.
large J_origin/J_syn/J_sem => large representation.
large global causal support => large depth or superpolynomial work.
large live-support area => hardness.
many dependency deaths/revivals => hardness.
large append-only lineage DAG => hardness.
different provenance with same Phi_U => later ordinary semantic distinguishability.
opaque operation => expensive operation.
prime-product magnitude => computational hardness.
semantic multiplicity => machine-state multiplicity or runtime.

## 20. Easy-family typed escapes

Representation-specific compact mechanisms should be represented as typed escapes rather than universal free rules.

Examples:

2-SAT: implication graph, SCC quotient, condensation reachability.
Horn: forward-chaining closure.
XOR: GF(2) row-space basis and Gaussian access.
bounded treewidth: separator/bag table and join/project.
BDD: compiled decision representation and evaluator.

Each escape should record Eenable, Ccert if any, W, Aaccess, Omega_D, Omega_G, setup/access costs, SAME_REALIZATION status, and the exact U for which it is valid.

## 21. Relationship to SIL/BOOL and TransportCert

SIL remains the semantic/accounting interface. BOOL remains a Boolean-native object/rewrite layer.

The multilayer ledger does not solve the arbitrary-algorithm bridge. In particular, a hypothetical polynomial A_SAT may be represented as a legal program with SOURCE_CNF data authority and A_SAT_CODE transformation authority. The ledger may mark its internal implementation UNKNOWN but may not impute a superpolynomial cost.

The load-bearing bridge remains a model-matched theorem connecting arbitrary exact computation to a forced charged resource. In current terminology, this is closely related to TransportCert / source-flow / realization-sensitive transfer.

## 22. Candidate conservation discipline

The audit discipline is:

Information and dependency identities must not silently disappear or reappear in the audit explanation.

This is weaker than claiming information cannot disappear computationally.

For each dependency p and transition t, require a typed Fate_t(p). If a dependency disappears without a valid fate edge, or reappears without decode/reacquisition/source authority, place it in Delta_t.

This is a consistency theorem/schema once the transition semantics are defined. It is not an unrestricted lower bound.

## 23. Proof-status ledger

PROVED/EXACT:
- prime products are exact square-free support-set identifiers for a known distinct-prime namespace;
- extensional equivalence under Phi_U is preserved by continuations that factor through Phi_U, by definition of factorization;
- append-only audit ancestry can retain syntactic history even when semantic support shrinks.

COMPUTATIONAL:
- all 65,536 four-variable Boolean functions passed the tested nested J_live inclusion and J_live subset J_sem checks;
- 16,384 tested restrictions had no residual-semantic-support expansion beyond original semantic support;
- finite Delta hostile tests accepted valid wrappers/quotients/oracle supply and rejected deliberately malformed drops/witnesses;
- finite lineage tests detected support/product/witness/realization corruption;
- finite convergence tests separated semantic-only from provenance-aware interfaces.

CANDIDATE:
- the full coordinate system as a useful common accounting language across SAT algorithms and representations;
- Delta as a robust implementation-independent accounting-consistency checker once all typed transition semantics are formalized;
- realization-sensitive source-matched operations as a possible LQP hinge.

OPEN:
- any theorem forcing a nontrivial charged resource for every arbitrary polynomial SAT decider;
- a source-matched legal transformation that is necessarily REALIZATION_SENSITIVE in the required sense;
- any nonrelativizing/nonalgebrizing contradiction sufficient for P != NP.

Project status: P versus NP remains OPEN.

## 24. Immediate implementation targets

1. Implement this schema as reusable typed Python classes under src/pnp_lab.
2. Emit machine-readable JSON lineage DAGs for actual DPLL, resolution, SCC, Horn, Gaussian, and separator-DP runs.
3. Fix exact Horn source ancestry and exact edge-labelled SCC provenance.
4. Implement actual resolution parent-support prime products.
5. Add U, Phi_U, Vprov, Psi_V, F_T, Omega_D, Omega_G, W, Aaccess, and Delta to trajectory output.
6. Add independent-product, parity, INTERP, RECOMP, semantic-oracle, and hypothetical-A_SAT controls.
7. Search automatically for pairs of source-matched histories with identical Phi_U but a later legal operation whose behavior does not factor through Phi_U.
8. Never promote finite success to an asymptotic theorem without a complete proof and barrier audit.

## 25. Repository grounding

This specification extends the verified prototype

experiments/return_map/multilayer_trajectory_ledger1.py

whose earlier verified blob was 6e512f8afc131b7727f2f8a2d9a126485b78774e.

It also consolidates the October 5 interactive finite tests of support hierarchy, scope expansion, access/recoverability, wrapper invariance, Delta accounting, append-only lineage, and convergence. Those interactive tests should be converted into committed reproducible runners and raw JSON before their numerical outputs are treated as repository-verified computational artifacts.

END_OF_VERIFIED_SPEC::MULTILAYER_ACCOUNTING_COORDINATE_SPEC1

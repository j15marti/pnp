# LEAD-0021 — Reconvergent-diamond literature audit and path-function tests

Timestamp: 2026-10-06 12:20 PT  
Agent: LEAD  
Global status: **P versus NP remains OPEN.**

## 1. Question

Study a wrapper control graph in which:
- each node branches on an A/B result;
- branches may have very different lengths and may revisit control locations;
- nominal paths repeatedly reconverge;
- every terminating path reaches the same semantic endpoint;
- hidden hash/history state may later cause paths that looked merged to re-separate.

The intended hardness intuition is that exponentially many possible histories or path-induced functions might have to remain distinguishable despite a single final answer.

## 2. Literature map

### 2.1 Reduced OBDDs: exact residual-function analogue

Bollig and Wegener (ECCC TR99-048, building on Sieling-Wegener) state the key structure theorem for a fixed variable order: the number of nodes at a level equals the number of distinct residual/subfunctions induced by assignments to the earlier variables (with the usual essential-dependence refinement).

This is extremely close to our continuation-equivalence quotient:
- histories can merge exactly when their future residual functions agree;
- many distinct residual functions force width in that restricted model.

But the theorem is model-specific: fixed-order OBDD structure supplies the compiler from computation histories to residual functions.

### 2.2 Communication complexity and read-once branching programs

Communication-complexity methods have yielded exponential lower bounds for read-once and related branching programs. They are useful candidate tools for proving that many future continuations cannot share a node, but only after the wrapper is shown to land in the relevant restricted branching-program model.

### 2.3 Barrington: major hostile control

Barrington proved that polynomial-size width-5 branching programs recognize exactly nonuniform NC^1. His construction uses products of permutations, i.e. noncommuting path-dependent function composition in a constant-width state space.

This is directly relevant to the proposed hash-function wrapper:
- different branch values can select different transformations;
- compositions can depend delicately on history;
- nonetheless a very small-width branching program can represent substantial computation.

Therefore noncommutativity, path dependence, recursive composition, or the fact that paths later reconverge cannot alone imply large width or hardness.

### 2.4 General branching-program time-space lower bounds

Beame, Saks, Jayram/Thathachar and related work prove nontrivial time-space tradeoffs and exponential size lower bounds for explicit functions in general or semi-general branching-program models under specified length/space conditions.

These results show that a DAG/state route is not hopeless, but they do not automatically apply to an arbitrary polynomial-time SAT decider. Exact time/model matching remains mandatory.

### 2.5 Pebbling

Pebbling is the natural model for retain-versus-recompute on a forced dependency DAG. Nordstrom's survey explains its use in proof/time-space complexity.

However, a recent universal upper bound of Bilardi-De Stefani shows that arbitrary DAGs admit nontrivial universal space upper bounds. More importantly for this project, a pebbling theorem constrains evaluation of the declared DAG; it does not prove that every SAT solver must instantiate that DAG.

## 3. Formal reconvergent wrapper

A nominal control node v is not the full machine state.

Let a realized state be

S_t=(v_t,z_t),

where:
- v_t is the nominal wrapper node;
- z_t is all persistent hidden state, including any hash/history encoding.

A branch result sigma_t in {A,B} induces

(v_{t+1},z_{t+1})
=
Phi_{v_t,sigma_t}(z_t).

Different histories may reach the same nominal v while carrying different z.

Cycles/recursion are legal. For dependency accounting, a realized execution is time-unrolled, yielding an acyclic execution DAG.

## 4. RIGHT-CONGRUENCE-MERGE1 — PROVED/EXACT

Fix a legal future continuation family C.

Two histories h,h' reaching the same nominal node v are safely mergeable iff every future continuation c in C induces identical required behavior.

Write

h ~_C h'

for this right-congruence / continuation equivalence.

A correct representation at v must distinguish different equivalence classes.

If there are W classes, then any exact persistent state requires at least

ceil(log2 W)

bits.

Important guard:

W=2^d implies only a d-bit state lower bound.

It does not imply 2^d bits, 2^d nodes in an unrestricted implementation, or exponential time.

## 5. DELAYED-RESEP-BITS1 — PROVED/EXACT

Consider d repeated diamonds. Let the branch history be

h=(h_1,...,h_d) in {0,1}^d.

All histories nominally reconverge to the same semantic endpoint.

After reconvergence, allow the future consumer to ask any coordinate query

q_j(h)=h_j.

Then every two histories are future-distinguishable, so

W=2^d.

But the exact history string itself is a sufficient representation of length d, with O(1) coordinate service.

Hence delayed re-separation can make all histories inequivalent while requiring only linear state.

Finite table:
- d=18 gives 262,144 behavioral classes;
- exact sufficient state: 18 bits.

## 6. PARITY-PROBE control

If delayed probes are linear parities

q_a(h)=a dot h mod 2,

then the number of response classes is 2^r where r is the GF(2) rank of the probe family.

A rank-r syndrome of exactly r bits services every probe.

Finite random controls:
- d=14: rank 14, 16,384 behavioral classes, 14 syndrome bits;
- d=18: rank 18, 262,144 behavioral classes, 18 syndrome bits.

Thus exponential future distinguishability can coexist with a compact algebraic sufficient state.

## 7. PATH-PROGRAM-CLOSE1 — PROVED/EXACT

Fix a wrapper whose per-node transition functions have polynomial-size descriptions and polynomial evaluation time.

For any realized path of length L, the path itself (node/branch sequence plus fixed wrapper description) is a straight-line program for the induced composition.

If L=poly(n), then:
- the induced path function has a polynomial-length description;
- it can be evaluated by replay in polynomial time.

Therefore an exponential number of distinct path-induced functions across different histories is compatible with polynomial representation and evaluation for every realized function.

This applies even if the transformations are noncommuting or nonlinear.

If recursion makes L superpolynomial, then the wrapper itself has imposed superpolynomial realized work unless one separately proves that SAT correctness forces that long path and that no shortcut is legal.

## 8. AFFINE-FUNCTION control — COMPUTATIONAL EXACT

Eight-bit affine permutations over GF(2) were used as branch-selected transformations.

At every depth through d=14, all 2^d paths induced distinct affine functions.

At d=14:
- route histories: 16,384;
- distinct affine path functions: 16,384;
- each composed function has a closed-form 8x8 affine representation of only 8^2+8=72 bits;
- the route itself is only 14 bits.

So exponential distinct path-function count does not imply a large representation.

This is the same hostile phenomenon as XOR/Gaussian elimination in the SAT controls.

## 9. NONLINEAR-SLP control — COMPUTATIONAL EXACT

A stage-specific 8-bit Feistel permutation pair was assigned to each diamond.

At every depth through d=14, all 2^d route histories induced distinct exact permutations on the 256-element state space.

At d=14:
- histories: 16,384;
- distinct nonlinear path permutations: 16,384;
- route description: 14 bits;
- one evaluation by replay: 14 rounds.

Thus the failure is not peculiar to linear algebra. The route sequence itself is a succinct straight-line description of the induced nonlinear function.

## 10. S5 / Barrington-style control — COMPUTATIONAL EXACT + KNOWN THEOREM

Using stage-specific branch-selected permutations in S5:
- histories at d=14: 16,384;
- distinct composed S5 products: at most 120;
- the experiment saturated all 120 products by depth 10.

This mirrors the literature warning from Barrington: extremely expressive branch-dependent noncommutative computation can live in constant width.

## 11. What survives from the user's idea

The most promising object is not:
- number of paths;
- number of distinct hashes;
- number of path-induced functions;
- noncommutativity;
- recursive control by itself.

The promising object is a **single merge state's required counterfactual service burden**.

At a nominal merge node v, define the history fiber H(v).

Let a SAT-forced future service family Q act on those histories. Define

Sigma(h)=(Ans(h,q))_{q in Q}.

The representation problem is to support Sigma(h) for the actual h using one ordinary state/representation, while the proof must explain why Q is required by SAT rather than invented by the wrapper.

## 12. MERGE-SERVICE1 — revised candidate

For a merge node v and SAT-forced service family Q, define

C_merge(v)
=
min_{Rep,Eval}
{
  C_acquire(Rep)
  + C_retain/reacquire(Rep)
  + C_service(Eval,Rep,Q)
}

over every legal ordinary representation, including:
- direct history encoding;
- algebraic state;
- BDD/DAG;
- circuit/straight-line program;
- memoization;
- replay/recomputation;
- source reread;
- alternate coordinate systems.

Desired theorem:

C_merge(v_n)=n^{omega(1)}

for a SAT-forced family of merge states.

Status: OPEN.

## 13. Two independent missing arrows

### SAT-MERGE-FORCING1 — OPEN
Prove that SAT correctness itself forces a future service family Q rich enough that histories reaching the same semantic endpoint cannot simply be forgotten.

The wrapper may not manufacture Q merely to recover its own history.

### MERGE-SERVICE-LB1 — OPEN
Prove that no polynomial-size ordinary representation/evaluator can service the forced continuation obligations, including replay, algebraic compression, and representation changes.

Together these would turn reconvergence into a genuine hardness mechanism.

## 14. Relationship to SRAS

The reconvergent wrapper fits SRAS cleanly:

- nominal merge does not imply semantic/state merge;
- histories in the same continuation class may be QUOTIENTED;
- distinctions that future SAT service requires must be RETAINED/ENCODED or REACQUIRED;
- oracle-supplied continuation information is EXTERNAL;
- the cost theorem must charge all ordinary routes.

The new contribution is to make the merge points explicit locations where continuation quotienting occurs.

## 15. Recommended next experiments

1. Replace artificial branch bits with actual SAT-wrapper decision bits on restriction calls.
2. Build repeated diamonds that nominally reconverge after each decision.
3. Permit delayed re-separation only through SAT-native future restrictions, not history queries.
4. Compute the exact right-congruence quotient at each merge.
5. For every large quotient, search compact representations:
   - Gaussian/affine basis;
   - ANF/Fourier form;
   - OBDD/FBDD;
   - bounded-treewidth dynamic state;
   - circuit/straight-line program;
   - replay from source.
6. Test 3-SAT against 2-SAT, Horn, affine/Tseitin, bounded treewidth.
7. For recursive/cyclic variants, test pointer-jumping and repeated-squaring style shortcuts before treating long path length as cost.

## 16. Strict status

PROVED/EXACT:
- RIGHT-CONGRUENCE-MERGE1;
- DELAYED-RESEP-BITS1;
- PATH-PROGRAM-CLOSE1.

COMPUTATIONAL EXACT FINITE:
- parity delayed probes;
- affine-function control;
- nonlinear Feistel/Straight-Line-Program control;
- S5 product control.

KNOWN LITERATURE:
- residual/subfunction counting exactly characterizes fixed-order OBDD levels;
- communication methods yield strong restricted BP lower bounds;
- Barrington width-5 polynomial branching programs capture NC1;
- pebbling/time-space methods constrain forced DAG computations.

OPEN:
- SAT-MERGE-FORCING1;
- MERGE-SERVICE-LB1;
- unrestricted ordinary-source acquisition/service lower bound;
- nonrelativizing/nonalgebrizing bridge.

P versus NP remains OPEN.

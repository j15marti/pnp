# RCCN-1 — Routed Causal Computation Networks

**Timestamp:** 2026-10-01 11:42 PT  
**Status:** PROVED/EXACT model theorems + OPEN store/recompute strengthening.  
**Global status:** P versus NP remains OPEN.

## 1. Purpose

RCCN formalizes a computation that is routed among several deterministic machines or deterministic modules:

\[
M_{i_1}\to M_{i_2}\to M_{i_3}\to\cdots,
\]

where the next active machine can depend on the result of the current computation, and routing may revisit earlier machines.

The model is useful for delayed queries, cyclic handoffs, local-state retention, communication, and recomputation. It is **not** based on the false claim that an NDTM must explore all possible routes.

## 2. Formal model

Fix a finite family of deterministic modules

\[
\mathcal M=\{M_1,\ldots,M_m\}.
\]

At routed epoch \(t\), the global configuration is

\[
C_t=(i_t,\sigma_{1,t},\ldots,\sigma_{m,t},h_t),
\]

where:

- \(i_t\in[m]\) is the active module;
- \(\sigma_{j,t}\) is the persistent local state of module \(M_j\);
- \(h_t\) is explicitly charged shared/message state.

The active module computes for \(c_t\) charged primitive steps and emits an output \(y_t\). A deterministic router \(R\) chooses the next active module and updates shared state:

\[
(i_{t+1},h_{t+1})=R(i_t,y_t,h_t).
\]

Local state updates are part of the charged computation. Cycles such as

\[
M_1\to M_3\to M_1\to M_4
\]

are legal.

All message copying, state transport, and routing work must be charged in the declared machine model.

## 3. Theorem RCCN-1 — Flattening / single-DTM simulation

### Statement

For every fixed finite RCCN with deterministic modules and deterministic router, there exists a single deterministic Turing machine \(U_{\mathcal M,R}\) that produces exactly the same routed transcript and final output.

If the routed execution uses total local computation time

\[
T_{\rm local}=\sum_{t<z} c_t
\]

and total explicit routing/communication work \(T_{\rm route}\), then a standard multitape flattening has time

\[
O(T_{\rm local}+T_{\rm route})
\]

for a fixed number of modules/tapes, up to the chosen fixed-machine simulation convention. Under a different standard DTM encoding, the overhead is at worst the usual polynomial universal-simulation overhead.

Consequently, if the number of routed epochs is polynomial and every charged module invocation plus routing step is polynomial, the whole RCCN computation is polynomial-time.

### Proof

Construct one DTM whose finite control contains a tag for the currently active module and whose work tapes contain the persistent local tapes/states of all modules together with the shared routing state. When the active tag is \(i\), apply exactly the transition function of \(M_i\). When \(M_i\) reaches its declared handoff state, execute the fixed router transition, write/copy the explicitly charged message state, change the active tag, and continue.

Because the module family and router are fixed, their control descriptions can be hard-wired into the flattening machine. Thus every routed primitive step is simulated by a constant number of fixed-model multitape steps, plus whatever message-copy cost the routed model itself declares. For alternative standard DTM encodings, compose with the standard polynomial simulation. The simulated configuration is identical after every routed step, so the final result is identical.

**Status:** PROVED/EXACT.

## 4. Corollary RCCN-2 — Nondeterministic simulation guard

Because

\[
DTIME(t)\subseteq NTIME(t)
\]

up to the same standard model conventions, an NDTM can simply run the flattened deterministic RCCN computation without making nondeterministic choices.

Therefore:

\[
\boxed{\text{routing or cycling alone cannot force an NDTM to explore every possible route.}}
\]

Exponential latent routing possibilities are not an NEXP lower bound.

**Status:** PROVED/EXACT.

## 5. Delayed-return setup

Suppose that during one module invocation a \(K\)-bit record

\[
X\in\{0,1\}^K
\]

is generated. At a cut immediately after the handoff, the original record and its generating source become unavailable for direct rereading.

Across the entire routed network, let all persistent information depending on \(X\) be summarized by

\[
P(X)\in\{0,1\}^s.
\]

This includes **all** persistent local states of every module plus all persistent messages/shared storage. If there is a free side channel

\[
Z(X)
\]

taking at most \(2^r\) values, it is accounted separately.

Only after the cut, a selector

\[
j\in[K]
\]

is revealed. The routed network may then cycle among modules arbitrarily, but receives no additional information depending on \(X\). It must output \(X_j\) exactly.

## 6. Theorem RCCN-3 — Global delayed-return state lower bound

### Statement

Under the delayed-return setup, exact recovery for every \(X\in\{0,1\}^K\) and every \(j\in[K]\) implies

\[
\boxed{s\ge K-r.}
\]

More exactly,

\[
s\ge \log_2\max_z |Z^{-1}(z)|.
\]

### Proof

Fix a side-information value \(z\). Suppose two distinct records \(X,X'\in Z^{-1}(z)\) produce the same global persistent state:

\[
P(X)=P(X').
\]

Because \(X\ne X'\), choose a coordinate \(j\) with \(X_j\ne X'_j\). After the cut, give both executions the same delayed selector \(j\). Their complete persistent routed state and free side information are identical. Every subsequent routed transition is deterministic and receives no new \(X\)-dependent information, so the two executions have identical future trajectories and identical outputs. They therefore cannot output both \(X_j\) and \(X'_j\), contradiction.

Thus \(P\) is injective on every fiber \(Z^{-1}(z)\), giving

\[
2^s\ge \max_z |Z^{-1}(z)|.
\]

Since at most \(2^r\) fibers partition \(2^K\) records, some fiber has size at least \(2^{K-r}\). Hence \(s\ge K-r\).

**Status:** PROVED/EXACT in the declared no-reread/no-reacquisition model.

## 7. Corollary RCCN-4 — Distributed/cyclic state does not evade the bound

If module \(M_a\) retains \(s_a\) bits and persistent inter-module messages contain \(s_{\rm msg}\) bits, then

\[
s=\sum_a s_a+s_{\rm msg}
\]

may be used in RCCN-3.

Hence splitting information among many machines, or routing it around a cycle, does not reduce the **total** information that must survive the cut:

\[
\boxed{\sum_a s_a+s_{\rm msg}\ge K-r.}
\]

**Status:** PROVED/EXACT.

## 8. Theorem RCCN-5 — Cycles cannot recreate discarded information

### Statement

Under the hypotheses of RCCN-3, allow any finite number of deterministic handoffs and revisits after the cut before the delayed query is answered. If no post-cut source provides additional \(X\)-dependent information, the RCCN-3 lower bound is unchanged.

### Proof

The complete post-cut routed evolution is a deterministic function of

\[
(P(X),Z(X),j).
\]

If two records give the same triple, every later routed configuration is identical by induction on routed steps. Cycling changes where the state is processed but cannot increase the number of distinguishable pre-cut records represented by that state. The injectivity proof of RCCN-3 therefore applies unchanged.

**Status:** PROVED/EXACT.

## 9. Theorem RCCN-6 — Store-or-reacquire necessity

### Statement

If

\[
s<K-r,
\]

then no exact RCCN can answer every delayed coordinate query using only the retained state, free \(r\)-bit side information, routing, and deterministic post-cut computation.

Equivalently, every exact implementation with \(s<K-r\) must obtain additional information that depends on \(X\) after the cut.

### Proof

This is the contrapositive of RCCN-3. If no additional \(X\)-dependent information enters after the cut, exact recovery implies \(s\ge K-r\). Therefore an implementation below that storage threshold must reacquire \(X\)-dependent information from some source.

**Status:** PROVED/EXACT.

### Limitation

RCCN-6 proves that reacquisition is necessary, **not that reacquisition is expensive**. If the original record remains in a unit-cost random-access store, one post-cut read can answer a coordinate query. Therefore a P-vs-NP-strength route needs an independent lower bound on the cost of reacquisition/recomputation.

## 10. Routed causal SAT integration

A SAT/CCSPC-flavored routed epoch can be written as

\[
M_{i_t}:\quad
\Phi_t\longrightarrow T_t=\operatorname{CanSAT}(\Phi_t)\longrightarrow X_t,
\]

followed by a fresh causal challenge

\[
B_t\longrightarrow q_t,
\]

where \(q_t\) asks for a value associated with the just-completed record/dependency state \(X_t\). The routed response is

\[
Y_t=V_t(X_t,q_t),
\]

and the next active module and next SAT pointer are

\[
\boxed{
(i_{t+1},p_{t+1})
=F_t(i_t,p_t,T_t,B_t,Y_t).
}
\]

This permits both result-dependent routing and cycles.

RCCN-3 through RCCN-6 then provide an exact local theorem when the challenge family can recover arbitrary independent coordinates of a prior ephemeral record and no cheap reread is available.

## 11. OPEN strengthening — Routed Store/Recompute Theorem

The desired stronger theorem is

\[
\boxed{
S_{\rm persistent}
+C_{\rm communication}
+C_{\rm reread}
+C_{\rm recompute}
+C_{\rm sequential}
\ge L(D)
}
\]

for an explicit dependency family \(D\), with the bound holding for **every** correct implementation rather than for one chosen decomposition.

This is not proved by RCCN-3. It requires a model-matched lower bound showing that reacquisition of the delayed value is expensive.

Candidate tools include pebbling/time-space tradeoffs and branching-program lower bounds, but these remain restricted-model transfers unless a compiler from arbitrary static SAT computation is proved.

**Status:** OPEN / load-bearing candidate.

## 12. Hostile controls

Every RCCN hardness claim must survive:

1. **Flattening:** replace all routed modules by one DTM.
2. **NDTM simulation:** the NDTM may run the flattened DTM verbatim.
3. **Static reread:** one random-access probe may destroy a delayed-indexing storage claim.
4. **Memoization and pointer jumping.**
5. **Compact summaries / group compression.**
6. **Recomputation instead of storage.**
7. **Message compression:** count total information, not number of messages.
8. **Easy formula controls:** Horn, 2-SAT, bounded treewidth, affine/Tseitin.
9. **Semantic oracle:** current SAT answers supplied for free.
10. **Wrapper equivalence:** DEAD/COPY/DELAY/INTERP/RECOMP.
11. **Input-size normalization.**
12. **Relativization/algebrization audit.**

## 13. Literature relationship

Pebbling is an established abstraction for memory versus recomputation on dependency DAGs. Paul and Tarjan (1978) proved explicit time-space tradeoffs in a pebble game; modern surveys such as Nordstrom (2013) explain its use in computation and proof complexity. Beame, Jayram, and Saks (2001) proved nontrivial time-space lower bounds for branching programs and related RAM models.

These results support the STORE/RECOMPUTE interpretation but do not directly prove RCCN hardness for unrestricted SAT algorithms.

References:

- W. J. Paul and R. E. Tarjan, *Time-space trade-offs in a pebble game*, Acta Informatica 10(2):111–115, 1978, doi:10.1007/BF00289150.
- P. Beame, T. S. Jayram, M. Saks, *Time-Space Tradeoffs for Branching Programs*, JCSS 63(4):542–572, 2001, doi:10.1006/jcss.2001.1778.
- J. Nordstrom, *Pebble Games, Proof Complexity, and Time-Space Trade-offs*, LMCS 9(3):15, 2013, doi:10.2168/LMCS-9(3:15)2013.

## 14. Strict status summary

**PROVED/EXACT**

- deterministic routed networks flatten to one DTM;
- an NDTM can simulate the flattened DTM;
- global delayed-return state lower bound \(s\ge K-r\) in the no-reacquisition model;
- distributing state across modules or cycling does not evade that total-state bound;
- if retained state is below the threshold, additional \(X\)-dependent information must be reacquired.

**OPEN**

- any nontrivial lower bound on the cost of that reacquisition for arbitrary static SAT algorithms;
- a universal routed STORE/RECOMPUTE/SEQUENTIAL theorem;
- a static-SAT-to-RCCN/CRS-PPC compiler;
- a nonrelativizing/nonalgebrizing endgame.

## 15. Reusable short definition

> **RCCN:** A fixed finite network of deterministic modules with persistent local state and charged messages, where each module's result determines the next routed module and cycles are allowed. The network is computationally equivalent to one DTM. Its useful lower-bound feature is delayed return: if a future result-dependent challenge asks for previously generated information after that information has been discarded, then the total persistent network state must store enough information or the network must reacquire/recompute it.

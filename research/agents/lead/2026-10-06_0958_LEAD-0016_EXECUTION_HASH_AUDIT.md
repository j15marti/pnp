# LEAD-0016 — EXECUTION-HASH / 2^k-to-2^x AUDIT

**Timestamp:** 2026-10-06 09:58 PT  
**Agent:** LEAD  
**P vs NP status:** OPEN  
**Purpose:** Audit whether an execution-specific hash-chain provenance wrapper supplies the missing SAME_REALIZATION ingredient required by the project's existing `2^k/2^x` / continuation-reduction framework.

## Executive conclusion

The execution hash-chain is a valid **implementation-specific provenance instrument**, but it does **not** close the current `2^k/2^x` extraction/contraction gap.

The reason is exact and structural:

1. The current `2^k/2^x` core in `main2.tex` is expressed through solver-independent continuation equivalence and valid continuation reduction
   [
   K_{s\to t}=\log_2\frac{\kappa_U(S_s)}{\kappa_U(S_t)}.
   ]
   Neither `BRTHRESH1`, `CONTSEP1`, nor `NO2K1` requires an execution-specific provenance label.

2. SAME_REALIZATION enters later, in source/accounting/compiler attempts that try to transfer an arbitrary static SAT decider into an auxiliary model (CRS-PPC / RMV / reconstruction). There it prevents substitution by an unrelated realization, but does not itself establish contraction or cost.

3. For any deterministic polynomial-time decider `A`, any polynomial-overhead online hash of its actual trace is itself polynomial-time computable from `(A,F)` by simulating `A(F)`. Therefore the hash does not create an information object unavailable to an ordinary simulator with access to `A`'s code and input.

4. A bare SAT oracle answer does not determine the fingerprint. This is a genuine intensional/extensional separation, but it is weaker than the required nonrelativizing compiler theorem. Under oracle replacement, the oracle machine has its own execution realization and its own cheaply computable fingerprint; requiring the fingerprint of a fixed reference implementation becomes trace simulation, already covered by the project's reference-trace upper bound.

## Definitions

Let deterministic algorithm `A` on input `F` have trace
[
\operatorname{Tr}_A(F)=(s_0,e_1,s_1,\ldots,e_T,s_T).
]
Let `H` be any deterministic polynomial-time update map with `b(n)=poly(n)` output bits. Define
[
P_0=\mathrm{Seed}(A,F),\qquad
P_t=H(P_{t-1},e_t),\qquad
P_A(F)=P_T.
]
Historical feedback variants such as
[
P_t=H(P_{t-1},P_{j_t},e_t)
]
with polynomially maintainable index rule `j_t` are included.

## PROVED/EXACT — EXECUTION-HASH-CLOSE1

If deterministic `A` runs in time `T(n)=poly(n)` and the provenance update is polynomial-time with polynomial-size state, then `P_A(F)` is polynomial-time computable from `(A,F)` by universal simulation.

### Proof
Run the universal simulator for `A(F)`. As each transition/event is produced, apply the declared provenance update. There are `T(n)` events and polynomial work per update. Historical-feedback variants remain polynomial when the wrapper maintains only polynomially many polynomial-size states, because the wrapper is an observer and its storage/work is explicitly polynomial. Hence the final fingerprint is in FP relative to the ordinary description of `A` and `F`. QED.

This is a direct instance of the existing `TRACECLOSE1` / reference-trace simulation closure.

## PROVED/EXACT — SEMANTIC-NONDETERMINACY1

There is no function `g(F,b)` that equals `P_A(F)` for every deterministic exact SAT decider `A` using only `b=SAT(F)`, unless all such implementations happen to induce the same fingerprint.

### Witness
Take two correct implementations with the same SAT result but different internal event sequences. A path-sensitive hash chain gives different fingerprints except for an allowed collision. Therefore extensional SAT semantics do not determine implementation provenance.

This proves
[
(F,SAT(F))\not\Rightarrow P_A(F)
]
in general.

## Why SEMANTIC-NONDETERMINACY1 does not close relativization

A relativizing proof is not limited to recovering the fingerprint from the single SAT bit. Under oracle replacement the candidate machine becomes an oracle machine `M^O`; it has an ordinary finite description and an actual run on `F`. The provenance wrapper can simply hash that oracle-machine execution:
[
P_{M^O}(F).
]
Thus the same-realization requirement is satisfiable for the **replacement realization itself**.

If the proof instead insists on reproducing the fingerprint of a fixed reference algorithm `A`, then the task is reference-trace reproduction. The project's `Reference-Trace Simulation Upper Bound` already states that a universal machine with `A`'s description can reproduce the reference transcript with ordinary simulation overhead.

Therefore:
[
\boxed{\text{SAT oracle does not determine }P_A(F)}
]
is true, but
[
\boxed{\text{oracle replacement cannot satisfy SAME_REALIZATION}}
]
does not follow.

## Audit of the existing 2^k/2^x chain

### BRTHRESH1
If a **valid independently defined reduction** removes factor `2^x` from initial Boolean mass `2^n`, polynomial residual requires
[
x=n-O(\log n).
]
Execution provenance is not used here.

### CONTSEP1 / NO2K1
These count continuation-equivalence classes
[
\kappa_U(\mathcal H)=|\mathcal H/\!\equiv_U|.
]
A summary serving all legal continuations needs at least that many states. Again, no execution hash is required. Adding an implementation fingerprint generally refines histories more than continuation semantics and therefore risks counting distinctions irrelevant to the consumer.

### SRAS
SRAS explicitly permits provenance hashes as identity labels but states
[
\text{unique provenance}\not\Rightarrow\text{expensive acquisition}.
]
The execution hash fits naturally in coordinate `P` / history `H`, but does not establish the open acquisition curve lower bound
[
\mathcal C_{F,U,M}(n-O(\log n))=n^{\omega(1)}.
]

### CSE1
CSE1 still requires an arbitrary exact SAT decider to yield a source-bound recursively consumable object with actual source contraction and fully charged acquisition. Hashing its ordinary polynomial trace produces only a polynomial-size observer transcript/fingerprint and does not imply live-source shrinkage
[
|J_{\rm live}^U(Q_i)|\le N^{b+o(1)},\quad b<1.
]

### CRS-E / SAME_REALIZATION
Here SAME_REALIZATION is genuinely part of the target compiler. The hash-chain can provide a clean implementation of an execution-identity tag. It can therefore improve **formal typing** of CRS-E, but not prove CRS-E and not prove the resource lower bound.

## Hostile controls

### DEAD / COPY / DELAY
An execution fingerprint is expected to change under these wrappers. This is not a bug if it is used only as an implementation identity. It becomes a problem only if the proof charges the fingerprint difference as SAT-relevant reduction.

### 2-SAT / XOR / bounded treewidth
The same execution fingerprint can be attached to easy algorithms. Therefore fingerprint complexity is not SAT-specific and must never be used as a lower-bound quantity by itself.

### Oracle shadow
Give the oracle every semantic SAT answer. It still does not know a fixed ordinary algorithm's fingerprint from semantics alone. But it can:
- hash its own realization;
- simulate the fixed reference algorithm if its description is available; or
- be strengthened to a trace/provenance oracle.

No contradiction follows without a separate theorem that the **same fixed ordinary realization** is mandated by a solver-independent SAT obligation and cannot be replaced by another correct realization.

## Candidate refinement — REALIZATION-BIND1

The strongest potentially useful role for the hash chain is a narrow binding lemma:

> If a downstream compiler theorem already requires an object `Q` to be derived from the actual execution of `A(F)`, attach `P_A(F)` so that substitution by an unrelated execution is detectable (up to the declared collision model).

This is an identity/coupling device, not a contraction or cost theorem.

Status: **CANDIDATE utility lemma**, because the exact collision model and canonical event encoding must be fixed.

## What would make the provenance load-bearing?

A new theorem would need to say more than `P_A(F)` is not determined by `SAT(F)`. It would need an independently defined solver-independent obligation `R(F,Q)` such that:

1. every polynomial SAT decider `A` induces a SAME_REALIZATION `Q_A(F)` satisfying `R`;
2. `Q_A(F)` cannot be replaced by the corresponding object of a different correct implementation;
3. acquiring/using `Q_A(F)` lands in a model with an unconditional lower bound or yields genuine source contraction;
4. a maximal semantic oracle cannot provide a substitute satisfying `R` without introducing an explicitly disallowed EXTERNAL source.

No such theorem is currently proved.

## Status ledger

- Execution hash as deterministic realization fingerprint: **PROVED/EXACT mechanics**
- `EXECUTION-HASH-CLOSE1`: **PROVED/EXACT**
- Semantic SAT answer does not determine arbitrary implementation fingerprint: **PROVED/EXACT**
- Hash chain supplies a clean identity tag for SAME_REALIZATION: **CANDIDATE utility / straightforward once encoding fixed**
- Hash chain repairs `BRTHRESH1` / `CONTSEP1` / `NO2K1`: **NO — not required there**
- Hash chain proves CSE1: **NO / OPEN**
- Hash chain blocks general oracle replacement: **FALSIFIED as stated**
- SAT-native nonrelativizing compiler: **OPEN**
- Nonalgebrizing hinge: **OPEN**
- P vs NP: **OPEN**

## Next target

Do not optimize the fingerprint further. Formalize `REALIZATION-BIND1` only as a typed subroutine inside one concrete compiler (most naturally CRS-E or the current CSE source-transport interface), then identify the first downstream statement that actually fails if `P_A(F)` is replaced by `P_B(F)` for another correct implementation. If no such solver-independent statement exists, SAME_REALIZATION is bookkeeping rather than a load-bearing proof hinge.

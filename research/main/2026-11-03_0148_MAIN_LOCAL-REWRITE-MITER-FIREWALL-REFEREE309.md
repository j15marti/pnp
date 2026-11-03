# LOCAL-REWRITE-MITER-FIREWALL-REFEREE309

**PNP Independent Proof Red Team — November 3, 2026, 01:48 PST**

**Status.** **PROVED/RESTRICTED** output-equivalence compiler for explicitly certified local AND/XOR rewrite traces in unchanged `Rmix341`; **PROVED/EXACT** eleven finite strict-Resolution templates and four complete nonclone miter refutations; **FALSIFIED** automatic extension from structural clones to arbitrary semantic equivalence; **OPEN** superpolynomial worst-case minimum, B1, B2, B3, and P versus NP.

No task identity, title, enabled state, schedule, ownership, safeguard, calculus rule, or weight changed.

## Exact obstruction

LSPV-2 CLONE-MITER-RES355 proves a linear Resolution upper bound for two exactly corresponding circuit copies. Its own handoff correctly leaves different but semantically equivalent circuits outside the theorem. The obstruction is not proof search: a claimed short derivation must contain checkable logical evidence connecting the differently structured outputs. Treating “the circuits are equivalent” as a free axiom would be the forbidden one-step semantic jump.

This run asks the narrower falsifiable question: does a supplied sequence of fixed local commutativity/associativity rewrites, including every affected output-cone gate, compile into a legal polynomial `Rmix341` refutation of the contradictory-output miter?

## Fixed calculus and trace grammar

Use only the already fixed source-independent signed two-input `AND`/`XOR` `VARDEF` gates and strict binary `RES`. Each paid fresh gate definition costs one and authenticates its constant defining-clause slots. Original circuit Tseitin clauses are zero-cost authenticated sources. Every Resolution node costs one. The proof may share nodes and choose its best sequence freely; discovery of the rewrite trace is separate machine work.

Let circuits \(C_0,C_r\) have the same named primary inputs and one output each. Their miter source contains their authentic gate clauses and contradictory output units \(o_0\) and \(\neg o_r\). A legal rewrite trace has \(r\) steps. Each step applies AND/XOR commutativity or associativity and explicitly lists its affected output cone. Let \(a_i\) be the number of distinct ancestor gates rebuilt at step \(i\). Fanout and reconvergence are charged by this cone count, not hidden in syntactic depth.

## New theorem: paid local rewrites suffice

**Theorem.** Every authenticated trace above compiles uniformly to an `Rmix341` contradiction DAG with

$$
W_{Rmix341}(M(C_0,C_r))
\le 34r+24\sum_{i=1}^{r}a_i+2.
$$

The bound is polynomial in the explicitly encoded circuits and trace whenever \(r+\sum_i a_i\) is polynomial.

### Proof

Finite strict-Resolution certificates establish the following source-independent constants for both gate types:

- commutativity and associativity output equivalence require at most \(B=30\) RES nodes;
- replacing one equal input of an AND/XOR gate and deriving output equivalence requires at most \(C=10\) RES nodes;
- composing two Boolean equalities requires exactly two RES nodes.

For one local rewrite, at most two fresh right-side gates are required, costing at most two DEF nodes, and the local output equivalence costs at most \(B\) RES nodes. If an ancestor has one changed input, rebuild it with one fresh gate and apply one congruence certificate. If both inputs changed, use one intermediate rebuild and the final rebuild, apply congruence twice, then compose the two equalities. The worst charge per affected ancestor is therefore

$$
2+2C+2=24.
$$

After each rewrite, compose its output equality with the accumulated equality using at most two RES nodes. This gives \(B+2+2=34\) per rewrite plus the displayed context-cone cost. Finally, resolve the accumulated two output-equivalence clauses against \(o_0\) and \(\neg o_r\) in two RES nodes. Every intermediate gate is either an authenticated gate already present in an endpoint circuit source or a fresh paid `VARDEF`; no semantic equivalence oracle, correctness axiom, or instance advice appears. QED.

Signed gate inputs are covered by consistent literal substitution in the fixed templates. A trace changing an operator, introducing an unlisted algebraic identity, or omitting an affected reconvergent ancestor is rejected rather than silently generalized.

## Exact finite replay

The producer saturated ordinary binary Resolution and retained only target ancestry for:

- AND commutativity: 4 RES;
- AND associativity: 11 RES;
- AND one-input congruence: 6 RES;
- XOR commutativity: 6 RES;
- XOR associativity: 30 RES;
- XOR one-input congruence: 10 RES;
- equality transitivity: 2 RES;
- complete contradictory-output miters for commuted AND/XOR: 4/7 RES;
- complete contradictory-output miters for associated AND/XOR: 10/23 RES.

The eleven retained certificates contain 210 lines, including 113 genuine RES nodes. A separately authored Node.js checker reconstructs every legal source slot and independently checks every pivot, exact resolvent, target, constant \(B,C\), SAT control, and malformed classification. Raw SHA-256:

`6ff5186ea2e6b24c26b1962562031f20702c626fde4ae26a101bea2a8c8323e6`.

The associated circuits

$$
(a\circ b)\circ c
\quad\text{and}\quad
a\circ(b\circ c),\qquad \circ\in\{\wedge,\oplus\},
$$

are not input-fixing gate clones: their first internal supports are \(\{a,b\}\) and \(\{b,c\}\). Nevertheless, the checked certificates refute their contradictory-output miters. This is a genuine extension beyond exact cloning, but only because the rewrite evidence is explicit.

## Four falsifiers and dispositions

1. **Only exact gatewise clones admit the peer's proof-carrying shortcut. — FALSIFIED in restricted form.** Explicit AND/XOR associativity and commutativity traces also compile with the displayed polynomial bound.
2. **Semantic equivalence automatically supplies such a trace. — FALSIFIED as an inference.** The theorem quantifies over a supplied, checkable rewrite trace; finding or even possessing an arbitrary semantic equivalence statement is not a proof rule.
3. **Contradictory output units alone prove circuit equivalence. — FALSIFIED.** Replacing the right associated XOR subgate by AND yields a SAT miter; exhaustive enumeration found witnesses.
4. **Fanout/reconvergence is free because a rewrite has small syntactic depth. — FALSIFIED.** The bound charges every distinct affected ancestor gate via \(\sum_i a_i\), including two-input changes and equality composition.

## Both-label, malformed, and nonuniform controls

- The four certified equivalent commuted/associated miters are UNSAT by explicit strict-Resolution empty-clause DAGs.
- Same-label associated XOR outputs are SAT.
- The XOR-versus-AND contradictory-output neighbor is SAT; the producer records concrete witnesses and the independent checker reenacts enumeration.
- Valid SAT and valid UNSAT DIMACS strings parse.
- Bad header, wrong clause count, out-of-range variable, missing terminator, and nonnumeric literal are rejected.
- A semantic-equivalence axiom, after-answer constant, or instance-tailored advice record is rejected because it is neither an original source nor a fixed legal inference.

## B1/B2/B3 classification

This theorem proves none of the three bridges.

- **B1 remains OPEN:** no arbitrary total SAT decider trace is compiled into an `Rmix341` proof.
- **B2 remains OPEN:** no worst-case runtime-to-proof-cost upper domination is obtained.
- **B3 remains OPEN:** assuming SAT in P does not provide polynomial rewrite traces for every UNSAT CNF or polynomially bounded proofs in this same calculus.

The result only retires clone-like and locally rewritten circuit miters as candidate hard families. A fast or short-proof circuit family does not bound \(\overline W_R(N)\). P versus NP remains OPEN.

## Work and all-phase space ledger

The logical theorem charges every DEF and RES node but intentionally omits optimal trace discovery from \(W_R\). An implementable compiler must parse both circuits and the trace, validate gate freshness and signatures, topologically check every affected cone, construct clauses, index dependencies, emit the proof, and validate the final ancestry. Those phases are separate from the logical minimum.

The finite Python producer charged closure discovery, SAT enumeration, malformed parsing, certificate extraction, JSON output, and process overhead: 14.505 seconds wall time and 10,664 KiB peak RSS. The independent Node verifier ran separately. These are host upper measurements, not native machine lower bounds. Materializing all clauses uses polynomial space; streaming and recomputation trade time for space. Any recursive machine statement retains

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
$$

with \(\rho\) covering every local phase, including trace validation and cone rebuilding.

## Literature and project audit

Fresh searches included `circuit equivalence checking resolution proof generation local rewrite miter`, `extended resolution circuit equivalence proof BDD SAT miter`, GitHub circuit-equivalence proof logging, and `github.com/openai` circuit-equivalence/SAT proofs.

- Chatterjee, Mishchenko, Brayton, and Kuehlmann, *On Resolution Proofs for Combinational Equivalence*, DAC 2007, explicitly discusses proof generation through structural hashing, intermediate equivalences, and rewriting: <https://doi.org/10.1145/1278480.1278631>.
- Bryant and Heule, *Generating Extended Resolution Proofs with a BDD-Based SAT Solver*, TACAS 2021, separates solver computation from checkable ER evidence: <https://doi.org/10.1007/978-3-030-72016-2_5>.
- Sinz and Biere, *Extended Resolution Proofs for Conjoining BDDs*, CSR 2006, is earlier proof-carrying symbolic-SAT context: <https://fmv.jku.at/ebddres/>.
- Yosys/EQY documents practical miter construction and equivalence workflows but is not treated as this proof calculus: <https://yosyshq.readthedocs.io/projects/yosys/en/latest/cmd/index_passes_equiv.html>.

Project reads included the verified 12:04 handoff, issue #3, LSPV-2 CLONE-MITER-RES355, LSPV-1 ER2-SOURCE-PADDING-TYPE-FIREWALL358, LSPV-3 FULL-LIFTED-K4 certificate358, LSPV-4 source/index reports, REFEREE299, and REFEREE308. The authenticated `github.com/openai` search found no reusable fixed-calculus circuit-equivalence checker. No novelty is claimed for proof-carrying circuit rewriting generally; the project contribution is the explicit bound and exact templates in the preselected `Rmix341` grammar.

## Exact next gap

Do not promote structural or locally rewritten equivalence to arbitrary semantic equivalence. A surviving circuit candidate must force every legal proof to escape all polynomially sized checked rewrite traces, ER2/BDD certificates, algebraic shortcuts, and compact auxiliary definitions. In parallel, B3 still requires the independent same-calculus implication

$$
\mathrm{SAT}\in P\Longrightarrow \overline W_{Rmix341}(N)\le\mathrm{poly}(N).
$$

No such implication is proved here. **P versus NP remains OPEN.**

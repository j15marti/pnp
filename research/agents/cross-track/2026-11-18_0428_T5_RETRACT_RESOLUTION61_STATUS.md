# CROSS-TRACK 61 | Two-coordinate T5 retract and Resolution firewall
**November 18, 2026, 04:28 PST. P versus NP remains OPEN.** Exact restricted mathematical results, executed finite audit, independent external mathematical review OPEN.

## Pre-search proposals, frozen before retrieval
Original local file `presearch_2026-11-18_0418.md`, SHA256 `25e22e5d03dfb8523bd77930b2e43df6f63b3228720e50a223c66028b390cf84`.
1. Charge full source/generation/workspace/recursion and try reducing balanced 25-state T5 CSP to five states before any compulsory resource claim.
2. Require an actual encoding-specific proof transport, not arbitrary polynomial decider -> Resolution.
3. Put same-input UWI against a hypothetical polynomial decider-to-witness program and one common clock.
4. Test any claimed WRAPPER operation against graph source recognition, orbit/adhesion contraction and replay.

## Retrieved newest substantive specialist outputs and targeted context
Resource: [TMR-1/088, exact authenticated long-subdivision path counting/relative approximation (04:04 PST)](https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_0404_TMR1_T5_LONGPATH_SPECTRAL_APPROX088.md); [TMR-3/082, cycle-rank residue DP and orbit-factor tables (03:25 PST)](https://github.com/j15marti/pnp/pull/270). Both are scoped upper algorithms, not universal contractions.

Nonrelativizing Simulation: [LSPV-5/CONGRUENCE_KRYLOV1 (04:06 PST)](https://github.com/j15marti/pnp/blob/main/research/main/2026-11-18_0406_MAIN_LSPV5_CONGRUENCE_KRYLOV1_CONDENSED.tex), coNP-complete supplied nonlinear congruence check but polynomial explicit affine endpoint certificates; [CLOCKZEROGAUGE34 (03:30 PST)](https://github.com/j15marti/pnp/blob/main/research/agents/clock-gate/2026-11-18_0330_CLOCKZEROGAUGE34.md), restricted reversible-baseline representatives. Neither establishes a logically necessary nonrelativizing hinge.

Universal Obstruction: [TMR-2/081 (03:12 PST)](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_0312_TMR2_T5_GAUGE_KERNEL081.md), source-authenticated 33-vertex critical T5 NO/YES pair, degree-two suppression and gauge-pinned width-4 exact decision/counting; 22,280 tuple visits versus 94,405 predecessor. No all-algorithm lower bound.

Proof Transport: [TMR-4/086 (Nov 18, draft PR #271)](https://github.com/j15marti/pnp/pull/271), exact signed-cycle count and low-cycle-rank OBDD upper algorithm; historical [ASSUME-RUP-TREE1](https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-10-16_1845_PROOF-TRANSPORT_ASSUME_RUP_TREE1.md) is proof-logging scoped, not arbitrary decider transport.

Read current project two-coordinate experiment, GitHub newest commits and issue #3 latest comments, project Library search, historical Google Drive CROSS-TRACK KRYLOVGUARD41, and primary literature (Bang-Jensen/Hell/MacGillivray 1988 DOI 10.1137/0401029; Hell/Nešetřil 1990 DOI 10.1016/0095-8956(90)90132-J; Ben-Sasson/Wigderson 2001 DOI 10.1145/375827.375835). Drive results were older, not evidence of exhaustive absence.

## Theorem: B/D relational retraction, one-way canonical Resolution transport
Let `R(a,b)` iff `(b-a)%5 in {1,3}`. On 25 states `x=(a,alpha)`, let
`D(x,y):=(a!=b)&(alpha!=beta)&(R(a,b) XOR R(alpha,beta))`,
`B(x,y,z):=D(x,y)&D(x,z)&(R(a,b) XOR R(a,c))`.
On five letters let
`T(a,b,c):=(R(a,b)&R(c,a)) OR (R(b,a)&R(a,c))`.
Define `p(a,alpha)=a`, `s(a)=(a,-a mod 5)`.
Pointwise: `B(x,y,z)=>T(p(x),p(y),p(z))`, `D(x,y)=>p(x)!=p(y)`, while `B(s(a),s(b),s(c))=T(a,b,c)` and `D(s(a),s(b))=[a!=b]`. Thus EVERY mixed B/D instance is satisfiable iff the five-letter T/inequality projection is, by a uniform global anti-diagonal lift. Exact solution counts are NOT preserved.

For the **direct exactly-one one-hot CNF** of B/D and its five-state projection, set all `X_{v,(a,alpha)}=0` when `alpha!=-a`, and rename `X_{v,(a,-a)}` to `Y_{v,a}`. Every one-hot and forbidden-tuple clause restricts *exactly* to the analogous five-letter clause (delete satisfied clauses, normalize duplicates). Therefore `CNF_25(I)|rho=CNF_5(pI)`.

Standard Resolution restriction closure produces a refutation of the five-state formula from ANY Resolution refutation of the unsatisfiable 25-state formula, with no greater width or derived-line count. In the declared encodings,
`ResSize(CNF_25(I)) >= ResSize(CNF_5(pI))`
and likewise for minimum refutation width. This is a genuine **one-way, encoding-specific proof-system lower-bound transport**; it is not arbitrary SAT-decider-to-Resolution or a computational separation. Source parse and projected constraint generation take O(n+m) fixed-domain operations / O((n+m)log(n+2)) encoded bit work, witness lift O(n) fixed-domain operations, and proof restriction charges reading/writing the entire proof and relevant clause data. The 25-state CNF may have up to 25^3 forbidden tuple patterns per B constraint; no free space or access model assumed.

## Hostile tests and falsifications
- **Counting mismatch:** on four variables, one B triple: #5-state solutions 200 vs #25-state solutions 20,000 (ratio 100); shared-center two B triples: 80 vs 3,200 (ratio 40). No constant count-transport factor and no 25^n necessary decision search.
- **Weak-XOR W is not in the common letter retract without separate proof:** `W((0,0),(0,1))=1` with equal letters. Pure W has different quotient `h(a,alpha)=alpha-a`; the B/D theorem does NOT automatically cover mixed B/W.
- **Concordant Q breaks the anti-diagonal section:** if `Q(x,y)=R(letter(x),letter(y)) & R(color(x),color(y))`, then `B(x0,x1,x2)&Q(x0,x1)` is 25-state UNSAT, while naive projected `T(a0,a1,a2)&R(a0,a1)` has witness (0,1,2). It is an immediate local contradiction, not a hard family.
- **Actual Resolution control:** a one-variable 25-color forbidden-unary CNF has a checked 25-inference refutation; the restricted five-color proof uses five. This does not convert arbitrary decider traces.

**Executed finite audit:** Python3 stdlib `t5_retract_res61_audit.py` SHA256 `6a68953775c919ed8bf01b4db6594df0df9756dc065fd580bfa86bc5f7abbe32`, zero failed assertions. Exhaustive 15,625 25-state triples and 625 ordered pairs; 125 five-state section triples; *entire* CNF restriction set equality on five test instances, including 60,854-clause 25-state CNF -> 394-clause five-state CNF; six mixed B/D 3-variable cases; explicit Q counterexample and a verified 25-to-5 step Resolution certificate. Result JSON SHA256 `cc91e345ef3542624595510f7fa41f31bc93d1d540f69a068e8203de96c87122`. Symbolic general theorem is independent of these finite checks.

## Proof DAG
**ESTABLISHED:** graph 5-coloring NP-complete; fixed T5 H-coloring NP-complete; standard Resolution closure under restrictions.
**PROVED RESTRICTED:** B/D 25->5 relational retract and converse lift; explicit CNF syntactic restriction; one-way five-to-25 Resolution lower-bound transfer.
**FALSIFIED:** intrinsic 25-state mandatory exponential search; uniform #solution multiplier; W has the same letter projection; arbitrary cross-attribute additions preserve section.
**CONDITIONAL:** independently proved five-state balanced Resolution hard family would transfer to canonical 25-state B/D; polynomial balanced decider would support fully charged polynomial witness recovery by appropriate reduction.
**OPEN:** full-cost all-input contractor, nonrelativizing WRAPPER hinge, same-final-input common-clock UWI forall eligible programs, arbitrary-decider-to-proof-system transport, representation-independent T5 superpolynomial deterministic lower bound, **P versus NP**.

## Next four specialists
**Resource Contraction:** normalize B/D to five states before measuring any width; count all parsing, schedule search, generation, exact arithmetic, recursion, live storage, witness output; test stronger mixed B/W or B/Q only after proving a valid quotient.
**Nonrelativizing Simulation:** construct a source-defined cross-attribute coupling breaking all cheap global sections **without** producing constant local contradictions; hostile-check WRAPPER against source recognition, affine/orbit shortcuts and matched oracle.
**Universal Obstruction:** one identical SAT instance, one common clock; challenger includes a hypothetical uniform polynomial decider, reduction/self-reduction, explicit 5->25 witness lift and source-derived queries; quantify correctly.
**Proof Transport:** implement proof-file Resolution restriction converter and certify each line; seek a truly hard five-state balanced family; retain a strict firewall against arbitrary-decider lower-bound inference.

**Highest-value missing arrow:** unrestricted, model-wide lower bound after full source-aware preprocessing and alternative algorithms. **P versus NP remains OPEN.** No peer files, root proof tracker or agent schedules modified.

# CROSS-TRACK SYNTHESIS 68 | FIXED-GADGET RESOLUTION UPPER TRANSPORT
**Timestamp:** 2026-11-18 11:19 PST, America/Los_Angeles.
**Status:** PROVED scoped constructive upper transport; checked finite proof certificate; P versus NP OPEN. External peer review and physical Turing-machine replay OPEN.

## Proposals frozen before current source searches
(1) Fully paid source-aware contraction of repeated fixed gadgets; (2) same-input, common-clock UWI decision-to-witness firewall; (3) forward/reverse proof-system transport and explicit Resolution checker; (4) a necessary, genuinely nonrelativizing WRAPPER hinge. Strongest surviving target: (3).

## Newest substantive four-track evidence actually read
- RESOURCE CONTRACTION: TMR-1/095 (11:00 PST, research branch tmr1-20261115-independent-lean060), a zero-auxiliary T5-to-strict3CNF compiler: 3n Boolean bits, 3n+5m triple-distinct-literal clauses; local 8-word vertex and 25-pair arc truth tables independently checked this run. TMR-3/089 (10:24 PST, draft PR #293): exact bipartite T5 counting O(poly(N)5^tau) with tau the min missing-cross-edge cover and all access, arithmetic, and live-space costs charged.
- NONRELATIVIZING SIMULATION: LSPV-5 XORORBIT1 (10:06 PST, main): source-certified restricted affine small-XOR-orbit exact endpoint certificate, no universal WRAPPER necessity.
- UNIVERSAL OBSTRUCTION: TMR-2/089 (10:12 PST, main): exactly ten binary shifted-projection polymorphisms, no majority/Maltsev; no unrestricted time lower bound. TMR-2/088 supplies fixed 65-vertex/87-arc girth-eight edge gadget with exact transfer 142884 R, recognizably contractible.
- PROOF TRANSPORT: TMR-4/092 (draft PR #294): all-order five-way assignment OBDD width >= 2^floor(b(H)/(4 Delta^2)) for bounded-degree forward bipartite sources, while SAT and a witness remain linear-time (set all senders 0, receivers 1). This refutes the inference from exact assignment-representation hardness to mandatory SAT decision work.

Project GitHub issue #3 and current branch reports were read; Library/project files and previous cross-track chats were checked. Google Drive searches for T5 and proof transport showed older September matching material but no newer source. Primary sources: Bang-Jensen, Hell, MacGillivray 1988 DOI 10.1137/0401029; Baker-Gill-Solovay 1975 DOI 10.1137/0204037; Kun DOI 10.1007/s00493-013-2405-4.

## Constructive theorem 68.1 (upper transport, NOT a lower bound)
Let R(a,b) iff (b-a) mod 5 is 1 or 3. Encode a T5 source graph G by canonical five-way one-hot CNF F_G, with 15 forbidden-pair clauses per arc. Fix a finite two-terminal T5 gadget J with t private vertices and existential endpoint relation exactly R. Replace each original arc with an independent copy J to obtain C_J(G). For every Resolution-with-weakening refutation pi of F_G having S inferences and maximum width w, there is an effectively constructible refutation Pi of F_{C_J(G)} with
```
 inference_count(Pi) <= S + C_J*m
 width(Pi) <= max(w,W_J)
```
where C_J and W_J are constants for fixed J, and generation time/space/output is polynomial in the encoded source plus pi.

Proof: for any forbidden endpoint pair (u=a,v=b), enumerate each of the fixed 5^t assignments to J's private vertices. Since (a,b) has no extension, each violates a genuine arc axiom. Weaken that axiom to a clause containing both forbidden terminal literals and the negative literal of the assigned color of each private vertex. For each private variable, resolve the five alternatives against its at-least-one clause to eliminate it. Obtain the exact source pair clause. Derive the 15 forbidden clauses for each source arc, append pi unchanged. This is a proof-system specific *forward upper* transfer only. It does NOT imply reverse size lower bounds or any all-algorithm SAT time lower bound. An application to fixed 65-vertex J follows if its exact cofactor certificate is accepted, without constructing the enormous 65-vertex certificate.

## Explicit nine-arc gadget and executed hostile audit
The private-path orientation words (minus means edge backwards along the path) are `--`, `---`, `---+` with integer transfer vectors
```
 --    [0,2,0,1,1]
 ---   [3,1,1,3,0]
 ---+  [1,6,1,4,4]
 product [0,12,0,12,0] = 12R
```
Ten of the 15 forbidden endpoint color pairs are excluded using the length-two path, five using the length-three path. Deriving all 15 arc constraints needs exactly 375 additional Resolution+weakening inferences and width <=7 per original arc:
```
 ResWeakSize(F_C9(G)) <= ResWeakSize(F_G)+375*m
 ResWeakWidth(F_C9(G)) <= max(ResWeakWidth(F_G),7)
```
An independently generated canonical CNF for the opposing-two-arcs UNSAT source has 47 distinct axioms and a 30-resolution-step refutation. After compiling both arcs, the 14-vertex/18-arc instance has 424 distinct canonical axioms. A completed 1,199-record proof has 424 input axioms, 350 weakening inferences, 425 binary resolutions, derives the empty clause, and never exceeds width 7. Two different Python source/checker implementations verify each axiom and inference, zero failed checks. The checker independently regenerates original edge/one-hot axioms. JSONL certificate SHA256:
`90557e7fcb929a0f2d66979eec914b5e19abda62435b9606b445cd0ded1d9bcf`.
This is a finite exact proof/certificate, not a complexity lower bound. Plain Resolution without weakening requires a separate step-count normalization.

## Proof DAG
| Implication | Status |
|---|---|
| Fixed T5 CSP NP-complete | ESTABLISHED literature |
| TMR-1/095 T5 -> strict3CNF exact compiler | DIRECT LOCAL TABLE RECHECKED, general follows from local composition |
| Nine-arc gadget cofactor 12R | PROVED, enumerated |
| Canonical T5 one-hot Resolution+weakening forward upper transport | **CLOSED**, constructive, complete checked certificate |
| Same theorem for fixed C65 | CONDITIONAL on independently audited /088 exact cofactor |
| Reverse transport of hard Resolution from source to compiled | OPEN |
| Hard assignment OBDD -> hard unrestricted SAT decision | FALSIFIED as an inference by easy-source controls |
| Polytime bipartite-girth8 decider -> original T5 witness in FP | PROVED CONDITIONAL in Synthesis 67 |
| Same-input/common-clock UWI against every polynomial competitor | OPEN |
| Mandatory nonrelativizing WRAPPER hinge | OPEN |
| Fully charged, all-algorithm resource contraction lower bound | OPEN |
| Unrestricted T5 superpolynomial time lower bound; P != NP | **OPEN** |

## Specialist assignments
1. Resource Contraction (TMR-1/TMR-3): compose /095 3-bit compiler with the source-aware 9-arc proof translator; authenticate and charge parse, source/target bit lengths, gadget recognition/contraction, inference output, all arithmetic, workspace and recursion. Test direct contraction before high-cost Fourier work.
2. Nonrelativizing Simulation (LSPV-5): isolate an operation genuinely not reproducible by relativizing polynomial reductions or direct source-aware proof compilation, with matched-oracle countermodel, before using WRAPPER. Guard XORORBIT1 against hidden reads and alternate compact evaluators.
3. Universal Obstruction (TMR-2): use the explicit small-width compiled UNSAT refutation as adversarial negative control. Seek growing noncompiled mixed YES/NO families; require same original final input and same clock for all admissible witness competitors, including derived-query decider self-reduction.
4. Proof Transport (TMR-4): independently replay checked 1,199-step proof, investigate an actual reverse proof-size transfer or counterexample, and differentiate weakening, one-hot clauses, bit code validity and adaptive diagrams. Never infer arbitrary-algorithm work from OBDD alone.

## Provenance
Full local scientific report SHA256 `6bf290c80e2b4f865c90790f9f6bbad12418ed68778eff0df6da50ebc6119c81`; local reproducibility archive contains pre-search proposal record, full report, two executable independent Python verifiers, complete 1,199-record proof, exact raw results and SHA256 manifest. No specialist schedule, root proof1/proof2 tracker or peer manuscript was edited.

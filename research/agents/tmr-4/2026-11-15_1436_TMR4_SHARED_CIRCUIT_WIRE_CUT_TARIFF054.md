# TMR-4/054: Shared-circuit crossing-bit tariff, exact rectangle transfer, and DISJ counterexample

**2026-11-15 14:36 PST | TMR-4 / PNP Cost-Sound Abstraction | Tracks A/C.**  
**Status:** PROVED/EXACT restricted structural theorem, independent mathematics review OPEN; COMPUTATIONAL finite audit. Unrestricted SAT decision and circuit-size transfer OPEN. P versus NP OPEN.

## Candidate, model and falsifiers

**CWCP054.** Let C be a deterministic acyclic shared Boolean circuit, with n named input nodes, g distinct internal fan-in-at-most-two Boolean gates, w directed operand-wire occurrences and a single output. Fix a partition of input bits X:Y. Assign every internal gate to either bank X or bank Y; an input node belongs to its own bank. For this fixed graph placement a, let E_a be the distinct producer nodes u with at least one outgoing wire to an opposite-bank consumer; e=|E_a|. Sharing is retained; one value sent to the opposite bank may be locally cached and reused by any number of consumers.

**Claim:** Over EVERY field K, rank_K(M_X:Y(f_C)) <= #accepting fixed-schedule crossing-bit transcripts <= 2^e. The matrix is the assignment-evaluation function of ONE supplied circuit, NOT the SAT decision language on encoded formulas.

Four falsifiers, fixed before testing: (F1) DISJ_k has full cut rank 2^k but a 2k-1 gate circuit; (F2) fanout of one bit across multiple wires cannot incur multiple independent transmissions; (F3) Horn, affine/Gaussian, equality, unique witness, products and padding may have genuine small representations; (F4) zero-priced combinational wires and adaptive gate strategies invalidate an unjustified transfer from message bits to arbitrary machine steps or circuit gates.

## Theorem and complete proof

Order all nodes topologically. For each crossing producer input, send its Boolean value to the opposite bank once, at the start in public order. For each subsequent internal gate in topological order, the owner computes the gate from its locally owned predecessors and already received opposite-bank predecessor values, then sends its one output bit if the node belongs to E_a. One incoming value may be cached and fanned out arbitrarily inside the receiving bank. All e messages occur in a public deterministic order; the output owner evaluates the final output.

For any full transcript t, the set of original input pairs producing t is a combinatorial rectangle A_t x B_t: inductively each next X message is a function solely of the previous transcript and x, and each next Y message solely of the previous transcript and y. Fixing each message therefore intersects only the corresponding side of the rectangle. Finally the accepting output owner tests its own input and t, narrowing only its own coordinate. Thus the accepting pairs associated with t form a rectangle R_t.

The accepting rectangles partition all 1-entries of the 0/1 assignment matrix. The rectangle indicator of R_t is a rank-at-most-one outer product over every field, so M=sum_t 1_R_t and

    rank_K(M) <= #accepting transcripts <= #all transcripts <= 2^e.

Hence every placement satisfies e >= ceil(log2 rank_K(M)) when rank is positive. This is a structural communication-interface result, not a circuit-gate lower bound. Repeated wire values are explicitly shared rather than duplicated.

**Exact restricted tariff:** In the QUALIFIED two-bank communication calculus, SEND of a previously unsent crossing producer has cost 1; LOCAL-EVAL, CACHE and local FANOUT have cost zero. If j distinct crossing-producer values have been delivered, p=e-j is a nonnegative integer potential; lambda=1 gives p(C)-p(C') <= cost(r) on every transition, zero on local operations, one on SEND; p(goal)=0. Zero-cost SCCs cannot reduce p. If one *physically* charges each crossing directed wire one, the structural inequality remains cost-sound because e<=w_cross. However arbitrary combinational circuits often charge wires zero in gate complexity; requiring SEND at positive machine cost is NOT a sound simulation of that unrestricted model. No claim that arbitrary SAT solvers must generate all these messages.

**Universal cheap placement guard:** Let usedX and usedY count inputs occurring syntactically as a gate predecessor. Assign all gates to Y to send at most usedX distinct input bits, or assign all gates to X to send at most usedY. Therefore min_a e <= min(usedX,usedY) <= min(|X|,|Y|). Optimizing a may itself require expensive discovery. This upper guard prevents deriving unrestricted superlinear circuit gate size from this static interface invariant.

## Genuine shortcut and finite verification

For DISJ_k(x,y)=AND_i NOT(x_i AND y_i), the k-fold tensor of [[1,1],[1,0]] has rank 2^k over EVERY field. An explicit k-NAND plus (k-1)-AND circuit has only 2k-1 shared binary gates, 4k-2 directed operand wires, and by assigning all gates to Y, e=k. The bound is exactly saturated. This is a legal compact circuit, NOT a hard SAT decision instance.

The finite native Node.js v22.16.0 audit enumerated all gate-owner placements on 17 exactly specified Boolean circuits, with actual source-node caching, exact finite-field ranks F2 and F101, explicit message transcripts, full and accepting rectangle checks. Every check passed: **478 owner placements, 15,217 rectangle assertions, zero failures.** Revision tmr4-circuit-wire-cut054.v1, seed NONE. Finite tests are COMPUTATIONAL; the symbolic rectangle proof is the restricted theorem.

| Control | k | gates | rank F2 | rank F101 | minimum e |
| --- | ---: | ---: | ---: | ---: | ---: |
| DISJ | 4 | 7 | 16 | 16 | 4 |
| Equality | 3 | 5 | 8 | 8 | 3 |
| Inner-product parity | 3 | 5 | 3 | 7 | 3 |
| Horn 2CNF chain | 2 | 5 | 3 | 3 | 2 |
| Affine XOR | 3 | 5 | 2 | 2 | 1 |
| Unique singleton | 2 | 7 | 1 | 1 | 1 |
| Independent product | 2 | 3 | 1 | 1 | 1 |
| Shared x0 fanout | 2 | 3 | 1 | 1 | 1 |
| Padded DISJ | 3 | 3 | 4 | 4 | 2 |

Sharing falsifier: in (x0 AND y0) OR (x0 AND y1) with Y-owned gates, two source-to-destination crossing wires correspond to ONE crossing producer, e=1 rather than two. AFFINE uses three/five XOR gates; despite many assignments its rank is two. The singleton has rank one across every cut. DISJ is a 2CNF, and all-zero is its satisfying witness, so no semantically necessary SAT search follows from high rank.

**Reproduce:** node experiments/tmr/tmr4_circuit_wire_cut054.js . No external dependencies. Executable source: experiments/tmr/tmr4_circuit_wire_cut054.js . Raw complete per-case data: results/raw/tmr/2026-11-15_1436_TMR4_WIRECUT054_NODE_RAW.json . Enumerating all 2^g placements is an external exponential audit, never a fast input-dependent compiler.

## Same-realization ledger and Track C firewall

| Stage | Paid resources | Scope / peak retained state |
| --- | --- | --- |
| Given circuit C | n inputs, g gates, w directed operand wires; encoded length O((n+g+w)log(n+g)) for fixed bounded basis | Graph creation and layout discovery NOT free |
| One topological circuit evaluation | O(n+g+w) standard RAM operations; word-to-bit machine adds address/index overhead | O(n+g) cached signal bits plus addresses; original sharing retained |
| Two-bank protocol | Exactly e one-bit crossing-producer sends, at most w_cross <= w operand occurrences | O(n+g) cached bits across banks; local computation NOT charged to communication |
| Exhaustive placement/rank audit | 2^g layouts; 2^n assignment rows and exact rank elimination over fixed fields | Exponential and not an online solver |
| Circuit-to-CNF (TMR-1/053) | Functional unique-extension CNF V=n+g, m<=5V for width<=3; O((n+g)log(n+g)) encoded bits including wire labels | Original n-input #Circuit-SAT time savings do not follow automatically from 2^o(V) #3SAT if g can be n^4 |

No P1-01/P1-03/P1-04 all-input decider; no P2-A2 uniform transformation or P2-B1/B2/B3 same-proof-system SAT implication. No native one-machine DTISP contradiction. TMR-1/053's pinned October-2026 counting theorem and quantitative E^NP witness implication remain separate, source-conditional claims. The graph-cut theorem supplies no new #SAT time exponent or NP-level separation.

## Mandatory four gates

| Gate | Status | Reason |
| --- | --- | --- |
| DISJ sanity | **PASS restricted; FAIL for rank-to-general-gate-size transfer** | Rank 2^k with 2k-1 gates and e=k |
| Relativization | **PASS restricted; OPEN unrestricted** | Communication rectangles are a valid relativizing intermediate theorem, but no exact nonrelativizing NP separator; algebrization/Natural Proofs audits still open |
| Simultaneous DTISP | **NOT APPLICABLE to this graph-representation theorem; OPEN for machine transfer** | One graph/protocol is charged, but no matched uniform SAT machine satisfies any strict joint time-space forbidden region |
| Configuration counting | **PASS upper-bound guard only** | For a fixed total deterministic read-only-input machine, T<=2^{O(s+log N)}, or T<=2^{O(s)} when s>=log N; not a work lower bound, not automatically randomized/quantum |

/341 remains FAIL as a full logical UNSAT authority; /386 remains RESTRICTED.

## Corpus, sources, integrity and one next lemma

Governing SAT compression directive read FIRST, SHA 7b8804dc7587abc5134055b5b0d16a143055ca5a. Inspected AGENTS.md, CODEX.md, research skill, current TMR-1..5 handoffs, issue #3, original TMR-4/053 adaptive BP report and TMR-1/053 circuit-CNF normalizer. Recovered complete proof1.txt SHA 06f7ebc8, proof2.txt SHA 930c5eed (1,051,196 characters), main.tex SHA 6ac34c5d (2,545,859 characters); oversized latter two recovered through Git blob by SHA after file-range endpoint returned empty. Examined relevant tracker OPEN nodes and main TMR-4 region. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root, tracker, peer file, agent identity or schedule edited. Local git clone failed DNS, hence full repository preflight, full test suite and Lean builds were not executed.

Related prior result: TMR-4/053's adaptive branching-program switch-node rectangle theorem. NEW here is a DIRECT shared-CIRCUIT fixed-topology two-bank wire-interface transfer with distinct producer fanout charged once, plus the explicit tariff/machine-cost nontransfer. Prior Boolean BP switching results are not relabeled as new. Sources: Borodin, Razborov & Smolensky (1993), https://www.cs.toronto.edu/~bor/Papers/lower-bounds-read-k-times-branching.pdf ; Beame, Jayram & Saks (2001), https://doi.org/10.1006/jcss.2001.1778 ; Williams ACC circuit hierarchy method, https://people.csail.mit.edu/rrw/acc-lbs-journal-final.pdf . Independent mathematical peer review OPEN.

**ONE NEXT LEMMA:** Formalize a fully physical adaptive shared-circuit evaluation machine with actual charged head/address/work states and show a TRUE lower bound for every evaluation schedule, or exhibit a legal compact affine/Horn/DISJ execution that undercuts any proposed dynamic potential. Do not assume crossing-producer sends are compulsory in general circuits or SAT machines.

END_OF_VERIFIED_REPORT::TMR-4::054

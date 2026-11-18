# TMR-5/076: complete signed-3SAT-image inverse and exact T5 forced-triad quotient audit

November 17, 2026, 17:42 PST. TMR-5 / PNP Machine Bottleneck Redteam. Named dependency C1-T5-SIGNED-SAT-QUOTIENT-AUDIT (from TMR-1/075). Status **PROVED/EXACT RESTRICTED**, independently derived symbolic proof, external mathematical review OPEN; finite evidence COMPUTATIONAL. P versus NP OPEN.

## Input, falsifiers, and exact claim

Use the canonical unary n,m / low-bit-first literal grammar and deterministic normalized 3SAT->NAE->3COLOR->anchored C5->T5 construction of TMR-5/074. Normalize a nonempty formula F by sorting/deduplicating **ordered signed clause triples**, deleting unused variables, and replacing original variable indices by increasing compact indices. Call this Norm(F). The target graph D(F) is an **exactly labelled** canonical directed source, with the original /074 vertex naming and sorted arc output.

Candidate theorem: A fixed deterministic standard-bit-machine Inv reconstructs Norm(F) from D(F), for all valid nonempty source formulas. More strongly, any target source accepted by the strict image recognizer satisfies D(Inv(Y))=Y. The empty target is the one explicit exception: all zero-clause sources map to the same empty YES graph and lose the original variable count.

The preregistered hostile checks were hidden cross-gadget feed-forward triads; failure to reconstruct signed literal order or need for an unpriced graph-isomorphism oracle; loss of exact solutions in the quotient; malformed input, duplicate clauses or unused names; and hidden source/serialization work.

## Labelled polynomial inverse, including authentic encoded input

For k active variables and m>=1 distinct normalized clauses, the **actual target** header must satisfy

    N_D=57+36k+168m;   A_D=80+52k+244m.

The determinant is 48, so source values are recovered **uniquely** from the parsed full target counts:

    k=[244(N_D-57)-168(A_D-80)]/48;
    m=[36(A_D-80)-52(N_D-57)]/48.

Reject noninteger or out-of-range values. Independently infer

    N_3=3+2k+8m, M_3=3+3k+15m;
    N_H=17+10k+46m, M_H=20+13k+61m.

For each source-ordered H-edge e, recover the exact four T5 arcs (u,z_e),(u,w_e),(w_e,z_e),(w_e,v) at private indices z_e=N_H+2e, w_e=z_e+1. Validate all arcs, source sorting, no extras, u<v<N_H, and distinct recovered H-edges. The anchored five-cycle H, N_3 two-edge root paths and M_3 ordered three-edge graph paths recover every ordered original G_3 edge. Authenticate the 3-color palette triangle, k+m positive/negative literal pairs, and 2m indexed NAE clause triangles. Every triangle's 3 port-to-literal spokes recover the **ordered** source clause literals. Splitter-positive, splitter-negative and fixed-F spokes enforce exact clause positions. Verify no missing/extra G_3 edges, distinct ordered clauses, and use of all k variables.

This reconstructs the complete canonical normalized binary signed CNF, not merely its satisfiability bit. Rebuilding the deterministic forward image validates the actual source bytes. Nothing consults a SAT solver, an assignment oracle, a free reduction descriptor, or a graph-isomorphism search. The recognizer rejects perfectly legitimate T5 graphs outside this exact labelled image; it is NOT a decision procedure for general T5-CSP.

Conservative one-realization bit-machine resource bounds, including parsing and failed attempts, source indexing, arithmetic, every candidate edge/triangle inspection, buffers, complete regenerated comparison, and the output word: T=O((L_D+1)^5), S_peak=O((L_D+1)^2). The normalized source fits polynomially within target encoded length L_D. Exact finite Python script has a stricter actual endpoint-source checker; no native instruction-level microtrace was run.

## Exact unannotated triad quotient and quantitative rank

For the five-symbol R(a,b) iff b-a mod5 in {1,3}, each genuine feed-forward triad a->b,b->c,a->c forces b=a+3 and c=a+1. In D(F), the only such triads are the **M_H private gadgets** (u,w_e,z_e). Every z_e has no outgoing arcs, and original H terminals have no original-to-original directed arcs. The forced-offset union-find therefore identifies each w_e,z_e with its owning u and leaves precisely N_H quotient variables with distinct roots. Each residual w_e->v contributes exactly the C5-difference mask {1,4}, not a spurious factor of two.

Thus the unannotated TMR-1/075 quotient of **every** /074 reduction image is **exactly its authentic middle H graph**, with a bijection of original T5 solutions and H-colorings. All nonempty /074 graphs are connected. Their exact cotree ranks are

    rho_raw=A_D-N_D+1=24+16k+76m,
    rho_quot=M_H-N_H+1=4+3k+15m,
    rho_raw-rho_quot=M_H.

The quotient removes a large *artificial* feedback-rank contribution, but rho_quot is still linear in the source's k,m. Consequently, this exact simplification neither supplies a polynomial general 3SAT algorithm nor a lower bound on arbitrary algorithms. The entire labelled reduction image can also be reverse-decoded to normalized signed CNF at polynomial bit cost. This is a genuine source-aware control against raw graph-width or representation-size-to-decision-time promotion.

## Actually executed independent reproduction

CPython 3, deterministic revision `tmr5-t5-labelled-inverse076-v1`, seed 20261117. The independent decoder reads authentic /074 outputs generated from the prior owned source compiler, but its recovery of k,m, H, G_3, clause ports, sorted arcs, and all feed-forward triads uses independent code.

86 original signed CNF sources (two empty); 84 nonempty valid full reduction images; 15,610 independently discovered original transitive triads; 612 small original-vs-normalized assignment comparisons; 450 original satisfiable-assignment-to-genuine-T5 lifts; 252 invalid mutation rejections (84 add, 84 delete, and 84 **same-vertex-count-and-same-arc-count** tamper controls); 8,383 integral-parameter identities. Zero failures. Brute-force enumeration of the final large negative target instances was NOT performed; their correctness depends on the separately proved reverse witness.

Actual executed source SHA256 `b06bf5b490aad0cca06b0a125d5a26b6e90b00af4ec6c07561a5695d3c5ef681`. Actual raw JSON SHA256 `2dc3d14b68726e912bd17edf4fdd7d3befa693651fb622a89dc9980c42f6c305`. Full legible Python verifier, the exact earlier authentic /074 input generator, the immutable raw JSON, and detailed independent report are preserved in conversation evidence ZIP `TMR5_076_T5_inverse_evidence.zip`. The script and raw are not claimed published in the GitHub repository unless they are actually uploaded and read back. No local pnp checkout exists (GitHub DNS inaccessible), so repository preflight was NOT RUN; full LaTeX compilation, Lean/nanoda, native bit-machine trace, and outside mathematical peer review also NOT RUN.

## Required gates and ranked open dependencies

DISJ sanity PASS for strict source-aware upper construction; rank/width-to-general-work promotion FAIL. Relativization PASS for the syntactic inverse, but unrestricted NP separation OPEN; algebrization and Natural Proofs unresolved. Simultaneous DTISP PASS only for matched same-run upper T,S; no forbidden lower region. Configuration counting NOT APPLICABLE to a proposed lower bound; retain the deterministic upper-only consistency check. Source-aware forest/cycle, affine/Gaussian and Fourier, bounded-treewidth, products, selectors, Horn/2SAT, unique-solution, local-basis, caching and adaptive FBDD controls are all admissible. /341 FAIL full UNSAT; /386 RESTRICTED.

Rank 1: TMR-1 original 3SAT->T5 chain plus unannotated modular quotient, now independently joined on the FULL /074 image, PROVED/EXACT scoped; NP-completeness KNOWN THEOREM (Bang-Jensen, Hell, MacGillivray 1988); arbitrary-machine lower bound OPEN. Rank 2: TMR-2 source-aware cofactor and restricted adaptive NROBP bounds, with cheap connected mixed YES/NO decider countercontrol; necessary work OPEN. Rank 3: TMR-4 pointwise OBDD/FBDD construction and restricted weighted counting, model-independent necessity OPEN. Rank 4: TMR-3 forest/incidence/Fourier recognized-family counting and prior checkpoint providers, unrestricted transfer OPEN.

**ONE next named load-bearing dependency:** a quantitatively unavoidable work/space invariant for authentic mixed YES/NO T5 instances surviving paid image recognition, modular quotients, arbitrary adaptive search and polynomial-time algebraic algorithms. P versus NP OPEN.

Primary papers: Bang-Jensen, Hell and MacGillivray, SIAM J. Discrete Math. 1(3):281-298, 1988, DOI 10.1137/0401029; Hell and Nešetřil, J. Comb. Theory B 48:92-110, 1990. Peer evidence: TMR-1/075 `C1-T5-RIGID-TRIAD-QUOTIENT`; TMR-5/074 signed3SAT compiler, draft PR #209.

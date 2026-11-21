# charged-construction handoff
Updated2026-11-21 11:32 PST.
Current report: [T5-POSITIVE-OFFSET1](PNP_Charged_construction_2026-11-21_113200_Positive_Offset_Pair.md).

PROVED/EXACT explicit paired reduction; external independent review pending. For every acyclic OR/NOT circuit H with p>=1 inputs,o OR,t NOT,b=p+o+t, compile a fresh selector s and W=s OR oldOutput. Unit-fiber Boolean domains use U2,U3,U4 from the prior exclusion theorem. Pin oldOutput for the negative twin and W for the positive twin. Both have SAME n,m,N and multiplier M:
Z(B^-)=2M #CircuitSAT(H), Z(B^+)=M(2^p+#CircuitSAT(H)).
Thus SAT(H) iff SAT(B^-) iff Z(B^+)>M2^p. B^+ is ALWAYS SAT; it is not a SAT-preserving target by itself.

Paired unsplit n=15+4b+2o,m=23+6b+5o+t. After prior equality splitter:
E=54+14b+13o+3t,n_B=285+74b+67o+15t,m_B=347+90b+83o+19t,M=10*2^E,max occurrence5.
3m_B-n_B=14E. Exact N=n+2+2floor(log2(m+1))+3m ceil(log2(n+1)). Ordered R conversion doubles clauses/occurrence bound10; not used in reported N.

FALSIFIED/RETIRED proposed use: positivity alone evades zero-atom obstruction. At fixed p,o,t and source UNSAT probability p0, true positive count equals known c=M2^p with probability p0. Equality to c costs<=6N gates on3N output bits and distinguishes any fake of average conditional min-entropy>=k by at least max(0,p0-2^-k). This is not a Shannon bound and does not exclude one bit. Varying parameter/source recognition must be charged.

COMPUTATIONAL final:98 source circuits,294 generic unsplit T5 counts (no anchor fixing or gadget contraction in counter), split size/degree/encoding checks. Code experiments/t5_construction_positive_offset1_20261121.py SHA2566cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb; raw results/raw/t5_construction_positive_offset1_20261121.json. Split counts use proved equality interface, not full target enumeration. False source NOT(x OR NOT x) gives same-length split n678,m828,E129,N25538,counts0 and20*2^129.

ONE next dependency: Bounds T5-SAT-SLICE-PAIR1, Redteam independent review and Synthesis tracking. Give a specified fake/source pair surviving full multiplier AND baseline-atom test, and prove cap-facing indistinguishability or give a small falsifier. No free SAT conditioning/sampling. Review requested for exact fibers, sharing, paired length and threshold-vs-SAT distinction. Same assistant session is not external independent review.

Retained prior result at c5d8802644abe2caef15ef67153fa76ab8da1152: unweighted graph J_G has Z=10 #3COL,n=5+3v+3e,m=5+4v+5e. Its split B*_G has E=10+9v+12e,n55+48v+63e,m65+58v+77e,Z=10*2^E #3COL,max occurrence5. These OLD GRAPH coefficients are distinct from the NEW CIRCUIT pair. Older weighted H_G remains distinct too. Accounting T5-UNWEIGHTED-CORE-SERVICE1 remains open, not resolved by the new construction.

All auxiliary orientations may be contracted. Affine/Tseitin, private-leaf/matching/tree, complement, forced domains, sharing, renaming, relocation, full-state entropy and decision-witness controls remain. Same fixed-A cap ceilings S N^a,physical CM N^(2a),descriptive CM N^(a+1),count gates N^a logN unchanged. Conservative separate compiler O(U^4)time/O(U)space; no same-exponent transfer, no excluded exponent.

Fresh literature and six-official-org searches/fallbacks recorded; Anthropic formal-math exact MainResults definitions inspected at16a5ce41304fcdaea4e0be7c132e1c361dc26da5 but no proof/kernel build or external theorem promotion. No local checkout/preflight/LaTeX, TMR ownership or schedule changes. P versus NP OPEN.

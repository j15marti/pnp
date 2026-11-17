# T5-PATHSATURATE45 | 2026-11-17 13:55 PST
P versus NP remains OPEN.

Restricted theorem: For R(a,b) iff (b-a) mod 5 in {1,3}, every oriented simple path of length >=4 with unconstrained internal vertices supports every endpoint-color pair. Write increments s_i(1+2z_i), z_i in {0,1}; signed sums range over L+1 consecutive integers, covering Z5 once L>=4. The L=3 threshold is sharp. Existential elimination of private interiors preserves SAT but not exact counts; length-four forward-path endpoint multiplicities are 1,4,6,4,1.

Auxiliary exact upper bound: Root-normalize a spanning forest with c components, then enumerate 2^(n-c) tree-edge binary choices and check non-tree arcs. Multiply counts by 5^c. Alternatively pin at most 2r non-tree endpoint vertices and run tree DP, giving poly(n+m)*5^(2r) time for r=m-n+c. Both are upper algorithms, not SAT lower bounds. TMR4/070 produces high-cycle-rank sources with polynomial-time exact counting.

Affine falsifier: Removing z_e in {0,1} from F5 edge equations x_v-x_u=1+2z_e makes every instance feasible by x_v=0,z_e=2. Plain affine consistency cannot detect UNSAT.

Independent reproducible audit: 62 path orientation patterns, 350 random graphs n<=7, 333 chord DP checks, 65 whole-graph path substitution tests, 8 named controls, 5482 assertions, zero failures. Source metadata n=47,m=236,r=190 was checked, but no exhaustive 47-vertex solve claimed.

DAG: ESTABLISHED T5 NP-complete. PROVED SAT-preserving path deletion and exact rooted-tree count. FALSIFIED count-preservation and unrestricted affine-relaxation refutation. OPEN fully charged hereditary SAT contraction, nonrelativizing WRAPPER necessity, same-input UWI, certificate/decider transport, P vs NP.

Four assignments: Resource Contraction authenticate and charge path reduction plus cofactor MDD; Nonrelativizing Simulation test delayed 3/4-edge guard and oracle replay; Universal Obstruction same final input/clock with path completion witnesses; Proof Transport field-specific elimination-to-proof mappings only.

Full report and standard-library audit saved locally as 2026-11-17_1355_CROSS_TRACK_T5_PATHSATURATE45.md and t5_pathsaturate45_audit.py.
END_T5_PATHSATURATE45_VERIFICATION_SENTINEL
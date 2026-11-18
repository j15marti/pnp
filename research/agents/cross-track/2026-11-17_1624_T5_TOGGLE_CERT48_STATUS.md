# CROSS-TRACK T5-TOGGLE-CERT48 | 2026-11-17 16:24 PST

STATUS: Restricted exact no-go integration and scoped proof-system construction; computational audit passed. External mathematical review OPEN. P versus NP OPEN.

PRE-SEARCH CANDIDATES: (1) TMR-2/070 all-order OBDD rank + fully paid resource contraction; (2) delayed SAT-status-changing WRAPPER plus positive four-path cofactor; (3) SAME-FINAL-INPUT UWI including source-level three-layer witness extractor; (4) actual one-hot Resolution proof transport for the switched UNSAT graph. Proposed before source and literature searches.

SOURCES READ: TMR-2/070 2026-11-17_1512 positive T5 cofactor / all-order OBDD report; TMR-4/069 exact MDD-to-bit-OBDD compiler (Library); TMR-4/062 shared-core source-accounting handoff; Nonrel TRACEAUDIT23 and Clock Gate CLOCKMASKEDINVERSE22; Universal DIAGONALLIST34 (GitHub and Drive index) and ORACLELEAK35 historical cross-track review; Proof Transport PC22-ORCLOSURE38; Cross-track T5-DIAMOND-CONTEXT47; PNP_Hostage_Review_and_Agent_Restart_2026-11-17; project chat summaries and GitHub recent commits. Targeted primary literature: Bang-Jensen/Hell/MacGillivray 1988 (semicomplete CSP dichotomy); FLMV JACM 2005 (model-specific time-space bounds); Amarilli/Monet/Senellart arXiv:1709.06188 (knowledge-compilation width). Google Drive targeted DIAGONALLIST34 and KRYLOVGUARD41. Current four named historical tracks are not assumed to have new Nov-17 individual reports.

FORMAL CONSTRUCTION: For an arbitrary nonempty undirected H=([n],E), enumerate each edge {u,v} with u<v. Make private vertices a_e,b_e,c_e and arcs (u,a_e),(a_e,b_e),(v,c_e),(c_e,b_e), all over R(x,y)=[(y-x) mod 5 in {1,3}]. Call result G_0(H). For lexicographically first edge e0 add exactly one arc (a_e0,u_e0) to form G_1(H).

THEOREM: G_0(H) is SAT, with the explicit 3-layer witness: all core labels 0, all a_e,c_e labels 1, all b_e labels 2. G_1(H) is UNSAT because it contains opposite arcs u->a and a->u, which a loopless tournament cannot satisfy simultaneously. The complete canonical graph serialization can be parsed, all vertices/arcs re-derived and checked, and the corresponding YES witness or NO reverse-arc certificate emitted in polynomial time on this source family. Conservative same-execution bound O((L+1)^6) time, O((L+1)^3) writable bits for explicit source length L, charging all source access, parser checks, construction, memory and witness output. Unknown source graphs receive correct general fallback, not an unsupported instant reject.

PROOF TRANSPORT, SCOPED: In the one-hot CNF for G_1 with variables X_{v,c}, each opposite-arc pair implies for every c,d a forbidden clause (-X_{u,c} OR -X_{a,d}) from one of the two original edges. Resolve the 5 clauses against the at-least-one domain clause of a to derive each -X_{u,c} in 5 steps, for all 5 c (25 steps). Resolve the resulting five units against the at-least-one domain clause for u (5 steps). The empty clause follows after exactly 30 ordinary Resolution inferences. This does not transport arbitrary decider traces or imply hard Resolution lower bounds.

REPRESENTATION BARRIER: TMR-2/070 independently reports exponential OBDD width for every order of the *original-variable assignment indicator* of G_0(H) on a source-generated expander H. The current audit DOES NOT independently prove the LPS expansion or rank theorem. The source decision and satisfying witness remain cheap. For G_1, the assignment indicator is constantly zero, so no exponential OBDD width is claimed. Delaying the choice of the reverse arc changes SAT status but leaves a trivial local test, proving that delay + representation rank + source-authenticated graph does NOT itself force a nonrelativizing resource hinge.

EXACT COUNT AUDIT: Four-arc core-edge transfer W_{s,t}=sum_{a,b,c}R(s,a)R(a,b)R(t,c)R(c,b), with first row (6,1,4,4,1), all entries positive. For G0, every original core coloring extends; no rank-to-decision inference. Fully independent deterministic local Python script t5_toggle_cert48_audit.py, seed 20261117048, 115 source-graph cases n=2..6, 230 switched/unswitched variants, witness replay, direct small counts versus weighted marginal counts, complete parser-tamper controls, exact one-hot axiom/reason check and 30-resolution-step proof replay. 5,681 assertions, zero failures. Machine-readable local results 2026-11-17_T5_TOGGLE_CERT48_results.json. This is finite evidence for a symbolic theorem, not an asymptotic SAT lower bound.

SAME-INPUT UWI FIREWALL: The explicitly constructed source-aware three-layer witness program defeats any proposed universal-on-this-family SAT witness obstruction when it belongs to the eligible program class and its polynomial budget is allowed. It does not establish a globally polynomial witness-finder for arbitrary SAT; the fallback may be exponential. The unsatisfiable switched graph cannot be used as a satisfying-input UWI witness.

DAG:
ESTABLISHED: T5 NP-complete (semicomplete-target dichotomy); model-scoped SAT time-space results.
PROVED RESTRICTED: uniform G0 witness; G1 switched UNSAT; authenticated family recognizer and full paid family upper bound; 30-step one-hot Resolution refutation.
IMPORTED RESTRICTED, EXTERNAL REVIEW OPEN: TMR-2/070 all-order exponential OBDD/cofactor rank on positive source lifts.
FALSIFIED: inference from representation hardness plus delayed source edit plus short UNSAT certificate to mandatory source-SAT decision cost.
OPEN: arbitrary-decider-to-hard-proof transport; genuinely SAT-correctness-forced nonrelativizing WRAPPER operation; identical-final-SAT-input UWI against every eligible program; uniform all-input fully charged hereditary contractor; P != NP.

FOUR NEXT ASSIGNMENTS:
RESOURCE: compare TMR2 positive-cofactor rank, TMR4 MDD and direct three-level witness under one complete charged source-cost ledger; find a parameter surviving source shortcuts.
NONREL: replace local reverse-arc switch with a delayed semantic change that resists direct evaluation, precomputation, replay and oracle controls.
UNIVERSAL: hold one final SAT graph and common clock fixed; include a source-certified witness extractor among challenging programs, with no quantifier swap.
PROOF TRANSPORT: attempt a genuine calculus- and field-specific decider-to-proof mapping beyond this constant local unsatisfiable core; show full proof length, encoding and construction costs.

Highest-value open arrow: establish an unavoidable, fully charged operation for every hypothetical polynomial-time decider on the identical final source, not only a representation lower bound. No scheduled task changed.

LOCAL FULL REPORT: /mnt/data/pnp_cross_track/2026-11-17_1624_CROSS_TRACK_T5_TOGGLE_CERT48.md
LOCAL FULL AUDIT: /mnt/data/pnp_cross_track/t5_toggle_cert48_audit.py
READBACK_SENTINEL::T5_TOGGLE_CERT48::P_VS_NP_OPEN

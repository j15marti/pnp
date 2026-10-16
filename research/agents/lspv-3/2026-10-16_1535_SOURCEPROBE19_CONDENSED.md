# SOURCEPROBE19 (LSPV-3)
Timestamp: 2026-10-16 15:35 Asia/Seoul. Scientific status: scoped theorem and finite computational checks; P versus NP OPEN.

## Ideas fixed before search
(1) Bound the success set of each black-box point-oracle program. (2) Compile the chosen point to explicit Circuit-SAT/3-CNF and test source recovery. (3) Audit all-collision SAT witness lifts. (4) Test diagonal construction clock inflation.

## Literature and previous work
Reviewed PORTFOLIOEQUIV15, CIRCUITPORTFOLIO16, TOTALSHIELD17, REJECTFIBER18, CROSS-TRACK_TRANSPORT_DIAGNOSIS6, and Google Drive BIG_PICTURE2-0207. References: Baker, Gill and Solovay 1975 DOI 10.1137/0204037; Cook 1971 DOI 10.1145/800157.805047; Orponen et al. 1994 DOI 10.1145/174644.174648.

## Exact theorem and proof
The public oracle circuit Q_n(x)=O(x) has a source and length N(n) fixed independently of the hidden oracle O_z(x)=[x=z]. A deterministic program making at most q oracle queries and returning one final witness candidate succeeds for at most q+1 hidden points z. Run the program against the constantly-zero oracle. If the run with O_z queries z, its first such query also occurs on the zero-oracle run. If it never queries z, the complete traces match, so a successful output equals the zero-oracle final candidate. Thus its success set is contained in its zero-oracle query set plus final candidate.

With K eligible programs, if 2^n>K(q+1), choose one z outside the combined query/output sets. Every program fails on the same final oracle instance. For logarithmic description caps K=O(N) and polynomial q, such z exists for large n. The construction is itself polynomial in N for each fixed clock, but may require a larger polynomial clock.

## Finite-source falsifier
The explicit point circuit AND_i(x_i if z_i=1 else NOT x_i), and its proper 3-CNF using four three-distinct-variable clauses per literal, expose every z bit. One fixed linear-time program reads clause polarity and produces a valid satisfying assignment. Thus the oracle-only lower bound cannot be lifted to unrestricted Circuit-SAT.

## Test and handoff
Six finite portfolios (n=7 through 12), 69,888 exhaustive point-CNF full assignments, and a sharpness cover of 64 points: 73,556 assertions, zero errors. All simulation, source generation and witness validation costs were charged in the scoped argument. Remaining obligation: a source-visible aggregate-success bound on one explicit satisfiable formula, without an oracle-only interface. No unrestricted P versus NP conclusion.
FINAL-SENTINEL-SOURCEPROBE19-OPEN

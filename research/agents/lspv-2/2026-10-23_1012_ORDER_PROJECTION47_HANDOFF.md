# 2026-10-23 10:12 Asia/Seoul | Role 2 ORDER-PROJECTION47
STATUS: P versus NP OPEN. Role: CHARGED NORMALIZATION. Full tested audit maintained separately in the current run's exported bundle.

Three proposed falsifiable constructions: (A) source-coherent trace-variable elimination of a parity XOR ladder, (B) source-first equisatisfiable elimination of the same ladder, (C) exact source-only vs source-plus-trace strong 2-CNF backdoor comparison.

For n original source bits x1,...,xn, form n-1 XOR2 gates t1=x1 xor x2, tj=t(j-1) xor x(j+1), output pin t(n-1)=1. Each XOR2 gate is encoded by four proper ternary clauses and the output is a unit clause. Original CNF length N=Theta(n log n); exactly 4(n-1)+1 clauses and 12(n-1)+1 literal occurrences. Each source assignment has exactly one valid functional gate-trace extension, and the source-projected predicate is parity-one.

ESTABLISHED (classical; Emdin et al., MFCS 2022): any CNF over just the original n source bits expressing parity-one requires exactly 2^(n-1) non-tautological full-width clauses. Reference https://doi.org/10.4230/LIPIcs.MFCS.2022.47. Stronger auxiliary-budget clause lower bounds appear in this paper. This is a representation lower bound, NOT a SAT lower bound.

ESTABLISHED (restricted fixed-order Davis-Putnam VE): eliminate t1,...,t(n-1) first and the source-only intermediate has 2^(n-1) clauses. The last trace pivot alone attempts (2^(n-1)+1)*2^(n-1) resolution pairs. Then eliminating source variables finishes at TRUE (k=n, r=0). Alternatively eliminate x1 first, then traces, then other sources: all gates vanish through tautological resolvents and the complete all-variable normalization finishes at TRUE (k=n, r=0) after exactly 4(n-1) attempted pairs; peak CNF representation is its input size. Thus identical final r and truth label do not determine charged work. Both are easy SAT instances; a polynomial source-aware gate reader solves directly.

ESTABLISHED (restricted backdoor): under direct assignment with clause shrinking, the minimum strong 2-CNF backdoor using source+aux variables is ceil((n-1)/2), versus n-1 using original source variables only. This is a hyperedge hitting-set fact for the XOR-gate supports. Certificate: n-1 XOR2 gate triplets, four truth-table clauses per gate, and output pin; verify by reading actual signed literals, check exact shared-source compatibility. No claim that discovering arbitrary hidden equivalent gates is easy.

COMPUTATIONAL n=3..11: exact Python resolution-pair audit, 4,088 original-source truth table evaluations; full assignment functional-extension tests n<=6; exhaustive small-backdoor optima n<=7. At n=11: N=949 bits in explicitly specified gamma-coded CNF representation; 41 initial clauses; trace-first source-only CNF has 1,024 clauses, peak 161,833 encoded bits, 1,403,248 attempted resolvent pairs, 1,398,136 discarded tautological pairs, and 32,689,104 clause-literal reads. The source-first all-variable order has 40 attempted pairs, 240 pair literal reads and peak 949 encoded CNF bits. Both end k=n, r=0. Exact all-variable trace-first run was executed only n<=7; for larger n the additional pairs are certified analytically, not claimed measured. Gate basis XOR2 with 2(n-1) directed gate-input wires; no switch/transistor lower bounds.

RETIRED: general necessary-work=2^r claim, and any transfer from a pure CNF-output lower bound or a fixed bad normalization order to all deterministic SAT deciders.

OPEN: arbitrary source-compatible normalization acquisition, representation-to-unrestricted-machine extraction, and P versus NP. Under hypothetical P=NP, a polynomial preprocessor can decide and return constant TRUE/FALSE, so any universal theorem must charge both-label decision and cover every uniform deterministic polynomial-time algorithm for one fixed NP-complete language.

Originals inspected exactly this run:
1. research/agents/lspv-3/2026-10-16_1535_SOURCEPROBE19_HANDOFF.md (SHA ebadafe4bd1ba8bde45263b6057eff7e1b1060ae);
2. research/main/2026-10-23_0648_MAIN_EXPANDER_RESIDUAL_SIZE82.md (SHA 99b395a16b8330d575dbfe70ab53a804654524f3);
3. Google Doc ES-ATLAS-0025, 1xUMt-pnPu2OMCVHIUGg3hPcEborWG7AMA4eJMh3qbzY.
Previous Role2 CHARGED-NORMALIZATION46 known from conversation but NOT rereviewed. Remaining unseen: generalized DOUBLE_WRAPPER executable, most Google Drive Living Logs, newer agent logs.

Primary results: Emdin/Kulikov/Mihajlin/Slezkin 2022 DOI 10.4230/LIPIcs.MFCS.2022.47; Davis/Putnam JACM 1960 DOI 10.1145/321033.321034; Gwynne/Kullmann arXiv:1406.7398.

Next experiment: two overlapping reordered parity chains (paired SAT/UNSAT), gate-corrupted source controls, graded remaining auxiliary budget, discovery cost for normalization orders, exact witness and contradiction certification. Explicitly do not infer P!=NP or P!=RP.

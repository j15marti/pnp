# LSPV-2/459 five-role handoff: tree-based OR fold (2026-11-06 20:16 PST)

**Status: PROVED/RESTRICTED decision identity; CONDITIONAL same-machine upper bounds; COMPUTATIONAL finite controls. P versus NP OPEN.**

**Route allocation unchanged:** LSPV-2 and LSPV-4 primarily Route A; LSPV-1, LSPV-3 and LSPV-5 primarily Route B. Five existing hourly agents, their titles, enabled state and schedules unchanged. No historical R_mix341 grammar or inference weight changes.

## Exact result

Existing LSPV-2/457 OR-folding, in a previously certified PATH3 original source grammar, extends to a canonical, authenticated **balanced binary tree** of contiguous original proper ternary clause blocks. Every variable is private to one tree node or belongs to exactly one interface between two adjacent nodes. Each node has at most two children. A message M_v(b) means subtree SAT given the parent edge boundary b. For every child c and forbidden assignment a with M_c(a)=0, add an ordinary CNF blocker D_(c,a) to the physically materialized guest. SAT of the local block plus all blockers and pins for b equals M_v(b), by exact bidirectional amalgamation. No independent-child SAT-label join is silently assumed.

For h tree nodes, edge width w and block size L, guest calls q<=(h-1)2^w+1. Depth-first traversal retains O(2^w log h) message bits, plus O(h log N) offsets and one B=O(L+2^w w log N) guest buffer. If h,L<=N^(1/2+o(1)), w<=(log_2 N)/10+o(log N), and the fixed general-CNF SAT decider A is embedded with the previously charged same-machine reserializer, then conditionally:
$$
t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),\quad
s'\le\max\left(\frac12,\frac s2\right).
$$
This does not improve LSPV-4/456's special aligned-encoding PATH3 space bound. It does not cover arbitrary sources or recursively compose since guest blockers/pins fall outside strict original source grammar.

## Published hard-family and shortcut control

Authenticated odd-charge cubic-expander Tseitin 3-CNF has H vertices, 3H/2 edge variables, 4H proper ternary clauses, N=Theta(H log H), and 2^Omega(H) **ordinary DAG Resolution** refutation lower bound for suitable expanders (Urquhart 1987, Ben-Sasson/Wigderson 2001). The charge-parity GF(2) shortcut is polynomial time. Source-packet-preserving balanced tree layouts with o(H) packets/node require a cut edge carrying Omega(H) variable-interface width, violating w=O(log N). This is NOT hardness for arbitrary SAT algorithms, ER, GF(2), or historical full R_mix341.

## Executed tests and artifact provenance

Full local Python producer: 36 original proper ternary sources, 18 SAT and 18 UNSAT, h=3,7,15 and deterministic seeds 0..5; 564 actual guest DPLL calls; 5,032 producer assertions PASS. Independent JS reconstruction, DPLL and pairwise-vs-OR-fold controls: 3,256 assertions PASS and exact 36/36 source SHA256 matches. Additional hostile controls include a source with independently SAT child blocks but globally UNSAT and forged all-true predecessor messages. Tests are host language, **not** native FLMV machine or historical R_mix341 checker execution. Complete local producer, independent original JS and unabridged raw data in reproducibility archive. Published standalone GitHub JS is a source-embedded variant; its exact GitHub bytes have readback but no native FLMV timing claim.

GitHub report: research/agents/lspv-2/2026-11-06_2016_LSPV2_BALANCED_TREE_ORFOLD459.md (blob 0b3b6f23b9d07585242f9bc5db7bbe420268493c). Standalone JS: experiments/arc/lspv2_459_independent_standalone.cjs (blob e9d080342faa23c1f9985668e503f4e5e6be082c). Per-case summary: results/raw/arc/2026-11-06_2016_LSPV2_459_TREE_ORFOLD_summary.json (blob 956b1113ef53f7809c47fdca769464808d49a7c1).

## Trackers and coordination

BOTH live proof1.txt and proof2.txt were inspected; relevant IDs [P1-S3], [P1-01], [P1-03], [P1-04], [P2-A1], [P2-A2], [P2-A3], [P2-A4], [P2-A5], [P2-B1], [P2-B2], [P2-D1]. Only restricted evidence in [P1-S3] and [P2-A4] can be extended; all load-bearing obligations remain OPEN. If an optimistic-concurrency update is blocked, preserve the file, document the blocker, and do not claim a successful tracker amendment. Root main.tex left unchanged if its body cannot be safely recovered for ownership-preserving modification.

**Next Route A target:** unrestricted A-dependent discovery and native-cost verification of small derived interfaces, recursive eligibility for arbitrary general CNF and malformed inputs. LSPV-4 audits physical work/space; Route B peers retain native proof-system legality and B3 as their primary tasks. P versus NP remains OPEN.

# LSPV-2 MIXED-RES-TRANSFER365

November 3, 2026, PST. Symbolic construction plus independently implemented finite verification; external specialist review pending. No new rule, weight, task, or schedule. P versus NP open.

## Established starting point

Buss and Turan, *Resolution Proofs of Generalized Pigeonhole Principles*, TCS 62(3):311-317 (1988), Theorem 1, proves that every ordinary DAG Resolution refutation of PHP(p,h), p>h, has at least (1/2)(3/2)^(h^2/(50p)) total lines. The CNF has one occupancy clause per pigeon and pairwise same-hole collision clauses, hence m=p+h*binom(p,2). There are no extra functionality clauses. The author PDF's printed page 3 was verified from text and screenshot: https://mathweb.ucsd.edu/~sbuss/ResearchWeb/WPHP/paper.pdf . This is a proof-model lower bound, not a SAT runtime bound.

## Positive transfer with explicit loss

Use the audited source-independent two-input wire-DEF interpretation of fixed R_mix341, with RES, AND3, GF(2), and justified LOCAL-CONVERT. Let pi be a valid refutation of normalized CNF F, with m source clauses, q charged nodes and g definitions. Let B contain all original variables directly input to any definition. Set b=|B|<=2g. Assigning B determines every auxiliary wire topologically.

For each non-RES/non-DEF inference, take the syntactically declared union of variables in its premises and conclusion, then remove B and auxiliary wires. Let d be the maximum remaining size, default zero. No free semantic support minimization is used.

**Theorem.** There is a strict ordinary Resolution refutation on the same original variables with at most

    Q = 2^b (m + q*2^(d+1) + 1) - 1

paid derived nodes.

**Proof.** Branch on all 2^b assignments to B; evaluate rather than guess auxiliary wires, making their defining clauses true. A restricted RES step needs at most one resolution or weakening. For any other sound inference on a variable union U, represent restricted conditions by their false-assignment blocking CNFs. For each false conclusion assignment, branch on the other U variables. Some antecedent is false at every leaf; weaken its authenticated blocking clause to the full leaf blocker and resolve upwards. Across all conclusion assignments this costs fewer than 2^(|U|+1) nodes. Constant false is the empty clause. Lift every branch by adjoining its B-assignment blocker, using at most m source weakenings. Glue the 2^b blockers with at most 2^b-1 resolutions. Finally erase weakenings through subclause representatives: alias a premise if its representative has lost the pivot, otherwise resolve. The empty-clause representative remains empty. No cost increase occurs. Shared nodes are translated once per branch. QED.

This statement assumes all exposed wires are original variables or charged conservative DEF outputs. It does not settle the outstanding interpretation in which a circuit-valued LOCAL-CONVERT exposes uncharged internal wire names. Explicit payload evaluation is charged; no bounded-payload normalization is assumed. The implementation uses normalized non-tautological clause records. Raw tautological inputs are separately parsed but not passed through this prototype compiler. Empty source clauses have a separate zero-cost case.

## Consequence for the missing transfer

The published lower bound and compiler give

    (1/2)(3/2)^(h^2/(50p)) <= m + 2^b(m+q*2^(d+1)+1)-1,

and therefore

    b+d+log2(2m+q+1) >= [log2(3/2)/50]*h^2/p - 2.

For p=h+1 and polynomial q, b+d=Omega(h), hence 2g+d=Omega(h). For the RES+DEF fragment d=0. For balanced PHP, encoded input length N=Theta(h^3 log(h+2)). This is a proof-size versus shortcut-scope tradeoff, NOT a q-only superpolynomial bound. Existing polynomial Extended Resolution proofs are compatible with it.

Small b+d=O(log N) gives a polynomial logical reverse simulation. A universal short-proof normalization into that regime cannot be assumed: known short extended PHP proofs and the Resolution lower bound obstruct it. No B1, B2, B3, or unrestricted SAT lower bound is established.

## Independent finite verification

Python producer and separately written JavaScript checker: 11 compiled proofs; 39,163 assertions; 2,401 local implication templates; 26 corrupt certificates rejected; 8 malformed DIMACS strings rejected; 110 clause-deletion SAT controls; 110 selected-literal sign flips (one per clause, not all occurrences); even K4 has 8 models. Model enumeration is capped at 12 variables and local semantic checks at 16. These are test cutoffs, not an optimality certificate.

| Case | q | b | d | Strict RES output |
|---|---:|---:|---:|---:|
| PHP(2,1) | 2 | 0 | 0 | 2 |
| PHP(3,2) | 10 | 0 | 0 | 10 |
| PHP(4,3) | 43 | 0 | 0 | 43 |
| Odd triangle | 5 | 0 | 3 | 5 |
| Odd K4 | 15 | 0 | 5 | 27 |
| Odd K3,3 | 23 | 0 | 9 | 163 |
| Used AND definition | 7 | 2 | 0 | 6 |
| Nested signed-definition control | 8 | 2 | 0 | 6 |
| Local clause conversion | 3 | 0 | 2 | 2 |
| Local circuit conversion | 3 | 0 | 2 | 2 |
| Charge-switched K4 | 15 | 0 | 5 | 27 |

No minimum cost is claimed for these translations. The full local results.json is 456,349 bytes, SHA-256 a74ce31aff1b8ccafa38f67327536aeeb3ddc768f875ca020ffc0bafe7b275e3. Full producer/checker/data are in the delivered reproducibility archive. The public JSON is a results ledger, not the full certificate dataset; the compact public checker replays only the emitted strict-Resolution proofs.

Let L be actual input proof/payload bits. A conservative compiler time is 2^(b+2d)*poly(L+n+m+q). Materialized output bits are O((m+Q)(n+1)log(n+Q+2)), in addition to input L. Host measurements: producer 0.85 seconds / 99,084 KiB peak RSS; independent checker 0.18 seconds / 37,040 KiB. These are not native FLMV measurements or work-domination theorems. All-phase memory and proof discovery remain separate from logical node cost.

## Reviewed project evidence

Original calculus: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Prior barrier: research/main/2026-11-02_1648_MAIN_EXTENSION-SIMULATION-BARRIER-REFEREE299.md, blob 71e3f22bd321970e8747d29147e4ac5815f20ab1. Current peer: research/agents/lspv-3/2026-11-03_0824_LSPV-3_BOUNDED_INTERFACE_TRANSFER367.tex, blob d63c29ed6a549ad46c8e325aa8a3f4d76a81332a. Its circuit-opacity caveat is retained, not resolved by this theorem.

Actual folders were located, not guessed. Read GROKPROOF/2026-11-03_1518_PROGRESS.md, blob 234fc189b01fa163eb10e128556e9d22e085b755: its unfinished ARC construction and restricted live-space claim do not supply B3 or the present translation. Read research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67: its barrier concerns specified alternation-trading rules, not arbitrary SAT algorithms. Neither assessment is accepted as authority beyond its proved scope.

Searches included repository `extension support resolution`, OpenAI-organization `resolution proof`, and primary literature on PHP, extensions, and proof simulation. OpenAI hits were unrelated uses of mathematical resolution; no relevant code was adopted and no novelty is inferred. Haken's publisher page returned 403. The Buss PDF was ultimately read successfully, including its displayed theorem. Governance, issue #3, and the repo skill were read; no complete repository-wide preflight was run.

Root main.tex returned an empty body via both file and blob reads despite SHA 01abe96105c071cdf405dba3a18b8aa69ae26bda. It remains unchanged. Only new role-owned outbox paths are written. The next gap is a valid bridge that survives both extension dependencies and global algebraic scope, not an unsupported assumption that both are logarithmic.

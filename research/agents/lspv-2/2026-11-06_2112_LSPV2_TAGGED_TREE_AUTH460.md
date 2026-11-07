% LSPV-2 REPORT::460::2026-11-06T21:12:30-08:00
# LSPV-2/460: Exact tagged-source authentication for restricted tree OR-folding
**2026-11-06 21:12 PST | Route A | PROVED/RESTRICTED parser and exact OR-fold identity, CONDITIONAL native resources, COMPUTATIONAL controls. P versus NP OPEN.**

## IDEA, four falsifiers, and search-driven revision
LSPV-2/459 assumed a streaming authenticator for its strict proper-3CNF balanced-tree source. Hypothesis: if variable names are arbitrary and untagged, that streaming ownership check requires global memory, but a canonical typed-ID namespace makes the *promised restricted language* explicitly recognizable with low work space. F1: a forged cross-block private ID passes; F2: a forged nonincident edge ID passes; F3: legal SAT or UNSAT originals are rejected; F4: one-pass verification needs an N-bit visited set.

Search revealed LSPV-4/431 already proves a one-pass untagged set-disjointness firewall and LSPV-4/429 already uses cheap bit-length namespaces. **These are prior results and are not claimed as new.** The present advance is a fully specified binary ownership grammar plus an actual low-state streaming parser and independent original 3-CNF SAT/UNSAT and corruption checks for the *tree OR-fold* compiler.

## Exact signed-3CNF encoding and authentication theorem
Let N be source bit length, K=bit_length(N+1), h=2^d-1, V=2^bit_length(h), I=2^K. An input has a fixed 16-bit magic 0xA531, K-bit fields d,w, and h blocks in heap node order 1,...,h. Each block has a K-bit positive clause count and exactly three signed original literals per clause; a literal is one sign bit and a 2K+2-bit identifier. All original clauses have three *distinct* underlying variables. Interpret IDs as

$$
\operatorname{id}(\tau,v,i)=((\tau V+v)I+i).
$$

Tag 0 is private P(v,i), allowed only at node v. Tag 1 is E(c,i), an interface edge owned by child c>=2, allowed only at c and floor(c/2), 1<=i<=w. Each source clause in node v can use only P(v,i), E(v,i) or E(c,i) for c=2v,2v+1. Verify owner locally on every original literal. Reject nonbinary, trailing/truncated bytes, zero IDs, illegal tags, nonincident edge owners, duplicate literal IDs, empty blocks and malformed headers. Require w<=ceil(log2 N /10), and h and each block bit length <=4(floor(sqrt(N))+1)K, enforcing N^(1/2+o(1)) limits.

**Theorem 460.1 (PROVED/RESTRICTED).** On the read-only, fixed-width tagged source above, a single forward pass checks *every* field and ownership constraint in O(N polylog N) deterministic bit time and O(h log N+polylog N) writable bits, including the h node offsets and only O(log N) transient counters and up to three current literal identifiers. Global private-name disjointness is immediate from injectivity of tagged ownership, rather than a globally memorized set. Python's independent streaming scan implements precisely these abstract operations; Python interpreter RAM is not a native FLMV space measurement. The source restriction is not a free all-input CNF normalization.

The old untagged obstruction remains: checking two groups of arbitrary m-element private-name sets S,T from [2m] for disjointness has at least binomial(2m,m) distinguishable one-pass first-half prefixes, requiring Omega(m) state bits, by choosing suffix [2m]\S. With h=Theta(sqrt m) source blocks and O(sqrt m log m) bits per block this yields N=Theta(m log m), a one-pass lower bound Omega(N/log N), far above N^(1/2+o(1)). This specializes known LSPV-4/431 to the tree grammar; indexed rereads and canonical tags are outside its restriction.

## Restricted tree SAT identity and resource ledger
Use the legal LSPV-2/459 child message M_c(a). For each node v and pinned parent interface b, add all local original clauses, physical b-pins, and one genuine CNF clause D_(c,a) excluding each child interface a with M_c(a)=false. Then

$$
M_v(b)=\operatorname{SAT}\left(F_v\wedge(Z_{vp}=b)\wedge\bigwedge_{c}\bigwedge_{a:M_c(a)=0}D_{c,a}\right).
$$

The AND of required independent child constraints is genuine conjunction; the existential SAT guest provides OR over compatible hidden choices without leaking branch-local assumptions. Guest count q<=(h-1)2^w+1, each guest B=O(L+2^w w log N)=N^(1/2+o(1)) *physical bits*, retained messages O(2^w log h), and offsets O(h log N). Source parse/index, materialization, query calls, update, retrieval/restart and output are charged. Conditional on the previously stated **same FLMV indexed-machine** guest interface, not native-executed in this run:

$$
t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),
\qquad s'\le\max\left(\frac12,\frac s2\right).
$$

The original strict-3CNF tagged grammar is not closed under ordinary-CNF blocker/pin guest syntax, and on ordinary CNF outside the grammar fallback correctness does not imply contraction. Recursive, all-input A->Phi(A) [P2-A2] is OPEN.

## Established hardness, controls, and exact theorem limits
Urquhart (JACM 1987) proves exponential ordinary shared-DAG Resolution refutation length for Tseitin formulas on suitable expander graphs. Cubic H-vertex odd-charge instances have 3H/2 edge variables, 4H proper ternary parity clauses, N=Theta(H log H); sum of charges odd certifies mathematical UNSAT. Ben-Sasson/Wigderson (JACM 2001) supply Resolution width/size relations; Itsykson/Riazanov/Smirnov (SAT 2022) give regular Resolution/OBDD treewidth bounds. GF(2) charge summation is a polynomial-time shortcut and MUST be retained. LSPV-4/457 shows packet-preserving expander guests fail recursive bounded-tree closure. None of these restricted proof lower bounds transfers to full R_mix341 or arbitrary SAT algorithms. No hardness-preserving 3-CNF conversion is claimed.

## Executed finite controls
Complete Python and independently written Node.js programs are packaged in the linked full reproducibility archive, including source hashes. 18 original signed proper ternary tree sources (h=3,7,15; 3 seeds; 9 SAT, 9 UNSAT), 282 actually evaluated DPLL guest calls. Python: 148 assertion groups passed. JavaScript: 94 checks passed, including four independently reproduced source-hash prefixes. In **each** language, 108 invalid sources rejected: cross-block private collision, nonincident edge, duplicate variable within a ternary clause, wrong magic, truncation, trailing bit. Source bit lengths at h=3,7,15: 894, 2392, 5457. These are finite host-language tests, not asymptotic hardness certificates or physical FLMV time/space measurements.

## Evidence and provenance
Both root proof trackers, current issue #3, November 2 five-role handoff, AGENTS.md, CODEX.md, project skill, actual peer LSPV-2/459, LSPV-4/431, /456, /457, and GROKPROOF/2026-11-06_2316_PROGRESS.md were read. A claimed Claude path on a separate branch was visible in issue #3, but fetching it on main returned 404 and is not claimed as read. External authenticated files: konard/p-vs-np/proofs/complexity/README.md (blob 7ee9a11e, different one-tape machine), blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md (blob 4aba9d94, fixed-width problem), MassimoLauria/cnfgen/cnfgen/families/tseitin.py (blob 4bb5fd19), meelgroup/frat-xor/format.md (blob 986a21aa, distinct XLRUP), berkeley-abc/abc/README.md (blob 88a9d1a3), and openai/math/README.md (blob cc5b0a03). Primary papers and project history were searched; no separate branded Google interface or native FLMV simulator was available.

**Exact tracker IDs:** [P1-S3], [P2-A4] restricted evidence; [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A5], [P2-B2], [P2-D1] all retain their earlier status. All 5 roles/allocations, scheduled tasks and historical R_mix341 grammar/weights unchanged.

**Actual advance:** a specific, locally authenticatable restricted source language and testable parser, replacing an unimplemented grammar premise in /459. **Verification:** finite Python/JS passed, no native FLMV run. **Remaining gap:** universal, recursively iterable same-machine all-input transformation, and independently Route B's same-R B3. P versus NP OPEN.

% END_OF_VERIFIED_REPORT::LSPV-2::460

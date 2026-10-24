# NAMED-PROFILE-IDENTITY125 — Role 5 additive handoff

Status: **PROVED/EXACT in the declared named-profile/CSP model; COMPUTATIONAL finite audit; ARC-EDGE-90 OPEN; P versus NP OPEN.**

## Exact recovered link

For an ordered proper clause (C_i), retain its ordered variable-ID triple (V_i) and its eight-bit local truth profile (p_i). The record ((V_i,p_i)) uniquely reconstructs the signed clause: the unique zero row gives all three signs. Therefore the ordered transcript


\[
\nu(F)=(n,m,(V_i,p_i)_{i=1}^m)
\]

is an injective, uniformly invertible encoding of the original ordered proper 3CNF.

The exact join condition is

\[
\mathrm{SAT}(F)\iff \exists a\in\{0,1\}^n\ \forall i,
\quad a|_{V_i}\in\{b:p_i(b)=1\}.
\]

This is the original Boolean CSP. Dropping (V_i) causes Role 3's connected opposite-label collision; retaining (V_i) restores correctness but leaves the original compatibility problem.

## Two-level audit

The complete named profile of every clause in the 13-clause pin child (H(C,b)) reconstructs (H(C,b)). Conversely (H(C,b)) is a fixed function of the first profile and (b). The second level is transcription/idempotence, not new global gluing information. Recursive enumeration is optional because the child can be regenerated or cached.

## Cross-family controls

- Role 3 connected pair: anonymous profiles equal, named profiles unequal; labels UNSAT/SAT.
- Role 4 periodic pair: all isolated length-3 child count vectors equal; named profiles unequal; labels UNSAT/SAT.
- Role 5 minimal pair: named profile differs only at clause 12; three coherent pins still yield UNSAT/SAT.
- Horn, 2-SAT, affine, source-reread and decide-first SAT/UNSAT controls remain legal adaptive bypasses.

## Reproducible evidence

- Program: `experiments/named_profile_identity125.py`
- Raw output: `results/raw/2026-10-24_LSPV5_NAMED_PROFILE_IDENTITY125_summary.json`
- 9,131 assertion-accounted checks; 64 first-level children; 64 complete two-level reconstructions; 6,656 independently solved grandchild statuses; zero failures.
- Code SHA-256: `3d39169ad54c8fd8dcc2ca29e0685e2295de8e2cc3c03166ba4d41dfafc2199f`
- Raw JSON SHA-256: `62ef6a0644b04f6d774008e5bd787b30c66f5d2f4d812a11633e83c583ba8a92`

## Peer audit

- **Accepted:** Role 1 ARC-ENDPOINT-GUARD125 exactly eliminates FLMV's auxiliary (c): for (t\ge1), membership in the declared two-level forbidden region is (s<\beta(t)), with strict slack. It constructs no successor machine.
- **Accepted as restricted:** Role 2 SELECTOR-SPLIT119 is another exact semantic split whose shared-assignment compatibility join remains NP-complete.
- **Narrowed:** Role 3's next source-name-preserving join test is exact but is source-equivalent unless it separately proves an all-input acyclic/bounded-width restriction or a favorable compatibility algorithm.

## Adaptive-state/resource ledger

Before extraction: read-only source, charged headers, source address, clause counter, profile-row counter, and remaining budget. Rules considered from observed syntax: Horn, SCC/2-SAT, affine elimination, bounded-structure join, anonymous profile, named streaming, source reread, exact DPLL fallback. Dropping names fails correctness; retaining names permits exact reconstruction and then requires the original join. Charge primitive bit work, all reads/writes including unchanged writes, head/address/control flips, failed recognizers, conversions, caches, generated children, join state, live ancestors, peak writable bits and actual cumulative bit-time. SAT and UNSAT terminal conditions remain asymmetric; no label oracle is used.

## Coverage manifest delta

Full current bodies read: root `main.tex`, `main13.tex`, AGENTS, CODEX, repository research skill/red-team protocol, current Roles 1–4 reports ARC-ENDPOINT-GUARD125, SELECTOR-SPLIT119, PIN-PROFILE-JOIN-FIREWALL89, PERIODIC-CHILD-COLLISION83, and Role 5 PINNED-CHILD-SEPARATOR124. Original literature checked: FLMV, Jahanjou–Miles–Viola local reductions, Yannakakis acyclic joins. The inherited pinned 3,532-file keyword/hash crawl is not an exhaustive mathematical reading. Remaining unread queue: full Drive LOG/BOOL/SIL pagination, most historical main2–main12 proof bodies, and the missing HEREDITARY-SCOPED10 executable.

## Exact next obligation

Inspect INTERFACE-PROJECTION8 and the recovered HEREDITARY-SCOPED10 material for an actual all-input theorem that forces the named compatibility hypergraph into an acyclic/bounded-width class while preserving an ordinary child encoding and improving a simultaneous achievable pair. If no such theorem exists, close named-profile recursion as lossless transcription and return to a different ARC mechanism.

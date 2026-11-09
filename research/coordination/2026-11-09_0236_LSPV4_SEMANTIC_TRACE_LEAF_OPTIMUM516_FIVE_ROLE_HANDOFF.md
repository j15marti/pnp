# LSPV-4/516 five-role handoff | 2026-11-09 02:36 PST

**Route A. PROVED/RESTRICTED + COMPUTATIONAL. Exact new node [P2-L4-516]**, refining [P2-L2-516], [P2-L2-515] and [P2-L4-515]. Still OPEN: [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P versus NP OPEN.

**Exact result:** On LSPV-2/516's authenticated original strict-three guarded K4 selector family with $k$ independently signed pins, there is precisely one UNSAT descriptor (zero) and $2^k-1$ SAT descriptors. Every deterministic total correct all-input guest makes at least $k+1$ distinct complete source read-value transcripts across the family, even though the rank of the zero trace is $k$. This lower bound is attained by a sound sign-blind *invariant-position source authenticator* followed by short-circuit evaluation of the pin signs. Reading all four negative signs in each zero pin is necessary for soundness on arbitrary mixed-sign template variants, rather than one sign (which would be promise-only). A fixed fastpath may accept at the first positive sign because any positive pin guard literal makes the guarded core satisfiable, and no positives force the odd Tseitin UNSAT core. A generic SAT fallback handles malformed/off-template inputs; it is exponential unconditionally, or polynomial conditional on SAT in P. Thus exact trace classes are $k+1$ (short-circuit) versus $2^k$ (full scan) while both complete guests are correct.

**Full resource firewall:** On $q=2^k$ inputs the shortcircuit route observes $5q-5$ *tag sign bits*, full scanning observes $4kq$. Both independently pay original-source invariant authentication, $O(qM)$ read work if run from scratch on all children, plus all indexed-head/INDEX writing and erasure, guest runtime, outputs, cache/state retention, reconstruction, and all-phase WORK high-water. This is neither a paid-computation lower bound nor a $t',s'$ contraction. Even with a trace trie $O(k\log k)$ bits on this example, the true general SAT fallback and source/child conversion dominate possible worst cases. [P2-A2]/[P2-A4]/[P2-A5] OPEN.

**Source details:** K4 odd-charge Tseitin 16 proper ternaries; $n=19+6k$, $m=27+9k$, exact unary/ordered-literal packet $M=8+n+1+3m(\lceil\log_2(n+1)\rceil+1)+2$ bits. The finite K4 control is NOT a certified asymptotic hard family. Urquhart's expander-Tseitin lower bound is for ordinary Resolution only; no hardness transfer to guarded selectors or historical R_mix341 is established.

**Independent checks:** 2,046 complete descriptor sources enumerated $k=1..10$; 62 DPLL original source controls each in Python and Node (57 SAT, 5 UNSAT); 226 independent Python and 235 Node arbitrary 4-sign-pattern tests plus 20 hostile malformed rejections each; V8 published executable: 2,118 grouped assertions, all 16 four-sign gadget cases and 40 hostile rejects. Python/Node source SHA-256 agreed across all ten baseline encodings. All PASS; no native FLMV or R_mix341 checker execution.

**Published exact paths:**
- research/agents/lspv-4/2026-11-09_0236_LSPV4_SEMANTIC_TRACE_LEAF_OPTIMUM516.md
- experiments/arc/lspv4_516_trace_leaf_optimum_v8.js
- results/raw/arc/2026-11-09_0236_LSPV4_516_TRACE_CLASS_RESOURCE_RAW.json
- this handoff.

**Role directions:** LSPV-2 distinguish the new exact $k+1$ transcript minimum from guest read-rank $k$, and charge all fixed-field validation when assessing the low-rank affine trie. LSPV-4 audit native indexed-skip instructions and simultaneous peak/workspace reset for a true same-machine compiler. LSPV-1/3/5 keep all proof model transfer gaps explicit; do not equate this observation-tree result with mixed-DAG proof work. No schedule/role/calculus edits.

**Outstanding:** Construct a uniform recursively iterable, all-input, both-label, malformed-aware solver contraction that improves the *actual guest exponent* while paying every physical phase. P versus NP OPEN.

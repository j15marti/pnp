# LSPV-2/465 five-role handoff | 2026-11-07 PST
Route A (LSPV-2) primary. Review **both** root proof chains, especially [P2-A2] OPEN, [P2-A4] restricted evidence, [P2-A5] OPEN, [P1-01]/[P1-03]/[P1-04] OPEN, and [P2-B2] OPEN. Keep exactly two Route A (LSPV-2/4) and three Route B (LSPV-1/3/5).

**New restricted index-budget lemma:** Starting at D0=ceil(log2(B+2)) without knowing guest s, maintain exact low D-bit numeric work-index value plus the count of 1 bits above D. Only at an actual legal work-index jump with high count>0, sequentially scan the guest index tape, take J=highest set bit, double D or raise it to J+1, reconstruct, then use the exact address. With polynomial measured work high-water S_A(B)=B^O(1), D_max=O_A(log B), O_A(1) expansions and O_A(T polylog B) index subcomponent time, O_A(log B) extra controller work space. Large temporary high 1-bit strings never require storing their positions. This is *not* a native whole-guest or universal SAT compiler.

**Executed controls:** published JS 199 scenarios / 845 assertions / 229 work-index jumps PASS; independent Python 266 scenarios / 986 exact jumps PASS. Files: `research/agents/lspv-2/2026-11-07_0212_LSPV2_EXPONENT_OBLIVIOUS_WORK_INDEX465.md`; `experiments/arc/lspv2_465_dynamic_work_index_selfcheck.cjs`; `results/raw/arc/2026-11-07_0212_LSPV2_465_DYNAMIC_WORK_INDEX.json`.

**For LSPV-4:** test the fully realized native mirrored WORK indexed moves and exact index-head/erasure semantics; include DATA/MARK reset (LSPV-4/461), direct index sweep (LSPV-2/464), input-index/guest-port and all-phase simultaneous peak. Do not silently insert an exponent extractor or permit uncharged memory. **LSPV-1,3,5:** keep R_mix341 exact historical rules/weights and cross-review B3 only as genuinely relevant. All-inference shared DAG minima unchanged.

**Source control:** original 3-regular expander odd-charge Tseitin 3-CNF, 4H signed ternary clauses, N=Theta(H log H), ordinary DAG Resolution 2^Omega(H) (Ben-Sasson–Wigderson), polynomial GF(2) shortcut. This is not unrestricted computational hardness.

No tasks, roles, titles, schedules, enabled states or root manuscript changed. [P2-A2] and [P2-A5] remain OPEN. P versus NP OPEN. Tracker and issue writes must be handled with current complete blobs and full readback.

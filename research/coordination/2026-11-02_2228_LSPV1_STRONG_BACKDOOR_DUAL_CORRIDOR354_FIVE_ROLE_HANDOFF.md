# Five-role handoff: STRONG-BACKDOOR-DUAL-CORRIDOR354 (2026-11-02 22:28 PST)

**LSPV-1, new project-level necessary screening theorem.** Fix the unchanged binary-premise unit-paid source-independent-VARDEF `Rmix341`. Let b(F) be the size of a smallest heterogeneous *strong* Horn-or-2CNF backdoor: all 2^b restricted formulas must belong to either Horn or 2CNF (which one may vary by assignment). Lift genuine RES leaf proofs back to original sources, then combine assignment-blocker subclauses in a binary decision tree. The proof uses only permitted RES, and yields

```
W_Rmix341(F) <= W_RES(F) <= 2^b(F) * ( c*(N+1)^2 + 1)
```

where N is the encoded source *bit length*. Thus b=O(log N) forces polynomial W_Rmix341. This conclusion does not charge free best-proof choice; any *implemented* search/solver separately charges discovery, parsing, source/index/head reads, switches, proof emission/checking and all-phase peak.

**Explicit falsifier to sufficiency of previous two-filter corridor:** The strict width-at-most-three signed `G_k` is a double-guarded, privately split minimally UNSAT Horn grid:
- m=2k^2+2(k-1)^2 clauses, v=k^2+2(k-1)^2 vars, deficiency k^2;
- primal graph has (k-1)x(k-1) grid minor, so tw>=k-1 for k>=3;
- a single selector z is a *strong Horn backdoor*;
- all original sources are indispensable and flipping any individual signed occurrence makes SAT;
- m-1 <= W_Rmix341(G_k) <= 4(k-1)^2+k^2+1=O(k^2)=O(N).
This has both deficiency and treewidth superlogarithmic in N, yet a short mixed-system proof. It does NOT disprove the earlier necessary-only dual-parameter theorem. It proves those criteria are insufficient on their own, and suggests a third necessary screening criterion.

**Independent full finite audit:** k=2,3,4,5: v=(6,17,34,57), m=(10,26,50,82), paid RES=(9,26,53,90), source floor=(9,25,49,81), exact mixed optimum k=2 only. A different-language Node verifier checked all 168 source deletions, 456 single-sign SAT repairs, 10,000 clause/witness evaluations, every signed proof pivot, both Horn selector assignments, grid-minor edge witnesses, 16 malformed inputs and 4 corrupted pivots. 12,174 assertions PASS. Four source SHA256s and all counts are in the raw ledger. The full source/proof/witness JSON and independent code are retained in a local reproducibility archive.

**Role-specific next assignments, no scheduler modifications:**

LSPV-1: preserve Wbar, B1/B2/B3 exact quantifiers. Extend the necessary corridor to strong Horn/2CNF backdoors, without claiming sufficiency or changing preselected R. Continue the separate weakest sufficient B3/UNIVERSAL-REFLECTION353 source compilation obligations.

LSPV-2: test published Peitl--Szeider extremal minimally UNSAT signed formulas for smallest *strong* Horn and 2CNF backdoors, alongside δ, tw and exact mixed W. Focus on nonaffine instances whose b exceeds logarithmic length. Guard/chain compilers must preserve each signed source and all paid nodes.

LSPV-3: seek growing mixed-hard high-deficiency/high-treewidth/high-backdoor families. Attempt to break the new family with even fewer legal nodes, and search for a truly superlinear *excess* amplification invariant; source direct sums and fresh splits/guards do not amplify.

LSPV-4: implement fixed-guest fully charged time-space tests on authentic signed candidates. Keep logical W upper certificate distinct from machine T/S, verifier read requirements and any same-machine FLMV transport. Do not elevate source-inspection lower bounds to arbitrary RAM/TM lower bounds.

LSPV-5: independently check the Resolution lifting and blocker-combination theorem including tautological source/implication edge controls, the Horn-grid 3CNF source minimality and graph-minor claim; challenge the step from parameterized upper proofs to any B3 statement. Watch malformed and changed-calculus cheats.

**Provenance/duplication:** Strong backdoors (Nishimura--Ragde--Szeider 2004) and Horn/2CNF Resolution are established classical methods. Earlier LSPV-2 guard 350 and LSPV-3 split 353 already prove nonamplification. This handoff adds a precise signed strict-3CNF high-high-low witness and a restricted-proof lifting analysis; no academic novelty asserted.

**Verified role paths:** report `research/agents/lspv-1/2026-11-02_2228_LSPV-1_STRONG_BACKDOOR_DUAL_CORRIDOR354.tex`; compact code `experiments/arc/lspv1_354_grid_backdoor_compact.js`; raw `results/raw/arc/2026-11-02_2228_LSPV1_GRID_BACKDOOR354_public.json`. B1/B2/B3, general mixed superpolynomial minimum and P versus NP OPEN. No task IDs, titles, enabled states, schedules or legacy agents changed.

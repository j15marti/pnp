# Grok continuation log: strict T5 resource lower bounds

Timestamp: 2026-11-24 06:35 America/Los_Angeles.

## Searches performed this cycle

- Authenticated as GitHub user j15marti. Confirmed private repository j15marti/pnp continues to hold the exhaustive handoff (research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md), prior continuation logs through 2026-11-22 21:15, and charged-accounting / charged-bounds agent notes.
- Code search across all of GitHub for "strict T5", "#T5", sole-tape cumulative memory, and related five-valued CSP counting lower bounds: results remain confined exclusively to the pnp repository.
- Organization repository and code searches:
  - org:openai : principal related public artifact remains the openai/math repository containing the Lean formalization of the claimed subexponential exact-counting algorithm for bounded-width CNF (SubexponentialSAT.lean). No additional matches for strict T5, sole-tape models, or CSP-specific resource accounting.
  - org:anthropics : anthropics/formal-math contains the eth/ and related folders with Lean 4 formalizations of the claimed 2^{o(n)} algorithm for 3-SAT/#3-SAT, plus a separate VP ≠ VNP formalization. No matches for five-valued T5 or sole-tape crossing arguments.
  - org:google, org:google-research, org:google-deepmind : no public matches for the strict five-valued T5 cycle relation over Z_5, sole-tape cumulative-memory accounting, matching-family crossing arguments, or related exact-counting resource lower bounds. (Public "T5" results continue to refer predominantly to the text-to-text transformer or unrelated objects.)
- Literature scan: continued focus on the October 2026 OpenAI and Anthropic preprints claiming deterministic subexponential exact #k-SAT algorithms (time roughly 2^{O(n log log n / \sqrt log n)} · poly_k(n, m)), accompanied by Lean 4 formalizations. Independent review (including by Impagliazzo, Paturi, Williams) remains ongoing as of late November 2026; the claims remain uncertified. Threshold analyses (e.g., Szeider note) show the algorithms remain exhaustive search until astronomically large n. Concurrent transfer results derive NTIME simulations from these algorithms. No unrestricted superpolynomial lower bounds for Count_N appear.
- Cumulative memory literature: Beame and Kornerup (arXiv:2301.05680; ICALP 2023; journal version ACM Trans. Comput. Theory 17(3), Article 20, 2025; DOI 10.1145/3728715) remains the principal general reference. Its paradigms convert time-space tradeoffs into cumulative-memory bounds of comparable strength. No new applications to the project's sole-tape matching families or model-free transfers to unrestricted scalar counters or the encoded Count_N map appeared.
- Representation and knowledge compilation: restricted DNNF/DLDD exponential lower bounds for high-treewidth independent-set and Tseitin predicates continue to hold via prior published results (Amarilli et al., Beame-Li-Roy-Suciu, de Colnet-Mengel, Itsykson et al.). No literature result supplies a polynomial bound on the shortcut-defect ratio α for arbitrary scalar counters.

## Key findings

The OpenAI and Anthropic algorithmic upper bounds, if accepted, refute ETH and thereby remove a common conditional-hardness premise used in some #SAT literature. They supply no technique for proving unrestricted superpolynomial lower bounds on the encoded count map of strict T5 (or general #SAT). Representation-specific exponential DNNF/DLDD lower bounds on high-treewidth independent-set and Tseitin predicates remain in force for those restricted classes. Classical one-tape crossing-sequence arguments continue to support the project's audited quadratic time and cubic CM theorems for the sparse matching layouts under the sole-tape model.

No public repository or literature source provides a proof of an unrestricted superpolynomial lower bound for exact counting of the fixed five-valued strict T5 relation. The principal open bridges identified in the handoff (Tasks A–F) remain open.

## Status relative to the handoff

The exhaustive research handoff of 21 November 2026 remains the authoritative baseline. Model-specific single-tape results T = \Omega(N^{2}) and CM = \Omega(N^{3}) for the sparse matching families are retained. Representation lower bounds are architecture-specific. Unrestricted superpolynomial exact-counting and decision lower bounds for strict #T5 remain OPEN. A count-only separation does not by itself separate P from NP. No unconditional superpolynomial claim is advanced.

## Next concrete tasks (priority unchanged)

1. Bounds / circuit: seek any explicit lower bound on C_N (unrestricted Boolean circuit size of the encoded count map Count_N) that exceeds the Pippenger–Fischer simulation ceiling for a target polynomial cap, on a family not known to be easy (e.g., high-treewidth NAND expanders). Verify survival against affine/Tseitin controls.
2. Accounting: construct one concrete compulsory information-transfer demand (with decoder, record, event set, and reuse factor) that survives the input-relocation wrapper of handoff Section 13.4.
3. Discovery: define one concrete scalar-counter operation (symmetry quotient, elimination rule, or algebraic transform) and compute its expansion ratio \alpha on the private-leaf tree and affine Tseitin examples.

All work must preserve the distinctions recorded in the handoff (symmetric C versus ordered R, transport matching versus NAND matching, count maps versus witness predicates, etc.). Finite verification remains non-asymptotic. Claims relying on ETH or similar hypotheses are out of scope for the unconditional objective.

This log is an additive research record. It does not promote any theorem.

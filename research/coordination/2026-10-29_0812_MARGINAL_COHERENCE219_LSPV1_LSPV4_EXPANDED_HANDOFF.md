# LSPV-2 MARGINAL-COHERENCE219 handoff

Status: PROVED/EXACT RESTRICTED (peer review pending); COMPUTATIONAL audits. P versus NP OPEN.

**Specific new construction**: two-state puncture profiles E={(0,0),(1,1)} and X={(0,1),(1,0)} have identical independent one-bit marginals. Build cyclic same-sign literal splice of a B module with exact profile {(0,0)} and k A modules, using proper ternary Pad and Pin0 gadgets. All X yields U_k UNSAT; changing one A to E yields S_k SAT. Both connected, proper ordinary 3CNF of n=7k+9, m=9k+13, max occurrence five, identical signed incidence and unsigned scopes; four physical sign flags differ. Strict signed exact-(2,2) is NOT preserved. No unconditional general SAT runtime lower bound.

**Certified bit-probe promise**: P_k={U_k,S_{k,1},...,S_{k,k}} has side-specific deterministic indexed bit-query complexity Q_+=Q_-=k=Theta(N/log N) for one uniform program; no free answer-class bit. This is input acquisition only. Full malformed-input checking scans the source and is separately charged.

**Restricted contractor**: authenticate full canonical fixed-record source, compare against U and each one-E candidate, emit fixed YES 54-bit or NO 340-bit ordinary 3CNF. Above k>=4, one child is <=N^(3/4). Closure on the restricted grammar and fixed terminal bases; does NOT include arbitrary SAT.

**Resource typing**: indexed bit-query promise k; full indexed-RAM source validation O(N polylog N) bit work O(log N) counters; conservative read-only-input fixed multitape O(N^2 polylog N) time/O(log N) work bits for candidate rescans; read/write one-tape simulation O(N^3 polylog N) time/O(N) total footprint; fixed UTM polynomial charged interpreter overhead, no claimed exact exponent. Real Python stores O(N) bit records rather than implementing the small-space streamer. Gates versus wires not conflated.

**Audit**: 131072 exhaustive assignments, 47042 independent DPLL calls through k=8, nine growing pairs through k=64, 44 mutated-record rejections, base-child bit lengths 54 and 340, two byte-identical raw executions. Independently reran user `Connected_Interface_Audit.zip` from Library: exactly 4680 boundary subsets, 7191 local discovery checks, 139 SAT comparisons. Static bound intact, not a machine lower bound.

**Duplication**: LSPV-3 GUARDED-BOUNDARY-ACQUISITION90 already proved NP-hard one-bit profile extraction; BOUNDED-OCCURRENCE-AFFINE147 already has a five-occurrence affine reduction; LSPV-5 MARGINAL-PARITY-FIREWALL192 already has high-order parity marginal insufficiency. These are not claimed new. The new result is the specific signed-splice bounded-degree, same-source-scopes, four-bit difference and exact side-specific probe theorem. The LSPV-2 SIGNED-PUNCTURE-PROFILE218 Boolean transfer remains valid and is the template being stress-tested.

**Open arrow**: strict exact-(2,2) bounded-degree correlation transport to arbitrary growing cores with polynomial profile discovery, ordinary SAT child generation, source grammar closure, and physical power contraction on both labels. No ARC/FLMV or P vs NP consequence from this control.
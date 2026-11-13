# TMR-3 handoff | 2026-11-13 13:35 PST

**Current owner:** NEW TMR-3 Time-Space Tradeoffs, 2026-11-13 five-role replacement directive, j15marti/pnp main. **P versus NP OPEN.** No schedule changes or legacy role reuse.

**Substantive latest report:** research/agents/tmr-3/2026-11-13_1334_TMR3_SAME_INPUT_MULTIPASS_TRADEOFF001.md (readback verification pending on this handoff's creation). **CANDIDATE** complete symbolic proof pending TMR-5 independent review; **COMPUTATIONAL** exhaustive finite controls.

**Exactly scoped new theorem:** Let E_n(a,b) be the complete TMR-2 binary proper-3CNF equality family, L(n)=13n+2+24n(1+max(1,ceil(log2(5n)))). Restrict a fixed correct finite machine to *complete sequential one-way source sweeps* with no input observations during paid resets, fixed finite work tapes and full writable-cell/head counting. For some one *satisfiable* E_n(a_n,a_n), for every n and every fixed correct machine M,

$$
p_M(E_n(a_n,a_n))(S_M(E_n(a_n,a_n))+1)\ge c_M n,
$$

and on the *same input* $T_M(S_M+1)\ge c_M L(n)n=\Omega_M(L(n)^2/\log L(n))$. A complete variable-length communication transcript for each diagonal is injective: collisions splice into mixed UNSAT. The 2^n binary strings force one serialized transcript of >=n bits, each bounded by O(p(S+1)) including all work-head positions/control. This is a restricted *same-input* tradeoff, distinct from merely multiplying different worst-case resource witnesses.

**Model transfer firewall:** An indexed-input implementation checks the rigid equality family in O(L polylog L) time and O(log L) work/index cells, bypassing complete source sweeps. Standard arbitrary computations can also reread, copy or reencode the source without the prescribed p-phase structure. Prior LSPV-5/167 crossing sequences are acknowledged; no unrestricted theorem or novelty in equality/communication complexity claimed. Known FLMV near-linear SAT exclusions do not remove an arbitrary polynomial exponent. No P != NP claim.

**Executable and immutable raw:** experiments/tmr/tmr3_multipass_equal3_tradeoff.cjs and results/raw/tmr/2026-11-13_1328_TMR3_MULTIPASS_EQUAL3_RAW.json. Original GitHub readback of code reran in V8: all 1,364 E(a,b), 6,372 batch checks, 258 positive transcript checks, 516 four-sign-bit flips, 20 n<=2 full SAT brute checks, 37,263 assertions PASS. Virtual streaming emulator, not physical native TM instructions. Node CLI/preflight/checker not run.

**Peer tasks:** TMR-1 audit quantifiers and strict-class transfer. TMR-2 investigate an information-cost beyond input reads still necessary with arbitrary replay and compact summaries. TMR-4 instantiate a simulation that includes every two-way head move, work-copy and state conversion. **TMR-5 independently falsify** same-input variable-length transcript injection/cost, completed-sweep assumption, and duplication against LSPV-5/167.

**Canonical records:** Root proof1/proof2 fully read (the latter recovered from Git blob), root main.tex fully read by blob; TMR-3 has no authorized synthesis region yet. TRACKERS REVIEWED; NO MATERIAL CHANGE. No root manuscript or shared task edits.

**Next target:** test a two-way input-crossing protocol against actual copying, caching, compact algebra and alternative representations, retaining cost direction and same-input quantifiers; publish a concrete failing counterexample if unrestricted transfer is false.

END_OF_HANDOFF::TMR-3::2026-11-13_1335_PST


---

# TMR-3 latest handoff | 2026-11-13 14:34 PST | TWO-WAY-CROSSING-TRADEOFF002

**Superseding directive:** research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md. New TMR-3 under five-TMR replacement, no historical role/task revival. **P versus NP remains OPEN.**

**New CANDIDATE mathematical report, published/readback SHA f7664532b1ee57496d059aa2d793a55714de3907:** research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md.

**Verified executable, SHA 6ca3cd1385b7b29ee5dc4df9d156c18f9f77678b:** experiments/tmr/tmr3_twoway_crossing_splice002.cjs. **Verified immutable raw, SHA 873ebb331fd1e173e5170508db9a623439c2a78c:** results/raw/tmr/2026-11-13_1434_TMR3_TWOWAY_CROSSING_RAW.json.

**Exact stronger model-scope result pending TMR-5 review:** For EACH one fixed correct total deterministic 3-SAT machine A with ONE freely reversing sequential two-way read-only input head and any fixed finite number of charged work tapes, for all sufficiently large n there is ONE SAT diagonal E_n(a_n,a_n) from the original TMR-2 strict-proper-3CNF equality family for which SAME-TRACE time and space obey

$$
T_A(E_n(a_n,a_n))(S_A(E_n(a_n,a_n))+1)\ge c_A L(n)n
=\Omega_A(L(n)^2/\log L(n)).
$$

**Method:** No complete source sweeps required. At Theta(L) physically distinct cuts *inside the fixed-suffix first-half gadgets*, exact diagonal source splicing supplies 2^j different prefix choices with a fixed suffix and mixed UNSAT hybrid. Full controller/work-symbol/head crossing transcripts are injective conditional on suffix, self-delimiting codes have length <=D_A*q_c(S+1)+O_A(log(S+2)), and a short-code union bound selects a single diagonal simultaneously expensive on every cut. If S>=n on any diagonal, direct travel T>=L/2 already gives product. If S<n on all, sum crossing costs over all cuts. No different-input time/space borrowing, and physical two-way reversals, copying and recomputation are admitted.

**Tightness and barrier:** TMR-2/002 ONE fixed all-input correct machine has T=Theta(L), S=Theta(n) on this exact easy family, so product is O(Ln). This matches and caps the bound. Fully paid indexed-input random access can recognize/compare the same rigid family in O(L log^2 L) time, O(log L) space, so the theorem has NO random-access transfer. Occupancy S<=b(T+1) gives only T=Omega(L/sqrt(log L)), weaker than actual T>=L/2. This is a **sequential-head physical transport theorem**, not unavoidable superpolynomial global-consistency work.

**Scientific prior art:** Classical Hennie crossing sequences; Santhanam 2001; project LSPV-5/167 already proves crossing averages on a separate exact22 gap family; Claude ONETAPE-0001 documents SAT/off-line quadratic product bounds. Increment is removing TMR-3/001 complete-sweep restriction for the *original TMR-2 exact encoding*, not discovery of the general method.

**COMPUTATIONAL executed V8 source audit:** all 1,364 ordered n<=5 original signed E(a,b) formulas, 16 unit-gadget truth-table assertions, 71,520 exact syntactic source splices (63,888 unequal-prefix UNSAT hybrids), 408 cut positions; 0 failed. Tested finite source locality, NOT full physical machine simulation or asymptotic coding. OS Node, formal TM executor, LaTeX compilation and repository preflight unexecuted.

**Peer requests:** TMR-5 independently review conditional-suffix cut syntax, complete crossing config, self-delimiting variable-S code, same-input all-cut union bound, and T>=L/2; TMR-1 inspect exact one-head vs indexed model transfer and the fixed polynomial barrier; TMR-4 construct a cost-sound actual-step crossing abstraction without assuming any sweep phase; TMR-2 test proposed compulsory global-consistency operations against the one-sweep easy upper.

**Root state:** full proof1/proof2 reviewed, large proof2 and main.tex recovered by Git blob rather than reconstructed. TRACKERS REVIEWED; NO MATERIAL CHANGE. New TMR-3 main.tex region is authorized, but the status remains CANDIDATE pending TMR-5 and manuscript synthesis was left unchanged intentionally. No task or schedule changes.

**One next target:** find or falsify a compulsory operation cost that survives indexed input access, streaming/caching interleaving, compact algebra and unbounded polynomial workspace, not just the sequential geometry. P versus NP OPEN.

END_OF_HANDOFF::TMR-3::2026-11-13_1434_PST

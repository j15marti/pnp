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

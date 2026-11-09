# LSPV-1/536 five-role handoff | 2026-11-09 07:12 PST

**Route B | PROVED/RESTRICTED assumption counterexample; COMPUTATIONAL 59 finite controls | P versus NP OPEN.**

**Exact affected IDs:** [P2-L1-536] corrects the polynomial peak-space claim in [P2-L1-535], and qualifies [P2-L1-534] and [P2-B3]. No material Route A tracker change. Historical [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN.

**Lemma.** A time-only premise `T_G(B,n) <= (B+2)^c 2^{C f(n)}`, `f(n)=n(loglog(n+16))^d/(log(n+16))^alpha`, alpha,d fixed nonnegative, DOES NOT imply polynomial guest space. For any hypothetical correct G satisfying the time bound, G-star writes and holds `2^floor(sqrt(n))` scratch bits and then runs G. Because sqrt(n)=o(f(n)), it preserves the time-rate envelope but has superpolynomial peak scratch even for B=poly(n). A source family with all long binary identifiers can cause a residual n-variable guest call in the stated identifier-cut wrapper.

**Repair.** Keep the theorem's time-only transfer unchanged; replace the unsupported space conclusion by `S_A <= poly(N)+max S_G(poly(N),O(N/log N))`. Add `S_G(B,n)<=poly(B+n)` as an explicit additional premise for the polynomial-space conclusion. OpenAI's `openai/math/lean/docs/378.md` independently asserts polynomial visited tape cells for its *particular* canonical k-CNF machine, so that special-case space statement is still supportable subject to external checker/model transport. The change is a scope correction, not a contradiction of OpenAI's algorithm, Pang's restricted proof lower bounds, or B2's time-only conditional separation for a different calculus.

**Evidence:** `research/agents/lspv-1/2026-11-09_0712_LSPV1_GUEST_SPACE_FIREWALL536.md`; code `experiments/arc/lspv1_536_guest_space_firewall.py`; raw `results/raw/arc/2026-11-09_0712_LSPV1_536_GUEST_SPACE_FIREWALL_RAW.json`. Executed Python 59 assertions, six SAT/UNSAT small controls, five malformed rejection controls, 21 formula-resource scenarios. Large-bit scratch costs are symbolic, not physically allocated. External guest not executed.

**Tasks:** LSPV-3 check native accepted-byte inference grammar and source authentication, not an ER2 surrogate. LSPV-5 red-team G-star quantifiers and keep B3 separate. LSPV-2/4 do not carry this into the same-FLMV-machine recursion without proving stronger guest space and applicability constraints. Maintain 2 Route A/3 Route B roles and schedules, historical R_mix341 grammar and weights, P versus NP OPEN.

Root main.tex content fetch returned zero bytes twice; unchanged for safety.

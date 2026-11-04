# LSPV-4/375: Logspace streaming recoding with paid guest-input access
**November 3, 2026, 19:36 PST. PROVED/EXACT scoped bit-cost transducer; finite tests COMPUTATIONAL; external specialist review pending. Full Rmix341 B1/B2/B3 and P versus NP OPEN.**

Haken (1985) proves that every unrestricted ordinary shared-DAG Resolution refutation of canonical unary PHP with h+1 pigeons and h holes requires 2^{Omega(h)} lines, on an explicit ASCII DIMACS source of length N=Theta(h^3 log h). This is NOT an Extended Resolution, Res(XOR), full Rmix341 or unrestricted decision-time bound. Cook polynomial ER proofs and linear mixed GF(2) odd-Tseitin proofs remain mandatory countercontrols.

**Prior result credited:** LSPV-2/377, research/agents/lspv-2/2026-11-03_1909_LSPV-2_LENGTH_PRESERVING_INVOLUTION377.md, blob a198a87cf349ae002a5d845a9491c7dffda03d68, established one fixed uniform, length-preserving, SAT-label-preserving involution E exchanging hard canonical PHP and same-length contradictory-unit CNFs; previous bound O(N^2) time, O(N) writable space.

**New resource sharpening for the SAME E:** one fixed deterministic logspace transducer using a charged read-only input, charged index/head operations and append-only **unreadable** output satisfies

$$
T_E(N)=O(N\log^4(N+2)), \qquad S_E(N)=O(\log(N+2)).
$$

Binary search finds candidate source lengths via capped on-the-fly generation, comparing both streams and emitting exactly N output bits, with no full writable intermediate. For Q random-access queries by a downstream guest, a paid lazy accessor uses O(log N) additional writable bits and O(N log^4 N + Q N log^2 N) work. An explicit N-bit writable transformed-input copy instead forces Omega(N) peak writable bits in that implementation, so rho>=1 in the all-phase envelope. The write-only output tape is not free guest read-only storage.

The corollary is scoped: an invariant I <= W_Resolution that is unchanged by every uniform low-space, near-linear-time, label-preserving length-preserving bijection has I(PHP_h)<=1, because the swapped unit source has one-step Resolution contradiction. This rules out *uncharged* representation invariance as a way of importing Haken, not a source-authenticated conversion-charged invariant. No Rmix341 proof rule was added, no superpolynomial full mixed lower bound or B3 follows.

F1 linear writable space necessary for the fixed recoder: FALSIFIED. F2 invariance of ordinary Resolution minima under this recoding: FALSIFIED. F3 free guest random access from streaming output: FALSIFIED. F4 full mixed B3 bridge: OPEN.

Readback tests: primary program 130 assertions on h=1..8, 16 original sources, eight round trips, 64 lazy byte requests, 10 nonmatching/malformed binary controls, exhaustive PHP labels for h<=3, odd/even K4 Tseitin 0/8. Independent referee 112 assertions, 16 swaps, 48 lazy byte checks. Host test buffers are not a Turing-machine writable-space measurement.

Located and examined Grok: GROKPROOF/2026-11-03_1912PST_PROGRESS.md (blob 66576e88) and GROKPROOF/2026-11-04_0116_PROGRESS.md (ca5a8353). Both still leave fully charged arbitrary-A transformation OPEN. Claude: research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6), 2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727), September 30 BOOL review (694c1c81). Their restrictions do not establish B3. Reviewed November 2 12:04 five-role handoff, issue #3, AGENTS.md, CODEX.md and pnp-research skill; LSPV-4/347 and /373 and LSPV-3/377 are credited. A search of github.com/openai returned only unrelated generic logic artifacts. No assertion of absence.

Full local-checkout preflight unavailable due container/Python infrastructure errors. Root main.tex fetch returned zero body with nonempty blob SHA 7beb6b48, preventing ownership-safe reconciliation; root unchanged. No task, schedule or rule change.

FORMAL REPORT: research/agents/lspv-4/2026-11-03_1936_LSPV-4_STREAM_LAZY_INVOLUTION375.tex
CODE: experiments/arc/lspv4_375_lazy_involution_stream.js
INDEPENDENT REFEREE: experiments/arc/lspv4_375_independent_verify.js
RAW: results/raw/arc/2026-11-03_1936_LSPV4_STREAM_LAZY_INVOLUTION375.json

NEXT: a source-provenance-preserving, fully cost-reflecting invariant under ALL permitted fixed mixed rules, followed independently by the B3 implication SAT in P => Wbar_Rmix341 polynomial. B1/B2/B3, superpolynomial full-mixed minima and P versus NP OPEN.

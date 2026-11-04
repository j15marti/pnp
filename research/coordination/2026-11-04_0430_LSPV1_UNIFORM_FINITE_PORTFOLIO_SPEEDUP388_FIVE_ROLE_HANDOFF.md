# LSPV-1/388 five-role handoff: uniform finite-portfolio speedup firewall

**2026-11-04 04:30 PST.** **KNOWN THEOREM** Blum (1967); **PROVED/EXACT DERIVED** all-binary prefix-worst-case finite-portfolio corollary for one *other* decidable language, pending independent mathematical audit; **COMPUTATIONAL** finite toy ledger; **OPEN** B1/B2/B3, full mixed-calculus superpolynomial lower bound and P versus NP.

## One precise result

By Blum's speedup theorem, fix **one** total recursive binary predicate f for the recursive bound r(n,t)=2^(n+t+10). Let L_f classify canonical binary integer strings as YES/NO according to f and reject noncanonical leading-zero or empty strings as MALFORMED. In a fixed acceptable deterministic multitape time model, for *each finite portfolio* of uniform total exact deciders A_1,...,A_k for this **same** all-binary language, there is **one** further uniform total exact decider B and N0 such that **for every N>=N0**, with T_A^wc(N)=max_{|x|<=N}T_A(x) over all binary strings, T_B^wc(N) < min_i T_Ai^wc(N). There is also pointwise eventual domination on every canonical integer input. Construct one uniform racer P; standard fixed-program dovetailing uses a polynomial in input length plus minimum portfolio runtime. Blum produces a uniformly correct J with T_P(n)>2^(n+T_J(n)+10) for all large n; exponential beats the race polynomial. Wrap J with constant-time malformed-prefix rejection, then derive the worst-case-prefix inequality by maximizing the unbounded B runtime on canonical inputs. This is a **known-theorem corollary**, not a new lower-bound technique or SAT result.

**Difference from LSPV-1/377 and /382:** those are nonuniform size-wise or per-instance optimizers. Here all competitors, including the improving B, are fixed uniform total machines. **Difference from LSPV-2/373:** that establishes representation-relative h-versus-one parity-charge query depth on a promised Tseitin charge record, not no-optimal-uniform-decider for a Blum language.

**Certified hard-family firewall:** Haken PHP lower bound is for all ordinary shared-DAG Resolution proofs of canonical unary PHP with N_h=Theta(h^3 log h) signed binary-index bits, 2^(Omega(h)) lines, not arbitrary algorithms; Cook polynomial ER proofs and R_mix341 GF(2) odd-Tseitin escapes block unrestricted transfer.

## Three exact falsifiers and the next division of labor

F1: Generic 'there is always one fastest uniform solver of a decidable problem' is **FALSIFIED** via Blum and the finite-portfolio corollary. F2: Whether **SAT** itself has this property is **OPEN**; neither universal SAT hardness nor B3 follows. F3: Whether proof-node cost itself becomes uniform machine time after normalizing evidence bits is **OPEN** for full R_mix341. The fixed calculus is unchanged and carries unit cost per authenticated binary-premise node, with uncertain full LOCAL-CONVERT export grammar.

- **LSPV-1:** continue B3 and exact quantifier discipline. Test whether the polynomial proof-budget normalization plus any genuine trace/reflection result yields more than a conditional reformulation.
- **LSPV-2:** authenticate the original LOCAL-CONVERT proof grammar, specifically whether a private gate may become independently accessible without a paid DEF. Keep original R_mix341 semantics, no revised calculus.
- **LSPV-3:** inspect whether any proposed signed-hypergraph/DAG invariant depends on selecting a fastest uniform policy, and whether any robust post-source-acquisition work floor survives adaptive GF(2), ER and lazy-circuit shortcuts.
- **LSPV-4:** separately charge every race, conversion and output, and verify the all-binary worst-case prefix definition; no transfer of non-SAT speedup or Blum running time to FLMV T/S.
- **LSPV-5:** attack the Blum-to-binary wrapper, racing polynomial and eventual worst-case inference; reject any claim that SAT lacks optimal deciders or that an externally optimal DAG gives a physical lower bound.

## Review and artifacts

Reviewed actual **GROKPROOF/2026-11-04_1217_PROGRESS.md** (blob cae0560d2e4f8c243da802c1d5d48ebf32bedd5c): still missing charged all-input ARC transfer, cut-width claims restricted. Reviewed actual **research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex** (blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a): one-tape lower bound is nonseparating and model-specific. Also reviewed LSPV-1/386, /387; LSPV-2/341 and /373; Red Team/334; directive, issue #3, AGENTS.md, CODEX.md and the repository skill. Primary proof: Blum, J. ACM 14(2) (1967), Theorem 5, DOI 10.1145/321386.321395. Searches found no directly applicable github.com/openai SAT proof translator. Duplicate general 'no fastest algorithm' as Blum 1967 is **credited as KNOWN**, not claimed newly discovered.

- [Formal proof](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-04_0430_LSPV-1_UNIFORM_FINITE_PORTFOLIO_SPEEDUP_FIREWALL388.tex)
- [Toy producer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_388_portfolio_guard.py)
- [Independent Node checker](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_388_independent_verify.js)
- [Raw toy ledger](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-04_0430_LSPV1_UNIFORM_PORTFOLIO_SPEEDUP388_toy.json): 511 strings, 128 YES / 128 NO / 255 MALFORMED, 3,046 Python assertions; 44 independent Node checks on the locally constructed counterpart. Toy checks do not prove Blum.

No task IDs, hourly schedules, enabled states or rule weights changed. The next substantive P-vs-NP milestone remains **fully charged legal trace-to-preselected-R B3 or a genuine obstruction**, plus independent superpolynomial mixed Wbar. P versus NP **OPEN**.

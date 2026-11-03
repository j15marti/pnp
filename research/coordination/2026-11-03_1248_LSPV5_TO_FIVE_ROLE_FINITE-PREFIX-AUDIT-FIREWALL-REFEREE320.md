# LSPV-5 to five-role handoff: FINITE-PREFIX-AUDIT-FIREWALL-REFEREE320

**November 3, 2026, 12:48 PST · PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` unchanged**

Established bound first: Braun reports `L_⊕(B_ell)>exp(n/(32768 ell^2))` for unrestricted shared-DAG Res(⊕) bit-PHP, `n=2^ell`, `ell>=32`, but current LSPV-1/2/3 backtranslations cover proper fragments only. Full circuit-valued `LOCAL-CONVERT`/extension escapes and B3 remain open.

**PROVED/EXACT finite-prefix firewall.** For every total correct decider `A` and every finite cutoff `N`, choose a valid SAT positive-unit CNF `S_N` longer than `N` and define `A_N(x)=UNSAT` on exactly `S_N`, otherwise `A(x)`. Then `A_N` agrees with `A` on **every** binary string of length at most `N`, including malformed encodings, has only linear comparison overhead, but is globally incorrect. Therefore bounded black-box tests and finitely many bounded reflection instances cannot themselves establish the all-length correctness premise needed by B3.

This does not rule out a finite symbolic proof of a universal correctness theorem. `A_N` is incorrect, so it refutes none of B1/B2/B3. It blocks only the promotion of bounded evidence to a global premise.

Controls: all 255 nonempty subsets of the eight complete three-variable clauses (254 SAT/1 UNSAT), cutoffs 32--256 bytes with explicit SAT exceptions, twelve malformed cases, odd/even K4 Tseitin 0/8 models, and 54 independent Node assertions. Raw SHA-256 `bceb725369de3d7f4ca374df3c120c3b1d9e5ca9ec2399ac24d690c1eee7d709`.

Actual Grok/Claude paths reviewed: `GROKPROOF/2026-11-03_1912_PROGRESS.md` blob `dbec4959...`; `GROKPROOF/2026-11-03_1217_PROGRESS.md` blob `acf9fbee...`; `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727...`; `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`; and Claude 0266 review blob `694c1c81...`. None proves B3.

Artifacts:

- `research/main/2026-11-03_1248_MAIN_FINITE-PREFIX-AUDIT-FIREWALL-REFEREE320.md`
- `experiments/arc/lspv5_320/finite_audit_firewall_referee320.py`
- `experiments/arc/lspv5_320/verify_finite_audit_firewall_referee320.js`
- `results/raw/arc/lspv5_320/finite_audit_firewall_referee320.json`

Root `main.tex` reconciliation is pending because the path API returned empty content with nonempty current SHA; do not overwrite it from that incomplete response. Next: obtain a full blob read and reconcile the executive synthesis, then seek a uniform all-length noncircular B3 correctness/reflection theorem. B1/B2/B3, superpolynomial full `Wbar_Rmix341`, and P versus NP remain OPEN.

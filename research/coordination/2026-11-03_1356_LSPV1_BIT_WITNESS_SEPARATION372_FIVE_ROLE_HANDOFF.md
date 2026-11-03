# LSPV-1 BIT-WITNESS-SEPARATION372: five-role transfer handoff

**November 3, 2026, 13:56 PST, America/Los_Angeles.** Existing LSPV-1 ownership, all schedules, enabled states, titles, rules and weights unchanged. The shared Rmix341 worst-case lower bound, B1/B2/B3 and P versus NP remain OPEN.

## Starting known result and precise new scoped results

Haken (1985) proves: for sufficiently large h, every unrestricted shared-DAG ordinary Resolution refutation of the standard unary PHP_(h+1)^h, with n=h(h+1) variables, m=(h+1)+h*binom(h+1,2) clauses and signed ASCII DIMACS length N=Theta(h^3 log h), requires at least 2^(c h) lines. This is restricted proof hardness, not arbitrary SAT computation hardness. Known polynomial Extended Resolution/Frege PHP shortcuts block direct transfer to the unchanged Rmix341.

**PROVED/EXACT, general bit-certification lemma:** For every fixed polynomial-time-in-evidence verifier V, conditional on SAT in P a uniform algorithm outputs a shortest *encoded-bit-length* UNSAT certificate in (N+ell_V(F)+2)^O(1) time, without receiving a budget. This uses unary bounded NP search, doubling, binary length search and prefix self-reduction. It extends LSPV-1 Result 365 beyond ER2's node-normalized syntax, but does NOT show polynomial (N+q) time for the minimum paid-node optimum q. The full Rmix341 LOCAL-CONVERT grammar and polynomial-bit-checker need a separate exact audit; SAT in P could make explicit circuit-implication checks easy without shortening payloads.

**PROVED/EXACT, methodological fixed-system countermodel (NOT an addition to Rmix341):** Define R_table with unit-paid strict Resolution plus binary-premise TAB-AND. A TAB-AND has two authenticated operands and outputs its full explicit 2^n-bit conjunction truth table over the source variables; no compact substitute is allowed. A deterministic rowwise checker takes polynomial time in the written evidence bits. PHP is clause-minimally UNSAT, so the source-arity argument gives q>=m-1; sequentially conjoining its m clauses attains q=m-1. Haken excludes a Resolution-only q=m-1 proof for sufficiently large h, so every node-optimal R_table proof has at least one TAB-AND node and must explicitly write 2^(h(h+1)) truth bits. Consequently no machine producing node-optimal R_table proofs can run in polynomial time in N+q, regardless of SAT in P. The toy remains sound/complete/effective, with Wbar_table(N)<=N, so its B3 is trivially true. This is a *representation/normalization separation*, not hardness of the project's full calculus.

## Controls, reproducibility and limitations

**COMPUTATIONAL:** Deterministic Python producer passed 143 assertions on PHP h=1,2,3 with (n,m,q)=(2,3,2),(6,9,8),(12,22,21), all 34 source-deletion SAT witnesses, 70 signed occurrence-flip SAT repairs, 8/512/86016 semantic table-bit entries, odd/even K4 parity 0/8 SAT models, 2SAT both labels, malformed and corrupted proof rejection. Independently implemented Node verifier passed 86,678 assertions, including all 86,016 truth entries in the h=3 transcript.

**Physical-memory firewall:** The producer/checker store each semantic truth bit in one host BYTE, not as a physically packed bit. Thus 86,016 logical truth bits occupy at least 86,016 bytes of host array storage, excluding runtime/allocator overhead. No FLMV memory upper bound is claimed.

Exact role-owned artifacts:
- Formal report: research/agents/lspv-1/2026-11-03_1356_LSPV-1_BIT_WITNESS_SEPARATION372.tex
- Producer: experiments/arc/lspv1_372_bit_witness_separation.py
- Independent verifier: experiments/arc/lspv1_372_independent_verify.js
- Producer raw: results/raw/arc/2026-11-03_1356_LSPV1_BIT_WITNESS_SEPARATION372.json
- Independent ledger: results/raw/arc/2026-11-03_1356_LSPV1_BIT_WITNESS_SEPARATION372_independent.json

## Duplication, independent assessments and coordination

Shared directive, issue #3, AGENTS.md, CODEX.md and repo skill reviewed. Compared original LSPV-1 reports 365/371, LSPV-4 LOCAL-CONVERT-CVP363, LSPV-5 LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315 and TRANSFER-CEILING-REFEREE321. REFEREE315 already shows constant paid-node count with large circuit payload under conditional syntax U; this result adds **a forced exponential written payload for every node-optimal proof of a published Haken-hard source**, in a distinct fixed toy calculus. No claimed external academic novelty.

Read actual repository paths GROKPROOF/2026-11-03_2114_PROGRESS.md (blob 4996f04756634904b4d1439911f1ef2d04e5aefb), research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex (d06a2d56), research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727), and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Grok's universal all-input FLMV contraction remains OPEN, and Claude's portfolio and crossing-sequence results retain their restricted models. None proves B3 or the missing evidence normal form. Also searched Haken 1985, Cook--Reckhow 1979, Buss 1987, Braun 2026, and github.com/openai verifier implementations; no matching project OpenAI verifier was adopted. Local Git checkout preflight could not run; container DNS could not resolve raw.githubusercontent.com, but authenticated GitHub connector readback and local experiments succeeded.

## Exact next arrows by specialist

LSPV-1: B3 still needs an independent nonrelativizing theorem from SAT in P to polynomial Wbar_Rmix341; do not equate bit-optimal extraction with polynomial node-cost or proof size.

LSPV-2: Pin down real LOCAL-CONVERT internal wire and payload semantics. Test polynomial encoded-evidence normalization against the unchanged rules, not the artificial TAB-AND toy.

LSPV-3: Any lower-bound invariant must survive full adaptive GF(2), paid extensions and LOCAL-CONVERT. Treat PHP and Tseitin shortcuts as countercontrols, not targets for new random formula generation.

LSPV-4: Keep logical truth-vector bits distinct from host bytes and from peak FLMV machine space; audit all phases, parsing, output and memoization.

LSPV-5: Independently red-team the binary-DAG source-arity proof, the all-node-optima forced-bit claim, and especially whether Rmix341's actual syntax has a corresponding normalization obstruction.

**Status: Full mixed Wbar superpolynomial lower bound OPEN; B1/B2/B3 OPEN; P versus NP OPEN.**

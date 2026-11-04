# LSPV-2 PARITY-PORT-COMPRESSION374 | Five-role handoff

**November 3, 2026, 16:44 PST.** Established prior hard-family context, no new hard-instance search. **PROVED/EXACT symbolic scoped construction**, **COMPUTATIONAL independently verified finite instances**, external specialist review pending. **P versus NP remains OPEN.** Rmix341, task identity, state, schedule, role ownership and weights unchanged.

## Exact result, with duplication firewall

Published Urquhart (JACM 1987) and Ben-Sasson--Wigderson (JACM 2001) give exponential lower bounds on **ordinary unrestricted DAG Resolution** for suitable odd expander Tseitin CNFs, using bounded-degree signed graph sources of encoded length Theta(h log h), not unrestricted SAT machines. Mandatory negative control: LSPV-2/341 proves exact W_Rmix341 = 4h−1 for odd connected bridgeless cubic Tseitin because XOR/GF(2) shortcuts are legal. No such lower bound transfers to the mixed calculus.

**Prior result:** LSPV-2/344 (blob f5949c8b2803a0a7c556b8b894eb16043153058e) already establishes the exact global 2^k−1 mixed optimum for the complete 2^k-clause assignment-blocker CNF F_k. We independently reverified but make no novelty claim for that count.

**New explicit witness:** Partition F_k into two *nonconstant* parity ports P_{k,0}(X), P_{k,1}(X). For each k>=2 construct private, conservative XOR2 circuit rails G_{k,0}(X,A), G_{k,1}(X,B), sharing only the k boundary input variables. Each gate is authenticated by four original proper width-three CNF clauses, with two distinctly labelled final unit clauses per rail. Each side individually has exactly the same projected boundary relation as the corresponding explicit parity port for every x assignment. Their combined source is UNSAT and has **3k−2 variables, 8k−4 clauses and a fully checkable mixed refutation of 8k−5 paid AND3/GF(2) nodes**. No unit source-to-row conversion is free: its two actual source clauses are conjoined by one paid AND3. Thus the proof-cost gap is exponential in k, but original N_F=Theta(k2^k log k) versus compact N_G=Theta(k log k). It is not a superpolynomial lower bound measured against N_F.

**Physical compiler:** A fixed uniform checker scans all k2^k source literal occurrences, marks the 2^k excluded assignments, rejects duplicates/missing/malformed records and then produces the compact circuit. It uses polynomial time and space in the *huge explicit input* N_F, not in the compact length N_G. The reverse explicit expansion costs Omega(N_F) output bits. A mathematical index oracle for the jth blocker runs in poly(k) work per clause and can expose the symbolic 2^64-clause object without materializing it; this is not a free original CNF source in Rmix341. No claim of polynomial **bidirectional** conversion measured relative to the small input.

**Invariant implication:** A scalar invariant preserved by *portwise existential boundary equivalence*, and lower-bounding source minimum W_R on every explicit presentation, cannot exceed 8k−5 on the expanded source F_k. This is a concrete two-nonconstant-port elaboration of the older LSPV-5/323 semantic quotient collapse, **not** a denial that a fully source- and provenance-sensitive, conversion-charged invariant could exist.

## Controls and work

Python producer + separately authored no-import Node verifier: 15 certificate fixtures (8 full blockers and 7 compact pairs), **107,113** independent assertions; **510** single-source deletion SAT witnesses, **510** parity-side SAT witnesses, seven same-charge SAT models; five corrupted certificates and five malformed records rejected. k=8: full source 256 clauses/255 exactly minimal paid nodes/45,152 DIMACS bits; compact source 60 clauses/59 paid upper nodes/5,296 bits. k=64: two indexed lazy clauses verified, no materialized 2^64 array. Full local proof dataset 75,945 bytes SHA256 e99d7533294d1cbf73a3c238ef6a39c072cb961d224cf390989b5eb61179b9de; the public repository JSON is a ledger, **not** complete certificates. Full producer, independently written checker and dataset are in the reproducibility ZIP delivered in this run. Observed host RSS/time are not FLMV machine exponents; charge bit access, output, intermediate materialization, caches, proof verification and all phases of peak memory.

Four falsifiers: false portwise equivalence, uncharged source-to-GF2 coercion, free large virtual-source materialization, corrupted proof acceptance. All addressed within their explicitly declared scope. G_k has an **upper certificate only**, not a certified mixed optimum. B1/B2/B3 remain OPEN.

## Mandatory Grok/Claude and peer checks

Actual Grok path: GROKPROOF/2026-11-03_2214_PROGRESS.md, blob 59fe73c20473bd6bc20500cf58d75e42519aee88. Universal all-input charged ARC contraction remains OPEN; no B3 theorem. Actual Claude path: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67. Quantitative TPORT bounds and the barrier are within its alternation-trading proof framework, not unrestricted SAT. Independently reviewed LSPV-1/374 (certified Resolution source splice), LSPV-3/378 (source-tag/original-support issue), LSPV-4/372 (sharing versus dependency walks) and LSPV-5/323 (semantic quotient and nonuniform per-input algorithm minimum). No one supplies an Rmix341-complete source-sensitive invariant or B3.

Search of original project corpus found the exact blocker optimum in LSPV-2/344 and the general quotient no-go in LSPV-5/323. Search of github.com/openai for matching proof checker/XOR certificate code returned no model-matched implementation; unrelated results are not proof of novelty. Primary references and actual model/quantifiers are recorded in the report.

## Outbox, strict scope and next arrow

- research/agents/lspv-2/2026-11-03_1644_LSPV-2_PARITY_PORT_COMPRESSION374.tex
- experiments/arc/lspv2_374_parity_ports_public.py
- results/raw/arc/2026-11-03_1644_LSPV2_PARITY_PORT_COMPRESSION374_public.json
- research/coordination/2026-11-03_1644_LSPV2_PARITY_PORT_COMPRESSION374_FIVE_ROLE_HANDOFF.md

The current specialist priority is to formalize **charged source-authenticated bidirectional proof transport** with typed original-variable support, and test each alleged intrinsic cost invariant against both compact port rails and large explicit blockers, including exponential intermediate representations and their actual bit costs. Even a robust invariant of logical paid nodes does not automatically dominate unrestricted physical SAT time. The B3 implication SAT in P => polynomially bounded worst-case W_Rmix341 remains OPEN. No user-approved tasks or schedules changed. **P versus NP remains OPEN.**


## Publication reconciliation and issue confirmation

The four above role-owned files were individually fetched after publication with complete content and nonempty blob SHAs. Root main.tex was fetched at old blob c5c0df71c282439dda4ab8638f3ad40424ac471d; contents API returned zero body but authenticated Git-blob fetch recovered all 1,513,363 characters. An exact 2,122-character update was inserted solely before the unique END LSPV-2 OWNED marker. GitHub root update commit 783c5c085e5a862eb577f08570fe26488a35a61f produced blob 41bdb641f441ca2f0b4555ecc00496bef80415b0. Complete new 1,515,485-character readback was byte-identical to the intended result, and deleting only the new insertion recovered every character of the original. Coordination issue #3 comment 6619628188 was independently fetched. No authorized markers or outside bytes were modified.

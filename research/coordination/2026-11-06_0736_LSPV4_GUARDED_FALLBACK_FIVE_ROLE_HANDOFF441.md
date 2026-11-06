# LSPV-4/441 five-role handoff | 2026-11-06 07:36 PST

**Allocation preserved: LSPV-2 and LSPV-4 Route A; LSPV-1, LSPV-3, LSPV-5 Route B. P versus NP OPEN.** No other research task, title, timezone, cadence, enabled state, ownership marker or historical R_mix341 rule/weight was changed.

## Result for Route A

**CONDITIONAL/PROVED-RESTRICTED.** Assume SAT is in P, with fixed total correct uniform polynomial decider B. For any arbitrary large integer d exceeding B's time exponent, pad B with n^d counted transitions to get another total correct polynomial SAT decider A_d. A fixed guarded fast-path compiler that on infinitely many inputs calls this **unchanged guest** on the complete original n-bit input has time exponent t'>=d, contradicting the target t'<=max(11/10,3/5+d/2). This falsifies only the guarded full-length black-box fallback architecture, not the existence of other universal compilers and not P=NP.

More generally, for answer-only black-box query geometry consisting of at least N^(mu-o(1)) **actually executed sequential** guest calls of length at least N^(lambda-o(1)), the padded guest forces t'>=mu+lambda*d. Because the target must hold for every arbitrarily large padded d, **lambda<=1/2 is necessary**. Workspace padding to touch n^s cells yields the same slope necessity for s'<=max(1/2,s/2). Nominal repeated children, legal memoization, shared proof DAGs and early SAT stopping are NOT automatically counted as distinct guest calls.

## Established source, adversarial controls and shortcuts

The unchanged LSPV-4/440 Hamiltonian cubic Tseitin proper 3-CNF source has 4H clauses, 3H/2 variables, and N=12H(w+1)+H+w+12 bits, w=floor(log2 H^2)+1. Published exponential **ordinary Resolution** lower bounds for suitable odd-charge cubic expanders (Urquhart 1987) do NOT imply mixed-calculus or arbitrary-machine hardness. The authenticated GF(2) total-charge parity shortcut remains a legal efficient upper control. LSPV-2/441 already gives a general canonical cubic Tseitin standard-logspace recognizer; do not duplicate or overstate its machine-time scope.

The old 440 packet recognizer rejects 28/28 clause-permuted packets despite perfect signed clause-multiset identity, including 12 SAT and 16 UNSAT fixture pairs; the canonical grammar is intentionally stricter than formula semantics. Python host producer and independent Node replay executed; 25,242 independent assertions passed. Published Node compact replay of one exact UNSAT source fixture executed locally: 57 checks PASS. Full 28-record raw fixture dataset and source scripts remain in the conversation ZIP; GitHub holds the audit report, executable compact control and raw summary with one signed source/permutation fixture.

## Immediate peer assignments

**LSPV-2:** On every candidate universal contraction, test the nonfamily path against arbitrary padded A_{d,s}. Record executed guest query sizes and count, prefilter overhead, malformed status and both-label join, whether the program code is modified, and whether cache or repetition invalidates nominal fanout. Produce an actual all-input shrinking guest input, not merely a sparse port or recognized family parity shortcut.

**LSPV-1/LSPV-3/LSPV-5:** This call-cost theorem is not a mixed proof-size theorem or noncircular B3. Continue the full fixed native shared-DAG minimum with AND cases, context legality, exact weights, Resolution vs ER/GF(2) shortcuts, and source authenticated certificates; avoid importing a black-box runtime claim into ideal proof work.

## Audit, publication, blocker

Report: research/agents/lspv-4/2026-11-06_0736_LSPV4_GUARDED_FALLBACK_BLACKBOX441.md.
Executable: experiments/arc/lspv4_441_guarded_fallback_check.mjs.
Raw summary: results/raw/arc/2026-11-06_0736_LSPV4_441_GUARDED_FALLBACK_SUMMARY.json.
The complete locally executed archive has producer, independent referee, complete raw records, report and SHA-256 manifest.

Source audit: governing historical handoff blob 033b54b8; issue #3; actual LSPV-2/439 and /441, LSPV-4/440, LSPV-5 REFEREE387, current Grok, Claude TPORT-0002, konard finite one-tape model, blkph0x incomplete residual quotient, CNFgen Tseitin generator, FRAT-XOR checker and openai/math costed driver were read. External primary literature consulted; no claim of Google-branded search or external code execution.

Root main.tex authenticated fetch returned SHA 6a6a2349 but zero readable bytes and was left untouched. Full repository preflight/CI unavailable without a complete checkout; local Python, Node and archive integrity tests passed. The remaining OPEN arrow is a uniform all-input recursively iterable same-machine SAT transformation with genuinely N^(1/2+o(1))-sized guest problems, charged policy search, child construction/retrieval, all branching and joins, and peak space. P versus NP OPEN.

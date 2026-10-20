# COMPACTSTRATEGY1: next-arrow note after SHORTCHALLENGE1 (hourly scheduled run)

Date: 2026-10-21
Status: CANDIDATE / KNOWN-THEOREM bookkeeping only. P vs NP remains OPEN. No new separation claimed.

## Corpus reviewed (this run)
Branch head c00f6467 (SHORTCHALLENGE1), LOW-SIDE-ORBIT-COLLAPSE29, root main.tex executive box, tasks/ list, research/review/spines. Not a full corpus reconciliation; main.tex was NOT edited (this note is a scheduled-run side note, not an LSPV ownership-region update).

## Recent progress (since previous hourly check)
- SHORTCHALLENGE1 (PROVED, standard model): QBF with q = O(log N) universal bits, any alternation, is in NP via strategy unrolling (2^q poly(N) size).
- LOW-SIDE-ORBIT-COLLAPSE29 synthesis/audit/ledger and two independent Grok 4.7 review annotations; all keep status OPEN.

## Gap identified
SHORTCHALLENGE1 charges the *table* of a strategy. For q = omega(log N) the table is exponential, but this is a representation cost, not a lower bound (identity game: linear-size circuit, 2^(r+1)-2 table).

## Proposed next arrow (CANDIDATE)
Compact-strategy relaxation: replace "Skolem table" by "Skolem circuits of size <= s(N)" for each existential variable.
- Language Q_s = { Phi : exists circuits C_e (|C_e|<=s) forall beta: V(beta, C(beta)) = 1 }. This is in Sigma_2^P by definition (KNOWN, trivial), and truth of Phi is implied by membership (soundness) but not conversely unless Phi has small strategies.
- Completeness direction needs: true QBFs from the hash/iterated-challenge family have poly-size strategies. This is exactly where adversarial-history dependence matters; if strategies need superpolynomial circuits the family is not in this relaxation.
- Barrier audit: any statement "no poly-size strategy exists" for an explicit NP-verifiable family is a circuit lower bound for a PSPACE-ish/Sigma_2 object; Karp-Lipton (NP in P/poly => PH = Sigma_2) and Cai-Watanabe-type results are the known frame. Classification: ANALOGY needing a new bridge; no EXACT transfer.
- Transfer domain checked: control theory (causal strategies = causal/nonanticipative controllers; q-bit memory = observability horizon). Misleading as proof: finite-horizon controller synthesis is exactly the QBF unrolling already used. FAILED TRANSFER for lower bounds.

## Concrete test to run next (not run here)
For the roundwise identity-style games and one non-trivial predicate (e.g. forall y exists z with z = parity-masked hash of y_{<i}), compute minimal strategy circuit size by SAT-based exact synthesis for r = 1..5 and compare with 2^(r+1)-2 table size; any family with measured growth faster than polynomial in r is a candidate witness family (COMPUTATIONAL only, never a proof).

## Status
OPEN. One OPEN load-bearing arrow (unconditional superpolynomial lower bound for all algorithms) remains.

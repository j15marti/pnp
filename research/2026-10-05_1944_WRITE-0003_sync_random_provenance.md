# WRITE-0003 — synchronization and causal-random-provenance audit

**Agent:** WRITE  
**P vs NP:** OPEN  
**Status:** RECORDING / REPAIR

## Audit
Current main2.tex and main3.tex still omit LEAD-0001 GLOBAL-INTENSIONAL-GATE1 and PROOF-0001 RESTRICTED-ACCESS-ELIMINATION1. PROOF-0002 and RED-0001 have only write-status stubs; no substantive RESEARCH-0001 report was located.

## Existing exact/candidate status
- RESTRICTED-ACCESS-ELIMINATION1: PROVED/EXACT only in its stated deterministic compiler model. It is not arbitrary-algorithm extraction and is not the nonrelativizing/nonalgebrizing hinge.
- GLOBAL-INTENSIONAL-GATE1: CANDIDATE.

## External random-bitstream audit
Repository search recovered the earlier Search-G IID fair-bitstream/precommitment line. Existing hostile controls REACQ1, RANDCLOSE1, TRACECLOSE1, STRATFLAT1/LEGALFLAT1, and PH-PROV-CLOSE/PH-absorption show that fresh future bits or causal provenance alone do not force superpolynomial acquisition. They can force causal order and block challenge-specific precomputation, but a polynomial evaluator/selector may still wait for each fresh block and answer afterward.

Current status: **CANDIDATE / DIAGNOSTIC ONLY**.

The sharpened live target is an **unavoidable post-revelation-work theorem**: after each fresh random revelation, prove that every legal ordinary realization must perform new work that cannot be compressed into a polynomial evaluator, selector, fixed-PH response relation, memoized replay, or ordinary rerun. This theorem is OPEN.

## Failed repair
WRITE retried a main2.tex integration of LEAD-0001, PROOF-0001, and the causal-random-provenance guard. The GitHub update was blocked before acceptance. No main2/main3 update is claimed.

## Missing publications
- RED-0001 detailed body: missing; do not reconstruct from stub.
- PROOF-0002 detailed body: missing; do not reconstruct from stub.
- RESEARCH-0001 substantive report: not located.

## Handoffs
LEAD: use causal random provenance only as a diagnostic; target unavoidable post-revelation work.
PROOF: recover PROOF-0002 and formalize the strongest surviving post-revelation theorem after the replay/PH/randomized closures.
RED: recover RED-0001 and attack the strengthened theorem with maximal semantic answers, preprocessing, memoization, replay, and polynomial evaluators, withholding only future random bits.
RESEARCH: publish/retry RESEARCH-0001 and review primary literature on online/adaptive computation, proofs of sequential work, VDFs, random-oracle lower bounds, and meta-complexity, distinguishing assumption-based sequentiality from unconditional lower bounds.
WRITE: retry main2/main3 synchronization first next run.

## Status ledger
P vs NP OPEN. CSE/arbitrary-algorithm extraction OPEN. FSC OPEN. Ordinary-source acquisition lower bound OPEN. Nonalgebrizing hinge OPEN. Unavoidable post-revelation-work theorem OPEN.

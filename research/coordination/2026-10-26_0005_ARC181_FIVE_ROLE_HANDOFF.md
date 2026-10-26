# ARC181: one-bit decision does not imply two query transcripts

Date: 2026-10-26 00:05 America/Los_Angeles. Role LSPV-1 formal proof lead. Existing five schedules and scientific allocation retained exactly; no task changes. P versus NP and ARC-EDGE-90 OPEN.

## New source-coherent theorem (PROVED/EXACT, independent review pending)

Construct a fixed-incidence, fixed-length family F_{p,b} of ordinary proper signed three-CNFs. A signed four-clause unary forcing gadget U(l;a,c) forces literal l. A four-clause XOR gadget enforces each bit of a running parity, and a final forcing gadget enforces odd parity. For b in {0,1}^p, the formula has exactly n=4p+1 variables, m=8p clauses and encoded N=Theta(p log p) bits. SAT(F_{p,b}) iff parity(b)=1. Flipping any single b_i changes exactly four signed literal fields in a fixed disjoint group D_i, with no other changes.

Every deterministic all-ordinary-input SAT decider, starting from an input-independent state, must read at least one source bit in each D_i on every member of the family. Otherwise it could not distinguish a formula from the one-bit flip that has the opposite SAT label. Therefore it makes >=p source-bit reads per promised input, and its complete address/answer transcript map is injective on all 2^p family members. The **final output alphabet still contains only SAT and UNSAT**, so an executive inference "R<=2 because decision outputs one bit" is only correct for final output labels, NOT for all query transcripts. R_transcripts may equal 2^p.

This is only Omega(N/log N) actual bit probes on an easy promise family, NOT a superlinear bound for general SAT. A balanced parity circuit of exactly 4(p-1) two-input NAND gates and depth <=3 ceil(log2 p) computes the entire promised decision map from b; hence 2^p query transcripts do not imply large decision circuits. A later checkpoint after computing and retaining one parity bit needs q=0 further probes; the initial transcript lower bound cannot be transported to arbitrary checkpoints without charging the earlier source reads.

## Exact finite reproducible controls (COMPUTATIONAL)

The standalone standard-library Python script enumerated all promised family inputs for 2<=p<=8: 508 ordinary proper three-CNFs, 254 SAT and 254 UNSAT. 508 independent DPLL evaluations; 12 additional full exhaustive truth-table evaluations (p<=3); 3,584 individual control-bit flips checked for exact four-sign-field locality, SAT-label reversal, and disjointness. 17,657 explicit assertions, zero failures. Largest case 33 variables and 64 clauses. Repro script and machine-readable data below.

## Dependencies, scope and remaining arrows

Dieter van Melkebeek survey 2007 Thm 1.3 and FLMV 2005 random-access indexed model inspected in primary PDFs; the two-algorithm condition is an OR, not a conjunction. Bathie-Williams 2024 bounds polylogtime-uniform NAND depth for full SAT, not arbitrary TM time or an instance-specific verifier. Döcker's monotone exact-(2,2) NP-complete grammar is distinct from the ordinary parity source.

LSPV-2 CIRCUIT-R15-VIRTUAL-ACCESS163 has a conditional fixed-incidence bit-local compiler into proper **signed** exact-(2,2) 3CNF. It should be independently checked whether this exact parity family transfers while retaining disjoint source-coordinate influences and charging every bit query; no clause-monotone transfer is claimed. A local parity promise circuit is not the full all-N-bit SAT decision circuit C_{A,N}. The user-mentioned PNP_Circuit_Certificate_Continuation.pdf and source bundle were not found by exact name in accessible conversation/Library/GitHub searches.

## Specific peer requests, retaining schedules

Role 2: audit R15 index locality and all-input model; test signed exact-(2,2) transfer, and separately analyze clause-monotone eligibility.
Role 3: do not confuse transcript cardinality with a complete affordable UNSAT certificate; test all-UNSAT coverage independently on parity and genuine hard controls.
Role 4: audit the before/after-checkpoint source reads, index/control, writable traffic, guest calls, retained state and exact FLMV model.
Role 5: correct only the overly broad R<=2 transcript claim in the executive summary; preserve the valid warning that SAT's one-bit output does not force retained models, witnesses or superlinear resource use. Independently review the parity proof and controls.
Role 1: preserve the formal achievable-set DAG and arbitrary unknown exponent K; the all-input affordable certificate scheme and deterministic small-space seed remain OPEN.

## Repository handoff paths

- research/agents/lspv-1/2026-10-26_0005_LSPV-1_ARC_PARITY_TRANSCRIPT_FIREWALL181.tex
- research/agents/lspv-1/2026-10-26_0005_ARC181_parity_transcript_audit.py
- research/agents/lspv-1/2026-10-26_0005_ARC181_results.json
- research/agents/lspv-1/2026-10-26_0005_ARC181_references.bib
- research/coordination/2026-10-26_0005_ARC181_FIVE_ROLE_HANDOFF.md

END_HANDOFF::ARC181

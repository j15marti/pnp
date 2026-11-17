# AUTOENC-SIGMA3-1 | 2026-11-18 05:01 KST

**Circuit-SAT / Sigma2 / Sigma3 research. P versus NP OPEN.**
**Status:** PROVED/EXACT restricted conditional theorem; COMPUTATIONAL finite checks; unrestricted A->Phi(A) OPEN. Independent mathematical peer review not performed.

## Ideas proposed before literature
1. **AUTOENC-SERIAL**: recognize an explicitly tagged, self-delimiting Sigma3 block source and compile one ordinary Circuit-SAT child at a time, using one complete source scan *per quantified tuple* rather than per child.
2. **OFFSET-INDEX**: precompute q offsets (cost O(q log N) bits) to accelerate source block access; unnecessary under the accepted coefficient budget.
3. **DYNAMIC-SEMANTIC-PORT**: dynamically acquire port scopes from an arbitrary DAG using solver A, not syntactic tags; OPEN because attaining even one port value can encode parent-sized SAT.
4. **FREE-STRATEGY**: collapse adaptive post-universal witnesses to globally committed bits; FALSIFIED by equality quantifier reorderings.

## Recovered project and primary literature
Connected GitHub reads: AGENTS.md blob 3b5d1788aa104b10f094e7eec28d22a070118b17; CODEX.md blob 15639f62a254aa9cd36a949b9f9d81985e5ed538; 2026-11-15 end-to-end directive blob 8451d955f6cd5397de0895f8ebb46e30818842c3; main3_PNP_TIME_SPACE_TRADEOFFS.tex blob e23bbe8a659595badc809b1ca6ed20af83c34b6b; prior virtual-child theorem blob a5499fd3b9e2ef6712182170f1ca34903abdf29e; sigma-primary CONTEXTOBSERVE8 blob 05dbfed470b899faa786c35d0628f7a18287fb06; LSPV2 input INDEX audit /467 blob a02e7895620d286786688860e025f23c1886622d.

Primary: Fortnow–Lipton–van Melkebeek–Viglas, JACM 2005, DOI 10.1145/1101821.1101822; R. Ryan Williams, STOC 2024, DOI 10.1145/3618260.3649723. Both require careful quantitative and same-machine hypotheses; neither yields arbitrary unknown-exponent contraction from P=NP alone.

## Exact source class and restricted theorem
A read-only N-byte input uses grammar:

```text
S3C 1 nx ny nb q
B ni ri
signed-literals 0
... exactly ri clauses ...
E
... exactly q blocks ...
Z
```

Shared variable positions correspond to outer existential x (nx bits), universal y (ny bits), then post-universal interface b (nb bits). Each block C_i has its own disjoint private variables z_i; cross-block sharing is *only* through x,y,b. Empty clauses are permitted and recognized. A streaming parser validates tags, counts, clause indices, canonical bounded integers and EOF. The *promised class* has p=nx+ny+nb <= (2/25)log_2 N, q <= sqrt N, and raw encoded block lengths <=sqrt N.

For every fixed correct ordinary Circuit-SAT decider A with T_A(m)<=m^{K+o(1)}, S_A(m)<=m^{L+o(1)}, K>=1, a uniform parser and serial compiler decides

```
exists x forall y exists b,z_1,...,z_q : AND_i C_i(x,y,b,z_i)
```

with

```
T(N) <= N^{max(27/25,29/50+K/2)+o(1)}
S(N) <= N^{max(1/2,L/2)+o(1)}.
```

Proof: fix x across y; for each y search b; each component's private witness is independent. Substitute x,y,b in C_i, compile one explicit AND/OR/NOT Circuit-SAT child in size N^{1/2+o(1)}, execute A, discard child and guest memory. Max 2^p<=N^{2/25} tuples, q<=N^{1/2} guests per tuple. **One stream scan per tuple** costs N^{27/25+o(1)} total, not q full parent scans per tuple. Guests cost N^{29/50+K/2+o(1)}. Peak live buffer plus guest space is N^{max(1/2,L/2)+o(1)}. Source input is read-only; materialized guest child, indices, guest INPUT-index tape, buffers and all workspace are counted. FLMV-specific machine interpreter transfer remains OPEN.

The resulting time exponent lies at least 1/50 below max(11/10,3/5+K/2) for K>=1 **on this promised source language**. It is not an all-input hereditary transformation.

## Tests executed
Python revision AUTOENC-SIGMA3-1.v1, seed 20261118: 360 random source instances (63 true,297 false); 5 special quantifier/empty-clause/conflict cases; 5 malformed-source rejections; one actual in-promise source of 10018 bytes with 100 blocks of 100 bytes and one quantified port bit; 3826 assertions, 3448 pointwise CNF-vs-circuit checks, 4246 exhaustive guest invocations, 1896 scan passes, zero discrepancies. Independent direct quantified CNF and compiled-circuit evaluators agreed. The guest is brute force, NOT a hypothetical polynomial A. Native Python parser not proved bit-exact for arbitrarily malformed giant numerals; formal tokenizer must be bounded.

Local reproducibility bundle SHA-256 manifest:
- test_autoenc_sigma3.py: 9de55d5302f913c84f9a053f5415d7d9811b3c48d0dd28705ba6de15ba4d7be5
- raw.json: 99f4e93da22374d3a8e41ddef53e9f8526ee42b833860e31dbbc28d05fc520fc

## Falsifiers and gates
PADDING: an arbitrary m-byte SAT core embedded with N=m^{2+o(1)} tautology padding yields inherited original-input time m^{K+1+o(1)}, not a true K/2 speedup.
HEREDITY: compiled ordinary Circuit-SAT children need not satisfy S3C grammar; recursion is not closed.
PORT ACCESS: source-only syntactic recognition does not extract semantic interfaces of arbitrary reconvergent DAGs.
PREFIX: outer x cannot vary with y; b may legitimately vary with y.
DISJ: correctness only, no circuit lower bound. Relativization: PASS as accounting, negative for separation. DTISP: same-run random-access accounting PASS restricted, FLMV physical transfer OPEN. Deterministic configuration counting: not a lower bound. Algebrization/Natural Proofs: no separation claimed.
No source replay, solver-A code introspection, parent-scale SAT call, free strategy or simultaneous q-child cache is assumed.

## Handoff
**Named missing lemma:** from arbitrary *unpadded* ordinary Circuit-SAT source and arbitrary fixed A, cheaply construct a semantically exact, small-interface *hereditary* decomposition with actual source-to-encoded-child access and no parent-sized SAT call. The present streaming theorem can be its downstream evaluator only after that lemma and same-machine model transfer are independently proved.

No TMR-owned root manuscript, retired proof trackers or schedules were modified. Local complete report, Python verifier and raw results remain in this run's reproducibility bundle. **P versus NP OPEN.**

FINAL_VERIFICATION_SENTINEL_AUTOENC_SIGMA3_1_20261118

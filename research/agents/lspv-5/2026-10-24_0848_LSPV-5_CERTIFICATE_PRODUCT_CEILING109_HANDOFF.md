# CERTIFICATE-PRODUCT-CEILING109 handoff

**Status:** P versus NP remains **OPEN**. This run proves an exact query-model ceiling, independently validates Role 4's heterogeneous switch, and retires a false amplification.

## New exact result

For every total Boolean label function on `M` explicit source fields,

`D(f) <= min(M, C0(f) C1(f))`.

For Role 3's `AND_q OR_q` grid, `C0=C1=q` and `D=q^2=M`. The certificate/minimax gap is real but is exactly full source acquisition. It gives no positive post-acquisition lower bound. The proper-3CNF embedding therefore yields only `Omega(N/log N)` addressed sign-group reads, matched by a canonical scan.

## Role 4 independent audit

HETEROGENEOUS-GATE72's local clauses force `t = X OR ell1`; the guard SCC reduces the target to `(x OR A_beta) AND (not x OR F_b)`. Its label is SAT iff `xor(beta)=0 OR b != 1^q`. Counts independently agree: `n=11q+9`, `m2=13q+5`, `k=9q+4`, `M=22q+9`. The `q/2` disjoint-top-clause packing proves the raw strong-2CNF backdoor lower bound. The `OR2 + even-XOR3` endpoint is NP-complete by Schaefer, while the family itself has a charged linear SCC/affine/2SAT hybrid and a direct linear sign scan.

## Computational audit

- 65,812 Boolean functions on 1--4 fields exhausted.
- 131,634 certificate-product/source-ceiling assertions.
- Exact grid measures recovered: `(D,C0,C1)=(4,2,2)` and `(9,3,3)`.
- 4,452 heterogeneous parity/label checks for `q=2,4,6`.
- `q=64` adaptive controls: SAT early/late = 64/4096 reads; UNSAT early/late = 64/4096 reads.
- Zero failures.

## Adaptive-state warning

The row policy and heterogeneous hybrid choose rules from observed states and charge parsing, recognition, failed affine work, switching, rereads, witness replay, and peak space. These are restricted constructive policies, not coverage of every decider. Any use of a fixed residual scalar, fixed branch rule, or finite menu as a proxy for arbitrary algorithms remains invalid.

## First missing lemma

Prove a post-acquisition adaptive dichotomy for one fixed NP-complete encoding: after all source reads are charged, every total uniform exact decider must either build/verify a superpolynomial compatibility representation actually used by its execution or incur superpolynomial continuation. The invariant must be runtime-independent, representation-agnostic, survive switching/caching/recomputation, and allow distinct SAT and UNSAT success conditions. This remains **OPEN**.

## Files

- `research/agents/lspv-5/2026-10-24_0848_LSPV-5_CERTIFICATE_PRODUCT_CEILING109.tex`
- `research/agents/lspv-5/2026-10-24_0848_LSPV-5_CERTIFICATE_PRODUCT_CEILING109_HANDOFF.md`
- `research/agents/lspv-5/code/certificate_product_audit109.py`


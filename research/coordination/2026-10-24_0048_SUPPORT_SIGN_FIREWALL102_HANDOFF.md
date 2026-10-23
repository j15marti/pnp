# SUPPORT-SIGN-FIREWALL102 handoff

**Owner:** LSPV-5  
**Status:** PROVED/EXACT in the stated support and query models; unrestricted deterministic lower bound OPEN.  
**Main report:** `research/main/2026-10-24_0048_MAIN_SUPPORT_SIGN_FIREWALL102.tex`

## Exact new theorem

Every simple 4-regular 3-uniform clause support admits a signing with exactly two positive and two negative occurrences per variable for which every clause contains a positive literal. The all-TRUE assignment therefore satisfies the signed exact-(2,2) formula.

Proof: give every variable two clones and match each clause to one incident clone. For every clause subset Q, 3|Q| incidences enter variables of total degree at most four, so the two-clone neighborhood has size at least 2(3|Q|/4) >= |Q|. Hall gives a clause-saturating matching. Mark matched occurrences positive and fill every variable to two positives.

## Concrete firewall

Apply the theorem to the verified 198-variable, 264-clause support-simple UNSAT source in `research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt`.

- New SAT formula: exact-(2,2), proper, same ordered unsigned supports and metadata.
- Witness: all TRUE.
- Matching size: 264.
- Sign-field Hamming distance from source: 398 of 792.
- SAT compact hash: `67e4955833ab2704f55ab4e1b13077e7be0bace85641afbacb9f59488111e088`.
- Unsigned-support hash: `b74c7384063fc4c7aa2fe5c882599925a2d0eee8787e5f3f56d612b2d2b23fab`.

Consequence: every invariant determined solely by the complete unsigned incidence/support representation is identical on opposite labels. Degree, Hall deficiency, matching data, width, expansion, separators, and clause-dual geometry are RETIRED as stand-alone label obstructions at this endpoint. This does not retire signed-semantic obstructions.

## Block lower bound and its exact limit

For p disjoint blocks, choose independently SAT template S or UNSAT template U. The conjunction is SAT iff all p blocks are S. On the all-S input, any exact deterministic sign-field, literal-word, or clause-record decision tree in the fixed block-major encoding must query one differing location in every block, hence at least p queries.

Parameters:

- n = 198p, m = 264p;
- fixed record words W = 1056p + 2;
- word width w = ceil(log2(64(462p+1)));
- encoded bit length N = Ww;
- lower bound p = Theta(N/log N).

This is an encoding-scoped acquisition bound, not an unrestricted time theorem. A template scan decides the promise family in O(N/w) words. A paid reduction from the p-field implication-chain source must write at least 1056p+2 target words, so the transport numerator `p - R - H` is negative. Direct inclusion preserves p queries but does not amplify their order.

## Independent Role-4 audit

REGULAR-DEFICIENCY63 passes symbolic review:

1. In exact-(2,2), n=3t and m=4t; deficiency at most t, and equality forces the full clause set.
2. Deleting one clause lowers the maximum deficiency exactly to t-1.
3. In the Horn selector lift, a selected group with ternary flag a and b selected implications contributes 0 when a=0 and b-2 when a=1. Positive contribution occurs only for a complete group (a=1,b=3). Thus incomplete groups cannot create a hidden equality case; deficiency and uniqueness transport exactly.

These are structural theorems only.

## Reproducibility ledger

- Code: `experiments/review/support_sign_firewall102_audit.py`
- Raw: `results/raw/review/SUPPORT_SIGN_FIREWALL102_raw.json`
- Assertion-accounted checks: 210
- Tested block range: p=1..32
- Failures: 0
- Raw digest excluding its digest field: `1b7627073c1330b62b5b0f08734edb2b3fbb478735cab62a09db5bdd0978fbc5`
- A naive general DPLL cross-check exceeded 30 seconds and was terminated; it is not used. The source UNSAT label remains the imported DOECKER-CORE-CERT61 checked-certificate dependency.

## Highest-value next lemma

Define a signed-semantic obstruction for one fixed NP-complete encoding and prove an acquisition/compression/continuation dichotomy for every total uniform deterministic exact decider that survives same-support opposite labels, template recognition, multi-pass branching programs, caching, and alternate representations, while leaving a positive transport remainder after parsing and construction.

Until that universal bridge is proved, the chain remains:

`signed obstruction` -/-> `charged dichotomy` -/-> `all deciders` -/-> `superpolynomial contradiction`.

P versus NP remains **OPEN**.

# LSPV-1/492 addendum: external third-party kernel/Comparator replay audit

**November 7, 2026 18:10 PST | Route B | REPORTED EXTERNAL REPRODUCTION, NOT INDEPENDENT EXECUTION BY LSPV-1 | P versus NP OPEN.**

**Tracker:** [P2-B3] receives material additional evidence, not a theorem-status promotion. [P2-D1], [P2-C3], [P2-B1], [P2-B2] and [P1-01] remain OPEN.

## New source located after initial research publication

A public *third-party, self-reported* reproducibility repository was located in a secondary web search and its actual source reviewed using the GitHub connector:

- \`unaltuzun/exponential-time-hypothesis-verify\`, pinned main commit \`a775e22cf311787b940577bb5378b4ce7b70b58c\` (October 30 2026), \`VERIFICATION.md\` and \`docs/REPORT.md\`.
- Claimed independently reproduced **OpenAI math** commit \`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a\` (not the newer repository head). Logs reportedly show \`lake build\` success for \`OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.Final\`, \`#print axioms\` listing only \`propext, Classical.choice, Quot.sound\`, and success for Comparator with the **ordinary Lean kernel**. The separate \`nanoda\` kernel was **NOT** enabled.
- The same third party reports a successful \`lake build\` and \`#print axioms\` for Anthropic \`eth/\` at commit \`16a5ce41304fcdaea4e0be7c132e1c361dc26da5\`. It **did NOT run Comparator** for Anthropic. The two expected \`sorry\` warnings were confined to its intentional \`Challenge.lean\` statements, not \`Solution.lean\`.

This is materially stronger evidence about **actual Lean kernel replay** than merely viewing repository source or CI status. But the current agent **did not independently run or inspect the complete reported command logs line by line**, and no formal mathematical proof audit outside these reported kernel checks was conducted. The independent review of encoding/cost-model fidelity and real-world theorem significance remains necessary. A passing kernel says the formal statement follows from trusted definitions and axioms, not independently that a complicated statement models the intended algorithm without a subtle definition flaw.

## Mathematical implication unchanged

Pang's fixed \`Res(PC_1/F_3)\` random proper 3CNF exponential shared-DAG lower bound and the published OpenAI/Anthropic fixed-3SAT \`2^{o(n)}\` counting claims jointly yield the **conditional non-tailored B1 failure** already proved in LSPV-1/492. Nothing in this addendum supplies a historical R_mix341 proof translation or worst-case B2/B3; no P versus NP resolution.

## Documentation and scope

Original report \`research/agents/lspv-1/2026-11-07_1810_LSPV1_492_SUBEXP_B1_TRANSFER.md\` and reproducible JS/Python finite controls are preserved. This is **new independent-source evidence, not another assertion of original theorem novelty**. The GitHub external verification report is a primary record of someone else's claimed commands, not an execution within this run.

Actual result: authenticated the existence and stated scope of a third-party kernel/Comparator **replay report**. Still OPEN: verified historical mixed grammar [P2-D1], full legal mixed translation [P2-C3], superpolynomial min across all native rules [P2-B1], noncircular B3 [P2-B2]. P versus NP OPEN.

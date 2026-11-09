# LSPV-1/531 five-role handoff, 2026-11-09 02:55 PST

**Route B lead.** [P2-L1-531] applies the *known* exact crown-graph biclique-cover theorem to the no-auxiliary original-indicator **two-boundary** one-hot modular relation. The least unrestricted-width CNF clause count is k(q)=min{k: q<=binom(k,floor(k/2))}; q=3 gives three, q=5 gives four (not five). The proof is a Sperner antichain lower bound plus a constant-weight-code explicit CNF construction. This is not a novel biclique theorem and not an R_mix341 all-rule work lower bound. It is a representation shortcut and a boundary to generalizing the q=3,b>=3 flat-CNF theorem [P2-L3-530].

**Verification:** independently executed Python and V8/JS, each 60 charge/orientation cases, q=2..11, 3030 total onehot pairs; JS also exhaustive all signed clause patterns and exact finite covering DP for q=2..4, finding first-cover sizes 2,3,4. Complete original-source exactly-one clauses and any native derivation remain separate obligations. Corrupted/non-onehot input is not silently accepted as an original source.

**Peer work and search:** consulted [P2-L1-530] (affine-hull), [P2-L3-530] (optimal ternary q=3,b>=3 mixed-polarity flat CNF), [P2-L5-457] (pure affine auxiliary projection), issue #3, Grok and actual Claude files, konard and blkph0x current indexed repositories, and frat-xor, cake_lpr, openai/math. Historical Rmix native grammar remains unauthenticated. External prior art Bezrukov-Fronček-Rosenberg (2008) explicitly establishes the crown-graph biclique theorem. The current report proves the SAT encoding corollary directly.

**To LSPV-3:** Test whether a strict 3-CNF original-source **native accepted** packet realizes the ternary b=2 three-clause relation without inventing a global conversion rule. Ordinary clause representation is not a paid mixed refutation.

**To LSPV-5:** Red-team the onehot promise, clause falsity rectangles, Sperner lower bound, auxiliary and width exclusions, and exact source-authentication limitation. Investigate b>=3 cross-branch sharing and known nonlinear shortcuts.

**Route A LSPV-2/LSPV-4 (secondary peer only):** A flat CNF representation shortcut is not an all-input same-machine SAT transformer and cannot be inserted into FLMV resource inequalities for free.

**OPEN:** [P2-D1], [P2-C3], [P2-B1], [P2-B2]. **No historical rule/weight/task/schedule/agent/allocation changes. P versus NP OPEN.**

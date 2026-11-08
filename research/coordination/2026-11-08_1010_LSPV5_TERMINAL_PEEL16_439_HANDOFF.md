# LSPV-5/439 handoff: terminal peel raises the finite proper-Resolution floor to 16

**2026-11-08 10:10 PST | Route B independent red team | P versus NP OPEN**

## Result

For the exact 16-source cancellation gadget, any minimum acyclic DAG deriving all three goals has a sink that is one of the goals. Exhaust every exact proper-Resolution parent/pivot pair for each possible sink. After removing that one paid sink inference, the remaining targets still have all 16 sources in one connected indispensable-source overlap component in all 20 branches. `[P2-L1-509]` therefore gives 15 remaining nodes, so total work is at least 16.

With `[P2-L1-507]`, the finite proper-Resolution range is now `16..19`. This strengthens `[P2-L5-438]`; it does not decide 16--18, authenticate historical mixed rules, or establish asymptotic hardness.

Post-publication reconciliation: `[P2-L1-510]` proves the compatible identity $q=15+\mu$ in this connected strict-binary setting. Hence `[P2-L5-439]` additionally forces cyclomatic rank $\mu\ge1$ for every legal three-goal proof. Its `15..19` sentence is a pre-`/439` baseline; the current range remains `16..19`.

## Verification

- Python: complete closure 1,270 clauses; 253,208 exact parent options; goal option counts `6,8,6`; 20 branches all floor 16; 13.446 s, 48,428 KiB RSS.
- Independent Node/V8: same closure/options/counts and all 20 branches; 30 assertions plus three hostile controls PASS; wrapper 4.919 s, 98,824 KiB child RSS.
- Recursive terminal-peel depths 0--3 returned `15,16,16,16`; no claim above 16.

## Next work

1. Add sound second-stage pruning or exact certified optimization for 16--18 nodes.
2. Continue adversarial historical RES/DEF/LOCAL accepted-byte authentication.
3. Keep `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` OPEN. P versus NP OPEN.

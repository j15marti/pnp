# SEQUENTIAL-CHECKPOINT-MIDDLE49 role handoff

Date: 2026-10-21 21:48 Asia/Seoul. GitHub publication intended. P versus NP and P versus RP remain OPEN.

## Exact result

For a source-free sequential length-\(M\) generator with \(s\)-bit state and per-bit transition time \(\tau\), checkpoints every \(B\) positions give the optimistic ordinary-KT ledger
\[
\lceil M/B\rceil s+B\tau+O(h+\log M).
\]
Its balanced exponent is \((1+v+u)/2\) when \(s=M^v,\tau=M^u\). At \(k=241\), even constant state and constant step give exponent \(1/2>1/241\). Therefore generic replay/checkpointing cannot certify the desired LOW target. This is not a KT lower bound: modular increment and other fast-forwardable transitions have much cheaper direct indexed programs.

The source-free hypothesis is mandatory. If transitions reread the SAT source, the source/indexer and reread time must be charged.

## Role-targeted next tests

- **:00 MKTP:** instantiate one deterministic total both-label generator with \(s\le p\), \(\tau\le M^{1/240}\), no post-acquisition source reads; attack direct indexing, algebraic powering and checkpoint replay.
- **:12 P!=RP:** Circuit-SAT/Tseitin uniqueness and digest geometry are representation properties; test every language candidate against point-circuit inspection and an alternative deterministic implementation.
- **:24 ARC:** nonuniform KT checkpoints are not algorithm workspace. Test an erasing SAT decider and count live checkpoint, source, child, failure and ancestor bytes.
- **:36 P=RP:** a compact sequential verifier state still needs a uniform accepting-seed hitting method; test equivalent verifier padding.
- **:48 synthesis:** reject both “short state implies LOW” and “failed checkpoint compiler implies HIGH.” Require a direct-index ledger plus a checkpoint/source ledger.

Audit: 8,570,287 assertions, zero failures. Circuit-SAT remains a comparison representation, not a third PNP route.

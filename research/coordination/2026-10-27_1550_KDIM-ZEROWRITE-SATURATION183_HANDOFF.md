# KDIM-ZEROWRITE-SATURATION183 additive handoff

Date: 2026-10-27 15:50 UTC. Role: LSPV-5 independent red team. P versus NP and ARC-EDGE-90 remain **OPEN**.

## New restricted theorem

For every fixed `k>=1`, one fixed deterministic finite controller with one two-way sequential read-only input head and `k` initially blank sequential work tapes decides an explicitly tagged `k`-dimensional DISJ promise with

`D=W=0`, `S=k(B+1)=Theta_k(m^(1/k))`, `C=2m`, `T=O_k(mN)`, where `m=B^k`.

Thus the WRITE-TIGHT2 face `d+k*s>=1` is attained at `(d,s)=(0,1/k)` on this tagged easy promise. This generalizes LSPV-4's `k=2` matrix endpoint and the unary `k=1` endpoint.

## Critical repair

The first executable used an unbounded host-side move log to undo source lookup. That is hidden memory and was **FALSIFIED** as a machine implementation. The published reproducer removes the log. It backtracks using only level delimiters, charged head positions, and fixed-depth finite control. The repaired implementation passed 12,005 runs.

## Scope barriers

- `k` is fixed. Growing `k` would grow the controller/alphabet and change the machine.
- The source has explicit hierarchical tags. This is **not** unchanged canonical exact22.
- A second input head, usable uncharged output-head position, or indexed RAM escapes the sequential model.
- Finite-state padding preserves exponents but does not prove exact22 syntax or full-SAT reduction soundness.
- No full-SAT, FLMV, circuit, ARC, or P-vs-NP consequence follows.

## Interior batching attack

A reusable `B=m^s` writable buffer does not yield `D=m/B`: adversarial overwrites/restorations cost `Theta(B)` per batch across `m/B` batches, hence `Theta(m)` actual changes. This falsifies the naive construction only. The existence of a different interior `0<d,s<1`, `d+s=1` algorithm remains **OPEN**.

## Role-addressed actions

- **LSPV-1:** keep this as a native restricted control, not an ARC/FLMV successor.
- **LSPV-3:** audit every streamed source return path for an uncharged trace/stack; delimiter-driven reversibility must be explicit. Preserve globally sound NO-input polarity.
- **LSPV-4:** the matrix construction is independently generalized; verify the log-free unwind and retain the tag-versus-canonical distinction.

Artifacts: report, log-free reproducer, and raw JSON under `research/agents/lspv-5/`, run ID `KDIM-ZEROWRITE-SATURATION183`.

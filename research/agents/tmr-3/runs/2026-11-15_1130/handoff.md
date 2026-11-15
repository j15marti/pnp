# TMR-3/050 | 2026-11-15 11:30 PST | Track B | readback handoff

Status **PROVED/RESTRICTED** for one explicitly described full-graph/physical-block protocol, independent mathematical review OPEN; finite tests COMPUTATIONAL; P versus NP OPEN.

## Primary result

Ryan Williams (2025) already states that retaining the O(B)-bit block-boundary graph guess limits the existing Tree Evaluation reduction to square-root space even with LOGSPACE Tree Evaluation. Our scoped, exact audit formalizes this: a protocol that materializes a complete pB-symbol ternary schedule and a complete b-bit block register, B=ceil(T/b), necessarily has physical writable peak S>=max(b,B), so min_b max(b,ceil(T/b))=ceil(sqrt T). This is **not** a new universal TIME[t] space lower bound; graph input/streaming/recomputation can avoid the contract.

## New exponent gate

If a hypothetical evaluator, graph generator, address generator and other costs have separate height exponents alpha,beta,zeta,omega, a combined upper template can use mu=max(alpha,beta,zeta,omega), resulting in target exponent rho=mu/(1+mu). Cube-root requires all four <=1/2. In Williams's explicit graph-guess interface beta=1, so improving only evaluator height dependence fails.

At T=2^18, b=T^(1/3)=64, B=4096. Hypothetical b+sqrt(B)=128 evaluator cannot hide the 4096-cell graph descriptor. The balanced two-register floor remains 512 (before logarithms).

## Exact controls and four gates

Falsifiers: lazy source-derived graph, streamed node identifiers, reused memory, time blowup. Concrete countercontrol: 2^B valid binary right/stay head-movement histories encoded in immutable input can be streamed without B writable schedule bits, so no entropy-based arbitrary-machine lower bound. DISJ PASS; relativization N/A for separation; simultaneous DTISP OPEN (no time theorem); deterministic configuration counting PASS as upper-only bound.

**Native Python:** 722196 exact checks, 0 failures, no random seed, 2 byte-identical runs (~1 sec each); T=1..1200, all b, ternary capacities, binary histories B<=10, streaming and exponent controls. No compiled original machine or improved evaluator.

## Paths on research branch

- Report: research/agents/tmr-3/2026-11-15_1130_TMR3_TREE_GRAPH_GUESS_BOTTLENECK050.md
- Code: experiments/tmr/tmr3_graphguess_address050.py
- Raw: results/raw/tmr/2026-11-15_1130_TMR3_GRAPHGUESS050_PY_RAW.json
- This isolated handoff: research/agents/tmr-3/runs/2026-11-15_1130/handoff.md

The historical canonical handoff was not overwritten; issue #3 will receive paths/status. No schedule changes. Root proof1 read fully; oversized proof2/main.tex returned SHAs but empty bodies, so no shared writes. Repository-wide preflight not run; local Git clone lacked network. TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE. /341 FAIL and /386 RESTRICTED.

**Next lemma:** construct/falsify a uniform lazy graph/path generator with O~(b+B^1/2) space covering every adaptive history and charge its input access plus actual sequential time. Couple to a truly improved Tree Evaluation algorithm. P versus NP OPEN.

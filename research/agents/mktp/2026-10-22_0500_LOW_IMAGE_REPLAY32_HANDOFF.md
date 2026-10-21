# LOW-IMAGE-REPLAY32: SAT image-replay obstruction

22 October 2026. Restricted result, not a complexity-class separation.

Suppose a deterministic, uniform, total SAT-to-ordinary-MKTP reduction R emits M=N^(6/5+o(1)) bits in time N^(alpha+o(1)), alpha<241/200, and space N^(1/2+o(1)), correctly mapping SAT to low ordinary indexed KT and UNSAT to high. Assume a uniformly indexable, easy SAT reference E(F), of the same input length, has R(E(F))=R(F) on every SAT F. Running R simultaneously on F and E(F), and comparing output bits without storing the target, decides SAT with the same asymptotic resources. This contradicts the matching deterministic SAT time-space lower bound of Fortnow, Lipton, van Melkebeek, and Viglas. For fixed-width proper 3CNF, E(F) can repeat the clause (x1 OR x2 OR x3) while preserving header parameters and encoding length.

The same contradiction holds for a polylogarithmic uniformly enumerated dictionary of SAT exemplars whose R-images cover all SAT images, assuming strict exponent slack.

A separate uniformly available short indexed program for a canonical LOW template permits an O(Mp polylog M) comparator. At k=241, the exponent (6/5)(1+1/241)=1452/1205 is below 241/200 by exactly 1/48200; k=240 has no strict slack.

Finite hostile test: 1,691 assertions, zero failures, 152 proper-3CNF formulas across 41 layouts, 131,682 streamed comparison steps. Includes padded SAT/UNSAT and minimal INDEX continuations. Toy Walsh targets were both low ordinary KT; no actual high-KT reduction was constructed.

Missing arrow: a source-dependent SAT low-image with no cheap representative cover, plus an independently proven high-KT image for every UNSAT input. P versus NP remains open.

Local report SHA256: 18347659e514783dd1b162fc7d117c7af9b114eefcc9c5054fb0f144578ee337.

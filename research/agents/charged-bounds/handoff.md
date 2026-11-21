# charged-bounds handoff
Updated2026-11-21 12:03 PST, America/Los_Angeles.
Latest [T5-MARGINAL-MATCHING-PAIR1](PNP_Charged_bounds_2026-11-21_120300_Marginal_Matched_Pair.md).
Base899d207c4f94559db08d730d588de99bce3b055b. External independent review pending; same continuous assistant authored the preceding reports.

PROVED/EXACT on Construction's pinned positive-offset image16db13effd093c0df7ce104b3c117ec570be7c7c: for p>=2 use H0=OR(x0,x0),H1=OR(x0,x1), one gate output, other inputs declared free. Source counts2^(p-1),3*2^(p-2). Positive split images have common E81+14p,n426+74p,m520+90p, exact unary/gamma/fixed-ID N, M10*2^E, counts y0=6M2^(p-2),y1=7M2^(p-2).
X=x_J fair; fake=y_L independent fair. Fake conditional Shannon and average-min entropy both1. True/fake output marginals agree EXACTLY. Full multiplier, positivity, shifted-baseline and every output-only test pass.

FALSIFIED/RETIRED this pair's indistinguishability: one differing encoded input bit selects the correct constant. Two output equality circuits plus selector give<=12N+3 gates and exact advantage1/2, which equals total variation. No generic count oracle or hard advice. Uniform generation by known formulas/explicit encodings is polynomial and paid. Atp2,N21594,E109,selector14937 zero-based,259124 gates. This is a new INPUT-AWARE correlation falsifier, not another low-bit/zero-atom test.

COMPUTATIONAL new experiments/t5_bounds_marginal_pair1_20261121.py, results/raw/t5_bounds_marginal_pair1_20261121.json:7 pairs p2..8,28 explicit AND/OR/NOT evaluations,28 output-only predicates. New code SHA256eb01ccb667fa7d7d75ef26a466794772cd58001728b5509bb5910ff49d974ee3. Pinned construction dependency SHA2566cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb. Split counts by published equality theorem, not expanded enumeration. Prior generic T5/zero-atom suites not rerun.

Prior zero-atom result remains: Adv>=max(0,p0-2^-k),budget3N, for average conditional min-entropy; not a Shannon restriction, not exclusion of one bit on balanced support. Positive-offset baseline atom also survives. This run passes all output-only controls yet fails joint testing. General pseudoentropy route remains OPEN.

Fixed A,K,a same execution ceilings unchanged:S N^a,physical CM N^(2a),minimum-description CM N^(a+1),count-map circuits N^a logN. No exponent excluded; SAT-only support has constant SAT answer and no decision separation. C and ordered R remain distinct. Parsing/authentication, generation, addresses, wire serialization, actual tape accesses, retained source, sharing, recomputation, switches and output charged. No virtual residual demand.

ONE next dependency T5-SAT-SLICE-JOINT1, Bounds owner, Redteam review/Synthesis tracking: explicit SAT-supported source/fake with one conditional bit and an independently justified input-aware cap-budget indistinguishability proof, or another concrete small falsifier. Marginal matching alone is insufficient.

Fresh primary Vadhan–Zheng2013 joint definition read; initial STOC endpoint timed out, alternate succeeded. Fresh six-org connected/web searches;Google429 retry succeeded no matches. No external theorem/code import/build. Current source bodies recovered, baseline not independently recertified. No checkout/preflight/LaTeX/TMR/schedule changes. P versus NP OPEN.

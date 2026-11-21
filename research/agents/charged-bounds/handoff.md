# charged-bounds handoff
Updated2026-11-21 10:01 PST, America/Los_Angeles.
Current [T5-SPLIT-QUOTIENT-RESIDUE1](PNP_Charged_bounds_2026-11-21_100100_Split_Quotient_Low_Bits.md).
Recovery3168128105d8f040f41f8a49da8d6f0deffb9112.

PROVED/EXACT explicit distinguisher, independent review pending; FALSIFIED/RETIRED candidate Ytilde=F_N(X)+10R on Construction's split graph image, R uniform k bits,1<=k<=E=10+3v+2e. True counts divisible10*2^E. Fake stays in alphabet, has k conditional Shannon/average-min entropy and passes mod10. Raw output bits1..r are uniform forfake and zero fortrue, so r-1 OR gates give advantage1-2^-r. One wire gives1/2 atzero noninput gates. General budgetB lower advantage1-2^-min(k,B+1). No quotient conversion cost required for this raw-bit test.

Same-N both-label control K2,3 / K4+isolate: n211,m243,E37,N6059; counts9411819533762560/0, source N_H351 kept separate. k37 has37 entropy bits but36 OR gates distinguish with1-2^-37. No decision hardness implication.

COMPUTATIONAL code experiments/t5_bounds_split_residue1_20261121.py; raw results/raw/t5_bounds_split_residue1_20261121.json.16380 fake values,156 rational advantage rows for k1..12; k37 symbolic only. Prior Accounting source counts reused with SHA pin, not re-enumerated. No solver benchmark.

Prior orbit divisibility, parity Omega(N/log N), and Synthesis quotient-budget interface remain unchanged. Fixed-cap S,physicalCM,descriptiveCM,count-circuit ceilings all retained; none exceeded. Fake entropy is not a resource demand.

ONE next dependency T5-FULL-MULTIPLIER-PAIR1, Bounds owner, Redteam review/Synthesis tracking: normalize10*2^E and prove/falsify an actual core-quotient pair against cap-sized distinguishers. Fakes supported on full multiplier defeat this specific test, not all possible tests.

Fresh Vadhan–Zheng2013 primary read and official five-org searches/ownership sources recorded. No theorem imported from snippets; no TMR/preflight/LaTeX/schedule changes. P versus NP OPEN.

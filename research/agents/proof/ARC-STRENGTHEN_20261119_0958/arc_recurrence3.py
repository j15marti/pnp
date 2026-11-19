import json
from fractions import Fraction

# Exact integer recurrence on N_h=2^(2^h): child=sqrt(N_h).
# Base T(2)=4; a=1,r=2,theta=1/2, branch multiplier C.
rows=[]
for c in (1,2,3):
    t=4
    for h in range(9):
        n=2**(2**h)
        if h:
            t=c*n*t+n*n
        normalized=Fraction(t,n*n)
        expected=h+1 if c==1 else (c**(h+1)-1)//(c-1)
        assert normalized==expected
        # Explicit depth-first frame retention, sigma=1.
        sizes=[2**(2**j) for j in range(h,-1,-1)]
        peak=sum(sizes)
        assert peak<=2*n
        rows.append({'C':c,'h':h,'log2_N':2**h,
                     'T_div_N_squared':int(normalized),
                     'peak_frame_words':str(peak),'N':str(n)})
print(json.dumps({'tests':len(rows),'rows':rows},separators=(',',':')))

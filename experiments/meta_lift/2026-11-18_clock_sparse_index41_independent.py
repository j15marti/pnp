#!/usr/bin/env python3
"""Independent bottom-up fixed-target witness comparison for CLOCKSPARSEINDEX41.
Uses explicit interval tables, not canonical reachability recursion.
"""
from itertools import product
import json

# 8-address automatic schedule with one positional override at address 5.
schedule=(0,1,1,0,1,2,0,1)
K=2
# Every transition has an independently specified next state and unpadded emission.
tab={
 (0,0,0):(0,''), (0,0,1):(1,'1'), (0,1,0):(1,'0'), (0,1,1):(0,'01'),
 (1,0,0):(1,''), (1,0,1):(0,'0'), (1,1,0):(0,'1'), (1,1,1):(1,''),
 (2,0,0):(1,'1'), (2,0,1):(0,''), (2,1,0):(0,'01'), (2,1,1):(1,'0'),
}
def run(w,p=0):
    y=''
    for sym,b in zip(schedule,w):
        p,z=tab[sym,p,b]
        y+=z
    return y,p

def bottomup(y):
    # entries[(lo,width,p,q,a,b)] store lexicographically least witness word
    cache={}
    def solve(lo,width,p,q,a,b):
        key=(lo,width,p,q,a,b)
        if key in cache:return cache[key]
        if width==1:
            options=[(bit,) for bit in (0,1) if tab[schedule[lo],p,bit]==(q,y[a:b])]
        else:
            options=[]; half=width//2
            for s in range(K):
                for mid in range(a,b+1):
                    left=solve(lo,half,p,s,a,mid)
                    right=solve(lo+half,half,s,q,mid,b)
                    if left is not None and right is not None:options.append(left+right)
        cache[key]=min(options) if options else None
        return cache[key]
    return solve

words=list(product((0,1),repeat=len(schedule)))
images={}
for w in words:
    images.setdefault(run(w),[]).append(w)
assert len(words)==256
checks=0
for (y,q),ws in images.items():
    dp=bottomup(y)
    ans=dp(0,len(schedule),0,q,0,len(y))
    assert ans==min(ws)
    assert run(ans)==(y,q)
    checks+=len(ws)+1
print(json.dumps({'name':'CLOCKSPARSEINDEX41_INDEPENDENT','source_words':256,
   'attained_fibers':len(images),'brute_comparisons':checks,'failures':0,
   'scope':'fixed 8-bit edited schedule; lex smallest full word, exhaustive'} ,sort_keys=True))

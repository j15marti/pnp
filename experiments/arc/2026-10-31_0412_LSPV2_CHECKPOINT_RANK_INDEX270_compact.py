#!/usr/bin/env python3
"""LSPV-2 270 self-contained exact checkpoint rank/select demonstration.
Runs exhaustive finite binary profile controls. Its oracle calls are NOT SAT
Turing-machine costs. Source-authenticated profile decisions are separately
provided in the full 270 reproducibility package.
"""
import bisect,itertools,json,random
from collections import Counter

def line(mask,b):
    return ' '.join(str(-j if mask>>(j-1)&1 else j) for j in range(1,b+1))+' 0\n'

def serialize(bits,b):
    return f'p cnf {b} {bits.count(False)}\n'+''.join(line(i,b) for i,v in enumerate(bits) if not v)

class Checkpoint:
    def __init__(self,profile,b,h):
        self.p=profile;self.b=b;self.M=1<<b;self.h=min(self.M,max(1,h));self.c=Counter()
        self.prefix=[0];bad=0
        for start in range(0,self.M,self.h):
            n=0
            for i in range(start,min(start+self.h,self.M)):
                v=self.p(i);self.c['build_reads']+=1
                if not v:n+=len(line(i,b));bad+=1
            self.prefix.append(self.prefix[-1]+n)
        self.header=f'p cnf {b} {bad}\n';self.length=len(self.header)+self.prefix[-1]
    def char(self,i):
        self.c['guest_queries']+=1
        if not 0<=i<self.length:return ' '
        if i<len(self.header):return self.header[i]
        x=i-len(self.header);t=bisect.bisect_right(self.prefix,x)-1
        x-=self.prefix[t]
        for m in range(t*self.h,min((t+1)*self.h,self.M)):
            self.c['read_profile_calls']+=1
            if not self.p(m):
                s=line(m,self.b)
                if x<len(s):return s[x]
                x-=len(s)
        raise AssertionError('prefix locator')

def run():
    rng=random.Random(2701031);c=Counter();examples=[]
    for b in range(7):
        M=1<<b
        patterns=[('allgood',[True]*M),('allbad',[False]*M)]
        patterns += [('singlebad_'+str(t),[i!=t for i in range(M)]) for t in {0,M//2,M-1}]
        patterns += [('random_'+str(k),[bool(rng.getrandbits(1)) for _ in range(M)]) for k in range(5)]
        for name,p in patterns:
            target=serialize(p,b)
            for h in {1,2,4,8,M}:
                ix=Checkpoint(p.__getitem__,b,h)
                assert ix.length==len(target)
                for i in range(-2,len(target)+3):
                    expect=target[i] if 0<=i<len(target) else ' '
                    assert ix.char(i)==expect,(b,h,name,i)
                    c['checked_characters']+=1
                assert ix.c['build_reads']==M
                c['indexed_variants']+=1
                c['build_profile_reads']+=ix.c['build_reads']
                c['read_profile_calls']+=ix.c['read_profile_calls']
            c['patterns']+=1
        examples.append({'b':b,'masks':M,'patterns':len(patterns)})
    print(json.dumps({'run':'CHECKPOINT-RANK-INDEX270','seed':2701031,'counts':dict(c),
                      'examples':examples,'status':'finite exact oracle-profile checks only; P-vs-NP OPEN'},indent=2))
if __name__=='__main__':run()

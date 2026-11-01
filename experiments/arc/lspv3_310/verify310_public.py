#!/usr/bin/env python3
"""Independent original-source spot checks. No producer import.
The full 14,574-check no-import verifier is in the GATE310 complete ZIP.
"""
import itertools,json,subprocess,sys
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
def original(t):
    F=[]
    for i in range(t):
        f=lambda v:9*i+v
        F.append(tuple(sorted((f(1),f(6),9*((i+1)%t)+5))))
        F.extend(tuple(sorted(f(v) for v in C)) for C in P[1:])
        F.extend(tuple(sorted(-f(v) for v in C)) for C in Q)
    return 9*t,F
def brute(n,F,pins):
    unknown=[x for x in range(1,n+1) if x not in pins]
    result=0
    for a in itertools.product((0,1),repeat=len(unknown)):
        values=dict(pins);values.update(zip(unknown,a))
        result+=all(any(values[abs(l)]==(1 if l>0 else 0) for l in C) for C in F)
    return result
def test():
    n,F=original(1);assert brute(n,F,{})==70
    mode=[0,0,0,0]
    for j in range(12):
      for k in range(j+1,12):
        for s,u in itertools.product((0,1),repeat=2):
          constraints=[]
          for C,target in ((F[j],s),(F[k],u)):
            constraints.extend((abs(l),int(l>0) if target else int(l<0)) for l in C)
          ok=all(not(any(v==w and b!=c for w,c in constraints[:q])) for q,(v,b) in enumerate(constraints))
          mode[2*s+u]+=int(ok)
    assert mode==[37,49,49,37],mode
    for t in (2,3,4):
        n,F=original(t)
        sat={};unsat={}
        for b in range(t):
            for x,v in ((1,1),(2,0),(3,1),(4,0),(8,0)):
                sat[9*b+x]=v;unsat[9*b+x]=v
        unsat[2]=1;unsat[3]=0
        assert brute(n,F,sat)==1
        assert brute(n,F,unsat)==0
    for t in (2,3,4,8):
        cp=subprocess.run([sys.executable,'experiments/arc/lspv3_310/compact310.py',str(t)],
                          capture_output=True,text=True,check=True)
        result=json.loads(cp.stdout)
        assert result['SAT']==['SAT',1] and result['UNSAT']==['UNSAT',0],result
    print(json.dumps({'status':'PASS','F9_root':70,'F9_four_mode_counts':mode,
                      'brute_original_both_labels_t':[2,3,4],
                      'scrambled_compact_spot_checks_t':[2,3,4,8],
                      'note':'Separate full no-import verifier in complete ZIP'}))
if __name__=='__main__':test()

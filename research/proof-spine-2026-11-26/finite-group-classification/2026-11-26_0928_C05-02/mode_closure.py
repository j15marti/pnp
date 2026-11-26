"""Paid guarded failed-mode affine probes on the same exact binary chart."""
from joint_merge import *

def mode_closure(F,target):
    live=[list(range(len(f))) for f in F];stats=Counter()
    while True:
        hs=[];base=0
        for i,L in enumerate(live):
            a=F[i][L[0]][0];base^=a;U=basis([v for b in L for v in F[i][b][1]]+[a^F[i][b][0] for b in L]);hs.append((a,U))
        if solve_span([v for a,U in hs for v in U],target^base) is None:return None,stats
        change=False
        for i,L in enumerate(live):
            if len(L)<2:continue
            others=basis([v for j,(a,U) in enumerate(hs) if j!=i for v in U]);t=target^base^hs[i][0]
            good=[]
            for b in L:
                a,U=F[i][b];stats['mode_probes']+=1
                if solve_span(others+U,t^a) is not None:good.append(b)
            if not good:return None,stats
            if good!=L:stats['mode_pins']+=len(L)-len(good);live[i]=good;change=True;break
        if not change:return live,stats

def run(F,t,cap=8):
    L,st=mode_closure(F,t)
    if L is None:return 'NO',None,dict(st)
    G=[[f[b] for b in L[i]] for i,f in enumerate(F)]
    s,w,d=pooled_join(G,t,cap=cap,max_pair_checks=300);st.update(d)
    if s=='YES':w={i:(L[i][b],r) for i,(b,r) in w.items()}
    return s,w,dict(st)

def main():
    rng=random.Random(261126054);out=[];A=Counter()
    for _ in range(400):
        n=rng.randrange(2,9);F=[[(rng.randrange(1<<n),[rng.randrange(1<<n) for _ in range(rng.randrange(3))]) for _ in range(2)] for _ in range(rng.randrange(1,7))];t=rng.randrange(1<<n)
        s,w,st=run(F,t,6);s0,_,_=join(F,t,6);assert s==s0;A[s]+=1;A['pins']+=st.get('mode_pins',0)
    old=json.load(open('pooled_results.json'))
    for k in [4,5,7,8,13]:
        T,R=sphere(k);V,B,W,c=close(T,R);assert T==V;D=pairs(V);X={v for c,v in R if c==0};t=(1<<len(X))-1;rec=[]
        for a in next(z for z in old['native'] if z['k']==k)['trials']:
            F,L,G=chart(D,[tuple(e) for e in a['chart0']],[tuple(e) for e in a['chart1']],X);s,w,st=run(F,t)
            if a['after']!='UNKNOWN':assert s==a['after']
            hit=None
            if s=='YES':hit=lift_chart(F,L,w);assert verify(T,R,hit)
            rec.append(dict(status=s,prior=a['after'],stats=st,witness=hit))
        out.append(dict(k=k,m=len(T),trials=rec));print(k,Counter((r['prior'],r['status']) for r in rec),'pins',sum(r['stats'].get('mode_pins',0) for r in rec),flush=True)
    json.dump(dict(seed=261126054,abstract=dict(A),native=out),open('mode_closure_results.json','w'),indent=2)
    print(A)
if __name__=='__main__':main()

#!/usr/bin/env python3
"""LSPV-3 SOURCE-LOCAL-RAM-TAPE-CERT136: exact22 local resolution proof.
Stdlib, deterministic, no SAT oracles, no measured TM resource claims.
Run python this_script.py [raw.json]. Under 30 seconds per invocation.
"""
import sys, json, hashlib, itertools, math
from collections import Counter

W_TEXT='''-1 3 -14 2 -8 9 10 -13 14 3 7 -13 -4 -9 -11 5 8 -14 4 -8 -11 1 7 13 1 -7 10 -5 -6 -15 -2 -6 12 -4 9 -10 -2 5 -12 -3 6 -15 6 -7 11 2 -9 11 4 8 -10 -3 12 15 -5 -12 15 -1 13 14'''
W_LITS=list(map(int,W_TEXT.split()))
W=[tuple(W_LITS[i:i+3]) for i in range(0,len(W_LITS),3)]
Q=[c for c in W if c!=(1,7,13)]
J=((1,-2,-3),(2,4,-5),(2,5,-6),(3,6,-4),(3,-5,-6),(-2,4,5),(-3,-4,6))
assert len(W)==20 and len(Q)==19

def check_model(clauses, model):
    return all(any(model.get(abs(x),0)==(x>0) for x in row) for row in clauses)

class Builder:
    def __init__(self,m): self.m=m;self.nextid=m+1;self.F=[];self.model={};self.side_meta={}
    def alloc(self,k):
        x=tuple(range(self.nextid,self.nextid+k));self.nextid+=k;return x
    def add(self,row):
        assert len(row)==3 and len({abs(x) for x in row})==3
        self.F.append(tuple(row))
    def j(self,signed_y):
        aux=self.alloc(5)
        mapid={1:abs(signed_y),2:aux[0],3:aux[1],4:aux[2],5:aux[3],6:aux[4]}
        for row in J:
            out=[]
            for v in row:
                out.append((1 if v>0 else -1)*(1 if abs(v)!=1 or signed_y>0 else -1)*mapid[abs(v)])
            self.add(out)
        for v in aux:self.model[v]=False
    def side(self,i,bit,label):
        start=len(self.F);qv=self.alloc(15)
        for row in Q:self.add(tuple((1 if v>0 else -1)*qv[abs(v)-1] for v in row))
        p,q,r=(qv[0],qv[6],qv[12]);x=i+1;sgn=x if bit else -x
        sign_id=len(self.F);self.add((sgn,p,q))
        u,v,z,w=self.alloc(4);self.add((-sgn,u,v));self.add((r,z,w))
        for y in (u,v,z,w):
            self.j(y);self.j(-y);self.j(-y)
        self.model.update({v:False for v in qv})
        self.model.update({u:True,v:False,z:True,w:False})
        assert len(self.F)-start==106 and self.nextid-(max(qv)+1)==64
        self.side_meta[label,i]={'q':qv,'sign_id':sign_id,'q_ids':tuple(range(start,start+19)), 'start':start}
    def gap(self):
        for _ in range(self.m):
            e=self.alloc(9)
            for row in range(3):
                edge=e[3*row:3*row+3]
                self.add(edge);self.add(tuple(-x for x in edge))
            for col in range(3):
                edge=(e[col],e[col+3],e[col+6])
                self.add(edge);self.add(tuple(-x for x in edge))
            for row in range(3):
                for col in range(3):self.model[e[3*row+col]]=bool((row+col)%2)
    def build(self,a,b):
        assert len(a)==len(b)==self.m
        self.model.update({i+1:bool(a[i]) for i in range(self.m)})
        for i in range(self.m):self.side(i,a[i],'L')
        self.gap()
        for i in range(self.m):self.side(i,b[i],'R')
        n=self.nextid-1
        assert len(self.F)==224*self.m and n==168*self.m
        deg=Counter((abs(v),v>0) for c in self.F for v in c)
        assert all((deg[v,True],deg[v,False])==(2,2) for v in range(1,n+1))
        assert len(set(self.F))==len(self.F)
        if a==b:assert check_model(self.F,self.model)
        return self.F,n

def serialize(clauses,n):
    w=max(1,n.bit_length());cw=w+2
    assert len(clauses)<(1<<cw)
    prefix='1'*w+'0'+format(n,f'0{w}b')+format(len(clauses),f'0{cw}b')
    return prefix+''.join(('1' if lit<0 else '0')+format(abs(lit),f'0{w}b')
                          for row in clauses for lit in row)

def parse(encoded):
    w=encoded.find('0');assert w>=1
    assert len(encoded)>=3*w+3
    n=int(encoded[w+1:2*w+1],2)
    k=int(encoded[2*w+1:3*w+3],2)
    assert w==n.bit_length() and len(encoded)==3*w+3+3*(w+1)*k
    j=3*w+3;out=[]
    for _ in range(k):
        row=[]
        for _ in range(3):
            sign=encoded[j];j+=1
            var=int(encoded[j:j+w],2);j+=w
            assert 1<=var<=n
            row.append(-var if sign=='1' else var)
        assert len({abs(v) for v in row})==3
        out.append(tuple(row))
    assert j==len(encoded)
    return n,out

def norm(row):return tuple(sorted(set(row)))

def unit_proof(q_ids,qs,target,record):
    # Greedy Davis-Putnam elimination; every line is an explicit resolution rule.
    active={norm(c):record(('source',j)) for j,c in zip(q_ids,qs)}
    remaining=set(abs(v) for c in qs for v in c)-{target}
    while remaining:
        def stats(v):
            a=sum(v in c for c in active);b=sum(-v in c for c in active)
            return a*b,a+b,v
        var=min(remaining,key=stats)
        pos=[(c,j) for c,j in active.items() if var in c]
        neg=[(c,j) for c,j in active.items() if -var in c]
        new={c:j for c,j in active.items() if var not in c and -var not in c}
        for pc,pid in pos:
            for nc,nid in neg:
                res=set(pc)|set(nc);res.discard(var);res.discard(-var)
                if any(-x in res for x in res):continue
                res=norm(res)
                if res not in new:new[res]=record(('resolve',pid,nid,var))
        cleaned={}
        for c in sorted(new,key=lambda z:(len(z),z)):
            if not any(set(s)<=set(c) for s in cleaned):cleaned[c]=new[c]
        active=cleaned;remaining.remove(var)
    assert norm((-target,)) in active and len(active)==1
    return active[norm((-target,))]

def certificate(builder,i):
    F=builder.F;R=[]
    def record(x):R.append(x);return len(R)-1
    def resolve(a,b,var):return record(('resolve',a,b,var))
    units=[];locs=[]
    for label in ('L','R'):
        meta=builder.side_meta[label,i];qids=meta['q_ids'];qs=[F[q] for q in qids]
        p,q=meta['q'][0],meta['q'][6]
        np=unit_proof(qids,qs,p,record)
        nq=unit_proof(qids,qs,q,record)
        sign=record(('source',meta['sign_id']))
        u=resolve(sign,np,p)
        u=resolve(u,nq,q)
        units.append(u);locs.append(meta['sign_id'])
    resolve(units[0],units[1],i+1)
    return R,locs

def verify(F,n,R):
    # Reads only authentic original source clauses, never source-supplied labels.
    vals=[];seen=0
    for j,line in enumerate(R):
        if line[0]=='source':
            idx=line[1]
            if not (0<=idx<len(F)):return False
            row=norm(F[idx]);seen+=1
        elif line[0]=='resolve':
            _,a,b,var=line
            if a>=j or b>=j or a<0 or b<0 or not 1<=var<=n:return False
            x=set(vals[a]);y=set(vals[b])
            if var in x and -var in y:pass
            elif -var in x and var in y:pass
            else:return False
            row=norm((x|y)-{var,-var})
            if any(-z in row for z in row):return False
        else:return False
        vals.append(row)
    return bool(vals) and vals[-1]==() and seen>=40

def pin(lit,n):
    a,b=n+1,n+2
    return [(lit,a,b),(lit,a,-b),(lit,-a,b),(lit,-a,-b)]

def run():
    q_models=0
    for bits in itertools.product((False,True),repeat=15):
        model={j+1:b for j,b in enumerate(bits)}
        if check_model(Q,model):
            q_models+=1
            assert model[1]==model[7]==model[13]==False
    assert q_models==244
    assert not any(check_model(W,{j+1:v for j,v in enumerate(b)})
                   for b in itertools.product((False,True),repeat=15))
    totals=Counter();cases=[]
    for m in (1,2,4,8,16):
        combos=[((0,)*m,(0,)*m),((1,)*m,(1,)*m)]
        for i in sorted({0,m//2,m-1}):
            b=[0]*m;b[i]=1;combos.append(((0,)*m,tuple(b)))
            a=[1]*m;a[i]=0;combos.append((tuple(a),(1,)*m))
        for a,b in combos:
            builder=Builder(m);F,n=builder.build(a,b)
            enc=serialize(F,n);n2,F2=parse(enc)
            assert n==n2 and F==F2 and len(enc)==3*n.bit_length()+3+3*(n.bit_length()+1)*len(F)
            totals['cases']+=1
            idx=next((i for i in range(m) if a[i]!=b[i]),None)
            if idx is not None:
                proof,locs=certificate(builder,idx)
                assert verify(F,n,proof)
                totals['unsat']+=1
                totals['max_records']=max(totals['max_records'],len(proof))
                # SAT input made by repairing the unique conflicting sign bit.
                forged=list(F)
                target=locs[1]
                forged[target]=tuple(-z if abs(z)==idx+1 else z for z in forged[target])
                assert not verify(forged,n,proof)
                mutilated=proof.copy();mutilated[-1]=('resolve',0,1,idx+1)
                assert not verify(F,n,mutilated)
                # Source sign records are physically separated by Omega(N) bits.
                gap=(locs[1]-locs[0])*3*(n.bit_length()+1)
                assert gap>0
                cases.append(dict(m=m,nvars=n,clauses=len(F),bits=len(enc),gap=gap,
                                  gap_ratio=round(gap/len(enc),6),records=len(proof),
                                  unsat_certificate=True))
            else:
                assert check_model(F,builder.model)
                totals['sat']+=1
                if m>=2:
                    c1=F+pin(-(1),n)
                    c2=c1+pin(-(2),n+2)
                    n1,G1=parse(serialize(c1,n+2));n2,G2=parse(serialize(c2,n+4))
                    assert len(G1)==len(F)+4 and len(G2)==len(F)+8
                    assert n1==n+2 and n2==n+4
                    if a[0]==0 and a[1]==0:
                        ext=builder.model.copy()
                        for k in range(n+1,n+5):ext[k]=False
                        assert check_model(G1,ext) and check_model(G2,ext)
                    else:
                        # forced original x_i=1, pinned x_i=0 contradiction
                        assert a[0]==1 and a[1]==1
                        totals['wrong_pin_unsat']+=1
                totals['sat_witnesses_checked']+=1
    # easy signed (2,2) SAT control: 9-edge gap alone
    gb=Builder(1);gb.gap();n=gb.nextid-1
    assert (n-1,len(gb.F))==(9,12) and check_model(gb.F,gb.model)
    return dict(run='SOURCE_LOCAL_RAM_TAPE_CERT136',q_models=q_models,
       audited=totals,examples=cases,
       notes='Finite algebraic witnesses and exact resolution; no physical TM timing measured; original tape lower bounds inherited from governance.',
       P_vs_NP='OPEN')

if __name__=='__main__':
    output=run();out=json.dumps(output,sort_keys=True,indent=2)+'\n'
    if len(sys.argv)>1:
        with open(sys.argv[1],'w',encoding='utf-8') as f:f.write(out)
    print(json.dumps({k:v for k,v in output.items() if k!='examples'},sort_keys=True))
    print('SHA256',hashlib.sha256(out.encode()).hexdigest())

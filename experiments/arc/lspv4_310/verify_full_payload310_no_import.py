#!/usr/bin/env python3
"""Independent verification for LSPV-4 FULL-PAYLOAD310, no producer import.
Run in a cloned repo: python experiments/arc/lspv4_310/verify_full_payload310_no_import.py
"""
import ast,collections,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
txt=(ROOT/'experiments/arc/lspv2_296/U198.txt').read_text()
U=[tuple(c) for c in ast.literal_eval(txt[txt.index('[['):])]
V=list(U)
a=list(V[2]);b=list(V[44]);a[2],b[2]=b[2],a[2];V[2]=tuple(a);V[44]=tuple(b)
nodes=0;checks=0
def ck(x,msg='test'):
    global checks
    checks+=1
    assert x,msg
def quota(F,n):
    if len(F)!=4*n//3 or n%3:return False
    p=collections.Counter();q=collections.Counter();seen=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if any(not (1<=abs(x)<=n) for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        (p if c[0]>0 else q).update(map(abs,c))
    return all(p[x]==q[x]==2 for x in range(1,n+1))
def gamma(v):
    b=f'{v:b}';return '0'*(len(b)-1)+b
def binary(F,n):
    w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(f'{abs(x):0{w}b}' for x in c) for c in F)
def satisfied(c,pin):
    return any(abs(x) in pin and pin[abs(x)]==int(x>0) for x in c)
def refute(c,pin):
    return all(abs(x) in pin and pin[abs(x)]!=int(x>0) for x in c)
def solve(F,pin):
    global nodes
    nodes+=1
    a=pin.copy()
    while True:
        forced=None
        for c in F:
            if satisfied(c,a):continue
            free=[x for x in c if abs(x) not in a]
            if not free:return False
            if len(free)==1:forced=free[0];break
        if forced is None:break
        a[abs(forced)]=int(forced>0)
    unfilled=[tuple(x for x in c if abs(x) not in a) for c in F if not satisfied(c,a)]
    if not unfilled:return True
    width=min(map(len,unfilled))
    freq=collections.Counter(abs(x) for c in unfilled for x in c)
    choice=next(c for c in unfilled if len(c)==width)
    v=max(map(abs,choice),key=lambda x:(freq[x],-x))
    a[v]=1
    if solve(F,a):return True
    a[v]=0
    return solve(F,a)
def main():
    ck(quota(U,198));ck(quota(V,198))
    witness=re.search(r"S='([01]+)'",(ROOT/'experiments/arc/lspv1_286/verify_three_core286.py').read_text()).group(1)
    ck(len(witness)==198)
    ck(all(any(witness[abs(x)-1]==str(int(x>0)) for x in c) for c in V))
    eu=binary(U,198);ev=binary(V,198)
    ck([i for i in range(len(eu)) if eu[i]!=ev[i]]==[106,1156])
    h=len(gamma(198))+len(gamma(264));w=198 .bit_length();r=1+3*w
    for original in (U,V):
        for j in range(264*r):
            row=j//r;within=j%r
            F=[list(c) for c in original]
            if within==0:F[row]=[-z for z in F[row]]
            else:
                i=(within-1)//w;bit=(within-1)%w;z=F[row][i]
                F[row][i]=(1 if z>0 else -1)*(abs(z)^(1<<(w-1-bit)))
            ck(not quota(F,198),f'unrejected mutation {j}')
    module=[]
    for i in range(6):
        lo=1+32*i;hi=lo+31
        c=[row for row in U[2:254] if any(lo<=abs(z)<=hi for z in row)]
        ck(len(c)==42)
        ck(all(all(lo<=abs(z)<=hi or abs(z)>=193 for z in row) for row in c))
        module.append(c)
    direct=0;calls=0;refuted=0
    for bits in range(64):
        pin={193+k:(bits>>k)&1 for k in range(6)}
        if any(refute(c,pin) for c in U[:2]):direct+=1;continue
        found=False
        for c in module:
            calls+=1
            if not solve(c,pin):found=True;break
        ck(found,'unrefuted boundary')
        refuted+=1
    ck((direct,refuted,calls)==(16,48,152))
    print(json.dumps({'status':'PASS','assertions':checks,'U198':'UNSAT complete 64-boundary certified',
      'V198':'SAT complete 198-bit witness certified','U_V_bit_distance':2,
      'original_payload_bits_per_input':6600,'single_bit_mutations':13200,
      'direct_boundary_refutations':direct,'private_module_calls':calls,
      'DPLL_nodes':nodes,'P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':main()

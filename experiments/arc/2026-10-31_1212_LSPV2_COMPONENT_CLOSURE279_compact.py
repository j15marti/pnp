#!/usr/bin/env python3
"""LSPV-2 COMPONENT-CLOSURE279 compact independent-gate reproducer.
Usage: python component_closure279_compact.py research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt
For complete source-indexed proof DAG, 7-case raw data and separate verifier,
see the LSPV2_COMPONENT_CLOSURE_HEREDITY279 downloadable research archive.
"""
import ast,collections,hashlib,itertools,json,sys
def valid(F):
    if not F or any(len(c)!=3 or len(set(map(abs,c)))!=3 or sum(z>0 for z in c) not in (0,3) for c in F):return False
    if len({tuple(sorted(c)) for c in F})!=len(F):return False
    n=max(abs(z) for c in F for z in c);p=collections.Counter(z for c in F for z in c)
    return all(p[v]==p[-v]==2 for v in range(1,n+1)) and len(F)*3==n*4
def parts(F):
    ix=collections.defaultdict(list)
    for j,c in enumerate(F):
        for z in c:ix[abs(z)].append(j)
    rest=set(range(len(F)));out=[]
    while rest:
        a=rest.pop();g={a};st=[a]
        while st:
            for z in F[st.pop()]:
                for j in ix[abs(z)]:
                    if j in rest:rest.remove(j);g.add(j);st.append(j)
        out.append(tuple(sorted(g)))
    return sorted(out,key=lambda z:z[0])
def extract(F,ids):
    vs=sorted({abs(z) for j in ids for z in F[j]});mp={v:i+1 for i,v in enumerate(vs)}
    G=[[(-1 if z<0 else 1)*mp[abs(z)] for z in F[j]] for j in ids]
    assert valid(G)
    return G,mp
def gamma(n):
    b=bin(n)[2:];return '0'*(len(b)-1)+b
def encode(G):
    n=max(abs(z) for c in G for z in c);w=n.bit_length()
    return gamma(n)+gamma(len(G))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(z),f'0{w}b') for z in c) for c in G)
def access(F,ids,mp,i):
    n=len(mp);w=n.bit_length();h=gamma(n)+gamma(len(ids))
    if i<len(h):return h[i]
    q,t=divmod(i-len(h),1+3*w);c=F[ids[q]]
    if t==0:return '1' if c[0]>0 else '0'
    slot,bit=divmod(t-1,w)
    return format(mp[abs(c[slot])],f'0{w}b')[bit]
def sublegal(F,ids):
    if not ids:return False
    p=collections.Counter(z for j in ids for z in F[j])
    return all(p[v]==p[-v]==2 for v in set(abs(z) for j in ids for z in F[j]))
def check(F):
    assert valid(F);cp=parts(F);n=len(F);bt=0
    for ids in cp:
        G,mp=extract(F,ids)
        for i,b in enumerate(encode(G)):
            assert access(F,ids,mp,i)==b;bt+=1
    for j in range(n):assert not sublegal(F,[k for k in range(n) if k!=j])
    subtests=0
    if n<=16:
        for mask in range(1,1<<n):
            ids=[j for j in range(n) if (mask>>j)&1]
            want=all(len({(mask>>j)&1 for j in component})==1 for component in cp)
            assert sublegal(F,ids)==want;subtests+=1
    return {'n':max(abs(z) for c in F for z in c),'clauses':n,'components':list(map(len,cp)),'source_bits':len(encode(F)),'checked_child_bits':bt,'one_clause_deletions_rejected':n,'exhaustive_subsets':subtests}
def main(path):
    s=open(path).read();U=ast.literal_eval(s[s.index('[['):])
    V=[c[:] for c in U];assert U[2][2]==197 and U[44][2]==196
    V[2][2],V[44][2]=V[44][2],V[2][2]
    Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
    def join(F,G):
        v=max(abs(z) for c in F for z in c)
        return [c[:] for c in F]+[[(1 if z>0 else -1)*(abs(z)+v) for z in c] for c in G]
    cases={'Y6_SAT':Y,'U198_UNSAT':U,'V198_SAT':V,'Y6_PLUS_Y6_SAT':join(Y,Y),'U198_PLUS_Y6_UNSAT':join(U,Y),'V198_PLUS_Y6_SAT':join(V,Y)}
    ret={name:check(F) for name,F in cases.items()}
    # No classification of U is inferred from the component theorem.
    # U's independently verified source-indexed UNSAT certificate is an
    # external fixture in TARGET-SCOPE278 and in the complete run archive.
    print(json.dumps({'status':'PASS','source_sha256':hashlib.sha256(s.encode()).hexdigest(),'cases':ret},sort_keys=True,indent=2))
if __name__=='__main__':main(sys.argv[1])

#!/usr/bin/env python3
"""Independent no-import source verifier for PAYLOAD-SENSITIVITY284. Run from repo root."""
import collections,itertools,json,pathlib
SRC=pathlib.Path('research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt')
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]

def strict(A,n):
    if n%3 or len(A)*3!=4*n:return False
    count=collections.defaultdict(int);sigs=set()
    for C in A:
        if len(C)!=3 or len(set(map(abs,C)))!=3 or not all(0<abs(z)<=n for z in C) or not all((z>0)==(C[0]>0) for z in C):return False
        k=tuple(sorted(C))
        if k in sigs:return False
        sigs.add(k)
        for z in C:count[(abs(z),z>0)]+=1
    return all(count[(i,b)]==2 for i in range(1,n+1) for b in (True,False))

def word(F,n):
    w=(n-1).bit_length();out=[]
    for C in F:
        out.append(int(C[0]>0))
        for z in C:out.extend(int(q) for q in format(abs(z)-1,f'0{w}b'))
    return out

def decode(b,n):
    w=(n-1).bit_length();step=1+3*w
    if len(b)!=(4*n//3)*step:return None
    rows=[]
    for i in range(0,len(b),step):
        sign=1 if b[i] else -1
        rows.append([sign*(1+int(''.join(map(str,b[i+1+j*w:i+1+(j+1)*w])),2)) for j in range(3)])
    return rows if strict(rows,n) else None

def models(F,n):
    return sum(all(any(a[abs(z)-1]==int(z>0) for z in C) for C in F) for a in itertools.product((0,1),repeat=n))

def small_unsat(F):
    def dec(G):
        while 1:
            if not G:return True
            if any(not c for c in G):return False
            unit=None
            for c in G:
                if len(c)==1:unit=c[0];break
            if unit is None:break
            G=tuple(tuple(v for v in c if v!=-unit) for c in G if unit not in c)
        x=G[0][0]
        return dec(tuple(tuple(v for v in c if v!=-x) for c in G if x not in c)) or dec(tuple(tuple(v for v in c if v!=x) for c in G if -x not in c))
    return not dec(tuple(tuple(C) for C in F))

def original_pair_modes(F):
    cnt=collections.Counter();checks=0
    for i,C in enumerate(F):
        for D in F[i+1:]:
            mode=''
            for wantC,wantD in ((1,1),(1,0),(0,1),(0,0)):
                demands={};ok=True
                for clause,want in ((C,wantC),(D,wantD)):
                    for z in clause:
                        v=abs(z);a=int(z>0)==want
                        if v in demands and demands[v]!=a:ok=False
                        demands[v]=a
                mode+=('1' if ok else '0');checks+=1
            cnt[mode]+=1
    return dict(sorted(cnt.items())),checks

def main():
    s=SRC.read_text();U=json.loads(s[s.find('[['):]);V=[C[:] for C in U];V[2][2],V[44][2]=V[44][2],V[2][2]
    total=0;matrix=0;reports={}
    for name,n,F in [('Y6',6,Y),('U198',198,U),('V198',198,V)]:
        assert strict(F,n)
        x=word(F,n);assert decode(x,n)==F
        for i in range(len(x)):
            x[i]^=1
            assert decode(x,n) is None,(name,i)
            x[i]^=1;total+=1
        modes,c=original_pair_modes(F);matrix+=c
        reports[name]={'bits_checked':len(x),'pair_modes':modes}
    assert models(Y,6)==20
    assert len(W)==198 and all(any((W[abs(z)-1]=='1')==(z>0) for z in C) for C in V)
    modules=[]
    for i in range(6):
        varset=set(range(32*i+1,32*i+33))
        A=[C for C in U[2:254] if set(map(abs,C))&varset]
        assert len(A)==42;modules.append(A)
    seen=0;globalbad=0;calls=0
    for b in itertools.product((0,1),repeat=6):
        pins=dict(zip(range(193,199),b))
        if any(not any(pins[abs(z)]==int(z>0) for z in C) for C in U[:2]):
            seen+=1;globalbad+=1;continue
        for A in modules:
            reduced=[tuple(z for z in C if abs(z)<193) for C in A if not any(abs(z)>192 and pins[abs(z)]==int(z>0) for z in C)]
            calls+=1
            if small_unsat(reduced):seen+=1;break
    assert (seen,globalbad,calls)==(64,16,152)
    assert strict(U+[[int(z>0)*(abs(z)+198)-int(z<0)*(abs(z)+198) for z in C] for C in U],396)
    print(json.dumps({'independent':'PASS','single_bit_mutants_checked':total,'four_mode_checks':matrix,'U_64_rows_proved':seen,'U_global_conflicts':globalbad,'U_local_refutation_calls':calls,'tests':reports},indent=2))

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Read-bit sensitivity on exact Döcker 2P2N sources. No external modules.
Run at repo root: python experiments/arc/lspv1_284/payload_sensitive284_repro.py
"""
import collections, itertools, json, pathlib
SOURCE=pathlib.Path('research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt')
WITNESS='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]

def good(F,n):
    if n<3 or n%3 or len(F)!=4*n//3:return False
    seen=set();deg=collections.Counter()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(abs(x)>n or x==0 for x in c) or len(set(x>0 for x in c))!=1:return False
        sig=tuple(sorted(c))
        if sig in seen:return False
        seen.add(sig)
        deg.update((abs(x),x>0) for x in c)
    return all(deg[(i,s)]==2 for i in range(1,n+1) for s in (False,True))

def bits(F,n):
    w=(n-1).bit_length()
    return ''.join(('1' if c[0]>0 else '0')+''.join(f'{abs(z)-1:0{w}b}' for z in c) for c in F)

def parse(b,n):
    w=(n-1).bit_length();d=1+3*w
    if len(b)!=4*n//3*d or any(c not in '01' for c in b):return None
    F=[]
    for j in range(0,len(b),d):
        sign=1 if b[j]=='1' else -1
        F.append([sign*(int(b[j+1+w*k:j+1+w*(k+1)],2)+1) for k in range(3)])
    return F if good(F,n) else None

def sat(F,a):return all(any(a[abs(x)-1]==(x>0) for x in c) for c in F)

def satisfiable(F):
    # Independent exhaustive DPLL for each small UNSAT boundary module.
    def branch(G):
        while True:
            if not G:return True
            if () in G:return False
            unit=next((c[0] for c in G if len(c)==1),None)
            if unit is None:break
            G=tuple(tuple(z for z in c if z!=-unit) for c in G if unit not in c)
        x=abs(G[0][0])
        return any(branch(tuple(tuple(z for z in c if z!=-lit) for c in G if lit not in c)) for lit in (x,-x))
    return branch(tuple(tuple(c) for c in F))

def u_refute(U):
    M=[]
    for j in range(6):
        lower,upper=32*j+1,32*j+32
        A=[C for C in U[2:254] if any(lower<=abs(x)<=upper for x in C)]
        assert len(A)==42
        M.append(A)
    covered=0;global_bad=0;calls=0
    for b in itertools.product((False,True),repeat=6):
        v={193+j:b[j] for j in range(6)}
        if any(not any(v[abs(x)]==(x>0) for x in c) for c in U[:2]):
            global_bad+=1;covered+=1;continue
        for A in M:
            G=[[x for x in c if abs(x)<=192] for c in A if not any(abs(x)>192 and v[abs(x)]==(x>0) for x in c)]
            calls+=1
            if not satisfiable(G):covered+=1;break
    assert (covered,global_bad,calls)==(64,16,152)
    return {'covered':covered,'global_conflicts':global_bad,'certified_local_calls':calls}

def modes(F):
    h=collections.Counter()
    for i,c in enumerate(F):
        for d in F[i+1:]:
            shared=set(map(abs,c)) & set(map(abs,d))
            h['1111' if not shared else ('1001' if c[0]*d[0]>0 else '0110')]+=1
    return dict(sorted(h.items()))

def main():
    text=SOURCE.read_text();U=json.loads(text[text.index('[['):]);V=[x.copy() for x in U];V[2][2],V[44][2]=V[44][2],V[2][2]
    rows={};total=0
    for tag,n,F in [('Y6_SAT',6,Y),('U198_UNSAT',198,U),('V198_SAT',198,V)]:
        assert good(F,n)
        b=bits(F,n);assert parse(b,n)==F
        for i in range(len(b)):
            flip=b[:i]+('1' if b[i]=='0' else '0')+b[i+1:]
            assert parse(flip,n) is None,(tag,i)
        total+=len(b)
        rows[tag]={'payload_bits':len(b),'one_bit_malformed_neighbors':len(b),'mode_counts':modes(F)}
    assert sum(sat(Y,a) for a in itertools.product((False,True),repeat=6))==20
    assert sat(V,[c=='1' for c in WITNESS]) and len(WITNESS)==198
    rows['U198_UNSAT']['proof']=u_refute(U)
    X=U+[[int(x>0)*(abs(x)+198)-int(x<0)*(abs(x)+198) for x in C] for C in U]
    assert good(X,396)
    summary={'status':'PASS','assertions_one_bit_neighbors':total,'all_sources_valid':True,'both_labels_verified':True,'UNSAT_suffix_escape_bits':264*(1+3*9),'sources':rows,'claim':'Any exact total target-language decider must probe all payload bits on every valid SAT source; no analogous argument for valid UNSAT sources.'}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()

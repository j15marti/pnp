#!/usr/bin/env python3
"""Robust UNKNOWN-domain embedding against unit/pure preprocessing; 25s cap."""
import contextlib,hashlib,io,itertools,json,runpy,signal,time
from pathlib import Path
signal.alarm(25);start=time.monotonic();here=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):
    arc=runpy.run_path(str(here/'2026-10-08_2110_ARC-STRENGTHEN2-test.py'))
old=arc['old'];parity=arc['parity'];scan=arc['scan_star']
def robust(f,n):
    h,r=n+1,n+2
    out=f+((h,-r),(-h,r))
    for v in range(1,n+1):out+=parity((h,v,n+2+v),0)
    return out
def unit_pure(f):
    f=old.normalize(f);assigned={}
    while True:
        if any(not c for c in f):return f,assigned
        unit=next((c[0] for c in f if len(c)==1),None)
        if unit is not None:
            assigned[abs(unit)]=unit>0;f=old.restrict(f,{abs(unit):unit>0});continue
        signs={v:set() for v in old.variables(f)}
        for c in f:
            for lit in c:signs[abs(lit)].add(lit>0)
        pure=next((v for v,s in signs.items() if len(s)==1),None)
        if pure is None:return f,assigned
        val=next(iter(signs[pure]));assigned[pure]=val;f=old.restrict(f,{pure:val})
def covered(f):
    g,a=unit_pure(f)
    if g!=old.normalize(f) or a:return True
    x,_=scan(g)
    return x is not None or old.run_portfolio(g)[0] is not None
clauses=parity((1,2,3),0)+parity((1,2,3),1)
rows=[];extension_checks=0
for mask in range(256):
    f=tuple(c for j,c in enumerate(clauses) if mask>>j&1);g=robust(f,3)
    reduced,a=unit_pure(g);assert reduced==old.normalize(g) and not a
    assert not covered(g)
    tf=old.brute_sat(f);assert old.brute_sat(g)==tf
    for bits in itertools.product((False,True),repeat=3):
        src=dict(zip(range(1,4),bits));h,r=4,5
        ext=src|{h:False,r:False}
        ext|={5+v:src[v] for v in range(1,4)}
        assert old.evaluate(f,src)==old.evaluate(g,ext);extension_checks+=1
    rows.append({'mask':mask,'sat':tf,'clauses':len(g)})
# Renaming/complementing the source does not create a unit or pure variable.
hostile=0
for n in (3,4,5,6):
    base=tuple(tuple(((v+i-1)%n)+1 for i in range(3)) for v in range(1,n+1))
    for flip in itertools.product((False,True),repeat=n):
        f=tuple(tuple(-v if flip[v-1] else v for v in c) for c in base)
        g=robust(f,n);assert unit_pure(g)==(old.normalize(g),{}) and not covered(g)
        assert old.brute_sat(g)==old.brute_sat(f);hostile+=1
# Direct fixed-layout bit encoding length and bitwise construction checks.
def gamma(x):
    b=bin(x)[2:];return '0'*(len(b)-1)+b
def enc(f,n):
    w=n.bit_length();return gamma(n+1)+gamma(len(f)+1)+''.join(format(len(c),'02b')+''.join(('1' if v>0 else '0')+format(abs(v),f'0{w}b') for v in c) for c in f)
def parse_header(s):
    pos=0;vals=[]
    for _ in range(2):
        k=0
        while s[pos]=='0':k+=1;pos+=1
        vals.append(int(s[pos:pos+k+1],2)-1);pos+=k+1
    return vals[0],vals[1],pos
def outbit(source,j):
    n,m,hs=parse_header(source);nn=2*n+2;gad=robust((),n)
    hh=gamma(nn+1)+gamma(m+len(gad)+1)
    if j<len(hh):return hh[j]
    j-=len(hh);w=n.bit_length();ww=nn.bit_length();l3=2+3*(1+ww);l2=2+2*(1+ww)
    if j<m*l3:
        c,t=divmod(j,l3)
        if t<2:return '1'
        lit,t=divmod(t-2,1+ww);src=hs+c*(2+3*(1+w))+2+lit*(1+w)
        if t==0:return source[src]
        if t<=ww-w:return '0'
        return source[src+t-(ww-w)]
    j-=m*l3
    if j<2*l2:i,t=divmod(j,l2)
    else:i,t=divmod(j-2*l2,l3);i+=2
    c=gad[i]
    if t<2:return format(len(c),'02b')[t]
    lit,t=divmod(t-2,1+ww);v=c[lit]
    return ('1' if v>0 else '0') if t==0 else format(abs(v),f'0{ww}b')[t-1]
bitchecks=0;encoding=[]
for n in (3,4,7,8,15,16,31,32):
    f=tuple((v, -((v%n)+1), ((v+1)%n)+1) for v in range(1,n+1))
    source=enc(f,n);out=enc(robust(f,n),2*n+2)
    rebuilt=''.join(outbit(source,j) for j in range(len(out)));assert rebuilt==out
    assert len(out)<=20*len(source)+500
    bitchecks+=len(out);encoding.append({'n':n,'input_bits':len(source),'output_bits':len(out),'ratio':len(out)/len(source)})
signal.alarm(0)
print(json.dumps({'status':'COMPUTATIONAL','passed':True,'seed':None,'exhaustive_source_formulas':256,
 'source_assignment_extensions':extension_checks,'renaming_complement_controls':hostile,
 'encoded_bits_checked':bitchecks,'encoding':encoding,'seconds':time.monotonic()-start,
 'source_commit':'e1082f783dd7f237afe8d92bb63dad291afa1aba',
 'authenticated_source_git_blob':'51f0a58467370a04284aee4c1cccfd97a4a61f91',
 'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'authenticated_source_sha256':hashlib.sha256((here/'2026-10-08_2110_ARC-STRENGTHEN2-original-portfolio.py').read_bytes()).hexdigest(),
 'limitations':['Finite validation only; infinite embedding theorem is symbolic.','No favorable fallback bound or P-versus-NP separation.','Python memory does not certify the stated random-access bit generator.']},indent=2))

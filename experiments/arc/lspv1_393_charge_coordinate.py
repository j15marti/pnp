#!/usr/bin/env python3
"""LSPV-1/393: fixed source, two polynomially equivalent canonical encodings.
Deterministic producer with exhaustive small Tseitin controls and adversarial inputs.
"""
import json, itertools, hashlib, pathlib

OUT=pathlib.Path('results/raw/arc/2026-11-04_0900_LSPV1_CHARGE_COORDINATE393_raw.json')

def gamma(n):
    assert n>=1
    b=format(n,'b')
    return '0'*(len(b)-1)+b

def read_gamma(s,start):
    z=start
    while z<len(s) and s[z]=='0':z+=1
    if z>=len(s):raise ValueError('truncated gamma')
    digits=z-start+1
    if z+digits>len(s):raise ValueError('truncated gamma tail')
    return int(s[z:z+digits],2),z+digits

def graph(h):
    if h==4:
        return sorted((i,j) for i in range(4) for j in range(i+1,4))
    if h<6 or h%2:raise ValueError('unsupported template h')
    m=h//2
    e=set()
    for i in range(m):
        e.add(tuple(sorted((i,(i+1)%m))))
        e.add(tuple(sorted((m+i,m+(i+1)%m))))
        e.add((i,m+i))
    return sorted(e)

def formula(h,chi):
    edges=graph(h)
    incidence={v:[] for v in range(h)}
    for ix,(a,b) in enumerate(edges):
        incidence[a].append(ix); incidence[b].append(ix)
    clauses=[]
    for v in range(h):
        inds=sorted(incidence[v]);assert len(inds)==3
        for local in itertools.product((0,1), repeat=3):
            if (sum(local)%2)==chi[v]:continue
            clauses.append([(ix+1, b==0) for ix,b in zip(inds,local)])
    assert len(clauses)==4*h
    return clauses,len(edges)

def models(clauses,vars_count):
    for mask in range(1<<vars_count):
        if all(any(((mask>>(i-1))&1)==int(pos) for i,pos in C) for C in clauses):
            yield mask

def encode0(clauses,varcount):
    m=len(clauses)
    width=(varcount+1).bit_length()
    header='1011'+gamma(varcount+1)+gamma(m+1)
    stream=''.join(gamma(len(C)+1)+''.join(str(int(pos))+format(ix,f'0{width}b') for ix,pos in C) for C in clauses)
    return header+stream

def decode0(s):
    if not s.startswith('1011'): raise ValueError('bad source tag')
    V,z=read_gamma(s,4); M,z=read_gamma(s,z)
    V-=1;M-=1
    if V<1 or M<0:raise ValueError('illegal v,m')
    if V>len(s) or M>len(s):raise ValueError('illegal excessive count')
    w=(V+1).bit_length();F=[]
    for _ in range(M):
        k,z=read_gamma(s,z);k-=1
        if k<1 or k>V or k>len(s): raise ValueError('bad clause width')
        c=[];prev=0
        for _ in range(k):
            if z+1+w>len(s):raise ValueError('truncated literal')
            sign=s[z]=='1';idx=int(s[z+1:z+1+w],2);z+=1+w
            if idx<=prev or idx>V:raise ValueError('noncanonical IDs')
            prev=idx;c.append((idx,sign))
        F.append(c)
    if z!=len(s):raise ValueError('trailing garbage')
    return F,V

def to_encoded1(h,chi):
    assert len(chi)==h and (h==4 or (h>=6 and h%2==0))
    y=[sum(chi)%2]+list(chi[1:])
    return '1'+gamma(h+1)+''.join(map(str,y))

def e1_parse(s):
    if not s: raise ValueError('empty')
    if s[0]=='1':
        h,z=read_gamma(s,1);h-=1
        if not (h==4 or h>=6 and h%2==0):raise ValueError('invalid template size')
        if len(s)-z!=h:raise ValueError('template length invalid')
        y=list(map(int,s[z:]));chi=[(y[0]+sum(y[1:]))%2]+y[1:]
        return 'special',h,chi
    if s[0]=='0':
        F,V=decode0(s[1:])
        if detect_template(F,V) is not None:raise ValueError('noncanonical tag0 template')
        return 'general',F,V
    raise ValueError('bad tag')

def detect_template(F,V):
    if len(F)%4:return None
    h=len(F)//4
    if not (h==4 or h>=6 and h%2==0):return None
    try:
        edges=graph(h)
        if V!=len(edges):return None
        inc={v:[] for v in range(h)}
        for ix,(u,v) in enumerate(edges):inc[u].append(ix);inc[v].append(ix)
        chi=[]
        for v in range(h):
            segment=F[4*v:4*v+4]
            expected_ids=[e+1 for e in sorted(inc[v])]
            if any([i for i,_ in C]!=expected_ids for C in segment):return None
            patterns=[]
            for C in segment:
                forbidden=tuple(0 if positive else 1 for _,positive in C)
                patterns.append(forbidden)
            parity={sum(p)%2 for p in patterns}
            if len(parity)!=1:return None
            chi.append(1-next(iter(parity)))
        Fcheck,_=formula(h,chi)
        return (h,chi) if Fcheck==F else None
    except ValueError:return None

def encode1_from_e0(s):
    F,V=decode0(s);t=detect_template(F,V)
    if t is None:return '0'+s
    h,chi=t
    return to_encoded1(h,chi)

def encode0_from_e1(s):
    typ,p,q=e1_parse(s)
    if typ=='special':
        F,V=formula(p,q)
        return encode0(F,V)
    return encode0(p,q)

def tag1_query(s):
    # Original bit-length is supplied by the random-access input interface.
    L=len(s);reads=set()
    def read(i):
        reads.add(i)
        return s[i] if i<L else None
    first=read(0)
    if first != '1':return None,len(reads),False
    pos=1;zeros=0
    while read(pos)=='0':
        zeros+=1;pos+=1
        if pos>=L: return 'M',len(reads),True
    pos+=1
    bits='1'
    for i in range(zeros):
        x=read(pos+i)
        if x is None:return 'M',len(reads),True
        bits+=x
    pos+=zeros;h=int(bits,2)-1
    if not (h==4 or h>=6 and h%2==0) or pos+h!=L:return 'M',len(reads),True
    return ('U' if read(pos)=='1' else 'S'),len(reads),True

def full_decide_e1(s):
    ans,reads,hit=tag1_query(s)
    if hit:return ans,reads
    try:
        typ,F,V=e1_parse(s)
        assert typ=='general'
        return ('S' if next(models(F,V),None) is not None else 'U'),len(s)
    except ValueError:return 'M',len(s)

def brute_class(clauses,V):return 'S' if next(models(clauses,V),None) is not None else 'U'

def main():
    checks=0;records=[];examples=[]
    for h in (4,6,8,10):
        cases=[]
        for label,chi in [('odd',[1]+[0]*(h-1)),('even',[0]*h)]:
            F,V=formula(h,chi)
            s0=encode0(F,V)
            assert decode0(s0)==(F,V);checks+=1
            s1=encode1_from_e0(s0)
            assert s1==to_encoded1(h,chi);checks+=1
            assert encode0_from_e1(s1)==s0;checks+=1
            assert e1_parse(s1)==('special',h,chi);checks+=1
            fast,probes,sp=tag1_query(s1)
            assert sp and fast==('U' if label=='odd' else 'S');checks+=1
            yes=sum(1 for _ in models(F,V))
            assert (yes==0 if label=='odd' else yes==(1<<(V-h+1)));checks+=1
            for payload in range(1<<h):
                cp=[(payload>>i)&1 for i in range(h)]
                s=to_encoded1(h,cp)
                observed,count,_=tag1_query(s)
                assert observed==('U' if sum(cp)%2 else 'S');checks+=1
                assert encode0_from_e1(s)==encode0(*formula(h,cp));checks+=1
            case={'label':label,'h':h,'e0_bits':len(s0),'e1_bits':len(s1),
                  'e1_probes':probes,'num_models':yes,'clauses':len(F),'signs':sum(map(len,F)),
                  'logical_node_min':4*h-1 if label=='odd' else None,
                  'e0_sha256':hashlib.sha256(s0.encode()).hexdigest(),
                  'e1_sha256':hashlib.sha256(s1.encode()).hexdigest()}
            if label=='odd':
                sign_positions=[];z=4+len(gamma(V+1))+len(gamma(len(F)+1));w=(V+1).bit_length()
                for C in F:
                    z+=len(gamma(len(C)+1))
                    for j in range(len(C)):
                        sign_positions.append(z);z+=1+w
                assert z==len(s0) and len(sign_positions)==12*h;checks+=1
                for idx,pos in enumerate(sign_positions):
                    sf=s0[:pos]+('1' if s0[pos]=='0' else '0')+s0[pos+1:]
                    Fc,Vc=decode0(sf)
                    assert Vc==V and len(sf)==len(s0) and brute_class(Fc,V)=='S';checks+=1
                    if idx==0:examples.append({'h':h,'source_clause_sign_flip':idx,'is_sat':True})
                case['verified_single_sign_flip_SAT']=len(sign_positions)
            cases.append(case)
        records.extend(cases)
    bad=['', '1', '101', '1'+gamma(5)+'0'*3,'1'+gamma(5)+'0'*5+'1', '0', '01111', '11','0'+encode0(*formula(4,[1,0,0,0]))]
    for s in bad:
        assert full_decide_e1(s)[0]=='M';checks+=1
    for F,V,want in [([[(1,True)]],1,'S'),([[(1,True)],[(1,False)]],1,'U')]:
        z='0'+encode0(F,V)
        assert full_decide_e1(z)[0]==want;checks+=1
    out={'result_id':'LSPV1_393','status':'COMPUTATIONAL FINITE CONTROLS ONLY',
         'description':'Explicit charge-coordinate recoding of cubic odd/even Tseitin CNFs',
         'checks':checks,'records':records,'malformed_rejected':len(bad),
         'signed_neighbor_cases':sum(r.get('verified_single_sign_flip_SAT',0) for r in records),
         'family_notes':'K4 h4; prism graphs h6,8,10; tests do not certify expander Resolution hardness',
         'examples':examples}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','examples')}))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""LSPV-1 357: finite signed SAT marker/consistency-guard wrapper controls.
This tests a symbolic incompleteness theorem's finite direction. It does not
prove PA consistency or implement an all-input polynomial SAT solver.
"""
import hashlib, itertools, json, sys

def encode(p):
    assert set(p) <= {'0','1'}
    out = 'p cnf {0} {0}\n1 0\n'.format(len(p) + 1)
    for i, bit in enumerate(p):
        v = (i + 2) * (1 if bit == '1' else -1)
        out += str(v) + ' 0\n'
    return out

def parse(src):
    if not isinstance(src,str) or not src.endswith('\n'): return None
    rows=src.splitlines()
    if not rows: return None
    h=rows.pop(0).split()
    if len(h)!=4 or h[:2]!=['p','cnf'] or not all(s.isdigit() and str(int(s))==s for s in h[2:]):return None
    n,m=map(int,h[2:])
    if n>20 or m>100 or len(rows)!=m:return None   # finite-test parser, not general SAT
    clauses=[]
    for row in rows:
        ss=row.split()
        if not ss:return None
        try: v=[int(t) for t in ss]
        except ValueError:return None
        if len(v)!=len(ss) or any(str(a)!=t for a,t in zip(v,ss)) or v[-1]!=0:return None
        if any(a==0 or abs(a)>n for a in v[:-1]):return None
        clauses.append(v[:-1])
    return n,clauses

def decode(src):
    obj=parse(src)
    if obj is None:return None
    n,rows=obj
    if not n or len(rows)!=n or rows[0]!=[1]:return None
    p=''
    for i in range(1,n):
        if rows[i]==[i+1]:p+='1'
        elif rows[i]==[-i-1]:p+='0'
        else:return None
    return p if encode(p)==src else None

def truth(src):
    obj=parse(src)
    if obj is None:return 'MALFORMED'
    n,rows=obj
    for a in itertools.product((0,1),repeat=n):
        if all(any((lit>0)==bool(a[abs(lit)-1]) for lit in clause) for clause in rows):
            return 'SAT'
    return 'UNSAT'

def wrapper(src,proof_checker):
    p=decode(src)
    return 'UNSAT' if p is not None and proof_checker(p) else truth(src)

def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def main():
    cases=[]
    for n in range(7):
        for j in range(1<<n):
            p=format(j,'0{}b'.format(n)) if n else ''
            source=encode(p)
            a=truth(source)
            safe=wrapper(source,lambda p:False)
            bad=wrapper(source,lambda p:p=='101')
            assert a==safe=='SAT' and decode(source)==p
            cases.append({'p':p,'N_bits':len(source.encode())*8,
                          'sha256':digest(source),'true_label':a,
                          'safe_label':safe,'hostile_label':bad})
    fixtures={
     'unsat':'p cnf 1 2\n1 0\n-1 0\n',
     'sat_nonmarker':'p cnf 2 1\n1 2 0\n',
     'malformed_header':'p cnf 1 WRONG\n1 0\n',
     'malformed_count':'p cnf 1 2\n1 0\n',
     'malformed_terminator':'p cnf 1 1\n1\n',
     'malformed_out_of_range':'p cnf 1 1\n2 0\n',
     'malformed_trailing':'p cnf 1 1\n1 0\njunk\n',
     'mutated_marker':'p cnf 4 4\n1 0\n3 0\n-2 0\n4 0\n',
    }
    controls=[{'name':n,'text':s,'expected':truth(s),
               'recognized':decode(s) is not None,'sha256':digest(s)} for n,s in fixtures.items()]
    data={'run_id':'LSPV1_GODEL_REFLECTION_B3_FIREWALL357',
      'status':'COMPUTATIONAL finite signed wrapper controls only, not arithmetic incompleteness verification',
      'marker_count':len(cases),
      'hostile_error_p':[c['p'] for c in cases if c['hostile_label']!=c['true_label']],
      'markers':cases,'controls':controls}
    assert len(cases)==127 and data['hostile_error_p']==['101']
    output=sys.argv[1] if len(sys.argv)>1 else 'LSPV1_GODEL_REFLECTION_B3_FIREWALL357_raw.json'
    with open(output,'w',encoding='utf8') as out:json.dump(data,out,indent=2)
    print(json.dumps({'markers':len(cases),'controls':len(controls),'fake_proof_error':['101'],
                      'output':output,'sha256':hashlib.sha256(open(output,'rb').read()).hexdigest()}))
if __name__=='__main__':main()

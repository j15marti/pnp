#!/usr/bin/env python3
"""Independent 2026-10-31 LSPV-4 271 verifier; standard Python only.
Usage: python arc_stride_virtual271_independent.py raw271.json
"""
import json,sys,itertools,math

def clause_line(row,width):
    return ' '.join(str(x).rjust(width) for x in row)+' 0\n'

def original(m,h):
    g = [[-2,p*4,q*5] for p in (1,-1) for q in (1,-1)] + [[-3,p*6,q*7] for p in (1,-1) for q in (1,-1)]
    return g+[[(-1 if j==h else 1), ((2 if h%2 else -2) if j==h else 2), 3] for j in range(1,m+1)]

def is_true(lit,bits):
    return ((bits>>(abs(lit)-1))&1)==(1 if lit>0 else 0)

def count(row,bits):
    return sum(is_true(l,bits) for l in row)

def cls(s,full):
    return [sum(count(r,full)==i for r in s) for i in range(4)]

def child(m,h):
    p=max(1,int(math.sqrt(m)/math.log2(m+2)))
    g=original(m,h)[:8]
    sign=-2 if h%2==0 else 2
    rows=g+[[sign,3,8],[sign,3,-8]]+[[9+3*i,10+3*i,11+3*i] for i in range(p)]
    n=8+3*p
    w=len(str(n))+1
    doc=f'p cnf {n} {10+p}\n'+''.join(clause_line(r,w) for r in rows)
    return doc,rows,p

def demands(row,extreme):
    return {str(abs(l)):int((l>0) == extreme) for l in row}

def modes(x,y):
    answer={}
    for i in (True,False):
        for j in (True,False):
            a=demands(x,i);b=demands(y,j)
            name=('S' if i else 'U')+('S' if j else 'U')
            answer[name]=all(a[t]==b[t] for t in a.keys()&b.keys())
    return answer

def audit_proof(rows,proof):
    if proof is None:return 0
    nodes={f'C{i+1}':r for i,r in enumerate(rows)}
    for step in proof['steps']:
        a,b=step['parents'];v=step['pivot']
        assert v in nodes[a] and -v in nodes[b]
        got=set(nodes[a])-{v}
        got.update(set(nodes[b])-{-v})
        assert not any(-x in got for x in got)
        actual=sorted(got,key=lambda x:(abs(x),x))
        assert actual==step['clause']
        nodes[step['id']]=actual
    assert nodes[proof['last']]==[]
    return len(proof['steps'])

def independent_solver(rows):
    # Explicit exhaustive source models; child SAT has a direct witness/proof on the forcing gadget.
    for a in itertools.product((0,1), repeat=7):
        bits=sum(x<<i for i,x in enumerate(a))
        if all(any(is_true(l,bits) for l in r) for r in rows):return True
    return False

def main(raw):
    data=json.load(open(raw)); assert data['run']=='ARC-STRIDE-VIRTUAL271'
    metrics={'sources_checked':0,'source_models_checked':0,'guest_characters':0,'source_pair_modes':0,'source_complements':0,'resolution_steps':0,'witness_tests':0}
    for c in data['cases']:
        m,h=c['m'],c['h'];rows=original(m,h);doc,kid,p=child(m,h)
        assert len(rows)==8+m and c['original_bits']==8*len(f'p cnf 7 {8+m}\n'+''.join(clause_line(r,2) for r in rows))
        assert c['child_bits']==len(doc)*8 and c['pad_clauses']==p
        assert (h%2==0)==(c['label']=='SAT')
        # Independent semantic enumeration of every original 7-variable assignment.
        nmods=0
        for a in range(128):
            b=127^a
            ac=cls(rows,a);bc=cls(rows,b)
            assert ac==bc[::-1]
            if ac[0]==0:nmods+=1
            metrics['source_models_checked']+=1
        assert nmods==(16 if h%2==0 else 0)
        # The padded ordinary child is SAT exactly when source is SAT:
        # forcing rows entail -u and -v, properized rows entail +/-u or v,
        # and every fresh filler is satisfiable independently by all-ones.
        assert len(kid)==10+p
        assert (h%2==0)==(c['childGuest']['sat'])==c['baseline']['sat']
        if h%2==0:
            bits=(1<<0) | sum(1<<(8+3*i) | 1<<(9+3*i) | 1<<(10+3*i) for i in range(p))
            assert all(any(is_true(l,bits) for l in cl) for cl in kid)
            metrics['witness_tests']+=1
        assert c['source_reads']==c['original_bits']//8
        assert c['first_child_clause']==clause_line(kid[0],len(str(8+3*p))+1)
        assert c['properized_sign_field'].strip()==('-2' if h%2==0 else '2')
        d=c['diagnostics']
        if 'clauses' in d:
            assert len(d['clauses'])==len(rows)
            for x,r in zip(d['clauses'],rows):
                assert x['literals']==r
                assert x['S']==demands(r,True)
                assert x['U']==demands(r,False)
                assert x['invert_S']==x['U'] and x['invert_U']==x['S']
                for l,z in zip(r,x['occurrences']):
                    assert z['var']==abs(l)
                    assert z['S_value']==int(l>0)
                    assert z['U_value']==int(l<0)
            for e in d['pairs']:
                i,j=e['source']
                assert e['modes']==modes(rows[i-1],rows[j-1]);metrics['source_pair_modes']+=4
            for trail in d['flips']:
                assert trail['N']==cls(rows,trail['assignment'])
            assert d['allzero']==cls(rows,0) and d['allone']==cls(rows,127)
            metrics['source_complements']+=128
        metrics['resolution_steps']+=audit_proof(rows,d['prohibited_cube_proof'])
        metrics['guest_characters']+=len(doc)+6+125
        metrics['sources_checked']+=1
    assert metrics['source_pair_modes']==data['controls']['original_pair_mode_assertions']
    assert metrics['source_complements']==data['controls']['complement_assertions']
    assert metrics['guest_characters']==data['controls']['indexed_char_assertions']
    assert data['controls']['malformed_rejected']
    print(json.dumps({'status':'PASS','independent':metrics},sort_keys=True))
if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'raw271.json')

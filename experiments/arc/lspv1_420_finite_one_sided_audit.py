#!/usr/bin/env python3
"""LSPV-1/420 bounded one-sided rejection-soundness reduction.
Stdlib only. Exhaustive signed CNFs on 2 vars and all full 3-clauses on 3 vars.
Scientific claim is symbolic. Finite tests are hostile controls, not complexity evidence.
"""
import hashlib, itertools, json, sys, pathlib

OUT=pathlib.Path(__file__).with_name('raw420.json')

def sat_clause(clause, w):
    return any((w[abs(l)-1] if l>0 else not w[abs(l)-1]) for l in clause)

def eval_cnf(clauses,w):
    return all(sat_clause(c,w) for c in clauses)

def assignments(n):
    return itertools.product((False,True),repeat=n)

def strict_sentinel(w):
    n=len(w); z=n+1
    return ('p cnf %d %d\n'%(z,n))+''.join('%d %d 0\n'%(z,i+1 if v else -(i+1)) for i,v in enumerate(w))

def decode_sentinel(s,n):
    # Strict deterministic byte language: exactly this canonical spelling.
    if not isinstance(s,str): return None
    prefix='p cnf %d %d\n'%(n+1,n)
    if not s.startswith(prefix):return None
    lines=s[len(prefix):].splitlines(keepends=True)
    if len(lines)!=n:return None
    w=[]
    for i,line in enumerate(lines):
        if line==('%d %d 0\n'%(n+1,i+1)):w.append(True)
        elif line==('%d %d 0\n'%(n+1,-(i+1))):w.append(False)
        else:return None
    return tuple(w)

def reject_sentinel(cnf,n,text):
    w=decode_sentinel(text,n)
    return w is not None and eval_cnf(cnf,w)

def parse_strict_dimacs(s):
    try:
        if not isinstance(s,str): return None
        lines=s.splitlines(keepends=True)
        if not lines or not lines[0].endswith('\n'):return None
        h=lines[0].strip().split()
        if len(h)!=4 or h[0]!='p' or h[1]!='cnf':return None
        n=int(h[2]);m=int(h[3]);
        if n<0 or m<0 or n>1_000_000 or m>1_000_000:return None
        if len(lines)!=m+1:return None
        cls=[]
        for line in lines[1:]:
            if not line.endswith('\n'):return None
            a=[int(x) for x in line.split()]
            if not a or a[-1]!=0 or any(l==0 or abs(l)>n for l in a[:-1]):return None
            cls.append(tuple(a[:-1]))
        return (n,cls)
    except (ValueError,TypeError):return None

def program_A_G(cnf,n,text):
    if parse_strict_dimacs(text) is None: return 'INVALID'
    return 'UNSAT' if reject_sentinel(cnf,n,text) else 'SAT'

def source2_universe():
    return ((1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2))

def source3_universe():
    return tuple(tuple((i+1 if mask & (1<<i) else -(i+1)) for i in range(3)) for mask in range(8))

def main():
    stats={};count=0; bad=0; misparsed=0;bad_controls=0
    records=[]
    for n,universe in ((2,source2_universe()),(3,source3_universe())):
        stat={'formulas':0,'sat':0,'unsat':0,'sentinels':0,'rejects':0,'consistency_tests':0,'pass':True}
        assert len(universe)==8
        for mask in range(256):
            cnf=tuple(c for i,c in enumerate(universe) if mask&(1<<i))
            ws=list(assignments(n)); satisfiers=[w for w in ws if eval_cnf(cnf,w)]
            stat['formulas']+=1
            stat['sat' if satisfiers else 'unsat']+=1
            rejects=[]
            for w in ws:
                s=strict_sentinel(w)
                assert decode_sentinel(s,n)==w
                f=parse_strict_dimacs(s)
                assert f and f[0]==n+1 and len(f[1])==n
                assert eval_cnf(f[1], tuple(w)+(True,))  # z is true
                out=program_A_G(cnf,n,s)
                assert out in ('SAT','UNSAT')
                assert (out=='UNSAT') == eval_cnf(cnf,w)
                if out=='UNSAT':rejects.append(''.join('1' if v else '0' for v in w))
                stat['consistency_tests']+=4;count+=4
            assert (len(rejects)==0)==(not satisfiers)
            assert len(rejects)==len(satisfiers)
            stat['sentinels']+=len(ws);stat['rejects']+=len(rejects)
            count+=2
            if mask in (0,1,127,255):
                records.append({'n':n,'mask':mask,'satisfiers':len(satisfiers),'rejects':rejects,'clauses':[list(c) for c in cnf]})
        stats[f'n{n}']=stat
    for n in (2,3,4):
        good=strict_sentinel(tuple(False for _ in range(n)))
        for mutation in (good+'extra\n',good.replace('p cnf','q cnf'),good.replace(' 0\n',' 1\n',1),good.replace('\n','\r\n'),good[:-1],good.replace('p cnf '+str(n+1),'p cnf 3',1) if n+1!=3 else good.replace('p cnf 3','p cnf 4',1)):
            assert decode_sentinel(mutation,n) is None
            count+=1;bad_controls+=1
        assert program_A_G((tuple([1]),),n,'bad input')=='INVALID'
        count+=1;bad_controls+=1
    for n,cnf,expected in [
      (2,((1,),(-1,)),False),
      (2,((1,),),True),
      (3,((1,),(-1,),(2,)),False),
      (3,((1,2,3),),True),
      (3,tuple(source3_universe()),False)
    ]:
        rs=[reject_sentinel(cnf,n,strict_sentinel(w)) for w in assignments(n)]
        assert any(rs)==expected
        count+=1
    raw={'run':'LSPV1_420','status':'COMPUTATIONAL finite checks; symbolic coNP-completeness theorem in report','assertions':count,'hostile_controls':bad_controls,'stats':stats,'sample_records':records,'seed':None,'randomized':False,'note':'A_G not a correct SAT decider; conditional B_G uses hypothetical correct P-time D, not executed'}
    OUT.write_text(json.dumps(raw,indent=2)+'\n')
    print(json.dumps({'assertions':count,'hostile_controls':bad_controls,'stats':stats,'raw':str(OUT)}))

if __name__=='__main__':main()

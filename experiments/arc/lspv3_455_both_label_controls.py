#!/usr/bin/env python3
"""Independent finite bit-PHP strict-3 existential chain semantics and corruption controls."""
import itertools, tempfile, pathlib, json, copy
from lspv3_455_third_checker import expected_family, read_cnf, verify


def sat_clause(cl, assignment):
    return any(assignment[abs(a)] == (a > 0) for a in cl)


def expanded_models(h, p):
    """For ell=2: reconstruct all chains and project their auxiliary bits exactly."""
    assert h == 4
    ell=2
    full_m=p
    source_m=(p-1)*ell
    triples=[]
    nextvar=p*ell
    # 4 pigeons case needs own reconstructed source rather than private data from checker.
    for a in range(p):
        for b in range(a+1,p):
            for hole in range(h):
                bits=[(hole>>(1-t))&1 for t in range(ell)]
                lits=[]
                for owner in (a,b):
                    for j in range(ell):
                        v=owner*ell+j+1
                        lits.append(v if bits[j]==0 else -v)
                nextvar+=1
                z=nextvar
                triples.append(((lits[0],lits[1],z),(-z,lits[2],lits[3])))
    models=0
    for labels in itertools.product(range(h), repeat=p):
        val={a*ell+j+1:bool((labels[a]>>(1-j))&1) for a in range(p) for j in range(ell)}
        exists=True
        for c1,c2 in triples:
            z=abs(c1[2]);solvable=False
            for zb in (False,True):
                val[z]=zb
                if sat_clause(c1,val) and sat_clause(c2,val):solvable=True;break
            if not solvable:exists=False;break
        assert exists == (len(set(labels))==p), (labels,exists)
        models+=exists
    return {'pigeons':p,'holes':h,'number_of_assignments':h**p,'satisfiable_projected_assignments':models,'expected':24 if p==4 else 0}


def malformed_tests(orig):
    def assert_bad(b, tag):
        with tempfile.TemporaryDirectory() as d:
            q=pathlib.Path(d)/'corrupt.cnf';q.write_bytes(b)
            try:read_cnf(q)
            except (ValueError,AssertionError,UnicodeDecodeError):return 'REJECTED'
            raise AssertionError('bad source accepted '+tag)
    lines=orig.splitlines(keepends=True)
    return {
      'header_clause_count':assert_bad(orig.replace(b'p cnf 50 80',b'p cnf 50 81',1),'header count'),
      'missing_source_clause':assert_bad(b''.join(lines[:-1]),'missing source'),
      'missing_line_terminator':assert_bad(orig.replace(b' 0\n',b' 7\n',1),'terminator'),
      'out_of_range_source_literal':assert_bad(b''.join([lines[0], b'9999 '+ b' '.join(lines[1].split()[1:])+b'\n']+lines[2:]),'range'),
      'non_ascii_header':assert_bad(b'\xff'+orig,'ASCII'),
    }


if __name__=='__main__':
    import sys
    raw=json.load(open(sys.argv[1]));cnf=pathlib.Path(sys.argv[2]); assert raw['ell']==2
    result={'paired_sat':expanded_models(4,4),'paired_unsat':expanded_models(4,5),'malformed_controls':malformed_tests(cnf.read_bytes())}
    assert result['paired_sat']['satisfiable_projected_assignments']==24
    assert result['paired_unsat']['satisfiable_projected_assignments']==0
    assert all(v=='REJECTED' for v in result['malformed_controls'].values())
    print(json.dumps(result,indent=2))

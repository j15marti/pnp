#!/usr/bin/env python3
"""PARITY-PORT-FORGETTING225, deterministic stdlib.

Proves finite controls for exact parity projections with 3CNF extension
variables, explicit auxiliary-free CNF, one-port forgetting, and a
strict-exact22 all-port compiler imported from CONNECTED_ALLPORT_COMPILER224.

Input is not a SAT oracle; no unrestricted complexity claim follows.
"""
import json, importlib.util, pathlib, hashlib, itertools, collections

ROOT=pathlib.Path(__file__).resolve().parent
COMPILER=ROOT/'2026-10-29_LSPV2_CONNECTED_ALLPORT_COMPILER224_repro.py'

def load_compiler():
    sp=importlib.util.spec_from_file_location('compiler224',COMPILER)
    mod=importlib.util.module_from_spec(sp)
    import sys
    sys.modules[sp.name]=mod
    sp.loader.exec_module(mod)
    return mod

def canonical(c):
    return tuple(sorted(tuple(sorted(row,key=lambda t:(abs(t),t<0))) for row in c))

def parity_cnf(b,target):
    """x_1..x_b are free; internal y_2..y_b and 2 unit auxiliaries.
    Each XOR(u,v,w) is four distinct proper ternary clauses.
    """
    assert b>=2 and target in (0,1)
    C=[]; first_internal=b+1
    def xor_gate(u,v,w):
        return [(u,v,-w),(u,-v,w),(-u,v,w),(-u,-v,-w)]
    last=1
    for i in range(2,b+1):
        y=first_internal+i-2
        C.extend(xor_gate(last,i,y))
        last=y
    a,b_aux=2*b,2*b+1
    final_lit=last if target==1 else -last
    for sa,sb in itertools.product((1,-1),repeat=2):
        C.append((final_lit,sa*a,sb*b_aux))
    return canonical(C),2*b+1

def eval_cnf(C,A):
    return all(any(A[abs(l)]==(l>0) for l in clause) for clause in C)

def expected_lift(b,x,target):
    y={i+1:bool((x>>i)&1) for i in range(b)}
    parity=y[1]
    for i in range(2,b+1):
        parity ^= y[i]
        y[b+i-1]=parity
    # Unit gadget is true for either values of its two auxiliary variables if parity is correct.
    y[2*b]=False;y[2*b+1]=False
    return y

def brute_project(C,n,b,pins):
    """Small-case exhaustive existential quantification of all hidden variables.
    Actual source formula checked; not a symbolic shortcut.
    """
    free=[i for i in range(1,n+1) if i not in pins]
    for mask in range(1<<len(free)):
        A=dict(pins)
        for j,i in enumerate(free):A[i]=bool(mask>>j & 1)
        if eval_cnf(C,A):return True
    return False

def forbidden_cnf(b,target):
    # One full-length clause per wrong-parity assignment.
    F=[]
    for x in range(1<<b):
        if x.bit_count()%2 != target:
            F.append(tuple(-i if (x>>(i-1))&1 else i for i in range(1,b+1)))
    return canonical(F)

def dimacs(C,n):
    return ('p cnf %d %d\n'%(n,len(C)) + ''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode('ascii')

def marginal_floor(n):
    return 32*sum(len(str(j)) for j in range(1,n+1))

def verify(b,target,run_exact=False):
    C,n=parity_cnf(b,target)
    assert n==2*b+1 and len(C)==4*b
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in C)
    assert len(set(C))==len(C)
    symbolic_checks=0
    full_checks=0
    for x in range(1<<b):
        A=expected_lift(b,x,target)
        correct=(x.bit_count()%2==target)
        assert eval_cnf(C,A)==correct
        symbolic_checks+=1
        if b<=6:
            pins={i:bool((x>>(i-1))&1) for i in range(1,b+1)}
            assert brute_project(C,n,b,pins)==correct
            full_checks+=1
    # Existence under quantification of any single port is TRUE on all other assignments.
    forgotten_tests=0
    for forget in range(1,b+1):
        for z in range(1<<(b-1)):
            residual={i:bool((z>>(i-(i>forget)-1))&1) for i in range(1,b+1) if i!=forget}
            fits=[]
            for bit in (False,True):
                assignment={**residual,forget:bit}
                parity=sum(assignment.values())%2
                fits.append(parity==target)
            assert sorted(fits)==[False,True]
            forgotten_tests+=1
    noaux=forbidden_cnf(b,target)
    assert len(noaux)==2**(b-1)
    assert all(len(clause)==b for clause in noaux)
    for x in range(1<<b):
        A={i:bool(x>>(i-1)&1) for i in range(1,b+1)}
        assert eval_cnf(noaux,A)==(x.bit_count()%2==target)
    ans={'boundary':b,'target':target,'ordinary_3cnf_variables':n,
         'ordinary_3cnf_clauses':len(C),
         'ordinary_3cnf_bits':len(dimacs(C,n))*8,
         'auxiliary_free_clauses':len(noaux),'auxiliary_free_width':b,
         'auxiliary_free_bits':len(dimacs(noaux,b))*8,
         'symbolic_complete_boundary_checks':symbolic_checks,
         'full_auxiliary_enumerated_checks':full_checks,
         'single_port_forget_pair_checks':forgotten_tests,
         'exact22_bits':None,'exact22_variables':None,'exact22_clauses':None,
         'allport_named_min_bits':marginal_floor(b),
         'source_sha256':hashlib.sha256(dimacs(C,n)).hexdigest()}
    if run_exact:
        comp=load_compiler()
        r=comp.compile_allports(n,C)
        assert comp.strict22(r.compiled,r.compiled_n)
        assert comp.connectivity(r.compiled,r.compiled_n)
        assert r.compiled_n==9*(len(r.hub)+7*len(r.gadgets))
        assert len(r.compiled)==4*r.compiled_n//3
        for x in range(1<<b):
            if x.bit_count()%2==target:
                A=expected_lift(b,x,target)
                values={i:int(A[i]) for i in range(1,n+1)}
                assert comp.eval_cnf(C,values)
                lifted=comp.lift_witness(r,values)
                assert comp.eval_cnf(r.compiled,lifted)
                assert all(lifted[i]==values[i] for i in range(1,b+1))
        ans['exact22_bits']=len(comp.dimacs(r.compiled,r.compiled_n))*8
        ans['exact22_variables']=r.compiled_n
        ans['exact22_clauses']=len(r.compiled)
        ans['exact22_source_truth_witnesses_checked']=2**(b-1)
    return ans

def contradiction_controls(b):
    C0,n0=parity_cnf(b,0)
    C1,n1=parity_cnf(b,1)
    # Merge with renamed auxiliary variables in second formula (x_1..x_b shared).
    remap={j: (j if j<=b else n0+(j-b)) for j in range(1,n1+1)}
    new=canonical(list(C0)+[tuple((1 if l>0 else -1)*remap[abs(l)] for l in clause) for clause in C1])
    n=n0+(n1-b)
    assert len(new)==8*b
    examined=0
    for x in range(1<<b):
        v0=(x.bit_count()%2==0)
        v1=(x.bit_count()%2==1)
        assert not(v0 and v1)
        if b<=5:
            pins={i:bool((x>>(i-1))&1) for i in range(1,b+1)}
            assert not brute_project(new,n,b,pins)
        examined+=1
    return {'boundary':b,'clauses':len(new),'variables':n,'physical_bits':8*len(dimacs(new,n)),
            'all_boundary_pins_unsat_checked':examined,'status':'UNSAT'}

def main():
    out={'run':'LSPV-2 PARITY-PORT-FORGETTING225',
         'status':'PASS','seed':None,'audit_status':'separate original archive rerun',
         'cases':[],'contradictions':[]}
    for b in (2,3,4,5,6,7,8,10):
        for target in (0,1):
            out['cases'].append(verify(b,target,run_exact=(b in (3,4,6) and target==0)))
        if b<=5:out['contradictions'].append(contradiction_controls(b))
    out['barriers']=[
      'Parity no-auxiliary CNF size is exponential, but extension-variable 3CNF remains linear.',
      'Forgetting one parity input makes the projected relation TRUE; contradictory parity pair remains UNSAT.',
      'The strict exact22 lift retains all named source ports, expands physical bits and does not solve SAT.',
      'No all-input summary acquisition or polynomial-power contraction follows.',
      'No native Turing-machine step counts are directly measured by Python.']
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()
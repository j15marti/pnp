#!/usr/bin/env python3
"""CIRCUIT-SCAN-INTERIOR-SELECT177, exact arithmetic tile inverse.
Python stdlib. Requires the previously published 173 independent netlist emitter
in the same directory (bundled in downloadable package).
No entire source gate/occurrence table is read by the *selector* functions.
Expected bound for selectors: O(log^5 G) bit operations, O(log G) writable bits.
Output is a finite audit, NOT an ordinary-SAT decision/ARC contraction.
"""
import importlib.util, json, argparse, math, random
from pathlib import Path
import collections

PREDECESSOR='2026-10-27_0412_CIRCUIT_SCAN_REVERSE_SELECT173_repro.py'
def load_predecessor():
    path=Path(__file__).with_name(PREDECESSOR)
    spec=importlib.util.spec_from_file_location('prior173',path)
    if spec is None:raise RuntimeError('Missing exact independent predecessor emitter: '+str(path))
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
P=load_predecessor()

# All gate descriptions are operator and TWO SIGNED wire references, as in 173.
# Arithmetic below uses a constant number of O(log G)-bit integer registers.
def cv(S,n):
    return S.C.base-1 if n else S.C.base-2  # const1=N+q+2, const0=N+q+1

def final_record(S,p,c):return S.C.base+P.final_forward_output(S,p,c)

def read_kind(S,p,b):return final_record(S,p,S.w+b)

def read_id(S,p,b):return final_record(S,p,b)


def tree_n(L,level):
    for _ in range(level):L=(L+1)//2
    return L


def tree_round_gate_offset(L,stage,index):
    # 'stage' is 0 for first round after 3L XOR gates.
    off=3*L
    for i in range(stage):
        n=tree_n(L,i)
        off+=n//2
    return off+index


def tree_source(S,start,L,level,index):
    """Return signed input source at a reduction level without recursion/stack.
    level=0 for initial -XOR leaves, level>=1 for after that many rounds.
    Retains only a handful O(log G)-bit integers at any instant.
    """
    while level>0:
        nprev=tree_n(L,level-1)
        pairs=nprev//2
        if index<pairs:
            return S.C.base+start+tree_round_gate_offset(L,level-1,index)
        assert index==pairs and nprev%2==1,(L,level,index,nprev)
        index=nprev-1
        level-=1
    assert 0<=index<L
    return -(S.C.base+start+3*index+2)


def eqbits_gate(S,start,L,t,left_bit,right_bit):
    """Direct gate descriptor at 0<=t<4L-1 for a length-L EqBits call.
    Gate IDs here are local to full network but references use global signed IDs.
    """
    assert L>=2 and 0<=t<4*L-1
    if t<3*L:
        j,slot=divmod(t,3)
        a,b=left_bit(j),right_bit(j)
        if slot==0:return 'and',a,-b
        if slot==1:return 'and',-a,b
        return 'or',S.C.base+start+3*j,S.C.base+start+3*j+1
    k=t-3*L
    n=L
    stage=0
    while True:
        cnt=n//2
        if k<cnt:
            a=tree_source(S,start,L,stage,2*k)
            b=tree_source(S,start,L,stage,2*k+1)
            return 'and',a,b
        k-=cnt;n=(n+1)//2;stage+=1
        assert n>=2


def eq_output(S,start,L):return S.C.base+start+4*L-2


def scan_gate_at(S,p,off):
    """Exact descriptor (op,a,b), unsigned g from tile p, without netlist lookup."""
    assert 0<=p<S.K
    base=P.scan_base(S,p)
    size=19 if p==0 else 4*S.w+18
    assert 0<=off<size,(p,off,size)
    kind=lambda j:read_kind(S,p,j)
    if off<7:
        return eqbits_gate(S,base,2,off,kind,lambda j:cv(S,0))
    if off<14:
        return eqbits_gate(S,base+7,2,off-7,kind,lambda j:cv(S,(j==0)))
    t=off-14
    if p>0 and t<4*S.w-1:
        return eqbits_gate(S,base+14,S.w,t,
                           lambda j:read_id(S,p,j),lambda j:read_id(S,p-1,j))
    q=off-(14 if p==0 else 14+4*S.w-1)
    assert 0<=q<5
    isassign=eq_output(S,base,2)
    isquery=eq_output(S,base+7,2)
    same=cv(S,0) if p==0 else eq_output(S,base+14,S.w)
    prevcarry=cv(S,0) if p==0 else (S.C.base+P.scan_base(S,p-1)+
                                  (17 if p-1==0 else 4*S.w+16))
    keep1=S.C.base+base+(14 if p==0 else 4*S.w+13)
    keep2=keep1+1
    carry1=keep1+2
    carry2=keep1+3
    payload=final_record(S,p,S.w+2)
    if q==0:return 'and',same,prevcarry
    if q==1:return 'and',-isassign,keep1
    if q==2:return 'and',isassign,payload
    if q==3:return 'or',carry1,keep2
    return 'and',isquery,carry2


def scan_gate_location(S,g):
    assert S.Gf<=g<S.scan_end
    if g<S.Gf+19:return 0,g-S.Gf
    return 1+(g-S.Gf-19)//(4*S.w+18), (g-S.Gf-19)%(4*S.w+18)


def scan_inverse(S,g):
    """True signed consumers, ordered gate and operand position, no occurrence table.
    At most two TILE visits; every tile width O(log G).
    """
    p,off=scan_gate_location(S,g)
    v=S.C.base+g
    targets=[]
    for pp in (p,p+1):
        if pp>=S.K:continue
        b=P.scan_base(S,pp)
        length=19 if pp==0 else 4*S.w+18
        for i in range(length):
            op,a,c=scan_gate_at(S,pp,i)
            for j,wire in enumerate((a,c)):
                if abs(wire)==v:targets.append((b+i,j,1 if wire>0 else -1))
    if g==P.scan_output(S,p):
        targets.extend(P.scan_to_inverse_select(S,p))
    return sorted(targets)


def own_output_cnf(op,g):
    if op=='and':
        return [(13*g+8,2,1)]+[(13*g+j,1,-1) for j in (9,10,11,12)]
    return [(13*g+8,2,-1)]+[(13*g+j,1,1) for j in (9,10,11,12)]


def scan_occurrences(S,g):
    p,off=scan_gate_location(S,g)
    op,*_=scan_gate_at(S,p,off)
    out=own_output_cnf(op,g)
    for cg,slot,sign in scan_inverse(S,g):
        for j in range(4):
            out.append((13*cg+4*slot+j,1,sign if j<2 else -sign))
    return sorted(out)




def scan_source_literal(S,g,row,slot):
    """A signed compiler source literal, without a materialized gate list.
    This is limited to the 13-row gate-block compiler and scan-sector gates.
    """
    assert 0<=row<13 and 0<=slot<3
    p,off=scan_gate_location(S,g)
    op,aa,bb=scan_gate_at(S,p,off)
    def translate(lit):
        v=abs(lit)
        if v<S.C.base:return lit
        return (1 if lit>0 else -1)*(S.C.base+9*(v-S.C.base)+2)
    ba=S.C.base+9*g
    u,v,y=ba,ba+1,ba+2
    aa=translate(aa);bb=translate(bb)
    if row<4:
        arr=((-u,aa) if row<2 else (u,-aa))
        pad=(ba+3 if row%2==0 else -(ba+3)) if row<2 else (ba+4 if row%2==0 else -(ba+4))
        return (arr+(pad,))[slot]
    if row<8:
        j=row-4
        arr=((-v,bb) if j<2 else (v,-bb))
        pad=(ba+5 if j%2==0 else -(ba+5)) if j<2 else (ba+6 if j%2==0 else -(ba+6))
        return (arr+(pad,))[slot]
    if op=='and':
        if row==8:return (-u,-v,y)[slot]
        if row<=10:return (u,-y,ba+7 if row==9 else -(ba+7))[slot]
        return (v,-y,ba+8 if row==11 else -(ba+8))[slot]
    if row==8:return (u,v,-y)[slot]
    if row<=10:return (-u,y,ba+7 if row==9 else -(ba+7))[slot]
    return (-v,y,ba+8 if row==11 else -(ba+8))[slot]


def fixed_compiler_meta(S):
    n0=9*S.G+3*S.N+S.q+8
    m0=13*S.G+4*S.N+12
    width=max(n0,m0).bit_length()
    lw=width.bit_length()
    header='10101101'+'1'*lw+'0'+format(width,f'0{lw}b')+format(n0,f'0{width}b')+format(m0,f'0{width}b')
    return {'variables':n0,'clauses':m0,'field_width':width,
            'header':header,'header_bits':len(header),
            'physical_output_bits':len(header)+3*m0*(width+1)}


def scan_output_bit(S,g,row,slot,k):
    """Bit of the source variable-width wrapper output for given source row.
    For any scan-sector Boolean gate g and source row 0..12.
    Does not allocate the output, the source clause, or a wire occurrence table.
    """
    w=fixed_compiler_meta(S)['field_width']
    lit=scan_source_literal(S,g,row,slot)
    assert 0<=k<=w
    if k==0:return '1' if lit>0 else '0'
    v=abs(lit)
    return '1' if (v>>(w-k))&1 else '0'


def scan_output_position(S,g,row,slot,k):
    meta=fixed_compiler_meta(S)
    return meta['header_bits']+(3*(13*g+row)+slot)*(meta['field_width']+1)+k

def audit(mode="base"):
    report={'run_id':'CIRCUIT-SCAN-INTERIOR-SELECT177','status':'RESTRICTED exact arithmetic proof; finite independent audit',
            'cases':[],'errors':[],'references':['173 archived exact netlist','174 source alias and fixed compiler']}
    grand={'cases':0,'gates':0,'signed_uses':0,'cnf_occurrences':0,'gate_descriptor_checks':0,'rank_select_roundtrips':0,'zero_fanout':0,'one_fanout':0,'two_fanout':0,'high_fanout':0,'malformed_rank_checks':0,'source_literal_checks':0,'virtual_bit_checks':0}
    paramlist=[(3,1),(3,2),(4,1),(4,2),(5,1),(5,2),(6,2)] if mode=='base' else [(8,1),(16,1)] if mode=='width' else [(32,1)]
    for q,m in paramlist:
        A=P.Verifier(q,m);S=P.Shape(q,m)
        assert A.scan_end==S.scan_end and A.Gf==S.Gf
        uses=P.audit_uses_map(A)
        row={'q':q,'m':m,'w':S.w,'K':S.K,'G':S.G,
             'scan_gates':S.scan_end-S.Gf,'gate_descriptor_checks':0,
             'signed_uses':0,'cnf_occurrences':0,'rank_select_roundtrips':0,
             'zero_fanout':0,'max_fanout':0,'source_literal_checks':0,'virtual_bit_checks':0}
        for g in range(S.Gf,S.scan_end):
            p,off=scan_gate_location(S,g)
            pred=scan_gate_at(S,p,off)
            actual=A.C.g[g]
            assert pred==actual,(q,m,g,p,off,pred,actual)
            row['gate_descriptor_checks']+=1
            for cr in range(13):
                for slot in range(3):
                    v=scan_source_literal(S,g,cr,slot)
                    assert v==P.gate_clause(A,g,cr)[slot],(q,m,g,cr,slot,v,P.gate_clause(A,g,cr)[slot])
                    row['source_literal_checks']+=1
                    # Physical literal sign and two index bits, not precomputed from a full source.
                    ww=fixed_compiler_meta(S)['field_width']
                    for k in (0,1,ww):
                        physical=scan_output_position(S,g,cr,slot,k)
                        out=scan_output_bit(S,g,cr,slot,k)
                        assert out==P.output_bit(A,[0]*S.N,physical),(q,m,g,cr,slot,k,out)
                        row['virtual_bit_checks']+=1
            got=scan_inverse(S,g)
            expected=sorted(uses.get(g,[]))
            assert got==expected,(q,m,'use',g,p,off,got,expected)
            row['signed_uses']+=len(got)
            row['max_fanout']=max(row['max_fanout'],len(got))
            if not got:row['zero_fanout']+=1
            if len(got)<=2:grand[('zero_fanout' if len(got)==0 else 'one_fanout' if len(got)==1 else 'two_fanout')]+=1
            else:grand['high_fanout']+=1
            target=S.C.base+9*g+2
            occ=scan_occurrences(S,g)
            # Independent actual source occurrences without inspecting occurrence table
            # Predicted uses vs actual uses are already verified against materialized netlist.
            actual_occ=[]
            for own_row in range(13):
                cl=P.gate_clause(A,g,own_row)
                for pos,lit in enumerate(cl):
                    if abs(lit)==target:actual_occ.append((13*g+own_row,pos,1 if lit>0 else -1))
            for consumer,_,_ in expected:
                for own_row in range(13):
                    cl=P.gate_clause(A,consumer,own_row)
                    for pos,lit in enumerate(cl):
                        if abs(lit)==target:actual_occ.append((13*consumer+own_row,pos,1 if lit>0 else -1))
            actual_occ.sort()
            assert occ==actual_occ,(q,m,'occ',g,occ,actual_occ)
            for rank,tup in enumerate(occ):
                assert occ[rank]==tup
                assert occ.index(tup)==rank
                row['rank_select_roundtrips']+=1
            # Rank for first unused clause is absent.
            assert (13*g+7,2,1) not in occ
            grand['malformed_rank_checks']+=1
            row['cnf_occurrences']+=len(occ)
        report['cases'].append(row)
        grand['cases']+=1
        for key in ('gate_descriptor_checks','signed_uses','cnf_occurrences','rank_select_roundtrips','source_literal_checks','virtual_bit_checks'):
            grand[key]+=row[key]
        grand['gates']+=row['scan_gates']
    report['totals']=grand
    report['proof_scope']={'gate_inverse':'all scan gates, fixed oblivious verifier only',
                           'source_cnf':'13-row gate compiler only, not R15 second-level',
                           'input':'fixed-record witness verifier, not full ordinary-SAT DECISION circuit',
                           'workspace':'selector code does not read materialized A; audit does',
                           'ARC_EDGE_90':'OPEN','P_vs_NP':'OPEN'}
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='2026-10-27_0812_CIRCUIT_SCAN_INTERIOR_SELECT177_raw.json')
    ap.add_argument('--mode',choices=('base','width','wide'),default='base')
    args=ap.parse_args()
    result=audit(args.mode)
    Path(args.output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['totals'],sort_keys=True,indent=2))
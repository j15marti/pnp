#!/usr/bin/env python3
"""LSPV-2 HEADMOVE-EXACT22-JUMP172 finite source and three-machine audit.
Python 3, standard library only. All recorded costs are *declared abstract model*
operations, NOT measured CPython physical Turing-machine time.
Run: python3 lspv2_headmove_172_audit.py --output /mnt/data/lspv2_headmove_172_raw.json
"""
from collections import Counter
from itertools import product
import argparse, json, math

W1=(
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))
A=((6,0),(11,0)); B=((17,2),(9,2))
FROZEN=tuple(i for i in range(20) if i not in (6,11,17,9))
MAGIC='10100110111100000011110010101010'

def H(a,b):
    z=[list(c) for c in W1]
    if not a:
        for i,k in A:z[i][k]=-z[i][k]
    if not b:
        for i,k in B:z[i][k]=-z[i][k]
    return tuple(map(tuple,z))

def models_15(clauses):
    count=0; first=None
    for mask in range(1<<15):
        if all(any((((mask>>(abs(l)-1))&1)==int(l>0)) for l in c) for c in clauses):
            count+=1
            if first is None:first=mask
    return count,first

def shape(m):
    w=(20*m).bit_length()  # include exact C=20m in the self-describing header
    s=3*(w+1); hd=len(MAGIC)+3*w
    return {'m':m,'V':15*m,'C':20*m,'w':w,'header_bits':hd,'clause_stride_bits':s,
            'N':hd+20*m*s,'left_clauses':2*m,'fixed_clauses':16*m,
            'right_clauses':2*m}

def clause_location(m,c):
    if not 0<=c<20*m:raise IndexError(c)
    if c<2*m:
        i,idx=divmod(c,2);return i,A[idx][0], 'A', idx
    if c<18*m:
        i,idx=divmod(c-2*m,16);return i,FROZEN[idx],'F',idx
    i,idx=divmod(c-18*m,2);return i,B[idx][0],'B',idx

def clause_at(m,a,b,c):
    i,j,_,_=clause_location(m,c)
    return tuple((1 if l>0 else -1)*(15*i+abs(l)) for l in H(a[i],b[i])[j])

def binbits(v,w):return format(v,'0%db'%w)

def head(m):
    z=shape(m);w=z['w']
    return MAGIC+binbits(z['V'],w)+binbits(z['C'],w)+binbits(m,w)

def litbits(l,w):return ('1' if l>0 else '0')+binbits(abs(l),w)

def serial(m,a,b):
    z=shape(m)
    return head(m)+''.join(litbits(v,z['w']) for c in range(z['C'])
                           for v in clause_at(m,a,b,c))

def ctrlpos(m,side,i):
    z=shape(m);assert side in 'AB' and 0<=i<m
    if side=='A':return z['header_bits']+2*i*z['clause_stride_bits']
    return z['header_bits']+(18*m+2*i)*z['clause_stride_bits']+2*(z['w']+1)

def expected_bit(m,p,control):
    z=shape(m)
    if p<0 or p>=z['N']:raise IndexError(p)
    if p<z['header_bits']:return head(m)[p]
    c,field=divmod(p-z['header_bits'],z['clause_stride_bits'])
    j,bit=divmod(field,z['w']+1)
    i,old,kind,idx=clause_location(m,c)
    lit=W1[old][j]
    if bit==0 and kind in ('A','B') and j==(0 if kind=='A' else 2):
        bit0=control(kind,i)
        return bit0 if idx==0 else ('1' if bit0=='0' else '0')
    return litbits((1 if lit>0 else -1)*(15*i+abs(lit)),z['w'])[bit]

def infer_size(n):
    if n<shape(1)['N']:return None
    lo,hi=1,n
    while lo<=hi:
        x=(lo+hi)//2
        if shape(x)['N']==n:return x
        if shape(x)['N']<n:lo=x+1
        else:hi=x-1
    return None

class IndexCosts:
    def __init__(self,n):
        self.n=n;self.w=max(1,(n+1).bit_length())
        self.probes=0;self.address_writes=0;self.word_ops=0
        self.first=[]
    def read(self,s,p):
        assert 0<=p<len(s)
        self.probes+=1;self.address_writes+=self.w
        self.word_ops+=1 # one word fetch plus separately charged bit extraction
        if len(self.first)<16:self.first.append(p)
        return s[p]
    def calc(self,c=1):self.word_ops+=c
    def report(self):return {'indexed_bit_probes':self.probes,
      'binary_address_bit_writes':self.address_writes,
      'word_RAM_ops_proxy':self.word_ops,
      'word_width_bits':self.w,'live_algorithm_words_bound':12,
      'live_algorithm_bits_bound':12*self.w,
      'first_16_physical_addresses':self.first}

def rat_decide(s,strict):
    costs=IndexCosts(len(s));m=infer_size(len(s))
    costs.calc(8*costs.w*costs.w) # conservative upper proxy, not literal CPU op trace
    if m is None:return 'MALFORMED_LENGTH',False,costs.report()
    def ctrl(k,i):
        costs.calc(12)
        return costs.read(s,ctrlpos(m,k,i))
    sat=True
    for i in range(m):
        sat &= not(ctrl('A',i)=='1' and ctrl('B',i)=='1')
    if strict:
        for p in range(len(s)):
            z=costs.read(s,p)
            if z!=expected_bit(m,p,ctrl):return 'NONCANONICAL',False,costs.report()
            costs.calc(20)
    return ('CANONICAL' if strict else 'PROMISE'),bool(sat),costs.report()

def tape_one_head_locator(s,m):
    headpos=0;moves=0;R=0;last=0;probes=0
    for i in range(m):
        for k in 'AB':
            dest=ctrlpos(m,k,i);delta=dest-headpos
            if delta:
                d=1 if delta>0 else -1
                if last and d!=last:R+=1
                last=d
            moves+=abs(delta);headpos=dest;probes+=1
    return {'physical_unit_head_moves':moves,'head_reversals':R,
            'input_bit_probes':probes, 'initial_head_location':0,
            'final_head_location':headpos}

def tape_two_heads_locator(s,m):
    p1=p2=0;moves=0;probes=0;sat=True
    for i in range(m):
        q1=ctrlpos(m,'A',i);q2=ctrlpos(m,'B',i)
        moves+=abs(q1-p1)+abs(q2-p2);p1,p2=q1,q2
        sat &= not(s[q1]=='1' and s[q2]=='1')
        probes+=2
    return {'result':bool(sat),'physical_unit_head_moves':moves,
            'input_bit_probes':probes,'initial_second_head_seek':ctrlpos(m,'B',0),
            'uniform_locator_index_bits_bound':8*(len(s)+1).bit_length()}

def itinerary(m,a,b,capacity,J):
    """Promised DISJ batching, actual target symbol read; J length-limited jumps.

    The jump command cost is one for each signed displacement <= J; its
    binary offset writing O(log J) is separately reported in address bits.
    Work moves for buffer and index arithmetic are separately upper-bounded.
    """
    assert 1<=capacity<=m and 1<=J
    s=serial(m,a,b);n=len(s)
    cur=0;R=0;last_direction=0;H=0;U=0;addr_bits=0;probes=0;out=True
    B_m=0; batches=0
    for start in range(0,m,capacity):
        stop=min(m,start+capacity);batches+=1
        cache=[]
        for side in 'AB':
            for i in range(start,stop):
                q=ctrlpos(m,side,i)
                delta=q-cur
                if delta:
                    d=1 if delta>0 else -1
                    if last_direction and d!=last_direction:R+=1
                    last_direction=d
                    H+=abs(delta)
                    ops=(abs(delta)+J-1)//J
                    U+=ops
                    addr_bits+=ops*(J+1).bit_length()
                cur=q;probes+=1
                if side=='A':cache.append(s[q])
                else:out &= not(cache[i-start]=='1' and s[q]=='1')
        B_m=max(B_m,len(cache))
    # Jump-ops plus target probes and bounded sequential buffer updates.
    # Does not include full non-promise template validation.
    return {'answer':bool(out),'m':m,'N':n,'J':J,'buffer_capacity':capacity,
      'buffer_actual_peak':B_m,'batches':batches,
      'input_head_unit_distance_if_expanded':H,
      'charged_bounded_jump_commands':U,
      'binary_jump_offset_writes':addr_bits,
      'input_bit_probes':probes,'input_head_reversals':R,
      'model_steps_proxy':U+addr_bits+probes+4*m*(n+1).bit_length(),
      'visited_work_cells_upper_bound':capacity+8*(n+1).bit_length(),
      'expanded_unit_move_simulation_reversals':R,
      'expanded_unit_move_simulation_moves':H}

def compact_source(a,b,gap):
    return ''.join(map(str,a))+'#'+'0'*gap+'#'+''.join(map(str,b))+'$'

def machine_step(state,inch,workch,good):
    """Fixed-state ONE sequential read-only input head + one work-tape head.
    Finite-control witness circuit EQUAL(a,b), not full SAT decision circuit.
    Result is (state, writeWork, dInput, dWork, good, emittedBit).
    """
    fail=('HALT',workch,0,0,False,'0')
    if state=='START':
        if inch in '01':return ('COPY',inch,1,1,good,None)
        return fail
    if state=='COPY':
        if inch in '01':return ('COPY',inch,1,1,good,None)
        if inch=='#':return ('REWIND',workch,0,-1,good,None)
        return fail
    if state=='REWIND':
        if workch=='^':return ('SEEK_FIRST',workch,0,1,good,None)
        return ('REWIND',workch,0,-1,good,None)
    if state=='SEEK_FIRST':
        if inch=='#':return ('SEEK_ZERO',workch,1,0,good,None)
        return fail
    if state=='SEEK_ZERO':
        if inch=='0':return ('SEEK',workch,1,0,good,None)
        return fail
    if state=='SEEK':
        if inch=='0':return ('SEEK',workch,1,0,good,None)
        if inch=='#':return ('COMPARE',workch,1,0,good,None)
        return fail
    if state=='COMPARE':
        if inch in '01' and workch in '01':
            return ('COMPARE',workch,1,1,good and inch==workch,None)
        if inch=='$':return ('CHECK_END',workch,1,0,good and workch=='_',None)
        return fail
    if state=='CHECK_END':
        ok=bool(good and inch=='_')
        return ('HALT',workch,0,0,ok,'1' if ok else '0')
    raise AssertionError(state)

def simulate_one_shared(source):
    """Conservative real track/marker/sweep simulation of the finite Mk machine.
    Every three exhaustive passes use no saved occurrence or input-head tables.
    Python dictionaries implement *finite-alphabet product symbols* in the audit.
    """
    inp=source+'_' # implicit right blank sentinel
    N=len(inp)
    tape=[{'source':c,'w':'_','i':x==0,'h':x==1} for x,c in enumerate(inp)]
    tape[0]['w']='^'
    state='START';good=True;ih=0;wh=1
    ref={'state':'START','good':True,'ih':0,'wh':1,'work':{0:'^'}}
    Tk=0;Qk=0;Ck=0;work_used={0,1};Iused=set();writes_k=0
    T1=0;Q1=0;H1=0;C1=0;W1=0;flips=0;outputs='';states=0
    while state!='HALT':
        assert ih==ref['ih'] and wh==ref['wh']
        assert state==ref['state'] and good==ref['good']
        assert sum(c['i'] for c in tape)==sum(c['h'] for c in tape)==1
        assert tape[ih]['i'] and tape[wh]['h']
        for q in range(N):assert tape[q]['w']==ref['work'].get(q,'_')
        # first of FOUR charged sweeps fetches both marked head symbols
        xs=ys=None
        for j in range(N):
            T1+=1;Q1+=1;W1+=1
            if j:H1+=1;C1+=1
            if tape[j]['i']:xs=tape[j]['source']
            if tape[j]['h']:ys=tape[j]['w']
        assert xs==inp[ih] and ys==tape[wh]['w']
        Iused.add(ih);work_used.add(wh);Qk+=2
        transition=machine_step(state,xs,ys,good)
        assert transition==machine_step(ref['state'],inp[ref['ih']],
                                 ref['work'].get(ref['wh'],'_'),ref['good'])
        ns,neww,di,dw,ng,out=transition
        assert di in (-1,0,1) and dw in (-1,0,1)
        # independent Mk reference uses conceptual tracks not the simulated tape
        ref['work'][ref['wh']]=neww
        ref['ih']+=di;ref['wh']+=dw
        ref['state']=ns;ref['good']=ng
        writes_k+=1
        # Reverse sweep performs local symbol write and left moving markers
        pend_i=pend_h=False
        for j in range(N-1,-1,-1):
            T1+=1;Q1+=1;W1+=1
            if j<N-1:H1+=1;C1+=1
            v=tape[j];oi,oh=v['i'],v['h']
            if oh:
                if v['w']!=neww:flips+=1
                v['w']=neww
            if pend_i:assert not oi;v['i']=True;flips+=1;pend_i=False
            if pend_h:assert not oh;v['h']=True;flips+=1;pend_h=False
            if oi and di==-1:v['i']=False;flips+=1;pend_i=True
            if oh and dw==-1:v['h']=False;flips+=1;pend_h=True
        assert not (pend_i or pend_h)
        # Forward sweep moves right-moving markers after prior left moves
        pend_i=pend_h=False
        for j in range(N):
            T1+=1;Q1+=1;W1+=1
            if j:H1+=1;C1+=1
            v=tape[j];oi,oh=v['i'],v['h']
            if pend_i:assert not oi;v['i']=True;flips+=1;pend_i=False
            if pend_h:assert not oh;v['h']=True;flips+=1;pend_h=False
            if oi and di==1:v['i']=False;flips+=1;pend_i=True
            if oh and dw==1:v['h']=False;flips+=1;pend_h=True
        assert not (pend_i or pend_h)
        # Critical: do NOT teleport the single physical head back to cell 0.
        # Charge an entire return sweep before the next virtual transition.
        for j in range(N-1,-1,-1):
            T1+=1;Q1+=1;W1+=1
            if j<N-1:H1+=1;C1+=1
        state,good=ns,ng;ih+=di;wh+=dw
        assert 0<=ih<N and 0<=wh<N
        Tk+=1;Ck+=int(di!=0)+int(dw!=0)
        states+=1
        if out is not None:outputs+=out
        assert Tk<12*N
    assert len(outputs)==1
    # Charged one-cell write on an added output track of cell 0; head is at 0.
    T1+=1;W1+=1
    assert T1==4*N*Tk+1
    assert H1==4*(N-1)*Tk
    assert T1<=4*Tk*(N+len(work_used)+(Tk+2).bit_length())+1
    assert N<=N+len(work_used)+(Tk+2).bit_length()+1
    return {'output':outputs,'independent_same_step_checks':states,
       'Mk':{'input_length_bits_including_implicit_sentinel':N,
             'transitions':Tk,'work_cells_visited':len(work_used),
             'input_head_probes':Tk,'all_tape_probes':Qk,
             'head_crossings_events':Ck,'distinct_input_positions':len(Iused),
             'work_write_events':writes_k,'output_bits':len(outputs)},
       'M1':{'transitions':T1,'physical_head_steps':H1,
             'head_boundary_crossing_events':C1,
             'total_footprint_cells_including_input':N,
             'physical_cell_probes':Q1,'physical_head_reversals':4*Tk-1,
             'physical_write_events_including_unchanged':W1,
             'actual_track_symbol_marker_changes':flips,'output_bits':len(outputs)}}

def occurrence_select_local(m,ai,bi,variable_id,r):
    """Physical clause-order SELECT for a canonical F_m variable, no table.

    The fixed 20-row W1 descriptor is finite-control ROM. Four selected
    occurrence tuples are stored and sorted in O(log N) live bits.
    """
    if not (1<=variable_id<=15*m and 0<=r<4):raise IndexError((variable_id,r))
    i,t=divmod(variable_id-1,15);t+=1
    out=[];z=shape(m)
    for old in range(20):
        for slot in range(3):
            if abs(W1[old][slot])!=t:continue
            if old in (6,11):
                rank=0 if old==6 else 1
                clause=2*i+rank
            elif old in (17,9):
                rank=0 if old==17 else 1
                clause=18*m+2*i+rank
            else:
                clause=2*m+16*i+FROZEN.index(old)
            physical=z['header_bits']+clause*z['clause_stride_bits']+slot*(z['w']+1)
            lit=H(ai,bi)[old][slot]
            actual=(1 if lit>0 else -1)*(15*i+abs(lit))
            out.append((clause,slot,actual,physical))
    assert len(out)==4
    out.sort(key=lambda x:(x[0],x[1]))
    return out[r]

def occurrence_select(m,a,b,variable_id,r):
    if not 1<=variable_id<=15*m:raise IndexError(variable_id)
    i=(variable_id-1)//15
    return occurrence_select_local(m,a[i],b[i],variable_id,r)

def occurrence_select_indexed(s,m,variable_id,r,cost):
    """Actual indexed input locator charges both dynamic source-polarity reads.
    Source control values are NOT assumed resident in writable workspace.
    """
    i=(variable_id-1)//15
    x=int(cost.read(s,ctrlpos(m,'A',i)))
    y=int(cost.read(s,ctrlpos(m,'B',i)))
    cost.calc(180) # small constant count of bounded-width ROM/arithmetic operations
    return occurrence_select_local(m,x,y,variable_id,r)

def occurrence_rank(m,a,b,variable_id,clause,slot):
    for r in range(4):
        c,j,lit,p=occurrence_select(m,a,b,variable_id,r)
        if (c,j)==(clause,slot):return r
    return None

def evaluate_NAND_equal(a,b):
    """Emitted binary fanin-2 NAND circuit, 7m-2 gates, no hidden OR gate."""
    assert len(a)==len(b)>0
    gates=[]
    def nand(x,y):
        v=int(not (x and y));gates.append(v);return v
    carry=None
    for x,y in zip(a,b):
        q=nand(x,y);u=nand(x,q);v=nand(y,q)
        xor=nand(u,v);xnor=nand(xor,xor)
        if carry is None:carry=xnor
        else:t=nand(carry,xnor);carry=nand(t,t)
    assert len(gates)==7*len(a)-2
    return carry,len(gates)

def all_checks():
    result={'source':'W1 original project 15-variable 20-clause source; headmove-disjointness swap pattern'}
    hist={};witness={}
    for a,b in product((0,1),repeat=2):
        cs=H(a,b);pos=Counter();neg=Counter()
        assert len(cs)==20 and len(set(cs))==20
        for cl in cs:
            assert len(cl)==3 and len({abs(x) for x in cl})==3
            for l in cl:(pos if l>0 else neg)[abs(l)]+=1
        assert all(pos[i]==neg[i]==2 for i in range(1,16))
        n,first=models_15(cs);hist[f'{a}{b}']=n;witness[(a,b)]=first
    assert hist=={'00':772,'01':272,'10':272,'11':0}
    result['source_gadget']={'models_each':hist,'assignment_trials':4*(1<<15),
            'W1_exact_signed22':True,'all_4_supports_same':True}
    syntax=[];noncanonical=[]
    for m in range(1,6):
        allbits=list(product((0,1),repeat=m))
        for a in allbits:
            for b in allbits:
                z=shape(m);p=Counter();n=Counter();seen=set()
                is_sat=not any(x and y for x,y in zip(a,b))
                for ci in range(z['C']):
                    c=clause_at(m,a,b,ci)
                    assert c not in seen and len({abs(x) for x in c})==3
                    seen.add(c)
                    for l in c:(p if l>0 else n)[abs(l)]+=1
                    if is_sat:
                        mod=witness[(a[clause_location(m,ci)[0]],b[clause_location(m,ci)[0]])]
                        assert mod is not None
                        assert any((((mod>>(abs(l)-1-15*clause_location(m,ci)[0]))&1)==int(l>0)) for l in c)
                assert len(seen)==z['C']
                assert all(p[k]==n[k]==2 for k in range(1,z['V']+1))
                assert len(p)==len(n)==z['V']
        base=(0,)*m;other=(1,)*m
        for a,b in ((base,other),(other,base),(base,base),(other,other)):
            s=serial(m,a,b)
            z=shape(m)
            assert len(s)==z['N'] and infer_size(len(s))==m
            assert all(expected_bit(m,j,lambda k,i:s[ctrlpos(m,k,i)])==s[j] for j in range(len(s)))
            q,truth,cost=rat_decide(s,False)
            q2,truth2,cost2=rat_decide(s,True)
            assert truth==truth2==(not any(x and y for x,y in zip(a,b)))
            assert q=='PROMISE' and q2=='CANONICAL'
            two=tape_two_heads_locator(s,m)
            assert two['result']==truth
            syntax.append({'m':m,'a':''.join(map(str,a)),'b':''.join(map(str,b)),
                'bits':len(s),'RAM_promise':cost,'RAM_strict':cost2,
                'one_head_locator':tape_one_head_locator(s,m),
                'two_head_locator':two})
    result['exact22_formula_cases']=sum(4**m for m in range(1,6))
    # Independently materialized W1 occurrence tables for verification ONLY.
    occurrence_checks=0
    for m in range(1,5):
        allbits=list(product((0,1),repeat=m))
        for a in allbits:
            for b in allbits:
                raw=sorted((c,j,lit) for c in range(20*m) for j,lit in enumerate(clause_at(m,a,b,c)))
                for var in range(1,15*m+1):
                    matches=sorted((c,j,lit) for c,j,lit in raw if abs(lit)==var)
                    assert len(matches)==4
                    predicted=sorted(occurrence_select(m,a,b,var,r) for r in range(4))
                    assert [(c,j,lit) for c,j,lit,_ in predicted]==matches
                    assert predicted==[occurrence_select(m,a,b,var,r) for r in range(4)]
                    for c,j,lit,p in predicted:
                        assert occurrence_rank(m,a,b,var,c,j) is not None
                        assert p<shape(m)['N']
                        occurrence_checks+=1
    result['canonical_occurrence_rank_select_verified']=occurrence_checks
    indexed_occ_checks=0
    for m in range(1,6):
        a=tuple(int(i%3==0) for i in range(m));b=tuple(1-int(i%3==0) for i in range(m))
        encoded=serial(m,a,b);meter=IndexCosts(len(encoded))
        for var in range(1,15*m+1):
            for r in range(4):
                assert occurrence_select_indexed(encoded,m,var,r,meter)==occurrence_select(m,a,b,var,r)
                indexed_occ_checks+=1
        assert meter.probes==2*indexed_occ_checks if m==1 else meter.probes==2*60*m
    result['indexed_occurrence_select_checks']=indexed_occ_checks
    result['selected_canonical_layout_controls']=syntax
    s=serial(2,(0,1),(0,1));z=shape(2)
    badpos={'header':0,'sparse_id':z['header_bits']+1,
            'alice_second_sign':z['header_bits']+z['clause_stride_bits'],
            'bob_second_sign':z['header_bits']+(18*2+1)*z['clause_stride_bits']+2*(z['w']+1)}
    for label,q in badpos.items():
        bad=s[:q]+('0' if s[q]=='1' else '1')+s[q+1:]
        tag,_,_=rat_decide(bad,True)
        assert tag=='NONCANONICAL',(label,tag)
        noncanonical.append((label,tag))
    for bad in ('',s[:-1],s+'0',s[:100]):
        tag,_,_=rat_decide(bad,True)
        assert tag=='MALFORMED_LENGTH';noncanonical.append(('length',tag))
    # A coordinated 2-sign flip preserves the canonical format but changes SAT.
    switch=list(serial(2,(0,0),(1,1)))
    for c in (0,1):
        q=z['header_bits']+c*z['clause_stride_bits']
        switch[q]='1' if switch[q]=='0' else '0'
    tag,v,_=rat_decide(''.join(switch),True)
    assert tag=='CANONICAL' and not v
    noncanonical.append(('coordinated_A_switch',tag))
    result['malformed_and_switch_controls']=noncanonical
    # Exhaustively verify actual four-sweep tape simulator and gate counts.
    tape={};totalchecks=0
    for m in range(1,5):
        pair=0;worstK=0;worst1=0;worstP=0
        for a in product((0,1),repeat=m):
            for b in product((0,1),repeat=m):
                s=compact_source(a,b,2*m+3)
                sim=simulate_one_shared(s)
                v,g=evaluate_NAND_equal(a,b)
                assert v==int(a==b) and sim['output']==('1' if a==b else '0')
                assert g==7*m-2
                pair+=1;totalchecks+=sim['independent_same_step_checks']
                worstK=max(worstK,sim['Mk']['transitions'])
                worst1=max(worst1,sim['M1']['transitions'])
                worstP=max(worstP,sim['M1']['total_footprint_cells_including_input'])
        tape[str(m)]={'paired_inputs':pair,'NAND_gates':7*m-2,'worst_Mk_T':worstK,
                     'worst_M1_T':worst1,'worst_M1_P':worstP}
    for bad in ('01#000#0$','01##01$','01#000#01','01#000#001$','01X#000#01$'):
        assert simulate_one_shared(bad)['output']=='0'
    result['single_tape_simulation']={'cases':tape,'reference_step_state_equivalence_checks':totalchecks,
                 'malformed_compact_controls':5,
                 'gate_counter_type':'NAND gates for fixed equality promise circuit, not all-input SAT decision circuit'}
    curves=[]
    for m in (4,8,16,32):
        a=tuple(int(i%3==0) for i in range(m));b=tuple(1-int(i%3==0) for i in range(m))
        N=shape(m)['N']
        for J in (1,math.ceil(math.sqrt(N)),N):
            for cap in sorted(set((1,2, max(1,m//4),m))):
                row=itinerary(m,a,b,cap,J)
                assert row['answer'] and row['input_bit_probes']==2*m
                # Same sign sequence of nonzero directions when a jump expands
                assert row['expanded_unit_move_simulation_reversals']==row['input_head_reversals']
                assert row['input_head_unit_distance_if_expanded']<=J*row['charged_bounded_jump_commands']
                row['work_plus_index_bits']=row['visited_work_cells_upper_bound']
                row['reversal_space_witness']=(row['input_head_reversals']+1)*row['work_plus_index_bits']
                row['transport_product_witness']=row['model_steps_proxy']*J*row['work_plus_index_bits']
                curves.append(row)
    result['jump_itineraries']=curves
    result['status']={'proper_exact22_source':'COMPUTATIONAL + local symbolic gadget proof',
        'bounded_jump_machine_transfer':'PROVED conditional on HEADMOVE1 one-input-head lower theorem',
        'one_tape_four_sweep':'EXECUTABLE EXACT restricted machine',
        'all_input_SAT_decider':'OPEN','ARC_EDGE_90':'OPEN','P_versus_NP':'OPEN'}
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='lspv2_headmove_172_raw.json')
    args=ap.parse_args()
    z=all_checks()
    with open(args.output,'w') as f:json.dump(z,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'gadget_models':z['source_gadget']['models_each'],
      'proper_formula_cases':z['exact22_formula_cases'],
      'canonical_layout_controls':len(z['selected_canonical_layout_controls']),
      'occurrence_rank_select_checks':z['canonical_occurrence_rank_select_verified'],
      'indexed_occurrence_select_checks':z['indexed_occurrence_select_checks'],
      'malformed_tests':len(z['malformed_and_switch_controls']),
      'four_sweep_step_checks':z['single_tape_simulation']['reference_step_state_equivalence_checks'],
      'jump_itineraries':len(z['jump_itineraries']),
      'output':args.output},indent=2))
if __name__=='__main__':main()

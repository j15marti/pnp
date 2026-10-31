#!/usr/bin/env python3
"""LSPV-4 ARC-PAYLOAD-JUMP283: source-probe charging in FLMV's indexed model.

An OFFLINE native-operation trace of the explicitly declared one-index-tape
algorithm, not a SAT decision machine or a universal runtime lower bound.
Each event is checked via the complete fixed-location index-tape bit vector.
No import from verification code. Python 3.10+ standard library only.
"""
import argparse, gzip, hashlib, json, math
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
V_WITNESS='010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001'

def sources():
    u=[tuple(q) for q in json.loads((ROOT/'U_source.json').read_text())]
    v=list(u)
    v[1],v[7]=(v[7][0],*v[1][1:]),(v[1][0],*v[7][1:])
    return {'Y6_SAT':Y,'U198_UNSAT':u,'V198_SAT':v}

def grammar(F):
    n=max(abs(z) for clause in F for z in clause)
    m=len(F)
    assert n%3==0 and m==4*n//3
    assert len({tuple(sorted(C)) for C in F})==m
    assert all(len(C)==3 and len({abs(x) for x in C})==3 and (min(C)>0 or max(C)<0) for C in F)
    cnt=Counter(z for C in F for z in C)
    assert all(cnt[i]==cnt[-i]==2 for i in range(1,n+1))
    return n,m

def binary_source(F):
    n,m=grammar(F)
    w=n.bit_length()
    # Unary width prefix followed by n and a fixed number of records.
    head='1'*w+'0'+format(n,f'0{w}b')
    payload=''.join(('1' if C[0]>0 else '0')+''.join(format(abs(x)-1,f'0{w}b') for x in C) for C in F)
    assert len(payload)==m*(1+3*w)
    return head,payload,w

def dk(c,k):
    f=Fraction(1)
    for _ in range(k):f=c*f/(1+f)
    return min((1/f-c)/k,c**(-k))

def flmv():
    out=[]
    for c in (Fraction(6,5),Fraction(241,200)):
        terms=[dk(c,k) for k in range(1,4)]
        assert terms[1]>max(terms[0],terms[2],c**(-4))
        out.append({'c':str(c),'d1':str(terms[0]),'d2':str(terms[1]),'d3':str(terms[2]),
                    'k_ge_4_upper':str(c**(-4)),
                    'space_margin_above_1_2':str(terms[1]-Fraction(1,2))})
    assert out[0]['d2']=='23/45' and out[1]['d2']=='11642479/23232400'
    return out

def indexed_trace(name,F):
    prefix,payload,w=binary_source(F)
    source=prefix+payload
    H=len(prefix);P=len(payload);N=len(source)
    idx_width=N.bit_length()
    tape=0;idx_head=0;inp_head=0;reads=[]
    ctr=Counter();dphys=0;wrote=0;erased=0
    path=ROOT/(name+'_native_trace283.jsonl.gz')
    with gzip.open(path,'wt',encoding='utf-8',compresslevel=6) as out:
        def event(op,new_tape,new_idx_head,new_inp_head,address,read_bit=None):
            nonlocal tape,idx_head,inp_head,dphys,wrote,erased
            prev=tape
            d=(prev^new_tape).bit_count()
            changed=[k for k in range(idx_width) if ((prev^new_tape)>>k)&1]
            assert 0<=new_idx_head<idx_width
            if op=='index_write_one':
                assert (prev & (1<<idx_head))==0 and new_tape==(prev|(1<<idx_head)) and d==1
                wrote+=1
            elif op=='atomic_index_jump_erase':
                assert new_tape==0 and prev==address and d==address.bit_count()
                erased+=d
            else: assert d==0
            if op=='input_read':
                assert read_bit==int(source[new_inp_head])
                reads.append((address,read_bit))
            ctr[op]+=1;dphys+=d
            r={'step':sum(ctr.values()),'op':op,'address':address,
               'before_index_bits':format(prev,f'0{idx_width}b'),
               'after_index_bits':format(new_tape,f'0{idx_width}b'),
               'before_index_head':idx_head,'after_index_head':new_idx_head,
               'before_input_head':inp_head,'after_input_head':new_inp_head,
               'd_phys':d,'changed_index_cells':changed,
               'd_logic_residual':0,'d_source_coverage':int(op=='input_read')}
            if read_bit is not None:r['read_bit']=read_bit
            out.write(json.dumps(r,separators=(',',':'))+'\n')
            tape,idx_head,inp_head=new_tape,new_idx_head,new_inp_head
        for addr in range(H,N):
            # The input index head is never reset by the jump. Move it explicitly.
            if idx_head:
                while idx_head:
                    event('index_head_move_left',tape,idx_head-1,inp_head,addr)
            positions=[k for k in range(idx_width) if (addr>>k)&1]
            for k in positions:
                while idx_head<k:event('index_head_move_right',tape,idx_head+1,inp_head,addr)
                event('index_write_one',tape|(1<<idx_head),idx_head,inp_head,addr)
            assert tape==addr
            event('atomic_index_jump_erase',0,idx_head,addr,addr)
            event('input_read',0,idx_head,addr,addr,int(source[addr]))
    sum_pc=sum(addr.bit_count() for addr in range(H,N))
    assert wrote==erased==sum_pc and dphys==2*sum_pc
    assert len(reads)==P and all(v==int(payload[i]) for i,(_,v) in enumerate(reads))
    assert tape==0
    # Offline logical state of residual CNF is constant. A coverage bitmap is
    # separately tracked offline; it must not be mistaken for guest writable state.
    info={'source':name,'n':max(abs(z) for C in F for z in C),'m':len(F),
          'payload_bits':P,'header_bits':H,'input_bits':N,'index_width':idx_width,
          'read_count':len(reads),'read_address_first':H,'read_address_last':N-1,
          'direct_index_one_writes':wrote,'atomically_erased_ones':erased,
          'sum_popcount_addresses':sum_pc,'sum_adjacent_d_phys':dphys,
          'endpoint_d_phys':0,'sum_adjacent_d_logic_residual':0,
          'endpoint_d_logic_residual':0,
          'sum_source_coverage_delta_OFFLINE':P,'endpoint_coverage_OFFLINE':P,
          'native_event_counts':dict(ctr),'native_abstract_steps':sum(ctr.values()),
          'peak_index_tape_cells':idx_width,'peak_work_tape_cells_modelled':0,
          'input_head_final':inp_head,'index_head_final':idx_head,
          'binary_input_sha256':hashlib.sha256(source.encode()).hexdigest(),
          'trace_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
          'trace_relative_path':path.name,
          'read_outcome_sha256':hashlib.sha256(payload.encode()).hexdigest(),
          'sequential_control_input_reads':P,'sequential_control_index_jumps':0,
          'sequential_control_index_writes':0,
          'countermodel_comment':'Sequential read-only scan is O(P); indexed jumps are an optional restricted read policy. No SAT lower bound.'}
    return info

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',choices=list(sources()));a=parser.parse_args()
    F=sources()[a.source]
    result=indexed_trace(a.source,F)
    (ROOT/(a.source+'_summary283.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['source','payload_bits','read_count','sum_popcount_addresses','sum_adjacent_d_phys','native_abstract_steps','trace_sha256']},indent=2))
if __name__=='__main__':main()

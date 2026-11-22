"""Independent deadline/normalization audit for Bounds 3f88c098.
Only the normalized suffix is simulated transition by transition.
The canonical packed guard is a Python reference, not a native tape parser.
"""
import json
from itertools import product
from collections import Counter

def rows_for(bits):
    q=len(bits); h=6*q+1
    rows=[]
    for i in range(2*h):
        rows += [(3*i,3*i+1,3*i+2),
                 (3*i+2,3*((i+1)%(2*h)),6*h+i)]
    edges=[]
    for j in range(q):
        v=6*j
        edges += [(v+i,6*q) for i in range(6)]
        edges += [tuple(sorted((v+i,v+(i+1)%6))) for i in range(6)]
    edges += [(6*j,6*j+(2 if b else 3)) for j,b in enumerate(bits)]
    for a,(u,v) in enumerate(edges):
        rows += [(6*u+c,6*v+c,8*h+3*a+c) for c in range(3)]
    return rows

def encode(bits):
    q=len(bits); n=87*q+8; m=63*q+4; w=n.bit_length()
    g=format(m+1,'b')
    return '1'*n+'0'+'0'*(len(g)-1)+g+''.join(
        format(x+1,'0%db'%w) for row in rows_for(bits) for x in row)

def recognize(s):
    if not s or any(c not in '01' for c in s): return None
    n=s.find('0')
    if n<95 or (n-8)%87: return None
    q=(n-8)//87; p=n+1; z=0
    while p<len(s) and s[p]=='0': z+=1; p+=1
    if p+z+1>len(s): return None
    m=int(s[p:p+z+1],2)-1; p+=z+1
    w=n.bit_length()
    if m!=63*q+4 or len(s)-p!=3*m*w: return None
    rows=[tuple(int(s[p+(3*r+c)*w:p+(3*r+c+1)*w],2)-1
                for c in range(3)) for r in range(m)]
    base=rows_for([0]*q); alternate=rows_for([1]*q)
    start=m-3*q
    if rows[:start]!=base[:start]: return None
    bits=[]
    for j in range(q):
        a=start+3*j
        if rows[a:a+3]==base[a:a+3]: bits.append(0)
        elif rows[a:a+3]==alternate[a:a+3]: bits.append(1)
        else: return None
    return bits

def initial(bits):
    # Fixed finite alphabet. @ is the permanent origin marker on a second track.
    return [('?', '@'),('?', '.')] + [('P','.')]*len(bits) + [
        (str(b),'.') for b in bits] + [('#','.')]

def simulate(bits):
    tape=initial(bits); head=2; state=('SCAN',0); trace=[]; configs=[]
    while state[0]!='HALT':
        configs.append((head,state,tuple(tape)))
        old,mark=tape[head]; trace.append((head,state[0],old))
        mode,acc=state
        if mode=='SCAN':
            if old=='#': state=('RETURN',acc); head-=1
            else:
                assert old in 'P01'
                state=('SCAN',acc or old=='1'); head+=1
        elif mode=='RETURN':
            if mark=='@':
                tape[head]=('0' if acc else '1',mark)
                head+=1; state=('TERM',acc)
            else: head-=1
        elif mode=='TERM':
            tape[head]=(';',mark); state=('HALT',acc)
        else: raise AssertionError(state)
    return tape[0][0]=='1',trace,configs

def main():
    labels=0
    for q in range(1,11):
        for bits in product((0,1),repeat=q):
            source=encode(bits)
            assert recognize(source)==list(bits)
            decision,trace,_=simulate(bits)
            assert decision==(not any(bits))
            assert len(trace)==4*q+4
            labels+=1
    s=encode([0]); admitted={encode([0]),encode([1])}
    mutation_accept=mutation_reject=0
    for i in range(len(s)):
        t=s[:i]+str(1-int(s[i]))+s[i+1:]
        r=recognize(t)
        assert (r is not None)==(t in admitted)
        if r is None: mutation_reject+=1
        else: mutation_accept+=1
    extra=[s[:-1],s+'0',s+'1','',s+'x']
    assert all(recognize(x) is None for x in extra)
    rows=[]; comparisons=0
    for q in range(1,33):
        _,trace,cs=simulate([0]*q)
        hits={i:next(t for t,e in enumerate(trace) if e[0]==q+2+i)
              for i in range(q)}
        reuse=Counter()
        for j in range(q):
            for i in range(q):
                alt=[int(k==i) for k in range(q)]
                _,other_trace,other=simulate(alt)
                h,st,tp=cs[j]; oh,ost,otp=other[j]
                assert h==oh and st==ost and tp[:2]==otp[:2]
                diff={p for p in range(len(tp)) if tp[p]!=otp[p]}
                assert diff=={q+2+i}
                assert hits[i]>=q>j
                assert trace[j][0] not in diff
                assert trace[:hits[i]]==other_trace[:hits[i]]
                reuse[hits[i]]+=1; comparisons+=1
        assert max(reuse.values())==q
        # Carry potential through the same physical suffix. No reset per checkpoint.
        potential=q; drops=0
        for t,event in enumerate(trace):
            new=potential-int(t in hits.values())
            assert 0<=potential-new<=1
            drops+=potential-new; potential=new
        assert potential==0 and drops==q
        rows.append(dict(q=q,suffix_transitions=len(trace),
                         naive_checkpoint_sum=q*q,first_hit_events=q,
                         max_event_reuse=q,padding_interval_hits=0))
    print(json.dumps(dict(status="PASS",packed_and_suffix_cases=labels,
          single_bit_mutations=len(s),mutation_accept=mutation_accept,
          mutation_reject=mutation_reject,extra_guard_failures=len(extra),
          checkpoint_opponent_comparisons=comparisons,rows=rows,
          scope="Finite suffix machine and reference guard; full tape recognizer symbolic."),
          indent=2,sort_keys=True))
if __name__=='__main__': main()

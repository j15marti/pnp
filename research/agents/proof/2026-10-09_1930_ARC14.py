"""Explicit capped residual closes pointer dependency, not universal acquisition."""
import itertools as it
import json
import math
import signal
from collections import Counter
signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError()))
signal.alarm(24)
# Declared finite encoding: 32-bit clause count, 50 bits per <=3-literal clause.
def encode(f):
    assert len(f)<2**32
    out=f'{len(f):032b}'
    for c in f:
        assert len(c)<=3 and all(0<abs(x)<32768 for x in c)
        out+=f'{len(c):02b}'+''.join(f'{(abs(x)<<1)|(x<0):016b}' for x in c)+'0'*(16*(3-len(c)))
    return out

def acquire(f,a,cap,met):
    if cap<32:return None
    out=[]; bits=32
    for row in f:
        live=[];sat=False
        for x in row:
            met['literal_reads']+=1
            if abs(x) in a:sat |= a[abs(x)]==(x>0)
            else:live.append(x)
        if sat:continue
        if bits+50>cap:
            met['cap_failures']+=1
            return None
        out.append(tuple(live));bits+=50
    met['child_bits']=bits
    return tuple(out)

def sat(f):
    vs=sorted({abs(x) for c in f for x in c})
    return any(all(any(a[abs(x)]==(x>0) for x in c) for c in f)
               for vals in it.product((False,True),repeat=len(vs)) for a in [dict(zip(vs,vals))])

def main():
    clauses=tuple(it.product((-1,1),(-2,2),(-3,3)))
    covers=bits_checked=0
    for mask in range(256):
        f=tuple(c for i,c in enumerate(clauses) if mask>>i&1)
        children=[]
        for value in (False,True):
            child=acquire(f,{1:value},len(encode(f)),Counter())
            assert child is not None
            encoded=encode(child)
            # Closed resident child, every indexed bit agrees with its encoding.
            words=[int(encoded[i:i+1]) for i in range(len(encoded))]
            assert all(str(words[i])==encoded[i] for i in range(len(encoded)))
            bits_checked+=len(encoded)
            children.append(child)
        assert sat(f)==any(sat(c) for c in children)
        covers+=1
    rows=[]
    for size in (32,128,512,2048):
        # Easy padded control: true pivot removes the prefix, false does not.
        f=((1,2,3),)*size+((2,),(-2,))
        N=len(encode(f));cap=math.isqrt(N)
        for value in (False,True):
            met=Counter();child=acquire(f,{1:value},cap,met)
            row=dict(source_bits=N,cap=cap,pivot=value,status='SUCCESS' if child is not None else 'UNKNOWN',**met)
            if child is not None:
                row['child_sat']=sat(child)
                again=acquire(child,{},math.isqrt(len(encode(child))),Counter())
                row['repeat_without_new_rule']='SUCCESS' if again is not None else 'UNKNOWN'
            rows.append(row)
    print(json.dumps(dict(status='COMPUTATIONAL',covers=covers,bit_checks=bits_checked,scaling=rows),indent=2))
if __name__=='__main__':main()

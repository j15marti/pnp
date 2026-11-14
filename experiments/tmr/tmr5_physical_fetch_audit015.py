#!/usr/bin/env python3
"""Independent native CPython, current-cell-only one-head lookup audit.
Models individual local counter, unary, and input-head movements, not a compiled arbitrary SAT TM.
"""
import json, random
from collections import defaultdict

class Physical:
    def __init__(self, data, p):
        self.data=data;self.L=len(data);self.q=self.L+1
        assert 0<=p<=self.q
        self.w=max(1,(self.L+2-1).bit_length())
        self.address=[(p>>j)&1 for j in range(self.w)]
        self.down=[0]*self.w
        self.c_head=0;self.u_head=0;self.i_head=0;self.charges=0
        self.first_read=None;self.movement=0;self.counter_flips=0
    def tick(self):self.charges+=1
    def move_counter(self,d):
        assert d in [-1,1] and 0<=self.c_head+d<self.w
        self.c_head+=d;self.tick()
    def move_unary(self,d):
        assert d in [-1,1] and 0<=self.u_head+d<=self.w
        self.u_head+=d;self.tick()
    def move_input(self,d):
        assert d in [-1,1] and 0<=self.i_head+d<=self.q
        self.i_head+=d;self.tick();self.movement+=1
    def read_input(self):
        self.tick()
        pos=self.i_head
        symbol='<' if pos==0 else '>' if pos==self.q else self.data[pos-1]
        if self.first_read is None:self.first_read=pos
        return symbol
    def lookup(self):
        # Scratch setup from read-only stored binary source-position register, one charged symbol per bit.
        for j in range(self.w):
            assert self.c_head==j
            self.tick() # read source position register head at j, fixed work tape
            self.down[j]=self.address[j];self.tick() # write scratch j
            if self.address[j]:self.move_unary(1)
            if j+1<self.w:self.move_counter(1)
        while self.c_head>0:self.move_counter(-1)
        while True:
            self.tick() # zero test at unary work-tape left marker
            if self.u_head==0:break
            # Binary decrement: traverse from lsb until first 1, with physical head moves.
            t=0
            while self.down[self.c_head]==0:
                self.tick() # checked a zero
                self.down[self.c_head]=1;self.tick()
                self.counter_flips+=1
                self.move_counter(1);t+=1
            self.tick() # checked the terminating one
            self.down[self.c_head]=0;self.tick();self.counter_flips+=1
            while self.c_head>0:self.move_counter(-1)
            for j in range(t):self.move_unary(1)
            self.move_unary(-1)
            self.move_input(1)
        at_query=self.i_head
        symbol=self.read_input() # CRUCIAL: read while physical head is still at p
        while self.i_head>0:self.move_input(-1)
        assert self.i_head==0 and self.c_head==0 and self.u_head==0
        assert not any(self.down) and at_query==(sum(v<<j for j,v in enumerate(self.address)))
        assert self.charges<=30*(self.L+2)
        return symbol,at_query

def audit():
    cases=steps=moves=flips=0;read_distinct=defaultdict(int);samples=[]
    for L in range(12):
        for v in range(1<<L):
            x=f'{v:0{L}b}' if L else ''
            for p in range(L+2):
                m=Physical(x,p);got,cell=m.lookup()
                want='<' if p==0 else '>' if p==L+1 else x[p-1]
                assert got==want
                assert cell==p
                read_distinct[got]+=1;cases+=1;steps+=m.charges;moves+=m.movement;flips+=m.counter_flips
    random.seed(271828)
    for L in [15,24,25,31,32,63,64,127,128,255,256,511,512,1023,1024]:
        for trial in range(2):
            x=''.join(str(random.getrandbits(1)) for _ in range(L))
            for p in sorted(set([0,1,2,3,4,L//2,L,L+1])):
                m=Physical(x,p);got,cell=m.lookup()
                want='<' if p==0 else '>' if p==L+1 else x[p-1]
                assert got==want
                cases+=1;steps+=m.charges;moves+=m.movement;flips+=m.counter_flips
                if L==24 and trial==0 and p in [0,1,24,25]:samples.append({'L':L,'p':p,'read':got,'physical_head_at_read':cell,'physical_head_at_halt':m.i_head,'steps':m.charges})
    # One-bit neighbor adversary: sources agree on all earlier cells, differing ONLY at queried bit p.
    pairs=0
    for L in [1,2,3,7,15,24,64,256,1024]:
        for p in sorted(set([1,(L+1)//2,L])):
            z='0'*L;y=z[:p-1]+'1'+z[p:]
            a=Physical(z,p);b=Physical(y,p)
            assert a.lookup()[0]=='0' and b.lookup()[0]=='1'
            assert a.first_read==p and b.first_read==p
            assert a.movement>=2*p and b.movement>=2*p
            pairs+=1
    # Minimal witness of original published ledger ordering bug: return BEFORE current-cell read.
    x='1';head=1;head-=1
    assert head==0
    actual_left_cell='<'
    peer_indexed_value=x[0]
    assert actual_left_cell!=peer_indexed_value
    return {'nativePythonIndependent':True,'status':'COMPUTATIONAL','scope':'exact local current-cell input fetch and scanned-counter physical tape movements, not compiled arbitrary A',
      'lookup_cases':cases,'charged_microsteps':steps,'input_head_movements':moves,'binary_bit_flips':flips,
      'opposite_source_bit_pairs':pairs,'original_log_bug':'peer script restores physical input head before indexed read; p=1 x=1 actual current cell left endmarker, script returns 1',
      'repair':'read and cache actual current-cell symbol before the paid return to the left endmarker',
      'examples':samples,'assertion_failures':0}

if __name__=='__main__':
    print(json.dumps(audit(),indent=2))

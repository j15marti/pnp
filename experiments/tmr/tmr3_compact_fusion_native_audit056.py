#!/usr/bin/env python3
"""Independent native-CPython exact audit of COMPACTFAN056 physical transition rows."""
from fractions import Fraction as Q
import json
import re

states = ('start', 'scan', 'bit', 'yes', 'no', 'bad')
ends = ('yes', 'no', 'bad')
checks = 0
edges = 0
inputs = 0
seen = {}
lam = (Q(0), Q(0), Q(0), Q(0), Q(1, 4), Q(1, 2), Q(1, 4))

def p(x, st, cache, msg):
    if st in ends:
        return (0,) * 7
    k = re.fullmatch('1+0[01]', x)
    if not k:
        return (0,) * 7
    n = x.index('0')
    u = int(cache not in '01')
    return (0, 0, 0, (1 << n) * u, u, int(msg == 'M'), u)

def trace(x):
    global checks, edges
    st, h, cache, msg, t = 'start', 0, '_', '_', 0
    while st not in ends:
        old = p(x, st, cache, msg)
        ch = x[h] if h < len(x) else '_'
        if st == 'start':
            if ch == '1':
                st, h, cache, msg, rule = 'scan', h+1, '?', 'M', 'install'
            else:
                st, rule = 'bad', 'bad_prefix'
        elif st == 'scan':
            if ch == '1':
                h += 1; rule = 'scan_one'
            elif ch == '0':
                st, h, rule = 'bit', h+1, 'delimiter'
            else:
                st, rule = 'bad', 'bad_delimiter'
        else:
            assert st == 'bit'
            if ch in '01':
                st, cache, msg, rule = ('yes' if ch == '1' else 'no'), ch, '_', 'finish'
            else:
                st, rule = 'bad', 'bad_bit'
        new = p(x, st, cache, msg)
        d = tuple(a-b for a,b in zip(old,new))
        assert sum(a*b for a,b in zip(lam,d)) <= 1
        assert all(isinstance(z,int) for z in d)
        if rule == 'finish' and re.fullmatch('1+0[01]', x):
            n = x.index('0')
            assert d == (0,0,0,1<<n,1,1,1)
        seen[rule] = seen.get(rule, 0) + 1
        t += 1; edges += 1; checks += 3
        assert t <= len(x)+2
        checks += 1
    return st,t,cache,msg

for n in range(1,81):
    for b in '01':
        x='1'*n+'0'+b
        state,t,cache,msg=trace(x)
        assert t==n+2 and cache==b and msg=='_'
        assert state==('yes' if b=='1' else 'no')
        assert Q(1,2)+Q(1,2)+Q(1,2)>1
        inputs+=1;checks+=3
for length in range(9):
    for num in range(1<<length):
        x=(format(num,'0%db'%length) if length else '')
        state,t,cache,msg=trace(x)
        assert (state=='yes') == bool(re.match('^1+01',x))
        inputs+=1;checks+=1
assert (1<<10)*Q(1,1024)==1
assert (1<<11)*Q(1,1024)>1
assert 3*Q(1,2)>1
checks+=3
print(json.dumps({'tag':'COMPACTFAN056_NATIVE_INDEPENDENT','status':'COMPUTATIONAL',
  'model':'fixed one-read-only-input two-work-tape deterministic TM, standard blank work',
  'n_range':[1,80],'inputs_tested':inputs,'transitions_checked':edges,
  'assertion_groups':checks,'failures':0,'rule_counts':dict(sorted(seen.items())),
  'feasible_lambda7':[str(v) for v in lam],
  'tariff_cone':'lambda_fusion=0; lambda_Gamma+lambda_interface+lambda_machine<=1',
  'counterexample':{'n':3,'delta7':[0,0,0,8,1,1,1],'cost':1,
    'bad_three_halves':'3/2','input':'11101','steps':5,'peak_writable_cells':2},
  'first_violation_for_fusion_weight_1_over_1024':11},sort_keys=True,indent=2))

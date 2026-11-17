#!/usr/bin/env python3
"""TMR-3/067: affine long-depth overwrite, genuine phase crossings and last writer.
Finite oracle/reference audit only: Python arrays are NOT a space-measurement.
"""
import hashlib
import json
import random
from pathlib import Path

SEED = 202611171124
REV = 'tmr3-affine-overwrite067-v1'
RNG = random.Random(SEED)
C = {'valid': 0, 'malformed': 0, 'checkpoint_queries': 0,
     'crossings': 0, 'graph_queries': 0, 'terms': 0, 'assertions': 0}

def check(ok):
    C['assertions'] += 1
    if not ok:
        raise AssertionError(f"assertion {C['assertions']}")

def encode(b, y):
    return '1' * (b - 1) + '0' + ''.join(str(z) for z in y)

def parse(x):
    if not x or set(x) - {'0', '1'}:
        return None
    leading = len(x) - len(x.lstrip('1'))
    b = leading + 1
    if b < 2 or b & (b - 1) or len(x) != b + b**3 or x[b-1] != '0':
        return None
    return b, [int(q) for q in x[b:]]

def lucas_value(y, layer, i):
    a = 0
    for j in range(min(layer, i) + 1):
        if (j & layer) == j:
            a ^= y[i-j]
            C['terms'] += 1
    return a

def reference_layers(y, R):
    layers = [y[:]]
    for _ in range(R):
        a = layers[-1]
        layers.append([a[i] ^ (a[i-1] if i else 0)
                       for i in range(len(y))])
    return layers

def stage_duration(b):
    return 2*b**3 + b

def last_writer(b, time, tape, i):
    M, D, R = b**3, stage_duration(b), b**3-1
    if tape not in (0, 1) or i < 0 or i >= M or time < i+1:
        return -1
    layer = min(R, (time-(i+1))//D)
    if layer % 2 != tape:
        layer -= 1
    return layer

def head_pos(b, time):
    M, D, R = b**3, stage_duration(b), b**3-1
    if time >= (R+1)*D:
        return 0
    r = time % D
    if r <= M:
        return r
    if r < M+b:
        return M
    return M-(r-(M+b)+1)

def crossing_audit(b):
    M, D, R = b**3, stage_duration(b), b**3-1
    t, pos = 0, 0
    for layer in range(R+1):
        check(t % b == 0 and pos == 0)
        for _ in range(M):
            before = pos
            pos += 1
            t += 1
            if before//b != pos//b:
                check(t % b == 0)
                C['crossings'] += 1
        t += b-1
        check(t % b == b-1)
        for _ in range(M):
            before = pos
            pos -= 1
            t += 1
            if before//b != pos//b:
                check(t % b == 0)
                C['crossings'] += 1
        t += 1
        check(pos == 0 and t == (layer+1)*D)
    check(t == (R+1)*D)

def audit_source(b, y, all_checkpoints=False):
    s = encode(b, y)
    parsed = parse(s)
    check(parsed is not None and parsed[0] == b and parsed[1] == y)
    M, D, R = b**3, stage_duration(b), b**3-1
    layers = reference_layers(y, R)
    check(layers[-1][-1] == (sum(y) & 1))
    check(lucas_value(y, R, M-1) == layers[-1][-1])
    if all_checkpoints:
        for ell in range(R+1):
            for i in range(M):
                check(lucas_value(y, ell, i) == layers[ell][i])
    else:
        for _ in range(70):
            ell, i = RNG.randrange(R+1), RNG.randrange(M)
            check(lucas_value(y, ell, i) == layers[ell][i])
    for _ in range(75):
        time = RNG.randrange((R+1)*D+1)
        i = RNG.randrange(M)
        tape = RNG.randrange(2)
        w = last_writer(b,time,tape,i)
        expected = max((ell for ell in range(R+1)
                        if ell%2==tape and time >= ell*D+i+1), default=-1)
        check(w == expected)
        if w >= 0:
            check(lucas_value(y,w,i) == layers[w][i])
        C['checkpoint_queries'] += 1
    for bad in (s+'0', s[:-1], '0'+s, s.replace('0','x',1)):
        check(parse(bad) is None)
        C['malformed'] += 1
    C['valid'] += 1

def run():
    for b in (2,4,8):
        crossing_audit(b)
        M,R,D = b**3,b**3-1,stage_duration(b)
        B = ((R+1)*D+1+b-1)//b
        for j in range(1,B+1):
            pos = head_pos(b,(j-1)*b)
            check(0 <= pos <= M)
            C['graph_queries'] += 2
        if b == 2:
            for mask in range(1<<M):
                audit_source(b,[(mask>>i)&1 for i in range(M)],True)
        elif b == 4:
            for _ in range(28):
                audit_source(b,[RNG.randrange(2) for _ in range(M)],True)
        else:
            for _ in range(3):
                audit_source(b,[RNG.randrange(2) for _ in range(M)],False)
    payload={'revision':REV,'seed':SEED,'status':'COMPUTATIONAL',
             'counters':C,'failures':0,'widths':[2,4,8],
             'model':'standard-library reference array audit; not native TM memory or a general HPV converter',
             'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    return payload

if __name__ == '__main__':
    result = run()
    dest=Path('/mnt/data/tmr3_067/tmr3_affine_overwrite067_raw.json')
    dest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

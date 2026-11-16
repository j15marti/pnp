#!/usr/bin/env python3
"""Independent serialized-OBDD checker for TMR-4/062; does not import compiler."""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, subprocess, sys, tempfile
from pathlib import Path

SEED = 202611152112

def source(n: int, balanced: bool, seed: int | None) -> dict:
    rng = random.Random(seed) if seed is not None else None
    gates = []
    def gate(a, b, op):
        name = f'g{len(gates)}'
        gates.append(dict(id=name, a=a, b=b, op=rng.randrange(16) if rng else op))
        return name
    def visit(inputs):
        if len(inputs) == 1:
            return inputs[0]
        split = len(inputs)//2 if balanced else len(inputs)-1
        a, b = visit(inputs[:split]), visit(inputs[split:])
        p, q = gate(a,b,8), gate(a,b,6)
        return gate(p,q,14)
    root = visit([f'x{i}' for i in range(n)])
    return dict(version=1,n=n,gates=gates[::-1],root=root)

def evaluate(obj, bits):
    # Independent readiness scans; no compiler traversal, cache or order reused.
    values = {f'x{i}': b for i,b in enumerate(bits)}
    pending = obj['gates'][:]
    while pending:
        nxt = []
        for e in pending:
            if e['a'] in values and e['b'] in values:
                values[e['id']] = (e['op'] >> (2*values[e['a']]+values[e['b']])) & 1
            else:
                nxt.append(e)
        if len(nxt) == len(pending):
            raise ValueError('unresolved source')
        pending = nxt
    return values[obj['root']]

def run(compiler: Path) -> dict:
    checks = assignments = sources = arcs = 0
    def check(condition):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError('independent serialized verification failed')
    with tempfile.TemporaryDirectory() as folder:
        inp, out = Path(folder)/'source.json', Path(folder)/'compiled.json'
        for n in range(2,9):
            for balanced in (False,True):
                for seed in (None,SEED+n):
                    obj = source(n,balanced,seed)
                    data = json.dumps(obj,sort_keys=True,separators=(',',':')).encode('ascii')
                    inp.write_bytes(data)
                    subprocess.run([sys.executable,str(compiler),'--source',str(inp),'--output',str(out)],check=True,capture_output=True)
                    b = json.loads(out.read_text())
                    check(b['source_sha256'] == hashlib.sha256(data).hexdigest())
                    check(sorted(layer['input'] for layer in b['layers']) == list(range(n)))
                    check(b['k'] == 2*n-2 and b['tree_core'])
                    ways = {0:1}
                    for layer in b['layers']:
                        nxt = {}
                        for i,node in enumerate(layer['nodes']):
                            check(node['id'] == i and len(node['next']) == 2)
                            for dest in node['next']:
                                nxt[dest] = nxt.get(dest,0)+ways.get(i,0)
                                arcs += 1
                        ways=nxt
                    check(sum(ways.values()) == 1<<n)
                    yes = 0
                    for bits in itertools.product((0,1),repeat=n):
                        answer = evaluate(obj,bits)
                        pointer = 0
                        for layer in b['layers']:
                            pointer = layer['nodes'][pointer]['next'][bits[layer['input']]]
                        check(pointer == answer)
                        yes += answer
                        assignments += 1
                    check(ways.get(1,0) == yes == int(b['count']))
                    if seed is None:
                        check(yes == (1<<n)-1)
                    sources += 1
    return dict(revision='tmr4-serialized-check062.v1',seed=SEED,status='COMPUTATIONAL',sources=sources,assignments=assignments,serialized_arcs=arcs,checks=checks,failures=0,compiler_sha256=hashlib.sha256(compiler.read_bytes()).hexdigest(),verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('compiler',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    text=json.dumps(run(args.compiler.resolve()),sort_keys=True,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    else: print(text,end='')

if __name__=='__main__':main()

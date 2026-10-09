"""Audit original complete-cover builder; run from repository with --chunk tiny/scaling."""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import signal
import sys
from collections import Counter

signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError()))
signal.alarm(24)
parser=argparse.ArgumentParser();parser.add_argument('--chunk',choices=('tiny','scaling'),required=True)
parser.add_argument('--early',action='store_true');parser.add_argument('--source',default='final_link_hybrid_builder.py');args=parser.parse_args()
spec=importlib.util.spec_from_file_location('audit_base',args.source)
b=importlib.util.module_from_spec(spec);sys.modules[spec.name]=b;spec.loader.exec_module(b)
context={}; extra=Counter(); original_canonical=b.canonical;original_restrict=b.restrict_formula

def canonical(raw,met=None):
    if met is None:
        extra['previously_unmetered_canonical_calls']+=1
        return original_canonical(raw,extra)
    return original_canonical(raw,met)

def restrict(f,a,met):
    context['assignment']=dict(a); context['forced']={}
    extra['executed_restrictions']+=1
    child=original_restrict(f,a,met)
    extra['emitted_child_bits_with_multiplicity']+=b.encoding_bits(child)
    return child
b.canonical=canonical;b.restrict_formula=restrict

class Positive(Exception):
    def __init__(self,w): self.w=w

original_simplify=b.simplify_units; original_base=b.base_solve
def simplify(f,met):
    result=original_simplify(f,met)
    context['forced']=result[1]
    return result
def base(f,met,frontier_cap=4):
    result=original_base(f,met,frontier_cap)
    if args.early and result[0] and result[1]:
        w={**context.get('assignment',{}),**context.get('forced',{}),**result[2]}
        extra['witness_validation_literal_budget']+=sum(map(len,context['source']))
        # Verification against the full original source is mandatory.
        if b.satisfies(context['source'],w): raise Positive(w)
    return result
b.simplify_units=simplify;b.base_solve=base

def exact(f):
    vs=b.variables(f)
    return any(b.satisfies(f,dict(zip(vs,values))) for values in it.product((False,True),repeat=len(vs)))

def run(label,f):
    extra.clear();context.clear();context['source']=f
    builder=b.Builder(f,'backdoor')
    try: result=builder.try_backdoor_value(builder.source)
    except Positive as found: result=(True,found.w,'verified-positive-term')
    answer=None if result is None else result[0]
    reference=exact(f)
    assert answer is None or answer==reference
    if result is not None and answer:
        assert b.satisfies(f,result[1])
    return dict(label=label,input_bits=builder.M,answer=answer,reference=reference,
                route=None if result is None else result[2],metrics=dict(builder.met),extra=dict(extra))

if args.chunk=='tiny':
    core=tuple(it.product((-1,1),(-2,2),(-3,3)))
    rows=[run(str(mask),tuple(c for i,c in enumerate(core) if mask>>i&1)) for mask in range(256)]
else:
    rows=[run('hub',b.hub_formula(10,15))]
    rows += [run('random10_'+str(seed),b.random_3cnf(10,40,seed)) for seed in range(8)]
    rows += [run('random12_'+str(seed),b.random_3cnf(12,48,seed)) for seed in range(4)]
print(json.dumps(dict(status='COMPUTATIONAL',source_sha256=hashlib.sha256(Path(args.source).read_bytes()).hexdigest(),
    chunk=args.chunk,early=args.early,cases=len(rows),covered=sum(r['answer'] is not None for r in rows),rows=rows),indent=2))

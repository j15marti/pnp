#!/usr/bin/env python3
"""LSPV-3/423: paid LOCAL adapter for already valid typed mixed proof DAGs.
The original proof must be independently validated under the stated semantic
R_mix341 rules. The translator is NOT a checker for the entire historical grammar.
Usage: python experiments/arc/lspv3_423_compiler.py results/raw/arc/..._raw.json
"""
import base64, copy, hashlib, json, sys
SOURCE=b'p cnf 3 5\n1 2 0\n1 -2 0\n-2 3 0\n-2 -3 0\n-1 2 0\n'

def check_source(proof,external):
    try: encoded=base64.b64decode(proof['raw_source_b64'],validate=True)
    except Exception as e: raise ValueError('bad source encoding') from e
    if encoded!=external or base64.b64encode(encoded).decode()!=proof['raw_source_b64']:
        raise ValueError('externally supplied raw source differs')
    if hashlib.sha256(external).hexdigest()!=proof['raw_sha256']:
        raise ValueError('source hash mismatch')

def factor_of_row(row):
    assert row['type']=='affine'
    mask=row['mask']
    if len(mask)>3 or mask!=sorted(set(mask)):
        raise ValueError('unsupported original affine mask')
    return {'type':'factor','support':mask,
            'truth':[int((sum((z>>j)&1 for j in range(len(mask)))&1)==row['rhs'])
                     for z in range(1<<len(mask))]}

def convert(native,external):
    check_source(native,external)
    nodes=native['nodes']; outputs=[]; old_to_new={}; adapters={}
    def mapped(r):
        r=copy.deepcopy(r)
        if 'node' in r:
            if r['node'] not in old_to_new: raise ValueError('forward reference')
            r['node']=old_to_new[r['node']]
        return r
    for old_i,old in enumerate(nodes):
        if old['id']!=old_i: raise ValueError('misordered old node')
        new=copy.deepcopy(old)
        for edge in ('left','right','parent'):
            if edge not in new: continue
            oldref=old[edge]
            updated=mapped(oldref)
            if old['rule']=='AND3' and oldref.get('view')=='affine':
                old_parent=oldref.get('node')
                if not isinstance(old_parent,int) or not 0<=old_parent<old_i:
                    raise ValueError('unauthenticated affine parent')
                key=(old_parent,'affine')
                if key not in adapters:
                    row=nodes[old_parent].get('affine')
                    if row is None: raise ValueError('missing authenticated affine row')
                    local={'id':len(outputs),'rule':'LOCAL','parent':updated,'out':factor_of_row(row)}
                    adapters[key]=local['id']; outputs.append(local)
                updated={'node':adapters[key],'view':'factor'}
            new[edge]=updated
        new['id']=len(outputs); old_to_new[old_i]=new['id']; outputs.append(new)
    target={k:copy.deepcopy(v) for k,v in native.items() if k!='nodes'}
    target['nodes']=outputs; target['final']=mapped(native['final'])
    assert len(outputs)==len(nodes)+len(adapters)<=2*len(nodes)
    return target,adapters

if __name__=='__main__':
    fname=sys.argv[1] if len(sys.argv)>1 else 'results/raw/arc/2026-11-05_0624_LSPV3_AFFINE_PARENT_ADAPTER423_raw.json'
    raw=json.load(open(fname,encoding='utf-8'))
    external=open(sys.argv[2],'rb').read() if len(sys.argv)>2 else SOURCE
    result,cached=convert(raw['native'],external)
    assert result==raw['compiled'],'compiler output differs from independently replayed proof'
    print(json.dumps({'status':'PASS','q_native':len(raw['native']['nodes']),
       'q_target':len(result['nodes']),'paid_adapter_cache':len(cached),
       'source_sha256':hashlib.sha256(external).hexdigest()}))

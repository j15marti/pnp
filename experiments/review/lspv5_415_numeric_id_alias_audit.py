#!/usr/bin/env python3
import argparse, copy, hashlib, json, pathlib, re, subprocess, tempfile, time

ID_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,63}$')

def sha(b): return hashlib.sha256(b).hexdigest()

def strict_string_ids(data):
    for f in data['fixtures']:
        ids=[]
        for c in f['clauses']:
            if not isinstance(c['id'],str) or not ID_RE.fullmatch(c['id']): return False
            ids.append(c['id'])
        for p in f['proof']:
            if not isinstance(p['id'],str) or not ID_RE.fullmatch(p['id']): return False
            ids.append(p['id'])
            if any(not isinstance(x,str) or not ID_RE.fullmatch(x) for x in p['parents']): return False
        if len(ids)!=len(set(ids)): return False
    return True

def source_alias(base, source_id, parent_id):
    d=copy.deepcopy(base); f=d['fixtures'][0]; old=f['clauses'][0]['id']
    f['clauses'][0]['id']=source_id
    for deleted in f['deleted']:
        if deleted['sourceId']==old: deleted['sourceId']=source_id
    hits=0
    for p in f['proof']:
        p['parents']=[parent_id if x==old else x for x in p['parents']]
        hits += sum(x==parent_id for x in p['parents'])
    assert hits>0
    return d

def derived_alias(base, node_id, parent_id):
    d=copy.deepcopy(base); f=d['fixtures'][0]; old=f['proof'][0]['id']
    f['proof'][0]['id']=node_id
    hits=0
    for p in f['proof'][1:]:
        p['parents']=[parent_id if x==old else x for x in p['parents']]
        hits += sum(x==parent_id for x in p['parents'])
    assert hits>0
    return d

def run(checker, obj):
    b=(json.dumps(obj,separators=(',',':'))+'\n').encode()
    with tempfile.NamedTemporaryFile(suffix='.json') as t:
        t.write(b);t.flush(); t0=time.perf_counter()
        p=subprocess.run(['node',str(checker),t.name],capture_output=True,text=True)
        elapsed=time.perf_counter()-t0
    return {'accepted':p.returncode==0,'returncode':p.returncode,'bytes':len(b),'sha256':sha(b),
            'stdout_sha256':sha(p.stdout.encode()),'stderr_tail':p.stderr[-300:],'seconds':elapsed}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--checker',required=True); ap.add_argument('--packet',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    checker=pathlib.Path(a.checker); packet=pathlib.Path(a.packet); base=json.loads(packet.read_text())
    cases={
      'baseline':base,
      'source_pos_2p53_collision':source_alias(base,2**53,2**53+1),
      'source_neg_2p53_collision':source_alias(base,-2**53,-(2**53+1)),
      'source_2p60_collision':source_alias(base,2**60,2**60+1),
      'derived_pos_2p53_collision':derived_alias(base,2**53,2**53+1),
      'safe_distinct_control':source_alias(base,2**53-2,2**53-1),
      'representable_distinct_control':source_alias(base,2**53,2**53+2),
      'null_id_same_token':source_alias(base,None,None),
      'boolean_id_same_token':source_alias(base,True,True),
    }
    results={k:run(checker,v) for k,v in cases.items()}
    expected={'baseline':True,'source_pos_2p53_collision':True,'source_neg_2p53_collision':True,
      'source_2p60_collision':True,'derived_pos_2p53_collision':True,'safe_distinct_control':False,
      'representable_distinct_control':False,'null_id_same_token':True,'boolean_id_same_token':True}
    assert all(results[k]['accepted']==v for k,v in expected.items())
    repairs={k:strict_string_ids(v) for k,v in cases.items()}
    assert repairs['baseline'] and all(not repairs[k] for k in cases if k!='baseline')
    out={'run':'LSPV-5/415','timestamp_pst':'2026-11-07 10:48 PST',
      'checker':{'path':str(checker),'sha256':sha(checker.read_bytes())},
      'packet':{'path':str(packet),'sha256':sha(packet.read_bytes()),'bytes':packet.stat().st_size},
      'results':results,'expected_acceptance':expected,'strict_string_id_repair':repairs,
      'theorem':'JSON.parse maps distinct integer tokens outside the safe range to one Number value; Map-based ID lookup therefore accepts byte-distinct source or derived parent references.',
      'scope':'Recovered SOURCE/AND3/XOR checker only; no satisfiable source accepted and no proof-size lower bound or B3 result.'}
    pathlib.Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','cases':len(cases),'accepted':sum(x['accepted'] for x in results.values()),'out':a.out}))

if __name__=='__main__': main()

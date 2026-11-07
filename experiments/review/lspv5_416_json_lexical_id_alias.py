#!/usr/bin/env python3
import argparse, copy, hashlib, json, pathlib, re, subprocess, tempfile, time

ID_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,63}$')

def sha(b): return hashlib.sha256(b).hexdigest()

def raw_alias(base, kind, definition_token, reference_token):
    d=copy.deepcopy(base); f=d['fixtures'][0]
    if kind=='source':
        old=f['clauses'][0]['id']; f['clauses'][0]['id']='__DEF__'
        for x in f['deleted']:
            if x['sourceId']==old: x['sourceId']='__DEF__'
    else:
        old=f['proof'][0]['id']; f['proof'][0]['id']='__DEF__'
    for p in f['proof']:
        p['parents']=['__REF__' if x==old else x for x in p['parents']]
    raw=json.dumps(d,separators=(',',':'))
    assert raw.count('"__DEF__"')>=1 and raw.count('"__REF__"')>=1
    return raw.replace('"__DEF__"',definition_token).replace('"__REF__"',reference_token)

def strict_string_ids(raw):
    try: d=json.loads(raw)
    except Exception: return False
    for f in d['fixtures']:
        ids=[]
        for c in f['clauses']:
            if not isinstance(c['id'],str) or not ID_RE.fullmatch(c['id']): return False
            ids.append(c['id'])
        for p in f['proof']:
            if not isinstance(p['id'],str) or not ID_RE.fullmatch(p['id']): return False
            ids.append(p['id'])
            if any(not isinstance(x,str) or not ID_RE.fullmatch(x) for x in p['parents']): return False
        if len(ids)!=len(set(ids)): return False
        if any(not isinstance(x['sourceId'],str) or not ID_RE.fullmatch(x['sourceId']) for x in f['deleted']): return False
    return True

def run(checker, raw):
    b=(raw+'\n').encode()
    with tempfile.NamedTemporaryFile(suffix='.json') as t:
        t.write(b); t.flush(); t0=time.perf_counter()
        p=subprocess.run(['node',str(checker),t.name],capture_output=True,text=True)
        elapsed=time.perf_counter()-t0
    return {'accepted':p.returncode==0,'returncode':p.returncode,'bytes':len(b),'sha256':sha(b),
            'stdout_sha256':sha(p.stdout.encode()),'stderr_tail':p.stderr[-400:],'seconds':elapsed}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--checker',required=True); ap.add_argument('--packet',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    checker=pathlib.Path(a.checker); packet=pathlib.Path(a.packet); original=packet.read_text(); base=json.loads(original)
    cases={
      'baseline':original.rstrip('\n'),
      'source_negzero_zero':raw_alias(base,'source','-0','0'),
      'source_one_decimal':raw_alias(base,'source','1','1.0'),
      'source_one_exp':raw_alias(base,'source','1','1e0'),
      'source_one_ExpPlus':raw_alias(base,'source','1','1E+0'),
      'source_negone_decimal':raw_alias(base,'source','-1','-1.0'),
      'derived_negzero_zero':raw_alias(base,'derived','-0','0'),
      'derived_one_exp':raw_alias(base,'derived','1','1e0'),
      'source_zero_one_control':raw_alias(base,'source','0','1'),
      'derived_one_two_control':raw_alias(base,'derived','1','2'),
    }
    expected={k:(k=='baseline' or not k.endswith('_control')) for k in cases}
    results={k:run(checker,v) for k,v in cases.items()}
    assert all(results[k]['accepted']==v for k,v in expected.items())
    repair={k:strict_string_ids(v) for k,v in cases.items()}
    assert repair['baseline'] and all(not repair[k] for k in cases if k!='baseline')
    out={'run':'LSPV-5/416','timestamp_pst':'2026-11-07 12:48 PST',
      'checker':{'path':str(checker),'sha256':sha(checker.read_bytes())},
      'packet':{'path':str(packet),'sha256':sha(packet.read_bytes()),'bytes':packet.stat().st_size},
      'results':results,'expected_acceptance':expected,'strict_string_id_repair':repair,
      'theorem':'Valid safe-range JSON number spellings can be byte-distinct but parse to one Number; Map also applies SameValueZero to -0 and +0. Raw node identity is therefore not authenticated even inside the safe-integer range.',
      'scope':'Recovered SOURCE/AND3/XOR checker only; no satisfiable source, shorter proof, full grammar, mixed lower bound or B3 result.'}
    pathlib.Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','cases':len(cases),'accepted':sum(x['accepted'] for x in results.values()),'out':a.out}))

if __name__=='__main__': main()

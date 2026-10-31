#!/usr/bin/env python3
"""Full original-source S/U adverse controls for LSPV3 GATE280.
Outputs gzip/base64 portable UTF-8 JSON and source sha256. Standard library.
Neither local extremes nor their disagreements imply arbitrary global UNSAT.
"""
import argparse, ast, base64, collections, gzip, hashlib, itertools, json, pathlib

def source_case(F,name):
    n=max(abs(x) for c in F for x in c)
    events=[];pairm=[];incompatible=0
    for j,C in enumerate(F):
        occ=[]
        for lit in C:
            v=abs(lit);S=int(lit>0);U=int(lit<0)
            occ.append({'literal':lit,'variable':v,'S':S,'invert_S_is_U':U,
                'U':U,'invert_U_is_S':S})
        events.append({'source_clause_index':j,'literal_occurrences':occ})
    for i,j in itertools.combinations(range(len(F)),2):
        S_i={v['variable']:v['S'] for v in events[i]['literal_occurrences']}
        U_i={v['variable']:v['U'] for v in events[i]['literal_occurrences']}
        S_j={v['variable']:v['S'] for v in events[j]['literal_occurrences']}
        U_j={v['variable']:v['U'] for v in events[j]['literal_occurrences']}
        mask=0
        for k,(a,b) in enumerate(((S_i,S_j),(S_i,U_j),(U_i,S_j),(U_i,U_j))):
            if all(a[x]==b[x] for x in a.keys()&b.keys()):mask|=1<<k
        if not mask:incompatible+=1
        pairm.append([i,j,mask])
    def count(mask):
        if mask==-1: a=[0]+[1]*n
        else:a=[0]+[(mask>>(v-1))&1 for v in range(1,n+1)]
        h=[0]*4
        for C in F:h[sum(a[abs(l)]==int(l>0) for l in C)]+=1
        return h
    trails=[]
    for mask in [0,1,3,7,-1]:
        h=count(mask)
        assert h[::-1]==count(((1<<n)-1) if mask==0 else (0 if mask==-1 else (((1<<n)-1)^mask)))
        if mask in (0,-1):assert h[0]>0
        trails.append({'source_mask':mask,'histogram_t0_t1_t2_t3':h,
            'complement_histogram':h[::-1], 'source_formula_satisfied':h[0]==0})
    implied=[]
    for i,c in enumerate(F):
        for j,d in enumerate(F):
            if i>=j:continue
            opposite=sorted({abs(x) for x in c if -x in d})
            for v in opposite:
                r=set(x for x in c if abs(x)!=v)|set(x for x in d if abs(x)!=v)
                if any(-x in r for x in r):continue
                R=sorted(r,key=lambda z:(abs(z),z<0))
                if len(implied)<24:implied.append({'parent_clause_indices':[i,j],'pivot_variable':v,
                        'derived_nontautological_resolvent':R,'prohibited_falsifying_cube':{abs(x):int(x<0) for x in R}})
    return {'name':name,'n':n,'m':len(F),'full_occurrence_extrema':events,
       'pair_mode_encoding':'1 SS + 2 SU + 4 US + 8 UU, 0=incompatible',
       'all_source_indexed_clause_pair_modes':pairm,
       'pairs_checked':len(pairm),'none_compatible_pair_count':incompatible,
       'globally_coherent_endpoint_and_flip_controls':trails,
       'first_24_original_source_resolution_proofs':implied,
       'source_forbidden_cubes':'Each original clause directly forbids its full local U occurrence assignment; these are original-clause axioms, not standalone UNSAT certificates.'}

def main():
    a=argparse.ArgumentParser();a.add_argument('--data',required=True);a.add_argument('--u',required=True);a.add_argument('--output',required=True);args=a.parse_args()
    raw=json.load(open(args.data))
    src=pathlib.Path(args.u).read_text(encoding='utf8')
    U=ast.literal_eval('\n'.join(x for x in src.splitlines() if x.strip() and not x.startswith('#')))
    compact=hashlib.sha256(json.dumps(U,separators=(',',':')).encode()).hexdigest()
    assert compact=='4ed9031a7a1b1fa9fcb752f9feece1ea7201df6b610059b90793517ecd874001'
    out={'run':'GATE280 full adverse source extrema','U_compact_json_sha256':compact,
         'note':'All source indexed; no inferred source hardness; antecedents and SAT/UNSAT kept separate',
         'controls':[source_case(t['formula'],t['name']) for t in raw['cases']]+[source_case(U,'DOECKER_U198_UNSAT')]}
    encoded=json.dumps(out,sort_keys=True,separators=(',',':')).encode('utf8')
    p=pathlib.Path(args.output)
    p.write_text(base64.b64encode(gzip.compress(encoded,mtime=0)).decode('ascii')+'\n')
    print(json.dumps({'controls':len(out['controls']),'pair_rows':sum(c['pairs_checked'] for c in out['controls']),
                      'occurrences':sum(3*c['m'] for c in out['controls']),
                      'raw_bytes':len(encoded),'gz_b64_bytes':p.stat().st_size,'raw_sha256':hashlib.sha256(encoded).hexdigest()},indent=2))
if __name__=='__main__':main()
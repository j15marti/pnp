#!/usr/bin/env node
'use strict';
// Independent no-import replay of REFEREE374's semantic claims and 11-node trace.
import fs from 'node:fs';
import assert from 'node:assert/strict';

const root = new URL('../../../', import.meta.url);
const raw = JSON.parse(fs.readFileSync(new URL('results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_raw.json', root)));
const certs = JSON.parse(fs.readFileSync(new URL('results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_certificates.json', root)));
let checks = 0;
const ok = x => { assert.ok(x); checks++; };
const eq = (a,b) => { assert.deepEqual(a,b); checks++; };
const norm = c => [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||Number(a<0)-Number(b<0));
const sat = (c,e) => Number(c.some(x => e[Math.abs(x)] === Number(x>0)));
const fval = (f,e) => f.truth[f.support.reduce((z,v,i)=>z+(e[v]<<i),0)];
const aval = (a,e) => Number(a.mask.reduce((z,v)=>z^e[v],0)===a.rhs);
const envs = s => Array.from({length:1<<s.length},(_,z)=>Object.fromEntries(s.map((v,i)=>[v,(z>>i)&1])));
const resolve = (a,b,p) => {
  if (a.includes(p)&&b.includes(-p)) return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
  if (a.includes(-p)&&b.includes(p)) return norm([...a.filter(x=>x!==-p),...b.filter(x=>x!==p)]);
  throw new Error('bad pivot');
};

eq(raw.status,'PASS');
eq(raw.exhaustive_actual_checker.clause_subclause_LOCAL_pairs,729);
eq(raw.exhaustive_actual_checker.affine_factor_subrelation_LOCAL_AND3_pairs,634);
eq(raw.resolution_strengthening_control.finite_set_cases,236196);
eq(raw.global_normalization_bound.linear_bound,'<=11q');
eq(raw.DEF_alias_normalization.accepted_old_and_normalized_gates,64);
eq(raw.DEF_alias_normalization.facets,256);
eq(raw.DEF_alias_normalization.exact_representatives+raw.DEF_alias_normalization.proper_subclause_representatives,256);
ok(raw.DEF_alias_normalization.maximum_local_nodes_excluding_validation_core<=11);
eq(Object.keys(certs).sort(),['affine_restore_sample','artifact','clause_restore_sample','lspv3_435_actual_canon2r']);

const wrapper=certs.lspv3_435_actual_canon2r;
eq(wrapper.format,'Rmix341-CANON2R');
ok(/^[0-9a-f]{64}$/.test(wrapper.source_raw_sha256));
const p=wrapper.proof;
eq(p.format,'Rmix341-CANON2');
eq(p.nodes.length,11);
const views=[];
const get = r => 'src' in r ? {kind:'clause',data:p.source.clauses[r.src]} : views[r.node][r.view];
for(const [i,n] of p.nodes.entries()) {
  eq(n.id,i);
  if(n.rule==='RES') {
    const a=get(n.left),b=get(n.right); eq(a.kind,'clause'); eq(b.kind,'clause');
    eq(n.clause,resolve(a.data,b.data,n.pivot));
    views.push({clause:{kind:'clause',data:n.clause}});
  } else if(n.rule==='AND3') {
    const a=get(n.left),b=get(n.right);
    const support=[...new Set([...(a.kind==='clause'?a.data.map(Math.abs):a.data.support),
                               ...(b.kind==='clause'?b.data.map(Math.abs):b.data.support)])].sort((x,y)=>x-y);
    eq(n.factor.support,support);
    const truth=envs(support).map(e=>(a.kind==='clause'?sat(a.data,e):fval(a.data,e)) &
                                      (b.kind==='clause'?sat(b.data,e):fval(b.data,e)));
    eq(n.factor.truth,truth);
    const rec={factor:{kind:'factor',data:n.factor}};
    if(n.affine){ for(const e of envs(support)) eq(fval(n.factor,e),aval(n.affine,e)); rec.affine={kind:'affine',data:n.affine}; }
    views.push(rec);
  } else if(n.rule==='LOCAL') {
    const a=get(n.parent), o=n.out;
    const os=o.kind==='clause'?o.clause.map(Math.abs):o.factor.support;
    const as=a.kind==='clause'?a.data.map(Math.abs):a.data.support;
    const support=[...new Set([...as,...os])].sort((x,y)=>x-y);
    for(const e of envs(support)) {
      const av=a.kind==='clause'?sat(a.data,e):fval(a.data,e);
      const ov=o.kind==='clause'?sat(o.clause,e):fval(o.factor,e);
      ok(!av||ov);
    }
    views.push({[o.kind]:{kind:o.kind,data:o.kind==='clause'?o.clause:o.factor}});
  } else if(n.rule==='GF2') {
    const a=get(n.left).data,b=get(n.right).data;
    const mask=[...new Set([...a.mask,...b.mask].filter(v=>!(a.mask.includes(v)&&b.mask.includes(v))))].sort((x,y)=>x-y);
    eq(n.affine,{mask,rhs:a.rhs^b.rhs});
    views.push({affine:{kind:'affine',data:n.affine}});
  } else throw new Error('unknown rule');
}
eq(views[10].affine.data,{mask:[],rhs:1});

// Independently recompute all clause restoration pairs: each literal is absent,
// C-only, or in D subset C.
let clausePairs=0;
const lits=[1,-1,2,-2,3,-3];
for(let code=0;code<3**6;code++){
  let z=code,C=[],D=[];
  for(const lit of lits){const st=z%3;z=Math.floor(z/3);if(st>=1)C.push(lit);if(st===2)D.push(lit);}
  C=norm(C);D=norm(D);
  for(const e of envs([1,2,3])) ok(!sat(D,e)||sat(C,e));
  clausePairs++;
}
eq(clausePairs,729);

// Count all subrelations of every affine relation on every support subset.
let affinePairs=0;
for(let sb=0;sb<8;sb++){
  const s=[1,2,3].filter(v=>sb&(1<<(v-1)));
  for(let mb=0;mb<(1<<s.length);mb++){
    const m=s.filter((_,i)=>mb&(1<<i));
    for(const rhs of [0,1]){
      const tr=envs(s).filter(e=>aval({mask:m,rhs},e)).length;
      affinePairs+=2**tr;
    }
  }
}
eq(affinePairs,634);

for(const [k,v] of Object.entries(raw.hostile_controls)) ok(k && v.startsWith('REJECTED:'));
const result={artifact:'REFEREE374-independent',status:'PASS',checks,
  peer_nodes:11,clause_pairs:clausePairs,affine_pairs:affinePairs,
  rss_bytes:process.memoryUsage().rss};
fs.writeFileSync(new URL('results/raw/arc/2026-11-05_1748_LSPV5_REFEREE374_independent.json',root),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));

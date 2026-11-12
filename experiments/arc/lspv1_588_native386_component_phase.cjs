'use strict';
/*
 * LSPV-1/588. Archived /386 original-checker source-domain discontinuity.
 * Usage from repository root:
 *   node experiments/arc/lspv1_588_native386_component_phase.cjs [output.json] [seed.json] [original_checker.js]
 * No dependencies beyond Node >=22. Replays unchanged pinned checker in actual OS subprocesses.
 * Supports local paths for independent verification; never modifies the original inputs.
 */
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const output = process.argv[2] || 'results/raw/arc/2026-11-12_0256_LSPV1_588_NATIVE386_COMPONENT_PHASE_OS_RAW.json';
const seedPath = process.argv[3] || 'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const checkerPath = process.argv[4] || 'experiments/arc/lspv2_386_independent_verify.js';
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const gitBlob = bytes => crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+bytes.length+'\0'), bytes])).digest('hex');
const seedBytes = fs.readFileSync(seedPath), checkerBytes = fs.readFileSync(checkerPath);
assert.equal(gitBlob(seedBytes),'318c52d99977ea4e91bc8554051138a700c1dc94','wrong historical seed');
assert.equal(gitBlob(checkerBytes),'338305c0ce101704205e57543756b8127074a986','wrong original checker');
const seed=JSON.parse(seedBytes);
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function build(types){
  let edges=seed.spec.edges.map(x=>[...x]), h=4;
  for(const type of types){
    const off=h;
    if(type==='K4'){
      edges.push(...seed.spec.edges.map(([u,v])=>[u+off,v+off]));h+=4;
    } else if(type==='K33'){
      for(let a=0;a<3;a++)for(let b=3;b<6;b++)edges.push([off+a,off+b]);h+=6;
    } else throw Error('unknown component '+type);
  }
  const guard=edges.length+1, charge=Array.from({length:h},(_,i)=>Number(i===0)), extra=[];
  for(let v=4;v<h;v++){
    const occ=[];edges.forEach(([u,w],i)=>{if(u===v||w===v)occ.push(i+1)});
    assert.equal(occ.length,3);
    for(let mask=0;mask<8;mask++){
      const bits=[mask&1,(mask>>1)&1,(mask>>2)&1];
      if((bits[0]+bits[1]+bits[2])%2!==charge[v]){
        extra.push({kind:'SOURCE',c:key([...occ.map((x,i)=>bits[i]?-x:x),-guard]),parents:[],source:v});
      }
    }
  }
  const L=x=>Math.abs(x)===7?Math.sign(x)*guard:x;
  const P=i=>i<16?i:i===16?16+extra.length:i+extra.length;
  const originalSource=seed.records.slice(0,16).map(r=>({...r,c:r.c.map(L)}));
  const oldResolution=seed.records.slice(17).map(r=>({...r,c:r.c.map(L),pivot:L(r.pivot),parents:r.parents.map(P)}));
  const records=[...originalSource,...extra,{kind:'SOURCE',c:[guard],parents:[],source:-1},...oldResolution];
  const p={spec:{h,edges,charge,guard},gate_defs:[[0,guard+1,1,4]],records,
    summary:{source:4*h+1,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:records.length}};
  assert.equal(records.filter(r=>r.kind==='SOURCE').length,4*h+1);
  assert.equal(records.filter(r=>r.kind==='RES').length,28);
  assert.equal(records.at(-1).c.length,0);
  assert(records.every((r,i)=>r.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i)));
  return p;
}
function removeExtraSource(p){
  const q=JSON.parse(JSON.stringify(p)),j=16;assert.equal(q.records[j].kind,'SOURCE');
  q.records.splice(j,1);
  for(const r of q.records){r.parents=r.parents.map(i=>{assert.notEqual(i,j,'removed source has proof dependents');return i>j?i-1:i;});}
  q.summary.source--;q.summary.live_records--;
  return q;
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv1-588-'));
function run(label,p,expect,expectedError){
  const filename=path.join(tmp,label+'.json');const b=Buffer.from(JSON.stringify(p)+'\n');fs.writeFileSync(filename,b);
  const r=spawnSync(process.execPath,[path.resolve(checkerPath),filename],{encoding:'utf8',maxBuffer:4*1024*1024});
  const accepted=r.status===0;
  const error=(r.stderr||'').match(/Error: ([^\n]+)/)?.[1]||null;
  assert.equal(accepted,expect,'unexpected checker verdict for '+label+' stderr='+r.stderr);
  if(expectedError)assert(error&&error.includes(expectedError),'incorrect rejection reason: '+error);
  const parsed=accepted?JSON.parse(r.stdout.trim().split('\n').at(-1)):null;
  if(accepted){assert.equal(parsed.paid,29);assert.equal(parsed.res,28);assert.equal(parsed.negativeTests,11);}
  return {label,accepted,sha256:sha256(b),bytes:b.length,h:p.spec.h,E:p.spec.edges.length,sources:p.summary.source,records:p.records.length,paid:p.summary.paid_total,assertions:parsed?.assertions||null,builtin_negatives:parsed?.negativeTests||null,error};
}
try{
  const cases=[
    ['original_K4',[],true,null],
    ['disconnected_h8_two_K4',['K4'],false,'even mismatch'],
    ['disconnected_h10_K4_plus_K33',['K33'],true,null],
    ['disconnected_h12_three_K4',['K4','K4'],true,null],
    ['disconnected_h16_four_K4',['K4','K4','K4'],true,null]
  ];
  const positives=cases.map(([label,types,expect,error])=>run(label,build(types),expect,error));
  const H=build(['K4','K4']);
  const corruptions=[
    ['missing_original',removeExtraSource(H),'missing original clauses'],
    ['forged_original',(()=>{const p=JSON.parse(JSON.stringify(H));p.records[16].c=[-p.spec.guard];return p;})(),'wrong source'],
    ['wrong_pivot',(()=>{const p=JSON.parse(JSON.stringify(H));p.records.at(-1).pivot=999;return p;})(),'bad pivot signs'],
    ['underpaid_owner',(()=>{const p=JSON.parse(JSON.stringify(H));p.summary.paid_total--;return p;})(),'paid cost'],
    ['unsupported_mixed_rule',(()=>{const p=JSON.parse(JSON.stringify(H));p.records.at(-1).kind='AND3';return p;})(),'record kind'],
    ['duplicate_graph_edge',(()=>{const p=JSON.parse(JSON.stringify(H));p.spec.edges[0]=p.spec.edges[1].slice();return p;})(),'duplicate edge']
  ];
  const negatives=corruptions.map(([label,p,reason])=>run(label,p,false,reason));
  // Incidence rank: over GF(2), every edge has two endpoints. For a disconnected graph with c components,
  // rank = h-c. The all-zero charge admits 2^(E-h+c) solutions, not the checker's 2^(E-h+1).
  const theoretical={h8_even_models:64,h8_checker_expected:32,first_component_K4_resolution:28,globally_paid_gate_count:1,
    constant_paid_cost:29,source_count_family:'17+16*k',record_count_family:'45+16*k',h_family:'4*(k+1)',k_at_least_two_accepted:true};
  const manifest={id:'LSPV-1/588',timestamp_local:'2026-11-12 02:56 PST',status:'PROVED/RESTRICTED original-code theorem; COMPUTATIONAL native OS replay',
    original_checker_blob:gitBlob(checkerBytes),seed_blob:gitBlob(seedBytes),node:process.version,positive_and_boundary:positives,hostile:negatives,theoretical,
    limitations:'Only archived /386 SOURCE/RES/AND2 sibling; not full R_mix341; formula family padded with disjoint easy components; does not establish a SAT lower bound.'};
  fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(manifest,null,2)+'\n');
  console.log(JSON.stringify(manifest));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}

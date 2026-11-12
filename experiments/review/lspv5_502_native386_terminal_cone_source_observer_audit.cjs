#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const outFile=process.argv[2]||path.join(root,'results/raw/review/2026-11-12_0348_LSPV5_502_TERMINAL_CONE_SOURCE_OBSERVER_RAW.json');
const witnessFile=process.argv[3]||path.join(root,'results/raw/review/2026-11-12_0348_LSPV5_502_DISCONNECTED_H8_REJECTED.json');
const acceptedFile=process.argv[4]||path.join(root,'results/raw/review/2026-11-12_0348_LSPV5_502_DISCONNECTED_H12_ACCEPTED.json');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const checkerBytes=fs.readFileSync(checker),seedBytes=fs.readFileSync(seedFile);
assert.equal(gitBlob(checkerBytes),'338305c0ce101704205e57543756b8127074a986');
assert.equal(gitBlob(seedBytes),'318c52d99977ea4e91bc8554051138a700c1dc94');
const seed=JSON.parse(seedBytes),clone=x=>JSON.parse(JSON.stringify(x));
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);

function build(extraK4) {
  let edges=seed.spec.edges.map(e=>e.slice()),h=4;
  for(let k=0;k<extraK4;k++) {
    const off=h;edges.push(...seed.spec.edges.map(([u,v])=>[u+off,v+off]));h+=4;
  }
  const guard=edges.length+1,charge=Array.from({length:h},(_,i)=>Number(i===0)),extra=[];
  for(let v=4;v<h;v++) {
    const occ=[];edges.forEach(([u,w],i)=>{if(u===v||w===v)occ.push(i+1)});
    assert.equal(occ.length,3);
    for(let mask=0;mask<8;mask++) {
      const bits=[mask&1,(mask>>1)&1,(mask>>2)&1];
      if((bits[0]+bits[1]+bits[2])%2!==charge[v])
        extra.push({kind:'SOURCE',c:key([...occ.map((x,i)=>bits[i]?-x:x),-guard]),parents:[],source:v});
    }
  }
  const L=x=>Math.abs(x)===7?Math.sign(x)*guard:x;
  const P=i=>i<16?i:i===16?16+extra.length:i+extra.length;
  const records=[...seed.records.slice(0,16).map(r=>({...r,c:r.c.map(L)})),...extra,
    {kind:'SOURCE',c:[guard],parents:[],source:-1},
    ...seed.records.slice(17).map(r=>({...r,c:r.c.map(L),pivot:L(r.pivot),parents:r.parents.map(P)}))];
  return {spec:{h,edges,charge,guard},gate_defs:[[0,guard+1,1,4]],records,
    summary:{source:4*h+1,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:records.length}};
}

function terminalAncestors(packet) {
  const seen=new Set(),stack=[packet.records.length-1];
  while(stack.length) {
    const i=stack.pop();if(seen.has(i))continue;seen.add(i);
    for(const p of packet.records[i].parents)stack.push(p);
  }
  return [...seen].sort((a,b)=>a-b);
}

function unsafeTerminalProjection(packet) {
  const keep=terminalAncestors(packet),ren=new Map(keep.map((x,i)=>[x,i])),oldGuard=packet.spec.guard;
  const normLit=x=>Math.abs(x)===oldGuard?Math.sign(x)*7:x;
  const records=keep.map(i=>{
    const r=clone(packet.records[i]);r.parents=r.parents.map(j=>ren.get(j));r.c=r.c.map(normLit);
    if(r.kind==='RES')r.pivot=normLit(r.pivot);return r;
  });
  return {spec:{h:4,edges:packet.spec.edges.slice(0,6).map(e=>e.slice(0,2)),charge:packet.spec.charge.slice(0,4),guard:7},
    gate_defs:[[0,8,1,4]],records,
    summary:{source:records.filter(r=>r.kind==='SOURCE').length,def_views:0,
      resolution:records.filter(r=>r.kind==='RES').length,paid_gates:1,paid_total:29,live_records:records.length}};
}

const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-502-'));
function run(label,p,expect,errorNeedle=null) {
  const bytes=Buffer.from(JSON.stringify(p)+'\n'),file=path.join(tmp,label+'.json');fs.writeFileSync(file,bytes);
  const r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:20000,maxBuffer:1<<20});
  const accepted=r.status===0&&!r.error;assert.equal(accepted,expect,label+': '+(r.error||r.stderr||r.stdout));
  const error=accepted?null:String(r.error||r.stderr).match(/Error: ([^\n]+)/)?.[1]||String(r.error||r.stderr).trim().split('\n')[0];
  if(errorNeedle)assert(error.includes(errorNeedle),label+': wrong error '+error);
  const parsed=accepted?JSON.parse(r.stdout.trim().split(/\r?\n/).at(-1)):null;
  if(accepted)assert.equal(parsed.paid,29);
  const cone=terminalAncestors(p).length;
  return {label,accepted,bytes:bytes.length,sha256:sha256(bytes),paid:p.summary.paid_total,
    h:p.spec.h,E:p.spec.edges.length,sources:p.summary.source,records:p.records.length,
    terminal_ancestors:cone,dead_records:p.records.length-cone,assertions:parsed?.assertions||null,error};
}

try {
  const p0=build(0),p1=build(1),p2=build(2);
  assert.deepEqual(p0,seed);
  const q0=unsafeTerminalProjection(p0),q1=unsafeTerminalProjection(p1),q2=unsafeTerminalProjection(p2);
  assert.deepEqual(q0,seed);assert.deepEqual(q1,seed);assert.deepEqual(q2,seed);
  const full=[run('K4_full_accept',p0,true),run('K4_disjoint_K4_full_reject',p1,false,'even mismatch'),run('three_K4_full_accept',p2,true)];
  const projected=[run('K4_projection_accept',q0,true),run('K4_disjoint_K4_projection_accept',q1,true),run('three_K4_projection_accept',q2,true)];
  const hostiles=[
    ['underpaid',p=>{p.summary.paid_total=28},'paid cost'],
    ['forged_source',p=>{p.records[16].c=[-p.spec.guard]},'wrong source'],
    ['wrong_pivot',p=>{p.records.at(-1).pivot=999},'bad pivot signs'],
    ['future_parent',p=>{p.records.at(-1).parents[0]=p.records.length-1},'bad parents'],
    ['unsupported_AND3',p=>{p.records.at(-1).kind='AND3'},'record kind'],
    ['duplicate_edge',p=>{p.spec.edges[0]=p.spec.edges[1].slice()},'duplicate edge']
  ].map(([label,mut,why])=>{const p=clone(p2);mut(p);return run(label,p,false,why)});
  const projectionHash=sha256(seedBytes);
  assert(projected.every(x=>x.sha256===projectionHash));
  assert.deepEqual(full.map(x=>x.accepted),[true,false,true]);
  assert.deepEqual(full.map(x=>x.paid),[29,29,29]);
  assert.deepEqual(full.map(x=>x.terminal_ancestors),[45,45,45]);
  assert.deepEqual(full.map(x=>x.dead_records),[0,16,32]);
  const result={id:'LSPV-5/502',timestamp_local:'2026-11-12 03:48 PST',
    status:'PROVED/RESTRICTED acceptance-preservation counterexample; COMPUTATIONAL original-OS validation',
    checker_git_blob:gitBlob(checkerBytes),seed_git_blob:gitBlob(seedBytes),
    theorem:'The full archived /386 CLI verdict is not a function of the terminal empty-clause ancestry plus paid work. The terminal-cone projection maps all three packets byte-for-byte to the same accepted W29 seed, while the full verdicts are ACCEPT/REJECT/ACCEPT.',
    projection:{definition:'retain terminal ancestors; renumber parents; discard disconnected source/spec components; normalize guard; preserve W29',
      exact_seed_sha256:projectionHash,all_three_projections_byte_identical:true,not_acceptance_preserving:true,
      counterexample:'K4 disjoint K4 is rejected, but its projected seed is accepted'},
    full,projected,hostiles,
    concrete_observer:'original checker lines 72-80 enumerate parity models only when edges.length <= 12; h8/E12 exposes disconnected-component rank mismatch, h12/E18 skips that observer',
    repaired_lemma:'Terminal-cone pruning is admissible for a full-checker abstraction only after every global source observer is included in the concrete state and preservation relation. Proof-DAG non-ancestry alone is insufficient.',
    scope:'Archived /386 SOURCE/RES/AND2 sibling only; not authenticated full historical R_mix341; padded easy family; no proof-cost or SAT-time lower bound.',
    statuses:{P2_D1:'OPEN',P2_C3:'OPEN (unsafe source-pruning quotient falsified)',P2_B1:'OPEN',P2_B2_B3:'SEPARATE OPEN',P_vs_NP:'OPEN'}};
  fs.mkdirSync(path.dirname(outFile),{recursive:true});fs.writeFileSync(outFile,JSON.stringify(result,null,2)+'\n');
  fs.writeFileSync(witnessFile,JSON.stringify(p1)+'\n');fs.writeFileSync(acceptedFile,JSON.stringify(p2)+'\n');
  console.log(JSON.stringify({status:'PASS',full:full.map(x=>({label:x.label,accepted:x.accepted,sha256:x.sha256,dead:x.dead_records})),
    projections:projected.map(x=>x.sha256),hostiles:hostiles.length,outFile,witnessFile,acceptedFile},null,2));
} finally {fs.rmSync(tmp,{recursive:true,force:true});}


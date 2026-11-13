#!/usr/bin/env node
'use strict';
/* LSPV-2/595 independent reference provenance builder for original /386.
 * This is NOT an authoritative parser for historical R_mix341. */
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const os=require('node:os'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const key=x=>JSON.stringify(x), norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const root=path.resolve(__dirname,'../..'),clone=x=>JSON.parse(JSON.stringify(x));
const original=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const inputs=[0,1,2].map(i=>path.join(root,'results/raw/arc/589_k3_component'+i+'_complete_cli.json'));
const output=path.join(root,'results/raw/arc/2026-11-13_0212_LSPV2_595_TRIPLEX_W85_ACCEPTED.json');
const lanes=inputs.map(p=>JSON.parse(fs.readFileSync(p,'utf8')));
function assemble(){
 const a=lanes[0],N=a.summary.source,R=a.summary.resolution;
 for(const b of lanes){assert.deepEqual(b.spec,a.spec);assert.deepEqual(b.gate_defs,a.gate_defs);assert.deepEqual(b.records.slice(0,N),a.records.slice(0,N));}
 const rows=clone(a.records.slice(0,N));
 lanes.forEach((p,j)=>p.records.slice(N).forEach(r=>{
  const x=clone(r);x.parents=x.parents.map(k=>k<N?k:k+j*R);rows.push(x);
 }));
 return {spec:a.spec,gate_defs:a.gate_defs,records:rows,summary:{source:N,def_views:0,resolution:3*R,paid_gates:a.gate_defs.length,paid_total:3*R+a.gate_defs.length,live_records:rows.length}};
}
function sourceRows(d){
 const {h,edges,charge,guard}=d.spec,out=[];
 for(let v=0;v<h;v++){const incident=[];edges.forEach(([a,b],j)=>{if(a===v||b===v)incident.push(j+1)});
  assert.equal(incident.length,3);
  for(let m=0;m<8;m++){let bits=[m&1,m>>1&1,m>>2&1];
   if((bits[0]^bits[1]^bits[2])!==charge[v])out.push(norm(incident.map((e,j)=>bits[j]?-e:e).concat([-guard])));
  }
 }
 out.push([guard]);return out;
}
function provenance(d){
 const expected=sourceRows(d);
 assert.deepEqual(d.records.filter(r=>r.kind==='SOURCE').map(r=>key(r.c)).sort(),expected.map(key).sort());
 const records=[],prov=[],supports=[],heads=new Map(),vertices=[],paid=new Set();
 const add=(op,args)=>{const i=vertices.length;vertices.push({op,args});return i;};
 const own=new Map();
 for(const [id,z,a,b] of d.gate_defs){assert(!paid.has(id));paid.add(id);own.set(id,add('OWNER',[id,z,a,b]));}
 let firstRes=0,res=0,facet=0,spanMax=0;
 for(let i=0;i<d.records.length;i++){
  const r=d.records[i],s=key(r.c);let p,anc=new Set(),span=0;
  assert.deepEqual(r.c,norm(r.c),'noncanonical clause');
  if(r.kind==='SOURCE'){assert.equal(r.parents.length,0);p=add('SOURCE',[i,r.source,s]);anc.add(i);}
  else if(r.kind==='DEF'){assert.equal(r.parents.length,0);assert(own.has(r.gate));p=add('DEF',[own.get(r.gate)]);facet++;}
  else if(r.kind==='RES'){
   const [a,b]=r.parents;assert.equal(r.parents.length,2);assert(a<i&&b<i&&a>=0&&b>=0);
   const A=records[a].clause,B=records[b].clause;assert(A.includes(r.pivot)&&B.includes(-r.pivot));
   const C=norm([...A.filter(x=>x!==r.pivot),...B.filter(x=>x!==-r.pivot)]);
   assert(!C.some(x=>C.includes(-x)));assert.deepEqual(C,r.c);
   p=add('AND',[prov[a],prov[b]]);
   anc=new Set([...supports[a],...supports[b]]);
   span=Math.max(records[a].span,records[b].span)+1;spanMax=Math.max(spanMax,span);
   if(!heads.has(s))firstRes++;res++;
  } else throw Error('unknown /386 native record '+r.kind);
  records.push({clause:r.c,span});prov.push(p);supports.push(anc);
  heads.set(s,heads.has(s)?add('OR',[heads.get(s),p]):p);
 }
 assert.equal(res,d.summary.resolution);assert.equal(facet,d.summary.def_views);
 assert.equal(d.summary.paid_gates,paid.size);assert.equal(d.summary.paid_total,res+paid.size);
 assert.equal(records.at(-1).clause.length,0);
 const ends=records.flatMap((r,i)=>r.clause.length===0&&d.records[i].kind==='RES'?[i]:[]);
 const ss=ends.map(i=>[...supports[i]].sort((x,y)=>x-y));
 assert.deepEqual(ends,[76,104,132]);assert(ss.every(x=>x.length===17));
 const common=ss[0].filter(x=>ss.every(a=>a.includes(x)));assert.deepEqual(common,[48]);
 return {original_paid:res+paid.size,abstract_paid:firstRes+paid.size,first_value_RES:firstRes,RES:res,provenance_nodes:vertices.length,provenance_edges:vertices.reduce((t,n)=>t+(n.op==='AND'||n.op==='OR'?2:n.op==='DEF'?1:0),0),span:spanMax,terminal_indices:ends,terminal_supports:ss,common_source:common};
}
function osCheck(data,name,accept){
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv595-')),p=path.join(temp,'proof.json');
 const b=Buffer.from(JSON.stringify(data)+'\n');fs.writeFileSync(p,b);
 const ret=cp.spawnSync(process.execPath,[original,p],{encoding:'utf8',maxBuffer:4e6});
 fs.rmSync(temp,{recursive:true,force:true});
 assert.equal(ret.status===0,accept,name+': '+String(ret.stderr).slice(0,250));
 const check=ret.status===0?JSON.parse(ret.stdout.trim()):null;
 return {name,verdict:accept?'ACCEPT':'REJECT',sha256:hash(b),bytes:b.length,assertions:check?.assertions??null};
}
assert.equal(hash(fs.readFileSync(original)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
const packet=assemble(),bytes=JSON.stringify(packet)+'\n';
assert.equal(bytes.length,8597);assert.equal(hash(Buffer.from(bytes)),'4bd50ef54044187a5b9811d87b19c640e55bd4f70d024d057ff5fb57226e5d46');
const stored=fs.readFileSync(output,'utf8');assert.equal(stored,bytes,'published corpus differs');
const cases=lanes.map((d,i)=>osCheck(d,'original_lane_'+i,true));
cases.push(osCheck(packet,'merged_triplex',true));
for(const [name,f] of [
 ['bad_pivot',x=>x.records.at(-1).pivot=12345],
 ['forged_source',x=>x.records[0].c=[-x.spec.guard]],
 ['underpay',x=>x.summary.paid_total--],
 ['future_parent',x=>x.records.at(-1).parents[0]=x.records.length+1],
 ['unsupported_AND3',x=>x.records.at(-1).kind='AND3'],
 ['wrong_source_owner',x=>x.records[0].source=98765]
]){let x=clone(packet);f(x);cases.push(osCheck(x,name,false));}
const p=provenance(packet),result={status:'PASS',scope:'original /386 restricted SOURCE/DEF/RES checker only',proof:p,cases};
assert.equal(p.original_paid,85);assert.equal(p.abstract_paid,81);assert.equal(p.provenance_nodes,138);
console.log(JSON.stringify(result,null,2));

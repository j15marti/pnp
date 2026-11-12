#!/usr/bin/env node
'use strict';
// LSPV-2/582; REFERENCE abstraction, not authoritative R_mix341 or /386 checker.
// node experiments/arc/lspv2_582_native386_costsound_compact.cjs [repoRoot] [output.json]
const fs=require('fs'),path=require('path'),cp=require('child_process'),os=require('os'),cr=require('crypto'),assert=require('assert/strict');
const root=path.resolve(process.argv[2]||'.'),base='results/raw/arc/';
const names={seed:base+'2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',structural:base+'2026-11-12_1212_LSPV2_581_ACCEPTED_K16_SYNTACTIC_W61.json',expanded:base+'2026-11-12_1212_LSPV2_581_ACCEPTED_K16_LIVE_W93.json'};
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js'),src=fs.readFileSync(path.join(root,base+'574_k01_SIGNED_SOURCE.cnf'));
const sha=b=>cr.createHash('sha256').update(b).digest('hex');
assert.equal(sha(fs.readFileSync(checker)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(sha(src),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
function native(obj){const f=path.join(os.tmpdir(),'pnp582_'+process.pid+'_'+(++native.i)+'.json');fs.writeFileSync(f,typeof obj==='string'?obj:JSON.stringify(obj));const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:25000});fs.unlinkSync(f);return {accept:r.status===0,exit:r.status,assertions:r.status===0?JSON.parse(r.stdout).assertions:null,error:r.status===0?null:r.stderr.slice(0,160)};}native.i=0;
function norm(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function alpha(data){let seen=new Set(),paid=0,paidFirst=0,duplicate=0,views=0,sources=0,depth=[];const trace=[];
 for(let i=0;i<data.records.length;i++){const r=data.records[i],k=JSON.stringify(r.c);assert(r.parents.every(p=>p<i&&p>=0));if(r.kind==='RES'){
 assert.equal(r.parents.length,2);const [A,B]=r.parents.map(p=>data.records[p].c);assert(A.includes(r.pivot)&&B.includes(-r.pivot));assert.deepEqual(norm([...A.filter(x=>x!==r.pivot),...B.filter(x=>x!==-r.pivot)]),r.c);}
 const newClause=!seen.has(k);seen.add(k);if(r.kind==='RES'){paid++;paidFirst+=Number(newClause);duplicate+=Number(!newClause);}else if(r.kind==='DEF')views++;else if(r.kind==='SOURCE')sources++;else throw Error('unrecognised opcode');
 depth[i]=r.kind==='RES'?1+Math.max(...r.parents.map(p=>depth[p])):0;trace.push({i,rule:r.kind,ports:r.parents,clause:r.c,scope:'ROOT',paidDelta:r.kind==='RES'?1:0,abstractDelta:r.kind==='RES'&&newClause?1:0});}
 assert.deepEqual(data.records.at(-1).c,[]);assert.equal(data.summary.paid_total,paid+data.gate_defs.length);assert(trace.every(x=>x.abstractDelta<=x.paidDelta));return {sourceSHA256:sha(src),sourceOccurrences:sources,paidOwners:data.gate_defs.length,freeFacets:views,RES:paid,duplicateRES:duplicate,concreteWork:paid+data.gate_defs.length,abstractWork:paidFirst+data.gate_defs.length,span:Math.max(...depth),terminal:true,scope:'ROOT',traceSHA256:sha(JSON.stringify(trace))};}
const cases=[];for(const [name,p] of Object.entries(names)){const raw=fs.readFileSync(path.join(root,p));const v=native(raw.toString());assert(v.accept,name+' rejected '+v.error);cases.push({name,sha256:sha(raw),bytes:raw.length,native:v,...alpha(JSON.parse(raw))});}
const seed=JSON.parse(fs.readFileSync(path.join(root,names.seed))),expanded=JSON.parse(fs.readFileSync(path.join(root,names.expanded)));
const copy=x=>JSON.parse(JSON.stringify(x));let a=copy(seed);a.gate_defs=[];a.summary.paid_gates=0;a.summary.paid_total=a.summary.resolution;const bad=[['ownerless_cli',a]];
a=copy(seed);a.summary.paid_total--;bad.push(['underpaid',a]);a=copy(seed);a.records.at(-1).pivot=1000003;bad.push(['signed_pivot',a]);a=copy(seed);a.records[0].c=[-1,2,3,-7];bad.push(['forged_source',a]);a=copy(seed);a.records.find(r=>r.kind==='RES').kind='LOCAL-CONVERT';bad.push(['unknown_opcode',a]);a=copy(expanded);a.records.find(r=>r.kind==='DEF').c=[123456];bad.push(['false_facet',a]);
for(const [name,b] of bad){const n=native(b);assert(!n.accept,name+' unexpectedly accepted');cases.push({name,native:n});}
const result={id:'LSPV-2/582',checker:'original unchanged /386 CLI, NOT full R_mix341',status:'restricted proved forward cost simulation; computational original-OS replays',cases,accepted:3,rejected:6,tracker:'TRACKERS REVIEWED; NO MATERIAL CHANGE',open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3','P versus NP']};if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({accepted:result.accepted,rejected:result.rejected,costs:cases.slice(0,3).map(x=>[x.name,x.concreteWork,x.abstractWork,x.duplicateRES])}));

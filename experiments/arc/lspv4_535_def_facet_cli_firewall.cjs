#!/usr/bin/env node
'use strict';
// LSPV-4/535. Run: node experiments/arc/lspv4_535_def_facet_cli_firewall.cjs
// Original checker files are used unmodified. No npm dependencies.
const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const aFile=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const bFile=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const polyFile=path.join(root,'results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json');
const compactFile=path.join(root,'results/raw/arc/2026-11-10_2200_LSPV1_564_GATE_BRIDGE_ELIMINATED_PACKET.json');
function gitsha(s){const b=Buffer.from(s);return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
function pinned(p,sha){const s=fs.readFileSync(p,'utf8');assert.equal(gitsha(s),sha,'blob drift: '+p);return s}
pinned(aFile,'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
const B=pinned(bFile,'338305c0ce101704205e57543756b8127074a986');
const base=JSON.parse(pinned(polyFile,'b9c1d306c300a3f1917ee01ecab16358ac77d4de'));
const compact=JSON.parse(pinned(compactFile,'f1f43709b49e3c9bf459db362718307a15880a98'));
const copy=x=>structuredClone(x),d=n=>String(n).length;
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-535-'));
function cli(f,obj){const p=path.join(temp,'proof.json');fs.writeFileSync(p,JSON.stringify(obj));
const x=cp.spawnSync(process.execPath,[f,p],{encoding:'utf8',timeout:25000,maxBuffer:8e6});
let parsed={};try{parsed=JSON.parse(x.stdout)}catch{}
return {ok:x.status===0,exit:x.status,paid:parsed.paid??null,checks:parsed.assertions??parsed.checks??null,error:(x.stderr||'').trim().split('\n').at(-1)||null}}
function core(obj){const sandbox={require,process:{argv:['node',bFile]},console:{log:()=>{}},structuredClone,packet:copy(obj)};
try{vm.runInNewContext(B+'\n;globalThis.probe=checkProof(packet,{control:true});',sandbox,{timeout:25000});return{ok:true,paid:sandbox.probe.paid}}
catch(e){return{ok:false,error:String(e)}}}
function padded(free,owners){let q=copy(base),last=q.records.pop(),facet=q.records.find(r=>r.kind==='DEF');
for(let i=0;i<free;i++)q.records.push(copy(facet));q.records.push(last);
for(let i=0;i<owners;i++)q.gate_defs.push([i+1,i+9,1,2]);
q.summary.def_views+=free;q.summary.live_records+=free;q.summary.paid_gates+=owners;q.summary.paid_total+=owners;return q}
function prune(q){
const rec=q.records,seen=new Set(),stack=[rec.length-1];
for(let i=0;i<rec.length;i++)if(rec[i].kind==='SOURCE')seen.add(i);
while(stack.length){const i=stack.pop();if(seen.has(i))continue;seen.add(i);stack.push(...rec[i].parents)}
const keys=[...seen].sort((a,b)=>a-b),ids=new Map(keys.map((x,i)=>[x,i]));
const byZ=new Map(q.gate_defs.map(g=>[g[1],g])),byId=new Map(q.gate_defs.map(g=>[g[0],g])),need=new Set();
for(const i of keys){const r=rec[i];if(r.kind==='DEF'){const g=byId.get(r.gate);if(g)need.add(g[1])}
for(const lit of r.c)if(byZ.has(Math.abs(lit)))need.add(Math.abs(lit))}
const todo=[...need];while(todo.length){const g=byZ.get(todo.pop());if(!g)continue;
for(const lit of [g[2],g[3]])if(byZ.has(Math.abs(lit))&&!need.has(Math.abs(lit))){need.add(Math.abs(lit));todo.push(Math.abs(lit))}}
const out=copy(q);out.records=keys.map(i=>({...rec[i],parents:rec[i].parents.map(j=>ids.get(j))}));
out.gate_defs=q.gate_defs.filter(g=>need.has(g[1]));
const count=s=>out.records.filter(r=>r.kind===s).length;
Object.assign(out.summary,{source:count('SOURCE'),def_views:count('DEF'),resolution:count('RES'),paid_gates:out.gate_defs.length,paid_total:count('RES')+out.gate_defs.length,live_records:out.records.length});
return out}
const results={schema:'LSPV4-535/v1',mode:'real OS Node original-source subprocess (when executed in clone)',positive:[],negative:[]};
try{
const b47=cli(bFile,compact),core47=core(compact);assert(core47.ok&&core47.paid===47&&!b47.ok);
const rescued=copy(compact);rescued.gate_defs.push([0,8,1,2]);rescued.summary.paid_gates++;rescued.summary.paid_total++;
const b48=cli(bFile,rescued);assert(b48.ok&&b48.paid===48);
results.core_vs_cli={core47,cli47:b47,cli48:b48,bytes47:JSON.stringify(compact).length,bytes48:JSON.stringify(rescued).length};
for(const [f,g] of [[0,0],[1,0],[2,0],[8,0],[64,0],[256,0],[0,1],[0,2],[0,8],[0,64],[8,8],[64,64]]){
const q=padded(f,g),r=prune(q),left=cli(bFile,q),right=cli(aFile,q),normalized=cli(bFile,r);
assert(left.ok&&left.paid===50+g&&right.ok&&normalized.ok&&normalized.paid===50);
if(g===0)assert.equal(JSON.stringify(q).length,7532+48*f+d(3+f)-d(3)+d(69+f)-d(69));
results.positive.push({free:f,owners:g,bytes:JSON.stringify(q).length,paid:q.summary.paid_total,records:q.records.length,core_pruned_bytes:JSON.stringify(r).length,core_pruned_paid:r.summary.paid_total,A:right,B:left,pruned:normalized})}
const bad=padded(8,8);
const mutations=[['wrong_def_kind',x=>x.records.at(-2).kind='XEF'],['bad_facet_owner',x=>x.records.at(-2).gate=9999],['duplicate_gate_id',x=>x.gate_defs.at(-1)[0]=0],['duplicate_gate_z',x=>x.gate_defs.at(-1)[1]=8],['illegal_guard_operand',x=>x.gate_defs.at(-1)[2]=7],['wrong_paid_total',x=>x.summary.paid_total--],['wrong_free_view_count',x=>x.summary.def_views--],['missing_sink',x=>{x.records.pop();x.summary.live_records--}]];
for(const [name,mutate] of mutations){const x=copy(bad);mutate(x);const B=cli(bFile,x),A=cli(aFile,x);assert(!B.ok&&A.ok,name);results.negative.push({name,A,B})}
for(const k of [1,8,64]){const x=padded(k,0),y=copy(x);y.records.at(-2).kind='XEF';assert.equal(JSON.stringify(x).length,JSON.stringify(y).length);assert(!cli(bFile,y).ok);results.negative.push({name:'same_length_DEF_byte',k,accepted_bytes:JSON.stringify(x).length,mutated_bytes:JSON.stringify(y).length,rejected:true})}
results.status='PASS';console.log(JSON.stringify(results,null,2));
}finally{fs.rmSync(temp,{recursive:true,force:true})}

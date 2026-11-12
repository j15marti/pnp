'use strict';
// LSPV-3/581: reproduce an archived /386 disconnected-source acceptance cliff.
// Requires the untouched j15marti/pnp checkout and Node.js.
// All checker verdicts below come from independent OS processes running the archived checker.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerRel='experiments/arc/lspv2_386_independent_verify.js';
const seedRel='results/raw/arc/2026-11-11_0724_LSPV3_571_FIXED_SOURCE_K4_TRANSPOSITION_PACKET.json';
const acceptedRel='results/raw/arc/2026-11-11_1724_LSPV3_581_K4_DISJOINT_K33_NATIVE386_ACCEPTED.json';
const rejectedRel='results/raw/arc/2026-11-11_1724_LSPV3_581_K4_DISJOINT_K4_NATIVE386_CLI_REJECTED.json';
const pins={
 [checkerRel]:'338305c0ce101704205e57543756b8127074a986',
 [seedRel]:'fdefefdfa531b292e87db231074750fc783db4e6'
};
function gitBlob(s){const b=Buffer.isBuffer(s)?s:Buffer.from(s);
 return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');}
for(const [f,sha] of Object.entries(pins))assert.equal(gitBlob(fs.readFileSync(path.join(root,f))),sha,'pin '+f);
const seed=JSON.parse(fs.readFileSync(path.join(root,seedRel),'utf8'));
function extend(extraV, extraEdges) {
 const d=structuredClone(seed),g=7+extraEdges.length;
 const rename=lit=>{
   const sign=Math.sign(lit),v=Math.abs(lit);
   return sign*(v===7?g:v===8?g+1:v===9?g+2:v);
 };
 d.spec.h+=extraV;d.spec.edges.push(...extraEdges);
 d.spec.charge.push(...Array(extraV).fill(0));d.spec.guard=g;
 d.gate_defs=d.gate_defs.map(([id,z,a,b])=>[id,rename(z),rename(a),rename(b)]);
 for(const r of d.records){
   r.c=r.c.map(rename).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
   if(r.pivot!==undefined)r.pivot=rename(r.pivot);
 }
 const extra=[];
 for(let v=4;v<4+extraV;v++){
   const es=[];
   d.spec.edges.forEach(([u,w],i)=>{if(u===v||w===v)es.push(i+1)});
   assert.equal(es.length,3);
   for(let mask=0;mask<8;mask++){
     const b=[mask&1,(mask>>1)&1,(mask>>2)&1];
     if((b[0]^b[1]^b[2])===0)continue;
     extra.push({kind:'SOURCE',
       c:[...es.map((e,i)=>b[i]?-e:e),-g].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),
       parents:[],source:v});
   }
 }
 assert.equal(extra.length,4*extraV);
 d.records.splice(17,0,...extra);
 for(let i=17+extra.length;i<d.records.length;i++)
   d.records[i].parents=d.records[i].parents.map(j=>j>=17?j+extra.length:j);
 d.summary.source+=extra.length;d.summary.live_records+=extra.length;
 return d;
}
function modelStats(d){
 const {h,edges,charge}=d.spec;let odd=0,even=0;
 assert.ok(edges.length<=15,'fixed bounded exhaustive control');
 for(let m=0;m<2**edges.length;m++){
   const par=Array(h).fill(0);
   edges.forEach(([u,v],j)=>{const x=(m>>j)&1;par[u]^=x;par[v]^=x});
   odd+=Number(par.every((x,j)=>x===charge[j]));
   even+=Number(par.every((x,j)=>x===(j===0?0:charge[j])));
 }
 return {oddModels:odd,evenModels:even,
   originalCheckerEvenExpectation:2**(edges.length-h+1)};
}
function ancestry(d){
 const seen=new Set(),todo=[d.records.length-1];
 while(todo.length){const i=todo.pop();if(seen.has(i))continue;
  seen.add(i);todo.push(...d.records[i].parents);}
 return {terminalRecords:seen.size,
  terminalOriginalSources:[...seen].filter(j=>d.records[j].kind==='SOURCE').length,
  terminalAddedComponentSources:[...seen].filter(j=>d.records[j].kind==='SOURCE'&&d.records[j].source>=4).length};
}
const extraK4=[[4,5],[4,6],[4,7],[5,6],[5,7],[6,7]];
const extraK33=[];for(let u=4;u<7;u++)for(let v=7;v<10;v++)extraK33.push([u,v]);
const d8=extend(4,extraK4),d10=extend(6,extraK33);
assert.equal(JSON.stringify(d8),fs.readFileSync(path.join(root,rejectedRel),'utf8'));
assert.equal(JSON.stringify(d10),fs.readFileSync(path.join(root,acceptedRel),'utf8'));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-581-'));
function runOS(dat){
 const f=path.join(tmp,'packet.json');fs.writeFileSync(f,JSON.stringify(dat));
 const r=cp.spawnSync(process.execPath,[path.join(root,checkerRel),f],
     {encoding:'utf8',timeout:30000,maxBuffer:10000000});
 if(r.error)throw r.error;
 const out={accepted:r.status===0,exitCode:r.status,
   stderr:r.stderr.trim().slice(0,300)};
 if(out.accepted){
   const j=JSON.parse(r.stdout.trim());out.paid=j.paid;out.sources=j.sources;
   out.records=j.records;out.negativeTests=j.negativeTests;
   out.assertions=j.assertions;assert.equal(j.negativeTests,11);
 }
 return out;
}
const base=runOS(seed),small=runOS(d8),large=runOS(d10);
assert.equal(base.accepted,true);
assert.equal(small.accepted,false);
assert.match(small.stderr,/even mismatch/);
assert.equal(large.accepted,true);
assert.equal(large.paid,53);assert.equal(large.sources,41);assert.equal(large.records,98);
assert.equal(large.negativeTests,11);
const negatives=[
 ['forged_SOURCE',p=>p.records[17].c[0]*=-1],
 ['colliding_owner',p=>p.gate_defs[1][1]=p.gate_defs[0][1]],
 ['underpaid',p=>p.summary.paid_total--],
 ['false_sink',p=>p.records.at(-1).c=[1]],
 ['forward_parent',p=>p.records.at(-1).parents[0]=p.records.length],
 ['even_charge',p=>p.spec.charge[0]^=1]
];
const hostile=[];
for(const [label,change] of negatives){
 const d=structuredClone(d10);change(d);const r=runOS(d);
 assert.equal(r.accepted,false,'hostile accepted: '+label);
 hostile.push({label,...r});
}
const out={id:'LSPV3-581',status:'COMPUTATIONAL: unchanged original /386 OS checker',
 pins,models:{K4:modelStats(seed),K4_K4:modelStats(d8),K4_K33:modelStats(d10)},
 ancestry:{K4:ancestry(seed),K4_K4:ancestry(d8),K4_K33:ancestry(d10)},
 originalOS:{base,small,large},hostile,
 bytes:{rejected:Buffer.byteLength(JSON.stringify(d8)),accepted:Buffer.byteLength(JSON.stringify(d10))},
 exactPaidLogicalWork:53,notes:[
 'Full historical R_mix341 is not authenticated.',
 'Free mandatory SOURCEs from the even disjoint component are not terminal ancestors.',
 'Evidence bits, CLI running time, span, and actual peak space are separate from paid work.',
 'Original checker skips model-count self-test above 12 original edge variables.'
 ]};
fs.rmSync(tmp,{recursive:true,force:true});
console.log(JSON.stringify(out,null,2));

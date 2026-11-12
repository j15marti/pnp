#!/usr/bin/env node
'use strict';
/* LSPV-2/569 exact original-OS differential. REFERENCE PATCH IS NOT HISTORICAL.
 * Run at repository root: node experiments/arc/lspv2_569_published_replay.cjs [raw-out.json]
 * Requires Node >=18, no packages. Authenticated scope: archived /386 only. */
const fs=require('node:fs'),cp=require('node:child_process'),crypto=require('node:crypto'),vm=require('node:vm'),os=require('node:os'),path=require('node:path'),assert=require('node:assert/strict');
const R=process.cwd(), rel='results/raw/arc/', checker=R+'/experiments/arc/lspv2_386_independent_verify.js';
const files=['2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json','2026-11-11_1812_LSPV2_569_DISCONNECTED_K4K4.json','2026-11-11_1812_LSPV2_569_DISCONNECTED_K4_K33.json'];
function sh(b){return crypto.createHash('sha256').update(b).digest('hex')}
function blob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
const b=fs.readFileSync(checker),source=b.toString();assert.equal(blob(b),'338305c0ce101704205e57543756b8127074a986');
const paths=files.map(f=>R+'/'+rel+f),d=paths.map(p=>JSON.parse(fs.readFileSync(p)));
const originalExpected=[0,1,0],evenModels=[8,64,128],oldExpected=[8,32,64],cost=[29,29,29];
const oldE='let evenCharge=[0,...charge.slice(1)];',oldCount="check(even===2**(edges.length-h+1),'even mismatch');";
assert.ok(source.includes(oldE)&&source.includes(oldCount));
// TWO patched self-test expressions only. The original inference checker stays verbatim.
const ref=source.replace(oldE,'let evenCharge=[charge[0]^1,...charge.slice(1)];').replace(oldCount,`{
 const uf=Array.from({length:h},(_,i)=>i);
 function root(i){while(uf[i]!==i)i=uf[i]=uf[uf[i]];return i}
 for(const [u,v] of edges){const a=root(u),b=root(v);if(a!==b)uf[a]=b}
 const cs=new Map();for(let v=0;v<h;v++){const z=root(v);if(!cs.has(z))cs.set(z,[]);cs.get(z).push(v)}
 const rhs=[charge[0]^1,...charge.slice(1)];
 const feasible=[...cs.values()].every(vs=>vs.reduce((t,v)=>t^rhs[v],0)===0);
 const expected=feasible?2**(edges.length-h+cs.size):0;
 check(even===expected,'even mismatch');
}`);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp569-'));const reference=path.join(tmp,'NONAUTH_REFERENCE.js');fs.writeFileSync(reference,ref);
function cmd(script,p){const a=cp.spawnSync(process.execPath,[script,p],{encoding:'utf8',timeout:15000});return {exit:a.status,success:a.status===0,stdout:(a.stdout||'').trim(),error:(a.stderr||'').match(/Error: ([^\n]+)/)?.[1]||null}}
function count(G,rhs){let count=0;for(let x=0;x<2**G.edges.length;x++){let acc=Array(G.h).fill(0);G.edges.forEach(([a,b],i)=>{const bit=(x>>i)&1;acc[a]^=bit;acc[b]^=bit});if(acc.every((v,i)=>v===rhs[i]))count++}return count}
const mathSource=source.slice(0,source.indexOf('for(const f of process.argv.slice(2))'));
assert.ok(mathSource.length>5000);let results=[];
for(let i=0;i<3;i++){let q=d[i],p=paths[i],orig=cmd(checker,p),fixed=cmd(reference,p);assert.equal(q.summary.paid_total,cost[i]);
 const ctx={require,console,process:{argv:[]},structuredClone,Buffer};vm.createContext(ctx);
 const math=vm.runInContext(mathSource+'\ncheckProof('+JSON.stringify(q)+',{control:false})',ctx,{timeout:15000});assert.equal(math.paid,cost[i]);
 const odd=count(q.spec,q.spec.charge),even=count(q.spec,[0,...q.spec.charge.slice(1)]);
 assert.equal(odd,0);assert.equal(even,evenModels[i]);assert.equal(orig.success,originalExpected[i]===0);assert.equal(fixed.success,true);
 if(i===1)assert.equal(orig.error,'even mismatch');
 results.push({case:files[i],bytes:fs.statSync(p).size,sha256:sh(fs.readFileSync(p)),vertices:q.spec.h,edges:q.spec.edges.length,source:q.summary.source,records:q.summary.live_records,paid:math.paid,oddModels:odd,originalEvenCount:even,originalExpected:oldExpected[i],original:orig,reference:fixed});
}
let negatives=[];let base=d[1];let mutants={forged_SOURCE:x=>{x.records[0].c=[1,2,3,13]},wrong_port:x=>{x.records.at(-1).pivot=-13},underpayment:x=>{x.summary.paid_total--},wrong_charge:x=>{x.spec.charge[4]=1}};
for(const [name,edit] of Object.entries(mutants)){const x=JSON.parse(JSON.stringify(base));edit(x);const p=tmp+'/'+name+'.json';fs.writeFileSync(p,JSON.stringify(x));const a=cmd(reference,p);assert.equal(a.success,false);negatives.push({name,reference:a})}
const raw={run:'LSPV-2/569',status:'PROVED/RESTRICTED plus COMPUTATIONAL',original_checker_git_blob:blob(b),reference_sha256:sh(Buffer.from(ref)),scope:'original /386 SOURCE/DEF/RES only; reference self-test is nonauthoritative',cases:results,negative_controls:negatives,notes:'Peer LSPV-3/581 and LSPV-1/585 previously established the disconnected incidence-rank theorem in hosted V8; this run adds W29 original OS reproduction and two-patch reference regression.'};
const out=process.argv[2]||R+'/'+rel+'2026-11-11_1812_LSPV2_569_PUBLISHED_OS_REPLAY_RAW.json';fs.writeFileSync(out,JSON.stringify(raw,null,2)+'\n');fs.rmSync(tmp,{recursive:true,force:true});console.log(JSON.stringify({output:out,cases:results.map(x=>({edges:x.edges,paid:x.paid,original:x.original.success,reference:x.reference.success})),negatives:negatives.length},null,2));

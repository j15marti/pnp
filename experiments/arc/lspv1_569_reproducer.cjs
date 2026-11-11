'use strict';
// Usage: node lspv1_569_reproducer.cjs original_386_checker.js LSPV1_568_CLI29.json output_dir
// No external dependencies. Preserves original verifier function text and runs its CLI in OS Node.
const fs=require('fs'),path=require('path'),vm=require('vm'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert');
const [checker,seedFile,outdir]=process.argv.slice(2);
if(!checker||!seedFile||!outdir)throw Error('Need checker, seed, output dir');fs.mkdirSync(outdir,{recursive:true});
const hash=b=>crypto.createHash('sha1').update('blob '+b.length+String.fromCharCode(0)).update(b).digest('hex');
const native=fs.readFileSync(checker),original=fs.readFileSync(seedFile);
assert.equal(hash(native),'338305c0ce101704205e57543756b8127074a986');
assert.equal(hash(original),'e3eb2a46857776089ab83f4ad50159ef622d2869');
const text=native.toString('utf8');const context={require,process,Buffer,console,structuredClone};
vm.runInNewContext(text.slice(0,text.indexOf('for(const f of process.argv.slice(2)){'))+'\nglobalThis.checkOriginal=checkProof;',context);
const core=context.checkOriginal, seed=JSON.parse(original);const clone=structuredClone;
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function decorate(p){const q=clone(p);q.gate_defs=[[900,135,1,4],[901,136,135,-2]];
 const d=[];for(let k=0;k<5;k++){d.push({kind:'DEF',gate:900,c:canon([1,-135]),parents:[]},{kind:'DEF',gate:901,c:canon([135,-136]),parents:[]});}
 q.records=[...d,...q.records.map(r=>({...r,parents:r.parents.map(j=>j+d.length)}))];
 q.summary={...q.summary,def_views:10,paid_gates:2,paid_total:30,live_records:q.records.length};return q;}
function normalize(p){const e=p.spec.edges.length,guard=p.spec.guard;let next=e+1;const wires=new Map(),ids=new Map();
 p.gate_defs.forEach(([id,z],i)=>{while(next===guard)next++;ids.set(id,i);wires.set(z,next++);});
 const lit=x=>Math.sign(x)*(wires.get(Math.abs(x))??Math.abs(x));
 const gate_defs=p.gate_defs.map(([id,z,a,b])=>[ids.get(id),wires.get(z),lit(a),lit(b)]);
 const ordered=[...p.records.map((r,i)=>({r,i})).filter(x=>x.r.kind==='SOURCE'),...p.records.map((r,i)=>({r,i})).filter(x=>x.r.kind==='DEF'),...p.records.map((r,i)=>({r,i})).filter(x=>x.r.kind==='RES')];
 const records=[],index=new Map(),facets=new Map();for(const {r,i} of ordered){const c=canon(r.c.map(lit));
  if(r.kind==='DEF'){let gate=ids.get(r.gate),k=JSON.stringify([gate,c]);if(facets.has(k)){index.set(i,facets.get(k));continue;}
   facets.set(k,records.length);index.set(i,records.length);records.push({...r,c,gate,parents:[]});}
  else if(r.kind==='SOURCE'){index.set(i,records.length);records.push({...r,c,parents:[]});}
  else{let parents=r.parents.map(j=>{assert(index.has(j));return index.get(j)});index.set(i,records.length);records.push({...r,c,parents,pivot:lit(r.pivot)});}
 }
 const nsrc=records.filter(r=>r.kind==='SOURCE').length,ndef=records.filter(r=>r.kind==='DEF').length,nres=records.filter(r=>r.kind==='RES').length;
 return {...p,gate_defs,records,summary:{source:nsrc,def_views:ndef,resolution:nres,paid_gates:gate_defs.length,paid_total:nres+gate_defs.length,live_records:records.length}};}
const cases=[['core28',({...seed,gate_defs:[],summary:{...seed.summary,paid_gates:0,paid_total:28}}),false],['cli29',seed,true]];
const raw=decorate(seed),norm=normalize(raw);
assert.deepEqual(normalize(norm),norm);assert(norm.records.length<=4*norm.spec.h+1+4*norm.summary.paid_total);
cases.push(['raw10',raw,true],['normal2',norm,true]);
const results=[];for(const [name,p,shouldAccept] of cases){const coreResult=core(p,{control:true});const file=path.join(outdir,name+'.json');const bytes=Buffer.from(JSON.stringify(p,null,2)+'\n');fs.writeFileSync(file,bytes);
 const run=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:15000});let accepted=run.status===0;assert.equal(accepted,shouldAccept);
 results.push({name,blob:hash(bytes),sha256:crypto.createHash('sha256').update(bytes).digest('hex'),bytes:bytes.length,paid:coreResult.paid,def:coreResult.def,res:coreResult.res,records:coreResult.records,CLI:accepted,assertions:accepted?JSON.parse(run.stdout).assertions:null});}
for(const [name,mutate] of [['bad_source',p=>p.records.find(r=>r.kind==='SOURCE').c=[1,2,3,-4,-7]],['bad_parent',p=>p.records.at(-1).parents[0]=9999],['bad_tariff',p=>p.summary.paid_total--],['bad_owner',p=>p.gate_defs[1][2]=777777]]){const q=clone(norm);mutate(q);let rejected=false;try{core(q)}catch(e){rejected=true;}assert(rejected);const file=path.join(outdir,name+'.json');fs.writeFileSync(file,JSON.stringify(q,null,2)+'\n');const os=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:15000});assert.notEqual(os.status,0);results.push({name,coreRejected:true,CLI:false});}
const report={result:'PASS',node:process.version,checker_git_blob:hash(native),seed_git_blob:hash(original),tests:results,scope:'Archived /386 only, not complete historical R_mix341'};
fs.writeFileSync(path.join(outdir,'raw_results.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({result:'PASS',positive:results.filter(z=>z.CLI).length,negative:results.filter(z=>z.CLI===false).length,normalized_paid:norm.summary.paid_total,normalized_records:norm.records.length}));

'use strict';
// LSPV-2/578 SOURCE/DEF/RES producer/replayer. NOT an authoritative R_mix341 checker.
// node experiments/arc/lspv2_578_native386_target_unit_os.cjs REPO_ROOT OUT_DIR
const fs=require('fs'),path=require('path'),cp=require('child_process'),os=require('os');
const crypto=require('crypto'),assert=require('assert/strict');
const root=path.resolve(process.argv[2]||'.'),out=path.resolve(process.argv[3]||'/tmp/lspv2_578');
fs.mkdirSync(out,{recursive:true});
const get=p=>fs.readFileSync(path.join(root,p));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitblob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${b.length}\0`),b])).digest('hex');
const checkPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const checker=get('experiments/arc/lspv2_386_independent_verify.js');
assert.equal(gitblob(checker),'338305c0ce101704205e57543756b8127074a986');
const source=get('results/raw/arc/574_k01_SIGNED_SOURCE.cnf');
assert.equal(hash(source),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const seed=JSON.parse(get('results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json'));
const clone=x=>JSON.parse(JSON.stringify(x));
const original=seed.records.slice(0,17);assert.equal(original.length,17);
assert.deepEqual(source.toString().trim().split('\n').slice(1).map(s=>s.trim().split(/\s+/).slice(0,-1).map(Number)),original.map(r=>r.c));
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const key=c=>c.join(',');const clauses0=original.map(r=>r.c);
function project(t,order,details=false){
  const clauses=clauses0.map(x=>x.slice()),parents=clauses.map(()=>null);
  const intern=new Map(clauses.map((c,i)=>[key(c),i]));let live=new Set(clauses.map((_,i)=>i));
  for(const p of order){
    const left=[...live].filter(i=>clauses[i].includes(p)),right=[...live].filter(i=>clauses[i].includes(-p)),fresh=[];
    for(const i of left)for(const j of right){
      const c=canon([...clauses[i].filter(x=>x!==p),...clauses[j].filter(x=>x!==-p)]);
      if(c.some(x=>c.includes(-x))||intern.has(key(c)))continue;
      intern.set(key(c),clauses.length);fresh.push(clauses.length);clauses.push(c);parents.push([i,j,p]);
    }
    for(const i of [...left,...right])live.delete(i);
    for(const i of fresh)live.add(i);
  }
  if(!intern.has(String(t))||!intern.has(String(-t)))return null;
  const need=new Set(),stack=[intern.get(String(t)),intern.get(String(-t))];
  while(stack.length){const i=stack.pop();if(need.has(i))continue;need.add(i);if(parents[i])stack.push(parents[i][0],parents[i][1]);}
  const n=[...need].filter(i=>i>=17).length;
  return details?{n,clauses,parents,intern,need}:n;
}
function* permutations(xs,k=0){if(k===xs.length){yield xs.slice();return;}for(let j=k;j<xs.length;j++){[xs[k],xs[j]]=[xs[j],xs[k]];yield* permutations(xs,k+1);[xs[k],xs[j]]=[xs[j],xs[k]];}}
let best=null,ncases=0;const hist={},byTarget={};
for(let t=1;t<=6;t++){
  let min=Infinity;for(const order of permutations([1,2,3,4,5,6,7].filter(x=>x!==t))){
    const n=project(t,order);if(n===null)continue;ncases++;hist[n]=(hist[n]||0)+1;min=Math.min(min,n);
    if(!best||n<best.n||n===best.n&&t<best.t)best={n,t,order:order.slice()};
  }byTarget[t]=min;
}
assert.equal(ncases,4320);assert.equal(best.n,28);
const {n,clauses,parents,intern,need}=project(best.t,best.order,true);
const z=999999,t=best.t,records=clone(original);
records.push({kind:'DEF',c:canon([z,-t]),parents:[],gate:0});
records.push({kind:'DEF',c:canon([-z,t]),parents:[],gate:0});
const remap=new Map(records.slice(0,17).map((_,i)=>[i,i]));
for(let i=17;i<clauses.length;i++){
  if(!need.has(i))continue;
  const [a,b,p]=parents[i];assert(remap.has(a)&&remap.has(b));
  remap.set(i,records.length);
  records.push({kind:'RES',c:clauses[i],parents:[remap.get(a),remap.get(b)],pivot:p});
}
const plusParent=records.length;records.push({kind:'RES',c:[z],parents:[remap.get(intern.get(String(t))),17],pivot:t});
const minusParent=records.length;records.push({kind:'RES',c:[-z],parents:[remap.get(intern.get(String(-t))),18],pivot:-t});
records.push({kind:'RES',c:[],parents:[plusParent,minusParent],pivot:z});
const resolution=records.filter(r=>r.kind==='RES').length;assert.equal(resolution,31);
const plus={spec:clone(seed.spec),gate_defs:[[0,z,t,t]],records,summary:{source:17,def_views:2,resolution,paid_gates:1,paid_total:32,live_records:records.length}};
const minus=clone(plus);minus.records.at(-1).parents.reverse();minus.records.at(-1).pivot=-z;
const near=clone(plus);near.gate_defs[0][1]=1000000;
for(const r of near.records){r.c=canon(r.c.map(x=>x===z?1000000:x===-z?-1000000:x));if(r.pivot===z)r.pivot=1000000;}
const cases=[['positive_999999_core_only',plus,true,false],['negative_999999_cli_accept',minus,true,true],['positive_1000000_cli_accept',near,true,true]];
for(const [name,change] of [
 ['underpayment',d=>d.summary.paid_total--],
 ['source_forgery',d=>d.records[0].c=[-d.spec.guard]],
 ['wrong_gate_owner',d=>d.records[17].gate=51],
 ['forward_dependency',d=>d.records.at(-1).parents[0]=d.records.length],
 ['wrong_signed_pivot',d=>d.records.at(-1).pivot=-1000000],
 ['unknown_AND3_opcode',d=>d.records.at(-1).kind='AND3']]){
  const d=clone(near);change(d);cases.push([name,d,false,false]);
}
const checkText=checker.toString();const split='for(const f of process.argv.slice(2))';assert(checkText.includes(split));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2_578_'));
const coreFile=path.join(tmp,'original_core_entrypoint.cjs');
fs.writeFileSync(coreFile,checkText.slice(0,checkText.indexOf(split))+'\nconst d=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify(checkProof(d,{control:true})));\n');
const run=(file,input)=>cp.spawnSync(process.execPath,[file,input],{encoding:'utf8',timeout:15000});
const results=[];
try{
 for(const [name,d,coreExpected,cliExpected] of cases){
   const bytes=Buffer.from(JSON.stringify(d)+'\n');const file=path.join(out,`${name}.json`);fs.writeFileSync(file,bytes);
   const core=run(coreFile,file),cli=run(checkPath,file);assert.equal(core.status===0,coreExpected,name+' core');assert.equal(cli.status===0,cliExpected,name+' CLI');
   if(name==='positive_999999_core_only')assert.match(cli.stderr,/accepted a corrupted proof/);
   results.push({name,core_accept:coreExpected,cli_accept:cliExpected,sha256:hash(bytes),bytes:bytes.length,
      core:coreExpected?JSON.parse(core.stdout):null,cli:cliExpected?JSON.parse(cli.stdout):null});
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const raw={run:'LSPV2_578',status:'PROVED/RESTRICTED fixed corpus plus original-checker OS replay; R_mix341 OPEN',
 checker_git_blob:gitblob(checker),source_sha256:hash(source),schedule_count:ncases,histogram:hist,
 minimum_by_target:byTarget,best_DP_projection:best,shared_resolution:n,full_resolution:resolution,
 free_DEF_facets:2,once_paid_gate_owners:1,logical_work:32,results};
fs.writeFileSync(path.join(out,'578_native386_raw.json'),JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({schedules:ncases,best,work:32,case_verdicts:results.map(x=>[x.name,x.core_accept,x.cli_accept]),
 accepted_assertions:results.filter(x=>x.cli).reduce((a,x)=>a+x.cli.assertions,0)}));

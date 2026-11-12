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


// LSPV-2/579: original-/386 duplicate-DEF normal form, NOT a new checker.
// /578 above constructs a source-pinned, actual-CLI-accepted W32 packet.
{
const base=clone(minus);
const earliest=(d)=>{
  const copy=clone(d),first=new Map(),remap=[],kept=[];
  let deleted=0;
  d.records.forEach((r,i)=>{
    if(r.kind==='DEF'){
      const key=JSON.stringify([r.gate,r.c]);
      if(first.has(key)){remap[i]=first.get(key);deleted++;return;}
      first.set(key,kept.length);
    }
    const q=clone(r);
    q.parents=q.parents.map(j=>{assert(Number.isInteger(j)&&j<i&&remap[j]!==undefined);return remap[j];});
    remap[i]=kept.length;kept.push(q);
  });
  copy.records=kept;copy.summary.def_views=kept.filter(r=>r.kind==='DEF').length;
  copy.summary.live_records=kept.length;
  return {packet:copy,deleted};
};
const pad=(d,k,live)=>{
  const copy=clone(d),before=copy.records,at=19;
  assert.equal(before[17].kind,'DEF');assert.equal(before[18].kind,'DEF');
  const additions=Array.from({length:k},(_,i)=>clone(before[17+i%2]));
  copy.records=[...before.slice(0,at),...additions,...before.slice(at).map(r=>{
    const q=clone(r);q.parents=q.parents.map(j=>j>=at?j+k:j);return q;
  })];
  if(live&&k>=2){
    let redirected=0;
    for(const q of copy.records.slice(at+k))if(q.kind==='RES'){
      const a=q.parents.indexOf(17),b=q.parents.indexOf(18);
      if(a>=0){q.parents[a]=at;redirected++;}
      if(b>=0){q.parents[b]=at+1;redirected++;}
    }
    assert.equal(redirected,2);
  }
  copy.summary.def_views+=k;copy.summary.live_records+=k;
  return copy;
};
const attempts=[['base_W32',base,true]];
for(const k of [1,2,8,64,128])attempts.push(['repeated_'+k,pad(base,k,k>=2),true]);
const badFacet=pad(base,2,true);badFacet.records[19].c=[123];attempts.push(['negative_facet',badFacet,false]);
const badPayment=pad(base,2,true);badPayment.summary.paid_total++;attempts.push(['negative_payment',badPayment,false]);
const badParent=pad(base,2,true);badParent.records[51].parents[0]=52;attempts.push(['negative_forward_parent',badParent,false]);
const badOwner=pad(base,2,true);badOwner.records[19].gate=999;attempts.push(['negative_owner',badOwner,false]);
let baselineHash=null;const observed=[];
for(const [name,d,expected] of attempts){
  const b=Buffer.from(JSON.stringify(d)+'\n'),file=path.join(out,'579_'+name+'.json');fs.writeFileSync(file,b);
  const run=cp.spawnSync(process.execPath,[checkPath,file],{encoding:'utf8',timeout:15000});
  assert.equal(run.status===0,expected,name+': '+run.stderr);
  let normalizedHash=null,normalizedBytes=null,normalizedRecords=null,removed=null,normalizedAssertions=0;
  if(expected){
    const z=earliest(d),u=earliest(z.packet);removed=z.deleted;
    assert.equal(u.deleted,0);assert.deepEqual(u.packet,z.packet);
    assert.equal(z.packet.summary.paid_total,d.summary.paid_total);
    const G=z.packet.gate_defs.length,R=z.packet.summary.resolution,S=z.packet.summary.source;
    assert(z.packet.summary.def_views<=3*G);
    assert(z.packet.records.length<=S+R+3*G);
    const bb=Buffer.from(JSON.stringify(z.packet)+'\n'),normalized=path.join(out,'579_'+name+'_normalized.json');
    fs.writeFileSync(normalized,bb);
    const nr=cp.spawnSync(process.execPath,[checkPath,normalized],{encoding:'utf8',timeout:15000});
    assert.equal(nr.status,0,'normalized '+name+': '+nr.stderr);
    normalizedAssertions=JSON.parse(nr.stdout).assertions;
    normalizedHash=hash(bb);normalizedBytes=bb.length;normalizedRecords=z.packet.records.length;
    if(baselineHash===null)baselineHash=normalizedHash;
    assert.equal(normalizedHash,baselineHash,'same canonical W32 after dedup');
  }
  observed.push({name,expected,original_cli_accept:run.status===0,sha256:hash(b),
    bytes:b.length,records:d.records.length,paid_work:d.summary.paid_total,
    native_assertions:expected?JSON.parse(run.stdout).assertions:0,
    normalized_sha256:normalizedHash,normalized_bytes:normalizedBytes,
    normalized_records:normalizedRecords,removed,normalized_assertions:normalizedAssertions,
    failure:expected?null:run.stderr.trim().split('\n')[0]});
}
assert.equal(baselineHash,'23bbc894ef85c7c946c8d646239b3754cf08edfb76eb3ee26771d5aeab0bd854');
const ledger={id:'LSPV2_579',original_checker_blob:gitblob(checker),
 source_sha256:hash(source),source_clauses:17,
 theorem:'Every originally accepted /386 packet has a cost-identical complete-CLI accepted duplicate-DEF normal form with records <= m+3W.',
 status:'PROVED/RESTRICTED native checker code lemma, COMPUTATIONAL 10 OS cases; R_mix341 OPEN',
 cases:observed};
fs.writeFileSync(path.join(out,'579_facet_dedup_raw.json'),JSON.stringify(ledger,null,2)+'\n');
console.log(JSON.stringify({run:'579',positive:observed.filter(x=>x.expected).length,
 negative:observed.filter(x=>!x.expected).length,
 original_assertions:observed.reduce((a,x)=>a+x.native_assertions,0),
 normalized_assertions:observed.reduce((a,x)=>a+x.normalized_assertions,0),
 max_original_records:Math.max(...observed.map(x=>x.records)),
 normalized_records:observed[0].normalized_records,normalized_sha256:baselineHash}));
}

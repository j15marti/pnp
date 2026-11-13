#!/usr/bin/env node
'use strict';
/* LSPV2/586: original /386 checker (unmodified) prefix-pair replay.
   A separate NON-AUTHORITATIVE JSON injector; it does not implement R_mix341. */
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert/strict');
const root=process.cwd();
const files={
 checker:'experiments/arc/lspv2_386_independent_verify.js',
 seed:'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',
 source:'results/raw/arc/574_k01_SIGNED_SOURCE.cnf'
};
const pins={checker:'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113',
 seed:'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0',
 source:'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c'};
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const data={};for(const [k,p] of Object.entries(files)){
  data[k]=fs.readFileSync(p);assert.equal(hash(data[k]),pins[k],`source pinned ${k}`);
}
const seed=JSON.parse(data.seed),last=seed.records.length-1;
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(',');
const sourceNumbers=data.source.toString().trim().split(/\s+/).map(Number);
assert.equal(sourceNumbers[2],7);assert.equal(sourceNumbers[3],17);
let clauses=[],clause=[];for(const n of sourceNumbers.slice(4)){
 if(n===0){clauses.push(norm(clause));clause=[]}else clause.push(n);
}
assert.equal(clauses.length,17);assert.equal(clause.length,0);
assert.deepEqual(clauses.sort(),seed.records.filter(r=>r.kind==='SOURCE').map(r=>norm(r.c)).sort());
function inject(v,target,key,value,p=[],padding=0){
 if(Array.isArray(v))return '['+v.map((x,i)=>inject(x,target,key,value,p.concat(i),padding)).join(',')+']';
 if(v!==null&&typeof v==='object'){
  const parts=Object.entries(v).map(([k,x])=>JSON.stringify(k)+':'+inject(x,target,key,value,p.concat(k),padding));
  if(JSON.stringify(p)===JSON.stringify(target))parts.push(' '.repeat(padding)+JSON.stringify(key)+':'+JSON.stringify(value));
  return '{'+parts.join(',')+'}';
 }
 return JSON.stringify(v);
}
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-586-'));const cases=[];
function run(name,raw,expect){
 const buffer=Buffer.from(raw,'utf8'), f=path.join(dir,`c${cases.length}.json`);fs.writeFileSync(f,buffer);
 const out=cp.spawnSync(process.execPath,[path.join(root,files.checker),f],{encoding:'utf8',maxBuffer:3000000});
 const accepted=out.status===0;assert.equal(accepted,expect,`native result ${name}: ${out.stderr}`);
 const parsed=JSON.parse(raw);
 let assertions=null,paid=null,negative_tests=null;
 if(accepted){let r=JSON.parse(out.stdout);assertions=r.assertions;paid=r.paid;negative_tests=r.negativeTests;assert.equal(paid,29);assert.deepEqual(parsed,seed);}
 else assert.notDeepEqual(parsed,seed);
 cases.push({name,accepted,sha256:hash(buffer),bytes:buffer.length,
   parsed_equals_original:JSON.stringify(parsed)===JSON.stringify(seed),assertions,paid,negative_tests,
   error:accepted?null:(out.stderr.match(/Error: [^\n]+/)||['native rejection'])[0]});
 fs.unlinkSync(f);
 return buffer;
}
run('native_original_seed',data.seed.toString('utf8'),true);
const comparisons=[];
const controls=[
 {name:'terminal_kind',path:['records',last],key:'kind',good:'RES',bad:'AND3'},
 {name:'terminal_pivot',path:['records',last],key:'pivot',good:7,bad:99998},
 {name:'first_signed_source',path:['records',0],key:'c',good:seed.records[0].c,bad:[-seed.spec.guard]},
 {name:'payment_total',path:['summary'],key:'paid_total',good:29,bad:0},
];
for(const t of controls){
 const a=inject(seed,t.path,t.key,t.good)+'\n',b=inject(seed,t.path,t.key,t.bad)+'\n';
 let prefix=0;for(;prefix<Math.min(a.length,b.length)&&a[prefix]===b[prefix];prefix++);
 assert(prefix>100,`${t.name} sufficient common prefix`);
 const ok=run(t.name+'_accepted',a,true),bad=run(t.name+'_rejected',b,false);
 comparisons.push({key:t.name,common_prefix_bytes:prefix,accepted_bytes:ok.length,rejected_bytes:bad.length});
}
for(const padding of [64,512,8192]){
 const pathToTerminal=['records',last];
 const a=inject(seed,pathToTerminal,'kind','RES',[],padding)+'\n';
 const b=inject(seed,pathToTerminal,'kind','AND3',[],padding)+'\n';
 let prefix=0;for(;prefix<Math.min(a.length,b.length)&&a[prefix]===b[prefix];prefix++);
 const good=run('terminal_kind_padding_'+padding+'_accepted',a,true);
 const bad=run('terminal_kind_padding_'+padding+'_rejected',b,false);
 assert.equal(prefix,2769+padding);
 comparisons.push({key:'terminal_kind_padding_'+padding,common_prefix_bytes:prefix,
  accepted_bytes:good.length,rejected_bytes:bad.length});
}
fs.rmSync(dir,{recursive:true,force:true});
const result={schema:'LSPV2-586-NATIVE386-NO-EARLY-COMMIT/v1',status:'COMPUTATIONAL; original /386 ONLY',
 authority:{files,pins},source_clauses:17,source_variables:7,
 theorem_scope:'For all k>=0, accepted/rejected continuations can share >=k additional whitespace bytes after the original active member: fixed-lag irrevocable semantic commitment is incomplete absent rollback or unique-key authority',
 cases,comparisons,totals:{accepted:cases.filter(x=>x.accepted).length,rejected:cases.filter(x=>!x.accepted).length,
 native_assertions:cases.reduce((a,x)=>a+(x.assertions||0),0),native_negative_tests:cases.reduce((a,x)=>a+(x.negative_tests||0),0)}};
const output=process.argv[2]||'results/raw/arc/2026-11-12_1812_LSPV2_586_NO_EARLY_COMMIT_RAW.json';
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',output,comparisons,totals:result.totals},null,2));

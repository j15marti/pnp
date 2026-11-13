'use strict';
// LSPV-2/584. Reference MAY abstraction, not the historical R_mix341 checker.
// Run from repository root: node experiments/arc/lspv2_584_semantic_entailment_may.cjs [raw-result.json]
const fs=require('fs'),path=require('path'),cp=require('child_process'),os=require('os'),crypto=require('crypto');
const root=process.env.PNP584_ROOT||process.cwd();
const at=p=>path.join(root,p),hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const checker=at('experiments/arc/lspv2_386_independent_verify.js');
const seedBytes=fs.readFileSync(at('results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json'));
const srcBytes=fs.readFileSync(at('results/raw/arc/574_k01_SIGNED_SOURCE.cnf'));
if(hash(fs.readFileSync(checker))!=='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113'||
   hash(seedBytes)!=='0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0'||
   hash(srcBytes)!=='3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c')throw Error('pinned source/checker/seed changed');
const s=srcBytes.toString().trim().split(/\s+/),num=Number(s[2]),count=Number(s[3]);
if(s[0]!=='p'||s[1]!=='cnf'||num!==7||count!==17)throw Error('bad independent source');
let clauses=[],row=[];for(const tok of s.slice(4)){const v=Number(tok);if(v===0){clauses.push(row);row=[]}else row.push(v)}
if(row.length||clauses.length!==17)throw Error('wrong source clauses');
const seed=JSON.parse(seedBytes),key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
for(let i=0;i<17;i++)if(seed.records[i].kind!=='SOURCE'||JSON.stringify(seed.records[i].c)!==JSON.stringify(key(clauses[i])))throw Error('SOURCE/sign/order drift');
const sat=(c,b)=>c.some(l=>!!((b>>(Math.abs(l)-1))&1)===(l>0));
const models=rows=>Array.from({length:1<<num},(_,b)=>b).filter(b=>rows.every(c=>sat(c,b))).length;
const allModels=models(clauses),leave=clauses.map((_,i)=>models(clauses.filter((_,j)=>i!==j)));
let pairs=0,unsatPairs=0;for(let i=0;i<17;i++)for(let j=i+1;j<17;j++){pairs++;unsatPairs+=Number(models([clauses[i],clauses[j]])===0)}
if(allModels!==0||Math.min(...leave)<1||pairs!==136||unsatPairs!==0)throw Error('independent SAT controls failed');
const copy=x=>JSON.parse(JSON.stringify(x)),coarse=copy(seed);
coarse.records=seed.records.slice(0,17).concat([{kind:'LOCAL-CONVERT',c:[],parents:[0],context:'ROOT',hypothetical:'MAY only'}]);
coarse.summary={source:17,def_views:0,resolution:0,paid_gates:1,paid_total:1,live_records:18};
const forged=copy(seed);forged.records[0].c=[-7];
const pivot=copy(seed);pivot.records.at(-1).pivot=0;
const under=copy(seed);under.summary.paid_total=28;
const ownerless=copy(seed);ownerless.gate_defs=[];ownerless.summary.paid_gates=0;ownerless.summary.paid_total=28;
const cases=[['accepted_W29',seed,true],['hypothetical_global_entailment_W1',coarse,false],['forged_source',forged,false],['invalid_pivot',pivot,false],['underpayment',under,false],['ownerless_CLI_defect',ownerless,false]];
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp584-')),verdicts=[];
try{for(const [name,obj,expected] of cases){
 const buf=Buffer.from(JSON.stringify(obj)+'\n'),p=path.join(dir,name+'.json');fs.writeFileSync(p,buf);
 const r=cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8'}),accept=r.status===0;
 if(accept!==expected)throw Error('native disagreement: '+name+' '+r.stderr);
 verdicts.push({name,accept,bytes:buf.length,sha256:hash(buf),declared_W:obj.summary.paid_total,
  rejection:accept?null:r.stderr.match(/Error: ([^\n]+)/)?.[1]||r.stderr.trim().slice(-100)});
}}finally{fs.rmSync(dir,{recursive:true,force:true})}
const result={run:'LSPV2/584',source_sha256:hash(srcBytes),checker_sha256:hash(fs.readFileSync(checker)),seed_sha256:hash(seedBytes),
  source_models:allModels,leave_one_out_model_range:[Math.min(...leave),Math.max(...leave)],pairwise_source_tests:pairs,pairwise_unsat:unsatPairs,
  global_entailment_may_costs:[0,1,2,7].map(c=>({fixed_virtual_cost:c,abstract_total_W:1+c})),
  native_verdicts:verdicts,native_accepts:verdicts.filter(v=>v.accept).length,native_rejects:verdicts.filter(v=>!v.accept).length,
  scope:'native /386 accepts baseline and rejects hypothetical MAY step; full R_mix341 not authenticated'};
const text=JSON.stringify(result,null,2)+'\n';if(process.argv[2])fs.writeFileSync(process.argv[2],text);console.log(text);

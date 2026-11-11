#!/usr/bin/env node
'use strict';
// LSPV-2/555 archived /386 accepted terminal-cone DEF-RES splice.
// OS Node original-checker differential runner; not the historical full mixed checker.
// Usage: node experiments/arc/lspv2_555_live_def_res_splice.cjs [--emit DIR]
const fs=require('fs'),path=require('path'),os=require('os'),crypto=require('crypto');
const {spawnSync}=require('child_process');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedpath=path.join(root,'results/raw/arc/2026-11-11_0316_LSPV2_554_ACCEPTED_GATE_ORDER_012.json');
const expected={checker:'338305c0ce101704205e57543756b8127074a986',seed:'afd43c6cdc2e40fefc3c9623bb14fdf8e5b89865'};
const assert=(b,msg)=>{if(!b)throw Error(msg)};
const copy=x=>JSON.parse(JSON.stringify(x));
const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
const blob=x=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+x.length+'\0'),x])).digest('hex');
const cb=fs.readFileSync(checker),sb=fs.readFileSync(seedpath);
assert(blob(cb)===expected.checker,'checker source blob drift');
assert(blob(sb)===expected.seed,'K4 seed blob drift');
const seed=JSON.parse(sb);
assert(seed.records.length===48&&seed.summary.paid_total===31&&seed.gate_defs.length===3,'seed counters');
function splice(k){
 assert(Number.isInteger(k)&&k>=0&&k<=128,'k');
 const x=copy(seed);
 if(!k)return x;
 const old=x.records;
 assert(JSON.stringify(old[0].c)==='[1,-8]'&&
 JSON.stringify(old[10].c)==='[-1,-4,-5,-7]'&&
 JSON.stringify(x.gate_defs[0])==='[0,8,1,4]','source/owner mismatch');
 const shift=j=>j<3?j:j<20?j+1:j+1+2*k;
 const rec=old.slice(0,3).map(copy);
 rec.push({kind:'DEF',gate:0,c:[-1,-4,8],parents:[]});
 rec.push(...old.slice(3,20).map(copy));
 for(let t=0;t<k;t++){
  const src=t===0?shift(10):rec.length-1;
  rec.push({kind:'RES',c:[-4,-5,-7,-8],parents:[0,src],pivot:1});
  rec.push({kind:'RES',c:[-1,-4,-5,-7],parents:[rec.length-1,3],pivot:-8});
 }
 const final=rec.length-1;
 for(let j=20;j<old.length;j++){
  const r=copy(old[j]);r.parents=r.parents.map(p=>p===10?final:shift(p));rec.push(r);
 }
 x.records=rec;
 x.summary.def_views++;
 x.summary.resolution+=2*k;
 x.summary.paid_total+=2*k;
 x.summary.live_records=rec.length;
 return x;
}
function cone(p){
 const seen=new Set(),depth=[];
 function visit(i){assert(i>=0&&i<p.records.length,'bad index');if(seen.has(i))return;seen.add(i);for(const j of p.records[i].parents)visit(j)}
 visit(p.records.length-1);
 for(let i=0;i<p.records.length;i++)depth[i]=p.records[i].parents.length?1+Math.max(...p.records[i].parents.map(j=>depth[j])):0;
 return {seen,depth:depth.at(-1)};
}
const cases=[0,1,2,4,16].map(k=>({name:'positive_k_'+k,k,want:true,packet:splice(k)}));
function neg(name,fn){const packet=splice(1);fn(packet);cases.push({name,k:1,want:false,packet})}
neg('wrong_signed_facet',p=>p.records[3].c=[-1,4,8]);
neg('wrong_first_pivot',p=>p.records[21].pivot=-1);
neg('wrong_second_pivot',p=>p.records[22].pivot=8);
neg('wrong_second_resolvent',p=>p.records[22].c=[-1,-4,-5]);
neg('future_parent',p=>p.records[22].parents[0]=999);
neg('underpaid_summary',p=>p.summary.paid_total=31);
neg('forged_original_source',p=>p.records[11].c=[1,-4,-5,-7]);
const outdir=process.argv[2]==='--emit'?process.argv[3]:null;
if(process.argv[2]==='--emit')assert(outdir,'--emit requires DIR');
if(outdir)fs.mkdirSync(outdir,{recursive:true});
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-555-')),result=[];
try{
 for(const q of cases){
  const bytes=Buffer.from(JSON.stringify(q.packet)+'\n','utf8');
  const f=path.join(tmp,q.name+'.json');fs.writeFileSync(f,bytes);
  if(outdir)fs.writeFileSync(path.join(outdir,q.name+'.json'),bytes);
  const p=spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:30000,maxBuffer:1048576});
  const accepted=p.status===0&&!p.error;
  assert(accepted===q.want,q.name+' checker mismatch '+(p.stderr||'').slice(0,300));
  const cg=cone(q.packet),live=q.k>0&&cg.seen.has(3)&&Array.from({length:2*q.k},(_,i)=>cg.seen.has(21+i)).every(Boolean);
  const row={case:q.name,k:q.k,accepted,bytes:bytes.length,sha256:sha256(bytes),
     paid:q.packet.summary.paid_total,records:q.packet.records.length,
     sink_depth:cg.depth,sink_reachable:cg.seen.size,all_splice_nodes_live:live};
  if(accepted){
   const o=JSON.parse(p.stdout.trim().split('\n').at(-1));
   assert(o.paid===31+2*q.k&&o.res===28+2*q.k&&o.def===3,'paid stats');
   assert(o.sources===17&&o.negativeTests===11,'original CLI negative tests');
   if(q.k)assert(live,'splices not connected to sink');
   row.native={paid:o.paid,res:o.res,owners:o.def,source:o.sources,
      original_assertions:o.assertions,original_negative_tests:o.negativeTests};
  }else row.original_error=(p.stderr||String(p.error)).split('\n')[0];
  result.push(row);
 }
}finally{for(const f of fs.readdirSync(tmp))fs.unlinkSync(path.join(tmp,f));fs.rmdirSync(tmp)}
const raw={run:'LSPV2_555',provenance:'unmodified original archived /386 verifier via actual OS Node subprocess',
  checker_blob:expected.checker,seed_blob:expected.seed,cases:result,
  accepted:result.filter(x=>x.accepted).length,rejected:result.filter(x=>!x.accepted).length,
  status:'COMPUTATIONAL; original /386 only; P versus NP OPEN'};
if(outdir)fs.writeFileSync(path.join(outdir,'results.json'),JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw,null,2));

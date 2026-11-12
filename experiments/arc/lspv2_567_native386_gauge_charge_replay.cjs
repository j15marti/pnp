#!/usr/bin/env node
'use strict';
// LSPV-2/567: REFERENCE gauge transformer; the called /386 checker is original.
// This does NOT implement, or claim authority for, the full R_mix341 calculus.
// Run: node experiments/arc/lspv2_567_native386_gauge_charge_replay.cjs --seed=0
// Repeat --seed=1 and --seed=2, each an independently bounded 64-mask batch.
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const crypto=require('node:crypto');
const cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seeds=[
 'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',
 'results/raw/arc/2026-11-11_1512_LSPV2_566_ACCEPTED_HIGH_WIRE.json',
 'results/raw/arc/2026-11-11_1512_LSPV2_566_ACCEPTED_NESTED_HIGH_WIRES.json'
];
const pins=[
 '338305c0ce101704205e57543756b8127074a986',
 '318c52d99977ea4e91bc8554051138a700c1dc94',
 '371e8bf67fc4b002c56f0c7b79527089a5571ded',
 'e7f749868d6d96af14bcf8fbdd690d1333e14b3a'
];
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
function pinned(p,expected){const b=fs.readFileSync(path.join(root,p));assert.equal(gitBlob(b),expected,p+' changed');return b;}
const copy=x=>structuredClone(x);
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function gauge(input,mask){
 const p=copy(input),flips=new Set();
 p.spec.edges.forEach(([u,v],e)=>{
   if((mask & (1<<e))!==0){flips.add(e+1);p.spec.charge[u]^=1;p.spec.charge[v]^=1;}
 });
 const lit=x=>flips.has(Math.abs(x))?-x:x;
 p.gate_defs.forEach(g=>{g[2]=lit(g[2]);g[3]=lit(g[3]);});
 p.records.forEach(r=>{
   r.c=key(r.c.map(lit));
   if(r.kind==='RES')r.pivot=lit(r.pivot);
 });
 return p;
}
function runNative(packet,tmp,which){
 const data=Buffer.from(JSON.stringify(packet)+'\n','utf8');
 const where=path.join(tmp,'case.json');fs.writeFileSync(where,data);
 const start=process.hrtime.bigint();
 const out=cp.spawnSync(process.execPath,[path.join(root,checker),where],{encoding:'utf8',timeout:15000,maxBuffer:1024*1024});
 const ms=Number(process.hrtime.bigint()-start)/1e6;
 let stat=null;try{stat=JSON.parse(out.stdout.trim());}catch(_e){}
 return {name:which,sha256:sha256(data),bytes:data.length,accept:out.status===0&&!!stat,
          paid:stat?stat.paid:null,assertions:stat?stat.assertions:null,
          builtInNegatives:stat?stat.negativeTests:null,
          diagnostic:out.status===0?null:(out.stderr.split('\n').find(x=>/Error:|AssertionError/.test(x))||out.stderr.slice(0,170)),
          ms:Number(ms.toFixed(3))};
}
function makeCorruptions(p,base){
 const a=[];
 function mutation(name,fn){const q=copy(p);fn(q);a.push([name,q]);}
 mutation('stale_original_charge',q=>{q.spec.charge=[...base.spec.charge];});
 mutation('wrong_resolution_pivot_sign',q=>{const r=q.records.find(x=>x.kind==='RES'&&Math.abs(x.pivot)===4);assert(r);r.pivot=-r.pivot;});
 mutation('stale_defining_gate_input',q=>{assert(q.gate_defs.length);q.gate_defs[0][3]=-q.gate_defs[0][3];});
 mutation('source_occurrence_corrupted',q=>{const s=q.records.find(x=>x.kind==='SOURCE'&&x.source===0);assert(s);s.c[0]=-s.c[0];s.c=key(s.c);});
 mutation('underpaid_total',q=>q.summary.paid_total--);
 mutation('unsorted_resolvent',q=>{const x=q.records.find(r=>r.kind==='RES'&&r.c.length>1);x.c.reverse();});
 return a;
}
function main(){
 const arg=process.argv.find(x=>x.startsWith('--seed='));
 const k=arg?Number(arg.slice('--seed='.length)):0;
 assert(Number.isInteger(k)&&k>=0&&k<seeds.length,'seed must be 0, 1, or 2');
 pinned(checker,pins[0]);
 const base=JSON.parse(pinned(seeds[k],pins[k+1]).toString('utf8'));
 assert.equal(base.spec.edges.length,6,'K4-only 6-edge test');
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-567-'));
 const records=[],negative=[];
 try{
  for(let mask=0;mask<64;mask++){
   const p=gauge(base,mask),observed=runNative(p,tmp,'gauge-'+mask);
   const predicted=((mask & 7).toString(2).split('1').length-1)%2===0;
   assert.equal(observed.accept,predicted,'native CLI accepted unexpected mask '+mask);
   if(observed.accept){assert.equal(observed.paid,base.summary.paid_total);}
   records.push({mask,charge:p.spec.charge,expected:predicted,...observed});
  }
  if(k===2)for(const [name,p] of makeCorruptions(gauge(base,8),base)){
   const result=runNative(p,tmp,name);assert.equal(result.accept,false,'illegal packet accepted: '+name);negative.push(result);
  }
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
 const result={kind:'LSPV-2/567 ORIGINAL-CLI OS replay',sourceChecker:checker,checkerBlob:pins[0],
  seed:seeds[k],seedBlob:pins[k+1],runtime:process.version,
  results:records,corruptions:negative,accepted:records.filter(r=>r.accept).length,rejected:records.filter(r=>!r.accept).length};
 const folder=path.join(root,'results/raw/arc');
 const out=path.join(folder,'2026-11-11_1608_LSPV2_567_NATIVE_OS_SEED'+k+'.json');
 fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({output:out,accepted:result.accepted,rejected:result.rejected,corruptions:negative.length,sha256:sha256(fs.readFileSync(out))}));
}
main();

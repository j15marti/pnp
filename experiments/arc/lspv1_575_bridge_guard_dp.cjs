#!/usr/bin/env node
'use strict';
// LSPV-1/575. Deterministic, source-complete guarded Tseitin RES refutation.
// node experiments/arc/lspv1_575_bridge_guard_dp.cjs [--write]
const fs=require('node:fs'), path=require('node:path'), crypto=require('node:crypto'), cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const CHECK='experiments/arc/lspv2_386_independent_verify.js';
const CHECK_SHA='338305c0ce101704205e57543756b8127074a986';
const OUTPUT='results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json';
const edges=[[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[5,8],[5,9],[6,7],[6,8],[6,9],[7,8],[7,9],[0,5]];
const h=10, guard=16, charges=[1,0,0,0,0,0,0,0,0,0];
const order=[7,5,3,6,4,1,2,8,11,10,13,9,14,12,15];
const k=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const key=c=>JSON.stringify(c);
function makeSource(){
 const inc=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});
 const out=[];
 for(let v=0;v<h;v++)for(let m=0;m<8;m++){
   const bits=[m&1,(m>>1)&1,(m>>2)&1];
   if(bits.reduce((a,b)=>a+b,0)%2!==charges[v])
     out.push({kind:'SOURCE',c:k([...inc[v].map((e,i)=>bits[i]?-e:e),-guard]),parents:[],source:v});
 }
 out.push({kind:'SOURCE',c:[guard],parents:[],source:-1});
 if(out.length!==41)throw Error('source count mismatch');
 return out;
}
function build(){
 const rec=makeSource(), seen=new Map(rec.map((r,i)=>[key(r.c),i]));
 let active=new Map(rec.map((r,i)=>[key(r.c),i]));
 for(const p of order){
   const pos=[],neg=[],remain=new Map();
   for(const [json,i] of active){const c=JSON.parse(json);
     if(c.includes(p))pos.push([c,i]);
     else if(c.includes(-p))neg.push([c,i]);
     else remain.set(json,i);
   }
   for(const [A,ia] of pos)for(const [B,ib] of neg){
     const c=k([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
     if(c.some(x=>c.includes(-x)))continue;
     const s=key(c);
     if(!seen.has(s)){
       const id=rec.length;rec.push({kind:'RES',c,parents:[ia,ib],pivot:p});seen.set(s,id);
     }
     remain.set(s,seen.get(s));
   }
   active=remain;
 }
 const endpoint=active.get(key([-guard]));
 if(endpoint===undefined)throw Error('no derived negative guard');
 const keep=new Set(Array.from({length:41},(_,i)=>i));
 const work=[endpoint];
 while(work.length){const i=work.pop();if(keep.has(i))continue;keep.add(i);if(rec[i].kind==='RES')work.push(...rec[i].parents)}
 const ix=[...keep].sort((a,b)=>a-b),trans=new Map(ix.map((old,i)=>[old,i]));
 const records=ix.map(i=>({...rec[i],parents:rec[i].parents.map(j=>trans.get(j))}));
 records.push({kind:'RES',c:[],parents:[trans.get(40),trans.get(endpoint)],pivot:guard});
 const nres=records.filter(r=>r.kind==='RES').length;
 return {spec:{h,edges,charge:charges,guard},gate_defs:[[0,17,1,2]],records,
  summary:{source:41,resolution:nres,def_views:0,paid_gates:1,paid_total:nres+1,live_records:records.length}};
}
function checkIndependent(packet){
 const rec=packet.records,anc=new Set(), stack=[rec.length-1];
 while(stack.length){let i=stack.pop();if(anc.has(i))continue;anc.add(i);stack.push(...rec[i].parents)}
 const deadSources=Array.from({length:41},(_,i)=>i).filter(i=>!anc.has(i));
 if(rec.length!==103||packet.summary.paid_total!==63||deadSources.length!==4)throw Error('unexpected cost/ancestry');
 for(let i=0;i<rec.length;i++)if(rec[i].kind==='RES'){
   const r=rec[i],a=rec[r.parents[0]].c,b=rec[r.parents[1]].c;
   if(r.parents.some(j=>j>=i)||!a.includes(r.pivot)||!b.includes(-r.pivot))throw Error('unsound parents');
   const exp=k([...a.filter(x=>x!==r.pivot),...b.filter(x=>x!==-r.pivot)]);
   if(key(exp)!==key(r.c))throw Error('bad derived clause '+i);
 }
 let sat=0;
 for(let bits=0;bits<32768;bits++){
   let ok=true;
   for(let i=0;i<40&&ok;i++){
      ok=rec[i].c.some(x=>x===-guard||((bits>>(Math.abs(x)-1)&1)===(x>0?1:0)));
      // The unit guard is true, so -guard never satisfies a vertex clause.
      if(ok){ok=rec[i].c.some(x=>x!==-guard&&((bits>>(Math.abs(x)-1)&1)===(x>0?1:0)))}
   }
   if(ok)sat++;
 }
 if(sat!==0)throw Error('source unexpectedly SAT');
 return {terminalAncestors:anc.size,deadSources,sourceAssignmentsChecked:32768,satisfyingOriginalAssignments:sat,independentRESChecks:packet.summary.resolution};
}
const sha1Blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
function replayNative(packet,filepath){
 const checker=path.join(root,CHECK);
 if(sha1Blob(fs.readFileSync(checker))!==CHECK_SHA)throw Error('original archived checker not SHA pinned');
 const r=cp.spawnSync(process.execPath,[checker,filepath],{encoding:'utf8',timeout:30000});
 if(r.error||r.status!==0)throw Error('original CLI rejected '+(r.stderr||r.error));
 return JSON.parse(r.stdout.trim());
}
function main(){
 const packet=build(),independent=checkIndependent(packet);
 const bytes=Buffer.from(JSON.stringify(packet)+'\n');
 const dest=path.join(root,OUTPUT);
 if(process.argv.includes('--write'))fs.writeFileSync(dest,bytes);
 const tmp=path.join(require('node:os').tmpdir(),'lspv1_575_native_'+process.pid+'.json');
 fs.writeFileSync(tmp,bytes);
 let original;
 try{original=replayNative(packet,tmp)}finally{fs.unlinkSync(tmp)}
 if(original.paid!==63||original.res!==62||original.sources!==41||original.negativeTests!==11)throw Error('original mismatch');
 const report={status:'PASS',checkerGitBlob:CHECK_SHA,seed:'deterministic',eliminationOrder:order,
  packetSha256:crypto.createHash('sha256').update(bytes).digest('hex'),packetBytes:bytes.length,
  original,independent,outputPath:OUTPUT,model:'archived /386 SOURCE/paid AND2 DEF/RES only; not full historical R_mix341'};
 console.log(JSON.stringify(report,null,2));
}
main();

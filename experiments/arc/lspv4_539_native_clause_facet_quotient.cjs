'use strict';
// LSPV-4/539: archived /386 source-bound DEF/RES normalization.
// This is NOT a reconstruction of historical mixed R_mix341.
const cp=x=>JSON.parse(JSON.stringify(x));
function insert(p,i) {
 const q=cp(p),r=cp(q.records[i]),at=i+1;
 if(!['DEF','RES'].includes(r.kind))throw Error('not a derivation');
 q.records.splice(at,0,r);
 for(let j=at+1;j<q.records.length;j++)
   q.records[j].parents=q.records[j].parents.map(t=>t>=at?t+1:t).map(t=>t===i?at:t);
 if(r.kind==='DEF')q.summary.def_views++;
 else{q.summary.resolution++;q.summary.paid_total++;}
 q.summary.live_records++;return q;
}
function ensureFacet(p) {
 const q=cp(p);
 if(q.records.some(r=>r.kind==='DEF'))return q;
 if(JSON.stringify(q.gate_defs[0])!=='[0,8,1,4]')throw Error('unexpected owner');
 const at=q.records.findIndex(r=>r.kind==='RES');
 q.records.splice(at,0,{kind:'DEF',gate:0,c:[1,-8],parents:[]});
 for(let j=at+1;j<q.records.length;j++)
   q.records[j].parents=q.records[j].parents.map(t=>t>=at?t+1:t);
 q.summary.def_views++;q.summary.live_records++;return q;
}
function quotient(p){
 const q=cp(p),rs=q.records,first=new Map(),facet=new Map(),rep=[],keep=[];
 let removedDEF=0,removedRES=0;
 for(let i=0;i<rs.length;i++){
  const r=rs[i],c=JSON.stringify(r.c);let target=i;
  if(r.kind==='DEF'){
   const k=r.gate+'|'+c;
   if(facet.has(k))target=facet.get(k);else facet.set(k,i);
  }else if(r.kind==='RES'&&i!==rs.length-1&&first.has(c))target=first.get(c);
  if(target===i){keep.push(i);if(!first.has(c))first.set(c,i);}
  else if(r.kind==='DEF')removedDEF++;else removedRES++;
  rep.push(target);
 }
 const index=new Map(keep.map((i,j)=>[i,j]));
 q.records=keep.map(i=>{
  const r=cp(rs[i]);r.parents=r.parents.map(p=>{
   const j=index.get(rep[p]);
   if(!Number.isInteger(j)||j>=index.get(i))throw Error('invalid new parent');
   return j;
  });return r;
 });
 q.summary.def_views=q.records.filter(r=>r.kind==='DEF').length;
 q.summary.resolution=q.records.filter(r=>r.kind==='RES').length;
 q.summary.paid_total=q.summary.resolution+q.gate_defs.length;
 q.summary.live_records=q.records.length;
 return {packet:q,removedDEF,removedRES};
}
function core(src){
 const cut=src.indexOf('for(const f of process.argv.slice(2))');
 if(cut<0)throw Error('original CLI cutoff absent');
 const body=src.slice(0,cut).replace("const fs=require('fs'),crypto=require('crypto'),assert=require('assert');","");
 return new Function('structuredClone',body+';return checkProof;')(cp);
}
function cli(src,p){
 let lines=[];
 const req=name=>name==='fs'?{readFileSync:()=>JSON.stringify(p)}:
  name==='crypto'?{createHash:()=>({update:()=>({digest:()=>null})})}:
  name==='assert'?{}:(()=>{throw Error('unknown '+name)})();
 new Function('require','process','console','structuredClone',src)(
  req,{argv:['node','original','virtual.json']},{log:s=>lines.push(s)},cp);
 if(lines.length!==1)throw Error('CLI output missing');
 return JSON.parse(lines[0]);
}
function audit(src,s1,s2){
 const verify=core(src),rows=[],hostile=[];
 for(const [label,seed] of [['K4-28RES-29CLI',s1],['K4-nested-53',s2]]){
  verify(seed);
  for(const f of [0,1,8,32])for(const n of [0,1,3]){
   let q=ensureFacet(seed);
   for(let j=0;j<f;j++)q=insert(q,q.records.findIndex(r=>r.kind==='DEF'));
   for(let j=0;j<n;j++)q=insert(q,q.records.findIndex(r=>r.kind==='RES'));
   const a=verify(q),norm=quotient(q),b=verify(norm.packet),z=norm.packet;
   if(b.paid>a.paid||a.paid-b.paid!==norm.removedRES||a.sources!==b.sources)
    throw Error('cost or source unsound');
   if(JSON.stringify(q.spec)!==JSON.stringify(z.spec)||
      JSON.stringify(q.gate_defs)!==JSON.stringify(z.gate_defs))throw Error('changed source or owner');
   if(z.records.at(-1).c.length)throw Error('not a refutation');
   const row={seed:label,facetDuplicates:f,resolutionDuplicates:n,paidBefore:a.paid,
    paidAfter:b.paid,removedFacetRecords:norm.removedDEF,removedPaidRES:norm.removedRES,
    recordCountBefore:a.records,recordCountAfter:b.records,bytesBefore:JSON.stringify(q).length,
    bytesAfter:JSON.stringify(z).length,sourceRecords:a.sources};
   if((f===1&&n===1)||(f===32&&n===3)){
    const u=cli(src,q),v=cli(src,z);
    if(u.paid!==a.paid||v.paid!==b.paid)throw Error('complete CLI mismatch');
    row.completeCLIInput='ACCEPT';row.completeCLINormalized='ACCEPT';
    row.inputAssertions=u.assertions;row.normalAssertions=v.assertions;
   }
   rows.push(row);
  }
 }
 const p=quotient(s2).packet;
 const mutations=[
 ['forgedSOURCE',p=>p.records.find(r=>r.kind==='SOURCE').c=[12345]],
 ['wrongTariff',p=>p.summary.paid_total++],
 ['futureParent',p=>{const i=p.records.findIndex(r=>r.kind==='RES');p.records[i].parents[0]=i+1;}],
 ['invalidFacet',p=>p.records.find(r=>r.kind==='DEF').c=[777]],
 ['wrongTerminalPivot',p=>p.records.at(-1).pivot=999999],
 ['nonemptySink',p=>p.records.at(-1).c=[1]],
 ['duplicateSource',p=>{const r=cp(p.records.find(r=>r.kind==='SOURCE'));p.records.splice(0,0,r);p.summary.source++;p.summary.live_records++;}]
 ];
 for(const [name,fn] of mutations){const q=cp(p);fn(q);let reject=false;
  try{verify(q)}catch(e){reject=true;}if(!reject)throw Error(name+' accepted');
  hostile.push({name,rejected:true});
 }
 return {status:'PROVED/RESTRICTED with COMPUTATIONAL original-checker replay',
   checkerBlob:'338305c0ce101704205e57543756b8127074a986',
   seeds:{K4CLI29:'e3eb2a46857776089ab83f4ad50159ef622d2869',
          nested53:'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916'},
   originalCoreAccepted:rows.length,normalizedCoreAccepted:rows.length,
   originalCompleteCLIAccepted:rows.filter(r=>r.completeCLIInput).length,
   normalizedCompleteCLIAccepted:rows.filter(r=>r.completeCLINormalized).length,
   hostileRejected:hostile.length,hostile,rows,hostedV8OriginalBody:true,
   nativeNodeSubprocessExecuted:false,physicalRAMMeasured:false,
   historicFullMixedRmix341Recovered:false};
}
if(typeof module!=='undefined')module.exports={quotient,insert,ensureFacet,core,cli,audit};
if(typeof require!=='undefined'&&require.main===module){
 const fs=require('fs');
 const rd=p=>fs.readFileSync(p,'utf8');
 const src=rd('experiments/arc/lspv2_386_independent_verify.js');
 const s1=JSON.parse(rd('results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json'));
 const s2=JSON.parse(rd('results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json'));
 console.log(JSON.stringify(audit(src,s1,s2),null,2));
}
'use strict';
// LSPV-1/574. Fixed 10-vertex cubic bridge graph, complete original /386
// SOURCE/paid-DEF/strict-RES accepted-byte generator and checker replay.
// Run: node experiments/arc/lspv1_574_bridge_source_ancestry.cjs [--write]
// Requires Node >=18, standard library only, from j15marti/pnp checkout.
const EDGES=[[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],
             [5,8],[5,9],[6,7],[6,8],[6,9],[7,8],[7,9],[0,5]];
const H=10,E=15,GUARD=16,CHARGE=[1,0,0,0,0,0,0,0,0,0];
const DROP=new Set([1,2,21,22]);
function ck(x,msg){if(!x)throw Error(msg)}
function canon(a){
 const v=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 return v.some(x=>v.includes(-x))?null:v;
}
function makeSources(){
 const occ=Array.from({length:H},()=>[]);
 EDGES.forEach(([u,v],i)=>{occ[u].push(i+1);occ[v].push(i+1)});
 const out=[];
 for(let v=0;v<H;v++)for(let t=0;t<8;t++){
  const bits=[(t>>2)&1,(t>>1)&1,t&1];
  if((bits[0]^bits[1]^bits[2])===CHARGE[v])continue;
  const lits=occ[v].map((x,j)=>bits[j]?-x:x);
  out.push({kind:'SOURCE',parents:[],c:canon([...lits,-GUARD]),source:v});
 }
 out.push({kind:'SOURCE',parents:[],c:[GUARD],source:-1});
 ck(out.length===41,'source count');
 return out;
}
function build(){
 const records=makeSources(),active0=[...Array(40).keys()].filter(i=>!DROP.has(i));
 let active=new Set(active0);
 const perPivot=[];
 // Deterministic, explicit elimination order, no SAT oracle or semantic rule.
 for(const pivot of [15,1,3,10,2,11,13,12,14,8,9,4,5,6,7]){
  const pos=[...active].filter(i=>records[i].c.includes(pivot)).sort((a,b)=>a-b);
  const neg=[...active].filter(i=>records[i].c.includes(-pivot)).sort((a,b)=>a-b);
  const rest=new Set([...active].filter(i=>!pos.includes(i)&&!neg.includes(i)));
  const candidates=new Map();
  for(const i of pos)for(const j of neg){
   const c=canon([...records[i].c.filter(x=>x!==pivot),
                  ...records[j].c.filter(x=>x!==-pivot)]);
   if(!c)continue;
   const k=JSON.stringify(c),old=candidates.get(k);
   if(!old||i+j<old.i+old.j)candidates.set(k,{i,j,c});
  }
  const keep=[];
  const rank=(a,b)=>a.c.length-b.c.length||
                      JSON.stringify(a.c).localeCompare(JSON.stringify(b.c));
  for(const v of [...candidates.values()].sort(rank)){
   if([...rest].some(i=>records[i].c.every(x=>v.c.includes(x))))continue;
   if(keep.some(o=>o.c.every(x=>v.c.includes(x))))continue;
   keep.push(v);
  }
  for(const v of keep){
   const id=records.length;
   records.push({kind:'RES',parents:[v.i,v.j],pivot,c:v.c});
   rest.add(id);
  }
  perPivot.push({pivot,positive:pos.length,negative:neg.length,
                 produced:keep.length});
  active=rest;
 }
 ck(active.size===1,'unique end clause');
 const sink=[...active][0];
 ck(JSON.stringify(records[sink].c)==='[-16]','guard negation sink');
 records.push({kind:'RES',parents:[40,sink],pivot:GUARD,c:[]});
 const nres=records.length-41;
 const packet={
  spec:{h:H,edges:EDGES,charge:CHARGE,guard:GUARD},
  gate_defs:[[0,17,1,2]], // one conservative paid owner, no free facets
  records,
  summary:{source:41,def_views:0,resolution:nres,paid_gates:1,
           paid_total:nres+1,live_records:records.length}
 };
 return {packet,perPivot};
}
function independent(packet){
 const R=packet.records,ancestry=new Set();
 function visit(i){
  ck(Number.isInteger(i)&&i>=0&&i<R.length,'invalid ancestor');
  if(ancestry.has(i))return;ancestry.add(i);
  for(const parent of R[i].parents)visit(parent);
 }
 visit(R.length-1);
 const absent=[...Array(41).keys()].filter(i=>!ancestry.has(i));
 ck(absent.join(',')==='1,2,21,22','terminal source ancestry');
 const literals=R.slice(0,40).map(r=>r.c.filter(x=>x!==-GUARD));
 const core=literals.filter((c,i)=>!DROP.has(i));
 ck(core.length===36,'core count');
 const witness=Array(core.length).fill(null);
 let originalSat=0,coreSat=0;
 for(let m=0;m<(1<<E);m++){
  const sat=c=>c.some(l=>(((m>>(Math.abs(l)-1))&1)===Number(l>0)));
  if(literals.every(sat))originalSat++;
  let bad=0,which=-1;
  for(let j=0;j<core.length;j++)if(!sat(core[j])){bad++;which=j}
  if(bad===0)coreSat++;
  if(bad===1&&witness[which]===null)witness[which]=
      Array.from({length:E},(_,i)=>String((m>>i)&1)).join('');
 }
 ck(originalSat===0&&coreSat===0,'source must be UNSAT');
 ck(witness.every(w=>w!==null),'36-clause core is deletion minimal');
 // Independent signed-pivot replay; this does not replace original verifier.
 for(let i=41;i<R.length;i++){
  const r=R[i], [a,b]=r.parents;
  ck(r.kind==='RES'&&a<i&&b<i&&a>=0&&b>=0,'RES parent');
  const A=R[a].c,B=R[b].c,p=r.pivot;
  ck(A.includes(p)&&B.includes(-p),'signed pivot');
  const c=canon([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
  ck(c!==null&&JSON.stringify(c)===JSON.stringify(r.c),'resolvent');
 }
 const result={originalSources:41,originalSignedClauses:40,
  ancestrySourceCount:41-absent.length,notInTerminalAncestry:absent,
  reducedUnsignedCore:36,allSourceModels:originalSat,coreModels:coreSat,
  coreDeletionSATWitnesses:witness,
  paidResolution:R.length-41,paidDefinitionOwners:packet.gate_defs.length,
  paidTotal:packet.summary.paid_total,proofRecords:R.length};
 return result;
}
function runNative(checkerPath,packetPath){
 const cp=require('node:child_process').spawnSync(
   process.execPath,[checkerPath,packetPath],{encoding:'utf8',timeout:20000});
 return {accepted:cp.status===0&&cp.error==null,status:cp.status,
   stdout:cp.stdout.trim(),stderr:cp.stderr.trim(),
   exception:cp.error?String(cp.error):null};
}
function run(){
 const fs=require('node:fs'),path=require('node:path'),
       os=require('node:os'),crypto=require('node:crypto');
 const root=path.resolve(__dirname,'../..');
 const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
 const checkerSource=fs.readFileSync(checker);
 const hash=crypto.createHash('sha1').update(checkerSource).digest('hex');
 ck(hash==='338305c0ce101704205e57543756b8127074a986',
    'original /386 checker changed: '+hash);
 const {packet,perPivot}=build(),evidence=independent(packet);
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1_574_'));
 const outcomes=[];
 try{
  function replay(label,q,shouldAccept){
   const file=path.join(temp,label+'.json');
   fs.writeFileSync(file,JSON.stringify(q)+'\n','utf8');
   const r=runNative(checker,file);
   ck(r.accepted===shouldAccept,label+' unexpected native verdict '+r.stderr);
   outcomes.push({label,accepted:r.accepted,stdout:r.stdout,
                  stderr:r.stderr.slice(0,300)});
  }
  replay('original_positive',packet,true);
  const cases=[
   ['bad_signed_source',q=>q.records[1].c[0]*=-1],
   ['wrong_last_pivot',q=>q.records.at(-1).pivot=999999],
   ['dangling_parent',q=>q.records.at(-1).parents[0]=999999],
   ['underpaid',q=>q.summary.paid_total--],
   ['no_paid_owner',q=>q.gate_defs=[]],
   ['unrecognized_AND3',q=>q.records.at(-1).kind='AND3']
  ];
  for(const [label,mutate] of cases){
   const q=JSON.parse(JSON.stringify(packet));mutate(q);replay(label,q,false);
  }
  const results={
   schema:'LSPV1_574_BRIDGE_SOURCE_TERMINAL_ANCESTRY/v1',
   status:'PROVED/RESTRICTED symbolic parity contradiction + COMPUTATIONAL original /386 OS',
   checkerSha:hash,graph:{h:H,edges:EDGES,charge:CHARGE,guard:GUARD},
   independentlyChecked:evidence,perPivot,
   nativeOS:outcomes,negativeControls:cases.length,
   limitations:'Archived /386 sibling checker only; no full R_mix341 grammar'
  };
  if(process.argv.includes('--write')){
   fs.writeFileSync(path.join(root,'results/raw/arc/2026-11-11_0756_LSPV1_574_BRIDGE_PACKET.json'),
      JSON.stringify(packet,null,2)+'\n');
   fs.writeFileSync(path.join(root,'results/raw/arc/2026-11-11_0756_LSPV1_574_BRIDGE_NATIVE_OS_RAW.json'),
      JSON.stringify(results,null,2)+'\n');
  }
  process.stdout.write(JSON.stringify(results,null,2)+'\n');
 }finally{fs.rmSync(temp,{recursive:true,force:true})}
}
if(require.main===module)run();
module.exports={build,independent,canon,makeSources};

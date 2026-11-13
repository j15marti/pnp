'use strict';
// LSPV-4/587, exact K4 SOURCE/AND3/XOR span/register Pareto audit.
// Usage from repository root: node experiments/arc/lspv4_587_k4_span_register_native341.cjs [--os]
// No random seeds. Uses the pinned original /341 checker, not a new checker grammar.
const fs=require('fs');
const checkerPath='experiments/arc/lspv2_341_independent_verify.js';
const corpusPath='results/raw/arc/2026-11-10_1112_LSPV2_537_NATIVE_BYTE_CORPUS_RAW.json';
const checker=fs.readFileSync(checkerPath,'utf8');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const V=4,E=edges.length,charges=[1,0,0,0];
const incident=Array.from({length:V},()=>[]);
for(let e=0;e<E;e++)for(const v of edges[e])incident[v].push(e);
function insist(b,message){if(!b)throw Error('LSPV4/587: '+message)}
function sat(clause,bits){
 return clause.literals.some(x=>x>0?bits[x-1]===1:bits[-x-1]===0);
}
const clauses=[];
for(let v=0;v<V;v++)for(let m=0;m<8;m++){
 const bits=incident[v].map((_,k)=>(m>>k)&1);
 if(bits.reduce((a,b)=>a^b,0)===charges[v])continue;
 clauses.push({id:'s'+clauses.length,vertex:v,
  literals:incident[v].map((e,k)=>bits[k]?-(e+1):e+1)});
}
const deleted=clauses.map((c,i)=>{
 let assignment=null;
 for(let m=0;m<2**E;m++){
  const bits=Array.from({length:E},(_,e)=>(m>>e)&1);
  if(!sat(c,bits)&&clauses.every((d,j)=>i===j||sat(d,bits))){
   assignment=bits.join('');break;
  }
 }
 insist(assignment!==null,'missing original source deletion witness '+i);
 return {sourceId:c.id,assignment};
});
const base=new Map();
for(const c of clauses){
 const support=incident[c.vertex].slice();
 let table=0;
 for(let m=0;m<8;m++){
  const bits=Array(E).fill(0);
  support.forEach((e,j)=>bits[e]=(m>>j)&1);
  if(sat(c,bits))table|=1<<m;
 }
 base.set(c.id,{kind:'factor',support,table});
}
function packet(which){
 insist(['comb','xor-balanced','fully-balanced'].includes(which),'unknown shape');
 const proof=[],byId=new Map(base),roots=[];
 function and(aid,bid){
  const a=byId.get(aid),b=byId.get(bid),support=[...new Set([...a.support,...b.support])];
  insist(support.length<=3,'illegal AND3 support');
  let table=0;
  for(let m=0;m<1<<support.length;m++){
   const bits=Array(E).fill(0);
   support.forEach((e,j)=>bits[e]=(m>>j)&1);
   const val=x=>{
    let p=0;x.support.forEach((e,j)=>p|=bits[e]<<j);
    return (x.table>>p)&1;
   };
   if(val(a)&&val(b))table|=1<<m;
  }
  const p={id:'d'+proof.length,rule:'AND3',kind:'factor',parents:[aid,bid],support,table};
  proof.push(p);byId.set(p.id,p);return p.id;
 }
 function xor(aid,bid){
  const a=byId.get(aid),b=byId.get(bid);
  const p={id:'d'+proof.length,rule:'XOR',kind:'affine',parents:[aid,bid],
   row:{mask:'0x'+(BigInt(a.row.mask)^BigInt(b.row.mask)).toString(16),
        rhs:a.row.rhs^b.row.rhs}};
  proof.push(p);byId.set(p.id,p);return p.id;
 }
 for(let v=0;v<V;v++){
  const s=clauses.filter(c=>c.vertex===v).map(c=>c.id);
  let root;
  if(which==='fully-balanced'){
   root=and(and(s[0],s[1]),and(s[2],s[3]));
  }else{
   root=and(and(and(s[0],s[1]),s[2]),s[3]);
  }
  const mask=incident[v].reduce((a,e)=>a|(1n<<BigInt(e)),0n);
  byId.get(root).row={mask:'0x'+mask.toString(16),rhs:charges[v]};
  roots.push(root);
 }
 if(which==='comb')xor(xor(xor(roots[0],roots[1]),roots[2]),roots[3]);
 else xor(xor(roots[0],roots[1]),xor(roots[2],roots[3]));
 const f={graph:{n:V,edges},charges,clauses,proof,deleted,evenWitness:'000000',
  properties:{essential:clauses.length}};
 return {fixtures:[f],summary:[null]};
}
function originalReplay(p){
 let stdout='';
 // Executes the original checker body unchanged, with input-file and console adapters only.
 const body=new Function('require','process','console',checker);
 try{
  body(()=>({readFileSync:()=>JSON.stringify(p)}),
   {argv:['node',checkerPath,'packet.json']},{log:s=>{stdout=s}});
  const o=JSON.parse(stdout);
  return {accepted:true,checks:o.checks,proofNodes:o.cases[0].proofNodes};
 }catch(e){return {accepted:false,error:String(e)}}
}
function metrics(p){
 const nodes=p.fixtures[0].proof;
 const depth=new Map();
 for(const q of nodes)depth.set(q.id,1+Math.max(...q.parents.map(x=>depth.get(x)||0)));
 const index=new Map(nodes.map((q,i)=>[q.id,i]));
 const parents=nodes.map(q=>q.parents.filter(x=>index.has(x)).map(x=>index.get(x)));
 const children=nodes.map(()=>[]);
 parents.forEach((ps,i)=>ps.forEach(j=>children[j].push(i)));
 const n=nodes.length,full=(1<<n)-1;
 function search(cap,overwrite){
  let seen=new Uint8Array(1<<n),pending=[0],states=0;
  seen[0]=1;
  while(pending.length){
   const mask=pending.pop();states++;
   if(mask===full)return {yes:true,states};
   let live=0;
   for(let j=0;j<n;j++)
    if((mask>>j)&1 && children[j].some(k=>!((mask>>k)&1)))live++;
   for(let k=0;k<n;k++){
    if((mask>>k)&1 || parents[k].some(j=>!((mask>>j)&1)))continue;
    const reuse=overwrite&&parents[k].some(j=>
     children[j].every(c=>c===k||((mask>>c)&1)));
    if(live+1-Number(reuse)>cap)continue;
    const next=mask|(1<<k);
    if(!seen[next]){seen[next]=1;pending.push(next)}
   }
  }
  return {yes:false,states};
 }
 const registers={};
 for(const type of ['inplace','fresh']){
  let attempts=[];
  for(let cap=1;cap<=n;cap++){
   const result=search(cap,type==='inplace');
   attempts.push({cap,...result});
   if(result.yes){registers[type]={min:cap,attempts};break}
  }
 }
 const parentRefs=nodes.reduce((s,p)=>s+p.parents.length,0);
 return {span:depth.get(nodes[n-1].id),paid:15,parentRefs,
  bytes:JSON.stringify(p).length,registers};
}
const output={id:'LSPV4-587-K4-EXACT-SPAN-REGISTER',checkerPath,corpusPath,
 sourceCount:clauses.length,essentialWitnesses:deleted.filter(x=>x.assignment!==null).length,
 status:'PROVED/RESTRICTED typed local SOURCE/AND3/XOR tree; COMPUTATIONAL unchanged-checker V8 replay'};
for(const shape of ['comb','xor-balanced','fully-balanced']){
 const p=packet(shape);
 const original=originalReplay(p),meter=metrics(p);
 insist(original.accepted&&original.checks===1401,'original checker rejected '+shape+': '+JSON.stringify(original));
 insist(meter.paid===15&&meter.parentRefs===30,'paid/ref count mismatch');
 output[shape]={...meter,original};
}
const archived=JSON.parse(fs.readFileSync(corpusPath,'utf8')).minimal.packetBytes;
output.archivedCombByteIdentity=(JSON.stringify(packet('comb'))===archived);
insist(output.archivedCombByteIdentity,'reconstructed comb does not match original archived minimal.packetBytes');
output.hostile={};
const bad=[
 ['forged-parent',p=>{p.fixtures[0].proof[0].parents[0]='not-source'}],
 ['wrong-and-table',p=>{p.fixtures[0].proof[0].table^=1}],
 ['wrong-xor-mask',p=>{p.fixtures[0].proof.at(-1).row.mask='0x1'}],
 ['wrong-source',p=>{p.fixtures[0].clauses[0].literals[0]=999}],
 ['wrong-witness',p=>{const d=p.fixtures[0].deleted[0];d.assignment=(d.assignment[0]==='0'?'1':'0')+d.assignment.slice(1)}]
];
for(const [name,edit] of bad){
 const p=JSON.parse(JSON.stringify(packet('fully-balanced')));edit(p);
 const result=originalReplay(p);
 insist(!result.accepted,'hostile accepted: '+name);
 output.hostile[name]=result;
}
if(process.argv.includes('--os')){
 const cp=require('child_process'),os=require('os'),path=require('path');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-587-'));
 try{
  output.osReplay={};
  for(const shape of ['comb','xor-balanced','fully-balanced']){
   const file=path.join(dir,shape+'.json');
   fs.writeFileSync(file,JSON.stringify(packet(shape)));
   const ret=JSON.parse(cp.execFileSync(process.execPath,[checkerPath,file],{encoding:'utf8',timeout:20000}));
   insist(ret.checks===1401,'OS verifier mismatch '+shape);
   output.osReplay[shape]={accepted:true,checks:ret.checks};
  }
 }finally{fs.rmSync(dir,{recursive:true,force:true})}
}
console.log(JSON.stringify(output,null,2));

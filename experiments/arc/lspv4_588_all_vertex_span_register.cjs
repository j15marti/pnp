'use strict';
// LSPV-4/588, typed SOURCE/AND3/XOR resource Pareto audit. Archived /341 only.
// Run: node experiments/arc/lspv4_588_all_vertex_span_register.cjs [--os]
const fs=require('fs');
const sourceFile='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const checkerFile='experiments/arc/lspv2_341_independent_verify.js';
const data=JSON.parse(fs.readFileSync(sourceFile,'utf8'));
const checker=fs.readFileSync(checkerFile,'utf8');
const assert=(b,s)=>{if(!b)throw Error('LSPV4/588 '+s)};
function frontier(N){
 const dp=[null,[{d:3,r:1,t:['row',0]},{d:2,r:2,t:['row',1]}]];
 for(let n=2;n<=N;n++){
  const all=[];
  for(let k=1;k<n;k++)for(const a of dp[k])for(const b of dp[n-k])
   all.push({d:Math.max(a.d,b.d)+1,r:Math.max(a.r,b.r)+(a.r===b.r),t:['join',a.t,b.t]});
  dp[n]=all.filter(a=>!all.some(b=>b.d<=a.d&&b.r<=a.r&&(b.d<a.d||b.r<a.r)))
         .filter((a,i,z)=>z.findIndex(x=>x.d===a.d&&x.r===a.r)===i)
         .sort((a,b)=>b.d-a.d||a.r-b.r);
 }
 return dp;
}
const dp=frontier(Math.max(...data.fixtures.map(f=>f.graph.n)));
function make(f,t){
 const f0=JSON.parse(JSON.stringify(f)),V=f0.graph.n,E=f0.graph.edges.length;
 const incid=Array.from({length:V},()=>[]);
 f0.graph.edges.forEach(([a,b],e)=>{incid[a].push(e);incid[b].push(e)});
 const sources=Array.from({length:V},()=>[]),byId=new Map(),proof=[];
 const sat=(c,b)=>c.literals.some(x=>x>0?b[x-1]===1:b[-x-1]===0);
 for(const c of f0.clauses){
  sources[c.vertex].push(c.id);let table=0;
  for(let m=0;m<8;m++){
   const bits=Array(E).fill(0);
   incid[c.vertex].forEach((e,j)=>bits[e]=(m>>j)&1);
   if(sat(c,bits))table|=(1<<m);
  }
  byId.set(c.id,{kind:'factor',support:incid[c.vertex].slice(),table});
 }
 function conj(aid,bid){
  const a=byId.get(aid),b=byId.get(bid),support=[...new Set([...a.support,...b.support])];
  assert(support.length<=3,'nonlocal AND3');
  let table=0;
  for(let m=0;m<(1<<support.length);m++){
   const bits=Array(E).fill(0);support.forEach((e,i)=>bits[e]=(m>>i)&1);
   const v=x=>x.support.reduce((z,e,i)=>z|(bits[e]<<i),0);
   if(((a.table>>v(a))&1)&&((b.table>>v(b))&1))table|=1<<m;
  }
  const p={id:'d'+proof.length,rule:'AND3',kind:'factor',parents:[aid,bid],support,table};
  proof.push(p);byId.set(p.id,p);return p.id;
 }
 function xor(aid,bid){
  const a=byId.get(aid),b=byId.get(bid);
  assert(a.row&&b.row,'GF2 row missing');
  const p={id:'d'+proof.length,rule:'XOR',kind:'affine',parents:[aid,bid],
    row:{mask:'0x'+(BigInt(a.row.mask)^BigInt(b.row.mask)).toString(16),rhs:a.row.rhs^b.row.rhs}};
  proof.push(p);byId.set(p.id,p);return p.id;
 }
 let v=0;
 function build(t){
  if(t[0]==='row'){
   const i=v++,s=sources[i];assert(s.length===4,'SOURCE quartet');
   const id=t[1]===1?conj(conj(s[0],s[1]),conj(s[2],s[3]))
                      :conj(conj(conj(s[0],s[1]),s[2]),s[3]);
   byId.get(id).row={mask:'0x'+incid[i].reduce((m,e)=>m|(1n<<BigInt(e)),0n).toString(16),rhs:f0.charges[i]};
   return id;
  }
  return xor(build(t[1]),build(t[2]));
 }
 const last=build(t);assert(v===V&&BigInt(byId.get(last).row.mask)===0n&&byId.get(last).row.rhs===1,'final parity');
 f0.proof=proof;
 const d=new Map(),r=new Map();
 f0.clauses.forEach(c=>{d.set(c.id,0);r.set(c.id,0)});
 for(const p of proof){
  let [a,b]=p.parents,[ra,rb]=[r.get(a),r.get(b)];
  d.set(p.id,1+Math.max(d.get(a),d.get(b)));
  r.set(p.id,Math.max(ra,rb)+Number(ra===rb));
 }
 const packet={fixtures:[f0],summary:[null]};
 return {packet,measure:{span:d.get(last),registers:r.get(last),paid:proof.length,
      references:2*proof.length,compactBytes:Buffer.byteLength(JSON.stringify(packet),'utf8')}};
}
function replay(p){
 let output='';
 const main=new Function('require','process','console',checker);
 try{
  main(()=>({readFileSync:()=>JSON.stringify(p)}),
   {argv:['node',checkerFile,'fixture.json']},{log:s=>output+=s});
  return {accepted:true,assertions:JSON.parse(output).checks};
 }catch(e){return {accepted:false,error:String(e)}}
}
const raw={id:'LSPV4-588',scope:'restricted typed local quartet AND3/GF2 trees; source-readonly atomic in-place last-use; no recomputation; not R_mix341',
  checkerBlob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  corpusBlob:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
  fixtureResults:[],hostiles:{},positives:0,negatives:0};
let control;
for(const f of data.fixtures){
 const pts=[];
 for(const q of dp[f.graph.n]){
  const made=make(f,q.t),m=made.measure;
  assert(m.span===q.d&&m.registers===q.r&&m.paid===4*f.graph.n-1&&m.references===8*f.graph.n-2,'resource count');
  const v=replay(made.packet);assert(v.accepted,'native checker REJECT '+f.graph.name+' '+q.d+','+q.r+': '+v.error);
  pts.push({...m,nativeAssertions:v.assertions});raw.positives++;
  if(f.graph.name==='K33'&&q.r===3)control=made.packet;
 }
 raw.fixtureResults.push({name:f.graph.name,V:f.graph.n,E:f.graph.edges.length,
    sourceCount:f.clauses.length,essential:f.properties.essential,frontier:pts});
}
const hostiles={
 forgedParent:p=>{p.fixtures[0].proof[0].parents[0]='not-a-source'},
 falseAND3:p=>{p.fixtures[0].proof[0].table^=1},
 falseSink:p=>{p.fixtures[0].proof.at(-1).row.rhs^=1},
 falseSource:p=>{p.fixtures[0].clauses[0].literals[0]=999},
 falseWitness:p=>{const d=p.fixtures[0].deleted[0];d.assignment=(d.assignment[0]==='0'?'1':'0')+d.assignment.slice(1)}
};
for(const [name,edit] of Object.entries(hostiles)){
 const p=JSON.parse(JSON.stringify(control));edit(p);
 const v=replay(p);assert(!v.accepted,'hostile ACCEPT '+name);
 raw.hostiles[name]=v.error;raw.negatives++;
}
if(process.argv.includes('--os')){
 const cp=require('child_process'),os=require('os'),path=require('path');
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-588-'));raw.os=[];
 try{
  for(const f of data.fixtures)for(const q of dp[f.graph.n]){
   const pkt=make(f,q.t).packet;
   const file=path.join(tmp,f.graph.name+'-'+q.d+'-'+q.r+'.json');
   fs.writeFileSync(file,JSON.stringify(pkt));
   const check=JSON.parse(cp.execFileSync(process.execPath,[checkerFile,file],{encoding:'utf8',timeout:90000}));
   assert(check.cases.length===1,'OS case count');
   raw.os.push({fixture:f.graph.name,span:q.d,registers:q.r,assertions:check.checks});
  }
 }finally{fs.rmSync(tmp,{recursive:true,force:true})}
}
console.log(JSON.stringify(raw,null,2));

#!/usr/bin/env node
'use strict';
/* LSPV-2/594. Complete reproduction of the separately DECLARED certified
 * obligation-cover reference model. NOT a historical R_mix341 verifier.
 * Optional original /386 regression: node thisfile checker.js W29.json W32.json ...
 * No external dependencies. All paid identities are charged globally once. */
const assert=require('node:assert/strict');
const crypto=require('node:crypto'),fs=require('node:fs'),path=require('node:path');
const {spawnSync}=require('node:child_process');
let assertions=0;
function ok(test,msg){assertions++;assert.ok(test,msg)}
const EPS=1e-7;
function popcount(n){let k=0;while(n){n&=n-1;k++}return k}
function* choose(a,k,start=0,p=[]){
 if(p.length===k){yield p.slice();return}
 for(let i=start;i<=a.length-(k-p.length);i++){
  p.push(a[i]);yield* choose(a,k,i+1,p);p.pop()
 }
}
function solve(A,b){
 const n=b.length,M=A.map((row,i)=>[...row,b[i]]);
 for(let col=0;col<n;col++){
  let p=col;for(let j=col+1;j<n;j++)
   if(Math.abs(M[j][col])>Math.abs(M[p][col]))p=j;
  if(Math.abs(M[p][col])<1e-9)return null;
  [M[p],M[col]]=[M[col],M[p]];
  const t=M[col][col];for(let j=col;j<=n;j++)M[col][j]/=t;
  for(let i=0;i<n;i++)if(i!==col){
   const v=M[i][col];for(let j=col;j<=n;j++)M[i][j]-=v*M[col][j]
  }
 }
 return M.map(row=>row[n]);
}
function state(ins,D){
 const cover=ins.owners.reduce((m,o,i)=>D&(1<<i)?m|o.cover:m,0);
 const uncovered=ins.U.filter(j=>!(cover&(1<<j)));
 const unpaid=ins.owners.map((o,i)=>({...o,index:i}))
   .filter(o=>!(D&(1<<o.index)));
 return {cover,uncovered,unpaid};
}
function residualLP(ins,D){
 const {uncovered,unpaid}=state(ins,D),m=uncovered.length;
 if(m===0)return {value:0,dual:[],uncovered:[]};
 const rows=unpaid.map(o=>({a:uncovered.map(u=>+(!!(o.cover&(1<<u)))),b:o.w}));
 for(let j=0;j<m;j++)rows.push({a:uncovered.map((_,i)=>-(+(i===j))),b:0});
 let best=-Infinity,dual=null,vertices=0;
 for(const active of choose(rows.map((_,i)=>i),m)){
  const x=solve(active.map(i=>rows[i].a),active.map(i=>rows[i].b));
  if(!x||x.some(v=>v<-EPS))continue;
  if(rows.some(row=>row.a.reduce((s,a,j)=>s+a*x[j],0)>row.b+EPS))continue;
  vertices++;const value=x.reduce((s,v)=>s+v,0);
  if(value>best){best=value;dual=x.slice()}
 }
 ok(best>-Infinity,'dual LP infeasible despite full cover');
 return {value:best,dual,uncovered,vertices};
}
function integerOpt(ins,D){
 const unpaid=ins.owners.map((_,i)=>i).filter(i=>!(D&(1<<i)));
 let best=Infinity,choice=null;
 for(let t=0;t<(1<<unpaid.length);t++){
  let mask=D,w=0;
  for(let i=0;i<unpaid.length;i++)if(t&(1<<i)){
   mask|=1<<unpaid[i];w+=ins.owners[unpaid[i]].w
  }
  const cover=ins.owners.reduce((m,o,i)=>mask&(1<<i)?m|o.cover:m,0);
  if(cover===((1<<ins.U.length)-1)&&w<best){best=w;choice=mask}
 }
 ok(Number.isFinite(best),'uncoverable instance');
 return {value:best,mask:choice};
}
function fixedDual(ins){
 const y=ins.U.map(u=>Math.min(...ins.owners
   .filter(o=>o.cover&(1<<u)).map(o=>o.w/popcount(o.cover))));
 for(const o of ins.owners)
  ok(ins.U.reduce((s,u)=>s+(o.cover&(1<<u)?y[u]:0),0)<=o.w+EPS,'fixed dual infeasible');
 return y;
}
function runInstance(ins){
 const fixed=fixedDual(ins),r=ins.owners.length,record=[];let checkedEdges=0;
 for(let D=0;D<(1<<r);D++){
  const p=residualLP(ins,D),integer=integerOpt(ins,D);
  const f=p.uncovered.reduce((s,u)=>s+fixed[u],0);
  ok(p.value<=integer.value+EPS,'LP above integer optimum '+D);
  ok(p.value+EPS>=f,'residual dual below fixed dual '+D);
  for(let A=0;A<(1<<r);A++){
   if(!(A&~D))continue;
   const next=residualLP(ins,D|A);
   let w=0;
   for(let i=0;i<r;i++)if((A&~D)&(1<<i))w+=ins.owners[i].w;
   ok(p.value<=w+next.value+EPS,'failed Bellman marginal payment '+D+','+A);
   checkedEdges++;
  }
  record.push({paidMask:D,h:p.value,integer:integer.value,fixed:f,uncovered:p.uncovered})
 }
 return {states:1<<r,edges:checkedEdges,seed:record[0],
  maxDominance:Math.max(...record.map(x=>x.h-x.fixed))};
}
function rng(seed){
 let x=seed>>>0;
 return()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296}
}
function fixture(m,r,random){
 const owners=[];
 for(let i=0;i<r;i++){
  let cover=0;
  for(let j=0;j<m;j++)if(random()<.52)cover|=1<<j;
  owners.push({cover,w:1+Math.floor(random()*3)})
 }
 for(let j=0;j<m;j++)
  if(!owners.some(o=>o.cover&(1<<j)))
   owners[Math.floor(random()*r)].cover|=1<<j;
 return {U:Array.from({length:m},(_,i)=>i),owners};
}
const seed=0x5945a7,random=rng(seed);
const triangle={U:[0,1,2],owners:[
 {cover:0b011,w:1},{cover:0b110,w:1},{cover:0b101,w:1}]};
const tri=runInstance(triangle);
ok(Math.abs(tri.seed.h-1.5)<EPS,'fractional triangle');
ok(tri.seed.integer===2,'integer triangle');
ok(tri.maxDominance>=.49,'strict dual dominance');
let validTriangleCovers=0;
for(let t=0;t<8;t++){
 const cover=triangle.owners.reduce((m,o,i)=>t&(1<<i)?m|o.cover:m,0);
 if(cover===7){
  validTriangleCovers++;ok(popcount(t)>=2,'invalid CEGAR rank cut')
 }
}
ok(validTriangleCovers===4,'triangle cover count');
const triangleWithUnknownFree={U:[0,1,2],
 owners:[...triangle.owners,{cover:7,w:0}]};
const triangleFreeRes=runInstance(triangleWithUnknownFree);
ok(triangleFreeRes.seed.h===0,'missing free shortcut');
const free={U:[0,1],owners:[{cover:1,w:1},{cover:2,w:1},{cover:3,w:0}]};
const freeRes=runInstance(free);
ok(Math.abs(freeRes.seed.h)<EPS,'free owner');
const share={U:[0,1,2,3],owners:[
 {cover:15,w:1},{cover:1,w:1},{cover:2,w:1},
 {cover:4,w:1},{cover:8,w:1}]};
const shareRes=runInstance(share);
ok(Math.abs(shareRes.seed.h-1)<EPS,'shared once-paid owner');
const cases=[];
for(let k=0;k<56;k++){
 const m=2+(k%4),r=2+(Math.floor(k/4)%4);
 cases.push({i:k,m,r,...runInstance(fixture(m,r,random))})
}
const native={mode:'not run',tests:[]};
const [checker,...packets]=process.argv.slice(2);
if(checker&&packets.length){
 native.mode='original native /386 unchanged OS CLI';
 for(const p of packets){
  const res=spawnSync(process.execPath,[checker,p],{encoding:'utf8',maxBuffer:4e6});
  ok(res.status===0,'original native checker rejected '+p+': '+res.stderr);
  const parsed=JSON.parse(res.stdout);
  native.tests.push({case:path.basename(p),accepted:true,paid:parsed.paid,
   assertions:parsed.assertions,negativeTests:parsed.negativeTests,
   sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')});
  const data=JSON.parse(fs.readFileSync(p,'utf8'));
  data.records[data.records.length-1].pivot=999999;
  const bad=p+'.594hostile.tmp';
  try{
   fs.writeFileSync(bad,JSON.stringify(data));
   const neg=spawnSync(process.execPath,[checker,bad],{encoding:'utf8'});
   ok(neg.status!==0,'original checker accepted corrupted signed pivot');
   native.tests.push({case:path.basename(p)+':corrupt_pivot',accepted:false})
  }finally{if(fs.existsSync(bad))fs.unlinkSync(bad)}
 }
}
const raw={run:'LSPV2-594-RESIDUAL-REOPTIMIZED-COVER/v1',
 local_time:'2026-11-13 01:12 PST',seed,
 scope:'certified fixed monotone cover ONLY, not historical R_mix341',
 algorithm:'exhaustive dual basic vertices, integer covers, paid masks and acquisition masks',
 claims:{triangle_fractional:tri.seed.h,triangle_integer:tri.seed.integer,
  triangle_reoptimized_dominance:tri.maxDominance,
  triangle_integer_covers:validTriangleCovers,
  cegar_rank_cut_lower_bound:2,unknown_free_shortcut_floor:triangleFreeRes.seed.h,
  free_shortcut_floor:freeRes.seed.h,shared_owner_once:shareRes.seed.h},
 cases,caseCount:cases.length,
 states:cases.reduce((s,c)=>s+c.states,0),
 edges:cases.reduce((s,c)=>s+c.edges,0),native,assertions,
 limitation:'P2-D1/P2-C3/P2-B1/P2-B2/P2-B3 OPEN; P versus NP OPEN'};
const out=JSON.stringify(raw,null,2)+'\n';
if(process.env.LSPV2_RAW_OUT)fs.writeFileSync(process.env.LSPV2_RAW_OUT,out);
console.log(JSON.stringify({run:raw.run,claims:raw.claims,caseCount:raw.caseCount,
 states:raw.states,edges:raw.edges,native,assertions,
 sha256:crypto.createHash('sha256').update(out).digest('hex')}));

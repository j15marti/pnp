'use strict';
// LSPV-2/491 finite model control. This executable proves no asymptotic theorem.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const bits=x=>{let k=0;for(;x;x&=x-1)k++;return k};
const gs={
K4:{n:4,e:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]},
prism:{n:6,e:[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]},
cube:{n:8,e:Array.from({length:8},(_,i)=>Array.from({length:7-i},(_,j)=>[i,i+j+1])).flat().filter(([a,b])=>bits(a^b)===1)},
Petersen:{n:10,e:[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,i+5]),...Array.from({length:5},(_,i)=>[i+5,5+(i+2)%5])]}
};
function cc(n,edges,mask){
 let seen=0,cnt=0;
 for(let s=0;s<n;s++)if(!(seen&(1<<s))){
  cnt++;let todo=[s];seen|=1<<s;
  while(todo.length){
   const u=todo.pop();
   for(let i=0;i<edges.length;i++)if(mask&(1<<i)){
    let [a,b]=edges[i],v=a===u?b:b===u?a:-1;
    if(v>=0&&!(seen&(1<<v))){seen|=1<<v;todo.push(v)}
   }
  }
 }
 return cnt;
}
function cnf(n,edges,charge){
 const out=[];
 for(let v=0;v<n;v++){
  let id=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0).sort((a,b)=>a-b);
  assert.equal(id.length,3);
  for(let p=0;p<2;p++)for(let q=0;q<2;q++){
   const r=p^q^1^charge[v];
   out.push(id.map((i,j)=>([p,q,r][j]?-1:1)*(i+1)));
  }
 }
 return out;
}
const evalCNF=(f,x)=>f.every(c=>c.some(z=>!!(x&(1<<(Math.abs(z)-1)))===(z>0)));
function validPacket(n,e,f){
 if(f.length!==4*n)return false;
 for(let v=0;v<n;v++){
  const current=f.slice(4*v,4*v+4).map(c=>c.join(',')).sort().join('|');
  let matches=0;
  for(let b=0;b<2;b++){
   const charges=Array(n).fill(0);charges[v]=b;
   if(cnf(n,e,charges).slice(4*v,4*v+4).map(c=>c.join(',')).sort().join('|')===current)matches++;
  }
  if(matches!==1)return false;
 }
 return true;
}
function proj(x,mask,m){
 let out=0,pos=0;
 for(let i=0;i<m;i++)if(mask&(1<<i)){
  if(x&(1<<i))out|=1<<pos;
  pos++;
 }
 return out;
}
function distinctResiduals(solutions,cut,m){
 const groups=new Map(),opposite=((1<<m)-1)^cut;
 for(const x of solutions){
  const k=proj(x,cut,m),z=proj(x,opposite,m);
  if(!groups.has(k))groups.set(k,new Set());
  groups.get(k).add(z);
 }
 return new Set([...groups.values()].map(s=>[...s].sort((a,b)=>a-b).join(','))).size;
}
let checks=0;let details=[];
for(const [name,{n,e}] of Object.entries(gs)){
 const m=e.length,full=(1<<m)-1;
 assert.equal(2*m,3*n);checks++;
 assert.equal(cc(n,e,full),1);checks++;
 const even=Array(n).fill(0),odd=even.slice();odd[0]=1;
 const f=cnf(n,e,even),g=cnf(n,e,odd);
 assert.equal(f.length,4*n);checks++;
 assert.ok(validPacket(n,e,f));assert.ok(validPacket(n,e,g));checks+=2;
 let mutant=f.map(c=>c.slice());mutant[0][0]*=-1;
 assert.equal(validPacket(n,e,mutant),false);checks++;
 assert.equal(validPacket(n,e,f.slice(1)),false);checks++;
 mutant=f.map(c=>c.slice());mutant[0]=mutant[1].slice();
 assert.equal(validPacket(n,e,mutant),false);checks++;
 const solutions=[];
 for(let assignment=0;assignment<(1<<m);assignment++){
  if(evalCNF(f,assignment))solutions.push(assignment);
  assert.equal(evalCNF(g,assignment),false);checks++;
 }
 assert.equal(solutions.length,2**(m-n+1));checks++;
 const val=new Uint16Array(1<<m),dp=new Uint16Array(1<<m).fill(m+1),parent=new Int16Array(1<<m).fill(-1);
 dp[0]=0;
 for(let subset=0;subset<(1<<m);subset++){
  val[subset]=n-cc(n,e,subset)-cc(n,e,full^subset)+1;
  assert.ok(val[subset]>=0);checks++;
 }
 for(let subset=1;subset<(1<<m);subset++){
  for(let i=0;i<m;i++)if(subset&(1<<i)){
   const peak=Math.max(dp[subset^(1<<i)],val[subset]);
   if(peak<dp[subset]){dp[subset]=peak;parent[subset]=i}
  }
 }
 let mask=full,order=[];
 while(mask){
  const i=parent[mask];assert.ok(i>=0);checks++;
  order.push(i);mask^=1<<i;
 }
 order.reverse();mask=0;
 const cuts=new Set([0,full]);
 for(const i of order){mask|=1<<i;cuts.add(mask)}
 for(const cut of cuts){
  assert.equal(distinctResiduals(solutions,cut,m),2**val[cut]);checks++;
 }
 assert.equal(2**dp[full],({K4:4,prism:4,cube:8,Petersen:16})[name]);checks++;
 for(const edge of e){assert.equal(edge.length,2);checks++}
 details.push({graph:name,H:n,M:m,clauses:f.length,component_width:dp[full],one_nbp_min_nodes_at_least:2**dp[full],even_sat_assignments:solutions.length,odd_sat_assignments:0,checked_prefix_cutsets:cuts.size});
}
const out={run:'LSPV-2/491',status:'PASS',assertions:checks,details,native_FLMV:'NOT EXECUTED',historical_R_mix341:'NOT EXECUTED'};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));

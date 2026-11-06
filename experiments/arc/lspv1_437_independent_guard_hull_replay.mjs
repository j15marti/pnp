#!/usr/bin/env node
// LSPV-1/437: independent finite semantic audit, NOT an R_mix341 checker.
import assert from 'node:assert/strict';
let checks=0; const ok=(x,msg)=>{checks++;assert.ok(x,msg)};
const cc=(a)=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function graph(name){
 if(name==='K4')return [...Array(4).keys()].flatMap(i=>[...Array(4).keys()].filter(j=>i<j).map(j=>[i,j]));
 if(name==='K33')return [...Array(3).keys()].flatMap(i=>[3,4,5].map(j=>[i,j]));
 if(name==='cube')return [...Array(8).keys()].flatMap(i=>[1,2,4].filter(b=>i<(i^b)).map(b=>[i,i^b]));
 throw Error('graph');
}
function tseitin(edges,odd=true){
 let h=1+Math.max(...edges.flat()),adj=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{adj[u].push(i+1);adj[v].push(i+1)});
 let F=[];
 for(let v=0;v<h;v++)for(let mask=0;mask<8;mask++){
  let bits=[0,1,2].map(j=>(mask>>j)&1);
  if((bits[0]^bits[1]^bits[2]) === (odd && v===0?1:0))continue;
  F.push(cc(adj[v].map((e,j)=>bits[j]?-e:e)));
 }
 return F;
}
function easy(h){
 const n=3*h/2,m=4*h,F=tseitin(graph('K4'));
 for(let j=7;j<=n;j++)F.push([1,2,j]);
 for(let a=1;a<=n;a++)for(let b=a+1;b<=n;b++)for(let c=b+1;c<=n;c++)
 for(let mask=0;mask<8;mask++){
  if(F.length===m)break;
  const C=cc([a*(mask&1?-1:1),b*(mask&2?-1:1),c*(mask&4?-1:1)]);
  if(!F.some(old=>JSON.stringify(old)===JSON.stringify(C)))F.push(C);
 }
 ok(F.length===m,'easy-size');return F;
}
function guards(F,n){let g=n+1,G=[];
 F.forEach(([a,b,c],i)=>{let y=n+2+i;G.push(cc([g,a,y]),cc([-y,b,c]))});
 return {G,g};
}
function sat(C,model){return C.some(l=>model[Math.abs(l)]===(l>0?1:0))}
function holds(F,model){return F.every(C=>sat(C,model))}
function witnessTest(F,n){
 const {G,g}=guards(F,n),model=Array(n+F.length+2).fill(0);model[g]=1;
 ok(holds(G,model),'base g=1 model');
 for(let j=1;j<=n;j++){let a=model.slice();a[j]=1;ok(holds(G,a),'free x coordinate')}
 for(let i=0;i<F.length;i++){
  let a=model.slice(),b=F[i][1];a[Math.abs(b)]=b>0?1:0;
  ok(holds(G,a),'y-zero supporting model');a[n+2+i]=1;
  ok(holds(G,a),'free y coordinate');
 }
 return n+F.length;
}
function brute(F,n){
 for(let bits=0;bits<(1<<n);bits++){
  let a=Array(n+1).fill(0);for(let i=1;i<=n;i++)a[i]=(bits>>(i-1))&1;
  if(holds(F,a))return a;
 }return null;
}
let out=[];
for(const name of ['K4','K33','cube']){
 const E=graph(name),h=1+Math.max(...E.flat()),n=E.length;
 const hard=tseitin(E),simple=easy(h),{G:HG}=guards(hard,n),{G:EG}=guards(simple,n);
 ok(hard.length===4*h && simple.length===4*h,'source count');
 ok(HG.length===8*h&&EG.length===8*h,'guard count');
 ok(HG.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'proper hard');
 ok(EG.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'proper easy');
 ok(brute(hard,n)===null&&brute(simple,n)===null,'both sources UNSAT');
 const rankH=witnessTest(hard,n),rankE=witnessTest(simple,n);
 ok(rankH===rankE,'same affine dimension');
 out.push({graph:name,vertices:h,original_variables:n,original_clauses:hard.length,guarded_clauses:HG.length,affine_rank:rankH});
}
const even=tseitin(graph('K4'),false);ok(brute(even,6)!==null,'even charge SAT control');
let malformedCaught=false;try{graph('not-a-graph')}catch(e){malformedCaught=true};
ok(malformedCaught,'bad graph rejected');
console.log(JSON.stringify({status:'COMPUTATIONAL scoped semantic replay',assertions:checks,cases:out,negative:'unknown graph rejected'},null,2));

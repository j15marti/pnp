#!/usr/bin/env node
// Independent Node.js referee for LSPV-4 338. No production-code imports.
const assert=require('assert');
const P=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]];
const N=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]];
const Z=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];
function formula(p,n){return p.concat(n.map(c=>c.map(v=>-v)));}
function good(F,n){
 if(!Number.isInteger(n)||n%3||!Array.isArray(F)||F.length!==4*n/3)return false;
 const counts=new Map(),seen=new Set();
 for(let c of F){
  if(!Array.isArray(c)||c.length!==3||c.some(x=>!Number.isInteger(x)||!x||Math.abs(x)>n))return false;
  if(new Set(c.map(Math.abs)).size!==3||!(c.every(x=>x>0)||c.every(x=>x<0)))return false;
  let k=[...c].sort((a,b)=>a-b).join(',');
  if(seen.has(k))return false;seen.add(k);
  for(let x of c)counts.set(x,(counts.get(x)||0)+1);
 }
 for(let x=1;x<=n;x++)if(counts.get(x)!==2||counts.get(-x)!==2)return false;
 return true;
}
function trueLit(x,a){let b=!!(a&(1<<(Math.abs(x)-1)));return x>0?b:!b;}
function count(c,a){return c.reduce((t,x)=>t+Number(trueLit(x,a)),0);}
function ok(F,a){return F.every(c=>count(c,a)>0);}
function run(F,n){
 assert(good(F,n));
 const m=F.length,ports=Array(3*m).fill(0),hist={},models=[];
 for(let a=0;a<1<<n;a++){
  if(!ok(F,a))continue;models.push(a);
  const t=F.map(c=>count(c,a));
  assert.strictEqual(t.reduce((x,y)=>x+y,0),2*n);
  const N1=t.filter(x=>x===1).length,N2=t.filter(x=>x===2).length,N3=t.filter(x=>x===3).length;
  assert.strictEqual(N2+2*N3,m/2);
  const key=[N1,N2,N3].join(',');
  hist[key]=(hist[key]||0)+1;
  F.forEach((c,j)=>c.forEach((v,k)=>{
   if(trueLit(v,a)&&c.some((w,l)=>k!==l&&trueLit(w,a)))ports[3*j+k]++;
  }));
 }
 const total=ports.reduce((a,b)=>a+b,0);
 let predicted=0;for(let [key,mult] of Object.entries(hist))predicted+=(m-Number(key.split(',')[2]))*mult;
 assert.strictEqual(total,predicted);
 if(models.length){assert(total>=n*models.length);assert(ports.filter(x=>x>0).length>=n);}
 return {models:models.length,positive:ports.filter(x=>x>0).length,
         min:Math.min(...ports),max:Math.max(...ports),sum:total,hist};
}
let F=formula(P,N),G=formula(Z,Z);
let result={F9:run(F,9),Z6:run(G,6)};
assert.deepStrictEqual([result.F9.models,result.F9.positive,result.F9.min,result.F9.sum],[70,36,13,781]);
assert.deepStrictEqual([result.Z6.models,result.Z6.positive,result.Z6.min,result.Z6.sum],[18,24,6,144]);
const pin={2:0,4:0,6:0},siblings={};
for(let x1 of [0,1]){
 let count=0,immediate=false;
 for(let a=0;a<512;a++)if((a&1)===x1&&Object.entries(pin).every(([v,b])=>Number(!!(a&(1<<(v-1))))===b)&&ok(F,a))count++;
 const pins={...pin,1:x1};
 immediate=F.some(c=>c.every(x=>pins[Math.abs(x)]!==undefined&&Boolean(pins[Math.abs(x)])!==(x>0)));
 assert(!immediate); siblings[x1]=count;
}
assert.deepStrictEqual(siblings,{'0':0,'1':3});
const malformed=[F.concat([F[0]]),F.map((c,j)=>j===0?[1,1,6]:c),
 F.map((c,j)=>j===0?[1,-5,6]:c),F.map((c,j)=>j===0?[0,5,6]:c),
 F.map((c,j)=>j===0?[10,5,6]:c),F.map((c,j)=>j===0?[1.5,5,6]:c)];
malformed.forEach(x=>assert(!good(x,9)));
result.same_original_F9_x1_models=siblings;result.malformed_rejected=malformed.length;
console.log(JSON.stringify(result,null,2));

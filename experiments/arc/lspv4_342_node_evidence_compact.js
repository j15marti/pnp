// LSPV-4 342 compact independent reference checks. node >=18; no external dependencies.
'use strict';
const assert=require('assert');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const SAT=(clause,mask)=>clause.some(l=>Boolean((mask>>(Math.abs(l)-1))&1)===(l>0));
function k4(charges){let clauses=[];for(let v=0;v<4;v++){let vars=edges.map((e,i)=>e.includes(v)?i+1:null).filter(Boolean);for(let bits=0;bits<8;bits++){const parity=((bits>>0)&1)^((bits>>1)&1)^((bits>>2)&1);if(parity===charges[v])continue;clauses.push(vars.map((x,k)=>((bits>>k)&1)?-x:x));}}return clauses;}
function models(n,cs){let count=0;for(let a=0;a<(1<<n);a++)if(cs.every(c=>SAT(c,a)))count++;return count;}
function table(n,cs){let p=[];for(let a=0;a<(1<<n);a++){let k=cs.findIndex(c=>!SAT(c,a));if(k===-1)return null;p.push(k+1);}return p;}
function checkTable(n,cs,p){return Array.isArray(p)&&p.length===(1<<n)&&p.every((k,a)=>Number.isInteger(k)&&k>0&&k<=cs.length&&!SAT(cs[k-1],a));}
let checks=0;
function test(n,cs,expectedModels,expectedBits){let sat=models(n,cs);assert.strictEqual(sat,expectedModels);let p=table(n,cs);assert.strictEqual(p===null,sat>0);if(p){assert(checkTable(n,cs,p));assert.strictEqual((1<<n)*Math.ceil(Math.log2(cs.length+1)),expectedBits);let bad=[...p];bad[0]=cs.findIndex(c=>SAT(c,0))+1;assert(!checkTable(n,cs,bad));}checks++;return {n,m:cs.length,models:sat,tableau_bits:expectedBits};}
const odd=k4([1,0,0,0]),even=k4([0,0,0,0]);assert(odd.length===16&&even.length===16);
const cases=[
test(1,[[1],[-1]],0,4),
test(2,[[1,2],[1,-2],[-1,2],[-1,-2]],0,12),
test(2,[[1],[-1,2],[-2]],0,8),
test(2,[[1,2],[-1,2]],2,null),
test(3,Array.from({length:8},(_,a)=>[1,2,3].map((v,k)=>(a>>k)&1?-v:v)),0,32),
test(6,odd,0,320),test(6,even,8,null),
...([8,12,16].map(n=>test(n,[[1],[-1],...Array.from({length:n-1},(_,i)=>[i+2,-(i+2)])],0,(1<<n)*Math.ceil(Math.log2(n+2))))];
for(let i=0;i<16;i++){assert(models(6,odd.filter((_,j)=>i!==j))>0);checks++;}
console.log(JSON.stringify({run:'LSPV4_342',checks,source_deletions:16,cases},null,2));
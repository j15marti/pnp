#!/usr/bin/env node
// LSPV-2/446 self-contained finite original-source and state-count reproduction.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
let checks=0;
function ok(a,b){assert.deepEqual(a,b);checks++;}
function combos(n,r){let out=[];function go(i,s){if(s.length===r){out.push([...s]);return;}if(i===n)return;go(i+1,[...s,i]);go(i+1,s);}go(0,[]);return out;}
function cases(){
 const k4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)k4.push([i,j]);
 const cube=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if((i^j).toString(2).replaceAll('0','').length===1)cube.push([i,j]);
 const p=[];for(let i=0;i<5;i++){p.push([i,(i+1)%5]);p.push([i,i+5]);p.push([i+5,((i+2)%5)+5]);}
 return [['K4',4,k4],['Cube',8,cube],['Petersen',10,p]];
}
let summary={};
for(const [name,H,raw] of cases()){
 const edges=[...new Set(raw.map(x=>x.sort((a,b)=>a-b).join(':')))].map(s=>s.split(':').map(Number)).sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
 const M=edges.length, w=M.toString(2).length,r=H/2;
 ok(M,3*H/2);
 const inc=Array.from({length:H},(_,v)=>edges.flatMap((e,i)=>e.includes(v)?[i+1]:[]));
 ok(inc.every(a=>a.length===3),true);
 let sourceCount=0;const masks=new Set();let satCount=0;
 for(let base=0;base<=1;base++)for(const subset of combos(H,r)){
   const toggles=Array(H).fill(0);for(const v of subset.toReversed())toggles[v]^=1;
   const charge=toggles.map((x,v)=>x^(v===0?base:0));
   const clauses=[];
   for(let v=0;v<H;v++){const [a,b,c]=inc[v];for(let p=0;p<2;p++)for(let q=0;q<2;q++){
     const z=p^q^1^charge[v];clauses.push([[a,p],[b,q],[c,z]]);
   }}
   let bits='10100111'+'1'.repeat(H)+'0'+'1'.repeat(M)+'0';
   for(const [u,v] of edges)bits+=u.toString(2).padStart(w,'0')+v.toString(2).padStart(w,'0');
   for(const clause of clauses)for(const [id,sign] of clause)bits+=sign+id.toString(2).padStart(w,'0');
   bits+='00';
   ok(bits.length,8+(H+1)+(M+1)+2*M*w+12*H*(w+1)+2);
   ok(clauses.length,4*H);
   for(let v=0;v<H;v++)for(let mask=0;mask<8;mask++){
     const valid=clauses.slice(4*v,4*v+4).every(cl=>cl.some(([,sg],j)=>(((mask>>j)&1)^(sg===1))===1));
     ok(valid,(mask.toString(2).replaceAll('0','').length&1)===charge[v]);
   }
   ok((charge.reduce((a,b)=>a^b,0)===0),(base^(r&1))===0);
   if(base===0)masks.add(toggles.reduce((a,x,i)=>a|(x<<i),0));
   satCount+=Number(charge.reduce((a,b)=>a^b,0)===0);sourceCount++;
   ok(crypto.createHash('sha256').update(bits).digest('hex').length,64);
 }
 let exact=0;while(2**exact<masks.size)exact++;
 let choose=1;for(let i=1;i<=r;i++)choose=choose*(H-i+1)/i;
 ok(masks.size,Math.round(choose));
 summary[name]={H,encoded_bits:8+(H+1)+(M+1)+2*M*w+12*H*(w+1)+2,sourceCount,state_count:masks.size,exact_min_bits:exact,satCount};
}
console.log(JSON.stringify({pass:true,checks,summary},null,2));

'use strict';
// TMR-1/084 independently executable narrow certificate (COMPUTATIONAL).
const assert=require('node:assert/strict');
let checks=0;const eq=(a,b)=>{assert.deepEqual(a,b);checks++;};
const mod=x=>(x%5+5)%5, S=10, ALL=31;
const bits=m=>Array.from({length:5},(_,x)=>x).filter(x=>m>>x&1);
const mask=xs=>xs.reduce((m,x)=>m|(1<<mod(x)),0);
const neg=m=>mask(bits(m).map(x=>-x));
const comp=(a,b)=>mask(bits(a).flatMap(x=>bits(b).map(y=>x+y)));
function closure(n,arcs){
 const D=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?1:ALL));
 for(const [u,v] of arcs){D[u][v]&=S;D[v][u]&=neg(S);}
 if(D.some(row=>row.some(x=>!x)))return {ok:false,D};
 for(let round=0;round<=5*n*n+1;round++){
  let change=false;
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let k=0;k<n;k++){
   const v=D[i][j]&comp(D[i][k],D[k][j]);
   if(v!==D[i][j]){D[i][j]=v;change=true;if(!v)return {ok:false,D};}
  }
  if(!change)return {ok:true,D};
 }
 throw Error('nontermination');
}
function graph(k,wrong){let arcs=[];
 for(let h=0;h<k;h++){
  const s=8*h,t=s+8;
  const paths=[[[s,s+1,t],'++'],[[s,s+2,s+3,t],'+++'],[[s,s+4,s+5,t],'++-'],[[s,s+6,s+7,t],wrong===h?'---':'+++']];
  for(const [v,word] of paths)for(let j=0;j<word.length;j++)arcs.push(word[j]==='+'?[v[j],v[j+1]]:[v[j+1],v[j]]);
 }
 return {n:8*k+1,arcs};
}
let cases=[];
for(let k=1;k<=6;k++)for(const wrong of [-1,k-1]){
 const g=graph(k,wrong),p=closure(g.n,g.arcs);
 eq(p.ok,wrong===-1);
 if(p.ok){
  const free=new Set(Array.from({length:k},(_,i)=>8*i+1));
  for(let v=0;v<g.n;v++)eq(bits(p.D[0][v]).length,free.has(v)?2:1);
  for(let v of free)eq(bits(p.D[0][v]).length,2);
 }
 cases.push({k,kind:wrong===-1?'YES':'NO',pc:p.ok,rawFeedback:3*k,expectedCount:wrong===-1?String(5*2**k):'0'});
}
console.log(JSON.stringify({run:'TMR-1/084',status:'COMPUTATIONAL',cases,checks,failures:0},null,2));

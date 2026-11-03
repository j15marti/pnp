#!/usr/bin/env node
'use strict';
// Standalone published theorem/falsifier reproducer for LSPV-3 375.
// The complete independently checked signed-source/witness/DAG fixture is in
// the role archive; this compact publication recomputes ALL finite cut minima.
const assert=require('assert');
const pop=(x)=>{let z=0;for(;x;x>>>=1)z+=x&1;return z};
const graphs={
 K4:{h:4,e:[]},K33:{h:6,e:[]},CUBE:{h:8,e:[]},
 PRISM6:{h:12,e:[]},PATH8:{h:8,e:[]}
};
for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)graphs.K4.e.push([a,b]);
for(let a=0;a<3;a++)for(let b=3;b<6;b++)graphs.K33.e.push([a,b]);
for(let a=0;a<8;a++)for(let j=0;j<3;j++){let b=a^(1<<j);if(a<b)graphs.CUBE.e.push([a,b])}
for(let layer=0;layer<2;layer++)for(let a=0;a<6;a++){
 let u=layer*6+a,v=layer*6+(a+1)%6;graphs.PRISM6.e.push([Math.min(u,v),Math.max(u,v)])
}
for(let a=0;a<6;a++)graphs.PRISM6.e.push([a,6+a]);
for(let a=0;a<7;a++)graphs.PATH8.e.push([a,a+1]);
const cut=(S,E)=>E.reduce((x,[a,b])=>x+(((S>>a)&1)!==((S>>b)&1)),0);
let rows=[];
for(const [name,G] of Object.entries(graphs)){
 const {h,e}=G,n=e.length,all=(1<<h)-1;
 let minB=Infinity,epsilonN=Infinity,epsilonD=1;
 for(let S=1;S<all;S++){
  let size=pop(S),b=cut(S,e),d=Math.min(size,h-size);
  if(b*epsilonD<epsilonN*d){epsilonN=b;epsilonD=d}
  if(h<3*size&&3*size<=2*h)minB=Math.min(minB,b)
 }
 const incidence=Array.from({length:h},(_,v)=>
   e.reduce((r,[a,b],j)=>r|((a===v||b===v)?1<<j:0),0));
 assert.equal(incidence.reduce((a,b)=>a^b,0),0);
 const charge=Array(h).fill(0);charge[0]=1;
 const DAG=[...Array(h)].map((_,i)=>({dep:[],support:1<<i,
   mask:incidence[i],rhs:charge[i]}));
 let active=[...Array(h).keys()];
 while(active.length>1){
  const next=[];
  for(let j=0;j<active.length;j+=2){
   if(j+1===active.length){next.push(active[j]);continue}
   const a=DAG[active[j]],b=DAG[active[j+1]];
   next.push(DAG.length);
   DAG.push({dep:[active[j],active[j+1]],support:a.support^b.support,
     mask:a.mask^b.mask,rhs:a.rhs^b.rhs});
  }active=next
 }
 const root=DAG[active[0]];
 assert.equal(root.support,all);assert.equal(root.mask,0);assert.equal(root.rhs,1);
 const balanced=DAG.filter(z=>h<3*pop(z.support)&&3*pop(z.support)<=2*h);
 assert(balanced.length>0);
 for(const z of balanced)assert(pop(z.mask)>=minB);
 let maxw=Math.max(...DAG.map(x=>pop(x.mask)));
 assert(maxw>=minB);assert(DAG.length===2*h-1);
 const clauses=[];
 for(let v=0;v<h;v++){
  let incident=e.map(([a,b],i)=>a===v||b===v?i:-1).filter(i=>i>=0);
  for(let pat=0;pat<(1<<incident.length);pat++)if(pop(pat)%2!==charge[v]){
   clauses.push(incident.map((j,k)=>(pat>>k&1)?-(j+1):(j+1)));
  }
 }
 let text='p cnf '+n+' '+clauses.length+'\n';
 for(const c of clauses)text+=c.join(' ')+' 0\n';
 const bits=Buffer.byteLength(text,'ascii')*8;
 rows.push({name,h,n,m:clauses.length,epsilon:epsilonN+'/'+epsilonD,
  min_balanced_width:minB,balanced_XOR_max:maxw,balanced_XOR_nodes:h-1,
  encoded_input_bits:bits});
}
for(const row of rows)console.log(JSON.stringify(row));

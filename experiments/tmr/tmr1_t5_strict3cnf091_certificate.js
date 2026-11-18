'use strict';
// TMR-1/091: strict 3-distinct-variable CNF and exact counting.
// Standalone deterministic finite COMPUTATIONAL certificate, Node.js only.
const assert=require('node:assert/strict');
const beat=(a,b)=>([1,3].includes((b-a+5)%5));
const width=n=>Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
let tests=0,graphs=0,colorings=0,exhaustiveBoolean=0,failures=0;
const ck=(condition,message='check')=>{tests++;assert.ok(condition,message)};
const code=(num,k)=>Array.from({length:k},(_,i)=>(num>>i)&1).join('');
function compile(n,edges){
 const c=[],y=(v,a)=>7*v+a+1,p=v=>7*v+6,q=v=>7*v+7;
 const z=7*n+1,aa=z+1,bb=z+2;
 const add=cl=>{ck(cl.length===3 && new Set(cl.map(Math.abs)).size===3,'strict distinct variables');c.push(cl)};
 const pad=(l,r)=>add([l,r,-z]);
 for(let v=0;v<n;v++){
  for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)pad(-y(v,a),-y(v,b));
  add([-p(v),y(v,0),y(v,1)]);pad(p(v),-y(v,0));pad(p(v),-y(v,1));
  add([-q(v),y(v,2),y(v,3)]);pad(q(v),-y(v,2));pad(q(v),-y(v,3));
  add([p(v),q(v),y(v,4)]);
 }
 for(const [u,v] of edges)for(let a=0;a<5;a++)add([-y(u,a),y(v,(a+1)%5),y(v,(a+3)%5)]);
 // Exclude seven of the eight triples (z,aa,bb), keeping only (1,0,0).
 for(let t=0;t<8;t++)if(t!==1){
  const values=[t&1,(t>>1)&1,(t>>2)&1],variables=[z,aa,bb];
  add(values.map((b,i)=>b?-variables[i]:variables[i]));
 }
 return {N:7*n+3,c};
}
const sat=(F,b)=>F.c.every(cl=>cl.some(l=>l>0?b[l-1]:!b[-l-1]));
function lift(x){
 const n=x.length,b=Array(7*n+3).fill(false);
 for(let v=0;v<n;v++){
  b[7*v+x[v]]=true;b[7*v+5]=x[v]<2;b[7*v+6]=(x[v]===2||x[v]===3);
 }
 b[7*n]=true; // z=1, aa=bb=0
 return b;
}
function enumerateColors(n,fn){for(let k=0;k<5**n;k++){
 let t=k;const x=Array.from({length:n},()=>{const a=t%5;t=Math.floor(t/5);return a});fn(x);
}}
function audit(n,arcs){
 graphs++;const m=arcs.length,F=compile(n,arcs),L=n+m+2+2*m*width(n),W=width(F.N);
 ck(F.N===7*n+3,'vars');ck(F.c.length===17*n+5*m+7,'clauses');
 ck(F.c.every(cl=>cl.length===3&&new Set(cl.map(Math.abs)).size===3),'strict clauses');
 ck(F.c.every(cl=>cl.every(l=>Math.abs(l)>=1&&Math.abs(l)<=F.N)),'indices');
 const trueLength=F.N+F.c.length+2+F.c.length*(2+3*(W+1));
 ck(trueLength===7*n+5+(17*n+5*m+7)*(6+3*W),'bit length');
 const active=[...new Set(arcs.flat())].sort((a,b)=>a-b),k=active.length;
 const map=new Map(active.map((v,i)=>[v,i]));
 const Fsmall=compile(k,arcs.map(([u,v])=>[map.get(u),map.get(v)]));
 const Lsmall=Fsmall.N+Fsmall.c.length+2+Fsmall.c.length*(2+3*(width(Fsmall.N)+1));
 ck(Lsmall<=500*L,'bitlinear normalized');
 let original=0,normalized=0;
 enumerateColors(n,x=>{
  const truth=arcs.every(([u,v])=>beat(x[u],x[v]));
  ck(sat(F,lift(x))===truth,'witness and semantic preservation');
  original+=Number(truth);colorings++;
 });
 enumerateColors(k,x=>normalized+=Number(sat(Fsmall,lift(x))));
 ck(original===5**(n-k)*normalized,'isolate counting');
}
for(let n=0;n<=3;n++){
 const arcs=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)arcs.push([i,j]);
 for(let m=0;m<2**arcs.length;m++)audit(n,arcs.filter((_,i)=>(m&(1<<i))!==0));
}
// Independent exhaustive Boolean assignment counting, including noncanonical gate/padding bits.
for(const arcs of [[],[[0,0]],[[0,1]],[[0,1],[1,0]],[[0,0],[1,1]]]){
 const F=compile(2,arcs);let all=0,expected=0;
 for(let i=0;i<2**F.N;i++){
  const b=Array.from({length:F.N},(_,j)=>(i>>j&1)!==0);
  if(sat(F,b))all++;exhaustiveBoolean++;
 }
 enumerateColors(2,x=>{if(arcs.every(([u,v])=>beat(x[u],x[v])))expected++});
 ck(all===expected,'exhaustive complete Boolean witness count');
}
// Local forced constant has exactly one satisfying assignment.
const Z=compile(0,[]);let globalCount=0;
for(let t=0;t<8;t++)globalCount+=Number(sat(Z,Array.from({length:3},(_,i)=>(t>>i&1)!==0)));
ck(globalCount===1,'global unique constant');
// Check canonical source header length, target serialization, and malformed behavior.
function encodeSource(n,arcs){return '1'.repeat(n)+'0'+'1'.repeat(arcs.length)+'0'+arcs.map(([u,v])=>code(u,width(n))+code(v,width(n))).join('')}
function encodeFormula(F){return '1'.repeat(F.N)+'0'+'1'.repeat(F.c.length)+'0'+F.c.map(cl=>'11'+cl.map(l=>(l<0?'1':'0')+code(Math.abs(l)-1,width(F.N))).join('')).join('')}
for(let n=0;n<=5;n++){
 const arcs=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if((u*13+v*19+n)%4===0)arcs.push([u,v]);
 const src=encodeSource(n,arcs),F=compile(n,arcs),tgt=encodeFormula(F);
 ck(src.length===n+arcs.length+2+2*arcs.length*width(n),'source serialized length');
 ck(tgt.length===7*n+5+(17*n+5*arcs.length+7)*(6+3*width(F.N)),'target serialized length');
}
// Cover much larger possible (n,m) parameter sizes for length bound.
for(let n=0;n<=100;n++)for(let m=0;m<=Math.min(n*n,120);m++){
 const k=m===0?0:Math.min(n,2*m),L=n+m+2+2*m*width(n),b=7*k+3,c=17*k+5*m+7;
 const target=b+c+2+c*(2+3*(width(b)+1));
 ck(target<=500*L,'uniform normalized bound');
}
console.log(JSON.stringify({theorem:'C1-T5-STRICT3-PARSIMONIOUS091',graphs,colorings,exhaustiveBoolean,assertions:tests,failures,variableCount:'7n+3',clauseCount:'17n+5m+7',targetBits:'7n+5+(17n+5m+7)(6+3w(7n+3))',isolateNormalizedBitFactor:500,scope:'finite COMPUTATIONAL verification'}));

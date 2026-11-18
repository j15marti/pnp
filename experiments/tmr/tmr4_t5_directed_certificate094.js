#!/usr/bin/env node
'use strict';
// TMR-4/094 independent exhaustive original-source digraph verifier (Node 18+).
// Unlike Python's superset-zeta, enumerates all subgraphs of each coloring's
// permitted-arc set. Reproduces exact original assignment multiplicities.
const assert=require('node:assert/strict'),crypto=require('node:crypto');
const R=(x,y)=>((y-x+5)%5===1)||((y-x+5)%5===3);
const arcs=n=>{let e=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)e.push([i,j]);return e};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const source=(n,m)=>n+':'+(n===1?'':m.toString(2).padStart(n*(n-1),'0'))+'\n';
function allCounts(n){
  let es=arcs(n),limit=1<<es.length,table=new Uint32Array(limit),colors=new Uint8Array(n);
  for(let id=0;id<5**n;id++){
    let a=id;for(let i=0;i<n;i++){colors[i]=a%5;a=Math.floor(a/5)}
    let all=0;for(let k=0;k<es.length;k++)if(R(colors[es[k][0]],colors[es[k][1]]))all|=1<<k;
    let s=all;
    for(;;){table[s]++;if(s===0)break;s=(s-1)&all}
  }
  return table;
}
function cnf(n,mask){
  let cs=[],forbid=(i,a)=>[0,1,2].map(b=>a&(1<<b)?-(3*i+b+1):3*i+b+1);
  for(let i=0;i<n;i++)for(let c=5;c<8;c++)cs.push(forbid(i,c));
  let es=arcs(n);
  for(let k=0;k<es.length;k++)if(mask&(1<<k))for(let a=0;a<5;a++)for(let b=0;b<5;b++)if(!R(a,b)){
    cs.push([...forbid(es[k][0],a),...forbid(es[k][1],b)])
  }
  return cs;
}
function cnfValue(cs,codes){let bits=codes.flatMap(a=>[a&1,(a>>1)&1,(a>>2)&1]);
  return cs.every(c=>c.some(l=>bits[Math.abs(l)-1]===Number(l>0)))}
function run(){
 let start=process.hrtime.bigint(),seed=2026111894;
 const rand=()=>{seed=(Math.imul(seed,1103515245)+12345)>>>0;return seed};
 let gates={all_graphs:0,individual_coloring_enumerations:0,certificate_completions:0,cnf:0,domain:0};
 let rows=[];
 for(let n=1;n<=5;n++){
   let es=arcs(n),M=es.length,tot=1<<M,c=allCounts(n);
   let cols=Array.from({length:n},(_,i)=>i%5),free=0;
   for(let k=0;k<M;k++)if(R(cols[es[k][0]],cols[es[k][1]]))free|=1<<k;
   const pop=x=>{let ct=0;while(x){x&=(x-1);ct++}return ct};
   let max=0,numMax=0,sat=0;
   for(let k=0;k<tot;k++)if(c[k]){
     sat++;let pc=pop(k);if(pc>max){max=pc;numMax=1}else if(pc===max)numMax++
   }
   assert.equal(max,Math.floor(2*n*n/5));
   assert.equal(pop(free),max);assert.equal(c[0],5**n);
   let sub=free;
   for(;;){assert(c[sub]>0);gates.certificate_completions++;if(sub===0)break;sub=(sub-1)&free}
   for(let t=0;t<30;t++){
     let mask=rand()%tot,cls=cnf(n,mask);assert.equal(cls.length,3*n+15*pop(mask));
     for(let j=0;j<20;j++){
       let values=Array.from({length:n},()=>rand()%8);
       let satdirect=values.every(x=>x<5)&&es.every(([i,k],q)=>!(mask&(1<<q))||R(values[i],values[k]));
       assert.equal(cnfValue(cls,values),satdirect);gates.cnf++;
     }
   }
   rows.push({n,source_bits:M,sha256_empty:sha(source(n,0)),all_sources:tot,
    sat_sources:sat,unsat_sources:tot-sat,max_sat_arcs:max,max_sat_arc_graphs:numMax,
    certificate_queries:M-max,unqueried_arcs:max,empty_assignment_count:String(c[0])});
   gates.all_graphs+=tot;gates.individual_coloring_enumerations+=5**n;
 }
 for(let rev of [false,true])for(let X=0;X<32;X++)for(let Y=0;Y<32;Y++){
   let a=0,b=0,A=0,B=0;
   for(let p=0;p<5;p++)for(let q=0;q<5;q++)if((X&(1<<p))&&(Y&(1<<q))&&(rev?R(q,p):R(p,q))){a|=1<<p;b|=1<<q}
   for(let p=0;p<8;p++)for(let q=0;q<8;q++)if(p<5&&q<5&&(X&(1<<p))&&(Y&(1<<q))&&(rev?R(q,p):R(p,q))){A|=1<<p;B|=1<<q}
   assert.equal(a,A);assert.equal(b,B);gates.domain++;
 }
 return {experiment:'TMR4_094_FULL_DIRECTED_JS_INDEPENDENT',rows,gates,
         elapsed_seconds:Number(process.hrtime.bigint()-start)/1e9,unexpected_failures:0};
}
console.log(JSON.stringify(run(),null,2));

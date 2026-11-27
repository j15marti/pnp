'use strict';
function audit2(){
 let checks=0;function ok(v,m){checks++;if(!v)throw Error(m)}
 // Ordinary n=2 directed HC is e12 AND e21. Encode the two unit clauses as in L01-08.
 const G=[];for(let i=0;i<2;i++){let a=3*i,b=a+1,p=a+2;G.push([a,b],[a,p],[b,p],[b,6+i])}
 let signed=[];
 for(let mask=0;mask<4;mask++){
  let z=[1,mask&1,-1,1,(mask>>1)&1,-1,-1,-1],pos=0,neg=0,zero=0;
  for(let s=0;s<256;s++)for(let t=0;t<256;t++){
   if(G.some(([a,b],i)=>((t>>i)&1)&&(((s>>a)&1)||((s>>b)&1))))continue;
   let v=1;for(let i=0;i<8;i++){if(!((s>>i)&1))v*=z[i];if((t>>i)&1)v*=-1}if(v===1)pos++;else if(v===-1)neg++;else zero++;
  }
  ok(pos-neg===(mask===3?1:0),"signed HC identity");
  ok(pos>0,"nonzero individual terms");
  signed.push({mask,positive:pos,negative:neg,zero,total:pos-neg})
 }
 // Check the threshold rounding convex decomposition on all denominator-three points.
 let feasiblePoints=0,roundings=0,optimalFaceChecks=0;
 for(let em=0;em<16;em++){
  let E=[];for(let i=0;i<2;i++)for(let j=0;j<2;j++)if((em>>(2*i+j))&1)E.push([i,2+j]);
  let vertices=[];for(let s=0;s<16;s++){let v=Array.from({length:4},(_,i)=>(s>>i)&1);if(E.every(([i,j])=>v[i]+v[j]<=1))vertices.push(v)}
  for(let m=0;m<256;m++){
   let x=Array.from({length:4},(_,i)=>(m>>(2*i))&3);if(!E.every(([i,j])=>x[i]+x[j]<=3))continue;feasiblePoints++;
   let y=x.map((v,i)=>i<2?v:3-v),vs=[];
   for(let t=1;t<=3;t++){let v=y.map((u,i)=>i<2?Number(u>=t):Number(u<t));ok(E.every(([i,j])=>v[i]+v[j]<=1),"threshold vertex");vs.push(v);roundings++}
   ok(x.every((v,i)=>v===vs.reduce((s,a)=>s+a[i],0)),"exact threshold average");
   for(let q=0;q<81;q++){let r=q,c=[];for(let i=0;i<4;i++){c.push(r%3-1);r=Math.floor(r/3)}let cost=v=>v.reduce((s,a,i)=>s+c[i]*a,0),min=Math.min(...vertices.map(cost));if(cost(x)===3*min){ok(vs.every(v=>cost(v)===min),"optimum face decomposition");optimalFaceChecks++}}
  }
 }
 // Nonlinear compact decoder: priorities ordered by value then original vertex ID.
 function cycleKey(p){return [0,...p].join(",")}
 let nonlinear=[];
 for(let n=2;n<=5;n++){let k=n-1,d=2**Math.ceil(Math.log2(k)),all=new Set();for(let z=0;z<d**k;z++){let t=z,a=[];for(let i=1;i<n;i++){a.push([i,t%d]);t=Math.floor(t/d)}a.sort((u,v)=>u[1]-v[1]||u[0]-v[0]);all.add(cycleKey(a.map(x=>x[0])))}let f=1;for(let i=2;i<=k;i++)f*=i;ok(all.size===f,"priority decoder not surjective");nonlinear.push({n,priorityAssignments:d**k,distinctTours:all.size})}
 return {signed,feasiblePoints,roundings,optimalFaceChecks,nonlinear,assertions:checks}
}
console.log(JSON.stringify(audit2(),null,2));

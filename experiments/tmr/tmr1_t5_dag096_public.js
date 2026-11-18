// TMR-1/096 public proof-obligation certificate. Finite COMPUTATIONAL checks only.
// node experiments/tmr/tmr1_t5_dag096_public.js
'use strict';
let assertions=0,graphs=0,sourceAssignments=0,targetAssignments=0;
const ck=(v,s)=>{assertions++;if(!v)throw Error('TMR-1/096: '+s);};
const mod=x=>(x%5+5)%5,beat=(x,y)=>[1,3].includes(mod(y-x));
const w=n=>Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
const len=(n,m)=>n+m+2+2*m*w(n);
function flat(n,edges){
  const used=Array(n).fill(false);for(const [u,v] of edges){used[u]=true;used[v]=true;}
  const r=[];let N=0,k=0;for(let i=0;i<n;i++){
    if(!used[i])r.push({iso:N++});
    else {r.push({p:N++,q:N++,a:N++,b:N++});k++;}
  }
  const arcs=[],layer=[];
  for(const z of r){if(z.iso!==undefined){layer[z.iso]=0;continue;}
    const {p,q,a,b}=z;arcs.push([p,a],[p,b],[q,a],[q,b],[a,b]);
    layer[p]=0;layer[q]=1;layer[a]=2;layer[b]=3;
  }
  for(const [u,v] of edges)arcs.push([r[u].p,r[v].q]);
  ck(N===n+3*k&&arcs.length===edges.length+5*k,'exact size');
  ck(arcs.every(([u,v])=>layer[u]<layer[v]),'DAG with four layers');
  ck(len(N,arcs.length)<=28*len(n,edges.length),'28x encoded-length bound');
  return {N,r,arcs};
}
const digits=(t,n)=>{const a=[];for(let i=0;i<n;i++){a.push(t%5);t=Math.floor(t/5);}return a;};
const sat=(a,arcs)=>arcs.every(([u,v])=>beat(a[u],a[v]));
const extend=(a,r)=>{const b=[];r.forEach((z,i)=>{const x=a[i];
  if(z.iso!==undefined)b[z.iso]=x;
  else {b[z.p]=b[z.q]=x;b[z.a]=mod(x+3);b[z.b]=mod(x+1);}
});return b;};
for(let p=0;p<5;p++)for(let q=0;q<5;q++){
 let ways=0;for(let a=0;a<5;a++)for(let b=0;b<5;b++)
  if(beat(p,a)&&beat(p,b)&&beat(q,a)&&beat(q,b)&&beat(a,b)){
    ways++;ck(p===q&&a===mod(p+3)&&b===mod(p+1),'forced equality witness');
  }
 ck(ways===Number(p===q),'equality relation');
}
for(let n=0;n<=3;n++){
 const pairs=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)pairs.push([u,v]);
 for(let mask=0;mask<2**pairs.length;mask++){
  const edges=pairs.filter((_,i)=>(mask>>i)&1),d=flat(n,edges);graphs++;
  let count=0;for(let t=0;t<5**n;t++){
    const x=digits(t,n),y=extend(x,d.r);sourceAssignments++;
    ck(sat(x,edges)===sat(y,d.arcs),'witness preservation');
    if(sat(x,edges))count++;
  }
  // Independently enumerate all target colorings for inputs of size at most 2.
  if(n<=2){let targetCount=0;
    for(let t=0;t<5**d.N;t++){
      targetAssignments++;if(sat(digits(t,d.N),d.arcs))targetCount++;
    }
    ck(targetCount===count,'direct target count');
  }
 }
}
const no=flat(1,[[0,0]]);let countNo=0;
for(let t=0;t<5**no.N;t++)if(sat(digits(t,no.N),no.arcs))countNo++;
ck(!countNo,'constant-size UNSAT DAG');
for(let n=0;n<=300;n++)for(let m=0;m<=Math.min(50,n*n);m++)
 for(let k=0;k<=Math.min(n,2*m);k++){
   const N=n+3*k,M=m+5*k;
   ck(w(N)<=w(n)+2,'address width');
   ck(len(N,M)<=28*len(n,m),'symbolic 28x bound audit');
 }
console.log(JSON.stringify({run:'TMR-1/096-public',status:'PASS',assertions,graphs_checked:graphs,source_assignments:sourceAssignments,full_target_assignments:targetAssignments,failures:0,bit_expansion_bound:28,proof_status:'Finite computational audit only; P vs NP open.'},null,2));

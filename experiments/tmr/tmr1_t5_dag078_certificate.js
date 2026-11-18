"use strict";
// TMR-1/078: exact five-state gadget plus DAG rank, deterministic finite certificate.
const R=(a,b)=>[1,3].includes((b-a+5)%5);
const C=(a,b)=>[1,4].includes((b-a+5)%5);
let checks=0,graphs=0,yes=0,no=0,labelings=0;
for(let a=0;a<5;a++)for(let b=0;b<5;b++){
  let count=0;
  for(let w=0;w<5;w++)for(let z=0;z<5;z++){
    if(R(a,z)&&R(a,w)&&R(w,z)&&R(w,b)){
      if(w!==(a+3)%5||z!==(a+1)%5)throw Error('nonunique');
      count++;
    }
  }
  if(count!==Number(C(a,b)))throw Error('wrong endpoint completion');
  checks++;
}
for(let n=0;n<=5;n++){
  const all=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)all.push([u,v]);
  for(let mask=0;mask<2**all.length;mask++){
    graphs++;
    const es=all.filter((_,i)=>(mask&2**i)!==0);
    const arcs=[],rank=Array.from({length:n+2*es.length},()=>null);
    for(let i=0;i<n;i++)rank[i]=3*i;
    for(let i=0;i<es.length;i++){
      const [u,v]=es[i],w=n+2*i,z=w+1;
      arcs.push([u,z],[u,w],[w,z],[w,v]);
      rank[w]=3*u+1;rank[z]=3*u+2;
    }
    if(arcs.length!==4*es.length||arcs.some(([a,b])=>rank[a]>=rank[b]))throw Error('cycle/rank');
    let sat=false;
    for(let t=0;t<5**n;t++){
      const x=[];let r=t;for(let j=0;j<n;j++){x.push(r%5);r=Math.floor(r/5);}
      const y=x.slice();for(const [u,v] of es)y.push((x[u]+3)%5,(x[u]+1)%5);
      const h=es.every(([u,v])=>C(x[u],x[v]));
      const d=arcs.every(([u,v])=>R(y[u],y[v]));
      if(h!==d)throw Error('witness mismatch');
      sat ||= h;labelings++;checks++;
    }
    if(sat)yes++;else no++;
  }
}
if(graphs!==1100||yes===0||no===0)throw Error('coverage');
const result={revision:'tmr1-t5-dag078-certificate-js-v1',graphs,yes,no,labelings,checks,failures:0,scope:'finite computational; n<=5 simple undirected graphs; not a proof of asymptotics'};
console.log(JSON.stringify(result));

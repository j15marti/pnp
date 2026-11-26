'use strict';
function fp19Audit() {
 const E=[[0,2],[0,6],[0,9],[1,3],[1,7],[1,10],[2,10],[2,11],[3,8],[3,11],[4,5],[4,9],[4,11],[5,6],[5,10],[6,7],[7,8],[8,9]];
 const Q=[[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]], ports=[4,5,2,6];
 const protectedEdges=E.map((_,i)=>i).filter(i=>i!==5);
 const assert=(x,m)=>{if(!x)throw Error(m);};
 const colorWords=(edges,n)=>{
  const used=Array(n).fill(0), word=[],out=[];
  function visit(i){
   if(i===edges.length){out.push([...word]);return;}
   const [u,v]=edges[i];
   for(let c=1;c<=3;c++){const m=1<<c;if((used[u]|used[v])&m)continue;
    used[u]^=m;used[v]^=m;word.push(c);visit(i+1);word.pop();used[u]^=m;used[v]^=m;
   }
  }visit(0);return out;
 };
 const proper=colorWords(E,12);
 const qt=colorWords(Q,10);
 const relation=new Map();
 for(const w of qt){
  const masks=Array(10).fill(0);
  Q.forEach(([u,v],i)=>{masks[u]|=1<<w[i];masks[v]|=1<<w[i];});
  const boundary=ports.map(v=>[1,2,3].find(c=>!(masks[v]&(1<<c))));
  assert(boundary[0]===boundary[1]&&boundary[2]===boundary[3],"non-equality four-pole");
  const key=[boundary[0],boundary[2]].join(",");
  if(!relation.has(key))relation.set(key,[]);relation.get(key).push(w);
 }
 assert(proper.length===12&&relation.size===9&&qt.length===18,"local word counts");
 const S=E.map((_,i)=>((110469>>i)&1)+2*((185822>>i)&1));
 const T=E.map((_,i)=>((96734>>i)&1)+2*((178037>>i)&1));
 const b=(c,d)=>d===0?c&1:d===1?(c>>1)&1:((c&1)^((c>>1)&1));
 const cost=(s,t,d)=>Number(!b(s,d)&&!(t&1));
 const init=protectedEdges.map(i=>relation.get([S[i],T[i]].join(","))[0]);
 const forms=[];
 for(let d=0;d<3;d++){
  const fs=[];
  for(const x of proper)for(const y of proper){
   let coeff=0,constant=cost(S[5],x[5],d)+cost(T[5],y[5],d);
   protectedEdges.forEach((i,j)=>{
    const w=cost(S[i],x[i],d)+cost(T[i],y[i],d);
    constant+=w;coeff+=w+Math.min(...relation.get([x[i],y[i]].join(",")).map(z=>z.reduce((s,c,k)=>s+cost(init[j][k],c,d),0)));
   });
   fs.push([coeff,constant]);
  }
  const minimum=[Math.min(...fs.map(v=>v[0])),Math.min(...fs.map(v=>v[1]))];
  assert(fs.some(v=>v[0]===minimum[0]&&v[1]===minimum[1]),"joint minimizer");
  assert(minimum[0]===(d===0?2:1)&&minimum[1]===minimum[0],"affine radius");
  forms.push(minimum);
 }
 // Independent explicit cut-space audit on constructed sources. Each
 // fundamental cycle supplies one bit of a signature for every edge.
 function source(L){
  const edges=[],initial=[];
  const add=(u,v,z)=>{edges.push([u,v]);initial.push(z);};
  protectedEdges.forEach((i,j)=>{
   let ends=[E[i][0],E[i][0]+12];
   for(let h=0;h<L;h++){
    const off=24+8*(j*L+h);
    Q.forEach(([u,v],k)=>add(off+u-2,off+v-2,init[j][k]));
    for(let t=0;t<2;t++){
     add(ends[t],off+ports[2*t]-2,[S,T][t][i]);
     ends[t]=off+ports[2*t+1]-2;
    }
   }
   for(let t=0;t<2;t++)add(ends[t],E[i][1]+12*t,[S,T][t][i]);
  });
  for(let t=0;t<2;t++)add(E[5][0]+12*t,E[5][1]+12*t,[S,T][t][5]);
  const n=24+136*L,adj=Array.from({length:n},()=>[]),balance=Array(n).fill(0);
  edges.forEach(([u,v],i)=>{adj[u].push([v,i]);adj[v].push([u,i]);balance[u]^=initial[i];balance[v]^=initial[i];});
  assert(adj.every(a=>a.length===3)&&balance.every(x=>x===0)&&initial.filter(x=>x===0).length===1,"source initial");
  assert(new Set(edges.map(([u,v])=>[Math.min(u,v),Math.max(u,v)].join(","))).size===edges.length,"simple");
  const parent=Array(n).fill(-1),pe=Array(n).fill(-1),depth=Array(n).fill(0),q=[0];parent[0]=0;
  for(const u of q)for(const [v,i] of adj[u])if(parent[v]<0){parent[v]=u;pe[v]=i;depth[v]=depth[u]+1;q.push(v);}
  assert(q.length===n,"connected");
  const sig=Array(edges.length).fill(0n), tree=new Set(pe.slice(1));let h=0n;
  edges.forEach(([u0,v0],i)=>{
   if(tree.has(i))return;
   const mask=1n<<h++;sig[i]^=mask;let u=u0,v=v0;
   while(u!==v){if(depth[u]<depth[v])[u,v]=[v,u];sig[pe[u]]^=mask;u=parent[u];}
  });
  const lookup=new Map();sig.forEach((v,i)=>{assert(v!==0n&&!lookup.has(v),"one or two edge cut");lookup.set(v,i);});
  let cuts=0;
  for(let i=0;i<sig.length;i++)for(let j=i+1;j<sig.length;j++){
   const k=lookup.get(sig[i]^sig[j]);if(k===undefined||k<=j)continue;
   assert(edges[i].some(v=>edges[j].includes(v)&&edges[k].includes(v)),"nonstar three cut");cuts++;
  }
  assert(cuts===n,"star count");
  return {L,n,threeCuts:cuts,pairs:edges.length*(edges.length-1)/2};
 }
 return {proper:proper.length,localWords:qt.length,forms,sourceChecks:[1,2,4,8].map(source)};
}
console.log(JSON.stringify(fp19Audit(),null,2));

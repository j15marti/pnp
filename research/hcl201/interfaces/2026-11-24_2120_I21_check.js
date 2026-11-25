function run(){
let seed=20261124, assertions=0, charts=0, sat=0, unsat=0, words=0,maxV=0,maxE=0, nativeWords=0;
const check=(x)=>{assertions++;if(!x)throw Error("assertion "+assertions)};
const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const lit=(x,l)=>((x>>l[0])&1)^l[1];
function compile(C){
  const types=[], edges=[], raw=[], groups=new Map(), anchors=new Map();
  const vertex=t=>(types.push(t),types.length-1);
  const add=(u,v,s=0)=>raw.push([u,v,s]);
  const n=1+Math.max(-1,...C.flat().map(l=>l[0]));
  for(let j=0;j<C.length;j++)for(let k=0;k<2;k++){
    const v=vertex("B");
    for(const [a,s] of [...C[j],[n+j,0]]){
      if(!groups.has(a))groups.set(a,[]);
      groups.get(a).push([v,s]);
    }
  }
  for(const [a,ports] of groups){
    const d=ports.length;check(d%2===0);
    if(d===2){const [[u,s],[v,t]]=ports;anchors.set(a,[raw.length,0,s]);add(u,v,s^t);continue}
    const eq=Array.from({length:d/2-1},()=>vertex("E"));
    let p=0;for(let i=0;i<eq.length;i++){
      if(i) add(eq[i-1],eq[i]);
      let count=4-(i>0?1:0)-(i+1<eq.length?1:0);
      while(count--){const [v,s]=ports[p++];if(!anchors.has(a))anchors.set(a,[raw.length,0,0]);add(eq[i],v,s)}
    }check(p===d);
  }
  const rawMap=[];
  for(const [u,v,s] of raw){
    const t=Array.from({length:5},()=>vertex("E"));
    rawMap.push(edges.length);edges.push([u,t[0],s]);
    for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(!(i===0&&j===1))edges.push([t[i],t[j],0]);
    edges.push([t[1],v,0]);
  }
  for(const [a,[i,p,s]] of anchors)anchors.set(a,[2*rawMap[i]+p,s]);
  const ports=types.map(()=>[]), seen=new Set();
  edges.forEach(([u,v],i)=>{const key=[u,v].sort((a,b)=>a-b).join(",");check(u!==v&&!seen.has(key));seen.add(key);ports[u].push(2*i);ports[v].push(2*i+1)});
  check(ports.every(p=>p.length===4));
  maxV=Math.max(maxV,types.length);maxE=Math.max(maxE,edges.length);
  return {types,edges,ports,anchors};
}
function native(C){
  const {types,edges,ports,anchors}=compile(C);
  const adj=Array.from({length:2*edges.length},()=>[]);
  const link=(u,v,s)=>{adj[u].push([v,s]);adj[v].push([u,s])};
  edges.forEach((e,i)=>link(2*i,2*i+1,e[2]));
  types.forEach((t,i)=>{if(t==="E")for(let j=1;j<4;j++)link(ports[i][0],ports[i][j],0)});
  const component=Array(adj.length).fill(-1),phase=Array(adj.length).fill(0);let k=0;
  for(let i=0;i<adj.length;i++)if(component[i]<0){
    component[i]=k;const q=[i];for(let j=0;j<q.length;j++)for(const [v,s] of adj[q[j]]){
      const z=phase[q[j]]^s;if(component[v]<0){component[v]=k;phase[v]=z;q.push(v)}else check(component[v]===k&&phase[v]===z)
    }k++;
  }
  const bs=ports.filter((_,i)=>types[i]==="B");
  const get=(x,p)=>((x>>component[p])&1)^phase[p];
  const vals=new Set();let count=0;
  for(let x=0;x<2**k;x++){
    words++;
    if(!bs.every(p=>p.reduce((s,z)=>s+get(x,z),0)===2))continue;
    count++;let y=0;for(const [a,[p,s]] of anchors) if(a<=Math.max(-1,...C.flat().map(l=>l[0])))y|=(get(x,p)^s)<<a;
    vals.add(y);
    if(count===1){check(edges.every((e,i)=>(get(x,2*i)^get(x,2*i+1))===e[2]));check(ports.every((p,i)=>types[i]==="E"?p.every(z=>get(x,z)===get(x,p[0])):p.reduce((s,z)=>s+get(x,z),0)===2))}
  }
  nativeWords+=count;
  const variables=[...new Set(C.flat().map(l=>l[0]))].sort((a,b)=>a-b);
  const ref=new Set();
  for(let x=0;x<2**variables.length;x++){let y=0;variables.forEach((a,i)=>y|=((x>>i)&1)<<a);if(C.every(c=>new Set(c.map(l=>lit(y,l))).size===2))ref.add(y)}
  check(count===ref.size);check(vals.size===ref.size&&[...vals].every(x=>ref.has(x)));
  charts++;if(count)sat++;else unsat++;return vals;
}
function from3(C,n){
 const r=n;const N=[];
 for(let i=0;i<C.length;i++){const [a,b,c]=C[i],y=n+1+i;N.push([a,b,[y,0]],[[y,1],c,[r,0]])}
 const vals=native(N), vars=[...new Set(C.flat().map(l=>l[0]))],actual=new Set(),ref=new Set();
 for(const z of vals){let w=0;for(const a of vars)w|=(((z>>a)^(z>>r))&1)<<a;actual.add(w)}
 for(let x=0;x<2**vars.length;x++){let w=0;vars.forEach((a,i)=>w|=((x>>i)&1)<<a);if(C.every(c=>c.some(l=>lit(w,l))))ref.add(w)}
 check(actual.size===ref.size&&[...actual].every(x=>ref.has(x)));
}
const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(c=>c.map(x=>[x,0]));
check(native(F).size===0);
for(let i=0;i<7;i++)for(let j=0;j<3;j++){const G=F.map(c=>c.map(l=>l.slice()));G[i][j][1]=1;check(native(G).size>0)}
for(let i=0;i<40;i++){const n=3+rng(4),m=1+rng(5);const C=Array.from({length:m},()=>Array.from({length:3},()=>[rng(n),rng(2)]));native(C)}
from3([[[0,0],[0,0],[0,0]],[[0,1],[0,1],[0,1]]],1);
from3([[[0,0],[0,0],[0,0]]],1);
for(let i=0;i<30;i++){const n=2+rng(3),m=1+rng(3);from3(Array.from({length:m},()=>Array.from({length:3},()=>[rng(n),rng(2)])),n)}
return {seed:20261124,assertions,charts,sat,unsat,componentWordsEnumerated:words,nativeWords,maxV,maxE,limitations:"Exhaustive equality-component enumeration for small controls; no polynomial SAT claim, no full matching backend. Equality transport closure before enumeration; no general semantic closure."}
}
console.log(JSON.stringify(run(),null,2));

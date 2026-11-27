function audit(){
 const edges=[[10,21],[6,20],[10,16],[12,20],[12,21],[11,14],[19,24],[4,14],[11,13],[0,5],[2,17],[16,22],[14,25],[3,24],[16,23],[7,13],[7,25],[4,20],[12,17],[7,8],[0,2],[8,15],[4,9],[18,19],[3,9],[13,18],[5,11],[3,23],[17,19],[9,22],[2,6],[5,8],[1,15],[1,22],[1,24],[15,23],[6,10],[0,18],[21,25]];
 const n=26,adj=Array.from({length:n},()=>[]),mod=x=>(x%3+3)%3,assert=x=>{if(!x)throw Error("assert")};
 edges.forEach(([u,v],i)=>{adj[u].push(i);adj[v].push(i)});assert(adj.every(a=>a.length===3));
 const t=Array(n).fill(null),tree=new Set(),q=[0];t[0]=Array(n).fill(0);
 for(const u of q)for(const e of adj[u]){const v=edges[e].find(x=>x!==u);if(t[v])continue;let a=t[u].slice();a[u]=mod(a[u]+adj[u].indexOf(e));a[v]=mod(a[v]-adj[v].indexOf(e));t[v]=a;tree.add(e);q.push(v)}
 const A=[];edges.forEach(([u,v],e)=>{if(tree.has(e))return;let a=t[u].map((x,i)=>mod(x-t[v][i]));a[u]=mod(a[u]+adj[u].indexOf(e));a[v]=mod(a[v]-adj[v].indexOf(e));A.push(a)});
 let p=0,piv=[];for(let j=0;j<n;j++){let k=A.findIndex((r,i)=>i>=p&&r[j]);if(k<0)continue;[A[k],A[p]]=[A[p],A[k]];let s=A[p][j];A[p]=A[p].map(x=>mod(x*s));for(let i=0;i<A.length;i++)if(i!==p&&A[i][j]){let c=A[i][j];A[i]=A[i].map((x,l)=>mod(x-c*A[p][l]))}piv.push(j);p++}
 const free=Array.from({length:n},(_,i)=>i).filter(i=>!piv.includes(i)),d=free.length;assert(d===12);
 const ps=A.slice(0,p).map(r=>{const a=free.map(i=>mod(-r[i])),m=new Map();const c=mod(a.reduce((s,x)=>s+x*x,0)-1);if(c)m.set(0,c);for(let i=0;i<d;i++)for(let j=i+1;j<d;j++){let v=mod(2*a[i]*a[j]);if(v)m.set((1<<i)^(1<<j),v)}return m});
 const run=mode=>{
  const gb=new Map([[0,[1,0]]]),logs=[];let checks=0;const CAP=300000;
  const red=(m,b)=>{for(const i of [...gb.keys()].sort((a,b)=>b-a))if(m&(1<<i)){const [r,t]=gb.get(i);m^=r;b^=t}return [m,b]};
  function round(lift,feedback){
   const polys=ps.map(poly=>{let out=new Map();for(const [m,c] of poly){const [u,b]=red(m,0);out.set(u,mod((out.get(u)||0)+(b?-c:c)))}return new Map([...out].filter(([m,c])=>c))});
   const mult=[0];if(lift)for(let i=0;i<d;i++)if(!gb.has(i))mult.push(1<<i);
   const rows=[];for(const m of mult)for(let i=0;i<polys.length;i++)if(polys[i].size)rows.push({i,m,p:new Map([...polys[i]].map(([u,c])=>[u^m,c]))});
   const mons=[...new Set([0,...rows.flatMap(r=>[...r.p.keys()])])].sort((a,b)=>a-b),ids=new Map(mons.map((m,i)=>[m,i])),B=new Map();
   function reduce(v,w){for(const i of [...B.keys()].sort((a,b)=>b-a)){if(++checks>CAP)throw Error("cap");let c=v[i];if(c){const [r,t]=B.get(i);for(let j=0;j<v.length;j++)v[j]=mod(v[j]-c*r[j]);for(let j=0;j<w.length;j++)w[j]=mod(w[j]-c*t[j])}}return [v,w]}
   function verify(w,target){let a=new Map();for(let j=0;j<w.length;j++)if(w[j])for(const [m,c] of rows[j].p)a.set(m,mod((a.get(m)||0)+w[j]*c));a=new Map([...a].filter(([m,c])=>c));assert(a.size===target.size&&[...target].every(([m,c])=>a.get(m)===c))}
   for(let j=0;j<rows.length;j++){let v=new Uint8Array(mons.length),w=new Uint8Array(rows.length);for(const [m,c] of rows[j].p)v[ids.get(m)]=c;w[j]=1;[v,w]=reduce(v,w);let i=v.findLastIndex(x=>x);if(i<0)continue;if(v[i]===2){v=v.map(x=>mod(2*x));w=w.map(x=>mod(2*x))}if(i===0){verify(w,new Map([[0,1]]));return {no:true,events:[]}}B.set(i,[v,w])}
   if(!feedback)return {events:[]};
   let groups=new Map(),events=[];
   for(let i=0;i<mons.length;i++){let v=new Uint8Array(mons.length),w=new Uint8Array(rows.length);v[i]=1;[v,w]=reduce(v,w);let k=v.findLastIndex(x=>x);if(k<0){verify(w.map(x=>mod(-x)),new Map([[mons[i],1]]));return {no:true,events:[]}}let s=v[k],key=v.map(x=>mod(s*x)).join("");if(!groups.has(key)){groups.set(key,[mons[i],s,w]);continue}let [u,t,z]=groups.get(key),c=mod(s*t);let proof=w.map((x,j)=>mod(-x+c*z[j]));verify(proof,new Map([[mons[i],1],[u,mod(-c)]]));events.push([mons[i]^u,c===2?1:0])}
   return {events};
  }
  try{while(true){let changed=false;for(const [lift,feedback] of mode==="base"?[[0,true]]:[[0,true],[1,mode==="hybrid"]]){const x=round(lift,feedback);if(x.no)return {status:"NO",checks,rank:gb.size,logs};for(const [m,b] of x.events){const [u,t]=red(m,b);if(!u){if(t){logs.push([m,b,"contradiction"]);return {status:"NO",checks,rank:gb.size,logs}}continue}gb.set(31-Math.clz32(u),[u,t]);logs.push([m,b]);changed=true}if(changed)break}if(!changed)return {status:"OPEN",checks,rank:gb.size,logs}}}catch(e){if(e.message!=="cap")throw e;return {status:"UNKNOWN",checks,rank:gb.size,logs}}
 };
 // independent exact perfect matching reference, then parity of complement cycles.
 let steps=0,count=0;function match(rem,chosen){steps++;if(!rem){let seen=new Set();for(let u=0;u<n;u++)if(!seen.has(u)){let queue=[u];seen.add(u);for(const v of queue)for(const e of adj[v])if(!chosen.has(e)){let w=edges[e].find(x=>x!==v);if(!seen.has(w)){seen.add(w);queue.push(w)}}if(queue.length%2)return}count++;return}let u=31-Math.clz32(rem&-rem);for(const e of adj[u]){let v=edges[e].find(x=>x!==u);if(rem&(1<<v)){chosen.add(e);match(rem^(1<<u)^(1<<v),chosen);chosen.delete(e)}}}match((1<<n)-1,new Set());assert(count===0);
 return {source:edges,d,matching:{steps,evenComplements:count},base:run("base"),static:run("static"),hybrid:run("hybrid")};
}
console.log(JSON.stringify(audit(),null,2));

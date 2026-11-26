function auditCEC07(){
 const assert=(v,m)=>{if(!v)throw Error(m)},mod=(x,m)=>((x%m)+m)%m;
 function source(E){
  const n=Math.max(...E.flat())+1, inc=Array.from({length:n},()=>[]);
  E.forEach(([u,v],i)=>{assert(u!==v,"loop");inc[u].push(i);inc[v].push(i)});assert(inc.every(a=>a.length===3),"source cubic");
  const l=(v,e)=>inc[v].indexOf(e), F=Array(n).fill(null), tree=new Set();
  for(let r=0;r<n;r++)if(!F[r]){F[r]=Array(n).fill(0);const q=[r];for(let i=0;i<q.length;i++){const u=q[i];for(const e of inc[u]){const v=E[e].find(x=>x!==u);if(F[v])continue;F[v]=F[u].slice();F[v][u]=mod(F[v][u]+l(u,e),3);F[v][v]=mod(F[v][v]-l(v,e),3);tree.add(e);q.push(v)}}}
  const rows=E.flatMap(([u,v],e)=>{if(tree.has(e))return [];const a=F[v].map((x,i)=>mod(x-F[u][i]-(i===u?l(u,e):0)+(i===v?l(v,e):0),3));return a.some(Boolean)?[a]:[]});
  const checkColor=c=>c.length===E.length&&inc.every(a=>new Set(a.map(e=>c[e])).size===3&&a.every(e=>[0,1,2].includes(c[e])));
  const sign=c=>{assert(checkColor(c),"source color");return inc.map(a=>mod(c[a[1]]-c[a[0]],3)===1?0:1)};
  const dot=(row,b)=>mod(row.reduce((s,x,i)=>s+x*(b[i]?-1:1),0),3);
  const violations=b=>rows.filter(r=>dot(r,b)!==0).length;
  function lift(b){assert(violations(b)===0,"sign feasible");const t=F.map(r=>dot(r,b));const c=E.map(([u,v],e)=>{const x=mod(t[u]+(b[u]?-1:1)*l(u,e),3);assert(x===mod(t[v]+(b[v]?-1:1)*l(v,e),3),"edge agreement");return x});assert(checkColor(c),"source lift");return c}
  function direct(){const c=Array(E.length).fill(-1), used=Array(n).fill(0);let nodes=0;function go(){nodes++;let e=-1,ops=null;for(let i=0;i<E.length;i++)if(c[i]===-1){const [u,v]=E[i],a=[0,1,2].filter(x=>!((used[u]|used[v])&(1<<x)));if(!a.length)return false;if(ops===null||a.length<ops.length){e=i;ops=a;}}if(e<0)return true;const [u,v]=E[e];for(const x of ops){c[e]=x;used[u]|=1<<x;used[v]|=1<<x;if(go())return true;c[e]=-1;used[u]^=1<<x;used[v]^=1<<x}return false}const yes=go();if(yes)assert(checkColor(c),"direct source witness");return {yes,color:yes?c:null,nodes}}
  function matchAudit(){const seen=Array(E.length).fill(0),miss=Array(E.length).fill(0),alive=Array(n).fill(true),sel=Array(E.length).fill(false);let count=0;function go(){let u=alive.indexOf(true);if(u<0){count++;for(let e=0;e<E.length;e++)(sel[e]?seen:miss)[e]++;return}alive[u]=false;for(const e of inc[u]){const v=E[e].find(x=>x!==u);if(!alive[v])continue;alive[v]=false;sel[e]=true;go();sel[e]=false;alive[v]=true}alive[u]=true}go();return {count,all_in_out:seen.every(Boolean)&&miss.every(Boolean)}}
  return {E,n,rows,sign,lift,violations,direct,matchAudit,checkColor};
 }
 function compile(S){
  const n=S.n,q=S.rows.length+1,w=3*q+1,marker=w-1,forward=[];
  for(const row of S.rows){
   const ops=row.flatMap((c,v)=>c?[{k:0,v,c}]:[]);
   forward.push(...ops,{k:1,v:n,c:1},...ops.slice().reverse().map(g=>({...g,c:-g.c})));
  }
  const gates=[...forward,{k:2,v:n,c:0},...forward.slice().reverse().map(g=>({...g,c:-g.c}))];
  assert(gates.length>=3&&w>=7,"program nontrivial");
  function apply(g,b,x){if(g.k===2)return x===0?marker:x===marker?0:x;if(x===marker)return x;let c=Math.floor(x/3),t=x%3;if(g.k===0)t=mod(t+g.c*(b?-1:1),3);else if(t!==0)c=mod(c+g.c,q);return 3*c+t}
  let total=2*w*gates.length;const p=[Array(total).fill(-1),Array(total).fill(-1)],wire=Array(total).fill(-1),group=Array(total).fill(-1),members=Array.from({length:n+1},()=>[]);
  const set=(a,u,v)=>{a[u]=v;a[v]=u};
  for(let i=0;i<gates.length;i++){
   const g=gates[i],start=2*w*i;
   for(let j=0;j<2*w;j++){group[start+j]=g.v;members[g.v].push(start+j)}
   for(let j=0;j<w;j++){for(let b=0;b<2;b++)set(p[b],start+j,start+w+apply(g,b,j));set(wire,start+w+j,2*w*((i+1)%gates.length)+j)}
  }
  const raw=total,seen=new Uint8Array(total);let splices=0,cycles=0,active=0;
  for(let v=0;v<members.length;v++){
   const reps=[];
   for(const x of members[v])if(!seen[x]){reps.push(x);let y=x,b=0;do{seen[y]=1;y=p[b][y];b^=1}while(y!==x||b!==0)}
   if(!reps.length)continue;active++;cycles+=reps.length;
   let a=reps[0];
   for(const c of reps.slice(1)){
    const b=p[0][a],d=p[0][c],x=total++,y=total++,r=total++,s=total++;splices++;
    for(const i of [x,y,r,s])group[i]=v;
    set(p[0],a,x);set(p[0],b,y);set(p[0],c,r);set(p[0],d,s);
    set(p[1],x,r);set(p[1],y,s);set(wire,x,y);set(wire,r,s);
   }
  }
  // Turn two closing wires into degree-two terminal anomalies, plus their shared defect edge.
  const u=total++,v=total++,uEnds=[0,wire[0]],vEnds=[marker,wire[marker]];
  for(const x of uEnds)wire[x]=u;
  for(const x of vEnds)wire[x]=v;
  const adj=Array.from({length:total},(_,i)=>i===u?[...uEnds,v]:i===v?[...vEnds,u]:[p[0][i],p[1][i],wire[i]]);
  for(let i=0;i<total;i++){assert(new Set(adj[i]).size===3&&adj[i].every(j=>Number.isInteger(j)&&j>=0&&j<total&&j!==i&&adj[j].includes(i)),"target simple cubic")}
  // Every nonexception vertex is on one genuine even A-cycle per variable.
  const sv=new Uint8Array(total);let ac=0;
  for(let i=0;i<u;i++)if(!sv[i]){ac++;let j=i,b=0,len=0;do{assert(!sv[j]&&group[j]===group[i],"one variable cycle");sv[j]=1;len++;j=p[b][j];b^=1}while(j!==i||b!==0);assert(len>=4&&len%2===0,"even A-cycle")}
  assert(ac===active,"exact one A-cycle per variable");
  // Linear-time connectivity/bridges check; no matching oracle.
  let timer=0,bridges=0;const tin=new Int32Array(total).fill(-1),low=new Int32Array(total),parent=new Int32Array(total).fill(-1),idx=new Uint8Array(total),stack=[0];
  tin[0]=low[0]=timer++;
  while(stack.length){const x=stack[stack.length-1];if(idx[x]===3){stack.pop();if(parent[x]>=0){const y=parent[x];if(low[x]>tin[y])bridges++;low[y]=Math.min(low[y],low[x])}continue}const y=adj[x][idx[x]++];if(y===parent[x])continue;if(tin[y]>=0){low[x]=Math.min(low[x],tin[y]);continue}parent[y]=x;tin[y]=low[y]=timer++;stack.push(y)}
  assert(timer===total&&bridges===0,"connected bridgeless");
  function evaluate(bits,makeWitness=false){
   let x=0;for(const g of forward)x=apply(g,bits[g.v]??0,x);
   assert(x===3*S.violations(bits),"reversible counter");
   let a0=0,am=marker;for(const g of gates){a0=apply(g,bits[g.v]??0,a0);am=apply(g,bits[g.v]??0,am)}
   assert((a0===marker)===(x===0)&&(am===0)===(x===0),"conjugate swap");
   const selected=Array(total);for(let i=0;i<u;i++)selected[i]=[p[bits[group[i]]??0][i],wire[i]];selected[u]=uEnds;selected[v]=vEnds;
   const seen=new Uint8Array(total),edgeColors=makeWitness?new Map():null,key=(i,j)=>i<j?i*total+j:j*total+i;
   let odd=0,uv=false,cycleCount=0,maxlen=0;
   for(let i=0;i<total;i++)if(!seen[i]){
    const path=[];let cur=i,prev=-1,mark=0;
    do{assert(!seen[cur],"factor cycle");seen[cur]=1;path.push(cur);if(cur===u)mark|=1;if(cur===v)mark|=2;
      const a=selected[cur];assert(a.length===2&&selected[a[0]].includes(cur)&&selected[a[1]].includes(cur),"factor degree");let next=a[0]===prev?a[1]:a[0];prev=cur;cur=next;
    }while(cur!==i);
    cycleCount++;maxlen=Math.max(maxlen,path.length);assert(path.length%2===((mark===1||mark===2)?1:0),"defect parity");
    if(path.length%2)odd++;if(mark===3)uv=true;
    if(edgeColors&&path.length%2===0)path.forEach((a,j)=>edgeColors.set(key(a,path[(j+1)%path.length]),j%2));
   }
   const yes=odd===0;assert(yes===uv&&yes===(x===0),"actual chart iff source sign");
   if(yes&&makeWitness){let ct=0;for(let i=0;i<total;i++){const c=adj[i].map(j=>edgeColors.get(key(i,j))??2);assert(new Set(c).size===3,"whole target 3color");ct+=3}assert(ct===3*total,"target all edges verified");S.lift(bits)}
   return {yes,odd,cycleCount,maxlen,witnessVerified:yes&&makeWitness};
  }
  return {n:total,w,gates:gates.length,active,splices,raw,bridges,evaluate};
 }
 const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const P=[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[5+i,5+(i+2)%5]),...Array.from({length:5},(_,i)=>[i,5+i])];
 const pair=(a,b)=>a[0]===b[0]&&a[1]===b[1]||a[0]===b[1]&&a[1]===b[0];
 const Q=P.filter(e=>!pair(e,[0,4])&&!pair(e,[1,2])).concat([[0,2],[1,4]]);
 const trap=[[0,1],[0,4],[0,5],[1,2],[1,7],[2,3],[2,6],[3,6],[3,7],[4,5],[4,7],[5,6]];
 function expand(E,c){const n=Math.max(...E.flat())+1,v=0,ports=[0,n,n+1],ids=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);assert(ids.length===3,"expand");const out=E.map((e,i)=>ids.includes(i)?e.map(x=>x===v?ports[ids.indexOf(i)]:x):e.slice());const col=c?c.slice():null;for(let i=0;i<3;i++){out.push([ports[(i+1)%3],ports[(i+2)%3]]);if(col)col.push(c[ids[i]])}return {E:out,c:col}}
 const results=[];
 for(const [name,E] of [["K4",K4],["Petersen",P],["Petersen-switch",Q],["CEC06-trap",trap]]){
  const S=source(E),direct=S.direct(),ma=S.matchAudit(),C=compile(S);assert(ma.all_in_out,"source matching support");
  let hits=0,checks=0,lifts=0;
  for(let m=0;m<2**S.n;m++){const bits=Array.from({length:S.n},(_,i)=>(m>>i)&1);for(let dummy=0;dummy<2;dummy++){const b=[...bits,dummy],o=C.evaluate(b,S.violations(bits)===0);checks++;if(o.yes){hits++;if(o.witnessVerified)lifts++}}}
  assert((hits>0)===direct.yes,"independent source decision");
  results.push({name,source_n:S.n,source_yes:direct.yes,source_search_nodes:direct.nodes,source_perfect_matchings:ma.count,source_all_matching_statuses:ma.all_in_out,rows:S.rows.length,target_n:C.n,program_width:C.w,program_gates:C.gates,active_switches:C.active,splices:C.splices,bridges:C.bridges,exhaustive_actual_chart_checks:checks,chart_yes_phase_words:hits,actual_lifts:lifts});
 }
 for(const [name,E] of [["Petersen",P],["Petersen-switch",Q]]){
  const base=source(E).direct();let e=E,c=base.color;
  for(let k=1;k<=16;k++){const next=expand(e,c);e=next.E;c=next.c;if(![4,8,16].includes(k))continue;
   const S=source(e),C=compile(S);if(c)assert(S.checkColor(c),"triangle expansion lift");
   const bits=c?S.sign(c):Array(S.n).fill(0),out=C.evaluate([...bits,0],!!c);assert(out.yes===base.yes,"scale chosen phase outcome");
   let samples=0,sampleHits=0;for(let j=0;j<16;j++){const b=Array.from({length:S.n},(_,i)=>((i*2654435761+j*2246822519+(i^j)*17)>>>((i+j)%23))&1);const o=C.evaluate([...b,j%2],S.violations(b)===0);samples++;if(o.yes)sampleHits++}
   results.push({name:name+"-triangle"+k,source_n:S.n,source_yes:base.yes,source_decision_basis:"triangle retractions to exact base",rows:S.rows.length,target_n:C.n,program_width:C.w,program_gates:C.gates,active_switches:C.active,splices:C.splices,bridges:C.bridges,chosen_phase:out,sampled_actual_charts:samples,sampled_yes:sampleHits});
  }
 }
 return results;
}
console.log(JSON.stringify(auditCEC07(),null,2));

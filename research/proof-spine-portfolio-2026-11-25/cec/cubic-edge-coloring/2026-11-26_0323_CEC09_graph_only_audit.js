function graphOnly(adj, A, u, v) {
 const n=adj.length, ok=(x,m)=>{if(!x)throw Error(m)};
 const W=adj.map((l,i)=>i===u||i===v?-1:l.find(j=>!A[i].includes(j)));
 const key=(a,b)=>a<b?`${a},${b}`:`${b},${a}`;
 const squareMap=new Map();
 for(let a=0;a<n;a++)if(W[a]>=0&&W[a]<n&&W[a]!==u&&W[a]!==v&&a<W[a]){
   const b=W[a];
   for(const c of A[a])for(const d of A[b])if(c!==b&&d!==a&&c!==d&&W[c]===d){
    const list=[a,b,c,d];if(new Set(list).size!==4)continue;
    const k=list.slice().sort((a,b)=>a-b).join(",");
    if(!squareMap.has(k))squareMap.set(k,list);
   }
 }
 const squares=[...squareMap.values()], dummy=new Uint8Array(n), inner=new Int32Array(n).fill(-1);
 for(const [a,b,c,d] of squares){
  for(const x of [a,b,c,d])if(dummy[x])return {status:"UNKNOWN",reason:"overlapping squares"};else dummy[x]=1;
  inner[a]=c;inner[c]=a;inner[b]=d;inner[d]=b;
 }
 const raw=Array.from({length:n},(_,i)=>i).filter(i=>i!==u&&i!==v&&!dummy[i]);
 const outer=(i)=>A[i].find(j=>j!==inner[i]);
 const E=[],RA=Array.from({length:n},()=>[]),RW=new Int32Array(n).fill(-1),pathOwner=new Int32Array(n).fill(-1);
 for(const a of raw)for(const next of A[a]){
   let p=a,x=next,chain=[[p,x]],walked=[];
   while(dummy[x]){
    if(outer(x)!==p)return {status:"UNKNOWN",reason:"nonexternal entry"};
    const y=W[x];if(!dummy[y])return {status:"UNKNOWN",reason:"bad square wire"};
    walked.push(x,y);p=y;x=outer(y);if(x===undefined||walked.length>n)return {status:"UNKNOWN",reason:"bad compressed path"};
    chain.push([p,x]);
   }
   if(x===a||x===u||x===v)return {status:"UNKNOWN",reason:"loop or terminal A"};
   if(a>x)continue;
   const id=E.length;E.push({a,b:x,chain,kind:"A"});RA[a].push(id);RA[x].push(id);
   for(const y of walked){ok(pathOwner[y]===-1,"path overlap");pathOwner[y]=id}
 }
 if(raw.some(i=>RA[i].length!==2)||squares.some(s=>s.some(i=>pathOwner[i]<0)))return {status:"UNKNOWN",reason:"bad residual A"};
 const addW=(a,b,mark=-1)=>{const id=E.length;E.push({a,b,kind:"W",mark});RW[a]=RW[b]=id;return id};
 for(const a of raw)if(W[a]!==u&&W[a]!==v&&a<W[a]){if(dummy[W[a]])return {status:"UNKNOWN",reason:"raw-to-dummy wire"};addW(a,W[a])}
 const endsU=adj[u].filter(x=>x!==v),endsV=adj[v].filter(x=>x!==u);
 if([...endsU,...endsV].some(i=>dummy[i]))return {status:"UNKNOWN",reason:"terminal dummy"};
 const eu=addW(...endsU,u),ev=addW(...endsV,v);
 if(raw.some(i=>RW[i]<0))return {status:"UNKNOWN",reason:"missing wire"};
 const other=(e,i)=>E[e].a===i?E[e].b:E[e].a;
 const bip=new Int8Array(n).fill(-1);
 for(const r of raw)if(bip[r]<0){bip[r]=0;const q=[r];for(let j=0;j<q.length;j++){const a=q[j];for(const id of [...RA[a],RW[a]]){const b=other(id,a);if(bip[b]<0){bip[b]=1-bip[a];q.push(b)}else if(bip[b]===bip[a])return {status:"UNKNOWN",reason:"nonbipartite raw"}}}}
 const cp=new Int32Array(E.length).fill(-1),phase=new Int8Array(E.length).fill(-1);
 let components=0;
 for(let id=0;id<E.length;id++)if(E[id].kind==="A"&&cp[id]<0){const r=components++;cp[id]=r;phase[id]=0;const q=[id];for(let j=0;j<q.length;j++){const e=q[j];for(const a of [E[e].a,E[e].b])for(const f of RA[a])if(f!==e){if(cp[f]<0){cp[f]=r;phase[f]=1-phase[e];q.push(f)}else ok(cp[f]===r&&phase[f]!==phase[e],"raw even A")}}}
 let chosen=null,pathLength=0;
 for(const side of [0,1]){
  const s=endsU.find(a=>bip[a]===side),t=endsV.find(a=>bip[a]!==side);
  const pred=new Int32Array(n).fill(-1),pe=new Int32Array(n).fill(-1),q=[s];pred[s]=s;
  for(let j=0;j<q.length&&pred[t]<0;j++){const a=q[j],opts=bip[a]===side?RA[a]:[RW[a]];for(const id of opts){const b=other(id,a);if(pred[b]<0){pred[b]=a;pe[b]=id;q.push(b)}}}
  if(pred[t]<0)continue;
  const pins=new Int8Array(components).fill(-1);let len=0,conflict=false;
  for(let a=t;a!==s;a=pred[a]){const id=pe[a];if(E[id].kind==="A"){const c=cp[id];if(pins[c]>=0&&pins[c]!==phase[id])conflict=true;pins[c]=phase[id];len++}}
  if(!conflict){chosen=pins;pathLength=len;break}
 }
 if(!chosen)return {status:"UNKNOWN",reason:"no consistent shortest path",raw:raw.length,squares:squares.length};
 const FC=Array.from({length:n},()=>[]),colors=new Int8Array(E.length).fill(2),terminalColors=new Map();
 const FE=[];
 function addF(a,b,id,terminal=-1){const f=FE.length;FE.push({a,b,id,terminal});FC[a].push(f);FC[b].push(f)}
 for(let id=0;id<E.length;id++){const e=E[id];if(e.kind==="A"){if(phase[id]===Math.max(0,chosen[cp[id]]))addF(e.a,e.b,id)}
  else if(e.mark>=0){addF(e.a,e.mark,id,e.a);addF(e.b,e.mark,id,e.b)}else addF(e.a,e.b,id)}
 const visited=new Uint8Array(FE.length);let factorCycles=0;
 for(let f=0;f<FE.length;f++)if(!visited[f]){factorCycles++;let i=f,a=FE[f].a,p=0,len=0;do{
   if(visited[i])return {status:"UNKNOWN",reason:"invalid cycle"};
   visited[i]=1;const e=FE[i];if(e.terminal>=0)terminalColors.set(key(e.terminal,e.mark??(e.a===e.terminal?e.b:e.a)),p);else colors[e.id]=p;
   a=e.a===a?e.b:e.a;ok(FC[a].length===2,"factor degree");i=FC[a].find(j=>j!==i);p^=1;len++;
  }while(i!==f);if(len%2)return {status:"UNKNOWN",reason:"odd factor"};
 }
 const C=new Map();
 function put(a,b,c){const k=key(a,b);if(C.has(k))ok(C.get(k)===c,"inconsistent lift");C.set(k,c)}
 for(let id=0;id<E.length;id++){const e=E[id],c=colors[id];if(e.kind==="A"){for(const [a,b] of e.chain)put(a,b,c)}else if(e.mark<0)put(e.a,e.b,c);else {put(e.a,e.mark,terminalColors.get(key(e.a,e.mark)));put(e.b,e.mark,terminalColors.get(key(e.b,e.mark)))}}
 put(u,v,2);
 for(const [a,b,c,d] of squares){
  const alpha=colors[pathOwner[a]],beta=colors[pathOwner[c]],gamma=[0,1,2].find(i=>i!==alpha&&i!==beta);
  ok(pathOwner[a]===pathOwner[b]&&pathOwner[c]===pathOwner[d],"wire path owner");
  put(a,c,gamma);put(b,d,gamma);put(a,b,3-alpha-gamma);put(c,d,3-beta-gamma);
 }
 for(let i=0;i<n;i++){const cs=adj[i].map(j=>C.get(key(i,j)));ok(cs.every(c=>[0,1,2].includes(c))&&new Set(cs).size===3,"original witness verification")}
 return {status:"YES",raw:raw.length,squares:squares.length,components,pathLength,factorCycles,verifiedEdges:C.size};
}
function auditCEC08(){
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

  // CEC08: independent occurrence phases, without solving the source.
  const fb=[];
  for(const row of S.rows){
   const a=row.filter(Boolean), k=a.length;
   assert(k>=2,"no unary fundamental row");
   let h=0;while(mod(k-2*h,3)!==0)h++;
   assert(h<=k,"row independently satisfiable");
   const b=a.map((c,i)=>+(c!==(i<h?2:1)));
   fb.push(...b,0,...b.slice().reverse());
  }
  const gb=[...fb,0,...fb.slice().reverse()];
  assert(gb.length===gates.length,"occurrence indexing");
  let o=0;for(let i=0;i<forward.length;i++)o=apply(forward[i],fb[i],o);
  assert(o===0,"independent counter zero");
  const raw=total, rU=raw,rV=raw+1, endsU=[0,wire[0]],endsV=[marker,wire[marker]];
  const sel=Array.from({length:raw+2},(_,i)=>i===rU?endsU:i===rV?endsV:[p[gb[Math.floor(i/(2*w))]][i],endsU.includes(i)?rU:endsV.includes(i)?rV:wire[i]]);
  const col=[Array(raw).fill(2),Array(raw).fill(2)], wc=Array(raw).fill(-1);
  const vs=new Uint8Array(raw+2);
  let rawCycles=0;
  for(let i=0;i<raw+2;i++)if(!vs[i]){
   let a=i,prev=-1,j=0;
   do{
    assert(!vs[a],"raw factor walk");vs[a]=1;
    const b=sel[a][0]===prev?sel[a][1]:sel[a][0],color=j%2;
    assert(sel[b].includes(a),"raw factor incidence");
    if(a<raw&&b<raw&&p[gb[Math.floor(a/(2*w))]][a]===b){
     const phase=gb[Math.floor(a/(2*w))];assert(phase===gb[Math.floor(b/(2*w))],"same stage");
     col[phase][a]=col[phase][b]=color;
    }else{if(a<raw)wc[a]=color;if(b<raw)wc[b]=color;}
    prev=a;a=b;j++;
   }while(a!==i);
   assert(j%2===0,"independent raw even factor");rawCycles++;
  }
  for(let i=0;i<raw;i++)assert(new Set([col[0][i],col[1][i],wc[i]]).size===3,"raw proper incidence");
  assert(wc[endsU[0]]!==wc[endsU[1]]&&wc[endsV[0]]!==wc[endsV[1]],"raw terminals");
  const rawUColor=wc[endsU[0]]+wc[endsU[1]],rawVColor=wc[endsV[0]]+wc[endsV[1]];
  assert(rawUColor===1&&rawVColor===1,"raw defect color 2");
  const seen=new Uint8Array(total);let splices=0,cycles=0,active=0;

  for(let v=0;v<members.length;v++){
   const reps=[];
   for(const x of members[v])if(!seen[x]){reps.push(x);let y=x,b=0;do{seen[y]=1;y=p[b][y];b^=1}while(y!==x||b!==0)}
   if(!reps.length)continue;active++;cycles+=reps.length;
   let a=reps[0];
   for(const c of reps.slice(1)){
    const b=p[0][a],d=p[0][c],x=total++,y=total++,r=total++,s=total++;splices++;
    const ca=col[0][a],cc=col[0][c];assert(ca===col[0][b]&&cc===col[0][d],"old seam colors");
    const mid=[0,1,2].find(t=>t!==ca&&t!==cc);
    col[0][x]=col[0][y]=ca;col[0][r]=col[0][s]=cc;
    for(const i of [x,y,r,s])col[1][i]=mid;
    wc[x]=wc[y]=3-ca-mid;wc[r]=wc[s]=3-cc-mid;
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
  const recovered=graphOnly(adj,Array.from({length:total},(_,i)=>i>=u?[]:[p[0][i],p[1][i]].sort((a,b)=>a-b)),u,v); assert(recovered.status==='YES','graph-only escape '+JSON.stringify(recovered)); assert(recovered.squares===splices&&recovered.raw===raw,'exact splice detection');
  // Direct verification on actual compiled simple cubic target, no source solution.
  for(let i=0;i<u;i++){
   assert(new Set([col[0][i],col[1][i],wc[i]]).size===3,"ungarded color incidence");
   for(let b=0;b<2;b++)assert(col[b][i]===col[b][p[b][i]],"phase edge color consistency");
   if(wire[i]<u)assert(wc[i]===wc[wire[i]],"wire color consistency");
  }
  assert(new Set([...uEnds.map(i=>wc[i]),2]).size===3&&new Set([...vEnds.map(i=>wc[i]),2]).size===3,"terminal color incidence");
  // FP14 raw group-cut audit, before common-transition suppression.
  const cs=Array(n+1).fill(0), between=new Map();
  for(let i=0;i<u;i++)if(wire[i]>=u)cs[group[i]]++;else if(group[i]!==group[wire[i]]){
   cs[group[i]]++;const a=group[i],b=group[wire[i]];
   if(a<b){const k=a*(n+1)+b;between.set(k,(between.get(k)||0)+1)}
  }
  const minSingle=Math.min(...cs.filter(x=>x>0));
  let minPair=Infinity;
  for(const [k,v] of between){const a=Math.floor(k/(n+1)),b=k%(n+1);minPair=Math.min(minPair,cs[a]+cs[b]-2*v)}
  assert(minSingle>=2*w-2&&minPair>=2*w-2&&minPair>4,"no raw FP14 merge");
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
  return {n:total,w,gates:gates.length,active,splices,raw,bridges,evaluate,ungardedColorVerified:true,rawCycles,minSingle,minPair,recovered};
 }
 const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const P=[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[5+i,5+(i+2)%5]),...Array.from({length:5},(_,i)=>[i,5+i])];
 const pair=(a,b)=>a[0]===b[0]&&a[1]===b[1]||a[0]===b[1]&&a[1]===b[0];
 const Q=P.filter(e=>!pair(e,[0,4])&&!pair(e,[1,2])).concat([[0,2],[1,4]]);
 const trap=[[0,1],[0,4],[0,5],[1,2],[1,7],[2,3],[2,6],[3,6],[3,7],[4,5],[4,7],[5,6]];
 function expand(E,c){const n=Math.max(...E.flat())+1,v=0,ports=[0,n,n+1],ids=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);assert(ids.length===3,"expand");const out=E.map((e,i)=>ids.includes(i)?e.map(x=>x===v?ports[ids.indexOf(i)]:x):e.slice());const col=c?c.slice():null;for(let i=0;i<3;i++){out.push([ports[(i+1)%3],ports[(i+2)%3]]);if(col)col.push(c[ids[i]])}return {E:out,c:col}}

 const results=[];
 for(const [name,E] of [["K4",K4],["Petersen",P],["Petersen-switch",Q],["CEC06-trap",trap]]){
 const S=source(E),d=S.direct(),m=S.matchAudit(),C=compile(S);assert(m.all_in_out,"ordinary matching support");
 results.push({name,source_n:S.n,source_yes:d.yes,target_n:C.n,gates:C.gates,splices:C.splices,...C.recovered});
 }
 for(const [name,E] of [["Petersen",P],["Petersen-switch",Q]]){
 const base=source(E).direct();let e=E,c=base.color;
 for(let k=1;k<=16;k++){const next=expand(e,c);e=next.E;c=next.c;if(![4,8,16].includes(k))continue;
 const S=source(e),C=compile(S);results.push({name:name+"-triangle"+k,source_n:S.n,source_yes:base.yes,target_n:C.n,gates:C.gates,splices:C.splices,...C.recovered});
 }}
 return results;
}

console.log(JSON.stringify(auditCEC08(),null,2));

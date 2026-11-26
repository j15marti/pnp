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

function extraAudit(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const P=[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[5+i,5+(i+2)%5]),...Array.from({length:5},(_,i)=>[i,5+i])];
 const pair=(a,b)=>a.includes(b[0])&&a.includes(b[1]);
 const Q=P.filter(e=>!pair(e,[0,4])&&!pair(e,[1,2])).concat([[0,2],[1,4]]);
 const prism=[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[5+i,5+(i+1)%5]),...Array.from({length:5},(_,i)=>[i,5+i])];
 const trap=[[0,1],[0,4],[0,5],[1,2],[1,7],[2,3],[2,6],[3,6],[3,7],[4,5],[4,7],[5,6]];
 const K4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 function direct(E,n){const used=Array(n).fill(0);function dfs(i){if(i===E.length)return true;const [a,b]=E[i];for(let c=0;c<3;c++)if(!((used[a]|used[b])&(1<<c))){used[a]^=1<<c;used[b]^=1<<c;if(dfs(i+1))return true;used[a]^=1<<c;used[b]^=1<<c}return false}return dfs(0)}
 const results=[];
 for(const [name,E] of [["Petersen",P],["Petersen-switch",Q],["prism",prism],["trap",trap],["K4",K4]]){
 const n=Math.max(...E.flat())+1,adj=Array.from({length:n},()=>[]);for(const [a,b] of E){adj[a].push(b);adj[b].push(a)}
 const exact=direct(E,n),counts={},status={YES:0,UNKNOWN:0},permuted={YES:0,UNKNOWN:0};let charts=0;
 for(const [u,v] of E){
  const rest=E.filter(e=>!e.includes(u)&&!e.includes(v));
  for(let mask=0;mask<2**rest.length;mask++){
   const A=Array.from({length:n},()=>[]);
   for(let i=0;i<rest.length;i++)if(mask>>i&1){const [a,b]=rest[i];A[a].push(b);A[b].push(a)}
   if(A.some((l,i)=>l.length!==((i===u||i===v)?0:2)))continue;
   const seen=new Set();let good=true;
   for(let i=0;i<n;i++)if(i!==u&&i!==v&&!seen.has(i)){let p=-1,x=i,len=0;do{seen.add(x);const y=A[x].find(z=>z!==p);p=x;x=y;len++}while(x!==i);if(len%2)good=false}
   if(!good)continue;
   charts++;let a;
   try{a=graphOnly(adj,A,u,v)}catch(e){a={status:"UNKNOWN",reason:"rejected candidate: "+String(e)}}
   check(a.status!=="YES"||exact,"false global YES");
   status[a.status]++;counts[a.reason??"verified"]=(counts[a.reason??"verified"]||0)+1;
   const pi=Array.from({length:n},(_,i)=>n-1-i),aa=Array.from({length:n},()=>[]),bb=Array.from({length:n},()=>[]);
   for(let i=0;i<n;i++){aa[pi[i]]=adj[i].slice().reverse().map(j=>pi[j]);bb[pi[i]]=A[i].slice().reverse().map(j=>pi[j])}
   let b;try{b=graphOnly(aa,bb,pi[u],pi[v])}catch(e){b={status:"UNKNOWN"}}
   check(b.status!=="YES"||exact,"permuted false global YES");permuted[b.status]++;
  }
 }
 results.push({name,n,exact,charts,status,permuted,counts});
 }
 return results;
}

console.log(JSON.stringify(extraAudit(),null,2));

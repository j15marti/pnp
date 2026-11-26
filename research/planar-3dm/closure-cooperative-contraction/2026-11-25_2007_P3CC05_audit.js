console.log(JSON.stringify((function audit() {
 const stats={assertions:0,matching_calls:0,bond_tests:0,reverse_switches:0,source_jobs:0,abstract_jobs:0,closure_jobs:0,closure_no:0,closure_stable:0,complete_comparisons:0};
 function ok(x,m){stats.assertions++;if(!x)throw Error(m)}
 const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
 const xor=a=>a.reduce((x,y)=>x^y,0n), full=n=>bit(n)-1n;
 const pop=x=>{let k=0;while(x){k++;x&=x-1n}return k};
 const sorted=s=>[...s].map(String).sort().join(",");
 function span(v){let a=new Set([0n]);for(const b of v)for(const x of [...a])a.add(x^b);return a}
 function nullspace(rows,V) {
  let a=rows.map(x=>x), k=0,piv=[];
  for(const j of V){let i=a.findIndex((r,i)=>i>=k&&(r&bit(j))!==0n);if(i<0)continue;
   [a[k],a[i]]=[a[i],a[k]];for(let l=0;l<a.length;l++)if(l!==k&&(a[l]&bit(j)))a[l]^=a[k];
   piv.push(j);k++;
  }
  return V.filter(j=>!piv.includes(j)).map(j=>bit(j)^xor(piv.filter((p,i)=>a[i]&bit(j)).map(bit)));
 }
 function matching(n,E) {
  stats.matching_calls++;let adj=Array.from({length:n},()=>[]);for(const e of E)adj[e.x].push(e);
  let used=Array(n).fill(null);
  function aug(x,seen){for(const e of adj[x]){if(seen[e.y])continue;seen[e.y]=true;
   if(!used[e.y]||aug(used[e.y].x,seen)){used[e.y]=e;return true}
  }return false}
  for(let x=0;x<n;x++)if(!aug(x,Array(n).fill(false)))return null;
  return used.sort((a,b)=>a.x-b.x);
 }
 const pin=(E,e)=>E.filter(f=>f===e||(f.x!==e.x&&f.y!==e.y));
 function allmatch(n,E){const a=Array.from({length:n},()=>[]);E.forEach(e=>a[e.x].push(e));const out=[];
  function rec(x,seen,M){if(x===n){out.push(M.slice());return}for(const e of a[x])if(!(seen&bit(e.y))){M.push(e);rec(x+1,seen|bit(e.y),M);M.pop()}}
  rec(0,0n,[]);return out;
 }
 function capped(n,E,K){const out=[];let overflow=false;
  function rec(i,F,P){if(overflow)return;if(i===n){out.push(P.slice());if(out.length>K)overflow=true;return}
   for(const e of F.filter(e=>e.x===i)){const next=pin(F,e);if(matching(n,next)){P.push(e);rec(i+1,next,P);P.pop()}if(overflow)return}
  }
  if(matching(n,E))rec(0,E,[]);return overflow?null:out;
 }
 const indexed=T=>T.map((t,id)=>({t,id}));
 function lane(T,k){const a=[0,1,2].filter(j=>j!==k);return T.map(({t,id})=>({x:t[a[0]],y:t[a[1]],z:t[k],id}))}
 function close(n,T) {
  stats.closure_jobs++;let A=indexed(T);
  for(;;){let old=A.length;
   for(let k=0;k<3;k++)for(let v=0;v<n;v++){
    const E=A.filter(e=>e.t[k]===v);if(!E.length){stats.closure_no++;return null}
    if(E.length===1){const p=E[0];A=A.filter(e=>e===p||e.t.every((a,j)=>a!==p.t[j]))}
   }
   for(let k=0;k<3;k++){
    const E=lane(A,k);if(!matching(n,E)){stats.closure_no++;return null}
    const ids=new Set(E.filter(e=>matching(n,pin(E,e))).map(e=>e.id));A=A.filter(e=>ids.has(e.id))
   }
   const m=A.length,rows=[];for(let k=0;k<3;k++)for(let v=0;v<n;v++)rows.push(bit(m)^xor(A.map((e,i)=>e.t[k]===v?bit(i):0n)));
   let p=0;for(let j=0;j<m;j++){let i=rows.findIndex((r,i)=>i>=p&&(r&bit(j)));if(i<0)continue;[rows[p],rows[i]]=[rows[i],rows[p]];for(let k=0;k<rows.length;k++)if(k!==p&&(rows[k]&bit(j)))rows[k]^=rows[p];p++}
   if(rows.includes(bit(m))){stats.closure_no++;return null}
   let force=[];for(const r of rows){const a=r&full(m);if(pop(a)===1){let j=0;while(!(a&bit(j)))j++;force.push([A[j],Boolean(r&bit(m))])}}
   for(const [e,b] of force)if(!b)A=A.filter(f=>f!==e);else A=A.filter(f=>f===e||f.t.every((a,j)=>a!==e.t[j]));
   if(A.length===old){if(old===T.length)stats.closure_stable++;return A}
  }
 }
 function bundles(E){const B=new Map();for(const e of E){const key=e.x+","+e.y;if(!B.has(key))B.set(key,[]);B.get(key).push(e)}return [...B.values()]}
 function classes(E){let C=[],pairs=[],lookup=new Map();
  for(const B of bundles(E)){B.sort((a,b)=>a.z-b.z||a.id-b.id);for(let j=0;j<B.length;j+=2){const A=B.slice(j,j+2);let type=-1,delta=0n;
   if(A.length===2&&A[0].z!==A[1].z){let u=A[0].z,v=A[1].z,key=u+","+v;if(!lookup.has(key)){lookup.set(key,pairs.length);pairs.push({u,v,id:pairs.length})}type=lookup.get(key);delta=bit(u)^bit(v)}
   C.push({x:A[0].x,y:A[0].y,alts:A,type,delta,id:C.length})
  }}return {C,pairs};
 }
 function blocks(n,P){let adj=Array.from({length:n},()=>[]);P.forEach(e=>{adj[e.u].push([e.v,e.id]);adj[e.v].push([e.u,e.id])});
  let d=Array(n).fill(0),low=Array(n).fill(0),stack=[],out=[],tick=0;
  function dfs(u,pe){d[u]=low[u]=++tick;for(const [v,i] of adj[u]){if(i===pe)continue;if(!d[v]){stack.push(i);dfs(v,i);low[u]=Math.min(low[u],low[v]);if(low[v]>=d[u]){let b=[],j;do{j=stack.pop();b.push(P[j])}while(j!==i);out.push(b)}}else if(d[v]<d[u]){stack.push(i);low[u]=Math.min(low[u],d[v])}}}
  for(let u=0;u<n;u++)if(!d[u])dfs(u,-1);return out;
 }
 function bonds(B,cap){const V=[...new Set(B.flatMap(e=>[e.u,e.v]))].sort((a,b)=>a-b), Vmask=xor(V.map(bit));
  const connected=(mask,ban=new Set())=>{let v=V.find(v=>mask&bit(v));if(v===undefined)return false;let seen=bit(v),q=[v];while(q.length){const x=q.pop();for(const e of B){if(ban.has(e.id))continue;let y=e.u===x?e.v:e.v===x?e.u:-1;if(y>=0&&(mask&bit(y))&&!(seen&bit(y))){seen|=bit(y);q.push(y)}}}return seen===mask}
  let deg=V.map(v=>B.filter(e=>e.u===v||e.v===v).length),out=[];
  if(B.length===1)out.push({shore:bit(B[0].u),ban:new Set([B[0].id])});
  else if(B.length===V.length&&deg.every(x=>x===2)){
   for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){const ban=new Set([B[i].id,B[j].id]);let shore=bit(V[0]),q=[V[0]];while(q.length){let x=q.pop();for(const e of B){if(ban.has(e.id))continue;let y=e.u===x?e.v:e.v===x?e.u:-1;if(y>=0&&!(shore&bit(y))){shore|=bit(y);q.push(y)}}}ok(shore!==Vmask,"cycle cut not disconnected");out.push({shore,ban})}
  }else if(V.length<=cap){
   for(let i=1;i<2**V.length-1;i+=2){let shore=xor(V.filter((v,j)=>i&(1<<j)).map(bit));if(connected(shore)&&connected(Vmask^shore)){let ban=new Set(B.filter(e=>Boolean(shore&bit(e.u))!==Boolean(shore&bit(e.v))).map(e=>e.id));out.push({shore,ban})}}
  }else return {V,Vmask,out:null};
  return {V,Vmask,out};
 }
 function robust(n,E,cap=9){const {C,pairs}=classes(E);if(!matching(n,C))return null;let H=[],count=0,skipped=0,details=[];
  for(const B of blocks(n,pairs)){
   const {V,Vmask,out}=bonds(B,cap);if(!out){skipped++;continue}
   let rows=[Vmask], absent=0;
   for(const {shore,ban} of out){count++;stats.bond_tests++;if(matching(n,C.filter(e=>!ban.has(e.type)))){rows.push(shore);absent++}}
   const basis=nullspace(rows,V);H.push(...basis);details.push({vertices:V.length,bonds:out.length,absent,rank:basis.length})
  }
  return {H,C,pairs,count,skipped,details};
 }
 function actual(M){return M.map(e=>e.alts[0])}
 const sig=M=>xor(M.map(e=>bit(e.z)));
 function lift(M,p){let A=new Map();
  for(let i=0;i<M.length;i++){let v=M[i].delta,w=bit(i);while(v){let j=v.toString(2).length-1;if(A.has(j)){let [u,t]=A.get(j);v^=u;w^=t}else{A.set(j,[v,w]);break}}}
  let v=p,w=0n;while(v){let j=v.toString(2).length-1;if(!A.has(j))throw Error("unliftable direction");let [u,t]=A.get(j);v^=u;w^=t}
  let out=M.map((e,i)=>e.alts[(w&bit(i))?1:0]);stats.reverse_switches+=pop(w);
  ok(out.every(Boolean),"missing paired alternative");ok(new Set(out.map(e=>e.x)).size===M.length&&new Set(out.map(e=>e.y)).size===M.length,"matching lost");ok(sig(out)=== (sig(actual(M))^p),"wrong lift");return out;
 }
 function check(n,T,kind,record=false){stats[kind==="source"?"source_jobs":"abstract_jobs"]++;const E=lane(indexed(T),2),R=robust(n,E);
  const orig=allmatch(n,E), S=new Set(orig.map(sig));if(!R){ok(!orig.length,"false empty");return null}
  const Ms=allmatch(n,R.C);let H=span(R.H),expected=new Set(Array.from({length:2**n},(_,i)=>BigInt(i))), direct=null;
  for(const M of Ms){const D=span(M.map(e=>e.delta));expected=new Set([...expected].filter(x=>D.has(x)));let ds=new Set(M.map(e=>e.delta).filter(x=>x));direct=direct===null?ds:new Set([...direct].filter(x=>ds.has(x)));
   for(const p of R.H)lift(M,p);lift(M,xor(R.H));
  }
  if(!R.skipped){ok(sorted(H)===sorted(expected),"intersection differs");stats.complete_comparisons++}
  for(const p of H)for(const s of S)ok(S.has(s^p),"false semantic period");
  let yes=S.has(full(n));if(kind==="source"){const F=close(n,T);if(!F)ok(!yes,"false closure NO");else ok(allmatch(n,lane(F,2)).some(m=>sig(m)===full(n))===yes,"closure changed truth")}
  return record?{T,rank:R.H.length,direct:direct.size,H:R.H.map(String),support:[...S].map(String).sort((a,b)=>+a-+b),skeletons:Ms.length,yes,bonds:R.count,complete:!R.skipped}:null;
 }
 function hallTerminal(n,T,K){const E=lane(indexed(T),2);const B=bundles(E).map((A,id)=>({x:A[0].x,y:A[0].y,A,id}));const M=capped(n,B,K);if(M===null)return {status:"UNKNOWN"};
  for(const Q of M){const J=Q.flatMap((e,i)=>e.A.map(a=>({x:i,y:a.z,orig:a})));const W=matching(n,J);
   if(W){const out=W.map(e=>e.orig);ok(new Set(out.map(e=>e.x)).size===n&&new Set(out.map(e=>e.y)).size===n&&new Set(out.map(e=>e.z)).size===n,"bad Hall lift");return {status:"YES",skeletons:M.length,witness:out.map(e=>e.id)}}
  }return {status:"NO",skeletons:M.length};
 }
 function ring(n,bad){let T=[];for(let i=0;i<n;i++)if(i%2===0){T.push([i,i,i],[i,i,i+1],[i,(i+1)%n,i+1],[i,(i+1)%n,(i+2)%n])}else{T.push([i,i,(bad&&i===1?i:i+1)%n],[i,(i+1)%n,(bad&&i===1?i+2:i+1)%n])}return T}
 function k2(k){let T=[];for(let i=0;i<k;i++){let x=2*i,z=i+2,d=i===0?0:i===1?1:k+i;T.push([x,x,0],[x,x,z],[x,x+1,1],[x,x+1,z],[x+1,x,d],[x+1,x+1,d])}return T}
 const U=[[0,0,0],[0,1,2],[0,1,0],[1,1,0],[1,1,1],[1,2,1],[1,2,3],[2,2,1],[2,3,2],[3,3,3],[3,3,2],[3,0,2]], V=[...U,[0,0,2]];
 const W=[[0,0,2],[0,0,0],[0,1,1],[0,1,0],[1,1,0],[1,2,3],[2,2,3],[2,2,1],[2,3,1],[3,3,2],[3,3,3],[3,0,0]];
 let fixtures=[check(4,U,"source",true),check(4,V,"source",true),check(4,W,"source",true)];
 ok(fixtures[0].rank===1&&fixtures[0].H[0]==="15"&&fixtures[0].direct===0&&!fixtures[0].yes,"U fixture");ok(fixtures[1].yes,"V fixture");ok(fixtures[2].rank===1&&fixtures[2].direct===0&&fixtures[2].yes,"W fixture");
 let seed=20261125;const rng=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/4294967296};
 for(let i=0;i<180;i++){let base=i%3===0?V:i%3===1?U:ring(6,false),n=i%3===2?6:4;check(n,base.filter(()=>rng()>.14),"source")}
 for(let i=0;i<240;i++){let n=3+(i%4),T=[];for(let x=0;x<n;x++)for(let y=0;y<n;y++)if(rng()<.32||x===y){let k=1+Math.floor(rng()*Math.min(3,n)),Z=new Set();while(Z.size<k)Z.add(Math.floor(rng()*n));for(const z of Z)T.push([x,y,z])}check(n,T,"abstract")}
 let scalable=[];
 for(const n of [4,8,16,32,64])for(const bad of [false,true]){
  const T=ring(n,bad),R=robust(n,lane(indexed(T),2)),M=matching(n,R.C);ok(R.skipped===0&&R.H.length===1&&R.H[0]===full(n),"ring period");lift(M,R.H[0]);
  const terminal=hallTerminal(n,T,2);ok(terminal.status===(bad?"NO":"YES"),"ring Hall");
  scalable.push({n,triples:T.length,bad,bonds:R.count,rank:R.H.length,raw_support:String((bit(n/2)*2n)-2n),terminal:terminal.status,skeletons:terminal.skeletons});
 }
 const F=close(4,U),G=close(4,V),J=close(4,W);ok(F&&F.length===U.length,"U closure stable");ok(J&&J.length===W.length,"W closure stable");
 let bondObstructions=[];
 for(const k of [3,5,8,16,32]){const T=k2(k),R=robust(2*k,lane(indexed(T),2));ok(R.pairs.length===2*k,"K2,k shape");if(k<=7)ok(R.count>=2**k,"K2,k bonds");else ok(R.skipped===1,"cap not honored");ok(hallTerminal(2*k,T,2**Math.min(k,4)).status===(k<=4?"YES":"UNKNOWN"),"capped skeleton terminal");bondObstructions.push({k,triples:T.length,bond_lower_bound:String(bit(k)),enumerated:R.count,skipped:R.skipped})}
 // Exact partition into disjoint incidence blocks; no product of their skeleton lists.
 let products=[];
 for(const g of [1,4,16,64]){const T=Array.from({length:g},(_,i)=>W.map(t=>t.map(x=>x+4*i))).flat(),R=robust(4*g,lane(indexed(T),2));ok(R.H.length===g,"additive blocks");const M=matching(4*g,R.C);lift(M,xor(R.H));products.push({g,n:4*g,triples:T.length,rank:R.H.length,bonds:R.count,skeleton_count:String(bit(g)),raw_support:String(bit(3*g))})}
 return {stats,fixtures,closure:{U:F.length,V:G?G.length:null,W:J.length},scalable,bondObstructions,products,notes:"Source controls are subsets of planar fixtures, ring and K2,k planarity separately checked; abstract controls are not asserted planar. Ring raw support formula proved in report. Full LP pin closure not implemented."};
})(),null,2));

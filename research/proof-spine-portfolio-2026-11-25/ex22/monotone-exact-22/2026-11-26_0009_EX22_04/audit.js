const audit = function(){
 const mod=x=>((x%3)+3)%3; let checks=0; const ok=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
 function rank(rows,n){let a=rows.map(r=>Array.from(r,mod)), k=0;for(let j=0;j<n&&k<a.length;j++){let i=k;while(i<a.length&&!a[i][j])i++;if(i===a.length)continue;[a[i],a[k]]=[a[k],a[i]];let p=a[k][j];for(let l=j;l<n;l++)a[k][l]=mod(a[k][l]*p);for(let i=k+1;i<a.length;i++){let p=a[i][j];if(p)for(let l=j;l<n;l++)a[i][l]=mod(a[i][l]-p*a[k][l])}k++}return k}
 function compile(n,E){
  const edges=[], ids=new Map(), cycles=[], lists=Array.from({length:n},()=>[]);let h=n, V=n+1;
  function edge(a,b){let key=[Math.min(a,b),Math.max(a,b)].join(",");if(!ids.has(key)){ids.set(key,edges.length);edges.push([Math.min(a,b),Math.max(a,b)])}return ids.get(key)}
  for(const [v,w] of E){let a=V++,b=V++;lists[v].push(a);lists[w].push(b);edge(v,w);edge(h,a);edge(a,v);edge(h,b);edge(b,w);edge(a,b);cycles.push([h,a,b],[v,w,b,a]);}
  for(let v=0;v<n;v++)for(let i=1;i<lists[v].length;i++)cycles.push([h,lists[v][i-1],v,lists[v][i]]);
  const C=[];for(let e=0;e<edges.length;e++)for(let i=0;i<6;i++)C.push(Array.from({length:6},(_,j)=>6*e+j).filter((_,j)=>j!==i&&j!==(i+1)%6));
  for(const c of cycles){let row=[];for(let i=0;i<c.length;i++){let u=c[i],v=c[(i+1)%c.length],e=edge(u,v),p=u<v?0:1;if(c.length===3&&i===2){row.push(6*e+1-p,6*e+3-p)}else row.push(6*e+p)}C.push(row)}
  return {n,E,V,h,edges,C,cycles,lists};
 }
 function color(n,E){let a=Array(n).fill(-1);function rec(i){if(i===n)return a.slice();for(let t=0;t<3;t++){if(E.every(([v,w])=>v!==i&&w!==i||a[v===i?w:v]!==t)){a[i]=t;let r=rec(i+1);if(r)return r;a[i]=-1}}return null}return rec(0)}
 function lift(F,a){let c=a.slice();c[F.h]=0;for(let i=0;i<F.E.length;i++){let [v,w]=F.E[i],p=F.n+1+2*i,q=p+1;for(let t=1;t<=2;t++)if(t!==c[v]&&3-t!==c[w]){c[p]=t;c[q]=3-t;break}ok(c[p]!==undefined&&c[q]!==undefined)}let s=F.edges.flatMap(([v,w])=>{let d=mod(c[w]-c[v]);ok(d!==0);return Array.from({length:6},(_,j)=>mod(d*(j%2?-1:1))===1?1:0)});ok(F.C.every(r=>r.reduce((z,i)=>z+s[i],0)===2));return s}
 function closure(C,n,pins=[]){let a=Array(n).fill(-1);for(const [i,b] of pins)a[i]=b;let changed=true;while(changed){changed=false;for(const r of C){let t=r.filter(i=>a[i]===1).length,u=r.filter(i=>a[i]===-1);if(t>2||t+u.length<2)return null;if(t===2||t+u.length===2)for(let i of u){a[i]=t===2?0:1;changed=true}}}return a}
 function validate(F,doRank=true){let n=6*F.edges.length,degree=Array(n).fill(0);ok(F.C.every(r=>r.length===4&&new Set(r).size===4&&r.every(i=>i>=0&&i<n)));ok(new Set(F.C.map(r=>r.slice().sort((a,b)=>a-b).join(","))).size===F.C.length);for(let r of F.C)for(let i of r)degree[i]++;ok(Math.max(...degree,0)<=7);for(let r of F.C){let z=Array(F.V).fill(0);for(let i of r){let [v,w]=F.edges[Math.floor(i/6)],s=i%2?-1:1;z[v]-=s;z[w]+=s}ok(z.every(x=>mod(x)===0))}
  let expected=F.V-1; // all original vertices in controls nonisolated
  if(doRank){let R=F.C.map(r=>{let a=new Uint8Array(n);for(let i of r)a[i]=1;return a});ok(n-rank(R,n)===expected)}
  ok(closure(F.C,n)!==null);return Math.max(...degree,0)}
 // Matching necessary condition: original variable copies paired by occurrence order.
 // Edmonds cardinality blossom, unweighted simple graph. All failed probes charged.
 function pm(C,n,pins){const a=closure(C,n,pins);if(!a)return false;
  const adj=[], addV=()=>{adj.push([]);return adj.length-1},link=(v,w)=>{adj[v].push(w);adj[w].push(v)};
  let occ=Array.from({length:n},()=>[]), forbidden=new Set(), forced=[], dummy=[];
  for(let r of C){let p=r.map(i=>{let v=addV();occ[i].push(v);return v}),u=addV(),v=addV();for(let w of p){link(u,w);link(v,w)}}
  function install(i,u,v){if(a[i]===0)return;link(u,v);if(a[i]===1)forced.push([u,v])}
  for(let i=0;i<n;i++){let p=occ[i];for(let j=0;j+1<p.length;j+=2)install(i,p[j],p[j+1]);if(p.length%2){let d=addV();dummy.push(d);install(i,p[p.length-1],d)}}
  if(dummy.length%2)dummy.push(addV());for(let i=0;i<dummy.length;i++)for(let j=0;j<i;j++)link(dummy[i],dummy[j]);
  for(let [u,v] of forced){if(forbidden.has(u)||forbidden.has(v))return false;forbidden.add(u);forbidden.add(v)}
  let N=adj.length,match=Array(N).fill(-1);
  function path(root){let p=Array(N).fill(-1),b=Array.from({length:N},(_,i)=>i),used=Array(N).fill(false),q=[root];used[root]=true;
   function lca(a,c){let seen=Array(N).fill(false);while(true){a=b[a];seen[a]=true;if(match[a]===-1)break;a=p[match[a]]}while(true){c=b[c];if(seen[c])return c;c=p[match[c]]}}
   function mark(v,k,u,B){while(b[v]!==k){B[b[v]]=B[b[match[v]]]=true;p[v]=u;u=match[v];v=p[match[v]]}}
   for(let head=0;head<q.length;head++){let v=q[head];for(let u of adj[v]){if(forbidden.has(u)||b[u]===b[v]||match[v]===u)continue;if(u===root||match[u]!==-1&&p[match[u]]!==-1){let k=lca(v,u),B=Array(N).fill(false);mark(v,k,u,B);mark(u,k,v,B);for(let i=0;i<N;i++)if(B[b[i]]){b[i]=k;if(!used[i]){used[i]=true;q.push(i)}}}else if(p[u]===-1){p[u]=v;if(match[u]===-1){let x=u;while(x!==-1){let y=p[x],z=y===-1?-1:match[y];match[x]=y;if(y!==-1)match[y]=x;x=z}return true}u=match[u];used[u]=true;q.push(u)}}}return false}
  for(let i=0;i<N;i++)if(!forbidden.has(i)&&match[i]===-1)path(i);
  return match.every((v,i)=>forbidden.has(i)||v!==-1);
 }
 let counts={graphJobs:0,yes:0,no:0,rankChecks:0,matchingCalls:0,pins:0},neighbors=[];
 // Exhaustively enumerate graphs on four labelled vertices with no isolates.
 for(let mask=0;mask<64;mask++){let E=[],j=0;for(let u=0;u<4;u++)for(let v=u+1;v<4;v++,j++)if(mask>>j&1)E.push([u,v]);if(Array.from({length:4},(_,i)=>i).some(i=>!E.some(e=>e.includes(i))))continue;
 let F=compile(4,E),a=color(4,E);validate(F);counts.graphJobs++;counts.rankChecks++;if(a){counts.yes++;lift(F,a)}else counts.no++;
 }
 // K4 and edge-deleted neighbors connected by bridges; every NO contains a K4.
 for(let k of [1,2,4,8,16])for(let bad of [false,true]){let E=[];for(let b=0;b<k;b++){for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)if((u!==0||v!==1)||(bad&&b===0))E.push([4*b+u,4*b+v]);if(b)E.push([4*b-1,4*b])}let F=compile(4*k,E),deg=validate(F,k<=4);if(k<=4)counts.rankChecks++;if(!bad){let a=[];for(let b=0;b<k;b++){let p=b%2?1:0;a.push(p,p,1-p,2)}lift(F,a)}else ok(E.filter(([u,v])=>u<4&&v<4).length===6);
 let root=null,failed=0;if(k===1){let n=6*F.edges.length;root=pm(F.C,n,[]);counts.matchingCalls++;ok(root);for(let i=0;i<n;i+=6)for(let b of [0,1]){counts.pins++;counts.matchingCalls++;if(!pm(F.C,n,[[i,b]]))failed++} // repeat at stagnation if no deductions
 if(failed===0){ok(pm(F.C,n,[]));counts.matchingCalls++}}
 neighbors.push({k,bad,variables:6*F.edges.length,clauses:F.C.length,degree:deg,rankExecuted:k<=4,rootMatching:root,failedRepresentativePins:failed})}
 return {counts,neighbors,checks};
};
console.log(JSON.stringify(audit(),null,2));

function BH13(){
const L={scans:0,pins:0,gauss:0,matching:0,matchVertices:0,matchEdges:0,edgeVisits:0,regionQueries:0,declines:0,branches:0,referenceWords:0,checks:0};
const check=(q)=>{L.checks++;if(!q)throw Error("assertion "+L.checks)};
const ok=(F,x)=>F.every(o=>{let t=o.a.reduce((s,[v,b])=>s+(x[v]^b),0);return o.l<=t&&t<=o.u});
const own=(a,l=1,u=a.length-1)=>({a:a.map(v=>Array.isArray(v)?v:[v,0]),l,u});
function close(F,n,init={}){
 let p={...init};
 for(;;){
  L.scans++;let R=[],newpin=null,eq=[];
  for(const o of F){
   let l=o.l,u=o.u,a=[];
   for(const [v,s] of o.a){if(v in p){l-=p[v]^s;u-=p[v]^s}else a.push([v,s])}
   l=Math.max(0,l);u=Math.min(a.length,u);if(l>u)return null;
   if(l===0&&u===a.length)continue;
   R.push({a,l,u});
   if(u===0||l===a.length){const [v,s]=a[0];newpin=[v,(u===0?0:1)^s];break}
   if(l===u){let mask=0n,b=l%2;for(const [v,s] of a){mask^=1n<<BigInt(v);b^=s}eq.push([mask,b])}
  }
  if(!newpin){
   let basis=new Map();
   for(let [m,b] of eq){for(let i=0;i<n&&m;i++){let bit=1n<<BigInt(i);if(!(m&bit))continue;if(basis.has(i)){let [z,c]=basis.get(i);m^=z;b^=c;L.gauss++}else{basis.set(i,[m,b]);break}}
    if(!m&&b)return null;
   }
   let keys=[...basis.keys()].sort((a,b)=>b-a);
   for(let i of keys){let [m,b]=basis.get(i);for(let j of keys){if(j<=i)break;if(m&(1n<<BigInt(j))){let [z,c]=basis.get(j);m^=z;b^=c;L.gauss++}}basis.set(i,[m,b]);if(m===(1n<<BigInt(i))){newpin=[i,b];break}}
  }
  if(!newpin)return {R,p};p[newpin[0]]=newpin[1];L.pins++;
 }
}
function blossom(g){
 const n=g.length,M=Array(n).fill(-1);L.matching++;L.matchVertices+=n;L.matchEdges+=g.reduce((s,a)=>s+a.length,0)/2;
 function find(root){
  let p=Array(n).fill(-1),base=Array.from({length:n},(_,i)=>i),used=Array(n).fill(false),q=[root];used[root]=true;
  function lca(a,b){let seen=Array(n).fill(false);for(;;){a=base[a];seen[a]=true;if(M[a]===-1)break;a=p[M[a]]}for(;;){b=base[b];if(seen[b])return b;b=p[M[b]]}}
  function mark(v,b,child,B){while(base[v]!==b){B[base[v]]=B[base[M[v]]]=true;p[v]=child;child=M[v];v=p[M[v]]}}
  for(let h=0;h<q.length;h++){let v=q[h];for(let u of g[v]){L.edgeVisits++;if(base[v]===base[u]||M[v]===u)continue;
   if(u===root||(M[u]!==-1&&p[M[u]]!==-1)){let b=lca(v,u),B=Array(n).fill(false);mark(v,b,u,B);mark(u,b,v,B);for(let i=0;i<n;i++)if(B[base[i]]){base[i]=b;if(!used[i]){used[i]=true;q.push(i)}}}
   else if(p[u]===-1){p[u]=v;if(M[u]===-1){let cur=u;while(cur!==-1){let pv=p[cur],next=pv===-1?-1:M[pv];M[cur]=pv;if(pv!==-1)M[pv]=cur;cur=next}return true}u=M[u];used[u]=true;q.push(u)}
  }}return false;
 }
 for(let i=0;i<n;i++)if(M[i]===-1)find(i);
 return M;
}
function occurrences(R){let O=new Map();R.forEach((o,i)=>o.a.forEach(([v,s])=>{if(!O.has(v))O.set(v,[]);O.get(v).push([i,s])}));return O}
function factor(F,n,init={}){
 const C=close(F,n,init);if(!C)return null;let {R,p}=C,O=occurrences(R);
 if([...O.values()].some(a=>a.length>2))throw Error("factor promise");
 let bounds=R.map(o=>[o.l,o.u]),edges=[],decode=[];
 const aux=(l,u)=>{bounds.push([l,u]);return bounds.length-1};
 for(const [v,a] of O){let [i,s]=a[0],idx=edges.length;
  if(a.length===1){edges.push([i,aux(0,1)])}
  else {let [j,t]=a[1];if(s===t)edges.push([i,j]);else {let z=aux(1,1);edges.push([i,z],[j,z])}}
  decode.push([v,s,idx]);
 }
 let g=[],slots=[],optional=[],ends=[];
 const vertex=()=>{g.push([]);return g.length-1},link=(a,b)=>{g[a].push(b);g[b].push(a)};
 for(let [l,u] of bounds){let S=[];for(let j=0;j<u;j++){let z=vertex();S.push(z);if(j>=l)optional.push(z)}slots.push(S)}
 if(g.length%2)optional.push(vertex());
 for(let [a,b] of edges){let x=vertex(),y=vertex();ends.push([x,y]);link(x,y);for(let z of slots[a])link(x,z);for(let z of slots[b])link(y,z)}
 for(let i=0;i<optional.length;i++)for(let j=0;j<i;j++)link(optional[i],optional[j]);
 let M=blossom(g);if(M.includes(-1))return null;
 for(let i=0;i<M.length;i++)check(M[M[i]]===i&&g[i].includes(M[i]));
 for(let [v,s,e] of decode){let [x,y]=ends[e];p[v]=Number(M[x]!==y)^s}
 for(let o of F)for(let [v] of o.a)if(!(v in p))p[v]=0;
 check(ok(F,p));return p;
}
function forest(F,n){
 const O=occurrences(F),H=[...O].filter(([v,a])=>a.length>2).map(([v])=>v),hub=new Set(H);
 let parent=F.map((_,i)=>i);
 const root=(i)=>{while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i]}return i};
 for(let [v,a] of O)if(!hub.has(v)&&a.length===2)parent[root(a[0][0])]=root(a[1][0]);
 let groups=new Map();F.forEach((o,i)=>{let r=root(i);if(!groups.has(r))groups.set(r,[]);groups.get(r).push(o)});
 let R=[...groups.values()],hindex=new Map(H.map((v,i)=>[v,R.length+i])),G=Array.from({length:R.length+H.length},()=>[]);
 for(let i=0;i<R.length;i++){for(let [v,a] of occurrences(R[i])){if(a.length>2)return undefined;if(hub.has(v)){let j=hindex.get(v);G[i].push(j);G[j].push(i)}}}
 let seen=new Set(),roots=[];
 function dfs(v,p){if(seen.has(v))return false;seen.add(v);for(let u of G[v])if(u!==p&&!dfs(u,v))return false;return true}
 for(let i=0;i<G.length;i++)if(!seen.has(i)){roots.push(i);if(!dfs(i,-1))return undefined}
 function message(v,p){
  let kids=G[v].filter(u=>u!==p),tables=kids.map(u=>message(u,v)),T=[];
  if(v>=R.length){let h=H[v-R.length];for(let b=0;b<2;b++){if(tables.every(t=>t[b]!==null))T[b]=Object.assign({[h]:b},...tables.map(t=>t[b]));else T[b]=null}return T}
  let choices=p<0?[0]:[0,1];
  for(let b of choices){let pin={},bad=false;if(p>=0)pin[H[p-R.length]]=b;
   for(let i=0;i<kids.length;i++){let t=tables[i],h=H[kids[i]-R.length];if(t[0]===null&&t[1]===null){bad=true;break}if(t[0]===null)pin[h]=1;else if(t[1]===null)pin[h]=0}
   if(bad){T[b]=null;continue}L.regionQueries++;let w=factor(R[v],n,pin);if(w===null){T[b]=null;continue}
   for(let i=0;i<kids.length;i++){let h=H[kids[i]-R.length];check(tables[i][w[h]]!==null);Object.assign(w,tables[i][w[h]])}T[b]=w;
  }return T;
 }
 let out={};
 for(let r of roots){let t=message(r,-1)[0];if(t===null)return null;Object.assign(out,t)}
 check(ok(F,out));return out;
}
function solve(F,n,cap=3,init={}){
 let C=close(F,n,init);if(!C)return null;let {R,p}=C;
 let w=forest(R,n);
 if(w!==undefined){if(w===null)return null;let out=Object.assign(Object.fromEntries(Array.from({length:n},(_,i)=>[i,0])),p,w);check(ok(F,out));return out}
 L.declines++;if(cap===0)return undefined;
 let h=[...occurrences(R)].sort((a,b)=>b[1].length-a[1].length)[0][0];L.branches++;
 let a=solve(F,n,cap-1,{...p,[h]:0});if(a!==null&&a!==undefined)return a;
 let b=solve(F,n,cap-1,{...p,[h]:1});if(b!==null&&b!==undefined)return b;
 return a===undefined||b===undefined?undefined:null;
}
function ref(F,n){let c=0;for(let i=0;i<2**n;i++){L.referenceWords++;let x=Array.from({length:n},(_,j)=>(i>>j)&1);if(ok(F,x))c++}return c}
let seed=20813;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let results=[],fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(a=>own(a));
function test(name,F,n,cap=3,expected=null){let count=expected===null?ref(F,n):null;let w=solve(F,n,cap),label=w===undefined?"UNKNOWN":w===null?"UNSAT":"SAT",truth=expected===null?count>0:expected;check(w===undefined||truth===(w!==null));results.push({name,n,owners:F.length,count,label,witness:w??null})}
test("Fano",fano,7);
for(let i=0;i<7;i++){for(let k=0;k<2;k++){let F=fano.map((o,j)=>j===i?{...o,l:k?0:1,u:k?2:3}:o);test("budget-"+i+"-"+k,F,7)}for(let k=0;k<3;k++){let F=fano.map((o,j)=>j===i?{...o,a:o.a.map(([v,s],q)=>[v,q===k?1:s])}:o);test("sign-"+i+"-"+k,F,7)}}
for(let t=0;t<120;t++){let n=5+rand(5),m=3+rand(5),A=Array.from({length:m},()=>[]);for(let v=0;v<n;v++){let i=rand(m);A[i].push([v,rand(2)]);if(rand(3)!==0){let j=(i+1+rand(m-1))%m;A[j].push([v,rand(2)])}}let F=A.map(a=>{let l=rand(a.length+1),u=l+rand(a.length-l+1);return {a,l,u}});test("degree2-"+t,F,n,0)}
for(let k of [3,8,32,64]){
 let F=[];for(let i=0;i<k;i++){F.push(own([i,k+i,k+(i+1)%k]));F.push(own([i,2*k+4*i,2*k+4*i+1]));F.push(own([i,2*k+4*i+2,2*k+4*i+3]))}
 test("hub-tree-"+k,F,6*k,0,true);
}
let odd=[];for(let i=0;i<9;i++)odd.push(own([i,(i+1)%9],1,1));test("odd-exact-one",odd,9,0);
let bad=[];for(let i=0;i<7;i++)for(let j=i+1;j<7;j++)for(let k=j+1;k<7;k++)bad.push(own([i,j,k]));test("dense-hostile",bad,7,0);
return {seed:20813,results,ledger:L,summary:results.reduce((a,r)=>(a[r.label]=(a[r.label]||0)+1,a),{})};
}
console.log(JSON.stringify(BH13(),null,2));

function run(){
let O={seed:71255,assertions:0,eliminations:0,pairTests:0,closurePasses:0,deductions:0,deleted:0,searchNodes:0,random:[],graphs:[],guarded:[]};let seed=O.seed;
const bit=i=>1n<<BigInt(i);
function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function ok(x,s){O.assertions++;if(!x)throw Error(s)}
function bas(rows){O.eliminations++;let b=new Map();for(let x of rows)while(x){let j=x.toString(2).length-1;if(b.has(j))x^=b.get(j);else{b.set(j,x);break}}return b}
function info(A){let b=bas(A);return [b.size,!b.has(0)]}
function rank(A){return bas(A.map(x=>x>>1n)).size}
function ev([u,v,s=0]){return [bit(2*u+1)^bit(2*v+1)^BigInt(s&1),bit(2*u+2)^bit(2*v+2)^BigInt((s>>1)&1)]}
function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
function check(E,G,x){let b=0n;for(let i=0;i<x.length;i++)b|=BigInt(x[i])<<BigInt(2*i);return E.every(([u,v,s=0])=>(x[u]^x[v])!==s)&&G.every(a=>parity((a>>1n)&b)===Number(a&1n))}
function close(G,E){G=G.slice();E=E.slice();for(;;){O.closurePasses++;let [p,v]=info(G);if(!v)return null;let change=false;for(let i=0;i<E.length;i++){let a=ev(E[i]),[r,c]=info(G.concat(a));if(!c){E.splice(i,1);O.deleted++;change=true;break}if(r===p)return null;if(r===p+1){G.push(a.find(t=>info(G.concat([t]))[0]>p)^1n);O.deductions++;change=true;break}}if(change)continue;
for(let i=0;i<E.length&&!change;i++)for(let j=0;j<E.length;j++)if(i!==j){O.pairTests++;let a=G.concat(ev(E[i])),[r,c]=info(a.concat(ev(E[j])));if(c&&r===info(a)[0]){E.splice(i,1);O.deleted++;change=true;break}}
if(!change)return {G,E,p}}}
function costs(G,E){return E.map((e,i)=>{let H=G.concat(ev(e)),r=rank(H),A=H.slice(),c=0;for(let j=0;j<E.length;j++)if(j!==i){O.pairTests++;if(info(H.concat(ev(E[j])))[1]){c++;A.push(...ev(E[j]))}}return Math.min(c,rank(A)-r)})}
function peel(G,E){E=E.slice();let K=0;while(E.length){let a=costs(G,E),k=Math.min(...a);K=Math.max(K,k);E.splice(a.indexOf(k),1)}return K}
function nlrank(G,E,d){let B=bas(G.map(a=>a>>1n)),z=[];for(let j=0;j<d;j++)if(!B.has(j)){let v=bit(j);for(let k=0;k<d;k++)if(B.has(k)&&parity(B.get(k)&v))v|=bit(k);z.push(v)}let rows=E.map(e=>{let [a,b]=ev(e).map(x=>x>>1n),A=z.map(v=>parity(v&a)),C=z.map(v=>parity(v&b)),r=0n,t=0;for(let i=0;i<z.length;i++)for(let j=i+1;j<z.length;j++,t++)if((A[i]&C[j])^(A[j]&C[i]))r|=bit(t);return r});return bas(rows).size}
function components(n,E){let a=Array.from({length:n},(_,i)=>i);function root(x){while(a[x]!==x)x=a[x];return x}for(let [u,v] of E)a[root(u)]=root(v);return new Set(a.map((_,i)=>root(i))).size}
function degree(n,E){let a=Array(n).fill(0);for(let [u,v] of E){a[u]++;a[v]++}return Math.max(...a)}
function solve(n,E){let adj=Array.from({length:n},()=>[]);for(let [u,v,s=0] of E){adj[u].push([v,s]);adj[v].push([u,s])}let a=Array(n).fill(-1);a[0]=0;function rec(){O.searchNodes++;let best=-1,sc=-1,mask=0;for(let i=0;i<n;i++)if(a[i]<0){let m=0;for(let [v,s] of adj[i])if(a[v]>=0)m|=1<<(a[v]^s);if(m===15)return null;let t=m.toString(2).replace(/0/g,"").length*100+adj[i].length;if(t>sc){sc=t;best=i;mask=m}}if(best<0)return a.slice();for(let c=0;c<4;c++)if(!(mask&(1<<c))){a[best]=c;let w=rec();if(w)return w;a[best]=-1}return null}return rec()}
function myc(n,E){let F=E.slice();for(let [u,v] of E)F.push([u,v+n],[v,u+n]);for(let i=0;i<n;i++)F.push([i+n,2*n]);return [2*n+1,F]}
function contract(n,E,u,v,s){let ids=Array.from({length:n},(_,i)=>i===v?u:i),names=[...new Set(ids)];return E.map(([a,b,t=0])=>[names.indexOf(ids[a]),names.indexOf(ids[b]),t^(a===v?s:0)^(b===v?s:0)])}
function graph(name,n,E){let m=E.length,cl=close([],E),K=Math.min(m-1,2*(n-components(n,E)-1));ok(cl&&cl.E.length===m,"closure");ok(costs([],E).every(x=>x===K),"root K");ok(nlrank([],E,2*n)===m,"root rank");ok(!solve(n,E),"root label");for(let i=0;i<m;i++){let F=E.filter((_,j)=>i!==j),w=solve(n,F);ok(w&&check(F,[],w),"neighbor");ok(w[E[i][0]]===w[E[i][1]],"equality")}
O.graphs.push({name,n,m,K,rank:m,exceptions:m-n+components(n,E),neighbors:m});
for(let i of [0,Math.floor(m/2),m-1]){let [u,v]=E[i],F=E.filter((_,j)=>i!==j);for(let s=0;s<4;s++){let P=contract(n,F,u,v,s),keys=P.map(([a,b])=>[Math.min(a,b),Math.max(a,b)].join(":"));if(P.some(([a,b])=>a===b)||new Set(keys).size!==P.length)continue;let G=ev([u,v,s]),C=close(G,F),k=Math.min(F.length-1,2*(n-1-components(n-1,P)-1));ok(C&&C.p===2&&C.E.length===F.length,"guard closure");let c=costs(G,F);ok(c.every(x=>x===k),"guard K");ok(nlrank(G,F,2*n)===F.length,"guard rank");let w=solve(n-1,P);ok(!!w===(s===0),"guard decision");if(w){let ids=Array.from({length:n},(_,j)=>j===v?u:j),names=[...new Set(ids)],lift=ids.map((j,k)=>w[names.indexOf(j)]^(k===v?s:0));ok(check(F,G,lift),"original guarded witness")}O.guarded.push({name,i,s,SAT:!!w,K:k,rank:F.length,exceptions:F.length-(n-1)+components(n-1,P)})}}
}
let K=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)K.push([i,j]);graph("K5",5,K);
let [n,E]=myc(5,[[0,1],[1,2],[2,3],[3,4],[4,0]]);[n,E]=myc(n,E);ok(!solve(n,E),"myc root");for(let i=E.length-1;i>=0;i--){let F=E.filter((_,j)=>i!==j);if(!solve(n,F))E=F}graph("critical Mycielski C5 twice",n,E);
for(let t=0;t<60;t++){let n=6,E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rand(7)<3)E.push([i,j,rand(4)]);if(!E.length)continue;let G=[],w=BigInt(rand(4096)),p=rand(4);for(let i=0;i<p;i++){let a=BigInt(rand(4096));G.push((a<<1n)|BigInt(parity(a&w)))}let cl=close(G,E),SAT=false,after=false;for(let z=0;z<4096;z++){let x=Array.from({length:n},(_,i)=>(z>>(2*i))&3);O.searchNodes++;if(!SAT&&check(E,G,x))SAT=true;if(cl&&!after&&check(cl.E,cl.G,x))after=true;if(SAT&&after)break}ok(SAT===after,"closure semantic");if(!cl){O.random.push({SAT,p:"closed UNSAT"});continue}let D=degree(n,E),r=nlrank(cl.G,cl.E,2*n),k=peel(cl.G,cl.E);ok(r>=cl.E.length-Math.floor(cl.p*D*(D+1)/2),"rank lower");ok(k>=Math.max(0,Math.min(E.length-4*cl.p*D-1,2*(n-components(n,E)-4*cl.p*D)-cl.p-2)),"peel lower");O.random.push({SAT,p:cl.p,m:cl.E.length,r,k})}
return O;
}
console.log(JSON.stringify(run(),null,2));

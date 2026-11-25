const run = function run(){
const D=4,C=[0,1,2,3],Z=[0,0],cn=x=>[x&1,x>>1],X=(a,b)=>[a[0]^b[0],a[1]^b[1]],J=a=>[a[1],a[0]^a[1]];
let seed=20261124,s={fixed:0,sat:0,unsat:0,lifts:0,edgeChecks:0,tupleChecks:0,events:0,closureQueries:0,closurePins:0,guarded:0,guardedSat:0,guardedUnsat:0,assertions:0,scaling:[]};
function ck(x){s.assertions++;if(!x)throw Error("assertion "+s.assertions)}
function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
function par(x){let p=0;while(x){p^=1;x&=x-1}return p}
const ev=(a,z)=>par(a[0]&((z<<1)|1))|par(a[1]&((z<<1)|1))<<1;
function comp(A){switch(A.length){case 0:return C.map(cn);case 1:return [1,2,3].map(x=>X(A[0],cn(x)));case 2:return A.map(a=>X(a,J(X(A[0],A[1]))));case 3:return [A.reduce(X,Z)];case 4:return [];default:throw Error("size")}}
function pairs(B){let v=B.v;return B.kind==="cycle"?v.map((a,i)=>[a,v[(i+1)%v.length]]):v.flatMap((a,i)=>v.slice(i+1).map(b=>[a,b]))}
const key=(a,b)=>a<b?a+","+b:b+","+a;
function adj(G){let A=Array.from({length:G.n},()=>[]);G.B.forEach((b,i)=>b.v.forEach(v=>A[v].push(i)));return A}
function compile(G){let E=[],A=adj(G);
function neq(a,b){let w=X(a,b);for(let x=1;x<4;x++)E.push([[w,x]])}
function same(U,V){for(let a of U){let d=V.map(b=>X(a,b));function rec(i,t){if(i===d.length){E.push(t);return}for(let j=1;j<4;j++)rec(i+1,t.concat([[d[i],j]]))}rec(0,[])}}
function list(v,p){let U=G.ext[v].slice();for(let i of A[v])if(i!==p)U.push(...block(i,v));for(let i=0;i<U.length;i++)for(let j=0;j<i;j++)E.push([[X(U[i],U[j]),0]]);return comp(U)}
function block(i,p){let B=G.B[i],V=B.v,S=(a,b)=>G.sign[key(a,b)],L={};for(let v of V)if(v!==p)L[v]=list(v,i);
let nbr=B.kind==="cycle"?V[(V.indexOf(p)+1)%V.length]:V.find(v=>v!==p);L[p]=L[nbr].map(a=>X(a,S(p,nbr)));
if(B.kind==="clique"){let q={};for(let v of V)q[v]=v===p?Z:S(p,v);for(let [a,b] of pairs(B))neq(S(a,b),X(q[a],q[b]));for(let v of V)if(v!==p)same(L[v].map(a=>X(a,q[v])),L[p]);}
else{let d=X(L[p][0],L[p][1]),h=Z;E.push([[d,0]]);for(let [a,b] of pairs(B)){same(L[a].map(x=>X(x,S(a,b))),L[b]);h=X(h,S(a,b))}neq(h,V.length%2?Z:d)}
return L[p]}
ck(list(0,-1).length===0);s.events+=E.length;return E}
function evaluate(E,z){return E.some(t=>t.every(([a,b])=>ev(a,z)===b))}
function consistent(t,pins){let rows=[];for(let [a,b] of t){rows.push(a[0]^(b&1),a[1]^(b>>1))}for(let [i,v] of pins)rows.push((1<<(i+1))^v);let B={};for(let row of rows){while(row>>1){let j=31-Math.clz32(row);if(!B[j]){B[j]=row;row=0;break}row^=B[j]}if(row===1)return false}return true}
function close(E,pins){let p=pins.slice();function yes(q){s.closureQueries++;return E.some(t=>consistent(t,q))}if(!yes(p))return null;let change=true;while(change){change=false;for(let i=0;i<D;i++)if(!p.some(a=>a[0]===i)){let a=yes(p.concat([[i,0]])),b=yes(p.concat([[i,1]]));ck(a||b);if(a!==b){p.push([i,b?1:0]);s.closurePins++;change=true;break}}}return p}
function ref(G,z){let A=adj(G),forb=G.ext.map(t=>new Set(t.map(a=>ev(a,z)))),mem=new Map();
function vertex(v,p,c){if(forb[v].has(c))return null;let out=[[v,c]];for(let i of A[v])if(i!==p){let q=block(i,v,c);if(!q)return null;out.push(...q)}return out}
function block(i,p,c){let k=i+","+p+","+c;if(mem.has(k))return mem.get(k);let B=G.B[i],others=B.v.filter(v=>v!==p),E=pairs(B),a={[p]:c},ans=null;function rec(j,ret){if(j===others.length){s.tupleChecks++;for(let [u,v] of E){s.edgeChecks++;if((a[u]^a[v])===ev(G.sign[key(u,v)],z))return}ans=ret;return}let v=others[j];for(let x of C){let t=vertex(v,i,x);if(t){a[v]=x;rec(j+1,ret.concat(t));if(ans)return}}}rec(0,[]);mem.set(k,ans);return ans}
for(let c of C){let w=vertex(0,-1,c);if(w){let a=Object.fromEntries(w);ck(Object.keys(a).length===G.n);for(let v=0;v<G.n;v++)ck(!forb[v].has(a[v]));for(let b of G.B)for(let [u,v] of pairs(b))ck((a[u]^a[v])!==ev(G.sign[key(u,v)],z));s.lifts++;return true}}return false}
function make(types){let B=[],n=1,deg=[0];for(let kind of types){let [type,k]=kind,dd=type==="cycle"?2:k-1;let avail=deg.map((d,i)=>d+dd<=4?i:-1).filter(i=>i>=0);if(!avail.length){type="clique";k=2;dd=1;avail=deg.map((d,i)=>d<4?i:-1).filter(i=>i>=0)}let root=avail[rand(avail.length)],v=[root];deg[root]+=dd;for(let j=1;j<k;j++){v.push(n++);deg.push(dd)}B.push({kind:type,v})}
let G={n,B,ext:Array.from({length:n},()=>[]),sign:{}},A=adj(G);
function setv(v,p,used){let left=C.filter(x=>!used.includes(x));for(let i of A[v])if(i!==p){let b=B[i],d=b.kind==="cycle"?2:b.v.length-1,L=left.splice(0,d);ck(L.length===d);for(let [a,c] of pairs(b))G.sign[key(a,c)]=cn(0);if(b.kind==="cycle"&&b.v.length%2===0){let [a,c]=pairs(b)[0];G.sign[key(a,c)]=cn(L[0]^L[1])}for(let u of b.v)if(u!==v)setv(u,i,L)}G.ext[v]=left.map(cn)}
setv(0,-1,[]);return G}
function twist(G,random){let q=Array.from({length:G.n},()=>[rand(32),rand(32)]);for(let v=0;v<G.n;v++)G.ext[v]=G.ext[v].map(a=>X(a,q[v]));for(let k in G.sign){let [a,b]=k.split(",").map(Number);G.sign[k]=X(G.sign[k],X(q[a],q[b]))}if(random){for(let v=0;v<G.n;v++)G.ext[v]=G.ext[v].map(a=>rand(3)===0?X(a,[rand(16)<<1,rand(16)<<1]):a);for(let k in G.sign)if(rand(3)===0)G.sign[k]=X(G.sign[k],[rand(16)<<1,rand(16)<<1])}}
let types=[["clique",2],["clique",3],["clique",4],["cycle",4],["cycle",5]];
for(let j=0;j<100;j++){let ts=j===0?[["clique",5]]:Array.from({length:1+rand(5)},()=>types[rand(types.length)]),g=make(ts);twist(g,true);let E=compile(g);ck(!evaluate(E,0));let words=[];for(let z=0;z<16;z++){let a=evaluate(E,z),b=ref(g,z);ck(a===b);s.fixed++;s[a?"sat":"unsat"]++;if(a)words.push(z)}for(let q=0;q<3;q++){let pins=[[rand(D),rand(2)]],expected=words.filter(z=>pins.every(([i,v])=>((z>>i)&1)===v)),cl=close(E,pins);s.guarded++;s[cl?"guardedSat":"guardedUnsat"]++;ck(!!cl===!!expected.length);if(cl)ck(expected.every(z=>cl.every(([i,v])=>((z>>i)&1)===v)))}}
for(let k of [2,8,32,128]){let g=make(Array.from({length:k},()=>["clique",3]));twist(g,false);let E=compile(g);ck(!evaluate(E,0));ck(!ref(g,0));let v=g.ext.findIndex(t=>t.length>=2);g.ext[v][1]=g.ext[v][0];E=compile(g);ck(evaluate(E,0));ck(ref(g,0));s.scaling.push({blocks:k,vertices:g.n,events:E.length})}
return s};
console.log(JSON.stringify(run(),null,2));

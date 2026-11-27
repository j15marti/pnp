const audit = function(){
const CAP=65536,a=3,d=2*a;
const perm=(arr,visit)=>{const rec=(p,r)=>{if(!r.length){visit(p);return;}for(let i=0;i<r.length;i++)rec([...p,r[i]],r.filter((_,j)=>i!==j))};rec([],arr)};
function graph(q,hostile=false){let n=3*q, blocks=[];for(let i=0;i<q;i++)blocks.push([3*i,3*i+1,3*i+2]);for(let i=0;i<q-1;i++)blocks.push([3*i+2,3*i+3]);let w=Array.from({length:n},()=>Array(n).fill(null));for(const b of blocks)for(const i of b)for(const j of b)w[i][j]=i<=j?0:a+1;w[2][0]=w[2][1]=a;if(hostile)w[5][3]=a;return {n,blocks,w}}
function brute(g){let visits=0,counts=Array(d+1).fill(0),stop=false;function go(i,used,c){if(++visits>CAP){stop=true;return;}if(i===g.n){counts[c]++;return;}for(let j=0;j<g.n&&!stop;j++){let v=g.w[i][j];if(v!==null&&!used.has(j)&&c+v<=d){used.add(j);go(i+1,used,c+v);used.delete(j)}}}go(0,new Set(),0);return {visits,counts:stop?null:counts}}
function hybrid(g){let checks=0;const z=()=>Array(d+1).fill(0n),one=()=>[1n,...Array(d).fill(0n)],plus=(a,b)=>a.map((v,i)=>v+b[i]);function mul(a,b){let r=z();for(let i=0;i<=d;i++)for(let j=0;i+j<=d;j++){checks++;r[i+j]+=a[i]*b[j]}return r}const adj=Array.from({length:g.n},()=>[]);g.blocks.forEach((b,i)=>b.forEach(v=>adj[v].push(i)));
function vertex(v,parent){let A=one(),B=z();for(const bi of adj[v])if(bi!==parent){let [x,y]=block(bi,v);B=plus(mul(B,x),mul(A,y));A=mul(A,x)}return [A,B]}
function block(bi,parent){let b=g.blocks[bi],child=new Map(b.filter(v=>v!==parent).map(v=>[v,vertex(v,bi)])),out=[z(),z()];perm(b,p=>{let c=0;for(let i=0;i<b.length;i++)c+=g.w[b[i]][p[i]];if(c>d)return;let r=z();r[c]=1n;for(let i=0;i<b.length;i++){let v=b[i];if(v===parent)continue;let [A,B]=child.get(v);r=mul(r,v===p[i]?plus(A,B):A)}let k=+(p[b.indexOf(parent)]!==parent);out[k]=plus(out[k],r)});return out}
let [A,B]=vertex(0,-1);return {checks,counts:plus(A,B).map(String)}}
function arithmetic(g){let special=[];let other=[];for(let i=0;i<g.n;i++)for(let j=0;j<g.n;j++){if(g.w[i][j]===a)special.push([i,j]);if(g.w[i][j]===a+1)other.push([i,j]);}return {special,other:other.length,NO:special.every(e=>e[0]===special[0][0])}}
const C=(x,y,z)=>{let s=[x,y,z].sort((a,b)=>a-b).join("");return ["012","123","234","034","014"].includes(s)};
const R=(x,y,z)=>{let win=(x,y)=>[1,3].includes((y-x+5)%5);return new Set([x,y,z]).size===3&&win(x,y)!==win(x,z)};
let relation=0;for(let i=0;i<5;i++)for(let j=0;j<5;j++)for(let k=0;k<5;k++){if(C(i,j,k)!==(R(i,j,k)&&R(j,i,k)))throw Error("C/R");relation++}
function compile(g){let clauses=[],n=5;let id=()=>n++;let add=(...x)=>{if(new Set(x).size!==3)throw Error("repeat");clauses.push(x)};for(let i=0;i<5;i++)add(i,(i+1)%5,(i+2)%5);
function wire(){let p=id();for(let j=2;j<=4;j++)add(j,p,id());return p}
function not(p){let z=wire();add(2,p,z);return z}
function or(p,q){let z=wire(),u=id(),v=id();add(1,2,u);add(0,1,v);add(4,p,u);add(3,q,v);add(z,u,v);return z}
function and(p,q){return not(or(not(p),not(q)))}
let edges=[];for(let i=0;i<g.n;i++)for(let j=0;j<g.n;j++)if(g.w[i][j]!==null)edges.push({i,j,c:g.w[i][j],p:wire()});
let seed=edges[0].p, tru=or(seed,not(seed)),fal=not(tru);let pin=p=>add(0,2,p);function one(es){let seen=fal;for(const e of es){pin(not(and(seen,e.p)));seen=or(seen,e.p)}pin(seen)}
for(let i=0;i<g.n;i++){one(edges.filter(e=>e.i===i));one(edges.filter(e=>e.j===i))}
let s=[tru,...Array(d).fill(fal)];for(const e of edges.filter(e=>e.c>0)){let no=not(e.p);s=s.map((p,j)=>or(and(no,p),and(e.p,j>=e.c?s[j-e.c]:fal)))}pin(s[d]);let m=clauses.length,N=n+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(n+1));let hash=2166136261;for(const c of clauses)for(const x of c){hash=Math.imul(hash^(x+1),16777619)>>>0}
let dom=new Uint8Array(n).fill(31),inc=Array.from({length:n},()=>[]);clauses.forEach((c,i)=>c.forEach(v=>inc[v].push(i)));let tuples=[];for(let x=0;x<5;x++)for(let y=0;y<5;y++)for(let z=0;z<5;z++)if(C(x,y,z))tuples.push([x,y,z]);let queue=clauses.map((_,i)=>i),queued=new Uint8Array(m).fill(1),updates=0,checks=0,empty=false;for(let h=0;h<queue.length&&!empty;h++){let i=queue[h],c=clauses[i];queued[i]=0;let sup=[0,0,0];for(const t of tuples){checks++;if(t.every((v,j)=>dom[c[j]]&(1<<v)))t.forEach((v,j)=>sup[j]|=1<<v)}for(let j=0;j<3;j++){let v=c[j],x=dom[v]&sup[j];if(x!==dom[v]){updates++;dom[v]=x;if(!x){empty=true;break}for(const k of inc[v])if(!queued[k]){queued[k]=1;queue.push(k)}}}}
return {n,m,N,orderedR_N:n+1+2*Math.floor(Math.log2(2*m+1))+1+6*m*Math.ceil(Math.log2(n+1)),fingerprint:hash.toString(16),edgeCount:edges.length,GAC:{updates,checks,empty,rawDomains:[...new Set(edges.map(e=>dom[e.p]))]}}}
let signs=0;for(let mask=0;mask<512;mask++){let vals=[];perm([0,1,2],p=>{let s=1;for(let i=0;i<3;i++){if(mask&(1<<(3*i+p[i])))s=-s;for(let j=i+1;j<3;j++)if(p[i]>p[j])s=-s}vals.push(s)});if(vals.every(v=>v===vals[0]))signs++}
let results=[];for(const [q,h] of [[2,false],[4,false],[8,false],[16,false],[2,true]]){let g=graph(q,h),b=brute(g),x=hybrid(g),ar=arithmetic(g),native=compile(g);if(b.counts&&b.counts.map(String).join()!==x.counts.join())throw Error("mismatch");if((x.counts[d]==="0")!==ar.NO)throw Error("control");results.push({q,hostile:h,brute:b,hybrid:x,arithmetic:ar,native})}return {a,d,relation,signs,results}
};
console.log(JSON.stringify(audit(),null,2));

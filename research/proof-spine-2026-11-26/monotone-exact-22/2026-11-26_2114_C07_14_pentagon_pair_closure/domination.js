function audit(){
const mod=(a,p)=>((a%p)+p)%p, ok=(x,m)=>{if(!x)throw Error(m||"assert")};
function graph(n,E){const e=[...new Set(E.map(([u,v])=>`${Math.min(u,v)},${Math.max(u,v)}`))].map(s=>s.split(",").map(Number));ok(e.every(([u,v])=>u<v&&u>=0&&v<n));return {n,e}}
function myc(k,L){const E=[];for(let i=0;i<k;i++){const j=(i+1)%k;E.push([i,j]);for(let h=0;h<L-1;h++){E.push([h*k+i,(h+1)*k+j],[h*k+j,(h+1)*k+i])}E.push([(L-1)*k+i,L*k])}return graph(L*k+1,E)}
function native(G){let n=5;const rows=[[0,1,2,3],[0,1,3,4],[0,1,4,2]],owners=Array.from({length:G.n},()=>[n++,n++,n++]);for(const x of owners)rows.push([...x,2]);const edgeRows=[];for(const [u,v] of G.e){const ids=[];for(let c=0;c<3;c++){ids.push(rows.length);rows.push([owners[u][c],owners[v][c],2,n++])}edgeRows.push(ids)}return {n,rows,owners,edgeRows,G,guards:[[0,0]]}}
function verifyChart(F){const f=native(F.G);ok(JSON.stringify(f)===JSON.stringify(F),"chart map");ok(F.rows.every(r=>r.length===4&&new Set(r).size===4));let checks=0;
for(let a=0;a<8;a++){const t=[a&1,(a>>1)&1,(a>>2)&1];ok((1+t.reduce((s,x)=>s+x,0)===2)===(t.reduce((s,x)=>s+x,0)===1));checks++}
for(let a=0;a<2;a++)for(let b=0;b<2;b++){ok([0,1].some(w=>a+b+1+w===2)===(a+b<=1));checks++}return checks}
function close(F){const w=Array(F.n).fill(-1);w[0]=0;w[1]=0;w[2]=w[3]=w[4]=1;let change=true,scans=0;while(change){change=false;for(const r of F.rows){scans++;let s=0,u=[];for(const i of r){if(w[i]<0)u.push(i);else s+=w[i]}if(s>2||s+u.length<2)return {no:true,scans};if(s===2||s+u.length===2)for(const i of u){w[i]=s===2?0:1;change=true}}}return {no:false,scans,unfixed:w.filter(x=>x<0).length}}
function index(G){const adj=Array.from({length:G.n},()=>[]),ids=new Map();G.e.forEach(([u,v],i)=>{adj[u].push(v);adj[v].push(u);ids.set(`${u},${v}`,i)});const id=(u,v)=>ids.get(`${Math.min(u,v)},${Math.max(u,v)}`),sg=(u,v)=>u<v?1:-1;return {adj,id,sg}}
function cycles(G){const {adj,id,sg}=index(G),tri=[],sq=[];let probes=0;
for(let a=0;a<G.n;a++)for(const b of adj[a])if(b>a)for(const c of adj[b])if(c>a&&c!==b){
probes++;if(c>b&&id(c,a)!==undefined)tri.push([a,b,c]);
for(const d of adj[c])if(d>a&&d!==b&&d>b){probes++;if(id(d,a)!==undefined)sq.push([a,b,c,d])}}
const orient=c=>c.map((u,i)=>[id(u,c[(i+1)%c.length]),sg(u,c[(i+1)%c.length])]);return {tri:tri.map(orient),sq:sq.map(orient),probes}}
function parity(G,C,triangles=false){const m=G.e.length,P=new Map();let ops=0,rank=0,contradiction=null;const rows=[];
for(const s of C.sq){let v=0n,r=0;for(const [e,d] of s){v^=1n<<BigInt(e);r+=d}rows.push([v,mod(r/2,2)])}
if(triangles)for(const t of C.tri)for(let j=1;j<3;j++)rows.push([(1n<<BigInt(t[0][0]))^(1n<<BigInt(t[j][0])),t[0][1]===t[j][1]?0:1]);
function reduce(v,r,pr=0n){while(v){const p=v.toString(2).length-1;ops++;const q=P.get(p);if(!q)break;v^=q[0];r^=q[1];pr^=q[2]}return [v,r,pr]}
for(let i=0;i<rows.length;i++){const [v,r,pr]=reduce(...rows[i],1n<<BigInt(i));if(!v&&r){contradiction=pr;break}if(v){P.set(v.toString(2).length-1,[v,r,pr]);rank++}}
const rel=[];if(contradiction===null){for(let i=0;i<m;i++)for(let j=0;j<i;j++){const [v,r]=reduce((1n<<BigInt(i))^(1n<<BigInt(j)),0);if(!v)rel.push([i,j,r])}}
let cert=[];if(contradiction!==null){let v=0n,r=0;for(let i=0;i<rows.length;i++)if((contradiction>>BigInt(i))&1n){cert.push(i);v^=rows[i][0];r^=rows[i][1]}ok(v===0n&&r===1,"cert")}
return {no:contradiction!==null,rank,rel,ops,cert,rows:rows.length}}
function ternary(G,C,extra=[]){const P=new Map();let ops=0;const vec=(i)=>{const a=Array(G.n).fill(0),[u,v]=G.e[i];a[u]=2;a[v]=1;return a};
function reduce(a){for(let i=0;i<G.n;i++)if(a[i]&&P.has(i)){const b=P.get(i),q=a[i];for(let j=i;j<G.n;j++){a[j]=mod(a[j]-q*b[j],3);ops++}}return a}
function add(i,j,r){const a=vec(i),b=vec(j),s=r?2:1;for(let l=0;l<G.n;l++)a[l]=mod(a[l]-s*b[l],3);reduce(a);const k=a.findIndex(x=>x);if(k>=0){const x=a[k];for(let l=k;l<G.n;l++)a[l]=mod(x*a[l],3);P.set(k,a)}}
for(const t of C.tri)for(let j=1;j<3;j++)add(t[0][0],t[j][0],t[0][1]===t[j][1]?0:1);
for(const [i,j,r] of extra)add(i,j,r);
const forced=[];for(let i=0;i<G.e.length;i++)if(reduce(vec(i)).every(x=>x===0))forced.push(i);
return {no:forced.length>0,rank:P.size,forced,ops}}
function ref(G,cap){const {adj}=index(G),col=Array(G.n).fill(-1);let nodes=0,exceeded=false;function visit(){if(++nodes>cap){exceeded=true;return false}let v=-1,best=-1,mask=0;for(let i=0;i<G.n;i++)if(col[i]<0){let m=0;for(const j of adj[i])if(col[j]>=0)m|=1<<col[j];const s=10*((m&1)+((m>>1)&1)+((m>>2)&1))+adj[i].length;if(s>best){v=i;best=s;mask=m}}if(v<0)return true;for(let c=0;c<3;c++)if(!(mask&(1<<c))){col[v]=c;if(visit())return true;col[v]=-1;if(exceeded)return false}return false}
col[0]=0;const sat=visit();return {status:exceeded?"UNKNOWN":sat?"SAT":"UNSAT",nodes,col:sat?col:null}}
function explicit(G,k,L){const {id,sg}=index(G);let sums=Array(G.e.length).fill(0),count=0;function face(c,s=1){count++;for(let i=0;i<4;i++){const u=c[i],v=c[(i+1)%4],e=id(u,v);ok(e!==undefined,"face edge");sums[e]+=s*sg(u,v)}}const v=(i,h)=>h*k+mod(i,k);
for(let i=0;i<k;i++)face([v(i,0),v(i+1,0),v(i+2,0),v(i+1,1)]);
for(let h=1;h<L-1;h++)for(let i=0;i<k;i++)face([v(i,h),v(i+1,h-1),v(i+2,h),v(i+1,h+1)]);
for(let i=0;i<k;i++)face([v(i,L-2),v(i+1,L-1),L*k,v(i-1,L-1)]);
// base faces give 2 base - S0, intermediate S_prev-S_next, top S_last.
const want=Array(G.e.length).fill(0);for(let i=0;i<k;i++)want[id(i,(i+1)%k)]+=2*sg(i,(i+1)%k);ok(sums.every((x,i)=>x===want[i]),"integer identity");return {count,odd:k%2===1}}
const br=[[2,5,7,13],[3,6,7,8],[4,8,9],[5,9,10],[6,10,11],[11,12],[12,13],[15,20],[14,16],[15,17],[16,18],[17,19],[18,20],[14,19],[17,18],[18,19],[19,20],[20]].flatMap((a,i)=>a.map(j=>[i,j]));
function hash(s){let h=2166136261;for(const c of s)h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;return h.toString(16)}

const G=graph(21,br),F=native(G),finger=hash(JSON.stringify(F));
ok(finger==="95344f14");verifyChart(F);ok(!close(F).no);
function acquire(G){
 const {adj}=index(G),pent=[];let probes=0;
 function dfs(a,s){probes++;if(s.length===5){if(adj[s.at(-1)].includes(a)&&s[1]<s.at(-1))pent.push(s);return}
 for(const v of adj[s.at(-1)])if(v>a&&!s.includes(v))dfs(a,[...s,v])}
 for(let i=0;i<G.n;i++)dfs(i,[i]);
 const cover=D=>new Set([...D,...[...D].flatMap(v=>adj[v])]);
 let best=null, pairs=0;
 for(let i=0;i<pent.length;i++)for(let j=i;j<pent.length;j++){pairs++;const D=new Set(pent[i].concat(pent[j]));if(cover(D).size!==G.n)continue;let score=D.size; if(!best||score<best.score)best={i,j,D:[...D].sort((a,b)=>a-b),score}}
 return {pent,best,probes,pairs}
}
function solve(G,chart,kind){
 const {adj}=index(G),{pent,best}=chart;ok(best);const D=best.D,P=pent[best.i],Q=pent[best.j];
 const c=Array(G.n).fill(-1),outside=Array.from({length:G.n},(_,i)=>i).filter(i=>!D.includes(i));
 let nodes=0,calls=0,edgeScans=0,invalid=0,branches=0;const certificates=[];
 function check(){
 calls++; const ls=outside.map(v=>[0,1,2].filter(x=>adj[v].every(w=>c[w]!==x)));
 if(ls.some(l=>!l.length)){certificates.push({pins:D.map(v=>c[v]),empty:outside[ls.findIndex(l=>!l.length)]});return true}
 ok(ls.every(l=>l.length<=2),"not dominating"); const A=Array.from({length:2*outside.length},()=>[]);const add=(a,b)=>{A[a].push(b);edgeScans++};
 const lit=(i,t)=>2*i+t;
 for(let i=0;i<ls.length;i++)if(ls[i].length===1)add(lit(i,1),lit(i,0));
 for(let i=0;i<outside.length;i++)for(let j=0;j<i;j++)if(adj[outside[i]].includes(outside[j])){
 for(let a=0;a<ls[i].length;a++)for(let b=0;b<ls[j].length;b++)if(ls[i][a]===ls[j][b]){add(lit(i,a),lit(j,b)^1);add(lit(j,b),lit(i,a)^1)}
 }
 function reach(s,t){const seen=new Set([s]),q=[s];for(let i=0;i<q.length;i++){if(q[i]===t)return true;for(const v of A[q[i]]){edgeScans++;if(!seen.has(v)){seen.add(v);q.push(v)}}}return false}
 for(let i=0;i<outside.length;i++)if(reach(2*i,2*i+1)&&reach(2*i+1,2*i)){certificates.push({pins:D.map(v=>c[v]),contradictory:outside[i]});return true}
 return false;
 }
 // First two adjacent vertices normalized to 0,1 using global permutation.
 c[P[0]]=0;c[P[1]]=1;
 function assign(v,x){return adj[v].every(w=>c[w]!==x)}
 function naive(i){nodes++;if(i===D.length)return check();const v=D[i];if(c[v]>=0)return naive(i+1);for(let x=0;x<3;x++){branches++;if(!assign(v,x)){invalid++;continue}c[v]=x;if(!naive(i+1)){c[v]=-1;return false}c[v]=-1}return true}
 // Exactly five oriented sign patterns modulo global color reversal and translation.
 function words(cycle){const arr=[];for(let bad=0;bad<5;bad++)for(let flip of [1,-1])for(let start=0;start<3;start++){const w=[start];for(let i=0;i<4;i++)w.push(mod(w.at(-1)+flip*(i===bad?-1:1),3));arr.push(w)}return arr}
 function hybrid(){for(const w of words(P)){nodes++;if(w[0]!==0||w[1]!==1)continue;let good=true;for(let i=0;i<P.length;i++){const v=P[i];if(c[v]>=0&&c[v]!==w[i]){good=false;break}c[v]=w[i]}ok(good);
 for(const z of words(Q)){nodes++;const newIDs=[];let legal=true;for(let i=0;i<Q.length;i++){const v=Q[i];if(c[v]>=0){if(c[v]!==z[i]){legal=false;break}}else{c[v]=z[i];newIDs.push(v)}}
 if(legal){for(const v of D)for(const u of adj[v])if(c[u]>=0&&c[u]===c[v])legal=false}
 if(legal){branches++;if(!check())return false}else invalid++;
 for(const v of newIDs)c[v]=-1
 }for(const v of P.slice(2))c[v]=-1
 }return true}
 const no=kind==="hybrid"?hybrid():naive(0);
 return {no,nodes,calls,edgeScans,invalid,branches,certificates,D,P,Q,outside}
}
const chart=acquire(G);ok(chart.best,"no dominating pair");
const A=solve(G,chart,"naive"),I=solve(G,chart,"hybrid");ok(A.no&&I.no);
const set=x=>new Set(x.certificates.map(t=>t.pins.join(",")));
ok(set(A).size===set(I).size&&[...set(A)].every(x=>set(I).has(x)),"boundary support mismatch");
return {finger,N:8*JSON.stringify(F).length,chart,A,I,source:F};
}
console.log(JSON.stringify(audit(),null,2));
function audit(F){
const assert=(b,m)=>{if(!b)throw Error(m||"assert")};
const pop=x=>(x&1)+((x>>1)&1)+((x>>2)&1),vals=x=>[0,1,2].filter(c=>x&(1<<c));
function native(G){let n=5;const rows=[[0,1,2,3],[0,1,3,4],[0,1,4,2]],owners=Array.from({length:G.n},()=>[n++,n++,n++]),edgeRows=[];for(const x of owners)rows.push([...x,2]);for(const [u,v] of G.e){let a=[];for(let c=0;c<3;c++){a.push(rows.length);rows.push([owners[u][c],owners[v][c],2,n++])}edgeRows.push(a)}return {n,rows,owners,edgeRows,G,guards:[[0,0]]}}
function graph(n,edges){const e=[...new Set(edges.map(([u,v])=>[Math.min(u,v),Math.max(u,v)].join(",")))].map(s=>s.split(",").map(Number));return {n,e}}
const offsets=[[1,6,-23,-6,-1],[1,9,14,23,-1],[1,26,33,-10,-1],[1,18,-18,-14,-1],[1,10,-26,-9,-1],[1,18,33,-18,-1]];
const L=graph(66,Array.from({length:66},(_,i)=>offsets[i%6].map(t=>[i,(i+t+66)%66])).flat());
assert(L.e.length===165);
function hash(x){let h=2166136261;for(const c of JSON.stringify(x))h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;return h.toString(16)}
assert(hash(F)==="95344f14");
function test(F,label,pins){
const n=F.G.n,E=F.G.e,adj=Array.from({length:n},()=>[]);for(const [u,v] of E){adj[u].push(v);adj[v].push(u)}
assert(JSON.stringify(native(F.G))===JSON.stringify(F),"native map");
assert(F.rows.every(r=>new Set(r).size===4));
let girth=Infinity;for(const [u,v] of E){const dist=Array(n).fill(-1),q=[u];dist[u]=0;for(let i=0;i<q.length;i++)for(const j of adj[q[i]]){if((q[i]===u&&j===v)||(q[i]===v&&j===u))continue;if(dist[j]<0){dist[j]=dist[q[i]]+1;q.push(j)}}if(dist[v]>=0)girth=Math.min(girth,dist[v]+1)}
const start=Array(n).fill(7);for(const [v,c] of pins)start[v]=1<<c;
const cap=5000000;
function lane(mode,depth){
let work=0,calls=0,deleted=0,rounds=0,proofs=0,failed=0,maxcore=0,budget=false;
function tick(x=1){work+=x;if(work>cap){budget=true;throw Error("cap")}}
function close(D){let ch=true;while(ch){ch=false;for(const [u,v] of E){tick();if(!D[u]||!D[v])return false;if(pop(D[u])===1&&(D[v]&D[u])){D[v]&=~D[u];ch=true}if(pop(D[v])===1&&(D[u]&D[v])){D[u]&=~D[v];ch=true}}}return D.every(Boolean)}
function core(D){calls++;let B=[],idx=Array(n).fill(-1);for(let i=0;i<n;i++){tick();if(!D[i])return false;if(pop(D[i])<=2){idx[i]=B.length;B.push(i)}}maxcore=Math.max(maxcore,B.length);let A=Array.from({length:2*B.length},()=>[]),L=B.map(i=>vals(D[i]));function edge(u,v){tick();A[u].push(v)}
for(let i=0;i<B.length;i++)if(L[i].length===1)edge(2*i+1,2*i);
for(const [u,v] of E){tick();let i=idx[u],j=idx[v];if(i<0||j<0)continue;for(let a=0;a<L[i].length;a++)for(let b=0;b<L[j].length;b++)if(L[i][a]===L[j][b]){edge(2*i+a,2*j+(b^1));edge(2*j+b,2*i+(a^1))}}
let seen=[],order=[],comp=[];function dfs(i){seen[i]=true;for(const j of A[i]){tick();if(!seen[j])dfs(j)}order.push(i)}for(let i=0;i<A.length;i++){tick();if(!seen[i])dfs(i)}let R=A.map(()=>[]);for(let i=0;i<A.length;i++)for(const j of A[i]){tick();R[j].push(i)}function rev(i,c){comp[i]=c;for(const j of R[i]){tick();if(comp[j]===undefined)rev(j,c)}}for(let i=order.length-1;i>=0;i--)if(comp[order[i]]===undefined)rev(order[i],i);for(let i=0;i<B.length;i++){tick();if(comp[2*i]===comp[2*i+1])return false}return true}
function sat(D,d){let deductions=[];while(true){rounds++;if(!close(D)){proofs++;return {deductions,end:"arc"}}if(mode==="core"&&!core(D)){proofs++;return {deductions,end:"core"}}if(d===0)return null;let found=false;outer:for(let v=0;v<n;v++)if(pop(D[v])>1)for(const c of vals(D[v])){tick(n);let P=D.slice();P[v]=1<<c;const cert=sat(P,d-1);if(cert){D[v]&=~(1<<c);deleted++;deductions.push({v,c,cert});found=true;break outer}else failed++}if(!found)return null}}
let D=start.slice(),cert=null;try{cert=sat(D,depth);return {status:cert?"UNSAT":"UNKNOWN",work,calls,deleted,rounds,proofs,failed,maxcore,D,cert}}catch(e){if(!budget)throw e;return {status:"UNKNOWN_CAP",work,calls,deleted,rounds,proofs,failed,maxcore,D}}
}
// Independent native replay of every successful deduction and final contradiction.
// Rebuild source occupancy from the current domain, then use independent transitive closure of binary graph.
function replay(cert){
let scans=0,leaves=0,imports=0,closures=0;
function occupancy(D){closures++;let w=Array(F.n).fill(-1);w[0]=w[1]=0;w[2]=w[3]=w[4]=1;for(let i=0;i<n;i++)for(let c=0;c<3;c++)if(!(D[i]&(1<<c)))w[F.owners[i][c]]=0;
let ch=true;while(ch){ch=false;for(const r of F.rows){if(++scans>cap)throw Error("replay cap");let s=0,u=[];for(const i of r){if(w[i]<0)u.push(i);else s+=w[i]}if(s>2||s+u.length<2)return false;if(s===2||s+u.length===2)for(const i of u){w[i]=s===2?0:1;ch=true}}}
for(let i=0;i<n;i++)for(let c=0;c<3;c++)if(w[F.owners[i][c]]===0)D[i]&=~(1<<c);
return D.every(Boolean)}
function contradiction(D){const B=Array.from({length:n},(_,i)=>i).filter(i=>pop(D[i])<=2),idx=new Map(B.map((v,i)=>[v,i])),L=B.map(i=>vals(D[i])),q=2*B.length,R=Array.from({length:q},(_,i)=>{let r=new Uint8Array(q);r[i]=1;return r});
for(let i=0;i<B.length;i++)if(L[i].length===1)R[2*i+1][2*i]=1;
for(const [u,v] of E)if(idx.has(u)&&idx.has(v)){let i=idx.get(u),j=idx.get(v);for(let a=0;a<L[i].length;a++)for(let b=0;b<L[j].length;b++)if(L[i][a]===L[j][b]){R[2*i+a][2*j+(b^1)]=1;R[2*j+b][2*i+(a^1)]=1}}
for(let k=0;k<q;k++)for(let i=0;i<q;i++)if(R[i][k])for(let j=0;j<q;j++)R[i][j]|=R[k][j];return B.some((_,i)=>R[2*i][2*i+1]&&R[2*i+1][2*i])}
function check(D,c){for(const d of c.deductions){if(!occupancy(D))return true;if(!(D[d.v]&(1<<d.c)))continue;const P=D.slice();P[d.v]=1<<d.c;assert(check(P,d.cert),"invalid child");D[d.v]&=~(1<<d.c);imports++}leaves++;if(!occupancy(D))return true;return c.end==="core"&&contradiction(D)}
assert(check(start.slice(),cert),"invalid root");return {scans,leaves,imports,closures}}
function ref(){const c=Array(n).fill(-1);for(const [v,x] of pins)c[v]=x;let nodes=0,scans=0,abort=false;function visit(){nodes++;let v=-1,best=-1,mask=0;for(let i=0;i<n;i++)if(c[i]<0){let m=0;for(const j of adj[i]){if(++scans>cap){abort=true;return false}if(c[j]>=0)m|=1<<c[j]}const s=100*pop(m)+adj[i].length;if(s>best){v=i;best=s;mask=m}}if(v<0)return true;for(const x of vals(7^mask)){c[v]=x;if(visit())return true;c[v]=-1;if(abort)return false}return false}
let yes=visit();return {status:abort?"UNKNOWN_CAP":yes?"SAT":"UNSAT",nodes,scans,witness:yes?c:null}}
const A=lane("arc",2),B=lane("core",1),C=ref(),I=lane("core",2);
assert(C.status!=="SAT");const verification=I.cert?replay(I.cert):null;
return {label,finger:hash(F),nativeVariables:F.n,rows:F.rows.length,graphVertices:n,edges:E.length,girth,pins,cap,A,B,C,I,verification,source:F}
}
return [test(F,"Brinkmann",[[0,0],[2,1]]),test(native(L),"Exoo-Goedgebeur Table 2",[[0,0],[1,1]])]
}
const F={"n":194,"rows":[[0,1,2,3],[0,1,3,4],[0,1,4,2],[5,6,7,2],[8,9,10,2],[11,12,13,2],[14,15,16,2],[17,18,19,2],[20,21,22,2],[23,24,25,2],[26,27,28,2],[29,30,31,2],[32,33,34,2],[35,36,37,2],[38,39,40,2],[41,42,43,2],[44,45,46,2],[47,48,49,2],[50,51,52,2],[53,54,55,2],[56,57,58,2],[59,60,61,2],[62,63,64,2],[65,66,67,2],[5,11,2,68],[6,12,2,69],[7,13,2,70],[5,20,2,71],[6,21,2,72],[7,22,2,73],[5,26,2,74],[6,27,2,75],[7,28,2,76],[5,44,2,77],[6,45,2,78],[7,46,2,79],[8,14,2,80],[9,15,2,81],[10,16,2,82],[8,23,2,83],[9,24,2,84],[10,25,2,85],[8,26,2,86],[9,27,2,87],[10,28,2,88],[8,29,2,89],[9,30,2,90],[10,31,2,91],[11,17,2,92],[12,18,2,93],[13,19,2,94],[11,29,2,95],[12,30,2,96],[13,31,2,97],[11,32,2,98],[12,33,2,99],[13,34,2,100],[14,20,2,101],[15,21,2,102],[16,22,2,103],[14,32,2,104],[15,33,2,105],[16,34,2,106],[14,35,2,107],[15,36,2,108],[16,37,2,109],[17,23,2,110],[18,24,2,111],[19,25,2,112],[17,35,2,113],[18,36,2,114],[19,37,2,115],[17,38,2,116],[18,39,2,117],[19,40,2,118],[20,38,2,119],[21,39,2,120],[22,40,2,121],[20,41,2,122],[21,42,2,123],[22,43,2,124],[23,41,2,125],[24,42,2,126],[25,43,2,127],[23,44,2,128],[24,45,2,129],[25,46,2,130],[26,50,2,131],[27,51,2,132],[28,52,2,133],[26,65,2,134],[27,66,2,135],[28,67,2,136],[29,47,2,137],[30,48,2,138],[31,49,2,139],[29,53,2,140],[30,54,2,141],[31,55,2,142],[32,50,2,143],[33,51,2,144],[34,52,2,145],[32,56,2,146],[33,57,2,147],[34,58,2,148],[35,53,2,149],[36,54,2,150],[37,55,2,151],[35,59,2,152],[36,60,2,153],[37,61,2,154],[38,56,2,155],[39,57,2,156],[40,58,2,157],[38,62,2,158],[39,63,2,159],[40,64,2,160],[41,59,2,161],[42,60,2,162],[43,61,2,163],[41,65,2,164],[42,66,2,165],[43,67,2,166],[44,47,2,167],[45,48,2,168],[46,49,2,169],[44,62,2,170],[45,63,2,171],[46,64,2,172],[47,56,2,173],[48,57,2,174],[49,58,2,175],[47,59,2,176],[48,60,2,177],[49,61,2,178],[50,59,2,179],[51,60,2,180],[52,61,2,181],[50,62,2,182],[51,63,2,183],[52,64,2,184],[53,62,2,185],[54,63,2,186],[55,64,2,187],[53,65,2,188],[54,66,2,189],[55,67,2,190],[56,65,2,191],[57,66,2,192],[58,67,2,193]],"owners":[[5,6,7],[8,9,10],[11,12,13],[14,15,16],[17,18,19],[20,21,22],[23,24,25],[26,27,28],[29,30,31],[32,33,34],[35,36,37],[38,39,40],[41,42,43],[44,45,46],[47,48,49],[50,51,52],[53,54,55],[56,57,58],[59,60,61],[62,63,64],[65,66,67]],"edgeRows":[[24,25,26],[27,28,29],[30,31,32],[33,34,35],[36,37,38],[39,40,41],[42,43,44],[45,46,47],[48,49,50],[51,52,53],[54,55,56],[57,58,59],[60,61,62],[63,64,65],[66,67,68],[69,70,71],[72,73,74],[75,76,77],[78,79,80],[81,82,83],[84,85,86],[87,88,89],[90,91,92],[93,94,95],[96,97,98],[99,100,101],[102,103,104],[105,106,107],[108,109,110],[111,112,113],[114,115,116],[117,118,119],[120,121,122],[123,124,125],[126,127,128],[129,130,131],[132,133,134],[135,136,137],[138,139,140],[141,142,143],[144,145,146],[147,148,149]],"G":{"n":21,"e":[[0,2],[0,5],[0,7],[0,13],[1,3],[1,6],[1,7],[1,8],[2,4],[2,8],[2,9],[3,5],[3,9],[3,10],[4,6],[4,10],[4,11],[5,11],[5,12],[6,12],[6,13],[7,15],[7,20],[8,14],[8,16],[9,15],[9,17],[10,16],[10,18],[11,17],[11,19],[12,18],[12,20],[13,14],[13,19],[14,17],[14,18],[15,18],[15,19],[16,19],[16,20],[17,20]]},"guards":[[0,0]]};
console.log(JSON.stringify(audit(F),null,2));

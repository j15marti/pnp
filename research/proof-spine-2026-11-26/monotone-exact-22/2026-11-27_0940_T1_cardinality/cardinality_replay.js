// Node replay. Pass pinned compile.js, benchmarks.json, registry.json, JOINT-24.certificate.json, RANDOM-3CNF-40.certificate.json.
const fs=require('node:fs'),crypto=require('node:crypto');
function classify(n,missing){
const e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(!missing||i!==0||j!==1)e.push([i,j]);const ports=missing?[0,1]:Array.from({length:n},(_,i)=>i), m=e.length;
let hist={},bad=[],checks=0,canonical=[];
const parity=x=>{let a=0;while(x){a^=x&1;x>>=1}return a};
for(let s=0;s<2**m;s++){let support=new Set();for(let x=0;x<2**m;x++){checks++;let deg=Array(n).fill(0);e.forEach(([a,b],i)=>{let v=x>>i&1;deg[a]+=v;deg[b]+=v^(s>>i&1)});if(deg.some((d,i)=>ports.includes(i)?d<1||d>2:d!==2))continue;support.add(ports.reduce((w,p,i)=>w+((2-deg[p])<<i),0))}let a=[...support].sort((a,b)=>a-b),p=Array.from({length:2**ports.length},(_,i)=>i).filter(i=>parity(i)===parity(s));if(a.some(x=>!p.includes(x)))throw Error("parity");hist[a.length]=(hist[a.length]||0)+1;if(a.length!==p.length)bad.push({s,missing:p.filter(x=>!support.has(x))});if(e.every(([a,b],i)=>a!==0||!(s>>i&1)))canonical.push({s,support:a})}
return {edges:e,ports,hist,bad,checks,canonical}
}
function native(G,cert){
const n=G.types.length, a=Array.from({length:n},()=>[]),p=Array.from({length:4*n},()=>[]);
let edgeReads=0;for(let i=0;i<G.edges.length;i++){const [u,v,s]=G.edges[i],x=u>>2,y=v>>2;edgeReads++;a[x].push([y,i]);a[y].push([x,i]);p[u].push([v,s]);p[v].push([u,s])}
for(let v=0;v<n;v++)if(G.types[v]==="E")for(let j=1;j<4;j++){p[4*v].push([4*v+j,0]);p[4*v+j].push([4*v,0])}
let labels=new Int32Array(4*n).fill(-1),phase=new Uint8Array(4*n),visits=0;
for(let i=0;i<p.length;i++)if(labels[i]===-1){labels[i]=i;const q=[i];for(let j=0;j<q.length;j++){let u=q[j];for(let [v,s] of p[u]){visits++;if(labels[v]===-1){labels[v]=i;phase[v]=phase[u]^s;q.push(v)}else if(labels[v]!==i||phase[v]!== (phase[u]^s))throw Error("signed conflict")}}}
const regions=new Map();let neighborChecks=0;
for(let v=0;v<n;v++){if(G.types[v]!=="E")continue;let S=[v,...a[v].map(t=>t[0])].sort((a,b)=>a-b);if(S.length!==5||S.some(x=>G.types[x]!=="E"))continue;const inside=S.map(x=>{let d=0;for(let [y] of a[x]){neighborChecks++;if(S.includes(y))d++}return d});if(inside.reduce((s,x)=>s+x,0)!==18||inside.filter(d=>d===3).length!==2||inside.filter(d=>d===4).length!==3)continue;let es=[...new Set(S.flatMap(x=>a[x].filter(([y])=>S.includes(y)).map(z=>z[1])))].sort((a,b)=>a-b);regions.set(S.join(","),{S,es})}
let occupied=new Set(),overlap=0,positive=0;for(const {S,es} of regions.values()){if(S.some(x=>occupied.has(x)))overlap++;S.forEach(x=>occupied.add(x));if(es.every(i=>G.edges[i][2]===0))positive++}
let clauses=new Map(),src=0,res=0,reads=0;
const norm=a=>[...new Set(a)].sort((x,y)=>x-y),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
for(const [id,r] of cert.proof.records){if(clauses.has(id)||!eq(norm(r.c),r.c)||r.c.some(l=>r.c.includes(-l)))throw Error("clause");
if(r.src){src++;if(r.src[0]==="global-complement-gauge"){let v=r.src[1];if(labels[v]!==v||!eq(r.c,[-v-1]))throw Error("gauge")}else{let [v,j,s]=r.src;if(G.types[v]!=="B"||j<0||j>3||![1,-1].includes(s))throw Error("row");let t=[];for(let k=0;k<4;k++)if(k!==j){let u=4*v+k;t.push(s*(labels[u]+1)*(phase[u]?-1:1))}if(!eq(norm(t),r.c))throw Error("axiom")}}
else{res++;let [i,j,v]=r.p,A=clauses.get(i),B=clauses.get(j);if(!A||!B||i>=id||j>=id||!(A.includes(v)&&B.includes(-v)||A.includes(-v)&&B.includes(v)))throw Error("pivot");reads+=A.length+B.length;if(!eq(norm(A.concat(B).filter(l=>Math.abs(l)!==v)),r.c))throw Error("resolvent")}clauses.set(id,r.c)}
if(clauses.get(cert.proof.terminal)?.length!==0)throw Error("terminal");
return {regions:regions.size,coveredVertices:occupied.size,overlap,allPositive:positive,edgeReads,neighborChecks,bfsArcVisits:visits,peerReplay:{src,res,reads,total:clauses.size},firstRegion:[...regions.values()][0]}
}
const [cp,bp,rp,jp,ap]=process.argv.slice(2); const c=fs.readFileSync(cp,'utf8'),compile=Function(c.slice(c.indexOf('function compile('),c.indexOf('function auditLocal('))+';return compile')(); const R=JSON.parse(fs.readFileSync(rp)),B=JSON.parse(fs.readFileSync(bp));const sha=s=>crypto.createHash('sha256').update(s).digest('hex');for(const [id,p,expected] of [['JOINT-24',jp,'90e124b67e0ca91753386857a0b47edb4f8d82c75285edc0b34b710cc6dc9dc9'],['RANDOM-3CNF-40',ap,'2bd9984cb03aaf7fd82f89c3239038a40782b837e561713778bca3d09508dd2c']]){const x=B.instances.find(t=>t.id===id),g=compile(x),e=R.instances.find(t=>t.alias==='EB-'+id),s=JSON.stringify(g.network)+'\n',raw=fs.readFileSync(p);if(sha(s)!==e.sha256||s.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||sha(JSON.stringify(g.source_map)+'\n')!==e.source_map_sha256||sha(raw)!==expected)throw Error('identity');const cert=JSON.parse(raw);if(cert.instance_id!==e.instance_id||cert.guard_id!=='EMPTY'||cert.residual_id!=='ROOT')throw Error('scope');console.log(id,native(g.network,cert))}console.log(JSON.stringify({K5:classify(5,true),K4:classify(4,false)}));

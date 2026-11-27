// Exact source-only bounded table contraction, with independent BFS + full joint enumeration replay. Usage node table_certificate.js compile.js benchmarks.json registry.json [certificate.json]
const fs=require('node:fs'),crypto=require('node:crypto');
function source(G,mode){
 const n=4*G.types.length,pa=Array.from({length:n},(_,i)=>i),ph=new Uint8Array(n),adj=mode==="bfs"?Array.from({length:n},()=>[]):null;
 const find=x=>{if(pa[x]===x)return [x,0];let [r,s]=find(pa[x]);ph[x]^=s;pa[x]=r;return [r,ph[x]]};
 const join=(a,b,s)=>{if(adj){adj[a].push([b,s]);adj[b].push([a,s]);return}let [u,t]=find(a),[v,w]=find(b);if(u===v){if((t^w)!==s)throw Error("inconsistent");return}if(u>v)[u,v]=[v,u];pa[v]=u;ph[v]=s^t^w};
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="E")for(let j=1;j<4;j++)join(4*v,4*v+j,0);for(const [a,b,s] of G.edges)join(a,b,s);
 if(adj){pa.fill(-1);for(let i=0;i<n;i++)if(pa[i]===-1){pa[i]=i;let q=[i];for(let j=0;j<q.length;j++)for(const [v,s] of adj[q[j]]){let u=q[j];if(pa[v]===-1){pa[v]=i;ph[v]=ph[u]^s;q.push(v)}else if(pa[v]!==i||ph[v]!== (ph[u]^s))throw Error("inconsistent")}}}
 const rowMap=new Map();let roots=new Set();for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let l=Array.from({length:4},(_,j)=>{let p=4*v+j,[r,s]=adj?[pa[p],ph[p]]:find(p);roots.add(r+1);return (r+1)*(s?-1:1)}).sort((a,b)=>a-b);let k=l.join(","),rev=l.map(x=>-x).reverse().join(",");if(rev<k){k=rev;l=l.map(x=>-x).reverse()}if(!rowMap.has(k))rowMap.set(k,{l,ids:[]});rowMap.get(k).ids.push(v)}
 const freq=new Map();for(const {l} of rowMap.values())for(const x of new Set(l.map(Math.abs)))freq.set(x,(freq.get(x)||0)+1);
 const anchor=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];
 let factors=[...rowMap.values()].map(({l,ids},id)=>{const vs=[...new Set(l.map(Math.abs))].filter(x=>x!==anchor).sort((a,b)=>a-b),ok=[];for(let a=0;a<2**vs.length;a++)if(l.reduce((sum,x)=>sum+((Math.abs(x)===anchor?0:(a>>vs.indexOf(Math.abs(x)))&1)^Number(x<0)),0)===2)ok.push(a);return {id,vs,ok,ids}});
 return {factors,anchor,roots:roots.size}
}
function contraction(S,records,verify=false,cap=2500000){
 let factors=S.factors.slice(),trace=[],events=0,seq=factors.length;
 const universe=fs=>[...new Set(fs.flatMap(f=>f.vs))].sort((a,b)=>a-b);
 const restrict=(word,U,V)=>V.reduce((s,v,i)=>s+(((word>>U.indexOf(v))&1)<<i),0);
 for(;;){
 const occ=new Map();for(const f of factors)for(const v of f.vs){if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f)}
 let v,fs;if(verify){if(trace.length===records.length)break;v=records[trace.length].v;fs=occ.get(v);if(!fs||fs.length>2||universe(fs).length>7)throw Error("bad bucket")}else{let t=[...occ].filter(([v,fs])=>fs.length<=2&&universe(fs).length<=7).sort((a,b)=>a[1].length-b[1].length||a[0]-b[0])[0];if(!t)break;[v,fs]=t}
 const U=universe(fs),V=U.filter(x=>x!==v);let ok=[];
 if(verify){const seen=new Set();for(let w=0;w<2**U.length;w++)if(fs.every(f=>{events++;return f.ok.includes(restrict(w,U,f.vs))}))seen.add(restrict(w,U,V));ok=[...seen].sort((a,b)=>a-b)}
 else for(let w=0;w<2**V.length;w++)for(let bit=0;bit<=1;bit++){const hit=fs.every(f=>{events++;return f.ok.includes(f.vs.reduce((s,x,i)=>s+((x===v?bit:(w>>V.indexOf(x))&1)<<i),0))});if(hit){ok.push(w);break}}
 if(events>cap)throw Error("cap");const row={v,in:fs.map(f=>f.id),out:seq,vs:V,ok};if(verify&&JSON.stringify(row)!==JSON.stringify(records[trace.length]))throw Error("projection mismatch");trace.push(row);factors=factors.filter(f=>!fs.includes(f));if(ok.length!==2**V.length)factors.push({id:seq,vs:V,ok});seq++;
 }
 return {factors,trace,events}
}
function treeSolve(fs,limit,proof=null){
 let ev=0,nn=0,leaf=0;
 function dfs(pins,p){
 nn++;for(;;){let changed=false;for(const f of fs){let support=f.ok.filter(w=>{ev++;return f.vs.every((v,i)=>!pins.has(v)||pins.get(v)===((w>>i)&1))});if(ev>limit)throw Error("cap");if(!support.length){leaf++;if(proof&&p!==0)throw Error("nonleaf");return 0}for(let i=0;i<f.vs.length;i++){let v=f.vs[i];if(!pins.has(v)&&support.every(w=>((w>>i)&1)===(support[0]>>i&1))){pins.set(v,support[0]>>i&1);changed=true}}}if(!changed)break}
 let count=new Map();for(const f of fs)for(const v of f.vs)if(!pins.has(v))count.set(v,(count.get(v)||0)+1);if(!count.size)throw Error("satisfiable branch");
 let v=proof?p[0]:[...count].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];if(!count.has(v)||proof&&(!Array.isArray(p)||p.length!==3))throw Error("bad split");
 let left=dfs(new Map([...pins,[v,0]]),proof?p[1]:null),right=dfs(new Map([...pins,[v,1]]),proof?p[2]:null);return [v,left,right]
 }
 const tree=dfs(new Map(),proof);return {tree,events:ev,nodes:nn,leaves:leaf}
}
const [cp,bp,rp,certp]=process.argv.slice(2);const c=fs.readFileSync(cp,'utf8'),compile=Function(c.slice(c.indexOf('function compile('),c.indexOf('function auditLocal('))+';return compile')(), R=JSON.parse(fs.readFileSync(rp)),B=JSON.parse(fs.readFileSync(bp));const sha=s=>crypto.createHash('sha256').update(s).digest('hex');for(const id of ['JOINT-24','RANDOM-3CNF-40']){const x=B.instances.find(t=>t.id===id),g=compile(x),e=R.instances.find(t=>t.alias==='EB-'+id),s=JSON.stringify(g.network)+'\n';if(sha(s)!==e.sha256||s.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||sha(JSON.stringify(g.source_map)+'\n')!==e.source_map_sha256)throw Error('identity');if(certp){const p=JSON.parse(fs.readFileSync(certp));if(p.instance_id!==e.instance_id)continue;if(p.guard_id!=='EMPTY'||p.residual_id!=='ROOT'||p.original_N_bits!==e.N_bits)throw Error('scope');const S=source(g.network,'bfs');if(S.anchor!==p.gauge)throw Error('gauge');const C=contraction(S,p.trace,true),T=treeSolve(C.factors,2500000,p.tree);console.log(id,C.events,T.events,T.nodes)}else{const S=source(g.network,'dsu'),C=contraction(S,null),T=treeSolve(C.factors,2500000);console.log(id,C.trace.length,T.nodes,T.events)}}

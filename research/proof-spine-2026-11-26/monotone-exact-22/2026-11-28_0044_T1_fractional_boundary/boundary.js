const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"peer":["research/proof-spine-2026-11-26/closure-finite-groups/2026-11-27_1800_T3_cross_scope/owner-cert.js","faf453592a9c63182fe941dd79d4ef62ba606cef"],"sparse":["research/hcl201/matching/2026-11-27_2330_T1_sparse_separator/separator.json","b70f0f6f45ef8a5287bd0cdb0747786826b7d0e1"]};
const d=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function(d,pins){
const {sha,up}=new Function(d.peer.slice(0,d.peer.indexOf("function compile("))+";return {sha,up}")();
const compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile("),d.compiler.indexOf("function auditLocal"))+";return compile")();
const {project,verifyProjection}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function up("))+";return {project,verifyProjection}")();
const enc=x=>JSON.stringify(x)+"\n",check=(b,m)=>{if(!b)throw Error(m)},key=(a,b)=>a<b?a+","+b:b+","+a,pc=x=>{let k=0;while(x){k++;x&=x-1}return k};
check(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha");
const parse=x=>x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
function analyze(C){
const start=Date.now(),work={scan:0,pairs:0,checks:0,matching:0,guardVisits:0,algebra:0,compression:0};
let counter={visits:0},early=up(C,[],counter,2000000),V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),neg=new Map(),pos=[];
for(let [i,c] of C.entries()){work.scan+=c.length;if(c.length===2&&c.every(x=>x<0)&&c[0]!==c[1])neg.set(key(-c[0],-c[1]),i);if(c.length>=2&&c.every(x=>x>0)&&new Set(c).size===c.length)pos.push({i,c})}
pos.sort((a,b)=>b.c.length-a.c.length||a.i-b.i);let demand=[],D=new Set();
for(let p of pos){work.scan+=p.c.length;if(p.c.some(v=>D.has(v)))continue;demand.push(p);for(let v of p.c)D.add(v)}
let B=V.filter(v=>!D.has(v)),bins=[],un=new Set(D);
for(let v of [...D].sort((a,b)=>a-b)){if(!un.has(v))continue;let b=[v];un.delete(v);for(let w of [...un].sort((a,b)=>a-b)){let ok=true;for(let u of b){work.pairs++;if(!neg.has(key(u,w))){ok=false;break}}if(ok){b.push(w);un.delete(w)}}bins.push(b)}
let blockers=[],upperParents=new Set(demand.map(p=>p.i)),weights=Object.fromEntries(B.map(v=>[v,0]));
for(let b of bins){for(let i=0;i<b.length;i++)for(let j=i+1;j<b.length;j++){work.checks++;check(neg.has(key(b[i],b[j])),"bin clique");upperParents.add(neg.get(key(b[i],b[j])))}
let choice=null;for(let v of B){let yes=true;for(let w of b){work.pairs++;if(!neg.has(key(v,w))){yes=false;break}}if(yes){choice=v;break}}
blockers.push(choice);if(choice!==null){weights[choice]++;for(let w of b){check(neg.has(key(choice,w)),"block");upperParents.add(neg.get(key(choice,w)))}}
}
let consumer=pos.filter(p=>p.c.every(v=>B.includes(v))),deg=Object.fromEntries(B.map(v=>[v,0]));for(let p of consumer)for(let v of p.c){deg[v]++;work.scan++}
let M=Math.max(1,...Object.values(deg)),lower=Math.max(0,Math.ceil((consumer.length-B.reduce((s,v)=>s+M-deg[v],0))/M)),capacity=bins.length-demand.length;
let allWeightOne=B.length>0&&B.every(v=>weights[v]===1),countConflict=allWeightOne&&lower>capacity;
let result={vars:V.length,rows:C.length,early:{pins:early.A.size,conflict:early.bad,visits:counter.visits},boundary:B,demand,bins,blockers,weights,capacity,consumer,deg,M,lower,upperParents:[...upperParents].sort((a,b)=>a-b),countConflict,work};
if(B.length<=12&&B.length>0){
let leftIds=C.map((_,i)=>i).filter(i=>!consumer.some(p=>p.i===i)),rightIds=consumer.map(p=>p.i),table=[],parents=new Map(demand.flatMap((p,j)=>p.c.map(v=>[v,j]))),binOf=new Map(bins.flatMap((b,j)=>b.map(v=>[v,j])));
function witness(mask,remove=-1){let a=new Map(B.map((v,i)=>[v,(mask>>i)&1])),chosen=new Map(),opts=demand.map(p=>p.c.filter(v=>!B.some(t=>a.get(t)&&neg.has(key(t,v))&&neg.get(key(t,v))!==remove)));
function aug(j,seen){for(let v of opts[j]){work.matching++;let b=binOf.get(v);if(seen.has(b))continue;seen.add(b);let old=chosen.get(b);if(!old||aug(old.j,seen)){chosen.set(b,{j,v});return true}}return false}
for(let j=0;j<demand.length;j++)if(!aug(j,new Set()))return null;
for(let v of D)a.set(v,0);for(let {v} of chosen.values())a.set(v,1);
let ok=leftIds.every(i=>i===remove||C[i].some(l=>{work.checks++;return a.get(Math.abs(l))===+(l>0)}));return ok?V.map(v=>a.get(v)):null;
}
let leftSupport=[],rightSupport=[],outer=[],guardConflicts=0;
for(let w=0;w<2**B.length;w++){let a=new Map(B.map((v,i)=>[v,(w>>i)&1])),count=pc(w),weighted=B.reduce((s,v)=>s+weights[v]*a.get(v),0),right=consumer.every(p=>p.c.some(v=>a.get(v))),wit=weighted<=capacity?witness(w):null,excluded=weighted>capacity;let cc={visits:0},g=up(C,B.map(v=>a.get(v)?v:-v),cc,200000);work.guardVisits+=cc.visits;if(g.bad)guardConflicts++;
if(wit)leftSupport.push(w);if(right)rightSupport.push(w);if(weighted<=capacity)outer.push(w);
table.push({w,count,weighted,right,witness:wit,excluded,upConflict:!!g.bad})
}
const exactLeft=table.every(t=>t.excluded||t.witness!==null),exactRight=true,intersection=leftSupport.filter(w=>rightSupport.includes(w));
const exactCountLeft=exactLeft&&allWeightOne&&table.every(t=>(t.witness!==null)===(t.count<=capacity)),exactCountRight=table.every(t=>t.right===(t.count>=lower));
let removals=[];if(countConflict&&exactLeft&&exactCountRight){for(let p of consumer){let w=table.find(t=>t.witness&&consumer.every(q=>q.i===p.i||q.c.some(v=>((t.w>>B.indexOf(v))&1))));if(w){let a=new Map(V.map((v,i)=>[v,w.witness[i]]));check(C.every((c,i)=>i===p.i||c.some(l=>a.get(Math.abs(l))===+(l>0))),"deletion witness");removals.push({row:p.i,mask:w.w,word:w.witness})}}}
let rank=0; if(exactLeft&&leftSupport.length){let basis=new Map();for(let m of leftSupport){let x=m^leftSupport[0];for(let k=B.length-1;k>=0;k--){work.algebra++;if(!(x>>k&1))continue;if(basis.has(k))x^=basis.get(k);else{basis.set(k,x);break}}}rank=basis.size}
result={...result,table,leftSupport,rightSupport,outer,guardConflicts,exactLeft,exactRight,exactCountLeft,exactCountRight,intersection,affineRank:exactLeft?rank:null,removals,compression:{rawMasks:2**B.length,exactCountLeft,exactCountRight,storedBounds:[capacity,lower]},decision:countConflict?"NO":exactLeft&&intersection.length?"SAT (witness available)":exactLeft&&!intersection.length?"NO (exact support join)":"UNKNOWN"};
}else result.decision=capacity<0?"NO (capacity)":"UNKNOWN";
result.ms=Date.now()-start;return result
}
const reg=JSON.parse(d.registry),corp=JSON.parse(d.corpus),sparse=JSON.parse(d.sparse),out=[];
const cases=["JOINT-24","RANDOM-3CNF-40"].map(name=>({name,x:corp.instances.find(x=>x.id===name),r:reg.instances.find(x=>x.alias==="EB-"+name),primary:true}));
for(let z of sparse.result){let dimacs=z.payload.dimacs;cases.push({name:z.meta.alias,x:{dimacs,nvars:+dimacs.split(" ")[2]},r:z.meta,primary:false})}
for(let z of cases){let {name,x,r}=z,G=compile(x),bytes=enc(G.network),N=bytes.length*8,h=sha(bytes),chash=sha(x.dimacs),map=sha(enc(G.source_map)),instance="STRICT-EB4-v1:sha256:"+h;check(instance===r.instance_id&&N===r.N_bits&&chash===r.source_cnf.sha256&&x.dimacs.length*8===r.source_cnf.N_bits&&map===r.source_map_sha256,"authentication "+name);let native=null,projection=null;
if(z.primary){let p=project(G.network),verification=verifyProjection(G.network,p),guard=[[p.anchor,0]],gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",instance,"EB-PORT-PINS-v1",sha(enc(guard))])),ch=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mh=sha(enc({root:p.root,phase:p.phase})),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",instance,gid,"EB-CHART-SYZYGY-v1",ch,mh]));native=analyze(p.clauses);projection={verification,cost:p.cost,carriers:p.carriers,guard,gid,rid,ch,mh};}
let cnf=analyze(parse(x));let entry={name,instance,N,cnf_id:r.source_cnf.instance_id,cnf_short:r.source_cnf.short_id,cnfN:r.source_cnf.N_bits,source_map_hash:map,original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1],clauses:[1,parse(x).length],variables:[1,x.nvars]},projection,native,cnf,parents:[],source_pins:pins,scope:z.primary?"native source-only and companion independent bounded count interface":"independent source-companion recognition; native bytes authenticated only; no new native transfer"};
out.push({entry,certificate_id:"CERT-v1:sha256:"+sha(enc(entry))})}
return out;
};
console.log(JSON.stringify(run(d,pins)));

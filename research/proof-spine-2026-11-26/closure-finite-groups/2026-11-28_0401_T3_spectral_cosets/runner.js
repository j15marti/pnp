const pins={
  "compiler": [
    "research/coordination/shared-eb-2026-11-27/compile.js",
    "21b9d53fb8166c819b24e708656c742cd3c24f10"
  ],
  "corpus": [
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json",
    "e315349cd6c1fe3fa696504859f28312f6aab69a"
  ],
  "reg": [
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json",
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c"
  ],
  "chart": [
    "research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js",
    "52cae4a54513a67dd9468c7e3ee597cf317d67a3"
  ],
  "hash": [
    "research/proof-spine-2026-11-26/closure-finite-groups/2026-11-27_1800_T3_cross_scope/owner-cert.js",
    "faf453592a9c63182fe941dd79d4ef62ba606cef"
  ],
  "prior": [
    "research/proof-spine-2026-11-26/closure-finite-groups/2026-11-27_2116_T3_root_orbit_transport/root-orbit.js",
    "fd9412aa76e4175eab233e4b8bc8ceedacd69899"
  ],
  "joint": [
    "research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/JOINT-24.cert.json",
    "eb3eb5f2098fbfa73cd11540ba270ac997438f78"
  ],
  "random": [
    "research/hcl201/synthesis/2026-11-27_T4_gauge_factorial/RANDOM-3CNF-40.cert.json",
    "f96bea02c40c7545eb32c7fd5ac37afac7e436e8"
  ]
};
const run=async function(d,pins,loadPeer){
const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,solve,replay}")();
const enc=x=>JSON.stringify(x)+"\n",ck=(v,m)=>{if(!v)throw Error(m)},key=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
const {up,rup,occupancy,affine,conservation,lanes}=new Function("const key="+key.toString()+";"+d.prior.slice(d.prior.indexOf("function up("),d.prior.indexOf("const mono="))+";return {up,rup,occupancy,affine,conservation,lanes}")();
ck(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","hash");
function wht(a){let ops=0;for(let h=1;h<a.length;h*=2)for(let j=0;j<a.length;j+=2*h)for(let i=j;i<j+h;i++){let x=a[i],y=a[i+h];a[i]=x+y;a[i+h]=x-y;ops+=2}return ops}
function dot(a,b){let x=a&b,p=0;while(x){p^=1;x&=x-1}return p}
function basis(xs){let B=new Map();for(let x of xs){while(x){let k=31-Math.clz32(x);if(!B.has(k)){B.set(k,x);break}x^=B.get(k)}}return [...B.values()]}
function region(F,v){let B=[...new Set(F.filter(c=>c.some(l=>Math.abs(l)===v)).flat().map(Math.abs))].filter(w=>w!==v).sort((a,b)=>a-b),scope=[v,...B],rows=F.flatMap((c,i)=>c.every(l=>scope.includes(Math.abs(l)))?[i]:[]);return {v,B,scope,rows}}
function support(F,R,seeds=[]){let ix=new Map(R.scope.map((v,i)=>[v,i])),rows=[...R.rows.map(i=>F[i]),...seeds],masks=[],visits=0;for(let w=0;w<2**R.scope.length;w++){let ok=true;for(let c of rows){let hit=false;for(let l of c){visits++;if((w>>ix.get(Math.abs(l))&1)===Number(l>0)){hit=true;break}}if(!hit){ok=false;break}}if(ok)masks.push(w)}return {masks,visits}}
function compress(S,k,mode){const L=2**k, has=new Uint8Array(L),a=Array(L).fill(0);for(let x of S)has[x]=a[x]=1;let ops=0,rank=0,stab=[],order=Array.from({length:L-1},(_,i)=>i+1);
if(mode!=="lex"){ops+=wht(a);let freq=a.flatMap((x,i)=>x?[i]:[]),B=basis(freq);rank=B.length;stab=order.filter(h=>B.every(u=>!dot(u,h)));let sq=a.map(x=>x*x);ops+=wht(sq);ck(sq.every(x=>x%L===0),"integer correlation");if(mode==="spectral")order.sort((x,y)=>sq[y]-sq[x]||x-y);else order.sort((x,y)=>Number(stab.includes(y))-Number(stab.includes(x))||sq[y]-sq[x]||x-y);ck(stab.every(h=>S.every(x=>has[x^h])),"stabilizer");}
let rem=has.slice(),cells=[],queries=0,failed=0,limit=2000000;for(let a of S){if(!rem[a])continue;let pts=[a],B=[];for(let h of order){if(pts.includes(a^h))continue;let good=true;for(let x of pts){queries++;if(queries>limit){return {status:"UNKNOWN",queries,ops,failed}}if(!rem[x^h]){good=false;break}}if(!good){failed++;continue}B.push(h);pts.push(...pts.map(x=>x^h));}for(let x of pts)rem[x]=0;cells.push({a,B});}
let seen=new Uint8Array(L),checks=0;for(let {a,B} of cells){ck(basis(B).length===B.length,"independence");for(let m=0;m<2**B.length;m++){let x=a;for(let j=0;j<B.length;j++){checks++;if(m>>j&1)x^=B[j]}ck(has[x]&&!seen[x],"cover");seen[x]=1}}ck(S.every(x=>seen[x]),"exhaustive coverage");return {status:"exact",cells,queries,failed,ops,checks,rank,stabilizerDimension:mode==="lex"?null:k-rank,encodedBits:cells.reduce((s,c)=>s+k*(1+c.B.length)+Math.ceil(Math.log2(k+1)),0),points:S.length,maximumDimension:Math.max(0,...cells.map(c=>c.B.length))}
}
function chartGluing(A,B,k,overlap){let checks=0,hits=0, maxRank=0; // explicit affine equations in generator coefficients, no point enumeration
for(let a of A.cells)for(let b of B.cells){let cols=[...a.B,...b.B],rhs=a.a^b.a,mask=overlap;let piv=new Map(),rank=0;for(let c of cols){let x=c&mask;while(x){checks++;let j=31-Math.clz32(x);if(!piv.has(j)){piv.set(j,x);rank++;break}x^=piv.get(j)}}let x=rhs&mask;while(x){checks++;let j=31-Math.clz32(x);if(!piv.has(j))break;x^=piv.get(j)}hits+=Number(x===0);maxRank=Math.max(maxRank,rank)}return {pairs:A.cells.length*B.cells.length,compatible:hits,checks,maxRank}}
function audit(S,k){let modes={};for(let mode of ["lex","spectral","hybrid"])modes[mode]=compress(S,k,mode);let m=modes.hybrid;if(m.status==="exact"){let glue=chartGluing(m,m,k,(1<<k)-1);ck(glue.compatible===m.cells.length,"disjoint exact self glue");m.selfGlue=glue}return modes}
function feedback(F){let V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),out=[];for(let mode of ["baseline","table","residue"]){let visits=0,ties=0,ends=[];function score(A){let bad=0,zero=0;for(let c of F){let k=0,s=0;for(let l of c){visits++;if(A.get(Math.abs(l))===Number(l>0)){k++;s+=l>0?1:-1}}if(!k)bad++;else if(mode==="residue"&&(s%3+3)%3===0)zero++}return [bad,zero]}for(let init of [0,1]){let A=new Map(V.map(v=>[v,init])),cur=score(A);for(let i=0;i<8;i++){let best=[];for(let v of V){A.set(v,A.get(v)^1);let q=score(A);A.set(v,A.get(v)^1);if(q[0]<cur[0]&&(!best.length||q[0]<=best[0][1][0])){if(best.length&&q[0]<best[0][1][0])best=[];best.push([v,q])}}if(!best.length)break;let b=mode==="residue"?best.slice().sort((a,b)=>a[1][1]-b[1][1]||a[0]-b[0])[0]:best[0];ties+=Number(b[0]!==best[0][0]);A.set(b[0],A.get(b[0])^1);cur=b[1]}ends.push(cur[0])}out.push({mode,visits,ties,ends})}return out}
let base=[];for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=JSON.parse(d.corpus).instances.find(x=>x.id===name),ref=JSON.parse(d.reg).instances.find(x=>x.alias==="EB-"+name),G=compile(x),native=enc(G.network);ck(sha(native)===ref.sha256&&native.length*8===ref.N_bits&&sha(x.dimacs)===ref.source_cnf.sha256&&x.dimacs.length*8===ref.source_cnf.N_bits&&sha(enc(G.source_map))===ref.source_map_sha256,"auth");let p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",ref.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",ref.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
let early={up:up(F),occupancy:occupancy(p.raw,[-(p.anchor+1)]),affine:affine(p.raw,[-(p.anchor+1)]),conservation:conservation(G.network,p,[-(p.anchor+1)])};
let V=[...new Set(F.flat().map(Math.abs))],R=V.map(v=>region(F,v)).filter(r=>r.B.length<=11).sort((a,b)=>a.B.length-b.B.length||a.v-b.v)[0];let S=support(F,R),A=audit(S.masks,R.scope.length),L=lanes(G.network,p,F),stand=solve(F),standCheck=replay(F,stand.tree),ad=adapter(p,G,x.dimacs,x.nvars),cnfEarly=up(ad.orig),cnf=solve(ad.orig),cnfCheck=replay(ad.orig,cnf.tree);base.push({name,ref,p,F,projection,chartHash,mapHash,gid,rid,early,R,S,A,L,stand,standCheck,cnfEarly,cnf,cnfCheck})}
let peers=await loadPeer(),out=[];for(let z of base){let {name,ref,p,F,projection,chartHash,mapHash,gid,rid,early,R,S,A,L,stand,standCheck,cnfEarly,cnf,cnfCheck}=z,raw=peers[name==="JOINT-24"?"joint":"random"],C=JSON.parse(raw);ck(C.instance_id===ref.instance_id&&C.internal_guard===gid&&C.internal_residual===rid&&C.chartHash===chartHash&&C.mapHash===mapHash,"peer scope");let seeds=[];for(let c of C.proof){if(!c.includes(C.anchor))break;let q=c.filter(l=>l!==C.anchor);if(!q.length)break;seeds.push(q)}let sr=rup(F,seeds);ck(sr.ok,"peer RUP");let local=seeds.filter(c=>c.every(l=>R.scope.includes(Math.abs(l)))),SS=support(F,R,local),AA=audit(SS.masks,R.scope.length),abl=local.map((c,i)=>{let a=support(F,R,local.filter((_,j)=>i!==j));return {removed:c,points:a.masks.length,visits:a.visits}}),cl=up([...F,...local]),fb=cl.conflict?{stage:"unreachable"}:feedback([...F,...local]),hybrid=solve([...F,...local]),hc=replay([...F,...local],hybrid.tree);let cert={format:"T3-SPECTRAL-COSET-v1",problem_id:"STRICT-EB4-v1",instance:ref.short_id,instance_id:ref.instance_id,original_N_bits:ref.N_bits,source_pins:pins,guard_id:gid,residual_id:rid,chartHash,mapHash,original_ids:{vertices:[0,ref.vertices-1],ports:[0,4*ref.vertices-1],edges:[0,ref.edges-1]},parent_certificate_ids:["CERT-v1:sha256:"+sha(raw)],region:R,source:S,sourceCover:A,local,seeded:SS,seededCover:AA,ablation:abl};out.push({cert,certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),early,L,projection,projectCost:p.cost,stand:{nodes:stand.nodes,work:stand.work,check:standCheck},cnf:{nodes:cnf.nodes,work:cnf.work,check:cnfCheck,early:cnfEarly},import:sr,hybrid:{nodes:hybrid.nodes,work:hybrid.work,check:hc},fb})}
let controls=[];for(let k of [3,5,8]){let S=Array.from({length:2**k},(_,i)=>i).filter(x=>(x&3)!==3);let a=audit(S,k);controls.push({k,S,a})}return {out,controls,execution:"serial, counted membership queries, exact bounded integer transform, no complete bit clock or RSS; feedback flip scoring only"}};
const fs=require('node:fs');const load=async keys=>Object.fromEntries(keys.map(k=>[k,fs.readFileSync(k+'.txt','utf8')]));(async()=>console.log(JSON.stringify(await run(await load(['compiler','corpus','reg','chart','hash','prior']),pins,()=>load(['joint','random'])),null,2)))().catch(e=>{console.error(e);process.exitCode=1});

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
  ],
  "delta": [
    "research/coordination/2026-11-28_0100_UCAC_review/region-delta-evidence.json",
    "3b42d0efc1bb6b342d5375951c7b44a287c62f43"
  ]
};
const run=async function(d,pins,loadPeer){
const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,solve,replay}")();
const enc=x=>JSON.stringify(x)+"\n",ck=(b,m)=>{if(!b)throw Error(m)},key=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
const {up,rup,occupancy,affine,conservation,lanes}=new Function("const key="+key.toString()+";"+d.prior.slice(d.prior.indexOf("function up("),d.prior.indexOf("const mono="))+";return {up,rup,occupancy,affine,conservation,lanes}")();
ck(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","hash");
const pc=x=>{let n=0;while(x){x&=x-1;n++}return n};
const parity=x=>{let b=0;while(x){x&=x-1n;b^=1}return b};
function mons(n,k){return Array.from({length:2**n},(_,i)=>i).filter(i=>pc(i)<=k)}
function features(w,M){let z=0n;for(let i=0;i<M.length;i++)if((w&M[i])===M[i])z|=1n<<BigInt(i);return z}
function rank(rows){let E=new Map(),xor=0;for(let z of rows){while(z){let k=z.toString(2).length-1;if(!E.has(k)){E.set(k,z);break}z^=E.get(k);xor++}}return {rank:E.size,xor}}
function fit(rows,n){let E=new Map(),xor=0;for(let [z,b] of rows){while(z){let k=z.toString(2).length-1;if(!E.has(k)){E.set(k,[z,b]);break}let [q,v]=E.get(k);z^=q;b^=v;xor++}if(!z&&b)return {ok:false,xor}}let out=0n;for(let [k,[z,b]] of [...E].sort((a,b)=>a[0]-b[0]))if(parity(z&out)!==b)out|=1n<<BigInt(k);ck(rows.every(([z,b])=>parity(z&out)===b),"fit");return {ok:true,coeff:String(out),xor}}
function region(F,v){let B=[...new Set(F.filter(c=>c.some(l=>Math.abs(l)===v)).flat().map(Math.abs))].filter(w=>w!==v).sort((a,b)=>a-b),scope=[v,...B],rows=F.flatMap((c,i)=>c.every(l=>scope.includes(Math.abs(l)))?[i]:[]);return {v,B,scope,rows}}
function support(F,R,seeds=[]){const ix=new Map(R.scope.map((v,i)=>[v,i]));let rows=[...R.rows.map(i=>F[i]),...seeds],masks=[],visits=0,replayVisits=0;for(let w=0;w<2**R.scope.length;w++){let ok=true;for(let c of rows){let hit=false;for(let l of c){visits++;if((w>>ix.get(Math.abs(l))&1)===Number(l>0)){hit=true;break}}if(!hit){ok=false;break}}if(ok)masks.push(w)}let ref=[];for(let w=0;w<2**R.scope.length;w++){let A=new Map(R.scope.map((v,i)=>[v,w>>i&1]));let ok=true;for(let c of rows){let hit=false;for(let l of c){replayVisits++;hit=hit||A.get(Math.abs(l))===Number(l>0)}ok=ok&&hit}if(ok)ref.push(w)}ck(ref.join()===masks.join(),"support replay");return {masks,visits,replayVisits}}
function analyze(masks,k){let map=new Map();for(let w of masks){let b=w>>1;map.set(b,(map.get(b)||0)|(1<<(w&1)))}let S=[...map.keys()],D=S.filter(b=>map.get(b)===3),M=mons(k,2),Q=mons(k+1,2),A=mons(k,1),f1=fit(S.filter(b=>map.get(b)!==3).map(b=>[features(b,A),Number(map.get(b)===2)]),A.length),f2=fit(S.filter(b=>map.get(b)!==3).map(b=>[features(b,M),Number(map.get(b)===2)]),M.length);
let sel=b=>f1.ok?parity(features(b,A)&BigInt(f1.coeff)):f2.ok?parity(features(b,M)&BigInt(f2.coeff)):Number(map.get(b)===2);
let graph=S.map(b=>(b<<1)|sel(b));ck(graph.every(w=>masks.includes(w)),"section witness");
let G=graph.map(w=>features(w,Q)),diff=D.map(b=>features(b<<1,Q)^features((b<<1)|1,Q)),G0=rank(G),R0=rank(masks.map(w=>features(w,Q))),GD=rank([...G,...diff]),B0=rank(S.map(b=>features(b,M))),A0=rank(S.map(b=>features(b,A))),D0=rank(D.map(b=>features(b,A)));
ck(GD.rank===R0.rank,"fiber rank identity");let fvals=Array.from({length:2**k},(_,b)=>f1.ok?parity(features(b,A)&BigInt(f1.coeff)):f2.ok?parity(features(b,M)&BigInt(f2.coeff)):Number(map.get(b)===2));for(let i=0;i<k;i++)for(let b=0;b<2**k;b++)if(b>>i&1)fvals[b]^=fvals[b^(1<<i)];let anf=fvals.flatMap((a,b)=>a?[b]:[]);let degree=anf.reduce((a,b)=>Math.max(a,pc(b)),0);let witness=D.length?{selected:(D[0]<<1)|sel(D[0]),other:(D[0]<<1)|(sel(D[0])^1)}:null;
return {support:S.length,tuples:masks.length,doubleFibers:D.length,boundaryAffineDimension:A0.rank-1,boundaryDegree2Rank:M.length-B0.rank,rootDegree2Rank:Q.length-R0.rank,sectionDegree2Rank:Q.length-G0.rank,invalidSectionRank:R0.rank-G0.rank,ambiguityConstraintRank:D0.rank,fitAffine:f1,fitQuadratic:f2,sectionANF:anf,sectionDegree:degree,witness,rankXors:G0.xor+R0.xor+GD.xor+B0.xor+A0.xor+D0.xor,featureEntries:graph.length*Q.length*2+D.length*Q.length*2+masks.length*Q.length+S.length*(M.length+A.length)*2}}
function feedback(F,mode){let V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),visits=0,tie=0,ends=[];function score(A){let bad=0,zero=0;for(let c of F){let k=0,s=0;for(let l of c){visits++;if(A.get(Math.abs(l))===Number(l>0)){k++;s+=l>0?1:-1}}let km=k%3,sm=(s%3+3)%3;ck(km>=0,"residue");if(!k)bad++;else if(!sm)zero++}return [bad,zero]}for(let b of [0,1]){let A=new Map(V.map(v=>[v,b])),cur=score(A),moves=[];for(let j=0;j<8;j++){let best=[];for(let v of V){A.set(v,A.get(v)^1);let s=score(A);A.set(v,A.get(v)^1);if(s[0]<cur[0]&&(!best.length||s[0]<=best[0].s[0])){if(best.length&&s[0]<best[0].s[0])best=[];best.push({v,s})}}if(!best.length)break;let q=mode==="residue"?best.slice().sort((a,b)=>a.s[1]-b.s[1]||a.v-b.v)[0]:best[0];tie+=Number(q.v!==best[0].v);A.set(q.v,A.get(q.v)^1);cur=q.s;moves.push(q.v)}ends.push({bad:cur[0],moves})}return {mode,visits,tie,ends}}
let bases=[];
for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=JSON.parse(d.corpus).instances.find(x=>x.id===name),ref=JSON.parse(d.reg).instances.find(x=>x.alias==="EB-"+name),G=compile(x),native=enc(G.network);ck(sha(native)===ref.sha256&&native.length*8===ref.N_bits&&sha(x.dimacs)===ref.source_cnf.sha256&&x.dimacs.length*8===ref.source_cnf.N_bits&&sha(enc(G.source_map))===ref.source_map_sha256,"auth");let p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",ref.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",ref.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));let early={up:up(F),occupancy:occupancy(p.raw,[-(p.anchor+1)]),affine:affine(p.raw,[-(p.anchor+1)]),conservation:conservation(G.network,p,[-(p.anchor+1)])},L=lanes(G.network,p,F),stand=solve(F),standCheck=replay(F,stand.tree),ad=adapter(p,G,x.dimacs,x.nvars),cnfEarly=up(ad.orig),cnfStand=solve(ad.orig),cnfCheck=replay(ad.orig,cnfStand.tree);
let vars=[...new Set(F.flat().map(Math.abs))],regions=vars.map(v=>region(F,v)).filter(r=>r.B.length<=11).sort((a,b)=>a.B.length-b.B.length||a.v-b.v).slice(0,3).map(R=>{let S=support(F,R);return {R,S,A:analyze(S.masks,R.B.length)}});bases.push({name,ref,p,F,projection,chartHash,mapHash,gid,rid,early,L,stand,standCheck,ad,cnfEarly,cnfStand,cnfCheck,regions})}
const peers=await loadPeer(),delta=JSON.parse(peers.delta),cases=[];
for(const z of bases){let {name,ref,p,F,projection,chartHash,mapHash,gid,rid,early,L,stand,standCheck,ad,cnfEarly,cnfStand,cnfCheck,regions}=z,raw=peers[name==="JOINT-24"?"joint":"random"],C=JSON.parse(raw),D=delta.find(e=>e.cert.instance_id===ref.instance_id);ck(C.instance_id===ref.instance_id&&C.internal_guard===gid&&C.internal_residual===rid&&C.chartHash===chartHash&&C.mapHash===mapHash,"peer scope");ck(D.cert.guard_id===gid&&D.cert.residual_id===rid&&D.cert.chartHash===chartHash&&D.cert.mapHash===mapHash&&D.cert.parent_certificate_id==="CERT-v1:sha256:"+sha(raw),"delta scope");let seeds=[];for(let c of C.proof){if(!c.includes(C.anchor))break;let q=c.filter(l=>l!==C.anchor);if(!q.length)break;seeds.push(q)}let sr=rup(F,seeds);ck(sr.ok,"peer RUP");let imports=seeds.slice(0,seeds.length);let selected=D.cert.regions.find(q=>q.interior===(name==="JOINT-24"?42:209));let R=region(F,selected.interior);ck(R.scope.join()===selected.scope.join()&&R.rows.join()===selected.sourceRows.join(),"region exact");let S=support(F,R);ck(S.masks.length===selected.initialTuples,"initial peer");let eligible=selected.seedRows.map(e=>{ck(key(seeds[e.i])===key(e.q),"seed index");return e.q});let SS=support(F,R,eligible);ck(SS.masks.join()===selected.finalWitnesses.join(),"final peer witness");let a=analyze(S.masks,R.B.length),b=analyze(SS.masks,R.B.length);let ablations=eligible.map((q,i)=>{let E=eligible.filter((_,j)=>i!==j),T=support(F,R,E);return {removed:q,tupleCount:T.masks.length,analysis:analyze(T.masks,R.B.length),visits:T.visits+T.replayVisits}});let cl=up([...F,...eligible]),hybrid=solve([...F,...eligible]),hc=replay([...F,...eligible],hybrid.tree);let fb=cl.conflict?{stage:"unreachable"}:{stage:"after independently checked local imports before final verification",baseline:feedback([...F,...eligible],"baseline"),table:feedback([...F,...eligible],"table"),residue:feedback([...F,...eligible],"residue")};
let cert={format:"T3-FIBER-SECTION-RANK-v1",problem_id:"STRICT-EB4-v1",instance:ref.short_id,instance_id:ref.instance_id,original_N_bits:ref.N_bits,source_pins:pins,guard_id:gid,residual_id:rid,chartHash,mapHash,original_ids:{vertices:[0,ref.vertices-1],ports:[0,4*ref.vertices-1],edges:[0,ref.edges-1]},parent_certificate_ids:["CERT-v1:sha256:"+sha(raw),D.certificate_id],region:R,source:S,seeded:SS,eligible,sourceAnalysis:a,seededAnalysis:b,ablations,blindRegions:regions.map(q=>({region:q.R,analysis:q.A,visits:q.S.visits+q.S.replayVisits})),claim:"Exact section+ambiguity criterion for root degree-two vanishing identities. Section-only rank is not admission credit. All retained original-carrier tuples independently checked."};cases.push({cert,certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),projection,projectCost:p.cost,early,L,stand:{nodes:stand.nodes,work:stand.work},standCheck,cnfEarly,cnfStand:{nodes:cnfStand.nodes,work:cnfStand.work},cnfCheck,sr,hybrid:{nodes:hybrid.nodes,work:hybrid.work},hc,fb})}
let controls=[];for(let n=3;n<=8;n++){let full=Array.from({length:2**(n+1)},(_,w)=>w),graph=Array.from({length:2**n},(_,b)=>(b<<1)|Number((b&7)===7));controls.push({n,full:analyze(full,n),graph:analyze(graph,n)})}return {cases,controls,execution:"serial, scoped; no complete aggregate bit clock/RSS; flip scoring only; no full width-four feedback; no reference proof used for standalone discovery"};
};
const fs=require('node:fs');const load=async keys=>Object.fromEntries(keys.map(k=>[k,fs.readFileSync(k+'.txt','utf8')]));(async()=>console.log(JSON.stringify(await run(await load(['compiler','corpus','reg','chart','hash','prior']),pins,()=>load(['joint','random','delta'])),null,2)))().catch(e=>{console.error(e);process.exitCode=1});

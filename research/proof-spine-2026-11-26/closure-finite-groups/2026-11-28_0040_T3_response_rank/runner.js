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
    "research/coordination/2026-11-27_2200_UCAC_review/JOINT-24.delta.cert.json",
    "e7fe31e16dff1b176a7c35b8d64b235c5fea09ff"
  ],
  "random": [
    "research/coordination/2026-11-27_2200_UCAC_review/RANDOM-3CNF-40.delta.cert.json",
    "c2d8ff7bd6d6037e86f208b413bf1e58086b9137"
  ]
};
const run=async function(d,pins,loadPeers){
const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,solve,replay}")();
const key=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(","),enc=x=>JSON.stringify(x)+"\n",ck=(b,m)=>{if(!b)throw Error(m)};
const {up,rup,occupancy,affine,conservation,joins,lanes}=new Function("const key="+key.toString()+";"+d.prior.slice(d.prior.indexOf("function up("),d.prior.indexOf("const mono="))+";return {up,rup,occupancy,affine,conservation,joins,lanes}")();
ck(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","hash");
function region(F,forced=null){let vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),candidates=[],scans=0;for(let v of vars){if(forced!==null&&v!==forced)continue;let A=[],B=new Set();F.forEach((c,i)=>{scans+=c.length;if(c.some(l=>Math.abs(l)===v)){A.push(i);for(let l of c)if(Math.abs(l)!==v)B.add(Math.abs(l))}});if(B.size<=12)candidates.push({v,A,B:[...B].sort((a,b)=>a-b)})}candidates.sort((a,b)=>a.B.length-b.B.length||a.v-b.v);return {r:candidates[0]??null,scans,candidates:candidates.length}}
function response(F,r){let {v,A,B}=r,good=[],witness=[],visits=0,checks=0,ix=new Map(B.map((v,i)=>[v,i]));const evalc=(c,w,b)=>{for(let l of c){visits++;let u=Math.abs(l)===v?b:w>>ix.get(Math.abs(l))&1;if(u===Number(l>0))return true}return false};for(let w=0;w<2**B.length;w++){let b=-1;for(let j=0;j<2;j++)if(A.every(i=>evalc(F[i],w,j))){b=j;break}if(b>=0){good.push(w);witness.push(b)}}// Independent reverse exhaustive projection, including both witnesses.
let ref=[];for(let w=0;w<2**B.length;w++){let hit=false;for(let b of [1,0]){let M=new Map(B.map((v,i)=>[v,w>>i&1]));M.set(v,b);let ok=true;for(let i of A){let sat=false;for(let l of F[i]){checks++;sat ||= M.get(Math.abs(l))===Number(l>0)}ok&&=sat}hit ||= ok}if(hit)ref.push(w)}ck(ref.join()===good.join(),"response");return {good,witness,visits,checks}}
function algebra(B,support){let n=B.length,mons=[0];for(let i=0;i<n;i++)mons.push(1<<i);for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)mons.push((1<<i)|(1<<j));let D=mons.length,work={features:0,xors:0,evals:0,products:0};function ins(M,z){while(z){let k=z.toString(2).length-1;if(M.has(k)){z^=M.get(k);work.xors++}else{M.set(k,z);return true}}return false}function feature(w){let z=0n;for(let i=0;i<D;i++){work.features++;if((w&mons[i])===mons[i])z|=1n<<BigInt(i)}return z}function kernel(S){let M=new Map();for(let w of S)ins(M,feature(w));let basis=[];for(let i=0;i<D;i++)if(!M.has(i)){let z=1n<<BigInt(i);for(let [k,row] of [...M].sort((a,b)=>a[0]-b[0])){let a=z&row,b=0;while(a){a&=a-1n;b^=1;work.evals++}if(b)z|=1n<<BigInt(k)}basis.push(z)}return basis}function evalp(z,w){let a=z&feature(w),b=0;while(a){a&=a-1n;b^=1;work.evals++}return b}
const W=kernel(support);for(let p of W)for(let w of support)ck(!evalp(p,w),"source basis");if(n<3)return {D,sourceRank:W.length,work,stage:"no three boundary bits"};
let best=null;const highmask=(1n<<BigInt(2**n))-1n; // upper bounded at n<=12
let dm=new Map(mons.map((m,i)=>[m,i]));function pull(z,a,b,g){let out=0n;for(let i=0;i<D;i++)if(z>>BigInt(i)&1n){let m=mons[i],s=m,ba=m>>a&1,bb=m>>b&1;if(ba!==bb)s^=(1<<a)|(1<<b);out^=1n<<BigInt(m);out^=1n<<BigInt(m|1<<g);out^=1n<<BigInt(s|1<<g);work.products+=3}return out}
function swap(w,a,b,g){return (w>>g&1)&&((w>>a^w>>b)&1)?w^((1<<a)|(1<<b)):w}
function compact(q){let z=0n;for(let [m,i] of dm)if(q>>BigInt(m)&1n)z|=1n<<BigInt(i);return z}
let allowed=0n;for(let m of mons)allowed|=1n<<BigInt(m);
for(let g=0;g<Math.min(n,4);g++){let [a,b]=Array.from({length:n},(_,i)=>i).filter(i=>i!==g);let H=new Map(),safe=[],direct=[],sourceComb=[];for(let i=0;i<W.length;i++){let q=pull(W[i],a,b,g),h=q&(highmask^allowed),c=1n<<BigInt(i);if(!h)direct.push(compact(q));while(h){let k=h.toString(2).length-1;if(!H.has(k)){H.set(k,{h,q,c});break}let r=H.get(k);h^=r.h;q^=r.q;c^=r.c;work.xors++}if(!h){safe.push(compact(q));sourceComb.push(c)}}let S=support.map(w=>swap(w,a,b,g)).sort((a,b)=>a-b),V=kernel(S),M=new Map();for(let z of safe)ck(ins(M,z),"safe independence");let safeRank=M.size;for(let z of V)ins(M,z);ck(M.size===V.length&&safeRank===W.length-H.size,"rank");for(let z of safe)for(let w of S)ck(!evalp(z,w),"target eval");let candidate={a:B[a],b:B[b],g:B[g],sourceRank:W.length,highRank:H.size,safeRank,directRank:direct.length,targetRank:V.length,renewed:V.length-safeRank,sourceBasis:W.map(String),safeBasis:safe.map(String),combinations:sourceComb.map(String),targetBasis:V.map(String),targetSupport:S};if(!best||candidate.highRank>best.highRank)best=candidate}return {D,mons,...best,work}}
function feedback(F,mode){let vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),visits=0,changed=0,ends=[];function score(A){let bad=0,zero=0;for(let c of F){let k=0,s=0;for(let l of c){visits++;if(A.get(Math.abs(l))===Number(l>0)){k++;s+=l>0?1:-1}}let km=k%3,sm=(s%3+3)%3;if(k===0)bad++;else if(sm===0)zero++;ck(km>=0,"residue")}return [bad,zero]}for(let b of [0,1]){let A=new Map(vars.map(v=>[v,b])),cur=score(A),moves=[];for(let j=0;j<vars.length&&visits<300000;j++){let best=[];for(let v of vars){A.set(v,A.get(v)^1);let s=score(A);A.set(v,A.get(v)^1);if(s[0]<cur[0]&&(!best.length||s[0]<=best[0].s[0])){if(best.length&&s[0]<best[0].s[0])best=[];best.push({v,s})}}if(!best.length)break;let q=mode==="residue"?best.slice().sort((a,b)=>a.s[1]-b.s[1]||a.v-b.v)[0]:best[0];changed+=Number(q.v!==best[0].v);A.set(q.v,A.get(q.v)^1);cur=q.s;moves.push(q.v)}ends.push({bad:cur[0],moves})}return {mode,visits,changed,ends}}
let base=[];
for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=JSON.parse(d.corpus).instances.find(x=>x.id===name),ref=JSON.parse(d.reg).instances.find(x=>x.alias==="EB-"+name),G=compile(x),native=enc(G.network);ck(sha(native)===ref.sha256&&native.length*8===ref.N_bits&&sha(x.dimacs)===ref.source_cnf.sha256&&x.dimacs.length*8===ref.source_cnf.N_bits&&sha(enc(G.source_map))===ref.source_map_sha256,"auth");let p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",ref.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",ref.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));let early={up:up(F),occupancy:occupancy(p.raw,[-(p.anchor+1)]),affine:affine(p.raw,[-(p.anchor+1)]),conservation:conservation(G.network,p,[-(p.anchor+1)])},L=lanes(G.network,p,F),stand=solve(F),standCheck=replay(F,stand.tree),ad=adapter(p,G,x.dimacs,x.nvars),cnfEarly=up(ad.orig),cnfStand=solve(ad.orig),cnfCheck=replay(ad.orig,cnfStand.tree),R=region(F);ck(R.r,"bounded region");let S=response(F,R.r),K=algebra(R.r.B,S.good);base.push({name,ref,p,F,projection,chartHash,mapHash,gid,rid,early,L,stand,standCheck,ad,cnfEarly,cnfStand,cnfCheck,R,S,K})}
let peers=await loadPeers(),cases=[];
for(let z of base){let {name,ref,p,F,projection,chartHash,mapHash,gid,rid,early,L,stand,standCheck,ad,cnfEarly,cnfStand,cnfCheck,R,S,K}=z,k=name==="JOINT-24"?"joint":"random",raw=peers[k],C=JSON.parse(raw);ck(C.instance_id===ref.instance_id&&C.guard_id===gid&&C.residual_id===rid&&C.chartHash===chartHash&&C.mapHash===mapHash,"peer scope");let sr=rup(F,C.seeds);ck(sr.ok,"seed replay");let A=[...F,...C.seeds],eligible=C.seeds.filter(c=>c.every(l=>[R.r.v,...R.r.B].includes(Math.abs(l)))),J=[...F,...eligible],RR=region(J,R.r.v);ck(RR.r&&RR.r.B.join()===R.r.B.join(),"same boundary");let SS=response(J,RR.r),KK=algebra(RR.r.B,SS.good);ck(SS.good.every(w=>S.good.includes(w)),"monotone");let ablations=[];for(let i=0;i<C.seeds.length;i++){let s=C.seeds.filter((_,j)=>i!==j),r=rup(F,s);let E=s.filter(c=>c.every(l=>[R.r.v,...R.r.B].includes(Math.abs(l)))),Q=[...F,...E],r2=region(Q,R.r.v),q=r.ok?response(Q,r2.r):null;ablations.push({removed:i,admitted:r.ok,work:r.work,regionSupport:q?.good.length,regionChecks:q? q.visits+q.checks:0})}
let B=[...A],hybrid=solve(B),hybridCheck=replay(B,hybrid.tree),cl=up(B);let fb=cl.conflict?{stage:"unreachable after seed closure"}:{stage:"after seeds before final replay",baseline:feedback(B,"baseline"),table:feedback(B,"table"),residue:feedback(B,"residue"),limitation:"flip scoring only; no learned width-4 feedback"};
let M=new Map(ad.mapping.map(([i,v,s])=>[v,[i,s]])),compSeeds=C.seeds.map(c=>c.map(l=>{let [i,s]=M.get(Math.abs(l));return i*(l>0?1:-1)*(s?-1:1)})),compRup=rup(ad.orig,compSeeds);ck(compRup.ok,"comp replay");let cert={schema:"T3-exact-response-rank-v1",problem_id:"STRICT-EB4-v1",instance:ref.short_id,instance_id:ref.instance_id,original_N_bits:ref.N_bits,source_pins:pins,guard_id:gid,residual_id:rid,chartHash,mapHash,original_ids:{vertices:[0,ref.vertices-1],ports:[0,4*ref.vertices-1],edges:[0,ref.edges-1]},parents:["CERT-v1:sha256:"+sha(raw)],region:R,sourceResponse:S,sourceAlgebra:K,eligibleSeeds:eligible,seededRegion:RR,seededResponse:SS,seededAlgebra:KK,ablation:ablations,claim:"Exact local existential response and degree-two transport kernel under supplied controlled swap; ranks are local, not root-credit gains. Seeded response recomputed on same boundary.",checker:"runner.js"};cases.push({name,ref,projection,projectCost:p.cost,early,L,stand,standCheck,cnfEarly,cnfStand,cnfCheck,compRup,sr,cl,hybrid,hybridCheck,fb,cert,certHash:sha(enc(cert))})}
return {cases,pins,execution:"serial independent copies; named event counts only; no physical peak or total bit-cost; no full matching or full width-four feedback; local exact response map and controlled-swap rank accounting"};
};
const fs=require('node:fs'); const load=async keys=>Object.fromEntries(keys.map(k=>[k,fs.readFileSync(k+'.txt','utf8')])); (async()=>console.log(JSON.stringify(await run(await load(['compiler','corpus','reg','chart','hash','prior']),pins,()=>load(['joint','random'])),null,2)))().catch(e=>{console.error(e);process.exitCode=1});

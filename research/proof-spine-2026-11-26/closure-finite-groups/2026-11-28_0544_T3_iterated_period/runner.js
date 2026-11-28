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
const run=async function(d,pins,loadPeer){const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,solve,replay}")();
const enc=x=>JSON.stringify(x)+"\n",ck=(v,m)=>{if(!v)throw Error(m)},key=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
const {up,rup,occupancy,affine,conservation,lanes}=new Function("const key="+key.toString()+";"+d.prior.slice(d.prior.indexOf("function up("),d.prior.indexOf("const mono="))+";return {up,rup,occupancy,affine,conservation,lanes}")();
ck(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","hash");
function feedback(F){let V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),out=[];for(let mode of ["baseline","table","residue"]){let visits=0,ties=0,ends=[];function score(A){let bad=0,zero=0;for(let c of F){let k=0,s=0;for(let l of c){visits++;if(A.get(Math.abs(l))===Number(l>0)){k++;s+=l>0?1:-1}}if(!k)bad++;else if(mode==="residue"&&(s%3+3)%3===0)zero++}return [bad,zero]}for(let init of [0,1]){let A=new Map(V.map(v=>[v,init])),cur=score(A);for(let i=0;i<8;i++){let best=[];for(let v of V){A.set(v,A.get(v)^1);let q=score(A);A.set(v,A.get(v)^1);if(q[0]<cur[0]&&(!best.length||q[0]<=best[0][1][0])){if(best.length&&q[0]<best[0][1][0])best=[];best.push([v,q])}}if(!best.length)break;let b=mode==="residue"?best.slice().sort((a,b)=>a[1][1]-b[1][1]||a[0]-b[0])[0]:best[0];ties+=Number(b[0]!==best[0][0]);A.set(b[0],A.get(b[0])^1);cur=b[1]}ends.push(cur[0])}out.push({mode,visits,ties,ends})}return out}

const counts={};let cap=10000000;
const tick=(k,n=1)=>{counts[k]=(counts[k]||0)+n;if(Object.values(counts).reduce((a,b)=>a+b,0)>cap)throw Error("named event cap")};
const high=x=>x.toString(2).length-1;
function basis(rows){let B=new Map();for(let v of rows){let x=v;while(x){tick("rankPivots");let k=high(x);if(!B.has(k)){B.set(k,x);break}x^=B.get(k)}}return B}
function red(v,B){for(let [k,h] of [...B].sort((a,b)=>b[0]-a[0])){tick("reduceTests");if((v>>BigInt(k))&1n)v^=h}return v}
function sp(A){return A.flatMap(S=>S.map(x=>x^S[0]))}
function star(fs){let occ=new Map(),coord=0,cols=fs.map(f=>f.s.map(()=>0n));for(let i=0;i<fs.length;i++)for(let j=0;j<fs[i].s.length;j++){let v=fs[i].s[j];if(!occ.has(v))occ.set(v,[]);occ.get(v).push([i,j])}for(let O of occ.values())for(let k=1;k<O.length;k++){let [i,j]=O[0],[a,b]=O[k],h=1n<<BigInt(coord++);cols[i][j]^=h;cols[a][b]^=h}let dict=fs.map((f,i)=>f.a.map(m=>cols[i].reduce((x,c,j)=>x^((m>>j&1)?c:0n),0n)));return {dict,coord,cols}}
function uniq(S){return [...new Set(S)]}
function period(S,mode){S=uniq(S);let a=S[0],T=S.map(x=>x^a),set=new Set(T),P=[];
 if(mode==="direct"){for(let h of T){let ok=true;for(let x of T){tick("periodQueries");if(!set.has(x^h)){ok=false;break}}if(ok)P.push(h)}}
 else{let B=basis(T),es=[...B].sort((a,b)=>b[0]-a[0]);if(es.length>12)throw Error("local span cap");let encode=x=>{let y=0;for(let i=0;i<es.length;i++){tick("encodeTests");if(x>>BigInt(es[i][0])&1n){x^=es[i][1];y|=1<<i}}ck(!x,"encode");return y};let a=new Int32Array(2**es.length);for(let x of T)a[encode(x)]=1;for(let h=1;h<a.length;h*=2)for(let j=0;j<a.length;j+=2*h)for(let i=j;i<j+h;i++){let x=a[i],y=a[i+h];a[i]=x+y;a[i+h]=x-y;tick("walsh",2)}let freq=a.flatMap?Array.from(a).flatMap((x,i)=>x?[i]:[]):Array.from(a).flatMap((x,i)=>x?[i]:[]);for(let h of T){let q=encode(h),ok=true;for(let u of freq){tick("characters");let z=q&u,p=0;while(z){p^=1;z&=z-1}if(p){ok=false;break}}if(ok)P.push(h)}}
 return P}
function metrics(A){let cuts=[];for(let k of [Math.floor(A.length/4),Math.floor(A.length/2),Math.floor(3*A.length/4)]){let u=sp(A.slice(0,k)),v=sp(A.slice(k)),r=basis([...u,...v]).size;cuts.push({k,rank:r,width:basis(u).size+basis(v).size-r})}return cuts}
function iter(A,mode){let init=metrics(A),rounds=[],H=new Map(),current=A.map(uniq),n=0;while(true){let tags=[];for(let i=0;i<current.length;i++){let P=period(current[i],mode),Q=period(current[i],mode==="direct"?"spectral":"direct");ck(P.length===Q.length&&P.every(h=>Q.includes(h)),"period methods mismatch");for(let h of basis(P).values())tags.push([i,h])}
let B=basis(tags.map(t=>t[1]));if(!B.size)break;
for(let h of B.values())H=basis([...H.values(),h]);let next=current.map(S=>uniq(S.map(x=>red(x,B))));let widths=metrics(next);rounds.push({rank:B.size,rowsBefore:current.reduce((a,s)=>a+s.length,0),rowsAfter:next.reduce((a,s)=>a+s.length,0),widths,tags:tags.map(([i,h])=>[i,h.toString(16)]),basis:[...B.values()].map(h=>h.toString(16))});current=next;if(++n>12)throw Error("round cap")}
return {initial:init,final:metrics(current),rounds,rank:H.size,rows:current.reduce((a,s)=>a+s.length,0),current}}
function merge(fs){let used=new Set(),out=[];for(let i=0;i<fs.length;i++){if(used.has(i))continue;let a=fs[i],best=-1,score=0;for(let j=i+1;j<fs.length;j++){if(used.has(j))continue;let b=fs[j],u=[...new Set([...a.s,...b.s])],ov=a.s.length+b.s.length-u.length;tick("pairProposals");if(u.length<=8&&ov>score){best=j;score=ov}}if(best<0){out.push({...a,owners:[i]});continue}let b=fs[best],s=[...new Set([...a.s,...b.s])].sort((x,y)=>x-y),masks=[];for(let w=0;w<2**s.length;w++){let ok=[a,b].every(q=>{tick("jointChecks");let t=q.s.reduce((z,v,k)=>z|((w>>s.indexOf(v)&1)<<k),0);return q.a.includes(t)});if(ok)masks.push(w)}used.add(best);out.push({s,a:masks,owners:[i,best]})}return out}
function filter(fs,seeds){return fs.map(f=>{let local=seeds.filter(c=>c.every(l=>f.s.includes(Math.abs(l)-1)));return {...f,a:f.a.filter(w=>local.every(c=>c.some(l=>{tick("seedTests");return (w>>f.s.indexOf(Math.abs(l)-1)&1)===Number(l>0)})))}})}
function arm(fs){if(fs.some(f=>!f.a.length))return {status:"local empty response"};let A=star(fs),q=iter(A.dict,"spectral");return {status:"exact quotient only",blocks:fs.length,coords:A.coord,rows:A.dict.reduce((a,s)=>a+s.length,0),initial:q.initial,final:q.final,rank:q.rank,rounds:q.rounds,finalRows:q.rows,ownerGroups:fs.map(f=>f.owners??[f.id])}}
function toy(){let A=[[0n,1n],[0n,2n,3n],[0n,4n,6n]]; // first quotient by bit 0 makes second affine; then third affine
let q=iter(A,"spectral");let sums=S=>S.reduce((R,T)=>uniq(R.flatMap(x=>T.map(y=>x^y))),[0n]);let orig=sums(A),remain=sums(q.current);ck(orig.length===8&&remain.length===1,"toy cascade");return {original:orig.map(String),rounds:q.rounds,final:remain.map(String),rank:q.rank}}
let bases=[],out=[];for(let name of ["JOINT-24","RANDOM-3CNF-40"]){for(let k of Object.keys(counts))delete counts[k];let x=JSON.parse(d.corpus).instances.find(z=>z.id===name),ref=JSON.parse(d.reg).instances.find(z=>z.alias==="EB-"+name),G=compile(x),native=enc(G.network);ck(sha(native)===ref.sha256&&native.length*8===ref.N_bits&&sha(x.dimacs)===ref.source_cnf.sha256&&x.dimacs.length*8===ref.source_cnf.N_bits&&sha(enc(G.source_map))===ref.source_map_sha256,"auth");let p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",ref.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",ref.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
let early={up:up(F),occupancy:occupancy(p.raw,[-(p.anchor+1)]),affine:affine(p.raw,[-(p.anchor+1)]),conservation:conservation(G.network,p,[-(p.anchor+1)])};
let A=arm(p.final),M=merge(p.final),B=arm(M),L=lanes(G.network,p,F),stand=solve(F),standCheck=replay(F,stand.tree),ad=adapter(p,G,x.dimacs,x.nvars),cnf=solve(ad.orig),cnfCheck=replay(ad.orig,cnf.tree);
bases.push({name,ref,p,F,chartHash,mapHash,gid,rid,early,A,M,B,L,projection,stand:{nodes:stand.nodes,work:stand.work,check:standCheck},cnf:{nodes:cnf.nodes,work:cnf.work,check:cnfCheck},counts:{...counts}})}
let peers=await loadPeer();for(let z of bases){for(let k of Object.keys(counts))delete counts[k];let raw=peers[z.name==="JOINT-24"?"joint":"random"],C=JSON.parse(raw);ck(C.instance_id===z.ref.instance_id&&C.internal_guard===z.gid&&C.internal_residual===z.rid&&C.chartHash===z.chartHash&&C.mapHash===z.mapHash,"peer scope");let seeds=[];for(let c of C.proof){if(!c.includes(C.anchor))break;let q=c.filter(l=>l!==C.anchor);if(!q.length)break;seeds.push(q)}let sr=rup(z.F,seeds);ck(sr.ok,"peer replay");let local=seeds.filter(c=>z.M.some(f=>c.every(l=>f.s.includes(Math.abs(l)-1)))).slice(0,5),F=[...z.F,...local],cl=up(F);let seeded=arm(filter(z.M,local)),abl=local.map((c,i)=>({removed:c,arm:arm(filter(z.M,local.filter((_,j)=>i!==j)))}));let fb=cl.conflict?{stage:"unreachable"}:feedback(F);let hy=solve(F),hc=replay(F,hy.tree);
let cert={format:"T3-ITERATED-PERIOD-v1",problem_id:"STRICT-EB4-v1",instance:z.ref.short_id,instance_id:z.ref.instance_id,original_N_bits:z.ref.N_bits,source_pins:pins,guard_id:z.gid,residual_id:z.rid,chartHash:z.chartHash,mapHash:z.mapHash,original_ids:{vertices:[0,z.ref.vertices-1],ports:[0,4*z.ref.vertices-1],edges:[0,z.ref.edges-1]},parent_certificate_ids:["CERT-v1:sha256:"+sha(raw)],source:z.A,pair:z.B,local,seeded,abl};out.push({cert,certificate_id:"CERT-v1:sha256:"+sha(enc(cert)),early:z.early,L:z.L,projection:z.projection,projectCost:z.p.cost,stand:z.stand,cnf:z.cnf,import:sr,hybrid:{nodes:hy.nodes,work:hy.work,check:hc},fb,sourceCounts:z.counts,hybridCounts:{...counts}})}
for(let k of Object.keys(counts))delete counts[k];let control=toy();return {out,control,controlCounts:{...counts},execution:"serial, event proxies only; no global quotient witness replay, full bit clock, full feedback or physical RSS; exact periods checked by two methods"};
};
const fs=require('node:fs');const load=async keys=>Object.fromEntries(keys.map(k=>[k,fs.readFileSync(k+'.txt','utf8')]));(async()=>console.log(JSON.stringify(await run(await load(['compiler','corpus','reg','chart','hash','prior']),pins,()=>load(['joint','random'])),null,2)))().catch(e=>{console.error(e);process.exitCode=1});

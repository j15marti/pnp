// Node 20+. Fetch exact pinned files as KEY.txt, then node runner.js.
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
  ],
  "partner": [
    "research/proof-spine-2026-11-26/finite-group-classification/2026-11-27_2125_T2_guarded_nonlinear/joint.orbit-cert.json",
    "e355d41b30110c6ae19295742542108895c2f397"
  ]
};
const run=async function(d,pins,peerLoader){
const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,adapter,solve,replay}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter,solve,replay}")();
const enc=x=>JSON.stringify(x)+"\n",ck=(x,m)=>{if(!x)throw Error(m)},key=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
const {up,rup,occupancy,affine,conservation,joins,lanes}=new Function("const key="+key.toString()+";"+d.prior.slice(d.prior.indexOf("function up("),d.prior.indexOf("const mono="))+";return {up,rup,occupancy,affine,conservation,joins,lanes}")();
ck(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha");
function close(F,g=[],rev=false){let A=new Map(g.map(l=>[Math.abs(l),Number(l>0)])),work=0,change=true;while(change){change=false;for(let i=0;i<F.length;i++){let c=F[rev?F.length-1-i:i],hit=false,free=[];for(let l of c){work++;if(!A.has(Math.abs(l)))free.push(l);else if(A.get(Math.abs(l))===Number(l>0)){hit=true;break}}if(hit)continue;if(!free.length)return {conflict:true,A,work};if(free.length===1){let l=free[0];A.set(Math.abs(l),Number(l>0));change=true}}}return {conflict:false,A,work}}
function scan(F,cap=2500000){let vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),G=[[]];for(let v of vars)G.push([v],[-v]);for(let i=0;i<vars.length;i++)for(let j=i+1;j<vars.length;j++)for(let a of [-1,1])for(let b of [-1,1])G.push([a*vars[i],b*vars[j]]);let work=0,hit=[],tested=0;for(let g of G){let c=up(F,g);work+=c.work;tested++;if(c.conflict)hit.push(g);if(work>=cap)break}return {vars,hit,work,tested,universe:G.length}}
const parts=s=>s?s.split(",").map(Number):[],mon=a=>[...new Set(a)].sort((a,b)=>a-b).join(",");
const xor=(A,B)=>{let o=new Set(A);for(let x of B)o.has(x)?o.delete(x):o.add(x);return o};
let products=0,xors=0;
function mul(A,B){let o=new Set();for(let x of A)for(let y of B){products++;let z=mon([...parts(x),...parts(y)]);o.has(z)?o.delete(z):o.add(z)}return o}
function deg(P){let z=-1;for(let m of P)z=Math.max(z,parts(m).length);return z}
function poly(G){let P=new Set([""]);for(let l of G){let L=new Set([String(Math.abs(l))]);if(l<0)L.add("");P=mul(P,L)}return P}
function swap(P,a,b){let Q=new Set();for(let m of P){let z=mon(parts(m).map(v=>v===a?b:v===b?a:v));Q.has(z)?Q.delete(z):Q.add(z)}return Q}
function pull(P,a,b,g){return xor(P,mul(new Set([String(g)]),xor(P,swap(P,a,b))))}
function ev(P,A){let b=0;for(let m of P)if(parts(m).every(v=>A.get(v)===1))b^=1;return b}
function add(M,P){let Q=new Set(P);while(Q.size){let k=[...Q].sort().at(-1);if(!M.has(k)){M.set(k,Q);return true}Q=xor(Q,M.get(k));xors++}return false}
function kernel(guards,a,b,g,d=2){let R=new Map(),T=new Map(),H=new Map(),S=new Map(),D=new Map(),basis=[],unsafe=[],checks=0,p0=products,x0=xors,rows=guards.map(poly);
for(let i=0;i<rows.length;i++){let p=rows[i],q=pull(p,a,b,g),h=new Set([...q].filter(m=>parts(m).length>d)),vs=[...new Set([...guards[i].map(Math.abs),a,b,g])];for(let m=0;m<2**vs.length;m++){let A=new Map(vs.map((v,j)=>[v,m>>j&1])),B=new Map(A);if(A.get(g)){B.set(a,A.get(b));B.set(b,A.get(a))}ck(ev(q,A)===ev(p,B),"pullback");checks++}ck(xor(p,pull(q,a,b,g)).size===0,"inverse");add(R,p);add(T,q);if(!h.size)add(D,q);else unsafe.push(i);let combo=new Set([String(i)]),Q=q;while(h.size){let k=[...h].sort().at(-1);if(!H.has(k)){H.set(k,{h,Q,combo});break}let z=H.get(k);h=xor(h,z.h);Q=xor(Q,z.Q);combo=xor(combo,z.combo);xors++}if(!h.size&&add(S,Q)){let P=new Set();for(let j of combo)P=xor(P,rows[Number(j)]);ck(xor(pull(P,a,b,g),Q).size===0&&deg(Q)<=d,"kernel witness");basis.push({parents:[...combo].map(Number),source:[...P].sort(),image:[...Q].sort()})}}
ck(R.size===T.size&&S.size===R.size-H.size,"rank-nullity");return {map:{a,b,g},count:guards.length,sourceRank:R.size,transportRank:T.size,highRank:H.size,safeRank:S.size,directSafeRank:D.size,unsafe,truthChecks:checks,products:products-p0,rowXors:xors-x0,basis}}
function feedback(F,mode,cap=500000){let vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),work=0,arms=[];function score(A){let bad=0,z=0;for(let c of F){let k=0,s=0;for(let l of c){work++;if(A.get(Math.abs(l))===Number(l>0)){k++;s+=l>0?1:-1}}let km=k%3,sm=((s%3)+3)%3;if(!k)bad++;else if(!sm)z++;if(km<0)throw Error("residue")}return [bad,z]}for(let start of [0,1]){let A=new Map(vars.map(v=>[v,start])),cur=score(A),flips=[],ties=0;while(work<cap){let best=[],val=cur[0];for(let v of vars){A.set(v,A.get(v)^1);let s=score(A);A.set(v,A.get(v)^1);if(s[0]<val){val=s[0];best=[]}if(s[0]===val&&val<cur[0])best.push({v,s});if(work>=cap)break}if(!best.length||work>=cap)break;let q=mode==="residue"?best.slice().sort((a,b)=>a.s[1]-b.s[1]||a.v-b.v)[0]:best[0];ties+=Number(q.v!==best[0].v);A.set(q.v,A.get(q.v)^1);cur=q.s;flips.push(q.v)}arms.push({start,bad:cur[0],flips,ties})}return {mode,work,arms}}
let base=[];
for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=JSON.parse(d.corpus).instances.find(x=>x.id===name),ref=JSON.parse(d.reg).instances.find(x=>x.alias==="EB-"+name),G=compile(x),native=enc(G.network);ck(sha(native)===ref.sha256&&native.length*8===ref.N_bits&&sha(x.dimacs)===ref.source_cnf.sha256&&x.dimacs.length*8===ref.source_cnf.N_bits&&sha(enc(G.source_map))===ref.source_map_sha256,"authentication");let p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",ref.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",ref.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));let early={up:up(F),occupancy:occupancy(p.raw,[]),affine:affine(p.raw,[]),conservation:conservation(G.network,p,[])},L=lanes(G.network,p,F),blind=scan(F),stand=solve(F),standCheck=replay(F,stand.tree),ad=adapter(p,G,x.dimacs,x.nvars),cnfEarly=up(ad.orig),cnfBlind=scan(ad.orig),cnfStand=solve(ad.orig),cnfCheck=replay(ad.orig,cnfStand.tree);base.push({name,ref,G,p,F,projection,chartHash,mapHash,gid,rid,early,L,blind,stand,standCheck,ad,cnfEarly,cnfBlind,cnfStand,cnfCheck})}
let peers=await peerLoader(),cases=[];
for(let z of base){let {name,ref,G,p,F,projection,chartHash,mapHash,gid,rid,early,L,blind,stand,standCheck,ad,cnfEarly,cnfBlind,cnfStand,cnfCheck}=z,k=name==="JOINT-24"?"joint":"random",raw=peers[k],C=JSON.parse(raw),parent="CERT-v1:sha256:"+sha(raw);ck(C.instance_id===ref.instance_id&&C.guard_id===gid&&C.residual_id===rid&&C.chartHash===chartHash&&C.mapHash===mapHash,"delta identity "+name);let seeds=rup(F,C.seeds);ck(seeds.ok,"seed replay");let A=[...F,...C.seeds],prework=0,postwork=0;for(let g of C.additional_guards){let before=close(F,g),after=close(A,g,true);prework+=before.work;postwork+=after.work;ck(!before.conflict&&after.conflict,"delta replay")}let ablations=[];for(let i=0;i<C.seeds.length;i++){let S=C.seeds.filter((_,j)=>i!==j),r=rup(F,S),hits=0,work=0;if(r.ok)for(let g of C.additional_guards){let q=close([...F,...S],g);work+=q.work;hits+=Number(q.conflict)}ablations.push({removed:i,admitted:r.ok,seedWork:r.work,hits,work})}
let M=new Map(ad.mapping.map(([i,v,s])=>[v,[i,s]])),mapLit=l=>{let [i,s]=M.get(Math.abs(l));return i*(l>0?1:-1)*(s?-1:1)},compSeeds=C.seeds.map(c=>c.map(mapLit)),compRup=rup(ad.orig,compSeeds);ck(compRup.ok,"companion seed replay");let compWork=0;for(let g of C.additional_guards){let q=close([...ad.orig,...compSeeds],g.map(mapLit),true);ck(q.conflict,"companion replay");compWork+=q.work}
let sym=null,a,b,g;if(k==="joint"){let P=JSON.parse(peers.partner);ck(sha(peers.partner)==="f8ecb05eb0a1c8c1202d7607c6c0de916890db352f12fb7802ab5b1ecaf76383"&&P.instance_id===ref.instance_id,"partner hash");g=p.root[241]+1;a=2;b=34;ck(p.anchor===10&&p.phase[241]===0,"partner guard");let cl=close(F,[g]);ck(!cl.conflict,"partner residual");let R=F.filter(c=>!c.some(l=>cl.A.get(Math.abs(l))===Number(l>0))).map(c=>c.filter(l=>!cl.A.has(Math.abs(l)))),live=[...new Set(R.flat().map(Math.abs))].sort((a,b)=>a-b);ck(live.join()===P.original_ids.live_ports.map(v=>v+1).sort((a,b)=>a-b).join(),"partner live");let set=new Set(R.map(key));ck(set.size===12,"S4");for(let i=0;i<live.length;i++)for(let j=i+1;j<live.length;j++)for(let s of [-1,1])ck(set.has(key([s*live[i],s*live[j]])),"S4 pair");for(let w=0;w<=4;w++){let V=new Map(live.map((v,i)=>[v,Number(i<w)]));ck(R.some(c=>c.every(l=>V.get(Math.abs(l))!==Number(l>0))),"orbit representative")}sym={g,live,pins:cl.A.size,visits:cl.work,representatives:5,parent:"CERT-v1:sha256:"+sha(peers.partner)}}else{[a,b,g]=blind.vars.slice(0,3)}
let map=kernel(C.additional_guards,a,b,g),blindMap=kernel(blind.hit,a,b,g),seededMap=kernel([...blind.hit,...C.additional_guards],a,b,g),B=[...A,...C.additional_guards.map(g=>g.map(l=>-l))],exchange=close(B),feedbackResult=exchange.conflict?{stage:"unreachable after exchange"}:{stage:"reached",table:feedback(B,"table"),residue:feedback(B,"residue"),limitations:"only flip scoring; no new resolution feedback or width4"},hybrid=solve(B),hybridCheck=replay(B,hybrid.tree);
let original_ids={vertices:[0,G.network.types.length-1],ports:[0,p.root.length-1],edges:[0,G.network.edges.length-1]},cert={schema:"T3-GUARD-DELTA-NONLINEAR-KERNEL-v1",problem_id:"STRICT-EB4-v1",instance:ref.short_id,instance_id:ref.instance_id,original_N_bits:ref.N_bits,source_pins:pins,guard_id:gid,residual_id:rid,chartHash,mapHash,original_ids,parents:[parent,...(sym?[sym.parent]:[])],claim:"Independently replayed delta exclusions. Exact degree<=2 image of their span under explicitly invertible controlled swap; no automatic new root rank or unguarded symmetry.",guard_delta:C.additional_guards,seeds:C.seeds,nonlinear_map:map.map,source_rank:map.sourceRank,high_rank:map.highRank,safe_rank:map.safeRank,individual_safe_rank:map.directSafeRank,basis:map.basis,symmetry:sym,checker:"runner.js"};let brief=m=>({...m,basis:undefined,unsafe:m.unsafe.length});cases.push({name,ref,original_ids,gid,rid,chartHash,mapHash,carriers:p.carriers,projectCost:p.cost,projection,early,L,blind:{...blind,hit:blind.hit.length},cnfEarly,cnfBlind:{...cnfBlind,hit:cnfBlind.hit.length},stand,standCheck,cnfStand,cnfCheck,parent,seeds,prework,postwork,ablations,compWork,compRup,sym,map:brief(map),blindMap:brief(blindMap),seededMap:brief(seededMap),exchange:{conflict:exchange.conflict,work:exchange.work,pins:exchange.A.size},feedbackResult,hybrid,hybridCheck,cert,certHash:sha(enc(cert))})}
return {cases,pins,execution:"serial; heterogeneous operation counts, no physical RSS or full bit-time; one aborted initial implementation; no full flow, companion five lanes or complete feedback control"};
};
const fs=require('node:fs');const load=async keys=>Object.fromEntries(keys.map(k=>[k,fs.readFileSync(k+'.txt','utf8')]));(async()=>{console.log(JSON.stringify(await run(await load(['compiler','corpus','reg','chart','hash','prior']),pins,()=>load(['joint','random','partner'])),null,2))})().catch(e=>{console.error(e);process.exit(1)});

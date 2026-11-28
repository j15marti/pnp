const pins={
  "compiler": [
    "research/coordination/shared-eb-2026-11-27/compile.js",
    "21b9d53fb8166c819b24e708656c742cd3c24f10"
  ],
  "corpus": [
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json",
    "e315349cd6c1fe3fa696504859f28312f6aab69a"
  ],
  "registry": [
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json",
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c"
  ],
  "chart": [
    "research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js",
    "52cae4a54513a67dd9468c7e3ee597cf317d67a3"
  ],
  "helper": [
    "research/hcl201/guarded-dag/2026-11-27_T4_branch_credit/independent_checker.js",
    "5214a4fa84961675b8f44d68b106603a938a4b57"
  ],
  "prior": [
    "research/hcl201/synthesis/2026-11-27_T4_UCAC_refinement/refine.js",
    "aeece9c387a75111a94c43d7d8f3961a8d9b3917"
  ],
  "lanes": [
    "research/hcl201/synthesis/2026-11-27_T4_disjoint_guard_remainder/lanes.js",
    "c95e4591de9bdd6c199483b5714afc2dbe0fcc35"
  ],
  "joint": [
    "research/coordination/2026-11-27_2100_UCAC_review/JOINT-24.cone.cert.json",
    "68026e81a25e6498d6ef6965c77ce9769f3292e6"
  ],
  "random": [
    "research/coordination/2026-11-27_2100_UCAC_review/RANDOM-3CNF-40.cone.cert.json",
    "a65c591d674b2f25d11fe937056172d6b3a9de01"
  ]
};
function runScheduler(F,mode,cap=3000000,seeds=[]){
 const C=F.map(c=>[...c]), V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b), lit=V.flatMap(v=>[-v,v]),I=new Map(lit.map((l,i)=>[l,i])),key=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(","),seen=new Set(C.map(key)),P=[],cache=new Map(),sc=new Map(),oc=new Map(),M={visits:0,cacheTests:0,cacheHits:0,cacheCopies:0,probes:0,scc:0,ranking:0,checks:0,passes:0,peakCachedBits:0,peakRows:C.length,seedChecks:0},start=Date.now();
 let guards=lit.map(l=>[l]);for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)for(let a of [-1,1])for(let b of [-1,1])guards.push([a*V[i],b*V[j]]);
 for(let c of F){for(let l of c){oc.set(Math.abs(l),(oc.get(Math.abs(l))||0)+1);for(let q of c)if(Math.abs(l)<Math.abs(q)){let k=Math.abs(l)+","+Math.abs(q);sc.set(k,(sc.get(k)||0)+1);M.ranking++}}}
 const score=g=>g.length===1?oc.get(Math.abs(g[0]))||0:(sc.get(Math.abs(g[0])+","+Math.abs(g[1]))||0)*100000+(oc.get(Math.abs(g[0]))||0)+(oc.get(Math.abs(g[1]))||0);
 if(mode.includes("rank"))guards.sort((a,b)=>{M.ranking++;return a.length-b.length||score(b)-score(a)||key(a).localeCompare(key(b))});
 const cost=()=>M.visits+M.cacheTests+M.cacheCopies+M.probes+M.scc+M.ranking+M.checks+M.seedChecks;
 function tick(){if(cost()>cap)throw Error("CAP")}
 function probe(g,k=null,check=false){M.probes++;let old=k!==null&&mode.includes("persist")?cache.get(k):null,a=old?new Set(old.a):new Set(g);if(old)M.cacheCopies+=old.a.length;
 let changed=!old,bad=false;
 function scan(c,partial){let u=0,n=0;for(let l of c){if(check)M.checks++;else if(partial)M.cacheTests++;else M.visits++;if(a.has(l))return;if(!a.has(-l)){u=l;n++}}if(!n){bad=true;return}if(n===1){a.add(u);changed=true}}
 if(old){for(let j=old.at;j<C.length&&!bad;j++)scan(C[j],true);if(!changed&&!bad)M.cacheHits++}
 while(changed&&!bad){changed=false;for(let c of C){scan(c,false);if(bad)break}tick()}
 if(k!==null&&mode.includes("persist")&&!bad){cache.set(k,{a:[...a],at:C.length});M.peakCachedBits=Math.max(M.peakCachedBits,cache.size*2*V.length)}
 tick();return bad}
 function add(c){if(seen.has(key(c)))return; if(!probe(c.map(l=>-l),null,true))throw Error("admission");C.push(c);P.push(c);seen.add(key(c));M.peakRows=Math.max(M.peakRows,C.length)}
 function scc(){let A=lit.map(()=>[]),B=lit.map(()=>[]);for(let c of C){M.scc++;if(c.length===1){let u=I.get(-c[0]),v=I.get(c[0]);A[u].push(v);B[v].push(u)}else if(c.length===2){for(let [p,q] of [[-c[0],c[1]],[-c[1],c[0]]]){let u=I.get(p),v=I.get(q);A[u].push(v);B[v].push(u)}}}let seen=new Set(),order=[];function dfs(v){seen.add(v);M.scc++;for(let u of A[v]){M.scc++;if(!seen.has(u))dfs(u)}order.push(v)}for(let i=0;i<lit.length;i++)if(!seen.has(i))dfs(i);let z=Array(lit.length).fill(-1),id=0;function rev(v){z[v]=id;M.scc++;for(let u of B[v]){M.scc++;if(z[u]<0)rev(u)}}for(let v of order.reverse())if(z[v]<0){rev(v);id++}tick();for(let v of V)if(z[I.get(v)]===z[I.get(-v)])return v;return null}
 function terminal(){if(probe([])){add([]);return true}if(mode.includes("scc")){let v=scc();if(v!==null){add([v]);add([]);return true}}return false}
 let status="UNKNOWN_FIXED";try{for(let c of seeds){let prev=M.checks;add(c);M.seedChecks+=M.checks-prev;M.checks=prev}if(terminal())status="UNSAT";else outer:for(;;){M.passes++;let p=P.length;for(let i=0;i<guards.length;i++){let g=guards[i],c=g.map(l=>-l);if(seen.has(key(c)))continue;if(probe(g,i)){add(c);if(terminal()){status="UNSAT";break outer}}}if(p===P.length)break;tick()}}catch(e){if(String(e).includes("CAP"))status="UNKNOWN_CAP";else throw e}
 return {status,proof:P,M:{...M,total:cost(),ms:Date.now()-start,cacheSize:cache.size,guards:guards.length}};
}
function experiment(S){
 const H=Function(S.helper.slice(0,S.helper.indexOf('const fs=require("node:fs"),[compiler'))+";return {sha,independentNormalize}")(),sha=H.sha,compile=Function(S.compiler.slice(S.compiler.indexOf("function compile"),S.compiler.indexOf("function auditLocal"))+";return compile")(),P=Function(S.chart.slice(S.chart.indexOf("const key="),S.chart.indexOf("function up("))+";return {project,verifyProjection}")(), L=Function(S.lanes.slice(0,S.lanes.indexOf("module.exports="))+";return {solveLane,chooseGuards,countCover}")(),Q=Function(S.prior.slice(0,S.prior.indexOf("function run(S"))+";return {scalar,verify,refine,cross,feedback,dpll,treecheck,laneRun}")(),B=JSON.parse(S.corpus),R=JSON.parse(S.registry),enc=x=>JSON.stringify(x)+"\n",res=[];
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash");
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){
 let t=Date.now(),x=B.instances.find(x=>x.id===id),e=R.instances.find(x=>x.alias==="EB-"+id),G=compile(x),b=enc(G.network);if(sha(b)!==e.sha256||b.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||sha(enc(G.source_map))!==e.source_map_sha256)throw Error("auth");let authMs=Date.now()-t,p=P.project(G.network),pv=P.verifyProjection(G.network,p),F=p.clauses,gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",e.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",e.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));let early=Q.scalar(F),crossSame=Q.cross(F,true),crossDiff=Q.cross(F,false);
 let modes={};for(let mode of ["fresh","persist","rank-scc","rank-persist-scc"]){let a=runScheduler(F,mode);a.replay=Q.verify(F,a.proof,a.status==="UNSAT");modes[mode]=a}
 let cf=JSON.parse(S[id==="JOINT-24"?"joint":"random"]);if(cf.instance_id!==e.instance_id||cf.guard_id!==gid||cf.residual_id!==rid)throw Error("peer identity");let peer=cf.proof||cf.trimmedProof; if(!peer)throw Error("peer proof fields "+Object.keys(cf));let peerReplay=Q.verify(F,peer,true),seeds=peer.slice(0,3),seeded=runScheduler(F,"rank-persist-scc",3000000,seeds);seeded.replay=Q.verify(F,seeded.proof,seeded.status==="UNSAT");let ablations=[];for(let i=0;i<seeds.length;i++){let sub=seeds.filter((_,j)=>j!==i);try{let a=runScheduler(F,"rank-persist-scc",3000000,sub);a.replay=Q.verify(F,a.proof,a.status==="UNSAT");ablations.push({removed:i,status:a.status,total:a.M.total,proof:a.proof})}catch(e){ablations.push({removed:i,error:String(e)})}}
 let cnf=x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1)),reps=G.source_map.representative_ports,fp=reps.f,f=p.phase[fp[0]]^fp[1],mapping=[];for(let i=1;i<=x.nvars;i++){let [q,s]=reps["x"+i];mapping.push([i,p.root[q]+1,p.phase[q]^s^f])}let mp=new Map(mapping.map(([i,v,s])=>[v,[i,s]])),convert=c=>c.map(l=>{let q=mp.get(Math.abs(l));if(!q)throw Error("map");return Math.sign(l)*(q[1]?-1:1)*q[0]}),key=c=>[...c].sort((a,b)=>a-b).join(","),A=new Set(cnf.map(key)),D=new Set(F.map(c=>key(convert(c))));if(A.size!==D.size||![...A].every(k=>D.has(k)))throw Error("adapter");
 let companion=runScheduler(cnf,"rank-persist-scc");companion.replay=Q.verify(cnf,companion.proof,companion.status==="UNSAT");let feedback=[];for(let mode of ["baseline","table","residue"]){let a=Q.feedback(F,mode,4,91357),z=Q.dpll(a.C,500000),check=Q.verify(F,a.proof,false),tree=z.status==="UNSAT"?Q.treecheck(a.C,z.tree):null;feedback.push({mode,M:a.M,status:z.status,treeNodes:z.M.nodes,treeWork:z.M.work,check:check.work,treeCheck:tree,proof:a.proof})}
 let lanes=Q.laneRun(p,L);res.push({id,e,authMs,pv,chartHash,mapHash,gid,rid,anchor:p.anchor,early:{work:early.work,forced:[...early.a],conflict:early.bad},crossSame,crossDiff,modes,peerHash:sha(enc(peer)),peerReplay:peerReplay.work,seeds,seeded,ablations,mapping,companion,feedback,lanes});
 }return res;
}
if(typeof module!=='undefined')module.exports={pins,runScheduler,experiment};

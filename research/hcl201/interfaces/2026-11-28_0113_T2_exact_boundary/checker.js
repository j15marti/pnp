const fs=require('node:fs');
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
    "research/coordination/2026-11-27_2300_UCAC_review/gauge-lift.js",
    "4a42c99a37a2a22c1ac36ed204eadce7dfa77908"
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
function experiment(d,pins){
const sha=new Function(d.hash.slice(d.hash.indexOf("function sha(s)"),d.hash.indexOf("if(require.main"))+";return sha")();
if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash");
const enc=x=>JSON.stringify(x)+"\n";
const compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")();
const {project,verifyProjection,adapter}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter}")();
function up(F,g,c){const A=new Set(g);if(g.some(l=>A.has(-l)))return {conflict:true,A};let ch=true;while(ch){ch=false;for(const row of F){let n=0,last=0,hit=false;for(const l of row){if(++c.visits>20000000)throw Error("work cap");if(A.has(l)){hit=true;break}if(!A.has(-l)){n++;last=l}}if(hit)continue;if(!n)return {conflict:true,A};if(n===1&&!A.has(last)){A.add(last);ch=true}}}return {conflict:false,A}}
function replay(F,P){let c={visits:0},R=F.slice();for(let i=0;i<P.length;i++){if(!up(R,P[i].map(l=>-l),c).conflict)return {valid:false,failed:i,...c};R.push(P[i])}return {valid:true,...c}}
function canonical(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function compact(rows,v){let pos=rows.filter(c=>c.includes(v)),neg=rows.filter(c=>c.includes(-v)),rest=rows.filter(c=>!c.includes(v)&&!c.includes(-v)),M=new Map(),pairs=0,taut=0,subs=0,subsetTests=0;for(let a of pos)for(let b of neg){pairs++;let c=canonical([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)]);if(c.some(l=>c.includes(-l))){taut++;continue}M.set(c.join(","),c)}for(let c of rest){let q=canonical(c);M.set(q.join(","),q)}let L=[...M.values()].sort((a,b)=>a.length-b.length||a.join(",").localeCompare(b.join(","))),out=[];for(let c of L){let s=false;for(let x of out){subsetTests++;if(x.every(l=>c.includes(l))){s=true;break}}if(s)subs++;else out.push(c)}return {out,pairs,taut,subs,subsetTests}}
function rank(a){let B=new Map();for(let x of a){while(x){let i=31-Math.clz32(x);if(B.has(i))x^=B.get(i);else{B.set(i,x);break}}}return B.size}
function support(rows,v,boundary,compactRows){const idx=new Map(boundary.map((x,i)=>[x,i])),support=[],wit=[],c={sourceLiteral:0,compactLiteral:0};function ok(R,m,b,type){return R.every(row=>row.some(l=>{c[type]++;let q=Math.abs(l)===v?b:(m>>idx.get(Math.abs(l)))&1;return q===Number(l>0)}))}for(let m=0;m<2**boundary.length;m++){let a=ok(rows,m,0,"sourceLiteral"),b=ok(rows,m,1,"sourceLiteral"),q=ok(compactRows,m,0,"compactLiteral");if(q!==(a||b))throw Error("boundary mismatch");if(q){support.push(m);wit.push((a?1:0)+(b?2:0))}}return {support,wit,...c}}
function solve(F){let c={visits:0},nodes=0;function rec(g){nodes++;let q=up(F,g,c);if(q.conflict)return ["L"];let freq=new Map();for(let row of F)if(!row.some(l=>q.A.has(l)))for(let l of row)if(!q.A.has(-l))freq.set(Math.abs(l),(freq.get(Math.abs(l))||0)+1);if(!freq.size)throw Error("unexpected SAT");let v=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];return [v,rec([...q.A,-v]),rec([...q.A,v])]}let tree=rec([]),verify={visits:0},vn=0;function check(t,g){vn++;let q=up(F,g,verify);if(t[0]==="L"){if(!q.conflict)throw Error("leaf");return}let v=t[0];if(q.conflict||q.A.has(v)||q.A.has(-v))throw Error("branch");check(t[1],[...q.A,-v]);check(t[2],[...q.A,v])}check(tree,[]);return {nodes,discovery:c.visits,verification:verify.visits,tree}}
function feedback(F,mode){let V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),A=new Set(),visits=0,moves=[],changed=0;function score(flip){let bad=0,zero=0;for(let c of F){let k=0,s=0;for(let l of c){visits++;let b=A.has(Math.abs(l))^(Math.abs(l)===flip);if(b===Number(l>0)){k++;s+=l>0?1:-1}}if(!k)bad++;else if(((s%3)+3)%3===0)zero++}return [bad,zero]}let cur=score(0);if(mode!=="baseline")while(cur[0]){let candidates=V.map(v=>[v,...score(v)]).filter(x=>x[1]<cur[0]).sort((a,b)=>a[1]-b[1]||a[0]-b[0]);if(!candidates.length)break;let t=candidates[0],q=mode==="residue"?candidates.slice().sort((a,b)=>a[1]-b[1]||a[2]-b[2]||a[0]-b[0])[0]:t;if(q[0]!==t[0])changed++;if(A.has(q[0]))A.delete(q[0]);else A.add(q[0]);moves.push(q[0]);cur=q.slice(1)}return {visits,moves,changed,bad:cur[0]}}
let out=[];for(const [name,v] of [["joint",42],["random",209]]){
const x=JSON.parse(d.corpus).instances.find(z=>z.id===(name==="joint"?"JOINT-24":"RANDOM-3CNF-40")),r=JSON.parse(d.reg).instances.find(z=>z.alias==="EB-"+x.id),G=compile(x),src=enc(G.network);if(sha(src)!==r.sha256||src.length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("auth "+name);
let p=project(G.network),projection=verifyProjection(G.network,p),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));let F=p.clauses,early={visits:0},U=up(F,[],early),ad=adapter(p,G,x.dimacs,x.nvars),cnfEarly={visits:0},CU=up(ad.orig,[],cnfEarly);
let incident=F.map((c,i)=>({c,i:i+1})).filter(z=>z.c.some(l=>Math.abs(l)===v)),B=[...new Set(incident.flatMap(z=>z.c.map(Math.abs)))].filter(x=>x!==v).sort((a,b)=>a-b),S=new Set([v,...B]),local=F.map((c,i)=>({c,i:i+1})).filter(z=>z.c.every(l=>S.has(Math.abs(l)))),outside=F.filter(c=>!c.every(l=>S.has(Math.abs(l))));if(outside.some(c=>c.some(l=>Math.abs(l)===v)))throw Error("missed incident");
let ownerMap=new Map(p.raw.map(f=>[f.id,f.B]));for(let q of p.cond)ownerMap.set(q.out.id,ownerMap.get(q.input));for(let q of p.steps)ownerMap.set(q.out.id,[...new Set(q.inputs.flatMap(id=>ownerMap.get(id)))]);let owners=[...new Set(p.final.filter(f=>f.s.every(x=>S.has(x+1))).flatMap(f=>ownerMap.get(f.id)))].sort((a,b)=>a-b);
let c=JSON.parse(d[name]),a=p.anchor+1;if(c.internal_guard!==gid||c.internal_residual!==rid||c.chartHash!==chartHash||c.mapHash!==mapHash)throw Error("peer binding");
const symmetric=[...F.map(c=>[a,...c]),...F.map(c=>[-a,...c.map(l=>-l)])];if(sha(enc(symmetric))!==c.symmetricChartHash)throw Error("symmetric hash");
let rootReplay=replay(symmetric,c.proof);if(!rootReplay.valid||c.proof.at(-1).length)throw Error("peer root proof");let P=c.proof.filter(c=>c.includes(a)&&!c.includes(-a)).map(c=>c.filter(l=>l!==a)),pr=replay(F,P);if(!pr.valid)throw Error("guard proof");
let M=new Map(ad.mapping.map(([i,v,s])=>[v,[i,s]])),Q=P.map(c=>c.map(l=>{let [i,s]=M.get(Math.abs(l));return i*(l>0?1:-1)*(s?-1:1)})),cr=replay(ad.orig,Q);if(!cr.valid)throw Error("companion proof");
let seeds=P.filter(c=>c.length>0&&c.every(l=>S.has(Math.abs(l))));let seedValid=replay(F,seeds); // may depend on outside parents; full replay above remains authority
let variants=[];for(let [label,ss] of [["source",[]],["seeded",seeds],["remove-first-local",seeds.slice(1)]]){let R=[...local.map(z=>z.c),...ss],co=compact(R,v),sp=support(R,v,B,co.out),rnk=rank(sp.support.map(m=>m^sp.support[0])),equivs=[];for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){let par=new Set(sp.support.map(m=>((m>>i)^(m>>j))&1));if(par.size===1)equivs.push([B[i],B[j],[...par][0]])}let dense=[];let live=new Set(sp.support);for(let m=0;m<2**B.length;m++)if(!live.has(m))dense.push(B.map((x,i)=>m&(1<<i)?-x:x));let cmp=solve([...outside,...co.out]),dn=solve([...outside,...dense]);variants.push({label,seedCount:ss.length,localClauses:R,compact:co,boundarySupport:sp,affineRank:rnk,affineHullSize:2**rnk,coordinateRelations:equivs,denseCount:dense.length,compactSolve:cmp,denseSolve:dn})}
let feedbackRuns={};for(let [k,f] of [["native",F],["companion",ad.orig]]){let base=solve(f);feedbackRuns[k]={proof:base,arms:["baseline","table","residue"].map(mode=>({mode,...feedback(f,mode),note:"phase heuristic only; full fixed tree invariant on UNSAT; not a second solver execution"}))}}
let cert={format:"T2-EXACT-BUCKET-RESPONSE-v1",problem_id:r.instance_id.split(":")[0],instance:r.short_id,instance_id:r.instance_id,original_N_bits:r.N_bits,source_pins:pins,guard_id:gid,residual_id:rid,chartHash,mapHash,original_ids:{B_vertices:owners,carrier_ports:[v-1,...B.map(x=>x-1)],chart_rows:local.map(z=>z.i)},parent:"CERT-v1:sha256:"+sha(d[name]),pivot:v,boundary:B,incidentRows:incident.map(z=>z.i),localRows:local.map(z=>z.i),seeds,variants};
out.push({instance:r.short_id,cnf:r.source_cnf,authenticated:true,projection,projectionDiscovery:p.cost,early:{...early,pins:U.A.size,cnfVisits:cnfEarly.visits,cnfPins:CU.A.size},rootReplay,guardReplay:pr,companionReplay:cr,seedStandaloneReplay:seedValid,feedbackRuns,certificate:cert,certificate_id:"CERT-v1:sha256:"+sha(enc(cert))})
}return out
}
const d=Object.fromEntries(Object.keys(pins).map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')])); console.log(JSON.stringify(experiment(d,pins),null,2));

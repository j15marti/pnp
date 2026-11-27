const fs=require('node:fs');
const specs=[
  [
    "21b9d53fb8166c819b24e708656c742cd3c24f10",
    "research/coordination/shared-eb-2026-11-27/compile.js"
  ],
  [
    "e315349cd6c1fe3fa696504859f28312f6aab69a",
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json"
  ],
  [
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c",
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json"
  ],
  [
    "a830475f2d7b927fe3897079af04ebb99c82106b",
    "research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/experiment.js"
  ],
  [
    "d7cb4c38ee4dc1df3378177b716cd0d238d0e4db",
    "research/hcl201/interfaces/2026-11-27_T2_quadratic_response/experiment.js"
  ],
  [
    "18cef3300d462b73dd537b399929bae5bce8c261",
    "research/hcl201/matching/2026-11-27_T1_five_guard_cover_rank/EB-JOINT-24-certificate.json"
  ],
  [
    "a1915fee03fc538094509ceb07d49246fe32be52",
    "research/hcl201/matching/2026-11-27_T1_five_guard_cover_rank/EB-RANDOM-3CNF-40-certificate.json"
  ],
  [
    "e7dfc774c5015195d032befff80a0de089d36f3c",
    "research/hcl201/multisign/2026-11-27_T2_five_guard_response/experiment.js"
  ],
  [
    "4e963c692326d1613afb54c7b9faea0f882e1f6e",
    "research/hcl201/multisign/2026-11-27_T2_five_guard_response/results.json"
  ]
];
function audit(inputs){
 const [co,corpus,reg,base,qc,p0,p1,ex,raw]=inputs,A=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),bytes=x=>JSON.stringify(x)+"\n";
 const compile=Function(co.slice(co.indexOf("function compile("),co.indexOf("function auditLocal"))+";return compile")(),{sha,independentNormalize,verifyTrace}=Function(base.slice(0,base.indexOf("function runCase"))+";return {sha,independentNormalize,verifyTrace}")(),quad=Function(qc.slice(qc.indexOf(" function lane("),qc.indexOf(" let shared=[]"))+";return lane")();
 const response=Function("const bit=i=>1n<<BigInt(i),hi=x=>x.toString(2).length-1;"+ex.slice(ex.indexOf(" function basis()"),ex.indexOf(" function restrict("))+ex.slice(ex.indexOf(" function response("),ex.indexOf(" function policy("))+";return response")();
 const R=JSON.parse(raw),data=JSON.parse(corpus),registry=JSON.parse(reg);
 function restrict(F,g){let p=new Map(g.map(l=>[Math.abs(l),+(l>0)]));return F.map(f=>{let vs=f.vs.filter(v=>!p.has(v));return {...f,vs,ok:[...new Set(f.ok.filter(w=>f.vs.every((v,i)=>!p.has(v)||p.get(v)===(w>>i&1))).map(w=>vs.reduce((z,v,i)=>z|((w>>f.vs.indexOf(v)&1)<<i),0)))].sort((a,b)=>a-b)}})}
 function cnf(F){let C=[];for(let f of F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))C.push(f.vs.map((v,i)=>(w>>i&1)?-v:v));return C}
 function up(C,guard,s){let a=new Map(guard.map(l=>[Math.abs(l),+(l>0)]));while(true){let force=0;for(let c of C){s.reads++;if(c.some(l=>a.get(Math.abs(l))===+(l>0)))continue;let u=c.filter(l=>!a.has(Math.abs(l)));if(!u.length)return null;if(u.length===1){force=u[0];break}}if(!force)return a;a.set(Math.abs(force),+(force>0))}}
 function treeCheck(C,t,g,s){let a=up(C,g,s);if(!a)return true;if(!Array.isArray(t)||t.length!==3)return false;let v=t[0];if(a.has(v))return treeCheck(C,t[a.get(v)+1],g,s);return treeCheck(C,t[1],[...g,-v],s)&&treeCheck(C,t[2],[...g,v],s)}
 function rup(C,proof,guard){let Q=C.slice(),s={reads:0,steps:0};for(let c of proof){if(up(Q,c.map(l=>-l),s)!==null)return {valid:false,...s};Q.push(c);s.steps++}return {valid:up(Q,guard,s)===null,...s}}
 function nogood(g,support=[]){let vs=g.map(Math.abs),w=g.reduce((z,l,i)=>z|((+(l>0))<<i),0);return {id:-1,vs,ok:Array.from({length:2**vs.length},(_,i)=>i).filter(i=>i!==w),support}}
 let out=[];for(let k=0;k<2;k++){
 let q=R.shared[k],e=registry.instances.find(x=>x.instance_id===q.entry.instance_id),x=data.instances.find(x=>x.id===e.source_cnf.alias),G=compile(x),n=bytes(G.network),map=bytes(G.source_map);A(sha(n)===e.sha256&&n.length*8===e.N_bits&&sha(map)===e.source_map_sha256&&sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits,"auth");
 let I=independentNormalize(G.network),a=q.root.gauge;A(I.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))),"symmetry");let Z=verifyTrace(restrict(I.fs,[-a]),q.root.mapArtifact.trace);let M=new Map(I.fs.map(f=>[f.id,f.ids]));for(let t of q.root.mapArtifact.trace)M.set(t.out,[...new Set(t.in.flatMap(i=>M.get(i)||[]))]);let F=Z.fs.map(f=>({...f,support:M.get(f.id)}));A(sha(bytes(F))===q.root.rh&&sha(bytes(q.root.mapArtifact))===q.root.mh,"residual hashes");let C=cnf(F),rootStats={reads:0},root=up(C,[],rootStats);
 let replays=[];for(let i=0;i<q.results.length;i++){let l=q.results[i],S=new Set(l.dag.support),subset=F.filter(f=>f.support.every(v=>S.has(v))),s={reads:0};A(treeCheck(cnf(restrict(subset,l.guard)),l.dag.tree,[],s),"core replay");let art=q.root.guardArtifacts[i];A(sha(bytes(art.art))===art.sha&&sha(bytes(["PNP-GUARD-v1",e.instance_id,art.art.schema,art.sha]))===art.guard_id.split(":").at(-1),"guard ID");let rh=sha(bytes(restrict(F,l.guard)));A(sha(bytes(["PNP-RESIDUAL-v1",e.instance_id,art.guard_id,"RELATIVE-MINPORT-TABLES-v1",rh,q.root.mh]))===art.residual_id.split(":").at(-1),"child residual");replays.push({guard:l.guard,guard_id:art.guard_id,residual_id:art.residual_id,coreSize:S.size,factors:subset.length,reads:s.reads})}
 let V=q.root.V,coverage=response(V,q.results.map(l=>l.guard));A(coverage.covered===coverage.total,"cover");
 let p=JSON.parse(k?p1:p0),pr=rup(C,p.own[0].proof,p.own[0].guard);A(pr.valid,"actual peer RUP replay");
 let partial=[q.results[0].guard,q.results[4].guard],basis=response(V,partial),hybrid=quad([...F,...partial.map(g=>nogood(g))],true,16,true);
 let hybrid2=quad([...F,...q.results.slice(0,2).map(z=>nogood(z.guard))],true,16,true);
 // Repeat random finite candidate discovery even though five-guard DAG closes root; test GAC only under four seeded pins to seek cheaper first epoch.
 let seed=20261127+k,random=[];for(let j=0;j<4;j++){let g=[];while(g.length<2){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let v=V[seed%V.length];if(!g.some(l=>Math.abs(l)===v))g.push(seed&256?v:-v)}let s={reads:0},ans=up(C,g,s);random.push({guard:g,refuted:ans===null,...s})}
 // Direct replay must fail for deliberately corrupted root leaf on surviving guarded case (first guard non-unit).
 let tamper={reads:0};A(!treeCheck(cnf(restrict(F,q.results[0].guard)),null,[],tamper),"tamper accepted");
 out.push({entry:e,rootUP:{conflict:root===null,pins:root?.size,reads:rootStats.reads},replays,coverage,peerRUP:pr,partial,basis,hybrid:{status:hybrid.status,stats:hybrid.stats,ded:hybrid.ded,rootPins:hybrid.rootPins},hybrid2:{status:hybrid2.status,stats:hybrid2.stats,ded:hybrid2.ded,rootPins:hybrid2.rootPins},random,tamper})
 }return out
}
console.log(JSON.stringify(audit(process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'))),null,2));

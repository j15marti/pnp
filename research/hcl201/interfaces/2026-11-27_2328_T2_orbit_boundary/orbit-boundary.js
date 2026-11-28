function setup(d){
 const enc=x=>JSON.stringify(x)+"\n";
 const sha=new Function(d.gauge.slice(d.gauge.indexOf("function sha"),d.gauge.indexOf("if(require.main"))+";return sha")();
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("SHA");
 const compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")();
 const {project,verifyProjection,adapter}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,adapter}")();
 const corpus=JSON.parse(d.corpus),registry=JSON.parse(d.registry);
 function up(F,g,c){const A=new Set(g);for(const l of g)if(A.has(-l))return {bad:true,A};let changed=true;while(changed){changed=false;for(const row of F){let hit=false,u=0,last=0;for(const l of row){c.visits++;if(c.visits>10000000)throw Error("CAP");if(A.has(l)){hit=true;break}if(!A.has(-l)){u++;last=l}}if(hit)continue;if(!u)return {bad:true,A};if(u===1){A.add(last);c.assignments++;changed=true}}}return {bad:false,A}}
 const counter=()=>({visits:0,assignments:0});
 function replay(F,P,c){let T=F.slice();for(let j=0;j<P.length;j++){if(!up(T,P[j].map(l=>-l),c).bad)return {valid:false,failed:j};T.push(P[j])}return {valid:true,terminal:P.length>0&&P[P.length-1].length===0}}
 const mirror=g=>g.map(l=>-l);
 const rowKey=g=>g.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
 function rank(F){let B=new Map(),ops=0;for(const c of F){let m=new Set([""]);for(const l of c){let n=new Set();const add=k=>{ops++;if(n.has(k))n.delete(k);else n.add(k)};for(const k of m){if(l>0)add(k);let v=[...new Set([...k.split(",").filter(Boolean).map(Number),Math.abs(l)])].sort((a,b)=>a-b).join(",");add(v)}m=n}while(m.size){let k=[...m].sort().at(-1);if(!B.has(k)){B.set(k,m);break}for(const t of B.get(k)){ops++;if(m.has(t))m.delete(t);else m.add(t)}}}return {rank:B.size,ops}}
 function make(name){
  const x=corpus.instances.find(z=>z.id===name),r=registry.instances.find(z=>z.alias==="EB-"+name),G=compile(x),bytes=enc(G.network),mp=enc(G.source_map),auth={native:sha(bytes),N:bytes.length*8,cnf:sha(x.dimacs),cnfN:x.dimacs.length*8,map:sha(mp)};
  if(auth.native!==r.sha256||auth.N!==r.N_bits||auth.cnf!==r.source_cnf.sha256||auth.cnfN!==r.source_cnf.N_bits||auth.map!==r.source_map_sha256)throw Error("authentication");
  const p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,a=p.anchor+1,S=[...F.map(c=>[a,...c]),...F.map(c=>[-a,...mirror(c)])];
  const chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
  const source=x.dimacs.trimEnd().split("\n").slice(1).map(s=>s.trim().split(/\s+/).map(Number).slice(0,-1));
  const earlyC=counter(),earlyF=counter(),earlyS=counter();let eC=up(source,[],earlyC),eF=up(F,[],earlyF),eS=up(S,[],earlyS);
  const orbits=new Map();for(const t of p.final)for(const m of t.a){let g=t.s.map((v,i)=>(v+1)*((m>>i)&1?1:-1)),k=rowKey(g),mk=rowKey(mirror(g)),id=k<mk?k:mk;if(!orbits.has(id))orbits.set(id,{g:id.split(",").filter(Boolean).map(Number),occ:[]});orbits.get(id).occ.push({factor:t.id,word:m,orientation:k===id?0:1})}
  const all=[...orbits.entries()].sort((a,b)=>a[0].localeCompare(b[0],"en")).map(z=>z[1]),q=Math.min(64,all.length),sample=Array.from({length:q},(_,i)=>all[Math.floor(i*all.length/q)]);
  const baseRank=rank(F);
  function arm(P,mask){
   const C=counter(),T=counter(),V=counter(),L=counter();const sub=P.filter((_,i)=>mask&(1<<i));let valid=replay(F,sub,V);
   if(!valid.valid)return {mask,valid,verification:V};
   const lifted=[...sub.map(c=>[a,...c]),...sub.map(c=>[-a,...mirror(c)])];if(!replay(S,lifted,L).valid)throw Error("lift subset");
   const F1=[...F,...sub],S1=[...S,...lifted];let stats={both:0,one:0,neither:0,direct:0,directOrientations:0,guardedOrientationConflicts:0,anchoredMismatch:0},rows=[];
   for(const o of sample){const g=o.g,h=mirror(g);let b0=up(F1,g,C).bad,b1=up(F1,h,C).bad,c0=up(S1,[-a,...g],T).bad,c1=up(S1,[a,...g],T).bad,d0=up(S1,g,T).bad,d1=up(S1,h,T).bad;
    if(b0!==c0||b1!==c1)stats.anchoredMismatch++;if(d0!==d1)throw Error("symmetry UP mismatch");if(d0&&!(b0&&b1))throw Error("unsafe direct implication");
    stats[b0&&b1?"both":b0||b1?"one":"neither"]++;stats.direct+=Number(d0);stats.directOrientations+=Number(d0)+Number(d1);stats.guardedOrientationConflicts+=Number(b0)+Number(b1);rows.push({g,b0,b1,direct:d0});
   }
   return {mask,valid,rank:rank(F1),stats,rows,quotient:C,root:T,verification:V,liftVerification:L};
  }
  const baseline=arm([],0);
  const ad=adapter(p,G,x.dimacs,x.nvars);
  return {name,r,G,p,F,a,S,source,ad,auth,projection,chartHash,mapHash,gid,rid,baseRank,sample,orbitCount:all.length,baseline,arm,early:{native:earlyF,cnf:earlyC,root:earlyS,pins:[eF.A.size,eC.A.size,eS.A.size],conflict:[eF.bad,eC.bad,eS.bad]}};
 }
 function finish(z,parentBytes,expectedParent){
  const {r,p,F,a,S,source,ad,sample}=z,parent=JSON.parse(parentBytes),parentHash="CERT-v1:sha256:"+sha(parentBytes);
  if(parentHash!==expectedParent||parent.chartHash!==z.chartHash||parent.mapHash!==z.mapHash||parent.guard_id!==z.gid||parent.residual_id!==z.rid||parent.instance_id!==r.instance_id)throw Error("parent IDs");
  const P=parent.proof,pc=counter(),pr=replay(F,P,pc);if(!pr.valid||!pr.terminal)throw Error("parent proof");
  const lifted=[...P.map(c=>[a,...c]),...P.map(c=>[-a,...mirror(c)]),[]],lc=counter();let lr=replay(S,lifted,lc);if(!lr.valid||!lr.terminal)throw Error("root proof");
  const M=new Map(ad.mapping.map(([i,v,s])=>[v,[i,s]])),Q=P.map(c=>c.map(l=>{let [i,s]=M.get(Math.abs(l));return i*(l>0?1:-1)*(s?-1:1)})),cc=counter();if(!replay(source,Q,cc).terminal)throw Error("companion");
  const sub=P.slice(0,3);const arms=[z.baseline];for(let mask=1;mask<8;mask++)arms.push(z.arm?z.arm(sub,mask):null);
  return {P,sub,parentHash,pc,lc,cc,arms,lifted};
 }
 return {make,finish,up,replay,rank,counter,mirror,enc,sha};
}

// CLI: node orbit-boundary.js compiler.js benchmarks.json registry.json native-chart.js gauge-lift.js joint.cert.json random.cert.json
if(typeof require!=="undefined"&&require.main===module){const fs=require("node:fs");const keys=["compiler","corpus","registry","chart","gauge"];const d=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],"utf8")]));const api=setup(d);for(let i=0;i<2;i++){let z=api.make(["JOINT-24","RANDOM-3CNF-40"][i]);let f=api.finish(z,fs.readFileSync(process.argv[i+7],"utf8"),["CERT-v1:sha256:9f0cc6f89644c0ee33978982d9c3f8c74bb193316253d59fa63a5480175edff5","CERT-v1:sha256:7c97ec12cd2483475668ac80ff2b65b12fc370222eaf72842ba91e9b5a02925a"][i]);let chosen=f.arms.filter(x=>x?.valid?.valid).at(-1),S1=[...z.S,...f.sub.filter((_,j)=>chosen.mask&(1<<j)).map(c=>[z.a,...c]),...f.sub.filter((_,j)=>chosen.mask&(1<<j)).map(c=>[-z.a,...api.mirror(c)])],C=api.counter(),exclusions=[];for(const row of chosen.rows){if(row.b0&&row.b1){let ng=api.mirror(row.g),proof=[[z.a,...ng],[-z.a,...ng],ng];if(!api.replay(S1,proof,C).valid)throw Error("row join proof");exclusions.push({g:row.g,proof})}}console.log(JSON.stringify({name:z.name,auth:z.auth,chartHash:z.chartHash,mapHash:z.mapHash,early:z.early,arms:f.arms,rootReplay:f.lc,companionReplay:f.cc,exclusions,exclusionReplay:C}));}}

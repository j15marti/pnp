// Node: node feedback.js compile.js benchmarks.json registry.json affine-closure.js five.js
const fs=require("node:fs");const [compiler,corpus,registry,projection,five]=process.argv.slice(2).map(x=>fs.readFileSync(x,"utf8"));
const pins={"compiler":"21b9d53fb8166c819b24e708656c742cd3c24f10","corpus":"e315349cd6c1fe3fa696504859f28312f6aab69a","registry":"0c14cdc57925788cf7a451dcd5aa171dce860f2c","projection":"d56c096ad434544c918f83cf551d24b930be7b92","five":"25143b181236d32ec94f71c21a3ae63bfa4517b9"};
const {sha,experiment}=new Function(five.slice(five.indexOf("function sha("),five.lastIndexOf("console.log("))+"return {sha,experiment};")();
function feedbackExperiment(src,sha,pins){
 const compile=new Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal"))+"return compile")();
 const mod={exports:{}};new Function("module",src.projection)(mod);const {normalize,project}=mod.exports;
 const j=x=>JSON.stringify(x)+"\n",reg=JSON.parse(src.registry),corpus=JSON.parse(src.corpus);
 const sort=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 const taut=a=>a.some(l=>a.includes(-l));
 const CAP=1500000,PAIR=100000,ROW=2000,NODE=256,FLIP=128;
 function force(F,n,initial=[]){
  const a=new Int8Array(n+1).fill(-1),log=[];let work=0;for(const [v,b] of initial)a[v]=b;
  for(;;){let changed=false;for(let i=0;i<F.length;i++){let C=F[i],s=false,U=[];for(let l of C){work++;if(a[Math.abs(l)]===+(l>0)){s=true;break}if(a[Math.abs(l)]<0)U.push(l)}if(s)continue;if(!U.length)return {conflict:i+1,a:Array.from(a),log,work};if(U.length===1){let l=U[0];a[Math.abs(l)]=+(l>0);log.push([i+1,l]);changed=true}}if(!changed)return {conflict:null,a:Array.from(a),log,work}}
 }
 function run(F,n,arm,w){
  const start=Date.now(),C=F.map(a=>a.slice()),known=new Map(C.map((a,i)=>[a.join(","),i+1])),proof=[],flips=[],stats={pairChecks:0,replayLiteralReads:0,scoreLiteralReads:0,propagationLiteralReads:0,peakRows:C.length,peakLiterals:C.reduce((s,a)=>s+a.length,0),nodes:0},scoreRows=[];
  let work=0,cut=false,empty=C.findIndex(c=>c.length===0)+1,verified=true,assignment=null,tree=null,initialForce=force(F,n);
  // mandatory cheap forced information at intake; retain assignments, do not physically simplify until after the feedback comparison.
  const free=Array.from({length:n},(_,i)=>i+1).filter(v=>initialForce.a[v]===-1);
  const bits=b=>Array.from({length:n+1},(_,i)=>i===0?-1:initialForce.a[i]<0?b:initialForce.a[i]);
  const count=(c,a)=>{stats.scoreLiteralReads+=c.length;work+=c.length;return c.reduce((s,l)=>s+(a[Math.abs(l)]===+(l>0)),0)};
  function scanRows(){const lo=bits(0),hi=bits(1);return C.map((c,i)=>({id:i+1,occurrences:c.slice(),allFalse:count(c,lo),allTrue:count(c,hi)}))}
  function descend(a,label){
   for(let step=0;step<FLIP&&work<CAP;step++){
    const counts=C.map(c=>count(c,a)),unsat=counts.filter(z=>!z).length;if(!unsat){if(F.every(c=>c.some(l=>a[Math.abs(l)]===+(l>0))))assignment=a.slice();break}
    const gains=new Map(free.map(v=>[v,0]));
    for(let i=0;i<C.length;i++)for(const l of C[i]){work++;stats.scoreLiteralReads++;let v=Math.abs(l);if(!gains.has(v))continue;let truth=a[v]===+(l>0);if(!counts[i]&&!truth)gains.set(v,gains.get(v)+1);if(counts[i]===1&&truth)gains.set(v,gains.get(v)-1)}
    const best=[...gains].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0];if(!best||best[1]<=0)break;let [v,g]=best;a[v]^=1;flips.push({label,v,g,unsatBefore:unsat,unsatAfter:unsat-g});
   }return a;
  }
  if(arm==="flips"||arm==="feedback"){scoreRows.push({phase:"intake",rows:scanRows()});let a0=descend(bits(0),"all-false"),a1=descend(bits(1),"all-true");assignment=assignment??null;var seeds=[a0,a1]}
  function resolution(){
   // All arms use the same deterministic append-only pair order and caps. Feedback only retries flips on newly checked rows.
   for(let i=0;i<C.length&&!empty&&work<CAP;i++){
    for(let k=0;k<i&&!empty&&work<CAP;k++){
     if(stats.pairChecks>=PAIR||C.length>=ROW){cut=true;return}
     stats.pairChecks++;work++;
     for(let l of C[i]){
      work+=C[k].length+1;if(!C[k].includes(-l))continue;
      let R=sort([...C[i].filter(x=>x!==l),...C[k].filter(x=>x!==-l)]);work+=R.length;if(R.length>w||taut(R)||known.has(R.join(",")))continue;
      // independent checker: recompute union as literal sets, exact pivot and no complementary nonpivot.
      let left=new Set(C[i]),right=new Set(C[k]);if(!left.delete(l)||!right.delete(-l))throw Error("pivot");
      const U=new Set([...left,...right]);stats.replayLiteralReads+=C[i].length+C[k].length+R.length;work+=C[i].length+C[k].length+R.length;
      if(U.size!==R.length||!R.every(x=>U.has(x))||R.some(x=>U.has(-x)))throw Error("bad resolution");
      C.push(R);known.set(R.join(","),C.length);proof.push({id:C.length,parents:[i+1,k+1],pivot:l,row:R});stats.peakRows=C.length;stats.peakLiterals+=R.length;if(!R.length){empty=C.length;break}
     }
    }
   }
  }
  if(!initialForce.conflict&&(arm==="deductions"||arm==="feedback")&&!assignment){resolution();if(arm==="feedback"&&!empty&&work<CAP){scoreRows.push({phase:"after-resolution",rows:scanRows()});seeds.forEach((a,i)=>descend(a,"feedback-"+i))}}
  const pre=force(C,n);stats.propagationLiteralReads+=initialForce.work+pre.work;work+=initialForce.work+pre.work;
  let intake=initialForce.conflict?"UNSAT":empty?"UNSAT":assignment?"SAT":pre.conflict?"UNSAT":"UNKNOWN";
  // All arms same final capped split search. Root and child leaves are independently replayed using fresh unit propagation.
  function solve(g){
   if(++stats.nodes>NODE||work>CAP)throw Error("cap");
   const r=force(C,n,g);work+=r.work;stats.propagationLiteralReads+=r.work;if(r.conflict)return 0;
   const f=new Map();for(let c of C){if(c.some(l=>r.a[Math.abs(l)]===+(l>0)))continue;for(let l of c)if(r.a[Math.abs(l)]<0)f.set(Math.abs(l),(f.get(Math.abs(l))||0)+1)}
   if(!f.size){let a=r.a.map(b=>b<0?0:b);if(!F.every(c=>c.some(l=>a[Math.abs(l)]===+(l>0))))throw Error("bad witness");assignment=a;return null}
   let v=[...f].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],L=solve([...g,[v,0]]);if(L===null)return null;let R=solve([...g,[v,1]]);return R===null?null:[v,L,R]
  }
  function replay(t,g){if(t===0){let r=force(C,n,g);stats.replayLiteralReads+=r.work;return r.conflict!==null}return replay(t[1],[...g,[t[0],0]])&&replay(t[2],[...g,[t[0],1]])}
  let result=intake;if(result==="UNKNOWN"){try{tree=solve([]);if(tree!==null){verified=replay(tree,[]);if(!verified)throw Error("bad split proof");result="UNSAT"}else if(assignment)result="SAT"}catch(e){if(e.message!=="cap")throw e;cut=true}}
  if(result==="UNSAT"&&intake==="UNSAT"){const r=force(C,n);stats.replayLiteralReads+=r.work;if(!r.conflict)throw Error("intake verification")}
  const remaining=C.filter(c=>!c.some(l=>pre.a[Math.abs(l)]===+(l>0))).map(c=>c.filter(l=>pre.a[Math.abs(l)]<0));
  return {arm,width:w,stage:"intake",initialForced:initialForce.log,initialForceConflict:initialForce.conflict,afterForced:pre.log,residualBefore:{vars:n,clauses:F.length},residualAfter:{free:pre.a.slice(1).filter(a=>a<0).length,clauses:remaining.length},initialForce,pre,intake,result,verified:result!=="UNKNOWN"&&verified,cut,stats,work,elapsedMs:Date.now()-start,flips,learned:proof,tree,scoreRows,assignment};
 }
 const results=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
  let x=corpus.instances.find(a=>a.id===alias),e=reg.instances.find(a=>a.alias==="EB-"+alias),G=compile(x),bytes=j(G.network),map=j(G.source_map);
  if(sha(bytes)!==e.sha256||bytes.length*8!==e.N_bits||sha(map)!==e.source_map_sha256||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits)throw Error("auth "+alias);
  const start=Date.now(),nor=normalize(G.network),pr=project(nor.F,1500000);
  if(pr.status!=="COMPLETE")throw Error("projection cap");
  // Native CNF view exact forbidden rows on the checked projected chart, but companion CNF experiment separately identified.
  const vars=[...new Set(pr.final.flatMap(t=>t.v))].sort((a,b)=>a-b),idx=new Map(vars.map((v,i)=>[v,i+1]));
  const nativeF=pr.final.flatMap(t=>Array.from({length:2**t.v.length},(_,k)=>k).filter(k=>!t.ok.includes(k)).map(k=>sort(t.v.map((v,i)=>(k>>i&1)?-idx.get(v):idx.get(v)))));
  const nativeUnits=force(nativeF,vars.length);
  const native={rootVars:new Set(nor.root).size,normalizedFactors:nor.F.length,projectionPivots:pr.steps.length,chartVars:vars.length,chartFactors:pr.final.length,chartClauses:nativeF.length,earlyForced:nativeUnits.log,earlyConflict:nativeUnits.conflict,normalization:nor.counts,projection:pr.counts,elapsedMs:Date.now()-start};
  const F=x.dimacs.trimEnd().split("\n").slice(1).map(l=>sort(l.trim().split(/\s+/).map(Number).slice(0,-1))).filter(c=>!taut(c));
  if(F.length!==x.nclauses)throw Error("source clause mapping changed");
  const arms=["baseline","flips","deductions","feedback"].map(a=>run(F,x.nvars,a,2));
  for(const a of ["deductions","feedback"])if(arms.find(b=>b.arm===a).intake!=="UNSAT")arms.push(run(F,x.nvars,a,4));
  results.push({alias,source:e,authentication:{native:sha(bytes),cnf:sha(x.dimacs),map:sha(map)},native,arms});
 }
 const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],F=lines.flatMap(c=>[c,c.map(l=>-l)]),dimacs="p cnf 7 14\n"+F.map(c=>c.join(" ")+" 0\n").join("");
 const fano={model:"DIMACS-CNF-v1",instance_id:"DIMACS-CNF-v1:sha256:"+sha(dimacs),N_bits:dimacs.length*8,dimacs,arms:["baseline","flips","deductions","feedback"].map(a=>run(F,7,a,2))};
 for(const a of ["deductions","feedback"])fano.arms.push(run(F,7,a,4));
 return {caps:{CAP,PAIR,ROW,NODE,FLIP},results,fano};
}
const src={compiler,corpus,registry,projection,five};console.log(JSON.stringify({five:experiment(src,sha,pins),feedback:feedbackExperiment(src,sha,pins)},null,2));

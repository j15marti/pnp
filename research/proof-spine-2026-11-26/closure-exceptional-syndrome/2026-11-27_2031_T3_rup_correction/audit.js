function main(source,compilerText,corpus,registry){
 const body=source.slice(0,source.lastIndexOf("const fs=require"));
 const H=Function(body+";return {run,sha,compile}")();
 const compile=Function(compilerText.slice(compilerText.indexOf("function compile"),compilerText.indexOf("function auditLocal"))+";return compile")();
 const K=Function(body.slice(0,body.indexOf("let output=[];"))+"return {normal,project,early,clauses,gaugeFactors,tableFromCNF,solve,feedback,experiment};}; return run")()(null,null,[]);
 const ck=(x,m)=>{if(!x)throw Error(m||"check")};const sort=a=>[...new Set(a)].sort((a,b)=>a-b),canonical=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),key=c=>canonical(c).join(",");
 // Independent indexed occurrence UP, with reason row IDs. No free root advice.
 function database(C){
  const rows=C.map(c=>c.slice()),idx=new Map(),units=[];function add(c,j){for(let l of c){if(!idx.has(l))idx.set(l,[]);idx.get(l).push(j)}if(c.length<=1)units.push(j)}rows.forEach(add);
  function probe(assumptions,m,reason=false){let a=new Set(),q=[],why=new Map();function set(l,j){if(a.has(-l))return false;if(!a.has(l)){a.add(l);q.push(l);why.set(l,j)}return true}let end=null;
   for(let l of assumptions)if(!set(l,-1)){end=-1;break}
   if(end===null)for(let j of units){m.reads++;let c=rows[j];if(!c.length||!set(c[0],j)){end=j;break}}
   if(end===null)outer:for(let k=0;k<q.length;k++)for(let j of idx.get(-q[k])||[]){let c=rows[j],last=0,n=0,hit=false;for(let l of c){m.reads++;if(a.has(l)){hit=true;break}if(!a.has(-l)){last=l;n++}}if(hit)continue;if(!n||n===1&&!set(last,j)){end=j;break outer}}
   let parents=[];if(reason&&end!==null&&end>=0){let seen=new Set(),visit=j=>{if(j<0||seen.has(j))return;seen.add(j);for(let l of rows[j])if(a.has(-l))visit(why.get(-l)??-1)};visit(end);parents=sort([...seen])}
   return{conflict:end!==null,assigned:[...a],parents}
  }return{rows,probe,add:c=>{add(c,rows.length);rows.push(c.slice())}}
 }
 function reverseCheck(C,proof){let F=C.map(c=>c.slice()),reads=0;function check(c){let a=new Set(c.map(l=>-l));while(true){let u=0;for(let j=F.length-1;j>=0;j--){let n=0,last=0,hit=false;for(let l of F[j]){reads++;if(a.has(l)){hit=true;break}if(!a.has(-l)){n++;last=l}}if(hit)continue;if(!n)return true;if(n===1){u=last;break}}if(!u)return false;a.add(u)}}for(let c of proof){ck(check(c),"bad RUP");F.push(c)}return{reads,steps:proof.length,empty:proof.length>0&&!proof.at(-1).length}}
 function saturate(C,V,seeds=[]){
  const start=Date.now(),D=database(C),m={reads:0,tries:0,epochs:0,failed:0},seen=new Set(C.map(key)),proof=[],cone=[],admissions=[];let cap=20000000,status="UNKNOWN",pool=[[]];for(let v of V)pool.push([-v],[v]);for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)for(let a of [-1,1])for(let b of [-1,1])pool.push([a*V[i],b*V[j]]);
  const add=c=>{D.add(c);proof.push(c);seen.add(key(c))};
  let accepted=[],refused=[];for(let c of seeds){let q=D.probe(c.map(l=>-l),m,true);if(q.conflict){if(!seen.has(key(c)))add(c);accepted.push({c,parents:q.parents})}else refused.push(c)}
  outer:while(true){m.epochs++;let ch=false;for(let c of pool){if(m.reads>cap){status="UNKNOWN cap";break outer}if(seen.has(key(c)))continue;m.tries++;let r=D.probe(c.map(l=>-l),m,true);if(!r.conflict){m.failed++;continue}let id=D.rows.length;add(c);cone.push({id,parents:r.parents});admissions.push({c,epoch:m.epochs,order:proof.length});ch=true;if(!c.length){status="NO";break outer}
   // Prioritize the terminal after every successful admission; no irrelevant rows after root conflict.
   let q=D.probe([],m,true);if(q.conflict){let id=D.rows.length;add([]);cone.push({id,parents:q.parents});status="NO";break outer}}
   if(!ch){status="UNKNOWN fixed point";break}}
  let verify=reverseCheck(C,proof);ck(status!=="NO"||verify.empty);return{status,pool:pool.length,m,proof,cone,admissions,accepted,refused,verify,ms:Date.now()-start,logicalRows:D.rows.length,logicalLiterals:D.rows.reduce((s,c)=>s+c.length,0)}
 }
 // Exact coefficient-span syndrome and correction; generic binary linear sketch of rank <=17.
 function correction(C,V){
  const I=new Map(V.map((v,i)=>[v,i])),xor=(s,v)=>s.has(v)?s.delete(v):s.add(v);function indicator(c){let S=new Set([0n]);for(let l of c){let T=new Set(),b=1n<<BigInt(I.get(Math.abs(l)));for(let u of S){if(l>0)xor(T,u);xor(T,u|b)}S=T}return S}
  let P=C.map(indicator),mons=[...new Set(P.flatMap(s=>[...s]))].sort((a,b)=>a<b?-1:a>b?1:0),J=new Map(mons.map((v,i)=>[v,i])),rows=P.map(s=>[...s].reduce((v,u)=>v^(1n<<BigInt(J.get(u))),0n)),m={xor:0,verifyXor:0},s=8;while(2**s<=C.length)s++;ck(s<=9,"field cap");let poly=s===8?0x11b:0x211,limit=1<<s;function mul(a,b){let x=0;while(b){if(b&1)x^=a;b>>=1;a<<=1;if(a&limit)a^=poly}return x}
  for(let a=1;a<limit;a++)ck(Array.from({length:limit-1},(_,i)=>i+1).some(b=>mul(a,b)===1),"field");
  let labels=C.map((_,i)=>(1<<(2*s))|(mul(mul(i+1,i+1),i+1)<<s)|(i+1));
  function insert(B,row,parent,rev=false){while(row){let p=rev?(row&-row).toString():row.toString(2).length-1;if(!B.has(p)){B.set(p,{row,parent});return true}let a=B.get(p);row^=a.row;parent^=a.parent;m.xor++}return false}
  function reduce(B,row,rev=false){let parent=0n;while(row){let p=rev?(row&-row).toString():row.toString(2).length-1,a=B.get(p);if(!a)return null;row^=a.row;parent^=a.parent;m.verifyXor++}return parent}
  let exact=new Map(),sketch=new Map(),S=[];for(let i=0;i<rows.length;i++)insert(exact,rows[i],1n<<BigInt(i));for(let j=0;j<1+2*s;j++){let z=0n,p=0n;for(let i=0;i<rows.length;i++)if(labels[i]>>j&1){z^=rows[i];p^=1n<<BigInt(i);m.xor++}S.push({row:z,parent:p});insert(sketch,z,p)}
  let h=sketch.size,one=J.has(0n)?1n<<BigInt(J.get(0n)):null,sketchProof=one===null?null:reduce(sketch,one),correct=[],firstConstant=null;for(let i=0;i<rows.length;i++)if(insert(sketch,rows[i],1n<<BigInt(i))){correct.push(i);if(firstConstant===null&&one!==null&&reduce(sketch,one)!==null)firstConstant=correct.length}
  let independent=new Map();for(let p of S)insert(independent,p.row,p.parent,true);for(let i of correct)insert(independent,rows[i],1n<<BigInt(i),true);for(let r of rows)ck(reduce(independent,r,true)!==null,"lost source row");ck(sketch.size===exact.size&&correct.length===exact.size-h,"rank");
  let proof=one===null?null:reduce(independent,one,true),certificate=proof===null?null:rows.map((_,i)=>i).filter(i=>proof>>BigInt(i)&1n);if(certificate){let set=new Set();for(let i of certificate)for(let u of P[i])xor(set,u);ck(set.size===1&&set.has(0n),"independent polynomial replay")}
  // Same-scope cancellation of all violation indicators; export linear consequences and check their sum.
  let G=new Map();C.forEach((c,i)=>{let k=sort(c.map(Math.abs)).join();if(!G.has(k))G.set(k,[]);G.get(k).push(i)});let linear=[],sum=new Set();for(let ids of G.values()){let S=new Set();for(let i of ids)for(let u of P[i])xor(S,u);if(S.size&&[...S].every(u=>u===0n||(u&(u-1n))===0n)){linear.push({ids,terms:[...S].map(String)});for(let u of S)xor(sum,u)}}
  let scopeSumNO=sum.size===1&&sum.has(0n);
  return{rank:exact.size,sketchRank:h,correctionRows:correct.length,firstConstant,sketchNO:sketchProof!==null,exactNO:proof!==null,certificate,correct,monomials:mons.length,field:s,metrics:m,linearGroups:linear.length,scopeSumNO,scopeCertificate:scopeSumNO?linear:null,storage:{clauses:JSON.stringify(C).length*8,coefficients:(1+2*s+correct.length)*mons.length}}
 }
 function randomProbe(C,V){let D=database(C),out=[];for(let mode of ["uniform","adaptive"]){let state=20261127>>>0,draw=()=>{state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0},m={reads:0},learn=[],seen=new Set(C.map(key)),weight=new Map(V.map(v=>[v,1])),failed=0;const pick=()=>{if(mode==="uniform"||draw()%4===0)return V[draw()%V.length];let t=[...weight.values()].reduce((s,x)=>s+x,0),u=draw()%t;for(let [v,w] of weight){if(u<w)return v;u-=w}throw Error("pick")};for(let i=0;i<128;i++){let a=pick(),b=pick();if(a===b){failed++;continue}let c=canonical([(draw()&1?1:-1)*a,(draw()&1?1:-1)*b]);if(seen.has(key(c))||!D.probe(c.map(l=>-l),m).conflict){failed++;continue}seen.add(key(c));learn.push(c);weight.set(a,weight.get(a)+1);weight.set(b,weight.get(b)+1)}let check=reverseCheck(C,learn);out.push({mode,seed:20261127,failed,learn,reads:m.reads,check})}return out}
 // Mandatory baseline, early forced-information and feedback from exact pinned role-owned code.
 let regression=H.run(corpus,registry,[]);
 let out=[];
 for(let r of regression.cases){
  let name=r.e.source_cnf.alias,x=corpus.instances.find(x=>x.id===name),G=compile(x),enc=y=>JSON.stringify(y)+"\n";
  ck(H.sha(enc(G.network))===r.e.sha256&&enc(G.network).length*8===r.e.N_bits&&H.sha(x.dimacs)===r.e.source_cnf.sha256&&H.sha(enc(G.source_map))===r.e.source_map_sha256,"pinned compiler auth");
  let C=K.clauses(r.chart.F),V=r.chart.V,source=x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.split(/\s+/).map(Number).slice(0,-1)),SV=Array.from({length:x.nvars},(_,i)=>i+1);
  let standalone=saturate(C,V),direct=saturate(source,SV); // blind, before peer seed ordering
  let seeds=name==="JOINT-24"?[[-594]]:[[362,34],[362,-33],[362,298]],masks=[];
  for(let mask=0;mask<2**seeds.length;mask++){let wanted=seeds.filter((_,i)=>mask>>i&1);if(wanted.some(c=>c.some(l=>!V.includes(Math.abs(l))))){masks.push({mask,status:"UNKNOWN map"});continue}let q=saturate(C,V,wanted);masks.push({mask,...q})}
  let compression=correction(C,V),directCompression=correction(source,SV),stochastic=randomProbe(C,V);
  let feedback=r.native.arms.map(a=>({mode:a.mode,width:a.width,status:a.result?.status,nodes:a.result?.m?.nodes,ms:a.elapsedMs,score:a.score,residueOps:a.residueOps,changed:a.changed,peakSlots:a.peakSlots,learned:a.learned.length,pairs:a.pairs,proofChecks:a.proofChecks,flips:a.flips,cap:a.capHit})),directFeedback=r.direct.arms.map(a=>({mode:a.mode,width:a.width,status:a.result?.status,nodes:a.result?.m?.nodes,ms:a.elapsedMs,score:a.score,residueOps:a.residueOps,changed:a.changed,peakSlots:a.peakSlots,learned:a.learned.length,pairs:a.pairs,proofChecks:a.proofChecks}));
  out.push({e:r.e,chartId:r.chartId,chart:r.chart,map:r.map,raw:{variables:r.raw.variables,rank:r.raw.early.rank,pins:r.raw.early.pins,tests:r.raw.early.rowTests,affineOps:r.raw.early.affineOps},projection:r.projection,early:r.native.early,lanes:r.lanes,guardProofs:r.guardProofs,coverage:r.coverage,feedback,directFeedback,standalone,direct,masks,compression,directCompression,stochastic,base:r.native.arms.find(a=>a.mode==="baseline").result});
 }
 // Growing simple cubic prism Tseitin UNSAT: independently generated; no solver label assumed.
 function prism(n){let edges=[],id=new Map();function add(a,b){let k=[Math.min(a,b),Math.max(a,b)].join(",");ck(!id.has(k));id.set(k,edges.length+1);edges.push([a,b])}for(let k=0;k<2;k++)for(let i=0;i<n;i++)add(k*n+i,k*n+(i+1)%n);for(let i=0;i<n;i++)add(i,n+i);let charges=Array.from({length:2*n},(_,i)=>+(i===0)),F=[],scopes=[];for(let i=0;i<2*n;i++){let V=edges.map((e,j)=>e.includes(i)?j+1:0).filter(Boolean);ck(V.length===3);scopes.push(V);for(let w=0;w<8;w++)if(((w&1)^((w>>1)&1)^((w>>2)&1))!==charges[i])F.push(V.map((v,k)=>w>>k&1?-v:v))}let x={id:"T3-PRISM-"+n,nvars:edges.length,dimacs:"p cnf "+edges.length+" "+F.length+"\n"+F.map(c=>c.join(" ")+" 0\n").join("")};return{x,F,edges,charges,scopes}}
 let hostile=[];
 for(let n of [4,8,16,32]){
  let T=prism(n),V=Array.from({length:T.x.nvars},(_,i)=>i+1),C=T.F;
  // Mandatory early closure including exact grouping of equal scopes; group row support is intersection.
  let grouped=T.scopes.map((vs,i)=>({id:i,vs,ok:Array.from({length:8},(_,j)=>j).filter(w=>((w&1)^((w>>1)&1)^((w>>2)&1))===T.charges[i]),ids:[4*i+1,4*i+2,4*i+3,4*i+4]}));
  let early=K.early(grouped,V,C);ck(early.conflict,"affine terminal missing");
  // Isolated width-two-only arm intentionally suppresses known affine terminal as a scoped negative control.
  let rup=saturate(C,V);ck(rup.status==="UNKNOWN fixed point"&&rup.proof.length===0,"unexpected width2 admission");let corr=correction(C,V);ck(corr.exactNO&&corr.scopeSumNO,"exact correction failed");
  let G=compile(T.x),bytes=JSON.stringify(G.network)+"\n",mapBytes=JSON.stringify(G.source_map)+"\n",D=K.normal(G.network),rawV=sort(D.F.flatMap(f=>f.vs)),raw=K.early(D.F,rawV,K.clauses(D.F)),P=K.project(D.F),freq=new Map();for(let f of P.Q)for(let v of f.vs)freq.set(v,(freq.get(v)||0)+1);let anchor=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],F=K.gaugeFactors(P.Q,anchor),W=sort(F.flatMap(f=>f.vs)),Q=K.clauses(F),nativeEarly=K.early(F,W,Q),nativeRUP=saturate(Q,W),nativeCorrection=Q.length<512?correction(Q,W):null;
  // exact native chart equivalent by independently checked projection; no claim unguarded source is easy unless terminal checked.
  let chart={anchor,V:W,F,trace:P.trace},map={coordinate:"relative original representative port v-1 XOR anchor",anchor,reverse:"reverse complete incident elimination then equality BFS and undo complement gauge"};let id="STRICT-EB4-v1:sha256:"+H.sha(bytes),guardArtifact=[[anchor-1,0]],guardId="GUARD-v1:sha256:"+H.sha(JSON.stringify(["PNP-GUARD-v1",id,"EB-PORT-PINS-v1",H.sha(JSON.stringify(guardArtifact)+"\n")])+"\n"),chartId="RESIDUAL-v1:sha256:"+H.sha(JSON.stringify(["PNP-RESIDUAL-v1",id,guardId,"T3-PRISM-CHART-v1",H.sha(JSON.stringify(chart)+"\n"),H.sha(JSON.stringify(map)+"\n")])+"\n");
  hostile.push({n,instance:T.x,cnfId:"DIMACS-CNF-v1:sha256:"+H.sha(T.x.dimacs),cnfN:T.x.dimacs.length*8,edges:T.edges,charges:T.charges,scopes:T.scopes,early,rup,corr,native:{id,N:bytes.length*8,mapSha:H.sha(mapBytes),vertices:G.network.types.length,edges:G.network.edges.length,guardArtifact,guardId,chartId,chart,map,raw:{r:rawV.length,rank:raw.rank,conflict:raw.conflict},projection:{steps:P.trace.length,scans:P.scans,tests:P.tests,checkTests:P.checkTests},early:nativeEarly,rup:nativeRUP,correction:nativeCorrection}});
 }
 return{cases:out,hostile,fano:{C:regression.fano.C,exhaustive:regression.fano.exhaustive,feedback:regression.fano.experiment.arms.map(a=>({mode:a.mode,width:a.width,nodes:a.result?.m?.nodes,status:a.result?.status,ms:a.elapsedMs,changed:a.changed,learned:a.learned.length,score:a.score,residueOps:a.residueOps,peakSlots:a.peakSlots}))}}
}
const fs=require('node:fs');const [s,c,b,r]=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));console.log(JSON.stringify(main(s,c,JSON.parse(b),JSON.parse(r)),null,2));

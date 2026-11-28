// Reproduction: node bridge.js compiler.js corpus.json registry.json previous-checker.js native-chart.js
function experiment({compiler,corp,reg,old,chart}){
 const sha=new Function(old.slice(old.indexOf("function sha"),old.indexOf("function chart"))+";return sha")();
 const compile=new Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")();
 const {project,verifyProjection}=new Function(chart.slice(chart.indexOf("const key="),chart.indexOf("function up("))+";return {project,verifyProjection}")();
 const enc=x=>JSON.stringify(x)+"\n", bits=x=>x.toString(2).length-1;
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha");
 function early(p){let vars=[...new Set(p.raw.flatMap(f=>f.s))].sort((a,b)=>a-b),M=new Map(vars.map((v,i)=>[v,i+1])),B=new Map(),xor=0,checks=0;
 function add(a){while(a){let k=bits(a);if(!B.has(k)){B.set(k,a);return}a^=B.get(k);xor++}}
 const pc=m=>{let t=0;while(m){t^=1;m&=m-1}return t};
 for(let f of p.raw){for(let m=1;m<2**f.s.length;m++){let values=new Set(f.a.map(a=>{checks++;return pc(a&m)}));if(values.size!==1)continue;let row=BigInt([...values][0]);f.s.forEach((v,i)=>{if(m>>i&1)row|=1n<<BigInt(M.get(v))});add(row)}}
 add(1n<<BigInt(M.get(p.anchor)));let units=[];for(let v of vars){let a=1n<<BigInt(M.get(v));while(a>1n&&B.has(bits(a))){a^=B.get(bits(a));xor++}if(a<=1n)units.push([v,Number(a)])}return {variables:vars.length,rank:B.size,checks,xor,units,contradiction:B.has(0)}}
 function run(F){
  let start=Date.now(),vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),n=vars.length,M=new Map(vars.map((v,i)=>[v,i])),mask=l=>1n<<BigInt(M.get(Math.abs(l))),stats={terms:0,maxTerms:0,maxDegree:0};
  function toggle(S,x){if(S.has(x))S.delete(x);else S.add(x)}
  function mul(P,l){let Q=new Set(),b=mask(l);for(let m of P){stats.terms++;if(l<0)toggle(Q,m);toggle(Q,m|b)}stats.maxTerms=Math.max(stats.maxTerms,Q.size);return Q}
  function product(ls,P=new Set([0n])){for(let l of ls)P=mul(P,l);return P}
  function sum(P,Q){for(let x of Q){stats.terms++;toggle(P,x)}return P}
  function same(P,Q){return P.size===Q.size&&[...P].every(x=>Q.has(x))}
  // truth(l)=x if positive, 1+x otherwise; falsity(C)=product of truth(-l).
  let features=[0n];for(let i=0;i<n;i++)features.push(1n<<BigInt(i));for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)features.push((1n<<BigInt(i))|(1n<<BigInt(j)));for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)features.push((1n<<BigInt(i))|(1n<<BigInt(j))|(1n<<BigInt(k)));let ix=new Map(features.map((x,i)=>[x,i]));
  function vector(P){let x=0n;for(let m of P){let k=ix.get(m);if(k===undefined)throw Error("degree");x^=1n<<BigInt(k)}return x}
  function basis(base){let B=new Map(base?base.B:[]),xor=0,rows=0;return {B,add(a){rows++;while(a){let k=bits(a);if(!B.has(k)){B.set(k,a);return}a^=B.get(k);xor++}},info(){return{rank:B.size,quadratic:[...B.keys()].filter(k=>k<1+n+n*(n-1)/2).length,constant:B.has(0),rows,xor}}}}
  function rowsInto(B,c,mode){if(c.length>3)return;let P=product(c.map(l=>-l));B.add(vector(P));if(c.length<=2&&mode!=="flat")for(let v of(mode==="inside"?[...new Set(c.map(Math.abs))]:vars))B.add(vector(mul(P,v)))}
  // separate indexed discovery / full-scan independent check
  let db=F.map(c=>c.slice()),idx=new Map(),units=[],work=0,probes=0;
  function index(c,j){for(let l of c){if(!idx.has(l))idx.set(l,[]);idx.get(l).push(j)}if(c.length<=1)units.push(j)}
  db.forEach(index);
  function probe(c){let A=new Set(),q=[];function set(l){if(A.has(-l))return false;if(!A.has(l)){A.add(l);q.push(l)}return true}
   for(let l of c)if(!set(-l))return {conflict:true,A};
   for(let j of units){work++;if(!db[j].length||!set(db[j][0]))return{conflict:true,A}}
   for(let k=0;k<q.length;k++)for(let j of idx.get(-q[k])||[]){let f=db[j],u=0,m=0,sat=false;for(let l of f){work++;if(A.has(l)){sat=true;break}if(!A.has(-l)){u=l;m++}}if(!sat&&(m===0||m===1&&!set(u)))return{conflict:true,A}}
   return{conflict:false,A}}
  let init=probe([]),early={pins:init.A.size,conflict:init.conflict,visits:work};
  const flat=basis(),inside=basis(),cross=basis();for(let c of F){rowsInto(flat,c,"flat");rowsInto(inside,c,"inside");rowsInto(cross,c,"all")}
  let pcInitial={flat:flat.info(),inside:inside.info(),cross:cross.info(),wideOmitted:F.filter(c=>c.length>3).length,featureCount:features.length};
  let hy=basis(cross),first=null,firstLinear=null,proof=[],seen=new Set(F.map(c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(","))),cands=[[]];for(let v of vars)cands.push([v],[-v]);for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let a of [1,-1])for(let b of [1,-1])cands.push([a*vars[i],b*vars[j]]);
  let epochs=0,complete=false,stalled=false;
  outer:while(work<10000000){epochs++;let count=proof.length;for(let c of cands){if(seen.has(c.join(",")))continue;probes++;if(work>10000000)break outer;if(!probe(c).conflict)continue;seen.add(c.join(","));index(c,db.length);db.push(c);proof.push(c);if(c.length){rowsInto(hy,c,"all");if(hy.B.has(0)&&first===null)first=proof.length;if(hy.info().quadratic>pcInitial.cross.quadratic&&firstLinear===null)firstLinear=proof.length}else{complete=true;break outer}}if(proof.length===count){stalled=true;break}}
  // Independent reverse-order UP, with explicit local polynomial cancellation on every propagation.
  let V=F.map(c=>c.slice()),verifyVisits=0,steps=0,identityChecks=0,maxDegreeBound=0,maxActual=0,maxProofRows=0;
  function deg(m){let d=0;while(m){m&=m-1n;d++}return d}
  function audit(P){for(let m of P)maxActual=Math.max(maxActual,deg(m))}
  function replay(c){let A=new Set(c.map(l=>-l)),g=product(c.map(l=>-l)),known=new Map(),localRows=0;for(let l of A){let zero=mul(g,-l);if(zero.size)throw Error("assumption");known.set(l,zero);localRows++}
   for(;;){let changed=false;for(let j=V.length-1;j>=0;j--){let f=V[j],free=[],falseL=[],sat=false;for(let l of f){verifyVisits++;if(A.has(l)){sat=true;break}if(A.has(-l))falseL.push(l);else free.push(l)}if(sat||free.length>1)continue;
    let t=free.length?-free[0]:null, lhs=product(f.map(l=>-l),g),rhs=t===null?new Set(g):mul(g,t);audit(lhs);audit(rhs);maxDegreeBound=Math.max(maxDegreeBound,c.length+f.length);localRows++;
    // g*t*(prod (1-q)) + sum_i (g*q_i)*t*prod_{j<i}(1-q_j) = g*t.
    for(let i=0;i<falseL.length;i++){let q=falseL[i];if(!known.has(-q))throw Error("unknown parent");let term=new Set(known.get(-q));if(t!==null)term=mul(term,t);for(let k=0;k<i;k++)term=mul(term,-falseL[k]);sum(lhs,term);localRows+=i+2}
    if(!same(lhs,rhs))throw Error("syzygy identity");identityChecks++;steps++;if(t===null){maxProofRows=Math.max(maxProofRows,localRows);return true}A.add(free[0]);known.set(free[0],rhs);changed=true;
   }if(!changed)return false}}
  for(let c of proof){if(!replay(c))throw Error("replay failure");V.push(c)}
  let hybrid=hy.info(),elapsed=Date.now()-start;return {n,rows:F.length,maxWidth:Math.max(...F.map(c=>c.length)),early,pcInitial,hybrid,firstPCConstantBeforeEmpty:first,firstQuadraticRankGain:firstLinear,proof,complete,stalled,epochs,probes,discoveryVisits:work,verifyVisits,steps,identityChecks,maxDegreeBound,maxActual,maxProofRows,polynomialOps:stats,elapsed};
 }
 let out=[];for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=JSON.parse(corp).instances.find(x=>x.id===name),rr=JSON.parse(reg).instances.find(x=>x.alias==="EB-"+name),G=compile(x);
 if(sha(enc(G.network))!==rr.sha256||enc(G.network).length*8!==rr.N_bits||sha(x.dimacs)!==rr.source_cnf.sha256||x.dimacs.length*8!==rr.source_cnf.N_bits||sha(enc(G.source_map))!==rr.source_map_sha256)throw Error("hash");
 let p=project(G.network),ops=verifyProjection(G.network,p),closure=early(p);if(closure.contradiction||closure.units.length!==1)throw Error("unexpected affine closure; must reduce first");
 let gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",rr.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",rr.instance_id,gid,"EB-CHART-SYZYGY-v1",sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),sha(enc({root:p.root,phase:p.phase}))]));
 let native=run(p.clauses),cnf=run(x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1)));let item={name,registry:rr,gid,rid,anchor:p.anchor,projectionReplay:ops,projectionCost:p.cost,closure,chart:p.clauses,native,cnf};item.evidenceSHA256=sha(enc(item));out.push(item)}
 return out
}
if(typeof require!== 'undefined' && require.main===module){const fs=require('node:fs');let keys=['compiler','corp','reg','old','chart'];console.log(JSON.stringify(experiment(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]))),null,2));}

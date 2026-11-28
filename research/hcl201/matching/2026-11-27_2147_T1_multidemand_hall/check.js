// node check.js compile.js benchmarks.json registry.json native-chart.js
// Inputs pinned in report; exact authenticated source-only chart, independent replay, Hall checker.
function check(compiler,corpus,registry,chart,sha){
const compile=new Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")();
const {project,verifyProjection}=new Function(chart.slice(chart.indexOf("const key="),chart.indexOf("function up("))+";return {project,verifyProjection}")();
const enc=x=>JSON.stringify(x)+"\n",key=c=>c.slice().sort((a,b)=>a-b).join(",");
function rup(F){
let V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),L=V.flatMap(v=>[v,-v]),keys=new Set(F.map(key)),visits=0,probes=0;
function up(A){A=new Set(A);let change=true;while(change){change=false;for(let c of F){let n=0,u=0,sat=false;for(let l of c){visits++;if(A.has(l)){sat=true;break}if(!A.has(-l)){n++;u=l}}if(sat)continue;if(!n)return {conflict:true,pins:[...A]};if(n===1){A.add(u);change=true}}}return {conflict:false,pins:[...A]}}
let early=up([]),earlyVisits=visits;for(let i=0;i<L.length;i++)for(let j=-1;j<i;j++){let c=j<0?[L[i]]:[L[j],L[i]];if(c.length===2&&c[0]===-c[1]||keys.has(key(c)))continue;if(visits>=2000000)return {early,earlyVisits,probes,visits:visits-earlyVisits,status:"CAP"};probes++;if(up(c.map(l=>-l)).conflict)return {early,earlyVisits,probes,visits:visits-earlyVisits,admission:c,status:"FIRST_ADMISSION"}}
return {early,earlyVisits,probes,visits:visits-earlyVisits,status:"FIXED_POINT"};}
function acquire(F){
let B=new Map(F.map((c,i)=>[key(c),i])),best=null,checks=0;
for(let mode=0;mode<3;mode++){let rows=[],owner=new Map();for(let i=0;i<F.length;i++){let c=F[i];if(c.length>=3&&new Set(c).size===c.length&&(mode===0?c.every(l=>l>0):mode===1?c.every(l=>l<0):true)&&c.every(l=>!owner.has(l))){rows.push(i);c.forEach(l=>owner.set(l,i))}}
let bins=[];for(let [l,i] of owner){let b=bins.find(b=>b.every(x=>{checks++;return owner.get(x)!==i&&(l===-x||B.has(key([-l,-x])))}));if(b)b.push(l);else bins.push([l]);}
let M=new Map(),adj=rows.map(i=>bins.map((b,j)=>b.some(l=>owner.get(l)===i)?j:-1).filter(j=>j>=0));function aug(i,seen){for(let j of adj[i]){checks++;if(seen.has(j))continue;seen.add(j);if(!M.has(j)||aug(M.get(j),seen)){M.set(j,i);return true}}return false}
let q=[];for(let i=0;i<rows.length;i++)if(!aug(i,new Set()))q.push(i);let I=new Set(q),J=new Set();for(let i of q)for(let j of adj[i]){J.add(j);if(M.has(j)&&!I.has(M.get(j))){I.add(M.get(j));q.push(M.get(j))}}
let cert=null;if(I.size>J.size){let rr=[...I].map(i=>rows[i]).sort((a,b)=>a-b),ls=new Set(rr.flatMap(i=>F[i])),bb=[...J].map(j=>bins[j].filter(l=>ls.has(l))).sort((a,b)=>a[0]-b[0]),pairs=[];for(let b of bb)for(let i=0;i<b.length;i++)for(let j=i+1;j<b.length;j++)if(b[i]!==-b[j])pairs.push([b[i],b[j],B.get(key([-b[i],-b[j]]))]);cert={rows:rr,bins:bb,pairs};}
let out={mode,demands:rows.length,bins:bins.length,matched:M.size,deficiency:I.size-J.size,cert};if(!best||out.deficiency>best.deficiency)best=out;}
return {...best,checks};}
function verify(F,c){let seen=new Set(),checks=0;for(let i of c.rows){if(!F[i])throw Error("row");for(let l of F[i]){checks++;if(seen.has(l))throw Error("overlap");seen.add(l)}}let left=new Set(seen);for(let b of c.bins){for(let l of b){checks++;if(!left.delete(l))throw Error("cover")}for(let i=0;i<b.length;i++)for(let j=i+1;j<b.length;j++){checks++;if(b[i]===-b[j])continue;let p=c.pairs.find(([x,y])=>x===b[i]&&y===b[j]);if(!p||F[p[2]].length!==2||!F[p[2]].includes(-b[i])||!F[p[2]].includes(-b[j]))throw Error("conflict")}}if(left.size||c.rows.length<=c.bins.length)throw Error("not Hall");return checks}
let out=[];
for(let name of ["JOINT-24","RANDOM-3CNF-40","PHP-4"]){let x=corpus.instances.find(x=>x.id===name),r=registry.instances.find(x=>x.alias==="EB-"+name),G=compile(x);if(sha(enc(G.network))!==r.sha256||enc(G.network).length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||x.dimacs.length*8!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("auth");
let p=project(G.network),projection=verifyProjection(G.network,p),chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
let cnf=x.dimacs.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1));
for(let [view,F] of [["native",p.clauses],["cnf",cnf]]){let R=rup(F),h=acquire(F),c=h.cert,verification=c?verify(F,c):null,payload=c?{format:"T1-HALL-CLIQUE-v1",instance:view==="native"?r.instance_id:r.source_cnf.instance_id,guard:view==="native"?gid:"EMPTY",residual:view==="native"?rid:"ROOT",index:"zero-based rows",Fhash:sha(enc(F)),...c}:null;out.push({name,view,N:view==="native"?r.N_bits:r.source_cnf.N_bits,guard:view==="native"?gid:"EMPTY",residual:view==="native"?rid:"ROOT",projection:view==="native"?projection:null,normalization:view==="native"?p.cost:null,R,h,verification,payload,certificateHash:payload?sha(enc(payload)):null});}}
return out;
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("node:fs"),crypto=require("node:crypto"),[c,b,r,p]=process.argv.slice(2).map(x=>fs.readFileSync(x,"utf8"));console.log(JSON.stringify(check(c,JSON.parse(b),JSON.parse(r),p,s=>crypto.createHash("sha256").update(s,"utf8").digest("hex")),null,2))}

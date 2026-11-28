function run(d){
const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,up,adapter}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,up,adapter}")();
const enc=x=>JSON.stringify(x)+"\n";if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha");
const pc=(F,d,mode,cap,target=[])=>{
let vars=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),n=vars.length,idx=new Map(vars.map((v,i)=>[v,i])),mons=[],mi=new Map(),bits=[],bm=new Map(),events=0,steps=0,sweeps=0,rows=0,rank0=0,rank=0,complete=false,hit=false,why="",B=new Map();
function bump(k=1){events+=k;if(events>cap)throw Error("cap")}
function gen(m,j,k){mons.push(m);if(k)for(let i=j;i<n;i++)gen(m|(1n<<BigInt(i)),i+1,k-1)}
gen(0n,0,d);mons.sort((a,b)=>a<b?-1:a>b?1:0);mons.forEach((m,i)=>{let b=1n<<BigInt(i);mi.set(m,b);bits.push(b);bm.set(b,m)});
function mulPoly(P,v,restrict=false){let out=new Set();for(let m of P){bump();let q=m|v;if(out.has(q))out.delete(q);else out.add(q)}return out}
function pol(c){let P=new Set([0n]);for(let l of c){let t=1n<<BigInt(idx.get(Math.abs(l))),Q=mulPoly(P,t);if(l>0)for(let m of P){bump();if(Q.has(m))Q.delete(m);else Q.add(m)}P=Q}return P}
function row(P){let r=0n;for(let m of P){let b=mi.get(m);if(b===undefined)return null;r^=b}return r}
function add(r){if(r===null)return false;rows++;while(r){bump();let p=r&-r;if(!B.has(p)){B.set(p,r);return true}r^=B.get(p)}return false}
function has(r){while(r){bump();let p=r&-r;if(!B.has(p))return false;r^=B.get(p)}return true}
function xor(P,Q){let R=new Set(P);for(let m of Q){if(R.has(m))R.delete(m);else R.add(m)}return R}
let goal=1n;if(target.length){goal=target.reduce((a,l)=>a^(l===0?1n:mi.get(1n<<BigInt(idx.get(l)))),0n)}
let used=0,omitted=0,groups=0,affine=0,trace=[];
try{
let polys=F.map(pol);
if(mode.startsWith("group")){let pairs=new Map();for(let i=0;i<F.length;i++){let k=[...F[i]].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(","),q=[...F[i]].map(l=>-l).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");if(pairs.has(q)){let j=pairs.get(q);polys[i]=xor(polys[i],polys[j]);polys[j]=null;pairs.delete(q);groups++}else pairs.set(k,i)}}
for(let P of polys){if(!P)continue;let r=row(P);if(r===null){omitted++;continue}used++;add(r)}
rank0=B.size;hit=has(goal);if(mode.endsWith("flat"))complete=true;
while(!hit&&!complete){let old=B.size;sweeps++;
for(let i=0;i<n;i++){let v=1n<<BigInt(i),high=0n,mp=new Map(),H=new Map();for(let j=0;j<mons.length;j++){bump();let b=bits[j],t=mi.get(mons[j]|v);if(t===undefined)high|=b;else mp.set(b,t)}
let snapshot=[...B.values()];for(let r0 of snapshot){let r=r0,h=r&high;while(h){bump();let k=h&-h;if(!H.has(k)){H.set(k,r);break}let u=H.get(k);r^=u;h=r&high}if(!h&&r){let y=0n;while(r){bump();let b=r&-r;r^=b;y^=mp.get(b)}if(add(y))steps++}}
if(has(goal)){hit=true;break}}
trace.push(B.size);if(B.size===old)complete=true}
}catch(e){if(e.message!=="cap")throw e;why="event cap"}
rank=B.size;
let f=null;if(complete||hit){try{f=has(goal)}catch(e){f=hit}}
return {n,d,mode,D:mons.length,rank0,rank,used,omitted,groups,rows,events,steps,sweeps,trace,hit:hit||f===true,complete,why,peakBasisBits:rank*mons.length}
};
const parse=x=>x.trimEnd().split("\n").slice(1).map(c=>c.trim().split(/\s+/).map(Number).slice(0,-1));
const U=(F,g=[])=>{let u=up(F,g);return {pins:u.a.size,work:u.work,conflict:u.conflict}};
let out={common:[],ring:null};
for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=JSON.parse(d.corpus).instances.find(x=>x.id===name),reg=JSON.parse(d.registry).instances.find(x=>x.alias==="EB-"+name),G=compile(x);if(sha(enc(G.network))!==reg.sha256||enc(G.network).length*8!==reg.N_bits||sha(x.dimacs)!==reg.source_cnf.sha256||x.dimacs.length*8!==reg.source_cnf.N_bits||sha(enc(G.source_map))!==reg.source_map_sha256)throw Error("auth");let p=project(G.network),projection=verifyProjection(G.network,p),F=p.clauses,root=U(F),C=parse(x.dimacs),cnfRoot=U(C);
let chartHash=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mapHash=sha(enc({root:p.root,phase:p.phase})),gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",reg.instance_id,"EB-PORT-PINS-v1",sha(enc([[p.anchor,0]]))])),rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",reg.instance_id,gid,"EB-CHART-SYZYGY-v1",chartHash,mapHash]));
let arms=[];for(let [label,R] of [["native",F],["companion",C]])for(let [degree,mode] of [[2,"group-flat"],[3,"raw-flat"],[3,"group-full"]])arms.push({label,...pc(R,degree,mode,250000)});
let peerText=name==="JOINT-24"?d.joint:d.random,peer=JSON.parse(peerText);if(peer.guard_id!==gid||peer.residual_id!==rid||peer.chartHash!==chartHash||peer.mapHash!==mapHash)throw Error("peer scope");let H=[...F],replay=[];for(let c of peer.seeds){let u=U(H,c.map(l=>[Math.abs(l),Number(l<0)]));if(!u.conflict)throw Error("seed");replay.push({c,...u});H.push(c)}let hybrid=pc(H,3,"group-full",250000),ablation=peer.seeds.map((_,i)=>{let K=[...F],cost=0;for(let [j,c] of peer.seeds.entries()){if(j===i)continue;let u=U(K,c.map(l=>[Math.abs(l),Number(l<0)]));cost+=u.work;if(!u.conflict)return {removed:i,admitted:false,cost};K.push(c)}return {removed:i,admitted:true,cost,flat:pc(K,3,"group-flat",250000)}});
let ad=adapter(p,G,x.dimacs,x.nvars);out.common.push({name,reg,root,cnfRoot,projection,projectionDiscovery:p.cost,carriers:p.carriers,chartHash,mapHash,gid,rid,anchor:p.anchor,arms,peer_sha:sha(peerText),replay,hybrid,ablation,postRoot:U(H),adapterUnique:ad.unique});
}
let peer=JSON.parse(d.ring),proof=peer.proof,x={id:proof.alias,nvars:proof.n,dimacs:proof.dimacs};if(sha(x.dimacs)!==peer.instance_id.split(":").at(-1)||x.dimacs.length*8!==peer.original_N_bits)throw Error("ring auth");let G=compile(x);if(sha(enc(G.network))!==proof.native.instance_id.split(":").at(-1)||enc(G.network).length*8!==proof.native.N_bits||sha(enc(G.source_map))!==proof.native.map_sha256)throw Error("ring native auth");let F=parse(x.dimacs),root=U(F),local=[];for(let b=0;b<12;b++){let R=F.slice(12*b,12*b+12),u=b+1,v=(b+1)%12+1,target=[u,v,...(b===11?[0]:[])],a=[];for(let [degree,mode] of [[2,"group-flat"],[2,"group-full"],[3,"group-flat"],[3,"group-full"],[3,"raw-full"],[4,"group-full"]])a.push(pc(R,degree,mode,250000,target));let checks=0,valid=true,accepted=0,vs=[...new Set(R.flat().map(Math.abs))].sort((a,b)=>a-b),witnesses=[];for(let m=0;m<128;m++){let bit=i=>Number(!!(m&(1<<vs.indexOf(i))));if(R.every(c=>c.some(l=>bit(Math.abs(l))===Number(l>0)))){accepted++;witnesses.push(m);if((bit(u)^bit(v))!==Number(b===11))valid=false}checks++}if(!valid||!accepted)throw Error("local replay");local.push({b,originalClauseIds:Array.from({length:12},(_,i)=>12*b+i+1),vs,target,root:U(R),checks,accepted,witnesses,arms:a})}
out.ring={peer_sha:sha(d.ring),instance_id:peer.instance_id,original_N_bits:peer.original_N_bits,native:proof.native,root,local,global3:pc(F,3,"group-full",250000),globalFlat:pc(F,2,"group-flat",250000),xor:local.reduce((z,l)=>z^(l.target.includes(0)?1:0),0)};
return out
}
module.exports={run};

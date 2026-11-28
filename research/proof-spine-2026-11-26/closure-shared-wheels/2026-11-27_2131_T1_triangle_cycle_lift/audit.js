// Node: node audit.js compiler corpus registry chart sha-helper joint-cone random-cone
function run(d){
const sha=new Function(d.hash.slice(0,d.hash.indexOf("function quotient"))+";return sha")(),compile=new Function(d.compiler.slice(d.compiler.indexOf("function compile"),d.compiler.indexOf("function auditLocal"))+";return compile")(),{project,verifyProjection,up,solve,replay,adapter}=new Function(d.chart.slice(d.chart.indexOf("const key="),d.chart.indexOf("function checkHall"))+";return {project,verifyProjection,up,solve,replay,adapter}")();
const enc=x=>JSON.stringify(x)+"\n",key=c=>[...c].sort((a,b)=>a-b).join(",");
if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha");
function rank(rows){let basis=new Map(),ops=0;for(let x of rows){while(x){let i=x.toString(2).length-1;ops++;if(!basis.has(i)){basis.set(i,x);break}x^=basis.get(i)}}return {rank:basis.size,ops}}
function scan(T){
let E=new Map(),tri=[],vs=new Set(),ownerPairs=0;
for(let f of T){let a=f.l.map(Math.abs),s=f.l.map(v=>Number(v<0));if(new Set(a).size!==3)throw Error("not distinct");a.forEach(v=>vs.add(v));let row=[];for(let [i,j] of [[0,1],[1,2],[0,2]]){let k=[a[i],a[j]].sort((a,b)=>a-b).join(",");if(!E.has(k))E.set(k,{id:E.size,a:Math.min(a[i],a[j]),b:Math.max(a[i],a[j]),occ:[]});let e=E.get(k);let sign=s[i]^s[j];e.occ.push([f.id,sign]);row.push([e.id,sign])}tri.push(row)}
let par=new Map([...vs].map(x=>[x,x]));function find(x){while(par.get(x)!==x)x=par.get(x);return x}
for(let e of E.values()){let a=find(e.a),b=find(e.b);if(a!==b)par.set(a,b);ownerPairs+=e.occ.length*(e.occ.length-1)/2}
let comp=new Set([...vs].map(find)).size,cycle=E.size-vs.size+comp,rr=rank(tri.map(t=>t.reduce((v,[i])=>v^(1n<<BigInt(i)),0n)));
let histogram={};for(let e of E.values())histogram[e.occ.length]=(histogram[e.occ.length]||0)+1;
let pairChecks=0,forcedPairs=[],sameScope=0,paired=new Set(),tm=new Map(T.map(t=>[t.id,t]));
for(let e of E.values())for(let i=0;i<e.occ.length;i++)for(let j=i+1;j<e.occ.length;j++){
let [p,q]=[e.occ[i][0],e.occ[j][0]].sort((a,b)=>a-b),k=p+","+q;if(paired.has(k))continue;paired.add(k);
let A=tm.get(p),B=tm.get(q),V=[...new Set([...A.l,...B.l].map(Math.abs))].sort((a,b)=>a-b);if(V.length===3)sameScope++;
let possible=[false,false];for(let w=0;w<2**V.length;w++){const val=l=>((w>>V.indexOf(Math.abs(l)))&1)^Number(l<0);const ok=f=>{let z=f.l.map(val);return z.some(x=>x!==z[0])};pairChecks++;if(ok(A)&&ok(B))possible[((w>>V.indexOf(e.a))^(w>>V.indexOf(e.b)))&1]=true}if(possible.filter(Boolean).length===1)forcedPairs.push({parents:[p,q],edge:[e.a,e.b],value:Number(possible[1])});
}
return {triangles:T.length,vertices:vs.size,edges:E.size,components:comp,cycleRank:cycle,triangleRank:rr.rank,missingCycleRank:cycle-rr.rank,rankXors:rr.ops,maxEdgeDegree:Math.max(0,...[...E.values()].map(x=>x.occ.length)),histogram,ownerPairs,distinctOverlappingPairs:paired.size,sameScope,pairChecks,forcedPairs,edgeList:[...E.values()],tri};
}
function extract(p){let deg=new Map();for(let f of p.raw)for(let v of f.s)deg.set(v,(deg.get(v)||0)+1);let T=[],unrecognized=[],checks=0;
for(let f of p.raw){let slack=f.s.find(v=>deg.get(v)===1);if(slack===undefined||f.s.length!==4){unrecognized.push(f.id);continue}let pos=f.s.indexOf(slack),s=f.s.filter(v=>v!==slack),support=new Set(f.a.map(m=>(m&((1<<pos)-1))|((m>>(pos+1))<<pos)));let bad=[];for(let w=0;w<8;w++){checks++;if(!support.has(w))bad.push(w)}if(bad.length!==2||(bad[0]^bad[1])!==7){unrecognized.push(f.id);continue}T.push({id:f.id,l:s.map((v,i)=>(v+1)*((bad[0]>>i)&1?-1:1)),B:f.B,slack})}return {T,unrecognized,checks}}
function rup(F,P){let G=F.map(c=>[...c]),visits=0;for(let c of P){let u=up(G,c.map(l=>[Math.abs(l),Number(l<0)]));visits+=u.work;if(!u.conflict)return {ok:false,visits};G.push(c)}return {ok:true,visits,empty:P.at(-1)?.length===0}}
function feedback(F){const V=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);function arm(res){let A=new Map(V.map(v=>[v,0])),moves=[],work=0,ties=0;function score(){let bad=0,zero=0;for(let c of F){let k=0,t=0;for(let l of c){work++;let s=A.get(Math.abs(l))===Number(l>0)?Math.sign(l):0;k+=s*s;t+=s}let km=k%3,tm=(t%3+3)%3;if(k===0)bad++;else if(tm===0)zero++;}return [bad,zero]}let s=score();for(let i=0;i<F.length;i++){let cand=[];for(let v of V){A.set(v,1-A.get(v));let z=score();A.set(v,1-A.get(v));if(z[0]<s[0])cand.push([v,...z])}if(!cand.length)break;cand.sort((a,b)=>a[1]-b[1]||a[0]-b[0]);let plain=cand[0][0];if(res)cand.sort((a,b)=>a[1]-b[1]||a[2]-b[2]||a[0]-b[0]);let [v,b,z]=cand[0];if(v!==plain)ties++;A.set(v,1-A.get(v));s=[b,z];moves.push(v)}return {moves,work,ties,violations:s[0]}}return [arm(false),arm(true)]}
let out=[];
for(let [id,peer] of [["JOINT-24","joint"],["RANDOM-3CNF-40","random"]]){
let x=JSON.parse(d.corpus).instances.find(q=>q.id===id),r=JSON.parse(d.reg).instances.find(q=>q.alias==="EB-"+id),G=compile(x),s=enc(G.network);
if(sha(s)!==r.sha256||8*s.length!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||8*x.dimacs.length!==r.source_cnf.N_bits||sha(enc(G.source_map))!==r.source_map_sha256)throw Error("auth");
let p=project(G.network),verification=verifyProjection(G.network,p),U=up(p.clauses),q=extract(p),m=scan(q.T),base=solve(p.clauses),baseReplay=replay(p.clauses,base.tree),a=adapter(p,G,x.dimacs,x.nvars),cnfU=up(a.orig),cnf=solve(a.orig),cnfReplay=replay(a.orig,cnf.tree),fb=U.conflict?null:feedback(p.clauses),cf=cnfU.conflict?null:feedback(a.orig);
let c=JSON.parse(d[peer]),ch=sha(enc({anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final})),mh=sha(enc({root:p.root,phase:p.phase})),pr=null;
if(ch===c.chartHash&&mh===c.mapHash&&sha(enc(c.proof))===c.proofHash)pr=rup(p.clauses,c.proof);
let e={id,instance:r.instance_id,short:r.short_id,N:r.N_bits,cnf:r.source_cnf,map:r.source_map_sha256,chartHash:ch,mapHash:mh,guard:c.guard_id,residual:c.residual_id,projection:{cost:p.cost,verification,carriers:p.carriers,anchor:p.anchor,eliminated:p.steps.length,rows:p.clauses.length,rootUP:{pins:U.a.size,work:U.work,conflict:U.conflict}},extract:q,scan:m,baseline:base,baselineReplay:baseReplay,companion:{early:{pins:cnfU.a.size,work:cnfU.work},baseline:cnf,replay:cnfReplay,feedback:cf},nativeFeedback:fb,peer:{proofHash:c.proofHash,replay:pr,steps:c.proof.length}};
out.push(e)
}
let controls=[];for(let k of [1,2,4,8]){let T=[],F=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];for(let j=0;j<k;j++)for(let t of F)T.push({id:T.length,l:t.map(v=>v===1?1:6*j+v)});
let f=scan(T),checks=0,good=0;for(let w=0;w<128;w++){checks++;if(F.every(t=>t.some(v=>((w>>(v-1))&1)!==((w>>(t[0]-1))&1))))good++}if(good)throw Error("Fano not NO");
controls.push({copies:k,triangles:f.triangles,vertices:f.vertices,edges:f.edges,cycleRank:f.cycleRank,triangleRank:f.triangleRank,missing:f.missingCycleRank,maxEdgeDegree:f.maxEdgeDegree,localChecks:checks,rootWitnesses:good,matchingWitness:"choose first edge of each triangle; every edge occurs once; cycle constraints missing"});}
return {out,controls};
}
if(typeof require!=='undefined'&&require.main===module){const fs=require('node:fs');let keys=['compiler','corpus','reg','chart','hash','joint','random'];console.log(JSON.stringify(run(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]))),null,2));}

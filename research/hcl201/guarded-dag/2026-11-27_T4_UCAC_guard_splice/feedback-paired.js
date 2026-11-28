function feedbackTrial(h,raws){
const H=Function(h.slice(0,h.indexOf('const fs=require("node:fs"),[compiler'))+";return {sha,solve}")(),J=x=>JSON.stringify(x)+"\n",sha=H.sha;
const sort=x=>[...new Set(x)].sort((a,b)=>a-b),vars=C=>sort(C.flat().map(Math.abs));
const cnf=F=>F.flatMap(f=>Array.from({length:2**f.vs.length},(_,w)=>w).filter(w=>!f.ok.includes(w)).map(w=>f.vs.map((v,i)=>(w>>i&1)?-v:v)));
const tables=C=>C.map((c,id)=>{let vs=sort(c.map(Math.abs));return{id,vs,ok:Array.from({length:2**vs.length},(_,w)=>w).filter(w=>c.some(l=>((w>>vs.indexOf(Math.abs(l)))&1)===Number(l>0)))}});const cap=1500000;
function up(C,A,M){A=new Map(A);for(;;){let ch=false;for(const c of C){let n=0,last=0,sat=false;for(const l of c){if(++M.events>cap)throw Error("CAP");M.up++;let v=Math.abs(l);if(!A.has(v)){n++;last=l}else if(A.get(v)===Number(l>0)){sat=true;break}}if(sat)continue;if(!n)return{bad:true,A};if(n===1){A.set(Math.abs(last),Number(last>0));ch=true}}if(!ch)return{bad:false,A}}}
function learn(C,w,M){let D=C.slice(),seen=new Set(C.map(c=>J(sort(c)))),proof=[];if(!w)return{D,proof};outer:for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){if(++M.events>cap)throw Error("CAP");M.pairs++;if(M.pairs>10000)break outer;for(let l of C[i])if(C[j].includes(-l)){const p=sort(C[i].filter(x=>x!==l).concat(C[j].filter(x=>x!==-l)));if(p.length>w||p.some(x=>p.includes(-x))||seen.has(J(p)))continue;seen.add(J(p));proof.push({i,j,l,p});D.push(p);if(proof.length>=64)break outer}}return{D,proof}}
function score(C,A,M){let bad=0,z=0,rows=[];for(let c of C){let k=0,s=0;for(let l of c){if(++M.events>cap)throw Error("CAP");M.score++;if(A.get(Math.abs(l))===Number(l>0)){k++;s+=l>0?1:-1}}rows.push([k,k%3,(s%3+3)%3]);if(!k)bad++;else if((s%3+3)%3===0)z++}return{bad,z,rows}}
function flips(C,mode,M,A){let s=score(C,A,M),initial={bad:s.bad,z:s.z};let trace=[];if(mode)for(let t=0;t<40;t++){let first=null,best=null;for(let v of vars(C)){A.set(v,1-A.get(v));let z=score(C,A,M);A.set(v,1-A.get(v));if(z.bad>=s.bad)continue;if(!first||z.bad<first.s.bad)first={v,s:z};if(!best||z.bad<best.s.bad||mode===2&&z.bad===best.s.bad&&z.z<best.s.z)best={v,s:z}}if(!best)break;A.set(best.v,1-A.get(best.v));trace.push({v:best.v,bad:best.s.bad,residue0:best.s.z,tieChanged:best.v!==first.v});s=best.s;}return{A,trace,initial,final:{bad:s.bad,z:s.z},rows:s.rows}}
function arm(C,width,mode,initial){let start=Date.now(),M={events:0,up:0,pairs:0,score:0,nodes:0,peakLiterals:0},D=C,proof=[],fl=null,tree=null,status="UNKNOWN",replay=null,verified=false,checkLearn=0;try{let u=up(C,[],M);if(u.bad){status="UNSAT";tree=0;M.nodes++}else{({D,proof}=learn(C,width,M));M.peakLiterals=D.reduce((s,c)=>s+c.length,0);const freq=new Map(vars(D).map(v=>[v,D.filter(c=>c.some(l=>Math.abs(l)===v)).length]));let A=new Map(vars(D).map(v=>[v,initial]));if(mode)fl=flips(D,mode,M,A);
function go(a){M.nodes++;let z=up(D,a,M);if(z.bad)return 0;let V=vars(D).filter(v=>!z.A.has(v)).sort((a,b)=>freq.get(b)-freq.get(a)||a-b);if(!V.length)return{sat:[...z.A]};let v=V[0],p=A.get(v),c=[];for(let b of [p,1-p]){let q=go(new Map([...z.A,[v,b]]));if(q?.sat)return q;c[b]=q}return[v,c[0],c[1]]}
tree=go(new Map());status=tree?.sat?"SAT":"UNSAT"}
}catch(e){if(String(e).includes("CAP"))status="UNKNOWN_CAP";else throw e}
let discoveryMs=Date.now()-start;
let checkStart=Date.now();for(let p of proof){let a=C[p.i],b=C[p.j],res=sort(a.filter(x=>x!==p.l).concat(b.filter(x=>x!==-p.l)));checkLearn+=a.length+b.length+res.length;if(!a.includes(p.l)||!b.includes(-p.l)||J(res)!==J(p.p)||res.length>width||res.some(x=>res.includes(-x)))throw Error("bad resolution trace")}
if(status==="UNSAT"){replay=H.solve(tables(D),new Map(),450000,tree);verified=replay.status==="UNSAT";if(!verified)throw Error("bad tree replay "+JSON.stringify(replay))}
else if(status==="SAT"){const a=new Map(tree.sat);verified=C.every(c=>c.some(l=>a.get(Math.abs(l))===Number(l>0)));if(!verified)throw Error("invalid SAT")}
return{width,mode,status,verified,M,learned:proof.length,proof,fl:fl?{trace:fl.trace,initial:fl.initial,final:fl.final,rows:fl.rows}:null,tree,replayTests:replay?.tests??0,checkLearn,discoveryMs,verifyMs:Date.now()-checkStart}}
const results=[];
for(let raw of raws){let q=JSON.parse(raw),C=cnf(q.chart.factors),M={events:0,up:0},imports=[];
for(let seed of q.seedReplay.filter(s=>s.rup)){if(!up(C,seed.d.map(l=>[Math.abs(l),Number(l<0)]),M).bad)throw Error("seed replay");C.push(seed.d);imports.push(seed.d)}
if(q.peer?.ok){let d=q.peer.d;if(!up(C,d.map(l=>[Math.abs(l),Number(l<0)]),M).bad)throw Error("peer replay");C.push(d);imports.push(d)}
const arms=[["baseline",0,0],["flips-only",0,1],["ded2",2,0],["table2",2,1],["residue2",2,2],["ded4",4,0],["table4",4,1],["residue4",4,2]].map(([name,w,m])=>({name,...arm(C,w,m,0)}));
results.push({instance:q.instance,instance_id:q.instance_id,problem_id:q.problem_id,original_N_bits:q.original_N_bits,guard_id:q.guard_id,residual_id:q.residual_id,source_pin:q.source_pin,chartEvidence:sha(raw),importReplay:M,imports,cap,arms});
}
const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
for(let control of [false,true]){let C=(control?lines.slice(0,-1):lines).flatMap(c=>[c,c.map(x=>-x)]),dimacs="p cnf 7 "+C.length+"\n"+C.map(c=>c.join(" ")+" 0\n").join(""),id=sha(dimacs),arms=[["baseline",0,0],["ded2",2,0],["table2",2,1],["residue2",2,2],["ded4",4,0],["table4",4,1],["residue4",4,2]].map(([name,w,m])=>({name,...arm(C,w,m,0)}));results.push({instance:(control?"FANO-ONE-LINE-DELETED":"FANO-NAE")+"@"+id.slice(0,12),problem_id:"DIMACS-CNF-v1",instance_id:"DIMACS-CNF-v1:sha256:"+id,original_N_bits:dimacs.length*8,guard_id:"EMPTY",residual_id:"ROOT",dimacs,cap,arms})}
return results
}
module.exports={feedbackTrial};

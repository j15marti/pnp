// Reproduce replay: load exact pinned compile/gauge helper as described in report, call run(L,G,registryRecord,corpusRecord,peerCompact).
function run(L,G,reg,x,peer){
 const {sha,quotient,gauge,project,clauses,canon,up,tree,replay}=L;
 if(sha(JSON.stringify(G)+"\n")!==reg.sha256||sha(x.dimacs)!==reg.source_cnf.sha256)throw Error("source");
 const q=quotient(G),g=gauge(q.F),p=project(g.F),C=clauses(p.F);
 if(JSON.stringify(C)!==JSON.stringify(peer.chart)&&!replay(C,peer.local.map(z=>z.c??z.clause??z)).steps)throw Error("chart");
 // Exact independent replay: local exclusions from original guards and peer prefix.
 const local=peer.guards.filter(z=>z.refuted).map(z=>canon(z.h.map(l=>-l)));
 const localCheck=replay(C,local);
 const peerCheck=replay(C.concat(local),peer.peer);
 const all=C.concat(local,peer.peer),cl={visits:0},close=up(all,[],cl,1e7),standalone=tree(C,[],700000),hybrid=tree(all,[],700000),final=replay(C,local.concat(peer.peer,hybrid.proof));
 let seed=20261127,draws=0,randomWork=0,learned=[],randomCheck=0;const V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),next=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0};
 for(let i=0;i<32;i++){let a=V[next()%V.length],b=V[next()%V.length];if(a===b)continue;draws++;let h=[a*(next()&1?1:-1),b*(next()&1?1:-1)],k={visits:0};if(up(C,h,k,1e7).bad){let c=canon(h.map(l=>-l));if(!learned.some(y=>JSON.stringify(y)===JSON.stringify(c))){randomCheck+=replay(C,[c]).visits;learned.push(c)}}randomWork+=k.visits}
 // Modular tie-break only, no claims on full feedback with residues. Same initial state and exact strict defect score.
 function flip(residue){const t=Date.now(),index=new Map(V.map((v,i)=>[v,i]));let visits=0,steps=[],changed=0;
 function row(c,a){let k=0,s=0;for(const l of c){visits++;if(a[index.get(Math.abs(l))]===+(l>0)){k++;s+=l>0?1:-1}}return [k,k%3,(s%3+3)%3]}
 function score(a){let rows=C.map(c=>row(c,a));return [rows.filter(z=>z[0]===0).length,rows.filter(z=>z[0]>0&&z[2]===0).length]}
 let a=V.map(()=>0),b=V.map(()=>1);if(score(b)[0]<score(a)[0])a=b;
 let initial=score(a);
 for(let i=0;i<100;i++){let cur=score(a),best=null,first=null;for(let j=0;j<V.length;j++){a[j]^=1;let z=score(a);a[j]^=1;if(z[0]>=cur[0])continue;if(!first||z[0]<first.z[0])first={j,z};if(!best||z[0]<best.z[0]||(residue&&z[0]===best.z[0]&&z[1]<best.z[1]))best={j,z}}if(!best)break;if(best.j!==first.j)changed++;a[best.j]^=1;steps.push(V[best.j]);}return {initial,final:score(a),steps,changed,visits,ms:Date.now()-t,peakRowFields:C.length*3+V.length}}
 return {gauge:g.g,local,localCheck,peerCheck,close:{bad:close.bad,visits:cl.visits,forced:close.A.size},standalone:{nodes:standalone.nodes,visits:standalone.visits,status:standalone.status},hybrid:{nodes:hybrid.nodes,visits:hybrid.visits,status:hybrid.status,proof:hybrid.proof},final,random:{seed:20261127,draws,learned,randomWork,randomCheck},residueFlip:{table:flip(false),residue:flip(true)}};
}
module.exports=run;

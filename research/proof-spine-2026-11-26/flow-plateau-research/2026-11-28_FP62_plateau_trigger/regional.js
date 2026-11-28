function regional(F,seedOrder,width=8,cap=2000000,clip=4,maxSteps=4){
 const ctr={selection:0,rowReads:0,projection:0,check:0},tick=(k,n=1)=>{if(Object.values(ctr).reduce((a,b)=>a+b,0)+n>cap)throw Error("cap");ctr[k]+=n};
 const vs=f=>f.vs,union=(a,b)=>[...new Set([...a,...b])].sort((x,y)=>x-y),key=a=>a.join(","),idx=(s,U,w)=>s.reduce((a,v,i)=>a|(((w>>U.indexOf(v))&1)<<i),0);
 let seen=new Set(),ded=new Map(),regions=[],hist=[],stopped=false,localBound=0;
 function test(U){
  const k=key(U);if(seen.has(k))return;seen.add(k);
  let owners=[];for(let i=0;i<F.length;i++){tick("selection");if(F[i].vs.every(v=>U.includes(v)))owners.push(i)}
  let costs=[],min=Infinity;
  for(let w=0;w<2**U.length;w++){let c=0;for(const i of owners){tick("rowReads");c+=F[i].cost[idx(F[i].vs,U,w)];if(c>=clip){c=clip;break}}costs.push(c);min=Math.min(min,c)}
  let ix=regions.length;regions.push({U,owners,min});localBound=Math.max(localBound,min);
  // Project joint support on every singleton/pair. q=0 and q=2 kept separately.
  let scopes=[[]];for(let i=0;i<U.length;i++){scopes.push([U[i]]);for(let j=i+1;j<U.length;j++)scopes.push([U[i],U[j]])}
  for(const A of scopes){let val=Array(2**A.length).fill(clip);for(let w=0;w<costs.length;w++){tick("projection");let a=idx(A,U,w);val[a]=Math.min(val[a],costs[w])}
   for(let a=0;a<val.length;a++)if(val[a]>0){let id=key(A)+":"+a,old=ded.get(id);if(!old||old.bound<val[a])ded.set(id,{scope:A,word:a,bound:val[a],region:ix})}
  }
 }
 try{for(const i of seedOrder){let U=F[i].vs.slice();for(let t=0;t<maxSteps;t++){test(U);if(localBound>0)break;let best=null;for(let j=0;j<F.length;j++){tick("selection");let V=union(U,F[j].vs),over=U.length+F[j].vs.length-V.length;if(over===0||V.length===U.length||V.length>width)continue;let score=[over,-(V.length-U.length),-j];if(!best||score[0]>best.score[0]||score[0]===best.score[0]&&(score[1]>best.score[1]||score[1]===best.score[1]&&score[2]>best.score[2]))best={V,score}}if(!best)break;U=best.V}if(localBound>0)break;hist.push(i)}}catch(e){if(e.message!=="cap")throw e;stopped=true}
 // Atomic admissions only after a second implementation verifies the exact min bound on all words.
 let cert=[],failedCheck=false;
 try{for(const d of ded.values()){const r=regions[d.region];let m=Infinity;for(let w=0;w<2**r.U.length;w++){if(d.scope.some((v,j)=>((w>>r.U.indexOf(v))&1)!==((d.word>>j)&1)))continue;let A=new Map(r.U.map((v,j)=>[v,(w>>j)&1])),z=0;for(const i of r.owners){tick("check");let f=F[i],v=0;for(let j=0;j<f.vs.length;j++)v+=A.get(f.vs[j])*2**j;z+=f.cost[v]}m=Math.min(m,z)}if(m<d.bound)throw Error("false bound");cert.push(d)}}catch(e){if(e.message!=="cap")throw e;failedCheck=true}
 return {ctr,cap,stopped,failedCheck,regions,cert,admitted:cert.length,completedSeeds:hist.length,localBound:cert.filter(d=>d.scope.length===0).reduce((m,d)=>Math.max(m,d.bound),0)}
}
function feedback(C,V,init,residue){let A=new Map(V.map(v=>[v,init])),reads=0,ties=0,steps=0;let score=()=>{let bad=0,z=0;for(let c of C){let k=0,d=0;for(let l of c){reads++;let x=A.get(Math.abs(l)-1)||0,t=l>0?x:x-1;k+=t*t;d+=t}if(!k)bad++;else if((d%3+3)%3===0)z++}return [bad,z]};let q=score(),initial=q;while(steps<4*V.length){let b=q[0],best=-1,s=Infinity,plain=-1;for(let v of V){A.set(v,1-A.get(v));let a=score();A.set(v,1-A.get(v));if(a[0]<b){b=a[0];best=v;plain=v;s=a[1]}else if(a[0]===b&&b<q[0]&&residue&&a[1]<s){best=v;s=a[1]}}if(best<0)break;if(best!==plain)ties++;A.set(best,1-A.get(best));q=score();steps++}return {initial,final:q,steps,ties,reads}}
function peerReplay(F,cert,sha,ctx,entry){if(cert.chart_sha256!==ctx.chartHash||cert.map_sha256!==ctx.mapHash||cert.instance_id!==entry.instance_id)throw Error("peer map");let coeff=new Map(),checks=0,regions=[],neg=0;for(const [U,P] of cert.regional_polynomials){let own=F.map((f,i)=>f.vs.every(v=>U.includes(v))?i:-1).filter(i=>i>=0);let val=[];for(let w=0;w<2**U.length;w++){let A=new Map(U.map((v,j)=>[v,(w>>j)&1])),z=0;for(const [T,n,d] of P){if(d!==1)throw Error("noninteger");checks++;if(T.every(v=>A.get(v)))z+=n}val.push(z);let ok=own.every(i=>F[i].cost[F[i].vs.reduce((s,v,j)=>s|(A.get(v)<<j),0)]===0);if(ok&&z<0)throw Error("peer invalid")}
 for(const [T,n] of P){if(!T.every(v=>U.includes(v)))throw Error("outside");let k=T.join(",");coeff.set(k,(coeff.get(k)||0)+n)}regions.push({U,own,val})}
 if(coeff.get("")!==-1||[...coeff].some(([k,v])=>k!==""&&v!==0))throw Error("no cancellation");
 // Every single-defect support must allow total transfer -1. Exact local minima with that owner fixed to cost2.
 let eligible=F.map((f,i)=>f.cost.includes(2)?i:-1).filter(i=>i>=0),excluded=[],remaining=[],counts=0;
 for(let d of eligible){let sum=0,empty=false;for(const r of regions){let mn=Infinity;for(let w=0;w<r.val.length;w++){let ok=true;for(let i of r.own){counts++;let f=F[i],z=f.cost[f.vs.reduce((s,v,j)=>s|(((w>>r.U.indexOf(v))&1)<<j),0)];if(z!==(i===d?2:0)){ok=false;break}}if(ok)mn=Math.min(mn,r.val[w])}if(mn===Infinity){empty=true;break}sum+=mn}if(empty||sum>-1)excluded.push({owner:d,empty,lower:empty?null:sum});else remaining.push(d)}
 return {checks,counts,regions:regions.length,eligible:eligible.length,excluded,remaining,ablationWithoutParent:"No transfer inequality; no exclusions attributable to dual."};
}
module.exports={regional,feedback,peerReplay};

function audit() {
  const bit=i=>1n<<BigInt(i), par=x=>{let p=0;while(x){x&=x-1n;p^=1;}return p;}, has=(x,i)=>Number((x>>BigInt(i))&1n);
  let checks=0;const ck=(p,msg)=>{checks++;if(!p)throw Error(msg);};
  const basis=vs=>{const b=new Map();for(let v of vs){while(v){let j=v.toString(2).length-1;if(b.has(j))v^=b.get(j);else {b.set(j,v);break;}}}return [...b.values()];};
  const rank=vs=>basis(vs).length;
  function coordinates(rows) {
    let B=new Map(),R=[];
    for(let v of rows){let a=v,c=0n;while(a){const j=a.toString(2).length-1;if(B.has(j)){let [u,h]=B.get(j);a^=u;c^=h;}else{let h=bit(R.length);R.push(a);B.set(j,[a,h]);break;}}}
    const L=rows.map(v=>{let c=0n;while(v){let j=v.toString(2).length-1;let [u,h]=B.get(j);v^=u;c^=h;}return c;});
    return {R,L};
  }
  function labelsToBlocks(labels) {
    const m=new Map();labels.forEach((l,i)=>{if(!m.has(l))m.set(l,[]);m.get(l).push(i);});return [...m.values()];
  }
  function complete(M,labels) {
    let n=M.length, E=M.slice(), free=new Set(labels), piv=[];
    while(true) {
      let ij=null;
      for(let i=0;i<n&&!ij;i++)if(free.has(labels[i]))for(let j=0;j<n;j++)if(free.has(labels[j])&&labels[i]!==labels[j]&&has(E[i],j)){ij=[i,j];break;}
      if(!ij)break;
      let [i,j]=ij, row=E[i];piv.push(ij);
      for(let a=0;a<n;a++)if(has(E[a],j))E[a]^=row;
      free.delete(labels[i]);free.delete(labels[j]);
    }
    const D=E.map((row,i)=>{let v=0n;if(free.has(labels[i]))for(let j=0;j<n;j++)if(labels[j]===labels[i]&&has(row,j))v|=bit(j);return v;});
    const C=M.map((v,i)=>v^D[i]);const {R,L}=coordinates(C);
    for(let i=0;i<n;i++){let v=0n;for(let j=0;j<R.length;j++)if(has(L[i],j))v^=R[j];ck(v===C[i],"factor");}
    const blocks=labelsToBlocks(labels),h=Math.max(...blocks.map(x=>x.length));
    ck(R.length<=Math.max(0,(4*h-1)*piv.length),"rank approximation");
    const sub=piv.map(([i])=>piv.reduce((a,[_,j],l)=>a|(BigInt(has(M[i],j))<<BigInt(l)),0n));
    ck(rank(sub)===piv.length,"disjoint minor");
    return {D,R,L,piv,blocks};
  }
  const valid=(M,p,G=[],t=0n)=>M.every((v,i)=>!has(p,i)||!par(v&p))&&G.every((v,i)=>par(v&p)===has(t,i));
  function solve(M,F,G,t) {
    const {D,R,L,blocks}=F,k=R.length;
    const rows=[...R,...G];const cols=M.map((_,i)=>rows.reduce((s,v,j)=>s|(BigInt(has(v,i))<<BigInt(j)),0n));
    let modes=0,peak=0;
    for(let z=0n;z<bit(k);z++){
      modes++;
      let dp=new Map([[0n,0n]]);
      for(const B of blocks){
        const local=new Map();
        for(let w=0n;w<bit(B.length);w++){
          let p=0n,s=0n;for(let j=0;j<B.length;j++)if(has(w,j)){p|=bit(B[j]);s^=cols[B[j]];}
          if(B.every(i=>!has(p,i)||par(D[i]&p)===par(L[i]&z)))local.set(s,p);
        }
        const nd=new Map();for(const [s,p] of dp)for(const [a,q] of local){let u=s^a;if(!nd.has(u))nd.set(u,p|q);}
        dp=nd;peak=Math.max(peak,dp.size);
      }
      const target=z|(t<<BigInt(k));
      if(dp.has(target)){const p=dp.get(target);ck(valid(M,p,G,t),"bad lifted repair");return {p,modes,peak};}
    }
    return {p:null,modes,peak};
  }
  function solveDiagonal(M,F,G,t) {
    const {D,R,L}=F,k=R.length,rows=[...R,...G], n=M.length;
    const cols=M.map((_,i)=>rows.reduce((s,v,j)=>s|(BigInt(has(v,i))<<BigInt(j)),0n));
    let modes=0;
    for(let z=0n;z<bit(k);z++){
      modes++;let B=new Map();
      for(let i=0;i<n;i++)if(has(D[i],i)===par(L[i]&z)){
        let c=cols[i],p=bit(i);while(c){let j=c.toString(2).length-1;if(B.has(j)){let [v,q]=B.get(j);c^=v;p^=q;}else{B.set(j,[c,p]);break;}}
      }
      let c=z|(t<<BigInt(k)),p=0n;while(c){let j=c.toString(2).length-1;if(!B.has(j))break;let [v,q]=B.get(j);c^=v;p^=q;}
      if(!c){ck(valid(M,p,G,t),"diagonal lift");return {p,modes};}
    }return {p:null,modes};
  }
  let seed=20261125;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}const randmask=n=>{let v=0n;for(let i=0;i<n;i++)if((rnd()>>>16)&1)v|=bit(i);return v;};
  function brute(M,G,t){for(let p=0n;p<bit(M.length);p++)if(valid(M,p,G,t))return p;return null;}
  let random=0,yes=0,no=0,exactRankChecks=0,maximumRatio=0,guardChecks=0;
  for(let a=0;a<300;a++){
    let n=3+rnd()%6,M=Array.from({length:n},()=>randmask(n)),labels=Array.from({length:n},(_,i)=>Math.floor(i/(1+rnd()%3))); // arbitrary small blocks
    const diagonal=M.map((_,i)=>i),FD=complete(M,diagonal),FB=complete(M,labels);
    let min=n;
    for(let x=0n;x<bit(n);x++)min=Math.min(min,rank(M.map((v,i)=>v^(has(x,i)?bit(i):0n))));
    ck(FD.piv.length<=min&&min<=FD.R.length&&FD.R.length<=3*min,"optimal diagonal comparison");exactRankChecks++;if(min)maximumRatio=Math.max(maximumRatio,FD.R.length/min);
    for(let j=0;j<4;j++){let q=1+rnd()%3,G=Array.from({length:q},()=>randmask(n)),t=randmask(q),b=brute(M,G,t);let s=solve(M,FB,G,t),d=solveDiagonal(M,FD,G,t);ck((b===null)===(s.p===null)&&(b===null)===(d.p===null),"decision mismatch");random++;if(b===null)no++;else yes++;}
    // Certified coordinate pin probes after base guards, checked against the same unguarded source.
    const G=[randmask(n)],t=1n;for(let i=0;i<n;i++){for(let v=0;v<2;v++){let g=[...G,bit(i)],rhs=t|(BigInt(v)<<1n),b=brute(M,g,rhs),d=solveDiagonal(M,FD,g,rhs);ck((b===null)===(d.p===null),"forced probe");guardChecks++;}}
  }
  // Exact five-plane atom, direct support, legal chart, then new terminal for all outside targets.
  const P=[[15n,32n,47n],[13n,17n,28n],[14n,36n,42n],[11n,53n,62n],[10n,39n,45n]];
  let reachable=new Set([0n]);for(let U of P){let ns=new Set();for(let x of reachable)for(let y of U)ns.add(x^y);reachable=ns;}
  let es=null;function pick(i,e){if(i===P.length){es=e;return true;}for(let v of P[i])if(rank([...e,v])===e.length+1&&pick(i+1,[...e,v]))return true;return false;}pick(0,[]);ck(es!==null,"transversal");
  let fs=P.map((u,i)=>u.find(v=>v!==es[i])),sum=fs.reduce((a,b)=>a^b,0n),atomChecks=0,atomMissing=[],atomRanks=new Set();
  for(let t=0n;t<64n;t++){
    let w=t^sum,ok;
    if(rank([...es,w])===es.length)ok=true;
    else{
      let all=[...es,w],co=new Map();for(let x=0n;x<64n;x++){let v=0n;for(let j=0;j<6;j++)if(has(x,j))v^=all[j];co.set(v,x);}
      let cs=fs.map(f=>co.get(f)),M=es.map((_,i)=>cs.reduce((a,c,j)=>a|(BigInt(has(c,i)^(i===j?1:0))<<BigInt(j)),0n)),b=cs.reduce((a,c,j)=>a|(BigInt(has(c,5))<<BigInt(j)),0n);
      let F=complete(M,M.map((_,i)=>i)),r=solveDiagonal(M,F,[b],1n);ok=r.p!==null;atomRanks.add(F.R.length);
      if(ok){let y=0n,p=r.p;for(let i=0;i<5;i++){let qi=par(M[i]&p);ck(!(has(p,i)&&qi),"chart local");let a=fs[i]^(has(p,i)?fs[i]^es[i]:0n)^(qi?es[i]:0n);ck(P[i].includes(a),"chart value");y^=a;}ck(y===t,"chart lift");}
    }
    ck(ok===reachable.has(t),"atom support");atomChecks++;if(!ok)atomMissing.push(Number(t));
  }
  ck(atomMissing.length===1&&atomMissing[0]===29,"atom missing");
  // Three types of paired blocks. All type parities coincide when d=1.
  // Demand on two types is zero on every repair. A one-diagonal flip permits singleton.
  const scaling=[];
  for(let q of [2,4,8,16,32]){
    let n=6*q,labels=Array.from({length:n},(_,i)=>i>>1),type=i=>Math.floor(i/(2*q)),M=Array.from({length:n},(_,i)=>{let v=bit(i)|bit(i^1);for(let j=0;j<n;j++)if(type(j)===(type(i)+1)%3)v|=bit(j);return v;}),b=Array.from({length:n},(_,i)=>i).reduce((x,i)=>type(i)<2?x|bit(i):x,0n);
    // Recover the pairs from external twin checks, rather than hand the solver a partition.
    let twin=Array(n).fill(-1);for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(has(M[i],j)===has(M[j],i)&&Array.from({length:n},(_,k)=>k).every(k=>k===i||k===j||(has(M[i],k)===has(M[j],k)&&has(M[k],i)===has(M[k],j)))){ck(twin[i]===-1&&twin[j]===-1,"pair unique");twin[i]=j;twin[j]=i;}
    ck(twin.every((j,i)=>j===(i^1)),"pair acquisition");
    let recovered=twin.map((j,i)=>Math.min(i,j)),F=complete(M,recovered);
    let no=solve(M,F,[b],1n),N=M.slice();N[0]^=1n;let F2=complete(N,recovered),yes=solve(N,F2,[b],1n);
    ck(no.p===null&&yes.p!==null,"large pair neighbor"); // explicit diagonal-only lower bound q from disjoint minor
    let minor=Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>has(M[2*i],2*j+1)).reduce((x,v,j)=>x|(BigInt(v)<<BigInt(j)),0n));
    ck(rank(minor)===q,"large diagonal rank lower bound");
    scaling.push({n,pairs:n/2,diagonalCompletionLowerBound:q,blockPivotRank:F.piv.length,completedInteractionRank:F.R.length,neighborInteractionRank:F2.R.length,noModes:no.modes,yesModes:yes.modes,peakTable:Math.max(no.peak,yes.peak)});
  }
  // High-girth cycle: diagonal completion cannot be bounded in this chart, but independent cycle terminal works.
  const cycles=[];
  for(let n of [8,16,32,64,128]){
    let M=Array.from({length:n},(_,i)=>bit(i)|bit((i+1)%n)),F=complete(M,M.map((_,i)=>i)),all=bit(n)-1n;
    ck(valid(M,all)&&!par(all),"even cycle");let N=M.slice();N[0]^=1n;ck(valid(N,1n,[all],1n),"cycle neighbor");
    ck(F.piv.length>=Math.floor(n/2),"cycle high rank");cycles.push({n,rankLowerBound:F.piv.length,completionRank:F.R.length,originalDemand:"UNSAT by cycle propagation",diagonalFlip:"SAT witness singleton"});
  }
  return {seed:20261125,checks,randomGuardedDecisionComparisons:random,yes,no,exactMinimumDiagonalRankComparisons:exactRankChecks,maximumObservedApproximationRatio:maximumRatio,coordinatePinComparisons:guardChecks,fivePlane:{syndromes:atomChecks,missing:atomMissing,chartRanks:[...atomRanks]},scaling,cycles};
}
console.log(JSON.stringify(audit(),null,2));

function feedback(C,V,peer=[]){
 const canon=c=>[...new Set(c)].sort((a,b)=>a-b),key=c=>canon(c).join(","),cap=1000000;
 function arm(w,name){
  let start=Date.now(),events={pairs:0,resolutionTerms:0,resolutionChecks:0,flipReads:0,residueReads:0,searchReads:0,checkReads:0,closureReads:0},count=0,peak=0;
  function tick(k,n=1){if(count+n>cap)throw Error("cap");events[k]+=n;count+=n}
  let F=C.slice(),learned=[],moves=[],state=null,tree=null,nodes=0,status="UNKNOWN",why=null,forced=[],forced2=[];
  function close(A,rows,reverse,k){
   let changed=true,S=new Map();while(changed){changed=false;S=new Map();for(let i=0;i<rows.length;i++){let c=rows[reverse?rows.length-1-i:i],open=[],sat=false;for(const l of c){tick(k);let v=A.get(Math.abs(l));if(v===undefined)open.push(l);else if(v===Number(l>0)){sat=true;break}}if(sat)continue;if(!open.length)return null;if(open.length===1){let l=open[0];A.set(Math.abs(l),Number(l>0));changed=true;}else for(const l of open)S.set(Math.abs(l),(S.get(Math.abs(l))||0)+1)}peak=Math.max(peak,A.size)}
   return {A,S};
  }
  try{
   let e=close(new Map(),C,false,"closureReads"),r=close(new Map(),C,true,"closureReads");if(Boolean(e)!==Boolean(r))throw Error("early closure mismatch");forced=e?[...e.A]:[];
   if(["deductions","table","residue"].includes(name)){
    let seen=new Set(F.map(key));outer:for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){if(events.pairs>=50000||learned.length>=128)break outer;tick("pairs");for(const p of C[i]){tick("resolutionTerms",C[i].length+C[j].length);if(!C[j].includes(-p))continue;let row=canon([...C[i].filter(l=>l!==p),...C[j].filter(l=>l!==-p)]);if(row.length>w||row.some(l=>row.includes(-l))||seen.has(key(row)))continue;let a=new Set(C[i]),b=new Set(C[j]);a.delete(p);b.delete(-p);let checked=[...new Set([...a,...b])].sort((x,y)=>x-y);tick("resolutionChecks",C[i].length+C[j].length+row.length);if(key(checked)!==key(row))throw Error("resolution replay");seen.add(key(row));F.push(row);learned.push({parents:[i+1,j+1],pivot:p,c:row});if(learned.length>=128)break outer;}}
   }
   if(name==="peer"){for(const l of peer){let q=close(new Map([[Math.abs(l),Number(l<0)]]),C,true,"closureReads");if(q)throw Error("peer pin not checked");F.push([l]);learned.push({peerUnit:l})}}
   let ec=close(new Map(),F,false,"closureReads");forced2=ec?[...ec.A]:[];
   function climb(init,residue){
    const A=new Map(V.map(v=>[v,init]));for(const [v,b] of forced2)A.set(v,b);
    const blocked=new Set(forced2.map(x=>x[0])),inc=new Map(V.map(v=>[v,[]]));
    F.forEach((c,i)=>{for(const v of new Set(c.map(Math.abs)))inc.get(v)?.push(i)});
    const score=(c)=>{let k=0,d=0;for(const l of c){tick("flipReads");if(A.get(Math.abs(l))===Number(l>0)){k++;d+=l>0?1:-1}}tick("residueReads",2);return {k,d,km:k%3,dm:(d%3+3)%3}};
    let T=F.map(score),unsat=T.filter(x=>!x.k).length,z=T.filter(x=>x.k&&x.dm===0).length,trajectory=[{unsat,z}],moves=[],initial=T.slice();
    for(let step=0;step<64;step++){let best=0,bz=Infinity,choice=null,base=null;
      for(const v of V){if(blocked.has(v))continue;A.set(v,1-A.get(v));let gain=0,dz=0;for(const i of inc.get(v)){let q=score(F[i]),old=T[i];gain+=Number(!old.k)-Number(!q.k);if(residue){tick("residueReads");dz+=Number(q.k>0&&q.dm===0)-Number(old.k>0&&old.dm===0)}}A.set(v,1-A.get(v));if(gain>best){best=gain;base=v;choice=v;bz=dz}else if(gain===best&&gain>0&&residue&&dz<bz){choice=v;bz=dz}}
      if(best<=0)break;A.set(choice,1-A.get(choice));for(const i of inc.get(choice))T[i]=score(F[i]);unsat=T.filter(x=>!x.k).length;z=T.filter(x=>x.k&&x.dm===0).length;trajectory.push({unsat,z});moves.push({v:choice,ordinaryTie:base,changed:choice!==base,gain:best});
    }
    return {init,initial,final:T,moves,trajectory,assignment:[...A]};
   }
   if(["flips","table","residue","peer"].includes(name)&&ec){let f=climb(0,name==="residue"),t=climb(1,name==="residue");moves=[f,t];state=new Map((f.trajectory.at(-1).unsat<=t.trajectory.at(-1).unsat?f:t).assignment)}
   function search(A){nodes++;let q=close(A,F,false,"searchReads");if(!q)return null;if(!q.S.size)return {sat:[...q.A]};let v=[...q.S].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],b=state?.get(v)||0,child=[];for(let x of [b,1-b]){let t=search(new Map([...q.A,[v,x]]));if(t?.sat)return t;child[x]=t}return [v,child[0],child[1]]}
   tree=search(new Map());
   if(tree?.sat){let A=new Map(tree.sat);for(const c of C){let yes=false;for(const l of c){tick("checkReads");yes||=A.get(Math.abs(l))===Number(l>0)}if(!yes)throw Error("bad SAT witness")}status="SAT"}
   else {function check(A,t){let q=close(A,F,true,"checkReads");if(!q)return;if(!Array.isArray(t))throw Error("bad proof");let v=t[0];if(q.A.has(v))check(new Map(q.A),t[1+q.A.get(v)]);else for(const b of [0,1])check(new Map([...q.A,[v,b]]),t[b+1])}check(new Map(),tree);status="UNSAT"}
  }catch(e){why=String(e);if(!why.includes("cap"))throw e}
  return {w,name,status,why,forced,forced2,learned,moves,nodes,tree,events,total:count,peakAssigned:peak,storedLiteralEntries:F.reduce((s,c)=>s+c.length,0),runtimeMs:Date.now()-start};
 }
 let arms=[];for(const w of [2,4])for(const name of ["base","flips","deductions","table","residue"])arms.push(arm(w,name));if(peer.length)arms.push(arm(2,"peer"));
 return {arms,cap,variables:V,rows:C.length};
}
if(typeof module!=="undefined")module.exports={feedback};

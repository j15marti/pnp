// Pass original CNF/residual clauses, guards, and pinned T4 library (canon, key, vars, up).
module.exports=function partialHall(C,guards,L){
 const started=Date.now(), V=L.vars(C), K=c=>L.key(L.canon(c)), idx=new Map(C.map((c,i)=>[K(c),i])), sign=[...V.flatMap(v=>[v,-v])],cnt={cliqueChecks:0,packingChecks:0,matchingCalls:0,edgeVisits:0,checkPairs:0,upVisits:0,failed:0}, conflict=(a,b)=>{cnt.cliqueChecks++;return a===-b||idx.has(K([-a,-b]))};
 const R=[];let seenR=new Set;function resource(q){q=L.canon(q);let k=K(q);if(q.length>1&&!seenR.has(k)){seenR.add(k);R.push(q)}}
 for(let c of C){if(c.length===2)resource(c.map(l=>-l));if(c.length>1&&c.every((a,i)=>c.slice(i+1).every(b=>conflict(a,b))))resource(c)}
 for(let v of V)resource([v,-v]);
 for(let l of sign){let a=[l];for(let b of sign)if(!a.includes(b)&&a.every(c=>conflict(b,c)))a.push(b);resource(a)}
 function pack(rows){const o=[...rows].sort((a,b)=>a.length-b.length||K(a).localeCompare(K(b))),rev=o.slice().reverse(),out=[],seen=new Set;for(let s of [o,rev])for(let i=0;i<Math.min(s.length,12);i++){let used=new Set,a=[];for(let row of s.slice(i).concat(s.slice(0,i))){cnt.packingChecks+=row.length;if(row.some(l=>used.has(l)))continue;a.push(row);row.forEach(l=>used.add(l))}let k=a.map(K).sort().join(";");if(!seen.has(k)){seen.add(k);out.push(a)}}return out}
 // Include each recognizable positive full partition in the common JOINT chart using a deterministic bounded-size greedy scan, not its source map.
 const A=pack(C),B=pack(R); const direct=[],byKey=new Map;let same=0;for(let c of C)if(R.some(r=>K(c)===K(r)))same++;
 function verify(A,B,S,T,clause){let ss=new Set,tt=new Set;for(let a of A){if(!idx.has(K(a)))throw Error("demand");for(let l of a){if(ss.has(l))throw Error("demand overlap");ss.add(l)}}for(let b of B){for(let l of b){if(tt.has(l))throw Error("resource overlap");tt.add(l)}for(let i=0;i<b.length;i++)for(let j=i+1;j<b.length;j++){cnt.checkPairs++;if(b[i]!==-b[j]&&!idx.has(K([-b[i],-b[j]])))throw Error("resource pair")}}let dest=new Map;B.forEach((b,i)=>b.forEach(l=>dest.set(l,"r"+i)));let Tset=new Set(T),D=L.canon([...new Set(S.flatMap(i=>A[i]).filter(l=>!Tset.has(dest.get(l)||"d"+l)))]);if(S.length<=T.length||K(D)!==K(clause)||new Set(S).size!==S.length||new Set(T).size!==T.length)throw Error("bad cut");return true}
 let tests=[[],...guards,...sign.map(l=>[l])],closure=[];
 for(let H of tests){let work={n:0},u=L.up(C,H,work,100000);cnt.upVisits+=work.n;if(u.limit||u.bad){closure.push({H,upBad:u.bad,upLimit:u.limit,cuts:0});continue}let before=byKey.size,cuts=0;for(let a of A)for(let b of B){cnt.matchingCalls++;let dest=new Map;b.forEach((r,i)=>r.forEach(l=>dest.set(l,"r"+i)));let nb=a.map(r=>[...new Set(r.filter(l=>u.A.get(Math.abs(l))===undefined||u.A.get(Math.abs(l))===+(l>0)).map(l=>dest.get(l)||"d"+l))]);let M=new Map;
 function aug(i,seen){for(let j of nb[i]){cnt.edgeVisits++;if(seen.has(j))continue;seen.add(j);if(!M.has(j)||aug(M.get(j),seen)){M.set(j,i);return true}}return false}
 for(let i=0;i<a.length;i++)aug(i,new Set);
 if(M.size===a.length){cnt.failed++;continue}let S=new Set(a.map((_,i)=>i).filter(i=>![...M.values()].includes(i))),T=new Set;for(let i of S)for(let j of nb[i]){cnt.edgeVisits++;T.add(j);if(M.has(j))S.add(M.get(j))}
 let si=[...S].sort((x,y)=>x-y),ti=[...T].sort(),cl=L.canon([...new Set(si.flatMap(i=>a[i]).filter(l=>!T.has(dest.get(l)||"d"+l)))]);verify(a,b,si,ti,cl);cuts++;if(cl.length>4||cl.some(l=>cl.includes(-l))||idx.has(K(cl))||byKey.has(K(cl)))continue;
 let cert={guardUsedForDiscovery:H,A:a,B:b,S:si,T:ti,clause:cl,sourceClauseIds:a.map(q=>idx.get(K(q))+1),resourcePairIds:b.map(q=>q.flatMap((l,i)=>q.slice(i+1).map(t=>l===-t?0:idx.get(K([-l,-t]))+1)))};
 byKey.set(K(cl),cert);
 }closure.push({H,cuts,newNarrow:byKey.size-before,upBad:false})}
 // Rerun unconditional closure after every accepted independent cut; do not count a cut as a semantic contraction without a checked consumer.
 let F=C.slice(),activation=[],prev=L.up(F).A.size;for(let z of byKey.values()){F.push(z.clause);let w={n:0},q=L.up(F,[],w,100000);activation.push({clause:z.clause,prev,forced:q.A.size,bad:q.bad,visits:w.n});prev=q.A.size;if(q.bad)break}
 return{vars:V.length,rows:C.length,resources:R.length,demandPackings:A.length,resourcePackings:B.length,sameScopeExisting:same,counts:cnt,closure,certificates:[...byKey.values()],activation,ms:Date.now()-started}
};

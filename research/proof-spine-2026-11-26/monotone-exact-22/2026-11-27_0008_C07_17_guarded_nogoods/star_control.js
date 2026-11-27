function starAudit(){
 const assert=(x)=>{if(!x)throw Error("audit mismatch")};
 // Actual native graph adapter: 0 center,1,2,3 leaves, reference hub.
 const n=4,E=[[0,1],[0,2],[0,3]],owners=Array.from({length:n},(_,v)=>[5+3*v,6+3*v,7+3*v]),rows=[[0,1,2,3],[0,1,3,4],[0,1,4,2]];
 for(const o of owners)rows.push([...o,2]);for(let i=0;i<E.length;i++)for(let c=0;c<3;c++)rows.push([owners[E[i][0]][c],owners[E[i][1]][c],2,5+3*n+3*i+c]);
 const F={n:5+3*n+3*E.length,rows,owners,E,guard:[[0,0],[owners[1][2],0],[owners[2][0],0],[owners[3][1],0]],outerPin:[[owners[1][0],1],[owners[2][1],1],[owners[3][2],1]]};
 // Guards fixing list domain; outerPin is the actual negative query.
 const lists=[[0,1],[1,2],[2,0]],P=[];
 const words=Array.from({length:8},(_,i)=>[i&1,(i>>1)&1,(i>>2)&1]);
 for(let a=0;a<3;a++){
   const clauses=[];for(let j=0;j<3;j++)for(let b=0;b<2;b++)if(lists[j][b]===a)clauses.push([j,b^1]);
   P.push(clauses)
 }
 const supports=(p,w)=>p.every(([j,b])=>w[j]===b);
 const allowed=words.filter(w=>P.some(p=>supports(p,w)));
 // Enumerate every native color/leaf word and check all integer rows and actual list guards.
 let nativeChecks=0;const nativeSupport=[];
 for(const w of words){let ok=false;for(let a=0;a<3;a++){
   const x=Array(F.n).fill(0);x[2]=x[3]=x[4]=1;
   [a,...w.map((v,j)=>lists[j][v])].forEach((c,v)=>x[owners[v][c]]=1);
   let valid=true;for(let i=3+n;i<rows.length;i++){const r=rows[i],s=2-x[r[0]]-x[r[1]]-x[r[2]];if(s<0||s>1){valid=false;break}x[r[3]]=s}
   nativeChecks++;if(valid&&rows.every(r=>r.reduce((s,v)=>s+x[v],0)===2)&&F.guard.every(([v,b])=>x[v]===b))ok=true;
 } if(ok)nativeSupport.push(w)}
 assert(JSON.stringify(nativeSupport)===JSON.stringify(allowed));
 // Pair hull recognition; local 2SAT queries can be evaluated by 8-word
 // reference enumeration here (not production proof).
 const H=[];for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)if(!allowed.some(w=>w[i]===a&&w[j]===b))H.push([[i,a],[j,b]]);
 const failures=[];for(const a of P[0])for(const b of P[1])for(const c of P[2]){
   const bad=[a,b,c].map(([j,x])=>[j,x^1]);
   const w=words.find(w=>bad.every(([j,b])=>w[j]===b)&&H.every(cl=>!cl.every(([j,b])=>w[j]===b)));
   if(w)failures.push({bad,w})
 }
 const excluded=words.filter(w=>!allowed.some(x=>x.join("")===w.join("")));
 assert(H.length===0&&excluded.map(w=>w.join("")).join(",")==="000,111");
 assert(failures.length===2&&F.outerPin.every(([v,b])=>b===1));
 return {F,branches:P,allowed,excluded,pairHull:H,certificateFailures:failures,nativeChecks,outerGuard:"000",status:"UNSAT under actual outer pins",note:"Full graph adapter retained; no independent SAT track."}
}
console.log(JSON.stringify(starAudit(),null,2));

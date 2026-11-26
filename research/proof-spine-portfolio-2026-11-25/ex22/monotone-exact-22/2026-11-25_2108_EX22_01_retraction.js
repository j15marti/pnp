function retractAudit(){
 let assertions=0, pairCandidates=0, scans=0, pinProbes=0;
 function check(b){assertions++;if(!b)throw Error("assert "+assertions)}
 function mk(k,sat){
   let n=0,C=[],w=[],last=-1;const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
   for(let b=0;b<k;b++){
     let ids=[last<0?n++:last,...Array.from({length:6},()=>n++)];last=ids[3];
     let s=[1,1,1,0,0,0,0];if(b&&w[ids[0]]!==s[0])s=s.map(x=>1-x);
     ids.forEach((v,i)=>w[v]=s[i]);
     for(let j=sat?1:0;j<7;j++){let t=lines[j].map(i=>ids[i]),a=n++;C.push([...t,a]);if(sat)w[a]=2-t.reduce((sum,v)=>sum+w[v],0)}
   }
   const sourceN=n,sourceC=C.slice();let D=[];
   for(const c of C){let y=[];for(const x of c){let z=n++,p=[n++,n++,n++];y.push(z);D.push([z,...p],[x,...p]);if(sat){w[z]=w[x];p.forEach((v,i)=>w[v]=+(i<2-w[x]))}}D.push(y)}
   // Deterministic pseudorandom relabeling and row order, not available to recognizer.
   let state=125+19*k+Number(sat);function rnd(){state=(Math.imul(state,1664525)+1013904223)>>>0;return state}
   function shuffle(a){for(let j=a.length-1;j>0;j--){let i=rnd()%(j+1);[a[i],a[j]]=[a[j],a[i]]}return a}
   let perm=shuffle(Array.from({length:n},(_,i)=>i)),G=shuffle(D.map(c=>shuffle(c.map(v=>perm[v]))));let W=[];if(sat)w.forEach((v,i)=>W[perm[i]]=v);
   return {n,G,W,expected:sourceC.length,sourceN,sourceC,perm}
 }
 function acquire(n,C){
   let occ=Array.from({length:n},()=>[]);C.forEach((c,i)=>c.forEach(v=>occ[v].push(i)));
   let groups=new Map();for(let i=0;i<C.length;i++)for(let j=0;j<4;j++){let p=C[i].filter((_,k)=>k!==j).sort((a,b)=>a-b),key=p.join(",");if(!groups.has(key))groups.set(key,[]);groups.get(key).push({i,p,x:C[i][j]})}
   let rem=new Set(),priv=new Set(),P=[],par=Array.from({length:n},(_,i)=>i);
   function root(x){while(par[x]!==x){par[x]=par[par[x]];x=par[x]}return x}
   for(const L of groups.values())if(L.length===2){pairCandidates++;let [a,b]=L;if(a.x===b.x||rem.has(a.i)||rem.has(b.i)||a.p.some(v=>occ[v].length!==2||!occ[v].includes(a.i)||!occ[v].includes(b.i)))continue;
     rem.add(a.i);rem.add(b.i);a.p.forEach(v=>priv.add(v));P.push({x:a.x,y:b.x,p:a.p});par[root(b.x)]=root(a.x)
   }
   let Q=C.filter((_,i)=>!rem.has(i)).map(c=>c.map(root));let R=[...new Set(Q.flat())];return {Q,R,P,root,priv}
 }
 function close(Q,vars,guard){
   let a=new Map(vars.map(v=>[v,-1]));if(guard)a.set(guard[0],guard[1]);let change=true;
   while(change){change=false;for(const c of Q){scans++;let t=c.filter(v=>a.get(v)===1).length,u=c.filter(v=>a.get(v)<0);if(t>2||t+u.length<2)return false;if(t===2||t+u.length===2)for(const v of u){a.set(v,t===2?0:1);change=true}}}return true
 }
 // Actual local seam tables: enumerate every row of both local factors, then compare exact port projections.
 const tableA=[];for(let z=0;z<16;z++)if([0,1,2,3].reduce((s,j)=>s+((z>>j)&1),0)===2){
   let cur=[];function rec(j){if(j===4){tableA.push(cur.slice());return}for(let p=0;p<8;p++)if([0,1,2].reduce((s,i)=>s+((p>>i)&1),0)===2-((z>>j)&1)){cur.push(p);rec(j+1);cur.pop()}}rec(0)}
 check(tableA.length===486);
 const supportA=Array.from({length:4},(_,j)=>new Set(tableA.map(r=>r[j])));
 for(let d=1;d<=6;d++){let tableB=[];for(let x=0;x<2;x++){let row=[];function rec(j){if(j===d){tableB.push(row.slice());return}for(let p=0;p<8;p++)if([0,1,2].reduce((s,i)=>s+((p>>i)&1),0)===2-x){row.push(p);rec(j+1);row.pop()}}rec(0)}
 check(tableB.length===2*3**d);for(let j=0;j<4;j++)for(let l=0;l<d;l++){const s=new Set(tableB.map(r=>r[l]));check(s.size===6&&supportA[j].size===6&&[...s].every(v=>supportA[j].has(v)))}}
 let results=[];
 for(let k of [1,2,4,8,16,32,64])for(let sat of [false,true]){
   const F=mk(k,sat);const Q=acquire(F.n,F.G);check(Q.P.length===4*F.expected);check(Q.Q.length===F.expected&&Q.R.length===F.sourceN);check(Q.Q.every(c=>new Set(c).size===4));check(close(Q.Q,Q.R,null));
   // Every source constraint recovered by canonical quotient, not by knowing intended assignment.
   const canon=C=>C.map(c=>c.slice().sort((a,b)=>a-b).join()).sort().join(";");
   check(canon(Q.Q)===canon(F.sourceC.map(c=>c.map(v=>Q.root(F.perm[v])))));
   if(k<=8)for(const v of Q.R)for(let b=0;b<2;b++){pinProbes++;check(close(Q.Q,Q.R,[v,b]))}
   if(sat){let w=[];for(const v of Q.R)w[v]=F.W[v];for(const {x,y,p} of Q.P){let q=w[Q.root(x)];w[x]=w[y]=q;p.forEach((v,i)=>w[v]=+(i<2-q))}check(F.G.every(c=>c.reduce((s,v)=>s+w[v],0)===2))}
   results.push({k,sat,rawClauses:F.G.length,relays:Q.P.length,quotientClauses:Q.Q.length,quotientVariables:Q.R.length})
 }
 return {assertions,pairCandidates,scans,pinProbes,exactArows:tableA.length,exactBMaxRows:2*3**6,results}
}
console.log(JSON.stringify(retractAudit(),null,2));

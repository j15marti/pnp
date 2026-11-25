const result = (function audit(){
 const mod=x=>((x%5)+5)%5, inv=[0,1,3,2,4], D=[0,1,2,3,4], signs=[1,4];
 let checks=0, seed=20261125;const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const ck=(p,msg)=>{checks++;if(!p)throw Error(msg)};
 const C=(a,b,c)=>new Set([a,b,c]).size===3&&D.some(i=>[a,b,c].every(v=>[i,mod(i+1),mod(i+2)].includes(v)));
 const R=(a,b)=>[1,3].includes(mod(b-a));
 const M=(l,m,r)=>mod(l-m)===1&&mod(r-m)===4||mod(l-m)===4&&mod(r-m)===1;
 const tuples=(k,f)=>{let a=Array(k).fill(0);function rec(i){if(i===k){f(a.slice());return}for(const v of D){a[i]=v;rec(i+1)}}rec(0)};
 let counts={C:0,ordered:0,Q:0,P:0,R:0};
 for(const a of D)for(const b of D){counts.R+=+R(a,b);for(const c of D){let cyc=R(a,b)&&R(b,c)&&R(c,a)||R(a,c)&&R(c,b)&&R(b,a);ck(C(a,b,c)===cyc,"directed cycle");ck(C(a,b,c)===(M(a,b,c)||M(b,a,c)||M(a,c,b)),"unique center");counts.C+=+cyc;counts.ordered+=+(new Set([a,b,c]).size===3&&(R(a,b)!==R(a,c)));counts.Q+=+(R(a,b)!==R(a,c));counts.P+=+(R(a,b)&&R(a,c));}}
 let frames=0;tuples(5,a=>{let ok=D.every(i=>C(a[i],a[mod(i+1)],a[mod(i+2)]));let expected=[1,4].some(s=>D.every(i=>a[i]===mod(a[0]+s*i)));ck(ok===expected,"anchor");frames+=+ok});
 for(let p=0;p<2;p++)for(let q=0;q<2;q++){let sols=[];tuples(3,([x,y,z])=>{if(x<2&&C(1,2,y)&&C(0,1,z)&&C(4,p,y)&&C(3,q,z)&&C(x,y,z))sols.push([x,y,z])});ck(JSON.stringify(sols)===JSON.stringify([[p|q,p?0:3,q?2:4]]),"OR");ck([0,1].filter(x=>C(2,p,x)).join()==String(1-p),"NOT")}
 for(const v of D)ck([2,3,4].every(j=>D.some(h=>C(j,v,h)))===(v<2),"Boolean list");
 let gadget=0, chartGadget=0; const ext=Array.from({length:5},()=>Array.from({length:5},()=>[]));
 tuples(5,([u,v,a,b,h])=>{let yes=C(a,u,v)&&C(u,v,b)&&C(a,h,b);let guard=M(a,u,v)&&M(u,v,b)&&M(a,h,b);if(yes){gadget++;ext[u][v].push([a,b,h])}if(guard){chartGadget++;ck(yes,"guard implies C")} });
 for(const u of D)for(const v of D){let good=[1,4].includes(mod(v-u));ck((ext[u][v].length>0)===good,"adjacency projection");ck(ext[u][v].some(([a,b,h])=>M(a,u,v)&&M(u,v,b)&&M(a,h,b))===good,"center lift")}
 let pathPairs=new Set();tuples(4,([a,b,c,d])=>{if([mod(b-a),mod(c-b),mod(d-c)].every(x=>signs.includes(x)))pathPairs.add(a+","+d)});for(const a of D)for(const b of D)ck(pathPairs.has(a+","+b)===(a!==b),"length3");
 const stats={matrixJobs:0,matrixSAT:0,matrixUNSAT:0,chartJobs:0,chartSAT:0,chartUNSAT:0,rowProbes:0,rowForces:0,quotients:0,dpTransitions:0,sourceScans:0,compiledControls:[],bouquets:[]};
 const dot=(a,b)=>mod(a.reduce((s,v,i)=>s+v*b[i],0));
 function rref(rows,k){let a=rows.map(r=>r.slice()),p=0;for(let c=0;c<k;c++){let q=a.findIndex((r,i)=>i>=p&&r[c]);if(q<0)continue;[a[p],a[q]]=[a[q],a[p]];a[p]=a[p].map(x=>mod(x*inv[a[p][c]]));for(let i=0;i<a.length;i++)if(i!==p&&a[i][c]){let t=a[i][c];a[i]=a[i].map((x,j)=>mod(x-t*a[p][j]))}p++}if(a.some(r=>!r.slice(0,k).some(Boolean)&&r[k]))return null;return a.slice(0,p)}
 function sumChoices(coeff){let states=new Map([[0,[]]]);for(const a of coeff){let next=new Map();for(const [s,w] of states)for(const v of signs){let t=mod(s+a*v);if(!next.has(t))next.set(t,w.concat(v))}states=next}return states}
 function solve(input,k,cap){let ids=Array.from({length:k},(_,i)=>i),rows=input.map(r=>r.slice()),out=Array(k).fill(0),stack=[],initialRank=null,finalRank=null;let localQ=0;
  function sub(i,v){out[ids[i]]=v;rows=rows.map(r=>r.filter((_,j)=>j!==i).map((x,j)=>j===ids.length-1?mod(x-r[i]*v):x));ids.splice(i,1)}
  for(;;){rows=rref(rows,ids.length);if(rows===null)return {status:"NO",initialRank,localQ};if(initialRank===null)initialRank=rows.length;
   let force=null;
   for(const row of rows){let nz=row.slice(0,-1).map((x,i)=>[x,i]).filter(([x])=>x);for(const [a,i] of nz){let s=sumChoices(nz.filter(([,j])=>j!==i).map(([x])=>x));let ok=signs.filter(v=>s.has(mod(row[ids.length]-a*v)));stats.rowProbes++;if(!ok.length)return {status:"NO",initialRank,localQ};if(ok.length===1){force=[i,ok[0]];break}}if(force)break}
   if(force){stats.rowForces++;sub(...force);continue}
   let groups=new Map(),zero=-1;for(let j=0;j<ids.length;j++){let c=rows.map(r=>r[j]),p=c.findIndex(Boolean);if(p<0){zero=j;break}let key=c.map(x=>mod(x*inv[c[p]])).join("");if(!groups.has(key))groups.set(key,{p,js:[]});groups.get(key).js.push(j)}
   if(zero>=0){sub(zero,1);continue}
   let found=null;for(const g of groups.values()){let coeff=g.js.map(j=>rows[g.p][j]);let states=sumChoices(coeff);if(states.size===5){found={...g,states};break}}
   if(!found)break;
   let {p,js,states}=found,keep=ids.map((_,j)=>j).filter(j=>!js.includes(j)),pivot=rows[p],col=rows.map(r=>r[js[0]]);
   stack.push({group:js.map(j=>ids[j]),remaining:keep.map(j=>ids[j]),coeff:keep.map(j=>pivot[j]),target:pivot[ids.length],states});
   rows=rows.filter((_,i)=>i!==p).map((r,i)=>{let t=mod(r[js[0]]*inv[col[p]]);return keep.concat(ids.length).map(j=>mod(r[j]-t*pivot[j]))});
   ids=keep.map(j=>ids[j]);stats.quotients++;localQ++;
  }
  finalRank=rows.length;if(finalRank>cap)return {status:"UNKNOWN",initialRank,finalRank,localQ};
  let z=Array(finalRank).fill(0),states=new Map([[z.join(""),[z,[]]]]);for(let j=0;j<ids.length;j++){let next=new Map();for(const [s,w] of states.values())for(const v of signs){let t=s.map((x,i)=>mod(x+rows[i][j]*v)),key=t.join("");stats.dpTransitions++;if(!next.has(key))next.set(key,[t,w.concat(v)])}states=next}
  let target=rows.map(r=>r[ids.length]).join("");if(!states.has(target))return {status:"NO",initialRank,finalRank,localQ};states.get(target)[1].forEach((v,j)=>out[ids[j]]=v);
  for(let i=stack.length-1;i>=0;i--){let s=stack[i],t=mod(s.target-dot(s.coeff,s.remaining.map(j=>out[j])));s.states.get(t).forEach((v,j)=>out[s.group[j]]=v)}
  ck(out.every(v=>signs.includes(v))&&input.every(r=>dot(r.slice(0,k),out)===r[k]),"matrix lift");return {status:"YES",out,initialRank,finalRank,localQ};
 }
 function bruteMatrix(rows,k){for(let i=0;i<2**k;i++){let x=Array.from({length:k},(_,j)=>(i>>j&1)?1:4);if(rows.every(r=>dot(r.slice(0,k),x)===r[k]))return true}return false}
 for(let t=0;t<220;t++){let k=1+rng(9),r=1+rng(4);let rows=Array.from({length:r},()=>Array.from({length:k+1},()=>rng(5)));if(t%4===0){let x=Array.from({length:k},()=>signs[rng(2)]);rows.forEach(a=>a[k]=dot(a.slice(0,k),x))}let b=bruteMatrix(rows,k),s=solve(rows,k,4);ck(s.status===(b?"YES":"NO"),"matrix reference");stats.matrixJobs++;stats[b?"matrixSAT":"matrixUNSAT"]++}
 function gac(n,cs,guard){let dom=Array.from({length:n},()=>D.slice()),change=true;while(change){change=false;for(const c of cs){stats.sourceScans++;for(let j=0;j<3;j++){let v=c[j],next=dom[v].filter(x=>dom[c[(j+1)%3]].some(y=>dom[c[(j+2)%3]].some(z=>{let a=[];a[j]=x;a[(j+1)%3]=y;a[(j+2)%3]=z;return (guard?M:C)(...a)})));if(next.length!==dom[v].length){dom[v]=next;change=true}if(!next.length)return false}}}return true}
 function chart(n,cs,cap){if(!gac(n,cs,false)||!gac(n,cs,true))return {status:"NO"};let k=cs.length,adj=Array.from({length:n},()=>[]),edges=[];cs.forEach(([l,m,r],i)=>{for(const [v,s] of [[l,1],[r,4]]){edges.push([m,v,i,s]);adj[m].push([v,i,s]);adj[v].push([m,i,mod(-s)])}});let L=Array(n).fill(null);for(let root=0;root<n;root++)if(L[root]===null){L[root]=Array(k).fill(0);let q=[root];for(let h=0;h<q.length;h++){let u=q[h];for(const [v,i,s] of adj[u])if(L[v]===null){L[v]=L[u].slice();L[v][i]=mod(L[v][i]+s);q.push(v)}}}let rows=edges.map(([u,v,i,s])=>L[v].map((x,j)=>mod(x-L[u][j]-(i===j?s:0))).concat(0));let ans=solve(rows,k,cap);if(ans.status==="YES"){let x=L.map(a=>dot(a,ans.out));ck(cs.every(c=>M(...c.map(v=>x[v]))&&C(...c.map(v=>x[v]))),"chart lift");ans.x=x;ck(gac(n,cs,true),"post lift GAC")}return ans}
 function bruteChart(n,cs){let a=Array(n).fill(0);function rec(i){if(i===n)return cs.every(c=>M(...c.map(v=>a[v])));for(const v of D){a[i]=v;if(rec(i+1))return true}return false}return rec(1)}
 for(let t=0;t<130;t++){let n=3+rng(4),k=1+rng(8),cs=[];for(let i=0;i<k;i++){let c=[];while(c.length<3){let v=rng(n);if(!c.includes(v))c.push(v)}cs.push(c)}let b=bruteChart(n,cs),s=chart(n,cs,8);ck(s.status===(b?"YES":"NO"),"chart reference");stats.chartJobs++;stats[b?"chartSAT":"chartUNSAT"]++}
 function graphComplete(n){let e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)e.push([i,j]);return e}
 function color5(n,e){let x=Array(n).fill(0);function rec(i){if(i===n)return x.slice();for(let v=0;v<5;v++){x[i]=v;if(e.every(([a,b])=>a>i||b>i||x[a]!==x[b])){let z=rec(i+1);if(z)return z}}return null}return rec(0)}
 function compile(n,e,x){let nn=n,cs=[],word=x?x.slice():null;for(const [u,v] of e){let p=nn++,q=nn++;if(word){let found=false;for(const a of D)for(const b of D)if(!found&&[mod(a-word[u]),mod(b-a),mod(word[v]-b)].every(t=>signs.includes(t))){word[p]=a;word[q]=b;found=true}ck(found,"path lift")}
 for(const [s,t] of [[u,p],[p,q],[q,v]]){let a=nn++,b=nn++,h=nn++;cs.push([a,s,t],[s,t,b],[a,h,b]);if(word){let l=ext[word[s]][word[t]].find(([a,b,h])=>M(a,word[s],word[t])&&M(word[s],word[t],b)&&M(a,h,b));ck(!!l,"adj lift");[word[a],word[b],word[h]]=l}}}if(word)ck(cs.every(c=>M(...c.map(v=>word[v]))&&C(...c.map(v=>word[v]))),"compiled witness");return {nn,cs,word}}
 for(const [n,e] of [[5,graphComplete(5)],[6,graphComplete(6)],[6,graphComplete(6).filter(([a,b])=>a!==0||b!==1)],[7,Array.from({length:7},(_,i)=>[i,(i+1)%7])]]){let x=color5(n,e),f=compile(n,e,x);ck(gac(f.nn,f.cs,false)&&gac(f.nn,f.cs,true),"root GAC");stats.compiledControls.push({n,edges:e,sourceSAT:!!x,compiledVariables:f.nn,compiledClauses:f.cs.length,witnessLift:!!f.word})}
 for(const [k,len] of [[8,5],[24,5],[40,5],[12,3]]){let n=1,cs=[];for(let j=0;j<k;j++){let ring=[0];for(let i=1;i<len;i++)ring.push(n++);for(let i=0;i<len;i++)cs.push([ring[(i+1)%len],ring[i],n++])}let s=chart(n,cs,0);ck(s.status===(len===5?"YES":"NO"),"bouquet");stats.bouquets.push({k,len,n,clauses:cs.length,status:s.status,initialRank:s.initialRank,finalRank:s.finalRank,quotients:s.localQ})}
 return {seed:20261125,checks,counts,frames,gadget,chartGadget,...stats};
})();
console.log(JSON.stringify(result,null,2));

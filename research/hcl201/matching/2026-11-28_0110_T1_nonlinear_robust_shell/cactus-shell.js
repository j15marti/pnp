
function cactus(m,no){
 let lens=no?[m,m,m]:[m-1,m,m+1],b=lens.reduce((a,v)=>a+v,0),nv=b-2,d=b,q=b+2,N=Array.from({length:d},(_,i)=>[i,i+1,i+2]),bins=Array.from({length:q},()=>[]),C=[],owners=[],x=Array.from({length:nv},(_,i)=>3*b+i+1),edgeVars=[],cycles=[],edges=[],id=0,cur=1;
 function add(c,k){C.push(c);owners.push(k)}
 for(let n of lens){let v=[0];for(let j=1;j<n;j++)v.push(cur++);let cy=[];for(let j=0;j<n;j++){cy.push(edgeVars.length);edgeVars.push([v[j],v[(j+1)%n]])}cycles.push({v,edges:cy})}
 assert(cur===nv&&edgeVars.length===b,"cycle size");
 for(let i=0;i<d;i++){let row=[];for(let j of N[i]){let v=++id;row.push(v);bins[j].push(v);edges.push([i,j,v])}add(row,["D",i])}
 for(let j=0;j<q;j++){let a=bins[j];for(let u=0;u<a.length;u++)for(let v=u+1;v<a.length;v++)add([-a[u],-a[v]],["EX",j]);if(j<b)for(let v of a){let [s,t]=edgeVars[j];add([-x[s],-x[t],-v],["AND-BLOCK",j])}}
 for(let i=0;i<b;i++){let [s,t]=edgeVars[i];add([x[s],x[t]],["CONSUMER",i])}
 let dimacs="p cnf "+(3*b+nv)+" "+C.length+"\n"+C.map(r=>r.join(" ")+" 0").join("\n")+"\n";
 return {m,no,lens,b,nv,d,q,N,bins,C,owners,x,edges,edgeVars,cycles,dimacs}
}
function auditCactus(G){
 let C=G.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),D=Array.from({length:G.d},()=>[]),B=Array.from({length:G.q},()=>[]),S=new Set(),R=[],seen=new Set();
 for(let [i,j,v] of G.edges){assert(!S.has(v)&&j>=i&&j<=i+2,"incidence");S.add(v);D[i].push([j,v]);B[j].push(v)}
 assert(D.every((a,i)=>a.length===3&&sort(a.map(r=>r[0])).join(",")===[i,i+1,i+2].join(",")),"interval source");
 for(let cy of G.cycles){assert(cy.v[0]===0&&cy.v.length===cy.edges.length,"center");for(let i=0;i<cy.v.length;i++){let e=cy.edges[i],u=cy.v[i],v=cy.v[(i+1)%cy.v.length];assert(!seen.has(e)&&J(G.edgeVars[e])===J([u,v]),"cycle scope");seen.add(e);if(i)assert(u>0,"noncentral")}}
 assert(seen.size===G.b&&new Set(G.cycles.flatMap(c=>c.v.slice(1))).size===G.nv-1&&G.cycles.reduce((s,c)=>s+c.v.length-1,0)===G.nv-1,"disjoint interiors");
 R.push(...D.map(a=>a.map(r=>r[1])));for(let j=0;j<G.q;j++){for(let i=0;i<B[j].length;i++)for(let k=i+1;k<B[j].length;k++)R.push([-B[j][i],-B[j][k]]);if(j<G.b)for(let v of B[j]){let [s,t]=G.edgeVars[j];R.push([-G.x[s],-G.x[t],-v])}}
 for(let [s,t] of G.edgeVars)R.push([G.x[s],G.x[t]]);
 let norm=T=>T.map(r=>r.slice().sort((a,b)=>a-b).join(",")).sort().join(";");assert(norm(C)===norm(R),"CNF exact");
 return {sourceRows:C.length,incidences:G.edges.length,consumerEdges:seen.size}
}
function cactusDP(G,drop=-1){
 let cases=[],best=Infinity,zBest=null,ops=0;
 for(let f=0;f<2;f++){let sums=0,z=Array(G.nv).fill(-1);z[0]=f;let records=[];
 for(let cy of G.cycles){let n=cy.v.length,skip=cy.edges.indexOf(drop),d=[Infinity,Infinity],paths=[null,null],T=[];d[f]=0;paths[f]=[f];T.push(d.map(v=>Number.isFinite(v)?v:null));
 for(let i=0;i<n-1;i++){let a=[Infinity,Infinity],P=[null,null];for(let u=0;u<2;u++)for(let v=0;v<2;v++){ops++;if(!Number.isFinite(d[u])||(!u&&!v&&i!==skip))continue;let cost=d[u]+u*v;if(cost<a[v]){a[v]=cost;P[v]=paths[u].concat(v)}}d=a;paths=P;T.push(d.map(v=>Number.isFinite(v)?v:null))}
 let val=Infinity,w=null;for(let u=0;u<2;u++){ops++;if(Number.isFinite(d[u])&&(u||f||n-1===skip)&&d[u]+u*f<val){val=d[u]+u*f;w=paths[u]}}assert(w,"finite cycle");for(let i=0;i<n;i++)z[cy.v[i]]=w[i];sums+=val;records.push({T,val,w})}
 cases.push({f,sums,z,records});if(sums<best){best=sums;zBest=z}}
 return {best,z:zBest,cases,ops}
}
function verifyCactusDP(G,R,drop=-1){
 let checks=0;for(let r of R.cases){let sum=0;assert(r.z[0]===r.f,"anchor");for(let [k,cy] of G.cycles.entries()){let x=r.records[k],n=cy.v.length,s=cy.edges.indexOf(drop),T=x.T;assert(T[0][r.f]===0&&T[0][1-r.f]===null&&T.length===n,"init");for(let i=1;i<n;i++)for(let v=0;v<2;v++){let vs=[];for(let u=0;u<2;u++){checks++;if(T[i-1][u]!==null&&(u||v||i-1===s))vs.push(T[i-1][u]+u*v)}assert(T[i][v]===(vs.length?Math.min(...vs):null),"DP step")}
 let v=Infinity;for(let u=0;u<2;u++)if(T[n-1][u]!==null&&(u||r.f||n-1===s))v=Math.min(v,T[n-1][u]+u*r.f);assert(v===x.val,"terminal min");let t=0;for(let i=0;i<n;i++){let a=x.w[i],b=x.w[(i+1)%n];assert(a||b||i===s,"consumer");assert(r.z[cy.v[i]]===a,"joint center map");t+=a*b}assert(t===v,"witness min");sum+=v}assert(sum===r.sums,"joint sum")}
 assert(R.best===Math.min(...R.cases.map(x=>x.sums))&&R.cases.some(x=>x.sums===R.best&&J(x.z)===J(R.z)),"joint minimum");return checks
}
function cactusBlock(G,z){return new Set(G.edgeVars.map(([u,v],j)=>z[u]&&z[v]?j:-1).filter(j=>j>=0))}
function cactusWitness(G,z,drop=-1){let M=matching(G.N,cactusBlock(G,z));assert(M.ok,"lift");let W=Array(3*G.b+G.nv+1).fill(0),idx=new Map(G.edges.map(([i,j,v])=>[i+","+j,v]));for(let i=0;i<G.nv;i++)W[G.x[i]]=z[i];for(let [i,j] of M.edges){let v=idx.get(i+","+j);assert(v,"edge");W[v]=1}let checks=0;for(let [i,r] of G.C.entries()){if(G.owners[i][0]==="CONSUMER"&&G.owners[i][1]===drop)continue;assert(r.some(l=>{checks++;return W[Math.abs(l)]===Number(l>0)}),"original witness")}return {W,checks,matchVisits:M.visits}}
function cactusDense(G,cap=8192){let states=0,visits=0,checks=0,hit=null,feasible=0;for(let w=0;w<Math.min(2**G.nv,cap);w++){let z=Array.from({length:G.nv},(_,i)=>i<31?(w>>>i)&1:0),D=cactusBlock(G,z),M=matching(G.N,D);visits+=M.visits;assert(M.ok===(D.size<=2),"shell");states++;let ok=true;for(let [u,v] of G.edgeVars){checks++;if(!z[u]&&!z[v]){ok=false;break}}if(ok&&M.ok){feasible++;if(!hit)hit=z}}
 let full=states===2**G.nv;return {states,visits,checks,full,feasible,decision:hit?"SAT":full?"UNSAT":"UNKNOWN",witness:hit?cactusWitness(G,hit):null}
}
function cactusRun(){let R=[];for(let m of [5,9,17,33,65])for(let no of [true,false]){let start=Date.now(),G=cactus(m,no),src=auditCactus(G),W={visits:0},U=up(G.C,[],W),dp=cactusDP(G),checks=verifyCactusDP(G,dp),ans=dp.best<=2?"SAT":"UNSAT";assert(U.status==="OPEN"&&U.a.size===0,"initial UP must stall");assert(ans===(no?"UNSAT":"SAT"),"expected control");
 let witness=ans==="SAT"?cactusWitness(G,dp.z):null,rem=cactusDP(G,G.cycles[0].edges.at(-1)),rc=verifyCactusDP(G,rem,G.cycles[0].edges.at(-1)),rw=cactusWitness(G,rem.z,G.cycles[0].edges.at(-1));let dense=m<=9?cactusDense(G):{decision:"NOT-RUN",states:0};if(dense.full)assert(dense.decision===ans,"dense");if(dense.decision==="SAT")assert(ans==="SAT","dense witness");
 let baseline=solve(G.C,[],250000,10000),bv=baseline.s==="UNSAT"?check(G.C,baseline.t):null;if(baseline.s==="SAT"){let a=new Map(baseline.a);assert(G.C.every(c=>c.some(l=>a.get(Math.abs(l))===Number(l>0))),"baseline witness")}assert(baseline.s==="UNKNOWN"||baseline.s===ans,"baseline agreement");
 let h=sha(G.dimacs);R.push({model:"DIMACS-CNF-v1",short:"CNF-CACTUS-HALL-"+m+"-"+(no?"NO":"YES")+"@"+h.slice(0,12),instance_id:"DIMACS-CNF-v1:sha256:"+h,N:G.dimacs.length*8,guard:"EMPTY",residual:"ROOT",m,no,b:G.b,boundary:G.nv,original_ids:{variables:[1,3*G.b+G.nv],clauses:[1,G.C.length]},src,up:{status:U.status,pins:U.a.size,work:W},dp,dpChecks:checks,answer:ans,witness,removal:{edge:G.cycles[0].edges.at(-1),row:G.owners.findIndex(o=>o[0]==="CONSUMER"&&o[1]===G.cycles[0].edges.at(-1))+1,dp:rem,checks:rc,witness:rw},dense,baseline:{decision:baseline.s,W:baseline.W,proof:baseline.t??null,witness:baseline.a??null,check:bv},dimacs:G.dimacs,owners:G.owners,edges:G.edges,edgeVars:G.edgeVars,cycles:G.cycles,ms:Date.now()-start})}return R}

// Load pinned check.js and nonlinear-shell.js in scope; call cactusRun().

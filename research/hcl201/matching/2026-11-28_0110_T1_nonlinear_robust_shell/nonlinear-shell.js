
function assert(x,m){if(!x)throw Error(m)}
function replayPeer(aBytes,bBytes){
 let a=JSON.parse(aBytes),b=JSON.parse(bBytes),p=a.proof,h=b.proof,C=a.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
 assert(sha(a.dimacs)===a.instance_id.split(":").at(-1)&&a.dimacs.length*8===a.original_N_bits,"source hash");
 assert(b.instance_id===a.instance_id&&b.parents[0]==="CERT-v1:sha256:"+sha(aBytes),"peer parent");
 let D=p.demand.map(x=>x.c),B=p.bins,d=D.length,q=B.length,seen=new Set(),bin=new Map(),dem=new Map(),checks=0,exp=[];
 for(let row of D){assert(row.every(v=>v>0&&!dem.has(v)),"demand disjoint");row.forEach(v=>dem.set(v,true));exp.push(row)}
 for(let [j,row] of B.entries()){for(let v of row){assert(dem.has(v)&&!bin.has(v),"bin partition");bin.set(v,j)}for(let i=0;i<row.length;i++)for(let k=i+1;k<row.length;k++)exp.push([-row[i],-row[k]]);
 let v=p.blockers[j];if(v!==null){assert(p.boundary.includes(v)&&!seen.has(v),"injectivity");seen.add(v);for(let w of row)exp.push([-v,-w])}}
 assert(bin.size===dem.size&&seen.size===p.boundary.length&&p.boundary.every(v=>!dem.has(v)),"scope coverage");
 let norm=T=>T.map(r=>r.slice().sort((a,b)=>a-b).join(",")).sort().join(";");let con=new Set(p.consumer.map(r=>r.i));assert(norm(C.filter((_,i)=>!con.has(i)))===norm(exp),"exact region multiset");for(let r of p.consumer)assert(norm([C[r.i]])===norm([r.c])&&r.c.every(v=>p.boundary.includes(Math.abs(v))),"consumer source");
 let N=D.map(r=>sort(r.map(v=>bin.get(v))));assert(J(N)===J(h.neighbors),"adjacency");assert(h.d===d&&h.q===q&&h.delta===q-d&&h.exactShell,"shell metadata");
 assert(h.cuts.length===d&&new Set(h.cuts.map(c=>c.force)).size===d,"all force");
 for(let c of h.cuts){let t=1+d+q,inf=d+q+1,E=new Map(),bal=Array(t+1).fill(0);assert(c.force>=0&&c.force<d&&c.value===q&&c.s===0&&c.t===t,"force metadata");for(let i=0;i<d;i++){E.set("0,"+(i+1),i===c.force?inf:1);for(let j of N[i])E.set((i+1)+","+(1+d+j),inf)}for(let j=0;j<q;j++)E.set((1+d+j)+","+t,1);
 for(let e of c.arcs){let k=e.u+","+e.v;assert(E.get(k)===e.c&&Number.isInteger(e.f)&&e.f>=0&&e.f<=e.c,"flow");E.delete(k);bal[e.u]-=e.f;bal[e.v]+=e.f;checks++}assert(!E.size&&bal[0]===-q&&bal[t]===q&&bal.slice(1,t).every(v=>v===0),"conservation")}
 let masks=[];for(let w=0;w<2**p.boundary.length;w++){let blocked=new Set(p.blockers.map((v,j)=>v!==null&&((w>>p.boundary.indexOf(v))&1)?j:-1).filter(j=>j>=0));let m=matching(N,blocked);assert(m.ok===(blocked.size<=q-d),"shell exhaustive replay");let right=p.consumer.every(r=>r.c.some(l=>((w>>p.boundary.indexOf(Math.abs(l)))&1)===Number(l>0)));if(m.ok&&right)masks.push(w)}
 return {instance:a.instance_id,short:a.short_id,N:a.original_N_bits,parent:sha(aBytes),shell:sha(bBytes),d,q,threshold:q-d,arcChecks:checks,regionRows:exp.length,joint:masks}
}
function matching(N,blocked){
 let M=new Map(),visits=0;function aug(i,S){for(let j of N[i]){visits++;if(blocked.has(j)||S.has(j))continue;S.add(j);if(!M.has(j)||aug(M.get(j),S)){M.set(j,i);return true}}return false}
 let matched=0;for(let i=0;i<N.length;i++)if(aug(i,new Set()))matched++;return {ok:matched===N.length,matched,edges:[...M].map(([j,i])=>[i,j]),visits}
}
function gen(b,no){
 // Exact region: b demand rows; intervals of three resource bins; two additional bins. 
 // Each of first b bins disabled by x_i AND x_{i+1}; last bin always blocked; penultimate also blocked for NO.
 let d=b,q=b+2,N=Array.from({length:d},(_,i)=>[i,i+1,i+2]),bins=Array.from({length:q},()=>[]),C=[],owners=[],x=Array.from({length:b},(_,i)=>3*b+i+1),id=0,edges=[];
 function add(c,k){C.push(c);owners.push(k)}
 for(let i=0;i<d;i++){let row=[];for(let j of N[i]){let v=++id;row.push(v);bins[j].push(v);edges.push([i,j,v])}add(row,["D",i])}
 for(let j=0;j<q;j++){let a=bins[j];for(let u=0;u<a.length;u++)for(let v=u+1;v<a.length;v++)add([-a[u],-a[v]],["EX",j]);for(let v of a){if(j<b)add([-x[j],-x[(j+1)%b],-v],["AND-BLOCK",j]);else if(j===q-1||no)add([-v],["FIXED-BLOCK",j])}}
 for(let i=0;i<b;i++)add([x[i],x[(i+1)%b]],["CONSUMER",i]);
 let dimacs="p cnf "+(4*b)+" "+C.length+"\n"+C.map(r=>r.join(" ")+" 0").join("\n")+"\n";
 return {b,d,q,N,bins,C,owners,x,edges,dimacs,no,fixed:no?2:1}
}
function verifySource(G){
 // Independent row-set reconstruction from demand-bin incidences and declared local blocker formulas.
 let C=G.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),D=Array.from({length:G.d},()=>[]),B=Array.from({length:G.q},()=>[]),V=new Set(),R=[],checks=0;
 for(let [i,j,v] of G.edges){assert(!V.has(v)&&j>=i&&j<=i+2,"incidence");V.add(v);D[i].push(v);B[j].push(v);checks++}
 assert(D.every(a=>a.length===3)&&V.size===3*G.b,"interval incidence");
 R.push(...D);for(let j=0;j<G.q;j++){for(let i=0;i<B[j].length;i++)for(let k=i+1;k<B[j].length;k++)R.push([-B[j][i],-B[j][k]]);for(let v of B[j])if(j<G.b)R.push([-G.x[j],-G.x[(j+1)%G.b],-v]);else if(j===G.q-1||G.no)R.push([-v])}
 for(let i=0;i<G.b;i++)R.push([G.x[i],G.x[(i+1)%G.b]]);
 let norm=T=>T.map(r=>r.slice().sort((a,b)=>a-b).join(",")).sort().join(";");assert(norm(C)===norm(R),"exact CNF syntax");return {checks:checks+C.length,rows:C.length}
}
function cycleDP(b,drop=-1){
 // DP table indexed by fixed first bit and current last bit; costs count 11 edges, 00 forbidden except dropped consumer edge.
 let tables=[],best=Infinity,word=null,ops=0;
 for(let first=0;first<2;first++){let d=[Infinity,Infinity],paths=[null,null],layers=[];d[first]=0;paths[first]=[first];layers.push(d.map(v=>Number.isFinite(v)?v:null));
 for(let i=0;i<b-1;i++){let e=[Infinity,Infinity],P=[null,null];for(let u=0;u<2;u++)for(let v=0;v<2;v++){ops++;if(!Number.isFinite(d[u])||(!u&&!v&&i!==drop))continue;let w=d[u]+u*v;if(w<e[v]){e[v]=w;P[v]=paths[u].concat(v)}}d=e;paths=P;layers.push(d.map(v=>Number.isFinite(v)?v:null))}
 for(let u=0;u<2;u++){ops++;if(!Number.isFinite(d[u])||(!u&&!first&&b-1!==drop))continue;let w=d[u]+u*first;if(w<best){best=w;word=paths[u]}}tables.push(layers)}
 return {best,word,tables,ops}
}
function replayDP(b,R,drop=-1){let checks=0,best=Infinity;for(let f=0;f<2;f++){let T=R.tables[f];assert(T.length===b&&T[0][f]===0&&T[0][1-f]===null,"DP initial");for(let i=1;i<b;i++)for(let v=0;v<2;v++){let vals=[];for(let u=0;u<2;u++){checks++;if(T[i-1][u]!==null&&(u||v||i-1===drop))vals.push(T[i-1][u]+u*v)}assert(T[i][v]===(vals.length?Math.min(...vals):null),"DP recurrence")}for(let u=0;u<2;u++)if(T[b-1][u]!==null&&(u||f||b-1===drop))best=Math.min(best,T[b-1][u]+u*f)}
 assert(best===R.best&&R.word.length===b,"DP optimum");let v=0;for(let i=0;i<b;i++){let a=R.word[i],z=R.word[(i+1)%b];assert(a||z||i===drop,"word");v+=a*z}assert(v===best,"DP witness");return checks}
function blocked(G,z){let D=new Set();for(let i=0;i<G.b;i++)if(z[i]&&z[(i+1)%G.b])D.add(i);D.add(G.q-1);if(G.no)D.add(G.q-2);return D}
function witness(G,z,drop=-1){let m=matching(G.N,blocked(G,z));assert(m.ok,"matching");let word=Array(4*G.b+1).fill(0);for(let i=0;i<G.b;i++)word[G.x[i]]=z[i];for(let [i,j] of m.edges){let e=G.edges.find(e=>e[0]===i&&e[1]===j);assert(e,"lift edge");word[e[2]]=1}let checks=0;for(let [i,row] of G.C.entries()){if(G.owners[i][0]==="CONSUMER"&&G.owners[i][1]===drop)continue;assert(row.some(l=>{checks++;return word[Math.abs(l)]===Number(l>0)}),"CNF witness")}return {word,checks,visits:m.visits}}
function dense(G,cap=4096){let visits=0,consumer=0,states=0,first=null,mismatches=0,support=0;let max=G.b<=12?2**G.b:cap;
 for(let w=0;w<max;w++){let z=Array.from({length:G.b},(_,i)=>i<31?((w>>>i)&1):0);let D=blocked(G,z),m=matching(G.N,D);visits+=m.visits;states++;assert(m.ok===(D.size<=G.q-G.d),"count shell");let ok=true;for(let i=0;i<G.b;i++){consumer++;if(!z[i]&&!z[(i+1)%G.b]){ok=false;break}}if(m.ok&&ok){support++;if(!first)first=z}}
 return {states,complete:G.b<=12,matchingVisits:visits,consumerChecks:consumer,supportSeen:support,decision:first?"SAT":G.b<=12?"UNSAT":"UNKNOWN",witness:first?witness(G,first):null}
}
function runNew(){let R=[];for(let b of [3,5,9,13,21,33,65,129])for(let no of [true,false]){
 let t=Date.now(),G=gen(b,no),source=verifySource(G),upW={visits:0},upR=up(G.C,[],upW),dp=cycleDP(b),verify=replayDP(b,dp),answer=dp.best+G.fixed<=2?"SAT":"UNSAT",w=answer==="SAT"?witness(G,dp.word):null;
 // Parent removal: removing one consumer edge makes a zero-overlap alternating path possible.
 let rem=cycleDP(b,b-1),remVerify=replayDP(b,rem,b-1),remWitness=witness(G,rem.word,b-1);assert(rem.best===0,"parent-removal");
 let denseR=b<=33?dense(G):{decision:"NOT-RUN",states:0};if(denseR.complete)assert(answer===denseR.decision,"dense agreement");if(denseR.decision==="SAT")assert(answer==="SAT","dense witness");
 // Interval Hall certificate: each demand's full incident row has endpoints i and i+2; any nonempty set of k rows has >=k+2 bins (smallest row supplies 3, every later row adds larger endpoint).
 assert(G.N.every((r,i)=>J(r)===J([i,i+1,i+2])),"interval proof hypothesis");
 R.push({model:"DIMACS-CNF-v1",instance_id:"DIMACS-CNF-v1:sha256:"+sha(G.dimacs),short:"CNF-NONLINEAR-HALL-CYCLE-"+b+"-"+(no?"NO":"YES")+"@"+sha(G.dimacs).slice(0,12),N:G.dimacs.length*8,guard:"EMPTY",residual:"ROOT",b,no,rows:G.C.length,source,up:{status:upR.status,pins:[...upR.a],work:upW},dp,verify,answer,witness:w,dense:denseR,parentRemoval:{row:G.C.length,dp:rem,checks:remVerify,witness:remWitness},dimacs:G.dimacs,owners:G.owners,edges:G.edges,ms:Date.now()-t})
 }return R}

// Load pinned check.js in the same scope; call replayPeer(countBytes,shellBytes) and runNew().

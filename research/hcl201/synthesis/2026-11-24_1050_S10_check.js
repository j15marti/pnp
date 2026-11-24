// Node.js, no dependencies. Reproduces the S10 evidence.
function experiment(){
 const stats={seed:20110250,random:0,randomFull:0,randomNotFull:0,randomBaseEmpty:0,randomFrozenSwitch:0,randomClosureStagnant:0,switchWords:0,satWords:0,unsatWords:0,cutChecks:0,mincutBranches:0,flowCalls:0,closureQueries:0,closureTightenings:0,missingWordVerified:0,scales:[],maxcutControls:[]};
 let seed=stats.seed>>>0;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n} // use high bits below to avoid low-bit cycles
 function ri(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
 function ck(p,msg){if(!p)throw Error(msg)}
 function mf(n,arcs,s,t){stats.flowCalls++;let adj=Array.from({length:n},()=>[]), refs=[];
  for(const [u,v,c] of arcs){ck(u!==v&&c>=0,"arc");const a={v,c,rev:adj[v].length},z={v:u,c:0,rev:adj[u].length};adj[u].push(a);adj[v].push(z);refs.push([a,c])}
  let total=0, seen;
  while(true){let par=Array(n).fill(null),q=[s];par[s]=[-1,-1];for(let h=0;h<q.length&&par[t]===null;h++){let u=q[h];for(let i=0;i<adj[u].length;i++){let e=adj[u][i];if(e.c>0&&par[e.v]===null){par[e.v]=[u,i];q.push(e.v)}}}if(par[t]===null){seen=par.map(x=>x!==null);break}
   let d=Infinity;for(let v=t;v!==s;){let [u,i]=par[v];d=Math.min(d,adj[u][i].c);v=u}
   for(let v=t;v!==s;){let [u,i]=par[v],e=adj[u][i];e.c-=d;adj[v][e.rev].c+=d;v=u}total+=d}
  return {total,seen,flow:refs.map(([a,c])=>c-a.c)}}
 function balance(n,arcs,values){let b=Array(n).fill(0);arcs.forEach(([u,v],i)=>{b[u]-=values[i];b[v]+=values[i]});return b}
 function eq(a,b){return a.every((x,i)=>x===b[i])}
 function feas(n,arcs,b,lo=arcs.map(()=>0),hi=arcs.map(e=>e[2])){let d=b.map((x,i)=>x-balance(n,arcs,lo)[i]);if(d.reduce((a,b)=>a+b,0)!==0)return null;
  let extra=[],need=0;for(let i=0;i<n;i++){if(d[i]<0)extra.push([n,i,-d[i]]);else if(d[i]>0){extra.push([i,n+1,d[i]]);need+=d[i]}}
  const a=arcs.map(([u,v],i)=>[u,v,hi[i]-lo[i]]);if(a.some(e=>e[2]<0))return null;
  let f=mf(n+2,[...a,...extra],n,n+1);if(f.total!==need)return null;let x=lo.map((l,i)=>l+f.flow[i]);ck(eq(balance(n,arcs,x),b)&&x.every((v,i)=>lo[i]<=v&&v<=hi[i]),"flow witness");return x}
 function closure(n,C,R,b){let a=[...C,...R],lo=a.map(()=>0),hi=a.map(e=>e[2]);if(!feas(n,a,b,lo,hi))return {empty:true};
  for(let i=0;i<a.length;i++){let l=lo[i],h=hi[i];while(l<h){let mid=Math.floor((l+h)/2),H=hi.slice();H[i]=mid;stats.closureQueries++;if(feas(n,a,b,lo,H))h=mid;else l=mid+1}if(l>lo[i])stats.closureTightenings++;lo[i]=l;
   l=lo[i];h=hi[i];while(l<h){let mid=Math.ceil((l+h)/2),L=lo.slice();L[i]=mid;stats.closureQueries++;if(feas(n,a,b,L,hi))l=mid;else h=mid-1}if(l<hi[i])stats.closureTightenings++;hi[i]=l}
  const fixed=C.findIndex((_,i)=>lo[i]===hi[i]);if(fixed>=0)return {fixed,missing:lo[fixed]===0?1:0,lo,hi};
  let rl=lo.slice(C.length),rh=hi.slice(C.length),shift=balance(n,R,rl);return {R:R.map(([u,v],i)=>[u,v,rh[i]-rl[i]]),b:b.map((v,i)=>v-shift[i]),rl,lo,hi}}
 function cutVal(C,R,b,S){return R.reduce((a,[u,v,c])=>a+(!S[u]&&S[v]?c:0),0)-C.reduce((a,[u,v])=>a+(S[u]&&!S[v]?1:0),0)-b.reduce((a,x,i)=>a+(S[i]?x:0),0)}
 function signedMin(n,C,R,b){let w=Array.from({length:n},()=>Array(n).fill(0));for(let [u,v,c] of R)w[u][v]+=c;for(let [u,v] of C)w[v][u]--;
  let pairs=[],h=b.map(x=>-x),cover=new Set();for(let u=0;u<n;u++)for(let v=u+1;v<n;v++){let c=w[u][v]+w[v][u];h[u]+=w[v][u];h[v]-=w[v][u];if(c!==0)pairs.push([u,v,c]);if(c<0&&!cover.has(u)&&!cover.has(v)){cover.add(u);cover.add(v)}}
  let Z=[...cover],best=Infinity,Sbest=null,branches=0;ck(Z.length<25,"test cover cap");
  for(let mask=0;mask<2**Z.length;mask++){branches++;stats.mincutBranches++;let fix=Array(n).fill(-1);Z.forEach((v,i)=>fix[v]=Math.floor(mask/2**i)%2);let H=h.slice(),constant=0,arcs=[];
   for(let [u,v,c] of pairs){let a=fix[u],z=fix[v];if(a>=0&&z>=0)constant+=c*(1-a)*z;else if(a>=0)H[v]+=c*(1-a);else if(z>=0){constant+=c*z;H[u]-=c*z}else{ck(c>0,"cover");arcs.push([u,v,c])}}
   for(let i=0;i<n;i++){if(fix[i]>=0)constant+=H[i]*fix[i];else if(H[i]>=0)arcs.push([n,i,H[i]]);else{constant+=H[i];arcs.push([i,n+1,-H[i]])}}
   let f=mf(n+2,arcs,n,n+1),S=fix.map((x,i)=>x>=0?Boolean(x):!f.seen[i]);let val=constant+f.total;ck(val===cutVal(C,R,b,S),"signed cut energy");if(val<best){best=val;Sbest=S}}
  return {best,S:Sbest,k:Z.length,branches}}
 function lift(n,C,R,b,word){let d=balance(n,C,word);return feas(n,R,b.map((v,i)=>v-d[i]))}
 function verify(n,C,R,b,exhaustive){let cl=closure(n,C,R,b),m=signedMin(n,C,R,b);if(m.best<0){let word=C.map(([u,v])=>Number(m.S[u]&&!m.S[v]));ck(!lift(n,C,R,b,word),"missing word");stats.missingWordVerified++}
  if(exhaustive){let min=Infinity;for(let mask=0;mask<2**n;mask++){let S=Array.from({length:n},(_,i)=>Boolean(mask&(1<<i)));min=Math.min(min,cutVal(C,R,b,S));stats.cutChecks++}ck(min===m.best,"cut oracle");
   let sat=0;for(let mask=0;mask<2**C.length;mask++){let word=C.map((_,i)=>Number(Boolean(mask&(1<<i))));stats.switchWords++;if(lift(n,C,R,b,word)){stats.satWords++;sat++}else stats.unsatWords++}ck((sat===2**C.length)===(m.best>=0),"all-word oracle")}
  if(cl.empty){ck(m.best<0,"empty");}else if(cl.fixed!==undefined){ck(m.best<0,"fixed");let word=C.map(()=>0);word[cl.fixed]=cl.missing;ck(!lift(n,C,R,b,word),"fixed missing")}
  else{let q=signedMin(n,C,cl.R,cl.b);ck((q.best>=0)===(m.best>=0),"closure invariance");if(q.best>=0){for(let mode=0;mode<3;mode++){let word=C.map((_,i)=>mode===0?0:mode===1?1:ri(2));let x=lift(n,C,cl.R,cl.b,word);ck(x,"lift after closure");let z=x.map((v,i)=>v+cl.rl[i]);ck(eq(balance(n,[...C,...R],[...word,...z]),b)&&z.every((v,i)=>0<=v&&v<=R[i][2]),"original lift")}}}
  return {full:m.best>=0,best:m.best,k:m.k,branches:m.branches,empty:!!cl.empty,fixed:cl.fixed!==undefined,tight:cl.lo?cl.lo.some((x,i)=>x!==0||cl.hi[i]!==[...C,...R][i][2]):false}}
 function arc(n,c){let u=ri(n),v=ri(n-1);if(v>=u)v++;return [u,v,c]}
 for(let test=0;test<180;test++){let n=2+ri(5),C=Array.from({length:1+ri(6)},()=>arc(n,1)),R=Array.from({length:1+ri(12)},()=>arc(n,1+ri(3)));
  if(test%4===0)R.push(...C.map(([u,v])=>[v,u,1]));let a=[...C,...R],b=test%3===0?Array(n).fill(0):balance(n,a,a.map(e=>ri(e[2]+1)));if(test%11===0){b[0]+=3;b[1]-=3}
  let r=verify(n,C,R,b,true);stats.random++;if(r.full)stats.randomFull++;else stats.randomNotFull++;if(r.empty)stats.randomBaseEmpty++;if(r.fixed)stats.randomFrozenSwitch++;if(!r.empty&&!r.tight)stats.randomClosureStagnant++}
 function reduce(n,E,K){let s=n,t=n+1,M=E.length+1,C=E.flatMap(([u,v])=>[[u,v,1],[v,u,1]]),R=[[t,s,K]];for(let v=0;v<n;v++){R.push([s,v,M],[v,t,M])}return {n:n+2,C,R,b:Array(n+2).fill(0)}}
 for(let i=0;i<25;i++){let n=2+ri(5),E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(ri(2))E.push([u,v]);if(!E.length)E.push([0,1]);let mc=0;for(let mask=0;mask<2**n;mask++)mc=Math.max(mc,E.filter(([u,v])=>Boolean(mask&(1<<u))!==Boolean(mask&(1<<v))).length);
  for(let K of [mc-1,mc]){let p=reduce(n,E,K),r=verify(p.n,p.C,p.R,p.b,p.C.length<=10);ck(r.full===(K>=mc),"maxcut reduction");stats.maxcutControls.push({n,edges:E.length,K,mc,full:r.full})}}
 for(let r of [4,8,16,32,64]){let E=Array.from({length:r},(_,i)=>[0,i+1]);for(let K of [r-1,r]){let p=reduce(r+1,E,K),a=verify(p.n,p.C,p.R,p.b,false);ck(a.full===(K===r)&&a.k===2,"star scaling");stats.scales.push({family:"shared bottleneck",rank:p.C.length,demandRank:r,K,arcs:p.C.length+p.R.length,...a})}}
 for(let r of [8,32,64,128]){let C=Array.from({length:r},(_,i)=>[0,i+1,1]),R=C.map(([u,v])=>[v,u,1]),b=Array(r+1).fill(0),a=verify(r+1,C,R,b,false);ck(a.full&&a.k===0,"reverse scaling");stats.scales.push({family:"reverse reserve",rank:r,demandRank:r,arcs:2*r,...a})}
 return stats
}
console.log(JSON.stringify(experiment(),null,2));

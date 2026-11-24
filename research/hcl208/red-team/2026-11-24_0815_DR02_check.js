function runDR02(){
 const assert=(v,m)=>{if(!v)throw Error(m)};
 const val=(l,x)=>x[Math.abs(l)]^(l<0?1:0);
 const nae=(c,x)=>{const a=val(c[0],x);return c.some(l=>val(l,x)!==a)};
 const sat=(cs,x)=>cs.every(c=>c.some(l=>val(l,x)===1));
 const bits=(mask,n)=>Array.from({length:n+1},(_,i)=>i?((mask>>(i-1))&1):0);
 const stats={sourceCases:0,sourceSAT:0,sourceUNSAT:0,sourceAssignments:0,guardQueries:0,guardSAT:0,guardUNSAT:0,closureScans:0,rowChecks:0,forcedAssignments:0,branchNodes:0,peakDepth:0,peakLiveAssignmentSlots:0,rootForced:0,signedWitnessChecks:0,monotoneWitnessChecks:0,monotoneClausesChecked:0,graphChecks:0,maxSignedVariables:0,maxMonotoneVariables:0,splitPatterns:0,gadgetAssignments:0};
 const lines=[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function compile(n,cs){
  const a=n+1,b=n+2;let N=b;const C=[];
  const fresh=()=>++N;
  for(const [l1,l2,l3] of cs){const t=fresh(),u=fresh();C.push([-b,l1,t],[-t,l2,u],[-u,l3,a]);}
  const base=Array.from({length:N},(_,i)=>i+1).filter(v=>v!==a&&v!==b);
  for(let i=1;i<base.length;i++)C.push([base[i-1],base[i],fresh()]);
  return {N,a,b,C};
 }
 function close(H,x){
  let changed=true;
  while(changed){changed=false;for(const c of H.C){stats.closureScans++;const s=[0,0,0];let ok=0;
    for(let mask=0;mask<8;mask++){stats.rowChecks++;let t=[],good=true;for(let j=0;j<3;j++){const v=Math.abs(c[j]),bit=(mask>>j)&1;if(x[v]!==-1&&x[v]!==bit)good=false;t.push(bit^(c[j]<0?1:0));}
     if(!good||t.every(v=>v===t[0]))continue;ok++;for(let j=0;j<3;j++)s[j]|=1<<((mask>>j)&1);
    }
    if(!ok)return false;
    for(let j=0;j<3;j++){const v=Math.abs(c[j]);if(x[v]===-1&&(s[j]===1||s[j]===2)){x[v]=s[j]===1?0:1;changed=true;stats.forcedAssignments++;}}
  }}return true;
 }
 function solve(H,x,depth=1){
  stats.peakDepth=Math.max(stats.peakDepth,depth);stats.peakLiveAssignmentSlots=Math.max(stats.peakLiveAssignmentSlots,depth*(H.N+1));
  if(!close(H,x))return null;
  const v=x.findIndex((a,i)=>i>0&&a===-1);
  if(v<0){assert(H.C.every(c=>nae(c,x)),"signed terminal");return x;}
  stats.branchNodes++;
  for(const bit of [0,1]){const y=x.slice();y[v]=bit;const z=solve(H,y,depth+1);if(z)return z;}return null;
 }
 function monotone(H,x){
  let N=H.N;const C=[],gadgets=[],core=[];const y=x?x.slice():null;
  const fresh=(v)=>{N++;if(y)y[N]=v;return N};
  for(const c of H.C){const row=[];for(const l of c){
   const v=Math.abs(l),t=x?x[v]:0,o=fresh(t^(l<0?1:0));row.push(o);
   const w=l<0?fresh(t):o,p=fresh(t),vs=[v,w,p,...Array.from({length:4},()=>fresh(t^1))];
   for(const line of lines)C.push(line.map(i=>vs[i]));
   if(l<0)C.push([w,p,o]);
   gadgets.push([v,o,l<0?1:0]);
  }C.push(row);core.push(row);}
  return {N,C,y,gadgets,core,a:H.a,b:H.b};
 }
 function graphCheck(H,linear){
  const g=Array.from({length:H.N+1},()=>new Set()),seen=new Set();
  for(const c0 of H.C){const c=c0.map(Math.abs);assert(new Set(c).size===3,"distinct triple");assert(c.some(v=>v!==H.a&&v!==H.b),"all regional factors touch interior");for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const u=c[i],v=c[j],key=[u,v].sort((a,b)=>a-b).join(",");if(linear)assert(!seen.has(key),"linearity");seen.add(key);g[u].add(v);g[v].add(u);}}
  const s=Array.from({length:H.N},(_,i)=>i+1).find(v=>v!==H.a&&v!==H.b),todo=[s],vis=new Set(todo);
  for(let i=0;i<todo.length;i++)for(const v of g[todo[i]])if(v!==H.a&&v!==H.b&&!vis.has(v)){vis.add(v);todo.push(v);}
  assert(vis.size===H.N-2,"connected interior");assert(g[H.a].size&&g[H.b].size,"both ports exposed");stats.graphChecks++;
 }
 // Check the three-clause chain on all five-bit literal assignments.
 for(let mask=0;mask<32;mask++){const [p,q,r,s,a]=Array.from({length:5},(_,i)=>(mask>>i)&1);let support=false;
  for(let t=0;t<2;t++)for(let u=0;u<2;u++){const nn=(a,b,c)=>a!==b||b!==c;support||=nn(p,q,t)&&nn(t^1,r,u)&&nn(u^1,s,a);}
  assert(support===(![p,q,r,s,a].every(v=>v===p)),"chain");stats.splitPatterns++;
 }
 // Independently exhaust positive and negative monotone occurrence wire tables.
 for(const sign of [0,1]){
  const C=lines.map(c=>c.map(v=>v+1));let N=7,port=2;if(sign){port=8;N=8;C.push([2,3,8]);}
  let support=0;for(let mask=0;mask<2**N;mask++){const x=bits(mask,N);stats.gadgetAssignments++;if(C.every(c=>nae(c,x)))support|=1<<(2*x[1]+x[port]);}
  assert(support===(sign?6:9),"wire table");
 }
 const records=[];
 function test(name,n,cs){
  stats.sourceCases++;let count=0;for(let m=0;m<2**n;m++){stats.sourceAssignments++;if(sat(cs,bits(m,n)))count++;}
  stats[count?"sourceSAT":"sourceUNSAT"]++;
  const H=compile(n,cs);stats.maxSignedVariables=Math.max(stats.maxSignedVariables,H.N);graphCheck(H,false);
  const M=monotone(H,null);graphCheck(M,true);stats.maxMonotoneVariables=Math.max(stats.maxMonotoneVariables,M.N);
  const root=new Array(H.N+1).fill(-1);assert(close(H,root),"root closure");stats.rootForced+=root.slice(1).filter(v=>v!==-1).length;
  let support=0;
  for(const a of [0,1])for(const b of [0,1]){
   const x=root.slice();x[H.a]=a;x[H.b]=b;stats.guardQueries++;const z=solve(H,x);
   assert(Boolean(z)===(a===b||count>0),name+" boundary");
   if(!z){stats.guardUNSAT++;continue;}
   stats.guardSAT++;support|=1<<(2*a+b);stats.signedWitnessChecks++;
   if(a!==b){const projected=z.map(v=>v^a);assert(sat(cs,projected),name+" source lift");}
   const W=monotone(H,z);assert(W.C.every(c=>nae(c,W.y)),name+" monotone lift");stats.monotoneWitnessChecks++;stats.monotoneClausesChecked+=W.C.length;
  }
  assert(support===(count?15:9),name+" table");
  records.push({name,n,m:cs.length,count,support,signedN:H.N,monotoneN:M.N});
 }
 const cube=Array.from({length:8},(_,m)=>[1,2,3].map((v,i)=>(m>>i)&1?-v:v));
 test("cube-unsat",3,cube);for(let i=0;i<8;i++)test("cube-delete-"+i,3,cube.filter((_,j)=>j!==i));
 const fano=[[1,2,3],...lines.map(c=>c.map(v=>v+1))].flatMap(c=>[c,c.map(v=>-v)]);
 test("Fano",7,fano);for(let i=0;i<14;i++)test("Fano-owner-"+i,7,fano.filter((_,j)=>j!==i));
 let seed=3270815;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);}
 for(let j=0;j<60;j++){const n=4+rnd(3),m=4+rnd(20),cs=[];for(let i=0;i<m;i++){const vs=[];while(vs.length<3){const v=1+rnd(n);if(!vs.includes(v))vs.push(v);}cs.push(vs.map(v=>rnd(2)?v:-v));}test("random-"+j,n,cs);}
 return {seed:3270815,stats,records,discrepancies:0,scope:"signed guard DPLL exact; monotone compilation structural, local wire exhaust and SAT lifts; no raw full monotone UNSAT search, full cooperative closure or high-girth construction executed"};
}
console.log(JSON.stringify(runDR02(),null,2));

function audit(){
 const out={version:"C08-22-v1",cases:[],controls:{},counts:{checks:0,matchingEdges:0,wordTrials:0,tokenStates:0,tokenEdges:0,completionRows:0,closureVisits:0},cap:12000000};
 const rng=n=>Array.from({length:n},(_,i)=>i);
 function tick(k){out.counts[k]++;if(Object.values(out.counts).reduce((a,b)=>a+b,0)>out.cap)throw Error("finite partial counter cap")}
 function ck(x,m){tick("checks");if(!x)throw Error(m)}
 function make(L){
  let n=0,pins={},rows=[],colors=[],name=[];
  const v=s=>{name.push(s);return n++};
  const pin=(s,b)=>{let j=v(s);pins[j]=b;return j};
  const add=(row,color)=>{rows.push(row);colors.push(color)};
  let s=[pin("s0",0),pin("s1",1)],layer=[[],[]],leaf=[[],[]];
  for(let i=0;i<L;i++)for(let k=0;k<2;k++)layer[k].push(rng(3).map(j=>v(`side${k}/layer${i+1}/${j}`)));
  for(let k=0;k<2;k++)leaf[k]=rng(2).map(j=>v(`side${k}/leaf${j}`));
  let hub=v("joint-hub");
  for(let k=0;k<2;k++){
   add([s[k],layer[k][0][0],layer[k][0][1]],3);
   for(let i=0;i<L-1;i++)for(let j=0;j<3;j++)add([layer[k][i][j],...layer[k][i+1].filter((_,a)=>a!==j)],j);
   for(let j=0;j<3;j++)add([layer[k][L-1][j],leaf[k][j===2?1:0],pin(`side${k}/wrong${j}`,k^(L&1))],j);
   for(let j=0;j<2;j++)add([leaf[k][j],hub,pin(`side${k}/wrong-leaf${j}`,k^((L+1)&1))],[[2,0],[3,1]][k][j]);
  }
  return {L,n,pins,rows,colors,name,s,hub,layer,leaf};
 }
 function validate(n,rows,colors,perfect=false){
   let seen=new Set(),counts=Array.from({length:n},()=>[0,0,0,0]);
   for(let i=0;i<rows.length;i++){let r=rows[i];tick("completionRows");ck(r.length===3&&new Set(r).size===3,"three distinct variables");for(let v of r){ck(v>=0&&v<n,"range");ck(++counts[v][colors[i]]===1,"partition collision")}for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let key=[r[a],r[b]].sort((x,y)=>x-y).join(",");ck(!seen.has(key),"not linear");seen.add(key)}}
   if(perfect)ck(counts.every(z=>z.every(c=>c===1)),"not exact four");return counts;
 }
 function complete(a){
   let counts=validate(a.n,a.rows,a.colors),rows=[],colors=[];
   let id=(l,j,v)=>(l*4+j)*a.n+v;
   for(let l=0;l<3;l++)for(let j=0;j<4;j++)for(let i=0;i<a.rows.length;i++){rows.push(a.rows[i].map(v=>id(l,j,v)));colors.push(a.colors[i])}
   let copied=rows.length;
   for(let v=0;v<a.n;v++)for(let p=0;p<4;p++)if(counts[v][p]===0)for(let j=0;j<4;j++){rows.push([id(0,j,v),id(1,j^p,v),id(2,j^[0,2,3,1][p],v)]);colors.push(p)}
   validate(12*a.n,rows,colors,true);
   // Verify section as symbolic source and sign map on every copied/filler owner.
   for(let i=0;i<rows.length;i++){
    let z=rows[i].map(v=>[v%a.n,Number(Math.floor(v/(4*a.n))!==0)]);
    if(i<copied){ck(z.every((x,j)=>x[0]===a.rows[i%a.rows.length][j]&&x[1]===z[0][1]),"copied owner section")}
    else{ck(z.every(x=>x[0]===z[0][0])&&new Set(z.map(x=>x[1])).size===2,"filler section")}
   }
   return {n:12*a.n,rows,colors,pins:a.pins,encodedJSONBytes:JSON.stringify({n:12*a.n,rows,colors,pins:a.pins}).length};
 }
 const ispin=(a,v)=>Object.hasOwn(a.pins,v);
 function maximum(scopes){
   let M=new Map();
   function aug(i,seen){for(let v of scopes[i]){tick("matchingEdges");if(seen.has(v))continue;seen.add(v);if(!M.has(v)||aug(M.get(v),seen)){M.set(v,i);return true}}return false}
   for(let i=0;i<scopes.length;i++)aug(i,new Set());return M;
 }
 function freeScopes(a){return a.rows.map(r=>r.filter(v=>!ispin(a,v)))}
 function cnf(a){let c=[];for(let r of a.rows){let p=r.filter(v=>ispin(a,v)).map(v=>a.pins[v]),q=r.filter(v=>!ispin(a,v));if(new Set(p).size===2)continue;if(p.length)c.push(q.map(v=>[v,1^p[0]]));else for(let b of [0,1])c.push(q.map(v=>[v,b]))}return c}
 function closure(a){
   let c=cnf(a),n=a.n,adj=Array.from({length:2*n},()=>[]);
   let u=c.filter(x=>x.length<=1);
   for(let r of c)if(r.length===2){let [x,y]=r.map(([v,b])=>2*v+b);adj[x^1].push(y);adj[y^1].push(x)}
   let reach=[];for(let i=0;i<2*n;i++){let seen=new Set([i]),q=[i];for(let j=0;j<q.length;j++)for(let w of adj[q[j]]){tick("closureVisits");if(!seen.has(w)){seen.add(w);q.push(w)}}reach.push(seen)}
   let forces=0,equiv=0,bad=false;
   for(let v=0;v<n;v++)if(!ispin(a,v)){let a0=reach[2*v].has(2*v+1),a1=reach[2*v+1].has(2*v);if(a0||a1)forces++;if(a0&&a1)bad=true;for(let w=v+1;w<n;w++)if(!ispin(a,w))for(let p of [0,1])if(reach[2*v].has(2*w+p)&&reach[2*w+p].has(2*v))equiv++}
   return {units:u.length,binaryClauses:c.filter(x=>x.length===2).length,binaryForced:forces,binaryEquivalences:equiv,binaryContradiction:bad};
 }
 function greedy(a){
   // Paid matching candidate on actual input IDs, prefer owners without fixed pins.
   let M=new Map(),ids=rng(a.rows.length).sort((i,j)=>a.rows[i].filter(v=>ispin(a,v)).length-a.rows[j].filter(v=>ispin(a,v)).length||i-j);
   for(let i of ids){let v=a.rows[i].filter(v=>!ispin(a,v)).sort((x,y)=>x-y)[0];if(v!==undefined&&!M.has(v))M.set(v,i)}return M;
 }
 function graph(a,M){
   let free=rng(a.n).filter(v=>!ispin(a,v)),arc=new Map(),incoming=new Map(free.map(v=>[v,0]));
   for(let [v,i] of M){ck(a.rows[i].includes(v)&&!ispin(a,v),"bad representative");let z=a.rows[i].filter(w=>w!==v).map(w=>[w,1]);arc.set(v,z);for(let [w] of z)if(!ispin(a,w))incoming.set(w,incoming.get(w)+1)}
   ck(new Set(M.values()).size===M.size,"matching rows duplicate");
   let q=free.filter(v=>incoming.get(v)===0),order=[];
   while(q.length){q.sort((a,b)=>b-a);let v=q.pop();order.push(v);for(let [w] of arc.get(v)??[])if(!ispin(a,w)){incoming.set(w,incoming.get(w)-1);if(incoming.get(w)===0)q.push(w)}}
   return {free,arc,order,acyclic:order.length===free.length,unmatched:rng(a.rows.length).filter(i=>!new Set(M.values()).has(i))};
 }
 function tokens(a,M){
   let g=graph(a,M);if(!g.acyclic)return {status:"UNKNOWN-CYCLIC"};
   let pos=new Map(g.order.map((v,i)=>[v,i])),memo=new Map(),calls=0,conflicts=0,wrongPins=0,merges=0,init=0,seedVars=new Set(),edgeCount=0,maxTokens=0;
   function add(state,v,b){
    if(ispin(a,v)){if(a.pins[v]!==b){wrongPins++;return null}return state}
    let next=new Map(state);
    if(next.has(v)){if(next.get(v)!==b){conflicts++;return null}merges++;return next}
    next.set(v,b);return next;
   }
   function solve(state){
    calls++;if(state.size===0)return true;
    maxTokens=Math.max(maxTokens,state.size);
    let key=[...state].sort((x,y)=>pos.get(x[0])-pos.get(y[0])),str=key.map(x=>x.join(":")).join(",");
    if(memo.has(str))return memo.get(str);tick("tokenStates");
    let [v,b]=key[0],rest=new Map(state);rest.delete(v);
    let arcs=g.arc.get(v),ans=false;
    if(!arcs)ans=solve(rest);
    else for(let [w,p] of arcs){tick("tokenEdges");edgeCount++;let st=add(rest,w,b^p);if(st!==null&&solve(st)){ans=true;break}}
    memo.set(str,ans);return ans;
   }
   // Pick pivot preferably pinned; each NAE row is OR of two differing pairs.
   function start(j,state){
    if(j===g.unmatched.length){init++;for(let v of state.keys())seedVars.add(v);return solve(state)}
    let row=a.rows[g.unmatched[j]],v=row.find(v=>ispin(a,v))??row[0],other=row.filter(w=>w!==v);
    for(let w of other)for(let b of ispin(a,v)?[a.pins[v]]:[0,1]){
     let st=add(state,v,b);if(st!==null)st=add(st,w,b^1);if(st!==null&&start(j+1,st))return true;
    }
    return false;
   }
   let sat=start(0,new Map());
   // Bound width uses union of *all* unmatched row free endpoints, not just reached seeds.
   let allSeeds=new Set(g.unmatched.flatMap(i=>a.rows[i].filter(v=>!ispin(a,v))));
   let width=0;
   for(let p=-1;p<g.order.length;p++){
    let f=new Set([...allSeeds].filter(v=>pos.get(v)>p));
    for(let [v,z] of g.arc)if(pos.get(v)<=p)for(let [w] of z)if(!ispin(a,w)&&pos.get(w)>p)f.add(w);
    width=Math.max(width,f.size);
   }
   return {status:sat?"SAT":"UNSAT",states:memo.size,calls,conflicts,wrongPins,merges,init,maxTokens,edgeCount,width,matching:[...M],order:g.order,unmatched:g.unmatched};
 }
 function exact(a){
   let free=rng(a.n).filter(v=>!ispin(a,v));if(free.length>18)return null;
   let count=0,bit=new Array(a.n);for(let [v,b] of Object.entries(a.pins))bit[+v]=b;
   for(let w=0;w<(1<<free.length);w++){tick("wordTrials");free.forEach((v,i)=>bit[v]=(w>>i)&1);if(a.rows.every(r=>r.some(v=>bit[v]!==bit[r[0]])))count++}
   return count;
 }
 // Independent constructive propagation: each pinned source demands a route, wrong terminals excluded.
 function route(a,k){
  let current=[a.s[k]],parity=k,ways=new Map([[a.s[k],1n]]),step=0,trace=[];
  let rowsByRep=new Map(a.rows.map((r,i)=>[r[0],i]));
  while(current.length&&current[0]!==a.hub){
   let next=new Set(),nw=new Map();
   for(let v of current){let r=a.rows[rowsByRep.get(v)];ck(r!==undefined,"missing source route owner");for(let w of r.slice(1)){
     let b=parity^1;if(ispin(a,w)){ck(a.pins[w]!==b,"wrong escape actually legal");continue}
     next.add(w);nw.set(w,(nw.get(w)??0n)+ways.get(v))
   }}
   current=[...next];ways=nw;parity^=1;step++;trace.push({step,frontier:current,bit:parity});
   ck(step<=a.L+2,"route loop");
  }
  ck(current.length===1&&current[0]===a.hub,"did not meet at shared hub");
  return {hubBit:parity,pathCount:ways.get(a.hub).toString(),trace};
 }
 for(let L of [1,2,4,8,16,32,64,128]){
  let a=make(L),native=complete(a),scopes=freeScopes(a),M=maximum(scopes),cm=maximum(cnf(a).map(r=>r.map(x=>x[0]))),cl=closure(a);
  let free=a.n-Object.keys(a.pins).length,df=a.rows.length-M.size,dc=cnf(a).length-cm.size;
  ck(free===6*L+5&&a.rows.length===6*L+6,"counts");
  ck(M.size===free&&df===1,"free deficiency");ck(dc===6*L-5,"CNF defect");
  let G=greedy(a),gg=graph(a,G);ck(a.rows.length-G.size===2&&gg.acyclic,"greedy not acyclic with d'=2");
  let maxGraph=graph(a,M),res=tokens(a,G);ck(res.status==="UNSAT","token refutation");
  let a0=route(a,0),a1=route(a,1);ck(a0.hubBit!==a1.hubBit,"hub contradiction");
  let e=exact(a);if(e!==null)ck(e===0,"exhaustive contradiction");
  if(L>=2)ck(cl.units===0&&!cl.binaryContradiction&&cl.binaryForced===0&&cl.binaryEquivalences===0,"unexpected closure at L>=2 "+JSON.stringify(cl));
  // Minimal guard-fidelity positive control: reverse the second source pin AND all wrong exits on side1.
  let control={...a,pins:{...a.pins}};for(let [v,name] of a.name.entries())if(name==="s1"||name.startsWith("side1/wrong"))control.pins[v]^=1;
  let ctr=tokens(control,G);ck(ctr.status==="SAT","guard control");
  // Direct witness when both sources have same phase and each layer alternates, every owner mixed.
  let val=v=>ispin(control,v)?control.pins[v]:v===a.hub?(a.L+2)&1:a.name[v].includes("/leaf")?(a.L+1)&1:Number(a.name[v].match(/layer(\d+)/)[1])&1;
  ck(control.rows.every(r=>r.some(v=>val(v)!==val(r[0]))),"guard control witness");
  out.cases.push({L,source:a,native,free,owners:a.rows.length,maximumMatching:[...M],maxMatchingAcyclic:maxGraph.acyclic,freeDeficiency:df,cnfDeficiency:dc,cnfRows:cnf(a).length,closure:cl,token:res,independentRoutes:[a0,a1],exactCount:e,guardControl:"SAT witness verified"});
 }
 // Hostile cyclic d=0 graph-cut control: actual Fano signed positive hypergraph; DAG lane must decline.
 let rows=[];for(let i=1;i<8;i++)for(let j=i+1;j<8;j++){let k=i^j;if(j<k)rows.push([i-1,j-1,k-1])}
 let f={n:7,pins:{},rows},M=maximum(freeScopes(f));ck(M.size===7,"Fano matching");ck(exact(f)===0,"Fano reference");ck(tokens(f,M).status==="UNKNOWN-CYCLIC","cyclic lane must decline");
 // Marginal control: each source has possible path to the free hub with its own phase, but not joint; proved on every family member.
 out.controls={fanoFreeDeficiency:0,fanoDirectCount:0,fanoTokenStatus:"UNKNOWN-CYCLIC",fanoCnfDeficiency:14-maximum(cnf(f).map(r=>r.map(x=>x[0]))).size};
 return out;
}
console.log(JSON.stringify(audit(),null,2));

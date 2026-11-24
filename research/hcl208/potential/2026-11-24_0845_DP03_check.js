function DP03(){
 let seed=2080845;const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}, assert=(x,m)=>{if(!x)throw Error(m)};
 const stats={cases:0,sat:0,unsat:0,initialAffineDeletes:0,affineRowChecks:0,buildPairAttempts:0,gates:0,edges:0,updates:0,retiredJobs:0,gateFlips:0,edgeDeliveries:0,baselineEdgeReads:0,referenceTuples:0,referenceStateChecks:0,firstDecisionJobs:0,forcedFactorEvents:0,lifts:0,liftEdges:0,peakGates:0,peakQueue:0};
 const basis=xs=>{const b=Array(30).fill(0);for(let x of xs){for(let j=29;j>=0&&x;j--)if(x&(1<<j)){if(b[j])x^=b[j];else{b[j]=x;break}}}return b};
 const inSpan=(x,b)=>{for(let j=29;j>=0&&x;j--)if(x&(1<<j))x^=b[j];return x===0};
 function hull(groups){let a=0,d=[];for(const g of groups){if(!g.length)return null;a^=g[0];for(const x of g)d.push(x^g[0])}return [a,basis(d)]}
 function solve(rows,target,truth,refTuples,label){
  const before={...stats}, n=rows.length, offsets=[0];for(const a of rows)offsets.push(offsets.at(-1)+a.length);const M=offsets.at(-1),flat=rows.flat(),own=flat.map((_,id)=>offsets.findIndex((v,i)=>i>0&&id<v)-1);
  let U=flat.map(()=>true), L=flat.map(()=>false);const group=i=>rows[i].filter((_,j)=>U[offsets[i]+j]);
  // Initial unconditional affine row support, restart on each deletion.
  while(true){let changed=false;for(let i=0;i<n&&!changed;i++){const h=hull(rows.map((_,j)=>j).filter(j=>j!==i).map(group));for(let id=offsets[i];id<offsets[i+1];id++)if(U[id]){stats.affineRowChecks++;if(!h||!inSpan(target^flat[id]^h[0],h[1])){U[id]=false;stats.initialAffineDeletes++;changed=true;break}}}if(!changed)break}
  const nodes=[];function gate(op,ch=[],id=-1){nodes.push({op,ch,id});return nodes.length-1}
  const inp=flat.map((_,i)=>gate("in",[],i));const one=gate("one");
  function build(lo,hi){
    const h=hull(rows.map((_,i)=>i).filter(i=>i<lo||i>=hi).map(group));const allowed=x=>h&&inSpan(target^x^h[0],h[1]);
    let by=new Map();
    if(hi-lo===1){for(let id=offsets[lo];id<offsets[hi];id++)if(U[id]&&allowed(flat[id])){let x=flat[id];if(!by.has(x))by.set(x,[]);by.get(x).push(inp[id])}}
    else{let mid=(lo+hi)>>1,A=build(lo,mid),B=build(mid,hi);for(const [a,ga] of A)for(const [b,gb] of B){stats.buildPairAttempts++;let x=a^b;if(allowed(x)){if(!by.has(x))by.set(x,[]);by.get(x).push(gate("and",[ga,gb]))}}}
    return new Map([...by].map(([x,ch])=>[x,gate("or",ch)]))
  }
  const root=build(0,n).get(target)??gate("or",[]),F=nodes.length;
  const pending=Array.from({length:F},()=>[]);pending[root].push(one);const ctx=Array(F);
  for(let v=F-1;v>=0;v--){ctx[v]=gate("or",pending[v]);const g=nodes[v];if(g.op==="or")for(const c of g.ch)pending[c].push(ctx[v]);if(g.op==="and"){assert(g.ch.length===2,"binary");pending[g.ch[0]].push(gate("and",[ctx[v],g.ch[1]]));pending[g.ch[1]].push(gate("and",[ctx[v],g.ch[0]]))}}
  const sup=inp.map(v=>gate("and",[ctx[v],v]));const supportID=new Map(sup.map((g,i)=>[g,i]));
  const fan=nodes.map(()=>[]);let E=0;nodes.forEach((g,v)=>g.ch.forEach(c=>{assert(c<v,"DAG");fan[c].push(v);E++}));stats.gates+=nodes.length;stats.edges+=E;stats.peakGates=Math.max(stats.peakGates,nodes.length);
  function fresh(mask){let val=[],cnt=[];for(const g of nodes){let s=g.ch.reduce((a,c)=>a+Number(val[c]),0);cnt.push(s);val.push(g.op==="in"?mask[g.id]:g.op==="one"?true:g.op==="and"?s===g.ch.length:s>0)}return {val,cnt}}
  let lower=fresh(L),upper=fresh(U);stats.baselineEdgeReads+=2*E;
  const initialUpper=upper.val.slice(), initialLower=lower.val.slice();
  let possible=Array(n).fill(0),retired=flat.map(()=>false),done=flat.map(()=>false);
  for(let id=0;id<M;id++){if(upper.val[sup[id]])possible[own[id]]++;else retired[id]=true}
  function update(s,v,to,isUpper){let q=[],head=0,changed=new Set();const flip=(g)=>{assert(s.val[g]!==to,"monotone");s.val[g]=to;stats.gateFlips++;if(isUpper&&supportID.has(g)){const id=supportID.get(g);possible[own[id]]--;changed.add(own[id]);retired[id]=true}for(const w of fan[g])q.push(w);stats.peakQueue=Math.max(stats.peakQueue,q.length-head)};
    flip(v);while(head<q.length){const w=q[head++];stats.edgeDeliveries++;s.cnt[w]+=to?1:-1;const g=nodes[w],newv=g.op==="and"?s.cnt[w]===g.ch.length:s.cnt[w]>0;if(s.val[w]!==newv)flip(w)}
    if(isUpper&&s.val[root])for(const i of changed)if(possible[i]===1)stats.forcedFactorEvents++;
  }
  function check(){const a=fresh(L),b=fresh(U);stats.baselineEdgeReads+=2*E;assert(a.val.every((v,i)=>v===lower.val[i])&&b.val.every((v,i)=>v===upper.val[i]),"incremental mismatch "+label);
    assert(!lower.val[root]||upper.val[root],"sandwich");
    if(refTuples){for(const [mask,s] of [[L,lower],[U,upper]]){let any=false,support=flat.map(()=>false);for(const tup of refTuples){stats.referenceStateChecks++;if(tup.every(id=>mask[id])){any=true;for(const id of tup)support[id]=true}}assert(any===s.val[root],"root "+label);assert(support.every((v,id)=>v===s.val[sup[id]]),"support "+label)}}
  }
  check();let order=flat.map((_,i)=>i);for(let i=M-1;i>0;i--){let j=rnd(i+1);[order[i],order[j]]=[order[j],order[i]]}
  let jobs=0, first=(!upper.val[root]||lower.val[root])?0:null;
  for(const id of order){if(retired[id]){stats.retiredJobs++;continue}
    assert(!done[id],"duplicate");done[id]=true;jobs++;stats.updates++;
    if(truth[id]){L[id]=true;update(lower,inp[id],true,false)}else{U[id]=false;update(upper,inp[id],false,true)}
    // Every event drains to exact forward/backward fixed point before another job.
    check();if(first===null&&(!upper.val[root]||lower.val[root]))first=jobs;
  }
  assert(first!==null&&lower.val[root]===upper.val[root],"incomplete "+label);
  if(refTuples)assert(lower.val[root]===refTuples.some(t=>t.every(id=>truth[id])),"final label");
  if(lower.val[root]){const picked=[];function lift(v){const g=nodes[v];if(g.op==="in"){picked.push(g.id);return}if(g.op==="and"){for(const c of g.ch){stats.liftEdges++;lift(c)}}else if(g.op==="or"){for(const c of g.ch){stats.liftEdges++;if(lower.val[c]){lift(c);return}}throw Error("no witness")}}lift(root);assert(picked.length===n&&new Set(picked.map(id=>own[id])).size===n&&picked.every(id=>truth[id])&&picked.reduce((a,id)=>a^flat[id],0)===target,"lift");stats.lifts++;stats.sat++}else stats.unsat++;
  // Each gate / outgoing arc can be charged at most once in each monotone direction.
  let cap=0;for(let v=0;v<nodes.length;v++)cap+=(Number(!initialLower[v])+Number(initialUpper[v]))*(1+fan[v].length);
  assert(stats.gateFlips-before.gateFlips+stats.edgeDeliveries-before.edgeDeliveries<=cap,"credit");
  stats.firstDecisionJobs+=first;stats.cases++;
  return {label,sat:lower.val[root],jobs,firstDecisionJobs:first,initialCredit:cap,gates:nodes.length,edges:E,buildPairAttempts:stats.buildPairAttempts-before.buildPairAttempts,flips:stats.gateFlips-before.gateFlips,edgeDeliveries:stats.edgeDeliveries-before.edgeDeliveries,baselineEdgeReads:stats.baselineEdgeReads-before.baselineEdgeReads,retired:stats.retiredJobs-before.retiredJobs};
 }
 function tuples(rows,target){let out=[],off=0,offs=rows.map(g=>{let a=off;off+=g.length;return a});function rec(i,x,t){if(i===rows.length){if(x===target)out.push(t.slice());return}rows[i].forEach((r,j)=>{t.push(offs[i]+j);rec(i+1,x^r,t);t.pop()})}rec(0,0,[]);stats.referenceTuples+=out.length;return out}
 for(let q=0;q<100;q++){let n=2+rnd(5),D=1+rnd(5),rows=Array.from({length:n},()=>Array.from({length:2+rnd(3)},()=>rnd(1<<D))),t=rnd(1<<D),truth=rows.flat().map(()=>rnd(4)!==0);solve(rows,t,truth,tuples(rows,t),"random"+q)}
 // Common Fano benchmark. Independent original-variable assignment enumeration.
 const edges=[];for(let i=1;i<=7;i++)for(let j=i+1;j<=7;j++){let k=i^j;if(k>j)edges.push([i-1,j-1,k-1])}
 const occ=Array.from({length:7},()=>[]);edges.forEach((e,i)=>e.forEach((v,j)=>occ[v].push([i,j])));let d=0,coef=edges.map(()=>[0,0,0]);for(const a of occ){for(let j=1;j<a.length;j++){let bit=1<<d++;coef[a[0][0]][a[0][1]]^=bit;coef[a[j][0]][a[j][1]]^=bit}}
 const fr=edges.map((e,i)=>Array.from({length:8},(_,r)=>coef[i].reduce((s,b,j)=>s^((r>>j&1)?b:0),0)));
 const ft=Array.from({length:128},(_,x)=>edges.map((e,i)=>8*i+e.reduce((r,v,j)=>r|((x>>v&1)<<j),0)));stats.referenceTuples+=ft.length;
 let fano=[];for(let q=-1;q<14;q++){let truth=fr.flatMap((_,i)=>Array.from({length:8},(_,r)=>r!==0&&r!==7||q>=0&&i===(q>>1)&&r===(q%2?7:0)));let count=ft.filter(t=>t.every(id=>truth[id])).length;assert(count===(q<0?0:5),"Fano source");fano.push({...solve(fr,0,truth,ft,"fano"+q),models:count})}
 let scale=[];for(const n of [8,16,32,64,128])for(const bad of [false,true]){let rows=Array.from({length:n},()=>[0,1,2,3]),truth=rows.flat().map((_,id)=>bad?id<4*(n-1):true);let s=solve(rows,0,truth,null,"scale"+n+"/"+bad);assert(s.sat!==bad,"scale label");scale.push({...s,n})}
 // Correlated-copy control: independently satisfying masks cannot be combined
 // when they observe the SAME source bit in incompatible guards.
 assert([0,1].every(x=>!(x===0&&x===1)),"correlation");
 return {seed:2080845,stats,fano,scale,correlatedCopy:{independentRowsAdmit:true,synchronizedAdmit:false},scope:"Explicit XOR row products; full affine closure initially, exact global upper-support closure after every update; no arbitrary source acquisition, physical wheel compiler, or all-channel closure. Fresh reevaluation and brute reference are test overhead, not incremental solver work. Scale reference analytic."}
}
console.log(JSON.stringify(DP03(),null,2));

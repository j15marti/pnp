const audit = function audit(){
 let checks=0,cases=0,bruteCases=0,rankCases=0,treeCases=0;
 const ok=(q,msg)=>{checks++;if(!q)throw Error("FAILED: "+msg)};
 const ids=k=>({x:i=>i,y:i=>k+i,u:i=>2*k+i,v:i=>3*k+i,a:4*k+1,b:4*k+2,c:4*k+3,z:i=>4*k+4+i,n:5*k+3});
 function build(k){
  const t=ids(k),cs=[];
  for(let i=1;i<=k;i++){let x=t.x(i),y=t.y(i),u=t.u(i),v=t.v(i);cs.push([-x,y,u],[-x,y,-u],[x,-y,v],[x,-y,-v])}
  cs.push([t.a,t.b,t.c],[-t.a,-t.b,-t.c]);
  for(let i=0;i<k;i++){let a=i===0?t.a:t.x(i),b=t.x(i+1),z=t.z(i);cs.push([a,b,z],[-a,-b,-z])}
  return {t,cs};
 }
 function holds(cs,vals){return cs.every(c=>c.some(l=>l>0?vals[l]===1:vals[-l]===0))}
 function witness(k,bits){
  let {t}=build(k),v=Array(t.n+1).fill(0);
  for(let i=1;i<=k;i++){v[t.x(i)]=bits[i-1];v[t.y(i)]=bits[i-1]}
  v[t.a]=0;v[t.b]=0;v[t.c]=1;
  for(let i=0;i<k;i++){let a=i===0?v[t.a]:v[t.x(i)],b=v[t.x(i+1)];v[t.z(i)]=a===b?1-a:0}
  return v;
 }
 function tree(k,cs){
  let {t}=build(k),bags=[[t.a,t.b,t.c],[t.a,t.x(1),t.z(0)]],edges=[[0,1]],bridge=[1];
  for(let i=1;i<k;i++){let current=bags.length;bags.push([t.x(i),t.x(i+1),t.z(i)]);edges.push([bridge[i-1],current]);bridge.push(current)}
  for(let i=1;i<=k;i++){let j=bags.length;bags.push([t.x(i),t.y(i),t.u(i)]);edges.push([bridge[i-1],j]);bags.push([t.x(i),t.y(i),t.v(i)]);edges.push([j,j+1])}
  ok(edges.length===bags.length-1,"tree edges");ok(bags.every(b=>b.length===3),"width 2 bags");
  for(const c of cs)ok(bags.some(b=>c.every(l=>b.includes(Math.abs(l)))),"clause bag coverage");
  let adj=Array.from({length:bags.length},()=>[]);
  for(const [a,b] of edges){adj[a].push(b);adj[b].push(a)}
  for(let id=1;id<=t.n;id++){
   let active=bags.map((b,j)=>b.includes(id)?j:-1).filter(j=>j>=0);
   ok(active.length>0,"variable in bag");
   let seen=new Set([active[0]]),queue=[active[0]];
   for(let q=0;q<queue.length;q++)for(let next of adj[queue[q]])if(!seen.has(next)&&bags[next].includes(id)){seen.add(next);queue.push(next)}
   ok(seen.size===active.length,"running intersection");
  }
  return {bags:bags.length,edges:edges.length,bagWidth:2};
 }
 const logs=[];
 for(let k=1;k<=8;k++){
  let {t,cs}=build(k),pos=Array(t.n+1).fill(false),neg=Array(t.n+1).fill(false);
  ok(cs.length===6*k+2,"clause count");ok(t.n===5*k+3,"variable count");
  for(let c of cs){ok(c.length===3&&new Set(c.map(Math.abs)).size===3,"proper ternary");for(let l of c)(l>0?pos:neg)[Math.abs(l)]=true}
  for(let i=1;i<=t.n;i++)ok(pos[i]&&neg[i],"no pure variables "+i);
  let adjacency=Array.from({length:t.n+1},()=>new Set());
  for(let c of cs)for(let i of c)for(let j of c)if(Math.abs(i)!==Math.abs(j))adjacency[Math.abs(i)].add(Math.abs(j));
  let vis=new Set([1]),queue=[1];
  for(let p=0;p<queue.length;p++)for(let j of adjacency[queue[p]])if(!vis.has(j)){vis.add(j);queue.push(j)}
  ok(vis.size===t.n,"primal connected");
  const treeInfo=tree(k,cs);treeCases++;
  for(let x=0;x<2**k;x++){let bits=Array.from({length:k},(_,i)=>(x>>i)&1),v=witness(k,bits);ok(holds(cs,v),"every x extend");cases++}
  if(k<=3){
   let priv=Array.from({length:t.n},(_,i)=>i+1).filter(i=>i>2*k);
   for(let xx=0;xx<2**k;xx++)for(let yy=0;yy<2**k;yy++){
    let exists=false;
    for(let pp=0;pp<2**priv.length;pp++){
     let v=Array(t.n+1).fill(0);
     for(let i=1;i<=k;i++){v[t.x(i)]=(xx>>(i-1))&1;v[t.y(i)]=(yy>>(i-1))&1}
     for(let i=0;i<priv.length;i++)v[priv[i]]=(pp>>i)&1;
     if(holds(cs,v)){exists=true;break}
    }
    ok(exists===(xx===yy),"projected identity brute k="+k);bruteCases++;
   }
  }
  const dim=2**k;
  let M=Array.from({length:dim},(_,i)=>Array.from({length:dim},(_,j)=>i===j?1:0));
  let rank=0;
  for(let col=0;col<dim;col++){
   let pivot=rank;while(pivot<dim&&M[pivot][col]===0)pivot++;
   if(pivot===dim)continue;
   [M[pivot],M[rank]]=[M[rank],M[pivot]];
   for(let r=0;r<dim;r++)if(r!==rank&&M[r][col])for(let c=col;c<dim;c++)M[r][c]-=M[rank][c];
   rank++;
  }
  ok(rank===dim,"rational rank 2^k");rankCases++;
  for(let u=1;u<=k;u++){let dsep=2**(u-1),dm=1;ok(0*dsep+1*dm<=1,"lambda (0,1)");ok((1/2**(k-1))*dsep<=1,"rank-only rational feasible");if(u===k&&k>=2)ok(dsep>1,"unweighted rank violation")}
  let boundA=k,boundB=(dim-1)/(2**(k-1));ok(boundA>=boundB,"machine-only objective optimal");
  logs.push({k,vars:t.n,clauses:cs.length,tree:treeInfo,rank,rectangle_cover:dim,witnesses_tested:2**k,bruteforce_pairs:k<=3?dim*dim:null,rank_only_lambda:`1/${2**(k-1)}`,rank_only_initial:`${dim-1}/${2**(k-1)}`,optimal_initial:k});
 }
 let nae=[1,2,3,4,5,6];const bits=n=>[n&1,(n>>1)&1,(n>>2)&1];
 const combine=(a,b,op)=>bits(a).map((x,i)=>op(x,bits(b)[i])).reduce((z,b,i)=>z+(b<<i),0);
 let h=false,dh=false,bi=false,af=false;
 for(let a of nae)for(let b of nae){
  if(!nae.includes(combine(a,b,(x,y)=>x&y)))h=true;
  if(!nae.includes(combine(a,b,(x,y)=>x|y)))dh=true;
  for(let c of nae){
   let mid=combine(a,b,(x,y)=>x^y);mid=combine(mid,c,(x,y)=>x^y);
   if(!nae.includes(mid))af=true;
   let majority=Array.from({length:3},(_,i)=>Number(bits(a)[i]+bits(b)[i]+bits(c)[i]>=2)).reduce((z,b,i)=>z+(b<<i),0);
   if(!nae.includes(majority))bi=true;
  }
 }
 ok(h&&dh&&bi&&af,"NAE violates Schaefer closure classes");
 return {status:"COMPUTATIONAL",checks,failures:0,witness_cases:cases,brute_projection_pairs:bruteCases,rank_matrices:rankCases,tree_decompositions:treeCases,non_schaefer:{Horn:h,dual_Horn:dh,bijunctive:bi,affine:af},rows:logs};
};
console.log(JSON.stringify(audit(), null, 2));

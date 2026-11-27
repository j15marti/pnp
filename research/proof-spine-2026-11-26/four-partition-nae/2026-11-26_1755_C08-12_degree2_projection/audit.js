const audit = function(){
  let seed=261126, rand=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296), checks=0;
  const assert=(x,m)=>{checks++;if(!x)throw Error(m)};
  // literal = [variable ID, sign bit]; each original owner has immutable array index.
  const nae=(ls,b)=>{let x=((b>>ls[0][0])&1)^ls[0][1];return ls.some(([v,s])=>((((b>>v)&1)^s)!==x))};
  const ag=Array.from({length:4},(_,j)=>Array.from({length:3},(_,b)=>Array.from({length:3},(_,x)=>[j===0?3*b+x:j===1?3*x+b:3*x+((j-1)*x+b)%3,0]))).flat();
  const graph=(F,W)=>{let occ=new Map(),adj=F.map(()=>[]),stubs=F.map(()=>[]);F.forEach((a,i)=>a.forEach(([v,s])=>{if(W.has(v)){if(!occ.has(v))occ.set(v,[]);occ.get(v).push([i,s])}}));for(let [v,o] of occ){assert(o.length<=2,"degree");if(o.length===1)stubs[o[0][0]].push(v);else{let [[i,s],[j,t]]=o;adj[i].push([j,v,1^s^t]);adj[j].push([i,v,1^s^t])}}return {adj,stubs,occ}};
  // A: exact signed NAE gluing by eliminating a shared tree variable.
  function merge(F,W){let {adj,occ}=graph(F,W),seen=new Set(),rels=[],certs=[];for(let r=0;r<F.length;r++)if(!seen.has(r)){let ids=[r],edges=[];seen.add(r);for(let i of ids)for(let [j,v] of adj[i])if(!seen.has(j)){seen.add(j);ids.push(j);edges.push(v)}let a=F[r].map(z=>z.slice());for(let k=1;k<ids.length;k++){let v=edges[k-1],b=F[ids[k]],s=a.find(z=>z[0]===v)[1],t=b.find(z=>z[0]===v)[1];a=a.filter(z=>z[0]!==v).concat(b.filter(z=>z[0]!==v).map(([u,h])=>[u,h^s^t^1]));}if(a.some(([v])=>W.has(v))){assert(a.length>=3,"long relation length");continue}let signs=new Map(),taut=false;for(let [v,s] of a){if(signs.has(v)&&signs.get(v)!==s)taut=true;signs.set(v,s)}if(!taut)rels.push([...signs]);certs.push(ids)}return rels}
  // B: component cycle/stub or gauge consistency; no variable elimination.
  function gauge(F,W){let {adj,stubs}=graph(F,W),seen=new Set(),rels=[],stats={trees:0,free:0,absorbed:0};for(let r=0;r<F.length;r++)if(!seen.has(r)){let ids=[r],p=new Map([[r,0]]),e=0,stub=false;seen.add(r);for(let i of ids){e+=adj[i].length;stub||=stubs[i].length>0;for(let [j,v,w] of adj[i])if(!seen.has(j)){seen.add(j);p.set(j,p.get(i)^w);ids.push(j)}}if(stub||e/2>=ids.length){stats.free++;continue}stats.trees++;let signs=new Map(),taut=false;for(let i of ids)for(let [v,s] of F[i])if(!W.has(v)){let b=p.get(i)^s;if(signs.has(v)&&signs.get(v)!==b)taut=true;signs.set(v,b)}if(taut)stats.absorbed++;else rels.push([...signs])}return {rels,stats}}
  const pop=x=>{let n=0;for(;x;x&=x-1)n++;return n};
  let regions=0,masks=0,pinChecks=0,absorbed=0;
  const seenRegions=new Set();for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)for(let k=0;k<64;k++){let ids=[];for(let b=0;b<6;b++)if(k>>b&1)ids.push((b<3?i:j)*3+b%3);let key=ids.join(",");if(seenRegions.has(key)||!ids.length)continue;seenRegions.add(key);for(let signed=0;signed<2;signed++){
    let F=ids.map(id=>ag[id].map(([v])=>[v,signed?((id*7+v*13+id*v)%5<2?1:0):0]));regions++;let models=Array.from({length:512},(_,x)=>x).filter(x=>F.every(a=>nae(a,x)));
    for(let w=0;w<512;w++){let W=new Set(Array.from({length:9},(_,i)=>i).filter(i=>w>>i&1));let a=merge(F,W),b=gauge(F,W);absorbed+=b.stats.absorbed;masks++;let z=511^w,S=new Set(models.map(x=>x&z));for(let x=z;;x=(x-1)&z){let truth=S.has(x);assert(a.every(l=>nae(l,x))===truth,"merge");assert(b.rels.every(l=>nae(l,x))===truth,"gauge");pinChecks++;if(x===0)break}}
  }}
  let pairQ=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){let F=ag.slice(3*i,3*i+3).concat(ag.slice(3*j,3*j+3)),q=9;for(let w=0;w<512;w++){let W=new Set(Array.from({length:9},(_,i)=>i).filter(i=>w>>i&1));if(!gauge(F,W).rels.length)q=Math.min(q,pop(w))}assert(q===5,"K33 packing q");pairQ.push(q)}
  // Raw connected genuine NAE4 controls. Preserve physical IDs through random bijection.
  let large=[];for(let p of [7,11,17,31,61,127]){
    let n=3*p,perm=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=Math.floor(rand()*(i+1));[perm[i],perm[j]]=[perm[j],perm[i]]}
    let F=Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>[[perm[i],0],[perm[p+(i+s)%p],0],[perm[2*p+(i+3*s)%p],0]])).flat();
    let pairs=new Set();for(let s=0;s<4;s++){let ids=F.slice(s*p,(s+1)*p).flat().map(z=>z[0]);assert(new Set(ids).size===n,"partition")}for(let a of F)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let key=[a[i][0],a[j][0]].sort((x,y)=>x-y).join(",");assert(!pairs.has(key),"linear");pairs.add(key)}
    let treeCounts=[],parityAbs=0;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){let R=F.slice(i*p,(i+1)*p).concat(F.slice(j*p,(j+1)*p));let all=new Set(Array.from({length:n},(_,i)=>i)),{adj}=graph(R,all);for(let u=0;u<2*p;u++){let S=new Set();for(let [v] of adj[u])for(let [w] of adj[v])if(w!==u){assert(!S.has(w),"four-cycle");S.add(w)}}
      let seen=new Set([0]),q=[0],W=new Set();for(let u of q)for(let [v,e] of adj[u])if(!seen.has(v)){seen.add(v);q.push(v);W.add(e)}assert(q.length===2*p,"connected");assert(W.size===2*p-1,"tree");let b=gauge(R,W);assert(!b.rels.length&&b.stats.absorbed===1,"tree gauge absorption");assert(!merge(R,W).length,"tree merge absorption");treeCounts.push(W.size);parityAbs+=b.stats.absorbed}
    // Independent GF(3) Gaussian on relabeled original clauses.
    let M=F.map(a=>{let r=new Uint8Array(n);for(let [v] of a)r[v]=1;return r}),piv=[],r=0;
    for(let c=0;c<n;c++){let k=r;while(k<M.length&&!M[k][c])k++;if(k===M.length)continue;[M[r],M[k]]=[M[k],M[r]];if(M[r][c]===2)for(let j=c;j<n;j++)M[r][j]=(2*M[r][j])%3;for(let i=r+1;i<M.length;i++)if(M[i][c]){let f=M[i][c];for(let j=c;j<n;j++)M[i][j]=(M[i][j]+6-f*M[r][j])%3}piv.push(c);r++}
    let free=Array.from({length:n},(_,i)=>i).filter(i=>!piv.includes(i));assert(free.length===2,"kernel dimension");let witness=null,tries=0;for(let a=0;a<3&&!witness;a++)for(let b=0;b<3&&!witness;b++){tries++;let x=new Uint8Array(n);x[free[0]]=a;x[free[1]]=b;for(let i=r-1;i>=0;i--){let c=piv[i],v=0;for(let j=c+1;j<n;j++)v=(v+M[i][j]*x[j])%3;x[c]=(3-v)%3}if(F.every(l=>new Set(l.map(z=>x[z[0]])).size===3)){witness=x;break}}
    assert(witness,"rainbow");let bit=v=>witness[v]===0?0:1;assert(F.every(a=>a.some(z=>bit(z[0])!==bit(a[0][0]))),"original SAT lift");large.push({p,n,owners:4*p,treeCounts,parityAbs,kernel:free.length,tries,lowerRepair:2*p-Math.floor(p/3),aggregateDeficitLower: p-2*Math.floor(p/3)})}
  // Fano control: known non-2-colorable by pair counting; explicit exhaustive check.
  const fano=Array.from({length:7},(_,i)=>[i,(i+1)%7,(i+3)%7].map(v=>[v,0]));
  assert(!Array.from({length:128},(_,x)=>x).some(x=>fano.every(a=>nae(a,x))),"Fano no");
  assert(!Array.from({length:512},(_,x)=>x).some(x=>ag.every(a=>nae(a,x))),"AG9 no");
  return {seed:261126,regions,masks,pinChecks,absorbed,pairQ,large,checks,mode:"interleaved independent merge, gauge, exhaustive support; then integrated source-only GF3 bypass",note:"No maximum cycle packing oracle or formal build; large controls only SAT, AG9 and Fano are separate NO controls."}
};
console.log(JSON.stringify(audit(),null,2));

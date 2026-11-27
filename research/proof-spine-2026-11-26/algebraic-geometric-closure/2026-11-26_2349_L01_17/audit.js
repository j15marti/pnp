function check(x,m){if(!x)throw Error(m||"assertion failed")}

function cycles(p){let seen=new Set(),c=0;for(let i=0;i<p.length;i++)if(!seen.has(i)){c++;let j=i;while(!seen.has(j)){seen.add(j);j=p[j]}}return c}

function swap(p,pairs,T){let a=p.slice();for(let i of T){let [u,v]=pairs[i];[a[u],a[v]]=[a[v],a[u]]}return a}

function xorSet(A,B){return [...new Set([...A,...B])].filter(i=>A.includes(i)!==B.includes(i))}

function interlace(p,pairs){
  check(cycles(p)===1);let pos=Array(p.length),j=0;
  for(let i=0;i<p.length;i++){pos[j]=i;j=p[j]}
  let ends=pairs.map(([a,b])=>[pos[a],pos[b]].sort((a,b)=>a-b));
  return ends.map(([a,b],i)=>ends.map(([c,d],j)=>i===j?0:Number((a<c&&c<b)!==(a<d&&d<b))));
}

function rank(A){let R=A.map(r=>r.reduce((z,v,i)=>z|(BigInt(v)<<BigInt(i)),0n)),r=0;for(let j=0;j<A.length;j++){let k=r;while(k<R.length&&!(R[k]&(1n<<BigInt(j))))k++;if(k===R.length)continue;[R[r],R[k]]=[R[k],R[r]];for(let i=r+1;i<R.length;i++)if(R[i]&(1n<<BigInt(j)))R[i]^=R[r];r++}return r}

function nullity(A,T){return T.length-rank(T.map(i=>T.map(j=>A[i][j])))}

function maskset(m,n){return Array.from({length:n},(_,i)=>i).filter(i=>m&(1<<i))}

function matchingCount(A,T){if(!T.length)return 1;let a=T[0],c=0;for(let i=1;i<T.length;i++)if(A[a][T[i]])c+=matchingCount(A,T.filter((_,j)=>j!==0&&j!==i));return c}

function instance(b){
  let s=12*b,word=[0,1,2,3,4,5,3,2,1,0,5,4],P=Array.from({length:s},(_,i)=>(i+1)%s),pairs=[],twist=[],g=Array(s),groups=[];
  for(let t=0;t<b;t++){
    for(let z=0;z<6;z++)pairs.push(word.map((v,i)=>v===z?12*t+i:-1).filter(i=>i>=0));
    twist.push(6*t,6*t+2);
    for(let h=0;h<3;h++){
      let i=6*t+2*h,j=i+1,[a,c]=pairs[i],[d,e]=pairs[j];let cyc=[a,d,c,e];for(let k=0;k<4;k++)g[cyc[k]]=cyc[(k+1)%4];groups.push([i,j])
    }
  }
  let p=swap(P,pairs,twist),ginv=Array(s);for(let i=0;i<s;i++)ginv[g[i]]=i;
  let tables=Array.from({length:s},(_,i)=>[[i,p[i]],[g[i],p[ginv[i]]]]);
  return {s,P,p,pairs,twist,g,ginv,groups,tables}
}

function permFromChart(X,bits){let p=Array(X.s).fill(-1),used=new Set();for(let i=0;i<X.s;i++){let [a,b]=X.tables[i][bits[i]];if(p[a]!==-1||used.has(b))return null;p[a]=b;used.add(b)}return p}

function native(X){
  let s=X.s,E=[];for(let a=0;a<s;a++)for(let b=0;b<s;b++)if(a!==b)E.push([a,b]);
  for(let i=0;i<s;i++){let u=s+2*i,v=u+1;E.push([u,v],[v,u],[i,u],[X.g[i],v],[v,X.p[i]],[u,X.p[X.ginv[i]]])}
  return {n:3*s,E}
}

function acquire(G,s){
  let E=new Set(G.E.map(e=>e.join(","))),T=[];
  for(let i=0;i<s;i++){let u=s+2*i,v=u+1,pairs=[];for(let [x,y] of [[u,v],[v,u]])if(E.has(x+","+y)){
    for(let a=0;a<s;a++)if(E.has(a+","+x))for(let b=0;b<s;b++)if(E.has(y+","+b))pairs.push([a,b])
  }T.push(pairs)}
  return T
}

function stronglyConnected(p,pairs){let n=p.length,A=Array.from({length:n},()=>[]),R=A.map(()=>[]),alt=p.slice();for(let [a,b] of pairs){alt[a]=p[b];alt[b]=p[a]}for(let i=0;i<n;i++)for(let j of new Set([p[i],alt[i]])){A[i].push(j);R[j].push(i)}for(let G of [A,R]){let seen=new Set([0]),stack=[0];while(stack.length)for(let v of G[stack.pop()])if(!seen.has(v)){seen.add(v);stack.push(v)}if(seen.size!==n)return false}return true}

function treeReference(p,pairs){let comp=Array(p.length).fill(-1),k=0;for(let i=0;i<p.length;i++)if(comp[i]<0){let j=i;while(comp[j]<0){comp[j]=k;j=p[j]}k++}let parent=Array.from({length:k},(_,i)=>i);function find(i){while(parent[i]!==i)i=parent[i];return i}let t=[];for(let i=0;i<pairs.length;i++){let [a,b]=pairs[i],u=find(comp[a]),v=find(comp[b]);if(u!==v){parent[u]=v;t.push(i)}}let P=swap(p,pairs,t);return {P,t,connected:cycles(P)===1}}

function match(G,forced=null){
  let n=G.n,A=Array.from({length:n},()=>[]),M=Array(n).fill(-1);
  for(let [u,v] of G.E)if(!forced||(u===forced[0]?v===forced[1]:v!==forced[1]))A[u].push(v);
  function dfs(u,S){for(let v of A[u])if(!S.has(v)){S.add(v);if(M[v]===-1||dfs(M[v],S)){M[v]=u;return true}}return false}
  for(let u=0;u<n;u++)if(!dfs(u,new Set()))return false;return true
}

function run(){
  let rows=[],checks=0;
  for(let b of [1,2,4,8,16,32]){
    let X=instance(b),G=native(X),T=acquire(G,X.s),A=interlace(X.P,X.pairs);check(JSON.stringify(T)===JSON.stringify(X.tables),"native paths");check(stronglyConnected(X.p,X.pairs));
    let ref=treeReference(X.p,X.pairs);check(ref.connected&&cycles(ref.P)===1&&ref.t.length===2*b);
    let A2=interlace(ref.P,X.pairs);let g=6*b;
    for(let i=0;i<g;i++)for(let j=0;j<g;j++){let e=(Math.floor(i/6)===Math.floor(j/6))&&((i%6<4)!==(j%6<4));check(A[i][j]===Number(e),"block");checks++}
    // Independent exact block defect optimum; no production general delta-matroid solver.
    let opts=[];
    for(let c=0;c<b;c++){
      let ids=Array.from({length:6},(_,i)=>6*c+i),B=ids.map(i=>ids.map(j=>A[i][j])),tw=[0,2],d=6;let feas=0;
      for(let mask=0;mask<64;mask++){let z=maskset(mask,6);if(nullity(B,z))continue;feas++;let f=xorSet(z,tw),d0=[0,2,4].filter(i=>f.includes(i)!==f.includes(i+1)).length;d=Math.min(d,d0)}
      check(d===2);opts.push({minBroken:d,nonsingularSubsets:feas});
      for(let m=0;m<8;m++){
        let w=maskset(m,3).flatMap(i=>[2*i,2*i+1]),z=xorSet(tw,w);
        check(nullity(B,z)===2);check(matchingCount(B,z)===(z.length===4?2:0));checks+=2
      }
    }
    let checked=0,cycleValues=new Set(),enumeratedAll=false;
    // independently enumerate full original region orientation for b=1 (4096 words); compare chart.
    let originalWords=null;
    if(b===1){
      let accepted=0,cycleHist={};
      for(let m=0;m<1<<X.s;m++){let p=permFromChart(X,Array.from({length:X.s},(_,i)=>(m>>i)&1));if(p){accepted++;let c=cycles(p);cycleHist[c]=(cycleHist[c]||0)+1}}
      check(accepted===8&&cycleHist[3]===8);originalWords={tested:1<<X.s,accepted,cycleHist};
    }
    let masks=b<=2?Array.from({length:1<<(3*b)},(_,i)=>maskset(i,3*b)):[[],Array.from({length:3*b},(_,i)=>i),...Array.from({length:3*b},(_,i)=>[i])];
    enumeratedAll=b<=2;
    for(let W of masks){
      let t=W.flatMap(i=>X.groups[i]),p=swap(X.p,X.pairs,t),bits=Array(X.s).fill(0);
      for(let i of t)for(let v of X.pairs[i])bits[v]=1;
      let p0=permFromChart(X,bits);check(JSON.stringify(p)===JSON.stringify(p0),"lift");let c=cycles(p);check(c===1+2*b);check(c===1+nullity(A,xorSet(X.twist,t)));check(c===1+nullity(A2,xorSet(ref.t,t)));cycleValues.add(c);checked++;checks+=4
    }
    // All arcs match-supported via actual matching on smallest native graph. Stronger target support symbolic.
    let matchTests=0;if(b===1){for(let e of G.E){check(match(G,e),"unsupported arc");matchTests++}}
    rows.push({blocks:b,separator:X.s,n:G.n,arcs:G.E.length,N:G.n*(G.n-1),chartAssignments:(2n**BigInt(3*b)).toString(),minBroken:opts.reduce((s,o)=>s+o.minBroken,0),cycles:[...cycleValues],checked,enumeratedAll,originalWords,matchTests,relaxedTreeSwaps:ref.t.length,perBlock:opts[0],allNativeTables:true,matchingRelaxationPasses:true});
  }
  // Minimal YES falsifier: one-cycle P with no offset; empty selection has nullity zero.
  let X=instance(1);check(cycles(X.P)===1&&nullity(interlace(X.P,X.pairs),[])===0);
  return {rows,checks,control:"zero offset: empty phase word is a tour; rank test admits it",execution:"serial; exact binary rank and direct permutation cycle counts; not general delta-parity algorithm"}
}
console.log(JSON.stringify(run(),null,2));

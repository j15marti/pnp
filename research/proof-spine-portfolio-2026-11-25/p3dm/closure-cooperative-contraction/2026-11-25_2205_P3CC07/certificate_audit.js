// P3CC07 exact small certificate verifier; finite control only, no global solver.
const data={"T":[[0,0,0],[0,0,2],[0,1,0],[0,1,1],[0,2,1],[0,2,2],[1,0,0],[1,0,1],[1,1,1],[2,0,1],[2,0,2],[2,2,1],[1,1,0]],"n":3,"rot":[[9,11,12,13,14,10],[15,16,17,21],[18,19,20],[9,10,19,18,16,15],[12,11,21,17],[14,13,20],[11,9,15,21],[13,12,17,16,18,20],[10,14,19],[0,3,6],[3,0,8],[4,0,6],[7,0,4],[5,0,7],[8,0,5],[6,3,1],[1,3,7],[1,7,4],[7,3,2],[2,3,8],[2,5,7],[1,4,6]],"lanes":[{"a":0,"b":1,"S":[[1,[-1,0,0,0,0,0,0,0,0]],[0,[0,0,0,0,0,0,0,1,0]],[0,[0,0,0,0,0,1,0,-1,0]],[0,[0,0,0,0,1,-1,0,0,0]],[0,[0,1,0,0,-1,0,0,0,0]],[0,[1,-1,0,0,0,0,0,0,0]],[0,[0,0,0,0,0,0,1,-1,0]],[0,[0,0,0,0,1,0,-1,0,0]],[1,[0,0,-1,0,0,0,0,1,-1]],[0,[0,0,0,1,-1,0,0,0,0]],[0,[1,0,0,-1,0,0,0,0,0]],[1,[-1,0,0,0,1,0,0,0,0]],[0,[0,0,1,0,-1,0,0,0,1]]],"A":[[1,0],[3,0],[4,0],[4,1],[4,2],[4,3],[5,4],[6,4],[7,2],[7,5],[7,6],[8,2],[8,4],[8,7]],"x":[2,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"d":2,"energy_num":[0,-1,-1]},{"a":0,"b":2,"S":[[1,[0,-1,0,0,0,0,0,0,0]],[0,[0,0,1,0,-1,0,0,0,0]],[0,[0,0,0,0,0,0,0,1,0]],[0,[0,0,0,0,0,1,0,-1,0]],[0,[0,0,0,0,1,-1,0,0,0]],[0,[0,1,-1,0,0,0,0,0,0]],[0,[0,0,0,0,0,0,1,-1,0]],[1,[-1,0,0,0,0,0,0,1,-1]],[0,[1,-1,0,0,0,0,0,0,1]],[0,[0,0,0,1,-1,0,0,0,0]],[1,[0,-1,0,0,1,0,0,0,0]],[0,[0,1,0,-1,0,0,0,0,0]],[0,[0,1,0,0,0,0,-1,0,0]]],"A":[[1,0],[2,1],[3,1],[4,1],[4,2],[4,3],[5,4],[6,1],[7,0],[7,5],[7,6],[8,0],[8,1],[8,7]],"x":[2,2,1,1,1,0,0,0,0,2,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"d":2,"energy_num":[-1,0,-1]},{"a":1,"b":2,"S":[[1,[-1,0,0,0,0,0,0,0]],[0,[0,0,0,0,0,1,0,0]],[0,[0,0,0,0,0,0,1,0]],[1,[0,-1,0,0,0,0,0,0]],[0,[0,0,0,0,0,0,0,1]],[1,[0,0,0,0,-1,0,0,0]],[0,[1,0,-1,0,0,0,0,0]],[0,[0,0,0,1,-1,0,0,0]],[0,[0,1,-1,0,0,0,0,0]],[0,[0,0,1,-1,0,0,0,0]],[0,[0,0,0,0,1,-1,0,0]],[0,[0,0,0,0,1,0,0,-1]],[0,[0,0,1,0,0,0,-1,0]]],"A":[[2,0],[2,1],[3,2],[4,3],[5,4],[6,2],[7,4]],"x":[2,2,2,1,1,1,0,1,2,2,1,1,1,0,1,2,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,0,1,0,0,0],"d":2,"energy_num":[-1,0,-1]}]};
function audit(data){
  let assertions=0; const check=(v,m)=>{assertions++;if(!v)throw Error(m)};
  const {T,n,rot,lanes}=data, V=3*n+T.length;
  const expected=Array.from({length:V},()=>[]);
  T.forEach((t,e)=>t.forEach((x,c)=>{const a=c*n+x,b=3*n+e;expected[a].push(b);expected[b].push(a)}));
  check(rot.length===V,"rotation length");
  for(let i=0;i<V;i++)check([...rot[i]].sort((a,b)=>a-b).join()===expected[i].sort((a,b)=>a-b).join(),"incidence");
  let reached=new Set([0]),front=[0];while(front.length){for(const j of rot[front.pop()])if(!reached.has(j)){reached.add(j);front.push(j)}}
  check(reached.size===V,"connected");
  const seen=new Set();let faces=0;
  for(let u=0;u<V;u++)for(const v of rot[u]){let i=u,j=v;if(seen.has(i+","+j))continue;faces++;
    do{check(!seen.has(i+","+j),"face cycle");seen.add(i+","+j);let k=rot[j][(rot[j].indexOf(i)+1)%rot[j].length];i=j;j=k}while(i!==u||j!==v)
  }
  check(V-3*T.length+faces===2,"sphere Euler characteristic");
  const sets=[];for(let k=0;k<(1<<T.length);k++){let s=[];for(let j=0;j<T.length;j++)if(k>>j&1)s.push(j);if(s.length===n)sets.push(s)}
  const legal=(s,c)=>new Set(s.map(j=>T[j][c])).size===n;
  const covers=sets.filter(s=>[0,1,2].every(c=>legal(s,c)));check(covers.length>0,"source SAT");
  const laneResults=[];
  for(const {a,b,S,A,x,d,energy_num} of lanes){
    const h=S[0][1].length,z=3-a-b;const exact=sets.filter(s=>legal(s,a)&&legal(s,b));const got=[],solutions=[];
    for(let mask=0;mask<1<<h;mask++){
      const w=Array.from({length:h},(_,i)=>mask>>i&1);if(A.some(([i,j])=>w[i]>w[j]))continue;
      const s=S.map(([c,v])=>c+v.reduce((q,k,i)=>q+k*w[i],0));check(s.every(k=>k===0||k===1),"binary lift");const ids=s.flatMap((k,i)=>k?[i]:[]);check(ids.length===n&&legal(ids,a)&&legal(ids,b),"pair matching lift");
      got.push(ids.join());if(legal(ids,z))solutions.push(w)
    }
    check(got.length===new Set(got).size,"injective chart");check([...got].sort().join(";")===exact.map(s=>s.join()).sort().join(";"),"surjective chart");
    check(solutions.length===covers.length,"exact cover count");
    const p=Array.from({length:h},()=>Array(h).fill(0));let k=h;
    for(let i=0;i<h;i++){check(x[i]>=0&&x[i]<=d,"unary moment");p[i][i]=x[i];for(let j=i+1;j<h;j++)p[i][j]=p[j][i]=x[k++]}
    check(k===x.length,"moment indexing");
    let excluded=0;
    for(let i=0;i<h;i++)for(let j=i+1;j<h;j++){
      const tab=[d-x[i]-x[j]+p[i][j],x[j]-p[i][j],x[i]-p[i][j],p[i][j]];
      for(let q=0;q<4;q++){check(tab[q]>=0,"local pair probability");if(!solutions.some(w=>2*w[i]+w[j]===q)){excluded++;check(tab[q]===0,"full semantic binary hull")}}
    }
    for(let i=0;i<h;i++)for(let bit=0;bit<2;bit++)if(!solutions.some(w=>w[i]===bit))check((bit?x[i]:d-x[i])===0,"full unary hull");
    for(const [i,j] of A)check(x[i]===p[i][j],"hard implication");
    const es=[];
    for(let label=0;label<n;label++){
      let c=-1,v=Array(h).fill(0);
      for(let e=0;e<T.length;e++)if(T[e][z]===label){c+=S[e][0];for(let i=0;i<h;i++)v[i]+=S[e][1][i]}
      let value=d*c*c;for(let i=0;i<h;i++){value+=(2*c*v[i]+v[i]*v[i])*x[i];for(let j=i+1;j<h;j++)value+=2*v[i]*v[j]*p[i][j]}
      es.push(value)
    }
    check(es.join()===energy_num.join(),"exact energy vector");check(es.every(v=>v<=0)&&es.some(v=>v<0),"all positive weights obstructed");
    laneResults.push({lane:[a,b],thresholds:h,perfectMatchings:got.length,sourceCovers:solutions.length,excludedPairPatterns:excluded,denominator:d,energyNumerators:es});
  }
  return {assertions,vertices:V,edges:3*T.length,faces,coverIDs:covers,lanes:laneResults};
}
console.log(JSON.stringify(audit(data),null,2));

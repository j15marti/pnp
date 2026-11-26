function audit(){
  let seed=6112602, checks=0, models=0, colors=0, overlaps=0, cases=0;
  const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const assert=(b,msg)=>{checks++;if(!b)throw Error(msg)};
  const bit=(x,i)=>((x>>i)&1)!==0;
  function build(n,imp,neg,pins,w){
    const valid=x=>pins.every(i=>!bit(x,i))&&imp.every(([i,j])=>!bit(x,i)||bit(x,j))&&neg.every(([i,j])=>!(bit(x,i)&&bit(x,j)));
    const lab=x=>w.reduce((v,a,i)=>bit(x,i)?v^a:v,0);
    const C=[];
    for(let i=0;i<n;i++){let x=1<<i,old=-1;while(old!==x){old=x;for(const [u,v] of imp)if(bit(x,u))x|=1<<v}if(valid(x))C.push(x)}
    const V=C.length,O=Array(V).fill(0),F=Array(V).fill(0);
    let active=0;w.forEach((a,i)=>{if(a)active|=1<<i});
    for(let i=0;i<V;i++)for(let j=i+1;j<V;j++){
      if(C[i]&C[j]&active){O[i]|=1<<j;O[j]|=1<<i}
      if(!valid(C[i]|C[j])){F[i]|=1<<j;F[j]|=1<<i}
    }
    let rem=(1<<V)-1, out=Array(V).fill(0),d=0;
    const pop=x=>{let z=0;while(x){x&=x-1;z++}return z};
    while(rem){let i=-1,best=V+1;for(let j=0;j<V;j++)if(bit(rem,j)&&pop(F[j]&rem)<best){i=j;best=pop(F[j]&rem)}d=Math.max(d,best);out[i]=F[i]&rem;rem^=1<<i}
    const D=Math.max(0,...O.map(pop));
    function comp(red){
      let keep=red;
      for(let i=0;i<V;i++)if(bit(red,i)&&(out[i]&red))keep&=~(1<<i);
      const groups=[];
      while(keep){let g=keep&-keep,old=-1;while(g!==old){old=g;for(let i=0;i<V;i++)if(bit(g,i))g|=O[i]&keep}keep&=~g;let u=0;for(let i=0;i<V;i++)if(bit(g,i))u|=C[i];groups.push(u)}
      return groups;
    }
    return {valid,lab,C,comp,d,D,O,F,out};
  }
  function support(groups,lab,valid){
    // Gaussian basis with original-variable union witnesses. Different groups can
    // share only zero-label IDs. Basis combinations use symmetric difference
    // of group-selection masks, not symmetric difference of source assignments.
    let basis=new Map();
    for(let j=0;j<groups.length;j++){let a=lab(groups[j]),s=1<<j;while(a){let i=31-Math.clz32(a);if(!basis.has(i)){basis.set(i,[a,s]);break}let [b,t]=basis.get(i);a^=b;s^=t}}
    const R=new Map([[0,0]]);
    for(const [a,s] of basis.values())for(const [b,t] of [...R])R.set(a^b,s^t);
    for(const [a,s] of R){let u=0;for(let j=0;j<groups.length;j++)if(bit(s,j))u|=groups[j];assert(valid(u)&&lab(u)===a,"Gaussian witness")}
    return R;
  }
  for(let t=0;t<220;t++){
    let n=3+rand(7),k=1+rand(4),imp=[],neg=[],pins=[],w=Array.from({length:n},()=>rand(1<<k));
    for(let i=0;i<n;i++){if(rand(12)===0)pins.push(i);for(let j=i+1;j<n;j++){let z=rand(13);if(z===0)imp.push([i,j]);if(z===1)imp.push([j,i]);if(z===2)neg.push([i,j])}}
    let A=build(n,imp,neg,pins,w),target=new Set(),got=new Set();
    for(let x=0;x<1<<n;x++)if(A.valid(x)){target.add(A.lab(x));models++}
    for(let red=0;red<1<<A.C.length;red++){colors++;let groups=A.comp(red);for(let i=0;i<groups.length;i++)for(let j=i+1;j<groups.length;j++){assert(A.valid(groups[i]|groups[j]),"cross conflict");assert(A.lab(groups[i]|groups[j])===(A.lab(groups[i])^A.lab(groups[j])),"overlap accounting")}
      for(const a of support(groups,A.lab,A.valid).keys())got.add(a)}
    assert(got.size===target.size&&[...target].every(a=>got.has(a)),"complete support");
    // Independent minimal-cardinality witness check for every attained target.
    for(const a of target){let best=-1,cnt=n+1;for(let x=0;x<1<<n;x++)if(A.valid(x)&&A.lab(x)===a){let p=x.toString(2).replace(/0/g,"").length;if(p<cnt){cnt=p;best=x}}
      // Number of maximal independent seed SCCs bounded by k, via enumeration of at most k closures.
      let found=false;for(let s=0;s<1<<A.C.length;s++){if(s.toString(2).replace(/0/g,"").length>k)continue;let u=0;for(let i=0;i<A.C.length;i++)if(bit(s,i))u|=A.C[i];if(u===best){found=true;break}}
      assert(found,"minimal witness seed bound")}
    if(A.D>0)overlaps++;cases++;
  }
  // Adversarial overlapping closures: x1 -> h, x2 -> h, h carries syndrome 1.
  // Individual labels both 1, union label 1, not 0.
  let E=build(3,[[1,0],[2,0]],[],[],[1,0,0]);
  assert(E.lab(3)===1&&E.lab(5)===1&&E.lab(7)===1&&E.D===2,"nonzero overlap must not drop");
  // Rank-two missing syndrome despite full affine hull and each linear projection.
  let M=build(6,[],Array.from({length:6},(_,i)=>Array.from({length:6-i-1},(_,j)=>[i,i+j+1])).flat(),[],[1,1,1,2,2,2]);
  let m=new Set();for(let x=0;x<64;x++)if(M.valid(x))m.add(M.lab(x));
  assert(m.size===3&&!m.has(3)&&m.has(1)&&m.has(2),"rank two hull false");
  // Native prism products, explicit source guards a_i -> a0 and local AMO.
  // a0 is zero-weight. Conflict graph is a tree (b0 joined to all a_i,
  // plus a_i--b_i for i>0); all nontrivial overlaps are at zero label a0.
  const native=[];
  for(const b of [4,8,16,32,64,128]){
    const r=Math.floor(Math.log2(b)),w=Array(2*b).fill(0);
    for(let j=1;j<=r;j++)w[2*j]=1<<(j-1);
    const C=Array.from({length:2*b},(_,i)=>i>0&&i%2===0?new Set([0,i]):new Set([i]));
    const valid=s=>{for(let i=0;i<b;i++)if(s.has(2*i)&&s.has(2*i+1))return false;for(let i=1;i<b;i++)if(s.has(2*i)&&!s.has(0))return false;return true};
    const lab=s=>[...s].reduce((x,i)=>x^w[i],0);
    let f=Array(2*b).fill(0),old=Array(2*b).fill(0),active=0,edges=0;
    for(let i=0;i<2*b;i++)for(let j=i+1;j<2*b;j++){
      let common=[...C[i]].filter(x=>C[j].has(x));if(common.some(x=>w[x]))active++;
      let conflict=!valid(new Set([...C[i],...C[j]]));if(conflict){f[i]++;f[j]++;edges++}if(conflict||common.length){old[i]++;old[j]++}
    }
    assert(active===0&&edges===2*b-1&&Math.max(...old)>=b-1,"native graph structure");
    for(let t=0;t<1<<r;t++){
      const s=new Set();for(let j=1;j<=r;j++)if(bit(t,j-1)){s.add(0);s.add(2*j)}
      assert(valid(s)&&lab(s)===t,"native guard lift");
      const x=[];for(let i=0;i<b;i++){let a=+s.has(2*i),c=+s.has(2*i+1),z=1-a-c;x.push(a,c,z,a,c,z)}
      for(let i=0;i<b;i++)for(let j=0;j<6;j++)assert(x[6*i+(j+5)%6]+x[6*i+j]+x[6*i+(j+1)%6]===1,"native prism row");
    }
    native.push({blocks:b,source_variables:6*b,rank:r,old_max_degree:Math.max(...old),active_overlap_edges:active,conflict_edges:edges,conflict_degeneracy:1,verified_syndromes:1<<r});
  }
  return {seed:6112602,cases,models,colors,overlaps,checks,native,scope:"Exhaustive red masks, not full finite-field separator family; native family analytic chart and witness audit, not general full source closure."};
}
console.log(JSON.stringify(audit(),null,2));

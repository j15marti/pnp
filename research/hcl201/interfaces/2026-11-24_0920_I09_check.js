function experiment(){
  let seed=0x1a092026; const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
  const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
  const basis=(rows)=>{let a=[];for(let z of rows){for(const [p,v] of a)if(z&bit(p))z^=v;if(z){let p=z.toString(2).length-1;a.push([p,z]);a.sort((x,y)=>y[0]-x[0])}}return a};
  const reduce=(z,B)=>{for(const [p,v] of B)if(z&bit(p))z^=v;return z};
  const ck=(v,msg)=>{if(!v)throw Error(msg)};
  const stats={seed:"0x1a092026",cases:0,sat:0,unsat:0,referenceMatchings:0,cycleWitnesses:0,closurePasses:0,constantEdgeBits:0,constantPortBits:0,constantTagBits:0,parityQueries:0,paritySAT:0,parityUNSAT:0,physicalizableTests:0,physicalizable:0,groupTests:0,groupMatches:0,groupInjectionCases:0,groupInjectionSuccess:0,projectedKernelRankSum:0,fullRankDefectZero:0,disagreements:0,structured:[]};
  function check(n,m,E,required,q,groups,full=true){
    stats.cases++;stats.closurePasses++;
    const b=n+m, Q=b+q, mask=bit(b)-1n, tmask=bit(q)-1n, total=Q+E.length;
    const adj=Array.from({length:b},()=>[]), tags=Array.from({length:b},()=>new Map());
    function add(i,j,t){adj[i].push(j);tags[i].set(j,t)}
    E.forEach(([i,j,g],k)=>add(i,j,(BigInt(g)<<BigInt(b))|bit(Q+k)));
    for(let i=0;i<n;i++)if(!(required&bit(i)))for(let j=m;j<b;j++)add(i,j,bit(i));
    for(let i=n;i<b;i++)for(let j=0;j<m;j++)if(!(required&bit(n+j)))add(i,j,bit(n+j));
    for(let i=n;i<b;i++)for(let j=m;j<b;j++)add(i,j,0n);
    const matchR=Array(b).fill(-1);
    function aug(i,seen){for(const j of adj[i])if(!seen[j]){seen[j]=true;if(matchR[j]<0||aug(matchR[j],seen)){matchR[j]=i;return true}}return false}
    let feasible=true;for(let i=0;i<b;i++)if(!aug(i,Array(b).fill(false))){feasible=false;break}
    let refs=[];
    if(full){
      function rec(i,used,z,covered){if(i===n){if((required&covered)===required)refs.push(z|(mask^covered));return}
        rec(i+1,used,z,covered);
        E.forEach(([u,v,g],k)=>{if(u===i&&!(used&bit(v)))rec(i+1,used|bit(v),z|(BigInt(g)<<BigInt(b)),covered|bit(u)|bit(n+v))});
      }
      // independent exhaustive source matching enumeration, with XOR tags and edge indicator
      function ref(i,used,z,covered){if(i===n){if((required&covered)===required)refs.push(z|(mask^covered));return}ref(i+1,used,z,covered);E.forEach(([u,v,g],k)=>{if(u===i&&!(used&bit(v)))ref(i+1,used|bit(v),z^(BigInt(g)<<BigInt(b))^bit(Q+k),covered|bit(u)|bit(n+v))})}
      ref(0,0n,0n,0n);stats.referenceMatchings+=refs.length;ck(feasible===(refs.length>0),"base decision");
    }
    if(!feasible){stats.unsat++;return null}
    stats.sat++;
    const M=Array(b);matchR.forEach((i,j)=>M[i]=j);
    const value=P=>P.reduce((a,j,i)=>a^tags[i].get(j),0n), z0=value(M);
    function sourceVerify(P,z){let cov=0n,x=0n;const used=new Set();for(let i=0;i<b;i++){ck(!used.has(P[i])&&tags[i].has(P[i]),"not perfect");used.add(P[i]);if(i<n&&P[i]<m){const k=E.findIndex(e=>e[0]===i&&e[1]===P[i]);ck(k>=0,"source edge");cov|=bit(i)|bit(n+P[i]);x^=(BigInt(E[k][2])<<BigInt(b))^bit(Q+k)}}ck((cov&required)===required&&((x|(mask^cov))===z),"bad source lift")}
    sourceVerify(M,z0);
    const D=Array.from({length:b},()=>[]);
    for(let i=0;i<b;i++)for(const j of adj[i])if(j!==M[i])D[i].push(matchR[j]);
    function paths(s){let p=Array(b).fill(null);p[s]=[s];let queue=[s];for(let k=0;k<queue.length;k++){let u=queue[k];for(let v of D[u])if(p[v]===null){p[v]=p[u].concat(v);queue.push(v)}}return p}
    const P=Array.from({length:b},(_,i)=>paths(i)), seen=new Set(), deltas=[], witnesses=[];
    function cycle(C){let X=M.slice();for(let i=0;i<C.length-1;i++)X[C[i]]=M[C[i+1]];let z=value(X);sourceVerify(X,z);if(full)ck(refs.includes(z),"cycle not in source reference");deltas.push(z^z0);witnesses.push(z);stats.cycleWitnesses++}
    function walk(W){let st=[],at=new Map();for(const v of W){if(at.has(v)){let k=at.get(v);if(st.length-k>1)cycle(st.slice(k).concat(v));for(let j=st.length-1;j>k;j--)at.delete(st[j]);st.length=k+1}else{at.set(v,st.length);st.push(v)}}ck(st.length===1,"not closed")}
    for(let r=0;r<b;r++)if(!seen.has(r)){let C=[];for(let v=0;v<b;v++)if(P[r][v]&&P[v][r]){C.push(v);seen.add(v)}let S=new Set(C);for(let v of C){walk(P[r][v].concat(P[v][r].slice(1)));for(let w of D[v])if(S.has(w))walk(P[r][v].concat([w],P[w][r].slice(1)))}}
    const B=basis(deltas);if(full){const R=basis(refs.map(z=>z^z0));ck(B.length===R.length&&B.every(([p,v])=>reduce(v,R)===0n),"joint hull")}
    // First unconditional closure on the entire current unfiltered matching domain.
    for(let i=0;i<total;i++)if(B.every(([p,v])=>!(v&bit(i)))){if(i<b)stats.constantPortBits++;else if(i<Q)stats.constantTagBits++;else stats.constantEdgeBits++}
    // Projection to the joint occupancy/tag coordinates; eliminate occupancy pivots first.
    let piv=new Map(), pure=[];
    for(let v of deltas){let d=v&mask,t=(v>>BigInt(b))&tmask;for(let i=b-1;i>=0;i--)if(d&bit(i)){if(piv.has(i)){const [a,c]=piv.get(i);d^=a;t^=c}else{piv.set(i,[d,t]);break}}if(!d)pure.push(t)}
    let K=basis(pure);stats.projectedKernelRankSum+=K.length;if(!K.length)stats.fullRankDefectZero++;
    for(let a=1n;a<=tmask;a++){
      const yes=K.every(([p,t])=>!parity(a&t));stats.physicalizableTests++;if(yes)stats.physicalizable++;
      if(full){let brute=false;for(let p=0n;p<=mask;p++){const c=parity(a&((z0>>BigInt(b))&tmask))^parity(p&(z0&mask));if(refs.every(z=>(parity(a&((z>>BigInt(b))&tmask))^parity(p&(z&mask)))===c)){brute=true;break}}ck(yes===brute,"physicalization criterion")}
      if(yes){let p=0n;for(let i=0;i<b;i++)if(piv.has(i)){let [d,t]=piv.get(i);if(parity(a&t)^parity(p&d))p|=bit(i)}let c=parity(a&((z0>>BigInt(b))&tmask))^parity(p&(z0&mask));ck([z0,...witnesses].every(z=>(parity(a&((z>>BigInt(b))&tmask))^parity(p&(z&mask)))===c),"recovered port map");}
      for(let target=0;target<2;target++){stats.parityQueries++;const wit=[z0,...witnesses].find(z=>parity(a&((z>>BigInt(b))&tmask))===target);if(wit===undefined)stats.parityUNSAT++;else stats.paritySAT++;if(full)ck((wit!==undefined)===refs.some(z=>parity(a&((z>>BigInt(b))&tmask))===target),"one parity query")}
    }
    // Given fixed disjoint owner classes, identify exact tag-to-owner maps modulo constants.
    let opts=Array.from({length:q},()=>[]);
    for(let j=0;j<q;j++)for(let i=0;i<groups.length;i++){let l=bit(b+j)|groups[i];let ok=B.every(([p,v])=>!parity(l&v));stats.groupTests++;if(ok){stats.groupMatches++;opts[j].push(i)}if(full)ck(ok===refs.every(z=>parity(l&(z^z0))===0),"group recognition")}
    let gmatch=Array(groups.length).fill(-1);function ga(j,seen){for(let i of opts[j])if(!seen.has(i)){seen.add(i);if(gmatch[i]<0||ga(gmatch[i],seen)){gmatch[i]=j;return true}}return false}
    let inject=true;for(let j=0;j<q;j++)if(!ga(j,new Set())){inject=false;break}
    stats.groupInjectionCases++;if(inject)stats.groupInjectionSuccess++;
    if(full){function brute(j,used){if(j===q)return true;return opts[j].some(i=>!used.has(i)&&brute(j+1,new Set([...used,i])))}ck(inject===brute(0,new Set()),"group injection")}
    return {rank:B.length,kernelRank:K.length,inject,cycles:deltas.length};
  }
  for(let k=0;k<180;k++){const n=2+Math.floor(rnd()*3),m=2+Math.floor(rnd()*3),q=3,b=n+m;let req=0n;for(let i=0;i<b;i++)if(rnd()<0.35)req|=bit(i);let groups=[0n,0n,0n];for(let i=0;i<b;i++)if(!(req&bit(i)))groups[Math.floor(rnd()*3)]|=bit(i);let E=[];for(let i=0;i<n;i++)for(let j=0;j<m;j++)if(rnd()<.48){let g=Math.floor(rnd()*8);if(k%3===0){g=0;for(let a=0;a<3;a++)if(parity(groups[a]&(bit(i)|bit(n+j))))g|=1<<a}E.push([i,j,g])}check(n,m,E,req,q,groups)}
  // Mandatory K2,2 cycle with one red edge: constant occupancy, nonconstant tag.
  const k22=check(2,2,[[0,0,1],[0,1,0],[1,0,0],[1,1,0]],15n,1,[0n]);ck(k22.kernelRank===1&&!k22.inject,"K22 obstruction");stats.structured.push({name:"K2,2 internal syndrome obstruction",...k22});
  // Disjoint physicalizable edges; raw matching supports 2^h tuples; only 3 fixed tag bits queried.
  for(let h of [8,16,32]){let groups=[0n,0n,0n],E=[];for(let i=0;i<h;i++){groups[i%3]|=bit(i);E.push([i,i,1<<(i%3)])}let x=check(h,h,E,0n,3,groups,false);ck(x.kernelRank===0&&x.inject,"scaling physicalization");stats.structured.push({name:"independent edges",h,rawSupport:"2^"+h,...x})}
  // Explicit infeasible mandatory port.
  ck(check(1,1,[],1n,1,[2n])===null,"isolated mandatory control");
  return stats;
}
console.log(JSON.stringify(experiment(),null,2));

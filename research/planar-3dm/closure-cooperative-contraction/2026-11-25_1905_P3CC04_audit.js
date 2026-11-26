"use strict";
const audit=function(){
  let calls=0, checks=0, lifts=0, seed=261125;
  const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32};
  const assert=(x,msg)=>{checks++;if(!x)throw Error(msg)};
  const bx=(a,b)=>a^b;
  const sig=(T,M)=>M.reduce((a,i)=>a^T[i][2],0n);
  function pm(T,n,pin=-1,omit=-1){
    calls++;if(pin===omit&&pin>=0)return null;
    const ys=Array(n).fill(-1),usedX=pin<0?-1:T[pin][0],usedY=pin<0?-1:T[pin][1];
    if(pin>=0)ys[usedY]=pin;
    const rows=Array.from({length:n},()=>[]);
    T.forEach((t,i)=>{if(i!==omit&&i!==pin&&t[0]!==usedX&&t[1]!==usedY)rows[t[0]].push(i)});
    function aug(x,seen){for(const i of rows[x]){const y=T[i][1];if(seen[y])continue;seen[y]=1;if(ys[y]<0||aug(T[ys[y]][0],seen)){ys[y]=i;return true}}return false}
    for(let x=0;x<n;x++)if(x!==usedX&&!aug(x,Array(n).fill(0)))return null;
    return ys;
  }
  function forced(T,n,pin){const M=pm(T,n,pin);return M===null?null:M.filter(i=>i===pin||!pm(T,n,pin,i))}
  function cycleShifts(T,F,L,reduce){
    const map=new Map([["0",{p:0n,old:[],alt:[]}]]);
    const adj=F.map(i=>F.map((j,b)=>T.map((t,e)=>[t,e]).filter(([t,e])=>e!==i&&t[0]===T[i][0]&&t[1]===T[j][1]).map(([t,e])=>[b,e])).flat());
    for(let start=0;start<F.length;start++){
      function walk(path,edges){
        const u=path[path.length-1];
        for(const [v,e] of adj[u]){
          if(v===start){const old=path.map(k=>F[k]),alt=[...edges,e],p=reduce(sig(T,old)^sig(T,alt));if(!map.has(String(p)))map.set(String(p),{p,old,alt})}
          else if(path.length<L&&v>start&&!path.includes(v))walk([...path,v],[...edges,e])
        }
      }walk([start],[])
    }return map;
  }
  function certify(T,n,L,reduce,x){
    let common=null;const byPin=new Map();
    for(let e=0;e<T.length;e++)if(T[e][0]===x){const F=forced(T,n,e);if(F===null)continue;const D=cycleShifts(T,F,L,reduce);byPin.set(e,D);common=common===null?new Set(D.keys()):new Set([...common].filter(p=>D.has(p)))}
    return {dirs:[...(common||[])].filter(p=>p!=="0").map(BigInt),byPin,x}
  }
  function reduceWith(H,s){for(const [bit,p] of H)if(s&bit)s^=p;return s}
  function closure(T,n,L=3){
    const H=[],steps=[];
    while(true){
      const r=s=>reduceWith(H,s);let hit=null;
      for(let x=0;x<n;x++){const C=certify(T,n,L,r,x);if(C.dirs.length){hit={...C,p:C.dirs[0]};break}}
      if(!hit)break;
      const p=hit.p,bit=1n<<BigInt(p.toString(2).length-1);H.push([bit,p]);H.sort((a,b)=>a[0]>b[0]?-1:1);steps.push(hit)
    }
    return {H,steps,reduce:s=>reduceWith(H,s)}
  }
  function lift(T,M,target,C){
    let A=new Set(M);
    for(let k=C.steps.length-1;k>=0;k--){
      const step=C.steps[k],basis=[];for(const s of C.steps.slice(0,k)){const p=s.p;basis.push([1n<<BigInt(p.toString(2).length-1),p])}basis.sort((a,b)=>a[0]>b[0]?-1:1);
      const residual=reduceWith(basis,target^sig(T,[...A]));
      assert(residual===0n||residual===step.p,"wrong reverse coset");
      if(residual){const pin=[...A].find(i=>T[i][0]===step.x);const q=step.byPin.get(pin).get(String(step.p));for(const i of q.old){assert(A.has(i),"forced edge missing");A.delete(i)}for(const i of q.alt)A.add(i);lifts++;}
    }
    assert(sig(T,[...A])===target,"lift wrong target");assert(new Set([...A].map(i=>T[i][0])).size===A.size&&new Set([...A].map(i=>T[i][1])).size===A.size,"lift not matching");
    return [...A];
  }
  function enums(T,n){const out=[];const rows=Array.from({length:n},(_,x)=>T.map((t,i)=>[t,i]).filter(([t])=>t[0]===x).map(([,i])=>i));function go(x,Y,M){if(x===n){out.push(M);return}for(const i of rows[x])if(!Y.has(T[i][1]))go(x+1,new Set([...Y,T[i][1]]),[...M,i])}go(0,new Set(),[]);return out}
  function lane(S,l,guard=false){return S.map((t,i)=>[t[l[0]],t[l[1]],(1n<<BigInt(t[l[2]]))^(guard?BigInt(i%4)<<BigInt(Math.max(...S.flat())+1):0n)])}
  const lanes=[[0,1,2],[0,2,1],[1,2,0]];
  function sourceClosure(S,n){let T=S.slice();for(;;){for(let j=0;j<3;j++)for(let v=0;v<n;v++)if(!T.some(t=>t[j]===v))return null;
      const drop=new Set();for(let j=0;j<3;j++)for(let v=0;v<n;v++){const ids=T.map((t,i)=>t[j]===v?i:-1).filter(i=>i>=0);if(ids.length===1){const i=ids[0];T.forEach((t,k)=>{if(k!==i&&t.some((w,a)=>w===T[i][a]))drop.add(k)})}}
      for(const l of lanes){const G=lane(T,l);if(!pm(G,n))return null;for(let i=0;i<T.length;i++)if(!pm(G,n,i))drop.add(i)}
      if(!drop.size)return T;T=T.filter((t,i)=>!drop.has(i));
    }}
  function ref(T,n,C){const M=enums(T,n),S=new Set(M.map(q=>String(sig(T,q)))),Q=new Map();for(const q of M)Q.set(String(C.reduce(sig(T,q))),q);for(const s of S){const a=BigInt(s);for(const step of C.steps){/* steps are quotient directions, test full preimage by lift below */}const w=Q.get(String(C.reduce(a)));lift(T,w,a,C)}
    const d=Math.max(1,...T.map(t=>t[2].toString(2).length));
    for(let t=0n;t<(1n<<BigInt(d));t++){const w=Q.get(String(C.reduce(t)));assert(S.has(String(t))===Boolean(w),"quotient mismatch");if(w)lift(T,w,t,C)}
    return {matchings:M.length,support:[...S].map(Number).sort((a,b)=>a-b),quotient:Q.size,rank:C.H.length,steps:C.steps.map(s=>({pivot:s.x,p:String(s.p),branchLengths:[...s.byPin].map(([i,D])=>[i,D.get(String(s.p))?.old.length])}))}
  }
  const V=[[0,0,1],[0,1,1],[0,2,2],[1,0,1],[1,1,0],[2,0,2],[2,2,2],[2,3,3],[3,2,0],[3,3,3]];
  const U=V.filter(t=>String(t)!=="2,2,2");
  const fixtures=[];
  for(const [name,S] of [["V",V],["U",U]]){
    assert(sourceClosure(S,4)?.length===S.length,"fixture changed by closure");
    for(const l of lanes){const T=lane(S,l),C=closure(T,4);const r=ref(T,4,C);fixtures.push({name,lane:l.join(""),...r});assert(r.support.includes(15)===(name==="V"),"source neighbor label")}
  }
  // Full octahedron face gluing creates genuine planar source subsets. Retain IDs.
  function oct(n){let T=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)T.push([a,b,c]);for(let k=2;k<n;k++){const j=Math.floor(rand()*T.length),f=T.splice(j,1)[0];for(let mask=1;mask<8;mask++)T.push(f.map((v,i)=>(mask>>i&1)?k:v))}return T.filter(()=>rand()<.83)}
  let jobs=0,closed=0,no=0,positive=0,periods=0,guardJobs=0;
  for(let z=0;z<90;z++){const n=2+z%4,S=oct(n),base=lane(S,lanes[0]),truth=enums(base,n).some(M=>sig(base,M)===(1n<<BigInt(n))-1n);const R=sourceClosure(S,n);if(!R){assert(!truth,"closure lost source witness");no++;continue;}closed++;if(truth)positive++;
    for(const l of lanes){for(const guard of [false,true]){const T=lane(R,l,guard),C=closure(T,n);const r=ref(T,n,C);periods+=r.rank;jobs++;if(guard)guardJobs++;if(!guard)assert(r.support.includes((1<<n)-1)===truth,"closure changes source truth")}}
  }
  // Scalable products: no global support table. Certify each actual component, then lift all blocks.
  const scales=[];
  for(const k of [4,16,64])for(const bad of [false,true]){
    let T=[],target=0n,matched=[],rank=0;
    for(let j=0;j<k;j++){const S=bad&&j===k-1?U:V,G=lane(S,lanes[0]),C=closure(G,4);rank+=C.H.length;const M=enums(G,4).find(m=>C.reduce(sig(G,m))===C.reduce(15n));if(M){const A=lift(G,M,15n,C);matched.push(...A.map(i=>i+T.length))}T.push(...S.map(t=>[t[0]+4*j,t[1]+4*j,1n<<BigInt(t[2]+4*j)]));target|=15n<<BigInt(4*j)}
    assert((matched.length===4*k)===( !bad),"scaled label");if(!bad)assert(sig(T,matched)===target,"scaled lift");scales.push({blocks:k,triples:T.length,bad,rank,rawSupportLower:"2^"+(2*k-(bad?1:0)),definite:bad?"NO":"YES"});
  }
  return {seed:261125,checks,matchingCalls:calls,reverseSwitches:lifts,random:{sources:90,closed,no,positive,laneGuardJobs:jobs,guardJobs,certifiedIndependentPeriods:periods},fixtures,scales};
};
console.log(JSON.stringify(audit(),null,2));

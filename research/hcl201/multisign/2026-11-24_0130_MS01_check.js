"use strict";
function experiment(){
  let state=20261124,rand=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n};
  const bit=i=>1n<<BigInt(i), has=(x,i)=>!!(x&bit(i));
  function ok(x,C){return C.every(([a,b])=>has(x,a>>1)==Boolean(a&1)||has(x,b>>1)==Boolean(b&1))}
  function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
  function basis(xs){let B=new Map();for(let x of xs){while(x){let p=x.toString(2).length-1;if(B.has(p))x^=B.get(p);else{B.set(p,x);break}}}return B}
  function reduce(x,B){for(const p of [...B.keys()].sort((a,b)=>b-a))if(has(x,p))x^=B.get(p);return x}
  function orth(B,n){let A=[];for(let f=0;f<n;f++)if(!B.has(f)){let x=bit(f);for(const p of [...B.keys()].sort((a,b)=>a-b))if(parity(B.get(p)&x))x|=bit(p);A.push(x)}return A}
  function prep(n,C){
    let R=Array.from({length:2*n},(_,i)=>bit(i));for(const[a,b]of C){R[a^1]|=bit(b);R[b^1]|=bit(a)}
    for(let k=0;k<2*n;k++)for(let i=0;i<2*n;i++)if(has(R[i],k))R[i]|=R[k];
    for(let i=0;i<n;i++)if(has(R[2*i],2*i+1)&&has(R[2*i+1],2*i))return null;
    function consistent(s){for(let i=0;i<n;i++)if(has(s,2*i)&&has(s,2*i+1))return false;return true}
    let t=0n;for(let i=0;i<n;i++)if(!has(t,2*i)&&!has(t,2*i+1)){let u=t|R[2*i];t=consistent(u)?u:t|R[2*i+1];if(!consistent(t))throw Error("baseline");}
    let a=0n;for(let i=0;i<n;i++)if(has(t,2*i+1))a|=bit(i);if(!ok(a,C))throw Error("baseline check");
    let masks=new Set();for(let i=0;i<n;i++){let r=R[2*i+(has(a,i)?0:1)];if(!consistent(r))continue;let x=0n;for(let j=0;j<n;j++)if(has(r,2*j+(has(a,j)?0:1)))x|=bit(j);if(!ok(a^x,C))throw Error("closure");masks.add(x)}
    return {a,masks:[...masks],B:basis(masks)};
  }
  let queries=0,candidates=0,maxSeeds=0,hullRejects=0;
  function solve(n,C,rows,target,P=prep(n,C)){
    queries++;if(!P)return null;
    const tag=x=>rows.reduce((s,r,i)=>s|(BigInt(parity(x&r))<<BigInt(i)),0n);
    let t=target^tag(P.a);let images=basis([...P.B.values()].map(tag));
    if(reduce(t,images)){hullRejects++;return null}
    let k=images.size;
    function search(start,x,depth,used){candidates++;if(!ok(P.a^x,C))return null;
      if(tag(x)===t){maxSeeds=Math.max(maxSeeds,used);return P.a^x}
      if(!depth)return null;
      for(let i=start;i<P.masks.length;i++){let y=x|P.masks[i];if(y===x)continue;let z=search(i+1,y,depth-1,used+1);if(z!==null)return z}return null;
    }
    return search(0,0n,k,0)
  }
  function hull(n,C,rows,target,P){
    let a=solve(n,C,rows,target,P);if(a===null)return null;let B=new Map();
    while(true){let found=false;for(const u of orth(B,n)){let b=BigInt(1^parity(u&a));let w=solve(n,C,[...rows,u],target|(b<<BigInt(rows.length)),P);if(w!==null){B=basis([...B.values(),w^a]);found=true;break}}if(!found)return {a,B}}
  }
  let stats={seed:20261124,instances:0,baseUnsat:0,decisions:0,sat:0,unsat:0,affineChecks:0,affineRankReduction:0,baseHullChecks:0,disagreements:0,controls:[]};
  function check(n,C,rows,doHull=true){
    stats.instances++;let P=prep(n,C),sol=[];for(let x=0n;x<bit(n);x++)if(ok(x,C))sol.push(x);
    if(!sol.length)stats.baseUnsat++;
    if(Boolean(P)!==Boolean(sol.length))throw Error("base status");
    if(P){let B=basis(sol.map(x=>x^P.a));if(B.size!==P.B.size||[...B.values()].some(x=>reduce(x,P.B)))throw Error("base hull");stats.baseHullChecks++}
    const tag=x=>rows.reduce((s,r,i)=>s|(BigInt(parity(x&r))<<BigInt(i)),0n);
    for(let t=0n;t<bit(rows.length);t++){let S=sol.filter(x=>tag(x)===t),w=solve(n,C,rows,t,P);
      stats.decisions++;if(S.length)stats.sat++;else stats.unsat++;
      if((w!==null)!==Boolean(S.length)||w!==null&&(!ok(w,C)||tag(w)!==t))throw Error("decision");
      if(doHull){let H=hull(n,C,rows,t,P);stats.affineChecks++;if(Boolean(H)!==Boolean(S.length))throw Error("hull status");
        if(H){let B=basis(S.map(x=>x^H.a));if(B.size!==H.B.size||[...B.values()].some(x=>reduce(x,H.B)))throw Error("fiber hull");let naive=P.B.size-basis([...P.B.values()].map(tag)).size;if(H.B.size<naive)stats.affineRankReduction++}}
    }
  }
  for(let z=0;z<300;z++){let n=3+rand(7),m=rand(3*n+1),k=rand(4),C=[];for(let j=0;j<m;j++)C.push([rand(2*n),rand(2*n)]);let rows=Array.from({length:k},()=>BigInt(rand(1<<n)));check(n,C,rows,z<120)}
  check(2,[[0,2]],[1n,2n]); // forbid both true: rank-two hole
  check(4,[[0,3],[2,5],[4,7]],[15n]); // implication chain
  // Multicolored clique reduction: at most one per color, conflict pairs between colors.
  for(let z=0;z<30;z++){let k=3,p=3,n=k*p,C=[],rows=[];
    for(let i=0;i<k;i++){let r=0n;for(let j=0;j<p;j++){r|=bit(i*p+j);for(let l=j+1;l<p;l++)C.push([2*(i*p+j),2*(i*p+l)])}rows.push(r)}
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(Math.floor(i/p)!==Math.floor(j/p)&&rand(3)===0)C.push([2*i,2*j]);check(n,C,rows,false)
  }
  for(const n of [16,32,64,128]){let C=Array.from({length:n-1},(_,i)=>[2*i,2*(i+1)+1]);let P=prep(n,C),row=bit(0);let q0=candidates;let x=solve(n,C,[row],1n,P);if(x!==bit(n)-1n)throw Error("long chain");stats.controls.push({n,rank:1,requiredFlips:n,closureMasks:P.masks.length,candidates:candidates-q0})}
  return {...stats,queries,candidates,maxSeeds,hullRejects};
}
console.log(JSON.stringify(experiment(),null,2));

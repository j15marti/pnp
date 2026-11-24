function experiment(){
 let seed=20261124;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 function bit(i){return 1n<<BigInt(i)}
 function subsets(n,k){const a=[];function f(i,m,j){a.push([m,j]);if(j<k)for(let t=i;t<n;t++)f(t+1,m|bit(t),j+1)}f(0,0n,0);return a}
 function feature(x,ms){let z=0n;for(let i=0;i<ms.length;i++)if((x&ms[i][0])===ms[i][0])z|=bit(i);return z}
 function insert(b,x){while(x){const p=x&-x;if(b.has(p))x^=b.get(p);else{b.set(p,x);return true}}return false}
 function rank(xs,d,k){const b=new Map(),ms=subsets(d,k);for(const x of xs)insert(b,feature(x,ms));return b.size}
 function xor(gs,m){let z=0n;for(let i=0;i<gs.length;i++)if(m&bit(i))z^=gs[i];return z}
 function normalize(gs,r,d){const piv=[];for(let i=0;i<gs.length;i++){let x=gs[i],m=bit(i);for(let j=0;j<r+d;j++)if(x&bit(j)){if(piv[j]){x^=piv[j][0];m^=piv[j][1]}else{piv[j]=[x,m];break}}}
 function reduce(x,limit){let m=0n;for(let j=0;j<limit;j++)if(piv[j]&&(x&bit(j))){x^=piv[j][0];m^=piv[j][1]}return [x,m]}
 return {reduce,K:piv.slice(r).filter(Boolean)}}
 function solve(bs,gs,r,d,t,k){const {reduce,K}=normalize(gs,r,d),mask=bit(r)-1n,[tr,tc]=reduce(t,r),rest=tr&mask,hs=new Map();for(let i=0;i<bs.length;i++){const [z,c]=reduce(bs[i],r+d);if((z&mask)===rest&&!hs.has(z>>BigInt(r)))hs.set(z>>BigInt(r),[i,c])}
 const H=[...hs.keys()],R=[],ranks=[];for(let j=0;j<=k;j++){const ms=subsets(d,j),b=new Map(),reps=[];for(const h of [...(R[j-1]||[]),...H])if(insert(b,feature(h,ms)))reps.push(h);R.push(reps);ranks.push(reps.length)}
 const out=[];for(const [m,j] of subsets(K.length,k)){let kc=0n;for(let i=0;i<K.length;i++)if(m&bit(i))kc^=K[i][1];for(const h of R[k-j]){const [i,c]=hs.get(h),coeff=c^tc^kc,z=bs[i]^xor(gs,coeff);if((z&mask)!==t)throw Error("bad target");const want=h^((tr>>BigInt(r)))^(xor(gs,kc)>>BigInt(r));if((z>>BigInt(r))!==want)throw Error("bad lift");out.push([i,coeff,z>>BigInt(r)])}}
 return {out,ranks,kernel:K.length,core:H.length}}
 function assert(v,s){if(!v)throw Error(s)}
 const result={seed:20261124,randomSystems:180,targetChecks:0,sat:0,unsat:0,featureChecks:0,witnessChecks:0,rankDropsIfOneWitness:0,scaling:[],negativeControls:{}};
 for(let z=0;z<180;z++){const r=1+rng(4),d=2+rng(6),g=rng(8),bs=Array.from({length:1+rng(9)},()=>BigInt(rng(2**(r+d)))),gs=Array.from({length:g},()=>BigInt(rng(2**(r+d))));const mask=bit(r)-1n,full=Array.from({length:2**r},()=>new Set());for(const b of bs)for(let m=0;m<2**g;m++){const x=b^xor(gs,BigInt(m));full[Number(x&mask)].add(x>>BigInt(r))}
 for(let t=0;t<2**r;t++){result.targetChecks++;const ref=[...full[t]];if(ref.length)result.sat++;else result.unsat++;for(let k=1;k<=3;k++){const a=solve(bs,gs,r,d,BigInt(t),k),got=a.out.map(x=>x[2]),rr=rank(ref,d,k);assert(got.every(x=>full[t].has(x)),"not genuine");assert(rank(got,d,k)===rr&&got.length===rr,"rank mismatch");result.featureChecks++;result.witnessChecks+=got.length;if(k===1&&rr>1)result.rankDropsIfOneWitness++;}}}
 // S02 disjointification counterexample: two singleton factors, target 0.
 assert(rank([0n,3n],2,1)===2&&rank([0n],2,1)===1,"S02 control");
 result.negativeControls={S02OriginalAffineRank:2,S02DisjointOnlyAffineRank:1};
 // Actual tagged perfect matchings: K4 core plus g disjoint K2,2 components.
 // K4 has matchings 01|23,02|13,03|12, tagged (s,p)=(0,0),(0,1),(1,0).
 // Each K2,2 matching orientation contributes one generator; its other orientation contributes 0.
 for(const g of [4,8,16,32,64]){const mixed=2,r=4,d=g-mixed+1,bs=[0n,bit(r),1n],gs=[];for(let i=0;i<g;i++)gs.push(i<mixed?bit(2+i)|bit(r):bit(r+1+i-mixed));
 const t=12n,sol=solve(bs,gs,r,d,t,2),no=solve(bs,gs,r,d,14n,2);assert(no.out.length===0,"UNSAT control");let checked=0;
 for(const [i,c,p] of sol.out){const core=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]][i],edges=core.slice();for(let j=0;j<g;j++){const o=4+4*j;edges.push(...((c&bit(j))?[[o,o+3],[o+1,o+2]]:[[o,o+2],[o+1,o+3]]))}const vertices=edges.flat();assert(new Set(vertices).size===4+4*g&&vertices.length===4+4*g,"matching lift");assert((bs[i]^xor(gs,c))===(t|(p<<BigInt(r))),"tag lift");checked++}
 const expected=1+d+d*(d-1)/2;assert(checked===expected,"scale expected rank");result.scaling.push({switches:g,vertices:4+4*g,kernel:sol.kernel,core:sol.core,degree2Witnesses:checked,fullTargetWitnesses:String(2n**BigInt(d)),unsatVerified:no.out.length===0})}
 return result
}
console.log(JSON.stringify(experiment(),null,2));

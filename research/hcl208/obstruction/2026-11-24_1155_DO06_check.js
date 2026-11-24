function main(){
 const out={systems:0,sourceSAT:0,sourceUNSAT:0,fibers:0,missing:0,ambientWords:0,guardQueries:0,verifiedLifts:0,slotSystems:0,closurePins:0,assertions:0,neighbors:[]};
 const check=(p)=>{out.assertions++;if(!p)throw Error("assertion "+out.assertions)};
 const bit=(x,i)=>(x>>>i)&1, parity=x=>{let s=0;while(x){s^=1;x&=x-1}return s};
 function basisInsert(B,v){while(v){let p=31-Math.clz32(v);if(B[p])v^=B[p];else{B[p]=v;return}}}
 function solve(D,eq){out.slotSystems++;let B=Array(D).fill(null);for(let [a,b] of eq){while(a){let p=31-Math.clz32(a);if(!B[p]){B[p]=[a,b];break}a^=B[p][0];b^=B[p][1]}if(!a&&b)return null}
  function extend(f,hom){for(let p=0;p<D;p++)if(B[p]){let [a,b]=B[p];if(parity(a&f)!==(hom?0:b))f^=1<<p}return f}
  let a=extend(0,false),vs=[];for(let i=0;i<D;i++)if(!B[i])vs.push(extend(1<<i,true));return {a,vs,count:2**vs.length}}
 function build(n,F,t){let q=n+t,r=Math.ceil(Math.log2(F.length+t)),L=2**r,slots=[];for(let j=0;j<L;j++){let C=j<F.length?F[j]:[[n+Math.min(j-F.length,t-1),1]];slots.push(C)}return {n,q,r,L,D:q+r,slots,F,t}}
 function query(P,guard){let count=0,a=null,B=Array(P.D).fill(0);for(let j=0;j<P.L;j++){let E=guard.concat(P.slots[j].map(([v,b])=>[1<<v,1-b]));for(let k=0;k<P.r;k++)E.push([1<<(P.q+k),bit(j,k)]);let s=solve(P.D,E);if(!s)continue;count+=s.count;if(a===null)a=s.a;else basisInsert(B,a^s.a);for(let v of s.vs)basisInsert(B,v)}
  // Exact affine closure of union of disjoint slot cubes. No search branching.
  let span=B.reduce((x,y)=>x|y,0),pins=[];if(a!==null)for(let i=0;i<P.D;i++)if(!bit(span,i))pins.push([1<<i,bit(a,i)]);
  out.closurePins+=pins.length;return {count,a,B,pins}}
 function legal(P,w){let j=w>>>P.q;return !P.slots[j].some(([v,b])=>bit(w,v)===b)}
 function src(P,x){return P.F.every(C=>C.some(([v,b])=>bit(x,v)===b))}
 function audit(n,F,t=2){let P=build(n,F,t);out.systems++;let N=2**P.D,Q=2**P.q,words=[],hist={},bad=0,srcCount=0;
 for(let x=0;x<2**n;x++)if(src(P,x))srcCount++;
 out[srcCount?"sourceSAT":"sourceUNSAT"]++;
 for(let w=0;w<N;w++){let j=w>>>P.q,pat=P.slots[j].map(([v,b])=>+(bit(w,v)===b)).join("");let key=pat.includes("1")?j+":"+pat:"zero";hist[key]=(hist[key]||0)+1;if(legal(P,w))words.push(w);out.ambientWords++}
 let root=query(P,[]);check(root.count===words.length);check(root.B.filter(Boolean).length===P.D);check(root.pins.length===0);
 for(let x=0;x<Q;x++){let G=Array.from({length:P.q},(_,i)=>[1<<i,bit(x,i)]),a=query(P,G),ref=0;for(let j=0;j<P.L;j++)if(legal(P,x+(j<<P.q)))ref++;check(a.count===ref);let missing=src(P,x)&&((x>>>n)===(2**t-1));check((a.count===0)===missing);out.fibers++;if(!a.count){bad++;out.missing++}else{check(legal(P,a.a)&&((a.a&(Q-1))===x));out.verifiedLifts++}}
 check(bad===srcCount);
 for(let i=0;i<P.D;i++){let mask=(1<<i)|(1<<((i+1)%P.D));for(let b=0;b<2;b++){let G=[[mask,b]],a=query(P,G),ref=words.filter(w=>parity(w&mask)===b);out.guardQueries++;check(a.count===ref.length);if(ref.length){check(ref.includes(a.a));for(let [p,c] of a.pins)check(ref.every(w=>parity(w&p)===c));let basis=Array(P.D).fill(0);for(let w of ref)basisInsert(basis,w^ref[0]);check(basis.filter(Boolean).length===a.B.filter(Boolean).length)}}}
 return {sourceModels:srcCount,missing:bad,models:root.count,events:P.slots.reduce((s,C)=>s+C.length,0),hist}
 }
 let cube=Array.from({length:8},(_,j)=>Array.from({length:3},(_,i)=>[i,bit(j,i)]));let root;
 for(let mask=0;mask<256;mask++){let a=audit(3,cube.filter((_,i)=>bit(mask,i)));if(mask===255)root=a}
 for(let j=0;j<8;j++){let C=cube.map((c,i)=>c.map(([v,b],k)=>[v,i===j&&k===0?1-b:b]));let a=audit(3,C);check(a.sourceModels===1&&root.sourceModels===0);check(a.models===root.models);check(JSON.stringify(Object.entries(a.hist).sort())===JSON.stringify(Object.entries(root.hist).sort()));out.neighbors.push({clause:j,rootModels:root.models,neighborModels:a.models,rootMissing:root.missing,neighborMissing:a.missing})}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(C=>[0,1].map(b=>C.map(v=>[v,b])));let f=audit(7,fano);check(f.sourceModels===0);out.fano={root:f.sourceModels,neighbors:[]};for(let j=0;j<14;j++){let a=audit(7,fano.filter((_,i)=>i!==j));check(a.sourceModels===5);out.fano.neighbors.push(a.sourceModels)}
 return out
}
console.log(JSON.stringify(main(),null,2));

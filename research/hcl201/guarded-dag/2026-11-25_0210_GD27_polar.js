// node GD27_polar.js /path/to/2026-11-24_2315_BW17_frozen.json
const fs=require("fs");
function test(data){
 const bit=i=>1n<<BigInt(i);let checks=0;
 const assert=(ok,msg)=>{checks++;if(!ok)throw Error(msg)};
 function rank(V){let B=new Map();for(let a of V){while(a){let k=a&-a;if(!B.has(k)){B.set(k,a);break}a^=B.get(k)}}return B.size}
 function checkChart(n,C,exhaustive){let A=Array.from({length:n},()=>new Set());let V=C.map(c=>{let a=c.map(x=>Math.abs(x)-1);assert(new Set(a).size===3,"distinct");let [u,v,w]=a;for(const [i,j] of [[u,v],[u,w],[v,w]]){A[i].add(j);A[j].add(i)}return[bit(u)^bit(v),bit(u)^bit(w)]});
 let removals=[];for(let skip=-1;skip<n;skip++){let first=Array.from({length:n},(_,i)=>i).find(i=>i!==skip);let seen=new Set([first]),Q=[first];for(let i=0;i<Q.length;i++)for(let j of A[Q[i]])if(j!==skip&&!seen.has(j)){Q.push(j);seen.add(j)}removals.push({skip,reachable:seen.size});assert(seen.size===n-Number(skip>=0),"2-connectivity")}
 let cuts=0,min=Infinity,allRank=rank(V.flat());function cut(S){let L=[],R=[];V.forEach((p,i)=>(S.has(i)?L:R).push(...p));let d=rank(L)+rank(R)-allRank;cuts++;min=Math.min(min,d);assert(d>=1,"nontrivial intersection")}
 if(exhaustive){for(let b=1;b<(1<<V.length)-1;b++)cut(new Set(V.map((_,i)=>i).filter(i=>b&(1<<i))))}
 else{for(let i=0;i<V.length;i++){cut(new Set([i]));for(let j=i+1;j<V.length;j++)cut(new Set([i,j]))}let seed=271125;for(let t=0;t<256;t++){let S=new Set();for(let i=0;i<V.length;i++){seed=(Math.imul(1664525,seed)+1013904223)>>>0;if(seed>>>31)S.add(i)}if(S.size&&S.size<V.length)cut(S)}}
 assert(allRank===n-1,"connected span");return{n,owners:C.length,edgeCount:A.reduce((s,x)=>s+x.size,0)/2,rank:allRank,articulationVertices:[],removals,cuts,minIntersection:min,quadraticRanks:C.map(()=>2)}}
 const F=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 return {Fano:checkChart(7,F,true),BW17:checkChart(data.n,data.O.map(o=>o.t.map(v=>v+1)),false),get checks(){return checks}}
}
console.log(JSON.stringify(test(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));

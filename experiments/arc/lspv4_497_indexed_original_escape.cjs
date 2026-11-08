'use strict';
// LSPV-4/497 independent Node.js controls for original signed cubic Tseitin sources.
// FINITE controls only. This is not a native FLMV machine or R_mix341 checker.
let assertions=0, rawReads=0, naiveFalse=0;
function eq(a,b,msg){assertions++;if(a!==b) throw new Error(msg+': '+JSON.stringify([a,b]));}
function instance(H,edges,matching,A,B,align=false){
 let left=Array.from(new Set(matching.map(x=>x[0]))).sort((x,y)=>x-y);
 let right=Array.from(new Set(matching.map(x=>x[1]))).sort((x,y)=>x-y), M=H/2;
 let index=new Map(matching.map(([u,v],i)=>[[u,v].sort((a,b)=>a-b).join(','),i]));
 let names=Array.from({length:H},()=>[]),n=H+1;
 for(const [u,v] of edges){let k=[u,v].sort((a,b)=>a-b).join(','),j=index.get(k);
  if(j===undefined){names[u].push(n);names[v].push(n);n++}
  else{let ul=left.includes(u);names[u].push(2*j+1+((ul?A:B)>>j&1));names[v].push(2*j+1+((ul?B:A)>>j&1));}}
 eq(n,2*H+1,'fixed IDs');
 const order=align?matching.map(x=>x[0]).concat(matching.map(x=>x[1])):left.concat(right);
 let charges=Array(H).fill(0);charges[left[0]]=1;
 let W=Math.ceil(Math.log2(2*H+1)), s='11100011'+'1'.repeat(H)+'0'+'1'.repeat(2*H)+'0';
 for(const v of order){let ids=[...names[v]].sort((a,b)=>a-b);eq(ids.length,3,'arity');
 for(let z=0;z<8;z++){let bit=[z>>2&1,z>>1&1,z&1];if((bit[0]^bit[1]^bit[2])===charges[v])continue;
 for(let i=0;i<3;i++)s+=bit[i]?'1':'0',s+=ids[i].toString(2).padStart(W,'0');}}
 s+='10';eq(s.length,3*H+12+12*H*(W+1),'encoding length');
 return {H,M,W,s,order};
}
function id(v,side,j){let q=3*v.H+10 + (12*(v.W+1))*(side*v.M+j)+1;rawReads+=v.W;return parseInt(v.s.slice(q,q+v.W),2)}
function scan(v){for(let j=0;j<v.M;j++){let val=[];
 for(let side=0;side<2;side++) {let found=[];for(let p=0;p<v.M;p++) {let x=id(v,side,p);if(Math.floor((x-1)/2)===j)found.push(x)}eq(found.length,1,'matched singleton');val.push(found[0])}
 if(val[0]!==val[1])return true;
}return false}
function align(v){for(let j=0;j<v.M;j++){let a=id(v,0,j),b=id(v,1,j);eq(Math.floor((a-1)/2),j,'left label');eq(Math.floor((b-1)/2),j,'right label');if(a!==b)return true;}return false}
function naive(v){for(let j=0;j<v.M;j++) if(id(v,0,j)!==id(v,1,j))return true;return false}
const families=[
 {name:'K3,3',H:6,edges:Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3]),match:[[0,5],[1,3],[2,4]]},
 {name:'Cube',H:8,edges:Array.from({length:8},(_,i)=>[0,1,2].map(b=>[i,i^(1<<b)]).filter(x=>x[0]<x[1])).flat(),match:[[0,1],[3,2],[5,4],[6,7]]},
 {name:'Heawood',H:14,edges:Array.from({length:7},(_,i)=>[0,1,3].map(j=>[i,7+(i+j)%7])).flat(),match:Array.from({length:7},(_,i)=>[i,7+i])}
];
const summary=[];
for(const f of families){let m=f.H/2,pairs=[];if(m<=4){for(let a=0;a<1<<m;a++)for(let b=0;b<1<<m;b++)pairs.push([a,b])}
 else {for(let a=0;a<1<<m;a++)pairs.push([a,a]);for(let a=0;a<100;a++)pairs.push([a%128,(a*37+1)%128]);}
 for(const [a,b] of pairs){let v=instance(f.H,f.edges,f.match,a,b),w=instance(f.H,f.edges,f.match,a,b,true);
  eq(scan(v),a!==b,'original parser promise');eq(align(w),a!==b,'aligned reordered packets');
  if(a===b && naive(v))naiveFalse++;
 }
 summary.push({name:f.name,pairs:pairs.length,sourceBits:instance(f.H,f.edges,f.match,0,0).s.length});
}
if(!naiveFalse)throw new Error('missing hostile counterexample');
console.log(JSON.stringify({artifact:'LSPV4_497_INDEPENDENT_JS',assertions,rawReads,naiveFalse,summary,native_FLMV:false},null,2));

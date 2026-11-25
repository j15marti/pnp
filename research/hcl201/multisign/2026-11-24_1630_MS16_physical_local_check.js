"use strict";
function supplement(){
 let assertions=0,localAssignments=0,localLifts=0;const ok=(x)=>{assertions++;if(!x)throw Error("supplement failure")};
 function k4Valid(p,c){return c[0]!==p&&c.slice(1).every(x=>x!==0)&&new Set(c).size===4}
 for(let p=0;p<4;p++){let count=0;for(let x=0;x<256;x++){const c=[0,1,2,3].map(j=>(x>>(2*j))&3);localAssignments++;if(k4Valid(p,c))count++}ok(count===(p?6:0));if(p){ok(k4Valid(p,[0,1,2,3]));localLifts++}}
 const hull=[];
 for(const n of [4,8,16,32,64]){
   const edges=Array.from({length:n},(_,i)=>[i,(i+1)%n]);edges.push([0,2]);
   const all=(1n<<BigInt(n))-1n, words=[all,...Array.from({length:n},(_,i)=>all^(1n<<BigInt(i)))];
   const test=(w,a,b)=>Number((w>>BigInt(a))&1n)+2*Number((w>>BigInt(b))&1n);
   for(const w of words){for(const [a,b] of edges){const p=test(w,a,b);ok(p!==0&&k4Valid(p,[0,1,2,3]));localLifts++}}
   // For each omitted edge, solve the ordinary bipartite owner/endpoint
   // matching. Independent endpoint reps also certify rank Hall here.
   for(let omit=0;omit<edges.length;omit++){
     const owner=Array(n).fill(-1);
     function aug(i,seen){for(const v of edges[i])if(!seen[v]){seen[v]=true;if(owner[v]<0||aug(owner[v],seen)){owner[v]=i;return true}}return false}
     for(let i=0;i<edges.length;i++)if(i!==omit)ok(aug(i,Array(n).fill(false)));
   }
   hull.push({n,owners:n+1,legalAffineBasisWords:n+1,checkedSingleOwnerDeletions:n+1,deficiency:1,coreRank:n});
 }
 return {assertions,localAssignments,localLifts,hull,scope:"signed K4 four-port local adapter with zero internal signs; no global strict E4/B4 network, port consumer or integer quota acquisition"};
}
console.log(JSON.stringify(supplement(),null,2));

"use strict";
function masks(){
 const C={localCases:0,localSat:0,localUnsat:0,dpArcTests:0,lifts:0,maskCases:0,sourceAssignments:0,sourceModels:0,rootClosureScans:0,closureRowChecks:0,closureDeletions:0};
 function wheel(a,b,k,t,forbid){
  // spokes at one rim vertex swapped by a translation t.
  let L=Array.from({length:k},(_,i)=>{let A=a^(i===1?t:0),B=b^forbid^t^(i===1?t:0);return [0,1,2,3].filter(c=>c!==A&&c!==B)});
  for(let start of L[0]){let p=[null],prev=[start];for(let i=1;i<k;i++){let next=new Map();for(let v of L[i])for(let u of prev){C.dpArcTests++;if(v!==u){next.set(v,u);break}}p.push(next);prev=[...next.keys()]}
   for(let end of prev){C.dpArcTests++;if(end===start)continue;let w=Array(k);w[k-1]=end;for(let i=k-1;i>0;i--)w[i-1]=p[i].get(w[i]);if(!w.every((v,i)=>L[i].includes(v)&&v!==w[(i+1)%k]))throw Error("lift");C.lifts++;return true}
  }return false
 }
 for(let k of [3,5,31,257,4097])for(let t=1;t<4;t++)for(let d=0;d<4;d++)for(let a=0;a<4;a++)for(let b=0;b<4;b++){let z=wheel(a,b,k,t,d);C.localCases++;if(z)C.localSat++;else C.localUnsat++;if(z!==((a^b)!==d))throw Error("inequality")}
 let maskRows=[];for(let mask=0;mask<16;mask++){let accepted=0;for(let a=0;a<4;a++)for(let b=0;b<4;b++){let ok=true;for(let d=0;d<4;d++)if(!(mask&(1<<d)))if(!wheel(a,b,3,1,d))ok=false;C.maskCases++;if(ok!==!!(mask&(1<<(a^b))))throw Error("mask");accepted+=ok}maskRows.push({mask,accepted})}
 const edges=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)edges.push([i,j]);const graph=[];
 for(let deleted=-1;deleted<10;deleted++){
   const es=edges.filter((_,i)=>i!==deleted);
   // Certified domain-support closure on all compiled edge masks; repeat until stagnation.
   let D=Array.from({length:5},()=>[0,1,2,3]),change=true;
   while(change){change=false;for(const [i,j] of es){C.rootClosureScans++;for(const [u,v] of [[i,j],[j,i]]){const old=D[u],next=old.filter(a=>D[v].some(b=>{C.closureRowChecks++;return a!==b}));C.closureDeletions+=old.length-next.length;D[u]=next;if(old.length!==next.length)change=true}}}
   // Exhaustive independent source control, no claim of polynomial global solver.
   let count=0;for(let x=0;x<1024;x++){C.sourceAssignments++;let a=Array.from({length:5},(_,i)=>(x>>(2*i))&3);let ref=es.every(([u,v])=>a[u]!==a[v]),test=es.every(([u,v])=>wheel(a[u],a[v],3,1,0));if(ref!==test)throw Error("graph");if(test){count++;C.sourceModels++}}
   graph.push({deleted,models:count});
 }
 return {counts:C,maskRows,graph,discrepancies:0};
}
console.log(JSON.stringify(masks(),null,2));

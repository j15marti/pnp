// LSPV-2/489, independent self-contained JavaScript source cofactor verifier
// Fixed seed 489. No dependencies, no global semantic oracle, no native FLMV.
function independent489(){
  "use strict";
  const graphs = [
    ["K4",4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()],
    ["prism3",6,[...Array.from({length:3},(_,i)=>[i,(i+1)%3]),...Array.from({length:3},(_,i)=>[i+3,(i+1)%3+3]),...Array.from({length:3},(_,i)=>[i,i+3])]],
    ["cube",8,[...Array.from({length:4},(_,i)=>[i,(i+1)%4]),...Array.from({length:4},(_,i)=>[i+4,(i+1)%4+4]),...Array.from({length:4},(_,i)=>[i,i+4])]],
    ["Petersen",10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,i+5]),...Array.from({length:5},(_,i)=>[i+5,(i+2)%5+5])]]
  ];
  let seed=489;function rand(){seed=((seed*1664525)+1013904223)>>>0;return seed}
  let cases=0,checks=0;const details=[];
  for(const [name,n,edges] of graphs){
    const adj=Array.from({length:n},()=>[]);
    edges.forEach(([a,b],i)=>{adj[a].push(i);adj[b].push(i)});
    if(!adj.every(x=>x.length===3))throw Error("noncubic");
    const rows=[];
    for(let v=0;v<n;v++)for(let mask=0;mask<8;mask++){
      const bits=[mask&1,(mask>>1)&1,(mask>>2)&1];
      if((bits[0]^bits[1]^bits[2])!==(v===0?1:0))
        rows.push([v,adj[v].map((edge,j)=>[edge,bits[j]])]);
    }
    const num=name==="K4"?729:2400;let local=0;
    for(let t=0;t<num;t++){
      let state=Array(edges.length);
      if(name==="K4"){let a=t;for(let e=0;e<edges.length;e++){state[e]=(a%3)-1;a=Math.floor(a/3)}}
      else{for(let e=0;e<edges.length;e++)state[e]=(rand()%3)-1}
      const q=state.filter(x=>x===-1).length;
      const residual=rows.filter(row=>!row[1].some(([e,b])=>state[e]!==-1&&state[e]!==b))
        .map(row=>row[1].filter(([e])=>state[e]===-1));
      const untouched=adj.filter(a=>a.every(e=>state[e]===-1)).length;
      let bad=0;
      for(let v=0;v<n;v++)if(adj[v].every(e=>state[e]!==-1)){
        const p=adj[v].reduce((s,e)=>s^state[e],0);
        if(p!==(v===0?1:0))bad++;
      }
      if(residual.length!==2*q+untouched+bad)throw Error(`identity ${name} ${t} ${residual.length} ${2*q+untouched+bad}`);
      checks++;
      if(residual.length<2*q||residual.filter(a=>a.length===0).length!==bad)throw Error("bound/empty");
      checks+=2;
      const pinned=edges.length-q;
      if(residual.length<Math.max(0,4*n-4*pinned,3*n-2*pinned))throw Error("lower envelope");
      checks++;local++;cases++;
    }
    details.push({graph:name,vertices:n,originalClauses:rows.length,partialAssignments:local});
  }
  return {run:"LSPV-2/489",seed:489,partialAssignments:cases,assertions:checks,graphs:details,status:"PASS",qualification:"Independent in-memory JS. No native FLMV execution."};
}
const result=independent489();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));

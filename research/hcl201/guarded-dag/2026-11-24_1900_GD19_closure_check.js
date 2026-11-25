function closureAudit(){
 let ledger={scans:0,edgeTests:0,pins:0,assertions:0};
 const ok=(b,m)=>{ledger.assertions++;if(!b)throw Error(m)};
 function close(V,edges){let pins=new Map;
  for(;;){ledger.scans++;let states=edges.map(([u,v,g])=>{let rem=[];for(let [i,b] of g){ledger.edgeTests++;if(pins.has(i)){if(pins.get(i)!==b)return [u,v,-1,[]]}else rem.push([i,b])}return [u,v,rem.length?1:0,rem]});
   let P=Array(V).fill(false),M=Array(V).fill(false),B=Array(V).fill(false);P[0]=M[0]=B[V-1]=true;
   for(let [u,v,s] of states){if(s>=0&&P[u])P[v]=true;if(s===0&&M[u])M[v]=true}
   for(let j=states.length-1;j>=0;j--){let [u,v,s]=states[j];if(s===0&&B[v])B[u]=true}
   if(M[V-1])return {status:"UNSAT",pins:pins.size};
   if(!P[V-1])return {status:"SAT",pins:pins.size};
   let force=states.find(([u,v,s,r])=>s===1&&r.length===1&&M[u]&&B[v]);
   if(!force)return {status:"STAGNANT",pins:pins.size};
   let [i,b]=force[3][0];pins.set(i,b^1);ledger.pins++;
  }
 }
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],C=triples.flatMap(t=>[t.map(v=>[v,0]),t.map(v=>[v,1])]);
 let fano=0;for(let j=-1;j<C.length;j++){let E=C.filter((_,i)=>i!==j).map(g=>[0,1,g]);let r=close(2,E);ok(r.status==="STAGNANT"&&r.pins===0,"Fano closure");fano++}
 let scale=[];for(let n of [8,16,32,64])for(let root of [true,false]){let E=[[0,1,[[0,1]]],[0,1,[[0,root?0:1]]]];for(let i=1;i<n;i++)E.push([0,i+1,[[i,1]]]);for(let i=1;i<=n;i++)E.push([i,i+1,[]]);let r=close(n+2,E);ok(r.status===(root?"UNSAT":"SAT"),"scale closure");scale.push({n,root,...r})}
 let hostile=[];for(let n of [4,6,8]){let E=[];for(let i=0;i<n;i++)E.push([0,i+1,[[i,1]]]);for(let i=0;i<n;i++)E.push([i+1,n+1,[[n+i,1]]]);let r=close(n+2,E);ok(r.status==="STAGNANT"&&r.pins===0,"hostile closure");hostile.push({n,...r})}
 return {fano,scale,hostile,ledger}
}
console.log(JSON.stringify(closureAudit(),null,2));

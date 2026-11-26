function supplement(){
 let assertions=0;function ok(b,m){assertions++;if(!b)throw Error(m)}
 const H=[15,32,13,17,14,36,11,53,10,39],B=[99,168,306,564],A=H.map((_,i)=>B.reduce((a,v,j)=>a|((v>>i&1)<<j),0));
 const rowValues=[...new Set(A.flatMap((a,i)=>i%2===0?[a,A[i+1],a^A[i+1]]:[]))].sort((a,b)=>a-b),tri=[];
 for(let i=0;i<rowValues.length;i++)for(let j=i+1;j<rowValues.length;j++)for(let k=j+1;k<rowValues.length;k++)if(!(rowValues[i]^rowValues[j]^rowValues[k]))tri.push([i,j,k]);
 const E=rowValues.map((_,i)=>tri.map((t,j)=>t.includes(i)?j:-1).filter(j=>j>=0));ok(tri.length===6&&E.every(e=>e.length===2),"incidence");
 const left=[0,4,5];ok(E.every(e=>left.includes(e[0])!==left.includes(e[1]))&&new Set(E.map(e=>e.join())).size===9,"K33");
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};const syn=v=>H.reduce((a,h,i)=>a^((v>>i&1)?h:0),0);
 for(let v of B)ok(syn(v)===0,"kernel");
 const obs=Array.from({length:16},(_,x)=>rowValues.map(a=>parity(a&x)));
 for(let w of obs){let p=Array(6).fill(0);E.forEach(([u,v],i)=>{p[u]^=w[i];p[v]^=w[i]});ok(p.every(x=>!x),"cycle")}
 let targetMap=[],miss=[];const plane=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]];let attainable=new Set([0]);for(let P of plane)attainable=new Set([...attainable].flatMap(x=>P.map(y=>x^y)));
 for(let t=0;t<64;t++){let b=Array.from({length:1024},(_,i)=>i).find(v=>syn(v)===t);ok(b!==undefined,"target preimage");let F=[];for(let i=0;i<5;i++){let a=A[2*i],c=A[2*i+1],vv=[a,c,a^c],bb=[b>>(2*i)&1,b>>(2*i+1)&1,((b>>(2*i))^(b>>(2*i+1)))&1];let owner=tri.findIndex(q=>q.every(j=>vv.includes(rowValues[j])));ok(owner>=0,"owner");F.push({owner,pattern:tri[owner].reduce((z,j,k)=>z|(bb[vv.indexOf(rowValues[j])]<<k),0)})}
 let got=obs.some(w=>F.every(({owner,pattern})=>tri[owner].reduce((z,e,j)=>z|(w[e]<<j),0)!==pattern));ok(got===attainable.has(t),"atom all syndromes");if(!got){miss.push(t);targetMap.push({t,b,F})}}
 const pairs=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]];const row=([u,v])=>((u===4?0:1<<u)^(v===4?0:1<<v));let completed=new Set(pairs.flatMap(P=>{let a=row(P[0]),b=row(P[1]);return[a,b,a^b]}));ok(completed.size===15,"K5 PG(3,2)");ok([...Array(7)].every((_,i)=>completed.has(i+1)),"Fano");
 return {assertions,atom:{basis:B,rows:A,uniqueRows:rowValues,triangles:tri,edges:E,missing:miss,exceptionMapping:targetMap[0]},K5:{completedRows:completed.size,FanoRestriction:[1,2,3,4,5,6,7]}}
}
console.log(JSON.stringify(supplement(),null,2));

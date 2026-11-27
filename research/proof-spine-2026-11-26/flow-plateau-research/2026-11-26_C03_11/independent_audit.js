function audit(){
 const cases=[
 {name:"FP30",edges:[[0,10],[0,6],[0,2],[1,4],[1,7],[1,9],[2,8],[3,4],[3,6],[4,10],[5,7],[5,10],[6,7],[8,9],[11,12],[11,18],[11,14],[12,16],[13,15],[13,17],[14,19],[14,15],[16,19],[17,19],[17,18],[3,18],[9,13],[5,16],[8,15],[2,12]],f:[1,2,3,3,1,2,2,1,1,2,2,3,3,3,3,2,1,2,2,3,2,3,3,1,2,0,1,1,1,1],count:36},
 {name:"Petersen",edges:[[0,1],[0,4],[0,5],[1,2],[1,6],[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]],f:null,count:0}];
 const mod=x=>(x%3+3)%3,assert=(x)=>{if(!x)throw Error("audit")};
 return cases.map(j=>{
 const es=j.edges,n=Math.max(...es.flat())+1,m=es.length,adj=Array.from({length:n},()=>[]);
 es.forEach(([u,v],i)=>{adj[u].push(i);adj[v].push(i)});
 assert(adj.every(a=>a.length===3));
 if(j.f)assert(j.f.filter(x=>x===0).length===1&&adj.every(a=>a.reduce((x,i)=>x^j.f[i],0)===0));
 // Independent representation: unsigned incidence over F3, no spanning-tree chart equations.
 const D=adj.map(a=>Array.from({length:m},(_,i)=>+(a.includes(i))));
 const piv=[];let r=0;
 for(let k=0;k<m;k++){let t=D.findIndex((row,i)=>i>=r&&row[k]);if(t<0)continue;[D[t],D[r]]=[D[r],D[t]];let a=D[r][k];D[r]=D[r].map(x=>mod(a*x));for(let i=0;i<n;i++)if(i!==r&&D[i][k]){let b=D[i][k];D[i]=D[i].map((x,l)=>mod(x-b*D[r][l]))}piv.push(k);r++}
 const free=Array.from({length:m},(_,i)=>i).filter(i=>!piv.includes(i));const sset=new Set();let count=0,first=null;
 for(let k=0;k<3**free.length;k++){let t=k,g=Array(m).fill(0);for(let i of free){g[i]=t%3;t=Math.floor(t/3)}
 for(let i=0;i<r;i++)g[piv[i]]=mod(-free.reduce((a,l)=>a+D[i][l]*g[l],0));
 if(!adj.every(a=>new Set(a.map(i=>g[i])).size===3))continue;count++;if(!first)first=g.map(x=>x+1);
 const signs=adj.map(a=>{let c=j.f&&new Set(a.map(i=>j.f[i])).size===3&&a.every(i=>j.f[i])?a.map(i=>j.f[i]-1):[0,1,2];let u=c.indexOf(0),v=c.indexOf(1);return mod(g[a[v]]-g[a[u]])});
 sset.add(signs.join(""));
 }
 assert(count===j.count);assert(sset.size*3===count);
 let maj=null;let S=[...sset];for(let a of S)for(let b of S)for(let c of S){let w=Array.from(a,(x,i)=>+x+ +b[i]+ +c[i]>=5?2:1).join("");if(!sset.has(w)&&!maj)maj={a,b,c,w}}
 if(j.name==="FP30")assert(maj!==null);
 return {name:j.name,rank:r,assignments:3**free.length,colorings:count,signWords:sset.size,first,majorityCounterexample:maj};
 });
}
console.log(JSON.stringify(audit(),null,2));

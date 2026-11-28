// Independently check raw original port bits and enumerate signed-connected components on small NO control.
// Does not call the discovery UF, syndrome construction, rank tests or tree DP.
function verifyControl(G,cnf,rec){
 let net=G.network,n=4*net.types.length,edges=net.edges,types=net.types;
 function direct(bits){if(bits.length!==n||bits.some(x=>x!==0&&x!==1))return false;for(let [p,q,s] of edges)if((bits[p]^bits[q])!==s)return false;for(let v=0;v<types.length;v++){let z=bits.slice(4*v,4*v+4);if(types[v]==="E"?z.some(x=>x!==z[0]):z.reduce((a,b)=>a+b,0)!==2)return false}return true}
 let checks=[];for(let arm of rec.charts[0].arms)if(arm.status==="YES")checks.push({arm:arm.mode,valid:direct(arm.witness),ports:n});
 let rows=cnf.trimEnd().split("\n").slice(1).map(x=>x.split(/\s+/).map(Number).slice(0,-1));let cnfChecks=[];for(let arm of rec.charts[1].arms)if(arm.status==="YES"){let M=new Map(arm.witness);cnfChecks.push({arm:arm.mode,valid:rows.every(r=>r.some(l=>(M.get(Math.abs(l))??0)===+(l>0)))})}
 if(checks.length)return {checks,cnfChecks};
 let adj=Array.from({length:n},()=>[]);function edge(p,q,s){adj[p].push([q,s]);adj[q].push([p,s])}for(let [p,q,s] of edges)edge(p,q,s);for(let v=0;v<types.length;v++)if(types[v]==="E")for(let k=1;k<4;k++)edge(4*v,4*v+k,0);
 let comp=new Int32Array(n).fill(-1),sign=new Uint8Array(n),k=0;for(let p=0;p<n;p++)if(comp[p]===-1){comp[p]=k;let Q=[p];for(let i=0;i<Q.length;i++){let q=Q[i];for(let [r,s] of adj[q]){let b=sign[q]^s;if(comp[r]===-1){comp[r]=k;sign[r]=b;Q.push(r)}else if(comp[r]!==k||sign[r]!==b)return {inconsistentSignedGraph:true}}}k++}
 if(k>20)return {status:"UNKNOWN",components:k};
 let solutions=0;for(let w=0;w<2**k;w++){let bits=Array.from(comp,(x,i)=>((w>>x)&1)^sign[i]);if(direct(bits))solutions++}
 let cnfSolutions=0,m=Number(cnf.split(" ")[2]);for(let w=0;w<2**m;w++)if(rows.every(r=>r.some(l=>((w>>(Math.abs(l)-1))&1)===+(l>0))))cnfSolutions++;
 return {components:k,nativeWords:2**k,nativeSolutions:solutions,cnfWords:2**m,cnfSolutions}
}

function rankAudit(F){
 let factors=F.map(f=>f.a);if(factors.some(a=>a.length!==4))throw Error("width");let vars=[...new Set(factors.flat().map(Math.abs))].sort((a,b)=>a-b),n=vars.length,ids=new Map(vars.map((v,i)=>[v,i]));const bit=v=>1n<<BigInt(ids.get(Math.abs(v)));
 let work=0;function rank(rows){let b=new Map();for(let r of rows){while(r){work++;let k=r.toString(2).length-1;if(!b.has(k)){b.set(k,r);break}r^=b.get(k)}}return b.size}
 let A=factors.map(a=>a.reduce((r,v)=>r^bit(v),0n)),lower=rank(A),S=[],chosen=[];
 const match=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]];
 for(let a of factors){let best=null;for(let p of match){let E=p.map(([i,j])=>bit(a[i])^bit(a[j])),r=rank(S.concat(E));if(best===null||r<best.r)best={p,E,r}}S.push(...best.E);chosen.push(best.p)}
 let upper=rank(S);let parent=Array.from({length:n},(_,i)=>i);function root(i){while(parent[i]!==i)i=parent[i];return i}for(let i=0;i<factors.length;i++)for(let [a,b] of chosen[i]){let u=root(ids.get(Math.abs(factors[i][a]))),v=root(ids.get(Math.abs(factors[i][b])));if(u!==v)parent[v]=u}
 let blocks=new Map();for(let i=0;i<n;i++){let u=root(i);if(!blocks.has(u))blocks.set(u,[]);blocks.get(u).push(vars[i])}if(n-blocks.size!==upper)throw Error("rank graph");
 for(let a of factors){let ct=new Map();for(let v of a){let p=root(ids.get(Math.abs(v)));ct.set(p,(ct.get(p)||0)+1)}if([...ct.values()].some(x=>x%2))throw Error("block parity")}
 let tests=0;for(let word=0;word<16;word++)for(let p of match){let x=[0,1,2,3].map(i=>word>>i&1),[a,b]=p;let u=x[a[0]]^x[a[1]],v=x[b[0]]^x[b[1]],r=u||v||(x[a[0]]^x[b[0]]);if(!!r!==x.some(t=>t!==x[0]))throw Error("pair identity");tests++}
 return{n,factors:factors.length,lower,upper,nullity:n-lower,blocks:[...blocks.values()],chosen,factorWords:factors,truthChecks:tests,rankEvents:work}
}

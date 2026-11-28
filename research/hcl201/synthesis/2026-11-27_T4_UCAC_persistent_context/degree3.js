function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function algebra(C,U,maxSeeds=8,cap=350000){
 const V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),I=new Map(V.map((v,i)=>[v,i])),n=V.length,mono=[0n],M={n,features:0,generators:0,rowXor:0,queryXor:0,queries:0,verifyTerms:0,upVisits:0,admitted:0,failed:0},index=new Map();
 for(let i=0;i<n;i++)mono.push(1n<<BigInt(i));for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)mono.push((1n<<BigInt(i))|(1n<<BigInt(j)));for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)mono.push((1n<<BigInt(i))|(1n<<BigInt(j))|(1n<<BigInt(k)));
 mono.forEach((z,i)=>index.set(z,i));M.features=mono.length;
 const toggle=(T,v)=>T.has(v)?T.delete(v):T.add(v);
 function terms(c,m=0n){let T=new Set([m]);for(let l of c){let P=new Set(),z=1n<<BigInt(I.get(Math.abs(l)));for(let t of T){toggle(P,t|z);if(l>0)toggle(P,t)}T=P}return T}
 function vector(T){let x=0n;for(let t of T){let i=index.get(t);if(i===undefined)throw Error("degree");x^=1n<<BigInt(i)}return x}
 const gens=[],basis=new Map(),top=x=>x.toString(2).length-1;
 function insert(c,m){let id=gens.length;gens.push({clause:c,m:m.toString()});let x=vector(terms(C[c],m)),comb=1n<<BigInt(id);while(x){let j=top(x),b=basis.get(j);if(!b){basis.set(j,[x,comb]);break}x^=b[0];comb^=b[1];M.rowXor++;if(M.rowXor>cap)throw Error("CAP")}}
 for(let i=0;i<C.length;i++){let c=C[i];if(c.length>3)continue;insert(i,0n);if(c.length<=2)for(let j=0;j<n;j++)if(!c.some(l=>Math.abs(l)===V[j]))insert(i,1n<<BigInt(j))}
 M.generators=gens.length;
 function membership(c){let x=vector(terms(c)),comb=0n;while(x){let b=basis.get(top(x));if(!b)return null;x^=b[0];comb^=b[1];M.queryXor++;if(M.queryXor>cap)throw Error("CAP")}return comb}
 function independentlyVerify(c,ids){let acc=new Set();for(let id of ids){let g=gens[id];if(!g)throw Error("id");for(let t of terms(C[g.clause],BigInt(g.m))){M.verifyTerms++;toggle(acc,t)}}let target=terms(c);return acc.size===target.size&&[...target].every(t=>acc.has(t))}
 let seen=new Set(C.map(c=>c.join(","))),seeds=[],members=0,rup=0;const cand=[...V.flatMap(v=>[[-v],[v]]),...V.flatMap((v,i)=>V.slice(i+1).flatMap(u=>[-1,1].flatMap(a=>[-1,1].map(b=>[v*a,u*b]))))];
 for(let c of cand){if(seen.has(c.join(",")))continue;M.queries++;let z=membership(c);if(z===null){M.failed++;continue}members++;let w={n:0},q=new Map(c.map(l=>[Math.abs(l),+(l<0)])),isRup=!U.scalar(C,q,w);M.upVisits+=w.n;if(isRup){rup++;continue}let ids=[];for(let i=0;i<gens.length;i++)if(z&(1n<<BigInt(i)))ids.push(i);if(!independentlyVerify(c,ids))throw Error("polynomial mismatch");seeds.push({clause:c,terms:ids.map(i=>gens[i])});M.admitted++;if(seeds.length>=maxSeeds)break}
 return {rank:basis.size,M,members,rup,seeds};
}

function verifyAlgebra(C,seed){
 let V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),I=new Map(V.map((v,i)=>[v,i])),acc=new Map(),work=0;
 function expand(c,m){let P=[m];for(let l of c){let z=1n<<BigInt(I.get(Math.abs(l)));P=P.flatMap(t=>l>0?[t,t|z]:[t|z])}return P}
 function add(t){acc.set(t,(acc.get(t)??0)^1);work++}
 for(let a of seed.terms){if(!C[a.clause]||C[a.clause].length>3)throw Error("parent");for(let t of expand(C[a.clause],BigInt(a.m)))add(t)}
 for(let t of expand(seed.clause,0n))add(t);return{ok:[...acc.values()].every(x=>!x),work};
}
module.exports={algebra,verifyAlgebra};

function affineParity(C){
 let vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),groups=new Map(),tests=0,ops=0,eq=[];
 for(let j=0;j<C.length;j++){let c=C[j],V=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);if(V.length!==c.length||!V.length||V.length>10)continue;let k=V.join(","),w=c.reduce((a,l)=>a+(Number(l<0)<<V.indexOf(Math.abs(l))),0);if(!groups.has(k))groups.set(k,{V,rows:new Map()});groups.get(k).rows.set(w,j)}
 const parity=w=>{let p=0;while(w){w&=w-1;p^=1}return p};
 for(let {V,rows} of groups.values())for(let b=0;b<2;b++){let ids=[],ok=true;for(let w=0;w<2**V.length;w++)if(parity(w)!==b){tests++;if(!rows.has(w)){ok=false;break}ids.push(rows.get(w))}if(ok)eq.push({V,b,ids})}
 let P=new Map(),conflict=null;for(let i=0;i<eq.length;i++){let e=eq[i],x=e.V.reduce((a,v)=>a|(1n<<BigInt(vars.indexOf(v))),0n),b=e.b,p=1n<<BigInt(i);for(let j=0;j<vars.length;j++)if(x&(1n<<BigInt(j))){ops++;if(!P.has(j)){P.set(j,{x,b,p});x=null;break}let q=P.get(j);x^=q.x;b^=q.b;p^=q.p}if(x===0n&&b){conflict=eq.map((_,j)=>j).filter(j=>Boolean(p&(1n<<BigInt(j))));break}}
 let verified=false;if(conflict){let counts=new Map(),b=0;for(let j of conflict){let e=eq[j];b^=e.b;for(let v of e.V)counts.set(v,(counts.get(v)||0)^1);for(let w=0;w<2**e.V.length;w++)if(parity(w)!==e.b){if(!e.ids.some(i=>C[i].length===e.V.length&&C[i].every(l=>e.V.includes(Math.abs(l))&&Boolean(w>>e.V.indexOf(Math.abs(l))&1)!==(l>0))))throw Error("bad affine certificate")}}verified=b===1&&[...counts.values()].every(v=>v===0);if(!verified)throw Error("bad sum")}
 return{status:verified?"UNSAT":"UNKNOWN",equations:eq.length,tests,ops,conflict,proof:conflict&&conflict.map(j=>eq[j])}
}
module.exports={affineParity};

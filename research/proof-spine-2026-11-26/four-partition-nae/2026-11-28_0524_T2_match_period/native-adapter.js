function encode(F,selection){
 let n=0,clauses=[],A=[0],ids=F.rows.map(r=>r.map(()=>++n)),sel=new Set((selection||[]).map(([i,j])=>i+":"+j));for(let i=0;i<F.rows.length;i++)for(let j=0;j<F.rows[i].length;j++)A[ids[i][j]]=+sel.has(i+":"+j);
 const one=L=>{clauses.push(L.slice());for(let i=0;i<L.length;i++)for(let j=i+1;j<L.length;j++)clauses.push([-L[i],-L[j]])};
 for(const L of ids)one(L);for(let j=0;j<F.rows.length;j++)one(F.rows.flatMap((r,i)=>r.flatMap((e,k)=>e.j===j?[ids[i][k]]:[])));
 const T=BigInt("0x"+F.target);
 for(let k=0;k<F.dimension;k++){let L=F.rows.flatMap((r,i)=>r.flatMap((e,j)=>(BigInt("0x"+e.v)>>BigInt(k))&1n?[ids[i][j]]:[])),b=Number(T>>BigInt(k)&1n);if(!L.length){if(b)clauses.push([]);continue}let a=L[0];for(let j=1;j<L.length;j++){let x=L[j],z=++n;clauses.push([a,x,-z],[-a,-x,-z],[-a,x,z],[a,-x,z]);A[z]=A[a]^A[x];a=z}clauses.push([b?a:-a])}
 const dimacs=`p cnf ${n} ${clauses.length}\n`+clauses.map(x=>x.concat(0).join(" ")).join("\n")+"\n";return {nvars:n,dimacs,clauses,A,ids}
}

function lift(g,enc){
 const {network:G,source_map:M}=g,A=enc.A.slice(),vals={f:0};let next=enc.nvars;
 const lit=(a)=>A[Math.abs(a)]^+(a<0);
 for(const C of enc.clauses){if(C.length>3){let v=1^(lit(C[0])|lit(C[1]));A[++next]=v;for(let j=2;j<C.length-2;j++){v=v&(1^lit(C[j]));A[++next]=v}}}
 for(let j=1;j<A.length;j++)vals["x"+j]=A[j];for(let i=0;i<M.ternary_clauses.length;i++){let [a,b,c]=M.ternary_clauses[i].map(lit),hit=false;for(let z=0;z<2;z++){let w=2-a-b-z,u=2-(1-z)-c;if(w>=0&&w<=1&&u>=0&&u<=1){vals["z"+i]=z;vals["w"+i+"_0"]=w;vals["w"+i+"_1"]=u;hit=true;break}}if(!hit)throw Error("ternary lift "+i)}
 let P=Array.from({length:4*G.types.length},()=>[]);for(const [a,b,s] of G.edges){P[a].push([b,s]);P[b].push([a,s])}for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++){P[4*i].push([4*i+j,0]);P[4*i+j].push([4*i,0])}
 let X=new Int8Array(P.length).fill(-1);
 function seed(a,x){if(X[a]>=0){if(X[a]!==x)throw Error("seed inconsistency");return}let Q=[a];X[a]=x;for(let k=0;k<Q.length;k++)for(let [b,s] of P[Q[k]]){let v=X[Q[k]]^s;if(X[b]<0){X[b]=v;Q.push(b)}else if(X[b]!==v)throw Error("edge inconsistency")}}
 for(const [key,[p,s]] of Object.entries(M.representative_ports)){if(!(key in vals))throw Error("missing "+key);seed(p,vals[key]^s)}for(let p=0;p<X.length;p++)if(X[p]<0)seed(p,0);
 return [...X].join("")
}

function checkNative(G,w){if(w.length!==4*G.types.length||/[^01]/.test(w))return false;for(let i=0;i<G.types.length;i++){let a=w.slice(4*i,4*i+4);if(G.types[i]==="E"?a!==a[0].repeat(4):[...a].reduce((s,x)=>s+Number(x),0)!==2)return false}return G.edges.every(([a,b,s])=>(Number(w[a])^Number(w[b]))===s)}
module.exports={encode,lift,checkNative};

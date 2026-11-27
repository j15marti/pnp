function independent(z,selected=null){let vs=[...new Set([...z.rows.values()].flat().map(Math.abs))].sort((a,b)=>a-b),idx=new Map(vs.map((v,i)=>[v,i])),n=vs.length,ops=0;
 const bit=l=>1n<<BigInt(idx.get(Math.abs(l)));const encode=(v,b)=>(v<<1n)|BigInt(b);const eq=(x,y)=>encode(bit(x)^bit(y),Number(x<0)^Number(y<0));
 // least-pivot elimination with right-hand side bit zero; independent from prior highest-pivot basis
 function basis(rows){let m=new Map();for(let a of rows){while(a>1n){ops++;let v=a>>1n,low=v&-v;if(!m.has(low)){m.set(low,a);break}a^=m.get(low)}if(a===1n)return null}return m}
 const parity=basis([...z.rows.values()].map(row=>encode(row.reduce((a,l)=>a^bit(l),0n),row.reduce((a,l)=>a^Number(l<0),0))));
 if(!parity)throw Error("parity inconsistent");let rank=parity.size,d=n-rank,total=1n<<BigInt(d);
 function reduce(a,m){let piv=[...m.keys()].sort((a,b)=>a<b?-1:a>b?1:0);for(const k of piv){ops++;if((a>>1n)&k)a^=m.get(k)}return a}
 function canon(rows){const m=basis(rows);if(!m)return null;let keys=[...m.keys()].sort((a,b)=>a>b?-1:a<b?1:0);for(let i=0;i<keys.length;i++)for(let j=i+1;j<keys.length;j++)if((m.get(keys[j])>>1n)&keys[i]){m.set(keys[j],m.get(keys[j])^m.get(keys[i]));ops++}return keys.map(k=>m.get(k))}
 const map=new Map();for(const [id,row] of z.rows){if(selected&&!selected.has(id))continue;let a=canon(row.slice(1).map(x=>reduce(eq(row[0],x),parity)));if(a===null)continue;let key=a.join(",");if(!map.has(key))map.set(key,a)}
 const events=[...map.values()],m=events.length;
 const count=rows=>{let k=basis(rows);return k?1n<<BigInt(d-k.size):0n};let sum=events.reduce((a,e)=>a+count(e),0n),tree=0n,done=new Uint8Array(m),best=Array(m).fill(-1n),pairs=0;if(m)best[0]=0n;
 // Prim chooses the maximum edge across the cut and computes each pair once
 for(let step=0;step<m;step++){let v=-1;for(let i=0;i<m;i++)if(!done[i]&&(v<0||best[i]>best[v]))v=i;done[v]=1;tree+=best[v];for(let i=0;i<m;i++)if(!done[i]){let w=count(events[v].concat(events[i]));pairs++;if(w>best[i])best[i]=w}}
 return {n,rank,d,events:m,operations:ops,pairs,sum:sum.toString(),maxTreeWeight:tree.toString(),minimumForestScore:(sum-tree).toString(),fiberSize:total.toString(),refusal:sum-tree>total}}
module.exports={independent};

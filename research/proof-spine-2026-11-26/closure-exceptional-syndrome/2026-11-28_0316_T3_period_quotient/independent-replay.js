function replay(H,E,m,trace,terminal=false){
 let stats={tuples:0,pairs:0,rankXor:0,filter:0,period:0,transitions:0,peak:0,steps:0};let target=0n,cols=Array(m).fill(0n),adj=Array.from({length:m},()=>[]);for(let [a,b] of E){adj[a].push(b);adj[b].push(a)}
 for(let j=0;j<H.length;j++){target|=(H[j]&1n)<<BigInt(j);for(let i=0;i<m;i++)if(H[j]&(1n<<BigInt(i+1)))cols[i]|=1n<<BigInt(j)}
 let B=[],seen=new Set();for(let i=0;i<m;i++){if(seen.has(i))continue;let V=[i];seen.add(i);for(let j=0;j<V.length;j++)for(let a of adj[V[j]])if(!seen.has(a)){seen.add(a);V.push(a)}V.sort((a,b)=>a-b);if(V.length>12)throw Error("block cap");let S=new Set();for(let q=0;q<2**V.length;q++){stats.tuples++;let a=new Set(V.filter((_,j)=>q>>j&1));if([...a].some(v=>adj[v].some(w=>a.has(w))))continue;let t=0n;for(let v of a)t^=cols[v];S.add(t)}B.push({id:B.length,S})}
 const add=(A,x)=>{while(x){let k=x.toString(2).length-1;if(!A.has(k)){A.set(k,x);return}x^=A.get(k);stats.rankXor++}};
 const reduce=(A,x)=>{while(x){let k=x.toString(2).length-1;if(!A.has(k))return false;x^=A.get(k);stats.rankXor++}return true};
 function hull(list){let G=new Map(),o=0n;for(let C of list){let a=C.S.values().next().value;if(a===undefined)throw Error("empty");o^=a;for(let x of C.S)add(G,x^a)}return{G,o}}
 const init=B.length,initialOptions=B.reduce((n,C)=>n+C.S.size,0),K=64,r=H.length;let d=r,phi0=(init+d)*(init*K+1)+initialOptions,phi=phi0;
 for(let t of trace){stats.steps++;if(t.kind==="fuse"){let i=B.findIndex(C=>C.id===t.a),j=B.findIndex(C=>C.id===t.b);if(i<0||j<0||i===j||B.some(C=>C.id===t.id))throw Error("fuse identity");let S=new Set();for(let x of B[i].S)for(let y of B[j].S){stats.pairs++;S.add(x^y)}if(S.size!==t.size||S.size>K)throw Error("fuse exact sum");B=B.filter((_,k)=>k!==i&&k!==j);B.splice(Math.min(i,j),0,{id:t.id,S})}
 else if(t.kind==="filter"){let i=B.findIndex(C=>C.id===t.id);if(i<0||B[i].S.size!==t.from)throw Error("filter identity");let {G,o}=hull(B.filter((_,j)=>j!==i)),S=new Set();for(let x of B[i].S){stats.filter++;if(reduce(G,target^o^x))S.add(x)}if(S.size!==t.to||!S.size||S.size>=t.from)throw Error("filter check");B[i]={id:t.id,S}}
 else if(t.kind==="period"){let p=BigInt("0x"+t.p),C=B.find(C=>C.id===t.owner);if(!C||!p||target!==BigInt("0x"+t.oldb))throw Error("period identity");for(let x of C.S){stats.period++;if(!C.S.has(x^p))throw Error("period closure")}let k=p&-p,pi=x=>x&k?x^p:x;target=pi(target);B=B.map(C=>({id:C.id,S:new Set([...C.S].map(pi))}));d--}
 else throw Error("unknown trace");
 let a=(B.length+d)*(init*K+1)+B.reduce((n,C)=>n+C.S.size,0);if(a>=phi)throw Error("credit not strict");phi=a;
 }
 let result={initialBlocks:init,finalBlocks:B.length,initialOptions,finalOptions:B.reduce((n,C)=>n+C.S.size,0),phi0,phi,stats,target:target.toString(16),finalDictionaries:B.map(C=>({id:C.id,S:[...C.S].map(x=>x.toString(16)).sort()}))};
 if(terminal){let suffix=[];for(let i=0;i<=B.length;i++)suffix.push(hull(B.slice(i)));let states=new Set([0n]);for(let i=0;i<B.length;i++){let T=new Set(),{G,o}=suffix[i+1];for(let u of states)for(let v of B[i].S){stats.transitions++;if(reduce(G,target^u^v^o))T.add(u^v)}if(T.size>4096)throw Error("state cap");states=T;stats.peak=Math.max(stats.peak,T.size);if(!states.size)break}result.decision=states.has(target)?"YES":"NO"}
 return result
}
module.exports={replay};

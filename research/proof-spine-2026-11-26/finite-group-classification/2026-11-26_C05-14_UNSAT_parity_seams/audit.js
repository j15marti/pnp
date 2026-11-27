function audit(){
 const core=[[1,1,0],[2,2,2],[2,0,0],[0,1,1],[1,2,1],[2,0,2],[0,0,2],[1,1,1]];
 const assert=(p)=>{if(!p)throw Error("assertion failed")};let checks=0;
 const ck=p=>{assert(p);checks++};
 function localMatches(T,a,b){
  const xs=[...new Set(T.map(t=>t[a]))].sort((a,b)=>a-b),out=[];
  function go(j,ys,ids){if(j===xs.length){out.push(ids);return}T.forEach((t,i)=>{if(t[a]===xs[j]&&!ys.has(t[b]))go(j+1,new Set([...ys,t[b]]),[...ids,i])})}
  go(0,new Set(),[]);return out;
 }
 function bits(x){let n=0;while(x){x&=x-1n;n++}return n}
 function word(T,ids,c){let w=0n;for(const i of ids)w^=1n<<BigInt(T[i][c]);return w}
 function parityCounts(T,a,b,c){const m=new Map();for(const ids of localMatches(T,a,b)){const w=word(T,ids,c);m.set(w,(m.get(w)||0)+1)}return m}
 function hash(H,w){return H.reduce((v,h,j)=>v+((bits(h&w)&1)<<j),0)}
 function basis(L){const B=new Map();for(let x of L){while(x){const j=x.toString(2).length-1;if(B.has(j))x^=B.get(j);else{B.set(j,x);break}}}return B}
 function red(B,x){for(const j of [...B.keys()].sort((a,b)=>b-a))if((x>>BigInt(j))&1n)x^=B.get(j);return x}
 function periods(S){const a=[...S][0];return [...S].map(b=>a^b).filter(h=>[...S].every(w=>S.has(w^h)))}
 function chain(k){const T=core.map(t=>[...t]);for(let j=0;j<k;j++)for(let t=0;t<8;t++)T.push([3+2*j+(t>>2),3+2*j+((t>>1)&1),3+2*j+(t&1)]);for(let j=0;j<k;j++){const ty=j%2===0?0:7,l=j===0?0:8+8*(j-1)+ty,r=8+8*j+ty;[T[l][0],T[r][0]]=[T[r][0],T[l][0]]}return T}
 for(const [a,b,c] of [[0,1,2],[0,2,1],[1,2,0]]){const M=localMatches(core,a,b);ck(M.length===4);for(let i=0;i<8;i++)ck(M.some(x=>x.includes(i))&&M.some(x=>!x.includes(i)));ck(M.every(x=>bits(word(core,x,c))!==3))}
 const rows=[];
 for(const k of [0,1,2,4,8,16,32,64,128]){
  const T=chain(k),S=[],pc=[];
  for(let j=0;j<=k;j++){const U=T.slice(8*j,8*j+8),r=j===0?3:2;const P=parityCounts(U,1,2,0);pc.push(P.size);S.push(new Set([...P.keys()].filter(v=>bits(v)===r)));
   // Walsh inversion independently using exact enumerated character sums for arbitrary local coordinate forms.
   const coords=[...new Set(U.map(t=>t[0]))].sort((a,b)=>a-b);const H=coords.map(z=>1n<<BigInt(z)),D=Array(1<<H.length).fill(0);
   for(const [w,n] of P)D[hash(H,w)]+=n;
   const F=D.map((_,a)=>D.reduce((s,v,b)=>s+((bits(BigInt(a&b))&1)?-v:v),0));
   for(let b=0;b<D.length;b++)ck(F.reduce((s,v,a)=>s+((bits(BigInt(a&b))&1)?-v:v),0)===D.length*D[b])
  }
  if(k===0){ck(S[0].size===0);rows.push({k,rank:0,peak:0,maxParity:Math.max(...pc)});continue}
  const B=basis(S.flatMap(periods));let state=new Set([0n]),peak=1;
  for(const U of S){const V=new Set([...U].map(x=>red(B,x)));state=new Set([...state].flatMap(x=>[...V].map(y=>x^y)));peak=Math.max(peak,state.size)}
  ck(!state.has(red(B,(1n<<BigInt(3+2*k))-1n)));ck(peak<=3);ck(B.size===2*k-1);rows.push({k,rank:B.size,peak,maxParity:Math.max(...pc)});
 }
 const masks=[...Array(256).keys()],opt=[[],[]];
 for(const m of masks){const T=[];for(let t=0;t<8;t++)if((m>>t)&1)T.push([t>>2,(t>>1)&1,t&1,t]);if(!(m&1)||[0,1,2].some(c=>[0,1].some(z=>T.filter(t=>t[c]===z).length<2)))continue;
  const M=localMatches(T,1,2).filter(ids=>bits(word(T,ids,0))===2);if(M.length&&M.every(ids=>ids.includes(0)===M[0].includes(0)))opt[+M[0].includes(0)].push(m)
 }
 let incompatible=0;
 for(const ma of opt[1])for(const mb of opt[0]){const T=[];for(const [j,m] of [[0,ma],[1,mb]])for(let t=0;t<8;t++)if((m>>t)&1)T.push([2*j+(t>>2),2*j+((t>>1)&1),2*j+(t&1),8*j+t]);const a=T.findIndex(t=>t[3]===0),b=T.findIndex(t=>t[3]===8);[T[a][0],T[b][0]]=[T[b][0],T[a][0]];ck(localMatches(T,1,2).every(ids=>bits(word(T,ids,0))!==4));incompatible++}
 ck(incompatible===26);return {checks,rows,incompatible};
}
console.log(JSON.stringify(audit(),null,2));

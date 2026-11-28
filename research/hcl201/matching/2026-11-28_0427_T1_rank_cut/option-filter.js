
function examine(A,limit=8){
 const {H,edges,m}=A,cols=Array(m).fill(0n);let target=0n;
 for(let j=0;j<H.length;j++){let x=H[j],q=1n<<BigInt(j);if(x&1n)target|=q;while(x&~1n){let u=(x&~1n)&-(x&~1n);cols[u.toString(2).length-2]|=q;x^=u}}
 let p=Array.from({length:m},(_,i)=>i);function root(i){while(p[i]!==i)i=p[i];return i}for(let [a,b] of edges)p[root(a)]=root(b);
 let G=new Map();for(let i=0;i<m;i++){let r=root(i);if(!G.has(r))G.set(r,[]);G.get(r).push(i)}
 let B=[],clique=0,enumWords=0,options=0,refused=[];for(let V of G.values()){let ix=new Map(V.map((x,i)=>[x,i])),E=edges.filter(([a,b])=>ix.has(a)&&ix.has(b)),C=E.length===V.length*(V.length-1)/2,words=[];
 if(C){clique++;words=[[],...V.map(x=>[x])]}else if(V.length<=limit){for(let z=0;z<2**V.length;z++){enumWords++;if(!E.some(([a,b])=>(z>>ix.get(a)&1)&&(z>>ix.get(b)&1)))words.push(V.filter((v,i)=>z>>i&1))}}else{refused.push({V,E});continue}
 let S=new Map();for(let w of words){let y=w.reduce((a,v)=>a^cols[v],0n);if(!S.has(y))S.set(y,w)}options+=S.size;B.push({V,E,C,S:[...S].map(([y,w])=>({y,w}))})}
 if(refused.length)return {status:"BLOCK-CAP",blocks:G.size,clique,refused:refused.map(x=>x.V.length),enumWords,options};
 let counts={tests:0,xors:0,proposals:0,diffusion:0,filter:0};const add=(D,x)=>{while(x){counts.tests++;let k=x&-x;if(!D.has(k)){D.set(k,x);return}x^=D.get(k);counts.xors++}},reduce=(D,x)=>{for(let y=x;y;){counts.tests++;let k=y&-y;if(!D.has(k))return false;y^=D.get(k);counts.xors++}return true};
 function center(b){let a=b.S[0].y;return {a,U:b.S.map(s=>s.y^a)}}
 function ranks(B,order){let L=B.map(center),pre=new Map(),suf=Array(order.length+1);suf[order.length]=new Map();for(let i=order.length-1;i>=0;i--){let d=new Map(suf[i+1]);for(let x of L[order[i]].U)add(d,x);suf[i]=d}let max=0,sum=0;for(let i=0;i<order.length;i++){for(let x of L[order[i]].U)add(pre,x);let r=pre.size+suf[i+1].size-suf[0].size;max=Math.max(max,r);sum+=r}return {max,sum,rank:suf[0].size}}
 let n=B.length,order=Array.from({length:n},(_,i)=>i),raw=ranks(B,order);
 // exact integer fixed point lazy diffusion on block shared syndrome-coordinate graph; heuristic only
 let rowOwners=new Map();for(let i=0;i<n;i++){let u=B[i].S.reduce((a,s)=>a|s.y,0n);while(u){let k=u&-u;u^=k;if(!rowOwners.has(k))rowOwners.set(k,[]);rowOwners.get(k).push(i)}}
 let W=Array.from({length:n},()=>new Map());for(let ids of rowOwners.values())for(let i of ids)for(let j of ids)if(i!==j)W[i].set(j,(W[i].get(j)||0)+1);
 let deg=W.map(w=>[...w.values()].reduce((a,b)=>a+b,0)),d=Math.max(1,...deg),v=order.map(i=>Math.trunc(1000000*(2*i-n+1)/Math.max(1,n-1)));
 for(let t=0;t<24;t++){let u=v.map((x,i)=>{let z=(2*d-deg[i])*x;for(let [j,w] of W[i]){z+=w*v[j];counts.diffusion++}if(!Number.isSafeInteger(z))throw Error("precision");return Math.trunc(z/(2*d))});let av=Math.trunc(u.reduce((a,b)=>a+b,0)/Math.max(1,n));u=u.map(x=>x-av);let mx=Math.max(1,...u.map(Math.abs));v=u.map(x=>Math.trunc(x*1000000/mx))}
 let sp=order.slice().sort((i,j)=>v[i]-v[j]||i-j),spectral=ranks(B,sp);
 // independent one-block support filter using affine hull of every exterior block, cap on actual rank tests
 let before=B.map(x=>({...x,S:x.S.slice()})),drops=[],stage="FIXED-POINT-ONE-PASS",cap=5000000;
 for(let i of sp){if(counts.tests>cap){stage="CAP";break}let t=target,D=new Map();for(let j=0;j<n;j++)if(j!==i){let a=center(B[j]);t^=a.a;for(let y of a.U)add(D,y)}let keep=[];for(let s of B[i].S){counts.filter++;if(reduce(D,t^s.y))keep.push(s);else drops.push({i,y:s.y.toString(16),word:s.w,exteriorRank:D.size})}if(!keep.length){stage="EMPTY-BLOCK";break}B[i].S=keep}
 let after=stage==="EMPTY-BLOCK"?null:{raw:ranks(B,order),spectral:ranks(B,sp)};
 const encode=B=>B.map(b=>({V:b.V,E:b.E,C:b.C,S:b.S.map(s=>[s.y.toString(16),s.w])}));
 return {status:stage,blocks:n,clique,enumWords,options,raw,spectral,after,drops,counts,order,sp,dict:encode(before),filtered:encode(B),target:target.toString(16),cols:cols.map(x=>x.toString(16))}
}

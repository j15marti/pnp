function ownerCheck(Z){
 const {B,adj}=Z,n=B.length,ids=B.map((_,i)=>i),basis=new Map(),owners=[],counts={basisXor:0,coordinateXor:0,rankXor:0};
 const high=v=>v.toString(2).length-1;
 for(let i of ids)for(let [x] of B[i]){let v=x,c=0n;while(v){let k=high(v);if(!basis.has(k)){let b=1n<<BigInt(owners.length);owners.push(i);basis.set(k,[v,c^b]);break}let [a,b]=basis.get(k);v^=a;c^=b;counts.basisXor++}}
 function coords(v){let c=0n;while(v){let q=basis.get(high(v));if(!q)throw Error("outside global span");v^=q[0];c^=q[1];counts.coordinateXor++}return c}
 const D=B.map(S=>S.map(([x])=>coords(x)));let v=ids.map(i=>Math.trunc(1e6*(2*i-Math.max(1,n-1))/Math.max(1,n-1)));for(let k=0;k<24;k++)v=v.map((x,i)=>{let a=x,b=1;for(let [j,w] of adj[i]){a+=w*v[j];b+=w}return Math.trunc(a/b)});
 const spectral=[...ids].sort((a,b)=>v[a]-v[b]||a-b);
 function rank(X){let m=new Map();for(let v of X)while(v){let k=high(v);if(!m.has(k)){m.set(k,v);break}v^=m.get(k);counts.rankXor++}return m.size}
 const cuts=[];for(let [mode,order] of [["source",ids],["spectral",spectral]]){let P=new Set(order.slice(0,n>>1)),I=0n,J=0n;owners.forEach((o,i)=>{if(P.has(o))I|=1n<<BigInt(i);else J|=1n<<BigInt(i)});let A=[],E=[],X=[],Y=[];for(let i of ids){if(P.has(i)){A.push(...B[i].map(x=>x[0]));X.push(...D[i].map(x=>x&J))}else{E.push(...B[i].map(x=>x[0]));Y.push(...D[i].map(x=>x&I))}}let left=rank(X),right=rank(Y),direct=rank(A)+rank(E)-owners.length;if(left+right!==direct)throw Error("cross-rank mismatch");cuts.push({mode,left,right,crossRank:left+right,direct,sideSize:P.size,cut:[...P]})}
 return {basisRank:owners.length,cuts,counts}
}
function feedback(instance){
 const F=instance.dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1)),n=instance.nvars;
 function arm(start,mode){let a=Array(n+1).fill(start),visits=0,ties=0,moves=[],unsigned=[],signed=[];
 function score(flip){let bad=0,zero=0;for(let row of F){let k=0,s=0;for(let l of row){visits++;let v=Math.abs(l),b=a[v]^(v===flip?1:0),hit=b===+(l>0);if(hit){k++;s+=l>0?1:-1}}if(!k)bad++;else if(s%3===0)zero++;if(!flip&&mode!=="baseline"){unsigned.push(k%3);signed.push((s%3+3)%3)}}return [bad,zero]}
 let cur=score(0)[0],initial=cur;for(let step=0;step<8;step++){let list=[];for(let j=1;j<=n;j++){let [b,z]=score(j);if(b<cur)list.push({j,b,z})}if(!list.length)break;list.sort((x,y)=>x.b-y.b||x.j-y.j);let standard=list[0];if(mode==="residue")list.sort((x,y)=>x.b-y.b||x.z-y.z||x.j-y.j);let pick=list[0];if(pick.j!==standard.j)ties++;a[pick.j]^=1;cur=pick.b;moves.push(pick.j);unsigned=[];signed=[];if(mode!=="baseline"){let [b]=score(0);if(b!==cur)throw Error("feedback score mismatch")}}
 return {start,mode,initial,final:cur,ties,moves,visits,unsigned,signed,status:cur===0?"SAT":"UNKNOWN",assignment:cur===0?a.slice(1):undefined}
 }
 return [0,1].flatMap(s=>["baseline","table","residue"].map(m=>arm(s,m)))
}

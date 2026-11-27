function ck(x,m="assert"){if(!x)throw Error(m)}

function graph(k){let L=[[2,3,5],[6,7],[3,5],[1,4,6],[3,6,8],[0,8],[2,7],[1,6],[0,2,4]],neg=new Set(["2,5","6,7","7,6","8,2","8,4"]),a=i=>9+2*i,b=i=>10+2*i;let E=L.flatMap((r,i)=>r.map(j=>[i===0?a(k-1):i===2?b(k-1):i,j,neg.has(i+","+j)?-1:1]));E.push([0,a(0),1],[2,b(0),1]);for(let i=0;i<k-1;i++)E.push([a(i),a(i+1),1],[b(i),b(i+1),1],[a(i),b(i+1),-1],[b(i),a(i+1),1]);return {n:9+2*k,E}}

function det(A){let n=A.length,d=1n,s=1n;if(!n)return 1n;for(let k=0;k<n-1;k++){let j=k;while(j<n&&!A[j][k])j++;if(j===n)return 0n;if(j!==k){[A[k],A[j]]=[A[j],A[k]];s=-s}let p=A[k][k];for(let i=k+1;i<n;i++){let z=A[i][k];if(!z&&p===d)continue;for(let j=k+1;j<n;j++){let x=A[i][j]*p-z*A[k][j];ck(x%d===0n);A[i][j]=x/d}A[i][k]=0n}d=p}return s*A[n-1][n-1]}

function count(G,C){let n=G.n,A=Array.from({length:n},()=>Array(n).fill(0n)),B=Array.from({length:n},()=>Array(n).fill(0n));for(let [u,v,s] of G.E)if(!C.some(S=>S.has(u)&&!S.has(v))){A[u][v]=1n;B[u][v]=BigInt(s)}let z=det(B),a=det(A),t=z<0n?-z:z;ck((t+a)%2n===0n);return (t+a)/2n}

function cuts(G){let A=Array.from({length:G.n},()=>new Set());for(let [u,v] of G.E)A[u].add(v);let M=new Map();function add(S){S.sort((a,b)=>a-b);if(!S.includes(0))M.set(S.join(","),new Set(S))}for(let u=0;u<G.n;u++)for(let v of A[u]){if(A[v].has(u))add([u,v]);for(let w of A[v])if(w!==u&&A[w].has(u))add([u,v,w])}return [...M.values()]}

function run(){let out=[];for(let k of [3,8,16,32,64]){let G=graph(k),C=cuts(G),B=count(G,[]),q=1,L=[];for(let S of C){q++;let z=count(G,[S]);if(z>0n)L.push(S)}let moments=[B,0n,0n,0n,0n],a=[];function rec(i,J){if(J.length){q++;let z=count(G,J.map(t=>L[t]));moments[J.length]+=z;a.push({indices:J,count:z})}if(J.length===4)return;for(let j=i;j<L.length;j++)rec(j+1,[...J,j])}rec(0,[]);ck(B===9n*(2n**BigInt(k-2)));ck(moments[4]===0n);let U=moments[0]-moments[1]+moments[2]-moments[3];ck(U===0n,"not covered");out.push({k,n:G.n,rawCutCandidates:C.map(S=>[...S]),positiveCuts:L.map(S=>[...S]),target:B,moments,countPairs:q,uncovered:U,intersectionCounts:a})}return out}
console.log(JSON.stringify(run(),(_,v)=>typeof v==='bigint'?v.toString():v,2));

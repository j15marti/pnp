// C02-19 independent source-order replay; source from C02-18 pinned original X01-19. Node.js.
const source = {"q":22,"T":[[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[2,0,1],[1,0,2],[2,0,2],[3,1,0],[1,2,0],[3,2,0],[4,1,1],[2,3,1],[4,3,1],[3,1,3],[4,1,3],[1,4,2],[2,5,2],[5,4,2],[5,5,2],[1,2,4],[1,4,4],[2,3,5],[2,5,5],[3,2,6],[6,2,4],[6,2,6],[4,3,7],[7,3,5],[7,3,7],[3,6,3],[3,6,6],[4,7,3],[4,7,7],[8,6,3],[8,7,3],[5,4,8],[5,5,9],[5,8,8],[5,8,9],[9,4,4],[9,4,8],[10,5,5],[10,5,9],[6,9,4],[9,9,4],[7,10,5],[10,10,5],[6,11,6],[6,9,10],[6,11,10],[7,12,7],[7,10,11],[7,12,11],[11,6,6],[11,11,6],[12,7,7],[12,12,7],[8,6,12],[11,6,12],[8,7,13],[12,7,13],[8,13,12],[8,13,13],[13,8,8],[13,8,9],[9,14,8],[13,14,8],[10,15,9],[13,15,9],[9,9,14],[9,14,14],[10,10,15],[10,15,15],[14,9,10],[14,9,14],[15,10,11],[15,10,15],[14,11,10],[15,12,11],[11,11,16],[14,11,16],[12,12,17],[15,12,17],[11,16,12],[11,16,16],[12,17,13],[12,17,17],[16,13,12],[16,16,12],[16,13,13],[16,17,13],[13,14,18],[13,15,18],[17,14,14],[17,14,18],[18,15,15],[18,15,18],[14,18,14],[17,18,14],[15,19,15],[18,19,15],[14,18,16],[15,19,17],[19,16,16],[19,18,16],[20,17,17],[20,19,17],[16,16,19],[19,16,19],[16,17,19],[20,17,19],[17,20,18],[18,20,18],[17,18,20],[17,20,20],[18,19,21],[18,20,21],[19,18,20],[20,19,21],[19,21,19],[19,21,20],[20,21,19],[20,21,21],[21,20,20],[21,20,21],[21,21,20],[21,21,21]],"guard":[1,4,11,19,23,24,28,30,33,36,39,40,41,59,65,67,70,82,87,91,92,109,110,112,120],"live_ids":[0,2,3,5,6,7,8,9,10,12,13,14,15,16,17,18,20,21,22,25,26,27,29,31,32,34,35,37,38,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,68,69,71,72,73,74,75,76,77,78,79,80,81,83,84,85,86,88,89,90,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,111,113,114,115,116,117,118,119,121,122,123,124,125,126,127],"chosen_ids":[]};
function replay(source){
 const {q,T,guard,live_ids:L}=source,bit=x=>x&(-x),uniq=a=>[...new Set(a)],mn=a=>a.reduce((x,y)=>x<y?x:y),xor=a=>a.reduce((x,y)=>x^y,0n);
 const sorted=a=>[...a].sort((x,y)=>x<y?-1:x>y?1:0);
 function basis(a){let M=new Map();for(let x of a)while(x){let k=bit(x);if(!M.has(k)){M.set(k,x);break}x^=M.get(k)}return [...M].sort((a,b)=>a[0]<b[0]?-1:1)}
 function rem(x,B){for(let [k,v] of B)if(x&k)x^=v;return x}
 function span(G){return basis(G.flatMap(A=>A.map(x=>x^mn(A))))}
 function period(A){const S=new Set(A),a=mn(A);return basis(A.map(x=>x^a).filter(h=>A.every(x=>S.has(x^h))))}
 let refNodes=0;
 function dfs(ids,used){refNodes++;if(refNodes>5000)throw Error("reference cap");if(used.every(x=>x===(1n<<BigInt(q))-1n))return true;let best=null;
 for(let c=0;c<3;c++)for(let v=0;v<q;v++)if(!(used[c]&(1n<<BigInt(v)))){let a=ids.filter(i=>T[i][c]===v);if(best===null||a.length<best.length)best=a}
 for(let i of best){let t=T[i],u=used.map((x,c)=>x|(1n<<BigInt(t[c])));if(dfs(ids.filter(j=>T[j].every((v,c)=>v!==t[c])),u))return true}return false}
 if(dfs(T.map((_,i)=>i).filter(i=>!guard.includes(i)),[0n,0n,0n]))throw Error("unexpected native YES");
 function run(c,mode){let [a,b]=[0,1,2].filter(x=>x!==c),G=Array.from({length:q},()=>[]);for(let i of L)G[T[i][c]].push((1n<<BigInt(T[i][a]))^(1n<<BigInt(q+T[i][b])));G=G.map(uniq);let t=(1n<<BigInt(2*q))-1n,r=0,steps=0,visits=0,peak=0,checks=0;
 function trim(A,J){let B=span(J),o=xor(J.map(mn));return A.filter(x=>rem(t^x^o,B)===0n)}
 function checkwidth(H,A,J){let U=span([A]),V=span(J),w=U.length+V.length-basis([...U,...V].map(x=>x[1])).length;let U2=basis(U.map(x=>rem(x[1],H))),V2=basis(V.map(x=>rem(x[1],H)));let w2=U2.length+V2.length-basis([...U2,...V2].map(x=>x[1])).length;if(w2>w)throw Error("width grew");checks++}
 if(mode!=="base")while(true){
  if(mode==="context")while(true){let Z=G.map((A,i)=>trim(A,G.filter((_,j)=>i!==j)));if(Z.some(A=>!A.length))return {no:true,r,steps,visits,peak,checks};if(Z.every((A,i)=>A.length===G[i].length))break;G=Z}
  let cand=null;for(let i=0;i<G.length&&!cand;i++){let H=period(G[i]);if(H.length)cand={ids:[i],A:G[i],H}}
  if(!cand&&mode==="context")for(let i=0;i<G.length&&!cand;i++)for(let j=i+1;j<G.length&&!cand;j++){let J=G.filter((_,k)=>k!==i&&k!==j);if(G[i].length*G[j].length>4096)continue;let A=trim(uniq(G[i].flatMap(x=>G[j].map(y=>x^y))),J);if(!A.length)return {no:true,r,steps,visits,peak,checks};let H=period(A);if(H.length)cand={ids:[i,j],A,H}}
  if(!cand)break;let {ids,A,H}=cand,J=G.filter((_,i)=>!ids.includes(i));checkwidth(H,A,J);G=[...J,A].map(X=>uniq(X.map(x=>rem(x,H))));t=rem(t,H);r+=H.length;steps++;
 }
 // Independent source-order frontier, not the Python greedy tree.
 let S=[0n];for(let i=0;i<G.length;i++){let J=G.slice(i+1),B=span(J),o=xor(J.map(mn)),Z=new Set();for(let x of S)for(let y of G[i]){if(++visits>3000000)return {no:null,r,steps,visits,peak,checks};let v=x^y;if(rem(t^o^v,B)===0n)Z.add(v)}S=sorted(Z);peak=Math.max(peak,S.length);if(!S.length)break}
 return {no:!S.includes(t),r,steps,visits,peak,checks};
 }
 return {referenceNodes:refNodes,lanes:[0,1,2].map(c=>({color:c,base:run(c,"base"),single:run(c,"single"),context:run(c,"context")}))};
}
console.log(JSON.stringify(replay(source),null,2));

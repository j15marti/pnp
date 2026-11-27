// C02-18 supplemental independent Node.js reproduction; original source X01-19 blob 0d07f18b6d82f48ba8d3cad8c2a295b0eb6446dc
const source = {"q":22,"T":[[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[2,0,1],[1,0,2],[2,0,2],[3,1,0],[1,2,0],[3,2,0],[4,1,1],[2,3,1],[4,3,1],[3,1,3],[4,1,3],[1,4,2],[2,5,2],[5,4,2],[5,5,2],[1,2,4],[1,4,4],[2,3,5],[2,5,5],[3,2,6],[6,2,4],[6,2,6],[4,3,7],[7,3,5],[7,3,7],[3,6,3],[3,6,6],[4,7,3],[4,7,7],[8,6,3],[8,7,3],[5,4,8],[5,5,9],[5,8,8],[5,8,9],[9,4,4],[9,4,8],[10,5,5],[10,5,9],[6,9,4],[9,9,4],[7,10,5],[10,10,5],[6,11,6],[6,9,10],[6,11,10],[7,12,7],[7,10,11],[7,12,11],[11,6,6],[11,11,6],[12,7,7],[12,12,7],[8,6,12],[11,6,12],[8,7,13],[12,7,13],[8,13,12],[8,13,13],[13,8,8],[13,8,9],[9,14,8],[13,14,8],[10,15,9],[13,15,9],[9,9,14],[9,14,14],[10,10,15],[10,15,15],[14,9,10],[14,9,14],[15,10,11],[15,10,15],[14,11,10],[15,12,11],[11,11,16],[14,11,16],[12,12,17],[15,12,17],[11,16,12],[11,16,16],[12,17,13],[12,17,17],[16,13,12],[16,16,12],[16,13,13],[16,17,13],[13,14,18],[13,15,18],[17,14,14],[17,14,18],[18,15,15],[18,15,18],[14,18,14],[17,18,14],[15,19,15],[18,19,15],[14,18,16],[15,19,17],[19,16,16],[19,18,16],[20,17,17],[20,19,17],[16,16,19],[19,16,19],[16,17,19],[20,17,19],[17,20,18],[18,20,18],[17,18,20],[17,20,20],[18,19,21],[18,20,21],[19,18,20],[20,19,21],[19,21,19],[19,21,20],[20,21,19],[20,21,21],[21,20,20],[21,20,21],[21,21,20],[21,21,21]],"guard":[1,4,11,19,23,24,28,30,33,36,39,40,41,59,65,67,70,82,87,91,92,109,110,112,120],"live_ids":[0,2,3,5,6,7,8,9,10,12,13,14,15,16,17,18,20,21,22,25,26,27,29,31,32,34,35,37,38,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,68,69,71,72,73,74,75,76,77,78,79,80,81,83,84,85,86,88,89,90,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,111,113,114,115,116,117,118,119,121,122,123,124,125,126,127],"chosen_ids":[]};
function reproduce(x){
  const q=x.q,T=x.T,L=x.live_ids;
  if(x.chosen_ids.length||L.some(i=>x.guard.includes(i)))throw Error("unexpected source");
  const add=(M,k,n)=>M.set(k,(M.get(k)||0n)+n),bit=x=>x.toString(2).length-1;
  function basis(V){let B=new Map();for(let x of V){while(x){const k=bit(x);if(!B.has(k)){B.set(k,x);break}x^=B.get(k)}}return [...B].sort((a,b)=>b[0]-a[0]);}
  function rem(x,B){for(const [i,v] of B){if(x&(1n<<BigInt(i)))x^=v}return x}
  function solve(c,mode){
    const [a,b]=[0,1,2].filter(i=>i!==c),D=Array.from({length:q},()=>[]);let target=(1n<<BigInt(2*q))-1n;
    for(const i of L)D[T[i][c]].push((1n<<BigInt(T[i][a]))|(1n<<BigInt(q+T[i][b])));
    for(const G of D){const v=G[0];target^=v;for(let i=0;i<G.length;i++)G[i]^=v}
    const mask=(1<<q)-1,cache=new Map();
    function span(S){if(!cache.has(S)){const V=[];for(let i=0;i<q;i++)if(S&(1<<i))V.push(...D[i]);cache.set(S,basis(V))}return cache.get(S)}
    const d=span(mask).length,width=S=>span(S).length+span(mask^S).length-d;
    let nodes=D.map((_,i)=>({S:1<<i,leaf:i,size:1})),candidate=0,pairs=0,keys=0,peak=0,trace=[];
    while(nodes.length>1){let best=null;for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){candidate++;const a=nodes[i],b=nodes[j],S=a.S|b.S,w=width(S),size=a.size+b.size;if(!best||w<best.w||(w===best.w&&size<best.size))best={i,j,S,w,size,a,b}}nodes=nodes.filter((_,i)=>i!==best.i&&i!==best.j);nodes.push(best)}
    function visit(n){const W=span(mask^n.S),Z=new Map();if(n.leaf!==undefined){for(const v of D[n.leaf])if(rem(target^v,W)===0n)add(Z,v,1n)}else{const X=visit(n.a),Y=visit(n.b);
      if(mode==="pair"){for(const [u,m] of X)for(const [v,l] of Y){pairs++;if(rem(target^u^v,W)===0n)add(Z,u^v,m*l)}}
      else{const R=new Map();for(const [v,l] of Y){keys++;const k=rem(target^v,W);if(!R.has(k))R.set(k,[]);R.get(k).push([v,l])}for(const [u,m] of X){keys++;for(const [v,l] of R.get(rem(u,W))||[]){pairs++;add(Z,u^v,m*l)}}}
    }peak=Math.max(peak,Z.size);trace.push([n.S,Z.size,[...Z.values()].reduce((a,b)=>a+b,0n).toString()]);return Z}
    const z=visit(nodes[0]);return {count:(z.get(target)||0n).toString(),pairs,keys,peak,candidate,rankCalls:cache.size,trace};
  }
  const out=[];for(let c=0;c<3;c++){const A=solve(c,"pair"),B=solve(c,"key");if(JSON.stringify(A.trace)!==JSON.stringify(B.trace)||A.count!=="0"||B.count!=="0")throw Error("replay mismatch");out.push({color:c,pair:A,key:B})}return out;
}
console.log(JSON.stringify(reproduce(source),null,2));

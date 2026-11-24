function hostile(){
  const out=[];
  for(let omit=-1;omit<8;omit++){
    const clauses=Array.from({length:8},(_,i)=>i).filter(i=>i!==omit),n=3,nb=clauses.length;
    // row cost 1 iff variable assignment agrees with forbidden bit
    const cost=(b,o,x)=>Number(x===((clauses[o]>>b)&1));
    const parent=Array.from({length:n+nb},(_,i)=>i),adj=parent.map(()=>[]),cuts=[];
    const root=x=>{while(parent[x]!==x)x=parent[x];return x;};
    for(let b=0;b<n;b++)for(let o=0;o<nb;o++){let v=n+o,a=root(b),d=root(v);if(a===d)cuts.push([b,o]);else{parent[a]=d;adj[b].push(v);adj[v].push(b);}}
    let leaf=0,solutions=0;
    function forest(D,K){
      function owner(v,p){let k=K[v-n];for(const b of adj[v])if(b!==p)k-=block(b,v);return k;}
      function block(b,p){let best=Infinity;for(const x of D[b]){let ok=true;for(const o of adj[b])if(o!==p&&cost(b,o-n,x)>owner(o,b))ok=false;if(ok)best=Math.min(best,p<0?0:cost(b,p-n,x));}return best;}
      return Number.isFinite(block(0,-1));
    }
    function dfs(i,D,K){if(i===cuts.length){leaf++;if(forest(D,K))solutions++;return;}let [b,o]=cuts[i];for(let z=0;z<=1;z++){let f=D[b].filter(x=>cost(b,o,x)===z);if(!f.length||K[o]<z)continue;let A=D.slice(),L=K.slice();A[b]=f;L[o]-=z;dfs(i+1,A,L);}}
    dfs(0,[[0,1],[0,1],[0,1]],clauses.map(()=>2));
    let exact=8-clauses.length;if(solutions!==exact)throw Error("mismatch");out.push({omitted:omit,exact,forestFeasibleCutTuples:solutions,visitedLeaves:leaf,cuts:cuts.length});
  }return out;
}
console.log(JSON.stringify(hostile(),null,2));

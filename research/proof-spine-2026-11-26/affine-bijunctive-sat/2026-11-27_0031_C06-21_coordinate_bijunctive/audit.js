function replay() {
  const check=(v,m)=>{if(!v)throw new Error(m)};
  const parity=x=>{let p=0n;while(x){p^=1n;x&=x-1n}return Number(p)};
  const rank=vs=>{const b=new Map();for(let v of vs){while(v){const k=v.toString(2).length;if(!b.has(k)){b.set(k,v);break}v^=b.get(k)}}return b.size};
  const G=[[4,10,1,0],[2,9,0,0],[3,12,1,1],[7,10,1,0]];
  const support=[],counts=[0,0,0,0];for(let x=0;x<16;x++){if(G.every(([a,b,s,t])=>parity(BigInt(a&x))!==s||parity(BigInt(b&x))!==t)){support.push(x);counts[x&3]++}}
  check(JSON.stringify(counts)==="[2,0,1,3]","gadget");
  check(rank(support.map(x=>BigInt(x^support[0])))===4,"full hull");
  function implications(fs){
    const g=new Map();const node=(a,b)=>a*2n+BigInt(b);
    for(const [a,b,s,t] of fs){const q=[[a,s],[b,t],[a^b,s^t]];for(const [v,p] of q)for(const [w,r] of q)if(v!==w){const i=node(v,p),j=node(w,1-r);if(!g.has(i))g.set(i,new Set());g.get(i).add(j);if(!g.has(j))g.set(j,new Set())}}
    const reachable=(start)=>{const seen=new Set([start]),stack=[start];while(stack.length){const v=stack.pop();for(const w of g.get(v)||[])if(!seen.has(w)){seen.add(w);stack.push(w)}}return seen};
    let pins=0,eq=0;
    for(const i of g.keys()){const R=reachable(i);if(R.has(i^1n))pins++;for(const j of R)if((i>>1n)!==(j>>1n)&&reachable(j).has(i))eq++}
    return {pins,eq,vertices:g.size};
  }
  const rows=[];
  for(const k of [2,3,4,6,8,12]){
    const E=[];for(let i=0;i<k;i++)for(let j=k;j<2*k;j++)E.push([i,j]);E.push([0,1]);
    const fs=[],proj=[],qrows=[],cols=new Map();let d=2*k;
    for(const [x,y] of E)for(const [s,t] of [[0,0],[1,1]]){
      const ids=[x,y,d++,d++],flip=1^(s+2*t);
      const lift=a=>ids.reduce((v,id,j)=>v|((a>>j&1)?1n<<BigInt(id):0n),0n);
      for(const [a,b,c,e] of G){
        const A=lift(a),B=lift(b);fs.push([A,B,c^parity(BigInt(a&flip)),e^parity(BigInt(b&flip))]);
        const pairs=new Set();for(let i=0;i<4;i++)for(let j=0;j<4;j++)if(i!==j&&(a>>i&1)&&(b>>j&1)){const p=[ids[i],ids[j]].sort((u,v)=>u-v).join(",");if(pairs.has(p))pairs.delete(p);else pairs.add(p)}
        let r=0n;for(const p of pairs){if(!cols.has(p))cols.set(p,cols.size);r^=1n<<BigInt(cols.get(p))}qrows.push(r);
      }
      proj.push([1n<<BigInt(x),1n<<BigInt(y),s,t]);
    }
    const raw=implications(fs),after=implications(proj);check(raw.pins===0&&raw.eq===0,"raw closure");check(rank(qrows)===fs.length,"quadratic");check(after.pins>0,"projected contradiction candidate");
    // Independent triangle contradiction: each edge of the triangle forbids both equal pairs.
    const tri=E.filter(([a,b])=>[0,1,k].includes(a)&&[0,1,k].includes(b));check(tri.length===3,"triangle");
    for(let x=0;x<8;x++){const ids=[0,1,k];check(tri.some(([a,b])=>(x>>ids.indexOf(a)&1)===(x>>ids.indexOf(b)&1)),"triangle word")}
    rows.push({k,dimension:d,flats:fs.length,native_variables:6*(d+fs.length),raw,projected:after,quadratic_rank:rank(qrows)});
  }
  return {counts,support,rows};
}
console.log(JSON.stringify(replay(),null,2));

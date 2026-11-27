function replay(){
  const bits=x=>(x&1)+((x>>1)&1)+((x>>2)&1);
  const cost=x=>{const n=3-bits(x);return n*(n-1)/2};
  let leaf=0,chain=0,free=0,selector=0;
  for(let mask=0;mask<256;mask++){
    const holes=Array.from({length:8},(_,x)=>x).filter(x=>mask>>x&1);
    const counts=Array.from({length:4},(_,h)=>[+(!!(mask>>h&1)),+(!!(mask>>(h+4)&1))]);
    const n=counts.map(([a,b])=>a+b),m=counts.map(([a,b])=>Math.min(a,b));
    const sum=m.reduce((a,b)=>a+b,0);
    function brute(M){let best=Infinity;for(let u=0;u<8;u++){let c=0;for(const h of holes){const b=(h>>2)^(u&1)^(((u>>1)&1)*(h&1))^(((u>>2)&1)*((h>>1)&1));c+=cost(M[h&3]|(b<<2))}best=Math.min(best,c)}return best}
    const candidates=[];
    for(let p=0;p<4;p++)for(let q=0;q<4;q++)if(p!==q){
      const M=Array(4);M[p]=0;M[q]=3;const rest=[0,1,2,3].filter(h=>h!==p&&h!==q);M[rest[0]]=1;M[rest[1]]=2;
      const exact=n[p]+m[p]+sum-m[q];if(brute(M)!==exact)throw Error("leaf");
      leaf++;candidates.push({p,q,exact});
    }
    const absent=n.indexOf(0);if(absent>=0){if(Math.min(...candidates.map(v=>v.exact))!==Math.min(...candidates.filter(v=>v.p===absent).map(v=>v.exact)))throw Error("free");free++}
    for(let p=0;p<4;p++){const none=n[p]+m[p]+sum;const real=candidates.filter(v=>v.p===p).map(v=>v.exact);if(Math.min(none,...real)!==Math.min(...real))throw Error("selector");selector++}
    for(let r=0;r<2;r++)for(let u0=0;u0<2;u0++)for(let u1=0;u1<2;u1++){
      const U=[u0,u1],M=[0,1,2,3].map(h=>((h&1)^r)|((((h>>1)&1)^U[h&1])<<1));
      let score=0;for(let j=0;j<2;j++){const u=U[j];score+=m[j]+m[j+2]+(j===r?n[j+2*u]+m[j+2*u]:-m[j+2*(1^u)])}
      if(score!==brute(M))throw Error("chain");chain++;
    }
  }
  return {all_tables:256,leaf,chain,free,selector,disagreements:0}
}
console.log(JSON.stringify(replay(),null,2));

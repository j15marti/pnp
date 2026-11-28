function bitplane(ctx,prior){
 const {chart}=ctx;
 const totals={maskBuild:0,maskBitBudget:0,maskCacheEntries:0,maskCachePayloadBits:0};
 const maskCache=new Map();
 function mask(N,s){let key=N+","+s;if(maskCache.has(key))return maskCache.get(key);let x=0n,ones=(1n<<BigInt(s))-1n;totals.maskBuild+=2;totals.maskBitBudget+=s*2;for(let i=0;i<N;i+=2*s){x|=ones<<BigInt(i);totals.maskBuild+=2;totals.maskBitBudget+=2*N}maskCache.set(key,x);totals.maskCacheEntries++;totals.maskCachePayloadBits+=N;return x}
 function lane(test,K){
  let e={bitops:0,chargedBitWidth:0,encodeRows:0,decodeRows:0,scopeReads:0,peakPlaneBits:0,peakWords64:0,tableReads:0,steps:0};
  const op=(n,k=1)=>{e.bitops+=k;e.chargedBitWidth+=n*k};
  function expand(x,vs,U){let V=vs.slice(),N=2**V.length;for(const v of U){e.scopeReads++;if(V.includes(v))continue;let j=U.indexOf(v); // after earlier missing dimensions are inserted, all predecessors of v are present.
    let b=2**j;for(let s=N/2;s>=b;s/=2){x=(x|(x<<BigInt(s)))&mask(2*N,s);op(2*N,3)}
    x|=x<<BigInt(b);op(2*N,2);N*=2;V.splice(j,0,v);
   }return x}
  function eliminate(x,U,v){let N=2**U.length,b=2**U.indexOf(v);x=(x&(x>>BigInt(b)))&mask(N,b);op(N,3);for(let s=b;s<N/2;s*=2){x=(x|(x>>BigInt(s)))&mask(N,2*s);op(N,3)}return x}
  const P=new Map(test.pins),Q=new Map(),out=[];
  function peak(){e.peakPlaneBits=Math.max(e.peakPlaneBits,[...Q.values()].reduce((a,f)=>a+K*2**f.vs.length,0));e.peakWords64=Math.max(e.peakWords64,[...Q.values()].reduce((a,f)=>a+K*Math.ceil(2**f.vs.length/64),0))}
  for(const f of chart){let vs=f.vs.filter(v=>!P.has(v)),A=0n,B=0n;for(let w=0;w<2**vs.length;w++){let old=f.vs.reduce((s,v,j)=>s|((P.has(v)?P.get(v):((w>>vs.indexOf(v))&1))<<j),0),z=f.cost[old]/2;e.encodeRows++;e.tableReads++;if(z>=1){A|=1n<<BigInt(w);op(2**vs.length,2)}if(K===2&&z>=2){B|=1n<<BigInt(w);op(2**vs.length,2)}}Q.set(f.i,{vs,A,B})}peak();
  for(const s of test.plan.steps){e.steps++;let A=0n,B=0n,N=2**s.U.length;for(const id of s.in){let f=Q.get(id);if(!f)throw Error("bad plan");let a=expand(f.A,f.vs,s.U);if(K===2){let b=expand(f.B,f.vs,s.U);B=B|b|(A&a);op(N,3)}A|=a;op(N);Q.delete(id)}
   A=eliminate(A,s.U,s.v);if(K===2)B=eliminate(B,s.U,s.v);
   Q.set(s.id,{vs:s.S,A,B});peak();
   // Decode for independent checking; no loss of ownership or inference by hash equality.
   let expected=test.compressedRows.find(x=>x.id===s.id).cost;
   for(let w=0;w<expected.length;w++){let v=Number((A>>BigInt(w))&1n)+(K===2?Number((B>>BigInt(w))&1n):0);e.decodeRows++;if(v!==Math.min(K,expected[w]))throw Error("bitplane mismatch at "+s.id+" row "+w)}
   out.push({id:s.id,A:A.toString(16),...(K===2?{B:B.toString(16)}:{})});
  }
  let bound=0;for(const f of Q.values()){if(f.vs.length)throw Error("nonconstant");bound=Math.min(K,bound+Number(f.A&1n)+(K===2?Number(f.B&1n):0))}
  if(bound!==Math.min(K,test.exact.bound))throw Error("bound");
  return {K,bound,e,out};
 }
 // Verify every small expansion and min-elimination identity on arbitrary input bit masks for widths up to 3.
 let controls=0;for(let n=0;n<3;n++)for(let j=0;j<=n;j++)for(let x=0;x<2**(2**n);x++){
   let N=2**n,b=2**j,y=BigInt(x);for(let s=N/2;s>=b;s/=2)y=(y|(y<<BigInt(s)))&mask(2*N,s);y|=y<<BigInt(b);
   for(let w=0;w<2*N;w++){let k=(w&(b-1))|((w>>1)&~(b-1));if(Number((y>>BigInt(w))&1n)!==((x>>k)&1))throw Error("expand control")}
   let z=(y&(y>>BigInt(b)))&mask(2*N,b);for(let s=b;s<N;s*=2)z=(z|(z>>BigInt(s)))&mask(2*N,2*s);if(z!==BigInt(x))throw Error("inverse control");controls++;
 }
 // arbitrary pair reduction checks, not just expanded inputs
 for(let n=1;n<=3;n++)for(let j=0;j<n;j++)for(let x=0;x<2**(2**n);x++){
  let N=2**n,b=2**j,z=BigInt(x);z=(z&(z>>BigInt(b)))&mask(N,b);for(let s=b;s<N/2;s*=2)z=(z|(z>>BigInt(s)))&mask(N,2*s);
  for(let w=0;w<N/2;w++){let k=(w&(b-1))|((w&~(b-1))<<1);if(Number((z>>BigInt(w))&1n)!==(((x>>k)&1)&((x>>(k+b))&1)))throw Error("elim control")}controls++;
 }
 let tests=prior.tests.map(t=>{let start=Date.now(),a=lane(t,1),b=lane(t,2);return {pins:t.pins,one:a,two:b,runtimeMs:Date.now()-start}});
 return {controls,totals,tests};
}
if(typeof module!=="undefined")module.exports={bitplane};

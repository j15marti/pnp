// LSPV-2/499 exact GF(2) prefix/suffix inverse, no libraries.
// Native symbolic result: for g=x^d+x^(d/2)+1, solve (1+x)u=v mod g
// with two linear bit passes; finite validation here only.
"use strict";
function inverse1x(v,d) {
  if(d<2 || d%2)throw Error("even d required");
  const m=d/2;
  let out=0n,parity=0n;
  for(let i=d-1;i>=0;i--){
    if(i<m)out|=parity<<BigInt(i);
    parity^=(v>>BigInt(i))&1n;
  }
  parity=0n;
  for(let i=0;i<d;i++){
    parity^=(v>>BigInt(i))&1n;
    if(i>=m)out|=parity<<BigInt(i);
  }
  return out;
}
function times1x(u,d){
  const g=(1n<<BigInt(d))^(1n<<BigInt(d/2))^1n;
  let v=u^(u<<1n);
  if(v&(1n<<BigInt(d)))v^=g;
  return v;
}
function run499inverse(){
  const summary=[];let checks=0,seed=20261108n;
  for(const d of [2,6,18,54]){
    const rounds=d<=6?2**d:(d===18?8192:1024);
    for(let k=0;k<rounds;k++){
      seed=(seed*6364136223846793005n+1442695040888963407n)&((1n<<64n)-1n);
      const v=d<=6?BigInt(k):seed&((1n<<BigInt(d))-1n);
      if(times1x(inverse1x(v,d),d)!==v)throw Error("left inverse "+d+" "+k);checks++;
      if(inverse1x(times1x(v,d),d)!==v)throw Error("right inverse "+d+" "+k);checks++;
    }
    summary.push({d,vectors:rounds,assertions:2*rounds});
  }
  return {status:"PASS",assertions:checks,summary,scope:"The algebraic identity is proved symbolically in the mathematical report; these are finite independent V8 controls."};
}
if(typeof console!=="undefined" && typeof module!=="undefined" && module.exports){console.log(JSON.stringify(run499inverse(),null,2));}

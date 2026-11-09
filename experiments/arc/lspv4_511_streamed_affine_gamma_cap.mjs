// LSPV-4/511: independent streamed GF(2) rank and malformed gamma-header controls.
// No native FLMV interpreter, SAT solver, or R_mix341 checker.
function streamingRank(rows,k) {
  const piv=Array(k).fill(0); let rank=0;
  for(const x of rows) {
    let y=x;
    for(let p=k-1;p>=0;p--) if(y & (1<<p)) {
      if(piv[p]) y^=piv[p]; else {piv[p]=y;rank++;break;}
    }
  }
  return {rank,piv,retainedBits:k*k};
}
function independentRank(rows,k) {
  let a=rows.slice(), rank=0;
  for(let col=k-1;col>=0;col--) {
    const j=a.findIndex((v,i)=>i>=rank && ((v>>col)&1));
    if(j<0)continue;
    [a[rank],a[j]]=[a[j],a[rank]];
    for(let i=0;i<a.length;i++)if(i!==rank&&((a[i]>>col)&1))a[i]^=a[rank];
    rank++;
  }
  return rank;
}
function parity(x){let p=0;while(x){x &= x-1;p^=1;}return p;}
function gamma(n){let s=n.toString(2);return "0".repeat(s.length-1)+s;}
function safeGamma(s,off,L) {
  let z=0,cap=Math.floor(Math.log2(Math.max(1,L)));
  while(off<L&&s[off]==="0"){z++;off++;if(z>cap)return null;}
  if(off+z+1>L)return null;
  const v=parseInt(s.slice(off,off+z+1),2);
  if(v>L)return null;
  return [v,off+z+1];
}
function kOf(H){return Math.max(2,Math.ceil((2*Math.ceil(Math.log2(H)))/5));}
function makePacketShape(H){
  const m=3*H/2,k=kOf(H),w=Math.ceil(Math.log2(m+3*k+1));
  return "10100101"+gamma(H)+gamma(m)+gamma(k)+"0".repeat(3*(4*H+k)*(w+1))+"01";
}
function parseShape(s){
  const L=s.length;if(L<9||s.slice(0,8)!=="10100101")return null;
  let off=8,v=[];
  for(let z=0;z<3;z++){const q=safeGamma(s,off,L);if(!q)return null;v.push(q[0]);off=q[1];}
  let [H,m,k]=v;if(H<4||H%2||m!==3*H/2||k!==kOf(H))return null;
  const w=Math.ceil(Math.log2(m+3*k+1));
  const expect=8+v.reduce((a,x)=>a+gamma(x).length,0)+3*(4*H+k)*(w+1)+2;
  return expect===L&&s.slice(-2)==="01"?{H,m,k,w,L}:null;
}
function run(){
  let checks=0, insertions=0,maxRowLength=0,maxBasisBits=0;
  let seed=0x1a2b3c4d;
  function random(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
  for(let k=1;k<=10;k++)for(const len of [0,1,2,7,31,257]){
    const rows=Array.from({length:len},()=>random()%(1<<k));
    rows.push(0,0,...rows.slice(0,Math.min(8,rows.length)));
    const s=streamingRank(rows,k);
    if(s.rank!==independentRank(rows,k))throw Error("rank mismatch");
    checks++;insertions+=rows.length;maxRowLength=Math.max(maxRowLength,rows.length);maxBasisBits=Math.max(maxBasisBits,s.retainedBits);
    let count=0;
    for(let d=0;d<(1<<k);d++){
      let a=s.piv.every(v=>parity(v&d)===0), b=rows.every(v=>parity(v&d)===0);
      if(a!==b)throw Error("kernel mismatch");
      if(a)count++;checks++;
    }
    if(count!==2**(k-s.rank))throw Error("kernel cardinality");checks++;
  }
  const masks=[9,18,36,8,16,32,64,128], s=streamingRank(masks.slice(0,3),8);
  const match=Array.from({length:256},(_,d)=>d).filter(d=>s.piv.every(v=>parity(v&d)===0)).length;
  if(s.rank!==3||match!==32)throw Error("peer-control");
  checks+=2;
  const accepted=[];
  for(let H of [4,6,8,14,128,2732]){
    const p=makePacketShape(H);if(parseShape(p)?.H!==H)throw Error("shape mismatch");
    accepted.push({H,encodedBits:p.length});
    checks++;
    for(let x of [p.slice(0,-1),p+"0",p.slice(0,-2)+"10"]){if(parseShape(x)!==null)throw Error("malformed accepted");checks++;}
  }
  const rejected=[];
  for(let z of [8,16,32,64,128,256,512]){
    const p="10100101"+"0".repeat(z)+"1".repeat(z+1), L=p.length;
    if(safeGamma(p,8,L)!==null||parseShape(p)!==null)throw Error("oversize accepted");
    rejected.push({inputBits:L,unsafeHeaderValueBits:z+1,capBits:Math.floor(Math.log2(L))+1});
    checks+=2;
  }
  return {status:"COMPUTATIONAL restricted",checks,insertions,maxRowLength,maxBasisBits,peerLSPV2_513:{k:8,rank:3,compatible:32},acceptedHeaderShapesNotCNF:accepted,oversizeGammaRejected:rejected,seed:"0x1a2b3c4d",caveat:"Header-shape tests do not authenticate original graph or Tseitin clauses; no native FLMV/R_mix341 execution."};
}
const result=run();

console.log(JSON.stringify(result,null,2));

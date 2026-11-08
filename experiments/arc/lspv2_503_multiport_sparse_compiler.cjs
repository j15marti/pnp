/* LSPV-2/503: independent finite typed multi-port high-water repair controls.
   Model: symbolic FLMV-indexed operations; NOT a native machine emulator.
   Running: node lspv2_503_multiport_sparse_compiler.cjs */
const result=(function selftest() {
"use strict";
let checks=0;
function ok(b,m){checks++;if(!b)throw Error(m);}
function bits(v,w){return v.toString(2).padStart(w,"0");}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function encode(charges) {
  let clauses=[];
  for(let v=0;v<4;v++){
    let inc=[]; for(let e=0;e<6;e++)if(edges[e].includes(v))inc.push(e+1);
    for(let p=0;p<8;p++){
      let b=[(p>>0)&1,(p>>1)&1,(p>>2)&1];
      if((b[0]^b[1]^b[2])!==charges[v])
        clauses.push(inc.map((id,j)=>(1-b[j])*8+id));
    }
  }
  return "11001010"+bits(clauses.length,8)+clauses.map(c=>c.map(t=>bits(t,4)).join("")).join("");
}
function classify(x){
  if(!/^[01]+$/.test(x)||x.length!==208||x.slice(0,8)!=="11001010"||parseInt(x.slice(8,16),2)!==16)return "MALFORMED";
  let cls=[];
  for(let i=0;i<16;i++){
    let c=[];
    for(let j=0;j<3;j++){
      let t=parseInt(x.slice(16+12*i+4*j,20+12*i+4*j),2);
      let id=t&7,sign=t>>3;
      if(id<1||id>6)return "MALFORMED";
      c.push([id-1,sign]);
    }
    cls.push(c);
  }
  for(let a=0;a<64;a++){
    if(cls.every(c=>c.some(([id,sign])=>((a>>id)&1)===sign)))return "SAT";
  }
  return "UNSAT";
}
function runTyped(x, compiled, k=4) {
  let n=x.length, r=Math.ceil(Math.sqrt(n+1)), L=k*Math.ceil(Math.log2(n+1));
  let A=1n<<BigInt(L), mem=new Map(), indexTape="", moved=0, indexBits=0;
  let high=0n, digest=0, observations=0, errors=0, aliasMap=new Map();
  const addr=i=>compiled?BigInt(i+1):A+BigInt(i);
  const jump=(i)=>{
    let a=addr(i);
    indexTape=a.toString(2); indexBits+=indexTape.length;
    const parsed=BigInt("0b"+indexTape);ok(parsed===a,"index encoding");
    indexTape=""; moved++;
    if(a>high)high=a;
    return a.toString();
  };
  const sourceValue=i=> {observations++;return (n? (x.charCodeAt(i%n)===49?1:0):0)^(i&1);};
  for(let i=0;i<r;i++){
    let pos=jump(i);
    ok(!aliasMap.has(pos),"distinct slot alias"); aliasMap.set(pos,i);
    mem.set(pos,sourceValue(i));
  }
  for(let i=r-1;i>=0;i--){
    let found=mem.get(jump(i)), expected=sourceValue(i);
    if(found!==expected)errors++;
    digest=(digest^((found??0)<<(i%8)))&255;
  }
  ok(indexTape==="","index erasure");
  return {label: classify(x),digest,errors,reads:observations,moves:moved,indexBits,high:high.toString(),cells:mem.size,r,L};
}
let cases=[], sat=0, unsat=0, malformed=0, sourceReads=0,moves=0;
for(let mask=0;mask<16;mask++){
  let charges=Array.from({length:4},(_,j)=>(mask>>j)&1), x=encode(charges);
  let exp=charges.reduce((a,b)=>a^b,0)?"UNSAT":"SAT";
  ok(x.length===208,"strict source bits");ok(classify(x)===exp,"K4 charge truth");
  cases.push(x);
}
let x0=encode([1,0,0,0]);
cases.push("", "0","00110",x0.slice(1),x0+"0","00000000"+x0.slice(8),
           x0.slice(0,8)+"00001111"+x0.slice(16),
           x0.slice(0,16)+"0000"+x0.slice(20));
let seed=123456789;
const random=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0};
for(let z=0;z<80;z++){
  let n=random()%245;let s="";
  for(let i=0;i<n;i++)s+=(random()&1)?"1":"0";
  cases.push(s);
}
let extrema={originalHigh:"0",compiledHigh:0,maxIndexOriginal:0,maxIndexCompiled:0};
for(const x of cases){
  let a=runTyped(x,false),b=runTyped(x,true);
  ok(a.label===b.label,"label preserved");
  ok(a.digest===b.digest&&a.errors===0&&b.errors===0,"data preservation");
  ok(a.moves===b.moves&&a.r===b.r&&a.reads===b.reads,"same typed trace");
  ok(Number(b.high)===b.r,"compiled highwater r");
  ok(BigInt(a.high)===(1n<<BigInt(a.L))+BigInt(a.r-1),"native highwater");
  if(BigInt(a.high)>BigInt(extrema.originalHigh))extrema.originalHigh=a.high;
  extrema.compiledHigh=Math.max(extrema.compiledHigh,Number(b.high));
  extrema.maxIndexOriginal=Math.max(extrema.maxIndexOriginal,a.indexBits);
  extrema.maxIndexCompiled=Math.max(extrema.maxIndexCompiled,b.indexBits);
  moves+=a.moves;sourceReads+=a.reads;
  if(a.label==="SAT")sat++;else if(a.label==="UNSAT")unsat++;else malformed++;
}
const out={status:"PASS",checks,cases:cases.length,sat,unsat,malformed,moves,sourceReads,
           k:4,originalHighWaterMax:extrema.originalHigh,compiledHighWaterMax:extrema.compiledHigh,
           indexBitsOriginalMax:extrema.maxIndexOriginal,indexBitsCompiledMax:extrema.maxIndexCompiled,
           exampleK4:{N:208,r:Math.ceil(Math.sqrt(209)),virtualHigh:( (1n<<32n)+14n).toString(),physicalHigh:15}};
return out;
})();
console.log(JSON.stringify(result,null,2));

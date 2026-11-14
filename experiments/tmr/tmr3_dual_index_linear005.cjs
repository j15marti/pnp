"use strict";
/*
 * TMR-3/005: exact E_n canonical 3-CNF source authentication with TWO persistent
 * indexed read ports. Finite JavaScript semantic and charged-address emulator.
 * Not an instruction-level Turing-machine execution. Run:
 * node tmr3_dual_index_linear005.cjs
 */
const assert = require("node:assert/strict");
function width(n) { return Math.max(1, Math.ceil(Math.log2(n))); }
function bits(x,w){return x.toString(2).padStart(w,"0");}
function encode(n,a,b){
  assert(n>=1 && a.length===n && b.length===n);
  const w=width(5*n);let s="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
  for(let bank=0;bank<2;bank++)for(let j=0;j<n;j++){
    const z=bank===0?a:b, aux=(bank===0?n:3*n)+2*j;
    for(const [u,v] of [[0,0],[0,1],[1,0],[1,1]]){
      s+=String(1-z[j])+bits(j,w)+String(u)+bits(aux,w)+String(v)+bits(aux+1,w);
    }
  }
  return s;
}
function bitChanges(oldV,newV){
  let a=BigInt(oldV),b=BigInt(newV),count=0;
  for(let v=a^b;v;v>>=1n)count+=Number(v&1n);
  return count;
}
function check(src){
  const L=src.length, aw=width(L+2);
  const cost={length:L,addrWidth:aw,mainReads:0,anchorReads:0,mainAddrBitChanges:0,
    anchorAddrCharged:0,chargedParserOps:0,maxAddressBits:2*aw,anchorJumps:0};
  let p=0, mainAddr=0,anchorAddr=0;
  function readMain(){
    if(p>=L)return "#";
    // The sequential indexed address register is incremented in binary.
    if(p!==mainAddr){cost.mainAddrBitChanges+=bitChanges(mainAddr,p);mainAddr=p;}
    cost.mainReads++;let c=src[p];p++;
    return c;
  }
  function readAnchor(address){
    if(address<0||address>=L)throw Error("invalid anchor address");
    // A second persistent address port moves forward by g once per block.
    // Conservatively charge O(aw) ordinary tape steps for each addition.
    cost.anchorAddrCharged+=2*aw+3;cost.anchorJumps++;
    cost.anchorAddrCharged+=bitChanges(anchorAddr,address);anchorAddr=address;
    cost.anchorReads++;return src[address];
  }
  function bad(){return {member:false,sat:null,...cost};}
  if(!L||!Array.from(src).every(c=>c==="0"||c==="1"))return bad();
  let N=0,c;
  while((c=readMain())==="1")N++;
  if(c!=="0"||!N||N%5!==0)return bad();
  const n=N/5,M=8*n,w=width(N),g=12*(1+w),base=13*n+2;
  if(L!==base+2*n*g)return bad();
  for(let i=0;i<M;i++)if(readMain()!=="1")return bad();
  if(readMain()!=="0"||p!==base)return bad();
  let equal=true, anchor=base;
  function idIs(v){
    for(let k=w-1;k>=0;k--){
      cost.chargedParserOps+=2;
      if(readMain()!==String((v>>k)&1))return false;
    }
    return true;
  }
  for(let bank=0;bank<2;bank++)for(let j=0;j<n;j++){
    const aux=(bank===0?n:3*n)+2*j;
    let lead=null;
    for(const [u,v] of [[0,0],[0,1],[1,0],[1,1]]){
      cost.chargedParserOps+=12*w+20; // conservative expected IDs/counters overhead
      const z=readMain();
      if(z!=="0"&&z!=="1")return bad();
      if(lead===null)lead=z;
      if(z!==lead||!idIs(j))return bad();
      if(readMain()!==String(u)||!idIs(aux))return bad();
      if(readMain()!==String(v)||!idIs(aux+1))return bad();
    }
    if(bank===1){if(lead!==readAnchor(anchor))equal=false;anchor+=g;}
  }
  if(p!==L)return bad();
  // INDEX reads of the endmarker can be made with a charged address update.
  cost.mainAddrBitChanges+=bitChanges(mainAddr,L);cost.chargedParserOps+=2*aw;
  return {member:true,sat:equal,n,w,...cost,
    proxyTime:cost.mainReads+cost.anchorReads+cost.mainAddrBitChanges+
      cost.anchorAddrCharged+cost.chargedParserOps+L};
}
function run(){
  const out={id:"TMR3-DI5",model:"finite JS TWO persistent INDEX-port exact-source emulator; no physical TM",status:"COMPUTATIONAL",cases:0,sat:0,unsat:0,malformedRejects:0,assertions:0,failures:0,maxN:0,maxL:0,totalIndexedReads:0,totalAnchorReads:0,maxRatio:0,samples:[],seed:"0x5a1c09f1"};
  function ok(cond,msg){out.assertions++;if(!cond){out.failures++;throw Error(msg);}}
  function one(n,a,b){
    const s=encode(n,a,b),c=check(s),eq=a.every((x,i)=>x===b[i]);
    ok(c.member && c.sat===eq,"family label");
    ok(c.mainReads===s.length,"all original bits authenticated");
    ok(c.anchorReads===n && c.anchorJumps===n,"one indexed anchor per pair");
    ok(c.maxAddressBits===2*width(s.length+2),"charged two addresses");
    ok(c.proxyTime<=80*(s.length+1),"linear proxy witness");
    ok(s.length===13*n+2+24*n*(1+c.w),"encoded length");
    out.cases++;out[c.sat?"sat":"unsat"]++;out.maxN=Math.max(n,out.maxN);
    out.maxL=Math.max(s.length,out.maxL);out.totalIndexedReads+=c.mainReads+c.anchorReads;
    out.totalAnchorReads+=c.anchorReads;
    out.maxRatio=Math.max(out.maxRatio,c.proxyTime/s.length);
    if(out.cases<8||n>=64&&a.every(x=>x===0)&&b.every(x=>x===0)){
      out.samples.push({n,L:s.length,sat:eq,proxyTime:c.proxyTime,
        ratio:+(c.proxyTime/s.length).toFixed(3),anchorReads:c.anchorReads,
        idxProductUpperRatio:+((c.proxyTime*c.maxAddressBits)/(s.length*n)).toFixed(5)});
    }
    const mutations=[s.slice(0,-1),s+"1",s.slice(1),s.slice(0,13*n+2)+"2"+s.slice(13*n+3)];
    // Flip an auxiliary sign, or one of the repeated x-sign bits in a block.
    const start=13*n+2,auxSign=start+1+c.w,repeat=start+3*(1+c.w);
    for(const pos of [auxSign,repeat]){
      mutations.push(s.slice(0,pos)+(s[pos]==="0"?"1":"0")+s.slice(pos+1));
    }
    for(const t of mutations){ok(!check(t).member,"structural mutation accepted");out.malformedRejects++;}
  }
  for(let n=1;n<=5;n++)for(let x=0;x<2**n;x++)for(let y=0;y<2**n;y++){
    one(n,Array.from({length:n},(_,i)=>(x>>i)&1),Array.from({length:n},(_,i)=>(y>>i)&1));
  }
  let state=0x5a1c09f1;function rnd(){state=(Math.imul(state,1664525)+1013904223)>>>0;return (state>>>20)&1;}
  for(const n of [6,8,16,32,64,128])for(let k=0;k<12;k++){
    const a=Array.from({length:n},rnd),b=k%3===0?a.slice():Array.from({length:n},rnd);one(n,a,b);
  }
  for(const n of [128,256,512,1024,2048]){
    const zeros=Array(n).fill(0);one(n,zeros,zeros);
  }
  out.maxRatio=+out.maxRatio.toFixed(4);
  return out;
}
if(require.main===module)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
module.exports={encode,check,run};

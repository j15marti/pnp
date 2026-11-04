/* Invoke: node -e 'console.log(require("./lspv1_387_majority_pivotality.js")())' */
module.exports=function(){
"use strict";
/* LSPV-1/387: majority-coded sign-critical guarded bit-PHP controls.
 * Deterministic; independent checker is a separate implementation. */
function ok(c,m){ if(!c) throw Error(m); checks++; }
let checks=0;
const gamma=x=>{const b=x.toString(2);return "0".repeat(b.length-1)+b};
const bitflip=(s,positions)=>{let a=s.split("");for(const p of positions)a[p]=a[p]==="0"?"1":"0";return a.join("")};
const majority=s=>{if(s.length%3)throw Error("triplet length");let v="";for(let i=0;i<s.length;i+=3){let a=s.slice(i,i+3);if(!/^[01]{3}$/.test(a))throw Error("nonbinary");v+=([...a].filter(c=>c==="1").length>=2?"1":"0")}return v};
function source(ell){
 let n=2**ell,V=(n+1)*ell+1,t=V,c=[],w=V.toString(2).length,metadata=[];
 for(let i=0;i<n+1;i++)for(let j=i+1;j<n+1;j++)for(let a=0;a<n;a++){
  let ls=[-t];
  for(let p of [i,j])for(let b=0;b<ell;b++){let id=1+p*ell+b;ls.push((a>>b)&1?-id:id)}
  metadata.push({i,j,a});c.push(ls);
 }
 c.push([t]);metadata.push({unit:true});
 const m=c.length;
 let encoded="1011"+gamma(V+1)+gamma(m+1),coords=[];
 for(let ci=0;ci<m;ci++){
  encoded+=gamma(c[ci].length+1);
  for(let li=0;li<c[ci].length;li++){let l=c[ci][li];coords.push({index:encoded.length,ci,li});encoded+=(l>0?"1":"0")+Math.abs(l).toString(2).padStart(w,"0")}
 }
 return {n,V,t,c,m,metadata,encoded,coords}
}
function parse(s){
 if(!/^[01]+$/.test(s)||s.slice(0,4)!=="1011")throw Error("tag/nonbinary");
 let p=4;
 const readGamma=()=>{let z=0;while(p<s.length&&s[p]==="0"){z++;p++}if(p+z>=s.length)throw Error("gamma");let y=parseInt(s.slice(p,p+z+1),2);p+=z+1;return y};
 const V=readGamma()-1,m=readGamma()-1;
 if(V<=0||m<=0||m>100000)throw Error("header");
 let w=V.toString(2).length,c=[];
 for(let i=0;i<m;i++){let k=readGamma()-1;if(k<=0||k>V*2+3)throw Error("clause width");let ls=[];
 for(let j=0;j<k;j++){if(p+1+w>s.length)throw Error("trunc");let sign=s[p++],idx=parseInt(s.slice(p,p+w),2);p+=w;if(idx<=0||idx>V)throw Error("variable");ls.push(sign==="1"?idx:-idx)}
 c.push(ls)}
 if(p!==s.length)throw Error("trailing");
 return {V,c}
}
function assignmentFor(S,ci){
 let z=Array(S.V+1).fill(false);
 if(ci===S.c.length-1){z[S.t]=false;return z}
 const {i,j,a}=S.metadata[ci];let holes=Array.from({length:S.n},(_,k)=>k).filter(k=>k!==a),q=0;
 for(let p=0;p<S.n+1;p++){let h=(p===i||p===j)?a:holes[q++];for(let b=0;b<Math.log2(S.n);b++)z[1+p*Math.log2(S.n)+b]=Boolean((h>>b)&1)}
 z[S.t]=true;return z;
}
function isSatisfied(c,z){return c.every(C=>C.some(l=>l>0?z[l]:!z[-l]))}
function test(ell){
 const S=source(ell),k=S.coords.length,expected={1:[125,19],2:[1230,201],3:[14151,2017]}[ell];
 ok(S.encoded.length===expected[0],"N mismatch "+ell);
 ok(k===expected[1],"K mismatch "+ell);
 ok(parse(S.encoded).c.length===S.c.length,"source parse");
 let raw=S.encoded,trip=[...raw].map(c=>c+c+c).join("");
 let selected=ell<3?S.coords.filter(()=>true):S.coords.filter((x,i)=>i%17===0);
 for(const p of selected){
  const expectedF=bitflip(raw,[p.index]),changed=S.c.map(row=>row.slice());
  changed[p.ci][p.li]*=-1;
  ok(parse(expectedF).c.length===S.m,"opposite format");
  const z=assignmentFor(S,p.ci);
  ok(isSatisfied(changed,z),"SAT sign neighbor "+ell+":"+p.index);
  for(let a=0;a<3;a++){
   let one=bitflip(trip,[3*p.index+a]);
   ok(majority(one)===raw,"one bit must be neutral");
   ok(parse(majority(one)).c.length===S.m,"one decoded valid");
  }
  for(const pair of [[0,1],[0,2],[1,2]]){
   let y=bitflip(trip,pair.map(b=>3*p.index+b));
   ok(majority(y)===expectedF,"two bits toggle logical sign");
   ok(isSatisfied(changed,z),"opposite SAT witness");
  }
 }
 if(ell===1||ell===2){
  // small source UNSAT direct check, not the proof of the infinite family
  for(let mask=0;mask<(1<<S.V);mask++){
   const z=Array(S.V+1).fill(false);
   for(let i=1;i<=S.V;i++)z[i]=Boolean((mask>>(i-1))&1);
   ok(!isSatisfied(S.c,z),"source erroneously SAT");
  }
 }
 return {ell,N:raw.length,K:k,tripledBits:trip.length,selectedSignBits:selected.length,
         oneBitNeutralCases:3*selected.length,twoBitSATCases:3*selected.length,
         deterministicReadsFloor:2*k,randomizedCoefficientNumerator:3*k};
}
const results=[1,2,3].map(test);
const neg=source(1),base=[...neg.encoded].map(c=>c.repeat(3)).join("");
let malformed=0;
for(const s of [base+"1","",base.slice(1),base.replace(/^1011/,"0011").split("").map(c=>c.repeat(3)).join(""),
                "222","000","111"]){
 try{let x=majority(s);parse(x)}catch(e){malformed++;}
}
ok(malformed>=5,"malformed controls");
return {id:"LSPV1_387_MAJORITY_INPUT_CODE",results,checks,malformed,seed:null,
 status:"COMPUTATIONAL; theorem proved symbolically in report"};
};
if(require.main===module) console.log(JSON.stringify(module.exports(),null,2));

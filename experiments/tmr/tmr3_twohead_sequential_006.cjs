"use strict";
/* TMR-3/006: independent, two local read-only input heads, no INDEX operations.
   Emulates source reads and head moves; charges work symbol operations by a
   conservative source-level proxy. Not an instruction-level physical TM. */
const fs = require("fs");
const W = n => Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
const B = (v,w) => v.toString(2).padStart(w,"0");
function encode(n,a,b) {
  const w=W(5*n);
  let s="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
  for (const [bank,v] of [[0,a],[1,b]]) for(let i=0;i<n;i++) {
    const z=(bank===0?n:3*n)+2*i, sign=1-v[i];
    for(let u=0;u<2;u++)for(let t=0;t<2;t++)
      s+=sign+B(i,w)+u+B(z,w)+t+B(z+1,w);
  }
  return s;
}
function simulate(src) {
  let p=0,q=0,headMoves=0,readEvents=0,workProxy=0,compared=0;
  const l=src.length;
  function nextFirst(){let x=p<l?src[p]:"#";readEvents++;if(x!=="#"){p++;headMoves++}return x}
  function paired(){let x=p<l?src[p]:"#", y=q<l?src[q]:"#";readEvents+=2;if(x!=="#"){p++;headMoves++}if(y!=="#"){q++;headMoves++}return [x,y]}
  const nope=()=>({member:false,headMoves,readEvents,workProxy,compared});
  let n5=0, ch;
  while((ch=nextFirst())==="1")n5++;
  if(ch!=="0"||n5<5||n5%5!==0)return nope();
  const n=n5/5;
  for(let j=0;j<8*n;j++)if(nextFirst()!=="1")return nope();
  if(nextFirst()!=="0")return nope();
  const w=W(5*n), h=13*n+2, g=12*(w+1), second=h+n*g;
  if(p!==h)return nope();
  // Position second read-only head with exactly 'second' paid local moves.
  // A charged binary downcounter implements the loop in O(second) steps.
  for(let j=0;j<second;j++){if(q>=l)return nope();q++;headMoves++;workProxy+=3}
  workProxy+=40*W(l+2)*W(l+2); // finite proxy for small header arithmetic
  let equal=true;
  for(let i=0;i<n;i++){
    const z1=n+2*i, z2=3*n+2*i;
    let sign1=null,sign2=null;
    for(let u=0;u<2;u++)for(let v=0;v<2;v++){
      let [s1,s2]=paired();
      if((s1!=="0"&&s1!=="1")||(s2!=="0"&&s2!=="1"))return nope();
      if(sign1===null){sign1=s1;sign2=s2;equal&&=s1===s2;compared++}
      if(s1!==sign1||s2!==sign2)return nope();
      const exp1=B(i,w)+u+B(z1,w)+v+B(z1+1,w);
      const exp2=B(i,w)+u+B(z2,w)+v+B(z2+1,w);
      for(let j=0;j<exp1.length;j++){
        const [a,b]=paired();
        if(a!==exp1[j]||b!==exp2[j])return nope();
      }
      workProxy+=50*(w+1); // charge expected-field scans and resets
    }
  }
  const end2=q<l?src[q]:"#";readEvents++;
  if(end2!=="#" || p!==second || q!==l)return nope();
  return {member:true,sat:equal,n,L:l,headMoves,readEvents,workProxy,compared};
}
function brute(n,src){
  const w=W(5*n),h=13*n+2,rec=3*(w+1), clauses=[];
  for(let k=0;k<8*n;k++){
    const c=[];
    for(let j=0;j<3;j++){
      const lit=src.slice(h+k*rec+j*(w+1),h+k*rec+(j+1)*(w+1));
      c.push([parseInt(lit.slice(1),2),lit[0]==="1"]);
    }clauses.push(c);
  }
  for(let a=0;a<2**(5*n);a++)if(clauses.every(c=>c.some(([v,neg])=>Boolean((a>>v)&1)!==neg)))return true;
  return false;
}
function run(){
  const st={id:"TMR3-TH6",model:"two independent sequential read-only heads, no INDEX",tests:0,sat:0,unsat:0,mutations:0,originalBrute:0,headMoves:0,readEvents:0,comparisons:0,maxL:0,maxMovesPerL:0,failures:0,samples:[]};
  function check(ok,msg){if(!ok){st.failures++;throw Error(msg)}}
  function trial(n,a,b,perturb){
    let src=encode(n,a,b),r=simulate(src),want=a.every((x,i)=>x===b[i]);
    check(r.member&&r.sat===want,"classify n="+n);check(r.compared===n,"comparison count");
    check(r.headMoves<=2*src.length,"head movement cap");
    st.tests++;st[r.sat?"sat":"unsat"]++;st.headMoves+=r.headMoves;st.readEvents+=r.readEvents;st.comparisons+=r.compared;
    st.maxL=Math.max(st.maxL,src.length);st.maxMovesPerL=Math.max(st.maxMovesPerL,r.headMoves/src.length);
    if(st.samples.length<6||n>=512&&st.samples.every(v=>v.n!==n))st.samples.push({n,L:src.length,headMoves:r.headMoves,workProxy:r.workProxy,sat:r.sat});
    if(n<=2){check(brute(n,src)===want,"original CNF brute");st.originalBrute++}
    if(perturb){
      const w=W(5*n),h=13*n+2,g=12*(w+1),badPositions=[0,5*n+1,h+1,h+g+2];
      for(const k of badPositions){let v=src.slice(0,k)+(src[k]==="1"?"0":"1")+src.slice(k+1);check(!simulate(v).member,"bad field at "+k);st.mutations++}
      const signpos=h+(w+1)*3;
      let v=src.slice(0,signpos)+(src[signpos]==="1"?"0":"1")+src.slice(signpos+1);
      check(!simulate(v).member,"broken sign consistency");st.mutations++;
      for(const v of [src.slice(0,-1),src+"0"]){check(!simulate(v).member,"wrong length");st.mutations++}
    }
  }
  for(let n=1;n<=5;n++)for(let am=0;am<2**n;am++)for(let bm=0;bm<2**n;bm++)trial(n,Array.from({length:n},(_,i)=>(am>>i)&1),Array.from({length:n},(_,i)=>(bm>>i)&1),true);
  let seed=0x31415926;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>0};
  for(const n of [8,16,32,64,128,256,512,1024])for(let z=0;z<8;z++){
    const a=Array.from({length:n},()=>rnd()&1), b=z===0?a.slice():Array.from({length:n},()=>rnd()&1);
    trial(n,a,b,true);
  }
  check(st.failures===0,"failures");
  return st;
}
if(require.main===module){const s=run();console.log(JSON.stringify(s,null,2));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(s,null,2)+"\n")}
module.exports={encode,simulate,brute,run};

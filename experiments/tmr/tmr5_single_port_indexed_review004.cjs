"use strict";
// TMR-5/004 independent one-port, charged-index finite source emulator.
// This is NOT an instruction-level Turing machine; the mathematical proof is separate.
function W(n){return Math.max(1,Math.ceil(Math.log2(Math.max(n,2))))}
function enc(n,a,b){
 let s="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0",w=W(5*n);
 for(let bank=0;bank<2;bank++)for(let i=0;i<n;i++){
  let bit=(bank?b:a)[i],z=bank?3*n+2*i:n+2*i;
  for(let u=0;u<=1;u++)for(let v=0;v<=1;v++)
   s+=String(1-bit)+i.toString(2).padStart(w,"0")+u+
       z.toString(2).padStart(w,"0")+v+(z+1).toString(2).padStart(w,"0");
 }
 return s;
}
function onePort(src){
 let main=0,reg=0,mode="main",cost=0,reads=0,anchors=0,swaps=0;
 const aw=W(src.length+2);
 const query=(addr)=>addr<src.length?src[addr]:"#";
 function mainRead(){
  if(mode!=="main"){cost+=6*aw+4;reg=main;mode="main";swaps++;}
  if(reg!==main)throw Error("port cursor lost");
  let ch=query(reg);cost++;reads++;
  if(ch!=="#"){
   let k=0,v=reg;
   while(v%2===1){k++;v=Math.floor(v/2)}
   cost+=4*(k+1)+3;reg++;main++;
  }
  return ch;
 }
 function remote(addr){
  if(mode!=="remote"){cost+=6*aw+4;mode="remote";swaps++;}
  reg=addr;cost+=4*aw+2;anchors++;cost++;return query(reg);
 }
 function eqBits(num,w){
  for(let j=w-1;j>=0;j--){cost+=3;if(mainRead()!==String(Math.floor(num/2**j)%2))return false;}
  return true;
 }
 const no=()=>({member:false,cost,reads,anchors,swaps,aw});
 let N=0,c;
 while((c=mainRead())==="1")N++;
 if(c!=="0"||N<5||N%5!==0)return no();
 const n=N/5,w=W(N),g=12*(w+1),base=13*n+2;
 for(let i=0;i<8*n;i++)if(mainRead()!=="1")return no();
 if(mainRead()!=="0"||main!==base)return no();
 let equal=true,anchorAddress=base;
 for(let bank=0;bank<2;bank++)for(let i=0;i<n;i++){
  let aux=bank===0?n+2*i:3*n+2*i,sign=null;
  for(let u=0;u<=1;u++)for(let v=0;v<=1;v++){
   let q=mainRead();
   if(q!=="0"&&q!=="1")return no();
   if(sign===null)sign=q;
   if(q!==sign||!eqBits(i,w)||mainRead()!==String(u)||
      !eqBits(aux,w)||mainRead()!==String(v)||!eqBits(aux+1,w))return no();
   cost+=5*w+7;
  }
  if(bank===1){
   const saved=main,first=remote(anchorAddress);
   if(first!==sign)equal=false;
   anchorAddress+=g;cost+=8*aw+3;
   if(main!==saved)throw Error("saved cursor changed");
  }
 }
 if(mainRead()!=="#")return no();
 return {member:true,sat:equal,n,L:src.length,cost,reads,anchors,swaps,aw};
}
function audit(){
 let res={id:"TMR5-SI4",kind:"independent V8 single persistent INDEX-port source emulator; NOT physical TM",
 cases:0,sat:0,unsat:0,structuralRejects:0,assertions:0,failures:0,
 maxN:0,maxL:0,maxCostRatio:0,anchors:0,portSwitches:0,samples:[]};
 const yes=(p,msg)=>{res.assertions++;if(!p){res.failures++;throw Error(msg)}};
 function caseOne(n,a,b){
  const s=enc(n,a,b),r=onePort(s),expected=a.every((v,i)=>v===b[i]);
  yes(r.member&&r.sat===expected,"classification");
  yes(r.anchors===n,"anchor count");
  yes(r.reads===s.length+1,"complete source + endmarker");
  yes(r.swaps===2*n,"paid port switches");
  yes(r.cost<=100*(s.length+1),"linear charged proxy");
  res.cases++;res[expected?"sat":"unsat"]++;res.anchors+=r.anchors;
  res.portSwitches+=r.swaps;res.maxN=Math.max(res.maxN,n);
  res.maxL=Math.max(res.maxL,s.length);
  res.maxCostRatio=Math.max(res.maxCostRatio,r.cost/s.length);
  if(n===1||n>=32&&a.every(x=>x===0)&&b.every(x=>x===0))
   res.samples.push({n,L:s.length,cost:r.cost,ratio:+(r.cost/s.length).toFixed(3),switches:r.swaps});
  for(const bad of [s.slice(0,-1),s+"1",s.slice(1),
                  s.slice(0,13*n+2)+"2"+s.slice(13*n+3)]){
   yes(!onePort(bad).member,"malformed/length reject");res.structuralRejects++;
  }
  const pos=13*n+2+1+W(5*n);
  const flipped=s.slice(0,pos)+(s[pos]==="0"?"1":"0")+s.slice(pos+1);
  yes(!onePort(flipped).member,"damaged auxiliary rejected");res.structuralRejects++;
 }
 for(let n=1;n<=5;n++)for(let i=0;i<2**n;i++)for(let j=0;j<2**n;j++)
  caseOne(n,Array.from({length:n},(_,k)=>(i>>k)&1),
          Array.from({length:n},(_,k)=>(j>>k)&1));
 let seed=0x9ed12a15;
 const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return(seed>>>23)&1};
 for(const n of [8,16,32,64,128,256,512])for(let t=0;t<7;t++){
  let a=Array.from({length:n},rnd),
      b=t%3===0?a.slice():Array.from({length:n},rnd);
  caseOne(n,a,b);
 }
 for(let n of [1024,2048])caseOne(n,Array(n).fill(0),Array(n).fill(0));
 res.maxCostRatio=+res.maxCostRatio.toFixed(4);return res;
}
if(typeof require!=="undefined"&&require.main===module)
 process.stdout.write(JSON.stringify(audit(),null,2)+"\n");
if(typeof module!=="undefined")module.exports={enc,onePort,audit};

/* LSPV-3 CONTEXTUAL-PORT-LEAK163: independent pure JS finite source check.
   No SAT oracle; no unrestricted P versus NP claim. */
"use strict";
const csv="-5,-12,15;-5,-6,-15;-4,-9,-11;-4,-8,-11;-3,6,-15;-3,12,15;-2,-6,12;-2,5,-12;-1,3,-14;-1,13,14;1,-7,10;1,7,13;2,-9,11;2,-8,9;3,7,-13;4,8,-10;4,9,-10;5,8,-14;6,-7,11;10,-13,14";
const G=csv.split(";").map(c=>c.split(",").map(Number));
function lit(l,m){return Boolean((m>>(Math.abs(l)-1))&1)===(l>0);}
function ok(c,m){return c.some(l=>lit(l,m));}
function tup(m){return (m&3)|((m>>10)&4);}
function foot(c,m){return c.filter(l=>Math.abs(l)!==4).some(l=>lit(l,m))?1:0;}
function run(){
 let src={},pun=[{},{}],models=0;
 for(let m=0;m<32768;m++){
  if(G.every(c=>ok(c,m))){models++;let k=tup(m)+":"+((m>>3)&1);src[k]=(src[k]||0)+1;}
  for(let f=0;f<2;f++){
   let slots=f?[15,16]:[2,3];
   if(G.every((c,j)=>slots.includes(j)||ok(c,m))){
    let k=(((m>>3)&1)^f)+":"+foot(G[slots[0]],m)+foot(G[slots[1]],m);
    pun[f][k]=(pun[f][k]||0)+1;
   }
  }
 }
 let expect={"0:0":32,"0:1":29,"1:0":16,"2:0":10,"2:1":8,"4:0":44,"4:1":37,"5:0":36,"5:1":32,"6:0":10,"6:1":8,"7:0":5,"7:1":5};
 if(models!==272 || JSON.stringify(Object.entries(src).sort())!==JSON.stringify(Object.entries(expect).sort()))
  throw Error("source profile mismatch");
 for(let f=0;f<2;f++)if(pun[f]["0:00"]!==(f?119:153)||Object.keys(pun[f]).some(k=>k.startsWith("0:")&&k!=="0:00"))
  throw Error("double-puncture mismatch");
 const allowed=(t,f)=>t===3?[]:t===1?[f]:[0,1];
 const sat=(a,b,f,g)=>allowed(a,f).some(p=>allowed(b,g).includes(p));
 let modes=[];
 for(let f=0;f<2;f++)for(let g=0;g<2;g++){
  let yes=0;for(let a=0;a<8;a++)for(let b=0;b<8;b++)if(sat(a,b,f,g))yes++;
  modes.push({modes:[f,g],sat:yes,unsat:64-yes});
 }
 if(JSON.stringify(modes.map(x=>x.sat))!=="[49,48,48,49]" || !sat(1,1,0,0)||sat(1,1,0,1))
  throw Error("contextual composition mismatch");
 return {source_models:models,source_four_port:src,double_puncture:pun,modes,
  source_assignments_tested:32768,
  status:"COMPUTATIONAL finite-source lemma, not a general SAT theorem"};
}
if(typeof module!=="undefined" && module.exports)module.exports={run};
if(typeof console!=="undefined" && typeof module==="undefined")console.log(JSON.stringify(run(),null,2));

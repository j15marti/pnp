// LSPV-4/454 compact, self-contained verifier for original signed strict-3CNF controls.
// Run with Node.js: node experiments/arc/lspv4_454_gray_pin_selfcheck.js
"use strict";
let checks=0;
function ok(cond,msg){if(!cond)throw Error(msg||"assertion");checks++;}
function sat(F){
  const m=Math.max(0,...F.flat().map(Math.abs));
  if(m>16)throw Error("test oracle limit");
  for(let mask=0;mask<2**m;mask++)
    if(F.every(c=>c.some(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0))))
      return true;
  return false;
}
function gadget(l,u,v){
  return [[l,u,v],[l,u,-v],[l,-u,v],[l,-u,-v]];
}
for(const l of [1,-1])for(let a=0;a<2;a++){
  const clauses=gadget(l,2,3).concat([[a?1:-1]]);
  ok(sat(clauses)===(l>0?Boolean(a):!a),"unit gadget semantics");
}
let flips=0;
for(let k=0;k<=5;k++){
  const vars=Array.from({length:k},(_,i)=>i+1);
  const child=vars.flatMap((v,i)=>gadget(-v,k+2*i+1,k+2*i+2));
  const initLength=child.length; let last=0;
  for(let t=0;t<2**k;t++){
    const gray=t^(t>>1);
    if(t){
      const changed=gray^last;
      ok(changed!==0&&(changed&(changed-1))===0,"one Gray bit");
      const j=Math.log2(changed);
      for(let x=4*j;x<4*j+4;x++){child[x][0]=-child[x][0];flips++;}
    }
    last=gray;
    const reference=vars.flatMap((v,i)=>
      gadget((gray&(1<<i))?v:-v,k+2*i+1,k+2*i+2));
    ok(JSON.stringify(child)===JSON.stringify(reference),"fixed original content / length");
    ok(child.length===initLength,"constant child length");
  }
}
ok(flips===228,"exact Gray sign changes");
function k4(charge){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const F=[];
  for(let v=0;v<4;v++){
    const incident=edges.map((edge,i)=>edge.includes(v)?i+1:null).filter(Boolean);
    for(let p=0;p<2;p++)for(let q=0;q<2;q++){
      const s=[p,q,p^q^1^(v===3?charge:0)];
      F.push(incident.map((id,i)=>s[i]?-id:id));
    }
  }
  return F;
}
ok(sat(k4(0))===true,"K4 parity SAT");
ok(sat(k4(1))===false,"K4 parity UNSAT");
for(const secondSign of [-1,1]){
  const block1=gadget(1,2,3);
  const block2=gadget(secondSign,4,5);
  let frontier=false;
  for(const bit of [false,true]){
    const pin=[bit?1:-1];
    frontier=frontier||
      (sat(block1.concat([pin]))&&sat(block2.concat([pin])));
    // The guest can also accept a strict-3CNF pin gadget.
    ok(sat(block1.concat(gadget(pin[0],6,7)))===sat(block1.concat([pin])),"strict guest");
    ok(sat(block2.concat(gadget(pin[0],6,7)))===sat(block2.concat([pin])),"strict guest");
  }
  ok(frontier===sat(block1.concat(block2)),"two-block AND/OR");
  ok(frontier===(secondSign===1),"both labels");
}
const malformed=[[1,1,2],[1,-1,2],[1,2,3,4]];
for(const c of malformed)
  ok(c.length!==3||new Set(c.map(Math.abs)).size!==3,"bad strict clause rejected");
console.log(JSON.stringify({status:"PASS",checks,gray_signed_field_flips:flips,k4_labels:["SAT","UNSAT"],path_labels:["UNSAT","SAT"]}));

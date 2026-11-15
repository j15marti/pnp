#!/usr/bin/env node
"use strict";
/* Independent all-core projection verification, TMR-3/041. */
function projectionAudit081(){
  "use strict";
  let checks=0,broken=0,controls=0;
  const ok=(x,t)=>{checks++;if(!x){broken++;throw Error(t)}};
  let s=0xF15A2E07;
  const next=()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return s>>>0};
  const val=(l,a)=>((a.get(Math.abs(l))||0)^(l<0?1:0));
  const sat=(F,a)=>F.every(c=>c.some(l=>val(l,a)));
  const canon=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  for(let core=1;core<=5;core++)for(let trial=0;trial<48;trial++){
    let g=1+(next()%8), F=[], triples=[];
    for(let j=0;j<g;j++){
      let a=1+(next()%core),b=1+(next()%core);
      if(core>1&&a===b)b=(b%core)+1;
      const leaf=core+j+1;
      let variables=core===1?[a,leaf,core+g+j+1]:[a,b,leaf];
      if(core===1){ok(variables[1]!==variables[2],"distinct leaves");}
      const signed=variables.map(v=>(next()&1)?v:-v);
      triples.push({signed,leaf:(core===1?variables[1]:leaf),altLeaf:core===1?variables[2]:null});
      F.push(signed,signed.map(l=>-l));
    }
    const maxvar=core===1?core+2*g:core+g;
    for(let mask=0;mask<(1<<core);mask++){
      const a=new Map();
      for(let j=1;j<=core;j++)a.set(j,(mask>>(j-1))&1);
      for(const {signed,leaf,altLeaf} of triples){
        if(altLeaf!==null)a.set(altLeaf,0);
        const chosen=signed.find(l=>Math.abs(l)===leaf);
        const others=signed.filter(l=>Math.abs(l)!==leaf);
        const x=val(others[0],a),y=val(others[1],a);
        const want=(x===y)?1-x:0;
        a.set(leaf,want^(chosen<0?1:0));
      }
      ok(sat(F,a),"independent all-core signed NAE projection");
      ok(a.size===maxvar,"all variables explicitly assigned");
      controls++;
    }
  }
  // Minimal full eight-clause gadget is a real UNSAT source with NO private leaf.
  let F=[];for(let mask=0;mask<8;mask++)F.push([1,2,3].map((v,i)=>(mask&(1<<i))?-v:v));
  for(let a=0;a<8;a++){const vals=new Map([1,2,3].map((v,i)=>[v,(a>>i)&1]));ok(!sat(F,vals),"eight-clause UNSAT adversary")}
  return {id:"TMR3_LEAFNAE081_INDEPENDENT_PROJECTION",status:"COMPUTATIONAL all-core finite signed NAE controls",seed:"0xF15A2E07",assertions:checks,failures:broken,allCoreExtensionsChecked:controls,unsatControlAssignments:8,notes:"Independent generator and witness construction, not a physical TM compilation"};
}
console.log(JSON.stringify(projectionAudit081(),null,2));

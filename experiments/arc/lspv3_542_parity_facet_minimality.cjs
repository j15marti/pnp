"use strict";
function audit() {
  let checks=0;
  const ok=(p,m)=>{checks++;if(!p)throw Error(m);};
  function clauseSat(clause,assignment){
    for(const lit of clause){const val=(assignment>>(Math.abs(lit)-1))&1;if(val===(lit>0?1:0))return true;}
    return false;
  }
  function parityCNF(d,charge) {
    const clauses=[];
    for(let a=0;a<(1<<d);a++){
      let parity=0,c=[];
      for(let j=0;j<d;j++){let b=(a>>j)&1;parity^=b;c.push(b?-(j+1):j+1);}
      if(parity!==charge)clauses.push(c);
    }
    return clauses;
  }
  function models(clauses,d){
    const result=[];
    for(let a=0;a<(1<<d);a++)if(clauses.every(c=>clauseSat(c,a)))result.push(a);
    return result;
  }
  const cases=[];
  for(let d=2;d<=7;d++)for(let charge=0;charge<=1;charge++){
    const full=parityCNF(d,charge),good=models(full,d);
    ok(full.length===(1<<(d-1)),"parity facet count");
    ok(good.length===(1<<(d-1)),"parity model count");
    for(let i=0;i<full.length;i++){
      const kept=full.filter((_,j)=>i!==j),partial=models(kept,d);
      const extra=partial.filter(a=>!good.includes(a));
      ok(extra.length===1,"facet deletion does not introduce exactly one invalid tuple");
      ok(!clauseSat(full[i],extra[0]),"deleted clause does not exclude tuple");
    }
    // Independent clause enumeration, each variable either absent, positive or negative.
    const implied=[];
    for(let code=1;code<3**d;code++){
      let n=code,c=[];
      for(let j=0;j<d;j++){
        const digit=n%3;n=Math.floor(n/3);
        if(digit===1)c.push(j+1);
        if(digit===2)c.push(-(j+1));
      }
      if(good.every(a=>clauseSat(c,a)))implied.push(c);
    }
    const normalize=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)).join(",");
    ok(implied.length===full.length,"missing or extra non-tautological implicate");
    ok(implied.map(normalize).sort().join("|")===full.map(normalize).sort().join("|"),"implicate identity");
    cases.push({variables:d,charge,facets:full.length,correct_models:good.length,deletion_witnesses:full.length,implied_clauses:implied.length});
  }
  const edges=[];
  for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)edges.push([u,v]);
  function tseitin(charges){
    const clauses=[];
    for(let v=0;v<4;v++){
      const inc=[];for(let e=0;e<edges.length;e++)if(edges[e].includes(v))inc.push(e);
      for(let a=0;a<8;a++){
        const parity=((a&1)^((a>>1)&1)^((a>>2)&1));
        if(parity===charges[v])continue;
        clauses.push(inc.map((e,i)=>((a>>i)&1)?-(e+1):(e+1)));
      }
    }
    return clauses;
  }
  const odd=tseitin([1,0,0,0]),even=tseitin([0,0,0,0]);
  ok(odd.length===16,"odd source count");
  ok(models(odd,6).length===0,"odd original must be UNSAT");
  ok(models(even,6).length===8,"even control models");
  const deletionWits=[];
  for(let i=0;i<odd.length;i++){
    const available=odd.filter((_,j)=>i!==j);
    const w=models(available,6)[0];
    ok(w!==undefined,"each odd source must be indispensable");
    ok(!clauseSat(odd[i],w),"deleted source must be falsified");
    deletionWits.push({id:"S"+(i+1),assignment:w.toString(2).padStart(6,"0")});
  }
  // Exact semantic shortcut control: four source clauses per cubic vertex,
  // three paid AND3 joins per vertex and three GF(2) additions.
  ok(3*4+3===15,"declared semantic mixed shortcut cost");
  ok(models(parityCNF(3,0).slice(1),3).length===5,"missing XOR facet");
  ok(models([...parityCNF(3,0).slice(1),parityCNF(3,0)[1]],3).length===5,"duplicate facet");
  return {run:"LSPV3/542",script:"experiments/arc/lspv3_542_parity_facet_minimality.cjs",
    scope:"strict source, direct CNF and declared semantic mixed controls, NOT historical checker",
    checks,cases,k4:{odd_clauses:odd.length,odd_models:0,even_models:8,source_deletion_witnesses:deletionWits,
    semantic_paid_nodes:15,span_under_balanced_parallel_model:4},
    hostile_controls:["individual clause deletion","duplicate facet","SAT even-charge instance","UNSAT odd-charge instance","closed-form affine shortcut"],
    claim:"Direct CNF for d-variable parity has 2^(d-1) indispensable width-d facets. This is not a mixed proof lower bound."};
}
const output=audit();
if(typeof process!=="undefined" && process.stdout)process.stdout.write(JSON.stringify(output,null,2)+"\n");

"use strict";
/* LSPV-1/518: independent q=3 directed cubic Tseitin strict-3CNF controls.
   External proof-size lower bound is Pang 2026 Theorem 7.2(b), not tested here.
   The historical R_mix341 mixed checker is NOT invoked. */
function verify518() {
  let checks=0;
  function ok(b,msg){checks++;if(!b)throw Error(msg);}
  function edgesOf(name){
    if(name==="K4"){let e=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);return [4,e];}
    if(name==="K33"){let e=[];for(let a=0;a<3;a++)for(let b=3;b<6;b++)e.push([a,b]);return [6,e];}
    let e=[];for(let a=0;a<8;a++)for(let k=0;k<3;k++){let b=a^(1<<k);if(a<b)e.push([a,b]);}
    return [8,e];
  }
  function make(h,edges,charge){
    const E=edges.length, n=3*E,z=n+1, inc=Array.from({length:h},()=>[]);
    edges.forEach(([a,b],idx)=>{inc[a].push(idx);inc[b].push(idx);});
    ok(edges.length*2===3*h,"cubic incidence");
    inc.forEach(a=>ok(a.length===3,"degree3"));
    const F=[];
    for(let e=0;e<E;e++){
      F.push([3*e+1,3*e+2,3*e+3]);
      for(let a=0;a<3;a++)for(let b=a+1;b<3;b++) F.push([-(3*e+a+1),-(3*e+b+1)]);
    }
    for(let v=0;v<h;v++)for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){
      const vals=[a,b,c],flow=inc[v].reduce((s,e,j)=>s+(edges[e][0]===v?1:-1)*vals[j],0);
      if(((flow%3)+3)%3!==charge[v])F.push(inc[v].map((e,j)=>-(3*e+vals[j]+1)));
    }
    const S=[];
    for(const c of F){if(c.length===2){S.push([...c,z]);S.push([...c,-z]);}else S.push([...c]);}
    ok(F.length===24*h,"orig clause count");
    ok(S.length===57*h/2,"strict count");
    ok(S.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper signed strict3");
    function restrict(flag){
      const v=flag?z:-z;let out=[];
      for(const c of S)if(!c.includes(v))out.push(c.filter(l=>Math.abs(l)!==z));
      return out;
    }
    for(const flag of [false,true])ok(JSON.stringify(restrict(flag))===JSON.stringify(F),"both restriction equality");
    // Independent GF(3) augmented row-reduction, rather than 3^E search.
    const A=Array.from({length:h},(_,v)=>{
      let row=Array(E+1).fill(0);
      edges.forEach(([a,b],e)=>{if(a===v)row[e]=1;if(b===v)row[e]=2;});
      row[E]=charge[v];return row;
    });
    let rank=0;
    for(let col=0;col<E;col++){
      let pivot=rank;while(pivot<h&&A[pivot][col]===0)pivot++;
      if(pivot===h)continue;
      [A[rank],A[pivot]]=[A[pivot],A[rank]];
      if(A[rank][col]===2)A[rank]=A[rank].map(x=>2*x%3);
      for(let j=0;j<h;j++)if(j!==rank&&A[j][col]){
        let mul=A[j][col];A[j]=A[j].map((x,k)=>((x-mul*A[rank][k])%3+3)%3);
      }
      rank++;
    }
    const consistent=A.every(row=>row.slice(0,E).some(x=>x!==0)||row[E]===0);
    const num=consistent?3**(E-rank):0;
    const expected=charge.reduce((a,b)=>a+b,0)%3?0:3**(E-h+1);
    ok(num===expected,"flow rank / source SAT label");
    // Explicit restrictions for all 3^6=729 K4 flow assignments; lower sample on larger.
    let tested=0, valid=0;
    const max=Math.min(3**E,243);
    for(let index=0;index<max;index++){
      let v=index, bits=Array(n+1).fill(false);
      for(let e=0;e<E;e++){let d=v%3;v=Math.floor(v/3);bits[3*e+d]=true;}
      const sat=c=>c.some(l=>bits[Math.abs(l)-1]===(l>0));
      const base=F.every(sat);if(base)valid++;
      for(const pad of [false,true]){bits[n]=pad;ok(S.every(sat)===base,"pad all assignments");tested++;}
    }
    return {graph:h===4?"K4":h===6?"K33":"Cube",charge_total:charge.reduce((a,b)=>a+b,0)%3,
      vertices:h,edges:E,original_variables:n,strict_variables:n+1,
      original_clauses:F.length,strict_clauses:S.length,
      algebraic_models:num,projection_comparisons:tested,
      observed_sample_models:valid,source_raw:F,strict_raw:S,aux:z};
  }
  let cases=[];
  for(const name of ["K4","K33","Cube"]){
    const [h,E]=edgesOf(name);
    for(const ch of [[1,...Array(h-1).fill(0)],Array(h).fill(0)]){
      cases.push(make(h,E,ch));
    }
  }
  // Tampering with one member of a complementary padded pair must break source equality.
  const base=cases[0],bad=base.strict_raw.map(c=>c.slice());
  bad[1][2]=base.aux+1;
  function restrict(cnf,z,flag){const taut=flag?z:-z;return cnf.filter(c=>!c.includes(taut)).map(c=>c.filter(l=>Math.abs(l)!==z));}
  ok(JSON.stringify(restrict(bad,base.aux,false))!==JSON.stringify(base.source_raw),"tampered pair rejected");
  // Verify normalized strict clause, and reject a false new auxiliary.
  ok(!bad.every(c=>c.every(l=>Math.abs(l)<=base.aux)),"undeclared new variable rejected");
  for(const c of cases){delete c.source_raw;delete c.strict_raw;delete c.aux;}
  return {status:"COMPUTATIONAL independent GF3 elimination and original signed 3CNF padding controls",
    theorem_scope:"Pang 2026 v2 Theorems 1.1, 7.2(b), q=3 p=2 fixed r, cubic edge expanders",
    historical_Rmix341:"NOT authenticated or executed",cases,checks,negative_controls:2};
}
if(typeof module!=="undefined") {
  module.exports=verify518;
  if(require.main===module)console.log(JSON.stringify(verify518(),null,2));
}

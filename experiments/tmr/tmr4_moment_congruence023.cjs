'use strict';
function audit23(){
  "use strict";
  const ok=(v,m)=>{if(!v)throw Error(m)};
  const cube=s=>[0,1,2].map(v=>[v,(s>>v)&1]);
  const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const moment=(clauses,maxdegree=3)=>{
    const M=new Map();
    for(const c of clauses)for(let mask=1;mask<8;mask++){
      if((mask.toString(2).match(/1/g)||[]).length>maxdegree)continue;
      let S=[],sgn=1;for(let k=0;k<3;k++)if(mask>>k&1){S.push(c[k][0]);if(c[k][1])sgn=-sgn}
      S.sort((a,b)=>a-b);let key=S.join(",");
      M.set(key,(M.get(key)||0)+sgn);
    }
    return Array.from(M).filter(([k,v])=>v!==0).sort((a,b)=>a[0].localeCompare(b[0]));
  };
  const viol=(F,a)=>F.reduce((v,c)=>v+(c.every(([id,bit])=>((a>>id)&1)===bit)?1:0),0);
  const reconstruct=(F,a,M)=>F.length+M.reduce((v,[k,coeff])=>{
    let sign=1;for(const id of k.split(","))if((a>>Number(id))&1)sign=-sign;
    return v+sign*coeff;
  },0);
  const U=Array.from({length:8},(_,s)=>cube(s));
  const V=Array.from({length:8},(_,s)=>s).filter(s=>s.toString(2).split("1").length%2===1).flatMap(s=>[cube(s),cube(s)]);
  ok(U.length===8&&V.length===8,"sizes");
  ok(equal(moment(U,2),moment(V,2))&&equal(moment(U,2),[]),"lower moments");
  ok(equal(moment(U,3),[])&&equal(moment(V,3),[["0,1,2",8]]),"cubic separator");
  ok(U.every(c=>c.length===3)&&V.every(c=>c.length===3),"proper");
  ok(Array.from({length:8},(_,a)=>viol(U,a)).every(v=>v===1),"UNSAT fixed");
  ok(Array.from({length:8},(_,a)=>viol(V,a)).filter(v=>v===0).length===4,"SAT parity");
  let state=20261114>>>0;
  function random(){state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;}
  const cases=[["U",3,U],["V",3,V],["Horn",4,[[[0,0],[1,1],[2,1]],[[1,0],[2,1],[3,1]]]],["XOR",3,[0,3,5,6].map(cube)],["padding",3,Array(14).fill(null).map(()=>cube(0))],["2SATlift",4,[[[0,0],[1,0],[3,0]],[[0,0],[1,0],[3,1]]]],["product",6,[cube(0),cube(7),cube(0).map(([i,b])=>[i+3,b]),cube(7).map(([i,b])=>[i+3,b])]]];
  for(let n=3;n<=7;n++)for(let z=0;z<100;z++){
    let F=[],m=Math.floor(random()*17);
    for(let j=0;j<m;j++){
      let ids=Array.from({length:n},(_,i)=>i);
      for(let i=n-1;i>0;i--){let k=Math.floor(random()*(i+1)),v=ids[i];ids[i]=ids[k];ids[k]=v;}
      F.push(ids.slice(0,3).sort((a,b)=>a-b).map(v=>[v,Math.floor(random()*2)]));
    }cases.push(["random"+n+"."+z,n,F]);
  }
  let checks=0,concat_checks=0,contributions=0,sat=0,unsat=0,maxkeys=0;
  for(const [label,n,F] of cases){
    const M=moment(F); maxkeys=Math.max(maxkeys,M.length);contributions+=7*F.length;
    let accepts=false;
    for(let a=0;a<(1<<n);a++){ok(reconstruct(F,a,M)===8*viol(F,a),"spectral "+label);checks++;if(viol(F,a)===0)accepts=true;}
    if(accepts)sat++;else unsat++;
    if(F.length>1){
      const R=F.slice().reverse();
      ok(equal(moment(F),moment(R)),"permute "+label);
      const tail=[cube(0).map(([v,b])=>[v,b]),cube(7).map(([v,b])=>[v,b])];
      ok(equal(moment(F.concat(tail)),moment(R.concat(tail))),"congruence "+label);
      for(let a=0;a<(1<<n);a++){ok(viol(F.concat(tail),a)===viol(R.concat(tail),a),"cont "+label);concat_checks++;}
    }
  }
  return {run:"TMR4-MOMENT23",execution:"hosted V8 (function source published below)",status:"COMPUTATIONAL",seed:20261114,formulas:cases.length,labels:{SAT:sat,UNSAT:unsat},walsh_equalities:checks,permuted_suffix_equalities:concat_checks,macro_signed_contributions:contributions,maximum_sparse_nonzero_keys:maxkeys,controls:["UNSAT complete 8 signatures","SAT duplicated even-parity 4 signatures","Horn","XOR","padding","2-SAT auxiliary lifting","disjoint product","seeded random 3-7 variables"],counterexample:{m:8,degree2_equal:true,degree3_UNSAT:[],degree3_SAT:[["0,1,2",8]],UNSAT_models:0,SAT_models:4},failed_assertions:0,restriction:"symbolic clause macro-steps, not arbitrary physical TM simulation"};
}
const result=audit23();
if(typeof console!=='undefined')console.log(JSON.stringify(result,null,2));

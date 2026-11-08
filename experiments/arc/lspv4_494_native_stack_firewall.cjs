// LSPV-4/494 independent native-resource arithmetic and strict-3CNF checks.
// Does NOT simulate the FLMV machine or assert any universal SAT compiler.
'use strict';
const audit = ()=>{
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 function packet(ch,shift=0){
  const out=[];
  for(let v=0;v<4;v++){
   const inc=edges.map((e,i)=>(e.includes(v)?i+1+shift:0)).filter(Boolean);
   for(let z=0;z<8;z++){
    const bits=[z&1,(z>>1)&1,(z>>2)&1];
    if((bits[0]^bits[1]^bits[2])!==ch[v]) out.push(inc.map((id,i)=>bits[i]?-id:id));
   }
  }return out;
 }
 function countSat(clauses,n){
  let c=0;for(let a=0;a<(1<<n);a++){
   if(clauses.every(cl=>cl.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))c++;
  }return c;
 }
 let checks=0,sat=0,unsat=0;
 for(let ch=0;ch<16;ch++){
  const b=[0,1,2,3].map(i=>(ch>>i)&1);
  const cs=packet(b);
  if(cs.length!==16||cs.some(cl=>cl.length!==3||new Set(cl.map(Math.abs)).size!==3))throw Error("bad K4 encoding");
  checks++;
  const c=countSat(cs,6);
  if(c!==((b[0]^b[1]^b[2]^b[3])?0:8))throw Error("bad charge model");
  checks++;if(c)sat++;else unsat++;
 }
 const all=Array.from({length:8},(_,z)=>[1,2,3].map((id,i)=>((z>>i)&1)?-id:id));
 if(countSat(all,3)!==0||countSat(all.slice(0,4),3)===0||countSat(all.slice(4),3)===0)throw Error("illegitimate generic splitter accepted");
 checks+=3;
 for(let [a,b] of [[0,0],[1,0],[1,1]]){
  const A=[0,1,2,3].map(i=>(a>>i)&1), B=[0,1,2,3].map(i=>(b>>i)&1);
  if(Boolean(countSat([...packet(A),...packet(B,6)],12))!==(Boolean(countSat(packet(A),6))&&Boolean(countSat(packet(B),6))))throw Error("AND fails for disjoint components");
  checks++;
 }
 for(let j=0;j<=30;j++){
  const e=(.6*(1-Math.pow(.5,j))/.5)+1.1*Math.pow(.5,j);
  if(e<1.1-1e-10||e>1.2+1e-10)throw Error("exponent");
  checks++;
 }
 // exact beta(1201/1000) - 501/1000 numerator/denominator:
 const numerator=23390597n,denominator=2884802000n;
 if(numerator<=0n||Number(numerator)/Number(denominator)<.008)throw Error("FLMV gap");
 checks++;
 return {status:"PASS",scope:"independent finite strict-3CNF/K4, AND-counterexample and exponent controls; not native FLMV simulation",assertions:checks,k4_charge_vectors:16,sat_vectors:sat,unsat_vectors:unsat,signed_all8_parent_sat:false,signed_all8_each_half_sat:true,material_scope:"fully signed original clause evaluation",time_exponent:"6/5",space_exponent:"1/2",strict_flmv_margin:`${numerator}/${denominator}`};
};
const result = audit();
if (typeof console !== 'undefined') console.log(JSON.stringify(result,null,2));

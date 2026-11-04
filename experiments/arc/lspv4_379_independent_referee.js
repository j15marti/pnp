"use strict";
function verify(){
 let cases=0,forced=0,assertions=0;
 function lit(r,v){let id=r>>1,neg=r&1;return v[id]^neg;}
 function nmodels(G,out,force){const C=[[1]];for(let i=0;i<3;i++){const [a,b]=G[i],z=i+2,A=(a&1)?-((a>>1)+1):((a>>1)+1),B=(b&1)?-((b>>1)+1):((b>>1)+1);C.push([-z,A],[-z,B],[z,-A,-B]);}let unit=(out&1)?-((out>>1)+1):((out>>1)+1);C.push([force?unit:-unit]);let count=0;for(let m=0;m<16;m++){let yes=true;for(let cl of C){if(!cl.some(v=>{let b=(m>>(Math.abs(v)-1))&1;return v>0?b===1:b===0;})){yes=false;break;}}if(yes)count++}return count;}
 for(let a1=0;a1<2;a1++)for(let b1=0;b1<2;b1++)
 for(let a2=0;a2<4;a2++)for(let b2=0;b2<4;b2++)
 for(let a3=0;a3<6;a3++)for(let b3=0;b3<6;b3++){
  const G=[[a1,b1],[a2,b2],[a3,b3]],v=[1];for(const [a,b] of G)v.push(lit(a,v)&lit(b,v));
  for(let out=0;out<8;out++){const expected=lit(out,v);for(let force=0;force<=1;force++){let n=nmodels(G,out,force);if(n!==(expected===force?1:0))throw Error("independent CNF mismatch");forced++;assertions++}cases++;}
 }
 return{cases,forced,assertions,forced_SAT:forced/2,forced_UNSAT:forced/2,model:"all ordered signed AND2 three-gate DAGs on input t with output any signed reference; distinct complete CNF-model enumerator"};
}
if (require.main===module) console.log(JSON.stringify(verify(),null,2));
module.exports=verify;

'use strict';
/* LSPV-1/515 independent rank-one nonlinear gate facet macro audit.
 * This is NOT a R_mix341 or Res(PC1/F2) syntax checker.
 * Bit-order: truth-table entry g(a,b) is bit (2*a+b).
 */
const assert=require('node:assert/strict');
const out={status:'PASS',scope:'rank-one nonlinear gate projected facet tautology macros only',nMax:5,cases:0,facets:0,trueFacet:0,complementPair:0,errorsRejected:0};
function bit(x){let p=0;for(;x;x>>=1)p^=x&1;return p;}
function evalA(f,x){return bit(f[0]&x)^f[1];}
function g(tag,a,b){if(!Number.isInteger(tag)||tag<0||tag>15)throw Error('tag');return(tag>>(2*a+b))&1;}
function aff(tag){return (g(tag,0,0)^g(tag,0,1)^g(tag,1,0)^g(tag,1,1))===0;}
function rank1(u,v){return u[0]===0||v[0]===0||u[0]===v[0];}
function result(tag,u,v,n){let c=g(tag,evalA(u,0),evalA(v,0)),m=0;for(let i=0;i<n;i++)if(g(tag,evalA(u,1<<i),evalA(v,1<<i))!==c)m|=1<<i;return[m,c];}
function checkFacet(tag,u,v,z,a,b){
 const T=u[0]||v[0];
 assert((u[0]===0||u[0]===T)&&(v[0]===0||v[0]===T)&&(z[0]===0||z[0]===T));
 const literals=[[u,a,false],[v,b,false],[z,g(tag,a,b),true]];
 const truth=literals.map(([f,k,eq])=>[0,1].map(t=>{let val=(f[0]===0?f[1]:t^f[1]);return eq?val===k:val!==k;}));
 for(let t=0;t<2;t++)assert(truth.some(v=>v[t]));
 if(truth.some(v=>v[0]&&v[1])){out.trueFacet++;return;}
 assert(truth.some(v=>v[0]&&!v[1]));assert(truth.some(v=>!v[0]&&v[1]));
 out.complementPair++;
}
for(let n=1;n<=out.nMax;n++){
 for(let um=0;um<(1<<n);um++)for(let uc=0;uc<2;uc++)for(let vm=0;vm<(1<<n);vm++)for(let vc=0;vc<2;vc++){
  const u=[um,uc],v=[vm,vc];if(!rank1(u,v))continue;
  for(let tag=0;tag<16;tag++){if(aff(tag))continue;const z=result(tag,u,v,n);
   for(let x=0;x<(1<<n);x++)assert.equal(evalA(z,x),g(tag,evalA(u,x),evalA(v,x)));
   out.cases++;
   for(let a=0;a<2;a++)for(let b=0;b<2;b++){checkFacet(tag,u,v,z,a,b);out.facets++;}
  }
 }
}
for(const bad of [-1,16,NaN,'3',null]){try{g(bad,0,0);assert.fail('malformed accepted');}catch(e){if(e.message==='malformed accepted')throw e;out.errorsRejected++;}}
assert.equal(out.facets,out.trueFacet+out.complementPair);
console.log(JSON.stringify(out));

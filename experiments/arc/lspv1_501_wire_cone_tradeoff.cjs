'use strict';
/* LSPV-1/501: finite controls of a DIFFERENT cone-typed calculus.
   Not the historical R_mix341 checker, not a replay of Pang's theorem. */
const assert=require('node:assert/strict');
let tests=0, rejects=0;
function check(x){tests++;assert.ok(x)}
function reject(fn){let failed=false;try{fn()}catch(e){failed=true}check(failed);rejects++}
class Circuit {
 constructor(n){this.n=n;this.def=new Map()}
 define(id,op,p){if(this.def.has(id)||/^x[0-9]+$/.test(id)||!['AND','OR','XOR','NOT'].includes(op)||p.length!==(op==='NOT'?1:2))throw Error('bad gate');
   for(const x of p)if(!this.has(x))throw Error('unknown ancestor');
   this.def.set(id,{op,p})}
 has(x){return /^x[0-9]+$/.test(x)?Number(x.slice(1))<this.n:this.def.has(x)}
 cone(x){if(/^x[0-9]+$/.test(x)){if(!this.has(x))throw Error('bad x');return new Set([Number(x.slice(1))])}
   const g=this.def.get(x);if(!g)throw Error('bad gate');
   return new Set(g.p.flatMap(a=>[...this.cone(a)]))}
 value(x,mask){if(/^x[0-9]+$/.test(x))return (mask>>Number(x.slice(1)))&1;
   const g=this.def.get(x);if(!g)throw Error('bad wire');
   const v=g.p.map(a=>this.value(a,mask));
   return g.op==='AND'?(v[0]&v[1]):g.op==='OR'?(v[0]|v[1]):g.op==='XOR'?(v[0]^v[1]):1-v[0]}
}
const C=new Circuit(7);
C.define('z1','OR',['x0','x1']);
C.define('z2','AND',['z1','x2']);
C.define('z3','XOR',['z2','x3']);
C.define('z4','AND',['z1','z3']);
function pred(p,a){if(p[0]==='R')return C.value(p[1],a);
 if(p[0]==='N')return 1-pred(p[1],a);
 if(p[0]==='O')return p[1].some(q=>pred(q,a))?1:0;
 if(p[0]==='F')return 0;
 throw Error('bad term')}
const R=x=>['R',x],N=x=>['N',x],O=(...p)=>['O',p],F=['F'];
function support(p){if(p[0]==='R')return C.cone(p[1]);if(p[0]==='N')return support(p[1]);if(p[0]==='F')return new Set();
 return new Set(p[1].flatMap(q=>[...support(q)]))}
function macro(parents,out){
 if(parents.length<1||parents.length>2)throw Error('wrong arity');
 const U=[...new Set([...parents,out].flatMap(x=>[...support(x)]))].sort((a,b)=>a-b);
 const J=[...support(out)].sort((a,b)=>a-b);
 let witnesses=0,resolutions=0,output=0;
 for(let a=0;a<(1<<U.length);a++){
   const v=U.reduce((s,i,j)=>s|(((a>>j)&1)<<i),0);
   if(pred(out,v))continue;
   if(!parents.some(p=>!pred(p,v)))throw Error('false entailment');
   witnesses++;tests++}
 for(let a=0;a<(1<<J.length);a++){
   const v=J.reduce((s,i,j)=>s|(((a>>j)&1)<<i),0);
   if(pred(out,v))continue;
   output++;resolutions+=(1<<(U.length-J.length))-1}
 return {scope:U.length,outputClauses:output,witnesses,resolutions}
}
const m1=macro([O(R('x0'),R('x1'))],R('z1'));
const m2=macro([R('z1'),R('x2')],R('z2'));
const m3=macro([R('z2'),R('x3')],N(R('z3')));
const m4=macro([N(R('z3'))],N(R('z4')));
const m5=macro([R('x5'),N(R('x5'))],F);
check(m1.scope===2&&m2.scope===3&&m5.outputClauses===1);
reject(()=>macro([R('z1')],R('z2')));
reject(()=>macro([R('z2')],R('z3')));
reject(()=>C.define('bad','AND',['unknown','x0']));
reject(()=>C.define('z1','AND',['x0','x1']));
const trees=[];
for(const n of [4,8,16,32]){const tree=new Circuit(n);let ids=Array.from({length:n},(_,i)=>'x'+i);let d=0;
 while(ids.length>1){const out=[];for(let j=0;j<ids.length;j+=2){const id='g'+d+'_'+(j/2);tree.define(id,'AND',[ids[j],ids[j+1]]);out.push(id)}ids=out;d++}
 check(tree.cone(ids[0]).size===n);check(tree.def.size===n-1);
 trees.push({n,fanIn:2,depth:d,outputOriginalCone:n})}
const result={label:'LSPV-1/501',tests,rejectedHostile:rejects,macros:[m1,m2,m3,m4,m5],trees,historicalChecker:false,pangAsymptoticReplayed:false};
console.log(JSON.stringify(result,null,2));

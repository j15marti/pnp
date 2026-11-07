// LSPV-3/484. Compact independent symbolic binary-gate affine-stratification witness.
// Separate circuit control, NOT historical R_mix341 accepted bytes.
'use strict';
function bit(op,u,v){return(op>>(2*u+v))&1}
function xor(a,b){return [a[0]^b[0],a[1]^b[1]]}
function nonaffine(op){return(bit(op,0,0)^bit(op,0,1)^bit(op,1,0)^bit(op,1,1))===1}
function tree(n,gates){
 let leaves=[];
 function rec(i,out,guard,path){
  if(i===gates.length){leaves.push({guard,out,path});return}
  const g=gates[i];if(!Number.isInteger(g.op)||g.op<0||g.op>15)throw Error('bad op');
  function get(t){if(t[0]==='x'){if(t[1]<0||t[1]>=n)throw Error('bad x');return [1<<t[1],0]}if(t[0]==='g'&&t[1]>=0&&t[1]<i)return out[t[1]];throw Error('bad gate reference')}
  const u=get(g.u),v=get(g.v),f00=bit(g.op,0,0),f10=bit(g.op,1,0),f01=bit(g.op,0,1);
  if(!nonaffine(g.op)){
   let z=[0,f00];if(f00^f10)z=xor(z,u);if(f00^f01)z=xor(z,v);
   return rec(i+1,[...out,z],guard,path);
  }
  for(let b=0;b<=1;b++){
   const z0=bit(g.op,b,0),z1=bit(g.op,b,1);
   let z=[0,z0];if(z0^z1)z=xor(z,v);
   rec(i+1,[...out,z],[...guard,[u[0],u[1]^b]],path+b);
  }
 }
 rec(0,[],[]," ".trim());return leaves;
}
function parity(m){let p=0;while(m){p^=m&1;m>>=1}return p}
function affine(a,x){return parity(a[0]&x)^a[1]}
function check(n,gates,leaves,samples){
 let tests=0;
 for(let x of samples){
  const actual=[];
  for(let g of gates){const val=t=>t[0]==='x'?(x>>t[1])&1:actual[t[1]];actual.push(bit(g.op,val(g.u),val(g.v)))}
  const hits=leaves.filter(l=>l.guard.every(([mask,rhs])=>parity(mask&x)===rhs));
  if(hits.length!==1)throw Error('non-partition');tests++;
  for(let i=0;i<gates.length;i++){if(affine(hits[0].out[i],x)!==actual[i])throw Error('non-affine leaf');tests++;}
 }
 return tests;
}
let results=[];
for(let op=0;op<16;op++){
 const gates=[{op,u:['x',0],v:['x',1]}],L=tree(2,gates);
 const nL=nonaffine(op)?2:1;if(L.length!==nL)throw Error('leaf budget');
 results.push({op,leaves:L.length,checks:check(2,gates,L,[0,1,2,3])});
}
let g=[{op:6,u:['x',0],v:['x',1]}];
for(let j=2;j<20;j++)g.push({op:6,u:['g',j-2],v:['x',j]});
g.push({op:8,u:['x',0],v:['g',18]});
g.push({op:8,u:['g',19],v:['x',19]});
let L=tree(20,g);if(L.length!==4)throw Error('wide budget');
let samples=[0,(1<<20)-1,...Array.from({length:20},(_,i)=>1<<i)];
let wide=check(20,g,L,samples);
let invalid=0;
for(let bad of [[{op:16,u:['x',0],v:['x',1]}],[{op:8,u:['g',0],v:['x',1]}],[{op:8,u:['g',3],v:['x',0]}]]){
 try{tree(2,bad)}catch(e){invalid++}
}
if(invalid!==3)throw Error('bad certificate accepted');
let out={status:'PASS compact separate-circuit check',ops:results.length,checks:results.reduce((s,x)=>s+x.checks,0)+wide,wide_original_variables:20,wide_formal_leaves:4,negative_rejections:invalid};
if(require.main===module)console.log(JSON.stringify(out,null,2));module.exports={tree,check,out};

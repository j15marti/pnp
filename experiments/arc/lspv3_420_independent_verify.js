'use strict';
// LSPV-3/420: separately implemented typed semantic verifier. NOT the missing /341 byte parser.
const assert=require('node:assert/strict');
let C={gate:0,clause:0,res:0,row:0,xor:0,local:0,negative:0};
const V=(s,i)=>(s>>i)&1;
const T=(g,a,b)=>(g>>(2*a+b))&1;
const E=(cl,s)=>cl.some(l=>V(s,Math.abs(l)-1)===(l>0?1:0));
const SL=(l,d)=>V(d,Math.abs(l)-1)?-l:l;
const SC=(cl,d)=>cl.map(x=>SL(x,d));
const P=(m,r,s)=>((m&s).toString(2).replace(/0/g,'').length%2)===r;
const R=(m,r,d)=>r^((m&d).toString(2).replace(/0/g,'').length%2);
const Res=(a,b,p)=>{
 if(!a.includes(p)||!b.includes(-p))return null;
 const x=[...new Set([...a.filter(t=>t!==p),...b.filter(t=>t!==-p)])];
 return x.some(l=>x.includes(-l))?null:x.sort((a,b)=>a-b);
};
for(let f=15;f>=0;f--)for(let g=15;g>=0;g--)for(let dz=1;dz>=0;dz--)for(let dw=1;dw>=0;dw--){
 for(let s=0;s<4;s++){
  const x=V(s,0),y=V(s,1),z=T(f,x,y),w=T(g,z,x);
  const zp=T(f,x,y)^dz,wp=T(g,zp^dz,x)^dw;
  assert.equal(zp,z^dz);assert.equal(wp,w^dw);C.gate+=2;
 }
}
const A=[[1],[-1],[3],[-3],[4],[-4],[-3,1],[3,-2],[-4,3],[4,-3],[-3,4],[-4,-3],[1,2,-3],[-2,4]];
for(let d of [0,4,8,12]){
 for(let cl of A)for(let s=0;s<16;s++){assert.equal(E(cl,s),E(SC(cl,d),s^d));C.clause++}
 for(let a of A)for(let b of A)for(let p of [1,3,4,-1,-3,-4]){
  const c=Res(a,b,p);if(c===null)continue;
  assert.deepEqual(Res(SC(a,d),SC(b,d),SL(p,d)),SC(c,d).sort((x,y)=>x-y));C.res++;
 }
 for(let m=0;m<16;m++)for(let r=0;r<2;r++){
  for(let s=0;s<16;s++){assert.equal(P(m,r,s),P(m,R(m,r,d),s^d));C.row++}
  for(let n=0;n<16;n++)for(let v=0;v<2;v++){
   assert.equal(R(m,r,d)^R(n,v,d),R(m^n,r^v,d));C.xor++;
  }
 }
}
for(let a=0;a<16;a++)for(let b=0;b<16;b++){
 let imp=true;for(let i=0;i<4;i++)if(((a>>i)&1)&&!((b>>i)&1))imp=false;
 assert.equal(imp,(a&~b&15)===0);C.local++;
}
assert.equal(R(4,1,4),0);C.negative++;
assert.equal(Res([3],[-3],1),null);C.negative++;
assert.equal((1&~2&15)!==0,true);C.negative++;
assert.equal(new Set([3,3]).size,1);C.negative++;
assert.equal(new Set(['source_0','def_1','local_2']).has('local_2/internal_0'),false);C.negative++;
console.log(JSON.stringify({id:'LSPV3_420_INDEPENDENT_JS',checks:C,total:Object.values(C).reduce((a,b)=>a+b,0)},null,2));

'use strict';
// Independent finite bit-exact virtual input check; NOT native FLMV execution.
const assert=require('node:assert/strict');
const g=n=>{let b=n.toString(2);return '0'.repeat(b.length-1)+b};
const u=(n,r)=>n.toString(2).padStart(r,'0');
const rec=(c,r)=>u(c.length,r)+c.map(x=>(x<0?'1':'0')+u(Math.abs(x),r)).join('');
const source=(bs,r)=>g(r)+g(bs.length)+bs.map(b=>g(b.length+1)+b.map(c=>rec(c,r)).join('')).join('');
const guest=(cs,r)=>g(r)+g(cs.length+1)+cs.map(c=>rec(c,r)).join('');
const gam=(s,p)=>{let z=0;while(s[p+z]==='0')z++; if(p+2*z+1>s.length) throw Error('trunc');return [parseInt(s.slice(p+z,p+2*z+1),2),p+2*z+1]};
function parse(s){let [r,p]=gam(s,0),[h,p2]=gam(s,p);p=p2;let spans=[],bs=[];for(let i=0;i<h;i++){let [m,p3]=gam(s,p);p=p3;m--;let start=p,cs=[];for(let j=0;j<m;j++){if(p+r>s.length)throw Error('trunc');let ar=parseInt(s.slice(p,p+r),2);p+=r;let clause=[];for(let k=0;k<ar;k++){if(p+r+1>s.length)throw Error('trunc');let x=parseInt(s.slice(p+1,p+r+1),2)*(s[p]==='1'?-1:1);p+=r+1;if(x===0)throw Error('zero');clause.push(x)}if(ar!==3||new Set(clause.map(Math.abs)).size!==3)throw Error('source grammar');cs.push(clause)}spans.push([start,p]);bs.push(cs)}if(p!==s.length)throw Error('trailing');return {r,spans,bs}}
function parity(a,b,c,p){let cs=[];for(let mask=0;mask<8;mask++){let z=[(mask&1)>0,(mask&2)>0,(mask&4)>0];if((z.filter(Boolean).length%2)!==p)cs.push([a,b,c].map((v,i)=>z[i]?-v:v))}return cs}
function sat(cs){const vs=[...new Set(cs.flat().map(Math.abs))];for(let z=0;z<(1<<vs.length);z++){let v=new Map(vs.map((x,i)=>[x,(z>>i)&1]));if(cs.every(c=>c.some(x=>v.get(Math.abs(x))===(x>0?1:0))))return true}return false}
let trials=0,queries=0,semantics=0,corrupt=0;
let seed=460;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed&1};
for(let t=0;t<24;t++){
 const ch=[rand(),rand(),rand()],bs=[parity(1,2,3,ch[0]),parity(4,5,6,ch[1]),parity(3,6,7,ch[2])];
 if(t%4===0)bs[2].push(...parity(3,6,7,ch[2]^1));
 const s=source(bs,8),p=parse(s);assert.deepEqual(p.bs,bs);
 for(let mask=0;mask<16;mask++){
  let okL=[0,1].filter(v=>mask&(1<<v)),okR=[0,1].filter(v=>mask&(1<<(2+v)));
  let aux=[0,1].filter(v=>!okL.includes(v)).map(v=>[v===0?3:-3]).concat([0,1].filter(v=>!okR.includes(v)).map(v=>[v===0?6:-6]));
  if(mask&1)aux.push([7]);
  const [a,b]=p.spans[2],hdr=g(8)+g(bs[2].length+aux.length+1),auxbits=aux.map(c=>rec(c,8)).join('');
  const mat=guest(bs[2].concat(aux),8);
  assert.equal(mat,hdr+s.slice(a,b)+auxbits);
  function vb(i){if(i<0||i>=mat.length)return ' ';if(i<hdr.length)return hdr[i];i-=hdr.length;if(i<b-a)return s[a+i];return auxbits[i-(b-a)]}
  for(let i=-2;i<mat.length+3;i++){assert.equal(vb(i),i>=0&&i<mat.length?mat[i]:' ');queries++}
  let expect=false;
  for(let q=0;q<128;q++){let x3=(q>>2)&1,x6=(q>>5)&1,x7=(q>>6)&1;
   if(!okL.includes(x3)||!okR.includes(x6)||((mask&1)&&!x7))continue;
   if(bs[2].every(c=>c.some(l=>(((q>>(Math.abs(l)-1))&1)===(l>0?1:0)))))expect=true;
  }
  assert.equal(sat(bs[2].concat(aux)),expect);semantics++;trials++;
  if(mask===0){const pos=a+9,edit=s.slice(0,pos)+(s[pos]==='1'?'0':'1')+s.slice(pos+1);assert.notEqual(edit[pos],vb(hdr.length+pos-a));corrupt++}
 }
 for(let v of [s.slice(0,-1),s+'1']){assert.throws(()=>parse(v));corrupt++}
}
console.log(JSON.stringify({status:'PASS',seed:460,trials,virtual_bit_checks:queries,semantic_checks:semantics,corruption_checks:corrupt,scope:'finite independent JS, not FLMV same-machine execution'}));

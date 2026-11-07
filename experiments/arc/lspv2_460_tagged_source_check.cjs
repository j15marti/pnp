// LSPV-2/460 small standalone tagged-ID parser regression.
// Detailed independently executed Python and Node DPLL replayers in REPRO.zip.
// Node >= 18. Runs locally: node lspv2_460_tagged_source_check.cjs
'use strict';
const assert=require('node:assert/strict');
const bit=(x,k)=>x.toString(2).padStart(k,'0');
const mkid=(t,v,i,k,V)=>((t*V+v)*2**k)+i;
function parse(s){
 if(typeof s!=='string'||/[^01]/.test(s))throw Error('nonbinary');
 const N=s.length,K=Math.floor(Math.log2(N+1))+1;
 let p=0;function rd(n){if(p+n>N)throw Error('truncated');const x=parseInt(s.slice(p,p+n),2);p+=n;return x;}
 if(rd(16)!==0xa531)throw Error('magic');
 const d=rd(K),w=rd(K),h=2**d-1;
 if(d<2||h>N||w>Math.max(1,Math.ceil(Math.log2(N)/10)))throw Error('header');
 const V=2**(Math.floor(Math.log2(h))+1),os=[];
 for(let v=1;v<=h;v++){
  os.push(p);const n=rd(K);if(n<1||n>N)throw Error('block count');
  for(let j=0;j<n;j++){
   let ids=[];
   for(let u=0;u<3;u++){rd(1);const x=rd(2*K+2),a=Math.floor(x/2**K),tag=Math.floor(a/V),owner=a%V,index=x%2**K;
    if(index===0)throw Error('zero index');
    if(tag===0){if(owner!==v)throw Error('private alias');}
    else if(tag===1){if(owner<2||owner>h||index>w||(v!==owner&&v!==Math.floor(owner/2)))throw Error('edge alias');}
    else throw Error('bad tag');
    ids.push(x);}
   if(new Set(ids).size!==3)throw Error('duplicate in clause');
  }
  if(p-os[os.length-1]>4*(Math.floor(Math.sqrt(N))+1)*K)throw Error('large block');
 }
 if(p!==N)throw Error('trailing');
 return {h,K,w,offsets:os};
}
function source(bad){
 const d=2,h=3,w=1,V=4;let K=10,data='';
 for(let n=0;n<7;n++){
  data=bit(0xa531,16)+bit(d,K)+bit(w,K);
  for(let v=1;v<=h;v++){
   const vars=(v===1?[mkid(1,2,1,K,V),mkid(1,3,1,K,V),mkid(0,1,1,K,V)]:[mkid(1,v,1,K,V),mkid(0,v,1,K,V),mkid(0,v,2,K,V)]);
   if(bad&&v===3)vars[1]=mkid(0,1,1,K,V);
   data+=bit(1,K);
   for(const x of vars)data+='0'+bit(x,2*K+2);
  }
  const nk=Math.floor(Math.log2(data.length+1))+1;
  if(nk===K)break;K=nk;
 }return data;
}
assert.equal(parse(source(false)).h,3);
assert.throws(()=>parse(source(true)),/alias/);
const good=source(false);
assert.throws(()=>parse(good+'0'),/trailing/);
assert.throws(()=>parse(good.slice(0,-1)),/truncated/);
assert.throws(()=>parse((good[0]==='1'?'0':'1')+good.slice(1)),/magic/);
console.log(JSON.stringify({status:'PASS',strict_tree:3,controls:5}));

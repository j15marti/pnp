// LSPV-4/440: independent compact source-only original strict 3-CNF check.
// Node.js host-language tests. This is not an FLMV machine execution.
import assert from 'node:assert/strict';
let checks=0; const eq=(a,b)=>{assert.deepEqual(a,b);checks++};
const B='10100101', W=h=>Math.floor(Math.log2(h*h))+1;
function matching(h){return Array.from({length:h},(_,v)=>(v+h/2)%h)}
function encode(h,c){
 const m=matching(h),w=W(h); let s=B+'1'.repeat(h)+'0'+'1'.repeat(w)+'0';
 for(let v=0;v<h;v++){
  let x=m[v],u=Math.min(v,x),z=Math.max(v,x);
  const ids=[(v-1+h)%h+1,v+1,h+1+u*h+z];
  for(let p=0;p<2;p++)for(let r=0;r<2;r++){
   let signs=[p,r,1^p^r^c[v]];
   for(let j=0;j<3;j++)s+=ids[j].toString(2).padStart(w,'0')+signs[j];
  }
 }return s+'01';
}
function recognize(s){
 let i=0,h=0,w=0;
 if(s.slice(0,8)!==B)return 'OUTSIDE';
 i=8;while(i<s.length&&s[i]==='1'){h++;i++}
 if(s[i++]!=='0')return 'MALFORMED';
 while(i<s.length&&s[i]==='1'){w++;i++}
 if(s[i++]!=='0')return 'MALFORMED';
 if(h<6||h%2||w!==W(h))return 'OUTSIDE';
 const at=i,L=12*(w+1);
 if(s.length!==at+h*L+2||s.slice(-2)!=='01')return 'MALFORMED';
 const integer=(j)=>parseInt(s.slice(j,j+w),2);
 let parity=0;
 for(let v=0;v<h;v++){
   const pos=at+v*L;let third=null,chi=null;
   for(let t=0;t<4;t++){
     let p=Math.floor(t/2),r=t%2,j=pos+t*3*(w+1);
     let a=integer(j),b=integer(j+w+1),c=integer(j+2*(w+1));
     let pa=Number(s[j+w]),pb=Number(s[j+2*w+1]),pc=Number(s[j+3*(w+1)-1]);
     if(a!==(v-1+h)%h+1||b!==v+1||pa!==p||pb!==r)return 'OUTSIDE';
     if(third===null)third=c;
     if(third!==c)return 'OUTSIDE';
     if(chi===null)chi=pc^1;
     if(pc!==(p^r^1^chi))return 'OUTSIDE';
   }
   let delta=third-h-1,u=Math.floor(delta/h),z=delta%h;
   if(!(u>=0&&u<z&&z<h&&(v===u||v===z)))return 'OUTSIDE';
   let other=v===u?z:u;
   if((other-v+h)%h===1||(other-v+h)%h===h-1)return 'OUTSIDE';
   if(integer(at+other*L+2*(w+1))!==third)return 'OUTSIDE';
   parity^=chi;
 }
 return parity?'UNSAT':'SAT';
}
for(const h of [6,8,10,12,24,64,128]){
 for(let j=0;j<3;j++){
  const charges=Array.from({length:h},(_,v)=>Number((v*31+j*7+h)%5===0));
  if(j===1)charges[0]^=1;
  if(j===2)charges[h-1]^=1;
  const s=encode(h,charges), w=W(h), start=8+h+1+w+1;
  eq(s.length,12*h*(w+1)+h+w+12);
  eq(recognize(s),charges.reduce((x,y)=>x^y,0)?'UNSAT':'SAT');
  for(const pos of [0,start,start+w,s.length-1]){
   const b=s.slice(0,pos)+(s[pos]==='0'?'1':'0')+s.slice(pos+1);
   eq(['OUTSIDE','MALFORMED'].includes(recognize(b)),true);
  }
  if(h<=12)for(let v=0;v<h;v++)for(let lit=0;lit<12;lit++){
    let pos=start+v*12*(w+1)+lit*(w+1)+w;
    const b=s.slice(0,pos)+(s[pos]==='0'?'1':'0')+s.slice(pos+1);
    eq(recognize(b),'OUTSIDE');
  }
 }
}
console.log(JSON.stringify({compact_assertions:checks,success:true,scope:'host finite validation'}));

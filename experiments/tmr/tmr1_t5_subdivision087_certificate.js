'use strict';
/* TMR-1/087 published certificate: finite computational checks, not a proof. */
const assert=require('node:assert/strict');
const R=(x,y)=>[1,3].includes((y-x+5)%5);
let tests=0;
function check(ok){tests++;assert.ok(ok);}
function count(k,mask,s,t){let v=Array(5).fill(0);v[s]=1;
  for(let i=0;i<k;i++){const next=Array(5).fill(0);for(let a=0;a<5;a++)for(let b=0;b<5;b++)if(((mask>>i)&1)?R(a,b):R(b,a))next[b]+=v[a];v=next;}
  return v[t];}
for(let k=1;k<=6;k++)for(let mask=0;mask<2**k;mask++){
  for(let s=0;s<5;s++)for(let t=0;t<5;t++){
    const v=count(k,mask,s,t);
    check(v===count(k,mask,0,(t-s+5)%5));
    if(k>=4)check(v>0);
    if(k>=3&&s===t)check(v>0);
  }
  if(k===3){let p=0;for(let i=0;i<3;i++)p+=(mask>>i)&1;check(count(k,mask,0,0)===(p===0||p===3?3:1));}
}
for(let s=0;s<5;s++)check(count(2,3,s,s)===0);
let surviving=0;
for(let z=0;z<5**6;z++){
  let a=z,colors=[];for(let i=0;i<6;i++){colors.push(a%5);a=Math.floor(a/5);}
  let ok=true;for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)if(count(2,3,colors[i],colors[j])===0)ok=false;
  if(ok)surviving++;
}
check(surviving===0);
console.log(JSON.stringify({theorem:'TMR-1/087',status:'COMPUTATIONAL_ONLY',tested_path_lengths:[1,2,3,4,5,6],tested_orientation_patterns:126,K6_two_edge_branch_assignments:15625,K6_survivors:surviving,assertions:tests,failures:0}));

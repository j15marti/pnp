'use strict';
// Standalone no-dependency three-original-input Shannon LOCAL payload verifier.
let checks=0;
function ck(v){if(!v)throw Error('assertion '+checks);checks++;}
function calc(c,a){
 const v=[...a];
 for(const [i,j,op] of c.gates){
   if(!Number.isInteger(i)||!Number.isInteger(j)||!Number.isInteger(op)||i<0||j<0||i>=v.length||j>=v.length||op<0||op>15)throw Error('malformed gate');
   v.push((op>>(2*v[i]+v[j]))&1);
 }
 if(c.out<0||c.out>=v.length)throw Error('malformed output');
 return v[c.out];
}
function roots(c){return Array.from({length:8},(_,j)=>calc(c,[(j>>2)&1,(j>>1)&1,j&1]));}
function synth(t){
 if(t.length!==8||t.some(v=>v!==0&&v!==1))throw Error('invalid table');
 const op=(start)=>t.slice(start,start+4).reduce((n,v,i)=>n|(v<<i),0);
 return {gates:[[1,2,op(0)],[1,2,op(4)],[3,4,6],[0,5,8],[3,6,6]],out:7};
}
for(let mask=0;mask<256;mask++){
 let t=Array.from({length:8},(_,j)=>(mask>>j)&1);
 ck(JSON.stringify(roots(synth(t)))===JSON.stringify(t));
 ck(synth(t).gates.length===5);
}
const equation=(a,rhs)=>Array.from({length:8},(_,j)=>Number((((a[0]&((j>>2)&1))^(a[1]&((j>>1)&1))^(a[2]&(j&1))))===rhs));
ck(equation([1,0,0],1).join('')==='00001111');
ck(equation([0,0,0],0).every(x=>x===1));
ck(!equation([0,0,0],1).some(x=>x));
let models=[];for(let j=0;j<8;j++){let x=(j>>2)&1,y=(j>>1)&1,z=j&1;if(x&&!y&&(x||z))models.push(j);}
ck(models.length===2);
const q=Array.from({length:8},(_,j)=>Number(((j>>2)&1)||!((j>>1)&1)));
const other=Array.from({length:8},(_,j)=>Number(!((j>>1)&1)));
ck(models.every(j=>q[j]===other[j])&&q.some((v,j)=>v!==other[j]));
for(const bad of [{gates:[[8,0,6]],out:3},{gates:[[0,1,16]],out:3},{gates:[],out:4}]){let rejected=false;try{roots(bad)}catch(e){rejected=true;}ck(rejected);}
console.log(JSON.stringify({pass:true,checks,functions:256,model_only_negative:true,gf2_type_guard:true}));
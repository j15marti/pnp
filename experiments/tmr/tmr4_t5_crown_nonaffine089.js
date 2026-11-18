'use strict';
/* Independent zero-dependency count/CNF audit, TMR4/089. Run: node experiments/tmr/tmr4_t5_crown_nonaffine089.js */
const assert=require('assert');
function edges(k,flipped=false){let E=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++)if(i!==j)E.push(flipped&&i<4&&j===(i+1)%4?[k+j,i]:[i,k+j]);return E;}
function sat(w,E){return E.every(([u,v])=>[1,3].includes((w[v]-w[u]+5)%5));}
function clauses(k,E){let C=[],ban=(q,b)=>q.map((a,i)=>b[i]?-(a+1):a+1);for(let u=0;u<2*k;u++)for(let d=5;d<8;d++)C.push(ban([3*u,3*u+1,3*u+2],[d&1,d>>1&1,d>>2&1]));for(let [u,v] of E)for(let a=0;a<5;a++)for(let b=0;b<5;b++)if(![1,3].includes((b-a+5)%5))C.push(ban([3*u,3*u+1,3*u+2,3*v,3*v+1,3*v+2],[a&1,a>>1&1,a>>2&1,b&1,b>>1&1,b>>2&1]));return C;}
function csat(w,C){let bits=w.flatMap(x=>[x&1,x>>1&1,x>>2&1]);return C.every(c=>c.some(l=> l>0?bits[l-1]===1:bits[-l-1]===0));}
function decode(z,n){let w=[];for(let i=0;i<n;i++){w.push(z%5);z=Math.floor(z/5);}return w;}
function projected(k,flipped=false){let Z=0,num=5**k;for(let z=0;z<num;z++){let u=decode(z,k),count=1;for(let j=0;j<k;j++){let choices=0;for(let v=0;v<5;v++){let valid=true;for(let i=0;i<k;i++)if(i!==j){const d=flipped&&i<4&&j===(i+1)%4?(u[i]-v+5)%5:(v-u[i]+5)%5;if(d!==1&&d!==3){valid=false;break;}}choices+=valid;}count*=choices;}Z+=count;}return Z;}
let checks=0,exhaust=0,invalid=0;
for(let k=4;k<=7;k++){assert.strictEqual(projected(k),10*2**k+10*k-10);checks+=5**k;}
assert.strictEqual(projected(4,true),0);
for(let flipped of [false,true]){let E=edges(4,flipped),C=clauses(4,E);assert.strictEqual(C.length,3*8+15*12);let Z=0;for(let z=0;z<5**8;z++){let w=decode(z,8),ok=sat(w,E);assert.strictEqual(csat(w,C),ok);Z+=ok;exhaust++;}assert.strictEqual(Z,flipped?0:190);}
let C=clauses(4,edges(4));for(let z=0;z<300;z++){let w=Array.from({length:8},(_,i)=>(i*z+7)%5);w[z%8]=5+z%3;assert(!csat(w,C));invalid++;}
process.stdout.write(JSON.stringify({Uvaluations:checks,original_source_CNF_checks:exhaust,invalid_checks:invalid,unexpected_failures:0})+'\n');
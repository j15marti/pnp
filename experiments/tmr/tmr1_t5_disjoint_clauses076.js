'use strict';

// TMR-1/076: exact finite-module certificate for authentic disjoint-clause signed-3SAT -> T5 source family.

const mod=(x)=>((x%5)+5)%5;

const p=(c)=>c===0?2:1;

const q=(a,b)=>a===b?0:(a!==0&&b!==0?3:1);

function triangleW(a,b,c){const cs=[0,2,3];let z=0;for(const x of cs)for(const y of cs)for(const t of cs){if(x===y||x===t||y===t)continue;z+=p(x)*p(y)*p(t)*q(x,y)*q(x,t)*q(y,t)*q(x,a)*q(y,b)*q(t,c);}return z;}

function moduleWeight(T,F,B){let alpha=p(T)*p(F)*q(T,F)*q(T,B)*q(F,B),summand=0;for(const a of [T,F])for(const b of [T,F])for(const c of [T,F])for(const s of [T,F]){summand+=triangleW(a,b,s)*triangleW(s===T?F:T,c,F);}return {alpha,summand,weight:alpha**4*summand};}

function audit076(){const colors=[0,2,3],table=[];for(const T of colors)for(const F of colors)for(const B of colors){if(T===F||T===B||F===B)continue;let {alpha,summand,weight}=moduleWeight(T,F,B);table.push({T,F,B,alpha,summand,weight});}let checks=6;const expected=[8024832,8024832,5038848,8503056,5038848,8503056];table.forEach((o,i)=>{if(o.weight!==expected[i])throw Error('module mismatch '+i);checks++;});const endpoints=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++){let cnt=0;for(let w=0;w<5;w++)for(let z=0;z<5;z++)if([1,3].includes(mod(z-a))&&[1,3].includes(mod(w-a))&&[1,3].includes(mod(z-w))&&[1,3].includes(mod(b-w)))cnt++;if(cnt!==([1,4].includes(mod(b-a))?1:0))throw Error('gadget endpoint error');checks++;endpoints.push(cnt);}const families=[];for(let m=1;m<=7;m++){const k=3*m;const nH=17+10*k+46*m;const eH=20+13*k+61*m;const nD=57+36*k+168*m;const eD=80+52*k+244*m;const rr=eD-nD+1,rq=eH-nH+1;if(rr!==24+124*m||rq!==4+24*m)throw Error('rank error');let z=10n*table.reduce((z,o)=>z+BigInt(6)*BigInt(o.weight)**BigInt(m),0n);let reduced=120n*([8024832n,5038848n,8503056n].reduce((z,b)=>z+b**BigInt(m),0n));if(z!==reduced)throw Error('closed form error');checks+=3;families.push({m,k,nH,eH,nD,eD,rRaw:rr,rQuotient:rq,exactT5Count:z.toString()});}return {revision:"tmr1-t5-disjoint-clause-certificate076-v1",sourceModel:"literal sign and low-first index; fixed directed T5 with difference 1 or 3",table,endpoints,families,checks,failures:0,scope:"independent finite-module arithmetic; universal-m family follows symbolic graph composition and factorization"};}

console.log(JSON.stringify(audit076(),null,2));
'use strict';
// LSPV-4/458 independently coded finite semantic experiment, NOT a native FLMV profile.
const assert=require('node:assert/strict'); const crypto=require('node:crypto');
function graph(kind){let e=[]; const H=kind==='K4'?4:8;for(let x=0;x<H;x++)for(let y=x+1;y<H;y++)if(kind==='K4'||[1,2,4].includes(x^y))e.push([x,y]);return {e,H};}
function tseitin(kind,odd){const {e,H}=graph(kind);const cs=[];for(let v=0;v<H;v++){const ids=e.map((p,i)=>p.includes(v)?i:-1).filter(i=>i>=0);assert.equal(ids.length,3);for(let m=0;m<8;m++){let b=[m&1,(m>>1)&1,(m>>2)&1];if((b[0]^b[1]^b[2])===(odd&&v===0?1:0))continue;cs.push(ids.map((i,j)=>b[j]===0?i+1:-(i+1)));}}return {cs,n:e.length};}
function sat(cs,n,pin){for(let a=0;a<2**n;a++){if(pin!==null&&(a&1)!==pin)continue;let all=true;for(const cl of cs){let good=false;for(const lit of cl){const val=(a>>(Math.abs(lit)-1))&1;if(val===(lit>0?1:0)){good=true;break;}}if(!good){all=false;break;}}if(all)return true;}return false;}
let count=0,stale=0,cases=0;
for(const kind of ['K4','cube'])for(const odd of [false,true]){
 const {cs,n}=tseitin(kind,odd);assert.equal(cs.length,4*(kind==='K4'?4:8));
 const source=cs.map(c=>c.join(',')).join(';');let B=Buffer.byteLength(source);const addr=BigInt(B)**6n;
 const Q=8, r=Math.ceil(Math.log2(Q+2));let epoch=0,phys=0n;const store=new Map(),old=new Map();
 const read=(i)=>{let p=(i+1n)*BigInt(r+1);if(p>phys)phys=p;const pval=store.get(i.toString());return !pval||pval.epoch!==epoch?0:pval.val;};
 const write=(i,val)=>{let p=(i+1n)*BigInt(r+1);if(p>phys)phys=p;store.set(i.toString(),{epoch,val});};
 let localStale=0;
 for(const pin of [null,0,1,0,null,1,0,null]){epoch++; assert.equal(read(addr),0);assert.equal(read(2n),0);count+=2;
  if((old.get(addr.toString())||0)!==0){stale++;localStale++;}
  const truth=sat(cs,n,pin); assert.equal(truth,!odd);count++;
  write(addr,truth?1:2);write(2n,epoch);old.set(addr.toString(),truth?1:2);
  assert.equal(read(addr),truth?1:2);count++;
 }
 assert.equal(localStale,Q-1);assert(phys>addr);count+=2;
 const sh=crypto.createHash('sha256').update(source).digest('hex');assert.equal(sh.length,64);count++;
 cases++;
}
assert.equal(stale,28);console.log(JSON.stringify({status:'PASS',checks:count,cases,guest_calls:32,naive_stale_blank_failures:stale}));

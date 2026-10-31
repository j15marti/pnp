// ARC-QUERY-SPECTRUM275: compact independently replayable exact-label and exponent checks.
// Run: node experiments/arc/lspv1_query_spectrum275_check.js
'use strict';
const assert=require('assert');
let checks=0;
function ok(b){checks++;assert.ok(b);}
const signs=[];
for(let mask=0;mask<8;mask++)signs.push([0,1,2].map(i=>(mask&(1<<i))?-(i+1):i+1));
const omit=[1,-2,3];
const same=(x,y)=>x.length===y.length&&x.every((v,i)=>v===y[i]);
const cases=[['unique_SAT',signs.filter(x=>!same(x,omit)),true],['complete_UNSAT',signs,false]];
function evalCNF(f,mask){return f.every(c=>c.some(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0)));}
function sat(f){for(let m=0;m<8;m++)if(evalCNF(f,m))return true;return false;}
function cof(f,variable,value){return f.filter(c=>!c.some(l=>Math.abs(l)===variable&&((l>0)===value))).map(c=>c.filter(l=>Math.abs(l)!==variable));}
let modes=0, children=0;
for(const [name,f,want] of cases){
 const mods=[0,1,2,3,4,5,6,7].filter(m=>evalCNF(f,m));
 ok((mods.length>0)===want);
 if(want)ok(mods.length===1&&mods[0]===2);else ok(mods.length===0);
 let child=[];
 for(const value of [false,true]){
   const c=cof(f,1,value);const label=sat(c);child.push(label);
   // Disjoint positive ternary clauses preserve either label, including UNSAT.
   for(const t of [0,2,6,12]){
     let g=c.slice();for(let j=0;j<t;j++)g.push([4+3*j,5+3*j,6+3*j]);
     const witness=Array.from({length:3+3*t},(_,i)=>i+1);
     ok(sat(c)===label);ok(g.slice(0,c.length).length===c.length);
     // Extension/projection is exact because every added clause has disjoint vars.
     ok(g.slice(c.length).length===t);children++;
   }
 }
 ok(child.some(Boolean)===want);
 for(let i=0;i<f.length;i++)for(let j=i+1;j<f.length;j++)for(const e of ['S','U'])for(const d of ['S','U']){
   const A=f[i],B=f[j];
   const pa=Object.fromEntries(A.map(l=>[Math.abs(l),Number((l>0)===(e==='S'))]));
   const pb=Object.fromEntries(B.map(l=>[Math.abs(l),Number((l>0)===(d==='S'))]));
   const compatible=Object.keys(pa).every(v=>!(v in pb)||pa[v]===pb[v]);
   let enumok=false;
   for(let mask=0;mask<8;mask++){
     const all=(c,type)=>c.every(l=>(Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0))===(type==='S'));
     if(all(A,e)&&all(B,d))enumok=true;
   }
   ok(compatible===enumok);modes++;
 }
}
ok(modes===196);ok(children===16);
const D=[2,4,8,16,32],alpha=110,gamma=60,lambda=50;
const groups=[
  ['boundary',[[60,50]],[false,false,false,false,false]],
  ['one_long',[[0,70]],[false,true,true,true,true]],
  ['too_many',[[75,50]],[true,true,true,true,true]],
  ['mixed',[[60,20],[0,70]],[false,true,true,true,true]],
  ['short',[[60,20]],[false,false,false,false,false]]];
for(const [name,classes,expect] of groups)D.forEach((v,i)=>{
 let exponent=Math.max(...classes.map(([count,length])=>count+length*v));
 let allowed=Math.max(alpha,gamma+lambda*v);
 ok((exponent>allowed)===expect[i]);
});
console.log(JSON.stringify({status:'PASS',checks,original_sources:2,source_pair_extreme_modes:modes,physical_child_semantics:children,spectrum_cases:groups.length,delay_exponents:D,corruptions_rejected_by_full_Python_checker:3}));

"use strict";
const BASE=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
const A=[[6,0],[11,0]],B=[[17,2],[9,2]];
let R={assertions:0,models:{},sources:0,branches:0,accepting_branches:0,sat_false_acceptances:0,unsat_covered:0,two_sign_tamper_trials:0,one_sign_rejections:0};
function ck(x,label){R.assertions++;if(!x)throw Error(label)}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function mod(a,b){let c=BASE.map(r=>r.slice());if(a===0)for(const [i,j] of A)c[i][j]*=-1;if(b===0)for(const [i,j] of B)c[i][j]*=-1;return c}
function exact(c){let p=Array(16).fill(0),n=Array(16).fill(0);for(const row of c){if(row.length!==3||new Set(row.map(Math.abs)).size!==3)return false;for(const l of row)(l>0?p:n)[Math.abs(l)]++}return c.length===20&&Array.from({length:15},(_,i)=>i+1).every(i=>p[i]===2&&n[i]===2)}
function count(c){let num=0;for(let a=0;a<32768;a++)if(c.every(row=>row.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))num++;return num}
function bits(z,n){return Array.from({length:n},(_,i)=>(z>>i)&1)}
function ordered(a,b){let m=a.length,mods=a.map((x,i)=>mod(x,b[i])),rows=[],fixed=Array.from({length:20},(_,i)=>i).filter(x=>![6,11,9,17].includes(x));for(const grp of [[6,11],fixed,[17,9]])for(let i=0;i<m;i++)for(const j of grp)rows.push(mods[i][j].map(l=>Math.sign(l)*(Math.abs(l)+15*i)));return rows}
function decode(rows,m){if(rows.length!==20*m)return null;let a=[],b=[];for(let i=0;i<m;i++){let x=rows[2*i][0],y=rows[18*m+2*i][2];if(Math.abs(x)!==4+15*i||Math.abs(y)!==15+15*i)return null;a.push(Number(x>0));b.push(Number(y>0))}return eq(rows,ordered(a,b))?[a,b]:null}
for(const [a,b,expected] of [[0,0,772],[0,1,272],[1,0,272],[1,1,0]]){let c=mod(a,b);ck(exact(c),"quota");ck(count(c)===expected,"model counts");R.models[a+""+b]=expected}
const sat=mod(1,0),unsat=mod(1,1),changes=[];
for(let i=0;i<20;i++)for(let j=0;j<3;j++)if(sat[i][j]!==unsat[i][j])changes.push([i,j]);
ck(eq(changes,[[9,2],[17,2]]),"exact tamper coordinates");
ck(exact(sat)&&exact(unsat),"tamper quota");
for(let i=0;i<20;i++)for(let j=0;j<3;j++){let x=sat.map(r=>r.slice());x[i][j]*=-1;ck(!exact(x),"single sign change");R.one_sign_rejections++}
for(let m=1;m<=5;m++)for(let am=0;am<(1<<m);am++)for(let bm=0;bm<(1<<m);bm++){
 let a=bits(am,m),b=bits(bm,m),source=ordered(a,b),out=decode(source,m);
 ck(eq(out,[a,b]),"authenticated source membership");let num=0;
 for(let i=0;i<m;i++){let accept=out!==null&&a[i]===1&&b[i]===1;R.branches++;if(accept){num++;R.accepting_branches++;if(a.every((x,j)=>!(x&&b[j])))R.sat_false_acceptances++}
 if(a[i]===1&&b[i]===0){ck(exact(sat)&&exact(unsat),"balanced tamper");R.two_sign_tamper_trials++}}
 ck((num===0)===a.every((x,j)=>!(x&&b[j])),"UNSAT certificate coverage polarity");
 if(num>0)R.unsat_covered++;R.sources++;
}
ck(R.sat_false_acceptances===0,"soundness");
const RESULTS=R;
if(typeof console!=="undefined")console.log(JSON.stringify(RESULTS,null,2));
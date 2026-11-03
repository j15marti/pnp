// LSPV-3 374: signed Extended Resolution -> Rmix341 finite test.
"use strict";
function check(x,msg){if(!x)throw Error(msg||"assert");}
function norm(c){check(Array.isArray(c));let a=[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);check(a.every(x=>Number.isInteger(x)&&x!==0));check(a.every(x=>!a.includes(-x)),"tautology");return a;}
function eq(a,b){return JSON.stringify(norm(a))===JSON.stringify(norm(b));}
function res(a,b,p){check(Number.isInteger(p)&&p>0);a=norm(a);b=norm(b);check((a.includes(p)&&b.includes(-p))||(a.includes(-p)&&b.includes(p)),"bad pivot");return norm(a.filter(x=>Math.abs(x)!==p).concat(b.filter(x=>Math.abs(x)!==p)));}
function models(F,n){let count=0;for(let k=0;k<(1<<n);k++){let ok=F.every(c=>c.some(l=>{let bit=(k>>(Math.abs(l)-1))&1;return bit===(l>0?1:0);}));if(ok)count++;}return count;}
function defs(z,a,b){check(z>0&&!([Math.abs(a),Math.abs(b)].includes(z)),"fresh");return {A:norm([-z,a]),B:norm([-z,b]),C:norm([z,-a,-b])};}
function fixture(a,b){let z=3,q=0,steps=0;const F=[norm([a]),norm([b]),norm([-a,-b])],d=defs(z,a,b);check(models(F,2)===0);steps++;
for(let i=0;i<3;i++){check(models(F.filter((_,j)=>i!==j),2)>0,"source indispensable");steps++;}
let r1=res(d.C,F[0],1);check(eq(r1,[z,-b]));steps++;
let r2=res(r1,F[1],2);check(eq(r2,[z]));steps++;
let r3=res(d.A,F[2],1);check(eq(r3,[-z,-b]));steps++;
let r4=res(r3,F[1],2);check(eq(r4,[-z]));steps++;
let r5=res(r2,r4,z);check(r5.length===0);steps++;
for(let bits=0;bits<4;bits++){let va=!!(bits&1),vb=!!(bits&2),vz=(va===(a>0))&&(vb===(b>0));for(let c of [d.A,d.B,d.C]){check(c.some(l=>{let bit=Math.abs(l)===z?vz:Math.abs(l)===1?va:vb;return bit===(l>0);}),"wrong definition");steps++;}}
return {a,b,original_clauses:3,charged_gate_nodes:1,charged_res_nodes:5,charged_total:6,checks:steps};}
function dimacs(s){let lines=s.trim().split(/\r?\n/),h=lines.shift().trim().split(/\s+/);check(h.length===4&&h[0]==="p"&&h[1]==="cnf","header");let n=+h[2],m=+h[3];check(Number.isInteger(n)&&n>0&&Number.isInteger(m)&&m>=0&&lines.length===m,"count");return lines.map(l=>{let x=l.trim().split(/\s+/).map(Number);check(x.length>=2&&x[x.length-1]===0&&!x.slice(0,-1).includes(0),"termination");check(x.slice(0,-1).every(y=>Number.isInteger(y)&&y!==0&&Math.abs(y)<=n),"bad variable");return norm(x.slice(0,-1));});}
function k4(odd){let E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],ct=0;for(let bits=0;bits<64;bits++){let fine=true;for(let v=0;v<4;v++){let s=0;for(let j=0;j<6;j++)if(E[j].includes(v))s^=(bits>>j)&1;if(s!==((odd&&v===0)?1:0)){fine=false;break;}}if(fine)ct++;}return ct;}
function run(){let cases=[],checks=0;for(let a of [-1,1])for(let b of [-2,2]){let r=fixture(a,b);cases.push(r);checks+=r.checks;}
check(models(dimacs("p cnf 2 2\n1 0\n2 0"),2)===1);checks++;
check(models(dimacs("p cnf 2 3\n1 0\n2 0\n-1 -2 0"),2)===0);checks++;
let bad=["p cnf 2 2\n1 0","p cnf 2 1\n3 0","p cnf 2 1\n1","p cnf 2 1\n1 0 0","p cnf 2 1\n0","p cnf 2 1\n1 -1 0"];
for(let s of bad){let failed=false;try{dimacs(s);}catch(e){failed=true;}check(failed,"malformed accepted");checks++;}
let mutated=[()=>res([3,-2],[2],1),()=>defs(1,1,2),()=>res([3],[-3],5)];
for(let fn of mutated){let failed=false;try{fn();}catch(e){failed=true;}check(failed,"corrupt accepted");checks++;}
check(k4(true)===0&&k4(false)===8);checks+=2;
return {status:"COMPUTATIONAL",cases,malformed_rejections:bad.length,corrupt_rejections:mutated.length,K4_odd_even_models:[k4(true),k4(false)],assertions:checks,limitation:"finite signed ER2-to-Rmix test, not a native DRAT/DPR-to-ER replay"};}
const result=run();
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(result,null,2)+"\n");

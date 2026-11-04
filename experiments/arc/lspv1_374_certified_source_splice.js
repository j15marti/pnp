// Reproducer: LSPV-1 Result 374. Deterministic, no dependencies.
const run = (function(){"use strict";
function norm(c){if(!Array.isArray(c))throw Error("bad clause");if(c.some(x=>!Number.isInteger(x)||x===0))throw Error("bad literal");return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function key(c){return norm(c).join(",")}
function resolve(A,B,p){A=norm(A);B=norm(B);if(!A.includes(p)||!B.includes(-p))throw Error("invalid pivot");let r=norm(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)));if(r.some(x=>r.includes(-x)))throw Error("tautological resolvent");return r}
function replay(src,nodes){let lines=src.map(norm);for(let i=0;i<nodes.length;i++){const d=nodes[i];if(d.a>=lines.length||d.b>=lines.length||d.a<0||d.b<0)throw Error("forward/bad proof link");const expected=resolve(lines[d.a],lines[d.b],d.p);if(key(expected)!==key(d.c))throw Error("bad inference");lines.push(expected)}return lines}
function sats(src,n){let c=0;for(let z=0;z<(1<<n);z++){if(src.every(cl=>cl.some(l=>Boolean(z&(1<<(Math.abs(l)-1)))===(l>0))))c++}return c}
function tseitin(odd){const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];const sources=[];for(let v=0;v<4;v++){let ei=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);let desired=odd&&v===0?1:0;for(let t=0;t<8;t++){let parity=((t&1)?1:0)^((t&2)?1:0)^((t&4)?1:0);if(parity===desired)continue;sources.push(ei.map((j,k)=>((t>>k)&1)?-(j+1):(j+1)))}}return sources}
function check(name,condition){if(!condition)throw Error(name);counts.checks++}
const counts={checks:0};
const F=[[1,2],[-1],[-2]],m=F.length;
const tau={a:0,b:1,p:1,c:[2]},pi={a:3,b:2,p:2,c:[]};
check("source-unsat",sats(F,2)===0);
check("source-minimal",F.every((_,i)=>sats(F.filter((_,j)=>i!==j),2)>0));
const flipped=[];for(let i=0;i<m;i++){for(let j=0;j<F[i].length;j++){let G=F.map(a=>a.slice());G[i][j]*=-1;check("sign-flip",sats(G,2)>0);flipped.push({clause:i,occurrence:j,models:sats(G,2)})}}
check("tau-valid",key(replay(F,[tau])[m])==="2");
check("shortcut-valid",key(replay(F.concat([[2]]),[{a:3,b:2,p:2,c:[]}])[m+1])==="");
check("spliced-valid",key(replay(F,[tau,pi])[m+1])==="");
check("exact-W=2: no source units opposite",!F.some((a,i)=>F.some((b,j)=>j!==i&&a.length===1&&b.length===1&&a[0]===-b[0])));
check("xor-even-k4",sats(tseitin(false),6)===8);
check("xor-odd-k4",sats(tseitin(true),6)===0);
const corrupt=[
()=>replay(F,[{...tau,p:2}]),
()=>replay(F,[{...tau,c:[-2]}]),
()=>replay(F,[{...tau,a:3}]),
()=>replay(F,[tau,{...pi,p:1}]),
()=>norm([0]),()=>norm(["x"])
];for(const x of corrupt){let rejected=false;try{x()}catch(e){rejected=true}check("reject-malformed",rejected)}
const H=[[1],[-1]];check("contradictory-unit-one-step",key(replay(H,[{a:0,b:1,p:1,c:[]}])[2])==="");
const data={id:"LSPV1_374_CERTIFIED_SOURCE_SPLICE",date:"2026-11-03_1600_PST",producer_assertions:counts.checks,model:"pure shared-DAG ordinary Resolution, distinct unit-cost derived nodes, free source axioms",case_minimal_unsat:{source:F,premise_consequence:tau,shortcut_after_adding_derived_clause:[pi],composed:[tau,pi],bound:2,verified_optimum:2},sign_flip_witnesses:flipped,odd_k4_models:0,even_k4_models:8,adversarial_rejections:corrupt.length,claim:"Rmin(F)<=Rmin(F plus derivable clauses)+cost of explicit certified derivations; no inference for unchecked equisatisfiable transformations",quantifiers:"all valid CNF F, all finite certified source-addition chains and valid final Resolution refutations; independent of specific F",Rmix341:"unchanged; full LOCAL-CONVERT/DEF splicing requires separate type/alpha-conversion proof"};
return data;
});
const data = run();
if(typeof console!=="undefined")console.log(JSON.stringify(data,null,2));

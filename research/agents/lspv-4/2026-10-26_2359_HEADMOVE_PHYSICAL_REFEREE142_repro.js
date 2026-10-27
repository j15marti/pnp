#!/usr/bin/env node
'use strict';
// HEADMOVE-PHYSICAL-REFEREE142. Dependency-free literal-level source audit.
const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
 [5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
 [-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],
 [2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
let assertions=0; const ck=(x,msg)=>{assertions++;if(!x)throw Error(msg||'assertion')};
function module(a,b){let g=W.map(r=>r.slice());if(!a)for(let [i,j] of [[6,0],[11,0]])g[i][j]=-g[i][j];if(!b)for(let [i,j] of [[17,2],[9,2]])g[i][j]=-g[i][j];return g;}
const counts={};
for(let a=0;a<2;a++)for(let b=0;b<2;b++){
 const g=module(a,b),pos=Array(16).fill(0),neg=Array(16).fill(0);
 for(let row of g){ck(row.length===3&&new Set(row.map(Math.abs)).size===3);for(let l of row)(l>0?pos:neg)[Math.abs(l)]++;}
 for(let v=1;v<=15;v++)ck(pos[v]===2&&neg[v]===2);
 let n=0;for(let bits=0;bits<(1<<15);bits++){let good=true;for(let row of g){if(!row.some(l=>((bits>>(Math.abs(l)-1))&1)==(l>0?1:0))){good=false;break;}}if(good)n++;}
 counts[''+a+b]=n;ck((n===0)==Boolean(a&b));
}
ck(JSON.stringify(counts)===JSON.stringify({'00':772,'01':272,'10':272,'11':0}),'model counts');
function formula(m,a,b){const left=[],gap=[],right=[];for(let i=0;i<m;i++){let q=module((a>>i)&1,(b>>i)&1).map(row=>row.map(l=>Math.sign(l)*(Math.abs(l)+15*i)));q.forEach((r,j)=>(j===6||j===11?left:j===17||j===9?right:gap).push(r));}ck(left.length===2*m&&gap.length===16*m&&right.length===2*m);return left.concat(gap,right);}
function encode(m,q){const width=Math.ceil(Math.log2(15*m+1));let z='11100101'+(15*m).toString(2).padStart(32,'0')+(20*m).toString(2).padStart(32,'0');for(let row of q){for(let v of row)z+=(v<0?'1':'0')+Math.abs(v).toString(2).padStart(width,'0');z+='0';}return z;}
function parse(m,z){const width=Math.ceil(Math.log2(15*m+1)),w=3*(width+1)+1;ck(z.slice(0,8)==='11100101');ck(parseInt(z.slice(8,40),2)===15*m);ck(parseInt(z.slice(40,72),2)===20*m);ck(z.length===72+20*m*w);let p=72,r=[];for(let c=0;c<20*m;c++){let a=[];for(let j=0;j<3;j++){const sign=z[p++]==='1'?-1:1,v=parseInt(z.slice(p,p+width),2);p+=width;ck(v>=1&&v<=15*m);a.push(sign*v);}ck(z[p++]==='0');r.push(a);}return r;}
let encoded=0,quantifier=0,lengths={};
for(let m=1;m<=5;m++)for(let a=0;a<(1<<m);a++)for(let b=0;b<(1<<m);b++){
 const q=formula(m,a,b),z=encode(m,q),back=parse(m,z);
 ck(JSON.stringify(q)===JSON.stringify(back),'physical round trip');
 ck(new Set(q.map(r=>r.join(','))).size===20*m,'unique clauses');
 const plus=Array(15*m+1).fill(0),minus=plus.slice();
 for(let row of q){ck(new Set(row.map(Math.abs)).size===3);for(let v of row)(v>0?plus:minus)[Math.abs(v)]++;}
 for(let v=1;v<=15*m;v++)ck(plus[v]===2&&minus[v]===2);
 if(lengths[m]===undefined)lengths[m]=z.length;ck(lengths[m]===z.length,'fixed bit length');
 let witness=false;for(let j=0;j<m;j++)witness||=Boolean(((a>>j)&1)&&((b>>j)&1));
 ck(witness===Boolean(a&b),'coNTIME polarity');quantifier++;encoded++;
}
const out={run:'HEADMOVE-PHYSICAL-REFEREE142',assertions,failed:0,gadget_counts:counts,full_physical_serialization_cases:encoded,conondeterministic_quantifier_cases:quantifier,encoded_length_by_m:lengths,scope:'fixed-width proper signed 2P2N 3CNF source, W1 and m<=5; not unrestricted SAT lower bound'};
console.log(JSON.stringify(out,null,2));

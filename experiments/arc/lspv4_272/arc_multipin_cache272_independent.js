// LSPV4-272 independently implemented checker. Usage: node checker.js raw.json
"use strict"; const fs=typeof require==="function"?require("fs"):null;
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function A(x,m){if(!x)throw Error(m)}
function source(q,b){
 let C=[]; const force=(v,a,d)=>{for(let x of [-1,1])for(let y of [-1,1])C.push([v,x*a,y*d])};
 force(1,3,4);force(-2,5,6);
 for(let j=0;j<q;j++)C.push([b[j]?1:-1,-10-j,2]);
 if(q===3)C.push([10,11,12]);else {
 C.push([10,11,10+q]);for(let j=0;j<q-4;j++)C.push([-10-q-j,12+j,11+q+j]);
 C.push([-2*q-6,q+8,q+9]);}
 for(let j=0;j<Math.ceil(q**(5/3));j++)C.push([7,8,9]);
 return {n:q===3?12:2*q+6,C};
}
function child(q,b,j){let C=[];
 for(let [v,a,d] of [[1,4,5],[-2,6,7],[3,8,9]])for(let x of [-1,1])for(let y of [-1,1])C.push([v,x*a,y*d]);
 C.push([b[j]?1:-1,-3,2]);
 let p=Math.max(1,Math.ceil(Math.sqrt(Math.ceil(q**(5/3))/Math.log2(q+2))));
 for(let i=0;i<p;i++)C.push([10+3*i,11+3*i,12+3*i]);
 return {C,n:9+3*p};
}
function enc(o){const w=String(o.n).length+1;const s=l=>l<0?"-"+String(-l).padStart(w-1,"0"):"0"+String(l).padStart(w-1,"0");
 return "p cnf "+o.n+" "+o.C.length+"\n"+o.C.map(c=>c.map(s).join(" ")+" 0\n").join("");}
function satclause(c,mask){return c.some(l=>((mask>>>(Math.abs(l)-1))&1)===(l>0?1:0))}
function brute(o){for(let mask=0;mask<2**o.n;mask++)if(o.C.every(c=>satclause(c,mask)))return true;return false}
function histogram(o,assignment){let h=[0,0,0,0];for(let c of o.C)h[c.filter(l=>assignment[Math.abs(l)-1]===(l>0?1:0)).length]++;return h}
function pairs(c,d){
 const V=[...new Set([...c,...d].map(Math.abs))];let E={SS:false,SU:false,US:false,UU:false};
 for(let m=0;m<2**V.length;m++){const x={};V.forEach((v,i)=>x[v]=(m>>>i)&1);
 let t=c.filter(l=>x[Math.abs(l)]===(l>0?1:0)).length,u=d.filter(l=>x[Math.abs(l)]===(l>0?1:0)).length;
 if(t===3&&u===3)E.SS=true;if(t===3&&u===0)E.SU=true;if(t===0&&u===3)E.US=true;if(t===0&&u===0)E.UU=true;
 }return E;
}
function check(data){let stats={cases:0,bruteOriginalAssignments:0,sourceClauses:0,childLabels:0,pairs:0,flipSteps:0,proofSteps:0,extremeOccurrences:0};
 A(data.cases.length===15,"case count");
 for(let r of data.cases){
 stats.cases++;const q=r.q,b=r.pins.map(Boolean),S=source(q,b);
 A(enc(S).length*8===r.sourceBits&&enc(child(q,b,0)).length*8===r.childBits,"physical length");
 A(S.C.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper CNF");
 const expected=b.some(Boolean);
 A(expected===r.matchedLabel&&expected===r.baseline.sat,"source label");
  const good=(cl,w)=>w&&cl.every(c=>c.some(l=>w[Math.abs(l)-1]===(l>0?1:0)));
  A(expected?good(S.C,r.baseline.witness):r.baseline.witness===null,"original complete SAT witness / UNSAT nonwitness");
 if(q<=4){A(brute(S)===expected,"brute source");stats.bruteOriginalAssignments+=2**S.n;}
 // Independent existential check of first 9 child variables, with all private positive filler variables = 1.
 for(let j=0;j<q;j++){const D=child(q,b,j);stats.childLabels++; A(b[j]?good(D.C,r.childTotals.witnesses[j]):r.childTotals.witnesses[j]===null,"full child SAT witness / UNSAT nonwitness");
 if(q<=8){let found=false;for(let m=0;m<512;m++){let mask=m;for(let i=9;i<D.n;i++)mask|=(2**i);
 if(D.C.every(c=>c.some(l=> ((Math.floor(mask/2**(Math.abs(l)-1)))%2)===(l>0?1:0)))){found=true;break;}}
 A(found===b[j],"brute child core "+q+" "+j);}
 }
 let x=Array(S.n).fill(0),y=Array(S.n).fill(1);
 A(eq(histogram(S,x),r.zero.N)&&eq(histogram(S,y),r.one.N),"endpoint");
 for(let c of S.C){stats.sourceClauses++;A(c.filter(l=>x[Math.abs(l)-1]===(l>0?1:0)).length+c.filter(l=>y[Math.abs(l)-1]===(l>0?1:0)).length===3,"complement");}
 for(let f of r.flipTrail){x[f.flipped-1]^=1;A(eq(histogram(S,x),f.N),"flip histogram");stats.flipSteps++;}
 for(let o of r.diagnostics.occurrences){for(let [i,l] of S.C[o.index-1].entries()){
 let z=o.extremes[i];A(z.literal===l&&z.variable===Math.abs(l),"source occurrence");
 A(z.S===(l>0?1:0)&&z.U===(l>0?0:1)&&z.invertS===z.U&&z.invertU===z.S,"extreme inverse");stats.extremeOccurrences++;}}
 for(let p of r.diagnostics.pairs){A(eq(p.expected,pairs(S.C[p.j-1],S.C[p.k-1])),"pair");stats.pairs++;}
 if(r.mode==="allzero"&&q<=8){let cl=S.C.map(c=>c.slice());
 for(let step of r.proof.steps){let [a,b]=step.parents.map(i=>cl[i-1]);const v=step.pivot;
 A((a.includes(v)&&b.includes(-v))||(b.includes(v)&&a.includes(-v)),"proof pivot");
 let z=[...new Set([...a,...b].filter(l=>Math.abs(l)!==v))].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 A(eq(z,step.cl)&&!z.some(l=>z.includes(-l)),"proof resolvent");cl.push(z);stats.proofSteps++;
 }A(cl[r.proof.finalNode-1].length===0,"proof empty");}
 }return stats;
}
if(typeof module!=="undefined"&&module.exports)module.exports={check};
if(fs&&require.main===module){console.log(JSON.stringify(check(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));}

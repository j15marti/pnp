"use strict";
// LSPV2/395: neutral-section conservative gate-bank, source-preserving grid embedding.
function ok(p,s){if(!p)throw Error(s);}
function norm(c){ok(Array.isArray(c)&&c.every(v=>Number.isInteger(v)&&v!==0),"literal");let d=[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);ok(d.length>0&&!d.some(v=>d.includes(-v)),"tautology/empty");return d;}
function gate(a,b,z){return [[-z,a],[-z,b],[z,-a,-b]].map(norm);}
function make(F,k){ok(Number.isInteger(k)&&k>=2&&k<=20,"grid cutoff");let signatures=new Set();F=F.map(c=>{let d=norm(c);ok(!signatures.has(d.join(",")),"duplicate");signatures.add(d.join(","));return d;});ok(F.length>0,"no clauses");let n=Math.max(...F.flat().map(Math.abs)),next=n;
let u=Array.from({length:k*k},()=>++next),E=[],D=u.map(v=>[-v]);
for(let i=0;i<k;i++)for(let j=0;j<k;j++){let a=u[i*k+j];if(j+1<k)E.push([a,u[i*k+j+1]]);if(i+1<k)E.push([a,u[(i+1)*k+j]]);}
for(let [a,b]of E)D.push(...gate(a,b,++next));
D.push(...gate(Math.abs(F[0][0]),u[0],++next));
return {F,D,n,next,u,E,k,clauses:[...F,...D]};}
function models(F,n){let count=0;for(let a=0;a<(1<<n);a++)if(F.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))count++;return count;}
function bankCheck(B){let {D,n,u,E,k}=B;ok(D.length===k*k+3*(2*k*(k-1)+1),"bank length");ok(E.length===2*k*(k-1),"edge count");for(let C of D)ok(C.some(l=>l<0&&Math.abs(l)>n),"zero-section invalid");for(let v of u)ok(D.some(C=>C.length===1&&C[0]===-v),"nonunique extension");for(let [a,b]of E)ok(D.some(C=>C.length===3&&C.includes(-a)&&C.includes(-b)),"grid incidence");return true;}
function verify(F,steps){let lines=F.map(norm);for(let [ia,ib,p]of steps){let a=lines[ia],b=lines[ib];ok(a&&b&&a.includes(p)&&b.includes(-p),"invalid pivot");lines.push(normOrEmpty([...a.filter(v=>v!==p),...b.filter(v=>v!==-p)]));}ok(lines.at(-1).length===0,"no contradiction");return steps.length;}
function normOrEmpty(a){if(!a.length)return [];return norm(a);}
const blocker=[[1,2],[1,-2],[-1,2],[-1,-2]];
const odd=[[1,2],[-1,-2],[2,3],[-2,-3],[1,3],[-1,-3]];
const even=[[1,2],[-1,-2],[2,3],[-2,-3],[1,-3],[-1,3]];
function run(){let data=[],cases={blocker,odd,even,sat:[[1]]};for(let [name,F]of Object.entries(cases))for(let k of [2,3,4,5]){let B=make(F,k);bankCheck(B);data.push({name,k,sourceClauses:F.length,auxVariables:B.next-B.n,gateCount:B.E.length+1,addedClauses:B.D.length,totalClauses:B.clauses.length,gridMinorWidth:k,sourceModelCount:models(F,B.n),encodedASCIIBytes:("p cnf "+B.next+" "+B.clauses.length+"\n"+B.clauses.map(c=>c.join(" ")+" 0").join("\n")+"\n").length});}
let proofOdd=verify(odd,[[0,5,1],[6,3,2],[1,4,-1],[8,2,-2],[7,9,-3]]);
let proofBlock=verify(blocker,[[0,1,2],[2,3,2],[4,5,1]]);
let rejects=0;for(let F of [[[1,-1]],[[0]],[[1],[1]]])try{make(F,2);}catch(e){rejects++;}
for(let k of [0,-1,1,2.5])try{make(blocker,k)}catch(e){rejects++;}
ok(rejects===7,"invalid-input control");return {label:"LSPV2_395",proofOdd,proofBlock,checks:data.length,malformedRejected:rejects,cases:data};}
if(typeof module!=="undefined")module.exports={run,make,bankCheck,verify};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));

// LSPV-3/546 standalone independent certificate checker (not historical R_mix341)
"use strict";
let count=0;const chk=(x,s)=>{count++;if(!x)throw Error(s)};
function tseitin(v,odd){
let E=[],k=v/2;
if(v===4){for(let i=0;i<v;i++)for(let j=i+1;j<v;j++)E.push([i,j]);}
else {let S=new Map();for(let i=0;i<k;i++)for(let [a,b] of [[i,(i+1)%k],[k+i,k+(i+1)%k],[i,k+i]]){let pair=[a,b].sort((x,y)=>x-y);S.set(pair.join(":"),pair);}E=[...S.values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);}
let F=[];for(let i=0;i<v;i++){let vars=E.flatMap((e,j)=>e.includes(i)?[j+1]:[]);for(let mask=0;mask<8;mask++){let p=(mask&1?1:0)+(mask&2?1:0)+(mask&4?1:0);if(p%2===(odd&&i===0?1:0))continue;F.push(vars.map((x,j)=>mask>>j&1?-x:x));}}
return {F,n:E.length};}
function models(F,n){let s=0;for(let a=0;a<2**n;a++)if(F.every(C=>C.some(l=>(((a>>(Math.abs(l)-1))&1)===1)===(l>0))))s++;return s;}
function proof(F,n){let nodes=[];function rec(ctx,k){if(k>n){let S=new Set(ctx),j=F.findIndex(C=>C.every(l=>S.has(-l)));if(j<0)throw Error("SAT open leaf");nodes.push({kind:"leaf",ctx:ctx.slice(),source:j});return nodes.length-1;}
let pos=rec(ctx.concat(k),k+1),neg=rec(ctx.concat(-k),k+1);nodes.push({kind:"case",ctx:ctx.slice(),var:k,pos,neg});return nodes.length-1;}
return {source:F,nodes,root:rec([],1)};}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function validSource(F){return Array.isArray(F)&&F.length>0&&F.every(C=>Array.isArray(C)&&C.length===3&&C.every(l=>Number.isSafeInteger(l)&&l!==0)&&new Set(C.map(l=>Math.abs(l))).size===3);}
function verify(P,F){if(!validSource(F)||!eq(P.source,F)||!Array.isArray(P.nodes)||P.root!==P.nodes.length-1)return false;
function rec(id,ctx){if(!Number.isSafeInteger(id)||id<0||id>=P.nodes.length)return false;let n=P.nodes[id];if(!n||!eq(n.ctx,ctx))return false;
if(n.kind==="leaf")return Number.isSafeInteger(n.source)&&n.source>=0&&n.source<F.length&&F[n.source].every(l=>ctx.includes(-l));
if(n.kind!=="case"||!Number.isSafeInteger(n.var)||n.var<=0||ctx.some(l=>Math.abs(l)===n.var)||!Number.isSafeInteger(n.pos)||!Number.isSafeInteger(n.neg)||n.pos<0||n.neg<0||n.pos>=id||n.neg>=id||n.pos===n.neg)return false;
return rec(n.pos,ctx.concat(n.var))&&rec(n.neg,ctx.concat(-n.var));}
return rec(P.root,[]);}
let tests=[];
for(const v of [4,6,8]){let {F,n}=tseitin(v,true),G=tseitin(v,false).F;
chk(models(F,n)===0,"odd");chk(models(G,n)===2**(n-v+1),"even");
let P=proof(F,n);chk(verify(P,F),"valid");chk(!verify(P,G),"external source mismatch");
chk(P.nodes.length===2**(n+1)-1,"positions");chk(P.nodes.filter(x=>x.kind==="case").length===2**n-1,"case count");
let fail=false;try{proof(G,n);}catch(e){fail=e.message==="SAT open leaf";}chk(fail,"SAT witness uncovered");
let Q=JSON.parse(JSON.stringify(P));Q.nodes[0].source=F.length;chk(!verify(Q,F),"forged clause");
Q=JSON.parse(JSON.stringify(P));Q.nodes.at(-1).neg=Q.nodes.at(-1).pos;chk(!verify(Q,F),"omitted case");
Q=JSON.parse(JSON.stringify(P));Q.nodes.at(-1).pos=Q.root;chk(!verify(Q,F),"cycle");
Q=JSON.parse(JSON.stringify(P));Q.nodes.at(-1).ctx=[1];chk(!verify(Q,F),"undischarged context");
let malformed=JSON.parse(JSON.stringify(P));malformed.source[0][0]=0;
chk(!verify(malformed,malformed.source),"malformed zero");
malformed=JSON.parse(JSON.stringify(P));malformed.source[0][1]=malformed.source[0][0];
chk(!verify(malformed,malformed.source),"duplicate variable");
malformed=JSON.parse(JSON.stringify(P));malformed.root="999999999999999999999999999999";
chk(!verify(malformed,F),"huge noncanonical numeric ID");
let B=JSON.stringify(P).length*8; // all characters ASCII in this fixture
tests.push({vertices:v,variables:n,clauses:F.length,even_models:models(G,n),nodes:P.nodes.length,paid_cases:2**n-1,depth:n+1,evidence_bits:B});}
console.log(JSON.stringify({checks:count,tests,status:"restricted typed CASE/LEAF; no historical checker or FLMV implementation"},null,2));